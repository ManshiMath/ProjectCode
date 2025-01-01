from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Video_1(Scene):
    def construct(self):
        def util(mob: Mobject):
            mob.move_to(mob.position.get_location()).set_opacity(mob.alpha.get_value())
            mob.shift(0.2*np.sin(0.25*(mob.phase + self.time)*PI)*UP)
        def avtivate(mob: Mobject, position: np.ndarray = ORIGIN):
            mob.position = Point(position)
            mob.alpha = ValueTracker(0)
            mob.phase = TAU*random.random()
            mob.add_updater(util)
        color_map = {r"{x}": GREEN, r"y": BLUE, (r"1", r"2", r"4"): ORANGE, (r"10", r"28"): YELLOW}
        problem = Songti("已知笼子里有兔子和鸡，\n数头一共10个头，数脚一共28只脚，\n一共有多少只鸡、多少只兔子呢？", t2c = {"鸡": GREEN, "兔子": BLUE, (r"10", r"28"): YELLOW}).scale(0.6)
        avtivate(problem, 2*UP + 2*LEFT)
        equations = MathTex(r"\begin{cases}1{x}+1y=10\\2{x}+4y=28\end{cases}", tex_to_color_map = color_map).scale(0.8)
        avtivate(equations, 3*RIGHT)
        matrix = MathTex(r"\begin{bmatrix}1&1\\2&4\end{bmatrix}\begin{bmatrix}{x}\\y\end{bmatrix}=\begin{bmatrix}10\\28\end{bmatrix}", tex_to_color_map = color_map).scale(0.8)
        avtivate(matrix, 2*DOWN + LEFT)
        # for mob in [problem, equations, matrix]:
        #     mob.alpha.set_value(1)
        ratio = 0.5
        self.add(problem).play(problem.position.shift(ratio*UP).animate.shift(ratio*DOWN), problem.alpha.animate.set_value(1))
        self.add(equations).play(equations.position.shift(ratio*RIGHT).animate.shift(ratio*LEFT), equations.alpha.animate.set_value(1))
        self.add(matrix).play(matrix.position.shift(ratio*DOWN).animate.shift(ratio*UP), matrix.alpha.animate.set_value(1))
        self.wait(8)
        misunderstand = ImageMobject("misunderstand.jpeg", height = 5).shift(3*RIGHT)
        self.play(*[mob.position.animate.set_x(-3) for mob in [problem, equations, matrix]], OverFadeIn(misunderstand, 3*LEFT))
        self.wait(8)

class Video_2(Scene):
    def construct(self):
        babylon = ImageMobject("babylon.jpg", height = 5)
        self.play(FadeIn(babylon, UP))
        self.wait()
        problem = Heiti("今有上禾三秉，中禾二秉，下禾一秉，實三十九斗；\n　　上禾二秉，中禾三秉，下禾一秉，實三十四斗；\n　　上禾一秉，中禾二秉，下禾三秉，實二十六斗。\n問上、中、下禾實一秉各幾何？", t2c = {("上禾", "上"): GREEN, ("中禾", "中"): TEAL, ("下禾", "下"): BLUE, ("一秉", "二秉", "三秉"): ORANGE, ("三十九斗", "三十四斗", "二十六斗"): YELLOW}).scale(2/3).shift(2.5*UP)
        self.play(FadeOut(babylon, 0.5*DOWN), FadeIn(problem, 0.5*DOWN))
        self.wait()
        solution = ImageMobject("rods.jpg", height = 4).shift(DOWN)
        def equations(*numbers: list[int]):
            color_map = {"x": GREEN, "y": TEAL, "z": BLUE, (r"{0}x", r"{0}y", r"{0}z"): GREY, (str(numbers[3]), str(numbers[7]), str(numbers[11])): YELLOW, (r"+", r"="): WHITE}
            MathTex = MathTex(r"\begin{cases}{"+str(numbers[0])+r"}x+{"+str(numbers[1])+r"}y+{"+str(numbers[2])+r"}z="+str(numbers[3])+r"\\{"+str(numbers[4])+r"}x+{"+str(numbers[5])+r"}y+{"+str(numbers[6])+r"}z="+str(numbers[7])+r"\\{"+str(numbers[8])+r"}x+{"+str(numbers[9])+r"}y+{"+str(numbers[10])+r"}z="+str(numbers[11])+r"\end{cases}", color = ORANGE, tex_to_color_map = color_map).set_stroke(width = 4, color = BLACK, background = True)
            MathTex[0:5].set_fill(color = WHITE)
            return MathTex.scale(1/3)
        buff_h, buff_v = 2, 4/3
        equation_0 = equations(3, 2, 1, 39, 2, 3, 1, 34, 1, 2, 3, 26).shift(2*buff_h*LEFT + buff_v*UP)
        equation_1 = equations(3, 2, 1, 39, 6, 9, 3, 102, 1, 2, 3, 26).shift(buff_h*LEFT + buff_v*UP)
        equation_2 = equations(3, 2, 1, 39, 0, 5, 1, 24, 1, 2, 3, 26).shift(buff_v*UP)
        equation_3 = equations(3, 2, 1, 39, 0, 5, 1, 24, 3, 6, 9, 78).shift(buff_h*RIGHT + buff_v*UP)
        equation_4 = equations(3, 2, 1, 39, 0, 5, 1, 24, 0, 4, 8, 39).shift(buff_h*LEFT)
        equation_5 = equations(3, 2, 1, 39, 0, 5, 1, 24, 0, 20, 40, 195)
        equation_6 = equations(3, 2, 1, 39, 0, 5, 1, 24, 0, 0, 36, 99).shift(buff_h*RIGHT)
        equation_7 = equations(3, 2, 1, 39, 0, 5, 1, 24, 0, 0, 4, 11).shift(0.5*buff_h*LEFT + buff_v*DOWN)
        equation_8 = equations(4, 0, 0, 37, 0, 4, 0, 17, 0, 0, 4, 11).shift(0.5*buff_h*RIGHT + buff_v*DOWN)
        calculation = VGroup(equation_0, equation_1, equation_2, equation_3, equation_4, equation_5, equation_6, equation_7, equation_8).shift(DOWN + 5/3*LEFT)
        surroundings = VGroup(*[SurroundingRectangle(mob, stroke_color = WHITE, stroke_width = 2, fill_opacity = 0.5, fill_color = BLACK) for mob in [equation_0, equation_1, equation_2, equation_3, equation_4, equation_5, equation_6, equation_7, equation_8]])
        surroundings[0].set_stroke(width = 0)
        arrow_map = {"tip_width_ratio": 2, "width_to_tip_len": 0.015, "stroke_color": GREY, "stroke_width": 8}
        arrow_0, arrow_1, arrow_2 = Arrow(surroundings[0].get_left() + 0.5*LEFT, surroundings[3].get_right() + 2/3*RIGHT, **arrow_map), Arrow(surroundings[4].get_left() + 0.5*LEFT, surroundings[3].get_right() + 2/3*RIGHT + buff_v*DOWN, **arrow_map), Arrow(surroundings[7].get_left() + 0.5*LEFT, surroundings[8].get_right() + 2/3*RIGHT, **arrow_map)
        all_left = VGroup(calculation.save_state(), surroundings.save_state(), arrow_0.save_state(), arrow_1.save_state(), arrow_2.save_state())
        all_shade = BackgroundRectangle(all_left, buff = 0.2, fill_opacity = 1)
        all_left.add(all_shade).next_to(solution.get_left() + 0.2*LEFT, RIGHT, buff = 0)
        self.play(FadeIn(solution, UP))
        self.wait()
        self.bring_to_back(arrow_0, arrow_1, arrow_2, surroundings, calculation, all_shade).play(*[mob.animate.restore() for mob in [arrow_0, arrow_1, arrow_2, surroundings, calculation]], solution.animate.shift(4*RIGHT), follow(all_shade, solution), run_time = 2)
        self.wait()
        back_0 = surroundings[0]
        calculation.remove(equation_0), surroundings.remove(back_0)
        self.add(back_0, equation_0)

        leibniz = LabelPicture("Leibniz.jpg", "戈特弗里德·威廉·莱布尼茨（1646.7.1 - 1716.11.14）").shift(3*LEFT + 0.5*UP)
        self.play(OverFadeIn(leibniz, 4*RIGHT), *[OverFadeOut(mob, 10*RIGHT) for mob in [problem, arrow_0, arrow_1, arrow_2, surroundings, calculation, all_shade, solution]], equation_0.animate.scale(3).move_to(2.5*RIGHT + 0.5*DOWN), back_0.animate.scale(3).move_to(2.5*RIGHT + 0.5*DOWN), run_time = 2)
        self.remove(back_0).wait()

        det_0 = MathTex(r"\begin{vmatrix}3&2&1\\2&3&1\\1&2&3\end{vmatrix}=12\ne 0", color = ORANGE).shift(2.5*RIGHT + 2*UP)
        det_0[:6].set_color(WHITE), det_0[15:24].set_color(WHITE), det_0[24:].set_color(RED)
        det_0.shift((equation_0[13].get_x() - det_0[21].get_x())*RIGHT)
        regular = Songti("有唯一解", color = RED).scale(0.8)
        for i in range(4):
            regular[i].move_to((i-1.5)*0.55*DOWN)
        regular.next_to(equation_0, buff = 0.3)
        self.play(FadeIn(det_0, 0.5*DOWN))
        self.wait()
        self.play(Write(regular))
        self.wait()

        self.play(IndicateAround(det_0[:21]))
        self.wait()
        self.play(IndicateAround(equation_0))
        self.wait()

#################################################################### 

class Patch3_1(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(1*OUT).set_orientation(Rotation(quadternion))
        square = Surface(u_range = (-2, 2), v_range = (-2, 2))
        overlap_square = TexturedSurface(square, "texture_3.jpg")
        self.add(overlap_square)

class Patch3_2(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(1*OUT).set_orientation(Rotation(quadternion))
        square = Surface(u_range = (-2, 2), v_range = (-2, 2), color = BLUE).shift(IN)
        overlap_square = TexturedSurface(square, "texture_2.jpg").shift(1.5*OUT)
        self.add(overlap_square, square)

class Patch3_3(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(1*OUT).set_orientation(Rotation(quadternion))
        square_1 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = RED).shift(1*OUT)
        square_2 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = GREEN).shift(0*IN)
        square_3 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = BLUE).shift(1*IN)
        self.add(square_1, square_2, square_3)

class Patch3_4(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(0.5*OUT).set_orientation(Rotation(quadternion))
        square = Surface(u_range = (-2, 2), v_range = (-2, 2), color = BLUE)
        overlap_square = TexturedSurface(square, "texture_2.jpg")
        self.add(overlap_square, square.rotate(PI/2, axis = RIGHT))

class Patch3_5(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(0.5*OUT).set_orientation(Rotation(quadternion))
        square_1 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = RED).shift(0.5*OUT)
        square_2 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = GREEN).shift(0.5*IN)
        square_3 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = BLUE).rotate(PI/2, axis = RIGHT)
        self.add(square_1, square_2, square_3)

class Patch3_6(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(0.5*OUT).set_orientation(Rotation(quadternion))
        square_1 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = RED).rotate(TAU/3, axis = RIGHT)
        square_2 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = GREEN).rotate(PI/3, axis = RIGHT)
        square_3 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = BLUE)
        self.add(square_1, square_2, square_3)

class Patch3_7(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(0.5*OUT).set_orientation(Rotation(quadternion))
        square_1 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = RED).rotate(TAU/3, about_point = 0.5*OUT, axis = RIGHT)
        square_2 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = GREEN).rotate(-TAU/3, about_point = 0.5*OUT, axis = RIGHT)
        square_3 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = BLUE)
        self.add(square_1, square_2, square_3)

class Patch3_8(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(0.5*OUT).set_orientation(Rotation(quadternion))
        square_1 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = RED).rotate(PI/2, axis = RIGHT)
        square_2 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = GREEN).rotate(PI/2, axis = UP)
        square_3 = Surface(u_range = (-2, 2), v_range = (-2, 2), color = BLUE)
        self.add(square_1, square_2, square_3)

class Video_3(Scene):
    def construct(self):
        def equations(*numbers: list[int]):
            color_map = {"x": GREEN, "y": BLUE, ("="+str(numbers[2]), "="+str(numbers[5])): YELLOW, (r"+", r"="): WHITE}
            MathTex = MathTex(r"\begin{cases}{"+str(numbers[0])+r"}x+{"+str(numbers[1])+r"}y="+str(numbers[2])+r"\\{"+str(numbers[3])+r"}x+{"+str(numbers[4])+r"}y="+str(numbers[5])+r"\end{cases}", color = ORANGE, tex_to_color_map = color_map).set_stroke(width = 4, color = BLACK, background = True)
            MathTex[0].set_fill(color = WHITE)
            return MathTex.scale(0.8)
        equations_1 = equations(1, 1, 4, 2, 4, 10).scale(1.25).shift(UP)
        self.play(Write(equations_1))
        self.wait()
        equations_1.generate_target().shift(1.5*UP).scale(0.8)
        equations_1.target[1:8].set_fill(color = BLUE)
        equations_1.target[8:].set_fill(color = GREEN)
        arrow_x = Arrow(0.5*LEFT, 2.5*RIGHT, buff = 0).shift(LEFT + 1.5*DOWN)
        arrow_y = Arrow(0.5*DOWN, 2.5*UP, buff = 0).shift(LEFT + 1.5*DOWN)
        line_1 = Line(0.25*LEFT + 1.25*UP, 1.25*RIGHT + 0.25*DOWN, color = BLUE).scale(1.5,about_point = ORIGIN).shift(LEFT + 1.5*DOWN)
        line_2 = Line(0.25*LEFT + 0.75*UP, 1.75*RIGHT + 0.25*DOWN, color = GREEN).scale(1.5,about_point = ORIGIN).shift(LEFT + 1.5*DOWN)
        point = Dot(1.5*(0.75*RIGHT + 0.25*UP), color = YELLOW).shift(LEFT + 1.5*DOWN)
        label = MathTex(r"(3, 1)", color = YELLOW).scale(0.8).next_to(point, UR, buff = 0.1)
        self.play(MoveToTarget(equations_1), ShowCreation(arrow_x), ShowCreation(arrow_y))
        self.wait()
        self.play(ShowCreation(line_1), ShowCreation(line_2))
        self.wait()
        self.play(ShowCreation(point), Write(label))
        self.wait()

        equations_2 = equations(1, 1, 4, 2, 2, 6).shift(3*LEFT + 2.5*UP)
        equations_2[1:8].set_fill(color = BLUE)
        equations_2[8:].set_fill(color = GREEN)
        graph_2 = VGroup(Arrow(0.5*LEFT, 2.5*RIGHT, buff = 0), Arrow(0.5*DOWN, 2.5*UP, buff = 0), Line(0.25*LEFT + 1.25*UP, 1.25*RIGHT + 0.25*DOWN, color = BLUE).scale(1.5,about_point = ORIGIN), Line(0.25*LEFT + 1*UP, 1*RIGHT + 0.25*DOWN, color = GREEN).scale(1.5,about_point = ORIGIN)).shift(LEFT + 1.5*DOWN + 3*LEFT)
        self.play(*[mob.animate.shift(3*RIGHT) for mob in [equations_1, arrow_x, arrow_y, line_1, line_2, point, label]], *[FadeIn(mob, 2*RIGHT) for mob in [equations_2, graph_2]])
        self.wait()

        equations_3 = equations(1, 1, 4, 2, 2, 8).shift(4*LEFT + 2.5*UP)
        equations_3[1:8].set_fill(color = BLUE)
        equations_3[8:].set_fill(color = GREEN)
        numbers = 10
        line = VGroup(*[Line(interpolate(0.25*LEFT + 1.25*UP, 1.25*RIGHT + 0.25*DOWN, i/numbers), interpolate(0.25*LEFT + 1.25*UP, 1.25*RIGHT + 0.25*DOWN, (i+1)/numbers), color = BLUE if i%2 else GREEN) for i in range(numbers)]).scale(1.5,about_point = ORIGIN)
        graph_3 = VGroup(Arrow(0.5*LEFT, 2.5*RIGHT, buff = 0), Arrow(0.5*DOWN, 2.5*UP, buff = 0), line).shift(LEFT + 1.5*DOWN + 4*LEFT)
        self.play(*[mob.animate.shift(RIGHT) for mob in [equations_1, arrow_x, arrow_y, line_1, line_2, point, label]], *[mob.animate.shift(3*RIGHT) for mob in [equations_2, graph_2]], *[OverFadeIn(mob, 5*RIGHT) for mob in [equations_3, graph_3]])
        self.wait()

        equations_4 = MathTex(r"\begin{cases}3x+2y+1z=39\\2x+3y+1z=34\\1x+2y+3z=26\end{cases}", tex_to_color_map = {r"3x+2y+1z=39": BLUE, r"2x+3y+1z=34": TEAL, r"1x+2y+3z=26": GREEN}).scale(0.8).shift(2.5*UP + 3*RIGHT)
        q_mark = MathTex(r"?")[0].scale(5).shift(0.5*DOWN + 3*RIGHT)
        self.play(*[mob.animate.shift(7*LEFT) for mob in [equations_1, arrow_x, arrow_y, line_1, line_2, point, label]], *[OverFadeOut(mob, 7*LEFT) for mob in [equations_2, graph_2, equations_3, graph_3]], *[OverFadeIn(mob, 7*LEFT) for mob in [equations_4, q_mark]], run_time = 2)
        self.wait()

        cases_3 = Group(*[ImageMobject("Patch3_" + str(i*4+j+1) + ".png", height = 8/3).shift((j-1.5)*3*LEFT + (i-0.5)*3*UP) for i in (0, 1) for j in range(4)])
        surrounding = Rectangle(height = 6.2, width = 12.2, color = YELLOW)
        cases_3[:4].shift(0.5*UP)
        cases_3[6].shift(0.2*DOWN)
        self.play(FadeOut(equations_4, 2.5*UP), FadeOut(equations_1,2.5*UP + 5*LEFT), *[FadeOut(mob,5*LEFT) for mob in [arrow_x, arrow_y, line_1, line_2, point, label]], Transform(q_mark, surrounding), FadeInFromPoint(cases_3, 0.5*DOWN + 3*RIGHT), run_time = 2)
        self.remove(q_mark)
        cases_3.add(q_mark)
        self.wait()

        numbers = 8
        cases_2 = VGroup(Line(color = BLUE).shift(3*LEFT + 0.5*UP), Line(color = GREEN).shift(3*LEFT + 0.5*DOWN), Line(color = BLUE), Line(UP, DOWN, color = GREEN), VGroup(*[Line(interpolate(LEFT, RIGHT, i/numbers), interpolate(LEFT, RIGHT, (i+1)/numbers), color = BLUE if i%2 else GREEN) for i in range(numbers)]).shift(3*RIGHT)).set_stroke(width = 8).add(Rectangle(height = 3.2, width = 9.2, color = YELLOW))
        number_2 = MathTexText(r"2维").scale(2).shift(4*LEFT + 2.5*UP)
        number_3 = MathTexText(r"3维").scale(2).shift(4*LEFT)
        self.play(cases_3.animate.scale(0.5).move_to(2*RIGHT), FadeIn(cases_2.scale(0.5).move_to(2*RIGHT + 2.5*UP), 3*DOWN), FadeIn(number_2, 5*RIGHT + 3*DOWN), FadeIn(number_3, 5*RIGHT), run_time = 2)
        self.wait()

        number_4 = MathTexText(r"4维").scale(2).shift(4*LEFT +2.5*DOWN)
        cases_4 = VGroup(MathTex("???", color = BLUE).scale(2).shift(2*RIGHT + 2.5*DOWN), Polyline(3.05*LEFT + 2*DOWN, 3.05*LEFT + 0.8*UP, 3.05*RIGHT + 0.8*UP, 3.05*RIGHT + 2*DOWN, color = YELLOW).shift(2*RIGHT + 2.5*DOWN))
        self.play(*[mob.shift(3*DOWN).animate.shift(3*UP) for mob in [number_4, cases_4]])
        self.wait()

#################################################################### 

class BlackBox(VGroup):
    def __init__(self, **kwargs):
        
        core = Square(side_length = 2, fill_color = BLACK, fill_opacity = 1)
        entrance = Polygon(1.1*LEFT + 0.5*UP, 1.7*LEFT + UP, 1.7*LEFT + DOWN, 1.1*LEFT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        export = Polygon(1.1*RIGHT + 0.5*UP, 1.7*RIGHT + UP, 1.7*RIGHT + DOWN, 1.1*RIGHT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        # background = Rectangle(width = 3, height = 2, stroke_width = 0, fill_color = BLACK, fill_opacity = 1)
        super().__init__(core, entrance, export, **kwargs)# background, 

class Flip(Animation):
    CONFIG = {
        "dim": 0,
        "color_interpolate": False
    }

    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject | None = None,
        **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.target_mobject = target_mobject
    
    def interpolate_mobject(self, alpha: float) -> None:
        if alpha <= 0.5:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 1-2*alpha
            self.mobject.become(self.starting_mobject).scale(vector, min_scale_factor = 0)
        else:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 2*alpha-1
            self.mobject.become(self.target_mobject).scale(vector, min_scale_factor = 0)
        if self.color_interpolate:
            self.mobject.set_color(interpolate_color(self.starting_mobject.get_color(), self.target_mobject.get_color(), alpha))
        return self

class Video_4(Scene):
    def construct(self):
        problem = Heiti("今有上禾三秉，中禾二秉，下禾一秉，實三十九斗；\n　　上禾二秉，中禾三秉，下禾一秉，實三十四斗；\n　　上禾一秉，中禾二秉，下禾三秉，實二十六斗。\n問上、中、下禾實一秉各幾何？", t2c = {("上禾", "上"): GREEN, ("中禾", "中"): TEAL, ("下禾", "下"): BLUE, ("一秉", "二秉", "三秉"): ORANGE, ("三十九斗", "三十四斗", "二十六斗"): YELLOW}).scale(2/3).shift(2.5*UP)
        equation_rough = MathTex(r"\begin{cases}3x+2y+z=39\\2x+3y+z=34\\x+2y+3z=26\end{cases}", tex_to_color_map = {r"3x+2y+z=39": BLUE, r"2x+3y+z=34": TEAL, r"x+2y+3z=26": GREEN}).scale(0.8)
        self.add(problem, equation_rough).wait()
        title = Title("线性映射")
        titleline = TitleLine()
        self.play(FadeIn(title, DOWN), GrowFromPoint(titleline, 4*UP), problem.animate.shift(DOWN), equation_rough.animate.shift(DOWN))
        self.wait()
        def equations(*numbers: list[int]):
            color_map = {"x": GREEN, "y": TEAL, "z": BLUE, (r"{0}x", r"{0}y", r"{0}z"): GREY, (str(numbers[3]), str(numbers[7]), str(numbers[11])): YELLOW, (r"+", r"="): WHITE}
            MathTex = MathTex(r"\begin{cases}{"+str(numbers[0])+r"}x+{"+str(numbers[1])+r"}y+{"+str(numbers[2])+r"}z="+str(numbers[3])+r"\\{"+str(numbers[4])+r"}x+{"+str(numbers[5])+r"}y+{"+str(numbers[6])+r"}z="+str(numbers[7])+r"\\{"+str(numbers[8])+r"}x+{"+str(numbers[9])+r"}y+{"+str(numbers[10])+r"}z="+str(numbers[11])+r"\end{cases}", color = ORANGE, tex_to_color_map = color_map).set_stroke(width = 4, color = BLACK, background = True)
            MathTex[0:5].set_fill(color = WHITE)
            return MathTex.scale(0.8)
        equation = equations(3, 2, 1, 39, 2, 3, 1, 34, 1, 2, 3, 26).next_to(equation_rough.get_right(), LEFT, buff = 0)
        copy_equation = equation.copy().save_state()
        shade = BackgroundRectangle(equation, buff = 0.2)
        self.bring_to_back(equation, shade).play(equation_rough.animate.shift(4*LEFT).fade(), shade.animate.shift(4*LEFT), FadeOut(problem))
        self.remove(shade).wait()
        xs, ys, zs = equation.get_parts_by_tex(r"x"), equation.get_parts_by_tex(r"y"), equation.get_parts_by_tex(r"z")
        adds = equation.get_parts_by_tex(r"+")
        coordinates = [copy_equation.get_parts_by_tex(tex) for tex in ["39", "34", "26"]]
        self.play(IndicateAround(xs))
        self.wait()
        self.play(IndicateAround(ys))
        self.wait()
        self.play(IndicateAround(zs))
        self.wait()

        texts = r"\begin{bmatrix}3&2&1\\2&3&1\\1&2&3\end{bmatrix}", r"\begin{bmatrix}x\\y\\z\end{bmatrix}", r"\begin{bmatrix}39\\34\\26\end{bmatrix}"
        matrix = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[0]: ORANGE, texts[1]: GREEN, texts[2]: YELLOW}).scale(0.8).shift(UP)
        parts = [matrix.get_part_by_tex(tex) for tex in [texts[0], texts[1], r"=", texts[2]]]
        self.play(*[mob.animate.set_opacity(0.5) for mob in [xs, ys, zs, adds]])
        self.wait()
        anims = [ReplacementTransform(equation[i], matrix[j], path_arc = -PI/6) for i, j in zip([5, 8, 11, 16, 19, 22, 27, 30, 33], [2, 3, 4, 5, 6, 7, 8, 9, 10])]
        self.bring_to_back(*[copy_equation[i].set_opacity(0.5) for i in [5, 8, 11, 16, 19, 22, 27, 30, 33]]).play(*anims, *[follow(matrix[i], anims[3], FadeIn, path_arc = -PI/6) for i in [0, 1]], *[follow(matrix[i], anims[5], FadeIn, path_arc = -PI/6) for i in [11, 12]])
        self.wait()
        self.play(Write(matrix[15:18]))
        self.wait()
        self.play(FadeIn(matrix[13], 0.2*DOWN), FadeIn(matrix[14], 0.2*DOWN), FadeIn(matrix[18], 0.2*DOWN), FadeIn(matrix[19], 0.2*UP))
        anims = [ReplacementTransform(equation[i], matrix[j], path_arc = -PI/6) for i, j in zip([14, 15, 25, 26, 36, 37], [23, 24, 25, 26, 27, 28])]
        self.bring_to_back(*[tex.set_opacity(0.5) for tex in coordinates]).play(*anims, *[follow(matrix[i], anims[0], FadeIn, path_arc = -PI/6) for i in [21, 22, 29, 30]])
        self.wait()
        anims = ReplacementTransform(equation[13], matrix[20]), Transform(equation[24], matrix[20].copy(), remover = True), Transform(equation[35], matrix[20].copy(), remover = True)
        self.bring_to_back(*[copy_equation[i].set_opacity(0.5) for i in [13, 24, 35]]).play(*anims)
        self.wait()
        copy_equation.set_opacity(0.5)
        copy_equation[:5].set_opacity(1)
        self.bring_to_back(copy_equation).remove(equation).play(copy_equation.animate.restore(), FadeOut(equation_rough))
        self.wait()

        notation = MathTex(r"A\vec{x}=\vec{b}", tex_to_color_map = {r"A": ORANGE, r"\vec{x}": GREEN, r"\vec{b}": YELLOW}).shift(2.5*UP).save_state()
        notation[0].set_x(parts[0].get_x())
        notation[1:3].set_x(parts[1].get_x())
        notation[3].set_x(parts[2].get_x())
        notation[4:].set_x(parts[3].get_x())
        self.play(Write(notation[0]))
        self.wait()
        self.play(Write(notation[1:3]))
        self.wait()
        self.play(Write(notation[4:]))
        self.wait()
        self.play(Write(notation[3]), ShowCreationThenDestructionAround(notation, run_time = 2))
        self.wait()

        others = matrix[13:]
        shade = BackgroundRectangle(others).next_to(parts[0].get_right()+0.2*RIGHT, LEFT)
        parts[0].save_state().generate_target().move_to(1.5*UP)
        shade.save_state().generate_target().next_to(parts[0].target.get_right()+0.2*RIGHT, LEFT)
        others.save_state().generate_target().next_to(parts[0].target.get_right(), LEFT)
        self.add(others, shade, parts[0]).play(notation.animating(remover = True).scale(np.array([1, 0, 1]), about_point = 2.9*UP), FadeOut(copy_equation), *[MoveToTarget(mob) for mob in [others, shade, parts[0]]])
        self.wait()
        box = BlackBox().set_fill(opacity = 0).save_state().shift(0.5*DOWN).set_stroke(width = 10, color = GREY).scale(np.array([4, 3, 0]))
        self.remove(others, shade).bring_to_back(box).play(IndicateAround(title), FadeIn(box))
        self.wait()

        texs = r"\begin{bmatrix}3\\2\\1\end{bmatrix}", r"\begin{bmatrix}2\\3\\2\end{bmatrix}", r"\begin{bmatrix}1\\1\\3\end{bmatrix}", r"\begin{bmatrix}8\\9\\8\end{bmatrix}"
        vector = MathTex(r"{1}"+texs[0]+r"+{2}"+texs[1]+r"+{1}"+texs[2]+r"="+texs[3], tex_to_color_map = {(texs[0], texs[1], texs[2]): ORANGE, (r"{1}", r"{2}"): GREEN, texs[3]: YELLOW}).scale(0.8).shift(0.5*DOWN)
        input = MathTex(r"\begin{bmatrix}1\\2\\1\end{bmatrix}", color = GREEN).scale(0.8).shift(5.6*LEFT + 0.5*DOWN)
        output = MathTex(r"\begin{bmatrix}8\\9\\8\end{bmatrix}", color = YELLOW).scale(0.8).shift(5.6*RIGHT + 0.5*DOWN)
        self.play(Write(input))
        self.wait()
        self.play(*[TransformFromCopy(input[i], vector[j]) for i, j in zip([2, 3, 4], [0, 9, 18])])
        self.wait()
        anims_1 = [TransformFromCopy(matrix[i], vector[j]) for i, j in zip([0, 1, 2, 5, 8], [1, 2, 3, 4, 5])]
        anims_1.extend([follow(vector[6], anims_1[3], FadeIn), follow(vector[7], anims_1[3], FadeIn)])
        anims_2 = [TransformFromCopy(matrix[i], vector[j]) for i, j in zip([3, 6, 9], [12, 13, 14])]
        anims_2.extend([follow(vector[j], anims_2[1], FadeIn) for j in [10, 11, 15, 16]])
        anims_3 = [TransformFromCopy(matrix[i], vector[j]) for i, j in zip([4, 7, 10, 11, 12], [21, 22, 23, 24, 25])]
        anims_3.extend([follow(vector[19], anims_3[3], FadeIn), follow(vector[20], anims_3[3], FadeIn)])
        self.play(LaggedStart(AnimationGroup(*anims_1), AnimationGroup(*anims_2), AnimationGroup(*anims_3), run_time = 2, lag_ratio = 0.5))
        self.wait()
        self.play(Write(VGroup(vector[8], vector[17], vector[26])))
        self.wait()
        self.play(Write(vector[27:]))
        self.wait()
        self.play(TransformFromCopy(vector[27:], output, path_arc = PI/6))
        self.wait()

        # self.bring_to_back(others, shade).play(vector.animate.set_y(-2), input.animate.move_to(6*LEFT+2*DOWN), output.animate.move_to(6*RIGHT+2*DOWN), parts[0].animate.restore().set_y(1), follow(shade, parts[0]), others.animate.restore().set_y(1))
        # self.wait()
        # input_2, output_2 = MathTex(r"\begin{bmatrix}?\\?\\?\end{bmatrix}", color = GREEN).scale(0.8).shift(UP+6*LEFT), MathTex(r"\begin{bmatrix}39\\34\\26\end{bmatrix}", color = YELLOW).scale(0.8).shift(UP+6*RIGHT)
        # self.play(Write(output_2))
        # self.wait()
        # self.play(FadeIn(input_2, 0.5*LEFT))
        # self.wait()

        self.play(*[FadeOut(mob) for mob in [input, vector]])
        self.wait()
        input = MathTex(r"\begin{bmatrix}x\\y\\z\end{bmatrix}", color = GREEN).scale(0.8).shift(5.6*LEFT + 0.5*DOWN)
        calculation = MathTex(texs[0]+r"{x}+"+texs[1]+r"{y}+"+texs[2]+r"{z}="+texs[0]+r"{x}+"+texs[1]+r"{y}+"+texs[2]+r"{z}", tex_to_color_map = {(texs[0], texs[1], texs[2]): ORANGE, (r"{x}", r"{y}", r"{z}"): GREEN}).scale(0.8).shift(0.5*DOWN)
        result = MathTex(r"\begin{bmatrix}3x+2y+1z\\2x+3y+1z\\1x+2y+3z\end{bmatrix}").scale(0.8).set_y(-0.5)
        for i in [3, 6, 9, 11, 14, 17, 19, 22, 25]:
            result[i].set_color(GREEN)
        for i in [0, 1, 2, 5, 8, 10, 13, 16, 18, 21, 24, 26, 27]:
            result[i].set_color(ORANGE)
        result.save_state()
        left, middle, right = calculation[:26], calculation[26], calculation[27:]
        copy_left = left.copy().set_x(0)
        self.play(Write(input))
        self.wait()
        self.play(*[TransformFromCopy(input[i], copy_left[j]) for i, j in zip([2, 3, 4], [7, 16, 25])])
        self.wait()
        anims_1 = [TransformFromCopy(matrix[i], copy_left[j]) for i, j in zip([0, 1, 2, 5, 8], [0, 1, 2, 3, 4])]
        anims_1.extend([follow(copy_left[5], anims_1[3], FadeIn), follow(copy_left[6], anims_1[3], FadeIn)])
        anims_2 = [TransformFromCopy(matrix[i], copy_left[j]) for i, j in zip([3, 6, 9], [11, 12, 13])]
        anims_2.extend([follow(copy_left[j], anims_2[1], FadeIn) for j in [9, 10, 14, 15]])
        anims_3 = [TransformFromCopy(matrix[i], copy_left[j]) for i, j in zip([4, 7, 10, 11, 12], [20, 21, 22, 23, 24])]
        anims_3.extend([follow(copy_left[18], anims_3[3], FadeIn), follow(copy_left[19], anims_3[3], FadeIn)])
        self.play(LaggedStart(AnimationGroup(*anims_1), AnimationGroup(*anims_2), AnimationGroup(*anims_3), run_time = 2, lag_ratio = 0.5))
        self.wait()
        self.play(Write(copy_left[8]), Write(copy_left[17]))
        self.wait()
        
        target = box.generate_target()
        target[0].set_width(10.8, stretch = True)
        target[1].scale(np.array([0.5, 1, 1]), about_point = 7*LEFT)
        target[2].scale(np.array([0.5, 1, 1]), about_point = 7*RIGHT)
        middle.save_state().set_x(copy_left.get_x(RIGHT), RIGHT)
        shade = BackgroundRectangle(middle, buff = 0.1).shift(0.05*LEFT)
        anim = ReplacementTransform(copy_left, left)
        self.add(middle, shade, copy_left).play(MoveToTarget(box.save_state()), input.animate.set_x(-6.3), output.animate.set_x(6.3), anim, follow(shade, anim, remover = True), middle.animate.restore(), TransformFromCopy(copy_left, right, path_arc = -PI/3), run_time = 2)
        self.wait()
        left = calculation[:27]
        left.generate_target().set_x(result.get_x(LEFT), LEFT)
        shade = BackgroundRectangle(left, buff = 0.1).shift(0.05*RIGHT)
        self.play(*[ReplacementTransform(right[i], result[j].set_x(right[i].get_x() + 0.6)) for i, j in zip([23, 24], [26, 27])], *[FadeOut(right[i], 0.2*UP) for i in [5, 9, 14, 18]], *[FadeOut(right[i], 0.2*DOWN) for i in [6, 10, 15, 19]])
        self.wait()
        self.play(*[ReplacementTransform(right[i], result[j].set_x(right[i].get_x())) for i, j in zip([0, 1, 2, 11, 20, 3, 7, 8, 12, 16, 17, 21, 25, 4, 13, 22], [0, 1, 2, 5, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24])], *[TransformFromCopy(right[i], result[j].set_x(right[i].get_x())) for i, j in zip([7, 8, 16, 17, 25, 7, 8, 16, 17, 25], [3, 4, 6, 7, 9, 19, 20, 22, 23, 25])])
        self.wait()
        self.add(left, shade.set_x(result.refresh_bounding_box().get_x(LEFT) - 0.2, LEFT), result).play(result.animate.restore(), follow(shade, result, direction = LEFT, remover = True), MoveToTarget(left, remover = True), box.animate.restore(), input.animate.set_x(-5.6), output.animate.set_x(5.6), run_time = 2)
        self.wait()

        equation = MathTex(r"\begin{bmatrix}3x+2y+1z\\2x+3y+1z\\1x+2y+3z\end{bmatrix}=\begin{bmatrix}8\\9\\8\end{bmatrix}", tex_to_color_map = {r"\begin{bmatrix}8\\9\\8\end{bmatrix}": YELLOW}).scale(0.8).set_y(-0.5)
        for i in [3, 6, 9, 11, 14, 17, 19, 22, 25]:
            equation[i].set_color(GREEN)
        for i in [0, 1, 2, 5, 8, 10, 13, 16, 18, 21, 24, 26, 27]:
            equation[i].set_color(ORANGE)
        left, middle, right = equation[:28], equation[28], equation[29:]
        middle.save_state().set_x(result.get_x(RIGHT), RIGHT)
        shade = BackgroundRectangle(middle, buff = 0.1).shift(0.1*LEFT)
        anim = ReplacementTransform(result, left)
        self.add(middle, shade, result).play(MoveToTarget(box.save_state()), input.animate.set_x(-5.6), output.animate.set_x(5.6), anim, follow(shade, anim, remover = True), middle.animate.restore(), TransformFromCopy(output, right, path_arc = -PI/6), run_time = 2)
        self.wait()

        solution = MathTex(r"\begin{cases}3x+2y+1z=8\\2x+3y+1z=9\\1x+2y+3z=8\end{cases}\Rightarrow \begin{cases}x=1\\y=2\\z=1\end{cases}", tex_to_color_map = {(r"x", r"y", r"z", r"{1}", r"{2}"): GREEN, (r"1", r"2", r"3"): ORANGE, (r"8", r"9"): YELLOW}).scale(0.7).shift(2.4*DOWN)
        left, right = solution[:35], solution[35:]
        left.save_state().set_x(0).set_y(equation.get_y(DOWN), DOWN)
        shade = BackgroundRectangle(left, buff = 0.2)
        self.add(left, shade, equation).play(left.animate.set_y(-2.4), run_time = 2)
        self.wait()
        right.save_state().set_x(left.get_x(RIGHT), RIGHT)
        shade = BackgroundRectangle(right, buff = 0.2)
        self.add(right, shade, left).play(left.animate.restore(), follow(shade, left, remover = True), right.animate.restore(), Flip(input, MathTex(r"\begin{bmatrix}1\\2\\1\end{bmatrix}", color = GREEN).scale(0.8).shift(5.6*LEFT + 0.5*DOWN)), run_time = 2)
        self.wait()
        
        
class Video_5(Scene):
    def construct(self):
        title = Title("线性映射")
        titleline = TitleLine()
        
        matrix_1 = MathTex(r"\begin{bmatrix}3&2&1\\2&3&1\\1&2&3\end{bmatrix}", color = ORANGE).scale(0.8).shift(1.5*UP)
        box_1 = BlackBox().shift(1.5*UP)
        matrix_2 = MathTex(r"\begin{bmatrix}3&2&1\\2&2&2\\1&2&3\end{bmatrix}", color = ORANGE).scale(0.8).shift(1.5*DOWN)
        box_2 = BlackBox().shift(1.5*DOWN)
        self.add(title, titleline, box_1, matrix_1, box_2, matrix_2)
        self.wait()

        output_1 = MathTex(r"\begin{bmatrix}8\\9\\8\end{bmatrix}", color = YELLOW).scale(0.8).shift(1.5*UP + 3*RIGHT)
        input_1 = MathTex(r"\begin{bmatrix}1\\2\\1\end{bmatrix}", color = GREEN).scale(0.8).shift(1.5*UP + 3*LEFT)
        output_2 = MathTex(r"\begin{bmatrix}8\\9\\8\end{bmatrix}", color = YELLOW).scale(0.8).shift(1.5*DOWN + 3*RIGHT).save_state()
        self.play(Write(output_1))
        self.wait()
        self.bring_to_back(output_1).play(output_1.animating(remover = True, rate_func = rush_into).scale(0, about_point = 1.5*UP + RIGHT))
        self.bring_to_back(input_1).play(GrowFromPoint(input_1, 1.5*UP + LEFT, rate_func = rush_from))
        self.wait()
        self.play(FadeOut(input_1), Write(output_2))
        self.wait()
        self.bring_to_back(output_2).play(output_2.animating(remover = True, rate_func = rush_into).scale(0, about_point = 1.5*DOWN + RIGHT))
        alpha = ValueTracker(0)
        def shaking_updater(mob: VMobject):
                a = alpha.get_value()
                m,n = 4,5
                Lissajous = np.sin(m*TAU*a/0.5) * 0.05 * UP + np.cos(n*TAU*a/0.5) * 0.05 * RIGHT
                mob.restore().shift(Lissajous)
        matrix_2.save_state().add_updater(shaking_updater)
        box_2.set_stroke(color = RED)
        box_2.save_state().add_updater(shaking_updater)
        self.play(alpha.animate.set_value(1))
        box_2.set_stroke(color = WHITE).clear_updaters()
        matrix_2.clear_updaters()
        def falling_updater(mob: VMobject, dt):
            mob.v += dt
            mob.shift(mob.v*0.5*DOWN).rotate(-2*dt)
        output_2.restore().shift(3*LEFT).rotate(-PI/6).v = 0
        output_2.add_updater(falling_updater)
        self.bring_to_back(output_2).wait(5)
            
#################################################################### 

class Video_6(Scene):
    def construct(self):
        box = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox()).add(MathTex(r"\begin{bmatrix}4&2\\1&1\end{bmatrix}", color = ORANGE)).shift(2*UP)
        equation = MathTex(r"\begin{cases}4x+2y=6\\1x+1y=2\end{cases}", tex_to_color_map = {("1", "2", "4"): ORANGE, ("=2", "6"): YELLOW, "=": WHITE, "x": BLUE, "y": GREEN}).shift(DOWN)
        self.add(box, equation).wait()
        
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-20, 20)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        self.play(box.animate.shift(4*LEFT), FadeOut(equation))
        self.bring_to_back(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).play(LaggedStart(*[ShowCreation(line) for line in lines_h], lag_ratio = 0.2, group = VGroup()), LaggedStart(*[ShowCreation(line) for line in lines_v], lag_ratio = 0.2, group = VGroup()), run_time = 2)
        self.remove(*lines_h, *lines_v)
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        self.bring_to_back(grid).wait()

        texts = r"\begin{bmatrix}4&2\\1&1\end{bmatrix}", r"\begin{bmatrix}1\\1\end{bmatrix}", r"\begin{bmatrix}6\\2\end{bmatrix}"
        matrix = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[0]: ORANGE, texts[1]: GREEN, texts[2]: YELLOW}).set_stroke(width = 8, color = BLACK, background = True).shift(4*LEFT + DOWN)
        parts = [matrix.get_part_by_tex(tex) for tex in [texts[0], texts[1], r"=", texts[2]]]
        self.play(Write(matrix))
        self.wait()

        copy_1 = VGroup(parts[1][0].copy(), parts[1][1].copy(), Line(parts[1].get_center(), parts[1].get_center()), parts[1][2].copy(), parts[1][3].copy())
        copy_2 = VGroup(parts[3][0].copy(), parts[3][1].copy(), Line(parts[3].get_center(), parts[3].get_center()), parts[3][2].copy(), parts[3][3].copy())
        point_1 = Dot(2*ratio*np.array([1, 1, 0]), color = GREEN)
        point_2 = Dot(2*ratio*np.array([6, 2, 0]), color = YELLOW)
        label_1 = MathTex(r"(1, 1)",color = GREEN).next_to(point_1, UL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        label_2 = MathTex(r"(6, 2)",color = YELLOW).next_to(point_2, UR, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        arrow = Arrow(point_1, point_2, color = [GREEN, YELLOW])
        self.play(ReplacementTransform(copy_1, label_1, run_time = 2, path_arc = -PI/6), ReplacementTransform(copy_2, label_2, run_time = 2, path_arc = -PI/6), ShowCreation(point_1), ShowCreation(point_2))
        self.wait()
        self.play(ShowCreation(arrow))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [matrix, label_1, label_2]])
        self.wait()

        points = [Dot(2*ratio*np.array([1, i, 0]), color = GREEN) for i in range(-5, 6)]
        arrows = [Arrow(2*ratio*np.array([1, i, 0]), 2*ratio*np.array([2*i+4, i+1, 0]), color = [GREEN, YELLOW]) for i in range(-5, 6) if i != 1]
        self.play(ShowCreation(VGroup(*points)), run_time = 2)
        self.remove(point_1).wait()
        self.play(*[ShowCreation(arrow) for arrow in arrows])
        self.wait()

        anims = []
        targets = []
        for mob in points:
            position = mob.get_center()
            target = Dot(np.array([4*position[0]+2*position[1], position[0]+position[1], 0]), color = YELLOW)
            targets.append(target)
            anims.append(TransformFromCopy(mob, target))
        self.play(*anims, run_time = 2)
        self.remove(point_2).wait()
        
        back = grid.copy().set_color(GREY)
        line = Line(ratio*2*(12*UP + RIGHT), ratio*2*(12*DOWN + RIGHT), color = GREEN)
        self.play(Write(line))
        self.bring_to_back(back).play(grid.save_state().animate.apply_matrix(np.array([[4, 2], [1, 1]])), line.animate.apply_matrix(np.array([[4, 2], [1, 1]])).set_color(YELLOW), run_time = 3)
        self.wait()
        self.play(*[FadeOut(mob) for mob in points + targets + arrows + [arrow]], FadeOut(line))
        self.wait()

        self.play(grid.animate.restore(), run_time = 3)
        self.wait()
        self.play(grid.animate.apply_matrix(np.array([[4, 2], [1, 1]])), run_time = 3)
        self.wait()

        indicates_h = [Line(4*UP+8*RIGHT, 4*DOWN+8*LEFT, stroke_width = 0 if i%2 else 8, color = YELLOW).shift(2*ratio*i*LEFT) for i in range(-20, 20)]
        indicates_v = [Line(2*UP+8*RIGHT, 2*DOWN+8*LEFT, stroke_width = 0 if i%2 else 8, color = YELLOW).shift(0.5*ratio*i*DOWN) for i in range(-30, 30)]
        self.add(*indicates_h, box).play(LaggedStart(*[ShowPassingFlash(mob, rate_func = linear) for mob in indicates_h], lag_ratio = 0.02, group = VGroup(), rate_func = linear), run_time = 3)
        self.add(*indicates_v, box).play(LaggedStart(*[ShowPassingFlash(mob, rate_func = linear) for mob in indicates_v], lag_ratio = 0.01, group = VGroup(), rate_func = linear), run_time = 3)
        self.wait()

        vec_1, vec_2 = 2*ratio*np.array([4, 1, 0]), 2*ratio*np.array([2, 1, 0])
        cell = Polygon(ORIGIN, vec_1, vec_1+vec_2, vec_2, stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE)
        cells = VGroup()
        for i in range(-14, 15):
            for j in range(-14, 15):
                if (i+j)%2 == 0:
                    cells.add(cell.copy().shift(i*vec_1+j*vec_2))
        self.bring_to_back(back, cells).play(FadeIn(cells))
        self.wait()
        self.play(FadeOut(cells))
        self.wait()

class Video_7(Scene):
    def construct(self):
        box = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox()).add(MathTex(r"\begin{bmatrix}4&2\\1&1\end{bmatrix}", color = ORANGE)).shift(2*UP + 4*LEFT)
        ratio = 0.4
        lines_h = [Line(6*LEFT_SIDE + i*ratio*DOWN, 6*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-60, 60)]
        lines_v = [Line(6*4*UP + i*ratio*RIGHT, 6*4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-100, 100)]
        operator = np.array([[4, 2], [1, 1]])
        inverse = np.array([[0.5, -1], [-0.5, 2]])
        grid = VGroup(*lines_h[:60], *lines_h[61:], *lines_v, lines_h[60])
        base = grid.copy().set_color(GREY).save_state().apply_matrix(operator)
        back = grid.copy().save_state().set_color(GREY)
        grid.save_state().apply_matrix(operator)
        self.add(back, grid, box).wait()
        
        shade = Shade(fill_color = BLUE, fill_opacity = 0.2)
        self.bring_to_back(shade).play(FadeIn(shade, rate_func = double_there_and_back, remover = True), run_time = 2)
        self.wait()

        point_1 = Dot(2*ratio*(1*RIGHT + 2*UP), color = GREEN)
        point_2 = Dot(2*ratio*(8*RIGHT + 3*UP), color = YELLOW)
        label_1 = MathTex(r"(1, 2)",color = GREEN).next_to(point_1, UL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        label_2 = MathTex(r"(8, 3)",color = YELLOW).next_to(point_2, UL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        texts = r"\begin{bmatrix}4&2\\1&1\end{bmatrix}", r"\begin{bmatrix}1\\2\end{bmatrix}", r"\begin{bmatrix}8\\3\end{bmatrix}"
        matrix = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[0]: ORANGE, texts[1]: GREEN, texts[2]: YELLOW}).set_stroke(width = 8, color = BLACK, background = True).shift(4*LEFT + DOWN)
        notation = MathTex(r"A\vec{x}=\vec{b}", tex_to_color_map = {r"A": ORANGE, r"\vec{x}": GREEN, r"\vec{b}": YELLOW}).set_stroke(width = 8, color = BLACK, background = True).next_to(matrix, DOWN)
        arrow = Arrow(point_2, point_1, color = [YELLOW, GREEN])
        self.play(ShowCreation(point_2), Write(label_2))
        self.wait()
        self.play(Write(matrix), Write(notation))
        self.wait()
        self.play(grid.animate.restore(), TransformFromCopy(point_2, point_1), run_time = 3)
        self.play(Write(label_1))
        self.wait()
        self.play(grid.animate.apply_matrix(operator), TransformFromCopy(point_1, point_2.copy(), remover = True), run_time = 3)
        self.wait()
        self.play(ShowCreation(arrow))
        self.wait()

        self.bring_to_back(base).play(FadeOut(box), FadeOut(grid), back.animate.restore())
        self.wait()
        self.play(base.animate.restore().set_color(GREY), back.animate.apply_matrix(inverse), TransformFromCopy(point_2, point_1.copy(), remover = True), run_time = 3)
        self.wait()

        box_wide = BlackBox()
        box_wide[0].scale(np.array([1.5, 1, 1]))
        box_wide[1].shift(0.5*LEFT)
        box_wide[2].shift(0.5*RIGHT)
        box_2 = box_wide.copy().set_stroke(color = BLACK, width = 16).add(box_wide).add(MathTex(r"\begin{bmatrix}0.5&-1\\-0.5&2\end{bmatrix}", color = TEAL)).shift(2*UP + 4*LEFT)
        texts = r"\begin{bmatrix}0.5&-1\\-0.5&2\end{bmatrix}", r"\begin{bmatrix}8\\3\end{bmatrix}", r"\begin{bmatrix}1\\2\end{bmatrix}"
        matrix_2 = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[0]: TEAL, texts[1]: YELLOW, texts[2]: GREEN}).set_stroke(width = 8, color = BLACK, background = True).shift(4*RIGHT + DOWN)
        notation_2 = MathTex(r"A^{-1}\vec{b}=\vec{x}", tex_to_color_map = {r"A^{-1}": TEAL, r"\vec{x}": GREEN, r"\vec{b}": YELLOW}).set_stroke(width = 8, color = BLACK, background = True).next_to(matrix_2, DOWN)
        self.play(FadeIn(box_2, 0.5*DOWN), Write(notation_2), Write(matrix_2))
        self.wait()

        shade = Shade(fill_color = BLUE, fill_opacity = 0.2)
        self.bring_to_back(shade).play(FadeIn(shade, rate_func = double_there_and_back, remover = True), run_time = 2)
        self.wait()

class Video_8(Scene):
    def construct(self):
        box = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox()).add(MathTex(r"\begin{bmatrix}4&2\\2&1\end{bmatrix}", color = ORANGE)).shift(1.5*UP)
        self.add(box).wait()
        
        ratio = 0.8
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 2 if i else 4, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(8*UP + i*ratio*RIGHT, 8*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 4, color = BLUE_E if i else WHITE) for i in range(-20, 20)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        base = grid.copy().set_color(GREY)
        self.play(box.animate.shift(4*LEFT))
        self.bring_to_back(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).play(LaggedStart(*[ShowCreation(line) for line in lines_h], lag_ratio = 0.2, group = VGroup()), LaggedStart(*[ShowCreation(line) for line in lines_v], lag_ratio = 0.2, group = VGroup()), run_time = 2)
        self.remove(*lines_h, *lines_v).bring_to_back(base, grid).wait()

        operator = np.array([[4, 2], [2, 1]])
        self.play(grid.save_state().animate.apply_matrix(operator), run_time = 3)
        self.wait()

        point_1 = Dot(ratio*(6*RIGHT + 3*UP), color = YELLOW)
        label_1 = MathTex(r"(6, 3)",color = YELLOW).next_to(point_1, UL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        point_2 = Dot(ratio*(8*RIGHT + 3*UP), color = YELLOW)
        label_2 = MathTex(r"(8, 3)",color = YELLOW).next_to(point_2, UL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        texts = r"\begin{bmatrix}4&2\\2&1\end{bmatrix}", r"\begin{bmatrix}x\\y\end{bmatrix}", r"\begin{bmatrix}8\\3\end{bmatrix}"
        matrix = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[0]: ORANGE, texts[1]: GREEN, texts[2]: YELLOW}).set_stroke(width = 8, color = BLACK, background = True).shift(4*LEFT + DOWN)
        texts = r"\begin{bmatrix}4&2\\2&1\end{bmatrix}", r"\begin{bmatrix}1\\1\end{bmatrix}", r"\begin{bmatrix}6\\3\end{bmatrix}"
        matrix_2 = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[0]: ORANGE, texts[1]: GREEN, texts[2]: YELLOW}).set_stroke(width = 8, color = BLACK, background = True).shift(4*LEFT + DOWN)
        judge = Songti("无解", color = RED).scale(0.8).next_to(matrix).set_stroke(width = 8, color = BLACK, background = True)
        judge_2 = Songti("有解", color = RED).scale(0.8).next_to(matrix).set_stroke(width = 8, color = BLACK, background = True)
        self.play(ShowCreation(point_2), Write(label_2), Write(matrix))
        self.wait()
        self.play(Write(judge))
        self.wait()
        self.play(Transform(point_2, point_1), Transform(label_2, label_1), FadeTransform(matrix, matrix_2), FadeOut(judge))
        self.wait()
        self.play(Write(judge_2))
        self.wait()

        self.play(*[FadeOut(mob) for mob in [matrix_2, judge_2, point_2, label_2]])
        self.wait()
        line = Line(4*UP+8*RIGHT, 4*DOWN+8*LEFT, color = YELLOW, stroke_width = 6)
        self.play(ShowPassingFlash(line.copy().set_stroke(width = 8)))
        self.play(ShowPassingFlash(line.copy().set_stroke(width = 8)), FadeIn(line))
        self.wait()

        title = Title("列空间").set_stroke(width = 8, color = BLACK, background = True)
        titleline = TitleLine().set_stroke(width = 12, color = BLACK).add(TitleLine())
        titleback = Shade(fill_color = BLACK, height = 1).shift(3.5*UP)
        self.play(titleback.save_state().scale(np.array([0, 1, 1])).animate.restore(), Write(title), GrowFromCenter(titleline))
        self.wait()
        target = box[4].generate_target()
        target[1].set_fill(color = BLUE)
        target[2].set_fill(color = GREEN)
        target[3].set_fill(color = BLUE)
        target[4].set_fill(color = GREEN)
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([4, 2, 0])), buff = 0, color = BLUE, width_to_tip_len = 0.015, tip_width_ratio = 5)
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = GREEN, width_to_tip_len = 0.015, tip_width_ratio = 5)
        col = MathTex(r"col(A)=\left\{\vec{x}\in \mathbb{R}^2:\ \vec{x}=c_1\begin{bmatrix}4\\2\end{bmatrix}+c_2\begin{bmatrix}2\\1\end{bmatrix}\right\}", tex_to_color_map = {r"A": ORANGE, (r"\vec{x}", r"c_1", r"c_2"): YELLOW, r"\begin{bmatrix}4\\2\end{bmatrix}": BLUE, r"\begin{bmatrix}2\\1\end{bmatrix}": GREEN}).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).next_to(2*DOWN + LEFT)
        self.play(Write(col), MoveToTarget(box[4]), GrowArrow(arrow_1), GrowArrow(arrow_2))
        self.wait()
        point_1 = Dot(2*ratio*(6*RIGHT + 3*UP), color = YELLOW)
        label_1 = Songti(r"有解",color = RED).next_to(point_1, UL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        point_2 = Dot(2*ratio*(8*RIGHT + 3*UP), color = YELLOW)
        label_2 = Songti(r"无解",color = RED).next_to(point_2, DL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        self.play(ShowCreation(point_1), ShowCreation(point_2), Write(label_1), Write(label_2))
        self.wait()
        self.fade_out(excepts = [titleback, title, titleline])

        operator = MathTex(r"\begin{bmatrix}4&2\\1&1\end{bmatrix}")
        operator[0].set_fill(color = ORANGE)
        operator[1].set_fill(color = BLUE)
        operator[2].set_fill(color = GREEN)
        operator[3].set_fill(color = BLUE)
        operator[4].set_fill(color = GREEN)
        operator[5].set_fill(color = ORANGE)
        box = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox(), operator).shift(1.5*UP + 4*LEFT)
        ratio = 0.8
        YELLOW_G = interpolate_color(YELLOW, GREY, 0.5)
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 2 if i else 4, color = YELLOW_G if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 4, color = YELLOW_G if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        base = grid.copy().set_color(GREY)
        operator = np.array([[4, 2], [1, 1]])
        grid.apply_matrix(operator)
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([4, 1, 0])), buff = 0, color = BLUE, width_to_tip_len = 0.015, tip_width_ratio = 5)
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = GREEN, width_to_tip_len = 0.015, tip_width_ratio = 5)
        col = MathTex(r"col(A)=\left\{\vec{x}\in \mathbb{R}^2:\ \vec{x}=c_1\begin{bmatrix}4\\2\end{bmatrix}+c_2\begin{bmatrix}2\\1\end{bmatrix}\right\}", tex_to_color_map = {r"A": ORANGE, (r"\vec{x}", r"c_1", r"c_2"): YELLOW, r"\begin{bmatrix}4\\2\end{bmatrix}": BLUE, r"\begin{bmatrix}2\\1\end{bmatrix}": GREEN}).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).next_to(2*DOWN + LEFT)
        self.fade_in(base, grid, box, arrow_1, arrow_2, col, excepts = [titleback, title, titleline])
        self.wait()
        point_1 = Dot(2*ratio*(6*RIGHT + 3*UP), color = YELLOW)
        label_1 = Songti(r"有解",color = RED).next_to(point_1, UL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        point_2 = Dot(2*ratio*(8*RIGHT + 3*UP), color = YELLOW)
        label_2 = Songti(r"有解",color = RED).next_to(point_2, DL, buff = 0.15).set_stroke(width = 8, color = BLACK, background = True)
        self.play(ShowCreation(point_1), ShowCreation(point_2), Write(label_1), Write(label_2))
        self.wait()
        self.fade_out(excepts = [titleback, title, titleline])
        operator = MathTex(r"\begin{bmatrix}4&2\\2&1\end{bmatrix}")
        operator[0].set_fill(color = ORANGE)
        operator[1].set_fill(color = BLUE)
        operator[2].set_fill(color = GREEN)
        operator[3].set_fill(color = BLUE)
        operator[4].set_fill(color = GREEN)
        operator[5].set_fill(color = ORANGE)
        box = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox(), operator).shift(1.5*UP + 4*LEFT)
        ratio = 0.8
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 2 if i else 4, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 4, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        base = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30]).set_color(GREY)
        grid = Line(4*UP+8*RIGHT, 4*DOWN+8*LEFT, color = YELLOW, stroke_width = 6)
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([4, 2, 0])), buff = 0, color = BLUE, width_to_tip_len = 0.015, tip_width_ratio = 5)
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = GREEN, width_to_tip_len = 0.015, tip_width_ratio = 5)
        col = MathTex(r"col(A)=\left\{\vec{x}\in \mathbb{R}^2:\ \vec{x}=c_1\begin{bmatrix}4\\2\end{bmatrix}+c_2\begin{bmatrix}2\\1\end{bmatrix}\right\}", tex_to_color_map = {r"A": ORANGE, (r"\vec{x}", r"c_1", r"c_2"): YELLOW, r"\begin{bmatrix}4\\2\end{bmatrix}": BLUE, r"\begin{bmatrix}2\\1\end{bmatrix}": GREEN}).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).next_to(2*DOWN + LEFT)
        self.fade_in(base, grid, box, arrow_1, arrow_2, col, excepts = [titleback, title, titleline])
        self.wait()

#################################################################### 

class Patch9_1(Scene):
    def construct(self):
        ratio = 1.2
        YELLOW_G = interpolate_color(YELLOW, GREY, 0.5)
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 3 if i else 6, color = YELLOW_G if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 3 if i else 6, color = YELLOW_G if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        base = grid.copy().set_color(GREY)
        operator = np.array([[4, 2], [1, 1]])
        grid.apply_matrix(operator)
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([4, 1, 0])), buff = 0, color = BLUE, stroke_width = 8, width_to_tip_len = 0.015, tip_width_ratio = 5)
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = GREEN, stroke_width = 8, width_to_tip_len = 0.015, tip_width_ratio = 5)
        self.add(base, grid, arrow_1, arrow_2)
        
class Patch9_2(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (16.0, 8.0)}, 
            }
    }
    def construct(self):
        ratio = 1.2
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 3 if i else 6, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 3 if i else 6, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        base = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30]).set_color(GREY)
        grid = Line(4*UP+8*RIGHT, 4*DOWN+8*LEFT, color = YELLOW, stroke_width = 6)
        # arrow_1 = Arrow(ORIGIN, ratio*(np.array([4, 2, 0])), buff = 0, color = BLUE, stroke_width = 8, width_to_tip_len = 0.015, tip_width_ratio = 5)
        # arrow_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = GREEN, stroke_width = 8, width_to_tip_len = 0.015, tip_width_ratio = 5)
        self.add(base, grid) #, arrow_1, arrow_2

class Video_9(Scene):
    def construct(self):
        graph_left = ImageMobject("Patch9_1.png", height = 4).shift(32/9*LEFT + 2*DOWN)
        graph_right = ImageMobject("Patch9_2.png", height = 4).shift(32/9*RIGHT + 2*DOWN)
        line_left = Line(4*UP, 4*DOWN).shift(0.05*LEFT)
        line_right = Line(4*UP, 4*DOWN, color = YELLOW_E).shift(0.05*RIGHT)
        line_middle = VGroup(Rectangle(width = 0.1, height = 8, stroke_width = 0, fill_opacity = 1, fill_color = BLACK), line_left, line_right)
        color_map = [ORANGE, BLUE, GREEN, BLUE, GREEN, ORANGE]
        operator = MathTex(r"\begin{bmatrix}4&2\\1&1\end{bmatrix}")
        for i in range(6):
            operator[i].set_fill(color = color_map[i])
        box_left = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox(), operator).shift(2.5*UP + 32/9*LEFT)
        operator = MathTex(r"\begin{bmatrix}4&2\\2&1\end{bmatrix}")
        for i in range(6):
            operator[i].set_fill(color = color_map[i])
        box_right = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox(), operator).shift(2.5*UP + 32/9*RIGHT)
        ratio = 0.6
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([4, 2, 0])), buff = 0, color = BLUE, width_to_tip_len = 0.015, tip_width_ratio = 5).shift(32/9*RIGHT + 2*DOWN)
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = GREEN, width_to_tip_len = 0.015, tip_width_ratio = 5).shift(32/9*RIGHT + 2*DOWN)
        self.add(graph_right, graph_left, line_middle, box_left, box_right, arrow_1, arrow_2)

        shade = Shade(fill_color = YELLOW_D, fill_opacity = 0.2).scale(0.5).shift(32/9*LEFT + 2*DOWN)
        self.add(shade, line_middle).play(FadeIn(shade, rate_func = double_there_and_back, remover = True), run_time = 2)
        self.wait()
        line = Line(4*LEFT + 2*DOWN, 4*RIGHT + 2*UP, color = YELLOW, stroke_width = 6).shift(32/9*RIGHT + 2*DOWN)
        self.add(line, graph_left, line_middle).play(ShowPassingFlash(line))
        self.add(line, graph_left, line_middle).play(ShowPassingFlash(line))
        self.wait()

        self.play(WiggleOutThenIn(arrow_1), WiggleOutThenIn(arrow_2))
        self.wait()
        copy_1 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, stroke_width = 3, color = GREEN, width_to_tip_len = 0.015, tip_width_ratio = 5).shift(32/9*RIGHT + 2*DOWN + 0.2*UP + 0.1*LEFT)
        copy_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, stroke_width = 3, color = GREEN, width_to_tip_len = 0.015, tip_width_ratio = 5).shift(32/9*RIGHT + 2*DOWN + 0.2*UP + 0.1*LEFT).shift(ratio*(np.array([2, 1, 0])))
        self.play(TransformFromCopy(arrow_2, copy_2), TransformFromCopy(arrow_2, copy_1))
        self.wait()
        self.play(FadeOut(copy_2), FadeOut(copy_1))
        self.wait()

        rank_left = MathTexText(r"秩为2", color = RED).scale(1.2).shift(0.8*UP + 32/9*LEFT).set_stroke(width = 8, color = BLACK, background = True)
        rank_right = MathTexText(r"秩为1", color = RED).scale(1.2).shift(0.8*UP + 32/9*RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        self.play(Write(rank_left), Write(rank_right))
        self.wait()
        
#################################################################### 

class Video_10(Scene):
    def construct(self):
        color_map = [ORANGE, BLUE, GREEN, BLUE, GREEN, ORANGE]
        operator = MathTex(r"\begin{bmatrix}4&2\\2&1\end{bmatrix}")
        for i in range(6):
            operator[i].set_fill(color = color_map[i])
        box = BlackBox().set_stroke(color = BLACK, width = 16).add(BlackBox(), operator).shift(1.5*UP + 4*LEFT)
        ratio = 0.8
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 2 if i else 4, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 4, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        base = grid.copy().set_color(GREY)
        operator = np.array([[4, 2], [2, 1]])
        grid.add(Line(12*UP+6*LEFT, 12*DOWN+6*RIGHT, color = TEAL)).save_state().apply_matrix(operator)
        col = Line(4*UP+8*RIGHT, 4*DOWN+8*LEFT, color = YELLOW, stroke_width = 6)
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([4, 2, 0])), buff = 0, color = BLUE, width_to_tip_len = 0.015, tip_width_ratio = 5)
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = GREEN, width_to_tip_len = 0.015, tip_width_ratio = 5)
        self.add(base, grid, col, box, arrow_1, arrow_2).wait()

        equation = MathTex(r"\begin{bmatrix}4\\2\end{bmatrix}=2\begin{bmatrix}2\\1\end{bmatrix}", tex_to_color_map = {r"\begin{bmatrix}2\\1\end{bmatrix}": GREEN, r"\begin{bmatrix}4\\2\end{bmatrix}": BLUE}).scale(0.8).shift(0.5*RIGHT + DOWN).set_stroke(width = 16, color = BLACK, background = True)
        self.play(Write(equation))
        self.wait()
        offset = 3*RIGHT + 2*DOWN
        buff = 0.2*UP + 0.1*LEFT
        arrows_1 = VGroup(arrow_2.copy().shift(offset), arrow_2.copy().shift(offset + ratio*(np.array([2, 1, 0]))))
        arrows_2 = arrow_1.copy().rotate(PI).shift(offset + buff)
        self.play(ShowCreation(VGroup(arrows_1, arrows_2)))
        self.wait()
        texts = r"\begin{bmatrix}4&2\\2&1\end{bmatrix}", r"\begin{bmatrix}-1\\2\end{bmatrix}", r"\begin{bmatrix}0\\0\end{bmatrix}"
        matrix = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[1]: TEAL, texts[2]: GREY}).set_stroke(width = 16, color = BLACK, background = True).shift(4*LEFT + 0.5*DOWN)
        for i in range(6):
            matrix[i].set_fill(color = color_map[i])
        self.play(Write(matrix))
        self.wait()

        matrix.insert_submobject(10, Line(ORIGIN, ORIGIN, fill_color = TEAL, fill_opacity = 1).set_stroke(width = 16, color = BLACK, background = True).shift(matrix[9].get_right()))
        texts = r"\begin{bmatrix}4&2\\2&1\end{bmatrix}", r"\begin{bmatrix}-k\\2k\end{bmatrix}", r"\begin{bmatrix}0\\0\end{bmatrix}"
        matrix_2 = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[1]: TEAL, texts[2]: GREY}).set_stroke(width = 16, color = BLACK, background = True).shift(4*LEFT + 0.5*DOWN)
        for i in range(6):
            matrix_2[i].set_fill(color = color_map[i])
        self.play(ReplacementTransform(matrix, matrix_2), equation.animating(arc = -PI/4).next_to(matrix_2, DOWN))
        self.wait()
        self.play(arrows_1.save_state().animate.scale(1.5, about_point = 8*RIGHT + 2*DOWN), arrows_2.save_state().animate.scale(1.5, about_point = 8*RIGHT + 2*DOWN + buff))
        self.wait()
        self.play(arrows_1.animate.rotate(PI), arrows_2.animate.rotate(PI))
        self.wait()
        self.play(arrows_1.animate.scale(1/3, about_point = 4*RIGHT + DOWN), arrows_2.animate.scale(1/3, about_point = 4*RIGHT + DOWN + buff))
        self.wait()

        position = ratio*np.array([-1, 2, 0])
        point = Dot(position, color = TEAL)
        shadow_1, shadow_2 = arrow_1.copy().set_color(BLUE_E), arrow_2.copy().set_color(GREEN_E)
        self.add(shadow_1, shadow_2).play(Transform(arrow_1.save_state(), Arrow(ORIGIN, ratio*RIGHT, buff = 0, color = BLUE, stroke_width = 6), run_time = 3), Transform(arrow_2.save_state(), Arrow(ORIGIN, ratio*UP, buff = 0, color = GREEN, stroke_width = 6), run_time = 3), grid.animating(run_time = 3).restore(), GrowFromPoint(point, ORIGIN, run_time = 3), arrows_1.animating(run_time = 2).restore().shift(LEFT), arrows_2.animating(run_time = 2).restore().shift(LEFT))
        self.wait()
        self.play(point.animate.move_to(1.5*position), arrows_1.animate.scale(1.5), arrows_2.animate.scale(1.5))
        self.wait()
        self.play(point.animate.move_to(0.5*position), arrows_1.animate.scale(1/3), arrows_2.animate.scale(1/3))
        self.wait()
        self.play(point.animate.move_to(-position), arrows_1.animate.scale(2).rotate(PI), arrows_2.animate.scale(2).rotate(PI))
        self.wait()
        self.add(arrow_1, arrow_2).play(grid.animating(run_time = 3).apply_matrix(operator), arrow_1.animating(run_time = 3).restore(), arrow_2.animating(run_time = 3).restore(), FadeOut(arrows_1), FadeOut(arrows_2), point.animating(run_time = 3, remover = True).scale(0, about_point = ORIGIN))
        self.remove(shadow_1, shadow_2).wait()        

        self.remove(grid, col)
        ratio = 0.8
        lines_h = [Line(20*ratio*(2*UP+LEFT), 20*ratio*(2*DOWN+RIGHT), stroke_width = 2 if i else 4, color = TEAL_E if i else TEAL).shift(i*ratio*(2*RIGHT + UP)/2) for i in range(-20, 20)]
        lines_v = [Line(10*ratio*(2*RIGHT+UP), 10*ratio*(2*LEFT+DOWN), stroke_width = 2 if i else 4, color = YELLOW_E if i else YELLOW).shift(i*ratio*(2*UP + LEFT)) for i in range(-20, 20)]
        grid = VGroup(*lines_h[:20], *lines_h[21:], *lines_v, lines_h[20]).save_state().apply_matrix(operator)
        self.add(grid, arrow_1, arrow_2, box, matrix_2, equation).play(grid.animate.restore(), run_time = 3)
        self.wait()
        
        points = [Dot(i*ratio*(2*RIGHT + UP)*5/2, color = TEAL_E if i else TEAL) for i in range(-20, 20)]
        self.add(*points, box, matrix_2, equation).play(grid.animate.apply_matrix(operator), *[TransformFromCopy(line, point) for line, point in zip(lines_h, points)], run_time = 3)
        self.wait()
        dot = Dot(ratio*(2*RIGHT + UP)*5/2, radius = 0.12, color = PURPLE_A).save_state().scale(3).set_stroke(width = 4).set_fill(opacity = 0)
        self.add(dot, arrow_1, arrow_2).play(ShowCreation(dot))#, rate_func = rush_into)
        self.play(dot.animate.restore())#, rate_func = rush_from)
        self.wait()
        self.play(grid.animate.restore(), Transform(arrow_1, Arrow(ORIGIN, ratio*RIGHT, buff = 0, color = BLUE, stroke_width = 6)), Transform(arrow_2, Arrow(ORIGIN, ratio*UP, buff = 0, color = GREEN, stroke_width = 6)), *[Transform(point, line, remover = True) for line, point in zip(lines_h, points)], Transform(dot.save_state(), Line(20*ratio*(2*UP+LEFT), 20*ratio*(2*DOWN+RIGHT), color = PURPLE_A, fill_opacity = 1).shift(ratio*(2*RIGHT + UP)/2)), run_time = 3)
        self.wait()
        
        function = MathTex(r"\begin{bmatrix}1\\0.5\end{bmatrix}+k\begin{bmatrix}-1\\2\end{bmatrix}", tex_to_color_map = {r"\begin{bmatrix}1\\0.5\end{bmatrix}": PURPLE, r"\begin{bmatrix}-1\\2\end{bmatrix}": TEAL}).shift(0.5*DOWN + 4*RIGHT).set_stroke(width = 16, color = BLACK, background = True)
        self.play(Write(function))
        self.wait()
        result = MathTex(r"\begin{bmatrix}4&2\\2&1\end{bmatrix}\left(\begin{bmatrix}1\\0.5\end{bmatrix}+k\begin{bmatrix}-1\\2\end{bmatrix}\right)=\begin{bmatrix}4&2\\2&1\end{bmatrix}\begin{bmatrix}1\\0.5\end{bmatrix}", tex_to_color_map = {r"\begin{bmatrix}1\\0.5\end{bmatrix}": PURPLE, r"\begin{bmatrix}-1\\2\end{bmatrix}": TEAL}).scale(0.8).next_to(function, DOWN).shift(1.5*LEFT).set_stroke(width = 16, color = BLACK, background = True)
        for i in range(6):
            result[i].set_fill(color = color_map[i])
            result[i+22].set_fill(color = color_map[i])
        self.play(Write(result))
        self.wait()
        self.play(grid.animating(run_time = 3).apply_matrix(operator), arrow_1.animating(run_time = 3).restore(), arrow_2.animating(run_time = 3).restore(), dot.animating(run_time = 3).restore())
        self.wait()


class Video_10_2(Scene):
    def construct(self):
        color_map = [ORANGE, BLUE, GREEN, BLUE, GREEN, ORANGE]
        operator = MathTex(r"\begin{bmatrix}4&2\\2&1\end{bmatrix}")
        for i in range(6):
            operator[i].set_fill(color=color_map[i])
        box = BlackBox().set_stroke(color=BLACK, width=16).add(BlackBox(), operator).shift(1.5 * UP + 4 * LEFT)
        ratio = 0.8
        lines_h = [Line(3 * LEFT_SIDE + i * ratio * DOWN, 3 * RIGHT_SIDE + i * ratio * DOWN, stroke_width=2 if i else 4,
                        color=BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3 * 4 * UP + i * ratio * RIGHT, 3 * 4 * DOWN + i * ratio * RIGHT, stroke_width=2 if i else 4,
                        color=BLUE_E if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        base = grid.copy().set_color(GREY)
        operator = np.array([[4, 2], [2, 1]])
        grid.add(Line(12 * UP + 6 * LEFT, 12 * DOWN + 6 * RIGHT, color=TEAL)).save_state().apply_matrix(operator)
        col = Line(4 * UP + 8 * RIGHT, 4 * DOWN + 8 * LEFT, color=YELLOW, stroke_width=6)
        arrow_1 = Arrow(ORIGIN, ratio * (np.array([4, 2, 0])), buff=0, color=BLUE, width_to_tip_len=0.015,
                        tip_width_ratio=5)
        arrow_2 = Arrow(ORIGIN, ratio * (np.array([2, 1, 0])), buff=0, color=GREEN, width_to_tip_len=0.015,
                        tip_width_ratio=5)
        self.add(base, grid, col, box, arrow_1, arrow_2).wait()

        equation = MathTex(r"\begin{bmatrix}4\\2\end{bmatrix}=2\begin{bmatrix}2\\1\end{bmatrix}",
                        tex_to_color_map={r"\begin{bmatrix}2\\1\end{bmatrix}": GREEN,
                                          r"\begin{bmatrix}4\\2\end{bmatrix}": BLUE}).scale(0.8).shift(
            0.5 * RIGHT + DOWN).set_stroke(width=16, color=BLACK, background=True)
        self.play(Write(equation))
        self.wait()
        offset = 3 * RIGHT + 2 * DOWN
        buff = 0.2 * UP + 0.1 * LEFT
        arrows_1 = VGroup(arrow_2.copy().shift(offset), arrow_2.copy().shift(offset + ratio * (np.array([2, 1, 0]))))
        arrows_2 = arrow_1.copy().rotate(PI).shift(offset + buff)
        self.play(ShowCreation(VGroup(arrows_1, arrows_2)))
        self.wait()
        texts = r"\begin{bmatrix}4&2\\2&1\end{bmatrix}", r"\begin{bmatrix}-1\\2\end{bmatrix}", r"\begin{bmatrix}0\\0\end{bmatrix}"
        matrix = MathTex(texts[0] + texts[1] + r"=" + texts[2], isolate="=",
                      tex_to_color_map={texts[1]: TEAL, texts[2]: GREY}).set_stroke(width=16, color=BLACK,
                                                                                    background=True).shift(
            4 * LEFT + 0.5 * DOWN)
        for i in range(6):
            matrix[i].set_fill(color=color_map[i])
        self.play(Write(matrix))
        self.wait()

        matrix.insert_submobject(10,
                                 Line(ORIGIN, ORIGIN, fill_color=TEAL, fill_opacity=1).set_stroke(width=16, color=BLACK,
                                                                                                  background=True).shift(
                                     matrix[9].get_right()))
        texts = r"\begin{bmatrix}4&2\\2&1\end{bmatrix}", r"\begin{bmatrix}-k\\2k\end{bmatrix}", r"\begin{bmatrix}0\\0\end{bmatrix}"
        matrix_2 = MathTex(texts[0] + texts[1] + r"=" + texts[2], isolate="=",
                        tex_to_color_map={texts[1]: TEAL, texts[2]: GREY}).set_stroke(width=16, color=BLACK,
                                                                                      background=True).shift(
            4 * LEFT + 0.5 * DOWN)
        for i in range(6):
            matrix_2[i].set_fill(color=color_map[i])
        self.play(ReplacementTransform(matrix, matrix_2), equation.animating(arc=-PI / 4).next_to(matrix_2, DOWN))
        self.wait()
        self.play(arrows_1.save_state().animate.scale(1.5, about_point=8 * RIGHT + 2 * DOWN),
                  arrows_2.save_state().animate.scale(1.5, about_point=8 * RIGHT + 2 * DOWN + buff))
        self.wait()
        self.play(arrows_1.animate.rotate(PI), arrows_2.animate.rotate(PI))
        self.wait()
        self.play(arrows_1.animate.scale(1 / 3, about_point=4 * RIGHT + DOWN),
                  arrows_2.animate.scale(1 / 3, about_point=4 * RIGHT + DOWN + buff))
        self.wait()

        position = ratio * np.array([-1, 2, 0])
        point = Dot(position, color=TEAL)
        shadow_1, shadow_2 = arrow_1.copy().set_color(BLUE_E), arrow_2.copy().set_color(GREEN_E)
        self.add(shadow_1, shadow_2).play(
            Transform(arrow_1.save_state(), Arrow(ORIGIN, ratio * RIGHT, buff=0, color=BLUE, stroke_width=6),
                      run_time=3),
            Transform(arrow_2.save_state(), Arrow(ORIGIN, ratio * UP, buff=0, color=GREEN, stroke_width=6), run_time=3),
            grid.animating(run_time=3).restore(), GrowFromPoint(point, ORIGIN, run_time=3),
            arrows_1.animating(run_time=2).restore().shift(LEFT), arrows_2.animating(run_time=2).restore().shift(LEFT))
        self.wait()
        self.play(point.animate.move_to(1.5 * position), arrows_1.animate.scale(1.5), arrows_2.animate.scale(1.5))
        self.wait()
        self.play(point.animate.move_to(0.5 * position), arrows_1.animate.scale(1 / 3), arrows_2.animate.scale(1 / 3))
        self.wait()
        self.play(point.animate.move_to(-position), arrows_1.animate.scale(2).rotate(PI),
                  arrows_2.animate.scale(2).rotate(PI))
        self.wait()
        self.add(arrow_1, arrow_2).play(grid.animating(run_time=3).apply_matrix(operator),
                                        arrow_1.animating(run_time=3).restore(),
                                        arrow_2.animating(run_time=3).restore(), FadeOut(arrows_1), FadeOut(arrows_2),
                                        point.animating(run_time=3, remover=True).scale(0, about_point=ORIGIN))
        self.remove(shadow_1, shadow_2).wait()

        self.remove(grid, col)
        ratio = 0.8
        lines_h = [Line(20 * ratio * (2 * UP + LEFT), 20 * ratio * (2 * DOWN + RIGHT), stroke_width=2 if i else 4,
                        color=TEAL_E if i else TEAL).shift(i * ratio * (2 * RIGHT + UP) / 2) for i in range(-20, 20)]
        lines_v = [Line(10 * ratio * (2 * RIGHT + UP), 10 * ratio * (2 * LEFT + DOWN), stroke_width=2 if i else 4,
                        color=YELLOW_E if i else YELLOW).shift(i * ratio * (2 * UP + LEFT)) for i in range(-20, 20)]
        grid = VGroup(*lines_h[:20], *lines_h[21:], *lines_v, lines_h[20]).save_state().apply_matrix(operator)
        self.add(grid, arrow_1, arrow_2, box, matrix_2, equation).play(grid.animate.restore(), run_time=3)
        self.wait()

        points = [Dot(i * ratio * (2 * RIGHT + UP) * 5 / 2, color=TEAL_E if i else TEAL) for i in range(-20, 20)]
        self.add(*points, box, matrix_2, equation).play(grid.animate.apply_matrix(operator),
                                                        *[TransformFromCopy(line, point) for line, point in
                                                          zip(lines_h, points)], run_time=3)
        self.wait()
        dot = Dot(ratio * (2 * RIGHT + UP) * 5 / 2, radius=0.12, color=PURPLE_A).save_state().scale(3).set_stroke(
            width=4).set_fill(opacity=0)
        self.add(dot, arrow_1, arrow_2).play(ShowCreation(dot))  # , rate_func = rush_into)
        self.play(dot.animate.restore())  # , rate_func = rush_from)
        self.wait()
        self.play(grid.animate.restore(),
                  Transform(arrow_1, Arrow(ORIGIN, ratio * RIGHT, buff=0, color=BLUE, stroke_width=6)),
                  Transform(arrow_2, Arrow(ORIGIN, ratio * UP, buff=0, color=GREEN, stroke_width=6)),
                  *[Transform(point, line, remover=True) for line, point in zip(lines_h, points)],
                  Transform(dot.save_state(),
                            Line(20 * ratio * (2 * UP + LEFT), 20 * ratio * (2 * DOWN + RIGHT), color=PURPLE_A,
                                 fill_opacity=1).shift(ratio * (2 * RIGHT + UP) / 2)), run_time=3)
        self.wait()

        function = MathTex(r"\begin{bmatrix}1\\0.5\end{bmatrix}+k\begin{bmatrix}-1\\2\end{bmatrix}",
                        tex_to_color_map={r"\begin{bmatrix}1\\0.5\end{bmatrix}": PURPLE,
                                          r"\begin{bmatrix}-1\\2\end{bmatrix}": TEAL}).shift(
            0.5 * DOWN + 4 * RIGHT).set_stroke(width=16, color=BLACK, background=True)
        self.play(Write(function))
        self.wait()
        result = MathTex(
            r"\begin{bmatrix}4&2\\2&1\end{bmatrix}\left(\begin{bmatrix}1\\0.5\end{bmatrix}+k\begin{bmatrix}-1\\2\end{bmatrix}\right)=\begin{bmatrix}4&2\\2&1\end{bmatrix}\begin{bmatrix}1\\0.5\end{bmatrix}",
            tex_to_color_map={r"\begin{bmatrix}1\\0.5\end{bmatrix}": PURPLE,
                              r"\begin{bmatrix}-1\\2\end{bmatrix}": TEAL}).scale(0.8).next_to(function, DOWN).shift(
            1.5 * LEFT).set_stroke(width=16, color=BLACK, background=True)
        for i in range(6):
            result[i].set_fill(color=color_map[i])
            result[i + 22].set_fill(color=color_map[i])
        self.play(Write(result))
        self.wait()
        self.play(grid.animating(run_time=3).apply_matrix(operator), arrow_1.animating(run_time=3).restore(),
                  arrow_2.animating(run_time=3).restore(), dot.animating(run_time=3).restore())
        self.wait()


#################################################################### 

class Video_11_1(Scene):
    CONFIG = {
        "camera_class": AACamera
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(100).set_orientation(Rotation(quadternion))
        # def camera_updater(mob, dt):
        #     mob.quadternion = quaternion_mult(quad(OUT, DEGREES*dt), mob.quadternion)
        #     mob.set_orientation(Rotation(mob.quadternion))

        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        nil = Line(2*np.array([1, 2, 2]), 2*np.array([-1, -2, -2]), color = TEAL, depth_test = True)
        ratio = 2
        grid_0 = VGroup(*[Line(4*IN, 4*OUT, color = GREY, depth_test = True).shift(ratio*((i+0.5)*RIGHT + (j+0.5)*UP)) for i in range(-2, 2) for j in range(-2, 2)])
        grid = VGroup(grid_0.copy(), grid_0.copy().rotate(PI/2, axis = UP), grid_0.copy().rotate(PI/2, axis = RIGHT), depth_test = True).save_state()
        self.add(axes, grid).wait()

        operator = np.array([[8/9, -2/9, -2/9], [-2/9, 5/9, -4/9], [-2/9, -4/9, 5/9]])
        self.play(grid.animate.apply_matrix(operator).set_color(YELLOW), run_time = 3)
        grid.anti_alias_width = 0
        copy_grid = grid.copy()
        self.add(copy_grid).wait()
        self.play(GrowFromCenter(nil), grid.animate.restore(), run_time = 3)
        self.wait()

        n_1, n_2 = np.array([2/3, -2/3, 1/3]), np.array([-2/3, -1/3, 2/3])
        plane = Polygon(5*n_1+5*n_2, 5*n_1-5*n_2, -5*n_1-5*n_2, -5*n_1+5*n_2, stroke_width = 0, fill_opacity = 0.2, fill_color = YELLOW_D, depth_test = True)
        copy_nil = nil.copy().set_stroke(color = TEAL_E, opacity = 0.2)
        self.add(copy_nil).play(copy_nil.animate.shift(0.02*unit(PI/3)), nil.save_state().animate.scale(0), grid.animating(remover = True).apply_matrix(operator).set_stroke(width = 0, opacity = 0), copy_grid.animating(remover = True).set_stroke(width = 0, opacity = 0), FadeIn(plane), run_time = 3)
        self.wait()

        nil.restore()
        nils = [nil.copy().shift(2*(i*n_1+j*n_2)).set_stroke(color = TEAL_E if i or j else TEAL, opacity = 0.2 if i or j else 1).save_state().apply_matrix(operator) for i in range(-2, 3) for j in range(-2, 3)]
        planes = VGroup(*[plane.copy().shift(i*np.array([1, 2, 2])*2/3).save_state() for i in (-2, -1, 1, 2)])
        planes.set_opacity(0).apply_matrix(operator)
        self.remove(nil).add(*planes, *nils).play(plane.animate.set_fill(opacity = 0.5), *[plane.animate.restore() for plane in planes], *[line.animate.restore() for line in nils], run_time = 3)
        self.wait()

class Video_11_2(Scene):
    CONFIG = {
        "camera_class": AACamera
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI+PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(100).set_orientation(Rotation(quadternion))
        eye = np.dot(camera.get_orientation().as_matrix(), camera.get_focal_distance()*OUT) + camera.get_center()

        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        ratio = 2
        grid_0 = VGroup(*[Line(4*IN, 4*OUT, color = GREY, depth_test = True).shift(ratio*((i+0.5)*RIGHT + (j+0.5)*UP)) for i in range(-2, 2) for j in range(-2, 2)])
        grid = VGroup(grid_0.copy(), grid_0.copy().rotate(PI/2, axis = UP), grid_0.copy().rotate(PI/2, axis = RIGHT), depth_test = True).save_state()
        self.add(axes, grid).wait()

        operator = np.array([[1/9, 2/9, 2/9], [2/9, 4/9, 4/9], [2/9, 4/9, 4/9]])
        n_1, n_2 = np.array([2/3, -2/3, 1/3]), np.array([-2/3, -1/3, 2/3])
        nil = Polygon(5*n_1+5*n_2, 5*n_1-5*n_2, -5*n_1-5*n_2, -5*n_1+5*n_2, stroke_width = 0, fill_opacity = 0.5, fill_color = TEAL, depth_test = True, anti_alias_width = 0).insert_n_curves(12)
        copy_nil = nil.copy().set_fill(color = TEAL_E, opacity = 0.2).scale(1.05, about_point = eye)
        self.play(grid.animate.apply_matrix(operator).set_color(YELLOW), run_time = 3)
        copy_grid = Line(17/9*np.array([1, 2, 2]), 17/9*np.array([-1, -2, -2]), color = YELLOW, depth_test = True, anti_alias_width = 0)
        self.add(copy_grid).wait()
        self.play(GrowFromCenter(nil), GrowFromCenter(copy_nil), grid.animate.restore(), run_time = 3)
        self.wait()

        self.play(nil.save_state().animate.scale(0), grid.animating(remover = True).apply_matrix(operator).set_color(YELLOW), run_time = 3)
        self.remove(grid).wait()

        nils = [copy_nil.copy().shift(i*np.array([1, 2, 2])*2/3).set_opacity(1/3).save_state().set_opacity(0).apply_matrix(operator) for i in (-2, -1, 1, 2)]
        grids = [copy_grid.copy().shift(2*(i*n_1+j*n_2)).set_stroke(color = YELLOW, opacity = 1/3 if i or j else 0).save_state().apply_matrix(operator) for i in range(-2, 3) for j in range(-2, 3) if i or j]
        self.add(*grids, *nils).play(nil.animate.restore(), *[line.animate.restore() for line in grids], *[plane.animate.restore() for plane in nils], run_time = 3)
        self.wait()

def perspective(camera: CameraFrame, return_ratio: bool = False):
    position = camera.get_center()
    distance = camera.get_focal_distance()
    orientation = camera.get_orientation().as_matrix()
    def util_2(point: np.ndarray):
        raw = np.dot(orientation.T, point - position) - distance*OUT
        if math.isclose(raw[2], 0):
            ratio = 0
            point = np.array([10000*raw[0], 10000*raw[1], 0])
            return 
        else:
            ratio = -distance/raw[2]
            point = raw*ratio + distance*OUT
        if return_ratio:
            return point, ratio
        else:
            return point
    return util_2

class Video_11_3(Scene):
    CONFIG = {
        "camera_class": AACamera
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI+PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(100).set_orientation(Rotation(quadternion))
        eye = np.dot(camera.get_orientation().as_matrix(), camera.get_focal_distance()*OUT) + camera.get_center()
        
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        
        operator = np.array([[1/9, 2/9, 2/9], [2/9, 4/9, 4/9], [2/9, 4/9, 4/9]])
        n_1, n_2 = np.array([2/3, -2/3, 1/3]), np.array([-2/3, -1/3, 2/3])
        nil = Polygon(5*n_1+5*n_2, 5*n_1-5*n_2, -5*n_1-5*n_2, -5*n_1+5*n_2, stroke_width = 0, fill_opacity = 0.5, fill_color = TEAL, depth_test = True, anti_alias_width = 0).insert_n_curves(12)
        copy_nil = nil.copy().set_fill(color = TEAL_E, opacity = 0.2).scale(1.05, about_point = eye)
        copy_grid = Line(17/9*np.array([1, 2, 2]), 17/9*np.array([-1, -2, -2]), color = YELLOW, depth_test = True, anti_alias_width = 0)

        nils = [copy_nil.copy().shift(i*np.array([1, 2, 2])*2/3).set_opacity(1/3).save_state() for i in (-2, -1, 1, 2)]
        grids = [copy_grid.copy().shift(2*(i*n_1+j*n_2)).set_stroke(color = YELLOW, opacity = 1/3 if i or j else 0).save_state() for i in range(-2, 3) for j in range(-2, 3) if i or j]
        self.add(axes, copy_grid, nil, copy_nil, *grids, *nils).wait()
        self.play(*[FadeOut(mob) for mob in nils + grids])
        self.wait()

        offset = 4*unit(PI/3)
        box = BlackBox().fix_in_frame().shift(2.5*RIGHT)
        self.play(FadeIn(box, 3*LEFT), *[mob.animate.scale(0.5, about_point = ORIGIN).shift(offset) for mob in [axes, copy_grid, nil]], Transform(copy_nil, nil.copy().scale(0.5).shift(offset).scale(1.05, about_point = eye)))
        self.wait()
        pers = perspective(camera)
        arrow_1 = Arrow(ORIGIN, n_1, buff = 0, color = BLUE, ).shift(offset)
        arrow_2 = Arrow(ORIGIN, n_2 - n_1, buff = 0, color = GREEN, ).shift(offset)
        arrow_3 = Arrow(ORIGIN, 2*n_2 - n_1, buff = 0, color = TEAL).shift(offset)
        label_1 = MathTex(r"\vec{u}", color = BLUE).next_to(pers(arrow_1.get_end()), UP).fix_in_frame().set_stroke(width = 8, color = BLACK, background = True)
        label_2 = MathTex(r"\vec{v}", color = GREEN).next_to(pers(arrow_2.get_end()), RIGHT).fix_in_frame().set_stroke(width = 8, color = BLACK, background = True)
        label_3 = MathTex(r"\vec{u}+2\vec{v}", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": GREEN, r"2": ORANGE}).next_to(pers(arrow_3.get_end()), UR).fix_in_frame().set_stroke(width = 8, color = BLACK, background = True)
        input_1 = MathTex(r"\vec{u}", color = BLUE).shift(UP + 0.5*LEFT).fix_in_frame()
        input_2 = MathTex(r"\vec{v}", color = GREEN).shift(0.5*LEFT).fix_in_frame()
        input_3 = MathTex(r"\vec{u}+c\vec{v}", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": GREEN, r"c": ORANGE}).shift(DOWN + 0.5*LEFT).fix_in_frame()
        output_1 = MathTex(r"\vec{0}", color = interpolate_color(BLUE, GREY, 0.5)).shift(UP + 5.5*RIGHT).fix_in_frame()
        output_2 = MathTex(r"\vec{0}", color = interpolate_color(GREEN, GREY, 0.5)).shift(5.5*RIGHT).fix_in_frame()
        output_3 = MathTex(r"\vec{0}+c\vec{0}=\vec{0}", tex_to_color_map = {r"c": ORANGE}).shift(DOWN + 5.5*RIGHT).fix_in_frame()
        output_3[0:2].set_color(interpolate_color(BLUE, GREY, 0.5))
        output_3[4:6].set_color(interpolate_color(GREEN, GREY, 0.5))
        output_3[7:].set_color(interpolate_color(TEAL, GREY, 0.5))
        self.play(GrowArrow(arrow_1), GrowArrow(arrow_2), Write(label_1), Write(label_2), Write(input_1), Write(input_2))
        self.wait()
        copy_1, copy_2, copy_3 = input_1.copy(), input_2.copy(), input_3.copy()
        self.add(copy_1, copy_2, box).play(copy_1.animate.scale(0, about_point = 2*RIGHT), copy_2.animate.scale(0, about_point = 2*RIGHT), remover = True, rate_func = rush_into)
        self.add(output_1, output_2, box).play(GrowFromPoint(output_1, 3*RIGHT), GrowFromPoint(output_2, 3*RIGHT), rate_func = rush_from)
        self.wait()
        self.play(GrowArrow(arrow_3), Write(label_3), Write(input_3))
        self.wait()
        self.add(copy_3, box).play(copy_3.animate.scale(0, about_point = 2*RIGHT), remover = True, rate_func = rush_into)
        self.add(output_3, box).play(GrowFromPoint(output_3, 3*RIGHT), rate_func = rush_from)
        self.wait()
        
class Video_11_4(Scene):
    CONFIG = {
        "camera_class": AACamera
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI+PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(100).set_orientation(Rotation(quadternion))
        eye = np.dot(camera.get_orientation().as_matrix(), camera.get_focal_distance()*OUT) + camera.get_center()
        
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        
        operator = np.array([[1/9, 2/9, 2/9], [2/9, 4/9, 4/9], [2/9, 4/9, 4/9]])
        n_1, n_2 = np.array([2/3, -2/3, 1/3]), np.array([-2/3, -1/3, 2/3])
        nil = Polygon(5*n_1+5*n_2, 5*n_1-5*n_2, -5*n_1-5*n_2, -5*n_1+5*n_2, stroke_width = 0, fill_opacity = 0.5, fill_color = TEAL, depth_test = True, anti_alias_width = 0).insert_n_curves(12)
        copy_nil = nil.copy().set_fill(color = TEAL_E, opacity = 0.2).scale(1.05, about_point = eye)
        copy_grid = Line(17/9*np.array([1, 2, 2]), 17/9*np.array([-1, -2, -2]), color = YELLOW, depth_test = True, anti_alias_width = 0)

        nils = [copy_nil.copy().shift(i*np.array([1, 2, 2])*2/3).set_opacity(1/3).save_state() for i in (-2, -1, 1, 2)]
        grids = [copy_grid.copy().shift(2*(i*n_1+j*n_2)).set_stroke(color = YELLOW, opacity = 1/3 if i or j else 0).save_state() for i in range(-2, 3) for j in range(-2, 3) if i or j]
        self.add(axes, copy_grid, nil, copy_nil, *grids, *nils).wait()
        self.play(*[mob.save_state().animate.apply_matrix(operator) for mob in nils], *[mob.save_state().animate.apply_matrix(operator).set_opacity(0) for mob in grids], run_time = 3)
        self.wait()

        huaji = TexturedSurface(ParametricSurface(u_range = (-5, 5), v_range = (-5, 5), uv_func = lambda u, v: u*n_1+v*n_2), "huaji.png")
        huajis = [huaji.copy().shift(i*np.array([1, 2, 2])*2/3).set_opacity(1/3).save_state() for i in (-2, -1, 0, 1, 2)]
        self.play(*[mob.apply_matrix(operator).animate.restore() for mob in huajis], *[mob.animate.restore() for mob in grids], run_time = 3)
        self.wait()
        self.play(*[mob.animate.apply_matrix(operator) for mob in huajis], *[mob.animate.apply_matrix(operator).set_opacity(0) for mob in grids], run_time = 3)
        self.wait()
        self.play(*[mob.apply_matrix(operator).animate.restore() for mob in huajis], run_time = 3)
        self.wait()
        self.play(*[mob.animate.apply_matrix(operator) for mob in huajis], run_time = 3)
        self.wait()
        self.play(*[mob.apply_matrix(operator).animate.restore() for mob in nils], *[mob.animate.restore() for mob in grids], run_time = 3)
        self.wait()
        self.play(*[mob.animate.apply_matrix(operator) for mob in nils], *[mob.animate.apply_matrix(operator).set_opacity(0) for mob in grids], run_time = 3)
        self.wait()

# Write a scene that load huaji.png and show it on the screen
# Then create a two-dimensional grid with axes, one point.
class Video_11_5(Scene):
    def construct(self):
        huaji = ImageMobject("huaji.png").scale(2)
        self.add(huaji)
        self.wait(2)
        # Create a two-dimensional grid with axes, and tick marks
        axes = Axes(x_range = (-5, 5), y_range = (-5, 5), x_length = 10, y_length = 10, axis_config = {"include_tip": False, "include_ticks": True})
        self.play(
            LaggedStart(Create(axes)),
            run_time = 3
        )
        self.wait(2)

#################################################################### 

class Patch12_1(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        ratio = 0.8
        lines_h = [Line(20*ratio*(2*UP+LEFT), 20*ratio*(2*DOWN+RIGHT), stroke_width = 4 if i else 8, color = TEAL_E if i else TEAL).shift(i*ratio*(2*RIGHT + UP)) for i in range(-20, 20)]
        lines_v = [Line(10*ratio*(2*RIGHT+UP), 10*ratio*(2*LEFT+DOWN), stroke_width = 4 if i else 8, color = YELLOW_E if i else YELLOW).shift(i*ratio*(2*UP + LEFT)) for i in range(-20, 20)]
        grid = VGroup(*lines_h[:20], *lines_h[21:], *lines_v, lines_h[20]).save_state()
        self.add(grid).play(grid.animate.restore(), run_time = 3)
        
class Patch12_2(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (12.0, 12.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(100).set_orientation(Rotation(quadternion))

        n_1, n_2 = np.array([2/3, -2/3, 1/3]), np.array([-2/3, -1/3, 2/3])
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        nil = Line(1.5*np.array([1, 2, 2]), 1.5*np.array([-1, -2, -2]), color = TEAL, stroke_width = 12, depth_test = True)
        nils = [nil.copy().shift(3*(i*n_1+j*n_2)).set_stroke(color = TEAL_E if i or j else TEAL, opacity = 0.2 if i or j else 1) for i in range(-1, 2) for j in range(-1, 2)]
        plane = Polygon(4*n_1+4*n_2, 4*n_1-4*n_2, -4*n_1-4*n_2, -4*n_1+4*n_2, stroke_width = 0, fill_opacity = 0.2, fill_color = YELLOW_D, depth_test = True)
        planes = VGroup(*[plane.copy().shift(i*np.array([1, 2, 2])).save_state() for i in (-1, 1)])
        plane.set_fill(color = YELLOW, opacity = 0.5)
        self.add(axes, plane, *planes, *nils)
        
class Patch12_3(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (12.0, 12.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI+PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(100).set_orientation(Rotation(quadternion))

        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        n_1, n_2 = np.array([2/3, -2/3, 1/3]), np.array([-2/3, -1/3, 2/3])
        nil = Polygon(4*n_1+4*n_2, 4*n_1-4*n_2, -4*n_1-4*n_2, -4*n_1+4*n_2, stroke_width = 0, fill_opacity = 0.5, fill_color = TEAL, depth_test = True, anti_alias_width = 0).insert_n_curves(12)
        copy_nil = nil.copy().set_fill(color = TEAL_E, opacity = 0.1)
        copy_grid = Line(17/9*np.array([1, 2, 2]), 17/9*np.array([-1, -2, -2]), stroke_width = 12, color = YELLOW, depth_test = True, anti_alias_width = 0)
        nils = [copy_nil.copy().shift(i*np.array([1, 2, 2])).set_opacity(1/3) for i in (-1, 1)]
        grids = [copy_grid.copy().shift(3*(i*n_1+j*n_2)).set_stroke(color = YELLOW, opacity = 1/3) for i in range(-1, 2) for j in range(-1, 2) if i or j]
        self.add(*grids, *nils, nil, copy_grid, axes)

class Video_12(Scene):
    def construct(self):
        space_1, space_2, space_3 = ImageMobject("Patch12_1.png", height = 4).shift(4*LEFT), ImageMobject("Patch12_2.png", height = 4), ImageMobject("Patch12_3.png", height = 4).shift(4*RIGHT)
        col_1, col_2, col_3 = MathTexText(r"列空间：1维", color = YELLOW).shift(3.25*UP + 4*LEFT), MathTexText(r"列空间：2维", color = YELLOW).shift(3.25*UP), MathTexText(r"列空间：1维", color = YELLOW).shift(3.25*UP + 4*RIGHT)
        nil_1, nil_2, nil_3 = MathTexText(r"零空间：1维", color = TEAL).shift(2.5*UP + 4*LEFT), MathTexText(r"零空间：1维", color = TEAL).shift(2.5*UP), MathTexText(r"零空间：2维", color = TEAL).shift(2.5*UP + 4*RIGHT)
        sum_1, sum_2, sum_3 = MathTex(r"2=1+1").shift(2.5*DOWN + 4*LEFT), MathTex(r"3=2+1").shift(2.5*DOWN), MathTex(r"3=1+2").shift(2.5*DOWN + 4*RIGHT)
        formula = MathTexText(r"总维数=矩阵的秩（列空间维数）+零空间维数", tex_to_color_map = {r"总维数": BLUE, r"矩阵的秩（列空间维数）": YELLOW, r"零空间维数": TEAL}).shift(2.5*DOWN)
        title = Title("线性代数基本定理")
        titleline = TitleLine()
        for mob in [sum_1, sum_2, sum_3]:
            mob[0].set_color(BLUE)
            mob[2].set_color(YELLOW)
            mob[4].set_color(TEAL)
        self.add(space_1, space_2, space_3).wait()
        self.play(Write(col_1), Write(col_2), Write(col_3))
        self.wait()
        self.play(Write(nil_1), Write(nil_2), Write(nil_3))
        self.wait()
        self.play(Write(sum_1), Write(sum_2), Write(sum_3))
        self.wait()
        self.play(*[mob.animate.shift(UP) for mob in [space_1, space_2, space_3, sum_1, sum_2, sum_3]], *[FadeOut(mob, UP) for mob in [col_1, col_2, col_3, nil_1, nil_2, nil_3]], FadeIn(formula, UP))
        self.wait()
        self.play(Write(title), GrowFromCenter(titleline))
        self.wait()

class Video_13(Scene):
    CONFIG = {
        "camera_class": AACamera
    }
    def cheese(self, *mobs):
        orientation = self.camera.frame.get_orientation().as_matrix()
        util = lambda t: np.dot(orientation, t)
        for mob in mobs:
            position = mob.get_center()
            # mob.restore().apply_function(util, about_point = position)
            # mob.move_to(position)
            mob.apply_function(util, about_point = position)
        return self
    
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(100).set_orientation(Rotation(quadternion))
        # def camera_updater(mob, dt):
        #     mob.quadternion = quaternion_mult(quad(OUT, DEGREES*dt), mob.quadternion)
        #     mob.set_orientation(Rotation(mob.quadternion))

        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        nil = Line(2*np.array([1, 2, 2]), 2*np.array([-1, -2, -2]), color = TEAL, depth_test = True)
        ratio = 2
        grid_0 = VGroup(*[Line(4*IN, 4*OUT, color = GREY, depth_test = True).shift(ratio*((i+0.5)*RIGHT + (j+0.5)*UP)) for i in range(-2, 2) for j in range(-2, 2)])
        grid = VGroup(grid_0.copy(), grid_0.copy().rotate(PI/2, axis = UP), grid_0.copy().rotate(PI/2, axis = RIGHT), depth_test = True).save_state()
        grid.anti_alias_width = 0
        self.add(axes, grid).wait()

        operator = np.array([[8/9, -2/9, -2/9], [-2/9, 5/9, -4/9], [-2/9, -4/9, 5/9]])
        n_1, n_2 = np.array([2/3, -2/3, 1/3]), np.array([-2/3, -1/3, 2/3])
        plane = Polygon(5*n_1+5*n_2, 5*n_1-5*n_2, -5*n_1-5*n_2, -5*n_1+5*n_2, stroke_width = 0, fill_opacity = 0.2, fill_color = YELLOW_D, depth_test = True)
        self.play(grid.animating(remover = True).apply_matrix(operator).set_stroke(width = 0, opacity = 0), FadeIn(plane), run_time = 3)
        self.wait()

        offset = -4*unit(PI/3)
        texts = r"\begin{bmatrix}8&-2&-2\\-2&5&-4\\2&-4&5\end{bmatrix}", r"\begin{bmatrix}x\\y\\z\end{bmatrix}", r"\begin{bmatrix}4\\-1\\-1\end{bmatrix}"
        matrix = MathTex(texts[0]+texts[1]+r"="+texts[2], isolate = "=", tex_to_color_map = {texts[0]: ORANGE, texts[1]: GREEN, texts[2]: YELLOW}).scale(0.8).fix_in_frame().set_stroke(width = 8, color = BLACK, background = True).shift(3*RIGHT + 2*UP)
        self.add(nil, plane).play(*[mob.animate.scale(0.5, about_point = ORIGIN).shift(offset) for mob in [axes, plane]], GrowFromPoint(nil.scale(0.5).shift(offset), ORIGIN), run_time = 3)
        self.wait()

        dot = Dot(np.array([4, -1, -1])*1/3 + offset, color = YELLOW)
        self.cheese(dot).play(FadeIn(matrix, DOWN), ShowCreation(dot))
        self.wait()
        texts = r"\begin{bmatrix}x\\y\\z\end{bmatrix}", r"\begin{bmatrix}1\\1\\1\end{bmatrix}", r"\begin{bmatrix}1\\2\\2\end{bmatrix}"
        solution = MathTex(texts[0]+r"="+texts[1]+r"+{t}"+texts[2], tex_to_color_map = {texts[0]: GREEN, texts[1]: YELLOW, texts[2]: TEAL, r"{t}": ORANGE}).scale(0.8).fix_in_frame().set_stroke(width = 8, color = BLACK, background = True).shift(3*RIGHT + 0.5*DOWN)
        solution_1, solution_2 = solution[:15], solution[15:]
        label_1, label_2 = MathTex(r"\vec{x}_p", color = YELLOW).next_to(solution[7:16], DOWN).fix_in_frame(), MathTex(r"\vec{x}_n", color = TEAL).next_to(solution_2[2:], DOWN).fix_in_frame()
        text = MathTex(r"t=0.00", color = ORANGE).fix_in_frame().shift(4*LEFT + 3*UP)
        copy_nil = nil.copy().shift(np.array([4, -1, -1])*1/3).set_stroke(opacity = 0.5)
        self.play(Write(solution_1))
        self.wait()
        self.play(Write(label_1))
        self.wait()
        self.add(copy_nil, plane, dot).play(GrowFromCenter(copy_nil), FadeIn(solution_2, 0.5*LEFT), FadeIn(text, 0.5*DOWN))
        self.wait()
        self.play(Write(label_2))
        self.wait()

        arrow = Arrow(color = TEAL, depth_test = True)
        alpha = ValueTracker(0.0)
        def arrow_updater(mob: Arrow):
            value = alpha.get_value()
            mob.become(Arrow(ORIGIN, value*np.array([1, 2, 2]), buff = 0, color = TEAL).shift(offset + np.array([4, -1, -1])*1/3))
        def dot_updater(mob: Arrow):
            value = alpha.get_value()
            mob.move_to(offset + np.array([4, -1, -1])*1/3 + value*np.array([1, 2, 2]))
        def text_updater(mob: Arrow):
            value = alpha.get_value()
            mob.become(MathTex(f"t={value: .2f}", color = ORANGE).fix_in_frame().shift(4*LEFT + 3*UP))
        arrow.add_updater(arrow_updater)
        dot.add_updater(dot_updater)
        text.add_updater(text_updater)
        self.add(arrow, dot).play(alpha.add_updater(arrow_updater).animate.set_value(1.0), run_time = 2)
        self.wait()
        self.play(alpha.add_updater(arrow_updater).animate.set_value(-1.0), run_time = 2)
        self.wait()
        self.play(alpha.add_updater(arrow_updater).animate.set_value(0.0), run_time = 2)
        self.wait()

#################################################################### 

class Template(Scene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
