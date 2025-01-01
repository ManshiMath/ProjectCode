import time

import moderngl
import numpy as np


class TimeIt:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        print(f'{self.name} 耗时 {time.time() - self.time:.2f}s')


with TimeIt('生成'):
    np.random.seed(114514)
    points = (np.random.rand(10240000, 2)).astype(np.float32)

with TimeIt('创建'):
    ctx = moderngl.create_standalone_context()

    compute_shader_source = """
    #version 430 core

    layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;

    layout(std430, binding = 0) buffer InputBuffer {
        vec2 points[];
    };

    layout(std430, binding = 1) buffer OutputBuffer {
        float results[];
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

    float distance_bezier(vec2 A, vec2 B, vec2 C, vec2 p)
    {
        B = mix(B + vec2(1e-4), B, abs(sign(B * 2.0 - A - C)));
        vec2 a = B - A, b = A - B * 2.0 + C, c = a * 2.0, d = A - p;
        vec3 k = vec3(3. * dot(a, b),2. * dot(a, a) + dot(d, b),dot(d, a)) / dot(b, b);
        vec3 t = clamp(solve_cubic(k.x, k.y, k.z), 0.0, 1.0);
        vec2 pos = A + (c + b * t.x) * t.x;
        float dis = length(pos - p);
        pos = A + (c + b * t.y) * t.y;
        dis = min(dis, length(pos - p));
        pos = A + (c + b * t.z) * t.z;
        dis = min(dis, length(pos - p));
        return dis;
    }

    const vec2 A = vec2(-1.4, 5.3);
    const vec2 B = vec2(4.2, -2.2);
    const vec2 C = vec2(3.1, 3.1);

    void main() {
        uint index = gl_GlobalInvocationID.x;
        vec2 point = points[index];

        results[index] = distance_bezier(A, B, C, point);
    }
    """

    compute_shader = ctx.compute_shader(compute_shader_source)

    input_buffer = ctx.buffer(points.tobytes())
    output_buffer = ctx.buffer(reserve=len(points) * 4)     # 4字节浮点数

    input_buffer.bind_to_storage_buffer(0)
    output_buffer.bind_to_storage_buffer(1)

with TimeIt('执行'):
    compute_shader.run(group_x=len(points) // 256)

with TimeIt('获取'):
    result = np.frombuffer(output_buffer.read(), dtype=np.float32)

print(result)
print(len(result))
