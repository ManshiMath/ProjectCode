from __future__ import annotations

from manimlib import *
import numpy as np

class Test_1(FrameScene):
    def construct(self):
        # polynomial_1 = np.poly1d([1, 2, -3])
        # roots_1 = polynomial_1.roots
        # polynomial_2 = np.poly1d([1, 0, -1, 1])
        # roots_2 = polynomial_2.roots
        # polynomial_3 = np.poly1d([1, 0, -2, 1])
        # roots_3 = polynomial_3.roots
        # print(roots_1, roots_2, roots_3)
        # print(type(roots_2), type(roots_3), type(roots_2[0]), type(roots_3[0]), )

        # polynomial_4 = polynomial_3.deriv()
        # print(polynomial_4, polynomial_3)

        bezier_2 = [ORIGIN, 2*RIGHT + DOWN, 2*UR + 2*RIGHT]
        curve = VMobject().set_points(bezier_2)
        point = 2*DOWN + 2.5*RIGHT
        dot = Dot(point)
        def get_nearest(point: np.ndarray, b0: np.ndarray, b1: np.ndarray, b2: np.ndarray):
            poly_x = np.poly1d([b2[0] - 2*b1[0] + b0[0], -2*b2[0] + 2*b1[0], b2[0] - point[0]])
            poly_y = np.poly1d([b2[1] - 2*b1[1] + b0[1], -2*b2[1] + 2*b1[1], b2[1] - point[1]])
            def poly(t: float):
                return poly_x(t)**2 + poly_y(t)**2
            dpoly = poly_x*poly_x.deriv() + poly_y*poly_y.deriv()
            # roots = poly.roots
            # print(poly.roots)
            nearest, critical = poly(0), 0
            for root in dpoly.roots:
                if isinstance(root, complex):
                    if abs(root.imag) > 1e-6:
                        continue
                    root = root.real
                distance = poly(clip(root, 0, 1))
                if distance < nearest:
                    nearest, critical = distance, root
            return np.sqrt(nearest), critical
            # return poly.roots
        distance, critical = get_nearest(point, *bezier_2)
        circle = Circle(radius = distance).shift(point)
        self.add(curve, dot, circle)

class Test_2(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        tg[0].set_color(BLUE)
        #tg[1].set_color(GREEN)
        tg[-1].set_color(MAROON_A)
        self.play(DrawBorderThenFill(tg), run_time = 2)

        self.wait(1)
        name = Songti("漫士沉思录", color = YELLOW).scale(1.8).shift(DOWN*0.5)
        self.play(
            FadeOut(tg[1:-1]),
            tg[0].animate.shift(RIGHT * 3+UP*2),
            tg[-1].animate.shift(LEFT * 3+UP*1.8),
            DrawBorderThenFill(name),
            run_time = 2, lag_ratio = 0.7)
        self.wait(2)
        self.play(*[FadeOut(mob)for mob in self.mobjects])

class Test_3(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        points_M, points_S = M.get_points().reshape((-1, 3, 3)), S.get_points().reshape((-1, 3, 3))
        self.add(M, S)
        # print(points_M[2], points_S[-1])
        # print(M.get_bounding_box(), S.get_bounding_box(), VGroup(M, S).get_bounding_box())
        # self.add(*[Dot(point, radius = 0.02) for point in [*points_M, *points_S]])
        # print(points_M, points_S, points_M.shape, points_S.shape)

        dot_0 = DotCloud([UP]*1000, radius = 0.04, color = [BLUE if i%2 else MAROON_A for i in range(500)])
        alpha = ValueTracker(0.0)
        def brownian(p: np.ndarray):
            return (p + alpha.get_value()*np.random.randn(3) + 1.5 - UP) %3 - 1.5 + UP
        def random_updater(mob: Mobject):
            mob.apply_function(brownian)
        self.add(dot_0).wait()
        dot_0.add_updater(random_updater)
        self.play(alpha.animate.set_value(0.05), rate_func = bezier([0]*6 + [1]*2))
        self.wait(5)
        dot_0.clear_updaters()

        def get_nearest(point: np.ndarray, b0: np.ndarray, b1: np.ndarray, b2: np.ndarray):
            poly_x = np.poly1d([b2[0] - 2*b1[0] + b0[0], -2*b2[0] + 2*b1[0], b2[0] - point[0]])
            poly_y = np.poly1d([b2[1] - 2*b1[1] + b0[1], -2*b2[1] + 2*b1[1], b2[1] - point[1]])
            def poly(t: float):
                return poly_x(t)**2 + poly_y(t)**2
            dpoly = poly_x*poly_x.deriv() + poly_y*poly_y.deriv()
            nearest, critical = poly(0), 0
            for root in dpoly.roots:
                if isinstance(root, complex):
                    if abs(root.imag) > 1e-6:
                        continue
                    root = root.real
                distance = poly(clip(root, 0, 1))
                if distance < nearest:
                    nearest, critical = distance, root**2*b0 + 2*root*(1-root)*b1 + (1-root)**2*b2
            return (np.sqrt(nearest), critical)
        
        def multi_brownian(points: np.ndarray):

            def nudge(index: int, point: np.ndarray):
                nudged = brownian(point)
                if index % 2:
                    nearests = [get_nearest(nudged, *bezier_points) for bezier_points in points_M]
                else:
                    nearests = [get_nearest(nudged, *bezier_points) for bezier_points in points_S]
                critical = min(nearests, key = lambda t: t[0])
                ds = (critical[1] - nudged)*0.1
                return nudged + ds
            
            return [nudge(i, point) for i, point in enumerate(points)]
        
        def random_updater(mob: Mobject):
            # mob.apply_points_function(multi_brownian) # can't figure out how .apply_points_function() works
            mob.set_points(multi_brownian(mob.get_points()))
        dot_0.add_updater(random_updater)
        self.wait(1)

class Test_4(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        points_M, points_S = M.get_points().reshape((-1, 3, 3)), S.get_points().reshape((-1, 3, 3))
        def reduce_curves(points: np.ndarray):
            print(points)
            reduced_curves = []

            def has_angle(p_0: np.ndarray, p_1: np.ndarray, p_2: np.ndarray, p_3: np.ndarray) -> bool: # oriented align, so can't use homogeneous coordinates
                v_01, v_12 = normalize(p_1 - p_0), normalize(p_3 - p_2)
                return np.arccos(np.dot(v_01, v_12)) > 5*DEGREES
            
            curr_curve = points[0].copy()
            for i in range(1, len(points)):
                next_curve = points[i]
                
                if has_angle(curr_curve[1], curr_curve[2], next_curve[0], next_curve[1]) or get_norm(curr_curve[2] - next_curve[0]) > 1e-6:
                    reduced_curves.append(curr_curve)
                    curr_curve = next_curve.copy()
                    continue

                anchors = [curr_curve[0], curr_curve[1], curr_curve[2], next_curve[1], next_curve[2]]
                line_fore, line_back = cross(anchors[0] + OUT, anchors[1] + OUT), cross(anchors[3] + OUT, anchors[4] + OUT)
                new_point = cross(line_fore, line_back)
                new_handle = np.array([new_point[0], new_point[1], 0]) / new_point[2]
                if np.all([get_norm(new_handle - point) < 0.23 for point in [curr_curve[1], curr_curve[2], next_curve[0], next_curve[1]]]):
                    curr_curve = np.array([anchors[0], new_handle, anchors[4]])
                else:
                    reduced_curves.append(curr_curve)
                    curr_curve = next_curve.copy()

            reduced_curves.append(curr_curve)
            return np.array(reduced_curves)
        
        reduced_points_M, reduced_points_S = reduce_curves(points_M), reduce_curves(points_S)
        list_points_M, list_points_S = reduced_points_M.reshape((-1, 3)), reduced_points_S.reshape((-1, 3))
        reduced_M, reduced_S = M.copy().set_points(list_points_M), S.copy().set_points(list_points_S)
        print(points_M.shape, points_S.shape, reduced_points_M.shape, reduced_points_S.shape)
        self.add(reduced_M, reduced_S, *[Dot(point, radius = 0.02) for point in [*list_points_M, *list_points_S]])

class Test_4_0(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (4.0, 4.0)}, 
            }
    }
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        self.camera.frame.shift(0.85*UP)
        self.add(M, S)

class Test_5(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        points_M, points_S = M.get_points().reshape((-1, 3, 3)), S.get_points().reshape((-1, 3, 3))

        def reduce_curves(points: np.ndarray):
            reduced_curves = []
            reduced_degree = []

            def get_line(p_1: np.ndarray, p_2: np.ndarray) -> np.ndarray:
                    line = cross(p_1 + OUT, p_2 + OUT)
                    if get_norm(line) < 1e-6:
                        print("cioncide:", p_1, p_2)
                        return line
                    else:
                        return line / get_norm(line)
            
            def is_aligned(p_0: np.ndarray, p_1: np.ndarray, p_2: np.ndarray, p_3: np.ndarray) -> bool: # oriented align, so can't use homogeneous coordinates
                v_01, v_12 = normalize(p_1 - p_0), normalize(p_3 - p_2)
                return np.arccos(np.dot(v_01, v_12)) < 0.05
                
            def curve_degree(points: np.ndarray):
                return 1 if is_aligned(points[0], points[1], points[1], points[2]) else 2
                
            curr_curve = points[0].copy()
            n = len(points)
            for i in range(1, n):
                next_curve = points[i]

                if not is_aligned(curr_curve[1], curr_curve[2], next_curve[0], next_curve[1]) or get_norm(curr_curve[2] - next_curve[0]) > 0.01:
                    reduced_curves.append(curr_curve)
                    reduced_degree.append(curve_degree(curr_curve))
                    curr_curve = next_curve.copy()
                    continue
                
                # print(curr_curve, is_aligned(curr_curve[0], curr_curve[1], curr_curve[1], curr_curve[2]))
                # print(next_curve, is_aligned(next_curve[0], next_curve[1], next_curve[1], next_curve[2]))
                # never triggers
                if is_aligned(curr_curve[0], curr_curve[1], curr_curve[1], curr_curve[2]) and is_aligned(next_curve[0], next_curve[1], next_curve[1], next_curve[2]):
                    print("aligned curves:", curr_curve, next_curve)
                    curr_curve = np.array([curr_curve[0], (curr_curve[0] + next_curve[2])/2, next_curve[2]])
                else:
                    line_fore, line_back = get_line(curr_curve[0], curr_curve[1]), get_line(next_curve[1], next_curve[2])
                    if get_norm(line_back) < 1e-6:
                        extra = points[(i+1)%n]
                        print("also?")
                        line_back = get_line(extra[0], extra[1])
                        print("not?")
                    new_point = cross(line_fore, line_back)
                    new_handle = np.array([new_point[0], new_point[1], 0]) / new_point[2]
                    if np.all([get_norm(new_handle - point) < 0.2 for point in [curr_curve[1], curr_curve[2], next_curve[1]]]):
                        curr_curve = np.array([curr_curve[0], new_handle, next_curve[2]])
                    # small_curr = np.all([get_norm(curr_curve[i%3] - curr_curve[(i+1)%3]) < 0.1 for i in range(3)])
                    # small_next = np.all([get_norm(next_curve[i%3] - next_curve[(i+1)%3]) < 0.1 for i in range(3)])
                    # if small_curr or small_next:
                    #     line_fore, line_back = cross(curr_curve[0] + OUT, curr_curve[1] + OUT), cross(next_curve[1] + OUT, next_curve[2] + OUT)
                    #     new_point = cross(line_fore, line_back)
                    #     new_handle = np.array([new_point[0], new_point[1], 0]) / new_point[2]
                    #     curr_curve = np.array([curr_curve[0], new_handle, next_curve[2]])
                    else:
                        reduced_curves.append(curr_curve)
                        reduced_degree.append(curve_degree(curr_curve))
                        curr_curve = next_curve.copy()

            reduced_curves.append(curr_curve)
            reduced_degree.append(curve_degree(curr_curve))
            return np.array(reduced_curves), reduced_degree
        
        reduced_points_M, reduced_degrees_M, reduced_points_S, reduced_degrees_S = *reduce_curves(points_M), *reduce_curves(points_S)
        list_points_M, list_points_S = reduced_points_M.reshape((-1, 3)), reduced_points_S.reshape((-1, 3))
        reduced_M, reduced_S = M.copy().set_points(list_points_M), S.copy().set_points(list_points_S)
        # self.add(M, S)
        print(points_M.shape, points_S.shape, reduced_points_M.shape, reduced_points_S.shape, reduced_degrees_M, reduced_degrees_S)
        self.add(reduced_M, reduced_S, *[Dot(point, radius = 0.02) for point in [*list_points_M, *list_points_S]])


#################################################################### 

compute_shader_source_0 = """
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

float cross2d(vec2 a, vec2 b) {
    return a.x * b.y - a.y * b.x;
}

void distance_bezier(in vec2 A, in vec2 B, in vec2 C, in vec2 p, out float distance, out vec2 nearest)
{
    vec2 v1 = normalize(B - A), v2 = normalize(C - B);
    if (abs(cross2d(v1, v2)) < 1e-3 && dot(v1, v2) > 0.0) {
        vec2 e = C - A;
        vec2 w = p - A;
        vec2 offset = e * clamp(dot(w, e) / dot(e, e), 0.0, 1.0);
        vec2 b = w - offset;
        distance = length(b);
        nearest = A + offset;
        return;
    }

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
    (感谢网友@jkjkil-jiang提供的代码)
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
    def __init__(self, curve_points, ctx):
        curve_points = np.array(curve_points)
        assert curve_points.ndim == 2
        assert curve_points.shape[1] == 2
        assert curve_points.shape[0] % 3 == 0

        # self.ctx = moderngl.create_standalone_context(require=430)
        self.ctx = ctx
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

class Test_6(FrameScene):
    # CONFIG = {
    #     "camera_config": {"ctx": moderngl.create_standalone_context(require=430)},
    # }
    def construct(self):
        txt = MTex("A").scale(20)[0]
        self.add(txt)

        curve_points = txt.get_points()

        np.random.seed(114514)
        points_2d = np.random.rand(10, 2) * 6 - 3

        sdf = BezierSDF(np.array(curve_points)[:, :2], self.camera.ctx)
        result = sdf.compute(points_2d)

        extra_column = np.zeros((len(result), 1))
        result = np.hstack([result[:, 1:], extra_column])
        points = np.hstack([points_2d, extra_column])

        dots_1, dots_2 = DotCloud(points, color = BLUE, radius = 0.08), DotCloud(result, color = RED, radius = 0.08)
        lines = [Line(dot_1, dot_2) for dot_1, dot_2 in zip(points, result)]
        self.add(*lines, dots_1, dots_2)

#################################################################### 

compute_shader_source_1 = """
#version 430 core

layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;

layout(std140, binding = 0) buffer CurvePoints {
    vec2 curve_points[];    // 其实会对齐到 vec4
};

layout(std140, binding = 1) buffer InputBuffer {
    vec2 points[];      // 其实会对齐到 vec4
};

layout(std140, binding = 2) buffer OutputBuffer {
    vec4 results[];     // 其实会对齐到 vec4
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

float cross2d(vec2 a, vec2 b) {
    return a.x * b.y - a.y * b.x;
}

void distance_bezier(in vec2 A, in vec2 B, in vec2 C, in vec2 p, out float distance, out vec2 nearest)
{
    vec2 v1 = normalize(B - A), v2 = normalize(C - B);
    if (abs(cross2d(v1, v2)) < 1e-3 && dot(v1, v2) > 0.0) {
        vec2 e = C - A;
        vec2 w = p - A;
        vec2 offset = e * clamp(dot(w, e) / dot(e, e), 0.0, 1.0);
        vec2 b = w - offset;
        distance = length(b);
        nearest = A + offset;
        return;
    }

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

    results[index] = vec4(dis, nearest, 0);
}
"""

class BezierSDF2:
    '''
    (感谢网友@jkjkil-jiang提供的代码)
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
    def __init__(self, curve_points, ctx):
        curve_points = np.array(curve_points)
        assert curve_points.ndim == 2
        assert curve_points.shape[1] == 2
        assert curve_points.shape[0] % 3 == 0

        # self.ctx = moderngl.create_standalone_context(require=430)
        self.ctx = ctx
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

        result = np.frombuffer(self.output_buffer.read(), dtype='f4').reshape(-1, 4)
        # return result[:, 0], result[:, 1:]
        return result[:, 1:3]

class Test_7(FrameScene):
    def construct(self):
        txt = MTex("C").scale(20)[0]
        self.add(txt)

        curve_points = txt.get_points()

        np.random.seed(114514)
        points_2d = np.random.rand(100, 2) * 8 - 4

        sdf = BezierSDF2(np.array(curve_points)[:, :2], self.camera.ctx)
        result = sdf.compute(points_2d)
        # _, result = sdf.compute(points_2d)

        extra_column = np.zeros((len(result), 1))
        result = np.hstack([result[:, 1:], extra_column])
        points = np.hstack([points_2d, extra_column])

        dots_1, dots_2 = DotCloud(points, color = BLUE, radius = 0.08), DotCloud(result, color = RED, radius = 0.08)
        lines = [Line(dot_1, dot_2) for dot_1, dot_2 in zip(points, result)]
        self.add(*lines, dots_1, dots_2)

class Test_8(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        anchors_M, anchors_S = M.get_points()[:, :2], S.get_points()[:, :2]
        sdf_M, sdf_S = BezierSDF2(anchors_M, self.camera.ctx), BezierSDF2(anchors_S, self.camera.ctx)
        # self.add(M, S)

        n = 10000
        dot_0 = DotCloud([UP]*n, radius = 0.01, color = [MAROON_A if i%2 else BLUE for i in range(n)])
        alpha = ValueTracker(0.0)
        def brownian(p: np.ndarray):
            p[:2] += alpha.get_value()*np.random.randn(2)
            if get_norm(p) > 4:
                p *= 0.9
            return p
        def random_updater(mob: Mobject):
            mob.apply_function(brownian, about_point = UP)
        self.add(dot_0).wait()
        dot_0.add_updater(random_updater)
        self.play(alpha.animate.set_value(0.05), rate_func = bezier([0]*6 + [1]*2))
        self.wait(5)
        dot_0.clear_updaters()

        beta = ValueTracker(0.0)
        def multi_brownian(points: np.ndarray):

            points_M, points_S = points[::2, :2], points[1::2, :2]
            len_M, len_S = len(points_M), len(points_S)
            points_M += alpha.get_value()*np.random.randn(len_M, 2)
            points_S += alpha.get_value()*np.random.randn(len_S, 2)
            result_M, result_S = sdf_M.compute(points_M), sdf_S.compute(points_S)

            ratio = beta.get_value()
            points[::2, :2] = (1-ratio)*points_M + ratio*result_M
            points[1::2, :2] = (1-ratio)*points_S + ratio*result_S
            # return [nudge(i, point) for i, point in enumerate(points)]
        
        def random_updater(mob: Mobject):
            # mob.apply_points_function(multi_brownian) # can't figure out how .apply_points_function() works
            # mob.set_points(multi_brownian(mob.get_points()))
            multi_brownian(mob.get_points())
        dot_0.add_updater(random_updater)
        self.play(beta.animate.set_value(0.8), run_time = 10, rate_func = linear)
        self.wait(5)

#################################################################### 
        
class ParallelClip:

    def __init__(self, code, ctx):
        # curve_points = np.array(curve_points)
        # assert curve_points.ndim == 2
        # assert curve_points.shape[1] == 2
        # assert curve_points.shape[0] % 3 == 0

        # self.ctx = moderngl.create_standalone_context(require=430)
        self.ctx = ctx
        self.shader = self.ctx.compute_shader(code)

        # self.curve_points_buffer = self.ctx.buffer(
        #     np.hstack([
        #         curve_points,
        #         np.zeros((len(curve_points), 2))
        #     ]).astype('f4').tobytes()
        # )
        self.input_buffer = self.ctx.buffer(reserve=1)
        self.output_buffer = self.ctx.buffer(reserve=1)

    def compute(self, points) -> np.ndarray:
        points = np.array(points)
        assert points.ndim == 2
        assert points.shape[1] == 2

        bytes = np.hstack([
            points,
        ]).astype('f4').tobytes()
        if len(bytes) != self.input_buffer.size:
            self.input_buffer.orphan(len(bytes))
        self.input_buffer.write(bytes)

        output_size = len(points) * 4 * 4
        if output_size != self.output_buffer.size:
            self.output_buffer.orphan(output_size)

        # self.curve_points_buffer.bind_to_storage_buffer(0)
        self.input_buffer.bind_to_storage_buffer(0)
        self.output_buffer.bind_to_storage_buffer(1)

        self.shader.run(group_x=(len(points) + 255) // 256)     # 相当于 len(points) / 256 向上取整

        result = np.frombuffer(self.output_buffer.read(), dtype='f4').reshape(-1, 4)
        return result[:, :2] # [:, 1:3]

class Test_9(FrameScene):
    def construct(self):
        compute_shader_code = """
            #version 430 core

            layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;

            layout(std430, binding = 0) buffer InputBuffer {
                vec2 points[];
            };

            layout(std430, binding = 1) buffer OutputBuffer {
                vec4 results[];
            };

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index];
                float dis = length(point);
                if (dis >= 1){
                    float factor = 0.5*1 + 0.5*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point, 0.0, 0.0);
            }
            """
        computer = ParallelClip(compute_shader_code, self.camera.ctx)

        n = 20
        dot_0 = DotCloud([UP]*n, radius = 0.08, color = color_gradient([RED, YELLOW, GREEN, BLUE], 20))
        alpha = ValueTracker(0.0)
        threshold = Circle(radius = 1, color = GREY)

        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            result = computer.compute(points_2d)
            print("points: ", points, "2d: ", points_2d, "result: ", result)
            points[:, :2] = result
            # ratio = beta.get_value()
            # points[::2, :2] = (1-ratio)*points_M + ratio*result_M
            # points[1::2, :2] = (1-ratio)*points_S + ratio*result_S
            # return [nudge(i, point) for i, point in enumerate(points)]
        
        def random_updater(mob: Mobject):
            multi_brownian(mob.get_points())
        self.add(threshold, dot_0).wait()
        dot_0.add_updater(random_updater)
        self.play(alpha.animate.set_value(0.05), rate_func = bezier([0]*6 + [1]*2))
        self.wait(5)
        dot_0.clear_updaters()

class ParallelClip2:

    def __init__(self, code, ctx, **kwargs):

        self.ctx = ctx
        self.shader = self.ctx.compute_shader(code)
        for key, value in kwargs.items():
            self.shader[key] = value
        self.input_buffer = self.ctx.buffer(reserve=1)
        self.output_buffer = self.ctx.buffer(reserve=1)

    def compute(self, points) -> np.ndarray:
        points = np.array(points)
        assert points.ndim == 2
        assert points.shape[1] == 2

        bytes = np.hstack([
            points,
        ]).astype('f4').tobytes()
        if len(bytes) != self.input_buffer.size:
            self.input_buffer.orphan(len(bytes))
        self.input_buffer.write(bytes)

        output_size = len(points) * 4 * 4
        if output_size != self.output_buffer.size:
            self.output_buffer.orphan(output_size)

        self.input_buffer.bind_to_storage_buffer(0)
        self.output_buffer.bind_to_storage_buffer(1)

        self.shader.run(group_x=(len(points) + 255) // 256)     # 相当于 len(points) / 256 向上取整

        result = np.frombuffer(self.output_buffer.read(), dtype='f4').reshape(-1, 4)
        return result[:, :2] # [:, 1:3]

class Test_10(FrameScene):
    def construct(self):
        compute_shader_code = """
            #version 430 core

            layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;

            layout(std430, binding = 0) buffer InputBuffer {
                vec2 points[];
            };

            layout(std430, binding = 1) buffer OutputBuffer {
                vec4 results[];
            };

            uniform vec2 center;

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index] - center;
                float dis = length(point);
                if (dis >= 1){
                    float factor = 0.5*1 + 0.5*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point + center, 0.0, 0.0);
            }
            """
        computer = ParallelClip2(compute_shader_code, self.camera.ctx, center = (0, 1))

        n = 20
        dot_0 = DotCloud([UP]*n, radius = 0.08, color = color_gradient([RED, YELLOW, GREEN, BLUE], 20))
        alpha = ValueTracker(0.0)
        threshold = Circle(radius = 1, color = GREY).shift(UP)

        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            result = computer.compute(points_2d)
            points[:, :2] = result
            # ratio = beta.get_value()
            # points[::2, :2] = (1-ratio)*points_M + ratio*result_M
            # points[1::2, :2] = (1-ratio)*points_S + ratio*result_S
            # return [nudge(i, point) for i, point in enumerate(points)]
        
        def random_updater(mob: Mobject):
            multi_brownian(mob.get_points())
        self.add(threshold, dot_0).wait()
        dot_0.add_updater(random_updater)
        self.play(alpha.animate.set_value(0.05), rate_func = bezier([0]*6 + [1]*2))
        self.wait(5)
        dot_0.clear_updaters()
        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        