from manim import *
import numpy as np


class Intro(Scene):
    def construct(self):
        # 我们都知道，正比例函数的解析式是y=kx，初中老师告诉我们，它的图像是一条直线。
        plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            })
        self.play(Create(plane))
        self.wait(2)

        k = ValueTracker(0.7)
        func_graph = always_redraw(
            lambda: plane.plot(lambda x: k.get_value() * x, x_range=[-10, 10], color=BLUE, stroke_width=8))
        label = MathTex("y=kx").set_color(ORANGE).set_stroke(background=True, width=5).shift(RIGHT + UP * 2)
        self.play(Create(func_graph))
        self.play(Write(label))
        self.wait(2)
        # 可让我问你一个有些奇怪的问题：除了看起来的确是直的，怎么严谨地去说明它是一条直线呢？
        self.play(k.animate.set_value(-1), run_time=1.5)
        self.wait(0.2)
        self.play(k.animate.set_value(0.5), run_time=2)
        self.wait()
        # 到了高中学习了向量我们知道，因为这条直线上所有的点都可以记为(x, kx)，
        x = ValueTracker(2.5)
        pt = always_redraw(lambda: Dot(color=RED).move_to(plane.c2p(x.get_value(), k.get_value() * x.get_value())))
        pt_label = always_redraw(
            lambda: MathTex(f'({x.get_value():.2f}, {x.get_value():.2f}k)').scale(0.8).set_color(YELLOW).set_stroke(
                background=True, width=5).next_to(pt, DOWN))
        self.play(Create(pt), run_time=0.5)
        self.add(pt_label)
        self.wait()
        self.play(x.animate.set_value(-1), run_time=2)
        self.wait(2)
        # 它总可以写成x(1,k)，因此平行于一个固定的向量(1,k)，
        vec_len = ValueTracker(1)
        arr = always_redraw(
            lambda: Arrow(plane.c2p(0, 0), plane.c2p(vec_len.get_value(), vec_len.get_value() * k.get_value()),
                          buff=0., color=GREEN, stroke_width=10)
        )
        arr_label = MathTex(r"(1, k)\times").set_color(BLUE).set_stroke(background=True, width=5).shift(RIGHT)
        x_value = always_redraw(
            lambda: MathTex(f'{vec_len.get_value():.2f}').scale(0.8).set_color(YELLOW).set_stroke(background=True,
                                                                                                  width=5).next_to(
                arr_label, RIGHT))
        self.play(Create(arr), Write(arr_label))
        self.play(Write(x_value))
        # 所以y=kx的图像是一条直线。
        # Show that the function graph is a line
        self.wait(2)
        self.play(ApplyWave(func_graph))
        self.wait(2)
        # 其实我们应该反过来说，不是因为平行于同一个向量所以是直线，
        self.play(FadeOut(pt), FadeOut(pt_label))
        self.wait()
        # 而是直线的定义就是“任意缩放同一个向量”得到的全部点的集合。
        self.play(vec_len.animate.set_value(5), run_time=2, rate_func=smooth)
        self.play(vec_len.animate.set_value(-3), run_time=2, rate_func=smooth)
        self.wait(2)
        # 所以，如果要表示一个三维空间中的直线，
        # 那么只需要把这个二维向量改成一个三维向量(1,1,2)，
        # 然后让缩放的倍数k取遍所有的实数，就可以用kv表示出这条直线了。


class ZeroSpace(Scene):
    def construct(self):
        # camera = self.camera.frame
        ratio = 0.6
        offset_x = 10 * ratio * RIGHT
        offset_y = 4 * ratio * UP
        offset = offset_x + offset_y
        # camera.shift(offset)
        left, right, up, down = 70 * ratio * LEFT, 70 * ratio * RIGHT, 40 * ratio * DOWN, 40 * ratio * UP
        axis_x, axis_y = Line(up, down), Line(left, right)
        lines_h = VGroup(*[Line(left + i * ratio * UP, right + i * ratio * UP, stroke_width=2, color=BLUE_E) for i in
                           range(-40, 41)])
        lines_v = VGroup(*[Line(up + i * ratio * RIGHT, down + i * ratio * RIGHT, stroke_width=2, color=BLUE_E) for i in
                           range(-70, 71)])
        points = [Dot((i - 8) * ratio * UP + (j - 20) * ratio * RIGHT, radius=0.06, color=GREY) for i in range(16) for j
                  in range(40)]
        grid = VGroup(lines_h, lines_v)
        arrows = Arrow(ORIGIN, ratio * UP, color=GREEN, buff=0), Arrow(ORIGIN, ratio * RIGHT, color=GREY, buff=0)
        background = VGroup(lines_h.copy().set_stroke(GREY, width=1), lines_v.copy().set_stroke(GREY, width=1),
                            axis_x.copy(), axis_y.copy())
        self.play(FadeIn(grid), Create(axis_x), Create(axis_y), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
        self.wait(2)
        self.bring_to_back(background).add(*points, *arrows).play(*[GrowFromCenter(mob) for mob in points])

        matrix_mark = MathTex(r"\begin{bmatrix} 2 & 2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x\\y \end{bmatrix}",
                              color=BLUE).add_background_rectangle().scale(0.8).shift(3 * ratio * UP + 8 * ratio * LEFT)
        self.play(Write(matrix_mark))

        self.wait()
        self.play(*[mob.save_state().animate.apply_matrix(np.array([[2, 2], [1, 1]])) for mob in [grid, *arrows]],
                  *[mob.save_state().animate.move_to(
                      np.dot(np.array([[2, 2, 0], [1, 1, 0], [0, 0, 0]]), mob.get_center())) for mob in points],
                  run_time=4)
        self.wait(2)

        # example = Dot(5*ratio*UP + 7*ratio*RIGHT)
        example = Dot(0 * UP + 0 * RIGHT)
        color_list = [MAROON, RED, ORANGE, YELLOW, TEAL, PURPLE]
        zs = Line(LEFT * 10 + UP * 10, RIGHT * 10 + DOWN * 10, stroke_width=4, color=ORANGE)
        zs_list = [zs.copy().set_color(color_list[i + 2]).shift(UP * ratio * i) for i in range(-2, 4)]

        # self.play(Write(x_mark), Write(y_mark))
        self.wait(2)

        example_dots = [Dot(i * ratio * UP + (-i) * ratio * RIGHT, color=ORANGE) for i in range(-9, 9)]
        for dot in example_dots:
            dot.save_state().move_to(np.dot(np.array([[2, 2, 0], [1, 1, 0], [0, 0, 0]]), dot.get_center()))
        zs.save_state().apply_matrix(np.array([[2, 2], [1, 1]]))
        self.play(Create(example_dots[0]), Create(zs))
        self.wait(2)
        self.play(Indicate(example_dots[0]))
        self.wait(2)
        # self.play(FadeOut(x_mark), FadeOut(y_mark))
        # self.wait()

        self.play(*[mob.animate.restore() for mob in [grid, zs, *arrows] + points + example_dots], run_time=4)
        self.wait(2)

        func_lbl = MathTex("y=-x", color=ORANGE).scale(0.8).shift(1.5 * ratio * LEFT + 3.5 * ratio * UP)
        _func_lbl = MathTex(r"k\begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=ORANGE).scale(0.8).move_to(func_lbl)
        self.play(Write(func_lbl))
        self.wait()
        self.play(Transform(func_lbl, _func_lbl), run_time=2)
        self.wait()

        equ = MathTex(
            r"\begin{bmatrix} 2 & 2 \\ 1 & 1 \end{bmatrix}\cdot k \begin{bmatrix} 1 \\ -1 \end{bmatrix}=\begin{bmatrix} 0 \\ 0 \end{bmatrix}",
            color=YELLOW).add_background_rectangle().shift(DOWN * 2)

        self.play(*[mob.save_state().animate.apply_matrix(np.array([[2, 2], [1, 1]])) for mob in [grid, *arrows, zs]],
                  *[mob.save_state().animate.move_to(
                      np.dot(np.array([[2, 2, 0], [1, 1, 0], [0, 0, 0]]), mob.get_center())) for mob in
                    points + example_dots], run_time=4)
        self.wait()
        self.play(DrawBorderThenFill(equ), run_time=2)
        self.wait(2)

        rect = SurroundingRectangle(func_lbl)
        mark = Text("零空间", color=YELLOW).add_background_rectangle().next_to(rect, RIGHT, buff=0.2)
        self.play(Create(rect))
        self.play(Write(mark))
        self.wait(2)
        self.play(FadeOut(rect), FadeOut(mark), FadeOut(equ), FadeOut(func_lbl))

        initial_points = [Dot(i * ratio * UP + 2 * i * ratio * RIGHT, color=ORANGE).set_color(color_list[i + 2]) for i
                          in range(-2, 4)]
        self.play(*[Create(dot) for dot in initial_points])
        self.wait()
        self.play(*[Indicate(dot) for dot in initial_points])

        self.wait()
        self.play(*[mob.animate.restore() for mob in [grid, zs, *arrows] + points + example_dots],
                  *[ReplacementTransform(initial_points[i], zs_list[i]) for i in range(6)],
                  run_time=4)
        self.wait(2)


class Elim(Scene):
    def construct(self):
        color_list = [MAROON, RED, ORANGE, YELLOW, TEAL, PURPLE]
        arr_list = [
            Arrow(ORIGIN, RIGHT * 2 * np.cos(i * np.pi / 3) + UP * 2 * np.sin(i * np.pi / 3), color=color_list[i],
                  buff=0) for i in range(6)]

        elim_order = [0, 2, 3, 4]
        self.play(LaggedStart(
            *[Create(arr) for arr in arr_list],
            lag_ratio=0.5
        ))
        self.wait(2)

        eq = VGroup(arr_list[0].copy().scale(0.4).move_to(ORIGIN + UP * 3 + LEFT * 5))
        for i in range(1, 6):
            eq.add(MathTex("+").next_to(eq[-1], RIGHT, buff=0.2))
            eq.add(arr_list[i].copy().scale(0.4).next_to(eq[-1], RIGHT, buff=0.2))

        eq.add(MathTex(r"= \vec{0}", color=YELLOW).next_to(eq[-1], RIGHT, buff=0.2))

        linear_depen = Text("线性相关", color=YELLOW).scale(2).shift(DOWN * 3)

        self.play(Write(eq), Write(linear_depen))
        self.wait(2)
        self.play(FadeOut(eq), FadeOut(linear_depen))
        self.wait()

        for i in elim_order:
            self.play(FadeOut(arr_list[i]), run_time=0.5)
            self.wait(0.5)
        self.wait(2)

        basis_text = Text("基底", color=YELLOW).shift(RIGHT * 4)
        dim = Text("维度=2", color=GREEN).shift(LEFT * 4)
        linear_indepen = Text("线性无关", color=YELLOW).scale(2).shift(DOWN * 3)
        rect = SurroundingRectangle(VGroup(*arr_list))
        self.play(Create(rect), Write(linear_indepen))
        self.wait(2)
        self.play(FadeOut(rect), Write(basis_text))
        self.wait(4)
        self.play(Write(dim))
        self.wait(2)


class ded(Scene):
    def construct(self):
        rec = MathTex("a_n=3a_{n-1}+a_{n-2}-3a_{n-3}", color=BLUE).shift(UP * 3)
        equ = MathTex("q^n=3q^{n-1}+q^{n-2}-3q^{n-3}", color=YELLOW)
        _equ = MathTex("q^3=3q^2+q-3", color=YELLOW)

        solution = MathTex(r"q_1=1,\quad q_2=-1,\quad q_3=3", color=GREEN).shift(DOWN)
        series = MathTex(r"a_n=A+B(-1)^n+C\times 3^n", color=ORANGE).shift(DOWN * 2)

        self.play(Write(rec))
        self.wait(2)
        self.play(Write(equ))
        self.wait()
        self.play(Transform(equ, _equ))
        self.wait(2)
        self.play(Write(solution))
        self.wait()
        self.play(Write(series))
        self.wait(3)


class formula(Scene):
    def construct(self):
        formula_l = MathTex("x", "Cu", r"=\!=\!=", "y", "Au").scale(0.8).shift(2 * UP + 3 * LEFT)
        formula_l[0].set_color(GREEN)
        formula_l[3].set_color(GREEN)
        formula_l[1].set_color(YELLOW)
        formula_l[4].set_color(YELLOW)

        # formula_l[:3].shift(0.3*LEFT)
        # formula_l[4:].shift(0.3*RIGHT)
        # formula_l[3].set_width(formula_l[3].get_width() + 0.6, stretch = True)
        texts = r"\begin{bmatrix}1&0\\0&-1\end{bmatrix}", r"\begin{bmatrix}x\\y\end{bmatrix}", r"=\begin{bmatrix}0\\0\end{bmatrix}"
        matrix_l = MathTex(
            r"\begin{bmatrix}1&0\\0&-1\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix}",
            color=BLUE).scale(0.8).shift(0.5 * DOWN + 3 * LEFT)
        self.play(Write(formula_l))
        self.wait()
        self.play(FadeIn(matrix_l))
        self.wait()

        formula_r = MathTex("x", "CO", r"=\!=\!=", "y", "CO_2").scale(0.8).shift(2 * UP + 3 * RIGHT)
        formula_r[0].set_color(GREEN)
        formula_r[3].set_color(GREEN)
        formula_r[1].set_color(YELLOW)
        formula_r[4].set_color(YELLOW)

        # formula_r[:3].shift(0.3*LEFT)
        # formula_r[4:].shift(0.3*RIGHT)
        # formula_r[3].set_width(formula_r[3].get_width() + 0.6, stretch = True)
        texts = r"\begin{bmatrix}1&0\\0&-2\end{bmatrix}", r"\begin{bmatrix}x\\y\end{bmatrix}", r"=\begin{bmatrix}0\\0\end{bmatrix}"
        matrix_r = MathTex(
            r"\begin{bmatrix}1&-1\\1&-2\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix}",
            color=GOLD).scale(0.8).shift(0.5 * DOWN + 3 * RIGHT)
        self.play(Write(formula_r))
        self.wait()
        self.play(FadeIn(matrix_r))
        self.wait()


class Det(Scene):
    def construct(self):
        A = MathTex("A",
                    r"=\begin{bmatrix}a_{11}&a_{12}&\cdots&a_{1n}\\a_{21}&a_{22}&\cdots&a_{2n}\\\vdots&\vdots&\ddots&\vdots\\a_{n1}&a_{n2}&\cdots&a_{nn}\end{bmatrix}",
                    color=BLUE).shift(2 * UP)
        A[0].set_color(GREEN)
        det_formula = MathTex(r"\det(A)=", r"\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^na_{i\sigma(i)}",
                              color=ORANGE).next_to(A, DOWN, buff=0.5)
        self.play(Write(A), run_time=1)
        self.wait(0.5)
        self.play(Write(det_formula), run_time=2)
        self.wait(2)

        rect = SurroundingRectangle(det_formula[1])
        self.play(Create(rect))
        self.wait(3)
        question_mark = MathTex("?", color=RED).scale(8).set_stroke(background=True, width=10).move_to(rect)
        self.play(Write(question_mark))
        self.wait(2)

        vol_text = Text("?体积", color=RED).scale(2).next_to(question_mark, DOWN, buff=0.5)
        self.play(Write(vol_text))
        self.wait(2)


class DetProd(Scene):
    def construct(self):
        nplane = NumberPlane(
            background_line_style={
                "stroke_color": BLUE_B,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            },
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
        )
        self.play(Create(nplane))
        self.wait(2)
        A = np.array([[1, -1], [1, 2]])
        B = np.array([[0.5, 1], [-1, 1]])
        AB = np.dot(A, B)

        A_lbl = MathTex(r"A=\begin{bmatrix}1&-1\\1&2\end{bmatrix}", color=BLUE).scale(0.8).add_background_rectangle().shift(
            3 * UP + 3 * LEFT)
        B_lbl = MathTex(r"B=\begin{bmatrix}0.5&1\\-1&1\end{bmatrix}", color=GREEN).scale(0.8).add_background_rectangle().next_to(
            A_lbl, DOWN, buff=0.5)

        curr_tsfm = MathTex("A", "B", r"=\!=\!=", "AB").scale(0.8).shift(2* DOWN)

        unit_sq = Polygon(nplane.c2p(0, 0), nplane.c2p(1, 0), nplane.c2p(1, 1), nplane.c2p(0, 1),
                          color=GOLD, fill_opacity=0.5)
        # Apply matrix to plane
        self.play(Create(unit_sq))
        self.wait()
        _nplane = nplane.copy().apply_matrix(B)
        _unit_sq = unit_sq.copy().apply_matrix(B)
        self.play(Transform(nplane, _nplane), Transform(unit_sq, _unit_sq),
                  Write(B_lbl), Write(curr_tsfm[1]), run_time=2)
        self.wait(2)

        _nplane = nplane.copy().apply_matrix(A)
        _unit_sq = unit_sq.copy().apply_matrix(A)
        self.play(Transform(nplane, _nplane), Transform(unit_sq, _unit_sq),
                  Write(A_lbl), Write(curr_tsfm[0]), run_time=2)
        self.wait(2)

class NegArea(Scene):
    def construct(self):
        # Define a number plane, draw a parallel with negative signed area
        nplane = NumberPlane(
            background_line_style={
                "stroke_color": BLUE_B,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            },
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
        )
        self.play(LaggedStart(Create(nplane), lag_ratio=0.5))
        self.wait()
        shape = Polygon(nplane.c2p(0, 0), nplane.c2p(1, 2), nplane.c2p(4, 1), nplane.c2p(3, -1))
        vec1 = Arrow(nplane.c2p(0, 0), nplane.c2p(1, 2), buff=0, color=GREEN)
        vec2 = Arrow(nplane.c2p(0, 0), nplane.c2p(3, -1), buff=0, color=YELLOW)
        self.play(LaggedStart(Create(vec1),
                              Create(vec2),
                              Create(shape),
                              lag_ratio=0.5), run_time=2)
        self.wait(2)
        # Show the area of the parallelogram
        area = MathTex(r"S=-7", color=ORANGE).shift(DOWN)
        question_mark = MathTex("?", color=RED).scale(8).set_stroke(background=True, width=10).move_to(area)

        self.play(Write(area))
        self.wait()
        self.play(Write(question_mark))
        self.wait(8)

class Prelude(Scene):
    def construct(self):
        self.wait(4)
        text = Text("这，是我们梦开始的地方", font="黑体", color=ORANGE).scale(1.2)
        self.play(FadeIn(text), run_time=1)
        self.wait(2)
        self.play(FadeOut(text), run_time=1)
        self.wait()

        tg = Tex("M", "athematic", "S").scale(2.5)
        tg[0].set_color(BLUE)
        #tg[1].set_color(GREEN)
        tg[2].set_color(MAROON_A)
        self.play(
            DrawBorderThenFill(tg),
            run_time=1
        )

        name = Text("漫士沉思录", color=YELLOW).scale(1.8).shift(DOWN*0.5)
        self.play(
            FadeOut(tg[1]),
            tg[0].animate.shift(RIGHT * 3+UP*2),
            tg[2].animate.shift(LEFT * 3+UP*1.8),
            DrawBorderThenFill(name),
            run_time=1,
            lag_ratio=0.7
        )
 
        self.wait()
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        self.wait(4)

        grate = Text("感谢你一路以来的支持",  color=BLUE).scale(2).shift(UP)
        self.play(
            FadeIn(grate),
            run_time=1
        )
        self.wait(2)
        self.play(
            FadeOut(grate),
            run_time=1
        )
        self.wait()

        hard_work = Text("每期视频平均工作量50小时", color=ORANGE).scale(1.2).shift(UP)
        self.play(
            Write(hard_work),
            run_time=1
        )
        self.wait()
        jstfyou = Text("只是为了告诉大家", color=MAROON).scale(1.2).next_to(hard_work, DOWN, buff=0.2)
        self.play(
            Write(jstfyou),
            run_time=1
        )
        self.wait()
        self.play(FadeOut(hard_work), FadeOut(jstfyou), run_time=1)

        mathisfun = Text("科学，真的可以很有趣", color=ORANGE).scale(1).shift(UP)
        self.play(
            Write(mathisfun),
            run_time=1
        )
        self.wait(2)
        self.play(
            FadeOut(mathisfun),
            run_time=1
        )


        tg = Tex("M", "athematic", "S").scale(2.5)
        tg[0].set_color(BLUE)
        #tg[1].set_color(GREEN)
        tg[2].set_color(MAROON_A)
        self.play(
            DrawBorderThenFill(tg),
            run_time=1
        )

        name = Text("漫士沉思录", color=YELLOW).scale(1.8).shift(DOWN*0.5)
        self.play(
            FadeOut(tg[1]),
            tg[0].animate.shift(RIGHT * 3+UP*2),
            tg[2].animate.shift(LEFT * 3+UP*1.8),
            DrawBorderThenFill(name),
            run_time=1.5,
            lag_ratio=0.7
        )
        text2 = Text("科普，永不停歇", font="黑体", color=ORANGE).scale(1.2).next_to(name, DOWN, buff=0.5)
        self.play(
            Write(text2),
            run_time=1
        )
        self.wait(3)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )