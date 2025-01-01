from manim import *
import numpy as np

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
        self.wait(1)
        t2 = Text("2024新年快乐", font='heiti', color=PURE_RED).next_to(name, DOWN, buff=0.5)
        self.play(
            Write(t2),
            run_time=1
        )
        self.wait(1.5)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )