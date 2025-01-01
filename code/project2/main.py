from manim import *
import numpy as np
import math

class Moving(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN*2)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        axes = NumberPlane(
            x_range=[-2.5, 3.5, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
        ).add_coordinates()

        whole_line = axes.plot(lambda x: x**2, x_range=[-2, 2], color=GREEN)
        func_label = (
            MathTex(r"f(x)=x^2")
            .set(width=2.5)
            .next_to(axes, UP, buff=0.2)
            .set_color(RED_C)
        )

        self.play(
            LaggedStart(
                DrawBorderThenFill(axes),
                Create(whole_line),
                Write(func_label),
                run_time = 3,
                lag_ratio=0.5
            )
        )

        end_point = axes.c2p(1,1)

        k = ValueTracker(0)

        moving_point = always_redraw(lambda: Dot(axes.c2p(k.get_value(), k.get_value()**2), color=YELLOW))
        static_point = Dot(end_point, color=RED)

        line = always_redraw(lambda: axes.plot(lambda t: (1+k.get_value())*t -k.get_value(), 
                                               color=RED))

        slope = always_redraw(lambda: MathTex('y=',f'{(1+k.get_value()):03f}',f'x{(-k.get_value()):03f}',
                                             color=BLUE).to_edge(UP+LEFT))
        
        self.add(static_point, moving_point)
        self.wait(4) # 这里我们关注一个定点

        cord = MathTex("(1,1)", color=BLUE).scale(0.8).next_to(static_point, DOWN+RIGHT)
        self.play(
            FadeIn(cord),
            Flash(static_point)
        )
        self.wait(2)

        self.play(
            Create(line),
            Write(slope),
            run_time=2
        )

        self.play(
            k.animate.set_value(2),
            run_time=5,
            rate_func=there_and_back
        )

        self.wait(5) # 我们可以在曲线上取另外的动点，然后观察他们的连线

        self.play(
            k.animate.set_value(0.99999),
            run_time=10,
            rate_func=slow_into
        )
        self.play(
            k.animate.set_value(1.),
            Flash(moving_point),
            run_time=1
        )
        self.wait(2)

        rect = SurroundingRectangle(slope[1], color=YELLOW)
        dev_def = MathTex("f'(1)=2", color=GREEN).next_to(rect, DOWN).shift(0.4*LEFT)
        self.play(Create(rect), run_time=0.5)
        self.play(Write(dev_def), run_time=2)
        self.wait(5)

def get_horizontal_line_to_graph(axes, function, x, width, color):
        result = VGroup()
        line = DashedLine(
            start=axes.c2p(0, function.underlying_function(x)),
            end=axes.c2p(x, function.underlying_function(x)),
            stroke_width = width,
            stroke_color = color
        )
        dot = Dot().set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
        result.add(line, dot)
        return result

def get_vline(axes, pt, width, color):
        result = VGroup()
        line = DashedLine(
            start=axes.c2p(pt[0], pt[1]),
            end=axes.c2p(pt[0], 0),
            stroke_width = width,
            stroke_color = color
        )
        inter = Line(
            start=axes.c2p(0, 0),
            end=axes.c2p(pt[0], 0),
            stroke_width = width*1.5,
            stroke_color = color
        )
        result.add(line, inter)
        return result

def get_hline(axes, pt, width, color):
        result = VGroup()
        line = DashedLine(
            start=axes.c2p(pt[0], pt[1]),
            end=axes.c2p(0, pt[1]),
            stroke_width = width,
            stroke_color = color
        )
        inter = Line(
            start=axes.c2p(0, 0),
            end=axes.c2p(0, pt[1]),
            stroke_width = width * 1.5,
            stroke_color = color
        )

        result.add(line, inter)
        return result


class Derivative(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        intro = Text("导函数就是求函数在某一点的切线斜率")
        self.play(
            DrawBorderThenFill(intro),
            run_time = 1
        )
        self.wait(5)
        self.play(FadeOut(intro))

        k = ValueTracker(-2)

        plane1 = (
            NumberPlane(x_range=[-3, 3, 1], x_length=6, y_range=[-1, 5], y_length=6)
            .add_coordinates()
            .shift(LEFT*3)
        )

        func1 = plane1.plot(
            lambda x: x ** 2, x_range=[-2.1, 2.1]
        )

        func1_label = (
            MathTex(r"f(x)=x^2")
            .set(width=2.5)
            .next_to(plane1, UP, buff=0.2)
            .set_color(RED_C)
        )
        
        moving_slope = always_redraw(
            lambda: plane1.get_secant_slope_group(
                x=k.get_value(),
                graph=func1,
                dx=0.05,
                secant_line_length=4,
                secant_line_color=YELLOW
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        plane2 = (
            NumberPlane(x_range=[-3, 3, 1], x_length=6, y_range=[-5, 5], y_length=6)
            .add_coordinates()
            .shift(RIGHT*3.5)
        )

        func2 = always_redraw(
            lambda: plane2.plot(
                lambda x: 2*x, x_range=[-2, k.get_value()], color=GREEN
            )
        )

        func2_label = (
            MathTex(r"f'(x)=2x")
            .set(width=2.5)
            .next_to(plane2, UP, buff=0.2)
            .set_color(GREEN)
        )
        
        moving_hline = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=plane2, function=func2, x=k.get_value(), width=4, color=YELLOW
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        slope_value_text = (
             Text("斜率: ")
             .next_to(plane1, DOWN, buff=0.1)
             .shift(0.3*LEFT)
             .set_color(YELLOW)
             .add_background_rectangle()
        )

        slope_value = always_redraw(
             lambda: DecimalNumber(num_decimal_places=2)
             .set_value(func2.underlying_function(k.get_value()))
             .next_to(slope_value_text, RIGHT, buff=0.1)
             .set_color(YELLOW)
        ).add_background_rectangle()

        self.play(
             LaggedStart(
                DrawBorderThenFill(plane1),
                DrawBorderThenFill(plane2),
                Create(func1),
                Write(func1_label),
                Write(func2_label),
                run_time=5,
                lag_ratio=0.5
             )
        )
        self.add(moving_slope, moving_hline, func2, dot)
        self.play(FadeIn(slope_value_text), FadeIn(slope_value))
        self.play(k.animate.set_value(2), run_time=15, rate_function=linear)
        self.wait(5)

class EulerCircle(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        k = ValueTracker(0.0)

        plane = (
            NumberPlane(x_range=[-1.5, 1.5, 0.5], x_length=6, y_range=[-1.5, 1.5, 0.5], y_length=6)
            .add_coordinates()
        )

        axis_labels = plane.get_axis_labels(
            MathTex("r").scale(1.2), MathTex("i").scale(1.2)
        )

        e_i_the = always_redraw(
            lambda: Line(
                start = plane.c2p(0, 0),
                end = plane.c2p(np.cos(k.get_value()), np.sin(k.get_value())),
                buff = 0,
                stroke_width=4,
                stroke_color=WHITE
            )
        )

        pt = always_redraw(
            lambda: Dot().move_to(
                plane.c2p(np.cos(k.get_value()), np.sin(k.get_value())))
                .set_color(RED)
            )
        
        curve = always_redraw(
            lambda: ParametricFunction(
                lambda t: plane.c2p(np.cos(t), np.sin(t)),
                t_range = [0, k.get_value()],
                color = RED
            )
        )

        cord = always_redraw(
            lambda: MathTex(r"e^{i\theta}")
            .scale(0.9)
            .set_color(YELLOW)
            .next_to(pt, 1.3*UP + RIGHT)
        )

        theta_equal = MathTex(r"\theta=", color=RED).scale(0.8).to_edge(UP+LEFT)
        theta = always_redraw(
            lambda: DecimalNumber(k.get_value(), 2)
            .scale(0.8)
            .next_to(theta_equal, RIGHT)
        )

        moving_hline = always_redraw(
            lambda: get_hline(
                axes=plane, pt=(np.cos(k.get_value()), np.sin(k.get_value())), 
                width=4, color=BLUE
            )
        )

        moving_vline = always_redraw(
            lambda: get_vline(
                axes=plane, pt=(np.cos(k.get_value()), np.sin(k.get_value())), 
                width=4, color=GREEN
            )
        )

        y_bar = always_redraw(
            lambda: Line(
                start = ORIGIN,
                end = ORIGIN + plane.c2p(np.sin(k.get_value()), 0) - plane.c2p(0, 0),
                stroke_width = 4,
                stroke_color = BLUE,
            ).shift(DOWN * 2.6 + LEFT * 5.5)
        )

        x_bar = always_redraw(
            lambda: Line(
                start = ORIGIN,
                end = ORIGIN + plane.c2p(np.cos(k.get_value()), 0) - plane.c2p(0, 0),
                stroke_width = 4,
                stroke_color = GREEN,
            ).shift(DOWN * 1.6 + LEFT * 5.5)
        )


        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                DrawBorderThenFill(e_i_the),
                Create(pt),
                Write(cord), 
                Write(axis_labels),
                run_time = 3,
                lag_ratio = 0.5
            )
        )   
        
        self.play(
            FadeIn(moving_hline),
            FadeIn(moving_vline),
            run_time=2
        )

        self.play(
            Write(theta_equal), Write(theta),
            run_time=1.5
        )

        cos_text = MathTex("\\cos(\\theta)=", color=YELLOW).scale(0.6).shift(DOWN * 1.1 + LEFT * 5.5)

        sin_text = MathTex("\\sin(\\theta)=", color=YELLOW).scale(0.6).shift(DOWN * 2.1 + LEFT * 5.5)

        cos_theta = always_redraw(
             lambda: DecimalNumber(np.cos(k.get_value()), 3)
             .scale(0.6)
             .set_color(GREEN)
             .next_to(cos_text, RIGHT)
        )

        sin_theta = always_redraw(
             lambda: DecimalNumber(np.sin(k.get_value()), 3)
             .scale(0.6)
             .set_color(BLUE)
             .next_to(sin_text, RIGHT)
        )

        self.play(
            TransformFromCopy(moving_vline[1], x_bar),
            TransformFromCopy(moving_hline[1], y_bar),
            run_time = 2
        )

        self.play(
            Write(cos_text),
            Write(cos_theta),
            Write(sin_text),
            Write(sin_theta),
            run_time = 2
        )

        self.play(
            k.animate.set_value(np.pi*0.6),
            run_time = 5,
            rate_func = smooth
        )

        self.play(
            k.animate.set_value(0),
            run_time = 3,
            rate_func = smooth
        )

        self.add(curve)
        self.wait(3)

        self.play(
            k.animate.set_value(np.pi*2),
            run_time = 8,
            rate_func = smooth
        )

        self.wait(2)

        self.play(Flash(
            curve, line_length=1,
            num_lines=30, color=RED,
            flash_radius = 2 + SMALL_BUFF,
            time_width=0.3, run_time=2,
            rate_func = rush_from
        ))

        self.wait(5)

        trig_equa = MathTex(r"\cos(\theta)^2" , "+", r"\sin(\theta)^2", "=1").scale(0.8).shift(RIGHT*5 + DOWN*1.5)
        circ_equa = MathTex(r"x^2" , "+", r"y^2", "=1").scale(0.8).shift(RIGHT*5 + DOWN*1.5)
        self.play(DrawBorderThenFill(trig_equa), run_time=2)
        
        self.wait(3)

        self.play(
            ReplacementTransform(trig_equa, circ_equa),
            run_time=2
        )

        self.wait(4)

        self.play(
            FadeOut(circ_equa), FadeOut(curve), 
            FadeOut(moving_hline), FadeOut(moving_vline)
            )
        self.wait(2)
        self.play(k.animate.set_value(2.4*np.pi), run_time=4)
        self.wait(1)
        
        e_i_mthe = always_redraw(
            lambda: Line(
                start = plane.c2p(0, 0),
                end = plane.c2p(np.cos(k.get_value()), -np.sin(k.get_value())),
                buff = 0,
                stroke_width=4,
                stroke_color=WHITE
            )
        )

        pt_conj = always_redraw(
            lambda: Dot().move_to(
                plane.c2p(np.cos(k.get_value()), -np.sin(k.get_value())))
                .set_color(BLUE)
            )
        
        conj_cord = always_redraw(
            lambda: MathTex(r"e^{-i\theta}")
            .scale(0.9)
            .set_color(YELLOW)
            .next_to(pt_conj, 1.3*DOWN + RIGHT)
        )

        pt_sum = always_redraw(
            lambda: Dot().move_to(
                plane.c2p(2*np.cos(k.get_value()), 0))
                .set_color(GREEN_C)
            )

        x_length = always_redraw(
            lambda: Line(
                start = plane.c2p(0, np.sin(k.get_value())),
                end = plane.c2p(np.cos(k.get_value()), np.sin(k.get_value())),
                stroke_width=6,
                stroke_color=GREEN_C
            )
        )

        y_length = always_redraw(
            lambda: Line(
                start = plane.c2p(0, np.sin(k.get_value())),
                end = plane.c2p(0, 0),
                stroke_width=6,
                stroke_color=BLUE_C
            )
        )

        self.play(Create(x_length), Create(y_length),run_time=3)
        self.wait(2)

        cos_vec = always_redraw(
            lambda: Arrow(
                start = plane.c2p(0, 0),
                end = plane.c2p(2*np.cos(k.get_value()), 0),
                buff=0,
                stroke_width= 4,
                color = GREEN_C,
            )
        )
        dline_1 = always_redraw(
            lambda: DashedLine(
                start = plane.c2p(np.cos(k.get_value()), np.sin(k.get_value())),
                end = plane.c2p(2*np.cos(k.get_value()), 0),
                stroke_width=3,
                color=YELLOW_C
            )
        )

        dline_2 = always_redraw(
            lambda: DashedLine(
                start = plane.c2p(np.cos(k.get_value()), -np.sin(k.get_value())),
                end = plane.c2p(2*np.cos(k.get_value()), 0),
                stroke_width=3,
                color=YELLOW_C
            )
        )

        sin_vec = always_redraw(
            lambda: Arrow(
                start = plane.c2p(np.cos(k.get_value()), -np.sin(k.get_value())),
                end = plane.c2p(np.cos(k.get_value()), np.sin(k.get_value())),
                stroke_width = 4,
                buff=0,
                color = BLUE_C,
            )
        )

        self.play(
            Create(VGroup(pt_conj, conj_cord, e_i_mthe)),
            run_time=3
        )

        self.wait(3)

        self.play(
            Create(dline_1), Create(dline_2),
            run_time = 1
        )
        self.play(Create(cos_vec), Create(pt_sum), run_time=2)

        cos_explain = MathTex(r"e^{i\theta}+e^{-i\theta}", color=RED).scale(0.7).next_to(cos_vec, RIGHT+0.5*UP)
        self.play(Write(cos_explain), run_time=1)
        self.wait(2)
        self.play(FadeOut(cos_explain), run_time=1)

        self.wait(5)
        self.play(
            Create(sin_vec),
            run_time=1
        )
        self.wait(3)
        sin_explain = MathTex(r"e^{i\theta}-e^{-i\theta}", color=RED).scale(0.7).shift(1.5*RIGHT+0.4*UP)
        self.play(Write(sin_explain), run_time=1)
        self.wait(2)
        self.play(FadeOut(sin_explain), run_time=1)
        self.wait(3)

        self.play(
            k.animate.set_value(2.8*np.pi),
            rate_func=there_and_back,
            run_time=6
        )

        self.wait(3)

        self.play(
            Indicate(x_length),
            Indicate(cos_vec),
            Indicate(x_bar),
            run_time=2.5
        )
        self.wait(5)

        cos_equation = (
            MathTex(r"e^{i\theta} + e^{-i\theta}=2\cos \theta", color=BLUE_C)
            .scale(0.7)
            .shift(5*RIGHT + 2 * UP)
            )

        self.play(
            DrawBorderThenFill(cos_equation),
            run_time = 2
        )

        self.wait(5)

        self.play(
            Indicate(y_length),
            Indicate(sin_vec),
            Indicate(y_bar),
            run_time=2.5
        )
        self.wait(4)
        
        sin_equation = (
            MathTex(r"e^{i\theta} - e^{-i\theta}=2\sin \theta", "\cdot i", color=GREEN_C)
            .scale(0.7)
            .shift(5*RIGHT+ 2*DOWN)
            )

        self.play(
            DrawBorderThenFill(sin_equation[0]),
            run_time = 2
        )
        self.wait(4)
        self.play(
            Write(sin_equation[1]),
            run_time = 1
        )
        self.wait(3)

        tsfm_cos_equation = (
            MathTex(r"\frac{e^{i\theta} + e^{-i\theta}}{2}=\cos \theta", color=BLUE_C)
            .scale(0.7)
            .shift(5*RIGHT + 2 * UP)
            )
        tsfm_sin_equation = (
            MathTex(r"\frac{e^{i\theta} - e^{-i\theta}}{2i}=\sin \theta", color=GREEN_C)
            .scale(0.7)
            .shift(5*RIGHT + 2 * DOWN)
            )
        self.play(
            ReplacementTransform(cos_equation, tsfm_cos_equation),
            ReplacementTransform(sin_equation, tsfm_sin_equation),
            run_time=3
        )
        self.wait(8)


class SinDer(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        k = ValueTracker(-3)

        plane1 = (
            NumberPlane(x_range=[-4, 4, 1], x_length=6, y_range=[-2, 2], y_length=4)
            .add_coordinates()
            .shift(LEFT*3)
        )

        func1 = plane1.plot(
            lambda x: np.sin(x), x_range=[-4, 4]
        )

        func1_label = (
            MathTex(r"f(x)=\sin(x)")
            .set(width=2.5)
            .next_to(plane1, UP, buff=0.2)
            .set_color(RED_C)
        )
        
        moving_slope = always_redraw(
            lambda: plane1.get_secant_slope_group(
                x=k.get_value(),
                graph=func1,
                dx=0.05,
                secant_line_length=4,
                secant_line_color=YELLOW
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        plane2 = (
            NumberPlane(x_range=[-4, 4, 1], x_length=6, y_range=[-2, 2], y_length=4)
            .add_coordinates()
            .shift(RIGHT*3.5)
        )

        func2 = always_redraw(
            lambda: plane2.plot(
                lambda x: np.cos(x), x_range=[-3, k.get_value()], color=GREEN
            )
        )

        func2_label = (
            MathTex(r"f'(x)=\cos(x)")
            .set(width=2.5)
            .next_to(plane2, UP, buff=0.2)
            .set_color(GREEN)
        )
        
        moving_hline = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=plane2, function=func2, x=k.get_value(), width=4, color=YELLOW
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        slope_value_text = (
             Text("斜率: ")
             .next_to(plane1, DOWN, buff=0.1)
             .shift(0.3*LEFT)
             .set_color(YELLOW)
             .add_background_rectangle()
        )

        slope_value = always_redraw(
             lambda: DecimalNumber(num_decimal_places=2)
             .set_value(func2.underlying_function(k.get_value()))
             .next_to(slope_value_text, RIGHT, buff=0.1)
             .set_color(YELLOW)
        ).add_background_rectangle()

        self.play(
             LaggedStart(
                DrawBorderThenFill(plane1),
                DrawBorderThenFill(plane2),
                Create(func1),
                Write(func1_label),
                Write(func2_label),
                run_time=3,
                lag_ratio=0.5
             )
        )
        self.add(moving_slope, moving_hline, func2, dot)
        self.play(FadeIn(slope_value_text), FadeIn(slope_value))
        self.play(k.animate.set_value(3.6), run_time=8, rate_function=linear)
        self.wait(5)

class CosDer(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        k = ValueTracker(-3)

        plane1 = (
            NumberPlane(x_range=[-4, 4, 1], x_length=6, y_range=[-2, 2], y_length=4)
            .add_coordinates()
            .shift(LEFT*3)
        )

        func1 = plane1.plot(
            lambda x: np.cos(x), x_range=[-4, 4]
        )

        func1_label = (
            MathTex(r"f(x)=\cos(x)")
            .set(width=2.5)
            .next_to(plane1, UP, buff=0.2)
            .set_color(RED_C)
        )
        
        moving_slope = always_redraw(
            lambda: plane1.get_secant_slope_group(
                x=k.get_value(),
                graph=func1,
                dx=0.05,
                secant_line_length=4,
                secant_line_color=YELLOW
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        plane2 = (
            NumberPlane(x_range=[-4, 4, 1], x_length=6, y_range=[-2, 2], y_length=4)
            .add_coordinates()
            .shift(RIGHT*3.5)
        )

        func2 = always_redraw(
            lambda: plane2.plot(
                lambda x: -np.sin(x), x_range=[-3, k.get_value()], color=GREEN
            )
        )

        func2_label = (
            MathTex(r"f'(x)=-\sin(x)")
            .set(width=2.5)
            .next_to(plane2, UP, buff=0.2)
            .set_color(GREEN)
        )
        
        moving_hline = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=plane2, function=func2, x=k.get_value(), width=4, color=YELLOW
            )
        )

        dot = always_redraw(
            lambda: Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        slope_value_text = (
             Text("斜率: ")
             .next_to(plane1, DOWN, buff=0.1)
             .shift(0.3*LEFT)
             .set_color(YELLOW)
             .add_background_rectangle()
        )

        slope_value = always_redraw(
             lambda: DecimalNumber(num_decimal_places=2)
             .set_value(func2.underlying_function(k.get_value()))
             .next_to(slope_value_text, RIGHT, buff=0.1)
             .set_color(YELLOW)
        ).add_background_rectangle()

        self.play(
             LaggedStart(
                DrawBorderThenFill(plane1),
                DrawBorderThenFill(plane2),
                Create(func1),
                Write(func1_label),
                Write(func2_label),
                run_time=3,
                lag_ratio=0.5
             )
        )
        self.add(moving_slope, moving_hline, func2, dot)
        self.play(FadeIn(slope_value_text), FadeIn(slope_value))
        self.play(k.animate.set_value(3.6), run_time=8, rate_function=linear)
        self.wait(5)

class CalcDer(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        x = ValueTracker(1)
        dx = ValueTracker(1.3)

        axes = NumberPlane(
            x_range=[-2.5, 3.5, 1],
            y_range=[-1, 7, 1],
            x_length=5,
            y_length=5,
        ).shift(LEFT * 2.5).add_coordinates()

        func = axes.plot(lambda x: x**2, x_range=[-2, 2.5], color=GREEN)       

        func_label = (
            MathTex(r"f(x)=x^2")
            .set(width=2.5)
            .next_to(axes, UP, buff=0.2)
            .set_color(RED_C)
        )

        self.play(
            LaggedStart(
                DrawBorderThenFill(axes),
                Create(func),
                Write(func_label),
                run_time = 3,
                lag_ratio=0.5
            )
        )

        end_point = axes.c2p(1,1)
        moving_point = always_redraw(lambda: Dot(axes.c2p(x.get_value()+ dx.get_value(),
                                                           (x.get_value()+dx.get_value())**2), 
                                                           color=YELLOW))
        static_point = Dot(end_point, color=RED)
        
        secant = always_redraw(
            lambda: axes.get_secant_slope_group(
                x = x.get_value(),
                graph = func,
                dx = dx.get_value(),
                dx_line_color=YELLOW,
                dy_line_color=ORANGE,
                dx_label = 'h',
                dy_label = '\\Delta y',
                secant_line_color = GREEN,
                secant_line_length = 5
            )
        )


        self.play(
            Create(VGroup(moving_point, static_point, secant)),
            run_time = 5
        )
        self.wait(3)

        x_text = MathTex("x=", color=GREEN).scale(0.8).shift(RIGHT*2 + UP*2)
        x_value = always_redraw(
            lambda: DecimalNumber(x.get_value(), 3)
            .scale(0.8)
            .next_to(x_text, RIGHT)
        )

        h_text = MathTex("h=", color=YELLOW).scale(0.8).next_to(x_value, buff=0.4)
        h_value = always_redraw(
            lambda: DecimalNumber(dx.get_value(), 3)
            .scale(0.8)
            .next_to(h_text, RIGHT)
        )


        dy_text = MathTex(r"\Delta y=(x+h)^2-x^2").next_to(h_text, 2*DOWN)
        dy_text2 = MathTex(r"\Delta y=x^2+2xh+h^2-x^2").next_to(h_text, 2*DOWN)
        dy_text3 = MathTex(r"\Delta y=2xh+h^2").next_to(h_text, 2*DOWN)
        calc_equ = MathTex(r"\frac{\Delta y}{h}=").shift(RIGHT * 2.5)

        for eq in [dy_text, dy_text2, dy_text3, calc_equ]:
             eq.align_to(x_text, LEFT)

        calc_equ2 = MathTex(r"\frac{2xh+h^2}{h}", color=BLUE).next_to(calc_equ, RIGHT)
        calc_equ3 = MathTex(r"2x","+h", color=BLUE).next_to(calc_equ, RIGHT)

        dk = always_redraw(
            lambda: DecimalNumber(dx.get_value()+2*x.get_value(), 3)
            .set_color(BLUE)
            .shift(2.5 * RIGHT + 2.5 * DOWN)
        )
        
        self.play(
            Write(x_text),
            Write(x_value),
            run_time = 1
        )
        self.wait(2)
        self.play(
            Write(h_text),
            Write(h_value),
            run_time = 2
        )
        
        self.wait(5)

        self.play(
            Write(dy_text),
            run_time = 2
        )
        self.wait(2)
        self.play(
            Transform(dy_text, dy_text2),
            run_time = 2
        )
        self.wait(2)
        self.play(
            Transform(dy_text, dy_text3),
            run_time = 2
        )
        self.wait(2)

        self.play(
            Write(calc_equ),
            run_time = 3
        )
        self.wait(4)
        self.play(
            Write(calc_equ2),
            run_time = 2,
        )
        self.wait(3)
        self.play(
            ReplacementTransform(calc_equ2, calc_equ3),
            run_time = 2,
        )
        self.wait(2)

        self.play(Write(dk), run_time=1)
        self.wait(3)
        self.play(
            dx.animate.set_value(-1.0),
            run_time=5,
            rate_func = there_and_back
        )
        self.wait(2)

        self.play(
            dx.animate.set_value(0.),
            run_time=10,
            rate_func = smooth
        )

        self.wait(3)

        rect = SurroundingRectangle(calc_equ3[1], color=YELLOW)
        lim_sign = MathTex(r"\lim_{h\to 0}", color=RED).next_to(calc_equ, LEFT)
        eq_0 = MathTex(r"= 0").next_to(calc_equ3, RIGHT, buff=0.2)

        self.play(Create(rect), 
                  Write(eq_0),
                  run_time = 1)

        self.wait(2)
        self.play(
            FadeOut(rect),
            FadeOut(eq_0)
        )

        self.play(
            FadeOut(calc_equ3[1], scale=0.5),
            Create(lim_sign),
            run_time = 1
            )
        
        self.wait(3)
        self.play(
            x.animate.set_value(-1),
            rate_func = there_and_back,
            run_time = 8
        )

        self.wait(5)

class CalcPolyDer(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        eq0 = MathTex(r"\lim_{h\to 0} \frac{(x+h)^n-x^n}{h}=","?").shift(UP * 2)
        eq1 = MathTex(r"(x+h)^n=\sum_{i=0}^n",r"\frac{n!}{i!(n-i)!}\cdot x^{n-i} h^{i}", color=BLUE).scale(0.8)
        eq_sum = MathTex(r"\frac{n!}{n!0!}x^n h^0", r"+\frac{n!}{1!(n-1)!} x^{n-1} h^1",
                         r"+\frac{n!}{2!(n-2)!} x^{n-2} h^2" , r"+\cdots", color=GREEN).scale(0.8).next_to(eq1, DOWN, buff=0.5)
        
        self.play(Write(eq0), run_time=3)
        self.wait(8)
        self.play(DrawBorderThenFill(eq1), run_time=4)
        self.wait(2)
        
        cnt = ValueTracker(0)
        index_text = MathTex("i=", color=YELLOW).scale(0.8).to_edge(LEFT)
        index = always_redraw(
             lambda: DecimalNumber(cnt.get_value(), 0).scale(0.8).next_to(index_text)
        )
        self.play(
            Write(index_text),
        )
        self.wait(4)
        for i in range(4):
            if i == 0:
                self.play(Write(index))
            else:
                self.play(
                    cnt.animate.set_value(i),     
                    run_time=0.5
                )
            self.wait(1)
            self.play(
                TransformFromCopy(eq1[1], eq_sum[i]),
                run_time = 2
            )
            self.wait(5 if i == 0 else 1)
    
        self.wait(6)
        
        fact_text = MathTex(r"5!=1\times 2 \times 3\times 4\times 5=120", color=RED).scale(0.8).to_edge(UP+LEFT)
        zero_fact = MathTex(r"0!=1", color=RED).scale(0.8).next_to(fact_text, DOWN).align_to(fact_text, LEFT)
        self.play(Write(fact_text), run_time=4)
        self.wait()
        self.play(Write(zero_fact), run_time=3)
        self.wait(2)

        self.play(
            FadeOut(eq1),
            FadeOut(index_text), FadeOut(index),
            eq_sum.animate.shift(UP * 1.5),
            run_time=1.5
        )
        self.wait(3)

        eq_numeric = MathTex(r"x^n", r"+n x^{n-1} h",
                         r"+\frac{n(n-1)}{2} x^{n-2} h^2" , r"+\cdots", color=GREEN).scale(0.8).move_to(eq_sum.get_center()+LEFT)

        for i in range(4):
            self.play(
                ReplacementTransform(eq_sum[i], eq_numeric[i]),
                run_time=1
            )
            self.wait(1)
        self.play(FadeOut(fact_text), FadeOut(zero_fact))
        self.wait(3)
        self.play(FadeOut(eq_numeric[0]))
        self.wait(3)
        self.play(
            eq0.animate.shift(LEFT*3),
            )
        frac_cal = MathTex(r"\lim_{h\to 0} \frac{nx^{n-1} h + n(n-1)/2 x^{n-2} h^2+\cdots}{h}", color=BLUE).scale(0.8).next_to(eq0, RIGHT)
        self.play(ReplacementTransform(eq0[1], frac_cal), run_time=3)
        self.wait(2)
        frac_cal2 = MathTex(r"\lim_{h\to 0}","nx^{n-1}",r" + n(n-1)/2 x^{n-2} h + h(\cdots)", color=BLUE).scale(0.8).next_to(eq0[0], RIGHT)
        self.play(
            ReplacementTransform(frac_cal, frac_cal2),
            FadeOut(eq_numeric[1:]),
            run_time=2
        )
        self.wait(3)

        rect2 = SurroundingRectangle(frac_cal2[2:], color=YELLOW)
        note = Text("跟h有关", color=RED).next_to(rect2, DOWN)

        self.play(
            Create(rect2),
            Write(note),
            run_time=2
        )
        self.wait(5)

        self.play(
            FadeOut(rect2), 
            FadeOut(note), 
            FadeOut(frac_cal2[2]), 
            run_time=3)
        
        self.wait(4)
        self.play(FadeOut(frac_cal2[0]))
        self.wait(3)

        derivative_formula = MathTex(r"\frac{d}{dx} (x^n) = n\cdot x^{n-1}", color=BLUE).shift(DOWN)
        self.play(Write(derivative_formula), run_time=3)
        self.wait(3)

class TasteDer(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        axes = NumberPlane(
            x_range=[-2.5, 3.5, 1],
            y_range=[-1, 5, 1],
            x_length=4,
            y_length=4,
        ).add_coordinates().shift(LEFT*3.5)

        whole_line = axes.plot(lambda x: x**2, x_range=[-2.5, 2.5], color=GREEN)
        func_label = (
            MathTex(r"f(x)=x^2")
            .set(width=2.5)
            .next_to(axes, UP, buff=0.2)
            .set_color(RED_C)
        )

        self.play(
            LaggedStart(
                DrawBorderThenFill(axes),
                Create(whole_line),
                Write(func_label),
                run_time = 1,
                lag_ratio=0.5
            )
        )

        end_point = axes.c2p(1,1)

        k = ValueTracker(1.8)

        moving_point = always_redraw(lambda: Dot(axes.c2p(k.get_value(), k.get_value()**2), color=YELLOW))
        static_point = Dot(end_point, color=RED)

        line = always_redraw(lambda: axes.plot(lambda t: (1+k.get_value())*t -k.get_value(), x_range=[0.6,2.2],
                                               color=RED))
       
        self.add(static_point, moving_point)
        self.wait(1) # 这里我们关注一个定点

        self.play(
            Create(line),
            run_time=1
        )
        self.wait(4)

        dy_d_dx = MathTex(r"\frac{(x+h)^2-x^2}{h}=").shift(RIGHT)
        nominator = always_redraw(
            lambda: DecimalNumber(k.get_value()**2 - 1, 5, color=BLUE).next_to(dy_d_dx, RIGHT)
        )
        divide_sign = MathTex(r"/", color=YELLOW).next_to(nominator, buff=0.2)
        denominator = always_redraw(
            lambda: DecimalNumber(k.get_value() - 1, 5, color=BLUE).next_to(divide_sign, RIGHT)
        )
        divide_g = VGroup(nominator, divide_sign, denominator)

        self.play(
            Create(dy_d_dx),
            Create(divide_g),
            run_time=2
        )
        self.wait(2)

        self.play(
            k.animate.set_value(1.0001),
            run_time=8,
            rate_func=slow_into
        )
        self.wait(5)

        self.play(
            k.animate.set_value(1.),
            run_time=0.5
        )
        self.wait(3)

        deriv_def = MathTex(r"f'(1)=2", color=GREEN).shift(3*RIGHT+1.5*UP)
        self.play(Write(deriv_def), run_time=2)
        self.wait(3)

        rect = SurroundingRectangle(divide_g, color=YELLOW)
        dividezero = MathTex(r"0/0=2\ ???", color=RED_C).next_to(rect, DOWN)

        self.play(
            Create(rect),
            Write(dividezero),
            run_time=3
        )

        self.wait(4)


class CalcSqrt2(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait(4)
        
        question = MathTex(r"\sqrt{1.01}","=?")
        self.play(Write(question), run_time = 2)
        approx = MathTex(r"\approx 1.0\cdots", color=GREEN).next_to(question[0], RIGHT)
        self.wait(3)
        self.play(Transform(question[1], approx), run_time=2)
        self.wait(2)
        self.play(
            question.animate.shift(UP*2),
            run_time=2
        )
        self.wait(5)

        func_def = MathTex(r"f(x)=\sqrt{x}=x^{0.5}", color=BLUE).scale(0.8).shift(UP+3*LEFT)
        derv_func = MathTex(r"f'(x)=0.5x^{-0.5}=\frac{1}{2\sqrt{x}}", color=ORANGE).scale(0.8).shift(UP+3*RIGHT)
        derv_1 = MathTex(r"f'(1)=\frac{1}{2}", color=ORANGE).scale(0.8).shift(UP+3*RIGHT)
        self.play(Write(func_def), run_time=2)
        self.wait(2)
        self.play(Write(derv_func), run_time=2)
        self.wait(2)
        self.play(Transform(derv_func, derv_1), run_time=1)
        self.wait(4)

        linear_approx = MathTex(r"f(x)\approx \frac{x}{2}+\frac{1}{2}", color=GREEN).shift(DOWN)
        x_close_1_text = Text("当x接近于1", color=YELLOW).scale(0.8).shift(4*RIGHT+DOWN)
        self.play(Write(linear_approx), run_time=2)
        self.wait(2)
        self.play(Write(x_close_1_text))
        self.wait(5)
        la2 = MathTex(r"\sqrt{x}\approx \frac{x}{2}+\frac{1}{2}", color=GREEN).shift(DOWN+2*LEFT)
        self.play(ReplacementTransform(linear_approx, la2), 
                  #FadeOut(x_close_1_text),
                  run_time=2)
        self.wait(2)
        la3 = MathTex(r"\sqrt{1.01}\approx",r"\frac{1.01}{2}+\frac{1}{2}", color=GREEN).shift(DOWN+2*LEFT)
        self.play(ReplacementTransform(la2, la3), run_time=2)
        self.wait(2)
        res = MathTex(r"1.005", color=ORANGE).next_to(la3[0], RIGHT)
        self.play(Transform(la3[1], res), run_time=2)
        self.wait(2)
        sqrt2 = MathTex(r"\sqrt{1.01}=",r"1.0049875621\cdots", color=BLUE).shift(DOWN*2).align_to(la3, LEFT)
        self.play(DrawBorderThenFill(sqrt2), run_time=2)
        self.wait(3)
        rect1 = SurroundingRectangle(res, color=YELLOW)
        rect2 = SurroundingRectangle(sqrt2[1], color=YELLOW)
        self.play(Create(rect1), Create(rect2), run_time=1.5)
        self.wait(6)

def f_money(k, x):
    res = 1.0
    for i in range(k):
        if  x >= i / k and x <= (i+1) / k:
            res *= (1 + x - i/k)
            break
        else:
            res *= (1 + 1/k)
    return res

class FuLiLv(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        # 不断精细差分，直到以无穷的速度取+存，卷复利率
        # 用折线图的方式展示最终接近于一个曲线，那就是e^x
        self.wait(4)
        bank = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project2\bank.svg")
        self.play(
            Create(bank),
            run_time=1
        )
        self.wait(3) # 现在假设有这么一家神奇的银行

        bank_move = bank.copy().scale(0.7).shift(LEFT*3+UP*2)
        self.play(
            Transform(bank, bank_move),
            run_time=2
        )
        self.wait(4)

        money = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project2\cash_money.svg").scale(0.3).shift(RIGHT*2+UP*2)

        self.play(Create(money))
        self.play(money.animate.shift(LEFT*4.5), run_time=3)
        self.wait(1)

        plane = NumberPlane(
            x_range=[0, 1.0, 0.2],
            y_range=[0, 4, 1],
            x_length=4,
            y_length=4,
        ).add_coordinates().shift(DOWN*1.5)
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane)
            ),
            run_time=2,
            lag_ratio=0.5
        )

        t1 = ValueTracker(0.0)
        S1_graph = always_redraw(
            lambda : plane.plot(lambda t: f_money(k=1, x=t), 
                                x_range=[0, t1.get_value()], 
                                color=ORANGE)
        )
        tmpt = always_redraw(
            lambda : Dot( plane.c2p(t1.get_value(), f_money(k=1, x=t1.get_value())),
                        color=BLUE
                        )
        )
        self.play(Create(S1_graph), Create(tmpt))

        money2= money.copy().next_to(money, DOWN)
        self.play(
            DrawBorderThenFill(money2),
            t1.animate.set_value(1),
            run_time=5
        )
        
        #money_group = VGroup(money, money2)
        self.wait(3)
        self.play(money.animate.shift(RIGHT*4.5), 
                  money2.animate.shift(RIGHT*4.5),
                  Flash(tmpt))
    
        self.wait(4)
        self.play(FadeOut(money), FadeOut(money2), FadeOut(S1_graph), FadeOut(tmpt))
        self.wait(3)
        
        sscq = Text("随时存取", color=YELLOW_C).to_edge(UP)
        self.play(Write(sscq), run_time=2)
        self.wait(3)

        money = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project2\cash_money.svg").scale(0.3).shift(RIGHT*2+UP*2)
        self.play(Create(money))
        self.play(money.animate.shift(LEFT*4.5), run_time=3)
        self.wait(1)

        t2 = ValueTracker(0.0)
        S2_graph = always_redraw(
            lambda : plane.plot(lambda t: f_money(k=2, x=t), x_range=[0, t2.get_value()], color=BLUE_A)
        )
        tmpt = always_redraw(
            lambda : Dot( plane.c2p(t2.get_value(), f_money(k=2, x=t2.get_value())),
                        color=BLUE
                        )
        )

        self.play(Create(S2_graph), Create(tmpt))
        self.play(
            t2.animate.set_value(0.5), run_time=3,
            rate_func=linear
        )
        self.play(Flash(tmpt))
        self.wait(2)
        self.play(money.animate.shift(4.5*RIGHT),
            rate_func=there_and_back,
            run_time=3
        )
        self.wait(3)
        self.play(
            t2.animate.set_value(1.0), run_time=3,
            rate_func=linear
        )
        self.wait(3)
        ind_line = DashedLine(
            start = plane.c2p(0, f_money(k=1, x=0)),
            end = plane.c2p(1 , f_money(k=1, x=1)),
            stroke_width = 4,
            color=YELLOW
        )
        self.play(Create(ind_line), run_time=2)
        t2_value = MathTex(r"= 2.25").scale(0.5).next_to(tmpt, RIGHT)
        self.play(Write(t2_value))
        self.wait(2)
        self.play(FadeOut(t2_value))

        self.wait(8)
        self.play(FadeOut(tmpt))

        t4 = ValueTracker(0.0)
        S4_graph = always_redraw(
            lambda : plane.plot(lambda t: f_money(k=4, x=t), x_range=[0, t4.get_value()], color=GREEN_C)
        )
        tmpt = always_redraw(
            lambda : Dot( plane.c2p(t4.get_value(), f_money(k=4, x=t4.get_value())),
                        color=BLUE
                        )
        )
        
        self.play(FadeOut(money)
        )

        # Play 2 segments
        money = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project2\cash_money.svg").scale(0.3).shift(RIGHT*2+UP*2)
        self.play(Create(money))
        self.play(money.animate.shift(LEFT*4.5), run_time=3)
        self.wait(1)

        self.play(Create(S4_graph), Create(tmpt))
        for i in range(1, 5):
            self.wait(0.5)
            self.play(
                t4.animate.set_value(i/4), run_time=1.5,
                rate_func=smooth
            )
            self.play(Flash(tmpt))

            if i < 4:
                self.play(money.animate.shift(4.5*RIGHT),
                    rate_func=there_and_back,
                    run_time=2.5
                )
        self.wait(2)
        t4_value = MathTex(r"\approx 2.441").scale(0.5).next_to(tmpt, RIGHT)
        self.play(Write(t4_value))
        self.wait(2)
        self.play(FadeOut(t4_value))
        self.wait(2)

        ## Play 20 segments
        self.play(FadeOut(money), FadeOut(tmpt))
        tt = ValueTracker(0.0)
        S20_graph = always_redraw(
            lambda : plane.plot(lambda t: f_money(k=20, x=t), x_range=[0, tt.get_value()], color=PURPLE_C)
        )
        tmpt = always_redraw(
            lambda : Dot( plane.c2p(tt.get_value(), f_money(k=20, x=tt.get_value())),
                        color=BLUE
                        )
        )
        money = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project2\cash_money.svg").scale(0.3).shift(RIGHT*2+UP*2)
        self.play(Create(money))
        self.play(money.animate.shift(LEFT*4.5), run_time=3)
        self.wait(1)

        self.play(Create(S20_graph), Create(tmpt))
        for i in range(1, 4):
            self.wait(0.2)
            self.play(
                tt.animate.set_value(i/20), run_time=0.5,
                rate_func=smooth
            )
            self.play(money.animate.shift(4.5*RIGHT),
                    rate_func=there_and_back,
                    run_time=2
                )
        self.play(
                tt.animate.set_value(1), run_time=5,
                rate_func=smooth
            )
        self.wait(2)
        t20_value = MathTex(r"\approx 2.653").scale(0.5).next_to(tmpt, RIGHT)
        self.play(Write(t20_value))
        self.wait(2)
        self.play(FadeOut(t20_value))
        self.wait(3)

        # Infinite Limit
        self.play(FadeOut(tmpt))
        tinf = ValueTracker(0.0)
        Sinf_graph = always_redraw(
            lambda : plane.plot(lambda t: np.exp(t), x_range=[0, tinf.get_value()], 
                                color = YELLOW, stroke_width=5)
        )
        tmpt = always_redraw(
            lambda : Dot( plane.c2p(tinf.get_value(), np.exp(tinf.get_value())),
                        color=RED
                        )
        )
        
        self.play(
            Create(Sinf_graph),
            Create(tmpt),
        )
        self.wait()
        self.play(
            tinf.animate.set_value(1),
            run_time=5
        )
        self.play(Flash(tmpt))
        tinf_value = MathTex(r"\approx 2.71828...").scale(0.8).next_to(tmpt, RIGHT)
        self.play(Write(tinf_value))
        self.wait(3)
        e_value = MathTex(r"=e", color=RED).scale(0.8).next_to(tmpt, RIGHT)
        self.play(
            ReplacementTransform(tinf_value, e_value), 
            run_time=2
        )
        self.wait(3)

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class DeduceE(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        self.wait(2)
        half_comp = MathTex(r"h(2)=", "1", r"\times \left( 1+ \frac{1}{2} \right)"
                             , r"\times \left( 1+ \frac{1}{2} \right)", color=GREEN).scale(0.8).shift(UP*2.5 + 2*LEFT)
        half_res = MathTex("=2.25", color=YELLOW_C).scale(0.8).next_to(half_comp, RIGHT)

        quad_comp = MathTex(r"h(4)=", r"\left( 1+ \frac{1}{4} \right)", 
                            r"\times \left( 1+ \frac{1}{4} \right)",
                            r"\times \left( 1+ \frac{1}{4} \right)",
                            r"\times \left( 1+ \frac{1}{4} \right)", color=BLUE).scale(0.7).next_to(half_comp, DOWN).align_to(half_comp, LEFT)
        quad_res = MathTex("=2.441", color=YELLOW_C).scale(0.7).next_to(quad_comp, RIGHT)

        #n_comp = MathTex(r"h(n)=\left( 1 + \frac{1}{n} \right)^n", color=RED_C)
        e_def = MathTex(r"e=", r"\lim_{n\to \infty} ",
                        r"h(n) =",r"\lim_{n\to \infty}",
                        r"\left( 1 + \frac{1}{n} \right)^n",
                          color=RED_C).shift(0.5*DOWN)

        self.play(Write(half_comp[0]))
        self.wait(5) # 我们用 h(n)表示存取n次最后得到的钱

        for i in range(1, 4):
            self.play(Write(half_comp[i]))
            if i == 1:
                self.play(Circumscribe(half_comp[i]))
                explan = Text("初始本金", color=YELLOW).scale(0.7).align_to(half_comp[i], UP).shift(RIGHT*3)
                self.play(Write(explan), time=1)
                self.wait(2)
                self.play(FadeOut(explan))
                self.wait(3)
            elif i == 2:
                self.play(Circumscribe(half_comp[i]))
                explan = Text("1+利率×时间", color=YELLOW).scale(0.7).align_to(half_comp[i], UP).shift(RIGHT*3)
                self.play(Write(explan), time=1)
                self.wait(2)
                self.play(FadeOut(explan))
                self.wait(3)
            else:
                self.wait(4)
        self.play(Write(half_res))
        self.wait(2)
        self.play(Write(quad_comp), time=3)
        self.wait(2)
        self.play(Write(quad_res), time=2)
        self.wait(2)

        self.play(Write(e_def[2]),
                  Write(e_def[4]),
                   run_time=3)
        self.wait(2)
        self.play(Write(e_def[1]),
                  Write(e_def[3]), run_time=3)
        self.wait(2)
        self.play(Write(e_def[0]))
        self.wait(4)

        self.play(
            FadeOut(half_comp), FadeOut(half_res),
            FadeOut(quad_comp), FadeOut(quad_res),
            FadeOut(e_def[1:3]),
            e_def[0].animate.shift(3*UP+1.7*RIGHT),
            e_def[3:].animate.shift(3*UP+0.8*LEFT),
            run_time=2
        )
        self.wait(5)

        plane = NumberPlane(
            x_range=[0, 1.0, 0.2],
            y_range=[0, 4, 1],
            x_length=6,
            y_length=4,
        ).add_coordinates().shift(DOWN*0.5 + LEFT * 3)

        self.play(
            LaggedStart(
                DrawBorderThenFill(plane)
            ),
            run_time=2,
            lag_ratio=0.5
        )
        
        func = plane.plot(
            lambda t: np.exp(t), x_range=[0,1]
        )

        x = ValueTracker(0.5)
        dx = ValueTracker(0.2)

        pt = always_redraw(
            lambda: Dot().move_to(plane.c2p(x.get_value(), np.exp(x.get_value())))
            .set_color(BLUE)
        )

        pt2 = always_redraw(
            lambda: Dot().move_to(plane.c2p(x.get_value()+dx.get_value(), np.exp(x.get_value()+dx.get_value())))
            .set_color(GREEN)
        )

        secant = always_redraw(
            lambda: plane.get_secant_slope_group(
                x = x.get_value(),
                graph = func,
                dx = dx.get_value(),
                dx_line_color=YELLOW,
                dy_line_color=ORANGE,
                dx_label = r'\Delta x',
                dy_label = r'\Delta y',
                secant_line_color = GREEN,
                secant_line_length = 4
            )
        )

        self.play(Create(func), run_time=1.5)
        self.wait(3)
        self.play( Create(VGroup(pt, pt2)),
            Create(secant), 
            run_time=4)
        self.wait(2)

        eq1 = MathTex(r"\Delta y=", r"y(1+\Delta x)","-y").scale(0.8).shift(RIGHT * 4 + UP)
        eq2 = MathTex(r"\Delta y=y \Delta x").scale(0.8).shift(UP).align_to(eq1, LEFT)
        eq3 = MathTex(r"\frac{\Delta y}{\Delta x} = y", color=BLUE).scale(0.8).shift(UP).align_to(eq1, LEFT)
        self.play(Write(eq1), run_time=1)
        self.wait(3)
        rect = SurroundingRectangle(eq1[1])
        self.play(Create(rect), run_time=2)
        self.wait(6)
        self.play(FadeOut(rect))
        self.play(ReplacementTransform(eq1, eq2), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(eq2, eq3), run_time=2)
        self.wait(3)

        self.play(
            dx.animate.set_value(0),
            run_time = 3
            )
        self.wait(2)

        eq4 = MathTex(r"\lim_{\Delta x \to 0}\frac{\Delta y}{\Delta x} = y", color=BLUE).scale(0.8).shift(UP).align_to(eq1, LEFT)
        eq5 = MathTex(r"y' = y", color=RED_C).scale(0.8).shift(UP).align_to(eq1, LEFT)

        self.play(ReplacementTransform(eq3, eq4), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(eq4, eq5), run_time=2)
        self.wait(3)

        e_another_def = MathTex(r"(e^x)'=e^x", color=YELLOW).next_to(eq5, DOWN, buff=0.4)
        self.play(Write(e_another_def), run_time=2)
        self.wait()
        self.play(Circumscribe(e_another_def), Circumscribe(eq5), run_time=1.5)
        self.wait(4)

class DivideZeroDestroy(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        # 纯公式动画，假设存在一个z是1/0的结果，会导致代数结构坍缩
        question = Text("凭什么不能定义1/0的结果呢？", color=BLUE).shift(UP * 2.5)
        self.play(
            DrawBorderThenFill(question),
            run_time=2
        )

        self.wait(4)

        answer = Text("可以，但会毁了整个数学", color=RED).scale(1.5)
        self.play(DrawBorderThenFill(answer), run_time=2)
        self.wait(4)
        self.play(FadeOut(question), FadeOut(answer), run_time=1.5)

        hypo = MathTex(r"1/0=", r"z", color=BLUE).shift(UP*2)
        eq1 = MathTex(r"1=z\times 0", color=BLUE).shift(UP*2)
        any_x = MathTex(r"\forall x\in \mathbb{R}", color=YELLOW).shift(RIGHT*4)
        eq2 = MathTex(r"1\times x = z\times 0 \times x", color=WHITE).next_to(eq1, DOWN, buff=0.4)
        eq3 = MathTex(r"1\times x = z\times (0 \times x)", color=WHITE).next_to(eq1, DOWN, buff=0.4)
        eq4 = MathTex(r"x = z\times 0", color=GREEN).next_to(eq1, DOWN, buff=0.4)

        self.wait(4) # 我们不妨假设真的这么定义了
        self.play(DrawBorderThenFill(hypo), run_time=2)
        self.wait(8) # 看起来挺好的对吧，但你的定义肯定要和原有的运算保持兼容和匹配
        self.play(ReplacementTransform(hypo, eq1), run_time=2)
        self.wait(5+3) # 所以根据乘法和除法互为逆运算的性质，z乘以0就应该是1
        # 接下来，我们对等式两边同时乘以一个x
        self.play(Write(eq2), run_time=1)
        self.wait(3) # 有人会问，乘以哪个x呢？
        self.play(Write(any_x), run_time=1)
        self.wait(7) # 回答是，任何一个x。接下来，根据乘法分配律，我们可以加一个括号先计算
        self.play(ReplacementTransform(eq2, eq3), run_time=2)
        self.wait(4) # 然后我们对等式两边计算以下
        self.play(ReplacementTransform(eq3, eq4), run_time=2)
        self.wait(4)
        self.play(
            Circumscribe(eq1), Circumscribe(eq4),
            run_time=2, lag_ratio=0.5
        )

        eq5 = MathTex("x=1", color=RED).scale(1.4)
        self.wait(4) # 仔细看，你发现了什么？
        self.play(Write(eq5), run_time=2)
        self.wait(1)
        self.play(Indicate(any_x))
        self.wait(5)

        eq6 = MathTex("0=1", color=RED).scale(1.4)

        consq = Text("整个数学系统坍方了，只剩下一个1", color=YELLOW).shift(DOWN*1.5)
        consq2 = Text("1又等于0，整个数学世界除了0空无一物").next_to(consq, DOWN, buff=0.2)

        self.play(Write(consq), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(eq5, eq6), run_time=2)
        self.wait(2)
        self.play(Write(consq2), run_time=2)
        self.wait(10)

        # 本质上，没有什么事情是因为“人”的定义而成为能或者不能。学习数学等理科学科，
        # 尤其是以后要创新，大家要明白，能或者不能，背后的唯一决定因素是“有用还是没用”。
        # 基础的理论说不能的东西，高等的理论可能辩证否定它。
        # 但是，大破之后需要有大立，
        # 虚数i破除了根号下不能为负数的限制，带来的是全新的结构和崭新的联系。
        # 但定义这个z只能带来原有数学世界的坍缩，没有其他的价值。

        # 错误和突破，荒谬和真知，往往一念之差，却又咫尺天涯

class RotateComplexPlane(Scene):
    def construct(self):
        # 建立复平面，选几个点，绘制一个半透明的矩形
        # 将所有的对象乘以e^i*theta，连续滑动，感受旋转
        # 具体的，在i的位置使用数值计算以下，验证这一点
        # 在极坐标的几何意义下明白运算的本质，再用直角坐标的简单表示计算结果
        # 这就是omega 的来源。一个复数既是一个数字，又代表了一种运算的“操作”，这其中的玄妙和群论有着很大的关系
        # 这就是数学的魅力

        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait(2)
        theta = ValueTracker(0.)
        plane = ComplexPlane().add_coordinates()
        self.play(Create(plane), run_time=2)

        # Create a few points

        num_list = [1j, -1, -1j,  -1+3j]
        color_list = [ BLUE_C, GREEN_C, PURPLE_C, MAROON_C]
        # for i in range(len(num_list)):
        #     points.append(always_redraw(
        #         lambda: Dot(plane.number_to_point(num_list[i] * np.exp(theta.get_value() * 1j))))
        #         .set_color(color_list[i]) 
        #     )
        
        # for pt in points:
        #     self.play(Create(pt), run_time=0.5)
        #     self.wait()
        pt = always_redraw(
                 lambda: Dot(plane.number_to_point((2+1j)* np.exp(theta.get_value() * 1j)))
                 .set_color(BLUE_C) 
             )
        pt_lbl = always_redraw(
            lambda:MathTex(r"(2+i)\omega", color=YELLOW).scale(0.8).next_to(pt, RIGHT+UP)
            )

        line_to_pt = always_redraw(
            lambda: DashedLine(
                start = plane.number_to_point(0),
                end = plane.number_to_point((2+1j)* np.exp(theta.get_value() * 1j)),
                stroke_width = 4,
                stroke_color=BLUE_C
            )
        )

        self.play(
            Create(pt),
            Create(pt_lbl),
            Create(line_to_pt),
            run_time=2,
            lag_ratio=0.5
            )
        self.wait(2)

        eit = always_redraw(
                 lambda: Dot(plane.number_to_point(np.exp(theta.get_value() * 1j)))
                 .set_color(RED) 
             )
        eit_lbl = always_redraw(
            lambda: MathTex(r"\omega=e^{i\theta}", color=RED).scale(0.8).next_to(eit, RIGHT+UP)
        )
        line_to_eit = always_redraw(
            lambda: Line(
                start = plane.number_to_point(0),
                end = plane.number_to_point(np.exp(theta.get_value() * 1j)),
                stroke_width = 4,
                stroke_color = ORANGE
            )
        )

        self.play(
            Create(eit),
            Create(eit_lbl),
            Create(line_to_eit),
            run_time=2,
            lag_ratio=0.5)
        # self.wait(2)
        # self.play(FadeOut(pt_lbl))
        self.wait(2)

        theta_text = MathTex(r"\theta=", color=RED).scale(0.7).move_to(plane.number_to_point(0.5-0.5j))
        theta_value = always_redraw(
            lambda: DecimalNumber(theta.get_value(), 3).scale(0.7).set_color(YELLOW_C).next_to(theta_text)
        )
        small_arc = always_redraw(
            lambda: ParametricFunction(
                lambda t: plane.c2p(0.2*np.cos(t), 0.2*np.sin(t)),
                t_range = [0, theta.get_value()],
                color = RED
            )
        )

        self.play(
            Write(theta_text),
            Write(theta_value),
            Create(small_arc),
            run_time=2,
            lag_ratio=0.5
        )
        self.wait(4)
        # Animate the rotation of the points
        self.play(
            theta.animate.set_value(0.7*np.pi),
            rate_func=linear,
            run_time=6
        )

        self.wait(3)

        self.play(
            theta.animate.set_value(0),
            rate_func=smooth,
            run_time=6
        )

        e0 = always_redraw(
            lambda: Dot(plane.number_to_point(num_list[0] * np.exp(theta.get_value() * 1j)))
            .set_color(color_list[0])
        )
        line_to_e0 = always_redraw(
            lambda: Line(
                start = plane.number_to_point(0),
                end = plane.number_to_point(num_list[0] * np.exp(theta.get_value() * 1j)),
                stroke_width = 4,
                stroke_color = color_list[0]
            )
        )
        self.play(Create(e0, run_time=0.5), Create(line_to_e0, run_time=1))
        self.wait(0.5)

        e1 = always_redraw(
            lambda: Dot(plane.number_to_point(num_list[1] * np.exp(theta.get_value() * 1j)))
            .set_color(color_list[1])
        )
        line_to_e1 = always_redraw(
            lambda: Line(
                start = plane.number_to_point(0),
                end = plane.number_to_point(num_list[1] * np.exp(theta.get_value() * 1j)),
                stroke_width = 4,
                stroke_color = color_list[1]
            )
        )
        self.play(Create(e1, run_time=0.5), Create(line_to_e1, run_time=1))
        self.wait(0.5)

        e2 = always_redraw(
            lambda: Dot(plane.number_to_point(num_list[2] * np.exp(theta.get_value() * 1j)))
            .set_color(color_list[2])
        )
        line_to_e2 = always_redraw(
            lambda: Line(
                start = plane.number_to_point(0),
                end = plane.number_to_point(num_list[2] * np.exp(theta.get_value() * 1j)),
                stroke_width = 4,
                stroke_color = color_list[2]
            )
        )
        self.play(Create(e2, run_time=0.5), Create(line_to_e2, run_time=1))
        self.wait(0.5)

        e3 = always_redraw(
            lambda: Dot(plane.number_to_point(num_list[3] * np.exp(theta.get_value() * 1j)))
            .set_color(color_list[3])
        )
        line_to_e3 = always_redraw(
            lambda: Line(
                start = plane.number_to_point(0),
                end = plane.number_to_point(num_list[3] * np.exp(theta.get_value() * 1j)),
                stroke_width = 4,
                stroke_color = color_list[3]
            )
        )
        self.play(Create(e3, run_time=0.5), Create(line_to_e3, run_time=1))
        self.wait(3)

        self.play(
            theta.animate.set_value(0.5*np.pi),
            rate_func=smooth,
            run_time=5
        )
        self.wait(5)
        xt = 1
        x_mtex_list = ["1", "i", "-1", "-i"]
        for i in range(4):
            arr = Arrow(
                start = plane.number_to_point(xt),
                end = plane.number_to_point(xt * 1j),
                buff=0.02,
                stroke_width=5,
                color=YELLOW
            )
            text = MathTex(x_mtex_list[i], r"\times i =", x_mtex_list[(i+1)%4]).scale(0.8).shift(5*LEFT + 2.5*UP)
            self.play(Write(text), run_time=1)
            self.wait(1)
            self.play(Create(arr), run_time=1)
            self.wait(1)
            self.play(FadeOut(text), FadeOut(arr))
            self.wait(2)
            xt = xt * 1j

        circ = Circle(
            radius=1,
            color=DARK_GRAY,
            stroke_width=4
        )
        self.play(Create(circ), run_time=2)
        self.play(ShowPassingFlash(
            circ.copy().set_color(BLUE),
            run_time=2,
            time_width=0.3
        ))
        self.wait()
        self.play(FadeOut(circ))
        self.wait()
        self.play(
            theta.animate.set_value(0),
            rate_func=smooth,
            run_time=2
        )
        self.wait()
        self.play(
            FadeOut(e0), FadeOut(line_to_e0),
            FadeOut(e1), FadeOut(line_to_e1),
            FadeOut(e2), FadeOut(line_to_e2),
            FadeOut(e3), FadeOut(line_to_e3),
        )

        self.wait()
        text = Text("要转45°就乘以").scale(0.8).shift(5*LEFT+2.5*UP)
        pi_d4 = MathTex(r"e^{i\pi/4}",color=YELLOW).next_to(text, RIGHT)
        pi_d4_t1 = MathTex(r"\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}",color=YELLOW).scale(0.8).next_to(text, RIGHT)
        pi_d4_t2 = MathTex(r"\frac{\sqrt{2}}{2}+i\frac{\sqrt{2}}{2}",color=YELLOW).scale(0.8).next_to(text, RIGHT)
        self.play(
            Write(text), Write(pi_d4),
            run_time=3
        )
        self.wait(0.5)
        self.play(
            theta.animate.set_value(np.pi * 0.25),
            rate_func=smooth,
            run_time=6
        )

        self.wait(3)
        self.play(ReplacementTransform(pi_d4, pi_d4_t1))
        self.wait(3)
        self.play(ReplacementTransform(pi_d4_t1, pi_d4_t2))
        self.wait(4)

        text2 = Text("用极坐标确定本质，用直角坐标方便计算").scale(0.8).add_background_rectangle().shift(DOWN*1.5)
        self.play(DrawBorderThenFill(text2), run_time=3)
        self.wait(5)
        self.play(FadeOut(text2))
        self.wait(2)
        self.play(Circumscribe(eit_lbl))
        text3 = Text("既是一个复数，又是一种变换的操作", color=YELLOW).add_background_rectangle().scale(0.8).shift(DOWN*1.5)
        self.play(Write(text3), run_time=2)
        self.wait(3)
        text4 = MathTex(r"e^{i\theta_1} \cdot e^{i\theta_2}=e^{i(\theta_1 + \theta_2})",
                        color=GREEN).scale(0.8).add_background_rectangle().shift(DOWN*2.5)
        self.play(Write(text4), run_time=2)
        self.wait(6)


class intro(Scene):
    def construct(self):
        title = Text("漫士沉思录", color=BLUE_C).shift(UP).scale(2)
        sub_title = Text("勘误答疑  导数  欧拉公式几何  自然常数e").scale(0.8).next_to(title, DOWN, buff=1)
        self.play(DrawBorderThenFill(title), run_time=5)
        self.play(Write(sub_title), run_time=4)
        self.wait(3)

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

        self.wait(1.5)
        name = Text("漫士沉思录", color=YELLOW).scale(1.5)
        self.play(
            FadeOut(tg[1]),
            tg[0].animate.shift(RIGHT * 3+UP*2),
            tg[2].animate.shift(LEFT * 3+UP*1.8),
            DrawBorderThenFill(name),
            run_time=2,
            lag_ratio=0.7
        )
        self.wait(3)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )