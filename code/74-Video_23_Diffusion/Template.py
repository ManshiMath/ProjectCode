from __future__ import annotations

from manimlib import *
import numpy as np

class Diffuse:

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

        bytes = points.astype('f4').tobytes()
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

uniform float surr;
uniform float ratio;

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
    
    vec2 direction = nearest - point;
    if (dis >= surr){
        float factor = ratio*(dis - surr);
        point += direction*factor/dis;
    }
    results[index] = vec3(point, 0.0);
}
"""

class BezierDiffuse:

    def __init__(self, code, curve_points, ctx, **kwargs):
        curve_points = np.array(curve_points)
        assert curve_points.ndim == 2
        assert curve_points.shape[1] == 2
        assert curve_points.shape[0] % 3 == 0

        # self.ctx = moderngl.create_standalone_context(require=430)
        self.ctx = ctx
        self.shader = self.ctx.compute_shader(code)
        for key, value in kwargs.items():
            self.shader[key] = value
        
        self.curve_points_buffer = self.ctx.buffer(
            np.hstack([
                curve_points,
                np.zeros((len(curve_points), 2))
            ]).astype('f4').tobytes()
        )
        self.input_buffer = self.ctx.buffer(reserve=1)
        self.output_buffer = self.ctx.buffer(reserve=1)

    def compute(self, points, **kwargs) -> np.ndarray:

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

        for key, value in kwargs.items():
            self.shader[key] = value

        self.shader.run(group_x=(len(points) + 255) // 256)     # 相当于 len(points) / 256 向上取整

        result = np.frombuffer(self.output_buffer.read(), dtype='f4').reshape(-1, 4)
        # return result[:, 0], result[:, 1:]
        return result[:, :2]
    
class Video_1(FrameScene):
    def construct(self):
        colors = list(np.random.choice(MANIM_COLORS, size=100))
        dot_0 = DotCloud([ORIGIN]*100, radius = 0.01, color = colors)

        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.1*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        add_more_dots = True
        def random_updater(mob: Mobject):
            multi_brownian(mob.get_points())
            if add_more_dots:
                mob.append_points([ORIGIN]*100)
                colors.extend(list(np.random.choice(MANIM_COLORS, size=100)))
                mob.set_color(colors)
        self.add(dot_0)# .wait()
        dot_0.add_updater(random_updater)
        self.wait(5)
        add_more_dots = False
        self.wait(15)
    
class Test1(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        anchors_M, anchors_S = M.get_points()[:, :2], S.get_points()[:, :2]
        sdf_M, sdf_S = BezierDiffuse(compute_shader_source, anchors_M, self.camera.ctx), BezierDiffuse(compute_shader_source, anchors_S, self.camera.ctx)
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

class Test2(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        anchors_M, anchors_S = M.get_points()[:, :2], S.get_points()[:, :2]
        sdf_M, sdf_S = BezierDiffuse(compute_shader_source, anchors_M, self.camera.ctx, surr = 0.1, ratio = 0.5), BezierDiffuse(compute_shader_source, anchors_S, self.camera.ctx, surr = 0.1, ratio = 0.5)
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

        def multi_brownian(points: np.ndarray):

            points_M, points_S = points[::2, :2], points[1::2, :2]
            len_M, len_S = len(points_M), len(points_S)
            points_M += alpha.get_value()*np.random.randn(len_M, 2)
            points_S += alpha.get_value()*np.random.randn(len_S, 2)

            points[::2, :2] = sdf_M.compute(points_M)
            points[1::2, :2] = sdf_S.compute(points_S)
        
        def random_updater(mob: Mobject):
            multi_brownian(mob.get_points())
        dot_0.add_updater(random_updater)
        # self.play(beta.animate.set_value(0.8), run_time = 10, rate_func = linear)
        self.wait(15)

class ShowIncreasingPoints(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
        "int_func": np.round,
    }

    def __init__(self, dotcloud: DotCloud, **kwargs):
        self.all_points = list(dotcloud.get_points())
        self.all_rgbas = list(dotcloud.data["rgbas"])
        # print(self.all_points)
        super().__init__(dotcloud, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        n_submobs = len(self.all_points)
        index = int(self.int_func(alpha * (n_submobs-1)) + 1) #if there's no point at beginning, the rendering will be skipped
        self.update_point_list(index)

    def update_point_list(self, index: int) -> None:
        self.mobject.set_points(self.all_points[:index])
        self.mobject.data["rgbas"] = np.array(self.all_rgbas[:index])

class Video_2(FrameScene):
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
            uniform float radius;
            uniform float ratio;

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index] - center;
                float dis = length(point);
                if (dis >= radius){
                    float factor = (1-ratio)*radius + ratio*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point + center, 0.0, 0.0);
            }
            """
        computer_0 = Diffuse(compute_shader_code, self.camera.ctx, center = (-4, 0), radius = 0.5, ratio = 0.8)
        computer_1 = Diffuse(compute_shader_code, self.camera.ctx, center = (0, 0), radius = 0.5, ratio = 0.8)
        computer_2 = Diffuse(compute_shader_code, self.camera.ctx, center = (4, 0), radius = 0.5, ratio = 0.8)

        dot_0 = DotCloud([4*LEFT]*5000, radius = 0.02, color = RED_A)
        dot_0.computer = computer_0
        dot_1 = DotCloud([ORIGIN]*5000, radius = 0.02, color = YELLOW)
        dot_1.computer = computer_1
        dot_2 = DotCloud([4*RIGHT]*5000, radius = 0.02, color = GREEN)
        dot_2.computer = computer_2

        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.5*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        def random_updater(mob: Mobject):
            simple_diffusion(mob.get_points(), computer = mob.computer)

        self.add(dot_0, dot_1, dot_2)# .wait()
        for mob in [dot_0, dot_1, dot_2]:
            mob.add_updater(random_updater)
        self.wait()
        for mob in [dot_0, dot_1, dot_2]:
            mob.clear_updaters()

        anchors_1 = Line(DL, UR).get_points()[:, :2]
        anchors_2 = SVGMobject("smile_face.svg").move_to(4*RIGHT).get_all_points()[:, :2]
        dot_0.computer = Diffuse(compute_shader_code, self.camera.ctx, center = (-4, 0), radius = 0.1, ratio = 0.1)
        dot_1.computer = BezierDiffuse(compute_shader_source, anchors_1, self.camera.ctx, surr = 0.1, ratio = 0.9)
        dot_2.computer = BezierDiffuse(compute_shader_source, anchors_2, self.camera.ctx, surr = 0.1, ratio = 0.9)
        
        def potential(points: np.ndarray, computer: Diffuse | BezierDiffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.05*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        
        def random_updater(mob: Mobject):
            potential(mob.get_points(), computer = mob.computer)
        for mob in [dot_0, dot_1, dot_2]:
            mob.add_updater(random_updater)
        self.wait(5)
        # self.wait(15)
        for mob in [dot_0, dot_1, dot_2]:
            mob.clear_updaters()

        # self.remove(dot_0, dot_1, dot_2)
        # self.wait()
        # print("start: ", dot_0.get_points())
        # self.play(*[ShowIncreasingPoints(mob) for mob in [dot_0, dot_1, dot_2]], run_time = 3)
        # print("end: ", dot_0.get_points())
        # self.wait()

        dot_0.computer = Diffuse(compute_shader_code, self.camera.ctx, center = (-4, 0), radius = 2, ratio = 0.995)
        dot_1.computer = Diffuse(compute_shader_code, self.camera.ctx, center = (0, 0), radius = 2, ratio = 0.995)
        dot_2.computer = Diffuse(compute_shader_code, self.camera.ctx, center = (4, 0), radius = 2, ratio = 0.995)
        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.05*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        def random_updater(mob: Mobject):
            simple_diffusion(mob.get_points(), computer = mob.computer)

        self.add(dot_0, dot_1, dot_2)# .wait()
        for mob in [dot_0, dot_1, dot_2]:
            mob.add_updater(random_updater)
        self.wait()
        self.wait(15)
        for mob in [dot_0, dot_1, dot_2]:
            mob.clear_updaters()

#################################################################### 
            
class Shot(Mobject):
    CONFIG = {
        "height": 2,
        "opacity": 1,
        "shader_folder": "image",
        "shader_dtype": [
            ('point', np.float32, (3,)),
            ('im_coords', np.float32, (2,)),
            ('opacity', np.float32, (1,)),
        ],
        "frame_shape": (270, 270)
    }
    def __init__(self, name: str, frame: CameraFrame, **kwargs):
        self.texture_paths = {"Texture": name}
        self.name = name
        self.frame = frame
        super().__init__(**kwargs)
        
    def init_points(self) -> None:
        self.set_width(2, stretch=True)
        self.set_height(self.height)

    def init_data(self) -> None:
        self.data = {
            "points": np.array([UL, DL, UR, DR]),
            "im_coords": np.array([(0, 0), (0, 1), (1, 0), (1, 1)]),
            "opacity": np.array([[self.opacity]], dtype=np.float32),
        }

    def set_opacity(self, opacity: float, recurse: bool = True):
        for mob in self.get_family(recurse):
            mob.data["opacity"] = np.array([[o] for o in listify(opacity)])
        return self

    def set_color(self, color, opacity=None, recurse=None):
        return self

    def get_shader_data(self) -> np.ndarray:
        shader_data = super().get_shader_data()
        self.read_data_to_shader(shader_data, "im_coords", "im_coords")
        self.read_data_to_shader(shader_data, "opacity", "opacity")
        return shader_data

class Test3(FrameScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shots: list[Shot] = []
        self.frame = self.camera.frame

    def add_shot(self, *shots: Shot):
        self.shots.extend(shots)
        for shot in shots:
            name = shot.name
            if self.camera.n_textures == 15:  # I have no clue why this is needed
                self.camera.n_textures += 1
            tid = self.camera.n_textures
            self.camera.n_textures += 1
            
            im = self.camera.get_image()
            texture = self.camera.ctx.texture(
                    size=im.size,
                    components=len(im.getbands()),
                    data=im.tobytes(),
                )
            texture.use(location=tid)
            self.camera.path_to_texture[name] = (tid, texture)
    
    def refresh(self):
        for shot in self.shots:
            self.camera.frame = shot.frame
            super().refresh()
            self.camera.path_to_texture[shot.name][1].write(data=self.camera.get_image().tobytes())
        self.camera.frame = self.frame
        super().refresh()

    def construct(self):
        testboard = Testboard()
        frame_1 = CameraFrame(frame_shape = (1, 1), center_point = 2*RIGHT)
        
        self.add(testboard).wait()
        
        shot_1 = Shot("shot_1", frame_1).shift(2*LEFT)
        self.add_shot(shot_1)
        self.add(shot_1).wait()

class Test4(FrameScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shots: list[Shot] = []
        self.frame = self.camera.frame
        self.fbo = self.camera.fbo
        self.fbo_msaa = self.camera.fbo_msaa
        self.frame_shape = self.camera.pixel_width, self.camera.pixel_height

    def add_shot(self, *shots: Shot):
        self.shots.extend(shots)
        for shot in shots:
            name = shot.name
            if self.camera.n_textures == 15:  # I have no clue why this is needed
                self.camera.n_textures += 1
            tid = self.camera.n_textures
            self.camera.n_textures += 1

            self.camera.pixel_width, self.camera.pixel_height = shot.frame_shape
            shot.fbo = self.camera.get_fbo(self.camera.ctx, 0)
            shot.fbo_msaa = self.camera.get_fbo(self.camera.ctx, self.camera.samples)
            self.camera.fbo = shot.fbo
            self.camera.fbo_msaa = shot.fbo_msaa
            
            im = self.camera.get_image()
            texture = self.camera.ctx.texture(
                    size=im.size,
                    components=len(im.getbands()),
                    data=im.tobytes(),
                )
            texture.use(location=tid)
            self.camera.path_to_texture[name] = (tid, texture)
        self.camera.pixel_width, self.camera.pixel_height = self.frame_shape
        self.camera.fbo = self.fbo
        self.camera.fbo_msaa = self.fbo_msaa
    
    def refresh(self):
        for shot in self.shots:
            self.camera.frame = shot.frame
            self.camera.fbo = shot.fbo
            self.camera.fbo_msaa = shot.fbo_msaa
            self.camera.fbo_msaa.use()
            super().refresh()
            im = self.camera.get_image()
            self.camera.path_to_texture[shot.name][1].write(data=im.tobytes())
        self.camera.frame = self.frame
        self.camera.fbo = self.fbo
        self.camera.fbo_msaa = self.fbo_msaa
        self.camera.fbo_msaa.use()
        super().refresh()

    def construct(self):
        testboard = Testboard()
        frame_1 = CameraFrame(frame_shape = (1, 1), center_point = 2*RIGHT)
        
        self.add(testboard).wait()

        shot_1 = Shot("shot_1", frame_1).shift(2*LEFT)
        surr_1 = Square(side_length = 1.2, color = YELLOW).shift(2*RIGHT)
        self.add_shot(shot_1)
        self.add(shot_1, surr_1).wait()
        self.play(testboard.animate.shift(RIGHT))
        self.play(testboard.animate.shift(UP))
        self.play(testboard.animate.shift(DL))
        self.wait()

class ShotScene(FrameScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shots: list[Shot] = []
        self.frame = self.camera.frame
        self.fbo = self.camera.fbo
        self.fbo_msaa = self.camera.fbo_msaa
        self.frame_shape = self.camera.pixel_width, self.camera.pixel_height

    def add_shot(self, *shots: Shot):
        self.shots.extend(shots)
        for shot in shots:
            name = shot.name
            if self.camera.n_textures == 15:  # I have no clue why this is needed
                self.camera.n_textures += 1
            tid = self.camera.n_textures
            self.camera.n_textures += 1

            self.camera.pixel_width, self.camera.pixel_height = shot.frame_shape
            shot.fbo = self.camera.get_fbo(self.camera.ctx, 0)
            shot.fbo_msaa = self.camera.get_fbo(self.camera.ctx, self.camera.samples)
            self.camera.fbo = shot.fbo
            self.camera.fbo_msaa = shot.fbo_msaa
            
            im = self.camera.get_image()
            texture = self.camera.ctx.texture(
                    size=im.size,
                    components=len(im.getbands()),
                    data=im.tobytes(),
                )
            texture.use(location=tid)
            self.camera.path_to_texture[name] = (tid, texture)
        self.camera.pixel_width, self.camera.pixel_height = self.frame_shape
        self.camera.fbo = self.fbo
        self.camera.fbo_msaa = self.fbo_msaa
    
    def refresh(self):
        for shot in self.shots:
            self.camera.frame = shot.frame
            self.camera.fbo = shot.fbo
            self.camera.fbo_msaa = shot.fbo_msaa
            self.camera.fbo_msaa.use()
            super().refresh()
            im = self.camera.get_image()
            self.camera.path_to_texture[shot.name][1].write(data=im.tobytes())
        self.camera.frame = self.frame
        self.camera.fbo = self.fbo
        self.camera.fbo_msaa = self.fbo_msaa
        self.camera.fbo_msaa.use()
        super().refresh()

class Test5(ShotScene):
    def construct(self):
        testboard = Testboard()
        frame_1 = CameraFrame(frame_shape = (1, 1), center_point = 2*RIGHT)
        
        self.add(testboard).wait()

        shot_1 = Shot("shot_1", frame_1).shift(2*LEFT)
        surr_1 = Square(side_length = 1.2, color = YELLOW).shift(2*RIGHT)
        self.add_shot(shot_1)
        self.add(shot_1, surr_1).wait()
        self.play(testboard.animate.shift(RIGHT))
        self.play(testboard.animate.shift(UP))
        self.play(testboard.animate.shift(DL))
        self.wait()

class Video_3(ShotScene):
    def refresh(self):
        for shot in self.shots:
            self.camera.frame = shot.frame
            self.camera.fbo = shot.fbo
            # self.camera.fbo.use()
            self.camera.fbo_msaa = shot.fbo_msaa
            self.camera.fbo_msaa.use()
            self.camera.clear()
            self.camera.capture(self.dot) # I don't know why it can't work
            im = self.camera.get_image()
            self.camera.path_to_texture[shot.name][1].write(data=im.tobytes())
        self.camera.frame = self.frame
        self.camera.fbo = self.fbo
        self.camera.fbo_msaa = self.fbo_msaa
        self.camera.fbo_msaa.use()
        self.camera.clear()
        self.camera.capture(*self.get_all_mobjects())

    def construct(self):
        colors = list(np.random.choice(MANIM_COLORS, size=3000))
        dot_0 = DotCloud([ORIGIN]*20000, radius = 0.02, color = colors)
        self.dot = dot_0

        alpha = ValueTracker(0.1)
        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        def random_updater(mob: Mobject):
            multi_brownian(mob.get_points())
        self.add(dot_0)# .wait()
        dot_0.add_updater(random_updater)
        self.wait(2)
        self.play(alpha.animate.set_value(0.00), rate_func = less_smooth)
        dot_0.clear_updaters()
        self.wait()

        center = 2*LEFT
        height = 0.2
        frame_1 = CameraFrame(frame_shape = (height, height), center_point = center)
        surr_0 = Square(side_length = height + 0.02, stroke_width = 2).shift(center)
        dot_0.generate_target()
        dot_0.target.set_color([RED if abs(p[0] - center[0])<height/2 and abs(p[1] - center[1])<height/2 else GREY_E for p in dot_0.target.get_points()])
        self.play(MoveToTarget(dot_0), ShowCreation(surr_0))
        self.wait()

        shot_1 = Shot("shot_1", frame_1, height = height).shift(center)
        surr_1 = Square(side_length = height + 0.02, stroke_width = 2).shift(center)
        self.add_shot(shot_1)
        self.add(shot_1, surr_1).play(self.camera.frame.animate.shift(2*LEFT), shot_1.animate.move_to(5*LEFT).set_height(2), 
                                      surr_1.animate.move_to(5*LEFT).set_height(2.2).set_stroke(width = 2))
        self.wait()
        lines = []
        for i, p in enumerate(dot_0.get_points()):
            if abs(p[0] - center[0])<height/2 and abs(p[1] - center[1])<height/2:
                lines.append(TracedPath(lambda idx = i: dot_0.get_points()[idx], stroke_width = 1, stroke_color = RED_A))
        dot_0.add_updater(random_updater)
        self.add(*lines, surr_0).play(alpha.animate.set_value(0.03))
        self.wait(5)
        # self.wait(15)

class Video_4(ShotScene):
    def refresh(self):
        for shot in self.shots:
            self.camera.frame = shot.frame
            self.camera.fbo = shot.fbo
            # self.camera.fbo.use()
            self.camera.fbo_msaa = shot.fbo_msaa
            self.camera.fbo_msaa.use()
            self.camera.clear()
            self.camera.capture(self.dot) # I don't know why it can't work
            im = self.camera.get_image()
            self.camera.path_to_texture[shot.name][1].write(data=im.tobytes())
        self.camera.frame = self.frame
        self.camera.fbo = self.fbo
        self.camera.fbo_msaa = self.fbo_msaa
        self.camera.fbo_msaa.use()
        self.camera.clear()
        self.camera.capture(*self.get_all_mobjects())

    def construct(self):
        colors = list(np.random.choice(MANIM_COLORS, size=3000))
        dot_0 = DotCloud([ORIGIN]*20000, radius = 0.02, color = colors)
        history = []
        self.dot = dot_0

        alpha = ValueTracker(0.1)
        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        def random_updater(mob: Mobject):
            history.append(mob.get_points().copy())
            multi_brownian(mob.get_points())
            
        self.add(dot_0)# .wait()
        dot_0.add_updater(random_updater)
        self.wait(2)
        self.play(alpha.animate.set_value(0.00), rate_func = less_smooth)
        dot_0.clear_updaters()
        self.wait()

        center = 2*LEFT
        height = 0.2
        frame_1 = CameraFrame(frame_shape = (height, height), center_point = center)
        surr_0 = Square(side_length = height + 0.02, stroke_width = 2).shift(center)
        dot_0.generate_target()
        colors = [RED if abs(p[0] - center[0])<height/2 and abs(p[1] - center[1])<height/2 else GREY_E for p in dot_0.target.get_points()]
        opacities = [1 if abs(p[0] - center[0])<height/2 and abs(p[1] - center[1])<height/2 else 0.2 for p in dot_0.target.get_points()]
        dot_0.target.set_color(colors)
        self.play(MoveToTarget(dot_0), ShowCreation(surr_0))
        self.wait()

        shot_1 = Shot("shot_1", frame_1, height = height).shift(center)
        surr_1 = Square(side_length = height + 0.02, stroke_width = 2).shift(center)
        self.add_shot(shot_1)
        self.add(shot_1, surr_1).play(self.camera.frame.animate.shift(2*LEFT), shot_1.animate.move_to(5*LEFT).set_height(2), 
                                      surr_1.animate.move_to(5*LEFT).set_height(2.2).set_stroke(width = 4))
        self.wait()
        lines = []
        indices = []
        for i, p in enumerate(dot_0.get_points()):
            if abs(p[0] - center[0])<height/2 and abs(p[1] - center[1])<height/2:
                indices.append(i)
                lines.append(TracedPath(lambda idx = i: dot_0.get_points()[idx], stroke_width = 0.5, stroke_color = RED_A))
        future = []
        special = []
        def reverse_updater(mob: Mobject):
            try:
                points = history.pop()
                future.append(points)
                special.append([points[i] for i in indices])
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
            
        dot_0.add_updater(reverse_updater)
        self.add(*lines, surr_0).wait(4)
        for line in lines:
            line.clear_updaters()
        self.play(self.camera.frame.animate.set_height(4).shift(RIGHT))
        self.wait()

        def inverse_updater(mob: Mobject):
            try:
                points = future.pop()
                history.append(points)
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
        dot_1 = DotCloud([ORIGIN]*len(special), radius = 0.03, color = RED)
        def special_updater(mob: Mobject):
            try:
                points = special.pop()
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
        arrow = Arrow(ORIGIN, center)
        dot_0.set_opacity(opacities).add_updater(inverse_updater)
        dot_1.add_updater(special_updater)
        self.add(dot_1, surr_0, arrow).play(GrowArrow(arrow, run_time = 3))
        self.wait()
        # self.wait(5)
        # self.wait(15)

#################################################################### 

class Video_5(FrameScene):
    def construct(self):
        colors = list(np.random.choice(MANIM_COLORS, size=5000))
        dot_0 = DotCloud([ORIGIN]*5000, radius = 0.02, color = colors)
        history = []
        self.dot = dot_0

        alpha = ValueTracker(0.1)
        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        def random_updater(mob: Mobject):
            history.append(mob.get_points().copy())
            multi_brownian(mob.get_points())
            
        self.add(dot_0)# .wait()
        dot_0.add_updater(random_updater)
        self.wait(5)
        self.play(alpha.animate.set_value(0.00), rate_func = less_smooth)
        dot_0.clear_updaters()
        self.wait()

        center = 2*LEFT
        height = 0.2
        surr_0 = Square(side_length = height + 0.02, stroke_width = 2).shift(center)
        dot_0.save_state().generate_target()
        colors = [RED if abs(p[0] - center[0])<height/2 and abs(p[1] - center[1])<height/2 else GREY for p in dot_0.target.get_points()]
        opacities = [1 if abs(p[0] - center[0])<height/2 and abs(p[1] - center[1])<height/2 else 0.8 for p in dot_0.target.get_points()]
        dot_0.target.set_color(colors).set_opacity(opacities)
        self.play(MoveToTarget(dot_0), ShowCreation(surr_0))
        self.wait()

        arrow = Arrow(2*LEFT, (1-1/5)*2*LEFT, buff = 0)
        self.play(GrowArrow(arrow))
        self.wait()
        n = 1
        arrows = [Arrow((i*RIGHT + j*UP)/n, (1-1/5)*(i*RIGHT + j*UP)/n, buff = 0, color = GREY_D) for i in range(-8*n, 8*n+1) for j in range(-4*n, 4*n+1)]
        index = (8*n+1)*6*n + 4*n
        self.add_background(*arrows).play(*[FadeOut(mob, delay = 1) for mob in [surr_0, arrow]], dot_0.animate.restore(), LaggedStart(*[GrowArrow(mob) for mob in arrows], lag_ratio = 0.05, run_time = 2, group = VGroup(), remover = True))
        self.wait()
        for arrow in arrows:
            arrow.generate_target()
            norm = get_norm(arrow.get_end() - arrow.get_start())
            if norm > 0.1:
                arrow.target.put_start_and_end_on(arrow.get_start(), arrow.get_start() + (arrow.get_end() - arrow.get_start())/norm/3)
                arrow.target.set_color(ratio_color(1 - clip(norm, 0, 1)))#.set_opacity(0.5)
        self.play(*[MoveToTarget(arrow) for arrow in arrows])
        self.wait()

        title = Title("评分函数")
        subtitle = Text("score function", font = "Times New Roman", color = YELLOW).scale(0.8).next_to(title)
        titleline = TitleLine()
        titleback = Rectangle(height = 1, width = 16, **background_dic, fill_color = BLACK).shift(3.5*UP)
        self.add_text(titleback, titleline, title, ).play(title.shift(UP).animate.shift(DOWN), 
                                                          GrowFromPoint(titleline, 4*UP), titleback.shift(UP).animate.shift(DOWN), )
        self.wait()
        self.add_text(subtitle).play(Write(subtitle))
        self.wait()

        future = []
        def reverse_updater(mob: Mobject):
            try:
                points = history.pop()
                future.append(points)
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
            
        dot_0.add_updater(reverse_updater)
        self.wait(8)

class Video_5_2(FrameScene):
    def construct(self):
        title = Title("评分函数")
        subtitle = Text("score function", font = "Times New Roman", color = YELLOW).scale(0.8).next_to(title)
        titleline = TitleLine()
        titleback = Rectangle(height = 1, width = 16, **background_dic, fill_color = BLACK).shift(3.5*UP)
        self.add_text(titleback, titleline, title, subtitle)

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
            uniform float radius;
            uniform float ratio;

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index] - center;
                float dis = length(point);
                if (dis >= radius){
                    float factor = (1-ratio)*radius + ratio*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point + center, 0.0, 0.0);
            }
            """
        colors = list(np.random.choice(MANIM_COLORS, size=5000))
        colors = [interpolate_color(color, GREY_E, 0.5) for color in colors]

        computer_1 = Diffuse(compute_shader_code, self.camera.ctx, center = (0, 0), radius = 0.5, ratio = 0.8)
        dot_1 = DotCloud([ORIGIN]*5000, radius = 0.02, color = colors)
        dot_1.computer = computer_1
        
        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 1*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        def random_updater(mob: Mobject):
            simple_diffusion(mob.get_points(), computer = mob.computer)

        self.add(dot_1)# .wait()
        dot_1.add_updater(random_updater)
        self.wait()
        dot_1.clear_updaters()

        # anchors_1 = Line(3*RIGHT + 2*UP, 2*DOWN + 3*LEFT).get_points()[:, :2]
        anchors_1 = SVGMobject("smile_face.svg", height = 4).get_all_points()[:, :2]
        dot_1.computer = BezierDiffuse(compute_shader_source, anchors_1, self.camera.ctx, surr = 0.1, ratio = 0.9)
        
        def potential(points: np.ndarray, computer: Diffuse | BezierDiffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.05*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        
        def potential_updater(mob: Mobject):
            potential(mob.get_points(), computer = mob.computer)
        dot_1.add_updater(potential_updater)
        self.wait(1)
        dot_1.clear_updaters()
        self.wait()

        data = dot_1.get_points().copy()[:100]

        def cal_exact_score(sigma, x):
            diff = data - x
            d2 = np.sum(diff**2, axis=1) / (2*sigma)
            d2 -= d2.min()
            kernel = np.exp(- d2)
            kernel /= np.sum(kernel)
            weight_x0 = diff * kernel[:, np.newaxis]
            score = np.sum(weight_x0, axis=0)

            return score/5

        n = 5
        arrows = []
        for i in range(-8*n, 8*n+1):
            for j in range(-4*n, 4*n+1):
                arrow = Arrow(buff = 0, color = GREY_D)
                arrow.position = (i*RIGHT + j*UP)/n
                score = cal_exact_score(0.01, arrow.position)
                norm = get_norm(score)
                if norm > 1/n:
                    score /= norm*n
                arrow.become(Arrow(arrow.position, arrow.position + score, buff = 0))
                arrow.set_color(ratio_color(1 - clip(norm, 0, 1)))
                arrows.append(arrow)
                
        self.add(*arrows).play(LaggedStart(*[GrowArrow(mob) for mob in arrows], lag_ratio = 0.05, run_time = 2, group = VGroup(), remover = True))
        self.wait()

        history = []

        alpha = ValueTracker(0.0)
        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        def random_updater(mob: Mobject):
            history.append(mob.get_points().copy())
            multi_brownian(mob.get_points())

        beta = ValueTracker(0.00)
        beta_history = []
        def trace_tracker(mob: ValueTracker):
            mob.increment_value(alpha.get_value()**2)
            beta_history.append(mob.get_value())
        beta.add_updater(trace_tracker)
        def arrow_updater(mob: Arrow):
            score = cal_exact_score(max(0.01, beta.get_value()), mob.position)
            norm = get_norm(score)
            if norm > 1/n:
                score /= norm*n
            mob.become(Arrow(mob.position, mob.position + score, buff = 0))
            mob.set_color(ratio_color(1 - clip(norm, 0, 1)))
                
        for arrow in arrows:
            arrow.add_updater(arrow_updater)
        dot_1.add_updater(random_updater)
        self.bring_to_back(alpha, beta).play(alpha.animate.set_value(0.1), rate_func = lambda t: (np.exp(2*t)-1)/(np.e**2 - 1), run_time = 2)
        self.wait(4)
        self.play(alpha.animate.set_value(0.00), rate_func = less_smooth)
        dot_1.clear_updaters()
        beta.clear_updaters()
        self.wait()

        def trace_tracker(mob: ValueTracker):
            try:
                value = beta_history.pop()
                mob.set_value(value)
            except IndexError:
                mob.clear_updaters()
        beta.add_updater(trace_tracker)
        future = []
        def reverse_updater(mob: Mobject):
            try:
                points = history.pop()
                future.append(points)
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
        dot_1.add_updater(reverse_updater)
        self.wait(8)

class Video_6_2(FrameScene):
    def construct(self):
        title = Title("评分函数")
        subtitle = Text("score function", font = "Times New Roman", color = YELLOW).scale(0.8).next_to(title)
        titleline = TitleLine()
        titleback = Rectangle(height = 1, width = 16, **background_dic, fill_color = BLACK).shift(3.5*UP)
        self.add_text(titleback, titleline, title, subtitle)

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
            uniform float radius;
            uniform float ratio;

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index] - center;
                float dis = length(point);
                if (dis >= radius){
                    float factor = (1-ratio)*radius + ratio*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point + center, 0.0, 0.0);
            }
            """
        colors = list(np.random.choice(MANIM_COLORS, size=5000))
        colors = [interpolate_color(color, GREY_E, 0.5) for color in colors]

        computer_1 = Diffuse(compute_shader_code, self.camera.ctx, center = (0, 0), radius = 0.5, ratio = 0.8)
        dot_1 = DotCloud([ORIGIN]*5000, radius = 0.02, color = colors)
        dot_1.computer = computer_1
        
        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 1*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        def random_updater(mob: Mobject):
            simple_diffusion(mob.get_points(), computer = mob.computer)

        self.add(dot_1)# .wait()
        dot_1.add_updater(random_updater)
        self.wait()
        dot_1.clear_updaters()

        # anchors_1 = Line(3*RIGHT + 2*UP, 2*DOWN + 3*LEFT).get_points()[:, :2]
        anchors_1 = SVGMobject("smile_face.svg", height = 4).get_all_points()[:, :2]
        dot_1.computer = BezierDiffuse(compute_shader_source, anchors_1, self.camera.ctx, surr = 0.1, ratio = 0.9)
        
        def potential(points: np.ndarray, computer: Diffuse | BezierDiffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.05*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        
        def potential_updater(mob: Mobject):
            potential(mob.get_points(), computer = mob.computer)
        dot_1.add_updater(potential_updater)
        self.wait(1)
        dot_1.clear_updaters()
        self.wait()

        data = dot_1.get_points().copy()[:120, :2]

        compute_shader_code_2 = """
            #version 430 core

            layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;

            layout(std140, binding = 0) buffer CurvePoints {
                vec2 sample_points[];    // 其实会对齐到 vec4
            };

            layout(std140, binding = 1) buffer InputBuffer {
                vec2 points[];      // 其实会对齐到 vec4
            };

            layout(std140, binding = 2) buffer OutputBuffer {
                vec3 results[];     // 其实会对齐到 vec4
            };

            uniform float sigma;

            const float INFINITY = uintBitsToFloat(0x7F800000);

            void main() {
                uint data_length = sample_points.length();
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index];

                float distances[120];
                float min = INFINITY;
                for (int i = 0; i < data_length; i ++) {
                    distances[i] = length(point - sample_points[i]);
                    if (distances[i] < min){
                        min = distances[i];
                    }
                }

                float sum_of_weights = 0;
                float weight;
                vec2 score = vec2(0.0, 0.0);
                for (int i = 0; i < data_length; i ++) {
                    weight = exp(-(distances[i] - min)*(distances[i] - min)/2/sigma);
                    sum_of_weights += weight;
                    score += weight * (point - sample_points[i]);
                }

                results[index] = vec3(score/sum_of_weights, 0.0);
            }
        """

        def cal_exact_score(sigma, x):
            diff = data - x
            d2 = np.sum(diff**2, axis=1) / (2*sigma)
            d2 -= d2.min()
            kernel = np.exp(- d2)
            kernel /= np.sum(kernel)
            weight_x0 = diff * kernel[:, np.newaxis]
            score = np.sum(weight_x0, axis=0)

            return score/5

        n = 5
        arrows = []
        score_history = [[]]
        for i in range(-8*n, 8*n+1):
            for j in range(-4*n, 4*n+1):
                arrow = Arrow(buff = 0, color = GREY_D)
                arrow.position = [i/n, j/n]
                score = cal_exact_score(0.01, arrow.position)
                score_history[0].append(score)
                norm = get_norm(score)
                if norm > 1/n:
                    score /= norm*n
                arrow.become(Arrow(np.array([*arrow.position, 0]), np.array([*(arrow.position + score), 0]), buff = 0))
                arrow.set_color(ratio_color(1 - clip(norm, 0, 1)))
                arrows.append(arrow)
            
        starts = [arrow.position for arrow in arrows]
                
        self.add(*arrows).play(LaggedStart(*[GrowArrow(mob) for mob in arrows], lag_ratio = 0.05, run_time = 2, group = VGroup(), remover = True))
        self.wait()

        history = []

        alpha = ValueTracker(0.0)
        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        def random_updater(mob: Mobject):
            history.append(mob.get_points().copy())
            multi_brownian(mob.get_points())

        beta = ValueTracker(0.00)
        beta_history = []
        def trace_tracker(mob: ValueTracker):
            mob.increment_value(alpha.get_value()**2)
            beta_history.append(mob.get_value())
        beta.add_updater(trace_tracker)

        arrows = VGroup(*arrows)
        self.add(*arrows)
        computer = BezierDiffuse(compute_shader_code_2, data, self.camera.ctx)
        def arrows_updater(mob: VGroup):
            scores = computer.compute(starts, sigma = max(0.01, beta.get_value())).copy()
            score_history.append(scores)
            for score, arrow in zip(scores, mob):
                norm = get_norm(score)
                if norm > 1/n:
                    score /= norm*n
                arrow.become(Arrow(np.array([*arrow.position, 0]), np.array([*(arrow.position + score), 0]), buff = 0))
                arrow.set_color(ratio_color(1 - clip(norm, 0, 1)))
        arrows.add_updater(arrows_updater)
        self.add(arrows)
                
        dot_1.add_updater(random_updater)
        self.bring_to_back(alpha, beta).play(alpha.animate.set_value(0.1), rate_func = lambda t: (np.exp(2*t)-1)/(np.e**2 - 1), run_time = 2)
        self.wait(4)
        self.play(alpha.animate.set_value(0.00), rate_func = less_smooth)
        dot_1.clear_updaters()
        beta.clear_updaters()
        arrows.clear_updaters()
        self.wait()

        def trace_tracker(mob: ValueTracker):
            try:
                value = beta_history.pop()
                mob.set_value(value)
            except IndexError:
                mob.clear_updaters()
        beta.add_updater(trace_tracker)
        def scores_tracker(mob: ValueTracker):
            try:
                scores = score_history.pop()
                for score, arrow in zip(scores, mob):
                    norm = get_norm(score)
                    if norm > 1/n:
                        score /= norm*n
                    arrow.become(Arrow(np.array([*arrow.position, 0]), np.array([*(arrow.position + score), 0]), buff = 0))
                    arrow.set_color(ratio_color(1 - clip(norm, 0, 1)))
            except IndexError:
                mob.clear_updaters()
        arrows.add_updater(scores_tracker)
        future = []
        def reverse_updater(mob: Mobject):
            try:
                points = history.pop()
                future.append(points)
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
        dot_1.add_updater(reverse_updater)
        self.wait(8)
        
#################################################################### 

class InnerImage(Mobject):
    CONFIG = {
        "height": 4,
        "opacity": 1,
        "shader_folder": "image",
        "shader_dtype": [
            ('point', np.float32, (3,)),
            ('im_coords', np.float32, (2,)),
            ('opacity', np.float32, (1,)),
        ]
    }

    def __init__(self, path: str, image: Image.Image, **kwargs):
        self.path = path
        self.image = image
        self.texture_paths = {"Texture": path}
        super().__init__(**kwargs)

    def init_data(self) -> None:
        self.data = {
            "points": np.array([UL, DL, UR, DR]),
            "im_coords": np.array([(0., 0.), (0., 1.), (1., 0.), (1., 1.)]), #不然无法插植
            "opacity": np.array([[self.opacity]], dtype=np.float32),
        }

    def init_points(self) -> None:
        size = self.image.size
        self.set_width(2 * size[0] / size[1], stretch=True)
        self.set_height(self.height)

    def set_opacity(self, opacity: float, recurse: bool = True):
        for mob in self.get_family(recurse):
            mob.data["opacity"] = np.array([[o] for o in listify(opacity)])
        return self

    def set_color(self, color, opacity=None, recurse=None):
        return self

    def point_to_rgb(self, point: np.ndarray) -> np.ndarray:
        x0, y0 = self.get_corner(UL)[:2]
        x1, y1 = self.get_corner(DR)[:2]
        x_alpha = inverse_interpolate(x0, x1, point[0])
        y_alpha = inverse_interpolate(y0, y1, point[1])
        if not (0 <= x_alpha <= 1) and (0 <= y_alpha <= 1):
            # TODO, raise smarter exception
            raise Exception("Cannot sample color from outside an image")

        pw, ph = self.image.size
        rgb = self.image.getpixel((
            int((pw - 1) * x_alpha),
            int((ph - 1) * y_alpha),
        ))
        return np.array(rgb) / 255

    def get_shader_data(self) -> np.ndarray:
        shader_data = super().get_shader_data()
        self.read_data_to_shader(shader_data, "im_coords", "im_coords")
        self.read_data_to_shader(shader_data, "opacity", "opacity")
        return shader_data

class Video_8(FrameScene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inner_images: list[Shot] = []
    
    def add_inner_image(self, *inner_images: InnerImage):
        self.inner_images.extend(inner_images)
        for image in inner_images:
            path = image.path
            if self.camera.n_textures == 15:  # I have no clue why this is needed
                self.camera.n_textures += 1
            tid = self.camera.n_textures
            self.camera.n_textures += 1

            im = image.image
            texture = self.camera.ctx.texture(
                    size=im.size,
                    components=len(im.getbands()),
                    data=im.tobytes(),
                )
            texture.use(location=tid)
            self.camera.path_to_texture[path] = (tid, texture)

    def construct(self):
        offset_l = 4*LEFT
        small_img = Image.open("crafting_table_front.png")
        data = np.asarray(small_img.convert("RGBA"))
        small_r, small_g, small_b = data[:, :, 0].reshape(-1)/255, data[:, :, 1].reshape(-1)/255, data[:, :, 2].reshape(-1)/255
        pic_0 = ImageMobject("enlarged_front.png", height = 3).shift(offset_l)
        self.play(FadeIn(pic_0, 0.5*UP))
        self.wait()

        # data = np.asarray(pic_0.image.convert("RGBA"))
        # data_r = data * np.array([1, 0, 0, 1], dtype = np.uint8)
        # image_r = Image.fromarray(data_r)
        # pic_r = InnerImage("red", image_r, height = 3).shift(RIGHT + 2*UP).save_state()
        # data_g = data * np.array([0, 1, 0, 1], dtype = np.uint8)
        # image_g = Image.fromarray(data_g)
        # pic_g = InnerImage("green", image_g, height = 3).shift(5*RIGHT + 2*UP).save_state()
        # data_b = data * np.array([0, 0, 1, 1], dtype = np.uint8)
        # image_b = Image.fromarray(data_b)
        # pic_b = InnerImage("blue", image_b, height = 3).shift(3*RIGHT + 1.5*DOWN).save_state()
        # self.add_inner_image(pic_r, pic_g, pic_b)
        # self.add(pic_r.move_to(offset_l), pic_g.move_to(offset_l), pic_b.move_to(offset_l), pic_0).play(
        #     pic_r.animate.restore(), pic_g.animate.restore(), pic_b.animate.restore())
        # self.wait()

        squares_r = VGroup(*[Square(side_length = 3/16, fill_color = rgb_to_color((red, 0, 0)), **background_dic) for red in small_r])
        squares_r.arrange_in_grid(16, 16, buff = 0).shift(RIGHT + 2*UP).save_state()
        squares_g = VGroup(*[Square(side_length = 3/16, fill_color = rgb_to_color((0, green, 0)), **background_dic) for green in small_g])
        squares_g.arrange_in_grid(16, 16, buff = 0).shift(3*RIGHT + 1.5*DOWN).save_state()
        squares_b = VGroup(*[Square(side_length = 3/16, fill_color = rgb_to_color((0, 0, blue)), **background_dic) for blue in small_b])
        squares_b.arrange_in_grid(16, 16, buff = 0).shift(5*RIGHT + 2*UP).save_state()
        # self.add(squares_r, squares_g, squares_b)
        self.add(squares_r.move_to(offset_l), squares_g.move_to(offset_l), squares_b.move_to(offset_l), pic_0).play(
            squares_r.animate.restore(), squares_g.animate.restore(), squares_b.animate.restore())
        self.wait()

        self.play(OverFadeOut(pic_0, 4*LEFT), squares_r.animating(path_arc = PI/2).move_to(4.5*LEFT).scale(4/3), 
                  squares_g.animating(path_arc = -PI/2).move_to(ORIGIN).scale(4/3), squares_b.animating(path_arc = PI/2).move_to(4.5*RIGHT).scale(4/3))
        self.wait()

        texs_r = VGroup(*[MTex("%.2f"%red,).set_stroke(width = 4, color = BLACK, background = True).scale(0.25) for red in small_r])
        texs_g = VGroup(*[MTex("%.2f"%green,).set_stroke(width = 4, color = BLACK, background = True).scale(0.25) for green in small_g])
        texs_b = VGroup(*[MTex("%.2f"%blue,).set_stroke(width = 4, color = BLACK, background = True).scale(0.25) for blue in small_b])
        for i in range(256):
            texs_r[i].move_to(squares_r[i])
            texs_g[i].move_to(squares_g[i])
            texs_b[i].move_to(squares_b[i])
        self.play(Write(texs_r), Write(texs_g), Write(texs_b))
        self.wait()

        for mob in [squares_r, squares_g, squares_b, texs_r, texs_g, texs_b]:
            mob.generate_target()
        vector = VGroup()
        for i in range(256):
            squares_r.target[i].scale(0), squares_g.target[i].scale(0), squares_b.target[i].scale(0)
            texs_r.target[i].set_stroke(color = WHITE).set_fill(color = squares_r.target[i].get_fill_color())
            texs_g.target[i].set_stroke(color = WHITE).set_fill(color = squares_g.target[i].get_fill_color())
            texs_b.target[i].set_stroke(color = WHITE).set_fill(color = squares_b.target[i].get_fill_color())
            vector.add(texs_r.target[i].copy(), texs_g.target[i].copy(), texs_b.target[i].copy())
        self.play(*[MoveToTarget(mob) for mob in [squares_r, squares_g, squares_b, texs_r, texs_g, texs_b]])
        self.wait()
        
        vector.generate_target().scale(2).arrange().next_to(3*UP + 6.5*LEFT)
        for i in range(1, 16):
            vector.target[48*i:48*(i+1)].next_to(3*UP + 8*RIGHT)
        self.play(LaggedStart(*[Transform(vector[i], vector.target[i]) for i in range(256*3)], lag_ratio = 0.001, run_time = 4, group = vector))
        self.wait()

        short_vector = VGroup(*vector[:24].copy())
        short_vector.add(*vector[-9:].copy().next_to(short_vector))
        self.remove(vector).add(short_vector)

        vector_target = VGroup(MTex("["), *short_vector[:9].copy(), MTex("\cdots"), *short_vector[-9:].copy(), MTex("]"), ).arrange()
        vector_target.shift(short_vector[0].get_center() - vector_target[1].get_center())
        self.play(Write(vector_target[0]), *[Transform(mob, vector_target[10]) for mob in short_vector[9:-9]], 
                  Transform(short_vector[-9:], vector_target[-10:-1]), vector_target[-1].save_state().next_to(short_vector).animate.restore(), run_time = 2)
        self.wait()

        self.play(texs_r.animate.scale(0.6).move_to(RIGHT + 1.2*UP), 
                  texs_g.animate.scale(0.6).move_to(2.5*RIGHT + 1.8*DOWN), 
                  texs_b.animate.scale(0.6).move_to(4*RIGHT + 1.2*UP), 
                  OverFadeIn(pic_0.shift(0.5*DOWN)), run_time = 2)
        self.wait()

#################################################################### 

class Video_11(FrameScene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inner_images: list[Shot] = []

    def refresh(self):
        im = self.images[((self.frames-1)//2)*2%32]
        self.camera.path_to_texture["gif"][1].write(data=im.tobytes())
        super().refresh()
    
    def add_inner_image(self, *inner_images: InnerImage):
        self.inner_images.extend(inner_images)
        for image in inner_images:
            path = image.path
            if self.camera.n_textures == 15:  # I have no clue why this is needed
                self.camera.n_textures += 1
            tid = self.camera.n_textures
            self.camera.n_textures += 1

            im = image.image
            texture = self.camera.ctx.texture(
                    size=im.size,
                    components=len(im.getbands()),
                    data=im.tobytes(),
                )
            texture.use(location=tid)
            self.camera.path_to_texture[path] = (tid, texture)

    def construct(self):
        image = Image.open("fire_1.png")
        data = np.asarray(image.convert("RGBA"))
        self.images = []
        for i in range(32):
            enlarged = np.zeros((256, 256, 4), dtype = np.uint8)
            data_slice = data[16*i:16*(i+1)]
            for j in range(16):
                for k in range(16):
                    enlarged[j::16, k::16] = data_slice
            self.images.append(Image.fromarray(enlarged))

        gif = InnerImage("gif", self.images[0], height = 4).shift(4*LEFT)
        self.add_inner_image(gif)
        self.add(gif)
        self.wait(0, 5*32)

        positions = [3*RIGHT + 0.5*UP + (i-1.5)*1.75*DOWN + (j-1.5)*1.75*RIGHT for i in range(4) for j in range(4)]
        gif_frames: list[InnerImage] = []
        for i in range(16):
            frame_i = InnerImage("gif_frame_" + str(i), self.images[(self.frames//2)*2%32], height = 1.5).move_to(positions[i])
            gif_frames.append(frame_i)
            self.add_inner_image(frame_i)
            self.add(frame_i).wait(0, 2)
        surr = SurroundingRectangle(gif_frames[0], buff = 0.1)
        self.add(surr)
        def move_updater(mob: SurroundingRectangle):
            mob.move_to(positions[((self.frames-1)//2)%16])
        surr.add_updater(move_updater)
        self.wait(0, 160)
        
        texts = []
        for i in range(16):
            start, end = gif_frames[i].image.getpixel((0, 0)), gif_frames[i].image.getpixel((255, 255))
            sr, sg, sb, er, eg, eb = start[0]/255, start[1]/255, start[2]/255, end[0]/255, end[1]/255, end[2]/255
            tex_0 = MTex("%.2f"%sr, fill_color = rgb_to_color((sr, 0, 0))).set_stroke(width = 4, color = WHITE if sr < 2/3 else BLACK, background = True).scale(0.3).next_to(0.6*UP + 0.75*LEFT, RIGHT, buff = 0.1)
            tex_1 = MTex("%.2f"%sg, fill_color = rgb_to_color((0, sg, 0))).set_stroke(width = 4, color = WHITE if sg < 2/3 else BLACK, background = True).scale(0.3).next_to(tex_0, RIGHT, buff = 0.1)
            tex_2 = MTex("%.2f"%sb, fill_color = rgb_to_color((0, 0, sb))).set_stroke(width = 4, color = WHITE, background = True).scale(0.3).next_to(tex_1, RIGHT, buff = 0.1)
            tex_3 = MTex("\cdots").set_stroke(width = 4, color = BLACK, background = True)
            tex_6 = MTex("%.2f"%eb, fill_color = rgb_to_color((0, 0, eb))).set_stroke(width = 4, color = WHITE, background = True).scale(0.3).next_to(0.6*DOWN + 0.75*RIGHT, LEFT, buff = 0.1)
            tex_5 = MTex("%.2f"%eg, fill_color = rgb_to_color((0, eg, 0))).set_stroke(width = 4, color = WHITE if eg < 2/3 else BLACK, background = True).scale(0.3).next_to(tex_6, LEFT, buff = 0.1)
            tex_4 = MTex("%.2f"%er, fill_color = rgb_to_color((er, 0, 0))).set_stroke(width = 4, color = WHITE if er < 2/3 else BLACK, background = True).scale(0.3).next_to(tex_5, LEFT, buff = 0.1)
            texts.append(VGroup(tex_0, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6).move_to(gif_frames[i]))
        self.play(LaggedStart(*[Write(mob) for mob in texts], lag_ratio = 1/30, run_time = 3))
        self.wait(0, 6)
        self.wait(0, 160)

        vector = VGroup(*[mob.copy() for text in texts for mob in text])
        vector_target = VGroup(MTex("["), *vector[:3].copy().scale(2), MTex("\cdots"), *vector[-3:].copy().scale(2), MTex("]"), ).arrange().move_to(4*LEFT + 3*UP)
        self.play(Write(vector_target[0]), Write(vector_target[-1]), *[Transform(mob, vector_target[4]) for mob in vector[3:-3]],
                  Transform(vector[:3], vector_target[1:4]), Transform(vector[-3:], vector_target[-4:-1]), run_time = 2)
        self.wait(0, 4)
        self.wait(0, 160)

#################################################################### 

compute_shader_source_9 = """
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

void distance_bezier(in vec2 A, in vec2 B, in vec2 C, in vec2 p, out float distance)
{
    vec2 v1 = normalize(B - A), v2 = normalize(C - B);
    if (abs(cross2d(v1, v2)) < 1e-3 && dot(v1, v2) > 0.0) {
        vec2 e = C - A;
        vec2 w = p - A;
        vec2 offset = e * clamp(dot(w, e) / dot(e, e), 0.0, 1.0);
        vec2 b = w - offset;
        distance = length(b);
        return;
    }

    B = mix(B + vec2(1e-4), B, abs(sign(B * 2.0 - A - C)));
    vec2 a = B - A, b = A - B * 2.0 + C, c = a * 2.0, d = A - p;
    vec3 k = vec3(3. * dot(a, b),2. * dot(a, a) + dot(d, b),dot(d, a)) / dot(b, b);
    vec3 t = clamp(solve_cubic(k.x, k.y, k.z), 0.0, 1.0);

    vec2 pos = A + (c + b * t.x) * t.x;
    float dis = length(pos - p);
    distance = dis;

    pos = A + (c + b * t.y) * t.y;
    dis = min(dis, length(pos - p));
    if (dis < distance) {
        distance = dis;
    }

    pos = A + (c + b * t.z) * t.z;
    dis = min(dis, length(pos - p));
    if (dis < distance) {
        distance = dis;
    }
}

const float INFINITY = uintBitsToFloat(0x7F800000);

void main() {
    uint index = gl_GlobalInvocationID.x;
    vec2 point = points[index];

    float dis = INFINITY;

    float part_dis;

    for (int i = 0; i < curve_points.length(); i += 3) {
        distance_bezier(
            curve_points[i],
            curve_points[i + 1],
            curve_points[i + 2],
            point,
            part_dis
        );
        if (part_dis < dis) {
            dis = part_dis;
        }
    }

    results[index] = vec3(dis, 0.0, 0.0);
}
"""

class Video_10(FrameScene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inner_images: list[Shot] = []
    
    def add_inner_image(self, *inner_images: InnerImage):
        self.inner_images.extend(inner_images)
        for image in inner_images:
            path = image.path
            if self.camera.n_textures == 15:  # I have no clue why this is needed
                self.camera.n_textures += 1
            tid = self.camera.n_textures
            self.camera.n_textures += 1

            im = image.image
            texture = self.camera.ctx.texture(
                    size=im.size,
                    components=len(im.getbands()),
                    data=im.tobytes(),
                )
            texture.use(location=tid)
            self.camera.path_to_texture[path] = (tid, texture)

    def construct(self):
        ratio = 0.2
        lines_h = [Line(3*LEFT + i*ratio*DOWN, 3*RIGHT + i*ratio*DOWN, stroke_width = 0.5 if i%5 else 1, color = BLUE if i else WHITE) for i in range(-15, 16)]
        lines_v = [Line(3*UP + i*ratio*RIGHT, 3*DOWN + i*ratio*RIGHT, stroke_width = 0.5 if i%5 else 1, color = BLUE if i else WHITE) for i in range(-15, 16)]
        grid = VGroup(*lines_h[:15], *lines_h[16:], *lines_v, lines_h[15])
        
        self.add(*grid).play(LaggedStart(*[ShowCreation(mob) for mob in lines_h], lag_ratio = 0.1, run_time = 2), 
                             LaggedStart(*[ShowCreation(mob) for mob in lines_v], lag_ratio = 0.1, run_time = 2), )
        self.wait()

        n = 1000
        points = np.random.rand(1000, 3)*np.array([6, 6, 0])-np.array([3, 3, 0])
        roll = ParametricCurve(lambda t: t*unit(t)/3, [0, 2*TAU, 0.01])
        computer = BezierDiffuse(compute_shader_source_9, roll.get_all_points()[:, :2], self.camera.ctx)
        distances = computer.compute(points[:, :2])[:, 0]
        gold, dust = [], []
        for i in range(n):
            if distances[i] < 0.2:
                gold.append(points[i])
            else:
                dust.append(points[i])
        # colors = [GOLD if distance < 0.2 else GREY for distance in distances]
        # dots_0 = DotCloud(points, color = colors)
        # self.add(dots_0)
        # self.add(roll)

        dots_gold, dots_dust = DotCloud(gold, color = GOLD), DotCloud(dust, color = GREY)
        self.play(ShowIncreasingPoints(dots_dust, run_time = 2))
        self.wait()

        p_A, p_B, p_C, p_D = dust[5], dust[14], dust[16], gold[9]
        randoms = []
        for _ in range(3):
            rand = np.random.randint(0, 255, size=(16, 16, 3), dtype = np.uint8)
            enlarged = np.zeros((256, 256, 3), dtype = np.uint8)
            for j in range(16):
                for k in range(16):
                    enlarged[j::16, k::16] = rand
            randoms.append(Image.fromarray(enlarged).convert("RGBA"))
        pic_1, pic_2, pic_3 = InnerImage("random_1", randoms[0], height = 2), InnerImage("random_2", randoms[1], height = 2), InnerImage("random_3", randoms[2], height = 2)
        self.add_inner_image(pic_1.move_to(2*UP + 5*RIGHT), pic_2.move_to(DOWN + 5*RIGHT), pic_3.move_to(DOWN + 5*LEFT))
        line_1 = Polyline(p_A, 0.8*UP + 3.8*RIGHT, 0.8*UP + 6.2*RIGHT, color = GREY)
        line_2 = Polyline(p_B, 2.2*DOWN + 3.8*RIGHT, 2.2*DOWN + 6.2*RIGHT, color = GREY)
        line_3 = Polyline(p_C, 2.2*DOWN + 3.8*LEFT, 2.2*DOWN + 6.2*LEFT, color = GREY)
        self.add_text(line_1, pic_1).play(GrowFromPoint(line_1, p_A), GrowFromPoint(pic_1, p_A))
        self.add_text(line_2, pic_2).play(GrowFromPoint(line_2, p_B), GrowFromPoint(pic_2, p_B))
        self.add_text(line_3, pic_3).play(GrowFromPoint(line_3, p_C), GrowFromPoint(pic_3, p_C))
        self.wait()

        pic_4 = ImageMobject("enlarged_front.png", height = 2).move_to(2*UP + 5*LEFT)
        line_4 = Polyline(p_D, 0.8*UP + 3.8*LEFT, 0.8*UP + 6.2*LEFT, color = GOLD)
        self.play(ShowIncreasingPoints(dots_gold, run_time = 2))
        self.wait()
        self.add_text(line_4, pic_4).play(GrowFromPoint(line_4, p_D), GrowFromPoint(pic_4, p_D))
        self.wait()

        randoms = []
        for _ in range(3):
            rand = np.random.randint(0, 255, size=(256, 256, 3), dtype = np.uint8)
            # enlarged = np.zeros((256, 256, 3), dtype = np.uint8)
            # for j in range(4):
            #     for k in range(4):
            #         enlarged[j::4, k::4] = rand
            randoms.append(Image.fromarray(rand).convert("RGBA"))
        pic_5, pic_6, pic_7 = InnerImage("random_5", randoms[0], height = 2).move_to(pic_1), InnerImage("random_6", randoms[1], height = 2).move_to(pic_2), InnerImage("random_7", randoms[2], height = 2).move_to(pic_3)
        self.add_inner_image(pic_5, pic_6, pic_7)
        pic_8 = ImageMobject("dog_0.png", height = 2).move_to(pic_4)
        self.play(FadeTransform(pic_1, pic_5), FadeTransform(pic_2, pic_6), FadeTransform(pic_3, pic_7), FadeTransform(pic_4, pic_8))
        self.wait()

        self.add_text(self.shade, pic_8).play(FadeIn(self.shade), self.camera.frame.save_state().animating(run_time = 2).set_height(8/3).move_to(2*UP + 6*LEFT))
        self.camera.frame.restore()
        self.clear().add(pic_8.scale(3).move_to(3*RIGHT)).wait()

        data = np.asarray(pic_8.image.convert("RGBA"))
        # print(data.shape)
        small_data = data[11*32:12*32, 15*32:16*32]
        enlarged = np.zeros((256, 256, 4), dtype = np.uint8)
        for j in range(8):
            for k in range(8):
                enlarged[j::8, k::8] = small_data
        scoped = InnerImage("scoped", Image.fromarray(enlarged).convert("RGBA"), height = 3).move_to(3.5*LEFT + 1.5*UP)
        surr = SurroundingRectangle(scoped)
        self.add_inner_image(scoped)
        # self.add(scoped)

        up, down = interpolate(3, -3, 11*32/1197), interpolate(3, -3, 12*32/1197)
        left, right = interpolate(0, 6, 15*32/1200), interpolate(0, 6, 16*32/1200)
        sample = Polygon(np.array([left, up, 0]), np.array([left, down, 0]), np.array([right, down, 0]), np.array([right, up, 0]))
        surr_2 = SurroundingRectangle(sample, buff = 0.02)
        self.play(ShowCreation(surr_2))
        self.wait()
        line = Line(color = YELLOW).save_state()
        def line_updater(mob: Line):
            mob.become(Line(surr, surr_2, color = YELLOW))
        self.add(line.add_updater(line_updater), scoped).play(scoped.save_state().replace(sample).animate.restore(), TransformFromCopy(surr_2, surr))
        line.clear_updaters()
        self.wait()

        up, down = interpolate(3, 0, 20/32), interpolate(3, 0, 21/32)
        left, right = interpolate(-5, -2, 15/32), interpolate(-5, -2, 18/32)
        sample_2 = Polygon(np.array([left, up, 0]), np.array([left, down, 0]), np.array([right, down, 0]), np.array([right, up, 0]))
        surr_3 = SurroundingRectangle(sample_2, buff = 0.02)
        self.play(ShowCreation(surr_3))
        self.wait()
        
        numbers = [small_data[20, i, :3]/255 for i in (15, 16, 17)]
        colors = [rgb_to_color(number) for number in numbers]
        squares = [Square(side_length = 1, color = colors[i], **background_dic).move_to(DOWN + 3.5*LEFT + (i-1)*1.5*RIGHT) for i in range(3)]

        positions = [surr_3.get_center() + 1.5/16*LEFT, surr_3.get_center(), surr_3.get_center() + 1.5/16*RIGHT]
        def line_updater(index: int):
            def util(mob: Line):
                mob.become(Line(positions[index], squares[index], color = mob.get_color()))
            return util
        lines = [Line(color = colors[i]).add_updater(line_updater(i)) for i in range(3)]
        self.add(*lines, *squares).play(*[squares[i].save_state().set_height(1.5/16).move_to(positions[i]).animate.restore() for i in range(3)])
        self.wait()

        def rgb_tex(rgb: np.ndarray):
            tex_0 = MTex("%.2f"%rgb[0], fill_color = rgb_to_color((rgb[0], 0, 0))).set_stroke(width = 4, color = WHITE if rgb[0] < 2/3 else BLACK, background = True).scale(0.5).shift(0.35*UP)
            tex_1 = MTex("%.2f"%rgb[1], fill_color = rgb_to_color((0, rgb[1], 0))).set_stroke(width = 4, color = WHITE if rgb[1] < 2/3 else BLACK, background = True).scale(0.5)
            tex_2 = MTex("%.2f"%rgb[2], fill_color = rgb_to_color((0, 0, rgb[2]))).set_stroke(width = 4, color = WHITE, background = True).scale(0.5).shift(0.35*DOWN)
            return VGroup(tex_0, tex_1, tex_2)
        rgb_texs = [rgb_tex(numbers[i]).move_to(squares[i]) for i in range(3)]
        approx_1, approx_2 = MTex(r"\approx").move_to(DOWN + 3.5*LEFT + 0.5*1.5*LEFT), MTex(r"\approx").move_to(DOWN + 3.5*LEFT + 0.5*1.5*RIGHT)
        self.play(*[Write(mob) for mob in rgb_texs], Write(approx_1), Write(approx_2))
        self.wait()

class Video_12(FrameScene):
    def construct(self):
        buff_h, buff_v = 1, 0.35
        m, n = 5, (12, 8, 6, 8, 12)
        dots = [VGroup(*[Dot((i-(m-1)/2)*buff_h*RIGHT + (j-(n[i]-1)/2)*buff_v*UP, stroke_width = 2, fill_opacity = 0, radius = 0.12) for j in range(n[i])]) for i in range(m)]
        lines = []
        for i in range(m-1):
            line = VGroup(*[Line(dot_1, dot_2, stroke_width = 1) for dot_1 in dots[i] for dot_2 in dots[i+1]])
            lines.append(line)
        nn = VGroup(*lines, *dots)#.move_to(4*LEFT)
        self.add(nn)

#################################################################### 

class Video_6(FrameScene):
    def construct(self):
        camera = self.camera.frame
        camera.set_height(10).shift(4*LEFT)

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
            uniform float radius;
            uniform float ratio;

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index] - center;
                float dis = length(point);
                if (dis >= radius){
                    float factor = (1-ratio)*radius + ratio*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point + center, 0.0, 0.0);
            }
            """
        size = 5000
        colors = list(np.random.choice(MANIM_COLORS, size=size))
        colors = [interpolate_color(color, GREY_E, 0.5) for color in colors]

        computer_1 = Diffuse(compute_shader_code, self.camera.ctx, center = (0, 0), radius = 0.5, ratio = 0.8)
        dot_1 = DotCloud([ORIGIN]*size, radius = 0.02, color = colors)
        dot_1.computer = computer_1
        
        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 1*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        def random_updater(mob: Mobject):
            simple_diffusion(mob.get_points(), computer = mob.computer)

        self.add(dot_1)# .wait()
        dot_1.add_updater(random_updater)
        self.wait()
        dot_1.clear_updaters()

        # anchors_1 = Line(3*RIGHT + 2*UP, 2*DOWN + 3*LEFT).get_points()[:, :2]
        back = SVGMobject("smile_face.svg", height = 4, stroke_width = 20, fill_opacity = 0, color = GREY_E)
        anchors_1 = back.get_all_points()[:, :2]
        dot_1.computer = BezierDiffuse(compute_shader_source, anchors_1, self.camera.ctx, surr = 0.1, ratio = 0.9)
        
        def potential(points: np.ndarray, computer: Diffuse | BezierDiffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.05*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        
        def potential_updater(mob: Mobject):
            potential(mob.get_points(), computer = mob.computer)
        dot_1.add_updater(potential_updater)
        self.add_background(back).wait(1)
        dot_1.clear_updaters()
        self.wait()

        history = []
        special = []
        alpha = ValueTracker(0.0)
        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        def random_updater(mob: Mobject):
            history.append(mob.get_points().copy())
            multi_brownian(mob.get_points())
            
        beta = ValueTracker(0.00)
        beta_history = []
        def trace_tracker(mob: ValueTracker):
            mob.increment_value(alpha.get_value()**2)
            beta_history.append(mob.get_value())
        beta.add_updater(trace_tracker)

        dot_1.add_updater(random_updater)
        n = 465
        position_0 = dot_1.get_points()[n]
        dot_special = Dot(color = ORANGE).move_to(position_0)
        pic = ImageMobject("dog_0.png", height = 4).move_to(9*LEFT)
        pic.diffuse = np.asarray(pic.image.convert("RGB"))
        line = Polyline(position_0, 6.8*LEFT + 2.2*DOWN, 11.2*LEFT + 2.2*DOWN, color = ORANGE)
        group_special = Group(dot_special, pic, line)
        self.play(GrowFromPoint(group_special, position_0))
        self.wait()
        self.refresh()

        def group_updater(mob: Group):
            position = dot_1.get_points()[n]
            mob[0].move_to(position)
            mob[2].set_points_as_corners([position_0, 6.8*LEFT + 2.2*DOWN, 11.2*LEFT + 2.2*DOWN])
            nudge = np.random.randn(1197, 1200, 3)
            nudge = np.asarray(100*alpha.get_value()*nudge, dtype = np.int8)
            mob[1].diffuse = np.asarray(nudge + mob[1].diffuse, dtype = np.uint8)
            pic = Image.fromarray(mob[1].diffuse).convert("RGBA")
            self.camera.path_to_texture[mob[1].path][1].write(data = pic.tobytes())
        group_special.add_updater(group_updater)
        trace = TracedPath(lambda : dot_1.get_points()[n], stroke_width = 2, stroke_color = RED_A)
        
        self.bring_to_back(alpha, beta).add(trace).play(alpha.animate.set_value(0.1), rate_func = lambda t: (np.exp(3*t)-1)/(np.e**3 - 1), run_time = 3)
        self.wait(4)
        self.play(alpha.animate.set_value(0.00), rate_func = less_smooth)
        dot_1.clear_updaters()
        beta.clear_updaters()
        self.wait()

        # self.add(Integer(213).scale(0.3).move_to(dot_1.get_points()[213]))
        # points = dot_1.get_points()
        # for i in range(500):
        #     self.add(Integer(i).scale(0.3).move_to(points[i]))
        # self.wait()

'''
class Video_0(FrameScene):
    def construct(self):
        tg = MTexText("MathematicS").scale(2.5)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 3*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 3*UP)
        anchors_M, anchors_S = M.get_points()[:, :2], S.get_points()[:, :2]
        sdf_M, sdf_S = BezierDiffuse(compute_shader_source, anchors_M, self.camera.ctx, surr = 0.2, ratio = 0), BezierDiffuse(compute_shader_source, anchors_S, self.camera.ctx, surr = 0.2, ratio = 0)
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
        self.play(alpha.animate.set_value(0.2), rate_func = lambda t: (np.exp(2.5*t)-1)/(np.e**2.5 - 1), run_time = 2)
        self.play(alpha.animate.set_value(0.175), run_time = 0.5, rate_func = linear, frames = 15)
        dot_0.clear_updaters()

        beta = ValueTracker(0.0)
        def multi_brownian(points: np.ndarray):

            points_M, points_S = points[::2, :2], points[1::2, :2]
            len_M, len_S = len(points_M), len(points_S)
            points_M += alpha.get_value()*np.random.randn(len_M, 2)
            points_S += alpha.get_value()*np.random.randn(len_S, 2)
            beta.increment_value(0.01)
            ratio = clip(beta.get_value(), 0, 0.8)
            surr = interpolate(0.2, 0.0, ratio)
            result_M, result_S = sdf_M.compute(points_M, ratio = ratio, surr = surr), sdf_S.compute(points_S, ratio = ratio, surr = surr)

            # print(ratio)
            # points[::2, :2] = (1-ratio)*points_M + ratio*result_M
            # points[1::2, :2] = (1-ratio)*points_S + ratio*result_S
            points[::2, :2] = result_M
            points[1::2, :2] = result_S
            # return [nudge(i, point) for i, point in enumerate(points)]
        
        def random_updater(mob: Mobject):
            # mob.apply_points_function(multi_brownian) # can't figure out how .apply_points_function() works
            # mob.set_points(multi_brownian(mob.get_points()))
            multi_brownian(mob.get_points())
        dot_0.add_updater(random_updater)
        # self.play(beta.animate.set_value(0.8), run_time = 10, rate_func = linear)
        # self.wait(5)
        self.play(alpha.animate.set_value(0.1), run_time = 1.5, rate_func = linear, frames = 45)
        

        name = Songti("漫士沉思录", color = YELLOW).scale(1.8).shift(1.5*DOWN)
        self.play(Write(name))
        self.wait()
        self.play(FadeIn(self.shade))
'''
        
class Video_0(FrameScene):
    def construct(self):
        camera = self.camera.frame
        camera.shift(DOWN)

        tg = MTexText("MathematicS").scale(2.5).shift(DOWN)
        M, S = tg[0].set_color(BLUE).shift(RIGHT * 3+UP*2).scale(2, about_point = 2*UP), tg[-1].set_color(MAROON_A).shift(LEFT * 3+UP*1.8).scale(2, about_point = 2*UP)
        anchors_M, anchors_S = M.get_points()[:, :2], S.get_points()[:, :2]
        sdf_M, sdf_S = BezierDiffuse(compute_shader_source, anchors_M, self.camera.ctx, surr = 0.02, ratio = 0.5), BezierDiffuse(compute_shader_source, anchors_S, self.camera.ctx, surr = 0.02, ratio = 0.5)

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
            uniform float radius;
            uniform float ratio;

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index] - center;
                float dis = length(point);
                if (dis >= radius){
                    float factor = (1-ratio)*radius + ratio*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point + center, 0.0, 0.0);
            }
            """
        size = 5000
        n = 10000
        dot_0 = DotCloud([ORIGIN]*n, radius = 0.01, color = [MAROON_A if i%2 else BLUE for i in range(n)])
        computer_1 = Diffuse(compute_shader_code, self.camera.ctx, center = (0, 0), radius = 0.5, ratio = 0.8)
        
        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 1*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        for _ in range(30):
            simple_diffusion(dot_0.get_points(), computer = computer_1)

        def potential(points: np.ndarray, nudge: float = 0.1, ratio: float = 0.8):

            points_M, points_S = points[::2, :2], points[1::2, :2]
            len_M, len_S = len(points_M), len(points_S)
            points_M += nudge*np.random.randn(len_M, 2)
            points_S += nudge*np.random.randn(len_S, 2)
            result_M, result_S = sdf_M.compute(points_M, ratio = ratio), sdf_S.compute(points_S, ratio = ratio)
            points[::2, :2] = result_M
            points[1::2, :2] = result_S
        for _ in range(60):
            potential(dot_0.get_points())

        history = []
        for _ in range(60):
            history.append(dot_0.get_points().copy())
            potential(dot_0.get_points(), nudge = 0.01, ratio = 0.4)
        for i in range(60):
            history.append(dot_0.get_points().copy())
            potential(dot_0.get_points(), nudge = 0.01, ratio = 0.4-i*0.3/60)

        shadow = dot_0.get_points().copy()
        def multi_brownian(points: np.ndarray, nudge: float = 0.03):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += nudge*np.random.randn(length, 2)
            points[:, :2] = points_2d/np.sqrt(1 + nudge/4)
        
        for i in range(120):
            history.append(dot_0.get_points().copy())
            power = clip(i, 0, 60)/30
            multi_brownian(dot_0.get_points(), nudge = 0.01*3**power)

        self.add(dot_0)

        def reverse_updater(mob: Mobject):
            try:
                points = history.pop()
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
        dot_0.add_updater(reverse_updater)
        self.wait(4)
        name = Songti("漫士沉思录", color = YELLOW).scale(1.8).shift(2.5*DOWN)
        self.play(Write(name))
        self.wait(2)
        self.play(FadeIn(self.shade))

#################################################################### 

"""
class Video_7(FrameScene):
    def construct(self):
        buff_h, buff_v = 1, 0.35
        m, n = 5, 12
        dots = [VGroup(*[Dot((i-(m-1)/2)*buff_h*RIGHT + (j-(m-1)/2)*buff_v*UP, stroke_width = 2, fill_opacity = 0, radius = 0.12) for j in range(n)]) for i in range(m)]
        lines = []
        for i in range(m-1):
            line = VGroup(*[Line(dot_1, dot_2, stroke_width = 1) for dot_1 in dots[i] for dot_2 in dots[i+1]])
            lines.append(line)
        nn = VGroup(*lines, *dots).move_to(4*LEFT)
        dic = {"fill_opacity": 1, "fill_color": BLACK, "stroke_width": 8, "stroke_color": GREY_C}
        rectangle = Rectangle(height = 4.5, width = 5, **dic).shift(4*LEFT)
        in_port = Polygon(2.5*LEFT + 2.5*UP, 1*LEFT + 4*UP, 7*LEFT + 4*UP, 5.5*LEFT + 2.5*UP, **dic)
        out_port = Polygon(2.5*LEFT + 2.5*DOWN, 1*LEFT + 4*DOWN, 7*LEFT + 4*DOWN, 5.5*LEFT + 2.5*DOWN, **dic)
        blackbox = VGroup(rectangle, in_port, out_port, nn).shift(1.6*DOWN)
        self.add(blackbox).wait()

        colors = list(np.random.choice(MANIM_COLORS, size=3000))
        dot_0 = DotCloud([3*RIGHT]*20000, radius = 0.02, color = colors)
        history = []
        special = []
        self.dot = dot_0

        alpha = ValueTracker(0.1)
        def multi_brownian(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += alpha.get_value()*np.random.randn(length, 2)
            points[:, :2] = points_2d
        
        def random_updater(mob: Mobject):
            points = mob.get_points().copy()
            history.append(points)
            special.append(points[:100])
            multi_brownian(mob.get_points())
        
        self.add(dot_0)# .wait()
        dot_0.add_updater(random_updater)
        self.wait(2)
        self.play(alpha.animate.set_value(0.00), rate_func = less_smooth)
        dot_0.clear_updaters()
        self.wait()
"""

class Video_7_2(FrameScene):
    def construct(self):
        offset_l = 4*LEFT
        camera = self.camera.frame
        camera.set_height(10).shift(offset_l)
        
        buff_h, buff_v = 1, 0.35
        m, n = 5, (12, 8, 6, 8, 12)
        dots = [VGroup(*[Dot((i-(m-1)/2)*buff_h*RIGHT + (j-(n[i]-1)/2)*buff_v*UP, stroke_width = 2, fill_opacity = 0, radius = 0.12) for j in range(n[i])]) for i in range(m)]
        lines = []
        for i in range(m-1):
            line = VGroup(*[Line(dot_1, dot_2, stroke_width = 1) for dot_1 in dots[i] for dot_2 in dots[i+1]])
            lines.append(line)
        nn = VGroup(*lines, *dots).move_to(4*LEFT)
        dic = {"fill_opacity": 1, "fill_color": BLACK, "stroke_width": 8, "stroke_color": GREY_C}
        rectangle = Rectangle(height = 4.5, width = 5, **dic).shift(4*LEFT)
        in_port = Polygon(2.5*LEFT + 2.5*UP, 1*LEFT + 4*UP, 7*LEFT + 4*UP, 5.5*LEFT + 2.5*UP, **dic)
        out_port = Polygon(2.5*LEFT + 2.5*DOWN, 1*LEFT + 4*DOWN, 7*LEFT + 4*DOWN, 5.5*LEFT + 2.5*DOWN, **dic)
        blackbox = VGroup(rectangle, in_port, out_port, nn).scale(1.25).shift(2*DOWN + offset_l)
        self.add_text(blackbox)

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
            uniform float radius;
            uniform float ratio;

            void main() {
                uint index = gl_GlobalInvocationID.x;
                vec2 point = points[index] - center;
                float dis = length(point);
                if (dis >= radius){
                    float factor = (1-ratio)*radius + ratio*dis;
                    point *= factor/dis;
                }
                results[index] = vec4(point + center, 0.0, 0.0);
            }
            """
        size = 200
        colors = list(np.random.choice(MANIM_COLORS, size=size))
        # colors = [interpolate_color(color, GREY_E, 0.5) for color in colors]

        computer_1 = Diffuse(compute_shader_code, self.camera.ctx, center = (0, 0), radius = 0.5, ratio = 0.8)
        dot_1 = DotCloud([ORIGIN]*size, radius = 0.1, color = colors)
        
        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 1*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        for _ in range(30):
            simple_diffusion(dot_1.get_points(), computer = computer_1)

        
        # anchors_1 = Line(3*RIGHT + 2*UP, 2*DOWN + 3*LEFT).get_points()[:, :2]
        back = SVGMobject("smile_face.svg", height = 3, stroke_width = 20, fill_opacity = 0, color = GREY_E)
        anchors_1 = back.get_all_points()[:, :2]
        computer_2 = BezierDiffuse(compute_shader_source, anchors_1, self.camera.ctx, surr = 0.1, ratio = 0.9)
        
        def potential(points: np.ndarray, computer: Diffuse | BezierDiffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.05*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        
        for _ in range(30):
            potential(dot_1.get_points(), computer = computer_2)

        self.add(dot_1).wait()

        colors_g = [interpolate_color(color, GREY_E, 0.5) for color in colors]
        lines = [TracedPath(lambda idx = i: dot_1.get_points()[idx], stroke_width = 0.5, stroke_color = colors_g[i]) for i in range(size)]

        history = [dot_1.get_points().copy()]
        def simple_diffusion(points: np.ndarray):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.1*np.random.randn(length, 2)
            points[:, :2] = points_2d

        def random_updater(mob: Mobject):
            history.append(mob.get_points().copy())
            simple_diffusion(mob.get_points())

        dot_1.add_updater(random_updater)
        self.add_background(*lines).wait(2)
        dot_1.clear_updaters()
        for mob in lines:
            mob.clear_updaters()
        self.wait()
        
        now = dot_1.get_points()
        prev = history.pop()
        arrows = VGroup(*[Arrow(ORIGIN, 0.3*(prev[i] - now[i])/get_norm(prev[i] - now[i]) if get_norm(prev[i] - now[i]) > 1e-6 else ORIGIN, buff = 0, color = colors[i]).shift(now[i]) for i in range(size)])
        self.play(ShowIncreasingSubsets(arrows), run_time = 2, rate_func = linear)
        self.wait()

        def fall_updater(mob, dt):
            mob.shift(mob.v*dt)
            mob.v += 2*DOWN*dt
            if mob.get_y(UP) < 3:
                self.remove(mob)

        center = 4*UP + 8*LEFT
        for i in range(40):
            for j in range(5):
                k = i*5 + j
                offset = center - now[k]
                self.remove(arrows[k])
                the_seed = VGroup(Dot(center, color = colors[k]), arrows[k].copy().shift(offset))
                the_seed.v = 5*(prev[k] - now[k])
                now[k] = prev[k]
                the_seed.add_updater(fall_updater)
                self.add(the_seed)
            self.wait(0, 1)
        self.wait(0, 50)

        now = dot_1.get_points()
        prev = history.pop()
        arrows = VGroup(*[Arrow(ORIGIN, 0.3*(prev[i] - now[i])/get_norm(prev[i] - now[i]) if get_norm(prev[i] - now[i]) > 1e-6 else ORIGIN, buff = 0, color = colors[i]).shift(now[i]) for i in range(size)])
        self.play(ShowIncreasingSubsets(arrows), run_time = 2, rate_func = linear)
        self.wait()

        for k in range(200):
            offset = center - now[k]
            self.remove(arrows[k])
            the_seed = VGroup(Dot(center, color = colors[k]), arrows[k].copy().shift(offset))
            the_seed.v = 5*(prev[k] - now[k])
            now[k] = prev[k]
            the_seed.add_updater(fall_updater)
            self.add(the_seed)
        now = dot_1.get_points()
        if not self.skip_animations:
            prev = history.pop()
        arrows = VGroup(*[Arrow(ORIGIN, 0.3*(prev[i] - now[i])/get_norm(prev[i] - now[i]) if get_norm(prev[i] - now[i]) > 1e-6 else ORIGIN, buff = 0, color = colors[i]).shift(now[i]) for i in range(size)])
        self.add(arrows).wait(2)

        for _ in range(2):
            for k in range(200):
                offset = center - now[k]
                self.remove(arrows[k])
                the_seed = VGroup(Dot(center, color = colors[k]), arrows[k].copy().shift(offset))
                the_seed.v = 5*(prev[k] - now[k])
                now[k] = prev[k]
                the_seed.add_updater(fall_updater)
                self.add(the_seed)
            now = dot_1.get_points()
            if not self.skip_animations:
                prev = history.pop()
            arrows = VGroup(*[Arrow(ORIGIN, 0.3*(prev[i] - now[i])/get_norm(prev[i] - now[i]) if get_norm(prev[i] - now[i]) > 1e-6 else ORIGIN, buff = 0, color = colors[i]).shift(now[i]) for i in range(size)])
            self.add(arrows).wait(1)

        for _ in range(4):
            for k in range(200):
                offset = center - now[k]
                self.remove(arrows[k])
                the_seed = VGroup(Dot(center, color = colors[k]), arrows[k].copy().shift(offset))
                the_seed.v = 5*(prev[k] - now[k])
                now[k] = prev[k]
                the_seed.add_updater(fall_updater)
                self.add(the_seed)
            now = dot_1.get_points()
            if not self.skip_animations:
                prev = history.pop()
            arrows = VGroup(*[Arrow(ORIGIN, 0.3*(prev[i] - now[i])/get_norm(prev[i] - now[i]) if get_norm(prev[i] - now[i]) > 1e-6 else ORIGIN, buff = 0, color = colors[i]).shift(now[i]) for i in range(size)])
            self.add(arrows).wait(0, 15)

        for _ in range(12):
            for k in range(200):
                offset = center - now[k]
                self.remove(arrows[k])
                the_seed = VGroup(Dot(center, color = colors[k]), arrows[k].copy().shift(offset))
                the_seed.v = 5*(prev[k] - now[k])
                now[k] = prev[k]
                the_seed.add_updater(fall_updater)
                self.add(the_seed)
            now = dot_1.get_points()
            if not self.skip_animations:
                prev = history.pop()
            arrows = VGroup(*[Arrow(ORIGIN, 0.3*(prev[i] - now[i])/get_norm(prev[i] - now[i]) if get_norm(prev[i] - now[i]) > 1e-6 else ORIGIN, buff = 0, color = colors[i]).shift(now[i]) for i in range(size)])
            self.add(arrows).wait(0, 5)

        for _ in range(42):
            for k in range(200):
                offset = center - now[k]
                self.remove(arrows[k])
                the_seed = VGroup(Dot(center, color = colors[k]), arrows[k].copy().shift(offset))
                the_seed.v = 5*(prev[k] - now[k])
                now[k] = prev[k]
                the_seed.add_updater(fall_updater)
                self.add(the_seed)
            now = dot_1.get_points()
            if not self.skip_animations:
                prev = history.pop()
            arrows = VGroup(*[Arrow(ORIGIN, 0.3*(prev[i] - now[i])/get_norm(prev[i] - now[i]) if get_norm(prev[i] - now[i]) > 1e-6 else ORIGIN, buff = 0, color = colors[i]).shift(now[i]) for i in range(size)])
            self.add(arrows).wait(0, 3)
        
        self.wait(2, 24)

        self.play(blackbox.animate.shift(2*DOWN))
        self.play(Rotate(blackbox, PI/2, about_point = 12*LEFT + 4*DOWN, run_time = 2), *[FadeOut(mob) for mob in lines + [dot_1]], FadeIn(back))
        self.wait()

        size = 5000
        colors = list(np.random.choice(MANIM_COLORS, size=size))
        colors = [interpolate_color(color, GREY_E, 0.5) for color in colors]

        dot_2 = DotCloud([ORIGIN]*size, radius = 0.02, color = colors)
        
        def simple_diffusion(points: np.ndarray, computer: Diffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 1*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        for _ in range(30):
            simple_diffusion(dot_2.get_points(), computer = computer_1)
        
        def potential(points: np.ndarray, computer: Diffuse | BezierDiffuse):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += 0.05*np.random.randn(length, 2)
            points[:, :2] = computer.compute(points_2d)
        
        for _ in range(30):
            potential(dot_2.get_points(), computer = computer_2)

        data = dot_2.get_points().copy()[:500]
        def multi_brownian(points: np.ndarray, nudge: float = 0.03):

            points_2d = points[:, :2]
            length = len(points_2d)
            points_2d += nudge*np.random.randn(length, 2)
            points[:, :2] = points_2d/np.sqrt(1 + nudge/8)
        
        for i in range(120):
            history.append(dot_2.get_points().copy())
            power = clip(i, 0, 60)/30
            multi_brownian(dot_2.get_points(), nudge = 0.01*3**power)

        def cal_exact_score(sigma, x):
            diff = data - x
            d2 = np.sum(diff**2, axis=1) / (2*sigma)
            d2 -= d2.min()
            kernel = np.exp(- d2)
            kernel /= np.sum(kernel)
            weight_x0 = diff * kernel[:, np.newaxis]
            score = np.sum(weight_x0, axis=0)

            return score/5

        n = 5
        arrows = []
        for i in range(-4*n, 4*n+1):
            for j in range(-4*n, 4*n+1):
                arrow = Arrow(buff = 0, color = GREY_D)
                arrow.position = (i*RIGHT + j*UP)/n
                score = cal_exact_score(1, arrow.position)
                norm = get_norm(score)
                if norm > 1/n:
                    score /= norm*n
                arrow.become(Arrow(arrow.position, arrow.position + score, buff = 0))
                arrow.set_color(ratio_color(1 - clip(norm, 0, 1)))
                arrows.append(arrow)
                
        self.add(*arrows).play(LaggedStart(*[mob.save_state().move_to(8*LEFT).animate.restore() for mob in arrows], lag_ratio = 0.005, run_time = 4, group = VGroup(), remover = True))
        self.wait()

        def reverse_updater(mob: Mobject):
            try:
                points = history.pop()
                mob.set_points(points)
            except IndexError:
                mob.clear_updaters()
        self.play(ShowIncreasingPoints(dot_2, run_time = 2))
        self.wait()
        dot_2.add_updater(reverse_updater)
        beta = ValueTracker(1.0)
        def arrow_updater(mob: Arrow):
            score = cal_exact_score(max(0.005, beta.get_value()), mob.position)
            norm = get_norm(score)
            if norm > 1/n:
                score /= norm*n
            mob.become(Arrow(mob.position, mob.position + score, buff = 0))
            mob.set_color(ratio_color(1 - clip(norm, 0, 1)))
                
        for arrow in arrows:
            arrow.add_updater(arrow_updater)
        self.play(beta.animate.set_value(0), run_time = 4)
        for arrow in arrows:
            arrow.clear_updaters()
        self.wait()

#################################################################### 

class Video_7_1(FrameScene):
    def construct(self):
        func = lambda x: 2*np.sin(x) - x/PI
        S = FunctionGraph(func, [-PI, PI, PI/100], stroke_width = 20, color = GREY_E).rotate(-PI/2).shift(0.5*UP)
        positions = [np.array([-func(y), y + 0.5, 0]) for y in [*np.random.rand(10)*TAU-PI, *np.linspace(-PI, PI, 10)]]
        points = [Dot(position) for position in positions]
        # origins = [point.copy().set_color(GREY_E) for point in points]
        # self.add(*origins, *points)
        # self.activate_test_grid()
        


#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        