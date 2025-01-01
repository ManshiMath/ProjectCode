from manim import *
import numpy as np

class b1(Scene):
    def construct(self):
        text = Text("高考，决定一生", color=YELLOW).scale(1.5)
        ques = Text("吗？", color=YELLOW).scale(1.5).next_to(text, RIGHT, buff=0.1)
        self.play(Write(text), run_time=0.5)
        self.wait(0.6)
        self.play(FadeIn(ques), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(text), FadeOut(ques), run_time=0.5)


class b2(Scene):
    def construct(self):
        text = Text("从未远去的科举", color=YELLOW).scale(1.5)
        self.play(GrowFromEdge(text, LEFT), run_time=0.5)
        self.wait()
        self.play(FadeOut(text), run_time=0.5)

class b3(Scene):
    def construct(self):
        text = Text("做题家与空心病", color=RED).scale(1.5)
        self.play(GrowFromCenter(text), run_time=0.7)
        self.wait()
        self.play(FadeOut(text), run_time=0.5)

class b4(Scene):
    def construct(self):
        text = Text("点评时间", color=YELLOW, font="heiti").scale(2)
        self.play(Write(text), run_time=1)
        self.wait()
        self.play(FadeOut(text), run_time=0.6)

class diag(Scene):
    def construct(self):
        # Draw a 5*5 table 
        t =  Table(
            [["", "","",""],
            ["", "","",""],
            ["", "","",""],
            ["", "","",""],
            ],
            row_labels=[MathTex("0"), MathTex("1"), MathTex("2"), MathTex("3")],
            col_labels=[MathTex("0"), MathTex("1"), MathTex("2"), MathTex("3")],
            top_left_entry=MathTex("i&j")).scale(0.8).shift(UP)
        
        self.play(Create(t), run_time=1.5)
        self.wait(2)
        
        l1 = t.get_cell((3, 4)).copy().set_fill(GREEN, opacity=0.7)
        l2 = t.get_cell((4, 3)).copy().set_fill(GREEN, opacity=0.7)
        # self.play(FadeIn(t[-1]), FadeIn(t[-2]), run_time=1)
        self.play(
            FadeIn(l1),
            FadeIn(l2),
            run_time=1
        )
        self.wait(2)

        eq = MathTex(r"P_m\approx \frac{2}{16} = \frac{1}{8}", color=ORANGE).next_to(t, DOWN, buff=0.2)
        self.play(Write(eq), run_time=1)
        self.wait(2)
