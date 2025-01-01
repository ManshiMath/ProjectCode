from manim import *
import numpy as np

class Fibonacci(Scene):
    def construct(self):
        recur = MathTex("F_n",r"=F_{n-1}+F_{n-2}", color=ORANGE).scale(1.5)
        self.play(Write(recur))
        self.wait(2)
        # _recur = recur.copy().scale(0.7).shift(2*UP)
        mat_form = MathTex(r"\begin{bmatrix} F_n \\ F_{n-1} \end{bmatrix} =",r" \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}",r"\begin{bmatrix} F_{n-1} \\ F_{n-2} \end{bmatrix}", 
                           color=BLUE).scale(1.2)
        mat_form[1].set_color(ORANGE)
        self.play(Transform(recur, mat_form), run_time=2)
        self.wait(2)
        _recur = recur.copy().shift(2*UP)
        self.play(Transform(recur, _recur), run_time=2)
        self.wait()
        opacity = ValueTracker(1)
        
        hl = SurroundingRectangle(recur[1], color=YELLOW, buff=0.1).add_updater(lambda m: m.set_stroke(opacity=opacity.get_value()))
        self.play(Create(hl))
        self.play(opacity.animate.set_value(0), rate_func=there_and_back, run_time=1)
        self.play(opacity.animate.set_value(0), rate_func=there_and_back, run_time=1)
        self.play(opacity.animate.set_value(0), run_time=0.5)
        self.wait(2)

        formula = MathTex(r"\begin{bmatrix} F_{n+1} \\ F_{n} \end{bmatrix} =",
                          r"A^n", r"\begin{bmatrix} F_1 \\ F_0 \end{bmatrix}", color=GOLD).scale(1.2).move_to(recur)
        self.play(ReplacementTransform(recur, formula), 
                  FadeOut(hl),
                  run_time=2)

        # calculate the eigenvalues of the matrix
        cal_eq = MathTex(r"\det\left(\begin{bmatrix} 1-\lambda & 1 \\ 1 & -\lambda \end{bmatrix}\right) = 0", color=GREEN).scale(1.2).next_to(recur, DOWN, buff=0.3)
        red_form = MathTex(r"\lambda^2 - \lambda - 1 = 0", color=ORANGE).scale(1.2).move_to(cal_eq)
        root = MathTex(r"\lambda = \frac{1\pm\sqrt{5}}{2}", color=BLUE).scale(1.2).next_to(red_form, DOWN, buff=0.3)
        self.play(Write(cal_eq))
        self.wait(2)
        self.play(ReplacementTransform(cal_eq, red_form), run_time=1.5)
        self.wait(2)
        self.play(Write(root), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(cal_eq), FadeOut(red_form), FadeOut(root), run_time=1.5)
        self.wait(1.5)

        # write the eigenvalue decomposition of the matrix in mat_form
        eig = MathTex(r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}= ", r"\begin{bmatrix} \phi & 1 \\ 1 & -\phi \end{bmatrix}", 
                      r"\begin{bmatrix} \phi & 0 \\ 0 & 1-\phi \end{bmatrix}", r"\begin{bmatrix} \phi & 1 \\ 1 & -\phi \end{bmatrix}^{-1}",
                        color=BLUE).scale(0.8).next_to(recur, DOWN, buff=0.7)
        self.play(Write(eig))
        self.wait(2)

        phi_tag = MathTex(r"\phi", r"=\frac{1+\sqrt{5}}{2}", color=GREEN).scale(0.8).next_to(eig, RIGHT, buff=1)
        self.play(Write(phi_tag))
        self.wait(2)

        PLPi = MathTex("A=", r"P", r"\Lambda", r"P^{-1}", color=ORANGE).scale(1.2).next_to(eig, DOWN, buff=0.5)
        for i in range(4):
            PLPi[i].next_to(eig[i], DOWN, buff=0.6)
            if i > 0:
                PLPi[i].align_to(PLPi[i-1], DOWN)
        self.play(Write(PLPi))
        self.wait(2)

        
        _eig = MathTex(r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}^n= ", r"\begin{bmatrix} \phi & 1 \\ 1 & -\phi \end{bmatrix}", 
                      r"\begin{bmatrix} \phi^n & 0 \\ 0 & (1-\phi)^n \end{bmatrix}", r"\begin{bmatrix} \phi & 1 \\ 1 & -\phi \end{bmatrix}^{-1}",
                        color=BLUE).scale(0.8).move_to(eig)
        self.wait(2)
        self.play(ReplacementTransform(eig, _eig), 
                  Transform(PLPi[0], MathTex(r"A^n=", color=ORANGE).scale(1.2).move_to(PLPi[0])),
                  Transform(PLPi[2], MathTex(r"\Lambda^n", color=ORANGE).scale(1.2).move_to(PLPi[2])),
                  run_time=2)
        self.wait(3)
        eq = MathTex("F_n",r"=\frac{1}{\sqrt{5}}\left[\left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n\right]",
                     color=BLUE).scale(1.5)

        eq[0].set_color(YELLOW)

        self.play(
            FadeOut(formula),
            FadeOut(phi_tag),
            PLPi.animate.shift(2*DOWN),
            ReplacementTransform(_eig, eq),
            run_time=2.5
        )
        self.wait(2)
        self.play(FadeOut(PLPi), run_time=1)
        self.wait(3)

class Intro(Scene):
    def construct(self):
    # 后来大卫希尔伯特，没错，就是提出现代数学纲领和希尔伯特旅馆的那个希尔伯特，
        hilbert = ImageMobject("hilbert.jpg").scale(0.6).shift(4*LEFT)
        name = Text("David Hilbert").next_to(hilbert, DOWN, buff=0.5)
        self.play(FadeIn(hilbert), Write(name))
        self.wait(2)
        # 第一次使用了eigenvalue这个名词，eigen这个德语词根的意思是“自己、自己的”，
        eigv = MathTex(r"\text{eigen}",r"\text{value}", color=GREEN).scale(2).next_to(hilbert, RIGHT, buff=1.5)
        self.play(Write(eigv))
        self.wait(2)
        self.play(eigv[0].animate.set_color(YELLOW), run_time=1)
        self.wait(2)
        rect = SurroundingRectangle(eigv[0], color=YELLOW, buff=0.1)
        mean = Text("自己的", font="heiti", color=ORANGE).scale(1.2).next_to(eigv[0], DOWN, buff=0.5)
        self.play(
            Create(rect),
            Write(mean), run_time=1)
        self.wait(2)
        # 所以这就是为什么特征值在其他学科，比如量子力学里往往也被称作本征值。
        benzheng = Text("本征值", color=GOLD, font="heiti").scale(1.5).next_to(eigv, UP, buff=1)
        self.play(
            Write(benzheng)
            )
        # 尽管知道了这些历史，好像还是不知道为什么叫特征值和特征向量。
        self.wait(2)
        # Fadeout everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        # 这里我给大家提供我自己的一个视角，可以把这些线索都串联起来，
        eig_eq = MathTex(r"A\vec{v} = \lambda \vec{v}", tex_to_color_map={"A": BLUE, r"\vec{v}": ORANGE, r"\lambda": YELLOW}).scale(4)
        self.play(Write(eig_eq))
        tezheng = Text("特征", color=YELLOW).scale(1.5).next_to(eig_eq, UP, buff=1)
        ques_mark = MathTex("?", color=RED).scale(5).move_to(eig_eq).set_stroke(width=2, background=True)
        self.play(Write(ques_mark), Write(tezheng), run_time=1)
        self.wait(3)
        # 那就是：特征值和特征向量刻画了一个矩阵是如何运作的， 
        answer = Text("特征值/向量刻画了矩阵变换空间的特征", color=RED).next_to(eig_eq, DOWN, buff=1.5)
        # 换言之，它描述了一个矩阵“变换整个空间的特征”。 
        self.play(Write(answer), run_time=2)
        self.wait(3)

class DeduceEig(Scene):
    def construct(self):
        mat = MathTex(r"A=\begin{bmatrix} a & b \\ c & d \end{bmatrix}", color=GOLD).scale(1.5).shift(2*UP)
        mat_lambda = MathTex(r"A - \lambda I = \begin{bmatrix} a-\lambda & b \\ c & d-\lambda \end{bmatrix}",
                             color=GOLD).scale(1.5).shift(2*UP)
        eq = MathTex(r"A\vec{v} = \lambda \vec{v}", 
                     tex_to_color_map={"A": BLUE, r"\vec{v}": ORANGE, r"\lambda": YELLOW}).scale(2).next_to(mat, DOWN, buff=1)

        eq_1 = MathTex(r"A\vec{v} - \lambda \vec{v} = \vec{0}", 
                      tex_to_color_map={"A": BLUE, r"\vec{v}": ORANGE, r"\lambda": YELLOW}).scale(2).next_to(mat, DOWN, buff=1)
        eq_2 = MathTex(r"(A - \lambda I)\vec{v} = \vec{0}", 
                      tex_to_color_map={"A": BLUE, r"\vec{v}": ORANGE, r"\lambda": YELLOW, "I": GREEN}).scale(2).next_to(mat, DOWN, buff=1)
        eq_3 = MathTex(r"\det(A - \lambda I) = 0", tex_to_color_map={"A": BLUE, r"\lambda": YELLOW, "I": GREEN}).scale(2).next_to(mat, DOWN, buff=1)
        self.play(Write(mat))
        self.wait(2)
        self.play(Write(eq))
        self.wait(2)
        self.play(ReplacementTransform(eq, eq_1))
        self.wait(2)
        self.play(ReplacementTransform(eq_1, eq_2))
        self.wait(2)
        self.play(ReplacementTransform(eq_2, eq_3))
        self.wait(2)
        
        self.play(ReplacementTransform(mat, mat_lambda))
        equation = MathTex(r"(a-\lambda)(d-\lambda) - bc = 0", 
                           tex_to_color_map={"A": BLUE, r"\lambda": YELLOW, "I": GREEN}).scale(1.2).next_to(mat_lambda, DOWN, buff=1)
        self.wait(2)
        self.play(ReplacementTransform(eq_3, equation))
        self.wait(2)
        # self.play(FadeOut(mat_lambda), equation.animate.shift(2*UP), run_time=1.5)
        self.wait(2)
        root = MathTex(r"\lambda^2 - (a+d)\lambda + (ad-bc) = 0", 
                        color=BLUE).scale(1.2).next_to(equation, DOWN, buff=0.5)
        self.play(Write(root))
        self.wait(2)
        mat_lambdai = MathTex(r"A - \lambda_1 I =",r"\begin{bmatrix} a-\lambda_1 & b \\ c & d-\lambda_1 \end{bmatrix}", 
                             color=GOLD).scale(1.5).shift(2*UP)
        self.play(ReplacementTransform(mat_lambda, mat_lambdai))
        self.wait(2)

        self.play(FadeOut(mat_lambdai[0]), mat_lambdai[1].animate.shift(3*LEFT), run_time=1.5)
        mult_eig_eq0 = MathTex(r"\vec{v}",r"= \vec{0}", tex_to_color_map={r"\vec{v}": ORANGE}).scale(2).next_to(mat_lambdai, RIGHT, buff=0.2)
        self.play(Write(mult_eig_eq0))
        self.wait(2)
        rect = SurroundingRectangle(mult_eig_eq0[0], color=YELLOW, buff=0.1)
        self.play(Create(rect))
        self.wait(3)
