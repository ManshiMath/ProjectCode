from manim import *
import numpy as np
from functools import partial
import math

class Prelude(Scene):
    def construct(self):
        tg = Tex("M", "athematic", "S").scale(2.5)
        tg[0].set_color(BLUE)
        #tg[1].set_color(GREEN)
        tg[2].set_color(MAROON_A)
        self.play(
            DrawBorderThenFill(tg),
            run_time=2
        )

        self.wait(1)
        name = Text("漫士沉思录", color=YELLOW).scale(1.8).shift(DOWN*0.5)
        self.play(
            FadeOut(tg[1]),
            tg[0].animate.shift(RIGHT * 3+UP*2),
            tg[2].animate.shift(LEFT * 3+UP*1.8),
            DrawBorderThenFill(name),
            run_time=2,
            lag_ratio=0.7
        )
        text2 = Text("也能讲物理，想不到吧", color=BLUE).shift(DOWN*2.5)
        self.play(Write(text2))
        self.wait(2)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class BCS(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        k1 = ValueTracker(0.)
        k2 = ValueTracker(0.)
        vib = ValueTracker(0.)

        x1 = ValueTracker(-2.4)
        x2 = ValueTracker(-3.5)

        ions = VGroup()

        vib_dir = np.random.rand(36, 1) *0.1 * DOWN + np.random.rand(36, 1) *0.1 * RIGHT
        def create_dot(i, j):
            f_strength = k1.get_value() / ((i - x1.get_value()) ** 2 + (j + 0.5) ** 2)
            dirc = (x1.get_value() - i) * 1.5 * RIGHT + (-0.5-j) * 1.5 * DOWN
            _disp = vib_dir[i*4+j+18] * np.sin(PI*vib.get_value())
            return Dot(radius=0.15, color=RED_C, fill_opacity=0.7).shift(i * 1.5 * RIGHT + j * 1.5 * DOWN).shift(dirc*f_strength + _disp)
            
        for i in range(-4, 5):
            for j in range(-2, 2):
                ions.add(always_redraw(partial(create_dot, i, j)))

        elec1 = always_redraw(
            lambda: Dot(radius=0.05, color=BLUE_C, fill_opacity=0.7).shift(x1.get_value()*1.5*RIGHT+0.5*1.5*UP)
        )

        self.play(FadeIn(ions), run_time=4, lag_ratio=0.2)
        self.wait(3)

        sq = always_redraw(lambda: VGroup(
            DashedLine(start=ions[5].get_center(), end=ions[6].get_center(), color=GREEN, stroke_width=2),
            DashedLine(start=ions[5].get_center(), end=ions[9].get_center(), color=GREEN, stroke_width=2),
            DashedLine(start=ions[6].get_center(), end=ions[10].get_center(), color=GREEN, stroke_width=2),
            DashedLine(start=ions[9].get_center(), end=ions[10].get_center(), color=GREEN, stroke_width=2)
        ))
        ucell = Text("晶胞 Unit Cell", color=GREEN).scale(1.5).shift(DOWN*3)

        self.play(Create(sq), Write(ucell), run_time=2)
        self.wait(3)
        self.play(FadeOut(ucell))
        self.wait(2)
        
        e1 = Dot(radius=0.05, color=BLUE_C, fill_opacity=0.7).shift(5 * LEFT+2*UP)
        e2 = Dot(radius=0.05, color=BLUE_C, fill_opacity=0.7).shift(4 * LEFT+0.5*UP)
        e3 = Dot(radius=0.05, color=BLUE_C, fill_opacity=0.7).shift(5 * LEFT+0.5*DOWN)
        self.play(Create(VGroup(e1, e2, e3)))
        self.play(
            e1.animate.shift(RIGHT*9),
            e2.animate.shift(RIGHT*8.5),
            e3.animate.shift(RIGHT*10.8),
            run_time = 6,
            rate_func=linear
        )
        self.wait(3)
        self.play(FadeOut(e1, e2, e3))

        self.play(FadeIn(elec1))
        self.wait(4)

        arr1 = Arrow(ions[5].get_center(), elec1.get_center(), stroke_width=4, color=YELLOW)
        arr2 = Arrow(ions[6].get_center(), elec1.get_center(), stroke_width=4, color=YELLOW)
        arr3 = Arrow(ions[9].get_center(), elec1.get_center(), stroke_width=4, color=YELLOW)
        arr4 = Arrow(ions[10].get_center(), elec1.get_center(), stroke_width=4, color=YELLOW)
        arrs = VGroup(arr1, arr2, arr3, arr4)
        self.play(Create(arrs), run_time=2)
        self.wait(3)

        self.play(k1.animate.set_value(0.1), run_time=2, rate_func=rate_functions.ease_out_elastic)
        self.play(FadeOut(arrs), FadeOut(sq))
        self.wait(2)
        self.play(x1.animate.set_value(3.5), run_time=8, rate_func=there_and_back)
        self.wait(2)

        self.play(x1.animate.set_value(-1.1), run_time=3)
        self.wait(2)

        self.play(FocusOn(VGroup(elec1, ions[13], ions[14])),
                   run_time=1.5)
        rect = SurroundingRectangle(VGroup(elec1, ions[13], ions[14]))
        self.play(Create(rect), run_time=2)

        pos_col = MathTex("+", color=RED).scale(0.8).next_to(rect, DOWN, buff=0.1)
        halo = always_redraw(
            lambda:ImageMobject("gradient_orange.png").set_opacity(0.3).move_to(elec1.get_center())
            )

        self.wait(3)
        self.play(Write(pos_col))
        self.wait(2)
        self.play(FadeOut(rect), run_time=2)
        self.wait(2)
        self.play(FadeIn(halo), run_time=2)
        self.wait(3)

        phonon_text = Text("声子 Phonon", color=YELLOW).scale(1.5).shift(DOWN * 3)
        self.play(Write(phonon_text))
        self.wait(2)
        self.play(x1.animate.set_value(3.5), run_time=6, rate_func=there_and_back)
        self.wait(2)
        self.play(FadeOut(phonon_text))
        self.wait(3)

        elec2 = always_redraw(
            lambda: Dot(radius=0.05, color=BLUE_C, fill_opacity=0.7).shift(x2.get_value()*1.5*RIGHT+0.5*1.5*UP)
        )
        neg_col = always_redraw(
            lambda: MathTex("e-", color=BLUE).scale(0.8).next_to(elec2, DOWN, buff=0.1)
        ) 
        self.play(Create(elec2), Write(neg_col), run_time=2)
        self.wait(3)
        self.play(x2.animate.set_value(-1.2), run_time=3)
        self.wait(3)
        self.play(FadeOut(pos_col), FadeOut(neg_col), FadeOut(halo), run_time=2)
        self.wait(2)
        rect = SurroundingRectangle(VGroup(elec1, elec2))
        self.play(Create(rect))

        note = Text("Cooper Pair", color=YELLOW_C).next_to(rect, DOWN, buff=0.6)
        self.play(Write(note), run_time=2)
        self.wait(3)
        self.play(FadeOut(note), FadeOut(rect), run_time=2)
        self.play(k1.animate.set_value(1e-4), run_time=2)
        self.wait(2)
        self.play(x1.animate.set_value(3.3), x2.animate.set_value(3.2), 
                  run_time=6, rate_func=there_and_back)
        no_r = Text("没有阻力", color=YELLOW).shift(DOWN*2.5)
        self.wait()
        self.play(Write(no_r), run_time=2)
        self.wait(3)
        self.play(FadeOut(no_r))

        self.wait(2)
        self.play(FadeOut(elec2))
        self.play(vib.animate.set_value(100), 
                  run_time=10,
                  rate_func=linear,
                  )

        self.play(vib.animate.set_value(160),
                  run_time=8,
                  rate_func=rush_from)
        self.play(FadeIn(elec2), run_time=3)
        self.wait(4)

class Ressist(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        t = ValueTracker(0.)

        Proton = always_redraw(
            lambda: Dot(radius=0.3, color=RED_C, fill_opacity=0.7).shift(np.sin(t.get_value())*(0.1*DOWN + 0.1*RIGHT))
            )
        plus_sign = always_redraw(
            lambda: Text('+', color=YELLOW).move_to(Proton.get_center())
            )

        self.play(Create(Proton))
        self.play(FadeIn(plus_sign))
        self.wait(4)

        el = Dot(radius=0.05, color=BLUE_C, fill_opacity=0.7).shift(UP*1+LEFT*2.5)
        e_sign = always_redraw(
            lambda: MathTex("e^-", color=BLUE).next_to(el)
        )
        self.play(Create(el), Write(e_sign))
        self.play(el.animate.shift(RIGHT*11), run_time=3, rate_func=linear)
        self.play(FadeOut(el), FadeOut(e_sign))
        self.wait(3)

        el = Dot(radius=0.05, color=BLUE_C, fill_opacity=0.7).shift(LEFT*4+UP*0.4)
        self.play(el.animate.shift(RIGHT * 3.65), run_time=1.5, rate_func=linear)
        self.play(t.animate.set_value(30), el.animate.shift(RIGHT * 6 + UP * 6), 
                  run_time=8, rate_func=linear)
        
        halo = ImageMobject("gradient_orange.png").set_opacity(0.3)
        self.play(t.animate.set_value(90), 
                  FadeIn(halo),
                  run_time=16, rate_func=rush_into
                  )
        self.play(t.animate.set_value(170), 
                  run_time=8, rate_func=linear)


class Ohm_vs_Temp(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        axes = NumberPlane(
            x_range=[4.0, 4.6, 0.1],
            y_range=[0, 0.15, 0.03],
            x_length=6,
            y_length=5,
        ).add_coordinates().shift(LEFT*2 + UP)

        def ohm_func(T):
            if T < 4.15:
                return 1e-5
            elif T < 4.22:
                return 0.11 / 0.07 * (T-4.15) + 1e-5
            else:
                return 0.1 * (T-4.15) + 0.11 + 1e-5

        T = ValueTracker(4.5)
        seg1 = always_redraw(
            lambda: axes.plot(
                lambda x: ohm_func(x), x_range=[max(T.get_value(),4.22), 4.5], color=GREEN
            )
        )
        seg2 = always_redraw(
            lambda: axes.plot(
                lambda x: ohm_func(x), x_range=[max(T.get_value(), 4.15), 4.22], color=GREEN
            )
        )
        seg3 = always_redraw(
            lambda: axes.plot(
                lambda x: ohm_func(x), x_range=[T.get_value(), 4.15], color=GREEN
            )
        )


        dot = always_redraw(
            lambda: Dot().move_to(
                axes.c2p(T.get_value(), ohm_func(T.get_value()))
                ).set_color(ORANGE)
        )

        self.play(Create(axes), run_time=3)
        self.wait(4)
        self.play(Create(dot), Create(seg1))
        self.wait(3)
        self.play(T.animate.set_value(4.22), run_time=4, rate_func=slow_into)
        self.wait(2)
        self.play(Create(seg2))
        self.play(T.animate.set_value(4.15), run_time=4, rate_func=smooth)
        self.wait(2)
        self.play(Flash(dot))

        temp=MathTex(r"T_c \approx 4.15 K", color=YELLOW).scale(0.5).next_to(dot, DOWN)
        zero=MathTex(r"R \leq 10^{-5} \Omega", color=YELLOW).scale(0.5).next_to(temp, DOWN)
        self.play(Write(temp))
        self.play(Write(zero))
        self.wait(2)
        self.play(FadeOut(temp), FadeOut(zero), Create(seg3))

        self.play(T.animate.set_value(4.02), run_time=4)
        self.wait(3)