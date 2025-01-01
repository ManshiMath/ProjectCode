import numpy as np
from manim import *

class Video0(Scene):
    def construct(self):
        # 即得易见平凡，仿照上例显然，留作习题答案略，读者自证不难。
        # 反之亦然同理，推论自然成立，略去过程QED，由上可知证毕。

        sent1 = Text("即得易见平凡", font="kaiti").shift(LEFT*3+UP).set_stroke(width=3, background=True)
        # sent2 = Text("仿照上例显然").set_color(YELLOW).next_to(sent1, DOWN, buff=0.3)
        sent2 = Text("仿照上例显然", font="kaiti").set_stroke(width=3, background=True).next_to(sent1, DOWN, buff=0.3)
        # sent3 = Text("留作习题答案略").set_color(YELLOW).next_to(sent2, DOWN, buff=0.3)
        sent3 = Text("留作习题答案略", font="kaiti").set_stroke(width=3, background=True).next_to(sent2, DOWN, buff=0.3)
        # sent4 = Text("读者自证不难").set_color(YELLOW).next_to(sent3, DOWN, buff=0.3)
        sent4 = Text("读者自证不难", font="kaiti").set_stroke(width=3, background=True).next_to(sent3, DOWN, buff=0.3)
        # sent5 = Text("反之亦然同理").set_color(YELLOW).shift(RIGHT*3+UP*3)
        sent5 = Text("反之亦然同理", font="kaiti").set_stroke(width=3, background=True).shift(RIGHT*3+UP)
        # sent6 = Text("推论自然成立").set_color(YELLOW).next_to(sent5, DOWN, buff=0.3)
        sent6 = Text("推论自然成立", font="kaiti").set_stroke(width=3, background=True).next_to(sent5, DOWN, buff=0.3)
        # sent7 = Text("略去过程QED").set_color(YELLOW).next_to(sent6, DOWN, buff=0.3)
        sent7 = Text("略去过程QED", font="kaiti").set_stroke(width=3, background=True).next_to(sent6, DOWN, buff=0.3)
        # sent8 = Text("由上可知证毕").set_color(YELLOW).next_to(sent7, DOWN, buff=0.3)
        sent8 = Text("由上可知证毕", font="kaiti").set_stroke(width=3, background=True).next_to(sent7, DOWN, buff=0.3)
        all = VGroup(sent1, sent2, sent3, sent4, sent5, sent6, sent7, sent8)

        for i in range(8):
            self.play(Write(all[i]), run_time=2)
            if i == 3:
                self.wait()
        self.wait()

        title = Text("西江月·数学", font="heiti").set_color(YELLOW).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(5)

        notethat = Text("注意到", color=RED).scale(2.5).set_stroke(width=5, background=True)
        self.play(
            *[mobj.animate.set_opacity(0.5) for mobj in all],
            title.animate.set_opacity(0.5),
            Write(notethat),
            run_time=2
        )
        self.wait(3)
        # Fadeout everything
        self.play(
            *[FadeOut(mobj) for mobj in self.mobjects],
            run_time=1
        )
        self.wait(2)

        ques = Text("求证，任何一个有理数都可以写成三个有理数的立方和", font="kaiti", color=GREEN).scale(0.7).set_stroke(width=3, background=True).shift(UP*3)
        note = Text("证明：注意到", font="heiti").set_color(PURE_RED).to_edge(LEFT, buff=0.5).shift(UP*1.5)
        eq = MathTex(r"a=",r"\left(\frac{a-3^2}{3^2}\right)^3","+",r"\left(\frac{-a^3+3^5 a+3^6}{3^2 a^2+3^4 a+3^6}\right)^3","+",r"\left(\frac{3^5 a+3^3 a^2}{3^2 a^2+3^4 a+3^6}\right)^3",
                     color=BLUE).scale(0.8).set_stroke(width=3, background=True)
        qed = Text("证毕!", font="heiti").next_to(eq, DOWN, buff=0.5).set_stroke(width=3, background=True).shift(RIGHT*5)
        self.play(Write(ques), run_time=2)
        self.wait(2)
        self.play(Write(note), run_time=1)
        self.wait(2)
        self.play(Write(eq), run_time=2.5)
        self.wait(2)

        r1 = SurroundingRectangle(eq[1], buff=0.1).set_stroke(width=3)
        r2 = SurroundingRectangle(eq[3], buff=0.1).set_stroke(width=3)
        r3 = SurroundingRectangle(eq[5], buff=0.1).set_stroke(width=3)
        self.play(LaggedStart(Create(r1), Create(r2), Create(r3), lag_ratio=0.5), run_time=3)
        self.wait(2)
        self.play(Write(qed), run_time=1)
        self.wait()
        self.play(FadeOut(r1), FadeOut(r2), FadeOut(r3), run_time=1)
        self.wait(2)

        ques_mrk = MathTex(r"???").scale(3).set_color(YELLOW).set_stroke(width=5, background=True)
        self.play(Write(ques_mrk), run_time=1.5)
        self.wait(3)

class Video2(Scene):
    def construct(self):
        eq = MathTex(r"\pi^3-31",r"=\int_0^1 \frac{x^{12}\left(1091239949453-240010278547 x^2\right) \ln ^2(1 / x)}{83203139250\left(1+x^2\right)} d x").scale(0.8).shift(UP*2)
        self.play(Write(eq[0]), run_time=1)
        self.wait(2)
        self.play(Write(eq[1]), run_time=2)
        self.wait(2)

        geq_0 = MathTex(r"\geq 0").next_to(eq, DOWN, buff=0.4).align_to(eq[1], LEFT).set_color(YELLOW)
        self.play(Write(geq_0), run_time=1)
        self.wait(3)

        ques_mark = MathTex(r"???").scale(3).set_color(RED).set_stroke(width=5, background=True)
        self.play(Write(ques_mark), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(ques_mark), FadeOut(geq_0), run_time=1)

        temp = MathTex(r"\int_0^1 \frac{x^m\left(a+b x^2\right) \ln ^{n-1}(1 / x)}{1+x^2} d x", color=ORANGE).set_stroke(width=3, background=True)
        _eq = eq.copy().set_opacity(0.4).shift(UP)
        self.play(
            Transform(eq, _eq),
            Write(temp),
            run_time=1.5
        )
        self.wait(2)

        nm_val = MathTex(r"m=12,\quad n=3").next_to(temp, UR, buff=0.2).scale(0.8)
        self.play(Write(nm_val), run_time=1)
        self.wait(2)
        plug_eq = MathTex(r"\int_0^1 \frac{x^{12}\left(a+b x^2\right) \ln ^2(1 / x)}{1+x^2} d x=",r"\frac{1}{16}(a-b) " ,
                          "\pi^3+",r"\left(-\frac{80596213364}{41601569625} a+\frac{177153083899958}{91398648466125} b\right)").scale(0.6).move_to(temp).set_stroke(width=3, background=True)
        self.play(TransformMatchingShapes(temp, plug_eq[0]), run_time=1.5)
        self.wait()
        self.play(Write(plug_eq[1:]), run_time=1)
        self.wait(2)

        self.play(eq.animate.set_opacity(1).set_color(YELLOW).set_stroke(width=3, background=True), run_time=1.5)
        self.wait(2)

        rect1 = SurroundingRectangle(plug_eq[1], buff=0.1)
        rect2 = SurroundingRectangle(plug_eq[3], buff=0.1)
        eq_1 = MathTex(r"=1", color=GREEN).next_to(rect1, DOWN, buff=0.2).set_stroke(width=3, background=True)
        eq_m31 = MathTex(r"=-31", color=BLUE).next_to(rect2, DOWN, buff=0.2).set_stroke(width=3, background=True)
        self.play(Create(rect1), Create(rect2), run_time=1)
        self.wait()
        self.play(Write(eq_1), run_time=1)
        self.wait()
        self.play(Write(eq_m31), run_time=1)
        self.wait(2)

        ab_eq = MathTex(r"a=\frac{1091239949453}{83203139250},\ b=-\frac{240010278547}{83203139250}", color=TEAL
                        ).scale(0.6).next_to(plug_eq, UP, buff=0.2).align_to(plug_eq, LEFT).set_stroke(width=3, background=True)
        self.play(Write(ab_eq), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(eq_m31), FadeOut(eq_1), FadeOut(rect1), FadeOut(rect2), run_time=1)
        self.wait(2)

        new_rhs = MathTex(r"\pi^3-31").set_color(YELLOW).next_to(plug_eq[0], RIGHT, buff=0.2).set_stroke(width=3, background=True)
        self.play(ReplacementTransform(plug_eq[1:], new_rhs), run_time=1)
        self.wait(2)
        r1 = SurroundingRectangle(eq[1], buff=0.1).set_stroke(width=3)
        r2 = SurroundingRectangle(plug_eq[0], buff=0.1).set_stroke(width=3)
        self.play(Create(r1), Create(r2), run_time=1.5)
        self.wait(2)

