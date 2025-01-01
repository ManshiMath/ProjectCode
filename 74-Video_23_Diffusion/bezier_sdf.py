import moderngl
import numpy as np

compute_shader_source = """
#version 430 core

layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;

layout(std140, binding = 0) buffer CurvePoints {
    vec2 curve_points[];    // 其实会对齐到 vec4
};

layout(std140, binding = 1) buffer InputBuffer {
    vec2 points[];      // 其实会对齐到 vec4
};

layout(std140, binding = 2) buffer OutputBuffer {
    vec3 results[];     // 其实会对齐到 vec4
};

vec3 solve_cubic(float a, float b, float c)
{
    float p = b - a * a / 3.0, p3 = p * p * p;
    float q = a * (2.0 * a * a - 9.0 * b) / 27.0 + c;
    float d = q * q + 4.0 * p3 / 27.0;
    float offset = -a / 3.0;
    if(d >= 0.0) {
        float z = sqrt(d);
        vec2 x = (vec2(z, -z) - q) / 2.0;
        vec2 uv = sign(x) * pow(abs(x), vec2(1.0 / 3.0));
        return vec3(offset + uv.x + uv.y);
    }
    float v = acos(-sqrt(-27.0 / p3) * q / 2.0) / 3.0;
    float m = cos(v), n = sin(v) * 1.732050808;
    return vec3(m + m, -n - m, n - m) * sqrt(-p / 3.0) + offset;
}

void distance_bezier(in vec2 A, in vec2 B, in vec2 C, in vec2 p, out float distance, out vec2 nearest)
{
    B = mix(B + vec2(1e-4), B, abs(sign(B * 2.0 - A - C)));
    vec2 a = B - A, b = A - B * 2.0 + C, c = a * 2.0, d = A - p;
    vec3 k = vec3(3. * dot(a, b),2. * dot(a, a) + dot(d, b),dot(d, a)) / dot(b, b);
    vec3 t = clamp(solve_cubic(k.x, k.y, k.z), 0.0, 1.0);

    vec2 pos = A + (c + b * t.x) * t.x;
    float dis = length(pos - p);
    nearest = pos;
    distance = dis;

    pos = A + (c + b * t.y) * t.y;
    dis = min(dis, length(pos - p));
    if (dis < distance) {
        nearest = pos;
        distance = dis;
    }

    pos = A + (c + b * t.z) * t.z;
    dis = min(dis, length(pos - p));
    if (dis < distance) {
        nearest = pos;
        distance = dis;
    }
}

const float INFINITY = uintBitsToFloat(0x7F800000);

void main() {
    uint index = gl_GlobalInvocationID.x;
    vec2 point = points[index];

    float dis = INFINITY;
    vec2 nearest;

    float part_dis;
    vec2 part_nearest;

    for (int i = 0; i < curve_points.length(); i += 3) {
        distance_bezier(
            curve_points[i],
            curve_points[i + 1],
            curve_points[i + 2],
            point,
            part_dis,
            part_nearest
        );
        if (part_dis < dis) {
            dis = part_dis;
            nearest = part_nearest;
        }
    }

    results[index] = vec3(dis, nearest);
}
"""


class BezierSDF:
    '''
    例子：

    ```
    curve_points = ...  #（曲线的点集，3维的）
    points = ...        #（待求点的点集，2维的）

    sdf = BezierSDF(curve_points[:, :2])    # 传入的是2维的点，所以每个点只取前两个分量
    result = sdf.compute(points)    # 传入2维的点，返回三维的 [(距离, x, y), ...]

    # 所以：
    result[:, 0]    # 最近距离
    result[:, 1:]   # 最近的点

    ```
    '''
    def __init__(self, curve_points):
        curve_points = np.array(curve_points)
        assert curve_points.ndim == 2
        assert curve_points.shape[1] == 2
        assert curve_points.shape[0] % 3 == 0

        self.ctx = moderngl.create_standalone_context(require=430)
        self.shader = self.ctx.compute_shader(compute_shader_source)

        self.curve_points_buffer = self.ctx.buffer(
            np.hstack([
                curve_points,
                np.zeros((len(curve_points), 2))
            ]).astype('f4').tobytes()
        )
        self.input_buffer = self.ctx.buffer(reserve=1)
        self.output_buffer = self.ctx.buffer(reserve=1)

    def compute(self, points) -> np.ndarray:
        '''
        返回值的是一个 `numpy` 的 `n * 3` 数组

        其中 `[:, 0]` 表示距离，`[:, 1:]` 表示最近的点

        例如，可能有这样的输出：

        ```
        [
            [1.9, 5.4, 3.4],
            [4.5, 1.2, 7.5],
            [0.1, 1.0, 3.7],
            [1.9, 5.4, 4.3]
        ]
        ```

        表示：

        - 第一个点离曲线最近距离是 `1.9`，最近的点是 `(5.4, 3.4)`
        - 第二个点离曲线最近距离是 `4.5`，最近的点是 `(1.2, 7.5)`
        '''
        points = np.array(points)
        assert points.ndim == 2
        assert points.shape[1] == 2

        bytes = np.hstack([
            points,
            np.zeros((len(points), 2))
        ]).astype('f4').tobytes()
        if len(bytes) != self.input_buffer.size:
            self.input_buffer.orphan(len(bytes))
        self.input_buffer.write(bytes)

        output_size = len(points) * 4 * 4
        if output_size != self.output_buffer.size:
            self.output_buffer.orphan(output_size)

        self.curve_points_buffer.bind_to_storage_buffer(0)
        self.input_buffer.bind_to_storage_buffer(1)
        self.output_buffer.bind_to_storage_buffer(2)

        self.shader.run(group_x=(len(points) + 255) // 256)     # 相当于 len(points) / 256 向上取整

        return np.frombuffer(self.output_buffer.read(), dtype='f4').reshape(-1, 4)[:, :3]
