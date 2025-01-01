from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        COLORA, COLORB = PINK, BLUE
        alice, bob = SVGMobject("Alice.svg", color = COLORA, **background_dic).shift(4*LEFT + DOWN), SVGMobject("Bob.svg", color = COLORB, **background_dic).shift(4*RIGHT + DOWN)
        
        self.add(bob).wait()

        alice.shift(4.5*LEFT)
        for _ in range(3):
            self.play(alice.animating(path_arc = -PI/4).shift(1.5*RIGHT), rate_func = linear, run_time = 8/30, frames = 8)
            self.wait(0, 2)
        self.wait()

        start_a, start_b = alice.get_right(), bob.get_left()
        def talk(p1: np.ndarray, p2: np.ndarray, color = WHITE):
            shape = p2-p1
            arc = Arc(-PI/2, PI/2, color = color).scale(shape, min_scale_factor = None)
            arc.shift(p1 - arc.get_start())
            return arc
        frac_0 = MTex(r"\frac{1}{89}").next_to(3*LEFT + 0.5*DOWN, UR)
        line_0 = Underline(frac_0, buff = 0.2, color = COLORA)
        talk_0 = VGroup(frac_0, line_0, talk(start_a, line_0.get_center(), color = COLORA))
        self.play(GrowFromPoint(talk_0, start_a, path_arc = PI/2))
        self.wait()

        frac_1 = MTex(r"1+2+3+4+\cdots = -\frac{1}{12}").scale(0.8).next_to(3*RIGHT + 0*UP, UL)
        line_1 = Underline(frac_1, buff = 0.2, color = COLORB)
        talk_1 = VGroup(frac_1, line_1, talk(start_b, line_1.get_center(), color = COLORB))
        self.play(GrowFromPoint(talk_1, start_b, path_arc = -PI/2), talk_0.animate.shift(2*UP))
        self.wait()

        frac_2 = MTex(r"\frac{1}{89}=0.01123595505617977\cdots").scale(0.8).next_to(3*LEFT + 0*UP, UR)
        line_2 = Underline(frac_2, buff = 0.2, color = COLORA)
        talk_2 = VGroup(frac_2, line_2, talk(start_a, line_2.get_center(), color = COLORA))
        self.play(GrowFromPoint(talk_2, start_a, path_arc = PI/2), *[mob.animate.shift(2.5*UP) for mob in [talk_0, talk_1]])
        self.wait()

        last = []
        for i in range(5):
            self.remove(*last)
            frac_2[i+8].set_color(YELLOW)
            last = [SurroundingRectangle(frac_2[i+8])]
            self.add(*last).wait(0, 12)
        self.remove(*last).wait()

        t_0 = frac_2[13].set_color(RED)
        last = SurroundingRectangle(t_0, color = RED)
        self.add(last).play(*[FadeOut(mob) for mob in [talk_0, talk_1]])
        self.wait()

        numbers = MTex("0123456789", color = YELLOW).scale(0.8)
        h = 0.4*UP
        extra_2_0 = numbers[8].copy().move_to(t_0).shift(h)
        extra_2_1 = numbers[1].copy().move_to(t_0).shift(h*2)
        self.play(TransformFromCopy(t_0, extra_2_0), TransformFromCopy(t_0, extra_2_1), 
                  Transform(last, SurroundingRectangle(VGroup(extra_2_0, extra_2_1))))
        self.wait()

        t_1 = frac_2[14]
        extras_3 = VGroup(numbers[3].copy().move_to(t_1).shift(h*2), numbers[2].copy().move_to(t_1).shift(h*3))
        self.play(FadeOut(last), *[TransformFromCopy(t_1, mob) for mob in extras_3])
        self.wait(1)
        extras_4 = VGroup(numbers[1].copy().move_to(frac_2[15]).shift(h*3), numbers[3].copy().move_to(frac_2[15]).shift(h*4))
        self.add(extras_4).wait(1)
        extras_5 = VGroup(numbers[4].copy().move_to(frac_2[16]).shift(h*4), numbers[5].copy().move_to(frac_2[16]).shift(h*5))
        self.add(extras_5).wait(1)
        extras_6 = VGroup(numbers[5].copy().move_to(frac_2[17]).shift(h*5), numbers[8].copy().move_to(frac_2[17]).shift(h*6), numbers[1].copy().move_to(frac_2[17]).shift(h*7))
        self.add(extras_6).wait(1)
        extras_7 = VGroup(numbers[9].copy().move_to(frac_2[18]).shift(h*6), numbers[4].copy().move_to(frac_2[18]).shift(h*7), numbers[2].copy().move_to(frac_2[18]).shift(h*8))
        self.add(extras_7).wait(1)
        extras_8 = VGroup(numbers[4].copy().move_to(frac_2[19]).shift(h*7), numbers[3].copy().move_to(frac_2[19]).shift(h*8), numbers[3].copy().move_to(frac_2[19]).shift(h*9))
        self.add(extras_8).wait(1)
        extras_9 = VGroup(numbers[3].copy().move_to(frac_2[20]).shift(h*8), numbers[7].copy().move_to(frac_2[20]).shift(h*9), numbers[6].copy().move_to(frac_2[20]).shift(h*10))
        self.add(extras_9).wait(1)
        self.wait()

        frac_3 = MTex(r"\frac{1}{9899}=0.0001010203050813213455\cdots").scale(0.75).next_to(3*RIGHT + 0*UP, UL)
        line_3 = Underline(frac_3, buff = 0.2, color = COLORB)
        talk_3 = VGroup(frac_3, line_3, talk(start_b, line_3.get_center(), color = COLORB))
        self.play(GrowFromPoint(talk_3, start_b, path_arc = -PI/2), *[mob.animate.shift(2.5*UP) for mob in [talk_2, extra_2_0, extra_2_1, extras_3, extras_4, extras_5, extras_6, extras_7, extras_8, extras_9]])
        self.wait()

        last = []
        frac_3[9:11].set_color(GREY)
        for i in range(10):
            self.remove(*last)
            last = [SurroundingRectangle(frac_3[2*i+11: 2*i+13].set_color(YELLOW if i%2 else GOLD))]
            self.add(*last).wait(0, 12)
        self.remove(*last).wait()

        unexcepted = Heiti("!?", color = YELLOW).scale(2).next_to(alice, UP)
        self.play(GrowFromEdge(unexcepted, DOWN))
        self.wait()

        frac_4 = MTex(r"\frac{1}{998999}=0.000001001002003005008013021034055\cdots").scale(0.55).next_to(3.3*RIGHT + 0*UP, UL)
        line_4 = Underline(frac_4, buff = 0.2, color = COLORB)
        talk_4 = VGroup(frac_4, line_4, talk(start_b, line_4.get_center(), color = COLORB))
        frac_4[11:14].set_color(GREY)
        for i in range(10):
            frac_4[14+3*i:17+3*i].set_color(YELLOW if i%2 else GOLD)
        self.play(GrowFromPoint(talk_4, start_b, path_arc = -PI/2), *[mob.animate.shift(2.5*UP) for mob in [talk_3, talk_2, extra_2_0, extra_2_1, extras_3, extras_4, extras_5, extras_6, extras_7, extras_8, extras_9]])
        self.wait()

        frac_5 = MTex(r"\frac{1}{99989999}=0.00000001000100020003000500080013002100340055\cdots").scale(0.43).next_to(3.3*RIGHT + 0*UP, UL)
        line_5 = Underline(frac_5, buff = 0.2, color = COLORB)
        talk_5 = VGroup(frac_5, line_5, talk(start_b, line_5.get_center(), color = COLORB))
        frac_5[13:17].set_color(GREY)
        for i in range(10):
            frac_5[17+4*i:21+4*i].set_color(YELLOW if i%2 else GOLD)
        self.play(GrowFromPoint(talk_5, start_b, path_arc = -PI/2), *[mob.animate.shift(2.5*UP) for mob in [talk_4, talk_3, talk_2, extra_2_0, extra_2_1, extras_3, extras_4, extras_5, extras_6, extras_7, extras_8, extras_9]])
        self.wait()

class Video_2(FrameScene):
    def construct(self):
        h = 1.0*DOWN
        frac_2_1 = MTex(r"\frac{1}{49}=0.0204081632653061\cdots").scale(0.8)
        frac_2_1.shift(0*h + 3*UP + 5*LEFT - frac_2_1[4].get_center())
        self.wait(1)
        self.play(Write(frac_2_1))
        self.wait()

        target = frac_2_1.generate_target()
        for i in range(5):
            target[7+2*i:9+2*i].set_color(YELLOW if i%2 else GOLD)
        target[17:-3].set_color(GREY)
        self.play(MoveToTarget(frac_2_1), lag_ratio = 0.1)
        self.wait()

        frac_2_2 = MTex(r"\frac{1}{499}=0.002004008016032064128256513026052\cdots").scale(0.8)
        frac_2_2.shift(1*h + 3*UP + 5*LEFT - frac_2_2[5].get_center())
        for i in range(8):
            frac_2_2[8+3*i:11+3*i].set_color(YELLOW if i%2 else GOLD)
        frac_2_2[32:-3].set_color(GREY)
        self.play(Write(frac_2_2))
        self.wait()

        frac_2_3 = MTex(r"\frac{1}{4999}=0.0002000400080016003200640128025605121024204840968193\cdots").scale(0.8)
        frac_2_3.shift(2*h + 3*UP + 5*LEFT - frac_2_3[6].get_center())
        for i in range(12):
            frac_2_3[9+4*i:13+4*i].set_color(YELLOW if i%2 else GOLD)
        frac_2_3[57:-3].set_color(GREY)
        self.play(Write(frac_2_3))
        self.wait()

        frac_1_1 = MTex(r"\frac{1}{89}=0.011235955\cdots").scale(0.8)
        frac_1_1.shift(3*h + 2.5*UP + 5*LEFT - frac_1_1[4].get_center())
        for i in range(5):
            frac_1_1[8+i].set_color(YELLOW if i%2 else GOLD)
        frac_1_1[7].set_color(GREY), frac_1_1[13:-3].set_color(GREY)

        frac_1_2 = MTex(r"\frac{1}{9899}=0.0001010203050813213455904636\cdots").scale(0.8)
        frac_1_2.shift(4*h + 2.5*UP + 5*LEFT - frac_1_2[6].get_center())
        for i in range(10):
            frac_1_2[11+2*i:13+2*i].set_color(YELLOW if i%2 else GOLD)
        frac_1_2[9:11].set_color(GREY), frac_1_2[31:-3].set_color(GREY)

        frac_1_3 = MTex(r"\frac{1}{998999}=0.000001001002003005008013021034055089144233377610988\cdots").scale(0.8)
        frac_1_3.shift(5*h + 2.5*UP + 5*LEFT - frac_1_3[8].get_center())
        for i in range(15):
            frac_1_3[14+3*i:17+3*i].set_color(YELLOW if i%2 else GOLD)
        frac_1_3[11:14].set_color(GREY), frac_1_3[59:-3].set_color(GREY)

        self.play(*[FadeIn(mob, 0.5*UP) for mob in [frac_1_1, frac_1_2, frac_1_3]])
        self.wait()

        divisor_2_1, divisor_2_2, divisor_2_3, divisor_1_1, divisor_1_2, divisor_1_3 = frac_2_1[2:4], frac_2_2[2:5], frac_2_3[2:6], frac_1_1[2:4], frac_1_2[2:6], frac_1_3[2:8]
        for mob in [divisor_2_1, divisor_2_2, divisor_2_3, divisor_1_1, divisor_1_2, divisor_1_3]:
            mob.generate_target().set_color(BLUE)
        divisor_2_1.target[0].set_color(GREEN), divisor_2_2.target[0].set_color(GREEN), divisor_2_3.target[0].set_color(GREEN)
        divisor_1_1.target[0].set_color(GREEN), divisor_1_1.target[1].set_color(GREEN), divisor_1_2.target[0].set_color(GREEN), divisor_1_2.target[2].set_color(GREEN), divisor_1_3.target[0].set_color(GREEN), divisor_1_3.target[3].set_color(GREEN)
        self.play(*[MoveToTarget(mob) for mob in [divisor_2_1, divisor_2_2, divisor_2_3, divisor_1_1, divisor_1_2, divisor_1_3]], 
                  *[IndicateAround(mob) for mob in [divisor_2_1, divisor_2_2, divisor_2_3, divisor_1_1, divisor_1_2, divisor_1_3]])
        self.wait()

        self.play(*[OverFadeOut(mob, 0.5*UP - 3*h) for mob in [frac_2_1, frac_2_2, frac_2_3, frac_1_2, frac_1_3]], 
                  frac_1_1.animate.shift(0.5*UP - 3*h), run_time = 2)
        self.wait()
        
        fibonaccis = [0, 1]
        for _ in range(20):
            fibonaccis.append(fibonaccis[-1] + fibonaccis[-2])

        n = 8
        texs_1 = [MTex(r"a_{"+str(i+1)+r"}=" + str(fibonaccis[i]), tex_to_color_map = {str(fibonaccis[i]): GOLD if i%2 else YELLOW, "a_{"+str(i+1)+"}": BLUE}).scale(0.8) for i in range(n)]
        for i in range(n):
            texs_1[i].shift(5*LEFT + 1.9*UP + i*0.9*DOWN - texs_1[i][2].get_center())
        recursive = MTex(r"a_n=a_{n-1}+a_{n-2}(n\ge 2)", tex_to_color_map = {(r"a_n", r"a_{n-1}", r"a_{n-2}"): BLUE}).scale(0.8).next_to(3*UP)
        self.play(LaggedStart(*[FadeIn(mob, 0.5*UP) for mob in texs_1], lag_ratio = 0.3, run_time = 2))
        self.wait()
        self.play(IndicateAround(texs_1[0], rect_kwargs = {}), IndicateAround(texs_1[1], rect_kwargs = {}))
        self.wait(1)
        self.play(Write(recursive))
        self.wait()

        self.play(LaggedStart(*[mob.animating(rate_func = there_and_back).shift(0.1*UP) for mob in frac_1_1[5:]], lag_ratio = 0.2, run_time = 2))
        self.wait(1)
        texs_2 = [MTex(r"\frac{a_{"+str(i+1)+r"}}{10^{"+str(i+1)+r"}}=0." + r"{0}"*(i if i<=7 else i-1) + str(fibonaccis[i]), isolate = "=", tex_to_color_map = {r"{0}": GREY, str(fibonaccis[i]): GOLD if i%2 else YELLOW, r"a_{"+str(i+1)+"}": BLUE, r"10^{"+str(i+1)+r"}": RED}).scale(0.8) for i in range(n)]
        texs_2[0][-3].set_color(WHITE)
        terms, terms_2, values, values_2 = [], [], [], []
        anims = []
        for i in range(n):
            texs_2[i].shift(5*LEFT + 1.9*UP + i*0.9*DOWN - texs_2[i].get_part_by_tex("=").get_center())
            term, term_2, value = texs_1[i][:2], texs_2[i][2:6], texs_1[i][3:]
            length = len(value.submobjects)
            value_2 = texs_2[i][6:-length]
            terms.append(term), terms_2.append(term_2), values.append(value), values_2.append(value_2)
            anim = AnimationGroup(term.save_state().animate.move_to(texs_2[i][:2]), follow(term_2, term, FadeIn), 
                    value.save_state().animating(rate_func = rush_from).move_to(texs_2[i][-length:]), Write(value_2))
            anims.append(anim)
        self.play(LaggedStart(*anims, lag_ratio = 0.5))
        self.wait()

        self.play(LaggedStart(*[TransformFromCopy(texs_1[i][-1], frac_1_1[7+i].copy(), remover = True) for i in range(6)], lag_ratio = 0.5, remover = True))
        self.wait()

        series = MTex(r"\frac{1}{89} = \sum_{n=1}^{\infty}\frac{a_n}{10^n}", tex_to_color_map = {r"89": GREEN, r"a_n": BLUE, r"10^n": RED}).scale(0.8)
        series.shift(frac_1_1[4].get_center() - series[4].get_center())
        self.play(FadeOut(frac_1_1[5:]))
        self.play(Write(series[5:]))
        self.remove(frac_1_1).add(series).wait()

        notice = MTex(r"\frac{1}{10}\to x", color = RED).scale(0.7).next_to(series, buff = 0.5)
        notice.shift((series[-4].get_y() - notice[1].get_y())*UP)
        self.play(FadeIn(notice, 0.5*LEFT), *[terms[i].animate.restore() for i in range(n)], *[follow(terms_2[i], terms[i], FadeOut) for i in range(n)], 
                  *[values[i].animating(rate_func = rush_into).restore() for i in range(n)], *[FadeOut(values_2[i][::-1], lag_ratio = 0.5) for i in range(n)])
        self.wait()

        texts = [str(fibonaccis[i]) + r"x^" + str(i+1) for i in range(8)] + [r"\cdots"]
        series_Fibonacci = MTex(r"+".join(texts), isolate = [r"+", *texts]).scale(0.8).next_to(1.5*LEFT+1.25*UP, buff = 0)
        terms_Fibonacci = [series_Fibonacci.get_part_by_tex(text) for text in texts]
        adds_Fibonacci = series_Fibonacci.get_parts_by_tex(r"+")
        symbol_Fibonacci = MTex(r"f(x)=", tex_to_color_map = {r"x": RED, r"f": BLUE_D}).scale(0.8).next_to(1.5*LEFT+1.2*UP, LEFT)
        symbol_Fibonacci_1 = MTex(r"xf(x)=", tex_to_color_map = {r"x": RED, r"f": BLUE_D}).scale(0.8).next_to(1.5*LEFT+0.4*UP, LEFT)
        symbol_Fibonacci_2 = MTex(r"x^2f(x)=", tex_to_color_map = {(r"x", r"x^2"): RED, r"f": BLUE_D}).scale(0.8).next_to(1.5*LEFT+0.4*DOWN, LEFT)
        terms_array = []
        terms_power = []
        for i in range(8):
            terms_array.append(terms_Fibonacci[i][0:-2].set_color(BLUE if i else GREY))
            terms_power.append(terms_Fibonacci[i][-2:].set_color(RED))
        terms_array_1 = []
        terms_remain_1 = VGroup()
        terms_array_2 = []
        terms_remain_2 = VGroup(terms_power[1].copy().shift(10*DOWN), adds_Fibonacci[1].copy().shift(10*DOWN)) #这两个物品不会出现在屏幕里，它们的作用是让两个Write动画同步
        ellipsis_1 = terms_Fibonacci[8].copy().shift(0.8*DOWN)
        ellipsis_2 = terms_Fibonacci[8].copy().shift(1.6*DOWN)
        for i in range(7):
            terms_array_1.append(terms_array[i].copy().next_to(terms_array[i+1].get_corner(RIGHT), LEFT, buff = 0).shift(0.8*DOWN))
            terms_remain_1.add(terms_power[i+1].copy().shift(0.8*DOWN), adds_Fibonacci[i+1].copy().shift(0.8*DOWN))
        anims = [TransformFromCopy(terms_array[1], terms_array_1[0])]
        for i in range(6):
            terms_array_2.append(terms_array_1[i].copy().next_to(terms_array_1[i+1].get_corner(RIGHT), LEFT, buff = 0).shift(0.8*DOWN))
            terms_remain_2.add(terms_power[i+2].copy().shift(1.6*DOWN), adds_Fibonacci[i+2].copy().shift(1.6*DOWN))
            anims.append(TransformFromCopy(terms_array[i+2], terms_array_2[i]))
            anims.append(TransformFromCopy(terms_array[i+2], terms_array_1[i+1]))
        anims.append(TransformFromCopy(terms_Fibonacci[8], ellipsis_2))
        anims.append(TransformFromCopy(terms_Fibonacci[8], ellipsis_1))
        
        self.play(Write(VGroup(symbol_Fibonacci, series_Fibonacci)))
        self.wait()
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.wait()
        self.play(Write(terms_remain_1), Write(terms_remain_2))
        self.wait()
        self.play(Write(symbol_Fibonacci_1), Write(symbol_Fibonacci_2))
        self.wait()

        equation_1 = MTex(r"\Rightarrow f(x)=", tex_to_color_map = {r"x": RED, r"f": BLUE_D}).scale(0.8).next_to(1.5*LEFT + 1.2*DOWN, LEFT)
        equation_2 = MTex(r"x^2+xf(x)+x^2f(x)", tex_to_color_map = {(r"x", r"x^2"): RED, r"f": BLUE_D}).scale(0.8).next_to(1.5*LEFT + 1.2*DOWN, buff = 0)
        self.play(IndicateAround(VGroup(terms_array[1], terms_power[1])))
        self.wait()
        self.play(Write(VGroup(equation_1, equation_2)))
        self.wait()

        solution_1 = MTex(r"\Rightarrow f(x)=", tex_to_color_map = {r"x": RED, r"f": BLUE_D}).scale(0.8).next_to(1.5*LEFT + 2.2*DOWN, LEFT)
        solution_2 = MTex(r"\frac{x^2}{1-x-x^2}", tex_to_color_map = {(r"x", r"x^2"): RED, r"\phi": YELLOW}).scale(0.8).next_to(1.5*LEFT + 2.2*DOWN, buff = 0)
        self.play(FadeIn(solution_1, 0.3*RIGHT), FadeIn(solution_2, 0.3*RIGHT))
        self.wait()

        extra = MTex(r"\Rightarrow f(\frac{1}{10})=\frac{1}{89}", tex_to_color_map = {r"\frac{1}{10}": RED, r"f": BLUE_D, "89": GREEN}).scale(0.8).next_to(solution_2, buff = 1.5)
        self.play(Write(extra))
        self.wait()
        
class Video_3(FrameScene):
    def construct(self):
        
        n = 8
        offset = 3*UP + 3*LEFT
        powers = tuple(["{" + str(2**(i+1)) + "}" for i in range(n)])
        tex_0 = MTex(r"\frac{2x}{1-2x}=f(x)="+"+".join([powers[i] + "x^" + str(i+1) for i in range(n)]) + "+\cdots", tex_to_color_map = {r"x": RED, powers: BLUE, "f": BLUE_D}, isolate = "=").scale(0.8)
        tex_0[0].set_color(GREEN), tex_0[3].set_color(GREEN), tex_0[5].set_color(GREEN)
        tex_0.shift(offset - tex_0.get_parts_by_tex("=")[1].get_center())
        self.wait()
        self.play(FadeIn(tex_0, 0.5*UP))
        self.wait()

        h = 1.5*DOWN
        tex_1 = MTex(r"\frac{1}{49}=f\left(\frac{1}{100}\right)=0.0204081632653061\cdots", tex_to_color_map = {r"\frac{1}{100}": RED, r"f": BLUE_D}).scale(0.8)
        tex_1.shift(h + offset - tex_1[13].get_center())
        tex_1[2:4].set_color(GREEN)
        for i in range(5):
            tex_1[16+2*i:18+2*i].set_color(YELLOW if i%2 else GOLD)
        tex_1[26:-3].set_color(GREY)
        self.play(FadeIn(tex_1, 0.5*UP))
        self.wait()

        tex_2 = MTex(r"\frac{1}{499}=f\left(\frac{1}{1000}\right)=0.002004008016032064128256513026052\cdots", tex_to_color_map = {r"\frac{1}{1000}": RED, r"f": BLUE_D}).scale(0.8)
        tex_2.shift(2*h + offset - tex_2[15].get_center())
        tex_2[2:5].set_color(GREEN)
        for i in range(10):
            tex_2[18+3*i:21+3*i].set_color(YELLOW if i%2 else GOLD)
        tex_2[48:-3].set_color(GREY)
        self.play(FadeIn(tex_2, 0.5*UP))
        self.wait()

        tex_3 = MTex(r"\frac{1}{4999}=f\left(\frac{1}{10000}\right)=0.0002000400080016003200640128025605121024204840968193\cdots", tex_to_color_map = {r"\frac{1}{10000}": RED, r"f": BLUE_D}).scale(0.8)
        tex_3.shift(3*h + offset - tex_3[17].get_center())
        tex_3[2:6].set_color(GREEN)
        for i in range(12):
            tex_3[20+4*i:24+4*i].set_color(YELLOW if i%2 else GOLD)
        tex_3[68:-3].set_color(GREY)
        self.play(FadeIn(tex_3, 0.5*UP))
        self.wait()

class Video_4(FrameScene):
    def construct(self):

        n = 8
        offset_0 = 3.2*UP + 0*LEFT
        fibonaccis = [1, 1]
        for _ in range(50):
            fibonaccis.append(fibonaccis[-1] + fibonaccis[-2])
        coefficients = tuple(["{" + str(fibonaccis[i]) + "}" for i in range(n)])
        tex_0 = MTex(r"\frac1{1-x-x^2}=f(x)="+"+".join([coefficients[i] + "x^" + str(i) for i in range(n)]) + "+\cdots", tex_to_color_map = {r"x": RED, coefficients: BLUE, "f": BLUE_D}, isolate = "=").scale(0.8)
        tex_0.shift(offset_0 - tex_0.get_parts_by_tex("=")[0].get_center())
        self.add(tex_0).wait()

        offset_1 = 4.5*LEFT + 2.5*DOWN
        axis_x, axis_y = Arrow(1.5*LEFT, 1.5*RIGHT, stroke_width = 3, buff = 0).shift(offset_1), Arrow(0.5*DOWN, 5*UP, stroke_width = 3, buff = 0).shift(offset_1)
        graph = FunctionGraph(lambda t: 1/(1-t-t**2), [-1.55, 0.61, 0.01]).shift(offset_1)
        self.play(GrowFromPoint(axis_x, offset_1), GrowFromPoint(axis_y, offset_1))
        self.play(ShowCreation(graph))
        self.wait()

        colors = [GREEN, TEAL, BLUE, PURPLE_B, RED, ORANGE] + [GREEN_E, TEAL_E, BLUE_E, PURPLE_E, RED_E, interpolate_color(ORANGE, BLACK, 0.5)]
        texs = r"f(x)=", r"1+", r"{x}+", r"2x^2+", r"3x^3+", r"5x^4+", r"8x^5+", r"\cdots"
        func_1 = MTex(r"f(x)=1+{x}+2x^2+3x^3+5x^4+8x^5+\cdots", isolate = [r"=", *texs], tex_to_color_map = {r"f": BLUE_D, r"x": RED, **{texs[i+1]: colors[i] for i in range(6)}, "+": WHITE})
        func_1.shift(offset_0 + 2.5*DOWN - func_1.get_part_by_tex("=").get_center())
        adds = func_1.get_parts_by_tex(r"+")
        parts = [func_1.get_part_by_tex(tex) for tex in texs]
        parts[-1].save_state().shift((adds[0].get_x() - adds[-1].get_x())*RIGHT)
        def taylors(order):
            def util(t: float):
                sum = 1
                for i in range(order):
                    sum = fibonaccis[order-1-i]+sum*t
                return sum
            return util
        curves = [FunctionGraph(taylors(i), [-1.5, 1.5, 0.01], color = colors[i if i < 6 else i%6+6], stroke_width = 2).shift(offset_1) for i in range(50)]
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

        # sum_up = MTex(r"=\frac{1-x^n}{1-x}", tex_to_color_map = {r"x": YELLOW, r"n": RED})
        # sum_up.shift(func_1[4].get_center() - sum_up[0].get_center() + 1.5*DOWN)
        # self.play(Write(sum_up))
        # self.wait()

        # lim = MTex(r"\lim_{{n}\to\infty}\frac{1-x^{n}}{1-x}=\frac{1}{1-x}(-1<x<1)", tex_to_color_map = {r"x": YELLOW, r"{n}": RED}).shift(2.5*RIGHT + DOWN)
        # line_l, line_r = DashedLine(0.5*DOWN, 3*UP).shift(LEFT + offset), DashedLine(0.5*DOWN, 6.5*UP).shift(RIGHT + offset)
        # self.play(FadeIn(lim), ShowCreation(line_l), ShowCreation(line_r))
        # self.wait()

        for i in range(6, 50):
            self.bring_to_back(curves[i])
            self.wait(0, 2)
        self.wait()

        self.fade_out(excepts = [tex_0], anims = [self.camera.frame.animate.shift(4*RIGHT)], run_time = 2)
        self.camera.frame.shift(4*LEFT), tex_0.shift(4*LEFT)
        self.wait()

        lim = MTex(r"\lim_{{n}\to\infty}\frac{a_{n+1}}{a_{n}}=\phi=\frac{\sqrt5+1}{2}\approx 1.618\cdots", 
                   tex_to_color_map = {r"a": BLUE, (r"{n}", r"{n+1}"): PURPLE_B, r"\phi": YELLOW, (r"\frac{\sqrt5+1}{2}", r"1.618\cdots"): YELLOW_B}).scale(0.8).next_to(1.85*UP + 6*LEFT)
        self.play(Write(lim))
        self.wait()

        root = MTex(r"1-\frac{1}{\phi}-\frac{1}{\phi^2}=0", tex_to_color_map = {r"\phi": YELLOW}).scale(0.6).next_to(2.2*UP + 1.5*RIGHT)
        roots = MTex(r"1-x-x^2=(1-\phi x)(1+x/\phi)", tex_to_color_map = {r"\phi": YELLOW, r"x": RED}).scale(0.6).next_to(1.5*UP + 1.5*RIGHT)
        self.play(FadeIn(root, 0.5*LEFT), FadeIn(roots, 0.5*LEFT))
        self.wait()

        texts = r"f(x)", r"=\frac1{1-x-x^2}", r"=\frac{1}{\sqrt5}\frac{\phi(1+x/\phi)+1/\phi(1-\phi x)}{(1-\phi x)(1+x/\phi)}", r"=\frac{1}{\sqrt5}\left(\frac{\phi}{1-\phi x}+\frac{1/\phi}{1+x/\phi}\right)", r"=\frac{\phi}{\sqrt5}\sum_{n=0}^{\infty}(\phi x)^n+\frac{1}{\sqrt5\phi}\sum_{n=0}^{\infty}\left(-\frac{x}{\phi}\right)^n", r"=\sum_{n=0}^{\infty}\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}x^n"
        solution_2 = MTex(texts[0]+"&"+texts[1]+texts[2]+r"\\&"+texts[3]+texts[4]+r"\\&"+texts[5], isolate = [*texts, r"\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}"], tex_to_color_map = {r"x": RED, r"\phi": YELLOW}).scale(0.8).next_to(6*LEFT + 0.9*DOWN, buff = 0)
        solution_terms = [solution_2.get_part_by_tex(text) for text in texts]
        solution_terms[-1][-2:].shift(0.1*RIGHT)
        solution_terms[2].scale(0.75, about_edge = LEFT), 0.3*LEFT
        solution_terms[4].scale(0.75, about_edge = LEFT), 0.3*RIGHT
        hint = MTex(r"\frac{1}{1-x}=\sum_{n=0}^\infty x^n", tex_to_color_map = {r"x": RED, r"n": PURPLE_B}).scale(0.6).next_to(solution_terms[2], buff = 1.5)
        surr = SurroundingRectangle(hint, color = YELLOW)
        indicate = SurroundingRectangle(solution_2.get_part_by_tex(r"\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}"), color = BLUE)
        self.play(FadeIn(solution_terms[0], 0.3*RIGHT), FadeIn(solution_terms[1], 0.3*RIGHT))
        self.wait()
        self.play(Write(solution_terms[2]))
        self.wait()
        self.play(FadeIn(solution_terms[3], 0.3*LEFT))
        self.wait()
        self.play(Write(hint), ShowCreation(surr))
        self.wait()
        self.play(Write(solution_terms[4]))
        self.wait()
        self.play(FadeIn(solution_terms[5], 0.3*RIGHT))
        self.wait()
        self.play(ShowCreation(indicate))
        self.wait()

class Hide(Transform):
    CONFIG = {
        "remover": True
    }
    def __init__(
        self,
        mobject: VMobject,
        shift: np.ndarray|None = None,
        buff: float = 0.1, 
        **kwargs
    ):
        top = mobject.get_top()[1] + buff
        bottom = mobject.get_bottom()[1] - buff
        if shift is None:
            shift = (top - bottom)*UP

        for mob in mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("mask_fill_1")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_1")
            mob.uniforms["mask_y"] = top
        target = mobject.copy().shift(shift)
        
        super().__init__(mobject, target, **kwargs)

    def finish(self) -> None:
        for mob in self.mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        super().finish()

class Patch_1(FrameScene):
    def construct(self):
        offset = 4*LEFT + 0.6*UP
        v, h = 0.6, 0.4
        v_stack, h_stack = v*UP, h*RIGHT
        index = 4

        prime = Arc(-PI/6, PI/6, radius = 2*v).shift(offset + 2*v*LEFT + 0.5*v_stack - 0.5*h_stack)
        line_0 = Line(0.5*v_stack - 0.5*h_stack, 0.5*v_stack + (index+0.5)*h_stack).shift(offset)
        divisor = MTex(r"9899")
        for i in range(4):
            divisor[i].move_to(offset + (-4.5+i)*h_stack).set_color(GREEN if i%2 else TEAL)
        dividend_0 = MTex("1.0000")
        dividend_0[:2].shift(offset - dividend_0[0].get_center())
        for i in range(4):
            dividend_0[2+i].move_to(offset + (i+1)*h_stack)
        quotient_0 = MTex("0.000")
        quotient_0[:2].shift(offset + v_stack - quotient_0[0].get_center())
        for i in range(3):
            quotient_0[2+i].move_to(offset + v_stack + (i+1)*h_stack).set_color(GREY if i<2 else GOLD)
        self.add(prime, line_0, divisor, dividend_0, quotient_0).wait(1)

        zero = MTex("0")[0]
        length_2 = 5
        n_divisor = 9899
        n_remainder_old = 10000
        n_quotient, n_remainder = n_remainder_old // n_divisor, n_remainder_old % n_divisor
        quotient, difference, remainder = MTex(str(n_quotient)), MTex(str(n_quotient*n_divisor)), MTex(str(n_remainder))
        length_0, length_1, length_2 = length_2, len(difference), len(remainder)
        quotient.set_color(GOLD if (index + 1)%4 < 2 else YELLOW).move_to(offset + v_stack + index*h_stack)
        if n_quotient == 0:
            difference.set_color(GREY).move_to(offset - v_stack + index*h_stack)
        else:
            for i, mob in enumerate(difference):
                mob.move_to(offset - v_stack + (-(length_1-1-i) + index)*h_stack)
        for i, mob in enumerate(remainder):
            mob.move_to(offset - 2*v_stack + (-(length_2-1-i) + index)*h_stack)
        line = Line(-(max(length_0, length_1, length_2)-0.5)*h_stack, 0.5*h_stack).shift(offset + index*h_stack - 1.5*v_stack)
        self.play(*[FadeIn(mob, -h_stack) for mob in [difference, remainder, line]], Write(quotient), rate_func = less_smooth, run_time = 0.5)
        new_zero = zero.copy().move_to(offset + (index+1)*h_stack)
        index += 1
        self.play(Hide(VGroup(dividend_0, difference, line)), remainder.animate.shift(2*v_stack), FadeIn(new_zero, 2*v_stack), 
                  line_0.animate.put_start_and_end_on(0.5*v_stack - 0.5*h_stack, 0.5*v_stack + (index+0.5)*h_stack).shift(offset), 
                  rate_func = less_smooth, run_time = 0.5)

        for _ in range(20):
            n_remainder_old, dividend_0 = n_remainder*10, remainder.add(new_zero)
            n_quotient, n_remainder = n_remainder_old // n_divisor, n_remainder_old % n_divisor
            quotient, difference, remainder = MTex(str(n_quotient)), MTex(str(n_quotient*n_divisor)), MTex(str(n_remainder))
            length_0, length_1, length_2 = length_2, len(difference), len(remainder)
            quotient.set_color(GOLD if (index + 1)%4 < 2 else YELLOW).move_to(offset + v_stack + index*h_stack)
            if n_quotient == 0:
                difference.set_color(GREY).move_to(offset - v_stack + index*h_stack)
            else:
                for i, mob in enumerate(difference):
                    mob.move_to(offset - v_stack + (-(length_1-1-i) + index)*h_stack)
            for i, mob in enumerate(remainder):
                mob.move_to(offset - 2*v_stack + (-(length_2-1-i) + index)*h_stack)
            line = Line(-(max(length_0, length_1, length_2)-0.5)*h_stack, 0.5*h_stack).shift(offset + index*h_stack - 1.5*v_stack)
            self.play(*[FadeIn(mob, -h_stack) for mob in [difference, remainder, line]], Write(quotient), rate_func = less_smooth, run_time = 0.5)
            new_zero = zero.copy().move_to(offset + (index+1)*h_stack)
            index += 1
            self.play(Hide(VGroup(dividend_0, difference, line)), remainder.animate.shift(2*v_stack), FadeIn(new_zero, 2*v_stack), 
                    line_0.animate.put_start_and_end_on(0.5*v_stack - 0.5*h_stack, 0.5*v_stack + (index+0.5)*h_stack).shift(offset), 
                    rate_func = less_smooth, run_time = 0.5)
        self.wait(1)
        

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        