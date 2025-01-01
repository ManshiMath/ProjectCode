import numpy as np
from manim import *

class Video0(Scene):
    def construct(self):
        # 然后物理学家就发现了K介子有两个双胞胎：theta粒子和tau粒子，
        theta_p = MathTex(r"\theta^+").set_color(WHITE).scale(2).shift(UP+LEFT*3)
        tau_p = MathTex(r"\tau^+").set_color(WHITE).scale(2).shift(DOWN+LEFT*3)
        self.play(Write(theta_p), Write(tau_p))
        # 这俩粒子的质量、电荷和寿命都在测量精度下完全一致，所以似乎是同一个粒子。
        self.wait(5)
        rect1 = SurroundingRectangle(theta_p, buff=0.1)
        rect2 = SurroundingRectangle(tau_p, buff=0.1)
        self.play(Create(rect1), Create(rect2))
        self.wait(3)
        self.play(FadeOut(rect1), FadeOut(rect2))
        self.wait(6)
        # 但是为什么还要起两个不同的名字呢？因为衰变的产物不一样。
        eq1 = MathTex(r"\to \pi^+ + \pi^0", tex_to_color_map={r"\pi^+": RED, r"\pi^0": BLUE}).scale(2).next_to(theta_p, RIGHT)
        eq2 = MathTex(r"\to \pi^+ + \pi^+ + \pi^-", tex_to_color_map={r"\pi^+": RED, r"\pi^-": GREEN, r"\pi^0": BLUE}).scale(2).next_to(tau_p, RIGHT)
        self.play(Write(eq1))
        self.wait(3.5)
        self.play(Write(eq2))
        self.wait(12)

        # 实验中，theta粒子会衰变出两个π介子，而tau则会衰变出三个。
        text = Text("宇称 Parity").scale(1.5).to_edge(UP)
        self.play(Write(text))
        self.wait(3)

class Video1(Scene):
    def construct(self):
        yu = Text("宇", font="heiti").scale(2).shift(LEFT*1.5).set_color(YELLOW)
        zhou = Text("宙").scale(2).shift(RIGHT*1.5).set_color(BLUE)
        self.play(Write(yu), Write(zhou))
        self.wait()

        rect1 = SurroundingRectangle(yu, buff=0.1)
        space = Text("空间").next_to(yu, DOWN)

        rect2 = SurroundingRectangle(zhou, buff=0.1)
        time = Text("时间").next_to(zhou, DOWN)

        # 宇称这个名字很抽象，宇宙这两个字分别对应于“空间”和“时间”，
        self.play(Create(rect1), Write(space))
        self.wait()
        self.play(Create(rect2), Write(time))
        self.wait()
        # 所以你可以大概把宇称理解为“空间的对称性”。
        self.play(FadeOut(rect1), FadeOut(rect2), FadeOut(space), FadeOut(time))
        chen = Text("称", font="heiti").scale(2).shift(RIGHT*1.5).set_color(YELLOW)
        self.wait(2)
        self.play(ReplacementTransform(zhou, chen))
        self.wait()
        sym = Text("空间的对称性").set_color(ORANGE).shift(UP*2)
        self.play(Write(sym))
        self.wait(2)
        # 我有一个简单的方法帮你理解宇称，对于一个函数f(x)，如果我们已经知道它要么是奇函数、要么是偶函数，
        title = Text("宇称").to_edge(UP).set_color(YELLOW)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN, buff=0.2)
        self.play(FadeOut(sym), Transform(VGroup(yu, chen), title), GrowFromCenter(line), run_time=1.5)
        self.wait(2)

        plane1 = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": WHITE, "stroke_width": 4},
            x_length=4,
            y_length=4
        ).shift(LEFT*3+DOWN*0.5)

        plane2 = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": WHITE, "stroke_width": 4},
            x_length=4,
            y_length=4
        ).shift(RIGHT*3+DOWN*0.5)

        self.play(FadeIn(plane1), FadeIn(plane2))
        self.wait(2)

        # 而且除了原点都不等于0，
        f1_graph = plane1.plot(lambda x: np.sin(x)*3, color=YELLOW)
        f2_graph = plane2.plot(lambda x: np.abs(x), color=YELLOW)
        f1_lbl = MathTex(r"f(x) = 3\sin(x)").scale(0.7).next_to(plane1, UP).set_color(ORANGE)
        f2_lbl = MathTex(r"f(x) = |x|").scale(0.7).next_to(plane2, UP).set_color(ORANGE)
        self.play(Create(f1_graph), Create(f2_graph), Write(f1_lbl), Write(f2_lbl), run_time=1.5)
        self.wait(2)
        
        f1_m1 = ValueTracker(-3*np.sin(1))
        f1_1 = ValueTracker(3*np.sin(1))
        f2_m1 = ValueTracker(1)
        f2_1 = ValueTracker(1)

        # f1_xeq1 = DashedLine(plane1.coords_to_point(1, -0), plane1.coords_to_point(1, 3*np.sin(1)), color=WHITE)
        f1_xeq1 = always_redraw(lambda: DashedLine(plane1.c2p(1, 0), plane1.c2p(1, f1_1.get_value()), color=WHITE))
        # f1_xeqm1 = DashedLine(plane1.coords_to_point(-1, 0), plane1.coords_to_point(-1, -3*np.sin(1)), color=WHITE)
        f1_xeqm1 = always_redraw(lambda: DashedLine(plane1.c2p(-1, 0), plane1.c2p(-1, f1_m1.get_value()), color=WHITE))
        # f2_xeq1 = DashedLine(plane2.coords_to_point(1, 0), plane2.coords_to_point(1, 1), color=WHITE)
        f2_xeq1 = always_redraw(lambda: DashedLine(plane2.c2p(1, 0), plane2.c2p(1, f2_1.get_value()), color=WHITE))
        # f2_xeqm1 = DashedLine(plane2.coords_to_point(-1, 0), plane2.coords_to_point(-1, 1), color=WHITE)
        f2_xeqm1 = always_redraw(lambda: DashedLine(plane2.c2p(-1, 0), plane2.c2p(-1, f2_m1.get_value()), color=WHITE))
        # f1_dot1 = Dot(plane1.coords_to_point(1, 3*np.sin(1)), color=RED)
        f1_dot1 = Dot(plane1.c2p(1, 0), color=RED).add_updater(lambda x: x.move_to(plane1.c2p(1, f1_1.get_value())))
        # f1_dot2 = Dot(plane1.coords_to_point(-1, -3*np.sin(1)), color=GREEN)
        f1_dot2 = Dot(plane1.c2p(-1, 0), color=GREEN).add_updater(lambda x: x.move_to(plane1.c2p(-1, f1_m1.get_value())))
        # f2_dot1 = Dot(plane2.coords_to_point(1, 1), color=RED)
        f2_dot1 = Dot(plane2.c2p(1, 0), color=RED).add_updater(lambda x: x.move_to(plane2.c2p(1, f2_1.get_value())))
        # f2_dot2 = Dot(plane2.coords_to_point(-1, 1), color=GREEN)
        f2_dot2 = Dot(plane2.c2p(-1, 0), color=GREEN).add_updater(lambda x: x.move_to(plane2.c2p(-1, f2_m1.get_value())))

        # 那么可以定义一个“函数宇称”，它等于f(1)/f(-1)。
        # self.play(LaggedStart(Create(f1_xeq1), Create(f1_xeqm1), Create(f2_xeq1), Create(f2_xeqm1), run_time=1.5))
        self.play(Create(f1_dot1), Create(f1_dot2), Create(f2_dot1), Create(f2_dot2))
        self.wait(2)
        # 如果这个函数是偶函数，分子分母相等，则它等于1，如果是奇函数就等于-1。
        f2_text = MathTex(r"\frac{f(1)}{f(-1)} = 1").next_to(f2_lbl, RIGHT).scale(0.8)
        f1_text = MathTex(r"\frac{f(1)}{f(-1)} = -1").next_to(f1_lbl, LEFT).scale(0.8)
        self.play(Write(f2_text))
        self.wait(3)
        self.play(Write(f1_text))
        self.wait(6)
        # 如果两个函数的函数宇称不一样，肯定不是同一个函数。而把两个函数乘在一起，
        rect1 = SurroundingRectangle(f1_text, buff=0.1)
        rect2 = SurroundingRectangle(f2_text, buff=0.1)
        self.play(Create(rect1), Create(rect2))
        self.wait()
        self.play(ApplyWave(f1_graph), ApplyWave(f2_graph), run_time=1.5)
        self.wait(3)
        # 函数宇称等于各自函数宇称的乘积。
        self.play(FadeOut(rect1), FadeOut(rect2), FadeOut(f1_text), FadeOut(f2_text))
        self.wait(3)

        # 两个奇函数相乘得到偶函数，正如-1乘以-1得到+1；
        new_f1 = plane1.plot(lambda x: 3*np.sin(x)*np.sin(x), color=YELLOW)
        new_f2 = plane2.plot(lambda x: x*np.abs(x)/2, color=YELLOW, x_range=[-3, 3])
        new_f1_lbl = MathTex(r"f(x) = 3\sin^2(x)").scale(0.7).next_to(plane1, UP).set_color(ORANGE)
        new_f2_lbl = MathTex(r"f(x) = x|x|/2").scale(0.7).next_to(plane2, UP).set_color(ORANGE)
        m1tm1 = MathTex(r"(-1) \times (-1) = 1").next_to(plane1, DOWN).set_color(GOLD)
        m1t1 = MathTex(r"-1 \times 1 = -1").next_to(plane2, DOWN).set_color(GOLD)
        self.play(
            Transform(f1_graph, new_f1),
            TransformMatchingShapes(f1_lbl, new_f1_lbl),
            f1_m1.animate.set_value(3*np.sin(1)*np.sin(1)),
            f1_1.animate.set_value(3*np.sin(1)*np.sin(1)),
            Write(m1tm1),
        )
        self.wait(2)
        # 奇函数乘以偶函数得奇函数，正如1乘-1得到-1。
        self.play(
            Transform(f2_graph, new_f2),
            TransformMatchingShapes(f2_lbl, new_f2_lbl),
            f2_m1.animate.set_value(-1/2),
            f2_1.animate.set_value(1/2),
            Write(m1t1),
        )
        self.wait(3)
        # 它衡量了一个函数和自己镜像对称的函数之间，是相等，还是差一个负号。

        big1 = MathTex(r"1").scale(2).set_color(YELLOW).move_to(plane1.c2p(0, -2)).set_stroke(width=4, background=True)
        bigm1 = MathTex(r"-1").scale(2).set_color(YELLOW).move_to(plane2.c2p(0, -2)).set_stroke(width=4, background=True)
        self.play(
            f1_graph.copy().animate.scale([-1, 1, 1]).set_color(BLUE),
            Write(big1),
            run_time=1
        )
        self.play(
            f2_graph.copy().animate.scale([-1, 1, 1]).set_color(BLUE),
            Write(bigm1),
            run_time=1
        )
        self.wait(2)

class Video2(Scene):
    def construct(self):
        theta_p = MathTex(r"\theta^+").set_color(WHITE).scale(2).shift(UP*1.5+LEFT*3)
        tau_p = MathTex(r"\tau^+").set_color(WHITE).scale(2).shift(DOWN*1.2+LEFT*3)
        eq1 = MathTex(r"\to \pi^+ + \pi^0", tex_to_color_map={r"\pi^+": RED, r"\pi^0": BLUE}).scale(2).next_to(theta_p, RIGHT)
        eq2 = MathTex(r"\to \pi^+ + \pi^+ + \pi^-", tex_to_color_map={r"\pi^+": RED, r"\pi^-": GREEN, r"\pi^0": BLUE}).scale(2).next_to(tau_p, RIGHT)
        self.play(Write(theta_p), Write(tau_p), Write(eq1), Write(eq2))
        self.wait(2)

        two_m1_mul = MathTex(r"(-1) \times (-1) = 1").next_to(eq1, UP).set_color(TEAL)
        three_m1_mul = MathTex(r"(-1) \times (-1) \times (-1) = -1").next_to(eq2, UP).set_color(TEAL)
        self.play(Write(two_m1_mul))
        self.wait(2)
        self.play(Write(three_m1_mul))
        self.wait(2)

class Video3(Scene):
    def construct(self):
        nline = NumberLine(x_range=[-10, 10, 1], include_tip=True, include_ticks=True)
        timelbl = Text("时间", color=RED).scale(0.6).to_edge(RIGHT).shift(DOWN*0.5)
        self.play(Create(nline), Write(timelbl))
        
        self.wait()
        img1 = ImageMobject("exp.png").scale(0.6).move_to(nline.n2p(-0.5)).shift(UP*2)
        today = Text("今天", color=YELLOW).scale(0.5).next_to(img1, DOWN, buff=0.8)
        self.play(FadeIn(img1), Write(today), run_time=0.6)
        self.wait(0.4)

        img2 = img1.copy().shift(RIGHT*2)
        tomorrow = Text("明天", color=YELLOW).scale(0.5).next_to(img2, DOWN, buff=0.8)
        self.play(TransformFromCopy(img1, img2),
                  Write(tomorrow), run_time=0.6)
        self.wait(0.4)

        img3 = img1.copy().shift(LEFT*4.5)
        tang = Text("唐朝", color=YELLOW).scale(0.5).next_to(img3, DOWN, buff=0.8)
        self.play(TransformFromCopy(img1, img3),
                  Write(tang), run_time=0.6)
        self.wait(0.4)

        img4 = img1.copy().shift(RIGHT*4.5)
        future = Text("2077", color=YELLOW).scale(0.5).next_to(img4, DOWN, buff=0.8)
        self.play(TransformFromCopy(img1, img4),
                   Write(future), run_time=0.6)
        self.wait(3)

        rect1 = SurroundingRectangle(img1, buff=0.1)
        rect2 = SurroundingRectangle(img2, buff=0.1)
        rect3 = SurroundingRectangle(img3, buff=0.1)
        rect4 = SurroundingRectangle(img4, buff=0.1)
        self.play(Create(rect1), Create(rect2), Create(rect3), Create(rect4))
        self.wait(2)

class Video4(Scene):
    def construct(self):
        y = ValueTracker(3)
        circ = Circle(radius=0.5, color=BLUE_B, fill_opacity=1).add_updater(lambda x: x.move_to(ORIGIN+UP*y.get_value()))
    
        self.play(Create(circ))
        self.wait(2)

        self.play(y.animate.set_value(-2), run_time=3, rate_func=rate_functions.ease_out_bounce)
        self.wait(2)

        f_formula = MathTex(r"f=\frac{GMm}{r^2}").set_color(YELLOW).to_edge(UP).shift(LEFT*3)
        small_G = MathTex(r"G=1").scale(1.2).set_color(GREEN).shift(LEFT*4+UP)
        big_G = MathTex(r"G=2").scale(1.2).set_color(RED).shift(RIGHT*4+UP)

        energy_consump = MathTex(r"E_1 =").set_color(ORANGE).next_to(small_G, DOWN, buff=0.5).align_to(small_G, LEFT)
        e1 = DecimalNumber(0, num_decimal_places=2).set_color(ORANGE).next_to(energy_consump, RIGHT).add_updater(lambda x: x.set_value(2+y.get_value()))
        self.play(Write(f_formula))
        self.wait(2)
        self.play(Write(energy_consump), Write(e1))
        self.wait()
        self.play(Write(small_G))
        self.play(y.animate.set_value(3), 
                  run_time=2)
        self.wait(4)

        energy_emit = MathTex(r"E_2 =").set_color(ORANGE).next_to(big_G, DOWN, buff=0.5).align_to(big_G, LEFT)
        # remove e1's updater
        e1.clear_updaters()
        e2 = DecimalNumber(0, num_decimal_places=2).set_color(ORANGE).next_to(energy_emit, RIGHT).add_updater(lambda x: x.set_value(6-2*y.get_value()))
        self.play(Write(energy_emit), Write(e2))
        self.play(Write(big_G))
        self.play(y.animate.set_value(-2), 
                  run_time=1.4,
                  rate_func=rate_functions.ease_out_bounce)
        self.wait(2)

        rect1 = SurroundingRectangle(VGroup(energy_consump, e1), buff=0.1)
        rect2 = SurroundingRectangle(VGroup(energy_emit, e2), buff=0.1)
        self.play(Create(rect1), Create(rect2))
        self.wait(2)

class Video5(Scene):
    def construct(self):
        mirrorline = DashedLine(UP*4, DOWN*4).set_color(ORANGE)
        self.play(Create(mirrorline))
        self.wait()

        left_part = Dot(LEFT*3, color=RED, radius=0.3)
        right_part = Dot(RIGHT*3, color=RED, radius=0.3)

        self.play(FadeIn(left_part), FadeIn(right_part))
        self.wait()

        l1 = Dot(LEFT*3+UP*1.5, color=RED, radius=0.2)
        l1_lbl = MathTex(r"\pi^+").next_to(l1, LEFT)
        l2 = Dot(LEFT*3+DOWN*1.5, color=GREEN, radius=0.2)
        l2_lbl = MathTex(r"\pi^0").next_to(l2, LEFT)
        l_prod = VGroup(l1, l2)

        r1 = Dot(RIGHT*3+UP*1.5, color=RED, radius=0.2)
        r1_lbl = MathTex(r"\pi^+").next_to(r1, RIGHT)
        r2 = Dot(RIGHT*3, color=RED, radius=0.2)
        r2_lbl = MathTex(r"\pi^+").next_to(r2, RIGHT)
        r3 = Dot(RIGHT*3+DOWN*1.5, color=BLUE, radius=0.2)
        r3_lbl = MathTex(r"\pi^-").next_to(r3, RIGHT)
        r_prod = VGroup(r1, r2, r3)

        self.play(
            Transform(left_part, l_prod),
            Transform(right_part, r_prod),
            run_time=1.5
        )
        self.play(
            Write(l1_lbl), Write(l2_lbl), Write(r1_lbl), Write(r2_lbl), Write(r3_lbl)
        )
        self.wait(2)

class Video6(Scene):
    def construct(self):
        sf = Text("强相互作用").shift(LEFT*3+UP*2)
        ef = Text("电磁相互作用").shift(LEFT*3)
        wf = Text("弱相互作用").shift(RIGHT*3 + UP*2)
        gr = Text("引力").shift(RIGHT*3)

        rect1 = SurroundingRectangle(sf, buff=0.1)
        rect2 = SurroundingRectangle(ef, buff=0.1)
        rect3 = SurroundingRectangle(gr, buff=0.1)
        self.play(Write(sf), Write(ef), Write(wf), Write(gr))
        self.wait(2)
        self.play(Create(rect1), Create(rect2), Create(rect3))
        self.wait(4)
        ques_mk = MathTex(r"?", color=RED).scale(4).set_stroke(width=5, background=True).move_to(wf)
        self.play(Write(ques_mk))
        self.wait(8)

        self.play(
            FadeOut(sf), FadeOut(ef), FadeOut(gr),
            FadeOut(rect1), FadeOut(rect2), FadeOut(rect3),
            wf.animate.move_to(ORIGIN).scale(2),
            ques_mk.animate.move_to(ORIGIN).scale(2),
            run_time=2
        )
        self.wait(2)
        nobdy = Text("没人严谨验证过！", font="heiti", color=BLUE).next_to(ques_mk, DOWN, buff=0.5).set_stroke(width=5, background=True)
        self.play(Write(nobdy))
        self.wait(5)

class Video7(Scene):
    def construct(self):
        arr = VGroup()
        arr.add(Arrow(LEFT*3, UP*2+LEFT*3, buff=0.3).set_color(RED))
        arr.add(Arrow(LEFT*3, DOWN*2+LEFT*3, buff=0.3).set_color(BLUE))
        lblup = MathTex(r"I_1").next_to(arr[0], UP).set_color(YELLOW)
        lbldown = MathTex(r"I_2").next_to(arr[1], DOWN).set_color(YELLOW)
        for _ in range(5):
        # 发射出的电子也就是俗称的beta射线，是有电流的。电流方向和原子自旋有关。
            elecs = VGroup(*[Dot(ORIGIN, color=BLUE, radius=0.06).shift(RIGHT*np.random.rand()*0.2) for _ in range(8)])
            self.play(FadeIn(elecs))
            self.play(
                *[elecs[i].animate.shift(UP*5+RIGHT*(i-0.5)*0.7) for i in range(2)],
                *[elecs[i].animate.shift(DOWN*5+RIGHT*(i-5)*0.7) for i in range(2, 8)],
                run_time=3, rate_func=linear
            )
            if _ < 1:
                self.play(Create(arr[0]), Create(arr[1]), Write(lblup), Write(lbldown))
                self.wait(2)
        # 我们关注自旋轴方向上下两个方向的射线电流强度，一个是I1一个是I2。
        # 接下来注意看，如果我们用外界磁场把这个原子的自旋颠倒过来，
        # 那么右边这个原子两个射线的电流应该是多大呢？
        # 有两种看待方式：如果我们是用旋转180度的方式，把左边颠倒过来，
        # 那么应该是往上是I2，往下是I1；
        # 而如果我们当成这两个原子是照镜子，那么应该往上是I1、往下是I2。
        # 宇宙的旋转对称已经验证是对的，所以第一个等式肯定成立。
        # 第二个等式成立则依赖于物理过程在镜像中保持对称，也就是宇称守恒。
        # 所以，如果宇称守恒，那么这两个等式就同时成立，
        # 我们因此可以预测上下两个电流I1和I2一定是一样的。
        # 而一旦我们可以观测到I1和I2有显著的差异，
        # 那么这个实验就证明了一件极其神秘的事：这个世界的宇称不守恒。

class Video7_up(Scene):
    def construct(self):
        arr = VGroup()
        arr.add(Arrow(LEFT*2, UP*2+LEFT*2, buff=0.2, stroke_width=6).set_color(RED))
        arr.add(Arrow(LEFT*2, DOWN*2+LEFT*2, buff=0.2, stroke_width=6).set_color(BLUE))
        lblup = MathTex(r"I_1").next_to(arr[0], UP).set_color(YELLOW)
        lbldown = MathTex(r"I_2").next_to(arr[1], DOWN).set_color(YELLOW)
        self.play(Create(arr[0]), Create(arr[1]), Write(lblup), Write(lbldown))
        for _ in range(5):
        # 发射出的电子也就是俗称的beta射线，是有电流的。电流方向和原子自旋有关。
            elecs = VGroup(*[Dot(ORIGIN, color=BLUE, radius=0.06).shift(RIGHT*np.random.rand()*0.2) for _ in range(8)])
            self.play(FadeIn(elecs))
            self.play(
                *[elecs[i].animate.shift(UP*5+RIGHT*(i-0.5)*0.7) for i in range(2)],
                *[elecs[i].animate.shift(DOWN*5+RIGHT*(i-5)*0.7) for i in range(2, 8)],
                run_time=3, rate_func=linear
            )
class Video7_down(Scene):
    def construct(self):
        arr = VGroup()
        arr.add(Arrow(LEFT*2, UP*2+LEFT*2, buff=0.2, stroke_width=6).set_color(BLUE))
        arr.add(Arrow(LEFT*2, DOWN*2+LEFT*2, buff=0.2, stroke_width=6).set_color(RED))
        lblup = MathTex(r"I_2").next_to(arr[0], UP).set_color(YELLOW)
        lbldown = MathTex(r"I_1").next_to(arr[1], DOWN).set_color(YELLOW)
        self.play(Create(arr[0]), Create(arr[1]), Write(lblup), Write(lbldown))
        for _ in range(5):
        # 发射出的电子也就是俗称的beta射线，是有电流的。电流方向和原子自旋有关。
            elecs = VGroup(*[Dot(ORIGIN, color=BLUE, radius=0.06).shift(RIGHT*np.random.rand()*0.2) for _ in range(8)])
            self.play(FadeIn(elecs))
            self.play(
                *[elecs[i].animate.shift(UP*5+RIGHT*(i-0.5)*0.7) for i in range(6)],
                *[elecs[i].animate.shift(DOWN*5+RIGHT*(i-5)*0.7) for i in range(6, 8)],
                run_time=3, rate_func=linear
            )

class Video8(Scene):
    def construct(self):
        arr = VGroup()
        arr.add(Arrow(LEFT*3, UP*2+LEFT*3, buff=0.3))
        arr.add(Arrow(LEFT*3, DOWN*2+LEFT*3, buff=0.3))
        lblup = MathTex(r"I=?").next_to(arr[0], UP).set_color(YELLOW)
        lbldown = MathTex(r"I=?").next_to(arr[1], DOWN).set_color(YELLOW)
        self.play(Create(arr[0]), Create(arr[1]), Write(lblup), Write(lbldown))
        self.wait(5)