from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        ratio = 1
        e1, e2 = np.array([2, 0, 0]), np.array([1, 3, 0]), 
        dots = VGroup(*[Dot(i*ratio*RIGHT + j*ratio*UP, color = BLUE) for i in range(-7, 8) for j in range(-4, 5)])
        dots_base = dots.copy().set_color(GREY)
        dots_target = VGroup(*[Dot(i*ratio*e1 + j*ratio*e2, color = BLUE) for i in range(-7, 8) for j in range(-4, 5)])
        ratio = 0.5
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-20, 21)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v)
        self.add(base, grid, dots_base, dots).wait()
        self.play(grid.animate.apply_matrix(np.array([[2, 1], [0, 3]])), Transform(dots, dots_target), run_time = 3)
        self.wait()

        dots_copy = [dots_base.copy() for _ in range(20)]
        self.add(*dots_copy, dots).play(*[Transform(dots_copy[i], dots_target, run_time = 2, delay = i, rate_func = lambda t: (3**t-1)/2) for i in range(20)])
        self.wait()

class Patch1_1(FrameScene):
    def construct(self):
        matrix = MTex(r"A = \begin{bmatrix}2&1\\0&3\end{bmatrix}", color = ORANGE, tex_to_color_map = {r"=": WHITE}).shift(2.5*UP + 5*LEFT).set_stroke(**stroke_dic)
        eigen = MTex(r"A\vec{x}=\lambda\vec{x}", tex_to_color_map = {r"A": ORANGE, r"\vec{x}": BLUE, r"\lambda": YELLOW}).next_to(matrix, DOWN).set_stroke(**stroke_dic)
        self.wait()
        self.play(Write(matrix))
        self.wait()
        self.play(Write(eigen))
        self.wait()

class Patch1_2(FrameScene):
    def construct(self):
        line_1 = Line(LEFT_SIDE, RIGHT_SIDE, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5)
        line_2 = Line(5*UR, 5*DL, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5)
        self.wait()
        self.play(ShowCreation(line_1, start = 0.5), ShowCreation(line_2, start = 0.5), run_time = 2)
        self.wait()

class Patch1_3(FrameScene):
    def construct(self):
        line_1 = Line(5*DR, 5*UL, stroke_width = 12, color = RED, stroke_opacity = 0.8)
        line_2 = Line(5*(UR+RIGHT), 5*(DL+LEFT), stroke_width = 12, color = RED, stroke_opacity = 0.8)
        self.wait()
        self.play(ShowCreation(line_1, start = 0.5), ShowCreation(line_2, start = 0.5), run_time = 2)
        self.wait()
        self.play(FadeOut(line_1), FadeOut(line_2))
        self.wait()

class Video_3(FrameScene):
    def construct(self):
        ratio = 0.5
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-20, 21)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v)
        matrix = MTex(r"A = \begin{bmatrix}2&1\\0&3\end{bmatrix}", color = ORANGE, tex_to_color_map = {r"=": WHITE}).shift(2.5*UP + 5*LEFT).set_stroke(**stroke_dic)
        eigen = MTex(r"A\vec{x}=\lambda\vec{x}", tex_to_color_map = {r"A": ORANGE, r"\vec{x}": BLUE, r"\lambda": YELLOW}).next_to(matrix, DOWN).set_stroke(**stroke_dic)
        line_1 = Line(LEFT_SIDE, RIGHT_SIDE, stroke_width = 12, color = YELLOW, stroke_opacity = 0.2)
        line_2 = Line(5*UR, 5*DL, stroke_width = 12, color = YELLOW, stroke_opacity = 0.2)
        vector_1, vector_2 = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UR, color = GREEN, buff = 0, stroke_width = 8)
        GREEN_E = interpolate_color(GREEN, BLACK, 0.5)
        TEAL_E = interpolate_color(TEAL, BLACK, 0.5)
        YELLOW_E = interpolate_color(YELLOW, BLACK, 0.5)
        back_1, back_2 = Arrow(ORIGIN, RIGHT, color = BLUE_E, buff = 0, stroke_width = 8), Arrow(ORIGIN, UR, color = GREEN_E, buff = 0, stroke_width = 8)
        target_1, target_2 = Arrow(ORIGIN, 2*RIGHT, color = BLUE_E, buff = 0, stroke_width = 8), Arrow(ORIGIN, 3*UR, color = GREEN_E, buff = 0, stroke_width = 8)
        
        operator = np.array([[2, 1], [0, 3]])
        self.add(base, grid, matrix, eigen).wait()
        self.play(grid.save_state().animate.apply_matrix(operator), run_time = 2)
        self.wait()

        self.play(FadeOut(grid), run_time = 0.5, rate_func = rush_into)
        self.add(grid, matrix, eigen).play(FadeIn(grid.restore()), run_time = 0.5, rate_func = rush_from)
        self.wait()

        self.bring_to_back(line_1).play(ShowCreation(line_1, start = 0.5, run_time = 2), GrowArrow(vector_1))
        self.wait()
        self.bring_to_back(line_2).play(ShowCreation(line_2, start = 0.5, run_time = 2), GrowArrow(vector_2))
        self.wait()
        self.add(back_1, back_2, vector_1, vector_2
                 ).play(grid.animate.apply_matrix(np.array([[2, 1], [0, 3]])), Transform(back_1.save_state(), target_1), Transform(back_2.save_state(), target_2), run_time = 2)
        self.wait()

        tex_1 = MTex(r"A\begin{bmatrix}1\\0\end{bmatrix}={2}\begin{bmatrix}1\\0\end{bmatrix}", tex_to_color_map = {r"A": ORANGE, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE, r"{2}": YELLOW}).next_to(target_1, DOWN).set_stroke(**stroke_dic)
        tex_2 = MTex(r"A\begin{bmatrix}1\\1\end{bmatrix}={3}\begin{bmatrix}1\\1\end{bmatrix}", tex_to_color_map = {r"A": ORANGE, r"\begin{bmatrix}1\\1\end{bmatrix}": GREEN, r"{3}": YELLOW}).next_to(target_2.get_center(), UL).set_stroke(**stroke_dic)
        self.play(Write(tex_1))
        self.wait()
        self.play(Write(tex_2))
        self.wait()

        self.play(IndicateAround(tex_1.get_part_by_tex(r"{2}")), IndicateAround(tex_2.get_part_by_tex(r"{3}")))
        self.wait()
        
        restores = [grid, back_1, back_2]
        self.play(*[FadeOut(mob) for mob in restores], run_time = 0.5, rate_func = rush_into)
        self.add(grid, matrix, eigen, back_1, back_2, vector_1, vector_2, matrix, eigen, tex_1, tex_2).play(*[FadeIn(mob.restore()) for mob in restores], run_time = 0.5, rate_func = rush_from)
        self.wait()

        vector = Arrow(ORIGIN, UR+RIGHT, color = TEAL, buff = 0, stroke_width = 8)
        back = Arrow(ORIGIN, UR+RIGHT, color = TEAL_E, buff = 0, stroke_width = 8).save_state()
        target = Arrow(ORIGIN, 2*RIGHT + 3*UR, color = TEAL_E, buff = 0, stroke_width = 8)
        self.play(ShowCreation(vector))
        self.wait()
        self.add(back, vector).play(grid.animate.apply_matrix(operator).set_opacity(0), 
                                    back_1.animate.become(target_1).set_opacity(0), back_2.animate.become(target_2).set_opacity(0), back.animate.become(target).set_opacity(0), run_time = 2)
        self.wait()
        restores = [grid, back_1, back_2, back]
        self.add(grid, matrix, eigen, back_1, back_2, back, vector_1, vector_2, vector, matrix, eigen, tex_1, tex_2).play(*[FadeIn(mob.restore()) for mob in restores], run_time = 0.5, rate_func = rush_from)
        self.wait()

        linea_1, linea_2 = Line(UR+RIGHT, UR, color = YELLOW), Line(UR+RIGHT, RIGHT, color = YELLOW)
        lineb_1, lineb_2 = Line(UR, UR+RIGHT, color = YELLOW_E).apply_matrix(operator), Line(RIGHT, UR+RIGHT, color = YELLOW_E).apply_matrix(operator)
        self.add(linea_1, linea_2, vector_1, vector_2, vector, tex_1, tex_2).play(ShowCreation(linea_1), ShowCreation(linea_2))
        self.wait()
        self.play(grid.animate.apply_matrix(operator), Transform(back_1, target_1), Transform(back_2, target_2), run_time = 2)
        self.wait()
        self.add(lineb_1, lineb_2, back_1, back_2, linea_1, linea_2, vector_1, vector_2, vector, matrix, eigen, tex_1, tex_2).play(ShowCreation(lineb_1), ShowCreation(lineb_2))
        self.wait()
        self.add(back_1, back_2, back.become(target), linea_1, linea_2, vector_1, vector_2, vector, matrix, eigen, tex_1, tex_2).play(GrowArrow(back))
        self.wait()

        end = MTex(r"\begin{bmatrix}5\\3\end{bmatrix}", color = TEAL).next_to(back.get_corner(UR), DOWN).set_stroke(**stroke_dic)
        self.play(Write(end))
        self.wait()
        calculate = MTex(r"\begin{bmatrix}2&1\\0&3\end{bmatrix}\begin{bmatrix}2\\1\end{bmatrix}=\begin{bmatrix}5\\3\end{bmatrix}", color = TEAL, tex_to_color_map = {r"\begin{bmatrix}2&1\\0&3\end{bmatrix}": ORANGE, r"=": WHITE, r"\begin{bmatrix}5\\3\end{bmatrix}": TEAL}).next_to(3.5*LEFT, DOWN).set_stroke(**stroke_dic)
        self.play(Write(calculate))
        self.wait()

        self.play(*[FadeOut(mob) for mob in restores + [vector, linea_1, linea_2, lineb_1, lineb_2, end, calculate]])
        back_1.restore().set_stroke(width = 5), back_2.restore().set_stroke(width = 5)
        grid_arrows = VGroup(*[back_1.copy().shift(i*RIGHT+j*UP) for i in range(-8, 9) for j in range(-5, 5)], *[back_2.copy().shift(i*RIGHT+j*UP) for i in range(-8, 9) for j in range(-5, 5)])
        grid_targets = VGroup(*[target_1.copy().shift(i*2*RIGHT+j*(3*UP+RIGHT)) for i in range(-8, 9) for j in range(-5, 5)], *[target_2.copy().shift(i*2*RIGHT+j*(3*UP+RIGHT)) for i in range(-8, 9) for j in range(-5, 5)])
        grid_backs = VGroup(*[line_1.copy().shift(i*UP) for i in range(-4, 5)], *[line_2.copy().shift(i*RIGHT) for i in range(-7, 8)])
        self.bring_to_back(grid_backs).add(grid_arrows, vector_1, vector_2, matrix, eigen, tex_1, tex_2).play(FadeIn(grid_arrows), FadeIn(grid_backs))
        self.wait()
        self.play(Transform(grid_arrows, grid_targets), run_time = 2)
        self.wait()

"""
class Video_4(FrameScene):
    def construct(self):
        title = Title("特征值和特征向量")
        titleline = TitleLine()
        matrix = MTex(r"A=\begin{bmatrix}2&1\\0&3\end{bmatrix}", color = ORANGE, tex_to_color_map = {r"=": WHITE}).shift(5*LEFT)
        eigen_1 = MTex(r"\begin{cases}\vec{u}_1=\begin{bmatrix}1\\0\end{bmatrix}\\\lambda_1=2\end{cases}", 
                       tex_to_color_map = {(r"\vec{u}_1", r"\begin{bmatrix}1\\0\end{bmatrix}"): BLUE, (r"\lambda_1", r"2"): YELLOW}).scale(0.8).shift(2.3*LEFT)
        eigen_1[8].match_x(eigen_1[15])
        calc_1 = MTex(r":A\vec{u}_1=2\vec{u}_1;", tex_to_color_map = {r"\vec{u}_1": BLUE, r"2": YELLOW, r"A": ORANGE}).shift(0.2*RIGHT)
        eigen_2 = MTex(r"\begin{cases}\vec{u}_2=\begin{bmatrix}1\\1\end{bmatrix}\\\lambda_2=3\end{cases}", 
                       tex_to_color_map = {(r"\vec{u}_2", r"\begin{bmatrix}1\\1\end{bmatrix}"): GREEN, (r"\lambda_2", r"3"): YELLOW}).scale(0.8).shift(2.7*RIGHT)
        eigen_2[8].match_x(eigen_2[15])
        calc_2 = MTex(r":A\vec{u}_2=3\vec{u}_2;", tex_to_color_map = {r"\vec{u}_2": GREEN, r"3": YELLOW, r"A": ORANGE}).shift(5.2*RIGHT)
        calc_2.remove(calc_2[-1])
        eigen = VGroup(matrix, eigen_1, calc_1, eigen_2, calc_2).shift(2*UP).scale(0.9)
        line = titleline.copy().set_color(GREY).shift(2*DOWN)
        self.add(title, titleline, eigen, line).wait()

        texs = r"\begin{bmatrix}2\\1\end{bmatrix}", r"=", r"{1}\begin{bmatrix}1\\0\end{bmatrix}", r"+", r"{1}\begin{bmatrix}1\\1\end{bmatrix}"
        calc_ul = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\begin{bmatrix}2\\1\end{bmatrix}": TEAL, r"{1}": PURPLE_B, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE, r"\begin{bmatrix}1\\1\end{bmatrix}": GREEN}).scale(0.8)
        parts_ul = [calc_ul.get_part_by_tex(text) for text in texs]
        texs = r"\begin{bmatrix}5\\2\end{bmatrix}", r"=", r"{2}\begin{bmatrix}1\\0\end{bmatrix}", r"+", r"{3}\begin{bmatrix}1\\1\end{bmatrix}"
        calc_dl = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\begin{bmatrix}5\\2\end{bmatrix}": TEAL, (r"{2}", r"{3}"): YELLOW, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE, r"\begin{bmatrix}1\\1\end{bmatrix}": GREEN}).scale(0.8)
        parts_dl = [calc_dl.get_part_by_tex(text) for text in texs]
        calc_dl.shift(2*DOWN + 2.5*LEFT)
        for mob_1, mob_2 in zip(parts_ul, parts_dl):
            mob_1.move_to(mob_2).shift(2*UP)
        calc_ul.refresh_bounding_box()
        arrow_l = Arrow(parts_ul[3], parts_dl[3], buff = 0.5)
        tip_l = MTex(r"A", color = ORANGE).scale(0.8).next_to(arrow_l, RIGHT, buff = 0.1)

        texs = r"\vec{v}", r"=", r"c_1\vec{u}_1", r"+", r"c_2\vec{u}_2"
        calc_ur = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\vec{v}": TEAL, (r"c_1", r"c_2"): PURPLE_B, r"\vec{u}_1": BLUE, r"\vec{u}_2": GREEN})
        parts_ur = [calc_ur.get_part_by_tex(text) for text in texs]
        texs = r"A\vec{v}", r"=", r"c_1\lambda_1\vec{u}_1", r"+", r"c_2\lambda_2\vec{u}_2"
        calc_dr = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"A": ORANGE, r"\vec{v}": TEAL, (r"c_1", r"c_2"): PURPLE_B, (r"\lambda_1", r"\lambda_2"): YELLOW, r"\vec{u}_1": BLUE, r"\vec{u}_2": GREEN})
        parts_dr = [calc_dr.get_part_by_tex(text) for text in texs]
        calc_dr.shift(2*DOWN + 2.5*RIGHT)
        for mob_1, mob_2 in zip(parts_ur, parts_dr):
            mob_1.move_to(mob_2).shift(2*UP)
        calc_ur.refresh_bounding_box()
        arrow_r = arrow_l.copy().match_x(parts_ur[3])
        tip_r = MTex(r"A", color = ORANGE).scale(0.8).next_to(arrow_r, RIGHT, buff = 0.1)

        self.play(Write(calc_ul), Write(calc_ur))
        self.wait()
        self.play(GrowArrow(arrow_l, rate_func = rush_into), GrowArrow(arrow_r, rate_func = rush_into), Write(tip_l), Write(tip_r))
        self.play(FadeIn(VGroup(*parts_dl[2:]), 0.5*DOWN), FadeIn(VGroup(*parts_dr[2:]), 0.5*DOWN), rate_func = rush_from)
        self.wait()
        self.play(FadeIn(VGroup(*parts_dl[:2]), 0.3*RIGHT), FadeIn(VGroup(*parts_dr[:2]), 0.3*RIGHT))
        self.wait()

        shade = self.shade.copy().shift(4.5*DOWN).set_opacity(0.5)
        self.play(FadeIn(shade))
        self.wait()
"""

"""
class Video_5(FrameScene):
    def construct(self):
        title = Title("基底变换")
        titleline = TitleLine()
        title_back = Rectangle(height = 1.0, width = FRAME_WIDTH, **background_dic, fill_color = BLACK).next_to(4*UP, DOWN, buff = 0)
        self.add(title_back, title, titleline).wait()

        coordinate = MTex(r"\begin{bmatrix}x_1\\x_2\\\vdots\\x_n\end{bmatrix}\in\mathbb{R}^n", color = TEAL, tex_to_color_map = {r"\in": WHITE, r"\mathbb{R}^n": BLUE})
        surr = SurroundingRectangle(coordinate, buff = 0.3)
        tip = Heiti(r"坐标", color = YELLOW).next_to(surr, UP)
        self.play(Write(coordinate))
        self.wait()
        self.play(ShowCreation(surr), Write(tip))
        self.wait()
        self.play(FadeOut(surr), FadeOut(tip), FadeOut(coordinate))
        self.wait()

        ratio = 0.5
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v)
        base_1, base_2 = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8)
        arrow = Arrow(ORIGIN, 2*RIGHT+DOWN, color = TEAL, buff = 0, stroke_width = 8)
        coordinate = MTex(r"(2, -1)", color = TEAL).next_to(arrow.get_end(), DOWN).set_stroke(**stroke_dic)
        self.bring_to_back(base, grid, base_1, base_2, arrow, coordinate, self.shade).play(FadeOut(self.shade))
        self.wait()

        rod_1, rod_2 = Arrow(RIGHT, 2*RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(2*RIGHT, 2*RIGHT+DOWN, color = GREEN, buff = 0, stroke_width = 8)
        self.play(GrowArrow(rod_1, run_time = 0.5, rate_func = rush_into))
        self.play(GrowArrow(rod_2, run_time = 0.5, rate_func = rush_from))
        self.wait()

        base_3 = Arrow(ORIGIN, UR, color = GREEN, buff = 0, stroke_width = 8)
        rod_3 = Arrow(2*RIGHT, 3*RIGHT, color = BLUE, buff = 0, stroke_width = 8)
        coordinate_2 = MTex(r"(3, -1)", color = TEAL).next_to(arrow.get_end(), DOWN).set_stroke(**stroke_dic)
        self.play(grid.animate.apply_matrix(np.array([[1, 1], [0, 1]])), Transform(base_2, base_3), Transform(coordinate, coordinate_2), 
                  Transform(rod_2, Arrow(3*RIGHT, 2*RIGHT+DOWN, color = GREEN, buff = 0, stroke_width = 8)), GrowArrow(rod_3), run_time = 2)
        self.wait()
"""

class Basis(VGroup):
    def __init__(self, vec_1, vec_2, color_1 = BLUE, color_2 = GREEN, **kwargs):
        arrow_1 = Vector(vec_1, color = color_1, **kwargs)
        arrow_2 = Vector(vec_2, color = color_2, **kwargs)
        super().__init__(arrow_1, arrow_2)

class BlackBox(VGroup):
    CONFIG = {
        "height": 2,
        "buff": 0.1,
        "style": {"fill_opacity": 1, 
                   "fill_color": BLACK},
    }
    def __init__(self, **kwargs):
        
        digest_config(self, kwargs)
        core = Square(side_length = self.height, **self.style)
        entrance = Polygon((0.5*self.height + self.buff)*LEFT + (0.25*self.height)*UP, 
                           (0.75*self.height + 2*self.buff)*LEFT + (0.5*self.height)*UP, 
                           (0.75*self.height + 2*self.buff)*LEFT + (0.5*self.height)*DOWN, 
                           (0.5*self.height + self.buff)*LEFT + (0.25*self.height)*DOWN, **self.style)
        export = Polygon((0.5*self.height + self.buff)*RIGHT + (0.25*self.height)*UP, 
                           (0.75*self.height + 2*self.buff)*RIGHT + (0.5*self.height)*UP, 
                           (0.75*self.height + 2*self.buff)*RIGHT + (0.5*self.height)*DOWN, 
                           (0.5*self.height + self.buff)*RIGHT + (0.25*self.height)*DOWN, **self.style)
        background = Rectangle(width = 1.5*self.height + 4*self.buff, height = 0.5*self.height, stroke_width = 0, **self.style)
        super().__init__(background, core, entrance, export, **kwargs)# background, 

"""
class Video_6(FrameScene):
    def construct(self):
        title = Title("基底变换")
        titleline = TitleLine()
        self.add(title, titleline)

        e1, e2 = 3*RIGHT + DOWN, 2*RIGHT + UP
        offset = 5*LEFT
        basis = Basis(e1, e2).shift(offset)
        texs = VGroup(MTex(r"\vec{u}_1=\begin{bmatrix}3\\-1\end{bmatrix}", color = BLUE).scale(0.8).next_to(e1, DOWN), 
                      MTex(r"\vec{u}_2=\begin{bmatrix}2\\1\end{bmatrix}", color = GREEN).scale(0.8).next_to(e2, UP), 
                      ).shift(offset)
        self.add(basis, texs).wait()

        vec_1 = Vector(RIGHT + UP, color = TEAL).shift(offset)
        tex_1 = MTex(r"\vec{x}=(-1, 2)", color = TEAL).scale(0.8).next_to(RIGHT + UP, UL).shift(offset)
        calc_1 = MTex(r"\vec{x}={-}\begin{bmatrix}3\\-1\end{bmatrix}+{2}\begin{bmatrix}2\\1\end{bmatrix}=\begin{bmatrix}1\\1\end{bmatrix}", 
                      tex_to_color_map = {(r"\vec{x}", r"\begin{bmatrix}1\\1\end{bmatrix}"): TEAL, r"\begin{bmatrix}3\\-1\end{bmatrix}": BLUE, r"\begin{bmatrix}2\\1\end{bmatrix}": GREEN, (r"{2}", r"{-}"): ORANGE}).scale(0.8).next_to(UP + 0.5*RIGHT)
        self.play(GrowArrow(vec_1), GrowFromPoint(tex_1, offset), Write(calc_1))
        self.wait()

        vec_2 = Vector(3*RIGHT, color = RED).shift(offset)
        tex_2 = MTex(r"\vec{y}=\begin{bmatrix}3\\0\end{bmatrix}", color = RED).scale(0.8).next_to(3*RIGHT, RIGHT).shift(offset)
        calc_2 = MTex(r"\vec{y}=\ ?\vec{u}_1+\ ?\vec{u}_2", 
                      tex_to_color_map = {r"\vec{y}": RED, r"\vec{u}_1": BLUE, r"\vec{u}_2": GREEN, r"?": ORANGE}).scale(0.8).next_to(0.5*DOWN + 0.5*RIGHT)
        self.play(GrowArrow(vec_2), GrowFromPoint(tex_2, offset), Write(calc_2))
        self.wait()

        equation_2 = MTex(r"\begin{cases}3x+2y={3}\\-1x+{1}y=0\end{cases}", tex_to_color_map = {(r"3", r"-1"): BLUE, (r"2", r"{1}"): GREEN, (r"x", r"y"): ORANGE, (r"{3}", r"0"): RED}).scale(0.8).next_to(0.5*DOWN + 3.5*RIGHT)
        equation_2[1:8].shift((equation_2[14].get_x() - equation_2[6].get_x())*RIGHT)
        self.play(FadeIn(equation_2, 0.5*LEFT))
        self.wait()

        copy_1 = VGroup(vec_1.copy().move_to(5*LEFT + 1.5*UP), tex_1.copy().move_to(5*LEFT + 0.5*UP))
        copy_2 = VGroup(vec_2.copy().move_to(5*RIGHT + 1.5*UP), tex_2.copy().move_to(5*RIGHT + 0.5*UP))
        self.play(*[mob.animating(run_time = 2, path_arc = 2*np.arctan(3/7)).shift(1.5*UP + 3.5*RIGHT) for mob in [basis, vec_1, vec_2]], 
                  *[OverFadeOut(mob, 1.5*UP + 3.5*RIGHT, run_time = 2, path_arc = 2*np.arctan(3/7)) for mob in [tex_1, tex_2]], 
                  *[OverFadeOut(mob, 1.5*UP + 2.5*RIGHT, run_time = 2, path_arc = 2*np.arctan(3/5)) for mob in [calc_1, calc_2, equation_2]], 
                  texs[0].animating(run_time = 2, path_arc = -2*np.arctan(3/7), rate_func = bezier([0, 0, 0, 0, 1, 1, 1])).move_to(1.5*UL + DOWN), 
                  texs[1].animating(run_time = 2, path_arc = 2*np.arctan(3/7), rate_func = bezier([0, 0, 1, 1, 1])).next_to(e2 + 1.5*UL, RIGHT).shift(0.1*DOWN), 
                  *[OverFadeIn(mob, 1.5*UP + 2.5*RIGHT, run_time = 2, path_arc = 2*np.arctan(3/5)) for mob in [copy_1, copy_2]])
        self.wait()

        box = BlackBox().shift(1.5*DOWN)
        matrix = MTex(r"\begin{bmatrix}3&2\\-1&{1}\end{bmatrix}", tex_to_color_map = {(r"3", r"-1"): BLUE, (r"2", r"{1}"): GREEN}).shift(1.5*DOWN)
        self.play(FadeIn(box, 0.5*UP), FadeIn(matrix, 0.5*UP))
        self.wait()

        matrix_l = MTex(r"\begin{bmatrix}3&2\\-1&{1}\end{bmatrix}\begin{bmatrix}-1\\2\end{bmatrix}=\begin{bmatrix}1\\1\end{bmatrix}", tex_to_color_map = {(r"3", r"-1"): BLUE, (r"2", r"{1}"): GREEN, r"\begin{bmatrix}-1\\2\end{bmatrix}": ORANGE, r"\begin{bmatrix}1\\1\end{bmatrix}": TEAL}).scale(0.8).shift(4.5*LEFT + 1.5*DOWN)
        matrix_r = MTex(r"\begin{bmatrix}3&2\\{{-1}}&{1}\end{bmatrix}^{-1}\begin{bmatrix}3\\0\end{bmatrix}=\begin{bmatrix}0.6\\0.6\end{bmatrix}", tex_to_color_map = {(r"3", r"{{-1}}"): BLUE, (r"2", r"{1}"): GREEN, r"\begin{bmatrix}3\\0\end{bmatrix}": RED, r"\begin{bmatrix}0.6\\0.6\end{bmatrix}": ORANGE}).scale(0.8).shift(4.5*RIGHT + 1.5*DOWN)
        self.play(Write(matrix_l))
        self.wait()
        self.play(Write(matrix_r))
        self.wait()
"""

#################################################################### 

class MaskImage(ImageMobject):
    CONFIG = {
        "shader_folder": "mask_image",
        "trim_left": -FRAME_X_RADIUS,
        "trim_right": FRAME_X_RADIUS
    }
    # shader_folder: str = "mask_image"
    # trim_left: float = -FRAME_X_RADIUS
    # trim_right: float = FRAME_X_RADIUS

    def init_uniforms(self):
        super().init_uniforms()
        self.uniforms["trim_left"] = self.trim_left
        self.uniforms["trim_right"] = self.trim_right

    def set_trim(self, left: float, right: float):
        self.uniforms["trim_left"] = self.trim_left = left
        self.uniforms["trim_right"] = self.trim_right = right

class MaskCircle(ImageMobject):
    CONFIG = {
        "shader_folder": "mask_circle",
        "mask_radius": 1,
        "mask_center": ORIGIN
    }
    # shader_folder: str = "mask_image"
    # trim_left: float = -FRAME_X_RADIUS
    # trim_right: float = FRAME_X_RADIUS

    def init_uniforms(self):
        super().init_uniforms()
        self.uniforms["mask_radius"] = self.mask_radius
        self.uniforms["mask_center"] = self.mask_center

    def set_trim(self, radius: float, center: np.ndarray):
        self.uniforms["mask_radius"] = self.mask_radius = radius
        self.uniforms["mask_center"] = self.mask_center = center

class Test_1(FrameScene):
    def construct(self):
        image = MaskImage("test.png", height = 8)
        self.add(image)
        # self.play(image.animate.shift(RIGHT))
        # self.play(UpdateFromAlphaFunc(image, lambda m, dt: image.set_trim_x(dt)))
        def mask_updater(mob: MaskImage):
            time = self.time
            mob.set_trim(-time, time)
        image.add_updater(mask_updater)
        self.wait(5)

class Test_2(FrameScene):
    def construct(self):
        image = MaskCircle("test.png", height = 8)
        self.add(image)
        # self.play(image.animate.shift(RIGHT))
        # self.play(UpdateFromAlphaFunc(image, lambda m, dt: image.set_trim_x(dt)))
        def mask_updater(mob: MaskImage):
            time = self.time
            mob.set_trim(time, 0.5*time*UP + 0.25*time**2*RIGHT)
        image.add_updater(mask_updater)
        self.wait(5)

class Test_3(FrameScene):
    def construct(self):
        image = ImageMobject("test.png", height = 8)
        self.add(image).wait()
        self.play(image.animate.apply_matrix(np.array([[2, 1], [0, 3]])), run_time = 3)
        self.wait()

class Test_4(FrameScene):
    # test for self.check()
    def construct(self):
        title = Title("基底变换")
        titleline = TitleLine()
        title_back = Rectangle(height = 1.0, width = FRAME_WIDTH, **background_dic, fill_color = BLACK).next_to(4*UP, DOWN, buff = 0)
        self.add(title_back, title, titleline).wait()

        coordinate = MTex(r"\begin{bmatrix}x_1\\x_2\\\vdots\\x_n\end{bmatrix}\in\mathbb{R}^n", color = TEAL, tex_to_color_map = {r"\in": WHITE, r"\mathbb{R}^n": BLUE})
        surr = SurroundingRectangle(coordinate, buff = 0.3)
        tip = Heiti(r"坐标", color = YELLOW).next_to(surr, UP)
        self.play(Write(coordinate))
        self.wait()
        self.play(ShowCreation(surr), Write(tip))
        self.wait()
        self.play(FadeOut(surr), FadeOut(tip), FadeOut(coordinate))
        self.wait()
        self.check()

        ratio = 0.5
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v)
        base_1, base_2 = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8)
        arrow = Arrow(ORIGIN, 2*RIGHT+DOWN, color = TEAL, buff = 0, stroke_width = 8)
        coordinate = MTex(r"(2, -1)", color = TEAL).next_to(arrow.get_end(), DOWN).set_stroke(**stroke_dic)
        self.bring_to_back(base, grid, base_1, base_2, arrow, coordinate, self.shade).play(FadeOut(self.shade))
        self.wait()
        self.check()

        rod_1, rod_2 = Arrow(RIGHT, 2*RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(2*RIGHT, 2*RIGHT+DOWN, color = GREEN, buff = 0, stroke_width = 8)
        self.play(GrowArrow(rod_1, run_time = 0.5, rate_func = rush_into))
        self.play(GrowArrow(rod_2, run_time = 0.5, rate_func = rush_from))
        self.wait()

        base_3 = Arrow(ORIGIN, UR, color = GREEN, buff = 0, stroke_width = 8)
        rod_3 = Arrow(2*RIGHT, 3*RIGHT, color = BLUE, buff = 0, stroke_width = 8)
        coordinate_2 = MTex(r"(3, -1)", color = TEAL).next_to(arrow.get_end(), DOWN).set_stroke(**stroke_dic)
        self.play(grid.animate.apply_matrix(np.array([[1, 1], [0, 1]])), Transform(base_2, base_3), Transform(coordinate, coordinate_2), 
                  Transform(rod_2, Arrow(3*RIGHT, 2*RIGHT+DOWN, color = GREEN, buff = 0, stroke_width = 8)), GrowArrow(rod_3), run_time = 2)
        self.wait()
        self.check()

class Test_5(FrameScene):
    # test for multilayers
    def construct(self):
        title = Title("基底变换")
        titleline = TitleLine()
        title_back = Rectangle(height = 1.0, width = FRAME_WIDTH, **background_dic, fill_color = BLACK).next_to(4*UP, DOWN, buff = 0)
        self.add_text(title_back, title, titleline).wait()

        coordinate = MTex(r"\begin{bmatrix}x_1\\x_2\\\vdots\\x_n\end{bmatrix}\in\mathbb{R}^n", color = TEAL, tex_to_color_map = {r"\in": WHITE, r"\mathbb{R}^n": BLUE})
        surr = SurroundingRectangle(coordinate, buff = 0.3)
        tip = Heiti(r"坐标", color = YELLOW).next_to(surr, UP)
        self.play(Write(coordinate))
        self.wait()
        self.play(ShowCreation(surr), Write(tip))
        self.wait()
        self.play(FadeOut(surr), FadeOut(tip), FadeOut(coordinate))
        self.wait()
        self.check()

        ratio = 0.5
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v)
        base_1, base_2 = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8)
        arrow = Arrow(ORIGIN, 2*RIGHT+DOWN, color = TEAL, buff = 0, stroke_width = 8)
        coordinate = MTex(r"(2, -1)", color = TEAL).next_to(arrow.get_end(), DOWN).set_stroke(**stroke_dic)
        self.add_background(base, grid).add(base_1, base_2, arrow).bring_to_back_of(self.float_texts, coordinate, self.shade)
        self.play(FadeOut(self.shade))
        self.wait()
        self.check()

        rod_1, rod_2 = Arrow(RIGHT, 2*RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(2*RIGHT, 2*RIGHT+DOWN, color = GREEN, buff = 0, stroke_width = 8)
        self.play(GrowArrow(rod_1, run_time = 0.5, rate_func = rush_into))
        self.play(GrowArrow(rod_2, run_time = 0.5, rate_func = rush_from))
        self.wait()

        base_3 = Arrow(ORIGIN, UR, color = GREEN, buff = 0, stroke_width = 8)
        rod_3 = Arrow(2*RIGHT, 3*RIGHT, color = BLUE, buff = 0, stroke_width = 8)
        coordinate_2 = MTex(r"(3, -1)", color = TEAL).next_to(arrow.get_end(), DOWN).set_stroke(**stroke_dic)
        self.play(grid.animate.apply_matrix(np.array([[1, 1], [0, 1]])), Transform(base_2, base_3), Transform(coordinate, coordinate_2), 
                  Transform(rod_2, Arrow(3*RIGHT, 2*RIGHT+DOWN, color = GREEN, buff = 0, stroke_width = 8)), GrowArrow(rod_3), run_time = 2)
        self.wait()
        self.check()

#################################################################### 
        
class FloatWindow(VGroup):
    CONFIG = {
        "height": FRAME_HEIGHT,
        "width": FRAME_WIDTH,
        "buff": 0.1,
        "outer_dic": {"fill_opacity": 1, 
                      "fill_color": "#222222",
                      "stroke_color": YELLOW_E},
        "inner_dic":{"fill_opacity": 1, 
                      "fill_color": BLACK,
                      "stroke_color": WHITE}
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        outer = Rectangle(height = self.height + self.buff, width = self.width + self.buff, **self.outer_dic)
        inner = Rectangle(height = self.height - self.buff, width = self.width - self.buff, **self.inner_dic)
        super().__init__(outer, inner, **kwargs)

class Video_4(FrameScene):
    def construct(self):
        title = Title("特征值和特征向量")
        titleline = TitleLine()
        title_back = Rectangle(height = 1.0, width = FRAME_WIDTH, **background_dic, fill_color = BLACK).next_to(4*UP, DOWN, buff = 0)
        matrix = MTex(r"A=\begin{bmatrix}2&1\\0&3\end{bmatrix}", color = ORANGE, tex_to_color_map = {r"=": WHITE}).shift(5*LEFT)
        eigen_1 = MTex(r"\begin{cases}\vec{p}_1=\begin{bmatrix}1\\0\end{bmatrix}\\\lambda_1=2\end{cases}", 
                       tex_to_color_map = {(r"\vec{p}_1", r"\begin{bmatrix}1\\0\end{bmatrix}"): BLUE, (r"\lambda_1", r"2"): YELLOW}).scale(0.8).shift(2.3*LEFT)
        eigen_1[8].match_x(eigen_1[15])
        calc_1 = MTex(r":A\vec{p}_1=2\vec{p}_1;", tex_to_color_map = {r"\vec{p}_1": BLUE, r"2": YELLOW, r"A": ORANGE}).shift(0.2*RIGHT)
        eigen_2 = MTex(r"\begin{cases}\vec{p}_2=\begin{bmatrix}1\\1\end{bmatrix}\\\lambda_2=3\end{cases}", 
                       tex_to_color_map = {(r"\vec{p}_2", r"\begin{bmatrix}1\\1\end{bmatrix}"): GREEN, (r"\lambda_2", r"3"): YELLOW}).scale(0.8).shift(2.7*RIGHT)
        eigen_2[8].match_x(eigen_2[15])
        calc_2 = MTex(r":A\vec{p}_2=3\vec{p}_2;", tex_to_color_map = {r"\vec{p}_2": GREEN, r"3": YELLOW, r"A": ORANGE}).shift(5.2*RIGHT)
        calc_2.remove(calc_2[-1])
        eigen = VGroup(matrix, eigen_1, calc_1, eigen_2, calc_2).shift(2*UP).scale(0.9)
        line = titleline.copy().set_color(GREY).shift(2*DOWN)
        self.add_text(title_back, title, titleline).add(eigen, line).wait()

        texs = r"\begin{bmatrix}2\\1\end{bmatrix}", r"=", r"{1}\begin{bmatrix}1\\0\end{bmatrix}", r"+", r"{1}\begin{bmatrix}1\\1\end{bmatrix}"
        calc_ul = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\begin{bmatrix}2\\1\end{bmatrix}": TEAL, r"{1}": PURPLE_B, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE, r"\begin{bmatrix}1\\1\end{bmatrix}": GREEN}).scale(0.8)
        parts_ul = [calc_ul.get_part_by_tex(text) for text in texs]
        texs = r"\begin{bmatrix}5\\3\end{bmatrix}", r"=", r"{2}\begin{bmatrix}1\\0\end{bmatrix}", r"+", r"{3}\begin{bmatrix}1\\1\end{bmatrix}"
        calc_dl = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\begin{bmatrix}5\\3\end{bmatrix}": TEAL, (r"{2}", r"{3}"): YELLOW, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE, r"\begin{bmatrix}1\\1\end{bmatrix}": GREEN}).scale(0.8)
        parts_dl = [calc_dl.get_part_by_tex(text) for text in texs]
        calc_dl.shift(2*DOWN + 2.5*LEFT)
        for mob_1, mob_2 in zip(parts_ul, parts_dl):
            mob_1.move_to(mob_2).shift(2*UP)
        calc_ul.refresh_bounding_box()
        arrow_l = Arrow(parts_ul[3], parts_dl[3], buff = 0.5)
        tip_l = MTex(r"A", color = ORANGE).scale(0.8).next_to(arrow_l, RIGHT, buff = 0.1)

        texs = r"\vec{v}", r"=", r"x_1\vec{p}_1", r"+", r"x_2\vec{p}_2"
        calc_ur = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\vec{v}": TEAL, (r"x_1", r"x_2"): PURPLE_B, r"\vec{p}_1": BLUE, r"\vec{p}_2": GREEN})
        parts_ur = [calc_ur.get_part_by_tex(text) for text in texs]
        texs = r"A\vec{v}", r"=", r"x_1\lambda_1\vec{p}_1", r"+", r"x_2\lambda_2\vec{p}_2"
        calc_dr = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"A": ORANGE, r"\vec{v}": TEAL, (r"x_1", r"x_2"): PURPLE_B, (r"\lambda_1", r"\lambda_2"): YELLOW, r"\vec{p}_1": BLUE, r"\vec{p}_2": GREEN})
        parts_dr = [calc_dr.get_part_by_tex(text) for text in texs]
        calc_dr.shift(2*DOWN + 2.5*RIGHT)
        for mob_1, mob_2 in zip(parts_ur, parts_dr):
            mob_1.move_to(mob_2).shift(2*UP)
        calc_ur.refresh_bounding_box()
        arrow_r = arrow_l.copy().match_x(parts_ur[3])
        tip_r = MTex(r"A", color = ORANGE).scale(0.8).next_to(arrow_r, RIGHT, buff = 0.1)

        self.play(Write(calc_ul), Write(calc_ur), run_time = 1)
        self.wait()
        self.play(*[FadeIn(mob, 0.4*DOWN) for mob in [arrow_l, arrow_r, tip_l, tip_r, VGroup(*parts_dl[2:]), VGroup(*parts_dr[2:])]]) # GrowArrow(arrow_l, rate_func = rush_into), GrowArrow(arrow_r, rate_func = rush_into), Write(tip_l), Write(tip_r))
        self.wait()
        self.play(FadeIn(VGroup(*parts_dl[:2]), 0.3*RIGHT), FadeIn(VGroup(*parts_dr[:2]), 0.3*RIGHT))
        self.wait()

        ratio = 0.5
        offset_r = RIGHT_SIDE/2 + 0.5*DOWN + 2*LEFT
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state()
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v).shift(offset_r)
        window = FloatWindow(height = 9, width = 15)
        p_1 = MTex(r"\vec{p}_1=\begin{bmatrix}1\\0\end{bmatrix}", color = BLUE).move_to(2*UP + 4.5*LEFT)
        p_2 = MTex(r"\vec{p}_2=\begin{bmatrix}1\\1\end{bmatrix}", color = GREEN).move_to(2*UP + 2*LEFT)
        texs = r"\begin{bmatrix}2\\1\end{bmatrix}", r"=", r"{1}\begin{bmatrix}1\\0\end{bmatrix}", r"+", r"{1}\begin{bmatrix}1\\1\end{bmatrix}"
        decom_1 = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\begin{bmatrix}2\\1\end{bmatrix}": TEAL, r"{1}": PURPLE_B, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE, r"\begin{bmatrix}1\\1\end{bmatrix}": GREEN}).scale(0.8).move_to(0.3*UP + 3.25*LEFT)
        parts_1 = [decom_1.get_part_by_tex(text) for text in texs]
        texs = r"\vec{v}", r"=", r"x_1\vec{p}_1", r"+", r"x_2\vec{p}_2"
        decom_2 = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\vec{v}": TEAL, (r"x_1", r"x_2"): PURPLE_B, r"\vec{p}_1": BLUE, r"\vec{p}_2": GREEN}).scale(0.8).move_to(0.6*DOWN + 3.25*LEFT)
        parts_2 = [decom_2.get_part_by_tex(text) for text in texs]
        for mob_1, mob_2 in zip(parts_1, parts_2):
            mob_2.match_x(mob_1)
        self.add_background(base, grid, window).play(
            window.animate.shift(7.5*LEFT), line.animate.put_start_and_end_on(6*LEFT + UP, 0.5*LEFT + UP), 
            *[OverFadeOut(mob, 7.5*LEFT) for mob in [eigen, calc_ul, calc_dl, arrow_l, tip_l, calc_ur, calc_dr, arrow_r, tip_r]], 
            *[OverFadeIn(mob, 7.5*LEFT) for mob in [p_1, p_2, decom_1, decom_2]], run_time = 2)
        self.wait()

        matrix = MTex(r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}", tex_to_color_map = {(r"0", r"1"): BLUE, r"{1}": GREEN}).scale(0.8).move_to(3.25*LEFT + 2.25*DOWN)
        box = BlackBox(height = 1.4).move_to(3.25*LEFT + 2.25*DOWN)
        P = MTex(r"P", color = BLUE).next_to(box, UP, buff = 0.1)
        operator = np.array([[1, 1], [0, 1]])
        vecs = MTex(r"\vec{x}\vec{v}", tex_to_color_map = {r"\vec{x}": PURPLE_B, r"\vec{v}": TEAL}).scale(0.8).shift(1.5*DOWN)
        vec_1, vec_2 = vecs.get_part_by_tex(r"\vec{x}").set_x(-5.2), vecs.get_part_by_tex(r"\vec{v}").set_x(-1.3)
        text_1, text_2 = r"\begin{bmatrix}x_1\\x_2\end{bmatrix}", r"\begin{bmatrix}2\\1\end{bmatrix}"
        nums = MTex(text_1+text_2, tex_to_color_map = {text_1: PURPLE_B, text_2: TEAL}).scale(0.8).shift(2.4*DOWN).set_stroke(**stroke_dic)
        num_1, num_2 = nums.get_part_by_tex(text_1).set_x(-5.2), nums.get_part_by_tex(text_2).set_x(-1.3)
        num_3 = MTex(r"\begin{bmatrix}1\\1\end{bmatrix}", color = PURPLE_B).scale(0.8).move_to(num_1)
        arrow = Arrow(box.get_left(), box.get_right())
        basis = Basis(RIGHT, UR).shift(offset_r)
        self.play(Write(vec_1), Write(vec_2), Write(num_1), Write(num_2))
        self.play(ShowCreation(arrow))
        self.wait()
        self.play(GrowFromCenter(box, run_time = 1.5), GrowFromCenter(matrix, run_time = 1.5), grid.animating(run_time = 2).apply_matrix(operator, about_point = offset_r), 
                  basis.save_state().become(Basis(RIGHT, UP).shift(offset_r)).set_opacity(0).animating(run_time = 2).restore())
        self.play(Write(P), box.animate.set_stroke(color = BLUE_B))
        self.remove(arrow).wait()

        vector = Vector(2*RIGHT + UP, color = TEAL).shift(offset_r)
        self.play(GrowArrow(vector))
        self.wait()
        num_4 = num_2.copy()
        self.bring_to_back_of(self.mobjects, num_3, num_4
            ).play(grid.animating(run_time = 2).restore(), Transform(basis, Basis(RIGHT, UP).shift(offset_r), run_time = 2), 
                   Transform(vector, Vector(RIGHT + UP, color = PURPLE_B).shift(offset_r), run_time = 2), 
                   num_4.animating(rate_func = rush_into, remover = True).scale(0, about_point = box[1].get_right()), 
                   FadeOut(num_1), 
                   num_3.save_state().scale(0, about_point = box[1].get_left()).animating(rate_func = rush_from, delay = 1).restore(), 
                   )
        self.wait()

        ap_1 = MTex(r"A\vec{p}_1=2\vec{p}_1", tex_to_color_map = {r"\vec{p}_1": BLUE, r"2": YELLOW, r"A": ORANGE}).scale(0.9).shift(2.5*UP + 4.5*LEFT)
        ap_2 = MTex(r"A\vec{p}_2=3\vec{p}_2", tex_to_color_map = {r"\vec{p}_2": GREEN, r"3": YELLOW, r"A": ORANGE}).scale(0.9).shift(2.5*UP + 2*LEFT)
        texs = r"\vec{v}", r"=", r"x_1", r"\vec{p}_1", r"+", r"x_2", r"\vec{p}_2"
        calc_ur = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\vec{v}": TEAL, (r"x_1", r"x_2"): PURPLE_B, r"\vec{p}_1": BLUE, r"\vec{p}_2": GREEN})
        parts_ur = [calc_ur.get_part_by_tex(text) for text in texs]
        texs = r"A\vec{v}", r"=", r"{2}x_1", r"\vec{p}_1", r"+", r"{3}x_2", r"\vec{p}_2"
        calc_dr = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"A": ORANGE, r"\vec{v}": TEAL, (r"x_1", r"x_2"): PURPLE_B, (r"{2}", r"{3}"): YELLOW, r"\vec{p}_1": BLUE, r"\vec{p}_2": GREEN})
        parts_dr = [calc_dr.get_part_by_tex(text) for text in texs]
        calc_dr.shift(0.5*DOWN + 3.25*LEFT)
        for mob_1, mob_2 in zip(parts_ur, parts_dr):
            mob_1.move_to(mob_2).shift(2*UP)
        calc_ur.refresh_bounding_box()
        arrow_u = Arrow(parts_ur[3], parts_dr[3], buff = 0.2)
        tip = MTex(r"A", color = ORANGE).scale(0.8).next_to(arrow_u, RIGHT, buff = 0.1)
        self.play(OverFadeOut(p_1, scale = 0.5, about_point = 3*UP + 4.5*LEFT), OverFadeOut(p_2, scale = 0.5, about_point = 3*UP + 2*LEFT), 
                  *[OverFadeOut(mob, UP) for mob in [decom_1, decom_2, matrix, box, P, vecs, num_3, num_2]], 
                  line.animate.shift(UP), 
                  *[OverFadeIn(mob, UP) for mob in [ap_1, ap_2, calc_ur, calc_dr, arrow_u, tip]], run_time = 2)
        self.wait()

        matrix = MTex(r"\begin{bmatrix}2&0\\0&3\end{bmatrix}", tex_to_color_map = {(r"2", r"3"): YELLOW, r"0": GREY}).scale(0.8).move_to(3.25*LEFT + 2.25*DOWN)
        box = BlackBox(height = 1.4).move_to(3.25*LEFT + 2.25*DOWN)
        Lambda = MTex(r"\Lambda", color = YELLOW).next_to(box, UP, buff = 0.1)
        operator_2 = np.array([[2, 0], [0, 3]])
        vecs = MTex(r"\vec{x}\Lambda\vec{x}", isolate = [r"\Lambda\vec{x}"], tex_to_color_map = {r"\vec{x}": PURPLE_B, r"\Lambda": YELLOW}).scale(0.8).shift(1.5*DOWN)
        vec_1, vec_2 = vecs.get_part_by_tex(r"\vec{x}").set_x(-5.2), vecs.get_part_by_tex(r"\Lambda\vec{x}").set_x(-1.3)
        text_1, text_2 = r"\begin{bmatrix}x_1\\x_2\end{bmatrix}", r"\begin{bmatrix}{2}x_1\\{3}x_2\end{bmatrix}"
        nums = MTex(text_1+text_2, isolate = [text_1, text_2], color = PURPLE_B, tex_to_color_map = {(r"{2}", r"{3}"): YELLOW}).scale(0.8).shift(2.4*DOWN).set_stroke(**stroke_dic)
        num_1, num_2 = nums.get_part_by_tex(text_1).set_x(-5.2), nums.get_part_by_tex(text_2).set_x(-1.3)
        arrow = Arrow(box.get_left(), box.get_right())
        basis_back = Basis(RIGHT, UP, BLUE_E, GREEN_E).shift(offset_r)
        self.play(Write(vec_1), Write(vec_2), Write(num_1), Write(num_2))
        self.play(ShowCreation(arrow))
        self.wait()
        self.add(basis_back, basis, vector).play(GrowFromCenter(box, run_time = 1.5), GrowFromCenter(matrix, run_time = 1.5), grid.animating(run_time = 2).apply_matrix(operator_2, about_point = offset_r), 
                  Transform(basis_back, Basis(2*RIGHT, 3*UP, BLUE_E, GREEN_E).shift(offset_r), run_time = 2), Transform(vector, Vector(2*RIGHT + 3*UP, color = PURPLE_B).shift(offset_r), run_time = 2), )
        self.play(Write(Lambda), box.animate.set_stroke(color = YELLOW_B))
        self.remove(arrow).wait()

        texs = r"A\vec{v}", r"=", r"x_1\lambda_1", r"\vec{p}_1", r"+", r"x_2\lambda_2", r"\vec{p}_2"
        calc_1 = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"A": ORANGE, r"\vec{v}": TEAL, (r"x_1", r"x_2"): PURPLE_B, (r"\lambda_1", r"\lambda_2"): YELLOW, r"\vec{p}_1": BLUE, r"\vec{p}_2": GREEN}).scale(0.8).move_to(0.5*UP + 3.25*LEFT)
        parts_1 = [calc_1.get_part_by_tex(text) for text in texs]
        texs = r"\begin{bmatrix}5\\3\end{bmatrix}", r"=", r"{2}", r"\begin{bmatrix}1\\0\end{bmatrix}", r"+", r"{3}", r"\begin{bmatrix}1\\1\end{bmatrix}"
        calc_2 = MTex("".join(texs), isolate = texs, 
                       tex_to_color_map = {r"\begin{bmatrix}5\\3\end{bmatrix}": TEAL, (r"{2}", r"{3}"): PURPLE_B, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE, r"\begin{bmatrix}1\\1\end{bmatrix}": GREEN}).scale(0.8).move_to(0.4*DOWN + 3.25*LEFT)
        parts_2 = [calc_2.get_part_by_tex(text) for text in texs]
        for mob_1, mob_2 in zip(parts_1, parts_2):
            mob_2.match_x(mob_1)
        
        self.play(*[OverFadeOut(mob, DOWN) for mob in [ap_1, ap_2, calc_ur, calc_dr, arrow_u, tip, matrix, box, Lambda, vecs, nums]], 
                  line.animate.shift(DOWN), 
                  OverFadeIn(p_1, scale = 2, about_point = 3*UP + 4.5*LEFT), OverFadeIn(p_2, scale = 2, about_point = 3*UP + 2*LEFT), 
                  *[OverFadeIn(mob, DOWN) for mob in [calc_1, calc_2]], run_time = 2)
        self.wait()

        matrix = MTex(r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}", tex_to_color_map = {(r"0", r"1"): BLUE, r"{1}": GREEN}).scale(0.8).move_to(3.25*LEFT + 2.25*DOWN)
        box = BlackBox(height = 1.4).move_to(3.25*LEFT + 2.25*DOWN).set_stroke(color = BLUE_B)
        P = MTex(r"P", color = BLUE).next_to(box, UP, buff = 0.1)
        vecs = MTex(r"\Lambda\vec{x}A\vec{v}", isolate = [r"\Lambda\vec{x}", r"A\vec{v}"], tex_to_color_map = {r"\vec{x}": PURPLE_B, r"\Lambda": YELLOW, r"A": ORANGE, r"\vec{v}": TEAL}).scale(0.8).shift(1.5*DOWN)
        vec_1, vec_2 = vecs.get_part_by_tex(r"\Lambda\vec{x}").set_x(-5.2), vecs.get_part_by_tex(r"A\vec{v}").set_x(-1.3)
        text_1, text_2 = r"\begin{bmatrix}{2}x_1\\{3}x_2\end{bmatrix}", r"\begin{bmatrix}5\\3\end{bmatrix}"
        nums = MTex(text_1+text_2, color = PURPLE_B, tex_to_color_map = {text_1: PURPLE_B, text_2: TEAL, (r"{2}", r"{3}"): YELLOW}).scale(0.8).shift(2.4*DOWN).set_stroke(**stroke_dic)
        num_1, num_2 = nums.get_part_by_tex(text_1).set_x(-5.2), nums.get_part_by_tex(text_2).set_x(-1.3)
        arrow = Arrow(box.get_left(), box.get_right())
        self.play(Write(vec_1), Write(vec_2), Write(num_1), Write(num_2))
        self.play(ShowCreation(arrow))
        self.wait()
        self.play(*[GrowFromCenter(mob, run_time = 1.5) for mob in [box, matrix, P]], grid.animating(run_time = 2).apply_matrix(operator, about_point = offset_r), 
                  Transform(basis_back, Basis(2*RIGHT, 3*UR, BLUE_E, GREEN_E).shift(offset_r), run_time = 2), Transform(vector, Vector(2*RIGHT + 3*UR, color = PURPLE_B).shift(offset_r), run_time = 2), )
        self.remove(arrow).wait()

        matrix_p = MTex(r"P=\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}", tex_to_color_map = {(r"0", r"1", r"P"): BLUE, r"{1}": GREEN}).move_to(2*UP + 4.75*LEFT)
        matrix_lambda = MTex(r"\Lambda = \begin{bmatrix}2&0\\0&3\end{bmatrix}", tex_to_color_map = {(r"2", r"3", r"\Lambda"): YELLOW, r"0": GREY}).move_to(2*UP + 1.75*LEFT)
        texs = r"A", r"=", r"P", r"\Lambda ", r"P^{-1}"
        decom_a = MTex("".join(texs), isolate = texs, tex_to_color_map = {r"A": ORANGE, r"P": BLUE, r"\Lambda": YELLOW}).move_to(0.2*UP + 3.25*LEFT).set_stroke(**stroke_dic)
        parts_1 = [decom_a.get_part_by_tex(text) for text in texs]
        texs = r"\begin{bmatrix}2&1\\0&3\end{bmatrix}", r"=", r"{\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}}", r"\begin{bmatrix}2&0\\0&3\end{bmatrix}", r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}^{-1}"
        decom_matrix = MTex("".join(texs), isolate = texs, tex_to_color_map = {texs[0]: ORANGE, r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}": BLUE, texs[3]: YELLOW}).scale(0.8).move_to(1*DOWN + 3.25*LEFT).set_stroke(**stroke_dic)
        parts_2 = [decom_matrix.get_part_by_tex(text) for text in texs]
        for mob_1, mob_2 in zip(parts_1, parts_2):
            mob_1.match_x(mob_2)
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-30, 31)]
        grid_2 = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state().apply_matrix(operator, about_point = offset_r)
        self.add_background(grid_2, window).play(*[OverFadeOut(mob) for mob in [p_1, p_2, calc_1, calc_2, matrix, box, P, vecs, nums, grid, basis, basis_back, vector]], 
                  *[OverFadeIn(mob) for mob in [matrix_p, matrix_lambda, decom_a, decom_matrix, grid_2]], run_time = 2)
        self.wait()
        
        rectangles = [BackgroundRectangle(VGroup(parts_1[i+2], parts_2[i+2]), buff = 0.1, fill_color = YELLOW_E if i == 1 else BLUE_E, fill_opacity = 0.5) for i in range(3)]
        rectangles[0].match_height(rectangles[2], stretch = True).match_y(rectangles[2]), rectangles[1].match_height(rectangles[2], stretch = True).match_y(rectangles[2])
        rectangle = BackgroundRectangle(VGroup(parts_1[0], parts_2[0]), buff = 0.1, fill_color = ORANGE, fill_opacity = 0.5).match_height(rectangles[2], stretch = True).match_y(rectangles[2])
        text = Songti(r"特征分解", color = YELLOW).move_to(3.25*LEFT + 2.25*DOWN)
        surr = SurroundingRectangle(text)
        self.add_background(rectangles[2]).play(FadeIn(rectangles[2]), grid_2.animating(run_time = 2).restore())
        self.wait()
        self.add_background(rectangles[1]).play(FadeIn(rectangles[1]), FadeOut(rectangles[2]), grid_2.animating(run_time = 2).apply_matrix(operator_2, about_point = offset_r))
        self.wait()
        self.add_background(rectangles[0]).play(FadeIn(rectangles[0]), FadeOut(rectangles[1]), grid_2.animating(run_time = 2).apply_matrix(operator, about_point = offset_r))
        self.wait()
        self.add_background(rectangle).play(FadeIn(rectangle), FadeOut(rectangles[0]), Write(text), ShowCreation(surr))
        self.wait()
        
        self.play(*[FadeOut(mob, 0.25*DOWN) for mob in [rectangle, matrix_p, matrix_lambda, decom_a, decom_matrix, text, surr]], 
                  FadeOut(title), line.animate.shift(0.25*DOWN), rate_func = rush_into)
        decom_a.set_y(2.4)
        decom_matrix.set_y(1.3)
        title = Title("特征分解")
        self.add_text(title).play(*[FadeIn(mob, 0.25*DOWN) for mob in [decom_a, decom_matrix]], 
                  FadeIn(title), line.animate.shift(0.25*DOWN), rate_func = rush_from)
        self.wait()

        a_2 = MTex(r"A^2=\begin{bmatrix}2\cdot2+1\cdot0&2\cdot1+1\cdot3\\0\cdot2+3\cdot0&0\cdot1+3\cdot3\end{bmatrix}=\begin{bmatrix}4&5\\0&9\end{bmatrix}").scale(0.7).shift(3.5*LEFT + 0.1*DOWN)
        for i in [0, 1, 3, 32, 34, 35, 36, 37, 38, 39]:
            a_2[i].set_color(ORANGE)
        for i in [4, 8, 11, 15, 18, 22, 25, 29]:
            a_2[i].set_color(GOLD_B)
        for i in [6, 10, 13, 17, 20, 24, 27, 31]:
            a_2[i].set_color(DARK_BROWN)
        self.play(Write(a_2))
        self.wait()
        self.play(FadeOut(a_2))
        self.wait()

        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state().apply_matrix(operator, about_point = offset_r)
        decom_2 = MTex(r"A^2=P\Lambda P^{-1}P\Lambda P^{-1}", tex_to_color_map = {r"A^2": ORANGE, r"P": BLUE, r"\Lambda": YELLOW}).shift(3.25*LEFT + 0.1*DOWN).set_stroke(**stroke_dic)
        parts = [decom_2[3], decom_2[4], decom_2[5:9], decom_2[9], decom_2[10:13]]
        rects = [BackgroundRectangle(parts[i], buff = 0.0, color = YELLOW_E if i%2 == 1 else BLUE_E, fill_opacity = 0.5) for i in range(5)]
        height = rects[2].get_height() + 0.1
        for i in range(5):
            rects[i].set_height(height, stretch = True).match_y(rects[2])
        self.add_background(grid, window).play(Write(decom_2), OverFadeOut(grid_2), OverFadeIn(grid), run_time = 2)
        self.wait()
        self.add_background(rects[4]).play(FadeIn(rects[4]), grid.animating(run_time = 2).restore())
        self.wait()
        self.play(Transform(rects[4], rects[3], remover = True), grid.animating(run_time = 2).apply_matrix(operator_2, about_point = offset_r))
        self.add_background(rects[3]).wait()
        self.play(Transform(rects[3], rects[2], remover = True), grid.save_state().animating(run_time = 2).apply_matrix(operator, about_point = offset_r))
        self.add_background(rects[2]).play(grid.animating(run_time = 2).restore())
        self.wait()
        self.play(FadeOut(parts[2]))
        self.wait()

        part_5 = MTex(r"\Lambda^2", color = YELLOW).match_x(rects[2]).set_stroke(**stroke_dic)
        part_5.shift((parts[1].get_y() - part_5[0].get_y())*UP)
        rect_5 = BackgroundRectangle(part_5, color = YELLOW_E, fill_opacity = 0.5).set_height(height, stretch = True).match_y(rects[2])
        self.play(ReplacementTransform(VGroup(parts[1], parts[3]), part_5), Transform(rects[2], rect_5), grid.animating(run_time = 2).apply_matrix(operator_2, about_point = offset_r))
        self.wait()
        self.play(Transform(rects[2], rects[0], remover = True), grid.save_state().animating(run_time = 2).apply_matrix(operator, about_point = offset_r))
        self.add_background(rects[0]).wait()

        parts_1 = [decom_2[:2], decom_2[2], parts[0], part_5, parts[4]]
        texs = r"\begin{bmatrix}4&5\\0&9\end{bmatrix}", r"=", r"{\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}}", r"\begin{bmatrix}2^2&0\\0&3^2\end{bmatrix}", r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}^{-1}"
        decom_2_matrix = MTex("".join(texs), isolate = texs, tex_to_color_map = {texs[0]: ORANGE, r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}": BLUE, texs[3]: YELLOW}).scale(0.8).move_to(1.3*DOWN + 3.25*LEFT).set_stroke(**stroke_dic)
        parts_2 = [decom_2_matrix.get_part_by_tex(text) for text in texs]
        for mob_1, mob_2 in zip(parts_1, parts_2):
            mob_1.generate_target().match_x(mob_2)
        self.play(FadeIn(decom_2_matrix, 0.5*UP), *[MoveToTarget(mob) for mob in parts_1], follow(rects[0], parts_1[2], FadeOut))
        self.wait()

        a_2.set_x(-3.6).set_y(-0.2)
        self.play(window.animate.shift(7.5*RIGHT), *[mob.animate.shift(3.25*RIGHT) for mob in [decom_a, decom_matrix]], 
                  *[mob.animate.shift(6.75*RIGHT + 0.075*DOWN) for mob in parts_1 + [decom_2_matrix]], 
                  *[OverFadeIn(mob, 6*RIGHT) for mob in [a_2]], 
                  line.animate.put_start_and_end_on(6*LEFT + 0.5*UP, 6*RIGHT + 0.5*UP), run_time = 2)
        self.remove(window, grid, base).wait()

        a_4 = MTex(r"A^4=\begin{bmatrix}4\cdot4+5\cdot0&4\cdot5+5\cdot9\\0\cdot4+9\cdot0&0\cdot5+9\cdot9\end{bmatrix}=\begin{bmatrix}16&65\\0&81\end{bmatrix}").scale(0.7)
        a_4.shift(a_2[2].get_center() - a_4[2].get_center() + 1.2*DOWN)
        for i in [0, 1, 3, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42]:
            a_4[i].set_color(ORANGE)
        for i in [4, 8, 11, 15, 18, 22, 25, 29]:
            a_4[i].set_color(GOLD_B)
        for i in [6, 10, 13, 17, 20, 24, 27, 31]:
            a_4[i].set_color(DARK_BROWN)
        self.play(Write(a_4), FadeOut(parts_2[0]))
        self.wait()

        cancels = MTex(r"A^4=P\Lambda P^{-1}P\Lambda P^{-1}P\Lambda P^{-1}P\Lambda P^{-1}", tex_to_color_map = {r"A^4": ORANGE, r"P": BLUE, r"\Lambda": YELLOW}).scale(0.8).shift(2.5*DOWN)
        lines = [Line(cancels[5+5*i].get_corner(UL), cancels[8+5*i].get_corner(DR), color = GREY) for i in range(3)]
        targets = [MTex(r"{}^4", color = ORANGE)[0].move_to(parts_1[0][1]), MTex(r"{}^4", color = YELLOW)[0].move_to(parts_1[3][1]), 
                   MTex(r"{}^4", color = YELLOW)[0].scale(0.8).move_to(parts_2[3][2]), MTex(r"{}^4", color = YELLOW)[0].scale(0.8).move_to(parts_2[3][6])]
        target = MTex(r"\begin{bmatrix}16&65\\0&81\end{bmatrix}", color = ORANGE).scale(0.8).match_y(parts_2[0].refresh_bounding_box()).match_x(parts_2[0], RIGHT)
        self.play(FadeIn(cancels, 0.3*UP))
        self.wait()
        self.play(*[ShowCreation(line) for line in lines])
        self.play(*[IndicateAround(mob, rect_kwargs = {r"color": WHITE}) for mob in targets], Transform(parts_1[0][1], targets[0]), Transform(parts_1[3][1], targets[1]), Transform(parts_2[3][2], targets[2]), Transform(parts_2[3][6], targets[3]), )
        self.wait()
        self.play(*[FadeOut(mob) for mob in lines + [cancels]], Write(target))
        self.wait()

        self.play(*[FadeOut(mob) for mob in [a_2, a_4, target]])
        self.wait()
        targets = [MTex(r"{}^n", color = ORANGE)[0].move_to(parts_1[0][1]), MTex(r"{}^n", color = YELLOW)[0].move_to(parts_1[3][1]), 
                   MTex(r"{}^n", color = YELLOW)[0].scale(0.8).move_to(parts_2[3][2]), MTex(r"{}^n", color = YELLOW)[0].scale(0.8).move_to(parts_2[3][6])]
        target = MTex(r"\begin{bmatrix}2^n&3^n-2^n\\0&3^n\end{bmatrix}", color = ORANGE).scale(0.8).match_y(parts_2[0].refresh_bounding_box()).match_x(parts_2[0], RIGHT)
        self.play(*[IndicateAround(mob, rect_kwargs = {r"color": WHITE}) for mob in targets], Transform(parts_1[0][1], targets[0]), Transform(parts_1[3][1], targets[1]), Transform(parts_2[3][2], targets[2]), Transform(parts_2[3][6], targets[3]))
        self.wait()
        self.play(Write(target))
        self.wait()

class Video_5(FrameScene):
    def construct(self):
        pass

class Video_6(FrameScene):
    def construct(self):
        pass

#################################################################### 
    
class Patch7_1(FrameScene):
    def construct(self):
        ratio = 0.5
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-20, 21)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).apply_matrix(np.array([[1, 1], [0, 1]])).apply_matrix(np.array([[2, 1], [0, 3]]))
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-30, 31)]
        base = VGroup(*lines_h, *lines_v).apply_matrix(np.array([[1, 1], [0, 1]]))
        self.add(base, grid)
        
class Patch7_2(FrameScene):
    def construct(self):
        ratio = 0.5
        lines_h = [Line(2*RIGHT_SIDE + i*ratio*DOWN, 2*LEFT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*DOWN + i*ratio*RIGHT, 4*UP + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-20, 21)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).apply_matrix(np.array([[2, 1], [0, 3]]))
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v)
        self.add(base, grid)

class Patch7_3(FrameScene):
    def construct(self):
        ratio = 0.5
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = GREEN_E if i else WHITE) for i in range(-30, 31)]
        lines_v = [Line(2*4*UP + i*ratio*RIGHT, 2*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = GREEN_E if i else WHITE) for i in range(-20, 21)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).apply_matrix(np.array([[1, 0], [1, 1]])).apply_matrix(np.array([[2, 1], [0, 3]]))
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-30, 31)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else GREY) for i in range(-30, 31)]
        base = VGroup(*lines_h, *lines_v).apply_matrix(np.array([[1, 0], [1, 1]]))
        self.add(base, grid)
 
class BlackArrow(VGroup):
    CONFIG = {
        "height": 2,
        "buff": 0.1,
        "style": {"fill_opacity": 1, 
                   "fill_color": BLACK},
    }
    def __init__(self, **kwargs):
        
        digest_config(self, kwargs)
        core = Rectangle(width = 0.75*self.height, height = 0.75*self.height, **self.style)
        entrance = Polygon((0.375*self.height + self.buff)*LEFT + (0.25*self.height)*UP, 
                           (0.7*self.height + 2*self.buff)*LEFT + (0.5*self.height)*UP, 
                           (0.6*self.height + 2*self.buff)*LEFT, 
                           (0.7*self.height + 2*self.buff)*LEFT + (0.5*self.height)*DOWN, 
                           (0.375*self.height + self.buff)*LEFT + (0.25*self.height)*DOWN, **self.style)
        export = Polygon((0.375*self.height + self.buff)*RIGHT + (0.5*self.height)*UP, 
                           (0.7*self.height + 2*self.buff)*RIGHT + (0.0*self.height)*UP, 
                           (0.375*self.height + self.buff)*RIGHT + (0.5*self.height)*DOWN, **self.style)
        super().__init__(core, entrance, export, **kwargs)# background, 

class Video_7(FrameScene):
    def construct(self):
        title = Title("特征分解")
        titleline = TitleLine()
        title_back = Rectangle(height = 1.0, width = FRAME_WIDTH, **background_dic, fill_color = BLACK).next_to(4*UP, DOWN, buff = 0)
        matrix_p = MTex(r"P=\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}", tex_to_color_map = {(r"0", r"1", r"P"): BLUE, r"{1}": GREEN}).move_to(2*UP + 4.75*LEFT)
        matrix_lambda = MTex(r"\Lambda = \begin{bmatrix}2&0\\0&3\end{bmatrix}", tex_to_color_map = {(r"2", r"3", r"\Lambda"): YELLOW, r"0": GREY}).move_to(2*UP + 1.75*LEFT)
        texs = r"A", r"=", r"P", r"\Lambda ", r"P^{-1}"
        decom_a = MTex("".join(texs), isolate = texs, tex_to_color_map = {r"A": ORANGE, r"P": BLUE, r"\Lambda": YELLOW}).move_to(0.3*UP + 3.25*LEFT).set_stroke(**stroke_dic)
        parts_1 = [decom_a.get_part_by_tex(text) for text in texs]
        texs = r"\begin{bmatrix}2&1\\0&3\end{bmatrix}", r"=", r"{\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}}", r"\begin{bmatrix}2&0\\0&3\end{bmatrix}", r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}^{-1}"
        decom_matrix = MTex("".join(texs), isolate = texs, tex_to_color_map = {texs[0]: ORANGE, r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}": BLUE, texs[3]: YELLOW}).scale(0.8).move_to(0.9*DOWN + 3.25*LEFT).set_stroke(**stroke_dic)
        parts_2 = [decom_matrix.get_part_by_tex(text) for text in texs]
        for mob_1, mob_2 in zip(parts_1, parts_2):
            mob_1.match_x(mob_2)
        line = Line(6*LEFT + UP, 0.5*LEFT + UP, color = GREY)
        ratio = 0.5
        offset_r = RIGHT_SIDE/2 + 0.5*DOWN + 2*LEFT
        operator = np.array([[1, 1], [0, 1]])
        operator_2 = np.array([[2, 0], [0, 3]])
        operator_0 = np.array([[1, -1], [0, 1]])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v).shift(offset_r)
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state().apply_matrix(operator, about_point = offset_r)
        window = FloatWindow(height = 9, width = 15).shift(7.5*LEFT)
        self.bring_to_front(self.shade).add_text(title_back, title, titleline).add(matrix_p, matrix_lambda, line, decom_a, decom_matrix).add_background(base, grid, window)
        self.play(FadeOut(self.shade))
        self.wait()

        rectangles = [BackgroundRectangle(VGroup(parts_1[i+2], parts_2[i+2]), buff = 0.1, fill_color = YELLOW_E if i == 1 else BLUE_E, fill_opacity = 0.5) for i in range(3)]
        rectangles[0].match_height(rectangles[2], stretch = True).match_y(rectangles[2]), rectangles[1].match_height(rectangles[2], stretch = True).match_y(rectangles[2])
        rectangle = BackgroundRectangle(VGroup(parts_1[0], parts_2[0]), buff = 0.1, fill_color = ORANGE, fill_opacity = 0.5).match_height(rectangles[2], stretch = True).match_y(rectangles[2])
        self.add_background(rectangles[2]).play(FadeIn(rectangles[2]), grid.animating(run_time = 2).restore())
        self.wait()
        self.add_background(rectangles[1]).play(FadeIn(rectangles[1]), FadeOut(rectangles[2]), grid.animating(run_time = 2).apply_matrix(operator_2, about_point = offset_r))
        self.wait()
        self.add_background(rectangles[0]).play(FadeIn(rectangles[0]), FadeOut(rectangles[1]), grid.animating(run_time = 2).apply_matrix(operator, about_point = offset_r))
        self.wait()
        self.play(FadeOut(rectangles[0]))
        self.wait()

        self.play(FadeOut(grid), rate_func = rush_into)
        basis = Basis(RIGHT, UR).shift(offset_r).save_state()
        self.add_background(grid.restore().apply_matrix(operator, about_point = offset_r), window).play(FadeIn(grid), FadeIn(basis), rate_func = rush_from)
        self.wait()
        self.play(Transform(basis, Basis(2*RIGHT, UR).shift(offset_r)), grid.animate.apply_matrix(np.array([[2, -1], [0, 1]]), about_point = offset_r), run_time = 2, path_arc = 0)
        self.wait()
        self.play(Transform(basis, Basis(2*RIGHT, 3*UR).shift(offset_r)), grid.animate.apply_matrix(np.array([[1, 2], [0, 3]]), about_point = offset_r), run_time = 2, path_arc = 0)
        self.wait()

        lines_h = [Line(2*RIGHT_SIDE + i*ratio*DOWN, 2*LEFT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*DOWN + i*ratio*RIGHT, 4*UP + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-10, 21)]
        h_2, v_2 = VGroup(*lines_h[::-1]), VGroup(*lines_v[::-1])
        grid_2 = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state()
        self.play(FadeOut(grid), FadeOut(basis), rate_func = rush_into)
        self.add_background(grid_2, window, rectangle).play(FadeIn(rectangle), FadeIn(grid_2), FadeIn(basis.restore()), rate_func = rush_from)
        self.wait()
        self.play(Transform(basis, Basis(2*RIGHT, UR).shift(offset_r)), grid_2.animate.apply_matrix(np.array([[2, -1], [0, 1]]), about_point = offset_r), run_time = 2, path_arc = 0)
        self.wait()
        self.play(Transform(basis, Basis(2*RIGHT, 3*UR).shift(offset_r)), grid_2.animate.apply_matrix(np.array([[1, 2], [0, 3]]), about_point = offset_r), run_time = 2, path_arc = 0)
        self.wait()
        
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 21)]
        h_1, v_1 = VGroup(*lines_h), VGroup(*lines_v)
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state().apply_matrix(operator, about_point = offset_r)
        self.play(FadeOut(rectangle), FadeOut(grid_2), FadeOut(basis), rate_func = rush_into)
        self.add_background(grid_2, window, rectangles[2]).play(FadeIn(rectangles[2]), FadeIn(grid_2.restore()), FadeIn(basis.restore()), rate_func = rush_from)
        self.remove(base).wait()
        self.add_background(h_2, v_2, h_1, v_1, window, rectangles[2]).play(Uncreate(h_2, rate_func = lambda t: less_smooth(1-t)), Uncreate(v_2, rate_func = lambda t: less_smooth(1-t)), ShowCreation(h_1, rate_func = less_smooth), ShowCreation(v_1, rate_func = less_smooth), lag_ratio = 0.02, run_time = 2)
        self.wait()
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v).shift(offset_r).apply_matrix(operator, about_point = offset_r)
        self.remove(h_1, v_1).add_background(base, grid, window, rectangles[1]).play(FadeIn(rectangles[1]), FadeOut(rectangles[2]), 
                    grid.animating(run_time = 2).apply_matrix(np.array([[2, 1], [0, 3]]), about_point = offset_r), Transform(basis, Basis(2*RIGHT, 3*UR).shift(offset_r), run_time = 2))
        self.wait()

        view_1 = MaskCircle("Patch7_1.png", height = 8, mask_radius = 10, mask_center = 0.5*DOWN).shift(offset_r)
        view_2 = MaskImage("Patch7_2.png", height = 8, trim_left = 0).shift(offset_r)
        alpha = ValueTracker(0.0)
        circle_1 = VGroup(Circle(radius = 11, stroke_color = BLUE_E, n_components = 24), Circle(radius = 11, stroke_color = YELLOW_E, n_components = 24).reverse_points(), VMobject(stroke_width = 0, fill_opacity = 1, fill_color = "#222222")).shift(0.5*DOWN)
        matrix_a = MTex(r"\begin{bmatrix}2&1\\0&3\end{bmatrix}", color = ORANGE).set_stroke(**stroke_dic).next_to(6*RIGHT + 3*UP, DOWN)
        def paras(t: float):
            return 11*(1-t), 6*DOWN + 4*RIGHT + 5*t*(1.2*UP + 0.8*LEFT) + 12*t*(1-t)*(0.8*UR + 0.4*RIGHT)
        def mask_updater(mob: MaskImage):
            value = alpha.get_value()
            mob.set_trim(*paras(value))
        view_1.add_updater(mask_updater)
        def circle_updater(mob: VGroup):
            radius, center = paras(alpha.get_value())
            mob[0].set_height(radius*2 + 0.1).move_to(center), mob[1].set_height(radius*2 - 0.1).move_to(center)
            mob[2].set_points([*mob[0].get_points(), *mob[1].get_points()])
        circle_1.add_updater(circle_updater)
        self.remove(base, grid).add_background(view_2, view_1, circle_1, window, rectangles[1]).play(FadeOut(rectangles[1]), FadeOut(basis))
        self.wait()
        self.play(alpha.animate.set_value(1.0), run_time = 3, rate_func = linear)
        self.play(Write(matrix_a))
        self.remove(view_1, circle_1).wait()

        view_1 = MaskImage("Patch7_1.png", height = 8, trim_right = 0).shift(offset_r)
        line_m = VGroup(Line(4*UP, 4*DOWN, color = BLUE_E).shift(0.05*RIGHT), Line(4*UP, 4*DOWN, color = YELLOW_E).shift(0.05*LEFT), Rectangle(height = 8, width = 0.1, fill_color = "#222222", **background_dic))
        matrix_l = MTex(r"\begin{bmatrix}2&0\\0&3\end{bmatrix}", color = YELLOW).set_stroke(**stroke_dic).next_to(6*LEFT + 3*UP, DOWN)
        self.add_background(view_2, view_1, line_m, matrix_l, window
                ).play(*[mob.animating(remover = True).shift((64/9 + 0.05 + 0.02)*LEFT) for mob in [matrix_p, matrix_lambda, line, decom_a, decom_matrix, window]], 
                       *[mob.animate.move_to(0.5*DOWN) for mob in [view_1, view_2]], run_time = 2)
        self.wait()

        arrow = BlackArrow().add(MTex(r"\begin{bmatrix}1&1\\0&1\end{bmatrix}", color = BLUE)).shift(0.5*UP).scale(0.8)
        self.add(arrow).play(GrowFromCenter(arrow))
        self.wait()
        alpha = ValueTracker(0.0)
        def view_1_updater(mob: MaskImage):
            mob.set_trim(-FRAME_X_RADIUS, alpha.get_value())
        def view_2_updater(mob: MaskImage):
            mob.set_trim(alpha.get_value(), FRAME_X_RADIUS)
        def shift_updater(mob: BlackArrow):
            mob.set_x(alpha.get_value())
        view_1.add_updater(view_1_updater), view_2.add_updater(view_2_updater), arrow.add_updater(shift_updater), line_m.add_updater(shift_updater)
        self.play(alpha.animate.set_value(-4.5), run_time = 2)
        self.wait()
        self.play(alpha.animate.set_value(4.5), run_time = 3)
        self.wait()
        self.play(alpha.animate.set_value(0), run_time = 2)
        self.wait()
        for mob in [view_1, view_2, arrow, line_m]:
            mob.clear_updaters()

        view_3 = MaskCircle("Patch7_3.png", height = 8, mask_radius = 10, mask_center = 0.5*DOWN)
        alpha = ValueTracker(0.0)
        circle_3 = VGroup(Circle(radius = 2.5, stroke_color = GREY, n_components = 24), Circle(radius = 2.5, stroke_color = GREEN_E, n_components = 24).reverse_points().save_state(), VMobject(stroke_width = 0, fill_opacity = 1, fill_color = "#222222")).shift(0.5*DOWN)
        def paras(t: float):
            return 2.5*t, 5*DOWN + t*4.5*UP
        def mask_updater(mob: MaskImage):
            value = alpha.get_value()
            mob.set_trim(*paras(value))
        view_3.add_updater(mask_updater)
        def circle_updater(mob: VGroup):
            radius, center = paras(alpha.get_value())
            mob[0].set_height(radius*2 + 0.1).move_to(center), mob[1].restore().set_height(radius*2 - 0.1).move_to(center)
            mob[2].set_points([*mob[0].get_points(), *mob[1].get_points()])
        circle_3.add_updater(circle_updater)
        arrow_2 = BlackArrow().add(MTex(r"\begin{bmatrix}1&0\\1&1\end{bmatrix}", color = GREEN)).shift(2.5*RIGHT + 0.5*DOWN).scale(0.8)
        
        self.add_background(view_3, circle_3
                ).play(*[mob.animating(remover = True).shift((1+0.02)*UP) for mob in [title_back, title, titleline]], 
                  arrow.animate.shift(2.3*UP), *[mob.animate.shift(0.5*UP) for mob in [view_1, view_2]], 
                  GrowFromPoint(arrow_2, 5*DOWN), alpha.animate.set_value(1.0), run_time = 2)
        self.wait()
        matrix_3 = MTex(r"\begin{bmatrix}3&1\\0&2\end{bmatrix}", color = TEAL).set_stroke(**stroke_dic).move_to(2*DOWN)
        self.play(Write(matrix_3))
        self.wait()
        
        P = MTex(r"P", color = BLUE).scale(0.8).next_to(arrow, UP, buff = 0.0).set_stroke(**stroke_dic)
        Q = MTex(r"Q", color = GREEN).scale(0.8).next_to(arrow_2, UP, buff = 0.0).set_stroke(**stroke_dic)
        self.play(Write(P), Write(Q))
        self.wait()

        arc = Arc(start_angle = -PI*2/3, angle = PI*4/3, stroke_width = 8, color = YELLOW, n_components = 24).apply_matrix(np.array([[4, -1.25], [0, 1.75]])).shift(1.25*RIGHT + 1.15*UP)
        path = Arrow(stroke_width = 8).become(arc).set_color(WHITE).insert_tip_anchor().create_tip_with_stroke_width()
        path_back = Arrow().become(arc).set_color(BLACK).insert_tip_anchor().create_tip_with_stroke_width().set_stroke(width = path.get_stroke_widths() + 8)
        self.add(path_back, path, arrow[0], arrow[-1], arrow_2[0], arrow_2[-1]).play(ShowCreation(path_back), ShowCreation(path), run_time = 2)
        self.wait()

        com = MTex(r"P^{-1}Q", tex_to_color_map = {r"Q": GREEN, r"P": BLUE}).shift(2.5*LEFT + 0.5*DOWN).scale(0.8).set_stroke(**stroke_dic)
        matrix_3 = MTex(r"\begin{bmatrix}0&1\\-1&1\end{bmatrix}", color = LIME).shift(2.5*LEFT + 0.5*DOWN).scale(0.78)
        matrix_3[0].shift(0.11*RIGHT)
        for i in [1, 3, 4]:
            matrix_3[i].shift(0.085*RIGHT)
        for i in [2, 5, 6]:
            matrix_3[i].shift(0.11*LEFT)
        arrow_3 = BlackArrow().shift(2.5*LEFT + 0.5*DOWN).scale(np.array([-0.8, 0.8, 0.8]), min_scale_factor = -1)
        self.play(GrowFromCenter(arrow_3), GrowFromCenter(com))
        self.wait()
        self.play(com.animate.next_to(arrow_3, UP, buff = 0.0))
        self.play(FadeIn(matrix_3))
        self.wait()

#################################################################### 

class MaskVMobject(VMobject):
    CONFIG = {
        "stroke_shader_folder": "mask_stroke",
        "fill_shader_folder": "mask_fill",
        "mask_radius": 1,
        "mask_center": ORIGIN
    }
    def init_uniforms(self):
        super().init_uniforms()
        self.uniforms["mask_radius"] = self.mask_radius
        self.uniforms["mask_center"] = self.mask_center

    def set_trim(self, radius: float, center: np.ndarray):
        self.uniforms["mask_radius"] = self.mask_radius = radius
        self.uniforms["mask_center"] = self.mask_center = center

class Test_6(FrameScene):
    def construct(self):
        # image = MaskCircle("test.png", height = 8)
        # self.add(image)
        # def mask_updater(mob: MaskImage):
        #     time = self.time
        #     mob.set_trim(time, 0.5*time*UP + 0.25*time**2*RIGHT)
        # image.add_updater(mask_updater)
        # self.wait(5)

        ratio = 0.5
        dic_mask = {"stroke_shader_folder": "mask_stroke", "fill_shader_folder": "mask_fill"}
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-20, 21)]
        for mob in lines_h + lines_v:
            mob.uniforms["mask_radius"] = 1
            mob.uniforms["mask_center"] = ORIGIN
        base = VGroup(*lines_h, *lines_v)
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        self.add(base)
        
class Test_7(FrameScene):
    def construct(self):
        ratio = 0.5
        dic_mask = {"stroke_shader_folder": "sector_stroke", "fill_shader_folder": "mask_fill"}
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-20, 21)]
        for mob in lines_h + lines_v:
            mob.uniforms["half_1"] = unit(0)
            mob.uniforms["center_1"] = 3*RIGHT
            mob.uniforms["half_2"] = unit(PI/3)
            mob.uniforms["center_2"] = 3*RIGHT
        base = VGroup(*lines_h, *lines_v)
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        self.add(base)

class Flip(Animation):
    CONFIG = {
        "dim": 1,
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

class Video_8(FrameScene):
    def construct(self):
        title = Title("相似变换")
        titleline = TitleLine()
        title_back = Rectangle(height = 1.0, width = FRAME_WIDTH, **background_dic, fill_color = BLACK).next_to(4*UP, DOWN, buff = 0)
        # matrix_p = MTex(r"P=\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}", tex_to_color_map = {(r"0", r"1", r"P"): BLUE, r"{1}": GREEN}).move_to(2*UP + 4.75*LEFT)
        # matrix_lambda = MTex(r"\Lambda = \begin{bmatrix}2&0\\0&3\end{bmatrix}", tex_to_color_map = {(r"2", r"3", r"\Lambda"): YELLOW, r"0": GREY}).move_to(2*UP + 1.75*LEFT)
        # texs = r"A", r"=", r"P", r"\Lambda ", r"P^{-1}"
        # decom_a = MTex("".join(texs), isolate = texs, tex_to_color_map = {r"A": ORANGE, r"P": BLUE, r"\Lambda": YELLOW}).move_to(0.3*UP + 3.25*LEFT).set_stroke(**stroke_dic)
        # parts_1 = [decom_a.get_part_by_tex(text) for text in texs]
        # texs = r"\begin{bmatrix}2&1\\0&3\end{bmatrix}", r"=", r"{\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}}", r"\begin{bmatrix}2&0\\0&3\end{bmatrix}", r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}^{-1}"
        # decom_matrix = MTex("".join(texs), isolate = texs, tex_to_color_map = {texs[0]: ORANGE, r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}": BLUE, texs[3]: YELLOW}).scale(0.8).move_to(0.9*DOWN + 3.25*LEFT).set_stroke(**stroke_dic)
        # parts_2 = [decom_matrix.get_part_by_tex(text) for text in texs]
        # for mob_1, mob_2 in zip(parts_1, parts_2):
        #     mob_1.match_x(mob_2)
        # line = Line(6*LEFT + UP, 0.5*LEFT + UP, color = GREY)
        ratio = 0.5
        offset_r = RIGHT_SIDE/2 + 0.5*DOWN
        operator_l = np.array([[1, 1], [0, 1]])
        operator_b = np.array([[1, 0], [1, 1]])
        operator = np.array([[2, 1], [0, 3]])
        dic_mask = {"stroke_shader_folder": "sector_stroke", "fill_shader_folder": "mask_fill"}
        lines_h_a = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-10, 11)]
        lines_v_a = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-20, 21)]
        dic_a = {"half_1": unit(PI), "center_1": offset_r, "half_2": unit(TAU/3), "center_2": offset_r}
        for mob in lines_h_a + lines_v_a:
            mob.uniforms.update(dic_a)
        base_a = VGroup(*lines_h_a, *lines_v_a).shift(offset_r)
        lines_h_l = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-10, 11)]
        lines_v_l = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-20, 21)]
        dic_l = {"half_1": unit(0), "center_1": offset_r, "half_2": unit(PI/3), "center_2": offset_r}
        for mob in lines_h_l + lines_v_l:
            mob.uniforms.update(dic_l)
        base_l = VGroup(*lines_h_l, *lines_v_l).shift(offset_r)
        lines_h_b = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask).apply_matrix(operator_b) for i in range(-10, 21)]
        lines_v_b = [Line(2*4*UP + i*ratio*RIGHT, 2*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask).apply_matrix(operator_b) for i in range(-20, 21)]
        dic_b = {"half_1": unit(-TAU/3), "center_1": offset_r, "half_2": unit(-PI/3), "center_2": offset_r}
        for mob in lines_h_b + lines_v_b:
            mob.uniforms.update(dic_b)
        base_b = VGroup(*lines_h_b, *lines_v_b).shift(offset_r)
        
        lines_h_a = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE, **dic_mask) for i in range(-10, 11)]
        lines_v_a = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE, **dic_mask) for i in range(-20, 21)]
        dic_a = {"half_1": unit(PI), "center_1": offset_r, "half_2": unit(TAU/3), "center_2": offset_r}
        for mob in lines_h_a + lines_v_a:
            mob.uniforms.update(dic_a)
        grid_a = VGroup(*lines_h_a[:10], *lines_h_a[11:], *lines_v_a, lines_h_a[10]).shift(offset_r).save_state()
        lines_h_l = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-10, 11)]
        lines_v_l = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-20, 21)]
        dic_l = {"half_1": unit(0), "center_1": offset_r, "half_2": unit(PI/3), "center_2": offset_r}
        for mob in lines_h_l + lines_v_l:
            mob.uniforms.update(dic_l)
        grid_l = VGroup(*lines_h_l[:10], *lines_h_l[11:], *lines_v_l, lines_h_l[10]).shift(offset_r).save_state()
        lines_h_b = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = GREEN_E if i else WHITE, **dic_mask).apply_matrix(operator_b) for i in range(-10, 21)]
        lines_v_b = [Line(2*4*UP + i*ratio*RIGHT, 2*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = GREEN_E if i else WHITE, **dic_mask).apply_matrix(operator_b) for i in range(-20, 21)]
        dic_b = {"half_1": unit(-TAU/3), "center_1": offset_r, "half_2": unit(-PI/3), "center_2": offset_r}
        for mob in lines_h_b + lines_v_b:
            mob.uniforms.update(dic_b)
        grid_b = VGroup(*lines_h_b[:10], *lines_h_b[11:], *lines_v_b, lines_h_b[10]).shift(offset_r).save_state()
        
        dots_1 = 8*unit(-PI/6) + 0.05*unit(PI/3), unit(PI/6)/(10*np.sqrt(3)), 4*UP + 0.05*RIGHT
        dots_2 = 4*UP + 0.05*LEFT, unit(5*PI/6)/(10*np.sqrt(3)), 8*unit(-5*PI/6) + 0.05*unit(2*PI/3)
        dots_3 = 8*unit(-5*PI/6) + 0.05*unit(-PI/3), unit(-PI/2)/(10*np.sqrt(3)), 8*unit(-PI/6) + 0.05*unit(-2*PI/3)
        line_1 = Polyline(*dots_1, color = YELLOW_E)
        line_2 = Polyline(*dots_2, color = BLUE_E)
        line_3 = Polyline(*dots_3, color = GREEN_E)
        middle = Polygon(*dots_1, *dots_2, *dots_3, **background_dic, fill_color = "#222222")
        divider = VGroup(middle, line_1, line_2, line_3).shift(offset_r)

        # lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-10, 11)]
        # lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = YELLOW_E if i else WHITE) for i in range(-30, 31)]
        # grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state().apply_matrix(operator_l, about_point = offset_r)
        window = FloatWindow(height = 9, width = 15).shift(7.5*LEFT)

        offset_l = LEFT_SIDE/2 + 0.1*DOWN
        radius = 2.2
        center_a, center_l, center_b = radius*unit(5*PI/6) + offset_l, radius*unit(PI/6) + offset_l, radius*unit(-PI/2) + offset_l
        matrix_a = MTex(r"\begin{bmatrix}2&1\\0&3\end{bmatrix}", color = ORANGE).set_stroke(**stroke_dic).move_to(center_a)
        matrix_l = MTex(r"\begin{bmatrix}2&0\\0&3\end{bmatrix}", color = YELLOW).set_stroke(**stroke_dic).move_to(center_l)
        matrix_b = MTex(r"\begin{bmatrix}3&1\\0&2\end{bmatrix}", color = TEAL).set_stroke(**stroke_dic).move_to(center_b)
        circle_a = Circle(radius = 1, color = BLUE_E, stroke_width = 10).move_to(center_a)
        circle_l = Circle(radius = 1, color = YELLOW_E, stroke_width = 10).move_to(center_l)
        circle_b = Circle(radius = 1, color = GREEN_E, stroke_width = 10).move_to(center_b)
        arc_1, arc_2 = Arc(radius = 1, start_angle = -PI/6, angle = PI/3).shift(radius*unit(5*PI/6) + offset_l), Arc(radius = 1, start_angle = 5*PI/6, angle = PI/3).shift(radius*unit(PI/6) + offset_l)
        tunnel_la = VMobject(color = BLUE_E, stroke_width = 8).append_points(arc_1.get_points()).add_line_to(arc_2.get_start()).append_points(arc_2.get_points()).close_path()
        tunnel_bl = VMobject(color = LIME, stroke_width = 8).match_points(tunnel_la).rotate(-TAU/3, about_point = offset_l)
        tunnel_ba = VMobject(color = GREEN_E, stroke_width = 8).match_points(tunnel_la).rotate(TAU/3, about_point = offset_l)
        trans_la = MTex(r"\begin{bmatrix}1&1\\0&1\end{bmatrix}", color = BLUE).set_stroke(**stroke_dic).scale(0.8).move_to(tunnel_la)
        trans_bl = MTex(r"\begin{bmatrix}0&1\\-1&1\end{bmatrix}", color = LIME).set_stroke(**stroke_dic).scale(0.8).move_to(tunnel_bl)
        trans_bl[0].shift(0.11*RIGHT)
        for i in [1, 3, 4]:
            trans_bl[i].shift(0.085*RIGHT)
        for i in [2, 5, 6]:
            trans_bl[i].shift(0.11*LEFT)
        trans_ba = MTex(r"\begin{bmatrix}1&0\\1&1\end{bmatrix}", color = GREEN).set_stroke(**stroke_dic).scale(0.78).move_to(tunnel_ba)
        arrow_la = Arrow(circle_l, circle_a, stroke_width = 16, buff = 0.2, color = interpolate_color(BLUE_E, BLACK, 0.5))
        arrow_bl = Arrow(circle_b, circle_l, stroke_width = 16, buff = 0.1, color = interpolate_color(LIME, BLACK, 0.5))
        arrow_ba = Arrow(circle_b, circle_a, stroke_width = 16, buff = 0.1, color = interpolate_color(GREEN_E, BLACK, 0.5))
        self.bring_to_front(self.shade).add_text(title_back, title, titleline
                ).add(tunnel_la, tunnel_bl, tunnel_ba, arrow_la, arrow_bl, arrow_ba, circle_a, circle_l, circle_b, trans_la, trans_bl, trans_ba, matrix_a, matrix_l, matrix_b
                ).add_background(base_a, base_l, base_b, grid_a, grid_l, grid_b, divider, window)
        self.play(FadeOut(self.shade))
        self.wait()

        self.play(*[mob.animate.apply_matrix(operator, about_point = offset_r) for mob in [grid_a, grid_l, grid_b]], run_time = 2, path_arc = -PI/6)
        self.wait()

        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_from)
        self.wait()

        point_a, point_l, point_b = offset_r + radius*unit(PI*5/6), offset_r + radius*unit(PI/6), offset_r + radius*unit(-PI/2) + 0.5*UP
        indicate = Circle(stroke_width = 8).move_to(point_a)
        arc_1, arc_2 = Arc(radius = 1, start_angle = PI/6, angle = PI*5/3, n_components = 24).shift(radius*unit(5*PI/6) + offset_l), Arc(radius = 1, start_angle = -5*PI/6, angle = PI*5/3, n_components = 24).shift(radius*unit(PI/6) + offset_l)
        dic_mask = {"stroke_shader_folder": "sector_stroke", "fill_shader_folder": "sector_fill"}
        union = VMobject(color = BLUE_E, stroke_width = 0, fill_opacity = 0.5, **dic_mask).append_points(arc_1.get_points()).add_line_to(arc_2.get_start()).append_points(arc_2.get_points()).close_path()
        dic_1 = {"half_1": unit(0), "center_1": circle_a.get_left(), "half_2": unit(PI), "center_2": circle_a.get_right() + 0.05*LEFT}
        union.uniforms.update(dic_1)
        texs = r"\begin{bmatrix}2&1\\0&3\end{bmatrix}", r"=", r"{\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}}", r"\begin{bmatrix}2&0\\0&3\end{bmatrix}", r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}^{-1}"
        decom_matrix = MTex("".join(texs), isolate = texs, tex_to_color_map = {texs[0]: ORANGE, r"\begin{bmatrix}1&{1}\\0&{1}\end{bmatrix}": BLUE, texs[3]: YELLOW}).scale(0.6).next_to(3.5*LEFT + 3*UP, DOWN, buff = 0.1).set_stroke(**stroke_dic)
        parts_2 = [decom_matrix.get_part_by_tex(text) for text in texs]
        self.add_background(union).play(ShowCreation(indicate), FadeIn(union))
        self.wait()
        self.play(Write(parts_2[0], run_time = 2), *[mob.animating(run_time = 2, path_arc = -PI/6).apply_matrix(operator, about_point = offset_r) for mob in [grid_a, grid_l, grid_b]], )
        self.wait()
        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_from)
        self.wait()
        dic_2 = {"half_1": unit(0), "center_1": circle_l.get_left() + 0.05*RIGHT, "half_2": unit(PI), "center_2": circle_l.get_right()}
        union.generate_target().set_color(YELLOW_E).uniforms.update(dic_2)
        self.play(Write(parts_2[4]), indicate.animate.move_to(point_l), MoveToTarget(union))
        self.wait()
        self.play(Write(parts_2[3], run_time = 2), *[mob.animating(run_time = 2, path_arc = -PI/6).apply_matrix(operator, about_point = offset_r) for mob in [grid_a, grid_l, grid_b]], )
        self.wait()
        union.generate_target().set_color(BLUE_E).uniforms.update(dic_1)
        self.play(Write(parts_2[2]), indicate.animate.move_to(point_a), MoveToTarget(union), FadeIn(parts_2[1], scale = 1/3))
        self.wait()
        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_from)
        self.play(FadeOut(decom_matrix))
        self.add(parts_2[0]).play(*[FadeOut(mob) for mob in parts_2[1:]])
        self.wait()
        self.remove(parts_2[0])

        union.rotate(TAU/3, about_point = offset_l)
        dic_1 = {"half_1": unit(-PI/3), "center_1": center_a + unit(TAU/3), "half_2": unit(TAU/3), "center_2": center_a + 0.95*unit(-PI/3)}
        union.uniforms.update(dic_1)
        texs = r"\begin{bmatrix}2&1\\0&3\end{bmatrix}", r"=", r"{\begin{bmatrix}1&0\\{1}&{1}\end{bmatrix}}", r"\begin{bmatrix}3&1\\0&2\end{bmatrix}", r"\begin{bmatrix}1&0\\{1}&{1}\end{bmatrix}^{-1}"
        decom_matrix = MTex("".join(texs), isolate = texs, tex_to_color_map = {texs[0]: ORANGE, r"\begin{bmatrix}1&0\\{1}&{1}\end{bmatrix}": GREEN, texs[3]: TEAL}).scale(0.6).next_to(3.5*LEFT + 3*UP, DOWN, buff = 0.1).set_stroke(**stroke_dic)
        parts_2 = [decom_matrix.get_part_by_tex(text) for text in texs]
        self.add(parts_2[0])
        self.wait()
        
        dic_2 = {"half_1": unit(-PI/3), "center_1": center_b + 0.95*unit(TAU/3), "half_2": unit(TAU/3), "center_2": center_b + unit(-PI/3)}
        union.generate_target().set_color(GREEN_E).uniforms.update(dic_2)
        self.play(Write(parts_2[4]), indicate.animate.move_to(point_b), MoveToTarget(union))
        self.wait()
        self.play(Write(parts_2[3], run_time = 2), *[mob.animating(run_time = 2, path_arc = -PI/6).apply_matrix(operator, about_point = offset_r) for mob in [grid_a, grid_l, grid_b]], )
        self.wait()
        union.generate_target().set_color(BLUE_E).uniforms.update(dic_1)
        self.play(Write(parts_2[2]), indicate.animate.move_to(point_a), MoveToTarget(union), FadeIn(parts_2[1], scale = 1/3))
        self.wait()
        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_from)
        self.play(FadeOut(decom_matrix), FadeOut(indicate), FadeOut(union))
        self.wait()

        eigenvalues = MTex(r"\lambda_1 = 2\\\lambda_2 = 3", tex_to_color_map = {r"\lambda_1 = 2": YELLOW_E, r"\lambda_2 = 3": LIGHT_BROWN}).scale(0.8).move_to(offset_l + 2.4*UP)
        eigenline_1 = Line(LEFT_SIDE, RIGHT_SIDE, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5).shift(offset_r)
        eigenline_2 = Line(5*UR, 5*DL, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5).shift(offset_r)
        texts = r"\begin{bmatrix}1\\0\end{bmatrix}", r"\begin{bmatrix}1\\1\end{bmatrix}"
        vectors_a = MTex("".join(texts), tex_to_color_map = {texts[0]: YELLOW_E, texts[1]: LIGHT_BROWN}).scale(0.9).move_to(center_a)
        texts = r"\begin{bmatrix}1\\0\end{bmatrix}", r"\begin{bmatrix}0\\1\end{bmatrix}"
        vectors_l = MTex("".join(texts), tex_to_color_map = {texts[0]: YELLOW_E, texts[1]: LIGHT_BROWN}).scale(0.9).move_to(center_l)
        texts = r"\begin{bmatrix}1\\-1\end{bmatrix}", r"\begin{bmatrix}1\\0\end{bmatrix}"
        vectors_b = MTex("".join(texts), tex_to_color_map = {texts[0]: YELLOW_E, texts[1]: LIGHT_BROWN}).scale(0.9).move_to(center_b)
        vectors_b[0].shift(0.07*RIGHT)
        vectors_b[4:].shift(0.07*LEFT)
        vectors_b[:5].shift(0.06*RIGHT)
        vectors_b[5:].shift(0.06*LEFT)
        title_2 = Title(r"基底变换")
        self.bring_to_back(eigenline_1, eigenline_2).play(Write(eigenvalues), ShowCreation(eigenline_1, start = 0.5), ShowCreation(eigenline_2, start = 0.5), Transform(title.save_state(), title_2), 
                                                          *[FadeOut(mob, run_time = 0.5) for mob in [matrix_a, matrix_l, matrix_b]], 
                                                          *[FadeIn(mob, run_time = 0.5, delay = 0.5) for mob in [vectors_a, vectors_l, vectors_b]], )
        self.wait()
        self.play(*[mob.animating(run_time = 2).apply_matrix(operator, about_point = offset_r) for mob in [grid_a, grid_l, grid_b]])
        self.wait()
        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_from)
        self.wait()

        circle_1 = Circle(radius = 1.06, color = YELLOW_A, stroke_width = 8).move_to(center_l)
        circle_2 = Circle(radius = 1, color = BLACK).move_to(center_l)
        circle_3 = Circle(radius = 0.94, color = YELLOW_E, stroke_width = 8).move_to(center_l)
        self.play(*[ShowCreation(mob) for mob in [circle_1, circle_2, circle_3]])
        self.wait()

        title_3 = Title(r"相似对角化")
        self.play(Flip(title, title_3), *[FadeIn(mob, run_time = 0.5, delay = 0.5) for mob in [matrix_a, matrix_l, matrix_b]], *[FadeOut(mob, run_time = 0.5) for mob in [vectors_a, vectors_l, vectors_b]])
        self.wait()

        self.play(*[mob.animating(run_time = 2).apply_matrix(operator, about_point = offset_r) for mob in [grid_a, grid_l, grid_b]])
        self.wait()
        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, grid_l, grid_b]], run_time = 0.5, rate_func = rush_from)
        self.wait()

#################################################################### 

class Video_10(FrameScene):
    def construct(self):
        offset_l = LEFT_SIDE/2
        text_matrix = r"\begin{bmatrix}0&-1\\1&0\end{bmatrix}"
        matrix = MTex(text_matrix, color = ORANGE).shift(offset_l + 3*UP)
        ratio = 0.5
        offset_r = RIGHT_SIDE/2
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v).shift(offset_r)
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(2*4*UP + i*ratio*RIGHT, 2*4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state()
        window = FloatWindow(height = 9, width = 15).shift(7.5*LEFT)
        self.bring_to_front(self.shade).add(matrix).add_background(base, grid, window)
        self.play(FadeOut(self.shade))
        self.wait()
        self.play(Rotate(grid, PI/2, about_point = offset_r, run_time = 2))
        self.wait()
        self.play(FadeOut(grid, remover = False, run_time = 0.5, rate_func = rush_into))
        self.play(FadeIn(grid.restore(), run_time = 0.5, rate_func = rush_from))
        self.wait()

        polynomial = MTex(r"f(\lambda)=\begin{vmatrix}0\,{-}\,\lambda&-1\\1&0\,{-}\,\lambda\end{vmatrix}=\lambda^2+1", 
                          tex_to_color_map = {r"\begin{vmatrix}0\,{-}\,\lambda&-1\\1&0\,{-}\,\lambda\end{vmatrix}": ORANGE, r"{-}": WHITE, (r"f", r"\lambda"): YELLOW}
                          ).scale(0.8).next_to(offset_l + 1.5*UP + 3*LEFT)
        self.play(Write(polynomial))
        self.wait()

        complex_1 = MTex(text_matrix + r"\begin{bmatrix}i\\1\end{bmatrix}=\begin{bmatrix}-1\\i\end{bmatrix}={i}\begin{bmatrix}i\\1\end{bmatrix}", 
                         tex_to_color_map = {text_matrix: ORANGE, r"\begin{bmatrix}i\\1\end{bmatrix}": BLUE, r"\begin{bmatrix}-1\\i\end{bmatrix}": BLUE, r"{i}": YELLOW}
                         ).scale(0.8).next_to(offset_l + 0.5*DOWN + 3*LEFT)
        complex_2 = MTex(text_matrix + r"\begin{bmatrix}1\\i\end{bmatrix}=\begin{bmatrix}-i\\1\end{bmatrix}=-{i}\begin{bmatrix}1\\i\end{bmatrix}", 
                         tex_to_color_map = {text_matrix: ORANGE, r"\begin{bmatrix}1\\i\end{bmatrix}": GREEN, r"\begin{bmatrix}-i\\1\end{bmatrix}": GREEN, r"{i}": YELLOW}
                         ).scale(0.8).next_to(offset_l + 1.7*DOWN + 3*LEFT)
        self.play(Write(complex_1), Write(complex_2), Rotate(grid, PI/2, about_point = offset_r, run_time = 2))
        self.wait()
        
class Video_11(FrameScene):
    def construct(self):
        offset_l = LEFT_SIDE/2
        text_matrix = r"\begin{bmatrix}1&1\\0&1\end{bmatrix}"
        matrix = MTex(text_matrix, color = ORANGE).shift(offset_l + 3*UP)
        ratio = 0.5
        offset_r = RIGHT_SIDE/2
        operator = np.array([[1, 1], [0, 1]])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base = VGroup(*lines_h, *lines_v).shift(offset_r)
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(2*4*UP + i*ratio*RIGHT, 2*4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-30, 31)]
        grid = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(offset_r).save_state()
        window = FloatWindow(height = 9, width = 15).shift(7.5*LEFT)
        self.bring_to_front(self.shade).add(matrix).add_background(base, grid, window)
        self.play(FadeOut(self.shade))
        self.wait()
        self.play(grid.animate.apply_matrix(operator, about_point = offset_r), run_time = 2)
        self.wait()
        self.play(FadeOut(grid, remover = False, run_time = 0.5, rate_func = rush_into))
        self.play(FadeIn(grid.restore(), run_time = 0.5, rate_func = rush_from))
        self.wait()

        polynomial = MTex(r"f(\lambda)=\begin{vmatrix}1\,{-}\,\lambda&1\\0&1\,{-}\,\lambda\end{vmatrix}=(\lambda-1)^2", 
                          tex_to_color_map = {r"\begin{vmatrix}1\,{-}\,\lambda&1\\0&1\,{-}\,\lambda\end{vmatrix}": ORANGE, r"{-}": WHITE, (r"f", r"\lambda"): YELLOW}
                          ).scale(0.8).next_to(offset_l + 1.5*UP + 3*LEFT)
        self.play(Write(polynomial))
        self.wait()

        eigen = MTex(r"\begin{bmatrix}1\,{-}\,{1}&1\\0&1\,{-}\,{1}\end{bmatrix}\begin{bmatrix}x_1\\x_2\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix}", 
                     isolate = r"=", tex_to_color_map = {r"\begin{bmatrix}1\,{-}\,{1}&1\\0&1\,{-}\,{1}\end{bmatrix}": ORANGE, r"{-}": WHITE, r"{1}": YELLOW, r"\begin{bmatrix}x_1\\x_2\end{bmatrix}": BLUE, r"\begin{bmatrix}0\\0\end{bmatrix}": GREY}
                     ).scale(0.8).next_to(offset_l + 0.0*UP + 3*LEFT)
        eigenvector = MTex(r"\begin{bmatrix}x_1\\x_2\end{bmatrix}=c\begin{bmatrix}1\\0\end{bmatrix}", 
                           isolate = r"=", tex_to_color_map = {r"\begin{bmatrix}x_1\\x_2\end{bmatrix}": BLUE, r"c": PURPLE_B, r"\begin{bmatrix}1\\0\end{bmatrix}": BLUE}
                           ).scale(0.8)
        eigenvector.shift(eigen.get_part_by_tex(r"=").get_center() - eigenvector.get_part_by_tex(r"=").get_center() + 1.5*DOWN)
        eigenline = Line(LEFT_SIDE, RIGHT_SIDE, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5).shift(offset_r)
        self.play(FadeIn(eigen, UP))
        self.wait()
        self.bring_to_back(eigenline).play(Write(eigenvector), ShowCreation(eigenline, start = 0.5))
        self.wait()
        self.play(grid.animate.apply_matrix(operator, about_point = offset_r), run_time = 2)
        self.wait()

        text_geo = MTexText(r"几何重数为1", tex_to_color_map = {r"1": YELLOW, r"几何重数": YELLOW_E}).scale(0.6).next_to(eigenvector, LEFT, buff = 1)
        arrow = Arrow(text_geo, eigenvector)
        text_alg = MTexText(r"代数重数为2", tex_to_color_map = {r"2": RED, r"代数重数": RED_E}).set_stroke(**stroke_dic).scale(0.6).next_to(polynomial[-1], UP).shift(0.5*LEFT)
        surr = SurroundingRectangle(polynomial[-1], color = RED)
        self.play(FadeIn(text_geo.add(arrow), 0.5*RIGHT))
        self.wait()
        self.play(ShowCreation(surr), FadeIn(text_alg, 0.5*LEFT))
        self.wait()

#################################################################### 

class Test_9(FrameScene):
    # for how depth_tset works
    def construct(self):
        square_0 = Square(fill_color = GREEN, fill_opacity = 1)
        square_1 = Square(fill_color = BLUE, fill_opacity = 1).shift(np.array([1, 1, 1]))
        self.add(square_1, square_0).wait()
        square_0.apply_depth_test(), square_1.apply_depth_test()
        self.wait()

class Video_2_1(FrameScene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(200).shift(0.5*OUT).set_orientation(Rotation(quadternion))
        camera.quadternion = quadternion
        height, half_height = 3, 1.5
        top = ImageMobject(r"enlarged_top.png", depth_test = True, height = height).shift(half_height*OUT)
        bottom = ImageMobject(r"enlarged_bottom.png", depth_test = True, height = height).shift(half_height*IN)
        front = ImageMobject(r"enlarged_front.png", depth_test = True, height = height).rotate(PI/2, axis = RIGHT).shift(half_height*DOWN)
        side_1 = ImageMobject(r"enlarged_side.png", depth_test = True, height = height).rotate(PI/2, axis = RIGHT).shift(half_height*DOWN).rotate(PI/2, axis = OUT, about_point = ORIGIN)
        side_2 = ImageMobject(r"enlarged_side.png", depth_test = True, height = height).rotate(PI/2, axis = RIGHT).shift(half_height*DOWN).rotate(PI, axis = OUT, about_point = ORIGIN)
        side_3 = ImageMobject(r"enlarged_side.png", depth_test = True, height = height).rotate(PI/2, axis = RIGHT).shift(half_height*DOWN).rotate(-PI/2, axis = OUT, about_point = ORIGIN)
        faces = [top, bottom, front, side_1, side_2, side_3]
        dic = {r"buff": 0, r"depth_test": True, r"stroke_width": 12, r"color": WHITE, r"anti_alias_width": 0}
        polyline_x, poliline_y = Line(5*LEFT, 5*RIGHT, **dic).insert_n_curves(29), Line(5*DOWN, 5*UP, **dic).insert_n_curves(29)
        axes = VGroup(Arrow(**dic).become(polyline_x).insert_tip_anchor().create_tip_with_stroke_width(), 
                      Arrow(**dic).become(poliline_y).insert_tip_anchor().create_tip_with_stroke_width(), 
                      Arrow(4*IN, 4*OUT, **dic), depth_test = True).scale(np.array([0.99, 1.01, 1])).shift(0.065*OUT)
        eigen = np.array([1, 1, 1])
        eigenline = DashedLine(3*eigen, -3*eigen, dash_length = 0.1*np.sqrt(3), color = YELLOW, depth_test = True, stroke_width = 12, anti_alias_width = 0)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(quad(OUT, -PI/90*dt), mob.quadternion)
            mob.set_orientation(Rotation(mob.quadternion))
        camera.add_updater(camera_updater)
        self.add(*faces, axes, eigenline).wait(5)
        dic = {r"axis": eigen, r"about_point": ORIGIN}
        self.play(*[Rotate(mob, PI/3, run_time = 1, **dic) for mob in faces])
        self.wait()
        self.play(*[Rotate(mob, -PI/6, run_time = 1, **dic) for mob in faces])
        self.wait()
        self.play(*[Rotate(mob, 4*PI, run_time = 4, **dic) for mob in faces])
        self.wait()
        self.play(*[Rotate(mob, -PI - PI/2, run_time = 2, **dic) for mob in faces])
        self.wait(9)
  
class Patch2_1(FrameScene):
    def construct(self):
        Euler = LabelPicture("Euler.jpg", "　　莱昂哈德·欧拉\n（1707.4.15—1783.9.18）", picture_config = {"height": 3}).shift(5.7*LEFT + UP)
        Euler[1].set_stroke(**stroke_dic)
        self.play(FadeIn(Euler, 0.5*UP))
        self.wait()
        Lagrange = LabelPicture("Lagrange.jpg", "约瑟夫-路易·拉格朗日\n（1736.1.25—1813.4.10）", picture_config = {"height": 3}).shift(5.7*RIGHT + UP)
        Lagrange[1].set_stroke(**stroke_dic)
        self.play(FadeIn(Lagrange, 0.5*UP))
        self.wait()
        
class Video_2_2(FrameScene):
    CONFIG = {
        "camera_class": AACamera
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_focal_distance(500).shift(0.5*OUT).set_orientation(Rotation(quadternion))
        camera.quadternion = quadternion
        hyperbolic_paraboloid = ParametricSurface(lambda u, v: np.array([u, v, (u+v)*(u-v)/3]), [-3, 3], [-3, 3], color = [BLUE_D, GREEN_D])
        # mesh = SurfaceMesh(hyperbolic_paraboloid, color = GREY, anti_alias_width = 0)
        n = 12
        dic = {r"stroke_width": 1, r"color": GREY_D, r"depth_test": True, r"anti_alias_width": 0, r"buff": 0.02}
        mesh = VGroup(*[Line(np.array([i, n-abs(i), i*(n-abs(i))/n*2*np.sqrt(2)])*3*np.sqrt(2)/n, np.array([i, abs(i)-n, i*(abs(i)-n)/n*2*np.sqrt(2)])*3*np.sqrt(2)/n, **dic) for i in range(-n, n+1)], 
                      *[Line(np.array([n-abs(i), i, i*(n-abs(i))/n*2*np.sqrt(2)])*3*np.sqrt(2)/n, np.array([abs(i)-n, i, i*(abs(i)-n)/n*2*np.sqrt(2)])*3*np.sqrt(2)/n, **dic) for i in range(-n, n+1)], 
                      depth_test = True).rotate(-PI/4).shift(0.02*OUT)
        dic = {r"buff": 0, r"depth_test": True, r"stroke_width": 12, r"color": WHITE, r"anti_alias_width": 0}
        polyline_x, poliline_y = Line(3*DL, 3.2*UR, **dic).insert_n_curves(29), Line(3*UL, 3.2*DR, **dic).insert_n_curves(29)
        axes = VGroup(Arrow(**dic).become(polyline_x).insert_tip_anchor().create_tip_with_stroke_width(), 
                      Arrow(**dic).become(poliline_y).insert_tip_anchor().create_tip_with_stroke_width(), 
                      Arrow(4*IN, 4*OUT, **dic), depth_test = True).scale(np.array([0.99, 1.01, 1])).shift(0.065*OUT)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(quad(OUT, -PI/45*dt), mob.quadternion)
            mob.set_orientation(Rotation(mob.quadternion))
        camera.add_updater(camera_updater)
        self.add(hyperbolic_paraboloid, axes, mesh).wait(30)
        
class Patch2_2(FrameScene):
    def construct(self):
        Cauchy = LabelPicture("Cauchy.jpg", "奥古斯丁·路易·柯西\n（1789.8.21 - 1857.5.23）", picture_config = {"height": 3}).shift(5.7*LEFT + UP)
        Cauchy[1].set_stroke(**stroke_dic)
        self.play(FadeIn(Cauchy))
        self.wait()
        function = MTex(r"z=xy", tex_to_color_map = {r"x": BLUE, r"y": GREEN, r"z": PURPLE_B}).set_stroke(**stroke_dic).shift(5.5*RIGHT + 2*UP)
        self.play(Write(function))
        self.wait()
        text_normal = MTexText(r"规范形", color = YELLOW_E).set_stroke(**stroke_dic).scale(0.8).next_to(function, DOWN, buff = 0.5)
        normal = MTex(r"\begin{bmatrix}1&0&0\\0&-1&0\\0&0&{0}\end{bmatrix}", tex_to_color_map = {r"0": GREY, (r"1", r"-1", r"{0}"): YELLOW}
                      ).set_stroke(**stroke_dic).scale(0.8).next_to(text_normal, DOWN, buff = 0.1)
        self.play(FadeIn(normal, 0.5*UP), FadeIn(text_normal, 0.5*UP))
        self.wait()

#################################################################### 

class Video_6_2(FrameScene):
    def construct(self):

        ratio = 0.5
        operator = np.array([[1, 1], [1, 0]])
        lines_h = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-8, 9)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-14, 15)]
        base = VGroup(*lines_h, *lines_v)
        lines_h = [Line(2*LEFT_SIDE + i*ratio*DOWN, 2*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 0 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-16, 17)]
        lines_v = [Line(2*4*UP + i*ratio*RIGHT, 2*4*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-28, 29)]
        grid = VGroup(*lines_h[:16], *lines_h[17:], *lines_v, lines_h[16])
        phi, psi = (1+np.sqrt(5))/2, (1-np.sqrt(5))/2
        eigen_1, eigen_2 = np.array([phi, 1, 0]), np.array([psi, 1, 0]), 
        eigenline_1 = Line(4*eigen_1, -4*eigen_1, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5, anti_alias_width = 0).fix_in_frame()
        eigenline_2 = Line(4*eigen_2, -4*eigen_2, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5, anti_alias_width = 0).fix_in_frame()
        vec_dic = {r"color": RED, r"stroke_width": 8}
        vector = Vector(RIGHT, **vec_dic)
        f_n = np.zeros(20)
        f_n[1] = 1
        for i in range(2, 20):
            f_n[i] = f_n[i-1] + f_n[i-2]
        self.bring_to_front(self.shade).add(vector).add_background(eigenline_1, eigenline_2, base, grid).play(FadeOut(self.shade))
        self.wait()

        blurs = []
        RED_G = interpolate_color(RED_E, BLACK, 0.5)
        blur = vector.copy().set_color(RED_G)
        self.add(blur, vector), blurs.append(blur)
        self.play(Transform(vector, Vector(np.array([f_n[2], f_n[1], 0]), **vec_dic), run_time = 2), grid.animating(run_time = 2).apply_matrix(operator))
        self.wait()

        blur = vector.copy().set_color(RED_G)
        self.add(blur, vector), blurs.append(blur)
        self.play(Transform(vector, Vector(np.array([f_n[3], f_n[2], 0]), **vec_dic), run_time = 2), grid.animating(run_time = 2).apply_matrix(operator))
        self.wait()

        blur = vector.copy().set_color(RED_G)
        self.add(blur, vector), blurs.append(blur)
        self.play(Transform(vector, Vector(np.array([f_n[4], f_n[3], 0]), **vec_dic), run_time = 2), grid.animating(run_time = 2).apply_matrix(operator))
        self.wait()

        time = self.time
        def camera_updater(mob: CameraFrame):
            t = self.time - time
            # if t < 9:
            #     power = t*(9-t)/13.5 + t*2/3
            # else:
            #     power = (t+9)/3
            # print(power)
            power = t/3
            mob.set_height(8*phi**(power))
        self.camera.frame.add_updater(camera_updater)
        def arrow_updater(mob: Arrow):
            t = self.time - time
            power = t/3
            mob.set_stroke(width = 8*phi**power)
        vector.add_updater(arrow_updater)
        blur = vector.copy().set_color(RED_G).clear_updaters()
        self.add(blur, vector), blurs.append(blur)
        self.play(Transform(vector, Vector(np.array([f_n[5], f_n[4], 0]), color = RED, stroke_width = 8*phi**(2/3)), run_time = 2), grid.animating(run_time = 2).apply_matrix(operator))
        self.wait()

        for i in range(5, 10):
            blur = vector.copy().set_color(RED_G).clear_updaters()
            self.add(blur, vector), blurs.append(blur)
            self.play(Transform(vector, Vector(np.array([f_n[i+1], f_n[i], 0]), color = RED, stroke_width = 8*phi**(i-10/3)), run_time = 2), grid.animating(run_time = 2).apply_matrix(operator))
            self.wait()

class Patch6_2(FrameScene):
    def construct(self):
        matrix = MTex(r"\begin{bmatrix}1&{1}\\1&0\end{bmatrix}", color = ORANGE).set_stroke(**stroke_dic).shift(6*LEFT + 2*UP)
        tip_1 = MTex(r"y=\phi x", tex_to_color_map = {(r"x", r"y"): BLUE, r"\phi": YELLOW}).move_to(3*UR).set_stroke(**stroke_dic)
        tip_2 = MTex(r"y=-\frac{1}{\phi} x", tex_to_color_map = {(r"x", r"y"): GREEN, r"-\frac{1}{\phi}": YELLOW}).next_to(2*LEFT + 3*UP, DL).set_stroke(**stroke_dic)
        f_n = np.zeros(20)
        s_n = [r"0", r"1"]
        f_n[1] = 1
        for i in range(2, 20):
            f_n[i] = f_n[i-1] + f_n[i-2]
            s_n.append(str(int(f_n[i])))
        texs_vector = [MTex(r"\begin{bmatrix}" + s_n[i+1] + r"\\" + s_n[i] + r"\end{bmatrix}", tex_to_color_map = {(s_n[i+1], s_n[i]): RED}).move_to(2*DOWN + (i-4.5)*1.5*RIGHT).set_stroke(**stroke_dic) for i in range(19)]
        self.bring_to_front(self.shade).add(tip_1, tip_2, matrix, texs_vector[0]).play(FadeOut(self.shade))
        self.wait()

        for i in range(1, 10):
            self.play(Write(texs_vector[i]))
            # self.wait(2)
                
#################################################################### 

class Video_9(FrameScene):
    def construct(self):
        offset_l = LEFT_SIDE/2
        prop = MTex(r"\det(A)=\lambda_1\lambda_2\cdots\lambda_n", tex_to_color_map = {r"A": ORANGE, (r"\lambda_1", r"\lambda_2", r"\lambda_n"): YELLOW}).shift(3*UP)
        self.add(prop).wait()
        calc = MTex(r"f(\lambda)=\det(A-\lambda I)=\begin{vmatrix}2-\lambda&1\\0&3-\lambda\end{vmatrix}=({2}-\lambda)({3}-\lambda)", 
                    tex_to_color_map = {(r"A", r"\begin{vmatrix}2-\lambda&1\\0&3-\lambda\end{vmatrix}"): ORANGE, r"\lambda": YELLOW_E, (r"{2}", r"{3}"): YELLOW}).shift(1.5*UP)
        self.play(FadeIn(calc, UP))
        self.wait()
        solution = MTex(r"\det(A)=f(0)=2\times 3", tex_to_color_map = {r"A": ORANGE, r"0": GREY, (r"2", r"3"): YELLOW_E}).shift(0.0*UP)
        self.play(Write(solution))
        self.wait()

        window = FloatWindow(height = 9, width = 15)
        A = MTex(r"A=\begin{bmatrix}2&1\\0&3\end{bmatrix}", color = ORANGE, tex_to_color_map = {r"=": WHITE})# .shift(offset_l + 2*UP)
        A.shift(prop[6].get_center() - A[1].get_center() + offset_l + DOWN)
        area = MTex(r"S'=S\cdot\det(A)", tex_to_color_map = {(r"S", r"S'"): TEAL, r"A": ORANGE})# .next_to(4.5*LEFT + 0.5*UP)
        area.shift(A[1].get_center() - area[2].get_center() + 1.5*DOWN)
        start, r = 3.5*LEFT + 0.5*UP, 3.2
        point = Point(start)
        def mask_updater(mob: VMobject):
            mob.uniforms["mask_center"] = point.get_location()
        ratio = 0.5
        offset_r = RIGHT_SIDE/2 + 2.5*LEFT + 0.8*DOWN
        operator_l = np.array([[1, 1], [0, 1]])
        operator = np.array([[2, 1], [0, 3]])
        dic_mask = {"stroke_shader_folder": "mask_stroke", "fill_shader_folder": "mask_fill"}
        lines_h_a = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-10, 11)]
        lines_v_a = [Line(5*UP + i*ratio*RIGHT, 5*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(-20, 21)]
        base_a = VGroup(*lines_h_a, *lines_v_a).shift(offset_r)
        lines_h_l = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-10, 11)]
        lines_v_l = [Line(5*UP + i*ratio*RIGHT, 5*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-20, 21)]
        dic_l = {"mask_center": start, "mask_radius": r}
        for mob in lines_h_l + lines_v_l:
            mob.uniforms.update(dic_l)
            mob.add_updater(mask_updater)
        base_l = VGroup(*lines_h_l, *lines_v_l).shift(offset_r)
        lines_h_a = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-10, 11)]
        lines_v_a = [Line(5*UP + i*ratio*RIGHT, 5*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-20, 21)]
        grid_a = VGroup(*lines_h_a[:10], *lines_h_a[11:], *lines_v_a, lines_h_a[10]).shift(offset_r).save_state()
        lines_h_l = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-10, 11)]
        lines_v_l = [Line(5*UP + i*ratio*RIGHT, 5*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = YELLOW_E if i else WHITE, **dic_mask).apply_matrix(operator_l) for i in range(-20, 21)]
        for mob in lines_h_l + lines_v_l:
            mob.uniforms.update(dic_l)
            mob.add_updater(mask_updater)
        grid_l = VGroup(*lines_h_l[:10], *lines_h_l[11:], *lines_v_l, lines_h_l[10]).shift(offset_r).save_state()
        unit_a = Polygon(ORIGIN, RIGHT, UR, UP, color = TEAL, fill_opacity = 0.2).shift(offset_r).save_state()
        unit_l = Polygon(ORIGIN, RIGHT, UR+RIGHT, UR, color = TEAL, fill_opacity = 0.2, **dic_mask).shift(offset_r).save_state()
        unit_l.uniforms.update(dic_l), unit_l.add_updater(mask_updater)
        back_3 = Circle(radius = r, fill_opacity = 1, fill_color = BLACK).shift(start)
        circle_3 = VGroup(Circle(radius = r - 0.05, stroke_color = BLUE_E, n_components = 24), Circle(radius = r + 0.05, stroke_color = YELLOW_E, n_components = 24).reverse_points(), VMobject(stroke_width = 0, fill_opacity = 1, fill_color = "#222222")).shift(start)
        circle_3[2].set_points([*circle_3[0].get_points(), *circle_3[1].get_points()])
        self.add_background(base_a, grid_a, unit_a, back_3, base_l, grid_l, circle_3, unit_l, window).play(window.animate.shift(7.5*LEFT), prop.animate.shift(offset_l), *[OverFadeOut(mob, offset_l) for mob in [calc, solution]], OverFadeIn(A, offset_l), run_time = 2)
        self.wait()
        
        self.play(Write(area), *[mob.animating(run_time = 2).apply_matrix(operator, about_point = offset_r) for mob in [grid_a, unit_a]])
        self.wait()
        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, unit_a]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, unit_a]], run_time = 0.5, rate_func = rush_from)
        self.wait()

        lambda_1 = MTex(r"\lambda_1 = 2", color = YELLOW).next_to(RIGHT_SIDE + 0.8*DOWN, DL).set_stroke(**stroke_dic)
        lambda_2 = MTex(r"\lambda_2 = 3", color = YELLOW).next_to(offset_r + 3.2*UR + 0.3*RIGHT, UL).set_stroke(**stroke_dic)
        self.play(*[mob.animate.move_to(3.5*RIGHT + 0.5*UP) for mob in [point, back_3, circle_3]], run_time = 2)
        dic_l = {"mask_center": 3.5*RIGHT + 0.5*UP, "mask_radius": r}
        eigenline_1_a = Line(LEFT_SIDE, RIGHT_SIDE, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5).shift(offset_r)
        eigenline_2_a = Line(5*UR, 5*DL, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5).shift(offset_r)
        eigenline_1_l = Line(LEFT_SIDE, RIGHT_SIDE, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5, **dic_mask).shift(offset_r)
        eigenline_2_l = Line(5*UR, 5*DL, stroke_width = 12, color = YELLOW, stroke_opacity = 0.5, **dic_mask).shift(offset_r)
        eigenline_1_l.uniforms.update(dic_l), eigenline_2_l.uniforms.update(dic_l)
        self.add_background(eigenline_1_a, eigenline_2_a, base_a, grid_a, unit_a, back_3, eigenline_1_l, eigenline_2_l, base_l, grid_l, circle_3, unit_l, lambda_1, lambda_2, window
                    ).play(*[ShowCreation(mob, start = 0.5) for mob in [eigenline_1_a, eigenline_2_a, eigenline_1_l, eigenline_2_l]], Write(lambda_1), Write(lambda_2))
        self.wait()
        self.play(*[mob.animating(run_time = 2).apply_matrix(operator, about_point = offset_r) for mob in [grid_a, unit_a, grid_l, unit_l]])
        self.wait()
        self.play(*[FadeOut(mob, remover = False) for mob in [grid_a, unit_a, grid_l, unit_l]], run_time = 0.5, rate_func = rush_into)
        self.play(*[FadeIn(mob.restore()) for mob in [grid_a, unit_a, grid_l, unit_l]], run_time = 0.5, rate_func = rush_from)
        self.wait()

        prod = MTex(r"S'=S\cdot \lambda_1\cdot \lambda_2", tex_to_color_map = {(r"S", r"S'"): TEAL, (r"\lambda_1", r"\lambda_2"): YELLOW})
        prod.shift(area[2].get_center() - prod[2].get_center() + 1*DOWN)
        operator_1, operator_2 = np.array([[2, -1], [0, 1]]), np.array([[1, 2], [0, 3]])
        self.play(Write(prod), *[mob.animating(run_time = 2, path_arc = 0).apply_matrix(operator_1, about_point = offset_r) for mob in [grid_a, unit_a, grid_l, unit_l]])
        self.wait()
        self.play(*[mob.animating(run_time = 2, path_arc = 0).apply_matrix(operator_2, about_point = offset_r) for mob in [grid_a, unit_a, grid_l, unit_l]])
        self.wait()

        result = MTex(r"\det(A)=\lambda_1\cdot \lambda_2", tex_to_color_map = {r"A": ORANGE, (r"\lambda_1", r"\lambda_2"): YELLOW})
        div_1, div_2, div_3 = Line(UR, UR+2*RIGHT, color = TEAL).shift(offset_r), Line(2*UR, 2*UR+2*RIGHT, color = TEAL).shift(offset_r), Line(RIGHT, 3*UR+RIGHT, color = TEAL).shift(offset_r)
        result.shift(prod[2].get_center() - result[6].get_center() + 1*DOWN)
        self.add_background(div_1, div_2, div_3, window).play(Write(result), *[ShowCreation(mob) for mob in [div_1, div_2, div_3]])
        self.wait()
        self.play(window.animate.shift(7.5*RIGHT), *[mob.animate.shift(-offset_l) for mob in [prop, A, area, prod, result]], run_time = 2)
        self.wait()
        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        