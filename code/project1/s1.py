from manim import *
import numpy as np
import math

class Intro1(Scene):
    def construct(self):

        texts = "\\sin(x)", "=x", "-\\frac{x^3}{3!}", "+\\frac{x^5}{5!}", "-\\frac{x^7}{7!}", "+\\frac{x^9}{9!}", "-\\cdots"
        print(r"".join(texts))
        taylor = MathTex(r"".join(texts), tex_to_color_map={r"\\sin(x)": BLUE, r"=": WHITE}, substrings_to_isolate=texts,
                      color=GREEN).scale(0.8).shift(3.3 * UP)
        parts = VGroup(*[taylor.get_part_by_tex(text) for text in texts])
        rectangles = [SurroundingRectangle(parts[:i + 2]) for i in range(6)]
        self.play(Write(taylor))
        self.wait(5)  # 从封面看 这部视频讲的是正弦函数泰勒展开的几何含义

        # arrow_x = Arrow(4 * LEFT, 4 * RIGHT, buff=0, stroke_width=3)
        # arrow_y = Arrow(1.2 * DOWN, 1.2 * UP, buff=0, stroke_width=3)
        # axes = VGroup(arrow_x, arrow_y).shift(2.8 * LEFT)

        axes = Axes(
            x_range=[-5.7, 5.7, 1],
            y_range=[-1.7, 1.7, 1],
            x_length=8,
            y_length=2.5,
            axis_config={"color": BLUE},
        )
        labels = axes.get_axis_labels()

        self.play(Create(axes), Create(labels), run_time=2)

        #shade = VGroup(shade_0, shade_0.copy().shift(6.5 * DOWN))
        graph = axes.plot(np.sin, [-4, 4, 0.01], color=BLUE)#.shift(2.8 * LEFT)
        graph_0 = axes.plot(lambda t: t, [-4, 4, 0.01], color=GREEN)#.shift(2.8 * LEFT)
        graph_1 = axes.plot(lambda t: t - t ** 3 / 6, [-4, 4, 0.01], color=GREEN)#.shift(2.8 * LEFT)
        graph_2 = axes.plot(lambda t: t - t ** 3 / 6 + t ** 5 / 120, [-4, 4, 0.01], color=GREEN)#.shift(2.8 * LEFT)
        graph_3 = axes.plot(lambda t: t - t ** 3 / 6 + t ** 5 / 120 - t ** 7 / 5040, [-4, 4, 0.01],
                                color=GREEN)#.shift(2.8 * LEFT)
        graph_4 = axes.plot(lambda t: t - t ** 3 / 6 + t ** 5 / 120 - t ** 7 / 5040 + t ** 9 / 362880,
                                [-4, 4, 0.01], color=GREEN)#.shift(2.8 * LEFT)
        graph_5 = graph.copy().set_color(GREEN)
        self.add(graph, graph_0, taylor).play(Create(graph),
                                            Create(graph_0),
                                            Create(rectangles[0]))
        self.wait(1)
        self.play(Transform(graph_0, graph_1), Transform(rectangles[0], rectangles[1]))
        self.wait(1)
        self.play(Transform(graph_0, graph_2), Transform(rectangles[0], rectangles[2]))
        self.wait(1)
        self.play(Transform(graph_0, graph_3), Transform(rectangles[0], rectangles[3]))
        self.wait(1)
        self.play(Transform(graph_0, graph_4), Transform(rectangles[0], rectangles[4]))
        self.wait(1)
        self.play(Transform(graph_0, graph_5), Transform(rectangles[0], rectangles[5]))
        self.wait(6)  # 说实话 这种题材的视频没什么好看的 无非就是给泰勒展开硬找个几何含义 然后把泰勒展开的推导过程生搬过去 （空闲） 不过这种题材观众爱看


class SinValue(Scene):
    def construct(self):
        # First, we create the initial text
        question = MathTex(r"\sin(1) = ?")
        self.wait(8)
        self.play(Write(question))
        self.wait(5)
        # We then create the answer text
        answer = MathTex(r"\sin(1) = 0.841470984807...")
        # We move the answer to the same position as the question to prepare for the transformation
        answer.move_to(question.get_center())

        # The question transforms into the answer
        self.play(Transform(question, answer))

        # Then we wait a bit before fading out
        self.wait(12)
        self.play(FadeOut(question))

class Exp(Scene):
    def construct(self):
        # First, we create the initial text
        texts = "e^x", "=1", "+\\frac{x}{1!}", "+\\frac{x^2}{2!}", "+\\frac{x^3}{3!}", "+\\frac{x^4}{4!}", "+\\cdots"
        #print(r"".join(texts))
        taylor = MathTex(r"".join(texts), tex_to_color_map={r"e^(x)": BLUE, r"=": WHITE},
                         substrings_to_isolate=texts,
                         color=GREEN).scale(0.8).shift(1.3 * UP)
        parts = VGroup(*[taylor.get_part_by_tex(text) for text in texts])
        #rectangles = [SurroundingRectangle(parts[i + 2]) for i in range(5)]
        rect = SurroundingRectangle(parts[1:])
        self.play(Write(taylor), run_time=2)
        self.wait(5)
        self.play(Create(rect))
        self.wait(3)

        polynomials_text = Text("Polynomials").next_to(rect, UP)
        self.play(Write(polynomials_text))
        self.wait(2)
        self.play(FadeOut(rect), FadeOut(polynomials_text))
        self.wait(3)


        sum_eq = MathTex(r"e^x=\sum_{n=0}^{\infty} \frac{x^n}{n!}").move_to(taylor.get_center())
        self.play(Transform(taylor, sum_eq))
        self.wait(4)
        sum_eq2 = MathTex(r"e^{ix}=\sum_{n=0}^{\infty} \frac{{(ix)}^n}{n!}").move_to(taylor.get_center())
        self.play(ReplacementTransform(taylor, sum_eq2))
        self.wait(5)

        sum_eq3 = MathTex(r"e^{i\pi}=\sum_{n=0}^{\infty} \frac{{(i\pi)}^n}{n!}").move_to(taylor.get_center())
        self.play(ReplacementTransform(sum_eq2, sum_eq3))
        self.wait(5)


class Derivative(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-0.5, 4.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True},
        )
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        graph = axes.plot(lambda x: x**2, color=BLUE)
        func_label = axes.get_graph_label(graph, label='f(x) = x^2')

        point = Dot().move_to(axes.c2p(1, 1))
        point_label = MathTex("(1,1)", color=RED).next_to(point, RIGHT+0.3*DOWN)

        tangent_line = axes.plot(
            lambda x: 2*x-1, [0.5, 2.0, 0.01], color=GREEN,
        )
        line_label = axes.get_graph_label(tangent_line, label="y = 2x-1")
        rect = SurroundingRectangle(line_label)

        self.wait(2)
        self.play(Create(axes), Write(x_label), Write(y_label), runtime=2)
        self.wait(1)
        self.play(Create(graph), Write(func_label))
        self.wait(2)
        self.play(Create(point), Write(point_label))
        self.wait(4)

        self.play(Create(tangent_line), Write(line_label))
        self.wait(2)

        derv = MathTex(r"f'(1)=2").next_to(rect, DOWN)

        self.play(Create(rect))
        self.wait(2)
        self.play(Write(derv))
        self.wait(7)

        # Introduction to the derivative
        derivative_intro = Text("导数的几何含义就是函数在某一点的切线斜率").shift(3*DOWN)
        self.play(Write(derivative_intro))
        self.wait(4)
        self.play(FadeOut(derivative_intro))

        self.wait(3)
        # The formula for the derivative of k*x^n
        derivative_formula = MathTex(r"\frac{d}{dx} (x^n) = n\cdot x^{n-1}").shift(3.3*DOWN)
        self.play(Write(derivative_formula))
        self.wait(4)

class Whythis(Scene):
    def construct(self):
        # First, we create the initial text
        e1 = MathTex(r"e^x=\sum_{n=0}^{\infty} \frac{x^n}{n!}")
        self.wait(4)
        question = Text("为啥非要长成这个样子呢？", color=GREEN).next_to(e1, DOWN*1.2)
        self.play(Write(e1))
        self.wait(4)
        self.play(Write(question))
        self.wait(5)

        # Then we wait a bit before fading out
        self.play(FadeOut(question))

class ExpId(Scene):
    def construct(self):
        # Showing the Taylor expansion of e^x up to 5 terms
        taylor_expansion = MathTex(
            "e^x", "=", "1", "+", "x", "+", "\\frac{x^2}{2!}", "+", "\\frac{x^3}{3!}", "+", "\\frac{x^4}{4!}", "+", "\\cdots",
            color=GREEN
        ).scale(0.8).shift(1.3 * UP)
        self.play(Write(taylor_expansion))
        self.wait(2)

        # Show the derivative of x^n at the right top of the screen
        power_rule = MathTex(r"\frac{d}{dx} (x^n) = n x^{n-1}",color=RED).to_edge(UP).to_edge(RIGHT)
        self.play(Write(power_rule))
        self.wait(2)

        # Taking the derivative
        deriv_text = MathTex("(e^x)'", "=").next_to(taylor_expansion, 1.8*DOWN).shift(LEFT*3)
        self.play(Write(deriv_text))
        self.wait(2)

        # Copy the term from the Taylor expansion, take the derivative, and transform it into the corresponding result
        transformed_terms = ["0", "1", "x", "\\frac{x^2}{2!}", "\\frac{x^3}{3!}"]
        last_term = deriv_text
        for i in range(2, len(taylor_expansion)-1, 2):  # -1 to exclude "\\cdots"
            # Copy the term from the Taylor expansion
            term = taylor_expansion[i].copy().next_to(last_term, 2*RIGHT)
            self.play(TransformFromCopy(taylor_expansion[i], term))

            # Take the derivative
            if i == 2:  # For the first term (1)', we do not need a "+" at the left
                term_deriv = MathTex("\\left(" + taylor_expansion[i].get_tex_string() + "\\right)'").next_to(last_term, RIGHT)
            else:
                term_deriv = MathTex("+", "\\left(" + taylor_expansion[i].get_tex_string() + "\\right)'").next_to(last_term, RIGHT)
            self.play(Transform(term, term_deriv))

            # Transform the derivative into the corresponding result
            if i == 2:
                term_result = MathTex(transformed_terms[i // 2 - 1]).next_to(last_term, RIGHT)
                last_term = term_result
            else:
                term_result = MathTex("+", transformed_terms[i//2-1]).next_to(last_term, RIGHT)
                last_term = term_result
            self.play(Transform(term, term_result))

            # Update the derivative text

            # _deriv_text = MathTex(deriv_text.get_tex_string(), term_result.get_tex_string())
            # self.play(Transform(deriv_text, _deriv_text))
            # deriv_text = _deriv_text
            #self.play(Write(deriv_text))

            self.wait(1)

        ddd = MathTex("+...").next_to(last_term, RIGHT)
        self.play(Write(ddd))

        self.wait(3)

        # Showing that the derivative function is identical to the original function
        identical_text = Text("完全一致!", color=YELLOW).shift(2.5 * DOWN)
        self.play(Write(identical_text))
        self.wait(2)
        equal = MathTex("e^x=(e^x)'").next_to(identical_text, DOWN)
        self.play(Write(equal))
        self.wait(2)

class WhyExp(Scene):
    def construct(self):
        # First, we create the initial text
        e1 = MathTex(r"f(x)=\sum_{n=0}^{\infty} \frac{x^n}{n!}")
        self.wait(4)
        question = Text("为什么这个函数一定是一个指数函数呢？", color=GREEN).next_to(e1, DOWN*1.2)
        self.play(Write(e1))
        self.wait(3)
        self.play(Write(question))
        self.wait(3)

        # Then we wait a bit before fading out
        self.play(FadeOut(question))
        self.wait(4)

        e2 = MathTex(r"f(x)f(y)=\left(\sum_{n=0}^{\infty} \frac{x^n}{n!}\right)\left(\sum_{n=0}^{\infty} \frac{y^n}{n!}\right)",
                     color=BLUE).shift(1.3*UP+LEFT)
        e3 = MathTex(r"f(x)f(y)=\left(1+\frac{x}{1!}+\frac{x^2}{2!}+\frac{x^3}{3!}+\cdots\right)\left(1+\frac{y}{1!}+\frac{y^2}{2!}+\frac{y^3}{3!}\cdots\right)",
                     color=BLUE).scale(0.8).move_to(e2.get_center())
        self.play(Transform(e1, e2))
        self.wait(4)
        self.play(Transform(e1, e3))
        self.wait(3)

        zero = MathTex(r"0\ deg:",r"\quad 1").scale(0.6).next_to(e3, DOWN*2.5)
        one = MathTex(r"1\ deg:",r"\quad \frac{x}{1!}+\frac{y}{1!}").scale(0.6).next_to(zero, DOWN)
        one_1 = MathTex(r"1\ deg:",r"\quad \frac{x+y}{1!}").scale(0.6).next_to(zero, DOWN)
        two = MathTex(r"2\ deg:",r"\quad \frac{x^2}{2!}+\frac{xy}{1!\cdot 1!}+\frac{y^2}{2!}").scale(0.6).next_to(one, DOWN)
        two_1 = MathTex(r"2\ deg:",r"\quad \frac{1}{2!}\left(x^2+\frac{2!}{1!\cdot 1!} xy + y^2\right)").scale(0.6).next_to(one, DOWN)
        two_2 = MathTex(r"2\ deg:",r"\quad \frac{1}{2!}\left(x^2+2 xy + y^2\right)").scale(0.6).next_to(one, DOWN)
        two_3 = MathTex(r"2\ deg:",r"\quad \frac{(x+y)^2}{2!}").scale(0.6).next_to(one, DOWN)
        k = MathTex(r"k\ deg:",r"\quad \sum_{i=0}^k \frac{x^i}{i!}\cdot\frac{y^{k-1}}{(k-i)!}").scale(0.6).next_to(two, DOWN)
        k_1 = MathTex(r"k\ deg:", r"\quad \frac{1}{k!}\sum_{i=0}^k \frac{k!}{i!(k-i)!} x^i\cdot y^{k-i}").scale(0.6).next_to(two,
                                                                                                                   DOWN)
        k_2 = MathTex(r"k\ deg:", r"\quad \frac{(x+y)^k}{k!}").scale(0.6).next_to(two, DOWN)


        for eq in [zero,one, one_1, two, two_1, two_2, two_3, k, k_2, k_1]:
            eq.align_to(zero, LEFT)

        self.play(Write(zero))
        self.wait(3)
        self.play(Write(one))
        self.wait(3)
        self.play(Transform(one, one_1))
        self.wait(3)
        self.play(Write(two))
        self.wait(3)
        self.play(Transform(two, two_1))
        self.wait(1.5)
        self.play(Transform(two, two_2))
        self.wait(1.5)
        self.play(Transform(two, two_3))
        self.wait(1.5)
        self.play(Write(k))
        self.wait(2)
        self.play(Transform(k, k_1))
        self.wait(1.5)
        self.play(Transform(k, k_2))
        self.wait(5) #这是二项式定理

        feq1 = MathTex(r"f(x)f(y)=\sum_{n=0}^{\infty} \frac{(x+y)^n}{n!}",
                     color=BLUE).scale(0.8).move_to(e3.get_center())
        eqfxy = MathTex(r"f(x)f(y)=f(x+y)",
                     color=BLUE).scale(0.8).move_to(feq1.get_center())

        explusy = MathTex(r"a^x\cdot a^y=a^{x+y}, (a>0)",
                     color=YELLOW).scale(0.8).next_to(eqfxy, DOWN)

        self.play(Transform(e1, feq1))
        self.wait(3)
        self.play(Transform(e1, eqfxy))
        self.wait(3)
        self.play(Write(explusy))
        self.wait(3)

class Cale(Scene):
    def construct(self):
        e1 = MathTex(r"e^x =\sum_{n=0}^{\infty} \frac{x^n}{n!}").scale(0.8).shift(LEFT*2.8+UP*1.3)
        self.wait(4)
        question = Text("怎么计算e呢?", color=GREEN).next_to(e1, DOWN * 1.2)
        self.play(Write(e1))
        self.wait(3)
        self.play(Write(question))
        self.wait(3)
        self.play(FadeOut(question))

        e2 = MathTex(r"e^1 =\sum_{n=0}^{\infty} \frac{1^n}{n!}")
        e3 = MathTex(r"e =\sum_{n=0}^{\infty} \frac{1}{n!}")
        e4 = MathTex(r"e = \frac{1}{0!} + \frac{1}{1!} + \frac{1}{2!}+ \frac{1}{3!}+\frac{1}{4!}+\frac{1}{5!}+\frac{1}{6!}+\cdots")

        for e in [e2,e3, e4]:
            e.align_to(e1, LEFT)

        self.wait(3)
        self.play(Transform(e1, e2))
        self.wait(3)
        self.play(Transform(e1, e3))
        self.wait(3)
        self.play(Transform(e1, e4))

        result = MathTex(r"e\approx 2.71828183...", color=BLUE).next_to(e1, DOWN*1.5)
        self.play(Write(result))
        self.wait(5)

class Euler(Scene):
    def construct(self):
        e1 = MathTex(r"e^x =\sum_{n=0}^{\infty} \frac{x^n}{n!}").shift(LEFT*2.8+UP*1.3)
        self.wait(2)

        question = Text("欧拉:让我们代入复数试一试！", color=GREEN).next_to(e1, DOWN * 1.2)
        self.play(Write(e1))
        self.wait(8)
        zheshisha = MathTex(r"e^{i\theta}=??", color=RED).shift(1.5 * RIGHT + UP)
        self.play(Write(zheshisha))
        self.wait(4)
        self.play(Write(question))
        self.wait(3)
        self.play(FadeOut(question))
        self.play(FadeOut(zheshisha))

        power_rule = MathTex(r"i^2=-1, i^4=1", color=RED).scale(0.8).to_edge(UP).to_edge(RIGHT)
        # self.play(Write(power_rule))
        # self.wait(2)
        e2 = MathTex(r"e^{ix} =\sum_{n=0}^{\infty} \frac{(ix)^n}{n!}")
        e3 = MathTex(r"e^{ix} =\sum_{n=0}^{\infty} \frac{(ix)^{2n}}{(2n)!} + \sum_{n=0}^{\infty} \frac{(ix)^{2n+1}}{(2n+1)!}")
        e4 = MathTex(r"e^{ix} =", r"\sum_{n=0}^{\infty} (-1)^n\frac{x^{2n}}{(2n)!}", "+", r"i\sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{(2n+1)!}")

        eq_f = r"e^{ix} =", r"\sum_{n=0}^{\infty} (-1)^n\frac{x^{2n}}{(2n)!}", "+", r"i\sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{(2n+1)!}"
        # print(r"".join(texts))
        real_im = MathTex(r"".join(eq_f), tex_to_color_map={r"e^{ix}=": GREEN,
                                                            r"\sum_{n=0}^{\infty} (-1)^n\frac{x^{2n}}{(2n)!}":RED,
                                                            r"i\sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{(2n+1)!}":BLUE
                                                            },
                         substrings_to_isolate=eq_f,
                         color=GREEN).scale(0.8).shift(1.3 * UP)
        parts = VGroup(*[real_im.get_part_by_tex(text) for text in eq_f])
        real_rect = SurroundingRectangle(parts[1])
        img_rect = SurroundingRectangle(parts[3])

        for e in [e2,e3, e4]:
            e.align_to(e1, LEFT)

        self.wait(3)
        self.play(Transform(e1, e2))

        self.play(Write(power_rule))

        self.wait(5)
        self.play(Transform(e1, e3))
        self.wait(5)
        self.play(Transform(e1, e4))
        self.wait(6)

        self.play(Transform(e1, real_im))
        self.wait(3)
        self.play(Create(real_rect))

        rpt = Text("实部").next_to(real_rect, DOWN)
        ipt = Text("虚部").next_to(img_rect, DOWN)
        self.play(Write(rpt))
        self.wait(0.5)
        self.play(FadeOut(real_rect))

        self.wait(1)
        self.play(Create(img_rect))
        self.play(Write(ipt))
        self.wait(0.5)
        self.play(FadeOut(img_rect))
        self.wait(4)

        cosf = MathTex(r"=\cos x", color=RED).next_to(rpt, DOWN)
        sinf = MathTex(r"=i\sin x", color=BLUE).next_to(ipt, DOWN)
        self.play(Write(cosf))
        self.wait(2)
        self.play(Write(sinf))
        self.wait(2)

        final_equation = MathTex(r"e^{ix}=\cos x + i \sin x", color=YELLOW).shift(2.5*DOWN)
        notation = Text("欧拉公式").next_to(final_equation, RIGHT)
        self.play(Write(final_equation))
        self.wait(2)
        self.play(Write(notation))
        self.wait(6)
