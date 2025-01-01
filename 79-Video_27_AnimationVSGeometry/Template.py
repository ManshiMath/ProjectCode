from __future__ import annotations

from manimlib import *
import numpy as np

class Rigid(Animation):
    def __init__(
        self,
        mobject: Mobject,
        target: Mobject,
        **kwargs
    ):
        mob_diff = mobject.get_end() - mobject.get_start()
        tar_diff = target.get_end() - target.get_start()
        angle_start, angle_end = np.arctan2(mob_diff[1], mob_diff[0]), np.arctan2(tar_diff[1], tar_diff[0])
        self.angle = ((angle_end - angle_start)+PI)%TAU -PI
        self.shift = target.get_start() - mobject.get_start()
        self.scale = get_norm(tar_diff)/get_norm(mob_diff)
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for sm1, sm2 in self.get_all_families_zipped():
            sm1.set_points(sm2.get_points())
        self.mobject.rotate(alpha * self.angle, about_point = self.mobject.get_start()).shift(alpha * self.shift).scale(interpolate(1, self.scale, alpha))

class Video_1(FrameScene):
    def construct(self):
        phi = (1+np.sqrt(5))/2
        golden_rect = Rectangle(height = 4, width = 4*phi, stroke_width = 8)
        self.play(ShowCreation(golden_rect))
        self.wait()

        line = Line(2*UP, 2*DOWN).shift(2*phi*LEFT)
        tracker = TracedPath(line.get_end)
        self.add(line, tracker).play(Rotate(line, PI/2, about_point = 2*UP + 2*phi*LEFT))
        self.remove(line), tracker.clear_updaters()
        smaller = golden_rect.copy()
        self.play(Transform(smaller, Rectangle(height = 4, width = 4/phi, stroke_width = 8).match_x(golden_rect, RIGHT)))
        self.wait()

        fill = smaller.copy().set_stroke(width = 0).set_fill(color = YELLOW).set_opacity(0)
        stroke_smaller = Polygon(1.92*UP + 2*phi*RIGHT + 0.08*LEFT, 1.92*DOWN + 2*phi*RIGHT + 0.08*LEFT, 1.92*DOWN + 2*phi*LEFT + 4.08*RIGHT, 1.92*UP + 2*phi*LEFT + 4.08*RIGHT, color = YELLOW_D, stroke_width = 8)
        self.play(ShowCreation(stroke_smaller), rate_func = less_smooth)
        self.add_background(fill).play(fill.animate.scale(0.8).set_opacity(0.5), rate_func = less_smooth)
        alpha = ValueTracker(0.0)
        def fill_updater(mob: VMobject):
            value = alpha.get_value()
            mob.restore().rotate(PI/2*value).scale(interpolate(0.8, phi, value)/0.8).shift(mob.get_x()*value*LEFT)
        fill.save_state().add_updater(fill_updater)
        self.play(alpha.animate.set_value(1.0), rate_func = less_smooth)
        fill.clear_updaters()
        stroke_bigger = Polygon(2.08*UP + 2*phi*RIGHT + 0.08*RIGHT, 2.08*UP + 2*phi*LEFT + 0.08*LEFT, 2.08*DOWN + 2*phi*LEFT + 0.08*LEFT, 2.08*DOWN + 2*phi*RIGHT + 0.08*RIGHT, color = YELLOW_D, stroke_width = 8)
        self.play(FadeOut(fill, rate_func = less_smooth), TransformFromCopy(golden_rect, stroke_bigger))
        self.wait()

        text_1, tex_1_2, tex_1_3 = MTex(r"1").next_to(golden_rect, LEFT), MTex(r"1").next_to(line, DOWN), MTex(r"1").next_to(golden_rect, RIGHT)
        tex_phi, tex_phi_2 = MTex(r"\phi", color = GOLD).next_to(golden_rect, UP), MTex(r"\phi-1", tex_to_color_map = {r"\phi": GOLD}).next_to(line, DOWN).shift(2*phi*RIGHT)
        self.play(Write(text_1), Write(tex_phi), Write(tex_1_3))
        self.wait(1)
        self.play(Write(tex_1_2))
        self.wait(1)
        self.play(Write(tex_phi_2))
        self.wait()

        self.play(WiggleOutThenIn(stroke_smaller), WiggleOutThenIn(stroke_bigger))
        self.wait()
        equation = MTex(r"\frac{\phi}{1}=\frac{1}{\phi-1}", tex_to_color_map = {r"\phi": GOLD}).scale(0.9).shift(3*RIGHT + UP)
        self.play(*[mob.animate.shift(2.5*LEFT) for mob in [golden_rect, line, tracker, smaller, stroke_smaller, stroke_bigger, text_1, tex_1_2, tex_1_3, tex_phi, tex_phi_2]])
        self.wait(1)
        self.play(FadeIn(equation[1]), TransformFromCopy(tex_phi, equation[0]), TransformFromCopy(text_1, equation[2]))
        self.play(FadeIn(equation[5]), TransformFromCopy(tex_1_3, equation[4]), TransformFromCopy(tex_phi_2, equation[6:]))
        self.play(Write(equation[3]))
        self.wait()

        solution = MTex(r"\phi=\frac{\sqrt5+1}{2}\approx 1.618\cdots", tex_to_color_map = {r"\phi": GOLD, r"\frac{\sqrt5+1}{2}": YELLOW_D, r"1.618\cdots": YELLOW}).scale(0.9)
        solution.shift(equation[3].get_center() - solution[1].get_center() + 1.5*DOWN)
        self.play(Write(solution))
        self.wait()

        offset = 2*RIGHT
        triangle_0 = Polygon(UP + 0.5*LEFT, DOWN+0.5*LEFT, DOWN+0.5*RIGHT).shift(offset + 2*UP)
        self.play(*[OverFadeOut(mob, 8*LEFT) for mob in [golden_rect, line, tracker, smaller, stroke_smaller, stroke_bigger, text_1, tex_1_2, tex_1_3, tex_phi, tex_phi_2]], 
                  *[mob.animate.shift(8*LEFT) for mob in [equation, solution]], OverFadeIn(triangle_0, 8*LEFT), run_time = 2)
        self.wait()

        label_0, label_1, label_2, label_5 = Elbow().shift(DOWN+0.5*LEFT).shift(offset + 2*UP), MTex(r"1").scale(0.8).next_to(triangle_0, DOWN), MTex(r"2").scale(0.8).next_to(triangle_0, LEFT), MTex(r"\sqrt5").scale(0.8).next_to(triangle_0.get_center(), UR, buff = 0.1)
        self.add_text(label_1, label_2, label_5).play(*[Write(mob) for mob in [label_0, label_1, label_2, label_5]])
        self.wait()

        label_4 = label_5.copy().next_to(triangle_0, DOWN).match_y(label_1).shift(phi*RIGHT)
        line = Line(DOWN+0.5*RIGHT, UP + 0.5*LEFT, color = RED).shift(offset + 2*UP)
        self.play(ShowCreation(line))
        tracker = TracedPath(line.get_end)
        self.add(tracker).play(Rotate(line, np.arctan(2)-PI, about_point = line.get_start()), TransformFromCopy(label_5, label_4, path_arc = PI-np.arctan(2)))
        tracker.clear_updaters()
        label_a, label_b, label_c = MTex(r"A", color = GREY).scale(0.8).next_to(triangle_0, DL, buff = 0.1), MTex(r"B", color = GREY).scale(0.8).next_to(triangle_0, UL, buff = 0.1), MTex(r"C", color = GREY).scale(0.8).next_to(line, DR, buff = 0.1)
        self.play(Transform(line, Line(DOWN + 0.5*LEFT, DOWN + 0.5*LEFT + 2*phi*RIGHT, color = YELLOW).shift(offset + 2*UP)), *[FadeIn(mob) for mob in [label_a, label_b, label_c]])
        self.wait()

        line_ab = Line(UP + 0.5*LEFT, DOWN+0.5*LEFT, color = YELLOW_E).shift(offset + 2*UP)
        tex_ratio = MTex(r"\frac{AC}{AB}=\phi", tex_to_color_map = {r"\phi": GOLD}).next_to(label_2, LEFT).scale(0.8)
        self.play(Write(tex_ratio), FadeIn(line_ab))
        self.wait()

        points_1, points_2 = [ORIGIN, 2*RIGHT, 2*phi*unit(TAU/5)], [ORIGIN, 2*phi*RIGHT, 2*unit(TAU/10)]
        offset_l, offset_r = 0.5*LEFT + 2.5*DOWN, 2.5*RIGHT + 2*DOWN
        lines_1, lines_2 = [line_ab.copy().reverse_points(), line.copy(), ], [line_ab.copy().reverse_points(), line.copy(), ]
        self.play(Rigid(lines_1[0], Line(points_1[1], points_1[0]).shift(offset_l)), Rigid(lines_1[1], Line(points_1[1], points_1[2]).shift(offset_l)))
        self.play(Rigid(lines_2[0], Line(points_2[0], points_2[2]).shift(offset_r)), Rigid(lines_2[1], Line(points_2[0], points_2[1]).shift(offset_r)))
        lines_1.append(lines_1[1].copy()), lines_2.append(lines_2[0].copy())
        self.play(Rotate(lines_1[2], about_point = lines_1[2].get_end(), angle = -TAU/10), Rotate(lines_2[2], about_point = lines_2[2].get_end(), angle = 3*TAU/10))
        self.wait()

        angles_1 = [MTex(r"36^\circ").scale(0.5).set_stroke(**stroke_dic).move_to(points_1[2]+offset_l+DOWN), 
                    MTex(r"72^\circ").scale(0.5).set_stroke(**stroke_dic).move_to(points_1[0]+offset_l+0.5*unit(TAU/10)), 
                    MTex(r"72^\circ").scale(0.5).set_stroke(**stroke_dic).move_to(points_1[1]+offset_l+0.5*unit(PI-TAU/10)), ]
        angles_2 = [MTex(r"108^\circ").scale(0.5).set_stroke(**stroke_dic).move_to(points_2[2]+offset_r+0.4*DOWN), 
                    MTex(r"36^\circ").scale(0.5).set_stroke(**stroke_dic).move_to(points_2[0]+offset_r+0.8*unit(TAU/20)), 
                    MTex(r"36^\circ").scale(0.5).set_stroke(**stroke_dic).move_to(points_2[1]+offset_r+0.8*unit(PI-TAU/20)), ]
        self.play(*[Write(mob) for mob in angles_1 + angles_2])
        self.wait()

        points, jumps = [2*phi*unit(PI/2+TAU/5*i) for i in range(5)], [2*phi*unit(PI/2+2*TAU/5*i) for i in range(5)]
        offset = 3*RIGHT
        pentagon = VGroup(Polygon(*points), Polygon(*jumps)).shift(offset)
        self.play(*[mob.animating(rate_func = bezier([0, 0, 1, 1, 1, 1, 1, 1])).shift(2*UP) for mob in [equation, solution]], *[mob.animating(rate_func = bezier([0, 0, 0, 0, 1, 1, 1, 1])).shift(6*LEFT) for mob in lines_1 + lines_2 + angles_1 + angles_2], 
                  *[OverFadeOut(mob, 4*LEFT) for mob in [triangle_0, label_0, label_1, label_2, label_4, label_5, line, line_ab, tracker, label_a, label_b, label_c]], 
                  OverFadeOut(tex_ratio, 2*UP, rate_func = bezier([0, 0, 1, 1, 1, 1, 1, 1])), OverFadeIn(pentagon, 6*LEFT), run_time = 2)
        self.wait()

        line_1, line_phi = Line(points[0], points[1], color = BLUE, stroke_width = 8).shift(offset), Line(points[1], points[4], color = GREEN, stroke_width = 8).shift(offset + 0.02*DOWN)
        tex_1, tex_phi = MTex(r"1", color = BLUE).next_to(line_1.get_center(), UL).set_stroke(**stroke_dic), MTex(r"x", color = GREEN).next_to(line_phi, DOWN).set_stroke(**stroke_dic)
        self.add_text(tex_1, tex_phi).play(ShowCreation(line_1), ShowCreation(line_phi), Write(tex_1), Write(tex_phi))
        self.wait()

        line_2 = line_1.copy().rotate(-PI/5, about_point = points[1] + offset).shift(0.04*UP)
        tex_2 = tex_1.copy().next_to(line_2, UP)
        self.add_text(tex_2).play(TransformFromCopy(line_1, line_2, path_arc = PI/5), TransformFromCopy(tex_1, tex_2, path_arc = PI/5), line_phi.animate.shift(0.02*DOWN))
        self.wait()

        middle = line_2.get_start() + 0.04*DOWN
        line_3 = Line(middle + 0.04*UP, points[4] + 0.04*UP + offset, stroke_width = 8, color = PURPLE_B)
        tex_3 = MTex(r"x-1", color = PURPLE).next_to(line_3, UP).set_stroke(**stroke_dic)
        line_4 = Line(points[0], points[4], color = BLUE, stroke_width = 8).shift(offset)
        tex_4 = MTex(r"1", color = BLUE).next_to(line_4.get_center(), UR).set_stroke(**stroke_dic)
        self.add_text(tex_3, tex_4).play(ShowCreation(line_3), Write(tex_3), FadeIn(line_4), FadeIn(tex_4), line_2.animate.set_stroke(color = BLUE_E), tex_2.animate.set_fill(color = BLUE_E))
        self.wait()
        
        fill_small = Polygon(points[0] + offset, points[4] + offset, middle, color = RED, stroke_width = 0, fill_opacity = 0.2)
        copy_small = fill_small.copy().set_color(GOLD).set_opacity(0.5)
        self.add_background(copy_small, fill_small).play(FadeIn(copy_small), FadeIn(fill_small))
        self.wait()

        center = (points[0] + offset + points[4] + offset + 2*middle)/4
        self.play(fill_small.animate.scale(0.8, about_point = center).set_fill(opacity = 0.5))
        diff = (points[1] + points[4] + 2*points[0])/4 + offset - center
        alpha = ValueTracker(0.0)
        def fill_updater(mob: VMobject):
            value = alpha.get_value()
            mob.restore().rotate(-4*PI/5*value, about_point = center).scale(interpolate(0.8, phi, value)/0.8).shift(diff*value).set_fill(opacity = interpolate(0.5, 0.2, value))
        fill_small.save_state().add_updater(fill_updater)
        self.play(alpha.animate.set_value(1.0))
        fill_small.clear_updaters()
        self.wait()

        equation_2 = MTex(r"\frac{x}{1}=\frac{1}{x-1}", tex_to_color_map = {r"x": GREEN, r"1": BLUE, r"x-1": PURPLE_B}).scale(0.9).shift(LEFT + 3*UP)
        self.play(FadeIn(equation_2[1]), TransformFromCopy(tex_phi, equation_2[0]), TransformFromCopy(text_1, equation_2[2]))
        self.play(FadeIn(equation_2[5]), TransformFromCopy(tex_4, equation_2[4]), TransformFromCopy(tex_3, equation_2[6:]))
        self.play(Write(equation_2[3]))
        self.wait()

        self.play(Transform(tex_phi, MTex(r"\phi", color = GOLD).next_to(line_phi, DOWN).set_stroke(**stroke_dic)), line_phi.animate.set_color(YELLOW), 
                  Transform(tex_3, MTex(r"\phi-1", color = PURPLE, tex_to_color_map = {r"\phi": GOLD}).next_to(line_3, UP).set_stroke(**stroke_dic)))
        self.wait()

        self.play(*[FadeOut(mob) for mob in[line_1, line_phi, tex_1, tex_phi, line_2, tex_2, line_3, tex_3, line_4, tex_4, fill_small, fill_small, copy_small, equation_2]])
        self.wait()

        small_points = [2/phi*unit(-PI/2+TAU/5*i) for i in range(5)]
        line_1 = Line(small_points[1], small_points[0], color = RED, stroke_width = 8).shift(offset)
        tex_1 = MTex(r"1", color = RED).next_to(line_1.get_center(), UL, buff = 0.1).set_stroke(**stroke_dic)
        self.add_text(tex_1).play(ShowCreation(line_1), Write(tex_1))
        line_2 = Line(small_points[0], points[3], color = ORANGE, stroke_width = 8).shift(offset)
        tex_2 = MTex(r"\phi", color = ORANGE).next_to(line_2.get_center(), DL, buff = 0.1).set_stroke(**stroke_dic)
        self.add_text(tex_2).play(ShowCreation(line_2), Write(tex_2))
        line_3 = Line(points[3], points[4], color = YELLOW, stroke_width = 8).shift(offset)
        tex_3 = MTex(r"\phi^2", color = YELLOW).next_to(line_3.get_center(), DR).set_stroke(**stroke_dic)
        self.add_text(tex_3).play(ShowCreation(line_3), Write(tex_3))
        line_4 = Line(points[4], points[1], color = LIME, stroke_width = 8).shift(offset)
        tex_4 = MTex(r"\phi^3", color = LIME).next_to(line_4, UP).set_stroke(**stroke_dic)
        self.add_text(tex_3).play(ShowCreation(line_4), Write(tex_4))
        self.wait()

class Patch1_2(FrameScene):
    def construct(self):
        phi = (1+np.sqrt(5))/2
        offset = 2.5*LEFT
        golden_rect = Rectangle(height = 4, width = 4*phi, stroke_width = 8).shift(offset)
        line = Line(2*UP, 2*UP + 4*RIGHT).shift(2*phi*LEFT).shift(offset)
        tracker = Arc(-PI/2, PI/2, radius = 4, stroke_width = 2).shift(2*UP + 2*phi*LEFT + offset)
        smaller = Rectangle(height = 4, width = 4/phi, stroke_width = 8).match_x(golden_rect, RIGHT)
        
        stroke_smaller = Polygon(1.92*UP + 2*phi*RIGHT + 0.08*LEFT, 1.92*DOWN + 2*phi*RIGHT + 0.08*LEFT, 1.92*DOWN + 2*phi*LEFT + 4.08*RIGHT, 1.92*UP + 2*phi*LEFT + 4.08*RIGHT, color = YELLOW_D, stroke_width = 8).shift(offset)
        stroke_bigger = Polygon(2.08*UP + 2*phi*RIGHT + 0.08*RIGHT, 2.08*UP + 2*phi*LEFT + 0.08*LEFT, 2.08*DOWN + 2*phi*LEFT + 0.08*LEFT, 2.08*DOWN + 2*phi*RIGHT + 0.08*RIGHT, color = YELLOW_D, stroke_width = 8).shift(offset)
        self.add(golden_rect, line, tracker, smaller, stroke_smaller, stroke_bigger)
        
        text_1, tex_1_2, tex_1_3 = MTex(r"1").next_to(golden_rect, LEFT), MTex(r"1").next_to(line, DOWN), MTex(r"1").next_to(golden_rect, RIGHT)
        tex_phi, tex_phi_2 = MTex(r"\phi", color = GOLD).next_to(golden_rect, UP), MTex(r"\phi-1", tex_to_color_map = {r"\phi": GOLD}).next_to(line, DOWN).shift(2*phi*RIGHT)
        equation = MTex(r"\frac{\phi}{1}=\frac{1}{\phi-1}", tex_to_color_map = {r"\phi": GOLD}).shift(4*RIGHT + 2.5*UP)
        self.add(text_1, tex_1_2, tex_1_3, tex_phi, tex_phi_2, equation).wait()

        equation_2 = MTex(r"\phi=1+\frac{1}{\phi}=", tex_to_color_map = {r"\phi": GOLD})
        equation_2.shift(equation[3].get_center() - equation_2[1].get_center() + 2*DOWN)
        self.play(Write(equation_2[:-1]))
        self.wait()

        copy_2 = equation_2[1:-1].copy()
        copy_2.generate_target().shift(equation_2[-1].get_center() - copy_2[0].get_center())
        self.play(MoveToTarget(copy_2), self.camera.frame.animate.shift(RIGHT))
        self.wait()

        equation_3 = MTex(r"=1+\frac{1}{1+\frac{1}{\phi}}=", tex_to_color_map = {r"\phi": GOLD})
        equation_3.shift(equation_2[-1].get_center() - equation_3[0].get_center())
        self.play(IndicateAround(copy_2[-1], rect_kwargs = {},), IndicateAround(equation_2[2:-1], rect_kwargs = {}))
        self.wait()
        self.play(ReplacementTransform(copy_2[:-1], equation_3[:5]), OverFadeOut(copy_2[-1]), TransformFromCopy(equation_2[2:-1], equation_3[5:-1], path_arc = -PI/4), self.camera.frame.animate.shift(2*RIGHT))
        self.wait()

        copy_3 = equation_3[:-1].copy()
        copy_3.generate_target().shift(equation_3[-1].get_center() - copy_3[0].get_center())
        self.play(MoveToTarget(copy_3), self.camera.frame.animate.shift(2*RIGHT))
        self.wait()
        equation_4 = MTex(r"=1+\frac{1}{1+\frac{1}{1+\frac{1}{\phi}}}=", tex_to_color_map = {r"\phi": GOLD})
        equation_4.shift(equation_3[-1].get_center() - equation_4[0].get_center())
        self.play(ReplacementTransform(copy_3[:-1], equation_4[:9]), OverFadeOut(copy_3[-1]), TransformFromCopy(equation_2[2:-1], equation_4[9:-1], path_arc = -PI/4), self.camera.frame.animate.shift(2*RIGHT))
        self.wait()

        equation_5 = MTex(r"=1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{\phi}}}}=", tex_to_color_map = {r"\phi": GOLD})
        equation_5.shift(equation_4[-1].get_center() - equation_5[0].get_center())
        self.play(TransformFromCopy(equation_4[:-2], equation_5[:-6]), FadeTransform(equation_4[-2].copy(), equation_5[-6:-1], stretch = False), self.camera.frame.animate.shift(3*RIGHT))
        self.wait()

        equation_6 = MTex(r"=1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{\phi}}}}}=", tex_to_color_map = {r"\phi": GOLD})
        equation_6.shift(equation_5[-1].get_center() - equation_6[0].get_center())
        backup = MTex(r"\phi=1+\frac{1}{\phi}=", tex_to_color_map = {r"\phi": GOLD}).fix_in_frame().shift(3*UP)
        self.play(FadeIn(backup), TransformFromCopy(equation_5[:-2], equation_6[:-6]), FadeTransform(equation_5[-2].copy(), equation_6[-6:-1], stretch = False), self.camera.frame.animate.shift(4*RIGHT))
        self.wait(1)

        equation_7 = MTex(r"=1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{\phi}}}}}}=", tex_to_color_map = {r"\phi": GOLD})
        equation_7.shift(equation_6[-1].get_center() - equation_7[0].get_center())
        self.play(TransformFromCopy(equation_6[:-2], equation_7[:-6]), FadeTransform(equation_6[-2].copy(), equation_7[-6:-1], stretch = False), self.camera.frame.animate.shift(5*RIGHT))
        self.wait(1)
        equation_8 = MTex(r"=1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{1+\frac{1}{\cdots}}}}}}}=", tex_to_color_map = {r"\phi": GOLD})
        equation_8.shift(equation_7[-1].get_center() - equation_8[0].get_center())
        self.play(TransformFromCopy(equation_7[:-2], equation_8[:-8]), FadeTransform(equation_7[-2].copy(), equation_8[-8:-1], stretch = False), self.camera.frame.animate.shift(5*RIGHT))
        self.wait(1)

        self.remove(equation).play(self.camera.frame.animate.shift(15*LEFT + DOWN), run_time = 3)
        self.wait()

        cutoff_1 = MTex(r"1+\frac1{1}=2", tex_to_color_map = {r"{1}": GOLD, (r"2"): GREEN}).scale(0.8).set_y(-3).match_x(equation_2)
        self.play(FadeIn(cutoff_1, 0.5*DOWN))#, self.camera.frame.animate.shift(RIGHT))
        self.wait(1)
        cutoff_2 = MTex(r"1+\frac1{1+\frac1{1}}=\frac{3}{2}", tex_to_color_map = {r"{1}": GOLD, (r"2", r"3"):BLUE}).scale(0.8).set_y(-1.5).match_x(equation_3)
        self.play(FadeIn(cutoff_2, 0.5*UP), self.camera.frame.animate.shift(RIGHT))
        self.wait(1)
        cutoff_3 = MTex(r"1+\frac1{1+\frac1{1+\frac1{1}}}=\frac{5}{3}", tex_to_color_map = {r"{1}": GOLD, (r"3", r"5"):GREEN}).scale(0.8).set_y(-3).match_x(equation_4)
        self.play(FadeIn(cutoff_3, 0.5*DOWN), self.camera.frame.animate.shift(2*RIGHT))
        self.wait(1)
        cutoff_4 = MTex(r"1+\frac1{1+\frac1{1+\frac1{1+\frac1{1}}}}=\frac{8}{5}", tex_to_color_map = {r"{1}": GOLD, (r"5", r"8"):BLUE}).scale(0.8).set_y(-1.5).match_x(equation_5)
        self.play(FadeIn(cutoff_4, 0.5*UP), self.camera.frame.animate.shift(3*RIGHT))
        self.wait(1)
        cutoff_5 = MTex(r"1+\frac1{1+\frac1{1+\frac1{1+\frac1{1+\frac1{1}}}}}=\frac{13}{8}", tex_to_color_map = {r"{1}": GOLD, (r"8", r"13"):GREEN}).scale(0.8).set_y(-3).match_x(equation_6)
        self.play(FadeIn(cutoff_5, 0.5*DOWN), self.camera.frame.animate.shift(4*RIGHT))
        self.wait(1)
        cutoff_6 = MTex(r"1+\frac1{1+\frac1{1+\frac1{1+\frac1{1+\frac1{1+\frac1{1}}}}}}=\frac{21}{13}", tex_to_color_map = {r"{1}": GOLD, (r"13", r"21"):BLUE}).scale(0.8).set_y(-2).match_x(equation_7)
        self.play(FadeIn(cutoff_6, 0.5*UP), self.camera.frame.animate.shift(5*RIGHT))
        self.wait(1)
        cutoff_7 = MTex(r"1+\frac1{1+\frac1{1+\frac1{1+\frac1{1+\frac1{1+\frac1{1+\frac1{1}}}}}}}=\frac{34}{21}", tex_to_color_map = {r"{1}": GOLD, (r"34", r"21"):GREEN}).scale(0.8).set_y(-3).match_x(equation_8)
        self.play(FadeIn(cutoff_7, 0.5*DOWN), self.camera.frame.animate.shift(6*RIGHT))
        self.wait(1)

        offset = 37*RIGHT + DOWN
        numberline = Polyline(5*LEFT, interpolate(5*LEFT, 5*RIGHT, phi-1), 5*RIGHT, color = [BLUE, WHITE, GOLD, GOLD, WHITE, GREEN], stroke_width = 10).shift(offset)
        self.play(*[OverFadeOut(mob) for mob in [equation_7[:-1], equation_8[:-1], cutoff_6, cutoff_7]], *[OverFadeIn(mob) for mob in [numberline]], self.camera.frame.animate.shift(7*RIGHT))
        self.wait()

        def position(a: float):
            return (10*a-15)*RIGHT + offset
        def part(a: float, tex: str | None = None):
            p = position(a)
            if a == phi:
                color = GOLD
            elif a < phi:
                color = BLUE
            else:
                color = GREEN
            if tex is None:
                tex = str(a)
            dot = Dot(stroke_width = 2, radius = 0.08, fill_color = color, stroke_color = WHITE, fill_opacty = 1).shift(p)
            tex = MTex(tex, fill_color = color).set_stroke(**stroke_dic).shift(p + DOWN)
            return (dot, tex)
        part_1, part_2, part_phi = part(1, "1"), part(2, "2"), part(phi, r"\phi")
        self.play(LaggedStart(*[ShowCreation(mob[0]) for mob in [part_1, part_2, part_phi]], lag_ratio = 1/3), 
                  LaggedStart(*[Write(mob[1]) for mob in [part_1, part_2, part_phi]], lag_ratio = 1/3, delay = 0.5))
        self.wait()

        f_1 = part(3/2, r"\frac{3}{2}")
        self.bring_to_back(numberline, *f_1).play(ShowCreation(f_1[0]), Write(f_1[1]))
        f_2 = part(5/3, r"\frac{5}{3}")
        self.bring_to_back(numberline, *f_2).play(ShowCreation(f_2[0]), Write(f_2[1]), f_1[1].animate.fade(0.8))
        f_3 = part(8/5, r"\frac{8}{5}")
        self.bring_to_back(numberline, *f_3).play(ShowCreation(f_3[0]), Write(f_3[1]), f_2[1].animate.fade(0.8))
        f_4 = part(13/8, r"\frac{13}{8}")
        self.bring_to_back(numberline, *f_4).play(ShowCreation(f_4[0]), Write(f_4[1]), f_3[1].animate.fade(0.8))
        f_5 = part(21/13, r"\frac{21}{13}")
        self.bring_to_back(numberline, *f_5).play(ShowCreation(f_5[0]), Write(f_5[1]), f_4[1].animate.fade(0.8))
        f_6 = part(34/21, r"\frac{34}{21}")
        self.bring_to_back(numberline, *f_6).play(ShowCreation(f_6[0]), Write(f_6[1]), f_5[1].animate.fade(0.8))
        self.play(f_6[1].animate.fade(0.8))
        self.wait()

#################################################################### 

class Video_2(FrameScene):
    def construct(self):
        offset = 3*LEFT + 0.5*UP
        circle = Circle(radius = 3, color = WHITE).shift(offset)
        vertices = [3*unit((i+1/2)*TAU/4) for i in range(4)]
        square = Polygon(*vertices, color = YELLOW).shift(offset)
        self.wait(1)
        self.play(ShowCreation(circle))
        self.play(ShowCreation(square))
        self.wait()

        triangles_1 = VGroup(*[Polygon(ORIGIN, vertices[2*i], vertices[2*i+1], color = GREY_D, **background_dic).shift(offset) for i in range(2)])
        self.add_background(triangles_1).play(FadeIn(triangles_1))
        self.wait()

        area_triangle = MTex(r"S_{\text{三角形}}=w_1h_1", tex_to_color_map = {r"4": RED, "w_1": BLUE, r"h_1": GREEN}).shift(3*RIGHT + 2*UP)
        formula_1 = MTex("S_1 = 4w_1h_1=2", tex_to_color_map = {r"4": RED, "w_1": BLUE, r"h_1": GREEN})
        formula_1.shift(area_triangle[4].get_center() - formula_1[2].get_center() + DOWN)
        wh = MTex(r"w_1=\frac{1}{\sqrt2}\ ,\ h_1 = \frac{1}{\sqrt2}", tex_to_color_map = {r"w_1=\frac{1}{\sqrt2}": BLUE, r"h_1 = \frac{1}{\sqrt2}": GREEN}).scale(0.8).shift(3*RIGHT)
        triangle = Polygon(ORIGIN, vertices[2], vertices[3], color = RED).shift(offset)
        w_1 = Line(vertices[2], (vertices[2]+vertices[3])/2, color = BLUE).shift(offset)
        text_w1 = MTex("w_1", color = BLUE).set_stroke(**stroke_dic).scale(0.8).next_to(w_1, UP)
        h_1 = Line((vertices[2]+vertices[3])/2, ORIGIN, color = GREEN).shift(offset)
        text_h1 = MTex("h_1", color = GREEN).set_stroke(**stroke_dic).scale(0.8).next_to(h_1, RIGHT)
        self.play(ShowCreation(triangle))
        self.add_text(text_w1, text_h1).play(ShowCreation(w_1), Write(text_w1), ShowCreation(h_1), Write(text_h1))
        self.wait()
        self.play(FadeIn(area_triangle, RIGHT))
        self.wait()
        self.play(Write(formula_1[:-2]))
        self.wait()
        self.play(FadeIn(wh, RIGHT))
        self.wait()
        self.play(Write(formula_1[-2:]))
        self.wait()

        vertices_2 = [3*unit((i+1)*TAU/8) for i in range(8)]
        octagon = Polygon(*vertices_2, color = YELLOW).shift(offset)
        self.play(ShowCreation(octagon))
        self.wait()

        triangles_2 = VGroup(*[Polygon(ORIGIN, vertices_2[2*i], vertices_2[2*i+1], color = GREY_D, **background_dic).shift(offset) for i in range(4)])
        self.add_background(triangles_2).play(OverFadeOut(triangles_1), OverFadeIn(triangles_2), FadeOut(area_triangle), FadeOut(formula_1), FadeOut(triangle))
        self.wait()

        triangle_2 = Polygon(ORIGIN, vertices_2[4], vertices_2[5], color = RED).shift(offset)
        w_2 = Line(vertices_2[5], (vertices_2[4]+vertices_2[5])/2, color = BLUE).shift(offset)
        text_w2 = MTex("w_2", color = BLUE).set_stroke(**stroke_dic).scale(0.8).next_to(w_2.get_center(), DOWN)
        h_2 = Line((vertices_2[4]+vertices_2[5])/2, ORIGIN, color = GREEN).shift(offset)
        text_h2 = MTex("h_2", color = GREEN).set_stroke(**stroke_dic).scale(0.8).next_to(h_2.get_center(), RIGHT)
        residue = Line((vertices[2]+vertices[3])/2, vertices_2[5], color = PURPLE_B).shift(offset)
        text_r = MTex("1-h_1", color = PURPLE_B).set_stroke(**stroke_dic).scale(0.8).next_to(residue.get_center(), RIGHT)
        self.play(ShowCreation(triangle_2))
        self.add_text(text_w2, text_h2, text_r).play(ShowCreation(w_2), Write(text_w2), ShowCreation(residue), Write(text_r), ShowCreation(h_2), Write(text_h2), wh.animate.shift(UP))
        self.wait()

        recursive = MTex(r"(2w_2)^2=w_1^2+(1-h_1)^2", tex_to_color_map = {(r"w_1", r"w_2"): BLUE, r"1-h_1": PURPLE_B}).shift(3*RIGHT)
        triangle_r = Polygon(vertices[2], (vertices[2]+vertices[3])/2, vertices_2[5], color = ORANGE, **background_dic).shift(offset)
        copy_r = Polygon(vertices[2], (vertices[2]+vertices[3])/2, vertices_2[5], color = ORANGE).shift(4*RIGHT + 5.35*UP)
        length_0 = MTex(r"w_1", color = BLUE).scale(0.6).next_to(copy_r, UP, buff = 0.1)
        length_1 = MTex(r"1-h_1", color = PURPLE_B).scale(0.6).next_to(copy_r, RIGHT)
        length_2 = MTex(r"2w_2", color = PURPLE_B, tex_to_color_map = {r"w_2": BLUE}).scale(0.6).next_to(copy_r.get_center(), DL, buff = 0.1)
        self.add_background(triangle_r).play(FadeIn(triangle_r, rate_func = blink(5), run_time = 2), ShowCreation(copy_r), *[Write(mob, run_time = 1, delay = 1) for mob in [length_0, length_1, length_2]])
        self.wait()
        self.play(Write(recursive))
        self.wait()

        solution = MTex(r"w_2 &= \sqrt{\frac{1-h_1}{2}}\approx 0.38268\\h_2&=\sqrt{1-w_2^2}\approx 0.92387", tex_to_color_map = {(r"w_1", r"w_2"): BLUE, r"1-h_1": PURPLE_B, r"h_2": GREEN}).scale(0.8)
        solution.shift(recursive[6].get_center() - solution[2].get_center() + DOWN)
        self.play(FadeIn(solution, 0.5*DOWN))
        self.wait()
        formula_2 = MTex(r"S_2 = {8}w_2h_2 \approx 2.828", tex_to_color_map = {r"{8}": RED, "w_2": BLUE, r"h_2": GREEN})
        formula_2.shift(recursive[6].get_center() - formula_2[2].get_center() + 2*UP)
        #self.play(*[FadeOut(mob) for mob in [copy_r, length_0, length_1, length_2]])
        self.play(Write(formula_2))
        self.wait()

        vertices_3 = [3*unit((i)*TAU/16) for i in range(16)]
        gon_16 = Polygon(*vertices_3, color = YELLOW).shift(offset)
        r_3 = Line((vertices_2[4]+vertices_2[5])/2, vertices_3[11], color = PURPLE_B).shift(offset)
        self.play(ShowCreation(gon_16), *[FadeOut(mob) for mob in [w_1, text_w1, h_1, text_h1, residue, text_r, triangle_2]], 
                  *[mob.animate.shift(2.5*UP) for mob in [solution]], *[OverFadeOut(mob, 2.5*UP) for mob in [recursive, formula_2, wh, triangle_r, copy_r, length_0, length_1, length_2]], 
                  FadeIn(r_3))
        
        triangles_3 = VGroup(*[Polygon(ORIGIN, vertices_3[2*i], vertices_3[2*i+1], color = GREY_D, **background_dic).shift(offset) for i in range(8)])
        w_3 = Line(vertices_3[11], (vertices_3[10]+vertices_3[11])/2, color = BLUE).shift(offset)
        text_w3 = MTex("w_3", color = BLUE).set_stroke(**stroke_dic).scale(0.8).next_to(w_3.get_center(), DOWN)
        h_3 = Line((vertices_3[10]+vertices_3[11])/2, ORIGIN, color = GREEN).shift(offset)
        text_h3 = MTex("h_3", color = GREEN).set_stroke(**stroke_dic).scale(0.8).next_to(h_3.get_center(), LEFT)
        triangle_r = Polygon(vertices_2[5], (vertices_2[4]+vertices_2[5])/2, vertices_3[11], color = ORANGE, **background_dic).shift(offset)
        self.add_background(triangles_3, triangle_r).play(OverFadeOut(triangles_2), OverFadeIn(triangles_3), OverFadeIn(triangle_r))
        self.wait()
        self.add_text(text_w3, text_h3).play(ShowCreation(w_3), Write(text_w3), ShowCreation(h_3), Write(text_h3))
        self.wait()

        solution_3 = MTex(r"w_3 &= \sqrt{\frac{1-h_2}{2}}\approx 0.19509\\h_3&=\sqrt{1-w_3^2}\approx 0.98079", tex_to_color_map = {(r"w_3", r"w_2"): BLUE, r"1-h_2": PURPLE_B, r"h_3": GREEN}).scale(0.8)
        solution_3.shift(solution[2].get_center() - solution_3[2].get_center() + 2*DOWN)
        self.play(FadeIn(solution_3, RIGHT))
        self.wait()

        formula_3 = MTex(r"S_3 = 16w_3h_3 \approx 3.0615", tex_to_color_map = {r"16": RED, "w_3": BLUE, r"h_3": GREEN})
        formula_3.shift(solution[2].get_center() - formula_3[2].get_center() + 1.2*UP)
        self.play(Write(formula_3))
        self.wait()

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        