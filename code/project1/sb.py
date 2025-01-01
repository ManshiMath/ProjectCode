from manim import *
import math

class PlotFunctions(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": BLUE},
        )
        labels = axes.get_axis_labels()

        self.play(Create(axes), Create(labels), run_time=2)
        self.wait(4) # 我们知道有很多函数

        # Define functions
        functions = [
            {"function": lambda x: x, "color": RED, "label": MathTex("y=x")},
            {"function": lambda x: x**2, "color": GREEN, "label": MathTex("y=x^2")},
            {"function": lambda x: math.sin(x), "color": YELLOW, "label": MathTex("y=\\sin(x)")},
        ]

        # Plot functions
        id = 0
        for func in functions:
            graph = axes.plot(func["function"], color=func["color"])
            label = axes.get_graph_label(graph, label=func["label"], x_val=-1.5, direction=UP)
            label.move_to(5 * RIGHT - id * UP)
            self.play(Create(graph), Write(label), run_time=2)
            self.wait(1.5)
            id += 1
