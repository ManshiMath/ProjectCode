from __future__ import annotations

from manimlib import *
import numpy as np

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
        a = MTex(r"a=2", tex_to_color_map = {r"a": BLUE, r"2": GREEN}).shift(3*UP + 1*LEFT)
        p = MTex(r"p=11", tex_to_color_map = {r"p":PURPLE_B, r"11": PURPLE_B}).shift(3*UP + 1*RIGHT)
        self.play(Write(a), Write(p))
        self.wait()

        powers = [MTex(r"a^{"+str(i)+r"}", tex_to_color_map = {r"a": BLUE, str(i): YELLOW_D}).scale(1.1).shift(1.5*UP + (i-5)*1.2*RIGHT) for i in range(11)]
        # for i in range(11):
        #     powers.add(mod_powers[i][-2].copy().scale(0).move_to(powers[-1].get_right())).add(mod_powers[i][-1].copy().scale(0).move_to(powers[-1].get_right()))
        results = [MTex(str(2**i), color = LIME).shift(0.5*UP + (i-5)*1.2*RIGHT) for i in range(11)]
        backs = [Rectangle(width = 1.2, height = 2, stroke_width = 0, fill_opacity = 1, fill_color = BLACK if i%2 else GREY_E).shift(1*UP + (i-5)*1.2*RIGHT) for i in range(11)]
        line = Line(1*UP + 5.5*1.2*LEFT, 1*UP + 5.5*1.2*RIGHT, color = GREY)
        mod_powers = [MTex(r"a^{"+str(i)+r",\otimes}", tex_to_color_map = {r"a": BLUE, str(i): YELLOW_D, r"\otimes": RED}).scale(1.1).shift(DOWN + (i-5)*1.2*RIGHT) for i in range(11)]
        mod_results = [MTex(str(2**i%11), color = ORANGE).shift(2*DOWN + (i-5)*1.2*RIGHT) for i in range(11)]
        mod_backs = [Rectangle(width = 1.2, height = 2, stroke_width = 0, fill_opacity = 1, fill_color = BLACK if i%2 else GREY_E).shift(1.5*DOWN + (i-5)*1.2*RIGHT) for i in range(11)]
        mod_line = Line(1.5*DOWN + 5.5*1.2*LEFT, 1.5*DOWN + 5.5*1.2*RIGHT, color = GREY)
        self.play(LaggedStart(*[mob.save_state().scale(np.array([1, 0, 1])).animate.restore() for mob in backs], run_time = 2, lag_ratio = 0.1),
                  LaggedStart(*[FadeIn(mob, 0.2*UP) for mob in powers], run_time = 2, lag_ratio = 0.1), 
                  LaggedStart(*[FadeIn(mob, 0.2*DOWN) for mob in results], run_time = 2, lag_ratio = 0.1), 
                  ShowCreation(line, run_time = 1.5))
        self.wait()
        self.play(LaggedStart(*[mob.save_state().scale(np.array([1, 0, 1])).animate.restore() for mob in mod_backs], run_time = 2, lag_ratio = 0.1),
                  LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in mod_powers], run_time = 2, lag_ratio = 0.1), 
                  LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in mod_results], run_time = 2, lag_ratio = 0.1), 
                  ShowCreation(mod_line, run_time = 1.5))
        self.wait()
        # self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in backs_p], run_time = 2, lag_ratio = 0.1), 
        #           LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in backs_r], run_time = 2, lag_ratio = 0.1), 
        #           LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in powers], run_time = 2, lag_ratio = 0.1), 
        #           LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in results], run_time = 2, lag_ratio = 0.1))
        # self.wait()
        # self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in mod_backs_p], run_time = 2, lag_ratio = 0.1), 
        #           LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in mod_backs_r], run_time = 2, lag_ratio = 0.1), 
        #           LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in mod_powers], run_time = 2, lag_ratio = 0.1), 
        #           LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in mod_results], run_time = 2, lag_ratio = 0.1))
        # self.wait()

        module = MTex(r"1024\divisionsymbol11=93\cdots\cdots1", tex_to_color_map = {r"1": ORANGE, r"11": PURPLE_B, r"93": GREY, r"1024": LIME}).scale(0.8).shift(2.8*UP + 4.5*RIGHT)
        self.play(Write(module))
        self.wait()

        indicate = Rectangle(width = 1, height = 0.8, color = YELLOW).move_to(mod_results[10])
        self.play(ShowCreation(indicate))
        self.wait()

        a_3 = MTex(r"a=3", tex_to_color_map = {r"a": BLUE, r"3": GREEN}).shift(3*UP + 1*LEFT)
        results_3 = [MTex(str(3**i), color = LIME).shift(0.5*UP + (i-5)*1.2*RIGHT) for i in range(11)]
        for mob in results_3:
            mob.set_width(min(mob.get_width(), 1))
        mod_results_3 = [MTex(str(3**i%11), color = ORANGE).shift(2*DOWN + (i-5)*1.2*RIGHT) for i in range(11)]
        self.play(FadeOut(module), Flip(a[2], a_3[2], dim = 1), 
                  LaggedStart(*[Flip(results[i], results_3[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), 
                  LaggedStart(*[Flip(mod_results[i], mod_results_3[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), )
        self.wait()

        a_4 = MTex(r"a=4", tex_to_color_map = {r"a": BLUE, r"4": GREEN}).shift(3*UP + 1*LEFT)
        results_4 = [MTex(str(4**i), color = LIME).shift(0.5*UP + (i-5)*1.2*RIGHT) for i in range(11)]
        for mob in results_4:
            mob.set_width(min(mob.get_width(), 1))
        mod_results_4 = [MTex(str(4**i%11), color = ORANGE).shift(2*DOWN + (i-5)*1.2*RIGHT) for i in range(11)]
        self.play(Flip(a[2], a_4[2], dim = 1), 
                  LaggedStart(*[Flip(results[i], results_4[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), 
                  LaggedStart(*[Flip(mod_results[i], mod_results_4[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), )
        self.wait()

        a_5 = MTex(r"a=5", tex_to_color_map = {r"a": BLUE, r"5": GREEN}).shift(3*UP + 1*LEFT)
        results_5 = [MTex(str(5**i), color = LIME).shift(0.5*UP + (i-5)*1.2*RIGHT) for i in range(11)]
        for mob in results_5:
            mob.set_width(min(mob.get_width(), 1))
        mod_results_5 = [MTex(str(5**i%11), color = ORANGE).shift(2*DOWN + (i-5)*1.2*RIGHT) for i in range(11)]
        self.play(Flip(a[2], a_5[2], dim = 1), 
                  LaggedStart(*[Flip(results[i], results_5[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), 
                  LaggedStart(*[Flip(mod_results[i], mod_results_5[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), )
        self.wait()

        a_7 = MTex(r"a=7", tex_to_color_map = {r"a": BLUE, r"7": GREEN}).shift(3*UP + 1*LEFT)
        results_7 = [MTex(str(7**i), color = LIME).shift(0.5*UP + (i-5)*1.2*RIGHT) for i in range(11)]
        for mob in results_7:
            mob.set_width(min(mob.get_width(), 1))
        mod_results_7 = [MTex(str(7**i%11), color = ORANGE).shift(2*DOWN + (i-5)*1.2*RIGHT) for i in range(11)]
        self.play(Flip(a[2], a_7[2], dim = 1), 
                  LaggedStart(*[Flip(results[i], results_7[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), 
                  LaggedStart(*[Flip(mod_results[i], mod_results_7[i], dim = 1) for i in range(11)], run_time = 1.5, lag_ratio = 2/9), )
        self.wait()
        
#################################################################### 

class Video_2(FrameScene):
    def construct(self):
        title, titleline = Title("费马小定理"), TitleLine()
        self.play(Write(title), GrowFromCenter(titleline))
        self.wait()

        left = MTex(r"p\text{是素数}", tex_to_color_map = {r"p": PURPLE_B}).shift(2*UP + 2.5*LEFT)
        right = MTex(r"a \in \{1, 2, \cdots, p-1 \}", tex_to_color_map = {r"a": BLUE, (r"1", r"2", r"p-1"): GREEN}).shift(2*UP + 1.5*RIGHT)
        self.play(FadeIn(left, 0.5*UP))
        self.wait()
        self.play(FadeIn(right, 0.5*UP))
        self.wait()

        theorem = MTex(r"a^{p-1, \otimes}=1", tex_to_color_map = {r"a": BLUE, r"1": GREEN, r"p-1": YELLOW_D, r"\otimes": RED}).scale(1.2)
        surr = SurroundingRectangle(theorem, buff = 0.3)
        self.play(Write(theorem), ShowCreation(surr))
        self.wait()

        difinition_1 = MTexText(r"$\bullet\ a$与$b$除以$p$余数相同", tex_to_color_map = {(r"a", r"b"): BLUE, r"p": PURPLE_B}).next_to(0.5*DOWN + 5.5*LEFT)
        difinition_2 = MTexText(r"$\bullet\ a$与$b$模$p$同余", tex_to_color_map = {(r"a", r"b"): BLUE, r"p": PURPLE_B}).next_to(1.3*DOWN + 5.5*LEFT)
        difinition_3 = MTex(r"\bullet\ a\equiv b\ (\bmod{p})", tex_to_color_map = {(r"a", r"b"): BLUE, r"p": PURPLE_B}).next_to(2.1*DOWN + 5.5*LEFT)
        self.play(*[mob.animate.shift(UP) for mob in [theorem, surr]], *[mob.animate.shift(0.25*UP) for mob in [left, right]])
        self.wait()
        self.play(Write(difinition_1))
        self.wait()
        self.play(Write(difinition_2))
        self.wait()
        self.play(Write(difinition_3))
        self.wait()

        theorem_2 = MTex(r"a^{p-1}\equiv 1\ (\bmod{p})", tex_to_color_map = {r"a": BLUE, r"1": GREEN, r"p": PURPLE_B, r"p-1": YELLOW_D}).scale(1.2).shift(1.3*DOWN + 3.5*RIGHT)
        surr_2 = SurroundingRectangle(theorem_2, buff = 0.3)
        self.play(Write(theorem_2), ShowCreation(surr_2))
        self.wait()
        
        
#################################################################### 

class Video_3(FrameScene):
    def construct(self):
        title, titleline = Title("同余"), TitleLine()
        self.add(title, titleline).wait()

        question = MTex(r"2362837\times 1419853=?", tex_to_color_map = {(r"2362837", r"1419853"): GREEN, r"?": YELLOW}).shift(2*UP)
        choices = [MTex(r"A.\ 3,281,724,238,543", tex_to_color_map = {r"A": YELLOW}).move_to(0.5*UP + 3*LEFT), 
                   MTex(r"B.\ 3,354,881,202,961", tex_to_color_map = {r"B": YELLOW}).move_to(0.5*UP + 3*RIGHT), 
                   MTex(r"C.\ 3,125,209,479,182", tex_to_color_map = {r"C": YELLOW}).move_to(0.5*DOWN + 3*LEFT), 
                   MTex(r"D.\ 3,209,834,542,934", tex_to_color_map = {r"D": YELLOW}).move_to(0.5*DOWN + 3*RIGHT), ]
        self.play(Write(question))
        self.wait()
        self.play(*[Write(mob) for mob in choices])
        self.wait()

        for mob in choices:
            mob.save_state().generate_target()[2:-1].set_fill(opacity = 0.5)
        question.save_state().generate_target()
        question.target[:6].set_fill(opacity = 0.5), question.target[8:14].set_fill(opacity = 0.5)
        surrs = [SurroundingRectangle(mob[-1]) for mob in choices]
        surr_above = [SurroundingRectangle(question[6]), SurroundingRectangle(question[14])]
        self.play(*[MoveToTarget(mob) for mob in choices + [question]], *[ShowCreation(surr) for surr in surrs],
                  ShowCreation(surr_above[0]), ShowCreation(surr_above[1]))
        self.wait()
        self.remove(*surrs, *surr_above)
        question.add(*surr_above)
        for i in range(4):
            choices[i].add(surrs[i])

        mod = MTex(r"3\times 7\equiv 1\ (\bmod{10})", tex_to_color_map = {(r"3", r"7"): GREEN, r"1": YELLOW, r"10": PURPLE_B}).shift(1.5*DOWN)
        self.play(Write(mod))
        self.wait()

        checkmark = MTex(r"\checkmark", color = GREEN).scale(1.5).set_stroke(**stroke_dic).move_to(choices[1][0]).shift(0.15*DOWN + 0.2*RIGHT)
        self.play(Write(checkmark))
        self.wait()

        self.play(question.animate.scale(0.8).next_to(2.3*UP + 6*LEFT), 
                  *[mob.animate.scale(0.8).next_to(1.5*UP + 0.8*i*DOWN + 6*LEFT) for i, mob in enumerate(choices)], 
                  checkmark.animate.scale(0.8).next_to(0.6*UP + 5.9*LEFT), 
                  mod.animate.scale(0.8).next_to(2*DOWN + 5.7*LEFT), run_time = 2)
        self.wait()

        condition = MTex(r"x\equiv r\ (\bmod{10}),\ y\equiv s\ (\bmod{10})", tex_to_color_map = {(r"x", r"y"): GREEN, (r"r", r"s"): YELLOW, r"10": PURPLE_B}).scale(0.8).shift(2.3*UP + 3*RIGHT)
        result = MTex(r"\Rightarrow xy\equiv rs\ (\bmod{10})", tex_to_color_map = {(r"x", r"y"): GREEN, (r"r", r"s"): YELLOW, r"10": PURPLE_B}).scale(0.8).shift(1.6*UP + 3*RIGHT)
        self.play(FadeIn(condition, 0.5*UP))
        self.wait()
        self.play(Write(result))
        self.wait()

        row_1 = MTex(r"x = 10x'+r,\  y = 10y'+s", tex_to_color_map = {(r"x", r"y"): GREEN, (r"x'", r"y'"): GREEN_E, (r"r", r"s"): YELLOW, r"10": PURPLE_B}).scale(0.8).shift(0.5*UP + 3*RIGHT)
        row_2 = MTex(r"xy=&(10x'+r)(10y'+s)\\=&10^2x'y'+10x's+10y'r+rs", tex_to_color_map = {(r"x", r"y"): GREEN, (r"x'", r"y'"): GREEN_E, (r"r", r"s"): YELLOW, r"10": PURPLE_B}).scale(0.8)
        row_2.shift(row_1[1].get_center() - row_2[2].get_center() + 0.8*DOWN)
        self.play(FadeIn(row_1, 0.5*UP))
        self.wait()
        self.play(FadeIn(row_2, 0.5*UP))
        self.wait()
        self.play(row_2[20:40].animate.set_fill(opacity = 0.4))
        self.wait()

        condition_p = MTex(r"x\equiv r\ (\bmod{p}),\ y\equiv s\ (\bmod{p})", tex_to_color_map = {(r"x", r"y"): GREEN, (r"r", r"s"): YELLOW, r"p": PURPLE_B}).scale(0.8).shift(2.3*UP + 3*RIGHT)
        condition_p.insert_submobject(7, condition_p[7].copy()).insert_submobject(18, condition_p[18].copy())
        result_p = MTex(r"\Rightarrow xy\equiv rs\ (\bmod{p})", tex_to_color_map = {(r"x", r"y"): GREEN, (r"r", r"s"): YELLOW, r"p": PURPLE_B}).scale(0.8).shift(1.6*UP + 3*RIGHT)
        result_p.insert_submobject(10, result_p[10].copy())
        row_1_p = MTex(r"x = px'+r,\  y = py'+s", tex_to_color_map = {(r"x", r"y"): GREEN, (r"x'", r"y'"): GREEN_E, (r"r", r"s"): YELLOW, r"p": PURPLE_B}).scale(0.8).shift(0.5*UP + 3*RIGHT)
        row_1_p.insert_submobject(2, row_1_p[2].copy()).insert_submobject(11, row_1_p[11].copy())
        row_2_p = MTex(r"xy=&(px'+r)(py'+s)\\=&p^2x'y'+px's+py'r+rs", tex_to_color_map = {(r"x", r"y"): GREEN, (r"x'", r"y'"): GREEN_E, (r"r", r"s"): YELLOW, r"p": PURPLE_B}).scale(0.8)
        row_2_p.insert_submobject(4, row_2_p[4].copy()).insert_submobject(12, row_2_p[12].copy()).insert_submobject(20, row_2_p[20].copy()).insert_submobject(28, row_2_p[28].copy()).insert_submobject(34, row_2_p[34].copy())
        row_2_p.shift(row_1_p[1].get_center() - row_2_p[2].get_center() + 0.8*DOWN)
        row_2_p[20:40].set_fill(opacity = 0.4)
        self.play(Transform(condition, condition_p), Transform(result, result_p), Transform(row_1, row_1_p), Transform(row_2, row_2_p))
        self.wait()

        result_add = MTex(r"\Rightarrow x+y\equiv r+s\ (\bmod{p})", tex_to_color_map = {(r"x", r"y"): GREEN, (r"r", r"s"): YELLOW, r"p": PURPLE_B}).scale(0.8).shift(1.6*UP + 3*RIGHT)
        row_2_add = MTex(r"x+y=&(px'+r)+(py'+s)\\=&px'+py'+r+s", tex_to_color_map = {(r"x", r"y"): GREEN, (r"x'", r"y'"): GREEN_E, (r"r", r"s"): YELLOW, r"p": PURPLE_B}).scale(0.8)
        row_2_add.shift(row_2_p[1].get_center() - row_2_add[2].get_center())
        row_2_add[20:28].set_fill(opacity = 0.4)
        self.play(*[OverFadeOut(mob, 4*LEFT) for mob in [question, *choices, checkmark, mod]], 
                  condition.animate.shift(3*LEFT), row_1.animate.shift(3*LEFT), 
                  *[mob.animate.shift(6*LEFT) for mob in [result, row_2]], 
                  *[OverFadeIn(mob, 4*LEFT) for mob in [result_add, row_2_add]], run_time = 2)
        self.wait()

        difinition = MTex(r"a\equiv b\ (\bmod{p})\ \Leftrightarrow\ a-b=pk", tex_to_color_map = {(r"a", r"b"): BLUE, r"p": PURPLE_B, r"k": GREEN_E}).shift(0.5*DOWN)
        self.play(*[OverFadeOut(mob, 1.6*DOWN) for mob in [row_1, row_2, row_2_add]], OverFadeIn(difinition, 1.6*DOWN), 
                  condition.animate.scale(1.25).shift(0.2*DOWN), result.animate.scale(1.25).shift(0.4*DOWN), result_add.animate.scale(1.25).shift(0.4*DOWN))
        self.wait()

class SuddenFadeOut(FadeOut):
    def begin(self):
        super().begin()
        self.mobject.set_fill(opacity = 0)
    def interpolate_mobject(self, alpha: float) -> None:
        if alpha > 0:
            super().interpolate_mobject(alpha)

class Video_4(FrameScene):
    def construct(self):
        title, titleline = Title("费马小定理"), TitleLine()
        a = MTex(r"a\ne pk_0", tex_to_color_map = {r"a": BLUE, r"p": PURPLE_B, r"k_0": GREEN_E}).next_to(3*UP, DOWN)
        self.add(title, titleline, a).wait()

        muls = [MTex(r"a", tex_to_color_map = {r"a": BLUE}).next_to(2*UP + 4*LEFT, LEFT), 
                MTex(r"2a", tex_to_color_map = {r"2": GREEN, r"a": BLUE}).next_to(1.2*UP + 4*LEFT, LEFT), 
                MTex(r"3a", tex_to_color_map = {r"3": GREEN, r"a": BLUE}).next_to(0.4*UP + 4*LEFT, LEFT),
                MTex(r"\vdots", tex_to_color_map = {r"3": GREEN, r"a": BLUE}).set_y(-0.4),
                MTex(r"(p-2)a", tex_to_color_map = {r"(p-2)": GREEN, r"a": BLUE}).next_to(1.2*DOWN + 4*LEFT, LEFT),
                MTex(r"(p-1)a", tex_to_color_map = {r"(p-1)": GREEN, r"a": BLUE}).next_to(2*DOWN + 4*LEFT, LEFT),]
        muls[3].match_x(muls[2])
        self.play(LaggedStart(*[FadeIn(mob, 0.2*DOWN) for mob in muls], lag_ratio = 0.2, run_time = 2))
        self.wait()

        condition = MTex(r"1\le y<x\le p-1", tex_to_color_map = {(r"x", r"y"): GREEN, (r"1", r"(p-1)"): GREEN_E}).shift(4*RIGHT).match_y(a)
        same = MTex(r"xa\not\equiv ya\ (\bmod{p})", tex_to_color_map = {(r"x", r"y"): GREEN, r"a": BLUE, r"p": PURPLE_B}).shift(1.2*UP + 0*RIGHT)
        no = same[2].set_color(RED)
        same.remove(same[2])
        self.play(FadeIn(same, 0.5*RIGHT), FadeIn(condition, 0.5*RIGHT))
        self.wait()

        factor = MTex(r"(x-y)a=pk", tex_to_color_map = {(r"x", r"y"): GREEN, r"a": BLUE, r"p": PURPLE_B, r"k": GREEN_E}).shift(0.4*DOWN + 0*RIGHT)
        surr = SurroundingRectangle(factor[7], stroke_color = PURPLE_B)
        self.play(FadeIn(factor, 0.5*UP))
        self.wait()

        underline = Underline(factor[:5], color = GREEN)
        primes_1 = MTex(r"p_1p_2\cdots p_l", color = GREEN).scale(0.8).match_x(underline).shift(1.5*DOWN)
        primes_2 = MTex(r"q_1q_2\cdots q_m", color = BLUE).scale(0.8).match_x(factor[5]).shift(0.4*UP)
        arrow_1, arrow_2 = Arrow(primes_1, factor[:5], buff = 0.15, color = GREEN).shift(0.05*DOWN), Arrow(primes_2, factor[5], buff = 0.1, color = BLUE)
        self.play(ShowCreation(underline), GrowArrow(arrow_1), GrowArrow(arrow_2), Write(primes_1), Write(primes_2), ShowCreation(surr))
        self.wait()

        arrow_3, arrow_4 = Arrow(0.5*LEFT, 0.4*RIGHT, color = PURPLE_B).next_to(primes_1, LEFT), Arrow(0.5*LEFT, 0.4*RIGHT, color = PURPLE_B).next_to(primes_2, LEFT)
        cross_3, cross_4 = VGroup(Line(0.2*UL, 0.2*DR), Line(0.2*DL, 0.2*UR)).set_color(RED).move_to(arrow_3), VGroup(Line(0.3*UL, 0.3*DR), Line(0.3*DL, 0.3*UR)).set_color(RED).move_to(arrow_4)
        self.play(FadeIn(arrow_3, 0.2*RIGHT), FadeIn(arrow_4, 0.2*RIGHT))
        self.wait()

        self.play(arrow_3.animate.set_stroke(opacity = 0.3))
        self.wait()
        self.play(IndicateAround(a))
        self.wait()
        self.play(ShowCreation(cross_4), arrow_3.animate.set_stroke(opacity = 1))
        self.wait()

        small = MTex(r"1\le x-y\le p-2", tex_to_color_map = {(r"x", r"y"): GREEN}).scale(0.8).shift(1.2*UP + 4*RIGHT)
        between = MTex(r"0p< x-y< 1p", tex_to_color_map = {(r"x", r"y"): GREEN, r"p": PURPLE_B, (r"0", r"1"): GREEN_E}).scale(0.8).shift(0.4*UP + 4*RIGHT)
        self.play(Write(small))
        self.wait()
        self.play(FadeIn(between, 0.5*UP))
        self.wait()

        self.play(ShowCreation(cross_3))
        self.wait()

        self.play(*[OverFadeOut(mob, 4*RIGHT) for mob in [factor, underline, primes_1, primes_2, arrow_1, arrow_2, arrow_3, arrow_4, cross_3, cross_4, small, between, surr]], 
                  FadeIn(no.shift(4*RIGHT), 4*RIGHT), same.animate.shift(4*RIGHT), run_time = 2)
        self.wait()

        origins = [MTex(r"1", color = GREEN).next_to(2*UP + 3*LEFT), 
                MTex(r"2", color = GREEN).next_to(1.2*UP + 3*LEFT), 
                MTex(r"3", color = GREEN).next_to(0.4*UP + 3*LEFT),
                MTex(r"\vdots", color = GREEN).set_y(-0.4),
                MTex(r"p-2", color = GREEN).next_to(1.2*DOWN + 3*LEFT),
                MTex(r"p-1", color = GREEN).next_to(2*DOWN + 3*LEFT),]
        origins[3].match_x(origins[2])
        back_l, back_r = SurroundingRectangle(VGroup(*muls), buff = 0.3), SurroundingRectangle(VGroup(*origins), buff = 0.3)
        equal = MTex(r"=").shift(3.5*LEFT).scale(1.5)
        self.play(*[FadeIn(mob, 0.3*LEFT) for mob in origins + [back_r]], FadeIn(back_l), Write(equal))
        self.wait()
        
        offset = 0.25*DOWN + 3*RIGHT
        value = MTex(r"a=2", tex_to_color_map = {r"a": BLUE, r"2": GREEN}).next_to(5*RIGHT + 3*UP, DOWN)
        circle_inner = Circle(radius = 2, color = WHITE).shift(offset)
        numbers = [MTex(str(i), color = GREEN).scale(0.8).shift(offset + 2.5*unit(PI/2 + i*TAU/11)) for i in range(11)]
        points = [Dot(color = GREEN).scale(0.8).shift(offset + 2*unit(PI/2 + i*TAU/11)) for i in range(11)]
        self.play(*[OverFadeOut(mob) for mob in [condition, same, no]], *[OverFadeIn(mob) for mob in [value, circle_inner] + numbers + points])
        self.wait()

        line_2 = Polygon(*[offset + 2*unit(PI/2 + 2*i*TAU/11) for i in range(11)], color = BLUE)
        texs = [MTex(r"a", color = BLUE).scale(0.8).next_to(offset + 2*unit(PI/2 + 2*TAU/11), UP, buff = 0)] + [MTex(str(i)+r"a", tex_to_color_map = {str(i): GREEN, r"a": BLUE}).scale(0.8).next_to(offset + 2*unit(PI/2 + 2*i*TAU/11), UP, buff = 0) for i in range(2, 11)]
        self.add(line_2, *points).play(ShowCreation(line_2, rate_func = linear, run_time = 5.5), 
                                       LaggedStart(Animation(VMobject(), run_time = 0.5), *[SuddenFadeOut(tex, 0.3*UP, run_time = 1, rate_func = rush_from) for tex in texs], lag_ratio = 0.5, rate_func = linear, run_time = 6))
        self.wait()

        value_3 = MTex(r"a=3", tex_to_color_map = {r"a": BLUE, r"3": GREEN}).next_to(5*RIGHT + 3*UP, DOWN)
        line_3 = Polygon(*[offset + 2*unit(PI/2 + 3*i*TAU/11) for i in range(11)], color = BLUE)
        self.play(Transform(value, value_3), Transform(line_2, line_3))
        self.wait()

        value_5 = MTex(r"a=5", tex_to_color_map = {r"a": BLUE, r"5": GREEN}).next_to(5*RIGHT + 3*UP, DOWN)
        line_5 = Polygon(*[offset + 2*unit(PI/2 + 5*i*TAU/11) for i in range(11)], color = BLUE)
        self.play(Transform(value, value_5), Transform(line_2, line_5))
        self.wait()

        value_6 = MTex(r"a=6", tex_to_color_map = {r"a": BLUE, r"6": GREEN}).next_to(5*RIGHT + 3*UP, DOWN)
        line_6 = Polygon(*[offset + 2*unit(PI/2 + 6*i*TAU/11) for i in range(11)], color = BLUE)
        self.play(Transform(value, value_6), Transform(line_2, line_6))
        self.wait()

        self.bring_to_back(value, circle_inner, *numbers, line_2, *points, self.shade).play(FadeIn(self.shade))
        self.remove(value, circle_inner, *numbers, line_2, *points, self.shade).wait()

        prods = MTex(r"\text{\small 左边的乘积}\equiv\text{\small 右边的乘积}\ (\bmod{p})", tex_to_color_map = {r"左边的乘积": BLUE, r"右边的乘积": GREEN, r"p": PURPLE_B}).shift(1.5*UP + 3*RIGHT)
        factorials = MTex(r"a^{p-1}(p-1)!\equiv(p-1)!\ (\bmod{p})", tex_to_color_map = {r"a": BLUE, r"p": PURPLE_B, r"p-1": YELLOW_D, r"(p-1)!": GREEN}).shift(0.5*UP + 3*RIGHT)
        factor = MTex(r"\left(a^{p-1}-1\right)(p-1)!=pk", tex_to_color_map = {r"a": BLUE, r"p": PURPLE_B, r"k": GREEN_E, r"p-1": YELLOW_D, r"(p-1)!": GREEN}).shift(0.5*DOWN + 3*RIGHT)
        self.play(FadeIn(prods, 0.5*UP))
        self.wait()
        self.play(TransformFromCopy(prods[:5], factorials[:10]), TransformFromCopy(prods[5], factorials[10]), TransformFromCopy(prods[6:11], factorials[11:17]), TransformFromCopy(prods[11:], factorials[17:]))
        self.wait()
        self.play(FadeIn(factor, 0.5*UP))
        self.wait()

        under_l, under_r = Underline(factor[:8], color = BLUE), Underline(factor[8:14], color = GREEN)
        arrow_1, arrow_2 = Arrow(0.5*DOWN, 0.5*UP, color = PURPLE_B).next_to(under_l, DOWN), Arrow(0.5*DOWN, 0.5*UP, color = PURPLE_B).next_to(under_r, DOWN)
        cross = VGroup(Line(0.3*UL, 0.3*DR), Line(0.3*DL, 0.3*UR)).set_color(RED).move_to(arrow_2)
        surr = SurroundingRectangle(factor[15], stroke_color = PURPLE_B)
        self.play(ShowCreation(under_r), GrowArrow(arrow_2), ShowCreation(surr))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()
        self.play(ShowCreation(under_l), GrowArrow(arrow_1))
        self.wait()
        
class Video_5(FrameScene):
    def construct(self):
        texts = r"\log(p)_a(b\otimes c)", r"\log(p)_ab", r"\log(p)_ac", r"\oplus"
        question_2 = MTex(r"\log(p)_a(b\otimes c)=\log(p)_ab\oplus\log(p)_ac", isolate = texts, tex_to_color_map = {r"\otimes": RED, r"\oplus": RED_E, r"p": PURPLE_B, r"a": BLUE, (r"b", r"c"): ORANGE}).shift(3*UP)
        parts = [question_2.get_part_by_tex(text) for text in texts]
        self.add(question_2).wait()

        underline_2, underline_3 = Underline(parts[1], color = YELLOW_E), Underline(parts[2], color = YELLOW_E)
        u, v = MTex(r"u", color = YELLOW_D).set_y(1.5).match_x(parts[1]), MTex(r"v", color = YELLOW_D).set_y(1.5).match_x(parts[2])
        arrow_2, arrow_3 = Arrow(u.get_corner(UP), underline_2.get_center(), color = YELLOW_D), Arrow(v.get_corner(UP), underline_3.get_center(), color = YELLOW_D)
        self.play(ShowCreation(underline_2), FadeIn(u, 0.3*UP), FadeIn(arrow_2, 0.3*UP))
        self.wait()
        self.play(ShowCreation(underline_3), FadeIn(v, 0.3*UP), FadeIn(arrow_3, 0.3*UP))
        self.wait()
        
        equation_2 = MTex(r"a^u\equiv b\ (\bmod{p})", tex_to_color_map = {r"a": BLUE, r"u": YELLOW_D, r"b": ORANGE, r"p": PURPLE_B}).shift(0.6*UP).match_x(parts[3]).shift(0.1*RIGHT)
        equation_3 = MTex(r"a^v\equiv c\ (\bmod{p})", tex_to_color_map = {r"a": BLUE, r"v": YELLOW_D, r"c": ORANGE, r"p": PURPLE_B}).shift(0.2*DOWN).match_x(parts[3]).shift(0.1*RIGHT)
        equation_1 = MTex(r"a^{u+v}\equiv bc\ (\bmod{p})", tex_to_color_map = {r"a": BLUE, (r"u", r"v"): YELLOW_D, (r"b", r"c"): ORANGE, r"p": PURPLE_B}).shift(0.2*UP + 2.5*LEFT)
        self.play(FadeIn(equation_2, 0.5*LEFT), FadeIn(equation_3, 0.5*LEFT))
        self.wait()
        self.play(Write(equation_1))
        self.wait()

        underline_t_1 = Underline(equation_1[5:7], color = ORANGE)
        tip_1 = MTex(r"b\otimes c", color = ORANGE, tex_to_color_map = {r"\otimes": RED}).match_x(underline_t_1).set_y(1.5)
        arrow_4 = Arrow(tip_1.get_corner(DOWN), equation_1[5:7].get_corner(UP), color = ORANGE)
        self.play(ShowCreation(underline_t_1), FadeIn(tip_1, 0.3*DOWN), FadeIn(arrow_4, 0.3*DOWN))
        self.wait()

        # underline_t_2 = Underline(equation_1[:4], color = YELLOW_D)
        # texts = r"a^{(p-1)k+(u\oplus v)}", r"\left(a^{(p-1)}\right)^ka^{u\oplus v}", r"a^{(p-1)}", r"a^{u\oplus v}"
        # tip_2 = MTex(r"a^{u+v}\equiv a^{(p-1)k+(u\oplus v)}\equiv \left(a^{(p-1)}\right)^ka^{u\oplus v}\equiv a^{u\oplus v}\ (\bmod{p})", tex_to_color_map = {r"a": BLUE, (r"u", r"v"): YELLOW_D, r"p": PURPLE_B, r"\oplus": RED_E, r"(p-1)": YELLOW_D, r"k": GREEN_E}).scale(0.8).match_x(underline_t_2).set_y(-1.3)
        # parts = [tip_2.get_part_by_tex(text) for text in texts]
        # parts[1] = tip_2[19:32]
        # arrow_5 = Arrow(tip_2.get_corner(UP), underline_t_2.get_center(), color = YELLOW_D)
        # tip_2.match_x(equation_1, LEFT)
        # self.play(ShowCreation(underline_t_2), FadeIn(tip_2, 0.3*UP), FadeIn(arrow_5, 0.3*UP))
        # self.wait()
        # surr = SurroundingRectangle(parts[0])
        # self.play(ShowCreation(surr))
        # self.wait()
        # self.play(Transform(surr, SurroundingRectangle(parts[1])))
        # self.wait()
        # self.play(Transform(surr, SurroundingRectangle(parts[2])))
        # self.wait()
        # surr.add(surr.copy(), surr.copy()).clear_points()
        # fermat = MTex(r"=1", tex_to_color_map = {r"1": GREEN}).scale(0.8)
        # fermat[0].rotate(PI/2).next_to(surr, DOWN, buff = 0.1)
        # fermat[1].next_to(fermat[0], DOWN)
        # text = Heiti(r"(费马小定理)", color = YELLOW).scale(0.6).next_to(fermat).shift(0.1*DOWN)
        # self.play(ReplacementTransform(surr, fermat), FadeIn(text), parts[2].animate.set_fill(opacity = 0.5))
        # self.wait()
        # self.play(IndicateAround(question_2))
        # self.wait()

        underline_t_2 = Underline(equation_1[:4], color = YELLOW_D)
        texts = r"a^{u+v}\equiv a^{(p-1)k+(u\oplus v)}", r"\equiv \left(a^{(p-1)}\right)^ka^{u\oplus v}", r"\equiv a^{u\oplus v}", r"(\bmod{p})", r"a^{(p-1)}"
        tip_2 = MTex(r"a^{u+v}\equiv a^{(p-1)k+(u\oplus v)}\equiv \left(a^{(p-1)}\right)^ka^{u\oplus v}\equiv a^{u\oplus v}\ (\bmod{p})", isolate = texts, tex_to_color_map = {r"a": BLUE, (r"u", r"v"): YELLOW_D, r"p": PURPLE_B, r"\oplus": RED_E, r"(p-1)": YELLOW_D, r"k": GREEN_E}).scale(0.8).match_x(underline_t_2).set_y(-1.3)
        parts = [tip_2.get_part_by_tex(text) for text in texts]
        arrow_5 = Arrow(tip_2.get_corner(UP), underline_t_2.get_center(), color = YELLOW_D)
        tip_2.match_x(equation_1, LEFT)
        position_1 = MTex(r"a^{u+v}\equiv a^{(p-1)k+(u\oplus v)}(\bmod{p})", isolate = texts).scale(0.8)
        position_1.shift(tip_2[0].get_center() - position_1[0].get_center())
        p_1 = position_1.get_part_by_tex(texts[3])
        position_2 = MTex(r"a^{u+v}\equiv a^{(p-1)k+(u\oplus v)}\equiv \left(a^{(p-1)}\right)^ka^{u\oplus v}(\bmod{p})", isolate = texts).scale(0.8)
        position_2.shift(tip_2[0].get_center() - position_2[0].get_center())
        p_2 = position_2.get_part_by_tex(texts[3])
        self.play(ShowCreation(underline_t_2), FadeIn(parts[0], 0.3*UP), FadeIn(parts[3].save_state().move_to(p_1), 0.3*UP), FadeIn(arrow_5, 0.3*UP))
        self.wait()

        shade = BackgroundRectangle(parts[1], buff = 0.1)
        self.add(parts[1], shade, parts[3]).play(parts[3].animate.move_to(p_2), follow(shade, parts[3]))
        self.remove(shade).wait()
        surr = SurroundingRectangle(parts[4])
        self.play(ShowCreation(surr))
        self.wait()
        surr.add(surr.copy(), surr.copy()).clear_points()
        fermat = MTex(r"=1", tex_to_color_map = {r"1": GREEN}).scale(0.8)
        fermat[0].rotate(PI/2).next_to(surr, DOWN, buff = 0.1)
        fermat[1].next_to(fermat[0], DOWN)
        text = Heiti(r"(费马小定理)", color = YELLOW).scale(0.6).next_to(fermat[1])
        self.play(ReplacementTransform(surr, fermat), FadeIn(text), parts[4].animate.set_fill(opacity = 0.5))
        self.wait()
        shade = BackgroundRectangle(parts[2], buff = 0.1)
        self.add(parts[2], shade, parts[3]).play(parts[3].animate.restore(), follow(shade, parts[3]))
        self.remove(shade).wait()
        self.play(IndicateAround(question_2))
        self.wait()
        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        