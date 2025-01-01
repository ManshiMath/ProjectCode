from manim import *

class Start(Scene):
    def construct(self):
        text = Text("视频结构").set_color(ORANGE).scale(2)
        self.play(Write(text), run_time=1)
        self.wait(1)
        self.play(FadeOut(text), run_time=1)
        self.wait(1)

class P1(Scene):
    def construct(self):
        text = Text("第一章：经典力学").set_color(ORANGE).scale(1.5)
        self.play(Write(text), run_time=1)
        self.wait(1)
        self.play(FadeOut(text), run_time=1)
        self.wait(1)

class P2(Scene):
    def construct(self):
        text = Text("第二章：电磁学&万有引力").set_color(ORANGE).scale(1.5)
        self.play(Write(text), run_time=1)
        self.wait(1)
        self.play(FadeOut(text), run_time=1)
        self.wait(1)

class P3(Scene):
    def construct(self):
        text = Text("第三章：宇宙学&黑洞理论").set_color(ORANGE).scale(1.5)
        self.play(Write(text), run_time=1)
        self.wait(1)
        self.play(FadeOut(text), run_time=1)
        self.wait(1)

class section(Scene):
    def construct(self):
        l1 = Line(start=UP*1.5+LEFT*5, end=UP*1.5+LEFT*1.6, stroke_width=10, color=BLUE)
        l2 = Line(start=UP * 1.5 + LEFT * 1.4, end=UP * 1.5 + RIGHT * 1.4, stroke_width=10, color=GOLD)
        l3 = Line(start=UP * 1.5 + RIGHT * 1.6, end=UP * 1.5 + RIGHT * 5, stroke_width=10, color=RED)

        text1 = Text("经典力学").set_color(BLUE).next_to(l1, DOWN, buff=0.5)
        text2 = Text("电磁学").set_color(GOLD).scale(0.8).next_to(l2, DOWN, buff=0.5)
        text2_2 = Text("万有引力").set_color(GOLD).scale(0.8).next_to(text2, DOWN, buff=0.1)
        text3 = Text("宇宙学").set_color(RED).scale(0.8).next_to(l3, DOWN, buff=0.5)
        text3_2 = Text("黑洞理论").set_color(RED).scale(0.6).next_to(text3, DOWN, buff=0.1)

        self.play(LaggedStart(
            Create(l1),
            Create(l2),
            Create(l3),
        ), run_time=3, lag_ratio=0.5)

        self.wait(2)
        self.play(Write(text1), run_time=2)
        self.wait(2)
        self.play(Write(text2), Write(text2_2), run_time=2)
        self.wait(2)
        self.play(Write(text3), Write(text3_2), run_time=2)
        self.wait(2)

        rect = SurroundingRectangle(VGroup(l2, l3, text2, text2_2, text3, text3_2), buff=0.1)
        self.play(Create(rect), run_time=2)

        warning = Text("只是引路，想搞懂请看书").set_color(YELLOW).scale(1.5).shift(DOWN*2)
        self.play(Write(warning), run_time=2)
        self.wait(2)

class Parabola(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-0.5, 9.5, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.5,
            },
            x_length=8,
            y_length=8,
        )
        self.play(Create(plane), run_time=2)
        x = ValueTracker(0)
        para_curve = always_redraw(lambda: plane.plot(lambda x: 9-x**2, x_range=[0, x.get_value()], color=BLUE))
        dot = Dot(color=RED).add_updater(lambda m: m.move_to(plane.c2p(x.get_value(), 9-x.get_value()**2)))

        self.wait(2)
        self.play(Create(para_curve), Create(dot), run_time=2)
        self.wait()
        self.play(x.animate.set_value(3), run_time=2, rate_func=linear)
        self.wait(2)
        e1 = MathTex("x=v_0t").set_color(BLUE).scale(1.5).shift(UP+LEFT*4)
        e2 = MathTex("y=-\\frac{1}{2}gt^2").set_color(GREEN).next_to(e1, DOWN, buff=0.5)
        relation = MathTex("y=-\\frac{1}{2g}x^2").set_color(ORANGE).shift(DOWN*2).set_stroke(width=5, background=True)

        self.play(Write(e1), Write(e2), run_time=2)
        self.wait(2)
        self.play(Write(relation), run_time=2)
        self.wait(2)


class Cioujiju(Scene):
    def construct(self):
        eq = MathTex(r"\vec{m}=\frac{1}{2}\int (\vec{r} \times \vec{j}) d V").scale(2).set_color(ORANGE).shift(UP*2)
        self.play(Write(eq), run_time=2)
        label = Text("磁偶极矩").set_color(BLUE).scale(1.5).next_to(eq, DOWN, buff=0.5)
        force = MathTex(r"\vec{F}=\nabla (\vec{m} \cdot \vec{B})").scale(2).set_color(YELLOW).shift(DOWN*2)
        self.wait()
        self.play(Write(label), run_time=2)
        self.wait(2)
        self.play(Write(force), run_time=2)
        self.wait(2)

class BlackHole(Scene):
    def construct(self):
        singularity = Dot(color=WHITE).scale(0.5)
        zero_volu = MathTex(r"V=0", color=BLUE).shift(RIGHT*3+UP)
        eq = MathTex(r"\rho=\frac{M}{0}", color=GREEN).scale(0.8).shift(RIGHT*3)
        arr_to_singularity = Arrow(start=RIGHT*2+DOWN*2, end=ORIGIN, color=RED)
        label = Text("Singularity 奇点").set_color(GOLD).scale(0.8).next_to(arr_to_singularity.get_start(), DOWN, buff=0.1)

        mass = Text("质量 M").set_color(RED).scale(0.8).shift(LEFT*3+UP*2)
        ang_momentum = Text("角动量 L").set_color(BLUE).scale(0.8).next_to(mass, DOWN, buff=0.2)
        charge = Text("电荷 Q").set_color(GREEN).scale(0.8).next_to(ang_momentum, DOWN, buff=0.2)
        # no_surf = Text("表面").set_color(YELLOW).scale(0.8).next_to(charge, DOWN, buff=0.2)
        # # a red line cross the no_surf label showing that there is no surface
        # no_sign_1 = MathTex(r"\times").set_color(RED).scale(1.2).next_to(no_surf, RIGHT, buff=0.2)

        self.play(FadeIn(singularity), run_time=2)
        self.wait(2)
        self.play(Write(zero_volu), run_time=2)
        self.wait(2)
        self.play(Write(eq), run_time=2)
        self.wait(2)
        self.play(Create(arr_to_singularity), Write(label), run_time=2)
        self.wait(2)
        self.play(FadeOut(zero_volu), FadeOut(eq))
        self.play(
            LaggedStart(
                Write(mass),
                Write(ang_momentum),
                Write(charge),
            ), run_time=3, lag_ratio=0.3
        )
        self.wait(2)

class Classifi(Scene):
    def construct(self):
        # draw a table to show the classification of black hole
        tab = Table(
            [["史瓦西黑洞", "克尔黑洞"],
             ["RN黑洞", "克尔-纽曼黑洞"]],
            row_labels=[Text("无电荷", color=PURPLE_E), Text("有电荷", color=PURPLE_A)],
            col_labels=[Text("无自旋", color=GOLD_E), Text("有自旋", color=GOLD_A)],
        )
        tab.scale(0.8).shift(UP)
        self.play(Create(tab), run_time=2)
        self.wait(2)

        for i in range(2):
            for j in range(2):
                _tab = tab.add_highlighted_cell((i+2, j+2), color=YELLOW)
                self.play(Transform(tab, _tab), run_time=2)
                self.wait()

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)

class tideforce(Scene):
    def construct(self):
        # illustrate the tide force
        nplane = NumberPlane(
            x_range=[0, 5, 1],
            y_range=[0, 10, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.5,
            },
            x_length=8,
            y_length=8,
        ).shift(UP*2.5)

        gravity_func = lambda x: 1/x**2
        gravity_curve = nplane.plot(gravity_func, x_range=[0.1, 5], color=YELLOW, stroke_width=5)
        func_label = MathTex(r"F=\frac{G M m}{r^2}", color=GOLD).scale(1.2).shift(DOWN*3)
        x1 = ValueTracker(3)
        length = ValueTracker(0.5)
        vline1 = always_redraw(lambda: DashedLine(nplane.c2p(x1.get_value(), 0), nplane.c2p(x1.get_value(), gravity_func(x1.get_value())), color=RED))
        vline2 = always_redraw(lambda: DashedLine(nplane.c2p(x1.get_value()+length.get_value(), 0),
                                                   nplane.c2p(x1.get_value()+length.get_value(), gravity_func(x1.get_value()+length.get_value())), color=ORANGE))
        pt1 = always_redraw(lambda: Dot(nplane.c2p(x1.get_value(), gravity_func(x1.get_value())), color=RED))
        pt2 = always_redraw(lambda: Dot(nplane.c2p(x1.get_value()+length.get_value(), gravity_func(x1.get_value()+length.get_value())), color=ORANGE))
        lbl1 = always_redraw(lambda: MathTex("F_1").scale(0.8).next_to(pt1, UP+RIGHT, buff=0.1))
        lbl2 = always_redraw(lambda: MathTex("F_2").scale(0.8).next_to(pt2, UP+RIGHT, buff=0.1))

        self.play(Create(nplane), run_time=2)
        self.wait()
        self.play(Create(gravity_curve), run_time=2)
        self.play(Write(func_label), run_time=2)
        self.wait(2)
        self.play(LaggedStart(
            Create(vline1),
            Create(vline2),
            Create(pt1),
            Create(pt2),
        ), run_time=2)
        self.wait(2)
        self.play(LaggedStart(
            Write(lbl1),
            Write(lbl2),
        ), run_time=2)
        self.wait(2)    
        self.play(x1.animate.set_value(0.5), run_time=3)
        self.wait(2)
        self.play(x1.animate.set_value(3), run_time=1)
        self.wait(3)
        self.play(length.animate.set_value(1), x1.animate.set_value(0.32), run_time=3)
        self.wait(3)

class SpaceTime(Scene):
    def construct(self):
        right_arrow = Arrow(start=ORIGIN, end=RIGHT*4, color=RED, buff=0., stroke_width=10).shift(DOWN*2)
        up_arrow = Arrow(start=ORIGIN, end=UP*4, color=BLUE, buff=0., stroke_width=10).shift(DOWN*2)
        right_lbl = Text("时间",color=RED).next_to(right_arrow, RIGHT, buff=0.1)
        up_lbl = Text("空间", color=BLUE).next_to(up_arrow, UP+LEFT, buff=0.1)
        self.play(Create(right_arrow), Create(up_arrow), run_time=2)
        self.play(Write(right_lbl), Write(up_lbl), run_time=2)
        self.wait(10)