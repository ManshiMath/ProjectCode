from __future__ import annotations

from manimlib import *
import numpy as np

class Video_1(FrameScene):
    def construct(self):
        equation_a = MTex(r"a=\left(\frac{a-3^2}{3^2}\right)^3+\left(\frac{3^6+3^5a-a^3}{3^6+3^4a+3^2a^2}\right)^3+\left(\frac{3^5a+3^3a^2}{3^6+3^4a+3^2a^2}\right)^3")
        self.wait()
        self.play(Write(equation_a))
        self.wait()

        Ramanujan = ImageMobject("Ramanujan.png", height = 4).shift(4*RIGHT + 6.5*DOWN)
        self.play(equation_a.animate.shift(3*UP), Ramanujan.animate.shift(5.5*UP), run_time = 2)
        self.wait()

        start = Ramanujan.get_left() + 0.5*DOWN
        def talk(p1: np.ndarray, p2: np.ndarray, color = WHITE):
            shape = p2-p1
            arc = Arc(-PI/2, PI/2, color = color).scale(shape, min_scale_factor = None)
            arc.shift(p1 - arc.get_start())
            return arc
        equation_r = Tex(r"\frac{1}{\pi}=\frac{2\sqrt2}{99^2}\sum_{k=0}^\infty\frac{(4k)!(1103+26390k)}{(k!)^4396^{4k}}").scale(0.8).next_to(start, UL).shift(0.5*UP)
        line_r = Underline(equation_r, buff = 0.2)
        talk_r = VGroup(equation_r, line_r, talk(start, line_r.get_center()))
        self.play(GrowFromPoint(talk_r, start, path_arc = -PI/2))
        self.wait()

        self.play(*[FadeOut(mob, RIGHT) for mob in [Ramanujan, talk_r]], equation_a.animate.set_color(GREY))
        self.wait()

        color_f, color_g, color_h, color_q = RED, BLUE, YELLOW, GREEN
        def_f, def_g = MTex(r"f(x)=\cdots", color = color_f).shift(1.5*UP + 2*LEFT), MTex(r"g(x)=\cdots", color = color_g).shift(1.5*UP + 2*RIGHT)
        self.play(Write(def_f), Write(def_g, delay = 0.2), frames = 36)
        self.wait(1, 24)

        color_map = {r"f": color_f, r"g": color_g, r"h": color_h, r"q": color_q, r"kx": ORANGE}#, (r"f^2", r"f^3"): color_f, (r"g^2", r"g^3"): color_g}
        cube_sum = MTex(r"f^3+g^3 = (f+g)(f^2-fg+g^2)", tex_to_color_map = color_map, isolate = [r"(f^2-fg+g^2)"]).shift(0.5*UP)
        self.play(FadeIn(cube_sum, UP))
        self.wait()

        subpart = cube_sum.get_part_by_tex(r"(f^2-fg+g^2)")
        surr = SurroundingRectangle(subpart, color = color_h, buff = 0.1)
        replace = MTex(r"=h^3", color = color_h).next_to(surr, RIGHT)
        replace.shift((cube_sum[5].get_y() - replace[0].get_y())*UP)
        self.play(ShowCreation(surr))
        self.play(Write(replace))
        self.wait()

        cube_sum_2 = MTex(r"f^3+g^3 = (f+g)h^3", tex_to_color_map = color_map)
        cube_sum_2.shift(cube_sum[5].get_center() - cube_sum_2[5].get_center() + 1.2*DOWN)
        ijs = [(0, 2), (2, 3), (3, 5), (5, 6), (6, 11)]
        self.play(LaggedStart(*[TransformFromCopy(cube_sum[i:j], cube_sum_2[i:j]) for i, j in ijs], TransformFromCopy(replace[1:], cube_sum_2[11:], path_arc = PI/4), lag_ratio = 0.2, run_time = 2))
        self.wait()

        cube_sum_3 = MTex(r"\left(\frac{f}{h}\right)^3+\left(\frac{g}{h}\right)^3 = f+g", tex_to_color_map = color_map, isolate = [r"f+g"])
        cube_sum_3.shift(cube_sum[5].get_center() - cube_sum_3[-4].get_center() + 1.2*DOWN)
        brace_f, brace_g = VGroup(*[cube_sum_3[i] for i in [0, 2, 4, 5]]), VGroup(*[cube_sum_3[i] for i in [7, 9, 11, 12]])
        copy_f = brace_f.copy().shift(brace_g[1].get_center() - brace_f[1].get_center())
        brace_g.become(copy_f)
        self.play(cube_sum_2[0].animate.become(cube_sum_3[1]), follow(brace_f[:-1], cube_sum_2[0], FadeIn), cube_sum_2[1].animate.become(cube_sum_3[5]), 
                  cube_sum_2[2].animate.become(cube_sum_3[6]), 
                  cube_sum_2[3].animate.become(cube_sum_3[8]), follow(brace_g[:-1], cube_sum_2[3], FadeIn), cube_sum_2[4].animate.become(cube_sum_3[12]),)
        self.remove(cube_sum_2[11]).play(TransformFromCopy(cube_sum_2[11], cube_sum_3[3], path_arc = PI/4), TransformFromCopy(cube_sum_2[11], cube_sum_3[10], path_arc = PI/3), 
                                         FadeOut(cube_sum_2[12], 0.5*UP), *[cube_sum_2[7+i].animate.become(cube_sum_3[-3+i]) for i in range(3)], 
                                         follow(cube_sum_2[6], cube_sum_2[8], FadeOut), follow(cube_sum_2[10], cube_sum_2[8], FadeOut))
        self.remove(*cube_sum_2).add(cube_sum_3).wait()

        subpart_2 = cube_sum_3.get_part_by_tex(r"f+g")
        surr_2 = SurroundingRectangle(subpart_2, color = color_q, buff = 0.1)
        replace_2 = MTex(r"=q^3+kx", tex_to_color_map = color_map).next_to(surr_2, RIGHT)
        replace_2.shift((cube_sum_3[-4].get_y() - replace_2[0].get_y())*UP)
        self.play(ShowCreation(surr_2))
        self.play(Write(replace_2))
        self.wait()

        cube_sum_4 = MTex(r"kx = (-q)^3 + \left(\frac{f}{h}\right)^3+\left(\frac{g}{h}\right)^3", tex_to_color_map = color_map)
        cube_sum_4.shift(cube_sum_3[-4].get_center() - cube_sum_4[2].get_center() + 1.2*DOWN)
        brace_f, brace_g = VGroup(*[cube_sum_4[i] for i in [9, 11, 13, 14]]), VGroup(*[cube_sum_4[i] for i in [16, 18, 20, 21]])
        copy_f = brace_f.copy().shift(brace_g[1].get_center() - brace_f[1].get_center())
        brace_g.become(copy_f)
        self.play(Write(cube_sum_4))
        self.wait()

        substitution = MTex(r"x=\frac{a}{k}", color = ORANGE).next_to(cube_sum_4, RIGHT)
        self.play(Write(substitution), equation_a[0].animate.set_color(ORANGE), 
                  equation_a[3:10].animate.set_color(color_q), equation_a[14:24].animate.set_color(color_f), equation_a[40:48].animate.set_color(color_g), 
                  equation_a[25:36].animate.set_color(color_h), equation_a[49:60].animate.set_color(color_h), )
        self.wait()

        self.play(*[OverFadeOut(mob, 1.5*UP) for mob in [equation_a, cube_sum[:11], cube_sum_3[:-3], cube_sum_4, substitution]], 
                  *[mob.animate.shift(1.5*UP) for mob in [def_f, def_g, subpart, surr, replace, subpart_2, surr_2, replace_2]], run_time = 2)
        self.wait()

        equation_1 = MTex(r"f^2-fg+g^2 = h^3", tex_to_color_map = color_map).shift(3*LEFT + 2*UP)
        equation_2 = MTex(r"f+g = q^3+kx", tex_to_color_map = color_map).shift(3*RIGHT + 2*UP)
        self.play(subpart.animate.become(equation_1[:-4]), follow(surr, subpart, FadeOut), replace.animate.become(equation_1[-4:]))
        self.wait()
        self.play(subpart_2.animate.become(equation_2[:3]), follow(surr_2, subpart_2, FadeOut), replace_2.animate.become(equation_2[3:]), path_arc = PI/4)
        self.wait()

class Video_2(FrameScene):
    def construct(self):
        color_f, color_g, color_h, color_q = RED, BLUE, YELLOW, GREEN
        color_map = {r"f": color_f, r"g": color_g, r"h": color_h, r"q": color_q, r"kx": ORANGE}
        def_f, def_g = MTex(r"f(x)=\cdots", color = color_f).shift(3*UP + 2*LEFT), MTex(r"g(x)=\cdots", color = color_g).shift(3*UP + 2*RIGHT)
        equation_1 = MTex(r"f^2-fg+g^2 = h^3", tex_to_color_map = color_map).shift(3*LEFT + 2*UP)
        equation_2 = MTex(r"f+g = q^3+kx", tex_to_color_map = color_map).shift(3*RIGHT + 2*UP)
        self.add(def_f, def_g, equation_1, equation_2).wait()
        # self.check()

        omega = MTex(r"\omega = -\frac{1}{2}+\frac{\sqrt3}{2}i", color = TEAL).scale(0.8).shift(LEFT_SIDE/2 + 1.0*UP)
        offset_l = LEFT_SIDE/2 + 1.4*DOWN
        ratio = 0.8
        left, right, up, down = 2, 2, 2, 2
        lines_h = [Line((left+0.2)*ratio*LEFT + i*ratio*DOWN, (right+0.2)*ratio*RIGHT + i*ratio*DOWN, stroke_width = (1 if i%2 else 2) if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.2)*ratio*UP + i*ratio*RIGHT, (down+0.2)*ratio*DOWN + i*ratio*RIGHT, stroke_width = (1 if i%2 else 2) if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(offset_l)
        label_0 = MTex("0").scale(0.8).set_stroke(**stroke_dic).next_to(offset_l, DL, buff = 0.1)
        labels_real = [MTex(str(i)).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + 2*i*ratio*RIGHT, DOWN, buff = 0.1) for i in (-1, 1)]
        labels_imag = [MTex(str(i)+"i", tex_to_color_map = {r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + 2*i*ratio*DOWN, LEFT, buff = 0.1) for i in (-1, 1)] 
        labels = VGroup(label_0, *labels_real, *labels_imag)
        back = BackgroundRectangle(complex_plane)
        self.add_background(complex_plane, labels, back).play(Write(omega), FadeOut(back))
        arrow_1 = Vector(2*ratio*unit(TAU/3), color = TEAL).shift(offset_l)
        self.add_text(labels).play(GrowArrow(arrow_1))
        self.wait()

        arrow_2, arrow_3 = Vector(2*ratio*unit(-TAU/3), color = TEAL).shift(offset_l), Vector(2*ratio*unit(0), color = TEAL).shift(offset_l)
        self.play(TransformFromCopy(arrow_1, arrow_2, path_arc = -TAU/3))
        self.play(TransformFromCopy(arrow_2, arrow_3, path_arc = -TAU/3))
        self.wait()

        label_1 = MTex(r"\omega", color = TEAL).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + 2*ratio*unit(TAU/3), LEFT)
        label_2 = MTex(r"\omega^2", color = TEAL).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + 2*ratio*unit(-TAU/3), LEFT)
        label_3 = MTex(r"\omega^3=1", color = TEAL).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + 2*ratio*unit(0), UP)
        self.add_text(label_1, label_2, label_3).play(Write(label_1), Write(label_2), Write(label_3))
        self.wait()
        def fade_color(color: ManimColor):
            return interpolate_color(color, BLACK, 0.5)
        back_1, back_2 = arrow_1.copy().set_color(fade_color(TEAL)), arrow_2.copy().set_color(fade_color(TEAL))
        self.add_lower(back_1, back_2).play(Transform(arrow_1, arrow_2), Transform(arrow_2, arrow_1))
        self.play(Transform(arrow_1, arrow_2), Transform(arrow_2, arrow_1))
        self.remove(back_1, back_2).wait()

        expand = MTex(r"f^3+{g}^3 = (f+{g})(f+\omega {g})(f+\omega^2 {g})", isolate = [r"(f+\omega {g})", r"(f+\omega^2 {g})"], 
                      tex_to_color_map = {r"f": color_f, r"{g}": color_g, r"\omega": TEAL}).scale(0.8).shift(3*RIGHT + 0.6*UP)
        self.play(Write(expand))
        self.wait()

        calculate = MTex(r"=f^3+(1+\omega+\omega^2)f^2{g} + (\omega+\omega^2+\omega^3)f{g}^2+\omega^3{g}^3", isolate = [r"(1+\omega+\omega^2)", r"(\omega+\omega^2+\omega^3)"], 
                         tex_to_color_map = {r"f": color_f, r"{g}": color_g, r"\omega": TEAL}).set_opacity(0.5).scale(0.6).shift(3*RIGHT + 0.2*DOWN)
        self.play(FadeIn(calculate, 0.5*UP))
        part_1, part_2 = calculate.get_part_by_tex(r"(1+\omega+\omega^2)"), calculate.get_part_by_tex(r"(\omega+\omega^2+\omega^3)")
        line_1, line_2 = Line(part_1.get_left(), part_1.get_right(), color = GREY, stroke_width = 3), Line(part_2.get_left(), part_2.get_right(), color = GREY, stroke_width = 3)
        # back_1, back_2 = line_1.copy().set_stroke(width = 8, color = BLACK), line_2.copy().set_stroke(width = 8, color = BLACK)
        equal_1, equal_2 = MTex(r"=0", color = GREY).scale(0.6), MTex(r"=0", color = GREY).scale(0.6)
        equal_1[0].rotate(-PI/4).next_to(part_1, DR, buff = 0.1), equal_1[1].next_to(equal_1[0], DR, buff = 0.1)
        equal_2[0].rotate(-PI/4).next_to(part_2, DR, buff = 0.1), equal_2[1].next_to(equal_2[0], DR, buff = 0.1)
        self.play(ShowCreation(line_1), ShowCreation(line_2)) #ShowCreation(back_1), ShowCreation(back_2), 
        self.play(Write(equal_1), Write(equal_2))
        self.wait()
        back = BackgroundRectangle(VGroup(calculate, back_1, back_2, line_1, line_2, equal_1, equal_2))
        self.bring_to_back(calculate, back_1, back_2, line_1, line_2, equal_1, equal_2, back).play(ShowCreation(back))
        self.remove(calculate, back_1, back_2, line_1, line_2, equal_1, equal_2, back).wait()

        part_1, part_2 = expand.get_part_by_tex(r"(f+\omega {g})"), expand.get_part_by_tex(r"(f+\omega^2 {g})")
        underline_1, underline_2 = Underline(part_1, buff = 0.1, color = PURPLE_A, stroke_width = 3), Underline(part_2, buff = 0.1, color = PURPLE_A, stroke_width = 3)
        equal_1, equal_2 = MTex(r"=u^3", color = PURPLE_A).scale(0.8), MTex(r"=\bar{u}^3", color = PURPLE_A).scale(0.8)
        equal_1[0].rotate(-PI/2).next_to(part_1, DOWN, buff = 0.2), equal_1[1:].next_to(equal_1[0], DOWN, buff = 0.1)
        equal_2[0].rotate(-PI/2).next_to(part_2, DOWN, buff = 0.2), equal_2[1:].next_to(equal_2[0], DOWN, buff = 0.1)
        self.play(ShowCreation(underline_1, start = 0.5))
        self.play(Write(equal_1))
        self.wait()

        calculate = MTex(r"\overline{f+\omega {g}}=f+\omega^2 {g}", tex_to_color_map = {r"f": color_f, r"{g}": color_g, r"\omega": TEAL}).scale(0.8).shift(3*RIGHT + DOWN)
        self.play(FadeIn(calculate, 0.5*UP))
        self.wait()
        self.play(ShowCreation(underline_2, start = 0.5))
        self.play(Write(equal_2))
        self.wait()

        alter = MTex(r"=(f+g)(f^2-fg+g^2)", tex_to_color_map = color_map).scale(0.8)
        alter.shift(expand[5].get_center() - alter[0].get_center() + 0.6*UP)
        self.play(Write(alter), FadeOut(calculate))
        self.wait()

        calculate_1 = MTex(r"f^2-fg+g^2=(u\bar{u})^3", tex_to_color_map = {r"f": color_f, r"g": color_g, r"u\bar{u}": PURPLE_A}).scale(0.8).shift(3*RIGHT + 1.3*DOWN)
        self.play(FadeIn(calculate_1, 0.5*UP))
        self.wait()
        calculate_2 = MTex(r"h = u\bar{u}", tex_to_color_map = {r"u\bar{u}": PURPLE_A, r"h": color_h}).scale(0.8)
        calculate_2.shift(calculate_1[8].get_center() - calculate_2[1].get_center() + 0.7*DOWN)
        self.play(Write(calculate_2))
        self.wait()

        new_condition = MTex(r"f+\omega {g} = u^3,\ h=u\bar{u}", tex_to_color_map = {r"f": color_f, r"{g}": color_g, r"\omega": TEAL, (r"u", r"\bar{u}"): PURPLE_A, r"h": YELLOW}).shift(3*LEFT + 2*UP)
        self.play(Flip(equation_1, new_condition), *[FadeOut(mob) for mob in [calculate_1, calculate_2, alter]])
        self.wait()

        mul_1, mul_2 = MTex(r"\times(-\omega)", tex_to_color_map = {r"\omega": TEAL}).scale(0.8).next_to(part_1, UP), MTex(r"\times(-\omega^2)", tex_to_color_map = {r"\omega": TEAL}).scale(0.8).next_to(part_2, UP)
        self.play(Write(mul_1), Write(mul_2.match_y(mul_1)))
        calculate_1 = MTex(r"f+{g} = -\left(\omega u^3+\overline{\omega u^3}\right)", tex_to_color_map = {r"f": color_f, r"{g}": color_g, r"\omega": TEAL, r"u": PURPLE_A}).scale(0.8).shift(3*RIGHT + 1.5*DOWN)
        self.play(Write(calculate_1))
        self.wait()

        new_condition = MTex(r"-\left(\omega u^3+\overline{\omega u^3}\right)=q^3+kx", tex_to_color_map = {r"q": color_q, r"kx": ORANGE, r"\omega": TEAL, (r"u", r"\bar{u}"): PURPLE_A}).shift(3*RIGHT + 2*UP)
        def_u = MTex(r"u(x)=\cdots", color = PURPLE_A).shift(3*UP)
        self.play(Flip(equation_2, new_condition), *[FadeOut(mob) for mob in [calculate_1, expand, mul_1, mul_2, underline_1, underline_2, equal_1, equal_2]], 
                  def_f.animate.fade(0.5).shift(LEFT), def_g.animate.fade(0.5).shift(RIGHT), GrowFromCenter(def_u))
        self.wait()

        color_map_x = {r"x": ORANGE, r"\omega": TEAL, r"u": PURPLE_A}
        calculate_1 = MTex(r"u(x)=\omega-x", tex_to_color_map = color_map_x).scale(0.8).shift(2.5*RIGHT + UP)
        self.play(Write(calculate_1), Transform(def_u, MTex(r"u(x)=\omega-x", color = PURPLE_A).shift(3*UP)))
        calculate_2 = MTex(r"u^3 = 1-3\omega^2x+3\omega x^2-x^3", tex_to_color_map = color_map_x).scale(0.8)
        calculate_2.shift(calculate_1[4].get_center() - calculate_2[2].get_center() + 1.0*DOWN)
        calculate_3 = MTex(r"-\left(\omega u^3+\overline{\omega u^3}\right) = 1+6x+3x^2-x^3", tex_to_color_map = color_map_x).scale(0.8)
        calculate_3.shift(calculate_2[2].get_center() - calculate_3[11].get_center() + 1.0*DOWN)
        self.play(FadeIn(calculate_2, 0.5*UP), FadeIn(calculate_3, 0.5*UP))
        self.wait()

        result = MTex(r"=(1-x)^3+9x", tex_to_color_map = {r"1-x": color_q, r"9x": ORANGE}).scale(0.8)
        result.shift(calculate_3[11].get_center() - result[0].get_center() + 0.6*DOWN)
        self.play(Write(result))
        self.wait()

        # def path_func(starts: np.ndarray, ends: np.ndarray, alpha: float):
        #     centers, urs = np.array([ends[:, 0], starts[:, 1], ends[:, 2]]).T, np.array([starts[:, 0] - ends[:, 0], ends[:, 1] - starts[:, 1], ends[:, 2]]).T
        #     print(starts, ends, centers, urs)
        #     return centers + np.array([np.cos(alpha*PI/2), np.sin(alpha*PI/2), 0]) * urs
        # def single_func(start: np.ndarray, end: np.ndarray, alpha: float):
        #     center, ur = np.array([end[0], start[1], 0]), np.array([start[0] - end[0], end[1] - start[1], 0])
        #     return center + np.array([np.cos(alpha*PI/2), np.sin(alpha*PI/2), 0]) * ur
        # **0.5 = lambda starts, ends, alpha: np.array([single_func(start, end, alpha) for start, end in zip(starts, ends)])
        def path_func(start: np.ndarray, end: np.ndarray, alpha: float):
            factor = unit(alpha*PI/2)**0.5
            factor_starts, factor_ends = np.array([factor[0], 1 - factor[1], 0]), np.array([1 - factor[0], factor[1], 0])
            return start*factor_starts + end*factor_ends
        new_condition = MTex(r"f+g=(1-x)^3+9x", tex_to_color_map = {r"f": color_f, r"g": color_g, r"1-x": color_q, r"9x": ORANGE}).shift(3*RIGHT + 2*UP)
        self.play(Flip(equation_2, new_condition), *[OverFadeOut(mob, 1.5*UP + LEFT, run_time = 2, path_func = path_func) for mob in [calculate_3, result]], OverFadeOut(calculate_1, 0.5*UP + LEFT, run_time = 2, path_func = path_func), 
                  calculate_2.animating(run_time = 2, path_func = path_func).shift(UL))
        self.wait()


        new_condition = MTex(r"f+\omega {g} = u^3,\ h=1+x+x^2", tex_to_color_map = {r"f": color_f, r"{g}": color_g, r"\omega": TEAL, r"u": PURPLE_A, r"h": YELLOW, r"1+x+x^2": YELLOW}).shift(3.25*LEFT + 2*UP)
        equation_1.set_submobjects([*equation_1[:-3], equation_1[-3], equation_1[-3].copy(), equation_1[-2], equation_1[-2].copy(), equation_1[-1], equation_1[-1].copy()])
        # self.play(Transform(equation_1[:-3], new_condition[:-6], remover = True), FadeTransform(equation_1[-3:], new_condition[-6:], stretch = False,   remover = True))
        # self.add(equation_1.become(new_condition)).wait()
        self.play(Transform(equation_1, new_condition), equation_2.animate.shift(0.25*RIGHT))
        self.wait()

        equations = MTex(r"\begin{cases}f+\omega{g}=\left(\omega-x\right)^3\\f+\omega^2{g}=\left(\omega^2-x\right)^3\end{cases}", tex_to_color_map = {r"f": color_f, r"{g}": color_g, r"\omega": TEAL, r"x": ORANGE}).scale(0.8).shift(3*RIGHT + 0.2*DOWN)
        equations[1:12].shift((equations[17].get_x() - equations[5].get_x())*RIGHT)
        self.play(FadeIn(equations, LEFT))
        self.wait()
        solution_f = MTex(r"f=\frac{\omega^2 u^3-\omega \bar{u}^3}{\omega^2 - \omega}=1+3x-x^3", tex_to_color_map = {r"f": color_f, r"\omega": TEAL, (r"u", r"\bar{u}"): PURPLE_A, r"x": ORANGE}).scale(0.8).shift(3*RIGHT + 1.5*DOWN)
        solution_g = MTex(r"g=\frac{\bar{u}^3-u^3}{\omega^2 - \omega}=3x+3x^2", tex_to_color_map = {r"g": color_g, r"\omega": TEAL, (r"u", r"\bar{u}"): PURPLE_A, r"x": ORANGE}).scale(0.8).shift(3*RIGHT + 2.5*DOWN)
        solution_g.set_submobjects([*solution_g[:2], VMobject(), *solution_g[2:6], VMobject(), VMobject(), *solution_g[6:-6], VMobject(), *solution_g[-6:]])
        solution_g.shift((solution_f[-8].get_x() - solution_g[-8].get_x())*RIGHT)
        def_f.set_submobjects([*def_f[:-3], def_f[-3], def_f[-3].copy(), def_f[-2], def_f[-2].copy(), def_f[-2].copy(), def_f[-1], def_f[-1].copy()])
        def_g.set_submobjects([*def_g[:-3], def_g[-3], def_g[-3].copy(), def_g[-2], def_g[-2].copy(), def_g[-1], def_g[-1].copy()])
        self.play(Write(solution_f), Write(solution_g), 
                  Transform(def_f, MTex(r"f(x)=1+3x-x^3", color = color_f).shift(3*UP + 4*LEFT), delay = 1), 
                  Transform(def_g, MTex(r"g(x)=3x+3x^2", color = color_g).shift(3*UP + 4*RIGHT), delay = 1))
        self.wait()

        back = BackgroundRectangle(VGroup(complex_plane, labels, label_1, label_2, label_3, arrow_1, arrow_2, arrow_3))
        upper = FloatWindow(width = 15).shift(5.35*UP)
        self.add_top(back).play(*[FadeOut(mob) for mob in [equations, solution_f, solution_g, equation_1[:8], omega, calculate_2]], 
                                                      FadeOut(def_u, scale = 0), def_f.animate.shift(1.5*RIGHT), def_g.animate.shift(1.5*LEFT),
                  FadeIn(back), self.camera.frame.animate.shift(0.5*DOWN))
        self.remove(back, complex_plane, labels, label_1, label_2, label_3, arrow_1, arrow_2, arrow_3)
        def_h = equation_1[8:]
        for mob in [def_f, def_g, def_h, equation_2, upper, self.camera.frame]:
            mob.shift(0.5*UP)

        old_equation = MTex(r"kx = (-q)^3 + \left(\frac{f}{h}\right)^3+\left(\frac{g}{h}\right)^3", tex_to_color_map = color_map).shift(3*LEFT + 0.5*DOWN)
        brace_f, brace_g = VGroup(*[old_equation[i] for i in [9, 11, 13, 14]]), VGroup(*[old_equation[i] for i in [16, 18, 20, 21]])
        copy_f = brace_f.copy().shift(brace_g[1].get_center() - brace_f[1].get_center())
        brace_g.become(copy_f)
        self.add_background(upper).play(FadeIn(old_equation), FadeIn(upper))
        self.wait()

        expand = MTex(r"9x=(x-1)^3+\left(\frac{1+3x-x^3}{1+x+x^2}\right)^3+\left(\frac{3x+3x^2}{1+x+x^2}\right)^3", 
                            tex_to_color_map = {r"9x": ORANGE, r"x-1": color_q, r"1+3x-x^3": color_f, r"1+x+x^2": color_h, r"3x+3x^2": color_g}).scale(0.8).shift(1*RIGHT + UP)
        self.play(Write(expand))
        self.wait()

        substitution = MTex(r"x=\frac{a}{9}", tex_to_color_map = {(r"x", r"9"): ORANGE, r"a": TEAL}).shift(3*RIGHT + 0.5*DOWN)
        self.play(Write(substitution))
        self.wait()

        equation_a = MTex(r"a=\left(\frac{a-3^2}{3^2}\right)^3+\left(\frac{3^6+3^5a-a^3}{3^6+3^4a+3^2a^2}\right)^3+\left(\frac{3^5a+3^3a^2}{3^6+3^4a+3^2a^2}\right)^3", 
                          tex_to_color_map = {r"3^2": interpolate_color(ORANGE, WHITE, 0.5), r"a-3^2": GREEN_A, r"3^6+3^5a-a^3": RED_A, r"3^6+3^4a+3^2a^2": YELLOW_A, r"3^5a+3^3a^2": BLUE_A, r"a": TEAL}).scale(0.8).shift(1*RIGHT + 2*DOWN)
        self.play(Write(equation_a))
        self.wait()

        self.play(*[FadeOut(mob, 3*UP) for mob in [expand, substitution, old_equation, def_f, def_g, def_h, equation_2, upper]], 
                  equation_a.animate.shift(3*UP), run_time = 2)
        attention = MTexText("注意到：").shift(2*UP + 5*LEFT)
        self.play(Write(attention))
        qed = MTexText("证毕！").shift(0.5*DOWN + 5*RIGHT)
        self.play(Write(qed))
        self.wait()

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        