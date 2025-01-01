from manim import *
import numpy as np

class Video1(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-1, 8, 1],
            y_range=[-1, 5, 1],
             background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            },
            axis_config={
                "color": BLUE,
                "stroke_width": 8,
                "include_numbers": True,
            },
            x_length=9,
            y_length=6,
            tips=True
        )
        x_lbl = Text("参数T", color=BLUE).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1).scale(0.6)
        y_lbl = Text("宏观特性", color=GREEN).next_to(plane.y_axis.get_end(), UP, buff=0.1).scale(0.6)
        # self.play(Create(plane))
        self.play(FadeIn(plane))
        self.play(Write(x_lbl), Write(y_lbl))
        self.wait(2)
        x = ValueTracker(0.)
        def f(x):
            return 4/(1+np.exp(10*(x-4)))
        # plot the function f in range [0, x], with updater for graph
        graph = always_redraw(lambda: plane.plot(lambda x: f(x), x_range=[0, x.get_value()], color=ORANGE, stroke_width=5))
        self.add(graph)
        self.play(x.animate.set_value(3.5), run_time=6)
        self.wait()
        # Critical point and region
        critical_point = DashedLine(plane.coords_to_point(4, 0), plane.coords_to_point(4, 5), color=YELLOW, stroke_width=8)
        lbl = MathTex("T_c", color=YELLOW).next_to(critical_point, UP+RIGHT, buff=0.1)
        self.play(Create(critical_point), Write(lbl))
        self.wait(2)

        self.play(x.animate.set_value(4.5), run_time=4, rate_func=linear)
        self.wait()
        self.play(x.animate.set_value(7), run_time=3)
