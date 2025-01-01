from __future__ import annotations

from manimlib import *
import numpy as np
from pydub import AudioSegment
        
#################################################################### 

class ImageMesh(ImageMobject):
    CONFIG = {
        "u_range": (0, 1),
        "v_range": (0, 1),
        "resolution": (11, 11),
        "uv_func": lambda u, v: (u, v, 0.0), 
        "rescale": False
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_triangle_indices()

    def init_points(self):
        nu, nv = self.resolution

        u_samples, v_samples = np.linspace(*self.u_range, nu), np.linspace(*self.v_range, nv)
        uv_grid = np.array([self.uv_func(u, v) for v in v_samples for u in u_samples])
        self.set_points(uv_grid)

        u_samples, v_samples = np.linspace(0, 1, nu), np.linspace(1, 0, nv)
        self.data["im_coords"] = np.array([[u, v] for v in v_samples for u in u_samples])

        if self.rescale:
            size = self.image.size
            self.set_width(size[0] / size[1], stretch=True)
            self.set_height(self.height)

    def compute_triangle_indices(self):
        # TODO, if there is an event which changes
        # the resolution of the surface, make sure
        # this is called.
        nu, nv = self.resolution
        if nu == 0 or nv == 0:
            self.shader_indices = np.zeros(0, dtype=int)
            return
        index_grid = np.arange(nu * nv).reshape((nu, nv))
        indices = np.zeros(6 * (nu - 1) * (nv - 1), dtype=int)
        indices[0::6] = index_grid[:-1, :-1].flatten()  # Top left
        indices[1::6] = index_grid[+1:, :-1].flatten()  # Bottom left
        indices[2::6] = index_grid[:-1, +1:].flatten()  # Top right
        indices[3::6] = index_grid[:-1, +1:].flatten()  # Top right
        indices[4::6] = index_grid[+1:, :-1].flatten()  # Bottom left
        indices[5::6] = index_grid[+1:, +1:].flatten()  # Bottom right
        self.shader_indices = indices # I have no idea why this is self.triangle_indices in Surface

class Patch_Book(FrameScene):
    CONFIG = {
        "camera_class": AACamera
    }
    def construct(self):
        book = ImageMobject(r"book.jpg", height = 6).shift(0.5*UP)
        photo = ImageMobject(r"photo.jpg", height = 6).shift(0.5*UP + 3.5*RIGHT).save_state().set_width(2.58).next_to(3.5*UP + 2.09*RIGHT, DL, buff = 0)
        self.add(book, photo).wait()# .activate_test_grid().wait()
        self.play(book.animate.shift(3.5*LEFT), photo.animate.restore())
        self.wait()

        photo_0 = ImageMobject(r"photo.jpg", height = 6).set_width(2.58).next_to(3.5*UP + 2.09*RIGHT + 3.5*LEFT, DL, buff = 0)
        points = photo_0.get_points()
        surr_photo = Polygon(points[0], points[1], points[3], points[2], color = YELLOW, anti_alias_width = 150)
        points = [np.array([3.17, -0.75, 0]), np.array([4.19, 0.32, 0]), np.array([3.58, -1.94, 0]), np.array([4.7, -0.86, 0])]
        def perspective(*points: np.ndarray):
            A, B, C, D = [np.array([point[0], point[1], 1]) for point in points]
            l_AB, l_CD, l_AC, l_BD = cross(A, B), cross(C, D), cross(A, C), cross(B, D)
            E, F = cross(l_AB, l_CD), cross(l_AC, l_BD)
            l_EF = cross(E, F)
            ratio_h = np.linalg.solve(np.array([[l_AB[0], l_CD[0]], [l_AB[1], l_CD[1]]]), l_EF[:2])
            ratio_v = np.linalg.solve(np.array([[l_AC[0], l_BD[0]], [l_AC[1], l_BD[1]]]), l_EF[:2])
            # print(l_EF, ratio_h, ratio_v)
            # print(ratio_h[0]*l_AB + ratio_h[1]*l_CD)
            # print(ratio_v[0]*l_AC + ratio_v[1]*l_BD)
            lambda_h, lambda_v = ratio_h[1]/ratio_h[0], ratio_v[1]/ratio_v[0]
            def util(alpha: float, beta: float):
                # alpha, beta, _ = point
                h = (lambda_h*alpha, alpha-1)
                v = (lambda_v*beta, beta-1)
                # coor_h, coor_v = h/(1+h), v/(1+v)
                l_h, l_v = h[1]*l_AB + h[0]*l_CD, v[1]*l_AC + v[0]*l_BD
                target = cross(l_h, l_v)
                return np.array([target[0]/target[2], target[1]/target[2], 0])
            return util
        surr_book = Polygon(points[1], points[0], points[2], points[3], color = YELLOW, stroke_witdh = 8, anti_alias_width = 50)
        book_0 = ImageMesh(filename = r"book.jpg", uv_func = perspective(*points)).save_state()
        book_1 = ImageMesh(filename = r"book.jpg", rescale = True, height = 6).move_to(book)
        hand = ImageMobject(r"hand.png", height = 6).shift(0.5*UP + 3.5*RIGHT)
        self.add_text(hand).play(FadeIn(book_0))
        self.wait()
        self.play(TransformFromCopy(book_0, book_1, remover = True))
        self.wait()

        
        arrow_1 = Arrow(1.4*LEFT + 0.5*UP, 1.5*RIGHT + 0.5*UP, stroke_width = 10, path_arc = -PI/6)
        arrow_2 = Arrow(1.5*RIGHT + 0.5*DOWN, 1.4*LEFT + 0.5*DOWN, stroke_width = 10, path_arc = -PI/6)
        self.add(surr_photo, surr_book, photo_0, book_0).play(ShowCreation(arrow_1), ShowCreation(arrow_2), FadeIn(surr_photo), FadeIn(surr_book))
        self.wait()

        # book_0 = ImageMobject(r"book.jpg").set_points([points[1], points[0], points[3], points[2]])
        # book_1 = ImageMobject(r"book.jpg", height = 6).move_to(book)
        # hand = ImageMobject(r"hand.png", height = 6).shift(0.5*UP + 3.5*RIGHT)
        # self.add(book_0).add_text(hand).wait()
        # self.play(TransformFromCopy(book_0, book_1, remover = True))
        # self.wait() Consolas

class Patch_Car(FrameScene):
    def construct(self):
        car = SVGMobject("car.svg", **background_dic, fill_color = RED).shift(UP)
        factory = SVGMobject("factory.svg", **background_dic, fill_color = LIGHT_BROWN, height = 4).shift(4*LEFT + UP).set_stroke(**stroke_dic)
        self.play(GrowFromCenter(car))
        self.wait(2)
        self.play(FadeIn(factory, RIGHT), car.animate.scale(0.5).shift(3*RIGHT + DOWN))
        self.wait(2)

        ge = MTex(r">").scale(3).shift(0.25*RIGHT)
        self.play(FadeIn(ge, RIGHT), car.animate.shift(0.5*RIGHT))
        self.wait(2)

        car_fact = ImageMobject("car_fact.png", height = 3).shift(1.0*DOWN + 0.5*LEFT)
        source_1 = np.array([-3.0, -0.5, 0])
        line_1 = Line(source_1, car_fact.get_corner(LEFT) + 0.1*RIGHT, color = GREY).add(Dot(source_1, color = GREY))
        background_1 = Line(source_1, car_fact.get_corner(LEFT) + 0.1*RIGHT, stroke_width = 8, color = BLACK).add(Dot(source_1, radius = 0.12, color = BLACK))
        self.play(*[GrowFromPoint(mob, source_1) for mob in [background_1, line_1, car_fact]], *[mob.animate.shift(1.5*UP) for mob in [ge, car]])
        self.wait(2)

        car_small = car.copy().set_color(RED_A).scale(0.5).shift(3*DOWN)
        arrow_car = Arrow(car, car_small, stroke_width = 10, color = GREY)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(width = 10).set_color(RED).scale(0.25).move_to(arrow_car)
        impossible = Text("Impossible!", font = "Times New Roman", color = RED).next_to(car, UP, buff = 1.0)
        self.play(GrowArrow(arrow_car), GrowFromPoint(car_small, arrow_car.get_start()))
        self.play(ShowCreation(cross), Write(impossible))
        self.wait(2)

        bacteria = SVGMobject("bacteria.svg", **background_dic, fill_color = GREEN_E).shift(1.5*UP + 13*RIGHT)
        bacteria_small = bacteria.copy().set_color(GREEN_A).scale(0.5).shift(3*DOWN)
        arrow_bacteria = Arrow(bacteria, bacteria_small, stroke_width = 10, color = WHITE)
        hen = SVGMobject("hen.svg", **background_dic, fill_color = GOLD).shift(1.5*UP + 9*RIGHT)
        egg = SVGMobject("egg.svg", **background_dic, fill_color = GOLD_A).shift(1.5*UP + 9*RIGHT).scale(0.5).shift(3*DOWN)
        arrow_chicken = Arrow(hen, egg, stroke_width = 10, color = WHITE)
        possible = Text("Possible!", font = "Times New Roman", color = GREEN).match_y(impossible).set_x(11)
        self.add(self.shade, car, car_small, arrow_car, cross, impossible, bacteria, bacteria_small, arrow_bacteria, hen, egg, arrow_chicken, possible
                 ).play(self.camera.frame.animating(run_time = 2).shift(9*RIGHT), *[mob.animate.shift(2*RIGHT) for mob in [car, car_small, arrow_car, cross, impossible]], 
                        FadeIn(self.shade))
        self.remove(factory, ge, car_fact, line_1, background_1, self.shade).wait(2)

        question_mark = MTex(r"???").scale(8).rotate(PI/12).shift(9*RIGHT).set_stroke(**stroke_dic)
        self.play(FadeIn(question_mark, scale = 0.5))
        self.wait(2)
        
KEYWORD = "#C586C0" # 197 134 192
DEFAULT = "#569CD6" # 86 156 214
VARIABLE = "#9CDCFE" # 156 220 254
CONSTANT = "#4FC1FF" # 79 193 255
FUNCTION = "#DCDCAA" # 220 220 170
CLASS = "#4EC980" # 78 201 176
SYMBOL = "#D4D4D4" # 212 212 212
NUMBER = "#B5CEA8" # 181 206 168
STRING = "#CE9178" # 206 145 120
ESCAPE = "#D7BA7D" # 215 186 125
COMMENT = "#6A9955" # 106 153 85
BRACKET1 = "#FFD700" # 255 215 0
BRACKET2 = "#DA70D6" #218 112 214
BRACKET3 = "#179FFF" #23 159 255
VSCODE_COLORS = [KEYWORD, DEFAULT, VARIABLE, CONSTANT, FUNCTION, CLASS, SYMBOL, NUMBER, STRING, ESCAPE, COMMENT, BRACKET1, BRACKET2, BRACKET3]

#################################################################### 

class FeedBack(Mobject):
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
    def __init__(self, delay: int, **kwargs):
        self.delay = delay
        self.texture_paths = {"Texture": str(delay)}
        super().__init__(**kwargs)
        
    def init_points(self) -> None:
        self.set_width(2*16/9, stretch=True)
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
    
class FeedBackScene(FrameScene):
    CONFIG = {
        "transparent": False,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lagged_frames: list[Image.Image] = [self.camera.get_image()]
        self.feedbacks: list[FeedBack] = []
        self.max_delay: int = 1
        self.delays: list[int] = []

    def add_feedback(self, *feedbacks: FeedBack):
        self.feedbacks.extend(feedbacks)
        for feedback in feedbacks:
            delay = feedback.delay
            if delay > self.max_delay:
                self.lagged_frames.extend([self.lagged_frames[-1] for _ in range(delay - self.max_delay)])
            if delay not in self.delays:
                if self.camera.n_textures == 15:  # I have no clue why this is needed
                    self.camera.n_textures += 1
                tid = self.camera.n_textures
                self.camera.n_textures += 1
                
                self.delays.append(delay)
                im = self.lagged_frames[delay - 1]
                texture = self.camera.ctx.texture(
                        size=im.size,
                        components=len(im.getbands()),
                        data=im.tobytes(),
                    )
                texture.use(location=tid)
                self.camera.path_to_texture[str(delay)] = (tid, texture)
        return self
            
    def refresh(self):
        self.lagged_frames.remove(self.lagged_frames[-1])
        if self.transparent:
            background = self.camera.background_rgba
            self.camera.background_rgba[3] = 0
            self.camera.clear()
            self.camera.capture(*self.get_all_mobjects())
            self.camera.background_rgba = background
        self.lagged_frames = [self.camera.get_image()] + self.lagged_frames
        for delay in self.delays:
            self.camera.path_to_texture[str(delay)][1].write(data=self.lagged_frames[delay - 1].tobytes())
        super().refresh()

class Recursive_1(FeedBackScene):
    def construct(self):
        title = Title("无限递归")
        titleline = TitleLine()
        screen_1 = FeedBack(delay = 3, height = 5.6).shift(0.1*DOWN)
        rectangle = SurroundingRectangle(screen_1, buff = 0.1)
        self.add_feedback(screen_1).add(screen_1).play(Write(title), GrowFromCenter(titleline))
        self.wait(2)
        self.play(ShowCreation(rectangle))
        self.wait(2)
        self.play(rectangle.animate.set_width(FRAME_WIDTH - 0.04).set_height(FRAME_HEIGHT - 0.04, stretch = True).move_to(ORIGIN))
        self.wait(2)
        
class Recursive_2(FeedBackScene):
    def construct(self):
        screen_1 = FeedBack(delay = 3).shift(RIGHT_SIDE/2 + TOP/2)
        screen_2 = FeedBack(delay = 8).shift(LEFT_SIDE/2 + TOP/2)
        self.add_feedback(screen_1, screen_2)
        square = Square(stroke_width = 10).shift(5*RIGHT + 2.5*DOWN)
        self.play(ShowCreation(square))
        self.wait()
        self.add(screen_1, screen_2).wait(2)

class Patch_2(FrameScene):
    def construct(self):
        surr_1 = Rectangle(height = FRAME_HEIGHT/2, width = FRAME_WIDTH/2, color = GREY).shift(FRAME_HEIGHT/4*UP + FRAME_WIDTH/4*RIGHT)
        surr_2 = Rectangle(height = FRAME_HEIGHT/2, width = FRAME_WIDTH/2, color = GREY).shift(FRAME_HEIGHT/4*UP + FRAME_WIDTH/4*LEFT)
        self.play(ShowCreation(surr_1), ShowCreation(surr_2))
        self.wait()

class Recursive_3(FeedBackScene):
    def construct(self):
        self.transparent = True
        screen_1 = FeedBack(delay = 5, height = 8).apply_matrix(np.array([[1/2, 1/2], [-1/2, 1/2]])).shift(0.5*UP + 1.5*RIGHT)#.scale(1.08, about_point = DOWN)
        screen_2 = FeedBack(delay = 5, height = 8).apply_matrix(np.array([[1/2, -1/2], [1/2, 1/2]])).shift(0.5*UP + 1.5*LEFT)#.scale(1.08, about_point = DOWN)
        self.add_feedback(screen_1, screen_2).add(screen_1, screen_2).wait()
        line = Line(3*DOWN, DOWN, stroke_width = 40)
        self.play(ShowCreation(line), run_time = 1/3, rate_func = rush_from, frames = 10)
        self.wait(2, 20)
        # self.add(screen_1, screen_2).wait(2)
        
class Patch_3(FrameScene):
    def construct(self):
        surr_1 = Rectangle(height = FRAME_HEIGHT*0.75, width = FRAME_WIDTH*0.75, color = GREY).apply_matrix(np.array([[1/2, 1/2], [-1/2, 1/2]])).shift(0.5*UP + 1.5*RIGHT)
        surr_2 = Rectangle(height = FRAME_HEIGHT*0.75, width = FRAME_WIDTH*0.75, color = GREY).apply_matrix(np.array([[1/2, -1/2], [1/2, 1/2]])).shift(0.5*UP + 1.5*LEFT)
        surr_0 = Rectangle(height = FRAME_HEIGHT*0.75, width = FRAME_WIDTH*0.75, color = GREY_D, stroke_width = 10)
        self.play(FadeIn(surr_0), ShowCreation(surr_1), ShowCreation(surr_2))
        self.wait()

class Recursive_4(FeedBackScene):
    def construct(self):
        self.transparent = True
        screen_1 = FeedBack(delay = 10, height = 4).shift(1.5*UP + 0.25*DOWN).shift(0.5*UP)#.scale(1.08, about_point = DOWN)
        screen_2 = FeedBack(delay = 10, height = 4).shift(1.5*UP + 0.25*DOWN).rotate(PI*2/3, about_point = DOWN).shift(0.5*UP)#.scale(1.08, about_point = DOWN)
        screen_3 = FeedBack(delay = 10, height = 4).shift(1.5*UP + 0.25*DOWN).rotate(-PI*2/3, about_point = DOWN).shift(0.5*UP)
        self.add_feedback(screen_1, screen_2, screen_3).add(screen_1, screen_2, screen_3).wait()
        triangle = RegularPolygon(3, fill_color = WHITE, **background_dic).center().set_height(6)
        triangle.add(RegularPolygon(3, fill_color = BLACK, **background_dic).set_height(3).move_to(1.5*DOWN).rotate(PI)).shift(0.5*UP)
        self.bring_to_back(triangle).play(GrowFromPoint(triangle, DOWN), run_time = 2/3, rate_func = rush_from, frames = 20)
        # self.play(triangle.animate.set_stroke(width = 20), run_time = 1, frames = 30)
        self.wait(3, 10)
        # self.add(screen_1, screen_2).wait(2)

class Patch_4(FrameScene):
    def construct(self):
        self.camera.frame.shift(0.5*DOWN)
        surr_1 = Rectangle(height = FRAME_HEIGHT*0.75, width = FRAME_WIDTH*0.75, color = GREY).scale(0.5).shift(1.5*UP)
        surr_2 = Rectangle(height = FRAME_HEIGHT*0.75, width = FRAME_WIDTH*0.75, color = GREY).scale(0.5).shift(1.5*UP).rotate(PI*2/3, about_point = DOWN)
        surr_3 = Rectangle(height = FRAME_HEIGHT*0.75, width = FRAME_WIDTH*0.75, color = GREY).scale(0.5).shift(1.5*UP).rotate(-PI*2/3, about_point = DOWN)
        surr_0 = Rectangle(height = FRAME_HEIGHT*0.75, width = FRAME_WIDTH*0.75, color = GREY_D, stroke_width = 10)
        self.play(FadeIn(surr_0), ShowCreation(surr_1), ShowCreation(surr_2), ShowCreation(surr_3))
        self.wait()
        
#################################################################### 
        
class TRTC_1(FrameScene):
    def construct(self):
        X = MTex("X:").scale(3).move_to(5*LEFT)
        self.play(Write(X))
        self.wait()
        mountain = SVGMobject("mountain.svg", fill_color = GREEN).set_stroke(**stroke_dic).move_to(2*LEFT + 1.5*DOWN)
        self.play(Write(mountain))
        self.wait()
        source_1 = np.array([-1.8, -1.1, 0])
        temple = SVGMobject("temple.svg", fill_color = DARK_BROWN).set_stroke(**stroke_dic).move_to(0*LEFT + 1.5*UP)
        line_1 = Line(source_1, temple.get_corner(DL) + 0.1*DR, color = DARK_BROWN).add(Dot(source_1, color = DARK_BROWN))
        background_1 = Line(source_1, temple.get_corner(DL) + 0.1*DR, stroke_width = 8, color = BLACK).add(Dot(source_1, radius = 0.12, color = BLACK))
        self.play(GrowFromPoint(background_1, source_1), GrowFromPoint(line_1, source_1), GrowFromPoint(temple, source_1))
        self.wait()
        source_2 = np.array([0, 0.7, 0])
        old = SVGMobject("old monk.svg", color = GOLD).move_to(2*RIGHT + 1.5*DOWN)
        young = SVGMobject("little monk.svg", color = GOLD).move_to(3.5*RIGHT + 1.5*DOWN).scale(0.8, about_edge = DOWN)
        line_2 = Line(source_2, old.get_corner(UL) + 0.1*DR, color = GOLD).add(Dot(source_2, color = GOLD))
        background_2 = Line(source_2, old.get_corner(UL) + 0.1*DR, stroke_width = 8, color = BLACK).add(Dot(source_2, radius = 0.12, color = BLACK))
        self.play(*[GrowFromPoint(mob, source_2) for mob in [background_2, line_2, old, young, ]])
        self.wait()

        bubble = Polygon(2*RIGHT + 0.25*DOWN, 2.25*RIGHT + 0.5*UP, 2*RIGHT+0.5*UP, 2*RIGHT+2*UP, 4*RIGHT+2*UP, 4*RIGHT+0.5*UP, 2.75*RIGHT+0.5*UP)
        recursive = MTex("X").move_to(3*RIGHT + 1.25*UP)
        self.play(GrowFromPoint(bubble, 2*RIGHT + 0.25*DOWN), GrowFromPoint(recursive, 2*RIGHT + 0.25*DOWN))
        self.wait()

        rectangle = Polygon(3*DOWN + 3.5*LEFT, 3*UP + 3.5*LEFT, 3*UP + 4.5*RIGHT, 3*DOWN + 4.5*RIGHT, srtoke_width = 8, stroke_color = GREY)
        self.play(ShowCreation(rectangle))
        self.wait()

        copy = VGroup(rectangle.copy(), mountain.copy(), background_1.copy().set_submobjects([]), line_1.copy().set_submobjects([]), temple.copy(), background_2.copy().set_submobjects([]), line_2.copy().set_submobjects([]), old.copy(), young.copy(), bubble.copy(), recursive)
        copy.generate_target().scale(0.25).move_to(3*RIGHT + 1.25*UP)
        copy.target[0].set_stroke(width = 0, opacity = 0), copy.target[-2].set_stroke(width = 2)
        self.bring_to_back(copy).play(MoveToTarget(copy))
        self.wait()

        copy_2 = copy.copy()[:-1].add(copy[-1])
        copy_2.generate_target().scale(0.25).move_to(((3+2.5*0.25)*RIGHT + 1.25*5/4*UP))
        copy_2.target[-2].set_stroke(width = 1)
        self.bring_to_back(copy_2).play(MoveToTarget(copy_2))
        self.wait()

class TRTC_2(FrameScene):
    def construct(self):
        title = Text("TRTC", color = YELLOW).next_to(3*UP, UP)
        titleline = TitleLine()
        self.play(Write(title), GrowFromCenter(titleline))
        self.wait()

        trtc_1 = Text("The Recursive TRTC Creation").shift(2*UP)
        self.play(ReplacementTransform(title[0].replicate(3), trtc_1[0:3]), ReplacementTransform(title[1].replicate(9), trtc_1[3:12]), 
                  ReplacementTransform(title[2].replicate(4), trtc_1[12:16]), ReplacementTransform(title[3].replicate(8), trtc_1[16:]))
        self.wait()
        small_1 = SurroundingRectangle(trtc_1[12:16], color = BLUE_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_1, trtc_1).play(ShowCreation(small_1))
        self.wait()

        trtc_2 = Text("The Recursive TRTC Creation").shift(0.6*UP)
        big_2 = SurroundingRectangle(trtc_2, buff = 0.3, color = BLUE_A).set_fill(opacity = 1, color = BLACK)
        line_1 = Line(color = BLUE_A).add_updater(lambda mob: mob.put_start_and_end_on(small_1.get_corner(DL), big_2.get_corner(UL)))
        line_2 = Line(color = BLUE_A).add_updater(lambda mob: mob.put_start_and_end_on(small_1.get_corner(DR), big_2.get_corner(UR)))
        self.add(line_1, line_2, big_2).play(TransformFromCopy(small_1, big_2), 
                    ReplacementTransform(trtc_1[12].replicate(3), trtc_2[0:3]), ReplacementTransform(trtc_1[13].replicate(9), trtc_2[3:12]), 
                    ReplacementTransform(trtc_1[14].replicate(4), trtc_2[12:16]), ReplacementTransform(trtc_1[15].replicate(8), trtc_2[16:]))
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_2 = SurroundingRectangle(trtc_2[12:16], color = RED_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_2, trtc_2).play(ShowCreation(small_2))
        self.wait()

        trtc_3 = Text("The Recursive TRTC Creation").shift(1.2*DOWN)
        big_3 = SurroundingRectangle(trtc_3, buff = 0.3, color = RED_A).set_fill(opacity = 1, color = BLACK)
        line_1 = Line(color = RED_A).add_updater(lambda mob: mob.put_start_and_end_on(small_2.get_corner(DL), big_3.get_corner(UL)))
        line_2 = Line(color = RED_A).add_updater(lambda mob: mob.put_start_and_end_on(small_2.get_corner(DR), big_3.get_corner(UR)))
        self.add(line_1, line_2, big_3).play(TransformFromCopy(small_2, big_3), 
                    ReplacementTransform(trtc_2[12].replicate(3), trtc_3[0:3]), ReplacementTransform(trtc_2[13].replicate(9), trtc_3[3:12]), 
                    ReplacementTransform(trtc_2[14].replicate(4), trtc_3[12:16]), ReplacementTransform(trtc_2[15].replicate(8), trtc_3[16:]))
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_3 = SurroundingRectangle(trtc_3[12:16], color = YELLOW_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_3, trtc_3).play(ShowCreation(small_3))
        self.wait()

        trtc_4 = Text("The Recursive TRTC Creation").shift(3*DOWN)
        big_4 = SurroundingRectangle(trtc_4, buff = 0.3, color = YELLOW_A).set_fill(opacity = 1, color = BLACK)
        line_1 = Line(color = YELLOW_A).add_updater(lambda mob: mob.put_start_and_end_on(small_3.get_corner(DL), big_4.get_corner(UL)))
        line_2 = Line(color = YELLOW_A).add_updater(lambda mob: mob.put_start_and_end_on(small_3.get_corner(DR), big_4.get_corner(UR)))
        self.add(line_1, line_2, big_4).play(TransformFromCopy(small_3, big_4), 
                    ReplacementTransform(trtc_3[12].replicate(3), trtc_4[0:3]), ReplacementTransform(trtc_3[13].replicate(9), trtc_4[3:12]), 
                    ReplacementTransform(trtc_3[14].replicate(4), trtc_4[12:16]), ReplacementTransform(trtc_3[15].replicate(8), trtc_4[16:]))
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_4 = SurroundingRectangle(trtc_4[12:16], color = GREEN_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_4, trtc_4).play(ShowCreation(small_4))
        self.wait()

        trtc_5 = Text("The Recursive TRTC Creation").shift(4.8*DOWN)
        big_5 = SurroundingRectangle(trtc_5, buff = 0.3, color = GREEN_A).set_fill(opacity = 1, color = BLACK)
        line_1 = Line(color = GREEN_A).add_updater(lambda mob: mob.put_start_and_end_on(small_4.get_corner(DL), big_5.get_corner(UL)))
        line_2 = Line(color = GREEN_A).add_updater(lambda mob: mob.put_start_and_end_on(small_4.get_corner(DR), big_5.get_corner(UR)))
        self.add(line_1, line_2, big_5).play(TransformFromCopy(small_4, big_5), 
                    ReplacementTransform(trtc_4[12].replicate(3), trtc_5[0:3]), ReplacementTransform(trtc_4[13].replicate(9), trtc_5[3:12]), 
                    ReplacementTransform(trtc_4[14].replicate(4), trtc_5[12:16]), ReplacementTransform(trtc_4[15].replicate(8), trtc_5[16:]))
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_5 = SurroundingRectangle(trtc_5[12:16], color = BLUE_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_5, trtc_5).play(ShowCreation(small_5))
        self.wait()

#################################################################### 
        
class Quine_1(FrameScene):
    def construct(self):
        shade = Shade(fill_color = BLACK).append_points(Rectangle(width = 12.0, height = 3.5).shift(1.75*UP).reverse_points().get_points())
        surr = Rectangle(width = 12.2, height = 3.7).shift(1.75*UP)
        divide_line = Line(0.5*DOWN, 2.5*DOWN, color = GREY)
        title_code = Heiti("代码", color = YELLOW).scale(1.2)
        title_code[0].move_to(6.5*LEFT + DOWN), title_code[1].move_to(6.5*LEFT + 2*DOWN)
        title_print = Heiti("输出", color = YELLOW).scale(1.2)
        title_print[0].move_to(6.5*RIGHT + DOWN), title_print[1].move_to(6.5*RIGHT + 2*DOWN)
        self.bring_to_back(shade, surr, divide_line, title_code, title_print).wait()

        # print(open(__file__).read())
        sound_0, sound_1 = AudioSegment.from_file("sound_0.mp3"), AudioSegment.from_file("sound_1.mp3")
        code_0 = Code(r"print(open(__file__).read())", t2c = {(r"print", r"open", r"read"): FUNCTION, r"__file__": VARIABLE, r".": SYMBOL}).next_to(1.5*DOWN + 5.5*LEFT)
        print_0 = Code(r"print(open(__file__).read())").set_color(SYMBOL).next_to(1.5*DOWN + 0.5*RIGHT)
        color_map = {(5, 27): BRACKET1, (10, 19, 25, 26): BRACKET2}
        for key, value in color_map.items():
            for index in key:
                code_0[index].set_color(value)
        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.play(ShowIncreasingSubsets(code_0))
        self.wait()
        line_0 = Underline(code_0.select_part("__file__"), stroke_width = 2, color = VARIABLE)
        line_1 = Underline(code_0.select_part("open"), stroke_width = 2, color = FUNCTION).match_y(line_0)
        line_2 = Underline(code_0.select_part("read"), stroke_width = 2, color = FUNCTION).match_y(line_0)
        line_3 = Underline(code_0.select_part("print"), stroke_width = 2, color = FUNCTION).match_y(line_0)
        text_0 = Songti("这个代码文件", color = VARIABLE).scale(1/3).next_to(line_0, DOWN, buff = 0.1).save_state().next_to(line_0, UP, buff = 0.1)
        text_1 = Songti("打开", color = FUNCTION).scale(1/3).next_to(line_1, DOWN, buff = 0.1).save_state().next_to(line_1, UP, buff = 0.1)
        text_2 = Songti("获取文件内容\n （字符串）", color = FUNCTION).scale(1/3).next_to(line_2.get_left() + 0.1*LEFT, DR, buff = 0.1).save_state().next_to(line_2.get_left() + 0.1*LEFT, UR, buff = 0.1)
        text_3 = Songti("输出传入的\n　字符串", color = FUNCTION).scale(1/3).next_to(line_3.get_right() + 0.1*RIGHT, DL, buff = 0.1).save_state().next_to(line_3.get_right() + 0.1*RIGHT, UL, buff = 0.1)
        back = BackgroundRectangle(VGroup(code_0, line_0, line_1, line_2, line_3, text_0, text_1, text_2, text_3), buff = 0.05)
        # self.play(LaggedStart(*[GrowFromPoint(mob, mob[0].get_center(), rate_func = rush_from) for mob in [text_0, text_1, text_2, text_3]], rate_func = linear, lag_ratio = 1/3))
        self.add_background(text_0, text_1, text_2, text_3, back
            ).play(LaggedStart(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0, line_1, line_2, line_3]], rate_func = linear, lag_ratio = 1/3), 
                   LaggedStart(*[mob.animating(rate_func = rush_from).restore() for mob in [text_0, text_1, text_2, text_3]], rate_func = linear, lag_ratio = 1/3, group = VGroup()))
        self.remove(back).wait()
        self.file_writer.add_audio_segment(sound_1, time = self.get_time())
        self.add(print_0).wait()
        self.play(*[FadeOut(mob) for mob in [line_0, line_1, line_2, line_3, text_0, text_1, text_2, text_3, code_0, print_0]])
        self.wait()
        self.play(*[Flash(point, line_length = 0.6, flash_radius = 1.2, line_stroke_width = 5) for point in [1.5*DOWN + 3.5*LEFT, 1.5*DOWN + 3.5*RIGHT]])
        self.wait()

        # s = "..."
        # print(s)
        code_1 = Code("s = \"...\"\nprint(s)", t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, (r"(", r")"): BRACKET1, "\"...\"": STRING}).next_to(1.5*DOWN + 5.5*LEFT)
        print_1 = Code(r"...").set_color(SYMBOL).next_to(1.5*DOWN + 0.5*RIGHT)
        self.file_writer.add_audio_segment(sound_0[700:1100], time = self.get_time())
        self.play(ShowIncreasingSubsets(VGroup(*code_1[7:13], code_1[14])), run_time = 0.5)
        self.wait()
        self.file_writer.add_audio_segment(sound_0[:600], time = self.get_time())
        self.play(ShowIncreasingSubsets(VGroup(*code_1[:7], code_1[13])), run_time = 0.5)
        self.wait()
        self.file_writer.add_audio_segment(sound_1, time = self.get_time())
        self.add(print_1).wait()

        equal = MTex(r"=", color = YELLOW).next_to(print_1)
        mimic_1 = code_1.copy().set_color(SYMBOL).next_to(equal)
        self.play(Write(equal), TransformFromCopy(code_1, mimic_1, path_arc = -PI/3))
        self.wait()
        # s = "s = \"...\"\nprint(s)"
        # print(s)
        code_2 = Code("s = \"s = \\\"...\\\"\\nprint(s)\"\nprint(s)", 
                      t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, ("\\\"", "\\n"): ESCAPE, (r"(", r")"): BRACKET1}
                      ).next_to(1.5*DOWN + 5.5*LEFT)
        code_2[2:23].set_color(STRING)
        code_2.set_color_by_text(("\\\"", "\\n"), ESCAPE)
        print_2 = Code("s = \"...\"\nprint(s)").set_color(SYMBOL).next_to(1.5*DOWN + 0.5*RIGHT)
        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.remove(code_1[3:6]).play(Transform(code_1[6], code_2[22]), ShowIncreasingSubsets(code_2[3:22]))
        self.remove(code_1).add(code_2).wait()
        parts = [code_2.select_part("\\n"), code_2.select_parts("\\\"")]
        line_0 = Underline(parts[0], stroke_width = 2, color = ESCAPE)
        line_1 = Underline(parts[1][0], stroke_width = 2, color = ESCAPE).match_y(line_0)
        line_2 = Underline(parts[1][1], stroke_width = 2, color = ESCAPE).match_y(line_0)
        text_0 = Songti("输出回车", color = ESCAPE).scale(1/3).next_to(parts[0], UP, buff = 0.15).shift(0.3*RIGHT).save_state().move_to(parts[0]).shift(0.3*RIGHT)
        text_1 = Songti("输出引号", color = ESCAPE).scale(1/3).next_to(parts[1], UP, buff = 0.15).save_state().move_to(parts[1])
        back = BackgroundRectangle(VGroup(code_2, line_0, line_1, line_2, text_0, text_1), buff = 0.05)
        self.add_background(text_0, text_1, back
            ).play(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0, line_1, line_2]], 
                   *[mob.animating(rate_func = rush_from).restore() for mob in [text_0, text_1]])
        self.remove(back).wait()
        self.file_writer.add_audio_segment(sound_1, time = self.get_time())
        self.remove(print_1, equal, mimic_1).add(print_2).wait()
        
        self.play(IndicateAround(code_2[2:23]), IndicateAround(print_2[2:7]))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [line_0, line_1, line_2, text_0, text_1, divide_line, print_2, title_print]], )
        self.wait()

        s = "s = \"s = \\\"...\\\"\\nprint(s)\"\nprint(s)"
        print(s)
        code_3 = Code("s = \"s = \\\"s = \\\\\\\"...\\\\\\\"\\\\nprint(s)\\\"\\nprint(s)\"\nprint(s)", 
                      t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, ("\\\"", "\\n", "\\"): ESCAPE, (r"(", r")"): BRACKET1}
                      ).next_to(1.5*DOWN + 5.5*LEFT)
        # self.add(code_3)#, index_labels(code_3))
        code_3[2:44].set_color(STRING)
        code_3.set_color_by_text(("\\\"", "\\n", "\\"), ESCAPE)
        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.remove(code_2[7:10]).play(Transform(code_2[10:23], code_3[31:44]), ShowIncreasingSubsets(code_3[7:31]))
        self.remove(code_2).add(code_3).wait()
        parts = code_3.select_parts("\\\\")
        lines = [Underline(mob, stroke_width = 2, color = ESCAPE) for mob in parts]
        text_0 = Songti("输出反斜杠", color = ESCAPE).scale(1/3).next_to(parts, UP, buff = 0.15).save_state().move_to(parts[0])
        back = BackgroundRectangle(VGroup(code_2, *lines, text_0), buff = 0.05)
        self.add_background(text_0, back
            ).play(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in lines], 
                   text_0.animating(rate_func = rush_from).restore())
        self.remove(back).wait()
        self.play(IndicateAround(code_3[13:16]))
        self.wait()
        
class Quine_2(FrameScene):
    def construct(self):
        code_1 = Code("s = \"...\"\nprint(s)", t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, "\"...\"": STRING, (r"(", r")"): BRACKET1}).next_to(DOWN + 5.5*LEFT, DR)
        self.add(code_1).wait()
        small_1 = SurroundingRectangle(code_1[3:6], color = PURPLE_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_1, code_1).play(ShowCreation(small_1))
        self.wait()

        code_2 = Code("s = \"s = \\\"...\\\"\\nprint(s)\"", t2c = {r"=": SYMBOL, r"s": VARIABLE, ("\\\"", "\\n"): ESCAPE}
                      ).next_to(0.0*UP + 5.5*LEFT, DR)
        code_2[2:].set_color(STRING)
        code_2.set_color_by_text(("\\\"", "\\n"), ESCAPE)
        big_2 = SurroundingRectangle(code_2[3:22], color = PURPLE_A, buff = 0.05).set_fill(opacity = 1, color = BLACK)
        big_2.set_height(big_2.get_height() + 0.4, stretch = True)
        line_1 = Line(color = PURPLE_A).add_updater(lambda mob: mob.put_start_and_end_on(small_1.get_corner(UL), big_2.get_corner(DL)))
        line_2 = Line(color = PURPLE_A).add_updater(lambda mob: mob.put_start_and_end_on(small_1.get_corner(UR), big_2.get_corner(DR)))
        self.add(line_1, line_2, big_2).play(TransformFromCopy(small_1, big_2), 
                    TransformFromCopy(code_1[:3], code_2[:3]), FadeTransform(code_1[3:6].copy(), code_2[3:22]), TransformFromCopy(code_1[6], code_2[22]), )
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_2 = SurroundingRectangle(code_2[7:10], color = RED_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_2, code_2).play(ShowCreation(small_2))
        self.wait()

        code_3 = Code("s = \"s = \\\"s = \\\\\\\"...\\\\\\\"\\\\nprint(s)\\\"\\nprint(s)\"", 
                      t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, ("\\\"", "\\n", "\\"): ESCAPE}
                      ).next_to(1.0*UP + 5.5*LEFT, DR)
        code_3[2:].set_color(STRING)
        code_3.set_color_by_text(("\\\"", "\\n", "\\"), ESCAPE)
        big_3 = SurroundingRectangle(code_3[7:31], color = RED_A, buff = 0.05).set_fill(opacity = 1, color = BLACK)
        big_3.set_height(big_3.get_height() + 0.4, stretch = True)
        line_1 = Line(color = RED_A).add_updater(lambda mob: mob.put_start_and_end_on(small_2.get_corner(UL), big_3.get_corner(DL)))
        line_2 = Line(color = RED_A).add_updater(lambda mob: mob.put_start_and_end_on(small_2.get_corner(UR), big_3.get_corner(DR)))
        self.add(line_1, line_2, big_3).play(TransformFromCopy(small_2, big_3), 
                    TransformFromCopy(code_2[:7], code_3[:7]), FadeTransform(code_2[7:10].copy(), code_3[7:31]), TransformFromCopy(code_2[10:], code_3[31:]), )
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_3 = SurroundingRectangle(code_3[13:16], color = YELLOW_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_3, code_3).play(ShowCreation(small_3))
        self.wait()

        code_4 = Code("s = \"s = \\\"s = \\\\\\\"s = \\\\\\\\\\\\\\\"...\\\\\\\\\\\\\\\"\\\\\\\\nprint(s)\\\\\\\"\\\\nprint(s)\\\"\\nprint(s)\"", 
                      t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, ("\\\"", "\\n", "\\"): ESCAPE}
                      ).next_to(2.0*UP + 5.5*LEFT, DR)
        code_4[2:].set_color(STRING)
        code_4.set_color_by_text(("\\\"", "\\n", "\\"), ESCAPE)
        # self.add(code_4, index_labels(code_4))
        big_4 = SurroundingRectangle(code_4[13:47], color = YELLOW_A, buff = 0.05).set_fill(opacity = 1, color = BLACK)
        big_4.set_height(big_4.get_height() + 0.4, stretch = True)
        line_1 = Line(color = YELLOW_A).add_updater(lambda mob: mob.put_start_and_end_on(small_3.get_corner(UL), big_4.get_corner(DL)))
        line_2 = Line(color = YELLOW_A).add_updater(lambda mob: mob.put_start_and_end_on(small_3.get_corner(UR), big_4.get_corner(DR)))
        self.add(line_1, line_2, big_4).play(TransformFromCopy(small_3, big_4), 
                    TransformFromCopy(code_3[:13], code_4[:13]), FadeTransform(code_3[13:16].copy(), code_4[13:47]), TransformFromCopy(code_3[16:], code_4[47:]), )
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_4 = SurroundingRectangle(code_4[23:26], color = GREEN_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_4, code_4).play(ShowCreation(small_4))
        self.wait()

        code_5 = Code("s = \"s = \\\"s = \\\\\\\"s = \\\\\\\\\\\\\\\"s = \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"...\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\\nprint(s)\\\\\\\\\\\\\\\"\\\\\\\\nprint(s)\\\\\\\"\\\\nprint(s)\\\"\\nprint(s)\"", 
                      t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, ("\\\"", "\\n", "\\"): ESCAPE}
                      ).next_to(3.0*UP + 5.5*LEFT, DR)
        code_5[2:].set_color(STRING)
        code_5.set_color_by_text(("\\\"", "\\n", "\\"), ESCAPE)
        # self.add(code_5)#, index_labels(code_5))
        # self.camera.frame.shift(5*RIGHT)
        big_5 = SurroundingRectangle(code_5[23:77], color = GREEN_A, buff = 0.05).set_fill(opacity = 1, color = BLACK)
        big_5.set_height(big_5.get_height() + 0.4, stretch = True)
        line_1 = Line(color = GREEN_A).add_updater(lambda mob: mob.put_start_and_end_on(small_4.get_corner(UL), big_5.get_corner(DL)))
        line_2 = Line(color = GREEN_A).add_updater(lambda mob: mob.put_start_and_end_on(small_4.get_corner(UR), big_5.get_corner(DR)))
        self.add(line_1, line_2, big_5).play(TransformFromCopy(small_4, big_5), 
                    TransformFromCopy(code_4[:23], code_5[:23]), FadeTransform(code_4[23:26].copy(), code_5[23:77]), TransformFromCopy(code_4[26:], code_5[77:]), )
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_5 = SurroundingRectangle(code_5[41:44], color = BLUE_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_5, code_5).play(ShowCreation(small_5))
        self.wait()

        code_6 = Code("s = \"s = \\\"s = \\\\\\\"s = \\\\\\\\\\\\\\\"s = \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"s = \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"...\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\nprint(s)\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\\nprint(s)\\\\\\\\\\\\\\\"\\\\\\\\nprint(s)\\\\\\\"\\\\nprint(s)\\\"\\nprint(s)\"", 
                      t2c = {(r"print"): FUNCTION, r"=": SYMBOL, r"s": VARIABLE, ("\\\"", "\\n", "\\"): ESCAPE}
                      ).next_to(4.0*UP + 5.5*LEFT, DR)
        code_6[2:].set_color(STRING)
        code_6.set_color_by_text(("\\\"", "\\n", "\\"), ESCAPE)
        # self.add(code_5)#, index_labels(code_5))
        # self.camera.frame.shift(14*RIGHT + UP)
        big_6 = SurroundingRectangle(code_6[41:135], color = BLUE_A, buff = 0.05).set_fill(opacity = 1, color = BLACK)
        big_6.set_height(big_6.get_height() + 0.4, stretch = True)
        line_1 = Line(color = BLUE_A).add_updater(lambda mob: mob.put_start_and_end_on(small_5.get_corner(UL), big_6.get_corner(DL)))
        line_2 = Line(color = BLUE_A).add_updater(lambda mob: mob.put_start_and_end_on(small_5.get_corner(UR), big_6.get_corner(DR)))
        self.add(line_1, line_2, big_6).play(TransformFromCopy(small_5, big_6), 
                    TransformFromCopy(code_5[:41], code_6[:41]), FadeTransform(code_5[41:44].copy(), code_6[41:135]), TransformFromCopy(code_5[44:], code_6[135:]), )
        line_1.clear_updaters(), line_2.clear_updaters()
        self.wait()
        small_6 = SurroundingRectangle(code_6[75:78], color = PURPLE_A).set_fill(opacity = 1, color = BLACK)
        self.add(small_6, code_6).play(ShowCreation(small_6))
        self.wait()

        self.wait(2)
        self.play(code_6.copy().animate.shift(UP))
        self.wait()

class Quine_3(FrameScene):
    def construct(self):
        shade = Shade(fill_color = BLACK).append_points(Rectangle(width = 12.0, height = 3.5).shift(1.75*UP).reverse_points().get_points())
        surr = Rectangle(width = 12.2, height = 3.7).shift(1.75*UP)
        divide_line = Line(0.5*DOWN, 2.5*DOWN, color = GREY)
        title_code = Heiti("代码", color = YELLOW).scale(1.2)
        title_code[0].move_to(6.5*LEFT + DOWN), title_code[1].move_to(6.5*LEFT + 2*DOWN)
        title_print = Heiti("输出", color = YELLOW).scale(1.2)
        title_print[0].move_to(6.5*RIGHT + DOWN), title_print[1].move_to(6.5*RIGHT + 2*DOWN)
        self.bring_to_back(shade, surr, divide_line, title_code, title_print).wait()

        sound_0, sound_1 = AudioSegment.from_file("sound_0.mp3"), AudioSegment.from_file("sound_1.mp3")
        s = 's = %r\nprint(s%%s)'
        print(s%s)
        code_0 = Code(r"s = 's = %r\nprint(s%%s)'" + "\n" + r"print(s%s)", 
                      t2c = {r"print": FUNCTION, (r"%", r"="): SYMBOL, (r"(", r")"): BRACKET1, (r"%r", r"%%"): CONSTANT, r"s": VARIABLE, r"\n": ESCAPE}).next_to(1.5*DOWN + 5.5*LEFT)
        code_0[2:21].set_color(STRING)
        code_0.set_color_by_text((r"%r", r"%%"), CONSTANT).set_color_by_text(r"\n", ESCAPE)
        # self.add(code_0, index_labels(code_0))
        print_0 = Code(r"s = 's = %r\nprint(s%%s)'" + "\n" + r"print(s%s)").set_color(SYMBOL).next_to(1.5*DOWN + 0.5*RIGHT)
        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.play(ShowIncreasingSubsets(code_0))
        self.wait()
        self.file_writer.add_audio_segment(sound_1, time = self.get_time())
        self.add(print_0).wait()

        parts = [code_0.select_part(r"%r"), code_0.select_part(r"%%"), code_0[-3:-1]]
        line_0 = Underline(parts[0], stroke_width = 2, color = CONSTANT)
        line_1 = Underline(parts[1], stroke_width = 2, color = CONSTANT).match_y(line_0)
        line_2 = Underline(parts[2], stroke_width = 2, color = VARIABLE)
        text_0 = Songti("接受一个输入", color = CONSTANT).scale(1/3).next_to(parts[0], UP, buff = 0.15).save_state().move_to(parts[0])
        text_1 = Songti("输出%号", color = CONSTANT)
        text_1[2].become(Code("%", color = CONSTANT).scale(2).move_to(text_1[2]))
        text_1.scale(1/3).next_to(parts[1], UP, buff = 0.15).save_state().move_to(parts[1])
        text_2 = Songti("输入S", color = VARIABLE)
        text_2[2].become(Code("s", color = VARIABLE).scale(2).move_to(text_2[2]))
        text_2.scale(1/3).next_to(parts[2], DOWN, buff = 0.15).save_state().move_to(parts[2])
        back = BackgroundRectangle(VGroup(code_0, line_0, line_1, line_2, text_0, text_1, text_2), buff = 0.05)
        self.add_background(text_0, text_1, text_2, back
            ).play(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0, line_1, line_2]], 
                   *[mob.animating(rate_func = rush_from).restore() for mob in [text_0, text_1, text_2]])
        self.remove(back).wait()

class Quine_4(FrameScene):
    def construct(self):
        divide_line = Line(3*UP, 3*DOWN, color = GREY)
        title_code = Heiti("原理", color = YELLOW).scale(1.2)
        title_code[0].move_to(6.5*LEFT + UP), title_code[1].move_to(6.5*LEFT + DOWN)
        title_print = Heiti("输出", color = YELLOW).scale(1.2)
        title_print[0].move_to(6.5*RIGHT + UP), title_print[1].move_to(6.5*RIGHT + DOWN)
        self.bring_to_back(divide_line, title_code, title_print).wait()
        
        text_A = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前”", color = STRING).scale(0.6).shift(2*UP + 3*LEFT)
        text_A[:2].set_color(FUNCTION)
        symbol_A = MTex("A", color = BLUE).next_to(text_A.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        A = VGroup(text_A, symbol_A, SurroundingRectangle(VGroup(text_A, symbol_A), color = BLUE, buff = 0.3).round_corners(0.5))
        text_B = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前", color = FUNCTION, t2c = {"，": SYMBOL}).scale(0.6).shift(DOWN + 3*LEFT)
        text_B[2:10].set_color(STRING)
        symbol_B = MTex("B", color = GREEN).next_to(text_B.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        B = VGroup(text_B, symbol_B, SurroundingRectangle(VGroup(text_B, symbol_B), color = GREEN, buff = 0.3).round_corners(0.5))
        self.play(FadeIn(A, 0.5*UP), FadeIn(B, 0.5*UP))
        self.wait()

        output_A = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前", color = SYMBOL, ).scale(0.6).next_to(2*UP + 0.5*RIGHT)
        surr = SurroundingRectangle(text_A)
        self.play(ShowCreation(surr))
        self.wait()
        self.play(Write(output_A))
        self.wait()

        output_B2 = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前”", color = SYMBOL, ).scale(0.6).next_to(DOWN + 0.5*RIGHT)
        output_B1 = Heiti("打印“”", color = SYMBOL, ).scale(0.6)
        output_B1.shift(output_B2[0].get_center() - output_B1[0].get_center())
        self.play(Transform(surr, SurroundingRectangle(text_B[:10])))
        self.wait()
        self.play(Write(output_B1))
        self.wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[11:21])))
        self.wait()
        self.play(TransformFromCopy(output_A, output_B2[3:-1]), Transform(output_B1[-1], output_B2[-1]))
        self.remove(output_B1).add(output_B2).wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[22:])))
        self.wait()
        self.play(output_A.animate.next_to(0.5*DOWN + 0.5*RIGHT), output_B2.animate.next_to(1.5*UP + 0.5*RIGHT), path_arc = PI/4)
        self.wait()

        self.play(FadeOut(surr))
        self.wait()

class Quine_5(FrameScene):
    def construct(self):
        divide_line = Line(3*UP, 3*DOWN, color = GREY)
        title_code = Heiti("原理", color = YELLOW).scale(1.2)
        title_code[0].move_to(6.5*LEFT + UP), title_code[1].move_to(6.5*LEFT + DOWN)
        title_print = Heiti("输出", color = YELLOW).scale(1.2)
        title_print[0].move_to(6.5*RIGHT + UP), title_print[1].move_to(6.5*RIGHT + DOWN)
        self.bring_to_back(divide_line, title_code, title_print).wait()
        
        text_A = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算2+3”", color = STRING).scale(0.6).shift(2.1*UP + 3*LEFT)
        text_A[:2].set_color(FUNCTION)
        symbol_A = MTex("A", color = BLUE).next_to(text_A.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        A = VGroup(text_A, symbol_A, SurroundingRectangle(VGroup(text_A, symbol_A), color = BLUE, buff = 0.3).round_corners(0.5))
        text_B = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，", color = FUNCTION, t2c = {"，": SYMBOL}).scale(0.6).shift(0.71*DOWN + 3*LEFT)
        text_B[2:10].set_color(STRING)
        symbol_B = MTex("B", color = GREEN).next_to(text_B.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        B = VGroup(text_B, symbol_B, SurroundingRectangle(VGroup(text_B, symbol_B), color = GREEN, buff = 0.3).round_corners(0.5))
        text_T = Heiti("计算2+3", color = FUNCTION, t2c = {"+": SYMBOL, ("2", "3"): NUMBER}).scale(0.6).shift(2.4*DOWN + 3*LEFT)
        symbol_T = MTex("T", color = RED).next_to(text_T, LEFT)
        T = VGroup(text_T, symbol_T, SurroundingRectangle(VGroup(text_T, symbol_T), color = RED, buff = 0.3).round_corners(0.3)).set_x(-3)
        self.play(FadeIn(A, 0.5*UP), FadeIn(B, 0.5*UP), FadeIn(T, 0.5*UP))
        self.wait()

        output_A = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算2+3", color = SYMBOL, ).scale(0.6).next_to(2.1*UP + 0.5*RIGHT)
        surr = SurroundingRectangle(text_A)
        self.play(ShowCreation(surr), Write(output_A))
        self.wait()

        output_B2 = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算2+3”", color = SYMBOL, ).scale(0.6).next_to(DOWN + 0.5*RIGHT)
        output_B2.shift((text_B[0].get_y() - output_B2[0].get_y())*UP)
        output_B1 = Heiti("打印“”", color = SYMBOL, ).scale(0.6)
        output_B1.shift(output_B2[0].get_center() - output_B1[0].get_center())
        self.play(Transform(surr, SurroundingRectangle(text_B[:10])), Write(output_B1))
        self.wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[11:21])), TransformFromCopy(output_A, output_B2[3:-1]), Transform(output_B1[-1], output_B2[-1]))
        self.remove(output_B1).add(output_B2).wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[22:])), output_A.animating(path_arc = PI/4).next_to(0.5*DOWN + 0.5*RIGHT), output_B2.animating(path_arc = PI/4).next_to(1.5*UP + 0.5*RIGHT))
        self.wait()

        self.play(Transform(surr, SurroundingRectangle(text_T)))
        self.wait()

        self.play(FadeOut(surr))
        self.wait()

"""
class Quine_6(FrameScene):
    def construct(self):
        divide_line = Line(3*UP, 3*DOWN, color = GREY)
        title_code = Heiti("原理", color = YELLOW).scale(1.2)
        title_code[0].move_to(6.5*LEFT + UP), title_code[1].move_to(6.5*LEFT + DOWN)
        title_print = Heiti("输出", color = YELLOW).scale(1.2)
        title_print[0].move_to(6.5*RIGHT + UP), title_print[1].move_to(6.5*RIGHT + DOWN)
        self.bring_to_back(divide_line, title_code, title_print).wait()
        
        text_A = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算已输出的功能是否会停机”", color = STRING).scale(0.6).shift(2.1*UP + 3.1*LEFT)
        text_A[:2].set_color(FUNCTION)
        symbol_A = MTex("A", color = BLUE).next_to(text_A.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        A = VGroup(text_A, symbol_A, SurroundingRectangle(VGroup(text_A, symbol_A), color = BLUE, buff = 0.3).round_corners(0.5))
        text_B = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，", color = FUNCTION, t2c = {"，": SYMBOL}).scale(0.6).shift(0.71*DOWN + 3.1*LEFT)
        text_B[2:10].set_color(STRING)
        symbol_B = MTex("B", color = GREEN).next_to(text_B.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        B = VGroup(text_B, symbol_B, SurroundingRectangle(VGroup(text_B, symbol_B), color = GREEN, buff = 0.3).round_corners(0.5))
        text_T = Heiti("计算已输出的功能是否会停机", color = FUNCTION, t2c = {"+": SYMBOL, ("2", "3"): NUMBER}).scale(0.6).shift(2.4*DOWN + 3*LEFT)
        symbol_T = MTex("T", color = RED).next_to(text_T, LEFT)
        T = VGroup(text_T, symbol_T, SurroundingRectangle(VGroup(text_T, symbol_T), color = RED, buff = 0.3).round_corners(0.3)).set_x(-3.1)
        self.play(FadeIn(A, 0.5*UP), FadeIn(B, 0.5*UP), FadeIn(T, 0.5*UP))
        self.wait()

        output_A = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算已输出的功能是否会停机", color = SYMBOL, ).scale(0.6).next_to(2.1*UP + 0.5*RIGHT)
        surr = SurroundingRectangle(text_A)
        self.play(ShowCreation(surr), Write(output_A))
        self.wait()

        output_B2 = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算已输出的功能是否会停机”", color = SYMBOL, ).scale(0.6).next_to(DOWN + 0.5*RIGHT)
        output_B2.shift((text_B[0].get_y() - output_B2[0].get_y())*UP)
        output_B1 = Heiti("打印“”", color = SYMBOL, ).scale(0.6)
        output_B1.shift(output_B2[0].get_center() - output_B1[0].get_center())
        self.play(Transform(surr, SurroundingRectangle(text_B[:10])), Write(output_B1))
        self.wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[11:21])), TransformFromCopy(output_A, output_B2[3:-1]), Transform(output_B1[-1], output_B2[-1]))
        self.remove(output_B1).add(output_B2).wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[22:])), output_A.animating(path_arc = PI/4).next_to(0.5*DOWN + 0.5*RIGHT), output_B2.animating(path_arc = PI/4).next_to(1.5*UP + 0.5*RIGHT))
        self.wait()

        self.play(Transform(surr, SurroundingRectangle(text_T)))
        self.wait()

        self.play(FadeOut(surr))
        self.wait()
"""

class Quine_6(FrameScene):
    def construct(self):
        divide_line = Line(3*UP, 3*DOWN, color = GREY)
        title_code = Heiti("原理", color = YELLOW).scale(1.2)
        title_code[0].move_to(6.5*LEFT + UP), title_code[1].move_to(6.5*LEFT + DOWN)
        title_print = Heiti("输出", color = YELLOW).scale(1.2)
        title_print[0].move_to(6.5*RIGHT + UP), title_print[1].move_to(6.5*RIGHT + DOWN)
        self.bring_to_back(divide_line, title_code, title_print).wait()
        
        text_A = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算已输出的功能是否会停机，\n然后自己做出相反的动作”", color = STRING).scale(0.6).shift(2.1*UP + 3.1*LEFT)
        text_A[:2].set_color(FUNCTION)
        symbol_A = MTex("A", color = BLUE).next_to(text_A.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        A = VGroup(text_A, symbol_A, SurroundingRectangle(VGroup(text_A, symbol_A), color = BLUE, buff = 0.3).round_corners(0.5))
        text_B = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，", color = FUNCTION, t2c = {"，": SYMBOL}).scale(0.6).shift(0.71*DOWN + 3.1*LEFT)
        text_B[2:10].set_color(STRING)
        symbol_B = MTex("B", color = GREEN).next_to(text_B.get_corner(UL), UR, buff = 0).shift(0.2*UP)
        B = VGroup(text_B, symbol_B, SurroundingRectangle(VGroup(text_B, symbol_B), color = GREEN, buff = 0.3).round_corners(0.5))
        text_T = Heiti("计算已输出的功能是否会停机，\n然后自己做出相反的动作", color = FUNCTION, t2c = {"+": SYMBOL, ("2", "3"): NUMBER}).scale(0.6).shift(2.4*DOWN + 3*LEFT)
        symbol_T = MTex("T", color = RED).next_to(text_T, LEFT)
        T = VGroup(text_T, symbol_T, SurroundingRectangle(VGroup(text_T, symbol_T), color = RED, buff = 0.3).round_corners(0.3)).set_x(-3.1)
        self.play(FadeIn(A, 0.5*UP), FadeIn(B, 0.5*UP), FadeIn(T, 0.5*UP))
        self.wait()

        output_A = Heiti("输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算已输出的功能是否会停机，\n然后自己做出相反的动作", color = SYMBOL, ).scale(0.6).next_to(2.1*UP + 0.5*RIGHT)
        surr = SurroundingRectangle(text_A)
        self.play(ShowCreation(surr), Write(output_A))
        self.wait()

        output_B2 = Heiti("打印“输出打印两字和双引号，\n在引号里复制上段内容，\n将本段置于最前，\n计算已输出的功能是否会停机，\n然后自己做出相反的动作”", color = SYMBOL, ).scale(0.6).next_to(DOWN + 0.5*RIGHT)
        output_B2.shift((text_B[0].get_y() - output_B2[0].get_y())*UP)
        output_B1 = Heiti("打印“”", color = SYMBOL, ).scale(0.6)
        output_B1.shift(output_B2[0].get_center() - output_B1[0].get_center())
        self.play(Transform(surr, SurroundingRectangle(text_B[:10])), Write(output_B1))
        self.wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[11:21])), TransformFromCopy(output_A, output_B2[3:-1]), Transform(output_B1[-1], output_B2[-1]))
        self.remove(output_B1).add(output_B2).wait()

        self.play(Transform(surr, SurroundingRectangle(text_B[22:])), output_A.animating(path_arc = PI/4).next_to(1*DOWN + 0.5*RIGHT), output_B2.animating(path_arc = PI/4).next_to(1.5*UP + 0.5*RIGHT))
        self.wait()

        surr_2 = SurroundingRectangle(VGroup(output_A, output_B2))
        self.play(Transform(surr, SurroundingRectangle(text_T)), ShowCreation(surr_2))
        self.wait()

        self.play(FadeOut(surr), FadeOut(surr_2))
        self.wait()
            
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        