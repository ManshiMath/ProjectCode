from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        n = 10
        texs = ["a", "a+d"] + ["a+"+str(i)+"d" for i in range(2, n)]
        color_map = {("a", "d"): GREEN_A}
        formulas = [MTex(texs[i], tex_to_color_map = {**color_map, str(i): BLUE}).scale(0.8) for i in range(n)]
        for i in range(n):
            formulas[i].shift((2.5 - formulas[i][0].get_y())*UP).set_x((i-4)*1.5+0.2)
        texs = [r"a_{"+str(i+1)+r"}" for i in range(n)]
        color_map = {"a": WHITE}
        terms = [MTex(texs[i], tex_to_color_map = {**color_map, str(i+1): BLUE}).scale(1.2) for i in range(n)]
        for i in range(n):
            terms[i].shift((1.5 - terms[i][0].get_y())*UP).set_x((i-4)*1.5+0.2)
        self.play(LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in formulas], run_time = 2, lag_ratio = 0.2, ), 
                  LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in terms], run_time = 2, lag_ratio = 0.2, ), )
        self.wait()

        surrs = [SurroundingRectangle(formulas[i]) for i in (1, 3, 5, 7)]
        self.play(LaggedStart(*[ShowCreation(mob) for mob in surrs], run_time = 2, lag_ratio = 0.2))
        self.wait()
        arrows = [Arrow(surrs[i].get_corner(UR), surrs[i+1].get_corner(UL), path_arc = -PI/3) for i in range(3)]
        differences = [MTex(r"+2d", tex_to_color_map = {r"2": BLUE, r"d": GREEN_A}).scale(0.8).next_to(arrows[i], UP) for i in range(3)]
        self.play(LaggedStart(*[ShowCreation(mob) for mob in arrows], run_time = 2, lag_ratio = 0.5, rate_func = linear), 
                  LaggedStart(*[FadeIn(mob) for mob in differences], run_time = 2, lag_ratio = 0.5, rate_func = linear), )
        self.wait()

        cards = [VGroup(Square(side_length = 0.6, color = GREY), MTex(str(i+1), color = BLUE_B)).shift(0.5*DOWN + ((i-4)*1.5+0.2)*RIGHT) for i in range(n)]
        margins = [SurroundingRectangle(mob[1:]) for mob in terms]
        self.play(LaggedStart(*[ShowCreation(mob) for mob in margins], run_time = 2, lag_ratio = 0.2))
        self.wait()
        self.play(LaggedStart(*[Transform(mob_1, mob_2[0], remover = True) for mob_1, mob_2 in zip(margins, cards)], run_time = 2, lag_ratio = 0.2), 
                  LaggedStart(*[TransformFromCopy(mob_1[1:], mob_2[1:], remover = True) for mob_1, mob_2 in zip(terms, cards)], run_time = 2, lag_ratio = 0.2))
        self.add(*cards).wait()

        arrows = [Arrow(cards[i].get_corner(DR), cards[i+2].get_corner(DL), path_arc = PI/3) for i in (1, 3, 5)]
        differences = [MTex(r"+2", tex_to_color_map = {r"2": BLUE}).scale(0.8).next_to(arrows[i], DOWN) for i in range(3)]
        self.play(LaggedStart(*[mob[0].animate.set_color(YELLOW) for mob in [cards[1], cards[3], cards[5], cards[7]]], run_time = 2, lag_ratio = 1/3, rate_func = linear), 
                  LaggedStart(*[ShowCreation(mob) for mob in arrows], run_time = 2, lag_ratio = 0.5, rate_func = linear), 
                  LaggedStart(*[FadeIn(mob) for mob in differences], run_time = 2, lag_ratio = 0.5, rate_func = linear), )
        self.wait()

class Video_2(FrameScene):
    def construct(self):
        def card(tex, color_out = GREY, color_in = BLUE_B):
            return VGroup(Square(side_length = 0.6, color = color_out), MTex(tex, color = color_in))
        def choose(tex):
            return card(str(tex), BLUE, BLUE_B)
        def discard(tex):
            return card(str(tex), GREY, GREY)
        n = 6
        cards = [card(str(i+1)).scale(1.5).shift(UP + ((i-2.5)*1.5)*RIGHT) for i in range(n)]
        
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in cards], run_time = 2, lag_ratio = 0.2, ))
        self.wait()

        targets = VGroup(*[Square(side_length = 1.0, color = RED_B).shift(2.5*UP + ((i-1.5)*1.5)*RIGHT) for i in range(4)])
        self.play(ShowCreation(targets, lag_ratio = 1/3, run_time = 2))
        self.wait()

        cards_2 = [discard(1), choose(2), choose(3), choose(4), choose(5), discard(6)]
        solution_2 = VGroup(*[cards_2[i].shift((i-2.5)*0.8*RIGHT) for i in range(6)]).scale(0.75).move_to(DOWN)
        self.play(targets.animate.shift(1.5*DOWN), FadeIn(solution_2, 0.5*UP))
        self.wait()

        cards_1 = [choose(1), choose(2), choose(3), choose(4), discard(5), discard(6)]
        solution_1 = VGroup(*[cards_1[i].shift((i-2.5)*0.8*RIGHT) for i in range(6)]).scale(0.75).move_to(DOWN + 4*LEFT)
        self.play(targets.animate.shift(1.5*LEFT), FadeIn(solution_1, 0.5*UP))
        self.wait()

        cards_3 = [discard(1), discard(2), choose(3), choose(4), choose(5), choose(6)]
        solution_3 = VGroup(*[cards_3[i].shift((i-2.5)*0.8*RIGHT) for i in range(6)]).scale(0.75).move_to(DOWN + 4*RIGHT)
        self.play(targets.animate.shift(3*RIGHT), FadeIn(solution_3, 0.5*UP))
        self.wait()

        middles = [Square(side_length = 0, color = GREY).move_to((targets[i].get_center() + targets[i+1].get_center())/2) for i in range(3)]
        targets.set_submobjects([targets[0], middles[0], targets[1], middles[1], targets[2], middles[2], targets[3]])
        wide_targets = VGroup(*[Square(side_length = 1.0, color = GREY_D if i%2 else RED_B).shift(2.5*UP + ((i-2.5)*1.5)*RIGHT) for i in range(7)])
        self.play(Transform(targets, wide_targets))
        self.wait()
        self.play(FadeOut(targets))
        self.wait()

class Video_3(FrameScene):
    def construct(self):
        def card(tex, color_out = GREY, color_in = BLUE_B):
            return VGroup(Square(side_length = 0.6, color = color_out), MTex(tex, color = color_in))
        def choose(tex):
            return card(str(tex), BLUE, BLUE_B)
        def discard(tex):
            return card(str(tex), GREY, GREY)
        n = 18
        cards = [card(str(i+1)).shift(UP + ((i-8.5))*0.8*RIGHT) for i in range(n)]
        
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in cards], run_time = 3, lag_ratio = 0.2, ))
        self.wait()

        self.play(*[mob.animate.set_color(GREY_D).shift(0.3*DOWN) for mob in [cards[1], cards[12]]])
        self.wait()

        dash = DashedLine(UP, DOWN).shift(5*0.8*RIGHT + UP)
        self.play(ShowCreation(dash))
        self.wait()
        self.play(*[mob.animate.set_color(TEAL).shift(0.2*UP) for mob in cards[14:]])
        self.wait()

        offset = 0.8*2*RIGHT
        self.play(*[mob.animate.shift(offset) for mob in cards[:14]], *[FadeOut(mob, offset) for mob in cards[14:] + [dash]])
        self.wait()

        targets = VGroup(*[Square(side_length = 0.7, color = RED_B).shift(2*UP + (i-6.5)*0.8*RIGHT) for i in range(4)])
        self.play(ShowCreation(targets, lag_ratio = 1/3, run_time = 2))
        self.wait()

        cross = Cross(targets[1])
        self.play(ShowCreation(cross))
        self.play(FadeOut(cross))
        self.wait()

        wide_targets = VGroup(*[Square(side_length = 0.7, color = RED_B).shift(2*UP + (i*2-6.5)*0.8*RIGHT) for i in range(4)])
        self.play(Transform(targets, wide_targets))
        self.wait()

        self.play(targets.animate.shift(DOWN))
        self.wait()

        targets_2 = VGroup(*[Square(side_length = 0.7, color = YELLOW_B).shift(2*UP + (i*2-3.5)*0.8*RIGHT) for i in range(4)])
        self.play(ShowCreation(targets_2, lag_ratio = 1/3, run_time = 2))
        self.wait()

        self.play(*[IndicateAround(cards[i], rect_kwargs = {"color": BLUE}) for i in [8, 10, 11, 13]])
        self.wait()
        wide_targets_2 = VGroup(*[Square(side_length = 0.7, color = YELLOW_B).shift(2*UP + (i*4-3.5)*0.8*RIGHT) for i in range(4)])
        self.play(Transform(targets_2, wide_targets_2))
        self.wait()
        cross = Cross(wide_targets_2[-1])
        self.play(ShowCreation(cross))
        self.play(FadeOut(cross))
        self.wait()
        self.play(FadeOut(targets_2), targets.animate.shift(UP))
        self.wait()

        wide_targets = VGroup(*[Square(side_length = 0.7, color = RED_B).shift(2*UP + (i*3-6.5)*0.8*RIGHT) for i in range(4)])
        self.play(Transform(targets, wide_targets))
        self.wait()

        self.play(targets.animate.shift(DOWN))
        self.wait()

        targets_2 = VGroup(*[Square(side_length = 0.7, color = YELLOW_B).shift(2*UP + (i*1-6.5)*0.8*LEFT) for i in range(4)])
        cross = Cross(targets_2[0])
        self.play(ShowCreation(targets_2, lag_ratio = 1/3, run_time = 2), ShowCreation(cross))
        self.wait(1)
        wide_targets_2 = VGroup(*[Square(side_length = 0.7, color = YELLOW_B).shift(2*UP + (i*2-6.5)*0.8*LEFT) for i in range(4)])
        self.play(Transform(targets_2, wide_targets_2))
        self.wait(1)
        wide_targets_2 = VGroup(*[Square(side_length = 0.7, color = YELLOW_B).shift(2*UP + (i*3-6.5)*0.8*LEFT) for i in range(4)])
        self.play(Transform(targets_2, wide_targets_2), FadeOut(cross))
        self.wait()
        self.play(targets_2.animate.shift(DOWN))
        self.wait()

        n = 14
        colors = [RED_B, GREY_D, BLUE, RED_B, YELLOW_B, BLUE, RED_B, YELLOW_B, BLUE, RED_B, YELLOW_B, BLUE, GREY_D, YELLOW_B]
        cards_2 = VGroup(*[card(str(i+1)).set_color(colors[i]).shift(UP + ((i-8.5))*0.8*RIGHT) for i in range(n)]).scale(0.75).move_to(DOWN)
        self.play(FadeIn(cards_2, 0.5*UP), *[IndicateAround(cards[i], rect_kwargs = {"color": BLUE}) for i in [2, 5, 8, 11]])
        self.wait()

        self.play(targets.animate.shift(UP), FadeOut(targets_2, UP))
        self.wait()
        wide_targets = VGroup(*[Square(side_length = 0.7, color = RED_B).shift(2*UP + (i*4-6.5)*0.8*RIGHT) for i in range(4)])
        self.play(Transform(targets, wide_targets))
        self.wait()
        cross = Cross(wide_targets[-1])
        self.play(ShowCreation(cross))
        self.play(FadeOut(cross))
        self.wait()

        wide_targets = VGroup(*[Square(side_length = 0.7, color = RED_B).shift(2*UP + (i*5-6.5)*0.8*RIGHT) for i in range(4)])
        self.play(Transform(targets, wide_targets))
        self.wait()
        self.play(FadeOut(targets))
        self.wait()
        
class Video_4(FrameScene):
    def construct(self):
        def card(tex, color_out = GREY, color_in = BLUE_B):
            return VGroup(Square(side_length = 0.6, color = color_out), MTex(tex, color = color_in))
        
        n = 6
        cards = [card(str(i+1)).scale(1.5).shift(3*UP + ((i-2.5)*1.5)*RIGHT) for i in range(n)]

        self.wait()
        self.play(*[FadeIn(mob) for mob in cards])
        self.wait()

        template = VGroup(*[card(str(i+1)).shift((i-2.5)*0.75*RIGHT) for i in range(6)]).scale(0.6)
        copies = []
        for i in range(6):
            for j in range(i+1, 6):
                copy_i = template.copy()
                copy_i[i].set_color(GREY_D), copy_i[j].set_color(GREY_D)
                copies.append(copy_i)
        for i in range(15):
            if i < 8:
                copies[i].move_to(4.5*LEFT + (1.5-0.5*i)*UP)
            else:
                copies[i].move_to(1*LEFT + (1.5-0.5*(i-8))*UP)
        self.play(LaggedStart(*[FadeIn(mob, 0.2*UP) for mob in copies], lag_ratio = 0.1, run_time = 3))
        self.wait()

        stars = [MTex("\star").scale(0.5).next_to(copies[i], LEFT, buff = 0.1) for i in (0, 4, 14)]
        def choose(tex):
            return card(str(tex), BLUE, BLUE_B)
        def discard(tex):
            return card(str(tex), GREY, GREY)
        cards_1 = [choose(1), choose(2), choose(3), choose(4), discard(5), discard(6)]
        solution_1 = VGroup(*[cards_1[i].shift((i-2.5)*0.8*RIGHT) for i in range(6)]).scale(0.75).move_to(3.5*RIGHT + 1.5*UP)
        cards_2 = [discard(1), choose(2), choose(3), choose(4), choose(5), discard(6)]
        solution_2 = VGroup(*[cards_2[i].shift((i-2.5)*0.8*RIGHT) for i in range(6)]).scale(0.75).move_to(3.5*RIGHT + 0.5*UP)
        cards_3 = [discard(1), discard(2), choose(3), choose(4), choose(5), choose(6)]
        solution_3 = VGroup(*[cards_3[i].shift((i-2.5)*0.8*RIGHT) for i in range(6)]).scale(0.75).move_to(3.5*RIGHT + 0.5*DOWN)
        self.play(*[Write(mob) for mob in stars], *[FadeIn(mob, 0.5*LEFT) for mob in [solution_1, solution_2, solution_3]])
        self.wait()

        probability = MTex(r"P=\frac{3}{15}", tex_to_color_map = {r"P": TEAL}).move_to(3.5*RIGHT + 1.7*DOWN)
        self.play(Write(probability))
        self.wait()

class Video_5(FrameScene):
    def construct(self):
        def card(tex, color_out = GREY, color_in = BLUE_B):
            return VGroup(Square(side_length = 0.6, color = color_out), MTex(tex, color = color_in))
        
        n = 10
        cards = [card(str(i+1)).scale(1.2).shift(3*UP + ((i-4.5)*1.2)*RIGHT) for i in range(n)]

        self.wait()
        self.play(*[FadeIn(mob) for mob in cards])
        self.wait()

        template = VGroup(*[card(str(i+1)).shift((i-4.5)*0.75*RIGHT) for i in range(n)]).scale(0.3)
        copies = []
        for i in range(n):
            for j in range(i+1, n):
                copy_i = template.copy()
                copy_i[i].set_color(GREY_D), copy_i[j].set_color(GREY_D)
                copies.append(copy_i)
        for i in range(45):
            if i < 23:
                copies[i].move_to(5*LEFT + (2.27-0.27*i)*UP)
            else:
                copies[i].move_to(2*LEFT + (2.27-0.27*(i-23))*UP)
            # if i < 8:
            #     copies[i].move_to(4.5*LEFT + (1.5-0.5*i)*UP)
            # else:
            #     copies[i].move_to(1*LEFT + (1.5-0.5*(i-8))*UP)
        self.play(LaggedStart(*[FadeIn(mob, 0.2*UP) for mob in copies], lag_ratio = 0.1, run_time = 3))
        self.wait()

        stars = [MTex("\star").scale(0.5).next_to(copies[i], LEFT, buff = 0.1) for i in (0, 4, 8, 15, 30, 34, 44)]
        def group(*types: int):
            vgroup = VGroup()
            for i, type in enumerate(types):
                if type == 0:
                    mob = card(str(i+1), GREY, GREY)
                elif type == 1:
                    mob = card(str(i+1), BLUE, BLUE_B)
                elif type == 2:
                    mob = card(str(i+1), RED, RED_B)
                vgroup.add(mob.shift((i-4.5)*0.8*RIGHT))
            return vgroup.scale(0.75)

        solution_1 = group(0, 0, 1, 1, 1, 1, 2, 2, 2, 2).scale(0.75).move_to(3.5*RIGHT + 2*UP)
        solution_2 = group(0, 1, 1, 1, 1, 0, 2, 2, 2, 2).scale(0.75).move_to(3.5*RIGHT + 1.5*UP)
        solution_3 = group(0, 1, 1, 1, 1, 2, 2, 2, 2, 0).scale(0.75).move_to(3.5*RIGHT + 1*UP)
        solution_4 = group(1, 0, 1, 2, 1, 2, 1, 2, 0, 2).scale(0.75).move_to(3.5*RIGHT + 0.5*UP)
        solution_5 = group(1, 1, 1, 1, 0, 0, 2, 2, 2, 2).scale(0.75).move_to(3.5*RIGHT + 0*UP)
        solution_6 = group(1, 1, 1, 1, 0, 2, 2, 2, 2, 0).scale(0.75).move_to(3.5*RIGHT + 0.5*DOWN)
        solution_7 = group(1, 1, 1, 1, 2, 2, 2, 2, 0, 0).scale(0.75).move_to(3.5*RIGHT + 1*DOWN)
        solutions = [solution_1, solution_2, solution_3, solution_4, solution_5, solution_6, solution_7]
        self.play(*[Write(mob) for mob in stars], *[FadeIn(mob, 0.5*LEFT) for mob in solutions])
        self.wait()

        probability = MTex(r"P=\frac{7}{45}", tex_to_color_map = {r"P": TEAL}).move_to(3.5*RIGHT + 2*DOWN)
        self.play(Write(probability))
        self.wait()
        
        possibles = [MTex("1", color = YELLOW).move_to(0.2*LEFT + 1.8*UP), MTex("2", color = GOLD).move_to(0.5*RIGHT + 1.8*UP), 
                MTex("5", color = YELLOW).move_to(0.2*LEFT + 1.1*UP), MTex("6", color = GOLD).move_to(0.5*RIGHT + 1.1*UP), 
                MTex("9", color = YELLOW).move_to(0.2*LEFT + 0.4*UP), MTex("10", color = GOLD).move_to(0.5*RIGHT + 0.4*UP)]
        indicates = [Underline(mob, buff = 0.1).match_color(mob) for mob in possibles]
        surrs_1 = [SurroundingRectangle(mob[0], buff = 0.05) for mob in [solution_1, solution_2, solution_3]]
        surrs_2 = [SurroundingRectangle(mob[1], buff = 0.05, color = GOLD) for mob in [solution_1, solution_4]]
        surrs_5 = [SurroundingRectangle(mob[4], buff = 0.05) for mob in [solution_5, solution_6]]
        surrs_6 = [SurroundingRectangle(mob[5], buff = 0.05, color = GOLD) for mob in [solution_2, solution_5]]
        surrs_9 = [SurroundingRectangle(mob[8], buff = 0.05) for mob in [solution_4, solution_7]]
        surrs_10 = [SurroundingRectangle(mob[9], buff = 0.05, color = GOLD) for mob in [solution_3, solution_6, solution_7]]
        self.play(*[ShowCreation(mob) for mob in surrs_1], Write(possibles[0]))
        self.play(*[Uncreate(mob, start = 1) for mob in surrs_1], *[ShowCreation(mob) for mob in surrs_2], Write(possibles[1]))
        self.play(*[Uncreate(mob, start = 1) for mob in surrs_2], *[ShowCreation(mob) for mob in surrs_5], Write(possibles[2]))
        self.play(*[Uncreate(mob, start = 1) for mob in surrs_5], *[ShowCreation(mob) for mob in surrs_6], Write(possibles[3]))
        self.play(*[Uncreate(mob, start = 1) for mob in surrs_6], *[ShowCreation(mob) for mob in surrs_9], Write(possibles[4]))
        self.play(*[Uncreate(mob, start = 1) for mob in surrs_9], *[ShowCreation(mob) for mob in surrs_10], Write(possibles[5]))
        self.play(*[Uncreate(mob, start = 1) for mob in surrs_10])
        self.wait()
        self.add(surrs_1[0], surrs_2[0], indicates[0], indicates[1]).wait(1)
        self.remove(surrs_1[0], surrs_2[0], indicates[1]).add(surrs_1[1], surrs_6[0], indicates[3]).wait(1)
        self.remove(surrs_1[1], surrs_6[0], indicates[3]).add(surrs_1[2], surrs_10[0], indicates[5]).wait(1)
        self.remove(surrs_1[2], surrs_10[0], indicates[0], indicates[5]).add(surrs_9[0], surrs_2[1], indicates[1], indicates[4]).wait(1)
        self.remove(surrs_9[0], surrs_2[1], indicates[1], indicates[4]).add(surrs_5[0], surrs_6[1], indicates[2], indicates[3]).wait(1)
        self.remove(surrs_5[0], surrs_6[1], indicates[3]).add(surrs_5[1], surrs_10[1], indicates[5]).wait(1)
        self.remove(surrs_5[1], surrs_10[1], indicates[2]).add(surrs_9[1], surrs_10[2], indicates[4]).wait(1)
        self.remove(surrs_9[1], surrs_10[2], indicates[4], indicates[5]).wait(1)
        
        offset_r = 3*RIGHT + 0.5*UP
        buff = 1.2
        lines_h = [Line(1.8*buff*LEFT, 2*buff*RIGHT).shift(i*buff*UP + offset_r) for i in range(-2, 3)]
        lines_h[-1].shift(0.2*buff*DOWN)
        lines_v = [Line(1.8*buff*UP, 2*buff*DOWN).shift(i*buff*RIGHT + offset_r) for i in range(-2, 3)]
        lines_v[0].shift(0.2*buff*RIGHT)
        color_map = {("1", "5", "9"): YELLOW, ("2", "6", "10"): GOLD}
        texs = [MTex('1', tex_to_color_map = color_map).shift(np.array([-0.5, 1.4, 0])*buff + offset_r), 
                MTex('5', tex_to_color_map = color_map).shift(np.array([0.5, 1.4, 0])*buff + offset_r), 
                MTex('9', tex_to_color_map = color_map).shift(np.array([1.5, 1.4, 0])*buff + offset_r), 
                MTex('2', tex_to_color_map = color_map).shift(np.array([-1.4, 0.5, 0])*buff + offset_r), 
                MTex('6', tex_to_color_map = color_map).shift(np.array([-1.4, -0.5, 0])*buff + offset_r), 
                MTex('10', tex_to_color_map = color_map).shift(np.array([-1.4, -1.5, 0])*buff + offset_r), 
                MTex('(1, 2)', tex_to_color_map = color_map).scale(0.8).shift(np.array([-0.5, 0.5, 0])*buff + offset_r), 
                MTex('(1, 6)', tex_to_color_map = color_map).scale(0.8).shift(np.array([-0.5, -0.5, 0])*buff + offset_r), 
                MTex('(1, 10)', tex_to_color_map = color_map).scale(0.8).shift(np.array([-0.5, -1.5, 0])*buff + offset_r), 
                MTex('(5, 6)', tex_to_color_map = color_map).scale(0.8).shift(np.array([0.5, -0.5, 0])*buff + offset_r), 
                MTex('(5, 10)', tex_to_color_map = color_map).scale(0.8).shift(np.array([0.5, -1.5, 0])*buff + offset_r), 
                MTex('(9, 2)', tex_to_color_map = color_map).scale(0.8).shift(np.array([1.5, 0.5, 0])*buff + offset_r), 
                MTex('(9, 10)', tex_to_color_map = color_map).scale(0.8).shift(np.array([1.5, -1.5, 0])*buff + offset_r), ]
        table = VGroup(*lines_h, *lines_v, *texs)
        self.play(*[OverFadeOut(mob, 4*LEFT) for mob in copies + stars], *[FadeOut(mob) for mob in cards], 
                  *[mob.animate.shift(6.5*LEFT) for mob in solutions], *[OverFadeOut(mob, 5.25*LEFT) for mob in possibles], OverFadeOut(probability, 6.5*LEFT),
                  OverFadeIn(table, 4*LEFT), run_time = 2)
        self.wait()
        self.print_mark()
        
        for mob in solutions + texs:
            mob.save_state()
        smaller = Polygon(np.array([-1.75, 1.75, 0])*buff, np.array([-1.75, -0.95, 0])*buff, np.array([0.95, -0.95, 0])*buff, np.array([0.95, 1.75, 0])*buff, color = YELLOW).shift(offset_r)
        self.play(ShowCreation(smaller), *[texs[i].animate.fade(0.75) for i in [2, 5, 8, 10, 11, 12]], 
                  *[solutions[i].animate.scale(0.6).shift(2*0.45*LEFT).fade() for i in [2, 3, 5, 6]])
        self.wait()

        dash = VMobject(color = YELLOW).set_points(DashedLine(2.55*LEFT + 2.25*UP, 2.55*LEFT + 0.25*DOWN).get_all_points())
        self.play(ShowCreation(dash), *[solutions[i][6:].animate.fade(0.75) for i in [0, 1, 4]])
        self.wait()

        # alter_1 = group(0, 0, 1, 2, 1, 2, 1, 2, 1, 2).scale(0.75).move_to(3*LEFT + 2.6*UP)
        # self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in alter_1], lag_ratio = 0.1))
        # self.wait()

        rights = [Heiti("右增", color = RED_E, stroke_color = RED_E).scale(0.5).next_to(position*buff + offset_r, UL, buff = 0.1) for position in (np.array([0, 0, 0]), np.array([0, -1, 0]), np.array([1, -1, 0]))]
        self.play(Uncreate(dash, start = 1), *[solutions[i].animate.restore() for i in [0, 1, 4]], *[Write(mob) for mob in rights]) #FadeOut(alter_1)
        self.wait()
        
        self.play(Transform(smaller, Polygon(np.array([0.05, -0.05, 0])*buff, np.array([0.05, -1.95, 0])*buff, np.array([1.95, -1.95, 0])*buff, np.array([1.95, -0.05, 0])*buff, color = YELLOW).shift(offset_r)), 
                  *[solutions[i].animate.restore().scale(0.6).shift(2*0.45*RIGHT).fade() for i in [0, 1, 2, 3]], *[solutions[i].animate.restore() for i in [5, 6]], 
                  *[texs[i].animate.restore() for i in [2, 5, 10, 12]], *[texs[i].animate.fade(0.75) for i in [0, 3, 6, 7]])
        self.wait()

        dash = VMobject(color = YELLOW).set_points(DashedLine(3.45*LEFT + 0.25*UP, 3.45*LEFT + 1.25*DOWN).get_all_points())
        self.play(ShowCreation(dash), *[solutions[i][:4].animate.fade(0.75) for i in [4, 5, 6]])
        self.wait()

        lefts = [Heiti("左增", color = BLUE_D, stroke_color = BLUE_D).scale(0.5).next_to(position*buff + offset_r, DR, buff = 0.1) for position in (np.array([0, 0, 0]), np.array([0, -1, 0]), np.array([1, -1, 0]))]
        self.play(Uncreate(dash, start = 1), *[solutions[i].animate.restore() for i in [0, 1, 4]], *[Write(mob) for mob in lefts])
        self.wait()

        self.play(FadeOut(smaller), 
                  *[solutions[i].animate.restore().scale(0.6).fade(0.75) for i in [0, 1, 4, 5, 6]], *[solutions[i].animate.restore() for i in [2, 3]], 
                  *[texs[i].animate.restore() for i in [8, 11]], *[texs[i].animate.fade(0.75) for i in [1, 4, 9, 10, 12]])
        self.wait()

        arrow_1 = Arrow(ORIGIN, RIGHT, color = TEAL).next_to(solution_3, LEFT)
        self.play(GrowArrow(arrow_1))
        self.wait()

        surr_1, surr_2 = SurroundingRectangle(solution_3[1:5], color = BLUE, buff = 0.05), SurroundingRectangle(solution_3[5:9], color = RED, buff = 0.05)
        self.play(ShowCreation(surr_1), ShowCreation(surr_2))
        self.wait()

        repeat = Heiti("填充", color = TEAL_E, stroke_color = TEAL_E).scale(0.5).next_to(np.array([-0.5, -1, 0])*buff + offset_r, DOWN, buff = 0.1)
        self.play(FadeOut(surr_1), FadeOut(surr_2), Write(repeat))
        self.wait()

        arrow_2 = Arrow(ORIGIN, RIGHT, color = PURPLE_B).next_to(solution_4, LEFT)
        self.play(Transform(arrow_1, arrow_2))
        self.wait()

        mysterious = Heiti("???", color = PURPLE).scale(0.5).next_to(np.array([1.5, 0, 0])*buff + offset_r, UP, buff = 0.1)
        self.play(Write(mysterious))
        self.wait()

class Video_6(FrameScene):
    def construct(self):
        def card(tex, color_out = GREY, color_in = BLUE_B):
            return VGroup(Square(side_length = 0.6, color = color_out), MTex(tex, color = color_in))
        
        def group(*types: int):
            vgroup = VGroup()
            for i, type in enumerate(types):
                if type == 0:
                    mob = card(str(i+1), GREY_D, GREY_E)
                elif type == 1:
                    mob = card(str(i+1), BLUE, BLUE_B)
                elif type == 2:
                    mob = card(str(i+1), RED, RED_B)
                elif type == 3:
                    mob = card(str(i+1), GOLD, GOLD_B)
                elif type == 4:
                    mob = card(str(i+1), MAROON, MAROON_B)
                vgroup.add(mob.shift((i-4.5)*0.8*RIGHT))
            return vgroup
        
        special_10 = group(1, 0, 1, 2, 1, 2, 1, 2, 0, 2).move_to(2.5*UP)
        special_14 = group(1, 0, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 2).move_to(1.5*UP)
        self.add(special_10).wait()

        self.play(LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in special_14], lag_atio = 0.1, run_time = 1))
        self.wait()

        dice_0 = VGroup(Square(side_length = 0.6), Square(side_length = 0.4, fill_opacity = 1, stroke_width = 0))

        quad_1 = VGroup(*[dice_0.copy().set_color(BLUE).shift((i-1.5)*2*0.8*RIGHT) for i in range(4)])
        quad_2 = VGroup(*[dice_0.copy().set_color(RED).shift((i-1.5)*2*0.8*RIGHT) for i in range(4)]).shift(0.8*DOWN)
        self.play(special_14.save_state().animate.fade(), Write(quad_1), Write(quad_2))
        self.wait()

        self.play(quad_1.animating(path_arc = PI/2).shift(0.8*DL))
        self.wait()
        self.play(quad_2.animating(path_arc = PI).shift(1.6*RIGHT))
        self.play(*[mob.animate.shift(0.4*LEFT) for mob in [quad_1, quad_2]])
        self.wait()
        defect_1, defect_2 = quad_2[0].copy().shift(1.6*LEFT).fade(), quad_1[-1].copy().shift(1.6*RIGHT).fade()
        self.play(*[FadeIn(mob, rate_func = blink(5), run_time = 2) for mob in [defect_1, defect_2]])
        self.wait()
        self.play(*[mob.animate.set_color(GREY_D) for mob in [defect_1, defect_2]])
        self.wait()

        self.play(*[FadeOut(mob) for mob in [quad_1, quad_2, defect_1, defect_2]], special_14.animate.restore())

        quad_1 = VGroup(*[dice_0.copy().set_color(BLUE).shift((i-1.5)*3*0.8*RIGHT) for i in range(4)])
        quad_2 = VGroup(*[dice_0.copy().set_color(RED).shift((i-1.5)*3*0.8*RIGHT) for i in range(4)]).shift(0.8*DOWN)
        quad_3 = VGroup(*[dice_0.copy().set_color(GOLD).shift((i-1.5)*3*0.8*RIGHT) for i in range(4)]).shift(1.6*DOWN)
        self.play(*[FadeIn(mob) for mob in [quad_1, quad_2, quad_3]], special_10.save_state().animate.fade())
        self.wait()

        self.play(quad_1.animating(path_arc = PI/2).shift(0.8*DL), quad_3.animating(path_arc = PI/2).shift(0.8*UR))
        self.wait()
        self.play(quad_2.animating(path_arc = PI).shift(2.4*RIGHT))
        self.play(*[mob.animate.shift(0.8*LEFT) for mob in [quad_1, quad_2, quad_3]])
        self.wait()
        defect_1, defect_2 = quad_2[0].copy().shift(2.4*LEFT).fade(), quad_1[-1].copy().shift(2.4*RIGHT).fade()
        self.play(*[FadeIn(mob, rate_func = blink(5), run_time = 2) for mob in [defect_1, defect_2]])
        self.wait()
        self.play(*[mob.animate.set_color(GREY_D) for mob in [defect_1, defect_2]])
        self.wait()

        self.play(*[FadeOut(mob) for mob in [quad_1, quad_2, quad_3, defect_1, defect_2]], special_10.animate.restore())

        quad_1 = VGroup(*[dice_0.copy().set_color(BLUE).shift((i-1.5)*4*0.8*RIGHT) for i in range(4)])
        quad_2 = VGroup(*[dice_0.copy().set_color(RED).shift((i-1.5)*4*0.8*RIGHT) for i in range(4)]).shift(0.8*DOWN)
        quad_3 = VGroup(*[dice_0.copy().set_color(GOLD).shift((i-1.5)*4*0.8*RIGHT) for i in range(4)]).shift(1.6*DOWN)
        quad_4 = VGroup(*[dice_0.copy().set_color(MAROON).shift((i-1.5)*4*0.8*RIGHT) for i in range(4)]).shift(2.4*DOWN)
        self.play(*[FadeIn(mob) for mob in [quad_1, quad_2, quad_3, quad_4]])
        self.wait()

        self.play(quad_1.animating(path_arc = PI/2).shift(0.8*DL), quad_3.animating(path_arc = PI/2).shift(0.8*UR), quad_4.animating(path_arc = PI/2).shift(1.6*UR))
        self.wait()
        self.play(*[mob.animate.shift(1.2*LEFT) for mob in [quad_1, quad_2, quad_3, quad_4]])
        self.play(quad_2.animating(path_arc = PI).shift(3.2*RIGHT))
        self.wait()
        defect_1, defect_2 = quad_2[0].copy().shift(3.2*LEFT).fade(), quad_1[-1].copy().shift(3.2*RIGHT).fade()
        self.play(*[FadeIn(mob, rate_func = blink(5), run_time = 2) for mob in [defect_1, defect_2]])
        self.wait()
        self.play(*[mob.animate.set_color(GREY_D) for mob in [defect_1, defect_2]])
        self.wait()

        all_die = VGroup(quad_1[0], defect_1, quad_3[0], quad_4[0], 
                         quad_1[1], quad_2[0], quad_3[1], quad_4[1], 
                         quad_1[2], quad_2[1], quad_3[2], quad_4[2], 
                         quad_1[3], quad_2[2], quad_3[3], quad_4[3], 
                         defect_2, quad_2[3])
        special_18 = group(1, 0, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 0, 2).move_to(0.5*UP)
        self.play(ReplacementTransform(all_die, special_18))
        self.wait()

class Video_7(FrameScene):
    def construct(self):
        def card(tex, color_out = GREY, color_in = BLUE_B):
            return VGroup(Square(side_length = 0.6, color = color_out), MTex(tex, color = color_in))
        
        def group(*types: int):
            vgroup = VGroup()
            for i, type in enumerate(types):
                if type == 0:
                    mob = card(str(i+1), GREY_D, GREY_E)
                elif type == 1:
                    mob = card(str(i+1), BLUE, BLUE)
                elif type == 2:
                    mob = card(str(i+1), BLUE_E, BLUE_E)
                elif type == -1:
                    mob = card(str(i+1), RED, RED_B)
                elif type == -2:
                    mob = card(str(i+1), GOLD, GOLD_B)
                elif type == -3:
                    mob = card(str(i+1), MAROON, MAROON_B)
                vgroup.add(mob.shift((i-4.5)*0.8*RIGHT))
            return vgroup.scale(0.75)
        dice_0 = VGroup(VGroup(Polyline(0.3*UR, 0.3*UL, 0.3*DL, color = GREY), Polyline(0.3*DL, 0.3*DR, 0.3*UR, color = BLUE)), 
                        VGroup(Polygon(0.2*UR, 0.2*UL, 0.2*DL, color = GREY, fill_opacity = 1, stroke_width = 0), Polygon(0.2*DL, 0.2*DR, 0.2*UR, color = BLUE, fill_opacity = 1, stroke_width = 0)))
        dice_1 = VGroup(Square(side_length = 0.6), Square(side_length = 0.4, fill_opacity = 1, stroke_width = 0)).set_color(RED)

        offset_6 = 3*LEFT + 1*UP
        buff = 0.8
        lines_h = [Line(1.3*buff*LEFT, 1.5*buff*RIGHT).shift(i*buff*UP + offset_6) for i in (-1.5, -0.5, 0.5, 1.5)]
        lines_h[-1].shift(0.2*buff*DOWN)
        lines_v = [Line(1.3*buff*UP, 1.5*buff*DOWN).shift(i*buff*RIGHT + offset_6) for i in (-1.5, -0.5, 0.5, 1.5)]
        lines_v[0].shift(0.2*buff*RIGHT)
        texs = [MTex('1', color = YELLOW).shift(np.array([0, 0.9, 0])*buff + offset_6), 
                MTex('5', color = YELLOW).shift(np.array([1, 0.9, 0])*buff + offset_6), 
                MTex('2', color = GOLD).shift(np.array([-0.9, 0, 0])*buff + offset_6), 
                MTex('6', color = GOLD).shift(np.array([-0.9, -1, 0])*buff + offset_6), 
                MTex(r'\checkmark').shift(np.array([0, 0, 0])*buff + offset_6), 
                MTex(r'\checkmark').shift(np.array([0, -1, 0])*buff + offset_6), 
                MTex(r'\checkmark').shift(np.array([1, -1, 0])*buff + offset_6),]
        table_6 = VGroup(*lines_h, *lines_v, *texs)
        s6_1 = group(0, 0, 1, 1, 1, 1).scale(0.75).move_to(3*LEFT + 1.5*DOWN)
        s6_2 = group(0, 1, 1, 1, 1, 0).scale(0.75).move_to(3*LEFT + 2*DOWN)
        s6_3 = group(1, 1, 1, 1, 0, 0).scale(0.75).move_to(3*LEFT + 2.5*DOWN)

        offset_10 = 3*RIGHT + 0.6*UP
        lines_h = [Line(1.8*buff*LEFT, 2*buff*RIGHT).shift(i*buff*UP + offset_10) for i in range(-2, 3)]
        lines_h[-1].shift(0.2*buff*DOWN)
        lines_v = [Line(1.8*buff*UP, 2*buff*DOWN).shift(i*buff*RIGHT + offset_10) for i in range(-2, 3)]
        lines_v[0].shift(0.2*buff*RIGHT)
        texs = [MTex('1', color = YELLOW).shift(np.array([-0.5, 1.4, 0])*buff + offset_10), 
                MTex('5', color = YELLOW).shift(np.array([0.5, 1.4, 0])*buff + offset_10), 
                MTex('9', color = YELLOW).shift(np.array([1.5, 1.4, 0])*buff + offset_10), 
                MTex('2', color = GOLD).shift(np.array([-1.4, 0.5, 0])*buff + offset_10), 
                MTex('6', color = GOLD).shift(np.array([-1.4, -0.5, 0])*buff + offset_10), 
                MTex('10', color = GOLD).shift(np.array([-1.4, -1.5, 0])*buff + offset_10), ]
        table_10 = VGroup(*lines_h, *lines_v, *texs)

        self.wait()
        self.fade_in(table_6, s6_1, s6_2, s6_3, table_10)
        self.wait()

        arbitrary_6 = VGroup(*[dice_0.copy().shift(0.8*(i-2.5)*RIGHT) for i in range(6)]).shift(3*UP)
        self.play(LaggedStart(*[FadeIn(mob) for mob in arbitrary_6], run_time = 2, lag_ratio = 0.2))
        self.wait()

        p_1, p_2, p_3, p_4, p_5, p_6, p_7 = np.array([-0.5, 0.5, 0])*buff + offset_10, np.array([-0.5, -0.5, 0])*buff + offset_10, np.array([-0.5, -1.5, 0])*buff + offset_10, np.array([0.5, -0.5, 0])*buff + offset_10, np.array([0.5, -1.5, 0])*buff + offset_10, np.array([1.5, 0.5, 0])*buff + offset_10, np.array([1.5, -1.5, 0])*buff + offset_10
        
        right_6 = VGroup(*[dice_1.copy().shift(0.8*(i+3.5)*RIGHT) for i in range(4)]).shift(3*UP)
        right6_1 = group(0, 0, 1, 1, 1, 1, -1, -1, -1, -1).scale(0.75).move_to(3*RIGHT + 1.5*DOWN)
        right6_2 = group(0, 1, 1, 1, 1, 0, -1, -1, -1, -1).scale(0.75).move_to(3*RIGHT + 2*DOWN)
        right6_3 = group(1, 1, 1, 1, 0, 0, -1, -1, -1, -1).scale(0.75).move_to(3*RIGHT + 2.5*DOWN)
        self.play(LaggedStart(*[FadeIn(mob, 0.3*LEFT) for mob in right_6], lag_ratio = 0.2), LaggedStart(*[FadeIn(mob, 0.3*LEFT) for mob in [right6_1, right6_2, right6_3]], lag_ratio = 0.2), run_time = 1.5)
        self.wait(1, 15)

        checkmarks_right = [MTex(r"\checkmark", color = BLUE).scale(0.8).shift(position + 0.12*DR) for position in [p_1, p_2, p_4]]
        self.play(*[Write(mob) for mob in checkmarks_right])
        self.wait()

        self.play(*[FadeOut(mob) for mob in [right_6, right6_1, right6_2, right6_3]])
        self.wait()

        left_6 = VGroup(*[dice_1.copy().shift(0.8*(i+3.5)*LEFT) for i in range(4)]).shift(3*UP)
        left6_1 = group(-1, -1, -1, -1, 0, 0, 1, 1, 1, 1).scale(0.75).move_to(3*RIGHT + 1.5*DOWN)
        left6_2 = group(-1, -1, -1, -1, 0, 1, 1, 1, 1, 0).scale(0.75).move_to(3*RIGHT + 2*DOWN)
        left6_3 = group(-1, -1, -1, -1, 1, 1, 1, 1, 0, 0).scale(0.75).move_to(3*RIGHT + 2.5*DOWN)
        self.play(LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in left_6], lag_ratio = 0.2), LaggedStart(*[FadeIn(mob, 0.3*LEFT) for mob in [left6_1, left6_2, left6_3]], lag_ratio = 0.2), run_time = 1.5)
        self.wait(1, 15)

        checkmarks_left = [MTex(r"\checkmark", color = RED).scale(0.8).shift(position + 0.12*UL) for position in [p_4, p_5, p_7]]
        self.play(*[Write(mob) for mob in checkmarks_left])
        self.wait()

        self.play(*[FadeOut(mob) for mob in [left_6, left6_1, left6_2, left6_3]])
        self.wait()

        extra6_1 = group(0, 1, 1, 1, 1, -1, -1, -1, -1, 0).scale(0.75).move_to(3*RIGHT + 1.5*DOWN)
        extra6_2 = group(1, 0, 1, -1, 1, -1, 1, -1, 0, -1).scale(0.75).move_to(3*RIGHT + 2*DOWN)
        checkmarks_extra = [MTex(r"\checkmark", color = TEAL).scale(0.8).shift(p_3 + 0.12*UR), MTex(r"\checkmark", color = PURPLE_B).scale(0.8).shift(p_6 + 0.12*DL)]
        self.play(FadeIn(extra6_1, 0.3*LEFT), Write(checkmarks_extra[0]))
        self.wait()
        self.play(FadeIn(extra6_2, 0.3*LEFT), Write(checkmarks_extra[1]))
        self.wait()

        c = checkmarks_right + checkmarks_left + checkmarks_extra
        targets_10 = [MTex(r'\checkmark').shift(position + 8*LEFT) for position in [p_1, p_2, p_3, p_4, p_5, p_6, p_7]]
        indices = [0, 1, 3, 3, 4, 6, 2, 5]

        s10_1 = group(0, 0, 1, 1, 1, 1, 2, 2, 2, 2).scale(0.7).move_to(1.2*LEFT + 2*UP)
        s10_2 = group(0, 1, 1, 1, 1, 0, 2, 2, 2, 2).scale(0.7).move_to(1.2*LEFT + 1.6*UP)
        s10_3 = group(0, 1, 1, 1, 1, 2, 2, 2, 2, 0).scale(0.7).move_to(1.2*LEFT + 1.2*UP)
        s10_4 = group(1, 0, 1, 2, 1, 2, 1, 2, 0, 2).scale(0.7).move_to(1.2*LEFT + 0.8*UP)
        s10_5 = group(1, 1, 1, 1, 0, 0, 2, 2, 2, 2).scale(0.7).move_to(1.2*LEFT + 0.4*UP)
        s10_6 = group(1, 1, 1, 1, 0, 2, 2, 2, 2, 0).scale(0.7).move_to(1.2*LEFT + 0.0*DOWN)
        s10_7 = group(1, 1, 1, 1, 2, 2, 2, 2, 0, 0).scale(0.7).move_to(1.2*LEFT + 0.4*DOWN)
        s10 = [s10_1, s10_2, s10_3, s10_4, s10_5, s10_6, s10_7]

        offset_14 = 4.5*RIGHT + 0.2*UP
        lines_h = [Line(2.3*buff*LEFT, 2.5*buff*RIGHT).shift((i+0.5)*buff*UP + offset_14) for i in range(-3, 3)]
        lines_h[-1].shift(0.2*buff*DOWN)
        lines_v = [Line(2.3*buff*UP, 2.5*buff*DOWN).shift((i+0.5)*buff*RIGHT + offset_14) for i in range(-3, 3)]
        lines_v[0].shift(0.2*buff*RIGHT)
        color_map = {("1", "5", "9", "13"): YELLOW, ("2", "6", "10", "14"): GOLD}
        texs = [MTex('1', color = YELLOW).shift(np.array([-1, 1.9, 0])*buff + offset_14), 
                MTex('5', color = YELLOW).shift(np.array([0, 1.9, 0])*buff + offset_14), 
                MTex('9', color = YELLOW).shift(np.array([1, 1.9, 0])*buff + offset_14), 
                MTex('13', color = YELLOW).shift(np.array([2, 1.9, 0])*buff + offset_14), 
                MTex('2', color = GOLD).shift(np.array([-1.9, 1, 0])*buff + offset_14), 
                MTex('6', color = GOLD).shift(np.array([-1.9, 0, 0])*buff + offset_14), 
                MTex('10', color = GOLD).shift(np.array([-1.9, -1, 0])*buff + offset_14), 
                MTex('14', color = GOLD).shift(np.array([-1.9, -2, 0])*buff + offset_14), ]
        table_14 = VGroup(*lines_h, *lines_v, *texs)

        patch_10 = VGroup(*[dice_0.copy().shift(0.8*(i+1.5)*RIGHT) for i in range(4)]).shift(3*UP)

        self.play(*[OverFadeOut(mob, 4*LEFT) for mob in [table_6, s6_1, s6_2, s6_3]], *[OverFadeOut(mob, 8*LEFT) for mob in [extra6_1, extra6_2]], 
                  *[mob.animate.shift(8*LEFT) for mob in [table_10]], *[Transform(c[i], targets_10[indices[i]]) for i in range(8)], 
                  *[OverFadeIn(mob, 8*LEFT) for mob in [table_14] + s10], 
                  arbitrary_6.animate.shift(1.6*LEFT), FadeIn(patch_10, 1.6*LEFT), run_time = 2)
        offset_10 += 8*LEFT
        arbitrary_10 = VGroup(*[dice_0.copy().shift(0.8*(i-4.5)*RIGHT) for i in range(10)]).shift(3*UP)
        self.remove(arbitrary_6, patch_10).add(arbitrary_10).wait()
        
        right_10 = VGroup(*[dice_1.copy().shift(0.8*(i+5.5)*RIGHT) for i in range(4)]).shift(3*UP)
        right10_1 = group(0, 0, 1, 1, 1, 1, 2, 2, 2, 2, -1, -1, -1, -1).scale(0.6).move_to(0.0*RIGHT + 1*DOWN)
        right10_2 = group(0, 1, 1, 1, 1, 0, 2, 2, 2, 2, -1, -1, -1, -1).scale(0.6).move_to(0.0*RIGHT + 1.35*DOWN)
        right10_3 = group(0, 1, 1, 1, 1, 2, 2, 2, 2, 0, -1, -1, -1, -1).scale(0.6).move_to(0.0*RIGHT + 1.7*DOWN)
        right10_4 = group(1, 0, 1, 2, 1, 2, 1, 2, 0, 2, -1, -1, -1, -1).scale(0.6).move_to(0.0*RIGHT + 2.05*DOWN)
        right10_5 = group(1, 1, 1, 1, 0, 0, 2, 2, 2, 2, -1, -1, -1, -1).scale(0.6).move_to(0.0*RIGHT + 2.4*DOWN)
        right10_6 = group(1, 1, 1, 1, 0, 2, 2, 2, 2, 0, -1, -1, -1, -1).scale(0.6).move_to(0.0*RIGHT + 2.75*DOWN)
        right10_7 = group(1, 1, 1, 1, 2, 2, 2, 2, 0, 0, -1, -1, -1, -1).scale(0.6).move_to(0.0*RIGHT + 3.1*DOWN)
        rights_10 = [right10_1, right10_2, right10_3, right10_4, right10_5, right10_6, right10_7]
        self.play(LaggedStart(*[FadeIn(mob, 0.3*LEFT) for mob in right_10], lag_ratio = 0.2), LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in rights_10], lag_ratio = 0.2), run_time = 1.5)
        self.wait(1, 15)
        
        offset_right = -offset_10 + offset_14 + 0.5*buff*UL + 0.12*DR
        checkmarks_right = [MTex(r"\checkmark", color = BLUE).scale(0.8).move_to(previous).shift(offset_right) for previous in targets_10]
        self.play(*[Write(mob) for mob in checkmarks_right])
        self.wait()

        self.play(*[FadeOut(mob) for mob in [right_10] + rights_10])
        self.wait()

        left_10 = VGroup(*[dice_1.copy().shift(0.8*(i+5.5)*LEFT) for i in range(4)]).shift(3*UP)
        left10_1 = group(-1, -1, -1, -1, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2).scale(0.6).move_to(0.0*RIGHT + 1*DOWN)
        left10_2 = group(-1, -1, -1, -1, 0, 1, 1, 1, 1, 0, 2, 2, 2, 2).scale(0.6).move_to(0.0*RIGHT + 1.35*DOWN)
        left10_3 = group(-1, -1, -1, -1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0).scale(0.6).move_to(0.0*RIGHT + 1.7*DOWN)
        left10_4 = group(-1, -1, -1, -1, 1, 0, 1, 2, 1, 2, 1, 2, 0, 2).scale(0.6).move_to(0.0*RIGHT + 2.05*DOWN)
        left10_5 = group(-1, -1, -1, -1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2).scale(0.6).move_to(0.0*RIGHT + 2.4*DOWN)
        left10_6 = group(-1, -1, -1, -1, 1, 1, 1, 1, 0, 2, 2, 2, 2, 0).scale(0.6).move_to(0.0*RIGHT + 2.75*DOWN)
        left10_7 = group(-1, -1, -1, -1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0).scale(0.6).move_to(0.0*RIGHT + 3.1*DOWN)
        lefts_10 = [left10_1, left10_2, left10_3, left10_4, left10_5, left10_6, left10_7]
        self.play(LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in left_10], lag_ratio = 0.2), LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in lefts_10], lag_ratio = 0.2), run_time = 1.5)
        self.wait(1, 15)
        
        offset_left = -offset_10 + offset_14 + 0.5*buff*DR + 0.12*UL
        checkmarks_left = [MTex(r"\checkmark", color = RED).scale(0.8).move_to(previous).shift(offset_left) for previous in targets_10]
        self.play(*[Write(mob) for mob in checkmarks_left])
        self.wait()

        self.play(*[FadeOut(mob) for mob in [left_10] + lefts_10])
        self.wait()

        p_14 = []
        for i in range(4):
            for j in range(4):
                if i-j != 1:
                    p_14.append(np.array([i-1, 1-j, 0])*buff + offset_14)
        extra10_1 = group(0, 1, 1, 1, 1, -1, -1, -1, -1, -2, -2, -2, -2, 0).scale(0.75).move_to(3.5*RIGHT + 2.1*DOWN)
        extra10_2 = group(1, 0, -2, 1, -1, -2, 1, -1, -2, 1, -1, -2, 0, -1).scale(0.75).move_to(3.5*RIGHT + 2.6*DOWN)
        checkmarks_extra = [MTex(r"\checkmark", color = TEAL).scale(0.8).shift(p_14[3] + 0.12*UR), MTex(r"\checkmark", color = PURPLE_B).scale(0.8).shift(p_14[10] + 0.12*DL)]
        self.play(FadeIn(extra10_1, 0.3*RIGHT), Write(checkmarks_extra[0]))
        self.wait()
        self.play(FadeIn(extra10_2, 0.3*RIGHT), Write(checkmarks_extra[1]))
        self.wait()

        offset_18 = 3.5*RIGHT + 0.2*DOWN
        lines_h = [Line(2.8*buff*LEFT, 3*buff*RIGHT).shift(i*buff*UP + offset_18) for i in range(-3, 4)]
        lines_h[-1].shift(0.2*buff*DOWN)
        lines_v = [Line(2.8*buff*UP, 3*buff*DOWN).shift(i*buff*RIGHT + offset_18) for i in range(-3, 4)]
        lines_v[0].shift(0.2*buff*RIGHT)
        texs_h = [MTex(str(4*i+1), color = YELLOW).shift(np.array([-1.5+i, 2.4, 0])*buff + offset_18) for i in range(5)]
        texs_v = [MTex(str(4*i+2), color = GOLD).shift(np.array([-2.4, 1.5-i, 0])*buff + offset_18) for i in range(5)]
        table_18 = VGroup(*lines_h, *lines_v, *texs_h, *texs_v)

        patch_14 = VGroup(*[dice_0.copy().shift(0.8*(i+3.5)*RIGHT) for i in range(4)]).shift(3*UP)

        self.play(*[OverFadeOut(mob, 8*LEFT) for mob in [table_10, extra10_1, extra10_2] + s10 + c], 
                  *[mob.animate.shift(8*LEFT) for mob in [table_14]], *[OverFadeIn(mob, 8*LEFT) for mob in [table_18]], 
                  *[mob.animate.scale(1.25).shift(0.12*UL).set_color(WHITE).shift(8*LEFT) for mob in checkmarks_right], 
                  *[mob.animate.scale(1.25).shift(0.12*DR).set_color(WHITE).shift(8*LEFT) for mob in checkmarks_left], 
                  checkmarks_extra[0].animate.scale(1.25).shift(0.12*DL).set_color(WHITE).shift(8*LEFT), checkmarks_extra[1].animate.scale(1.25).shift(0.12*UR).set_color(WHITE).shift(8*LEFT), 
                  arbitrary_10.animate.shift(1.6*LEFT), FadeIn(patch_14, 1.6*LEFT), run_time = 2)
        offset_14 += 8*LEFT
        arbitrary_14 = VGroup(*[dice_0.copy().shift(0.8*(i-6.5)*RIGHT) for i in range(14)]).shift(3*UP)
        checkmarks_14 = [MTex(r'\checkmark').shift(position + 8*LEFT) for position in p_14]
        self.remove(arbitrary_10, patch_14, *checkmarks_right, *checkmarks_left, *checkmarks_extra).add(arbitrary_14, *checkmarks_14).wait()

        right_14 = VGroup(*[dice_1.copy().shift(0.8*(i+5.5)*RIGHT) for i in range(4)]).shift(3*UP)
        self.play(arbitrary_14.animate.shift(1.6*LEFT), FadeIn(right_14, 1.6*LEFT))
        self.wait()
        offset_right = -offset_14 + offset_18 + 0.5*buff*UL + 0.12*DR
        checkmarks_right = [MTex(r"\checkmark", color = BLUE).scale(0.8).move_to(previous).shift(offset_right) for previous in checkmarks_14]
        self.play(*[TransformFromCopy(mob1, mob2) for mob1, mob2 in zip(checkmarks_14, checkmarks_right)])
        self.wait()

        left_14 = VGroup(*[dice_1.copy().shift(0.8*(i+5.5)*LEFT) for i in range(4)]).shift(3*UP)
        self.play(arbitrary_14.animate.shift(3.2*RIGHT), OverFadeIn(left_14, 3.2*RIGHT), OverFadeOut(right_14, 3.2*RIGHT), run_time = 2)
        self.wait()
        offset_left = -offset_14 + offset_18 + 0.5*buff*DR + 0.12*UL
        checkmarks_left = [MTex(r"\checkmark", color = RED).scale(0.8).move_to(previous).shift(offset_left) for previous in checkmarks_14]
        self.play(*[TransformFromCopy(mob1, mob2) for mob1, mob2 in zip(checkmarks_14, checkmarks_left)])
        self.wait()

        p_18 = []
        for i in range(5):
            for j in range(5):
                if i-j != 1:
                    p_18.append(np.array([i-1.5, 1.5-j, 0])*buff + offset_18)
        extra14_1 = group(0, 1, 1, 1, 1, -1, -1, -1, -1, -2, -2, -2, -2, -3, -3, -3, -3, 0).scale(0.75).move_to(3*LEFT + 2.1*DOWN)
        extra14_2 = group(1, 0, -2, -3, 1, -1, -2, -3, 1, -1, -2, -3, 1, -1, -2, -3, 0, -1).scale(0.75).move_to(3*LEFT + 2.6*DOWN)
        checkmarks_extra = [MTex(r"\checkmark", color = TEAL).scale(0.8).shift(p_18[4] + 0.12*UR), MTex(r"\checkmark", color = PURPLE_B).scale(0.8).shift(p_18[17] + 0.12*DL)]
        self.play(FadeIn(extra14_1, 0.3*RIGHT), FadeIn(extra14_2, 0.3*RIGHT), FadeOut(arbitrary_14), FadeOut(left_14))
        self.wait()
        self.play(Write(checkmarks_extra[0]), Write(checkmarks_extra[1]))
        self.wait()

        offset_22 = 2.5*RIGHT + 0.2*UP
        lines_h = [Line(3.3*buff*LEFT, 3.5*buff*RIGHT).shift((i+0.5)*buff*UP + offset_22) for i in range(-4, 4)]
        lines_h[-1].shift(0.2*buff*DOWN)
        lines_v = [Line(3.3*buff*UP, 3.5*buff*DOWN).shift((i+0.5)*buff*RIGHT + offset_22) for i in range(-4, 4)]
        lines_v[0].shift(0.2*buff*RIGHT)
        texs_h = [MTex(str(4*i+1), color = YELLOW).shift(np.array([-2+i, 2.9, 0])*buff + offset_22) for i in range(6)]
        texs_v = [MTex(str(4*i+2), color = GOLD).shift(np.array([-2.9, 2-i, 0])*buff + offset_22) for i in range(6)]
        table_22 = VGroup(*lines_h, *lines_v, *texs_h, *texs_v)

        self.play(*[OverFadeOut(mob, 8*LEFT) for mob in [table_14, extra14_1, extra14_2] + checkmarks_14], 
                  *[mob.animate.shift(8*LEFT) for mob in [table_18]], *[OverFadeIn(mob, 8*LEFT) for mob in [table_22]], 
                  *[mob.animate.scale(1.25).shift(0.12*UL).set_color(WHITE).shift(8*LEFT) for mob in checkmarks_right], 
                  *[mob.animate.scale(1.25).shift(0.12*DR).set_color(WHITE).shift(8*LEFT) for mob in checkmarks_left], 
                  checkmarks_extra[0].animate.scale(1.25).shift(0.12*DL).set_color(WHITE).shift(8*LEFT), checkmarks_extra[1].animate.scale(1.25).shift(0.12*UR).set_color(WHITE).shift(8*LEFT), 
                  run_time = 2)
        offset_18 += 8*LEFT
        checkmarks_18 = [MTex(r'\checkmark').shift(position + 8*LEFT) for position in p_18]
        self.remove(*checkmarks_right, *checkmarks_left, *checkmarks_extra).add(*checkmarks_18).wait()

        offset_right = -offset_18 + offset_22 + 0.5*buff*UL + 0.12*DR
        checkmarks_right = [MTex(r"\checkmark", color = BLUE).scale(0.8).move_to(previous).shift(offset_right) for previous in checkmarks_18]
        self.play(*[TransformFromCopy(mob1, mob2) for mob1, mob2 in zip(checkmarks_18, checkmarks_right)])
        self.wait()

        offset_left = -offset_18 + offset_22 + 0.5*buff*DR + 0.12*UL
        checkmarks_left = [MTex(r"\checkmark", color = RED).scale(0.8).move_to(previous).shift(offset_left) for previous in checkmarks_18]
        self.play(*[TransformFromCopy(mob1, mob2) for mob1, mob2 in zip(checkmarks_18, checkmarks_left)])
        self.wait()

        p_22 = []
        for i in range(6):
            for j in range(6):
                if i-j != 1:
                    p_22.append(np.array([i-2, 2-j, 0])*buff + offset_22)
        checkmarks_extra = [MTex(r"\checkmark", color = TEAL).scale(0.8).shift(p_22[5] + 0.12*UR), MTex(r"\checkmark", color = PURPLE_B).scale(0.8).shift(p_22[-5] + 0.12*DL)]
        self.play(Write(checkmarks_extra[0]), Write(checkmarks_extra[1]))
        self.wait()

        self.play(*[OverFadeOut(mob, 6*LEFT) for mob in [table_18] + checkmarks_18], 
                  *[mob.animate.shift(6*LEFT) for mob in [table_22]], 
                  *[mob.animate.scale(1.25).shift(0.12*UL).set_color(WHITE).shift(6*LEFT) for mob in checkmarks_right], 
                  *[mob.animate.scale(1.25).shift(0.12*DR).set_color(WHITE).shift(6*LEFT) for mob in checkmarks_left], 
                  checkmarks_extra[0].animate.scale(1.25).shift(0.12*DL).set_color(WHITE).shift(6*LEFT), checkmarks_extra[1].animate.scale(1.25).shift(0.12*UR).set_color(WHITE).shift(6*LEFT), 
                  run_time = 2)
        checkmarks_22 = [MTex(r'\checkmark').shift(position + 6*LEFT) for position in p_22]
        self.remove(*checkmarks_right, *checkmarks_left, *checkmarks_extra).add(*checkmarks_22).wait()

        factor_5 = MTex(r"22=4\times5 + 2", tex_to_color_map = {r"22": TEAL, r"4": GREEN_B, r"5": BLUE}).shift(2*UP + 2.5*RIGHT)
        self.play(Write(factor_5))
        self.wait()

        p_5 = MTex(r"P_5&=\frac{(5+1)^2-5}{C_{4\times5 + 2}^2}\\&=\frac{31}{231}>\frac{1}{8}", tex_to_color_map = {r"P": YELLOW, r"4": GREEN_B, r"5": BLUE, r"\frac{1}{8}": YELLOW}).shift(0.5*DOWN + 2.5*RIGHT)
        self.play(Write(p_5[3:11]))
        self.wait()
        self.play(Write(p_5[12:19]))
        self.wait()
        self.play(Write(VGroup(*p_5[:3], p_5[11], p_5[19:])))
        self.wait()

        p_m = MTex(r"P_m&=\frac{(m+1)^2-m}{C_{4\times m + 2}^2}\\&=\frac{m^2+m+1}{8m^2+6m+1}>\frac{1}{8}", tex_to_color_map = {r"P": YELLOW, r"4": GREEN_B, r"m": BLUE, r"\frac{1}{8}": YELLOW})
        p_m.shift(p_5[2].get_center() - p_m[2].get_center())
        self.play(Transform(p_5[:20], p_m[:20]), Transform(p_5[-4:], p_m[-4:]), FadeTransform(p_5[20:-4], p_m[20:-4], stretch = False))
        self.wait()
        self.play(FadeIn(self.shade.shift(7.5*RIGHT)))
        self.wait()

class Video_8(FrameScene):

    def construct(self):
        offset_22 = 3.5*LEFT + 0.2*UP
        buff = 0.8
        lines_h = [Line(3.3*buff*LEFT, 3.5*buff*RIGHT).shift((i+0.5)*buff*UP + offset_22) for i in range(-4, 4)]
        lines_h[-1].shift(0.2*buff*DOWN)
        lines_v = [Line(3.3*buff*UP, 3.5*buff*DOWN).shift((i+0.5)*buff*RIGHT + offset_22) for i in range(-4, 4)]
        lines_v[0].shift(0.2*buff*RIGHT)
        texs_h = [MTex(str(4*i+1), color = YELLOW).shift(np.array([-2+i, 2.9, 0])*buff + offset_22) for i in range(6)]
        texs_v = [MTex(str(4*i+2), color = GOLD).shift(np.array([-2.9, 2-i, 0])*buff + offset_22) for i in range(6)]
        p_22 = []
        c_22 = []
        for i in range(6):
            for j in range(6):
                if i-j != 1:
                    p_22.append(np.array([i-2, 2-j, 0])*buff + offset_22)
                else:
                    c_22.append(np.array([i-2, 2-j, 0])*buff + offset_22)
        checkmarks_22 = [MTex(r'\checkmark').shift(position) for position in p_22]
        table_22 = VGroup(*lines_h, *lines_v, *texs_h, *texs_v, *checkmarks_22)
        self.add(table_22).wait()

        crosses = [Text(r"✗", font = "simsun", color = RED).scale(0.9).shift(position) for position in c_22]
        self.play(Write(VGroup(*crosses)))
        self.wait()

        self.clear()
        offset_26 = 3.5*LEFT + 0.2*UP
        buff = 0.7
        lines_h = [Line(3.9*buff*LEFT, 4*buff*RIGHT).shift(i*buff*UP + offset_26) for i in range(-4, 5)]
        lines_h[-1].shift(0.1*buff*DOWN)
        lines_v = [Line(3.9*buff*UP, 4*buff*DOWN).shift(i*buff*RIGHT + offset_26) for i in range(-4, 5)]
        lines_v[0].shift(0.1*buff*RIGHT)
        texs_h = [MTex(str(4*i+1), color = YELLOW).scale(0.9).shift(np.array([-2.5+i, 3.45, 0])*buff + offset_26) for i in range(7)]
        texs_v = [MTex(str(4*i+2), color = GOLD).scale(0.9).shift(np.array([-3.45, 2.5-i, 0])*buff + offset_26) for i in range(7)]
        p_26 = []
        c_26 = []
        for i in range(7):
            for j in range(7):
                if i-j != 1:
                    p_26.append(np.array([i-2.5, 2.5-j, 0])*buff + offset_26)
                else:
                    c_26.append(np.array([i-2.5, 2.5-j, 0])*buff + offset_26)
        checkmarks_26 = [MTex(r'\checkmark').shift(position) for position in p_26]
        table_26 = VGroup(*lines_h, *lines_v, *texs_h, *texs_v, *checkmarks_26)
        self.fade_in(table_26).wait()

        crosses = [(Text(r"✗", font = "simsun", color = RED).scale(0.9) if i != 2 and i != 3 else MTex(r'\checkmark', color = GREEN)).shift(position) for i, position in enumerate(c_26)]
        self.play(Write(VGroup(*crosses)))
        self.wait()

        def card(tex, color_out = GREY, color_in = BLUE_B):
            return VGroup(Square(side_length = 0.6, color = color_out), MTex(tex, color = color_in))
        
        colors_out = [GREY_D, BLUE, RED, GOLD, MAROON, TEAL, ORANGE, GREEN, PURPLE_B, YELLOW]
        colors_in = [GREY_E, BLUE_B, RED_B, GOLD_B, MAROON_B, TEAL_B, interpolate_color(ORANGE, YELLOW, 0.5), GREEN_B, PURPLE_A, YELLOW_B]
        def group(*types: int, num: int = 10):
            vgroup = VGroup()
            for i, color_type in enumerate(types):
                mob = card(str(i+1), colors_out[color_type], colors_in[color_type])
                row, column = i//num, i%num
                vgroup.add(mob.shift(column*0.8*RIGHT + row*0.8*DOWN))
            return vgroup.scale(0.75).center()
        group_1 = group(1, 2, 3, 2, 4, 2, 3, 2, 1, 0, 3, 4, 0, 5, 3, 5, 1, 5, 4, 5, 6, 6, 6, 6, 1, 4).shift(3*RIGHT + 2*UP)
        group_2 = group(1, 2, 3, 3, 3, 3, 4, 1, 4, 2, 4, 5, 4, 0, 1, 5, 0, 2, 6, 5, 6, 1, 6, 5, 6, 2).shift(3*RIGHT + DOWN)
        self.play(FadeIn(group_1, 0.5*UP), FadeIn(group_2, 0.5*UP))
        self.wait()

        self.fade_out()
        offset_30 = 3.5*LEFT + 0.2*UP
        buff = 0.7
        lines_h = [Line(4.4*buff*LEFT, 4.5*buff*RIGHT).shift((i+0.5)*buff*UP + offset_30) for i in range(-5, 5)]
        lines_h[-1].shift(0.1*buff*DOWN)
        lines_v = [Line(4.4*buff*UP, 4.5*buff*DOWN).shift((i+0.5)*buff*RIGHT + offset_30) for i in range(-5, 5)]
        lines_v[0].shift(0.1*buff*RIGHT)
        texs_h = [MTex(str(4*i+1), color = YELLOW).scale(0.9).shift(np.array([-3+i, 3.95, 0])*buff + offset_30) for i in range(8)]
        texs_v = [MTex(str(4*i+2), color = GOLD).scale(0.9).shift(np.array([-3.95, 3-i, 0])*buff + offset_30) for i in range(8)]
        p_30 = []
        c_30 = []
        for i in range(8):
            for j in range(8):
                if i-j != 1 or (i >= 3 and i <= 5):
                    p_30.append(np.array([i-3, 3-j, 0])*buff + offset_30)
                else:
                    c_30.append(np.array([i-3, 3-j, 0])*buff + offset_30)
        checkmarks_30 = [MTex(r'\checkmark').shift(position) for position in p_30]
        table_30 = VGroup(*lines_h, *lines_v, *texs_h, *texs_v, *checkmarks_30)
        self.fade_in(table_30).wait()

        crosses = [(Text(r"✗", font = "simsun", color = RED).scale(0.9) if i != 1 and i != 2 else MTex(r'\checkmark', color = GREEN)).shift(position) for i, position in enumerate(c_30)]
        self.play(Write(VGroup(*crosses)))
        self.wait()

        group_1 = group(1, 2, 1, 3, 1, 0, 1, 2, 0, 3, 4, 5, 4, 2, 4, 3, 4, 5, 6, 2, 6, 3, 6, 5, 6, 7, 7, 7, 7, 5).shift(3.5*RIGHT + 2*UP)
        group_2 = group(1, 2, 2, 2, 2, 3, 1, 3, 4, 3, 5, 3, 1, 5, 6, 4, 5, 6, 1, 5, 6, 0, 4, 6, 0, 7, 7, 7, 7, 4).shift(3.5*RIGHT + DOWN)
        self.play(FadeIn(group_1, 0.5*UP), FadeIn(group_2, 0.5*UP))
        self.wait()

        self.fade_out()
        offset_34 = 3.5*LEFT + 0.2*UP
        buff = 0.6
        lines_h = [Line(5*buff*LEFT, 5*buff*RIGHT).shift(i*buff*UP + offset_34) for i in range(-5, 6)]
        lines_v = [Line(5*buff*UP, 5*buff*DOWN).shift(i*buff*RIGHT + offset_34) for i in range(-5, 6)]
        texs_h = [MTex(str(4*i+1), color = YELLOW).scale(0.8).shift(np.array([-3.5+i, 4.5, 0])*buff + offset_34) for i in range(9)]
        texs_v = [MTex(str(4*i+2), color = GOLD).scale(0.8).shift(np.array([-4.5, 3.5-i, 0])*buff + offset_34) for i in range(9)]
        p_34 = []
        c_34 = []
        for i in range(9):
            for j in range(9):
                if i-j != 1 or (i >= 2 and i <= 7):
                    p_34.append(np.array([i-3.5, 3.5-j, 0])*buff + offset_34)
                else:
                    c_34.append(np.array([i-3.5, 3.5-j, 0])*buff + offset_34)
        checkmarks_34 = [MTex(r'\checkmark').scale(0.9).shift(position) for position in p_34]
        table_34 = VGroup(*lines_h, *lines_v, *texs_h, *texs_v, *checkmarks_34)
        self.fade_in(table_34).wait()

        crosses = [MTex(r'\checkmark', color = GREEN).scale(0.9).shift(position) for position in c_34]
        self.play(Write(VGroup(*crosses)))
        self.wait()

        group_1 = group(1, 0, 2, 1, 0, 3, 1, 4, 3, 1, 4, 3, 2, 4, 3, 5, 4, 6, 6, 6, 6, 5, 2, 7, 7, 7, 7, 5, 8, 8, 8, 8, 2, 5).shift(3.5*RIGHT + 2*UP)
        group_2 = group(1, 2, 3, 3, 3, 3, 1, 4, 4, 4, 4, 2, 1, 5, 5, 5, 5, 6, 1, 7, 6, 2, 7, 6, 8, 7, 6, 8, 7, 0, 8, 2, 0, 8).shift(3.5*RIGHT + 1.5*DOWN)
        self.play(FadeIn(group_1, 0.5*UP), FadeIn(group_2, 0.5*UP))
        self.wait()

        self.fade_out()


#################################################################### 

class Template(FrameScene):

    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        