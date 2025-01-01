from manim import *
import numpy as np

class Video0(Scene):
    def construct(self):
        equ = MathTex("S=", "1+", r"2+2^2+2^3+\hdots+2^n", color=BLUE).scale(1.2).shift(UP*2)
        equ[0].set_color(RED)

        equ_mul2 = MathTex("2S=", r"2+2^2+2^3+\hdots+2^{n}",r"+2^{n+1}", color=BLUE).scale(1.2).next_to(equ, DOWN, buff=1)
        equ_mul2[0].set_color(RED)

        self.play(Write(equ), run_time=2)
        self.wait(2)

        equ_ = equ.copy().align_to(equ, LEFT).align_to(equ_mul2, UP)
        self.play(TransformFromCopy(equ, equ_), run_time=1.5)
        self.wait()
        self.play(ReplacementTransform(equ_, equ_mul2), run_time=2)
        self.wait()

        _new_pos = equ_mul2[1:].copy().align_to(equ[2], LEFT)
        self.play(equ_mul2[1:].animate.move_to(_new_pos), run_time=1)
        self.wait()

        self.play(ApplyWave(equ[2:]), ApplyWave(equ_mul2[1:-1]), run_time=2)
        rect = SurroundingRectangle(equ_mul2[1:-1], buff=0.1)
        rect2 = SurroundingRectangle(equ[2:], buff=0.1)
        self.play(Create(rect), Create(rect2), run_time=1)
        self.wait(1)

        subtract = MathTex(r"2S-S=", r"2^{n+1}-1", color=BLUE).scale(1.2).shift(DOWN*2)
        subtract[0].set_color(YELLOW)

        self.play(Write(subtract), run_time=2)

        ans = MathTex(r"S=", color=RED).scale(1.2).next_to(subtract, LEFT, buff=0.5)
        self.play(Write(ans), run_time=1.5)
        self.wait(2)


class Video1(Scene):
    def construct(self):
        equ = MathTex("S=", "a+", r"ax+ax^2+ax^3+\hdots+ax^n", tex_to_color_map={"a": YELLOW, "x": BLUE}).scale(1.2).shift(UP*2.5)
        equ[0].set_color(YELLOW)
        equ_mulx = MathTex("xS=", r"ax+ax^2+ax^3+\hdots+ax^{n}",r"+ax^{n+1}", tex_to_color_map={"a": YELLOW, "x": BLUE}).scale(1.2).next_to(equ, DOWN, buff=1)
        equ_mulx[0].set_color(YELLOW)
        equ_ = equ.copy().align_to(equ, LEFT).align_to(equ_mulx, UP)
        self.play(Write(equ), run_time=1)
        self.wait(1)
        self.play(TransformFromCopy(equ, equ_), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(equ_, equ_mulx), run_time=1)
        self.wait(0.5)
        _new_pos = equ_mulx[1:].copy().align_to(equ[2], LEFT)
        self.play(equ_mulx[1:].animate.move_to(_new_pos), run_time=1)
        self.wait(1)

        subtract = MathTex(r"xS-S=", r"ax^{n+1}-a", tex_to_color_map={"a": YELLOW, "x": BLUE}).shift(DOWN*1.5+LEFT*3)
        result = MathTex(r"S=", r"a\cdot\frac{1-x^{n+1}}{1-x}", color=BLUE).scale(1.2).next_to(subtract, RIGHT, buff=2)
        subtract[0].set_color(YELLOW)
        result[0].set_color(RED)
        self.play(Write(subtract), run_time=1.5)
        self.wait(1)
        self.play(GrowFromEdge(result, LEFT), run_time=1.5)
        self.wait()
        rect = SurroundingRectangle(result, buff=0.1)
        self.play(Create(rect), run_time=1)
        self.wait(2)

        title = Text("等比求和", color=YELLOW).to_edge(UP)
        translation = Text("Geometric Series Sum", color=YELLOW).scale(0.8).next_to(title, DOWN, buff=0.4)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN)

        series = MathTex(r"a+ax+ax^2+ax^3+\hdots","+ax^n=",r"a\cdot\frac{1-x^{n+1}}{1-x}", color=BLUE).shift(UP)
        series[-1].set_color(YELLOW)
        # FadeOut Everything and FadeIn title, translation and line
        self.play(
            *[FadeOut(mob) for mob in [equ, equ_mulx, subtract, rect]],
            Write(title),
            Write(translation),
            GrowFromCenter(line),
            ReplacementTransform(result, series),
            run_time=1.5
        )
        # self.play(Write(series), run_time=2)
        self.wait(2.5)

        n_to_inf = MathTex(r"|x|<1,\quad n\rightarrow\infty", color=YELLOW).scale(1.2).shift(DOWN)
        self.play(Write(n_to_inf), run_time=1)
        self.wait(0.5)
        inf_sum = MathTex(r"=\frac{a}{1-x}", color=ORANGE).next_to(series[0], RIGHT, buff=0.5)
        self.play(
            FadeOut(series[1]),
            ReplacementTransform(series[-1], inf_sum),
            run_time=1.5
        )
        self.wait(2)

        self.play(FadeOut(n_to_inf), run_time=1)

        jiuzhe = Text("就这？？", color=ORANGE).scale(2).rotate(PI/6).set_stroke(background=True, width=5)
        self.play(Write(jiuzhe), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(jiuzhe), run_time=1)

        rect = SurroundingRectangle(series[0], buff=0.2)
        self.play(Create(rect), run_time=1)
        self.play(ApplyWave(series[0]), run_time=1.5)
        self.wait(0.5)
        x_not_number = Text("x根本不是数字?", font='heiti', color=YELLOW).scale(1.2).next_to(rect, DOWN, buff=0.8)
        self.play(Write(x_not_number), run_time=1.5)
        self.wait(2)

class Video5(Scene):
    def construct(self):
        taylor = MathTex(r"e^x=", r"1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\hdots", color=BLUE).scale(1.2).shift(UP*2)
        taylor[0].set_color(ORANGE)
        self.play(Write(taylor), run_time=2)
        self.wait(2)
        self.play(FadeOut(taylor), run_time=1)

        def_equ = MathTex(r"e^x=\int e^x\ dx").scale(2)
        self.play(Write(def_equ), run_time=1.5)
        self.wait(2)

        eq2 = MathTex(r"e^x - \int e^x=0").scale(2)
        self.play(ReplacementTransform(def_equ, eq2), run_time=1.5)
        self.wait(3)

        eq3 = MathTex(r"\left(I - \int\right)","e^x=","0").scale(2)
        self.play(ReplacementTransform(eq2, eq3), run_time=1.5)
        self.wait(3)

        eq4 = MathTex("e^x=",r"\left(1 - \int\right)","^{-1}","0").scale(2)
        self.play(Transform(eq3[0], eq4[1]), 
                  Transform(eq3[1], eq4[0]),
                  Transform(eq3[2], eq4[3]),
                  run_time=1)
        self.wait()
        self.play(Write(eq4[2]), run_time=1)
        self.wait(3)

class Video5_2(Scene):
    def construct(self):
        eq4 = MathTex("e^x=",r"\left(1 - \int\right)","^{-1}","0").scale(2)
        _eq4 = eq4.copy().scale(0.6).shift(UP*2.5).set_color(ORANGE)
        self.add(eq4)
        self.play(Transform(eq4, _eq4), run_time=1.5)
        
        geosum = MathTex(r"I+P+P^2+P^3+\hdots=(I-P)^{-1}", color=BLUE).next_to(eq4, DOWN, buff=0.6)
        operate_series = MathTex(r"\left(I - \int\right)^{-1}=I +\int + \int^2 + \int^3 + \hdots", color=YELLOW).next_to(geosum, DOWN, buff=0.6)
        self.play(Write(geosum), run_time=1.5)
        self.wait(1)
        self.play(Write(operate_series), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(geosum), run_time=1)
        new_eq4 = MathTex(r"e^x=", r"0 ", "+", r"\int 0", r"+", r"\int \int 0","+",r" \int \int \int 0 ",r"+ \hdots", color=BLUE).scale(1.2).align_to(eq4, UP)
        new_eq4[0].set_color(ORANGE)
        self.play(ReplacementTransform(eq4, new_eq4),
                  operate_series.animate.shift(DOWN*1.5),
                   run_time=1.5)
        self.wait(3)

        self.play(FadeOut(new_eq4[1:3]))
        self.wait(1)

        compu1 = MathTex(r"\int 0 = C", color=YELLOW).scale(1.2)
        self.play(Write(compu1), run_time=1.5)
        res1 = MathTex("C", color=ORANGE).move_to(new_eq4[3])
        self.wait()
        self.play(
            FadeOut(compu1),
            ReplacementTransform(new_eq4[3], res1), run_time=1.5)
        self.wait(1)

        compu2 = MathTex(r"\int \int 0 =\int C = Cx", color=YELLOW)
        self.play(Write(compu2), run_time=1.5)
        res2 = MathTex("Cx", color=ORANGE).move_to(new_eq4[5])
        self.wait()
        self.play(
            FadeOut(compu2),
            ReplacementTransform(new_eq4[5], res2), 
            run_time=1.5)
        
        self.wait(1)
        compu3 = MathTex(r"\int \int \int 0 =\int Cx = \frac{Cx^2}{2}", color=YELLOW)
        self.play(Write(compu3), run_time=1)
        res3 = MathTex(r"\frac{Cx^2}{2}", color=ORANGE).move_to(new_eq4[7])
        self.play(
            FadeOut(compu3),
            ReplacementTransform(new_eq4[7], res3), 
            run_time=1)
        self.wait(1)

        final_eq = MathTex(r"e^x=", "C","+","Cx","+",r"\frac{Cx^2}{2}","+",r"\frac{Cx^3}{6}",r"+\hdots", color=BLUE).scale(1.2)
        final_eq[0].set_color(ORANGE)
        self.play(
            FadeOut(new_eq4),
            FadeOut(res1),
            FadeOut(res2),
            FadeOut(res3),
            FadeOut(operate_series),
            Write(final_eq), run_time=1.5
        )
        self.wait(2)

        cond = MathTex(r"e^0=1", r"\Rightarrow C=1", color=YELLOW).scale(1.2).to_edge(UP) 
        final_taylor = MathTex(r"e^x=1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\hdots", color=BLUE).scale(1.2).move_to(final_eq)
        self.play(Write(cond), run_time=1.5)
        self.wait(1)
        self.play(ReplacementTransform(final_eq, final_taylor), run_time=1.5)
        self.wait()
        self.play(
            FadeOut(cond), 
            Circumscribe(final_taylor, color=YELLOW),
            run_time=1.5)
        self.wait(3)

class br1(Scene):
    def construct(self):
        text = Text("1.从特殊到一般", color=YELLOW).scale(1.5)
        self.play(Write(text), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(text), run_time=0.5)

class br2(Scene):
    def construct(self):
        text = Text("2.谁说必须是数字了", color=YELLOW).scale(1.5)
        self.play(Write(text), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(text), run_time=0.5)

class br3(Scene):
    def construct(self):
        text = Text("3.倒反天罡，且狂野", color=YELLOW).scale(1.5)
        self.play(Write(text), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(text), run_time=0.5)

class br4(Scene):
    def construct(self):
        text = Text("所以，什么是数学思维？", color=BLUE, font='heiti').scale(1.2)
        self.play(Write(text), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(text), run_time=0.5)

class Video2(Scene):
    def construct(self):
        eq1 = MathTex(r"\ y(1-x)", color=BLUE).scale(1.5).shift(UP*2)
        eq2 = MathTex(r"=y-y\cdot x", color=BLUE).scale(1.5).next_to(eq1, DOWN, buff=0.5)
        eq3 = MathTex(r"=Iy-Py", color=BLUE, tex_to_color_map={"I": YELLOW, "P": ORANGE}).scale(1.5).next_to(eq2, DOWN, buff=0.5)
        eq4 = MathTex(r"=(I-P)y", color=BLUE, tex_to_color_map={"I": YELLOW, "P": ORANGE}).scale(1.5).next_to(eq3, DOWN, buff=0.5)
        self.play(Write(eq1), run_time=1)
        self.wait(1)
        self.play(Write(eq2), run_time=1)
        self.wait(1)
        self.play(Write(eq3), run_time=1)
        self.wait(1)
        self.play(Write(eq4), run_time=1)
        self.wait(3)
