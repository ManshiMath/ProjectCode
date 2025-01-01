import numpy as np
from manim import *

class Main(Scene):
    def construct(self):
        stock = ImageMobject("stock.png").scale(1.2).shift(LEFT*2)
        self.play(FadeIn(stock))
        self.wait()

        man = SVGMobject("man.svg").scale(0.5).shift(RIGHT*3+UP).set_color(BLUE)
        man2 = man.copy().shift(DOWN*2)

        self.play(FadeIn(man), FadeIn(man2))
        self.wait()

        text1 = Text("买！").set_color(RED).next_to(man, RIGHT, buff=0.2)
        text2 = Text("卖！").set_color(GREEN).next_to(man2, RIGHT, buff=0.2)
        self.play(Write(text1), Write(text2))

        self.wait()

        ques_mark = MathTex("?").set_color(YELLOW).scale(4).set_stroke(background=True, width=3).shift(RIGHT*3.3)
        self.play(Write(ques_mark))
        self.wait(2)