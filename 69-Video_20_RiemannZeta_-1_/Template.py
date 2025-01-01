from __future__ import annotations

from manimlib import *
import numpy as np

import mpmath
mpmath.mp.dps = 7

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

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        series1_u = MTex(r"A=1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+\cdots", tex_to_color_map = {r"A": BLUE, r"1": GREEN_B, r"-1": RED_B, r"+": GREEN_B}).next_to(6.5*LEFT + 1.5*UP)
        self.play(Write(series1_u[2:]))
        self.wait()
        self.play(FadeIn(series1_u[:2], 0.5*RIGHT))
        self.wait()

        ket = MTex(r"A=1-()", tex_to_color_map = {r"A": BLUE, r"1": GREEN_B, r"-": RED}).next_to(6.5*LEFT + 0.5*UP)
        guide = ket[:4]
        series1_d = MTex(r"A=1-(1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-\cdots)", tex_to_color_map = {r"A": BLUE, r"1": GREEN_B, r"-": RED, r"-1": RED_B, r"+": GREEN_B}).next_to(6.5*LEFT + 0.5*UP)
        self.play(guide.save_state().set_opacity(0).shift(1*UP).animate.restore(), follow(ket[4:], guide, FadeIn))
        self.wait()
        self.play(Transform(ket[-1], series1_d[-1], run_time = 4), TransformFromCopy(series1_u[:3:-1], series1_d[-2:4:-1], lag_ratio = 0.2, run_time = 4))
        self.clear().add(series1_u, series1_d).wait()

        self.play(series1_u.animate.shift((series1_d[5].get_x() - series1_u[2].get_x())*RIGHT))
        self.wait()
        self.play(LaggedStart(*[mob.animating(rate_func = there_and_back).shift(0.2*UP).scale(1.2).set_color(YELLOW) for mob in series1_u[2:-2]], lag_ratio = 0.1, run_time = 2), 
                  LaggedStart(*[mob.animating(rate_func = there_and_back).shift(0.2*UP).scale(1.2).set_color(YELLOW) for mob in series1_d[5:-1]], lag_ratio = 0.1, run_time = 2))
        self.wait()

        series1_dd = MTex(r"=1-A", tex_to_color_map = {r"A": BLUE, r"1": GREEN_B, r"-": RED})
        series1_dd.shift(series1_d[1].get_center() - series1_dd[0].get_center() + DOWN)
        self.play(Write(series1_dd))
        self.wait()

        value_1 = MTex(r"\frac{1}{2}=A", color = BLUE, tex_to_color_map = {r"=": WHITE})
        value_1.shift(series1_u[0].get_center() - value_1[-1].get_center())
        self.play(FadeIn(value_1[:-1], 0.5*RIGHT))
        self.wait()

        series1_u.add(*value_1[:-1])
        self.remove(value_1).play(series1_u.animate.shift(1.5*UP), *[OverFadeOut(mob, 1.5*UP) for mob in [series1_d, series1_dd]], run_time = 2)
        self.wait()
        series_1 = series1_u

        series2_u = VGroup(MTex(r"B", color = BLUE), MTex(r"="), MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"2", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"3", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"4", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"5", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"6", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"7", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"8", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"9", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"10", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"11", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"12", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"13", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"14", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"\cdots"))
        for i, mob in enumerate(series2_u):
            mob.move_to((-6+0.55*i)*RIGHT + UP)
        series2_d = series2_u.copy().shift(DOWN)
        self.play(Write(series2_u[2:]))
        self.wait()
        self.play(FadeIn(series2_u[:2], 0.5*RIGHT))
        self.wait()
        self.play(ReplacementTransform(series2_u.copy(), series2_d, lag_ratio = 0.05, run_time = 2))
        self.wait()
        self.play(series2_d[2:].animate.shift(2*0.55*RIGHT))
        self.wait()
        series2_dd = VGroup(MTex(r"\frac{1}{2}", color = BLUE), MTex(r"="), MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"1", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"1", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"1", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"1", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"1", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"1", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"1", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"\cdots"))
        add, equal = MTex(r"+")[0].shift((-6+0.55)*RIGHT + 0.5*UP), MTex(r"=")[0].rotate(PI/2).shift((-6+0.55)*RIGHT + 0.6*DOWN)
        for i, mob in enumerate(series2_dd):
            mob.move_to((-6+0.55*i)*RIGHT + 1.2*DOWN)
        self.play(Write(add), Write(equal))
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in series2_dd[1:]], lag_ratio = 0.1, run_time = 2))
        self.wait()
        self.play(Write(series2_dd[0]))
        self.wait()

        list_2_u = [submob for mob in series2_u for submob in mob.submobjects]
        series_2 = MTex(r"\frac{1}{4}=B=1-2+3-4+5-6+7-8+9-10+11-12+13-14+\cdots", tex_to_color_map = {(r"+", r"1", r"3", r"5", r"7", r"9", r"11", r"13"): GREEN_B, (r"-", r"2", r"4", r"6", r"8", r"10", r"12", r"14"): RED_B, (r"\frac{1}{4}", r"B"): BLUE})
        series_2.shift(series_1[1].get_center() - series_2[5].get_center() + 1.25*DOWN)
        anim = ReplacementTransform(list_2_u[0], series_2[4])
        self.play(anim, *[ReplacementTransform(mob, target) for mob, target in zip(list_2_u[1:], series_2[5:])], follow(series_2[:4], anim, FadeIn), 
                  *[follow(mob, anim, OverFadeOut) for mob in [series2_d, series2_dd, add, equal]], run_time = 2)
        self.wait()

        series3_u = VGroup(MTex(r"S", color = BLUE), MTex(r"="), MTex(r"1", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"2", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"3", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"4", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"5", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"6", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"7", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"8", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"9", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"10", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"11", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"12", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"13", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"14", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"\cdots"))
        for i, mob in enumerate(series3_u):
            mob.move_to((-6+0.55*i)*RIGHT + 0.5*UP)
        series3_d = series3_u.copy().shift(DOWN)
        series3_d_2 = VGroup(MTex(r"4S", color = BLUE).shift(0.1*LEFT), MTex(r"="), MTex(r"4", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"8", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"12", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"16", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"20", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"24", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"28", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"32", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"36", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"40", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"44", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"48", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"52", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"56", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"\cdots"))
        for i, mob in enumerate(series3_d_2):
            mob.shift((-6+0.55*i)*RIGHT + 0.5*DOWN)
        self.play(Write(series3_u))
        self.wait()
        self.play(ReplacementTransform(series3_u.copy(), series3_d, lag_ratio = 0.05, run_time = 2))
        self.wait()
        self.play(LaggedStart(*[Flip(mob_1, mob_2, dim = 1) for mob_1, mob_2 in zip(series3_d, series3_d_2)], run_time = 2, lag_ratio = 0.1))
        self.wait()
        self.play(*[mob.animate.shift(0.55*(i+2)*RIGHT) for i, mob in enumerate(series3_d[2:])], run_time = 3)
        self.wait()
        series3_dd = VGroup(MTex(r"-3S", color = BLUE).shift(0.3*LEFT), MTex(r"="), MTex(r"1", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"2", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"3", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"4", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"5", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"6", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"7", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"8", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"9", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"10", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"11", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"12", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"13", color = GREEN_B), MTex(r"-", color = RED_B), MTex(r"14", color = RED_B), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"\cdots"))
        subtract, equal = MTex(r"-")[0].rotate(PI/2).shift((-6+0.55)*RIGHT), MTex(r"=")[0].rotate(PI/2).shift((-6+0.55)*RIGHT + 1.1*DOWN)
        for i, mob in enumerate(series3_dd):
            mob.shift((-6+0.55*i)*RIGHT + 1.7*DOWN)
        self.play(Write(subtract), Write(equal))
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in series3_dd], lag_ratio = 0.1, run_time = 2))
        self.wait()

        self.play(LaggedStart(*[mob.animating(rate_func = there_and_back).shift(0.2*UP).scale(1.2).set_color(YELLOW) for mob in series_2[6:-2]], lag_ratio = 0.1, run_time = 2), 
                  LaggedStart(*[mob.animating(rate_func = there_and_back).shift(0.2*UP).scale(1.2).set_color(YELLOW) for mob in [submob for mob in series3_dd[2:] for submob in mob.submobjects]], lag_ratio = 0.1, run_time = 2))
        self.wait()

        result_3, result_2 = MTex(r"-\frac{1}{12}=", color = BLUE, tex_to_color_map = {r"=": WHITE}).next_to(5.2*LEFT + 0.5*UP, LEFT), MTex(r"\frac{1}{4}=", color = BLUE, tex_to_color_map = {r"=": WHITE}).next_to(5.7*LEFT + 1.7*DOWN, LEFT)
        self.play(*[mob.animate.shift(1.0*RIGHT) for mob in [series3_u, series3_d, series3_dd, subtract, equal]], FadeIn(result_2, 1.0*RIGHT))
        self.wait()
        self.play(Write(result_3))
        self.wait()

        series_3 = MTex(r"-\frac{1}{12}=S=1+2+3+4+5+6+7+8+9+10+11+12+13+14+\cdots", tex_to_color_map = {(r"1", r"+3", r"+5", r"+7", r"+9", r"+11", r"+13"): GREEN_B, (r"+2", r"+4", r"+6", r"+8", r"+10", r"+12", r"+14"): RED_B, (r"-\frac{1}{12}", r"S"): BLUE})
        series_3.shift(series_2[5].get_center() - series_3[7].get_center() + 1.25*DOWN)
        self.play(*[FadeOut(mob) for mob in [series3_d, series3_dd, subtract, equal, result_2]], 
                  *[ReplacementTransform(mob, target) for mob, target in zip([submob for mob in [result_3, *series3_u] for submob in mob.submobjects], series_3)])
        self.wait()

#################################################################### 

'''
class Video_2(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 12.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = max((x+5.5)**(2/3), 2)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                if mob.counter % 2:
                    mob.add(MTex(r"-1", color = RED).shift(2.025*UP + 5.3*LEFT))
                else:
                    mob.add(MTex(r"+1", color = GREEN).shift(2*UP + 5.3*LEFT))
                mob.time -= 0.5
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0.5
        terms.add_updater(terms_updater)
        # mob_1, mob_2, mob_3 = MTex(r"+1", color = GREEN).shift(2*UP + 5.3*LEFT), MTex(r"-1", color = RED).shift(2*UP + 5.3*LEFT), MTex(r"+1", color = GREEN).shift(2*UP + 5.3*LEFT)
        # self.add(mob_1.add_updater(term_updater)).wait()
        # self.add(mob_2.add_updater(term_updater)).wait()
        # self.add(mob_3.add_updater(term_updater)).wait(10)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = (7-x)**1.1*0.2
            mob[0].shift(v*dt*RIGHT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                if mob.counter % 2:
                    new_dot = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                else:
                    new_dot = VGroup(Dot(0.5*DOWN + 6*LEFT, color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = mob[-1]
                mob.add(new_dot)
                mob.time -= 0.5
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(0.5*DOWN + 6*LEFT, color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 1, 0
        points.add_updater(points_updater)
        self.add(terms, points).wait(50)

class Video_3(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, (13+1/9+0.2)*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = 1.25*max((x+5.5)**(2/3), 2)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                mob.add(MTex((r"-" if mob.counter%2 else r"+") + r"\frac{1}{" + str(mob.counter*2+1) + r"}", color = RED if mob.counter%2 else GREEN).shift(2*UP + 5.2*LEFT))
                mob.time -= 0.5
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0
        terms.add_updater(terms_updater)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = 0.2*((7-x)**1.1)
            mob[0].shift(v*dt*RIGHT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                last = mob[-1]
                new_dot = VGroup(Dot(np.array([-6, last[0].get_y() + ((-1)**(mob.counter%2))*2/(mob.counter*2+1), 0]), color = BLUE_E if mob.counter%2 else BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = last
                mob.add(new_dot)
                mob.time -= 0.5
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 0, 0
        points.add_updater(points_updater)
        self.add(terms, points).wait(50)

class Video_4(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, (13+1/9+0.2)*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        peroid = 1/3
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = 1/peroid*max(0.5*(x+5.5)**(2/3), 1)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                mob.add(MTex(r"+1", color = GREEN).shift(2*UP + 5.2*LEFT))
                mob.time -= peroid
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0
        terms.add_updater(terms_updater)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = 0.1/peroid*((7-x)**1.1)
            mob[0].shift(v*dt*RIGHT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                last = mob[-1]
                new_dot = VGroup(Dot(np.array([-6, last[0].get_y() + 1, 0]), color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = last
                mob.add(new_dot)
                mob.time -= peroid
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 0, 0
        points.add_updater(points_updater)
        self.add(terms, points).wait(20)

class Video_5(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, (13+1/9+0.2)*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        peroid = 1/3
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = 1/peroid*max(0.5*(x+5.5)**(2/3), 1)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                mob.add(MTex(r"+"+str(mob.counter+1), color = GREEN).shift(2*UP + 5.2*LEFT))
                mob.time -= peroid
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0
        terms.add_updater(terms_updater)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = 0.1/peroid*((7-x)**1.1)
            mob[0].shift(v*dt*RIGHT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                last = mob[-1]
                new_dot = VGroup(Dot(np.array([-6, last[0].get_y() + 0.1*mob.counter, 0]), color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = last
                mob.add(new_dot)
                mob.time -= peroid
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 0, 0
        points.add_updater(points_updater)
        self.add(terms, points).wait(20)
'''

class Video_2(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 13.2*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = max((x+5.5)**(2/3), 2)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                if mob.counter % 2:
                    mob.add(MTex(r"-1", color = RED).shift(2.025*UP + 5.3*LEFT))
                else:
                    mob.add(MTex(r"+1", color = GREEN).shift(2*UP + 5.3*LEFT))
                mob.time -= 0.5
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0.5
        terms.add_updater(terms_updater)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = (6+x)*(max(1/(0.6+0.1*self.time), 0.15))
            mob[0].shift(v*dt*LEFT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                if mob.counter % 2:
                    new_dot = VGroup(Dot(0.5*DOWN + 7*RIGHT, color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                else:
                    new_dot = VGroup(Dot(2.5*DOWN + 7*RIGHT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = mob[-1]
                mob.add(new_dot)
                mob.time -= 0.5
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 1, 0.5
        points.add_updater(points_updater)
        self.add(terms, points).wait(50)

class Video_3(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 13.2*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = 1.25*max((x+5.5)**(2/3), 2)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                mob.add(MTex((r"-" if mob.counter%2 else r"+") + r"\frac{1}{" + str(mob.counter*2+1) + r"}", color = RED if mob.counter%2 else GREEN).shift(2*UP + 5.2*LEFT))
                mob.time -= 0.5
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0
        terms.add_updater(terms_updater)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = (6+x)*(max(1/(0.6+0.1*self.time), 0.15))
            mob[0].shift(v*dt*LEFT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= 0.5):
                last = mob[-1]
                new_dot = VGroup(Dot(np.array([7, last[0].get_y() + ((-1)**(mob.counter%2))*2/(mob.counter*2+1), 0]), color = BLUE_E if mob.counter%2 else BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = last
                mob.add(new_dot)
                mob.time -= 0.5
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 0, 0
        points.add_updater(points_updater)
        self.add(terms, points).wait(50)

class Video_4(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 13.2*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        peroid = 1/3
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = 1/peroid*max(0.5*(x+5.5)**(2/3), 1)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                mob.add(MTex(r"+1", color = GREEN).shift(2*UP + 5.2*LEFT))
                mob.time -= peroid
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0
        terms.add_updater(terms_updater)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = 0.6/peroid*((6+x)*(max(1/(0.1+0.5*self.time), 0.05)))
            mob[0].shift(v*dt*LEFT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                last = mob[-1]
                new_dot = VGroup(Dot(np.array([7, last[0].get_y() + 1, 0]), color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = last
                mob.add(new_dot)
                mob.time -= peroid
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 0, 0
        points.add_updater(points_updater)
        self.add(terms, points).wait(20)

class Video_5(FrameScene):
    def construct(self):
        sum = MTex(r"S=", tex_to_color_map = {r"S": BLUE}).shift(2*UP + 6*LEFT)
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 13.2*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        self.add(sum, axis_x, axis_y).wait()
        
        peroid = 1/3
        def term_updater(mob: VMobject, dt):
            x = mob.get_x()
            v = 1/peroid*max(0.5*(x+5.5)**(2/3), 1)
            mob.shift(v*dt*RIGHT).set_opacity(clip(inverse_interpolate(8, 0, x), 0, 1))
            return x > 8
        def terms_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                mob.add(MTex(r"+"+str(mob.counter+1), color = GREEN).shift(2*UP + 5.2*LEFT))
                mob.time -= peroid
                mob.counter += 1
            to_remove = []
            for submob in mob.submobjects:
                if_remove = term_updater(submob, dt)
                if if_remove:
                    to_remove.append(submob)
            mob.remove(*to_remove)
        terms = VGroup()
        terms.counter, terms.time = 0, 0
        terms.add_updater(terms_updater)

        def point_updater(mob: VMobject, dt):
            x = mob[0].get_x()
            v = 0.6/peroid*((6+x)*(max(1/(0.1+0.5*self.time), 0.05)))
            mob[0].shift(v*dt*LEFT)
            mob[1].put_start_and_end_on(mob[0].get_center(), mob.pointer[0].get_center())
            return x > 8
        def points_updater(mob: VGroup, dt):
            mob.time += dt
            while(mob.time >= peroid):
                last = mob[-1]
                new_dot = VGroup(Dot(np.array([7, last[0].get_y() + 0.1*mob.counter, 0]), color = BLUE), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
                new_dot.pointer = last
                mob.add(new_dot)
                mob.time -= peroid
                mob.counter += 1
            for submob in mob.submobjects:
                point_updater(submob, dt)
        point_0 = VGroup(Dot(2.5*DOWN + 6*LEFT, color = BLUE_E), Line(1.5*DOWN + 6*LEFT, 1.5*DOWN + 6*LEFT, stroke_width = 2)).set_stroke(background = True)
        point_0.pointer = point_0
        points = VGroup(point_0).set_stroke(background = True)
        points.counter, points.time = 0, 0
        points.add_updater(points_updater)
        self.add(terms, points).wait(20)
        
#################################################################### 

class Video_6(FrameScene):
    def construct(self):
        Cauchy = LabelPicture("Cauchy.jpg", "奥古斯丁·路易·柯西（1789.8.21 - 1857.5.23）").shift(3.5*LEFT)
        self.play(FadeIn(Cauchy))
        self.wait()

        series = MTex(r"A&=1-1+1-1+1-1+1-1+\cdots\\A&=1-(1-1+1-1+1-1+1-\cdots)\\&=1-A", tex_to_color_map = {r"A": BLUE, r"1": GREEN_B, r"-1": RED_B, r"+": GREEN_B}).next_to(0.5*LEFT)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(color = RED, width = 8).scale(np.array([2.5, 2, 1])).shift(3.5*RIGHT)
        self.fade_in(series, cross, excepts = [Cauchy])
        self.wait()
        self.fade_out().wait()

        series1_u = MTex(r"x=1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+\cdots", tex_to_color_map = {r"x": BLUE, r"1": GREEN_B, r"+": GREEN_B}).next_to(6.5*LEFT + 1.5*UP)
        self.play(Write(series1_u[2:]))
        self.wait()
        self.play(FadeIn(series1_u[:2], 0.5*RIGHT))
        self.wait()

        series1_d = MTex(r"x=1+1+(1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+\cdots)", tex_to_color_map = {r"x": BLUE, r"1": GREEN_B, r"+": GREEN_B}).next_to(6.5*LEFT + 0.5*UP)
        series1_d_0 = series1_u.copy().insert_submobject(6, series1_d[6].copy().scale(0).move_to(series1_u[5].get_right())).add(series1_d[-1].copy().scale(0).move_to(series1_u.get_right()))
        self.play(ReplacementTransform(series1_d_0, series1_d))
        self.wait()

        series1_dd = MTex(r"=2+x", tex_to_color_map = {r"x": BLUE, r"2": LIGHT_BROWN})
        series1_dd.shift(series1_d[1].get_center() - series1_dd[0].get_center() + DOWN)
        self.play(Write(series1_dd))
        self.wait()

        result_1 = MTex(r"0=2", tex_to_color_map = {r"0": GREEN_B, r"2": LIGHT_BROWN})
        result_1.shift(series1_dd[0].get_center() - result_1[1].get_center() + DOWN)
        self.play(Write(result_1))
        self.wait()

        series2_d = MTex(r"x=1+1+1+(1+1+1+1+1+1+1+1+1+1+1+1+1+1+\cdots)", tex_to_color_map = {r"x": BLUE, r"1": GREEN_B, r"+": GREEN_B}).next_to(6.5*LEFT + 0.5*UP)
        series2_d_0 = series2_d.copy()
        series2_d_0[6].move_to(series1_d[7]), series2_d_0[7].move_to(series1_d[8]), series2_d_0[8].move_to(series1_d[6])
        series2_dd = MTex(r"=3+x", tex_to_color_map = {r"x": BLUE, r"3": LIGHT_BROWN})
        series2_dd.shift(series2_d[1].get_center() - series2_dd[0].get_center() + DOWN)
        result_2 = MTex(r"0=3", tex_to_color_map = {r"0": GREEN_B, r"3": LIGHT_BROWN})
        result_2.shift(series2_dd[0].get_center() - result_2[1].get_center() + DOWN)
        self.remove(series1_d).play(ReplacementTransform(series2_d_0, series2_d), ReplacementTransform(series1_dd, series2_dd), ReplacementTransform(result_1, result_2))
        self.wait()

        series3_d = MTex(r"x=\overbrace{1+\cdots+1}^{\text{共114514项}}+(1+1+1+1+1+1+1+1+1+1+1+1+1+1+\cdots)", tex_to_color_map = {r"x": BLUE, r"1": GREEN_B, r"114514": LIGHT_BROWN, r"+": GREEN_B}).next_to(6.5*LEFT + 0.5*UP)
        brace = series3_d[2:16]
        offset = series2_d[0].get_center() - series3_d[0].get_center()
        series3_d.remove(*series3_d[2:16])
        series2_d.insert_submobject(4, series2_d[4].copy()).insert_submobject(4, series2_d[4].copy())
        series3_dd = MTex(r"=114514+x", tex_to_color_map = {r"x": BLUE, r"114514": LIGHT_BROWN})
        series2_dd.insert_submobject(1, series2_dd[1].copy()).insert_submobject(1, series2_dd[1].copy()).insert_submobject(1, series2_dd[1].copy()).insert_submobject(1, series2_dd[1].copy()).insert_submobject(1, series2_dd[1].copy())
        series3_dd.shift(series3_d[1].get_center() - series3_dd[0].get_center() + DOWN)
        result_3 = MTex(r"0=114514", tex_to_color_map = {r"0": GREEN_B, r"114514": LIGHT_BROWN})
        result_3.shift(series3_dd[0].get_center() - result_3[1].get_center() + DOWN)
        result_2.insert_submobject(2, result_2[2].copy()).insert_submobject(2, result_2[2].copy()).insert_submobject(2, result_2[2].copy()).insert_submobject(2, result_2[2].copy()).insert_submobject(2, result_2[2].copy())
        self.play(FadeIn(brace, offset/2), ReplacementTransform(series2_d, series3_d), ReplacementTransform(series2_dd, series3_dd), ReplacementTransform(result_2, result_3))
        self.wait()

        self.fade_out(run_time = 0.5)

        series_1 = MTex(r"\frac{1}{2}=A=1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+\cdots", tex_to_color_map = {r"1": GREEN_B, r"-1": RED_B, r"+": GREEN_B, (r"\frac{1}{2}", r"A"): BLUE}).next_to(6.5*LEFT + 1.5*UP)
        series_2 = MTex(r"\frac{1}{4}=B=1-2+3-4+5-6+7-8+9-10+11-12+13-14+\cdots", tex_to_color_map = {(r"+", r"1", r"3", r"5", r"7", r"9", r"11", r"13"): GREEN_B, (r"-", r"2", r"4", r"6", r"8", r"10", r"12", r"14"): RED_B, (r"\frac{1}{4}", r"B"): BLUE})
        series_2.shift(series_1[5].get_center() - series_2[5].get_center() + 1.5*DOWN)
        series_3 = MTex(r"-\frac{1}{12}=S=1+2+3+4+5+6+7+8+9+10+11+12+13+14+\cdots", tex_to_color_map = {(r"1", r"+3", r"+5", r"+7", r"+9", r"+11", r"+13"): GREEN_B, (r"+2", r"+4", r"+6", r"+8", r"+10", r"+12", r"+14"): RED_B, (r"-\frac{1}{12}", r"S"): BLUE})
        series_3.shift(series_2[5].get_center() - series_3[7].get_center() + 1.5*DOWN)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(color = RED, width = 12).scale(np.array([3, 3, 1]))
        self.fade_in(series_1, series_2, series_3, cross, run_time = 0.5)
        self.wait()

#################################################################### 
        
class WaveFunction(VGroup):
    def __init__(self, template: VMobject, number: int = 12, phase: float = 0, offset: np.ndarray = ORIGIN, **kwargs):
        self.template, self.offset = template, Point(offset)
        submobs = []
        for i in range(number):
            phase = (TAU*i/number + phase) % TAU
            submob = template.copy().scale(np.array([1, np.sin(phase), 0]), about_point = ORIGIN, min_scale_factor = -1).shift(offset)
            if i:
                submob.set_stroke(width = template.get_stroke_width()/4, color = interpolate_color(template.get_stroke_color(), BLACK, 0.5))
            submob.phase = phase
            submobs.append(submob)
        super().__init__(*submobs[::-1], **kwargs)

class Test_7(FrameScene):
    def construct(self):
        particle = WaveFunction(FunctionGraph(lambda t: np.sin(t+PI/2), [-PI/2, PI/2, PI/100], color = RED, stroke_width = 6))
        alpha = ValueTracker(0.0)
        def particle_updater(v: float):
            def util(mob: WaveFunction):
                angle = alpha.get_value()
                offset = mob.offset.get_location()
                for submob in mob.submobjects:
                    new_phase = (submob.phase + v*angle)%TAU
                    submob.set_points(mob.template.copy().scale(np.array([1, np.sin(new_phase), 0]), about_point = ORIGIN, min_scale_factor = -1).shift(offset).get_points())
            return util
        for i in range(3):
            particle = WaveFunction(FunctionGraph(lambda t: 0.5*np.sin((i+1)*(t+PI/2)), [-PI/2, PI/2, PI/100], color = RED, stroke_width = 6), offset = (i-1)*1.2*DOWN)
            particle.add_updater(particle_updater(i+1))
            self.add(particle)
        self.play(alpha.animate.set_value(10), run_time = 10, rate_func = linear)

class Video_7(FrameScene):
    def construct(self):
        self.wait(0, 26) #（空闲）
        title, titleline = Title(r"卡西米尔效应"), TitleLine()
        self.play(Write(title), GrowFromCenter(titleline))
        self.wait(2, 15) #在这个认知境界的人 通常会举出卡西米尔效应的例子
        self.wait(0, 14) #（空闲）

        board_left, board_right = Line(3*UP, 3*DOWN, color = GREY, stroke_width = 20).shift(PI/2*LEFT + 0.1*LEFT), Line(3*UP, 3*DOWN, color = GREY, stroke_width = 20).shift(PI/2*RIGHT + 0.1*RIGHT)
        self.bring_to_back(board_left, board_right).play(ShowCreation(board_left), ShowCreation(board_right))
        self.wait(0, 4) #简单来说就是
        self.wait(2, 3) #在真空中如果有两个金属板
        self.wait(1, 15) #它们靠的非常近
        arrow_l, arrow_r = Arrow(PI/2*LEFT, PI/2*LEFT + 0.5*RIGHT, buff = 0, color = BLUE), Arrow(PI/2*RIGHT, PI/2*RIGHT + 0.5*LEFT, buff = 0, color = BLUE)
        self.bring_to_back(arrow_l, arrow_r).play(GrowArrow(arrow_l), GrowArrow(arrow_r))
        self.wait(2, 10) #那么它们之间会因为量子场论的原因产生吸引力
        self.wait(0, 16) #（空闲）
        self.wait(1, 27) #这种力不是万有引力
        self.wait(2, 22) #而是由于量子涨落带来的虚粒子而产生的力
        self.wait(0, 22) #（空闲）

        alpha = ValueTracker(0.0).add_updater(lambda mob, dt: mob.increment_value(dt))
        self.add(alpha)
        def particle_updater(v: float):
            def util(mob: WaveFunction):
                angle = alpha.get_value()
                offset = mob.offset.get_location()
                for submob in mob.submobjects:
                    new_phase = (submob.phase + v*angle)%TAU
                    submob.set_points(mob.template.copy().scale(np.array([1, np.sin(new_phase), 0]), about_point = ORIGIN, min_scale_factor = -1).shift(offset).get_points())
            return util
        particle_1 = WaveFunction(FunctionGraph(lambda t: 0.5*np.sin(t+PI/2), [-PI/2, PI/2, PI/100], color = GREEN, stroke_width = 6), offset = 1.8*UP)
        particle_1.add_updater(particle_updater(1*1.5))
        cant = WaveFunction(FunctionGraph(lambda t: 0.5*np.sin(1.25*t+PI/2), [-PI/2, PI/2, PI/100], color = RED, stroke_width = 6), offset = 1.2*DOWN)
        cant.add_updater(particle_updater(1.25*1.5))
        self.play(FadeOut(arrow_l), FadeOut(arrow_r), run_time = 0.5, rate_func = rush_into)
        self.bring_to_back(alpha, particle_1, cant, self.shade).play(FadeOut(self.shade), run_time = 0.5, rate_func = rush_from)
        self.wait(1, 1) #你不需要知道很多具体的细节
        checkmark, cross = MTex(r"\checkmark", color = GREEN).next_to(1.8*UP + PI/2*RIGHT, RIGHT), Text(r"✗", font = "simsun", color = RED).scale(0.8).next_to(1.2*DOWN + PI/2*RIGHT, RIGHT)
        self.play(Write(checkmark), Write(cross))
        self.wait(2, 25) #只需要知道 只有某些特定的波函数
        self.wait(2, 5) #能够存在于这两个板之间
        self.wait(0, 15) #（空闲）

        indicate_left = Rectangle(width = 0.3, height = 0.6, stroke_color = YELLOW).shift(PI/2*LEFT + 1.2*DOWN)
        indicate_right = Rectangle(width = 0.3, height = 0.6, stroke_color = YELLOW).shift(PI/2*RIGHT + 1.2*DOWN)
        self.play(ShowCreation(indicate_left), ShowCreation(indicate_right))
        self.wait(3, 27) #具体来说 就是需要波在两端金属板的位置上不会震动
        self.wait(0, 19) #（空闲）

        steady = Heiti(r"驻波", color = YELLOW).scale(0.8).next_to(1.8*UP + PI/2*LEFT, LEFT)
        back = Rectangle(height = 1.2, width = PI/1.25, color = GREY, stroke_width = 0, fill_opacity = 0.5).shift(1.2*DOWN)
        node = Heiti(r"波节", color = YELLOW).scale(0.8).next_to(back, UP)
        self.bring_to_back(back).play(FadeIn(back), Write(node), Write(steady))
        self.wait(1, 18) #用专业的说法 这叫驻波
        self.wait(2, 16) #这样的枣核形状的称作波节
        
        self.bring_to_back(back, node, checkmark, cross, cant, steady, self.shade).play(FadeIn(self.shade), FadeOut(indicate_left), FadeOut(indicate_right), run_time = 0.5, rate_func = rush_into)
        self.remove(back, node, checkmark, cross, cant, steady, self.shade)

        colors = [GREEN, LIME, YELLOW, interpolate_color(YELLOW, ORANGE, 0.5)]
        particle_2 = WaveFunction(FunctionGraph(lambda t: 0.5*np.sin(2*(t+PI/2)), [-PI/2, PI/2, PI/100], color = LIME, stroke_width = 6), offset = 0.6*UP)
        particle_2.add_updater(particle_updater(2*1.5))
        particle_3 = WaveFunction(FunctionGraph(lambda t: 0.5*np.sin(3*(t+PI/2)), [-PI/2, PI/2, PI/100], color = YELLOW, stroke_width = 6), offset = 0.6*DOWN)
        particle_3.add_updater(particle_updater(3*1.5))
        particle_4 = WaveFunction(FunctionGraph(lambda t: 0.5*np.sin(4*(t+PI/2)), [-PI/2, PI/2, PI/100], color = colors[3], stroke_width = 6), offset = 1.8*DOWN)
        particle_4.add_updater(particle_updater(4*1.5))
        dots = MTex(r"\vdots", color = ORANGE).shift(2.7*DOWN)
        self.bring_to_back(particle_2, particle_3, particle_4, dots, self.shade).play(FadeOut(self.shade), run_time = 0.5, rate_func = rush_from)
        self.wait(3, 12) #那么正好有整数段波节的那些驻波才能存在
        self.wait(0, 24) #（空闲）

        arrows_l = [Arrow((1.8-1.2*i)*UP + PI/2*LEFT + 0.2*LEFT, (1.8-1.2*i)*UP + PI/2*LEFT + 0.2*LEFT + (0.5*(i+1)*LEFT), color = colors[i], buff = 0) for i in range(4)] + [Arrow().shift(5*DOWN)]
        arrows_r = [Arrow((1.8-1.2*i)*UP + PI/2*RIGHT + 0.2*RIGHT, (1.8-1.2*i)*UP + PI/2*RIGHT + 0.2*RIGHT + (0.5*(i+1)*RIGHT), color = colors[i], buff = 0) for i in range(4)] + [Arrow().shift(5*DOWN)]
        
        texts = r"F", r"2F", r"3F", r"4F"
        texts_l = [MTex(texts[i], color = colors[i]).scale(0.6).next_to(arrows_l[i], UP, buff = 0.1) for i in range(4)] + [MTex(r"\vdots", color = ORANGE).shift(2.7*DOWN + PI/2*LEFT + 0.2*LEFT + LEFT)]
        texts_r = [MTex(texts[i], color = colors[i]).scale(0.6).next_to(arrows_r[i], UP, buff = 0.1) for i in range(4)] + [MTex(r"\vdots", color = ORANGE).shift(2.7*DOWN + PI/2*RIGHT + 0.2*RIGHT + RIGHT)]
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows_l], run_time = 2, lag_ratio = 1/4), 
                  LaggedStart(*[GrowArrow(arrow) for arrow in arrows_r], run_time = 2, lag_ratio = 1/4), 
                  LaggedStart(*[Write(text) for text in texts_l], run_time = 2, lag_ratio = 1/4), 
                  LaggedStart(*[Write(text) for text in texts_r], run_time = 2, lag_ratio = 1/4))
        self.wait(2, 14) #每一个这样的驻波会因为复杂的量子效应产生对金属板的作用力
        self.wait(0, 16) #（空闲）
        self.wait(2, 4) #这个力是一个斥力
        self.wait(2, 2) #大小正比于波节的个数
        self.play(IndicateAround(texts_l[0], stroke_color = WHITE), IndicateAround(texts_r[0], stroke_color = WHITE))
        self.wait(0, 18) #比如说一节会产生1F的推力
        self.play(IndicateAround(texts_l[1], stroke_color = WHITE), IndicateAround(texts_r[1], stroke_color = WHITE))
        self.wait(0, 27) #两节是2F的推力 等等等等依此类推
        self.wait(0, 18) #（空闲）

        camera = self.camera.frame
        text = MTex(r"F_{\text{合}}&={F}+2F+3F+4F+\cdots\\&=F(1+2+3+4+\cdots)", tex_to_color_map = {r"F": BLUE, **{str(i+1): colors[i] for i in range(4)}, r"{F}": colors[0], r"2F": colors[1], r"3F": colors[2], r"4F": colors[3], r"F_{\text{合}}": BLUE, r"\cdots": ORANGE}).scale(0.8).shift(6*RIGHT)
        part_1, part_2 = text[:17], text[17:]
        part_2.shift(0.2*DOWN)
        self.play(*[mob.animate.shift(3*RIGHT) for mob in [title, titleline, camera]], OverFadeIn(part_1), run_time = 2)
        self.wait(2, 24) #所以 要计算这个合力 就是把所有满足这些条件的波产生的力加起来
        self.play(Write(part_2), run_time = 1)
        self.wait(3, 6) #这样 我们就会写出某一个1+2+3+……这样的无穷求和
        self.wait(0, 21) #（空闲）

        self.wait(1, 4) #这个求和是发散的
        self.wait(1, 18) #所以你可能会以为
        self.wait(2, 16) #这种排斥力会把两块板瞬间弹飞
        self.wait(0, 21) #（空闲）

        offset = 6.5*RIGHT
        board_left_2, board_right_2 = board_left.copy().shift(offset), board_right.copy().shift(offset)
        particles = []
        for i in range(4):
            particle = WaveFunction(FunctionGraph(lambda t: 0.5*np.sin((i+1)*(t+PI/2)), [-PI/2, PI/2, PI/100], color = colors[i], stroke_width = 6), offset = (1.8-1.2*i)*UP + offset)
            particle.add_updater(particle_updater((i+1)*1.5))
            particles.append(particle)
        dots_r = MTex(r"\vdots", color = ORANGE).shift(2.7*DOWN + offset)
        self.play(FadeOut(text), run_time = 0.5, rate_func = rush_into)
        self.bring_to_back(*particles, dots_r, board_left_2, board_right_2, self.shade).play(FadeOut(self.shade), run_time = 0.5, rate_func = rush_from)
        self.wait(3, 4) #科学家通过实验测量和其他理论方法计算
        
        arrow_l = Arrow(1/6*LEFT + PI/2*LEFT + 0.2*LEFT, PI/2*LEFT + 0.2*LEFT, color = BLUE, buff = 0).shift(offset)
        arrow_r = Arrow(1/6*RIGHT + PI/2*RIGHT + 0.2*RIGHT, PI/2*RIGHT + 0.2*RIGHT, color = BLUE, buff = 0).shift(offset)
        text_l = MTex(r"\frac{1}{12}F", color = BLUE).scale(0.6).next_to(PI/2*LEFT + 0.2*LEFT + offset, LEFT)
        text_r = MTex(r"\frac{1}{12}F", color = BLUE).scale(0.6).next_to(PI/2*RIGHT + 0.2*RIGHT + offset, RIGHT)
        self.play(FadeIn(arrow_l, 0.2*RIGHT), FadeIn(arrow_r, 0.2*LEFT), run_time = 0.5, rate_func = rush_from)
        self.wait(2, 21-15) #发现这个合力居然是吸引的
        self.play(Write(text_l), Write(text_r))
        self.wait(1, 12) #而它的大小等于F/12
        self.wait(0, 28) #（空闲）

        self.wait(1, 18) #这仿佛就是在说
        self.wait(2, 25) #全部自然数的和应该等于-1/12
        self.wait(0, 15) #（空闲）
        self.wait(4, 16) #这就是支持者经常用来证明这个式子成立的“卡西米尔效应”
        self.wait(10, 0) #（空闲）

#################################################################### 
        
def zeta(z):
    max_norm = FRAME_X_RADIUS
    try:
        return np.complex(mpmath.zeta(z))
    except:
        return np.complex(max_norm, 0)

class Patch8_1(FrameScene):
    def construct(self):
        # lines_h = [Line(5.5*ratio*RIGHT, 5.5*ratio*LEFT, stroke_width = 1 if i%2 else 2, color = TEAL_E if i else TEAL, depth_test = True).shift(i*ratio*UP + 0.02*OUT).apply_matrix(matrix) for i in range(-5, 6)]
        # lines_v = [Line(5.5*ratio*UP, 5.5*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = TEAL_E if i else TEAL, depth_test = True).shift(i*ratio*RIGHT + 0.02*OUT).apply_matrix(matrix) for i in range(-5, 6)]
        # lines_h = [Line(RIGHT_SIDE, LEFT_SIDE, stroke_width = 2, color = RED).shift(i*ratio*UP).insert_n_curves(int(16/(min(1, max(abs(i*ratio)**2, 0.01))))-1) for i in range(-20, 21)]
        # lines_v = [Line(TOP, BOTTOM, stroke_width = 2, color = YELLOW).shift(i*ratio*RIGHT).insert_n_curves(int(16/(min(1, max((i*ratio)**4, 0.0001))))-1) for i in range(-20, 21)]
        # lines_h = [Line(RIGHT_SIDE, LEFT_SIDE, stroke_width = 2, color = RED).shift(i*ratio*UP).insert_n_curves(511) for i in range(-20, 21)]
        # lines_v = [Line(TOP, BOTTOM, stroke_width = 2, color = YELLOW).shift(i*ratio*RIGHT).insert_n_curves(511) for i in range(-20, 21)]
        # grid = VGroup(*lines_h, *lines_v)
        # back = ComplexPlane(faded_line_ratio = 9)
        # self.add(back, grid)
        # self.play(grid.animate.apply_complex_function(zeta), run_time = 5)
        # self.wait()
        ratio = 0.1
        line_h, line_v = Line(RIGHT_SIDE, RIGHT, stroke_width = 3, color = YELLOW).insert_n_curves(127), Line(TOP, BOTTOM, stroke_width = 3, color = RED).insert_n_curves(127)
        lines_h = [line_h.copy().shift(i*ratio*UP) for i in range(-20, 21)]
        for i in range(10, 31):
            lines_h[i].insert_n_curves(128)
        for i in range(15, 26):
            lines_h[i].insert_n_curves(256)
        for i in range(18, 23):
            lines_h[i].insert_n_curves(512)
        lines_v = [line_v.copy().shift(i*ratio*RIGHT) for i in range(10, 41)]
        for i in range(10):
            lines_v[i].insert_n_curves(128)
        for i in range(5):
            lines_v[i].insert_n_curves(256)
        for i in range(3):
            lines_v[i].insert_n_curves(512)
        extra_h = [line_h.copy().shift(i*0.5*UP) for i in (5, 6, 7, 8, -5, -6, -7, -8)]
        extra_v = [line_v.copy().shift(i*0.5*RIGHT) for i in range(9, 15)]
        grid_r = VGroup(*lines_h, *extra_h, *lines_v, *extra_v)
        grid_r.apply_complex_function(zeta)
        back = ComplexPlane(faded_line_ratio = 1)
        self.add(back, grid_r).wait(3)

        line_h, line_v = Line(LEFT_SIDE, RIGHT, stroke_width = 3, color = PURPLE).insert_n_curves(127), Line(TOP, BOTTOM, stroke_width = 3, color = BLUE).insert_n_curves(127)
        lines_h = [line_h.copy().shift(i*ratio*UP) for i in range(-20, 21)]
        lines_v = [line_v.copy().shift(i*ratio*RIGHT) for i in range(-20, 10)]
        for i in range(20, 30):
            lines_v[i].insert_n_curves(128)
        for i in range(25, 30):
            lines_v[i].insert_n_curves(256)
        for i in range(27, 30):
            lines_v[i].insert_n_curves(512)
        # all_h = VGroup(*[line_h.copy().shift(i*0.5*UP) for i in [-8, -7, -6, -5]], *lines_h, *[line_h.copy().shift(i*0.5*UP) for i in [5, 6, 7, 8]]).apply_complex_function(zeta)
        # all_v = VGroup(*[line_v.copy().shift(i*0.5*UP) for i in range(-14, -4)], *lines_v).apply_complex_function(zeta)
        all_h = VGroup(*[line_h.copy().shift(i*0.5*UP) for i in [-8, -7, -6, -5]], *lines_h, *[line_h.copy().shift(i*0.5*UP) for i in [5, 6, 7, 8]]).apply_complex_function(zeta)
        all_v = VGroup(*lines_v).apply_complex_function(zeta)
        self.play(ShowIncreasingSubsets(all_h), ShowIncreasingSubsets(all_v), run_time = 5, rate_func = linear)
        self.wait()

class Test_8(FrameScene):
    def construct(self):
        page = ImageMobject("page.jpg", height = 6)
        mtex = MTex(r"\sum_{n=1}^{\infty}n=-\frac{1}{12}", color = RED).shift(0.105*LEFT + 0.675*DOWN).scale(0.305)
        self.add(page, mtex)

class Video_8(FrameScene):
    def construct(self):
        page = ImageMobject("page.jpg", height = 6)
        mtex = MTex(r"\sum_{n=1}^{\infty}n=-\frac{1}{12}", color = BLACK).shift(0.105*LEFT + 0.675*DOWN).scale(0.305).save_state()
        surr = SurroundingRectangle(mtex, color = YELLOW_E)
        back = surr.copy().set_fill(color = WHITE, opacity = 1).set_stroke(color = YELLOW).save_state().set_stroke(color = YELLOW_E)
        self.play(FadeIn(page, 0.5*UP))
        self.wait()
        self.play(ShowCreation(surr), FadeIn(mtex))
        self.wait()
        alpha = ValueTracker(0.0)
        def lines_updater(mob: VGroup):
            color = interpolate_color(YELLOW_E, YELLOW, alpha.get_value())
            mob[0].put_start_and_end_on(surr.get_corner(UR), back.get_corner(UL)).set_stroke(color = [YELLOW_E, color])
            mob[1].put_start_and_end_on(surr.get_corner(DR), back.get_corner(DL)).set_stroke(color = [YELLOW_E, color])
        lines = VGroup(Line(color = YELLOW), Line(color = YELLOW)).add_updater(lines_updater)
        self.add(lines, back, mtex).play(alpha.animate.set_value(1.0), *[mob.animate.restore().scale(1/0.305).shift(7*RIGHT).set_y(0) for mob in [back, mtex]], self.camera.frame.animate.shift(2.5*RIGHT))
        lines.clear_updaters()
        self.wait()
        self.fade_out()
        self.wait()

        self.camera.frame.shift(2.5*LEFT)
        zeta_right = MTex(r"\zeta(z)=\frac{1}{1^z}+\frac{1}{2^z}+\frac{1}{3^z}+\frac{1}{4^z}+\frac{1}{5^z}+\frac{1}{6^z}+\cdots,\ \Re(z)> 1", tex_to_color_map = {r"z": GREEN}).shift(3*UP)
        zeta_right[0].scale(1.5, about_point = zeta_right[0].get_right()).set_fill(color = [RED, ORANGE, YELLOW])
        surr = Rectangle(height = 4.4, width = 64/9+0.4).shift(0.5*DOWN + 3*LEFT)
        self.add(zeta_right[0]).play(Write(zeta_right[1:]), ShowCreation(surr))
        self.wait()

        zeta_left = MTex(r"\zeta(z)=???, \ \Re(z)\le 1", tex_to_color_map = {r"z": GREEN}).shift(1.8*UP + 4*RIGHT)
        zeta_n1 = MTex(r"\zeta(-1)=-\frac{1}{12}", tex_to_color_map = {r"-1": GREEN}).shift(0.8*UP + 4*RIGHT)
        zeta_left[0].scale(1.5, about_point = zeta_left[0].get_right()).set_fill(color = [BLUE, PURPLE_B])
        zeta_n1[0].scale(1.5, about_point = zeta_n1[0].get_right()).set_fill(color = [BLUE, PURPLE_B])
        self.add(zeta_left[0]).play(Write(zeta_left[1:]))
        self.wait(5)
        self.add(zeta_n1[0]).play(Write(zeta_n1[1:]))
        self.wait()

        cover = BVCover(r"cover.jpg", r"BV1tx411y7VG").shift(4*RIGHT + 1.6*DOWN)
        self.play(FadeIn(cover, 0.5*LEFT))
        self.wait()

#################################################################### 

class Video_9(FrameScene):
    def construct(self):
        camera = self.camera.frame.shift(DOWN)
        frog = SVGMobject("frog_face.svg", stroke_width = 0, height = 2).shift(DOWN)
        self.wait()
        self.play(Write(frog))
        self.wait()
        bubbles = [Circle(radius = 0.15 + 0.05*i, stroke_color = WHITE, fill_color = BLACK, fill_opacity = 1).shift(i*(0.2 + 0.04*i)*UP + i*(10-i)*0.02*RIGHT) for i in range(4)]
        bubbles.append(Ellipse(height = 2, width = 3.5, stroke_color = WHITE, fill_color = BLACK, fill_opacity = 1).shift(2*UP))
        symbols = MTex(r"+-\times\not\divisionsymbol")
        symbols.set_submobjects([*symbols[:3], symbols[4], symbols[3]])
        symbols[0].scale(1.5).set_color(BLUE).move_to(2.3*UP + 0.9*LEFT)
        symbols[1].scale(1.5).set_color(ORANGE).move_to(2.3*UP + 0.3*RIGHT)
        symbols[2].scale(1.5).set_color(GREEN).move_to(1.7*UP + 0.3*LEFT)
        symbols[3].scale(1.5).set_color(GREY).move_to(1.7*UP + 0.9*RIGHT)
        symbols[4].set_color(RED).move_to(1.7*UP + 0.9*RIGHT)
        self.add(*bubbles).play(LaggedStart(*[GrowFromPoint(mob, bubbles[0].get_center()) for i, mob in enumerate(bubbles)], lag_ratio = 1/4, rate_fun = linear, group = VGroup(), remover = True), 
                               camera.animate.shift(UP), )
        self.play(Write(symbols))
        self.wait()

        rules = [frog, *bubbles, symbols]
        polynomial = MTex(r"f(x)=a_0+a_1x+a_2x^2+\cdots+a_nx^n", tex_to_color_map = {r"x": YELLOW}).scale(0.8).shift(2.5*UP + 2.5*RIGHT)
        self.play(*[mob.animate.shift(4*LEFT) for mob in rules], OverFadeIn(polynomial, 2*LEFT), run_time = 2)
        self.wait()

        sin = MTex(r"\sin(x)=x-\frac{x^3}{6}+\frac{x^5}{120}-\frac{x^7}{5040}+\cdots", tex_to_color_map = {r"x": YELLOW}).scale(0.8).shift(UP + 2.5*RIGHT)
        cos = MTex(r"\cos(x)=1-\frac{x^2}{2}+\frac{x^4}{24}-\frac{x^6}{720}+\cdots", tex_to_color_map = {r"x": YELLOW}).scale(0.8)
        cos.shift(sin[6].get_center() - cos[6].get_center() + 1.2*DOWN)
        exp = MTex(r"\exp(x)=1+x+\frac{x^2}{2}+\frac{x^3}{6}+\cdots", tex_to_color_map = {r"x": YELLOW}).scale(0.8)
        exp.shift(cos[6].get_center() - exp[6].get_center() + 1.2*DOWN)
        self.play(Write(sin))
        self.wait()
        self.play(FadeIn(cos, 0.3*UP), FadeIn(exp, 0.3*UP, delay = 0.2))
        self.wait()

        series = MTex(r"f(x)=a_0+a_1x+a_2x^2+\cdots", tex_to_color_map = {r"x": YELLOW}).scale(0.8).shift(1.8*UP + 4*RIGHT)
        bubbles[-1].generate_target().shift(8*RIGHT).set_width(5.5, stretch = True).set_height(1.5, stretch = True).shift(0.2*DOWN)
        arrow = Arrow(2*LEFT, 2*RIGHT).shift(2.5*LEFT + 2.5*UP)
        answer = MTex(r"\frac{1}{1-x}", tex_to_color_map = {r"x": YELLOW}).shift(2.5*LEFT + 2.5*UP)
        block = SurroundingRectangle(answer, stroke_color = WHITE, fill_opacity = 1, fill_color = BLACK)
        mysterious = MTex(r"f(x)", tex_to_color_map = {r"x": YELLOW}).shift(2.5*LEFT + 2.5*UP)
        self.bring_to_back(arrow, block, mysterious, self.shade).play(*[mob.animate.shift(8*RIGHT) for mob in [frog, *bubbles[:-1]]], MoveToTarget(bubbles[-1]), 
                  OverFadeOut(symbols, 8*RIGHT + 0.2*DOWN), *[OverFadeOut(mob, 6*RIGHT) for mob in [polynomial, sin, cos, exp]], 
                  OverFadeIn(series, 8*RIGHT + 0.2*DOWN), OverFadeOut(self.shade), 
                  *[mob.shift(6*LEFT).animate.shift(6*RIGHT) for mob in [arrow, block, mysterious]], run_time = 2)
        self.wait()

        geometric = MTex(r"f(x)=1+x+x^2+x^3+x^4+\cdots", tex_to_color_map = {(r"1", r"x"): YELLOW}).scale(0.8).shift(2.5*LEFT + 1*UP)
        left, right = MTex(r"\frac{1}{2}", color = YELLOW).scale(0.8).next_to(arrow, LEFT), MTex(r"2").scale(0.8).next_to(arrow, RIGHT)
        correct = MTex(r"f\left(\frac{1}{2}\right)=1+\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\cdots", tex_to_color_map = {(r"1", r"\frac{1}{2}", r"\frac{1}{4}", r"\frac{1}{8}"): YELLOW}).scale(0.8)
        correct.shift(geometric[4].get_center() - correct[6].get_center() + 1.2*DOWN)
        self.play(Write(geometric))
        self.wait()
        
        blocks = []
        ratio = 1.5
        for i in range(12):
            w, h = ratio*2**(-(i//2)), ratio*2**(-((i+1)//2))
            rec = Rectangle(height = h, width = w).add(MTex(r"\frac{1}{"+str(2**i)+r"}" if i else r"1", color = YELLOW).set_height(height = min(h*0.75, 1)))
            rec.next_to(1.25*LEFT + 2.5*DOWN, UL, buff = 0).shift(h*UP if i%2 else w*LEFT)
            blocks.append(rec)
        blocks.append(blocks[-1].copy().set_submobjects([]).next_to(1.25*LEFT + 2.5*DOWN, UL, buff = 0))
        self.play(FadeIn(left, 0.2*RIGHT), Write(correct), LaggedStart(*[FadeIn(mob) for mob in blocks], lag_ratio = 0.2, rate_func = rush_into, run_time = 2))
        self.play(FadeIn(right, 0.2*RIGHT))
        self.wait()

        self.bring_to_back(left, right, correct, *blocks, self.shade).play(FadeIn(self.shade))
        self.remove(left, right, correct, *blocks, self.shade).wait()

        left, right = MTex(r"2", color = YELLOW).scale(0.8).next_to(arrow, LEFT), MTex(r"-1", color = RED).scale(0.8).next_to(arrow, RIGHT)
        incorrect = MTex(r"f\left(2\right)=1+2+4+8+\cdots", tex_to_color_map = {(r"1", r"2", r"4", r"8"): YELLOW}).scale(0.8)
        incorrect.shift(geometric[4].get_center() - incorrect[4].get_center() + 1.2*DOWN)
        self.play(FadeIn(left, 0.2*RIGHT), Write(incorrect))
        self.wait()
        self.play(Write(right))
        self.play(IndicateAround(right))
        self.wait()

        nonsense = MTex(r"???", color = RED).set_stroke(**stroke_dic).rotate(PI/8).scale(2).move_to(series)
        self.play(Write(nonsense), series.animate.set_fill(opacity = 0.5))
        self.wait()

        self.play(Flip(mysterious.save_state(), answer.scale(0.9), dim = 1), right.animate.set_color(WHITE), FadeOut(incorrect))
        self.wait()
        correct = MTex(r"\frac{1}{1-2}=-1", tex_to_color_map = {r"2": YELLOW}).scale(0.8).shift(2.5*LEFT)
        self.play(Write(correct))
        self.wait()
        self.play(IndicateAround(geometric))
        self.wait()

        region = MTex(r"(-1<x<1)", tex_to_color_map = {r"x": YELLOW}).scale(0.8).next_to(geometric, DOWN)
        incorrect.set_y(-1)
        equation = MTex(r"1+2+4+8+\cdots=-1", tex_to_color_map = {(r"1", r"2", r"4", r"8"): YELLOW}).scale(0.8).move_to(series)
        self.remove(correct, series, nonsense).add(incorrect, region).play(FadeOut(self.shade))
        self.wait()
        self.play(Write(equation))
        self.wait()
        self.play(nonsense.save_state().scale(3).set_opacity(0).animate.restore(), rate_func = rush_into)
        self.wait()

class Video9_2(FrameScene):
    def construct(self):
        offset = 4*LEFT + 2.5*DOWN
        axis_x, axis_y = Arrow(1.5*LEFT, 1.5*RIGHT, stroke_width = 3, buff = 0).shift(offset), Arrow(0.5*DOWN, 5*UP, stroke_width = 3, buff = 0).shift(offset)
        graph = FunctionGraph(lambda t: 1/(1-t), [-1.5, 0.99, 0.01]).shift(offset)
        func = MTex(r"f(x)=\frac{1}{1-x}", tex_to_color_map = {r"x": YELLOW}).scale(0.8).next_to(axis_y, UP).shift(0.5*LEFT).set_stroke(**stroke_dic)
        self.add(axis_x, axis_y, graph, func)

        colors = [GREEN, TEAL, BLUE, PURPLE_B, RED, ORANGE] + [GREEN_E, TEAL_E, BLUE_E, PURPLE_E, RED_E, interpolate_color(ORANGE, BLACK, 0.5)]
        texs = r"f(x)=", r"1+", r"{x}+", r"x^2+", r"x^3+", r"x^4+", r"x^5+", r"\cdots"
        func_1 = MTex(r"f(x)=1+{x}+x^2+x^3+x^4+x^5+\cdots", isolate = [r"+", *texs], tex_to_color_map = {r"x": YELLOW, r"1": colors[0], r"{x}": colors[1], **{r"x^"+str(i): colors[i] for i in range(2, 6)}}).next_to(LEFT + 2.5*UP)
        adds = func_1.get_parts_by_tex(r"+")
        parts = [func_1.get_part_by_tex(tex) for tex in texs]
        parts[-1].save_state().shift((adds[0].get_x() - adds[-1].get_x())*RIGHT)
        def taylors(order):
            def util(t: float):
                sum = 1
                for _ in range(order):
                    sum = 1+sum*t
                return sum
            return util
        curves = [FunctionGraph(taylors(i), [-1.5, 1.5, 0.01], color = colors[i if i < 6 else i%6+6], stroke_width = 2).shift(offset) for i in range(50)]
        curve = VMobject(color = WHITE, stroke_width = 4).set_points(curves[0].get_points())
        self.add(curve).play(ShowCreation(curve, start = 0.5), Write(VGroup(parts[0], parts[1], parts[-1])))
        self.wait()
        self.bring_to_back(curves[0]).play(curve.animate.set_points(curves[1].get_points()), GrowFromPoint(parts[2], parts[-1].get_left()), parts[-1].animate.shift((adds[1].get_x() - adds[0].get_x())*RIGHT))
        self.wait()
        self.bring_to_back(curves[1]).play(curve.animate.set_points(curves[2].get_points()), GrowFromPoint(parts[3], parts[-1].get_left()), parts[-1].animate.shift((adds[2].get_x() - adds[1].get_x())*RIGHT))
        self.wait()
        self.bring_to_back(curves[2]).play(curve.animate.set_points(curves[3].get_points()), GrowFromPoint(parts[4], parts[-1].get_left()), parts[-1].animate.shift((adds[3].get_x() - adds[2].get_x())*RIGHT))
        self.wait()
        self.bring_to_back(curves[3]).play(curve.animate.set_points(curves[4].get_points()), GrowFromPoint(parts[5], parts[-1].get_left()), parts[-1].animate.shift((adds[4].get_x() - adds[3].get_x())*RIGHT))
        self.wait()
        self.bring_to_back(curves[4]).play(curve.animate.set_points(curves[5].get_points()), GrowFromPoint(parts[6], parts[-1].get_left()), parts[-1].animate.shift((adds[5].get_x() - adds[4].get_x())*RIGHT))
        self.wait()
        self.bring_to_back(curves[5]).play(curve.animating(remover = True).set_stroke(opacity = 0, width = 0), parts[-1].animate.restore())
        self.wait()

        sum_up = MTex(r"=\frac{1-x^n}{1-x}", tex_to_color_map = {r"x": YELLOW, r"n": RED})
        sum_up.shift(func_1[4].get_center() - sum_up[0].get_center() + 1.5*DOWN)
        self.play(Write(sum_up))
        self.wait()

        lim = MTex(r"\lim_{{n}\to\infty}\frac{1-x^{n}}{1-x}=\frac{1}{1-x}(-1<x<1)", tex_to_color_map = {r"x": YELLOW, r"{n}": RED}).shift(2.5*RIGHT + DOWN)
        line_l, line_r = DashedLine(0.5*DOWN, 3*UP).shift(LEFT + offset), DashedLine(0.5*DOWN, 6.5*UP).shift(RIGHT + offset)
        self.play(FadeIn(lim), ShowCreation(line_l), ShowCreation(line_r))
        self.wait()

        for i in range(6, 50):
            self.bring_to_back(curves[i])
            self.wait(0, 2)
        self.wait()
        
class Video_10(FrameScene):
    def construct(self):
        func_1 = MTex(r"\frac{1}{1-x}", tex_to_color_map = {r"x": YELLOW}).shift(2*UP + 4*LEFT)
        series_1 = MTex(r"1+x+x^2+x^3+x^4+\cdots", tex_to_color_map = {r"x": YELLOW}).scale(0.8).next_to(2*UP + 2*LEFT)
        region_1 = MTex(r"(-1<x<1)", tex_to_color_map = {r"x": YELLOW}).scale(0.8).next_to(2*UP + 3.5*RIGHT)
        
        func_2 = MTex(r"\zeta(z)", tex_to_color_map = {r"z": YELLOW}).shift(DOWN + 4*LEFT)
        series_2 = MTex(r"\frac{1}{1^z}+\frac{1}{2^z}+\frac{1}{3^z}+\frac{1}{4^z}+\cdots", tex_to_color_map = {r"z": YELLOW}).scale(0.8).next_to(DOWN + 2*LEFT)
        region_2 = MTex(r"(\Re(z)>1)", tex_to_color_map = {r"z": YELLOW}).scale(0.8).next_to(DOWN + 3.5*RIGHT)
        self.add(func_1, series_1, func_2, series_2).wait()
        self.play(Write(region_1), Write(region_2))
        self.wait()

        equation_1 = MTex(r"-1={1}+2+4+8+\cdots", tex_to_color_map = {r"-1": RED, (r"{1}", r"2", r"4", r"8"): YELLOW}).scale(0.8)
        equation_1.shift(1*UP + 2.5*LEFT - equation_1[2].get_center())
        equation_1.insert_submobject(3, MTex(r"?", color = RED).set_stroke(**stroke_dic).move_to(equation_1[2]))
        equation_2 = MTex(r"-\frac{1}{12}={1}+{2}+3+4+\cdots", tex_to_color_map = {(r"{1}", r"{2}", r"3", r"4"): YELLOW, r"-\frac{1}{12}": RED}).scale(0.8)
        equation_2.shift(2*DOWN + 2.5*LEFT - equation_2[5].get_center())
        equation_2.insert_submobject(6, MTex(r"?", color = RED).set_stroke(**stroke_dic).move_to(equation_2[5]))
        self.play(Write(equation_1), Write(equation_2))
        self.wait()
                
#################################################################### 

class Video_11(FrameScene):
    def construct(self):
        frog = SVGMobject("frog_face.svg", stroke_width = 0, height = 2)
        special = frog.copy().shift(0.5*DOWN + 4*LEFT)
        special[5].set_color(ORANGE), special[8].set_color(ORANGE), special[1].set_color(GREY_E)
        idea = SVGMobject("idea.svg", stroke_width = 0, height = 1.5, color = YELLOW).shift(1.7*UP + 4*LEFT)
        idea[0].set_color(WHITE)
        self.add(special).wait()
        self.play(FadeIn(idea, 0.5*UP))
        self.wait()

        series_u = VGroup(MTex(r"S", color = BLUE), MTex(r"="), MTex(r"1", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"2", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"4", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"8", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"16", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"32", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"64", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"\cdots"))
        for i, mob in enumerate(series_u):
            mob.move_to((-1+0.55*i)*RIGHT + 3*UP)
        series_d = series_u.copy().shift(DOWN)
        series_d_2 = VGroup(MTex(r"2S", color = BLUE).shift(0.1*LEFT), MTex(r"="), MTex(r"2", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"4", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"8", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"16", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"32", color = PURPLE_A), MTex(r"+", color = GREEN_B), 
                                                                 MTex(r"64", color = GREEN_B), MTex(r"+", color = PURPLE_A), MTex(r"128", color = PURPLE_A), MTex(r"+", color = GREEN_B),
                                                                 MTex(r"\cdots"))
        for i, mob in enumerate(series_d_2):
            mob.shift((-1+0.55*i)*RIGHT + 2*UP)
        self.play(Write(series_u))
        self.wait()
        self.play(ReplacementTransform(series_u.copy(), series_d, lag_ratio = 0.05, run_time = 2))
        self.wait()
        self.play(LaggedStart(*[Flip(mob_1, mob_2, dim = 1) for mob_1, mob_2 in zip(series_d, series_d_2)], run_time = 2, lag_ratio = 0.1))
        self.wait()
        self.play(series_d[2:].animate.shift(1.1*RIGHT))
        self.wait()
        series_dd = VGroup(MTex(r"-S", color = BLUE).shift(0.1*LEFT), MTex(r"="), MTex(r"1", color = GREEN_B))
        subtract, equal = MTex(r"-")[0].rotate(PI/2).shift((-1+0.55)*RIGHT + 2.5*UP), MTex(r"=")[0].rotate(PI/2).shift((-1+0.55)*RIGHT + 1.5*UP)
        for i, mob in enumerate(series_dd):
            mob.shift((-1+0.55*i)*RIGHT + 1*UP)
        self.play(Write(subtract), Write(equal))
        self.play(FadeIn(series_dd, 0.5*DOWN))
        self.wait()

        frog_1, frog_2 = frog.copy().scale(0.6).shift(1.5*DOWN + 1*RIGHT), frog.copy().scale(0.6).shift(1.5*DOWN + 4.5*RIGHT)
        react_1, react_2 = MTex(r"!", color = RED).next_to(frog_1, UP), Text("", font = 'vanfont', color = RED)[0].scale(np.array([1, -1, 1]), min_scale_factor = -1).refresh_bounding_box().next_to(frog_2, UP)
        self.bring_to_back(frog_1, react_1, self.shade).play(*[mob.shift(0.5*DOWN).animate.shift(0.5*UP) for mob in [frog_1, react_1]], FadeOut(self.shade))
        self.wait()
        self.bring_to_back(frog_2, react_2, self.shade).play(*[mob.shift(0.5*DOWN).animate.shift(0.5*UP) for mob in [frog_2, react_2]], FadeOut(self.shade))
        self.wait()

class Video_12(FrameScene):
    def construct(self):
        func_1 = MTex(r"f(x)=1+x+x^2+x^3+x^4+x^5+x^6+x^7+x^8+x^9+\cdots", tex_to_color_map = {r"x": YELLOW}).next_to(4*LEFT + 3*UP, buff = 0)
        func_2 = MTex(r"xf(x)=x+x^2+x^3+x^4+x^5+x^6+x^7+x^8+x^9+\cdots", tex_to_color_map = {r"x": YELLOW})
        func_2[:6].shift(func_1[4].get_center() - func_2[5].get_center() + 1.25*DOWN)
        func_2[6:].shift(func_1[7].get_center() - func_2[6].get_center() + 1.25*DOWN)
        func_3 = MTex(r"(1-x)f(x)=1", tex_to_color_map = {r"x": YELLOW})
        func_3.shift(func_2[5].get_center() - func_3[-2].get_center() + 1.25*DOWN)
        subtract, equal = MTex(r"-")[0].rotate(PI/2).move_to(func_1[4].get_center() + 0.625*DOWN), MTex(r"=")[0].rotate(PI/2).move_to(func_2[5].get_center() + 0.625*DOWN)
        self.add(func_1).wait()
        self.play(FadeIn(func_2, 0.3*DOWN, lag_ratio = 0.03, run_time = 2), Write(VGroup(subtract, equal)))
        self.wait()
        self.play(FadeIn(func_3, 0.3*DOWN), func_1[4].animate.become(MTex(r"\sim", color = TEAL)[0].move_to(func_1[4])), func_2[5].animate.become(MTex(r"\sim", color = TEAL)[0].move_to(func_2[5])))
        self.wait()

        func_4 = MTex(r"f(x)=\frac{1}{1-x}", tex_to_color_map = {r"x": YELLOW}).shift(0.5*UP + RIGHT)
        equality = MTex(r"\Leftrightarrow").move_to((func_3.get_right() + func_4.get_left())/2)
        self.play(Write(equality), FadeIn(func_4, 0.3*LEFT))
        self.wait()

        equation_1 = MTex(r"\frac{1}{2}=f({-1})=1+1-1+1-1+1+1-1+1-1+1+1-1+1-1+\cdots", tex_to_color_map = {(r"1", r"{-1}"): YELLOW, r"\frac{1}{2}": BLUE})
        equation_1[9].become(MTex(r"\sim", color = TEAL)[0].move_to(equation_1[9]))
        equation_1.shift(func_3[-2].get_center() - equation_1[9].get_center() + 1.5*DOWN)
        equation_2 = MTex(r"-1=f(2)={1}+2+4+8+16+32+64+128+256+\cdots", tex_to_color_map = {(r"{1}", *(str(2**i) for i in range(1, 9))): YELLOW, r"-1": BLUE})
        equation_2[7].become(MTex(r"\sim", color = TEAL)[0].move_to(equation_2[7]))
        equation_2.shift(equation_1[9].get_center() - equation_2[7].get_center() + 1.0*DOWN)
        self.play(FadeIn(equation_1, 0.3*UP))
        self.wait()
        self.play(FadeIn(equation_2, 0.3*UP))
        self.wait()
        
class Video_13(FrameScene):
    def construct(self):
        line = Line(4*UP, 4*DOWN)
        dots = [Dot(radius = 0.2, fill_color = BLACK, stroke_width = 4, stroke_color = WHITE).shift((2.5-1.25*i)*UP) for i in range(5)]
        mtex_1 = MTex(r"A=\frac{1}{2}\sim 1-1+1-1+1-1+1-1+\cdots", tex_to_color_map = {r"1": YELLOW, r"\frac{1}{2}": BLUE, r"A": BLUE, r"\sim": TEAL}).scale(0.8).next_to(dots[0], buff = 0.5)
        rectangle_1 = SurroundingRectangle(mtex_1, buff = 0.2).add(mtex_1)
        line_1 = Line(dots[0], rectangle_1)
        mtex_2 = MTex(r"B=\frac1{4}\sim {1}-2+3-4+5-6+7-8+\cdots", tex_to_color_map = {(r"{1}", *(str(i) for i in range(2, 9))): YELLOW, r"\frac1{4}": BLUE, r"B": BLUE, r"\sim": TEAL}).scale(0.8).next_to(dots[2], buff = 0.5)
        rectangle_2 = SurroundingRectangle(mtex_2, buff = 0.2).add(mtex_2)
        line_2 = Line(dots[2], rectangle_2)
        mtex_3 = MTex(r"S=-\frac1{12}\sim {1}+{2}+3+4+5+6+7+8+\cdots", tex_to_color_map = {(r"{1}", r"{2}", *(str(i) for i in range(3, 9))): YELLOW, r"-\frac1{12}": BLUE, r"S": BLUE, r"\sim": TEAL}).scale(0.8).next_to(dots[4], buff = 0.5)
        rectangle_3 = SurroundingRectangle(mtex_3, buff = 0.2).add(mtex_3)
        line_3 = Line(dots[4], rectangle_3)

        formula_1 = MTex(r"f(x)=\frac{1}{1-x}\sim&\ 1+x+x^2+\cdots\\g(x)=\frac{1}{(1-x)^2}\sim&\ 1+2x+3x^2+\cdots\\f(x)=&\ (1-x)g(x)\\A=f(-1)=&\ {2}g(-1)={2}B", 
                       tex_to_color_map = {(r"x", r"-1"): YELLOW, (r"A", r"B"): BLUE, r"\sim": TEAL}).scale(0.5).next_to(dots[1], LEFT, buff = 0.5)
        rectangle_4 = SurroundingRectangle(formula_1, buff = 0.2).add(formula_1)
        line_4 = Line(dots[1], rectangle_4)
        formula_2 = MTex(r"\eta(z)\sim&\ \frac1{1^z}-\frac1{2^z}+\frac1{3^z}-\frac1{4^z}+\cdots\\\zeta(z)\sim&\ \frac1{1^z}+\frac1{2^z}+\frac1{3^z}+\frac1{4^z}+\cdots\\\eta(z)=&\ (1-z^{1-s})\zeta(z)\\B=\eta(-1)=&\ -3\zeta(-1)=-3S", 
                       tex_to_color_map = {(r"z", r"-1"): YELLOW, (r"B", r"S"): BLUE, r"\sim": TEAL}).scale(0.5).next_to(dots[3], LEFT, buff = 0.5)
        formula_2[56:].shift(0.7*RIGHT)
        rectangle_5 = SurroundingRectangle(formula_2.refresh_bounding_box(), buff = 0.2).add(formula_2)
        line_5 = Line(dots[3], rectangle_5)

        # self.add(line, *dots, rectangle_1, line_1, rectangle_2, line_2, rectangle_3, line_3, rectangle_4, line_4, rectangle_5, line_5)
        self.play(ShowCreation(line, run_time = 8, rate_func = linear), 
                  GrowFromCenter(dots[0], run_time = 0.5, delay = 1.5 ), ShowCreation(line_1, run_time = 0.5, delay = 2   , rate_func = rush_into), GrowFromEdge(rectangle_1, LEFT , delay = 2.5 , rate_func = rush_from), 
                  GrowFromCenter(dots[1], run_time = 0.5, delay = 2.75), ShowCreation(line_4, run_time = 0.5, delay = 3.25, rate_func = rush_into), GrowFromEdge(rectangle_4, RIGHT, delay = 3.75, rate_func = rush_from), 
                  GrowFromCenter(dots[2], run_time = 0.5, delay = 4   ), ShowCreation(line_2, run_time = 0.5, delay = 4.5 , rate_func = rush_into), GrowFromEdge(rectangle_2, LEFT , delay = 5   , rate_func = rush_from), 
                  GrowFromCenter(dots[3], run_time = 0.5, delay = 5.25), ShowCreation(line_5, run_time = 0.5, delay = 5.75, rate_func = rush_into), GrowFromEdge(rectangle_5, RIGHT, delay = 6.25, rate_func = rush_from), 
                  GrowFromCenter(dots[4], run_time = 0.5, delay = 6.5 ), ShowCreation(line_3, run_time = 0.5, delay = 6   , rate_func = rush_into), GrowFromEdge(rectangle_3, LEFT , delay = 7.5 , rate_func = rush_from), 
                  )
        self.wait()
        self.play(IndicateAround(formula_1[21:47], rect_kwargs = {"stroke_color": RED}), IndicateAround(formula_2[:28], rect_kwargs = {"stroke_color": RED}))
        self.wait()
        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        