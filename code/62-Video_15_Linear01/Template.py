from __future__ import annotations

from manimlib import *
import numpy as np

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

#################################################################### 

class Digit(VGroup):
    def __init__(self, digit: int = 0, **kwargs):
        
        colors = [GREY, RED, GREEN, BLUE, ORANGE, GOLD, PURPLE_B, MAROON_B, PINK, TEAL]
        number = MTex(str(digit))
        square = Square(side_length = 0.45, fill_opacity = 0.3)
        super().__init__(square, number, **kwargs)
        self.set_color(colors[digit])
        self.digit = digit

    # def __str__(self):
    #     return str(self.digit)

class Flip(Animation):
    CONFIG = {
        "dim": 0,
        "color_interpolate": False
    }

    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject | None = None,
        **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.target_mobject = target_mobject
    
    def interpolate_mobject(self, alpha: float) -> None:
        if alpha <= 0.5:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 1-2*alpha
            self.mobject.become(self.starting_mobject).scale(vector, min_scale_factor = 0)
        else:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 2*alpha-1
            self.mobject.become(self.target_mobject).scale(vector, min_scale_factor = 0)
        if self.color_interpolate:
            self.mobject.set_color(interpolate_color(self.starting_mobject.get_color(), self.target_mobject.get_color(), alpha))
        return self
    
#################################################################### 

class Video_0(FrameScene):
    def construct(self):

        ##  Making object
        quote = Text("如果世界的变化是线性的，\n两倍的今天减去昨天，就能预知明天的一切，\n那该是多么美妙和枯燥啊。", font = 'simsun', t2c={"线性": GREEN, ("今天", "昨天", "明天"): BLUE, ("美妙", "枯燥"): YELLOW})
        author = Text("-Tarski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DR), DL)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author))
        self.wait()
        self.play(FadeOut(quote), FadeOut(author))
        self.wait()

class Patch0_1(FrameScene):
    def construct(self):

        ##  Making object
        texts = [r"\begin{vmatrix}a_{11}&a_{12}&\cdots&a_{1n}\\a_{21}&a_{22}&\cdots&a_{2n}\\\vdots&\vdots&\ddots&\vdots\\a_{n1}&a_{n2}&\cdots&a_{nn}\end{vmatrix}"
                , r"=a_{i1}A_{i1}+a_{i2}A_{i2}+\cdots+a_{in}A_{in}"]
        det = MTex(texts[0]+texts[1], isolate = texts)
        part_0, part_1 = det.get_part_by_tex(texts[0]).save_state().set_x(0), det.get_part_by_tex(texts[1])
        self.play(FadeIn(part_0))
        self.wait()
        self.play(part_0.animate.restore())
        self.play(Write(part_1), rate_func = rush_from)
        self.wait()

class Notices(NoticeScene):
    CONFIG = {
        "extra_frames": False,
    }
    def construct(self):
        self.notices = [Notice("塔斯基·硕德", "请勿模仿"), 
                        Notice("视频前言", "请听介绍"),
                        Notice("简单规律", "请　熟练"),
                        Notice("吓人公式", "请　忽略"),
                        Notice("重要概念", "请记笔记"),
                        Notice("OZO", "ULU"),
                        Notice("简单例子", "请　理解"),
                        Notice("重要概念", "请记笔记"),
                        Notice("简单情景", "请　舒适"),
                        Notice("简单例子", "请　验证"),
                        Notice("小学奥数", "请　复习"),
                        Notice("初中数学", "请　复习"),
                        Notice("线性映射", "经典例题"),
                        Notice("一次方程组", "请　求解")]
        self.notice = self.notices[0]
        self.play(Write(self.notice))
        self.wait(1)
        for i in range(1, len(self.notices)):
            self.play(Transform(self.notice, self.notices[i]))
            self.wait(1)
        self.play(FadeOut(self.notice))
        self.wait(1)

class Video_1(FrameScene):
    def construct(self):
        title = Text("线性代数", font = "FZShuSong-Z01S").scale(2)
        for i in range(4):
            title[i].shift((i-1.5)*0.2*RIGHT)
        left = title[0:2]
        right = title[2:]
        self.play(Write(title))
        self.wait()
        self.play(left.animate.scale(1.5).set_color(YELLOW).shift(LEFT), right.animate.scale(0.75).set_fill(opacity = 0.5))
        self.wait()
        self.play(right.animate.scale(2).set_fill(color = YELLOW, opacity = 1).shift(RIGHT), left.animate.scale(2/3).set_fill(color = WHITE, opacity = 0.5))
        self.wait()

        title = Title("代数")
        for i in range(2):
            title[i].shift((i-0.5)*0.1*RIGHT)
        title_line = TitleLine()
        self.play(FadeOut(left), ReplacementTransform(right, title))
        self.play(GrowFromCenter(title_line))
        self.wait()

        def commutative(int_1: int, int_2: int):
            mobs = [Digit(int_1), MTex(r"+")[0], Digit(int_2), MTex(r"=")[0], Digit(int_2), MTex(r"+")[0], Digit(int_1)]
            return VGroup(*[mobs[i].shift((i-3)*0.6*RIGHT) for i in range(7)])
        def distributive(int_1: int, int_2: int, int_3: int):
            mobs = [Digit(int_1), MTex(r"\times")[0], MTex(r"(")[0], Digit(int_2), MTex(r"+")[0], Digit(int_3), MTex(r")")[0], MTex(r"=")[0], Digit(int_1), MTex(r"\times")[0], Digit(int_2), MTex(r"+")[0], Digit(int_1), MTex(r"\times")[0], Digit(int_3)]
            positions = [-6.5, -5.5, -5, -4.25, -3.25, -2.25, -1.5, -1, 0, 1, 2, 3, 4, 5, 6]
            return VGroup(*[mobs[i].shift(positions[i]*0.6*RIGHT) for i in range(15)])
        
        equation_1 = commutative(3, 5).shift(2.5*LEFT + UP)
        equation_2 = distributive(3, 5, 7).shift(1.5*RIGHT + DOWN)

        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in equation_1], lag_ratio = 0.1, run_time = 1))
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.5*UP) for mob in equation_2], lag_ratio = 0.05, run_time = 1))
        self.wait()

        equation_3 = commutative(4, 6).shift(2.5*LEFT + UP)
        equation_4 = distributive(4, 6, 2).shift(1.5*RIGHT + DOWN)
        self.play(LaggedStart(AnimationGroup(*[Flip(equation_1[i], equation_3[i]) for i in [0, 6]]), AnimationGroup(*[Flip(equation_1[i], equation_3[i]) for i in [2, 4]]), run_time = 1.5, lag_ratio = 0.5))
        self.wait()
        self.play(LaggedStart(AnimationGroup(*[Flip(equation_2[i], equation_4[i]) for i in [0, 8, 12]]), AnimationGroup(*[Flip(equation_2[i], equation_4[i]) for i in [3, 10]]), AnimationGroup(*[Flip(equation_2[i], equation_4[i]) for i in [5, 14]]), run_time = 2, lag_ratio = 0.5))
        self.wait()
        
        color_map = {r"a": ORANGE, r"b": GREEN, r"c": YELLOW, r"0": BLUE}
        equation_5 = MTex(r"a+b=b+a", tex_to_color_map = color_map)
        equation_5.shift(equation_1[1].get_center() - equation_5[1].get_center())
        for i in range(7):
            equation_5[i].set_x(equation_1[i].get_x())
        equation_6 = MTex(r"a\times (b+c)=a\times b+a\times c", tex_to_color_map = color_map)
        equation_6.shift(equation_2[1].get_center() - equation_6[1].get_center())
        for i in range(15):
            equation_6[i].set_x(equation_2[i].get_x())
        self.play(LaggedStart(AnimationGroup(*[Flip(equation_1[i], equation_5[i]) for i in [0, 6]]), AnimationGroup(*[Flip(equation_1[i], equation_5[i]) for i in [2, 4]]), run_time = 1.5, lag_ratio = 0.5))
        self.wait()
        self.play(LaggedStart(AnimationGroup(*[Flip(equation_2[i], equation_6[i]) for i in [0, 8, 12]]), AnimationGroup(*[Flip(equation_2[i], equation_6[i]) for i in [3, 10]]), AnimationGroup(*[Flip(equation_2[i], equation_6[i]) for i in [5, 14]]), run_time = 2, lag_ratio = 0.5))
        self.wait()

        law_1 = MTex(r"a+b=b+a", tex_to_color_map = color_map)
        law_1.shift(1.5*UP + 3*LEFT - law_1[3].get_center())
        law_2 = MTex(r"0a=0", tex_to_color_map = color_map)
        law_2.shift(3*LEFT - law_2[2].get_center())
        law_3 = MTex(r"a\times (b+c)=a\times b+a\times c", tex_to_color_map = color_map)
        law_3.shift(1.5*DOWN + 3*LEFT - law_3[7].get_center())
        law_4 = MTex(r"ab=ba", tex_to_color_map = color_map)
        law_4.shift(1.5*UP + 3*RIGHT - law_4[2].get_center())
        law_5 = MTex(r"a^2-b^2=(a+b)(a-b)", tex_to_color_map = color_map)
        law_5.shift(3*RIGHT - law_5[5].get_center())
        law_6 = MTex(r"(a+b)^2=a^2+2ab+b^2", tex_to_color_map = color_map)
        law_6.shift(1.5*DOWN + 3*RIGHT - law_6[6].get_center())
        laws = [law_1, law_2, law_3, law_4, law_5, law_6]
        
        self.play(ReplacementTransform(equation_1, law_1), ReplacementTransform(equation_2, law_3))
        self.wait()
        self.play(Write(law_2), Write(law_4), Write(law_5), Write(law_6), run_time = 1)
        self.wait()
        self.play(IndicateAround(law_2))
        self.wait()
        self.play(IndicateAround(law_5))
        self.wait()
        
        title_2 = Title("线性代数")
        for i in range(4):
            title_2[i].shift((i-1.5)*0.1*RIGHT)
        left = title_2[0:2].save_state().set_x(0)
        right = title_2[2:].save_state().set_x(0)
        shade = BackgroundRectangle(left, color = BLACK, fill_opacity = 1, buff = 0.1)
        self.remove(title).add(left, shade, right).play(left.animate.restore(), right.animate.restore(), follow(shade, right))
        self.wait()
        
        color_map = {(r"\vec{u}", r"A"): ORANGE, (r"\vec{v}", r"B"): GREEN, r"a": YELLOW, (r"0", r"\vec{0}"): BLUE}
        equation_1 = MTex(r"\vec{u}+\vec{v}=\vec{v}+\vec{u}", tex_to_color_map = color_map)
        equation_1.shift(1.5*UP + 3*LEFT - equation_1[5].get_center())
        equation_2 = MTex(r"0\vec{u}=\vec{0}", tex_to_color_map = color_map)
        equation_2.shift(3*LEFT - equation_2[3].get_center())
        equation_3 = MTex(r"a(\vec{u}+\vec{v})=a\vec{u}+a\vec{v}", tex_to_color_map = color_map)
        equation_3.shift(1.5*DOWN + 3*LEFT - equation_3[8].get_center())
        equation_4 = MTex(r"AB\ne BA", tex_to_color_map = color_map)
        equation_4.shift(1.5*UP + 3*RIGHT - equation_4[3].get_center())
        equation_4[2].set_color(RED)
        equation_4.set_submobjects(equation_4.submobjects[:2] + [equation_4[3], equation_4[2]] + equation_4.submobjects[4:])
        equation_5 = MTex(r"A^2-B^2\ne(A+B)(A-B)", tex_to_color_map = color_map)
        equation_5.shift(3*RIGHT - equation_5[6].get_center())
        equation_5[5].set_color(RED)
        equation_5.set_submobjects(equation_5.submobjects[:5] + [equation_5[6], equation_5[5]] + equation_5.submobjects[7:])
        equation_6 = MTex(r"(A+B)^2\ne A^2+2AB+B^2", tex_to_color_map = color_map)
        equation_6.shift(1.5*DOWN + 3*RIGHT - equation_6[7].get_center())
        equation_6[6].set_color(RED)
        equation_6.set_submobjects(equation_6.submobjects[:6] + [equation_6[7], equation_6[6]] + equation_6.submobjects[8:])
        equations = [equation_1, equation_2, equation_3, equation_4, equation_5, equation_6]
        
        self.play(LaggedStart(*[Flip(laws[i], equations[i], dim = 1) for i in range(3)], run_time = 2, lag_ratio = 0.5))
        self.wait()
        self.play(LaggedStart(*[Flip(laws[i], equations[i], dim = 1) for i in range(3, 6)], run_time = 2, lag_ratio = 0.5))
        self.wait()

        vector = law_1[9:]
        matrix = law_4[0]
        surr_vec = SurroundingRectangle(vector)
        surr_mat = SurroundingRectangle(matrix)
        name_vec = Songti("向量", color = YELLOW).scale(0.75).next_to(surr_vec, UP)
        name_mat = Songti("线性映射", color = YELLOW).scale(0.75).next_to(surr_mat, UP)
        law_1.generate_target()[:9].fade(0.75)
        law_4.generate_target()[1:].fade(0.75)
        self.play(MoveToTarget(law_1), ShowCreation(surr_vec), *[mob.animate.fade(0.75) for mob in [law_2, law_3]])
        self.play(Write(name_vec))
        self.wait()
        self.play(MoveToTarget(law_4), ShowCreation(surr_mat), *[mob.animate.fade(0.75) for mob in [law_5, law_6]])
        self.play(Write(name_mat))
        self.wait()

        title_3 = Title("向量")
        self.play(*[FadeOut(mob) for mob in [surr_vec, name_mat, surr_mat, title_2] + laws], Transform(name_vec, title_3))
        self.wait()
        
class Patch2_1(FrameScene):
    def construct(self):
        vector = Arrow(-1.5*unit(PI/3), 1.5*unit(PI/3), buff = 0, color = GREEN)
        length = MTex("3", color = GREEN).shift(0.5*unit(PI*5/6))
        self.play(ShowCreation(vector))
        self.play(Write(length))
        self.wait()
        self.fade_out()

class Patch2_2(FrameScene):
    def construct(self):
        def func(t):
            return np.array([3*t-1.5, 3*smooth(t)-1.5, 0])
        trace = ParametricCurve(func, [0, 1, 0.01])
        moving = VGroup(Dot(color = GREEN).shift(1.5*DL), VMobject(color = GREEN))
        alpha = ValueTracker(0.0)
        beta = ValueTracker(0.0)
        def moving_updater(mob: VGroup):
            v = beta.get_value()
            now = func(alpha.get_value()%1)
            then = func(alpha.get_value()%1 + v/30)
            alpha.increment_value(v/30)
            moving[0].move_to(now)
            moving[1].become(Arrow(now, 5*then-4*now, buff = 0, color = GREEN))
        self.play(ShowCreation(trace), ShowCreation(moving[0]))
        self.add(moving)
        moving.add_updater(moving_updater)
        self.play(beta.animate.set_value(1))
        self.wait(10)

class Video_2(FrameScene):
    def construct(self):
        title = Title("向量")
        titleline = TitleLine()
        self.add(title, titleline)

        example_1 = VGroup(Arrow(-1.5*unit(PI/3), 1.5*unit(PI/3), buff = 0, color = GREEN), MTex("3", color = GREEN).shift(0.5*unit(PI*5/6))).shift(3.5*LEFT + 0.5*DOWN)
        example_2_1 = ParametricCurve(lambda t: np.array([3*t-1.5, 3*smooth(t)-1.5, 0]), [0, 1, 0.01]).shift(3.5*RIGHT + 0.5*DOWN)
        example_2_2 = VGroup(Dot(color = GREEN), Arrow(ORIGIN, 0.5*(RIGHT + 15/8*UP), color = GREEN, buff = 0)).shift(3.5*RIGHT + 0.5*DOWN)
        example_3 = Text(r"int a[4] = {1, 2, 4, 8};", t2c = {r"a[4]": GREEN}).scale(0.8)
        self.play(Write(example_3))
        self.wait()
        self.play(example_3.animate.shift(2*UP), OverFadeIn(example_1, 2*UP), OverFadeIn(example_2_1, 2*UP), OverFadeIn(example_2_2, 2*UP))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [example_1, example_2_1, example_2_2]])
        self.wait()

        calculation_1 = Text(r"{1, 2, 4, 8} * 2 = {2, 4, 8, 16}", t2c = {r"{1, 2, 4, 8}": GREEN, r"{2, 4, 8, 16}": GREEN_B}).scale(0.8).shift(0.5*UP)
        calculation_2 = Text(r"{1, 2, 4, 8} + {4, 3, 2, 1} = {5, 5, 6, 9}", t2c = {r"{1, 2, 4, 8}": GREEN, r"{4, 3, 2, 1}": BLUE, r"{5, 5, 6, 9}": TEAL}).scale(0.8).shift(DOWN)
        self.play(Write(calculation_1))
        self.wait()
        self.play(Write(calculation_2))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [example_3, calculation_1, calculation_2]])
        self.wait()

        dot = Dot(2*LEFT + DOWN, stroke_width = 4)
        arrow_1 = Arrow(ORIGIN, 2*RIGHT + UP, color = GREEN, buff = 0).shift(2*DOWN + 4*LEFT)
        arrow_2 = Arrow(ORIGIN, RIGHT + 2*UP, color = BLUE, buff = 0).shift(2*DOWN + 4*LEFT)
        arrow_3 = Arrow(ORIGIN, 3*RIGHT + 3*UP, color = TEAL, buff = 0).shift(2*DOWN + 4*LEFT)
        line = Polyline(2*RIGHT + UP, 2*RIGHT + UP, ORIGIN, color = BACK).shift(2*DOWN + 4*LEFT)
        arrow_4 = Arrow(ORIGIN, 6*RIGHT + 3*UP, color = GREEN_E, buff = 0).shift(2*DOWN + 4*LEFT)
        text_1 = MTex(r"\begin{bmatrix}2\\1\end{bmatrix}", color = GREEN).scale(0.8).next_to(dot, DR)
        self.play(ShowCreation(dot))
        self.wait()
        self.play(GrowArrow(arrow_1), Write(text_1))
        self.wait()
        self.bring_to_back(line).play(GrowArrow(arrow_2), TransformFromCopy(arrow_1, arrow_3), line.animate.set_points_as_corners([2*RIGHT + UP, 3*RIGHT + 3*UP, RIGHT + 2*UP]).shift(2*DOWN + 4*LEFT))
        self.wait()
        self.add(arrow_4, dot, arrow_1, arrow_2, arrow_3).play(TransformFromCopy(arrow_1, arrow_4))
        self.wait()
        self.play(OverFadeOut(text_1, shift = 4*LEFT + 2*UP, scale = 1/3, about_point = 4*LEFT + 2*UP), *[mob.animate.scale(1/3, about_point = ORIGIN).shift(4*LEFT + 2*UP) for mob in [dot, arrow_1, arrow_2, arrow_3, arrow_4, line]], run_time = 2)
        self.wait()

        resistance = Line(LEFT, 0.375*LEFT).append_points(Rectangle(height = 0.2, width = 0.75).get_points()).append_points(Line(0.375*RIGHT, RIGHT).get_points())
        e_l, e_r = 0.075*LEFT + 2*DOWN, 0.075*RIGHT + 2*DOWN
        circuit = VGroup(resistance.copy().shift(LEFT), resistance.copy().shift(RIGHT), resistance.copy().shift(LEFT + 2*UP), resistance.copy().shift(RIGHT + 2*UP), resistance.copy().rotate(PI/2).shift(UP), Line(2*UL, 2*DL), Line(2*UR, 2*DR), Line(2*DL, e_l), Line(2*DR, e_r), Line(0.3*UP, 0.3*DOWN).shift(e_l), Line(0.15*UP, 0.15*DOWN).shift(e_r))
        arrow_h, arrow_v = Arrow(0.3*LEFT, 0.3*RIGHT, buff = 0, color = GREEN), Arrow(0.3*DOWN, 0.3*UP, buff = 0, color = GREEN)
        arrow_1 = arrow_h.copy().next_to(circuit[2], UP)
        notice_1 = MTex(r"I_1", color = GREEN).scale(0.6).next_to(arrow_1, UP, buff = 0.15).add(arrow_1)
        arrow_2 = arrow_h.copy().next_to(circuit[3], UP)
        notice_2 = MTex(r"I_1+I_3", color = GREEN).scale(0.6).next_to(arrow_2, UP, buff = 0.15).add(arrow_2)
        arrow_3 = arrow_h.copy().next_to(circuit[0], DOWN)
        notice_3 = MTex(r"I_2+I_3", color = GREEN).scale(0.6).next_to(arrow_3, DOWN, buff = 0.15).add(arrow_3)
        arrow_4 = arrow_h.copy().next_to(circuit[1], DOWN)
        notice_4 = MTex(r"I_2", color = GREEN).scale(0.6).next_to(arrow_4, DOWN, buff = 0.15).add(arrow_4)
        arrow_5 = arrow_v.copy().next_to(circuit[4], RIGHT)
        notice_5 = MTex(r"I_3", color = GREEN).scale(0.6).next_to(arrow_5, RIGHT, buff = 0.15).add(arrow_5)
        notices = VGroup(notice_1, notice_2, notice_3, notice_4, notice_5)
        self.play(FadeIn(circuit), FadeIn(notices))
        self.wait()
        current = MTex(r"\begin{bmatrix}I_1\\I_2\\I_3\end{bmatrix}", color = GREEN).shift(4*RIGHT)
        self.play(Write(current))
        self.wait()
        self.play(OverFadeOut(current), OverFadeOut(notices, shift = 4.5*LEFT, scale = 1/2, about_point = 4.5*LEFT), circuit.animate.scale(1/2, about_point = ORIGIN).shift(4.5*LEFT), run_time = 2)
        self.wait()

        reactant = MTex(r"C_2H_5OH+3O_2", tex_to_color_map = {(r"C_2H_5OH", r"O_2"): GREEN}).shift(UP + RIGHT)
        vectors = MTex(r"\begin{bmatrix}2\\1\\6\end{bmatrix}+3\begin{bmatrix}0\\2\\0\end{bmatrix}", color = GREEN, tex_to_color_map = {r"+3": WHITE}).shift(DOWN)
        reactant_0, reactant_1, reactant_2 = reactant[:6], reactant[6:8], reactant[8:]
        vectors_0, vectors_1, vectors_2 = vectors[:7].set_x(reactant_0.get_x()), vectors[7:9], vectors[9:].set_x(reactant_2.get_x())
        vectors_1[1].next_to(vectors_2, LEFT, buff = 0.1, coor_mask = np.array([1, 0, 0]))
        vectors_1[0].set_x((vectors_0.get_x(RIGHT) + vectors_1[1].get_x(LEFT))/2)
        self.play(FadeIn(reactant_0, 0.5*DOWN), FadeIn(reactant_2, 0.5*DOWN))
        self.wait()
        self.play(Write(vectors_0), Write(vectors_2))
        self.wait()
        self.play(Write(reactant_1), Write(vectors_1))
        self.wait()
        self.play(OverFadeOut(vectors, shift = 5*LEFT + 2.5*DOWN, scale = 1/2, about_point = 5*LEFT + 2.5*DOWN), reactant.animate.scale(1/2, about_point = ORIGIN).shift(5*LEFT + 2.5*DOWN), run_time = 2)
        self.wait()

        def add_cap(cap: VMobject):
            mob = Line(0.3*LEFT, 0.3*RIGHT)
            mob.append_points(Line(0.2*LEFT, cap.get_start()).get_points()).append_points(cap.get_points()).add_line_to(0.2*RIGHT).shift(0.5*UP)
            return mob
        a = add_cap(Polyline(0.2*LEFT + 0.9*DOWN, DOWN, 0.2*RIGHT + 0.9*DOWN).set_color(GREEN_A)).add(MTexText(r"A").scale(0.6).set_color(GREEN)).shift(RIGHT + UP)
        t = add_cap(Polyline(0.2*LEFT + DOWN, 0.9*DOWN, 0.2*RIGHT + DOWN).set_color(RED_A)).add(MTexText(r"T").scale(0.6).set_color(RED)).shift(0.6*RIGHT).shift(RIGHT + UP)
        c = add_cap(ArcBetweenPoints(0.2*LEFT + DOWN, 0.2*RIGHT + DOWN, angle = -PI/2).set_color(BLUE_A)).add(MTexText(r"C").scale(0.6).set_color(BLUE)).shift(1.2*RIGHT).shift(RIGHT + UP)
        g = add_cap(ArcBetweenPoints(0.2*LEFT + (1.2-0.2*np.sqrt(2))*DOWN, 0.2*RIGHT + (1.2-0.2*np.sqrt(2))*DOWN, angle = PI/2).set_color(interpolate_color(WHITE, ORANGE, 0.2))).add(MTexText(r"G").scale(0.6).set_color(ORANGE)).shift(1.8*RIGHT).shift(RIGHT + UP)
        basis = VGroup(a, t, c, g)
        text = MTex(r"1234")
        colors = [GREEN, RED, BLUE, ORANGE]
        for i in range(4):
            text[i].scale(0.8).move_to((1+i*0.6)*RIGHT).set_color(colors[i])
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in basis], lag_ratio = 1/3), FadeIn(text, 0.3*UP, lag_ratio = 1/3), run_time = 2)
        self.wait()
        double = MTex(r"2468")
        colors = [RED, ORANGE, GREY, GREY]
        for i in range(4):
            double[i].scale(0.8).move_to((1+i*0.6)*RIGHT + DOWN).set_color(colors[i])
        self.play(FadeIn(double, 0.3*UP, lag_ratio = 1/3), run_time = 2)
        self.wait()

        title_2 = Title("线性映射")
        self.add(self.shade.set_fill(color = BLACK), title, titleline).play(FadeIn(self.shade), Flip(title, title_2, dim = 1))
        self.wait()

#################################################################### 

class Shaft(VGroup):
    def __init__(self, position: np.ndarray = ORIGIN, **kwargs):
        
        inner = Circle(radius = 0.35, color = WHITE)
        arc_1 = Arc(radius = 0.55, angle = PI/2, start_angle = PI/4)
        arc_2 = Arc(radius = 0.55, angle = PI/2, start_angle = PI + PI/4)
        outer = Circle(radius = 0.75, color = WHITE)
        
        super().__init__(inner, arc_1, arc_2, outer, **kwargs)
        self.shift(position)

class Test_3(FrameScene):
    def construct(self):
        shaft_left = Shaft(4*LEFT + DOWN)
        shaft_right = Shaft(4*RIGHT + DOWN)
        belt = Line(4*LEFT + 0.15*DOWN, 4*RIGHT + 0.15*DOWN).append_points(ArcBetweenPoints(4*RIGHT + 0.15*DOWN, 4*RIGHT + 1.85*DOWN, angle = -PI).get_points()).add_line_to(4*LEFT + 1.85*DOWN).append_points(ArcBetweenPoints(4*LEFT + 1.85*DOWN, 4*LEFT + 0.15*DOWN, angle = -PI).get_points())
        mould = Rectangle(height = 1.5, width = 2.5, fill_opacity = 1, fill_color = BLACK).next_to(0.1*DOWN, UP, buff = 0).shift(2*UP)
        arm = Rectangle(height = 3, width = 1.5, fill_opacity = 1, fill_color = BLACK).next_to(mould, UP, buff = 0)
        mould.add(arm)
        self.add(shaft_left, shaft_right, belt, mould)
        self.shaft = [shaft_left, shaft_right]
        self.mould = mould
        digit_1 = Digit(1).next_to(2*LEFT, UP)
        digit_1.counter = -1
        digit_1.product = Digit(0).next_to(ORIGIN, UP)
        digit_2 = Digit(2).next_to(4*LEFT, UP)
        digit_2.counter = -2
        digit_2.product = Digit(1).next_to(ORIGIN, UP)
        self.on_belt = [digit_1, digit_2]
        self.add(digit_1, digit_2).wait()
        digit_3 = Digit(3).next_to(ORIGIN, UP)
        digit_3.product = Digit(2).next_to(ORIGIN, UP)
        self.form(digit_3)
        digit_4 = Digit(4).next_to(ORIGIN, UP)
        digit_4.product = Digit(3).next_to(ORIGIN, UP)
        self.form(digit_4)
        digit_5 = Digit(5).next_to(ORIGIN, UP)
        digit_5.product = Digit(4).next_to(ORIGIN, UP)
        self.form(digit_5)
        digit_6 = Digit(6).next_to(ORIGIN, UP)
        digit_6.product = Digit(5).next_to(ORIGIN, UP)
        self.form(digit_6)
        digit_7 = Digit(7).next_to(ORIGIN, UP)
        digit_7.product = Digit(6).next_to(ORIGIN, UP)
        self.form(digit_7)
        digit_8 = Digit(8).next_to(ORIGIN, UP)
        digit_8.product = Digit(7).next_to(ORIGIN, UP)
        self.form(digit_8)
        digit_9 = Digit(9).next_to(ORIGIN, UP)
        digit_9.product = Digit(8).next_to(ORIGIN, UP)
        self.form(digit_9)
        self.form()
        self.form()

    def form(self, *mobs):
        for mob in mobs:
            mob.counter = -3
            self.on_belt.append(mob)
            self.add(mob)
            if not hasattr(mob, "product") or mob.product is None:
                mob.product = mob
        self.add(self.mould)
        anims = []
        old = self.on_belt
        self.on_belt = []
        for mob in old:
            mob.counter += 1
            if mob.counter == -2:
                mob.set_x(-4)
                anims.append(FadeIn(mob, 2*RIGHT))
            elif mob.counter == 3:
                anims.append(FadeOut(mob, 2*RIGHT))
                continue
            else:
                anims.append(mob.animate.shift(2*RIGHT))
            self.on_belt.append(mob)
        self.play(*anims, *[Rotate(mob, -1.25) for mob in self.shaft])
        self.wait()
        self.play(self.mould.animate.shift(2*DOWN), run_time = 0.5, rate_func = rush_into)
        for mob in self.on_belt:
            if mob.counter == 0:
                mob.digit = mob.product.digit
                mob.become(mob.product)
        self.play(self.mould.animate.shift(2*UP), run_time = 0.5, rate_func = rush_from)
        self.wait()
    
class BlackBox(VGroup):
    def __init__(self, **kwargs):
        
        core = Square(side_length = 2, fill_color = BLACK, fill_opacity = 1)
        entrance = Polygon(1.1*LEFT + 0.5*UP, 1.7*LEFT + UP, 1.7*LEFT + DOWN, 1.1*LEFT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        export = Polygon(1.1*RIGHT + 0.5*UP, 1.7*RIGHT + UP, 1.7*RIGHT + DOWN, 1.1*RIGHT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        background = Rectangle(width = 3, height = 2, stroke_width = 0, fill_color = BLACK, fill_opacity = 1)
        super().__init__(background, core, entrance, export, **kwargs)

class Test_4(FrameScene):
    def construct(self):
        box_0 = BlackBox()
        self.add(box_0)

class Video_3(FrameScene):
    def construct(self):
        title = Title("线性映射")
        titleline = TitleLine()
        box_0 = BlackBox()
        text_1 = Heiti("线性").scale(0.8).shift(0.3*UP + 0.2*LEFT)
        text_2 = Heiti("映射").scale(0.8)# .shift(0.3*DOWN + 0.2*RIGHT)
        bra = MTex(r"\begin{cases}\\\\\\\\\\\\\end{cases}")#.set_color(interpolate_color(WHITE, BACK, 0.5))
        ket = bra.copy().scale(np.array([-1, 1, 0]), min_scale_factor = -1)
        left = VGroup(bra.copy().shift(5.5*LEFT), ket.copy().shift(2.5*LEFT))
        right = VGroup(bra.copy().shift(2.5*RIGHT), ket.copy().shift(5.5*RIGHT))
        middle = left.copy()
        self.add(title, titleline)
        self.wait()
        self.play(FadeIn(box_0, 0.5*DOWN), FadeIn(text_2, 0.5*DOWN))
        self.wait()
        self.play(FadeIn(left, 0.5*RIGHT))
        self.wait()
        self.bring_to_back(middle).play(middle.animate.scale(0, min_scale_factor = 0, about_point = LEFT), rate_func = rush_into)
        self.play(ReplacementTransform(middle.shift(2*RIGHT), right), rate_func = rush_from)
        self.wait()
        self.play(text_2.animate.shift(0.3*DOWN + 0.2*RIGHT), OverFadeIn(text_1, 0.3*DOWN + 0.2*RIGHT))
        self.wait()

        color_map = {r"\vec{a}": GREEN, r"\vec{b}": BLUE}
        left_vectors = [MTex(r"\vec{a}", tex_to_color_map = color_map).shift(4*LEFT + 1.8*UP), MTex(r"\vec{b}", tex_to_color_map = color_map).shift(4*LEFT + 0.6*UP),
                        MTex(r"3\vec{a}", tex_to_color_map = color_map).shift(4*LEFT + 0.6*DOWN), MTex(r"\vec{a}+\vec{b}", tex_to_color_map = color_map).shift(4*LEFT + 1.8*DOWN),]
        color_map = {r"\vec{u}": GREEN, r"\vec{v}": BLUE}
        right_vectors = [MTex(r"\vec{u}", tex_to_color_map = color_map).shift(4*RIGHT + 1.8*UP), MTex(r"\vec{v}", tex_to_color_map = color_map).shift(4*RIGHT + 0.6*UP),
                        MTex(r"3\vec{u}", tex_to_color_map = color_map).shift(4*RIGHT + 0.6*DOWN), MTex(r"\vec{u}+\vec{v}", tex_to_color_map = color_map).shift(4*RIGHT + 1.8*DOWN),]
        self.play(Write(left_vectors[0]), Write(left_vectors[1]))
        self.wait()
        middle_1, middle_2 = left_vectors[0].copy(), left_vectors[1].copy()
        self.bring_to_back(middle_1, middle_2).play(*[mob.animate.move_to(LEFT) for mob in [middle_1, middle_2]], rate_func = rush_into)
        middle_1.become(right_vectors[0]).move_to(RIGHT), middle_2.become(right_vectors[1]).move_to(RIGHT)
        self.play(ReplacementTransform(middle_1, right_vectors[0]), ReplacementTransform(middle_2, right_vectors[1]), rate_func = rush_from)
        self.wait()
        self.play(Write(left_vectors[2]), Write(left_vectors[3]))
        self.wait()
        middle_1, middle_2 = left_vectors[2].copy(), left_vectors[3].copy()
        self.bring_to_back(middle_1, middle_2).play(*[mob.animate.move_to(LEFT) for mob in [middle_1, middle_2]], rate_func = rush_into)
        middle_1.become(right_vectors[2]).move_to(RIGHT), middle_2.become(right_vectors[3]).move_to(RIGHT)
        self.play(ReplacementTransform(middle_1, right_vectors[2]), ReplacementTransform(middle_2, right_vectors[3]), rate_func = rush_from)
        self.wait()

        law_1 = MTex(r"f(k\vec{x})=kf(\vec{x})", tex_to_color_map = {r"\vec{x}": GREEN}).scale(0.8).shift(2*UP)
        law_2 = MTex(r"f(\vec{x}+\vec{y})=f(\vec{x})+f(\vec{y})", tex_to_color_map = {r"\vec{x}": GREEN, r"\vec{y}": BLUE}).scale(0.8).shift(2*DOWN)
        self.play(Write(law_1))
        self.wait()
        self.play(Write(law_2))
        self.wait()

        def util(t: float):
            if t < 1/3:
                return 2/3*smooth(1.5*t)
            else:
                return 1-4/3*(1-smooth(1-0.75*(1-t)))
        self.play(*[OverFadeOut(mob, scale = 4, over_factor = 3, about_point = ORIGIN) for mob in [title, titleline, text_1, text_2, left, right, law_1, law_2] + left_vectors + right_vectors], FadeOut(box_0.set_fill(opacity = 0), scale = 4, about_point = ORIGIN), run_time = 2, rate_func = util)
        self.wait()

class Video_4(FrameScene):
    def construct(self):
        shaft_left = Shaft(4*LEFT + DOWN)
        shaft_right = Shaft(4*RIGHT + DOWN)
        belt = Line(4*LEFT + 0.15*DOWN, 4*RIGHT + 0.15*DOWN).append_points(ArcBetweenPoints(4*RIGHT + 0.15*DOWN, 4*RIGHT + 1.85*DOWN, angle = -PI).get_points()).add_line_to(4*LEFT + 1.85*DOWN).append_points(ArcBetweenPoints(4*LEFT + 1.85*DOWN, 4*LEFT + 0.15*DOWN, angle = -PI).get_points())
        mould = Rectangle(height = 1.5, width = 2.5, fill_opacity = 1, fill_color = BLACK).next_to(0.1*DOWN, UP, buff = 0).shift(2*UP)
        arm = Rectangle(height = 6, width = 1.5, fill_opacity = 1, fill_color = BLACK).next_to(mould, UP, buff = 0)
        mould.add(arm)
        self.shaft = [shaft_left, shaft_right]
        self.mould = mould
        self.on_belt = []

        self.add(shaft_left, shaft_right, belt, mould, self.shade.set_fill(color = BLACK)).play(FadeOut(self.shade), *[mob.scale(0.5, about_point = ORIGIN).animate.scale(2, about_point = ORIGIN) for mob in [shaft_left, shaft_right, belt, mould]], rate_func = rush_from)
        self.wait()

        apple = SVGMobject("apple.svg", fill_color = RED, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        lemon = SVGMobject("lemon.svg", fill_color = YELLOW, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        juice_apple = SVGMobject("juice.svg", fill_color = RED, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        juice_lemon = SVGMobject("juice.svg", fill_color = YELLOW, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        
        fruit_1 = apple.copy()
        fruit_1.product = juice_apple.copy()
        self.form(fruit_1)
        fruit_2 = lemon.copy()
        fruit_2.product = juice_lemon.copy()
        self.form(fruit_2)
        fruit_3 = apple.copy().shift(0.2*LEFT)
        fruit_3.product = juice_apple.copy().shift(0.2*LEFT)
        fruit_4 = apple.copy().shift(0.2*RIGHT)
        fruit_4.product = juice_apple.copy().shift(0.2*RIGHT)
        fruit_5 = apple.copy().shift(0.3*UP)
        fruit_5.product = juice_apple.copy().shift(0.3*UP)
        self.form(fruit_3, fruit_4, fruit_5)
        fruit_6 = apple.copy().shift(0.2*LEFT)
        fruit_6.product = juice_apple.copy().shift(0.2*LEFT)
        fruit_7 = lemon.copy().shift(0.2*RIGHT)
        fruit_7.product = juice_lemon.copy().shift(0.2*RIGHT)
        self.form(fruit_6, fruit_7)
        self.form()
        self.form()
        self.form()
        self.form()
        self.form()

    def form(self, *mobs):
        for mob in mobs:
            mob.counter = -3
            self.on_belt.append(mob)
            self.add(mob)
            if not hasattr(mob, "product") or mob.product is None:
                mob.product = mob
        self.add(self.mould)
        anims = []
        old = self.on_belt
        self.on_belt = []
        for mob in old:
            mob.counter += 1
            if mob.counter == -2:
                mob.shift(4*LEFT)
                anims.append(FadeIn(mob, 2*RIGHT))
            elif mob.counter == 3:
                anims.append(FadeOut(mob, 2*RIGHT))
                continue
            else:
                anims.append(mob.animate.shift(2*RIGHT))
            self.on_belt.append(mob)
        self.play(*anims, *[Rotate(mob, -1.25) for mob in self.shaft])
        self.wait()
        self.play(self.mould.animate.shift(2*DOWN), run_time = 0.5, rate_func = rush_into)
        for mob in self.on_belt:
            if mob.counter == 0:
                mob.become(mob.product)
        self.play(self.mould.animate.shift(2*UP), run_time = 0.5, rate_func = rush_from)
        self.wait()

class Gather(Homotopy):
    CONFIG = {
        "run_time": 3,
        "height": 4,
        "width": 4,
    }

    def __init__(self, mobject, shift: np.ndarray | None = None, move_to: np.ndarray | None = None, scale = None, **kwargs):
        digest_config(self, kwargs, locals())
        center = mobject.get_center()
        if move_to is not None:
            shift = center - move_to
        elif shift is None:
            shift = ORIGIN
        if scale is None:
            scale = 1
        h_start = mobject.get_height()
        w_start = mobject.get_width()
        h_end = self.height
        w_end = self.width

        def homotopy(x, y, z, t):
            w_now, h_now = interpolate(w_start, w_end, t), interpolate(h_start, h_end, t)
            offset = (np.array([x, y, z]) - center)*(interpolate(1, scale, t))
            offset[0] = max(-w_now/2, min(w_now/2, offset[0]))
            offset[1] = max(-h_now/2, min(h_now/2, offset[1]))
            return offset + center + t*shift

        super().__init__(homotopy, mobject, **kwargs)

class Video_5(FrameScene):
    def construct(self):
        axis_x, axis_y = Line(10*DOWN, 10*UP), Line(10*LEFT, 10*RIGHT)
        ratio = 0.5
        lines_h = VGroup(*[Line(10*LEFT + i*ratio*UP, 10*RIGHT + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE_E) for i in range(-20, 20)])
        lines_v = VGroup(*[Line(10*UP + i*ratio*RIGHT, 10*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE_E) for i in range(-20, 20)])
        grid = VGroup(lines_h, lines_v)
        background = VGroup(lines_h.copy().set_stroke(GREY), lines_v.copy().set_stroke(GREY), axis_x.copy(), axis_y.copy())
        self.play(FadeIn(grid), ShowCreation(axis_x), ShowCreation(axis_y))
        grid.add(axis_x, axis_y)
        self.clear().add(background, grid).wait()
        self.play(Rotate(grid, PI/2), run_time = 3)
        self.wait()
        self.play(Gather(grid, 3.5*RIGHT, scale = 0.8), Gather(background, 3.5*LEFT, scale = 0.8))
        self.wait()

        ratio = 0.4
        arrow_1 = Arrow(ORIGIN, ratio*(2*RIGHT + UP), color = GREEN, buff = 0).shift(3.5*LEFT)
        arrow_2 = Arrow(ORIGIN, 2*ratio*(2*RIGHT + UP), color = "#306630", buff = 0).shift(3.5*LEFT)
        arrow_3 = Arrow(ORIGIN, ratio*(2*RIGHT + UP), color = GREEN, buff = 0).shift(3.5*RIGHT)
        arrow_4 = Arrow(ORIGIN, 2*ratio*(2*RIGHT + UP), color = "#306630", buff = 0).shift(3.5*RIGHT)
        self.play(GrowArrow(arrow_2), GrowArrow(arrow_1, rate_func = rush_into, run_time = 0.5), GrowArrow(arrow_4), GrowArrow(arrow_3, rate_func = rush_into, run_time = 0.5))
        self.wait()
        self.play(*[Rotate(mob, about_point = 3.5*RIGHT, angle = PI/2) for mob in [arrow_3, arrow_4]])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [arrow_1, arrow_2, arrow_3, arrow_4]])
        self.wait()

        ratio = 0.8
        arrow_1 = Arrow(ORIGIN, ratio*(2*RIGHT + UP), color = GREEN, buff = 0).shift(3.5*LEFT)
        arrow_2 = Arrow(ORIGIN, ratio*(LEFT + UP), color = BLUE, buff = 0).shift(3.5*LEFT)
        arrow_3 = Arrow(ORIGIN, ratio*(RIGHT + 2*UP), color = TEAL, buff = 0).shift(3.5*LEFT)
        arrow_4 = Arrow(ORIGIN, ratio*(2*RIGHT + UP), color = GREEN, buff = 0).shift(3.5*RIGHT)
        arrow_5 = Arrow(ORIGIN, ratio*(LEFT + UP), color = BLUE, buff = 0).shift(3.5*RIGHT)
        arrow_6 = Arrow(ORIGIN, ratio*(RIGHT + 2*UP), color = TEAL, buff = 0).shift(3.5*RIGHT)
        para_left = Polyline(ratio*(2*RIGHT + UP), ratio*(2*RIGHT + UP), ORIGIN, color = GREY).shift(3.5*LEFT)
        para_right = Polyline(ratio*(2*RIGHT + UP), ratio*(2*RIGHT + UP), ORIGIN, color = GREY).shift(3.5*RIGHT)
        self.play(GrowArrow(arrow_1), GrowArrow(arrow_4))
        self.add(para_left, para_right, arrow_1, arrow_4).play(para_left.animate.set_points_as_corners([ratio*(2*RIGHT + UP), ratio*(RIGHT + 2*UP), ratio*(LEFT + UP)]).shift(3.5*LEFT), para_right.animate.set_points_as_corners([ratio*(2*RIGHT + UP), ratio*(RIGHT + 2*UP), ratio*(LEFT + UP)]).shift(3.5*RIGHT), GrowArrow(arrow_2), GrowArrow(arrow_5), TransformFromCopy(arrow_1, arrow_3), TransformFromCopy(arrow_4, arrow_6))
        self.wait()
        self.play(*[Rotate(mob, about_point = 3.5*RIGHT, angle = PI/2) for mob in [arrow_4, arrow_5, arrow_6, para_right]])
        self.wait()
        self.shade.set_color(BLACK)
        self.fade_out()
        self.wait()


#################################################################### 

class Patch_6_1(FrameScene):
    def construct(self):
        self.shade.set_color(BLACK)
        hen = SVGMobject("hen.svg", height = 8, color = interpolate_color(BLACK, GREEN, 0.2), stroke_width = 0).shift(8*LEFT)
        self.play(hen.animate.shift(RIGHT), FadeOut(self.shade))
        self.wait()
        self.play(FadeIn(self.shade), hen.animate.shift(LEFT))
        self.wait()

class Patch_6_2(FrameScene):
    def construct(self):
        bunny = SVGMobject("rabbit.svg", height = 8, color = interpolate_color(BLACK, BLUE, 0.2), stroke_width = 0).shift(8*LEFT)
        self.play(FadeIn(bunny, RIGHT))
        self.wait()
        self.play(FadeOut(bunny, LEFT))
        self.wait()

class Talisman(VGroup):
    def __init__(self, path: str, side_color = GREY, svg_color = WHITE, **kwargs):
        
        back = RegularPolygon(8, start_angle = PI/8, stroke_color = side_color, stroke_width = 8, fill_opacity = 1, fill_color = interpolate_color(svg_color, GREY_D, 0.75))
        icon = SVGMobject(path, height = 1.2, color = svg_color, stroke_width = 0)
        super().__init__(back, icon, **kwargs)

    def dimming(self):
        self.save_state().generate_target()
        self.target[0].set_fill(color = interpolate_color(self[0].get_stroke_color(), GREY, 0.75))
        self.target[1].set_opacity(0)
        return MoveToTarget(self)
    
    def dimmed(self):
        self.save_state()
        self[0].set_fill(color = interpolate_color(self[0].get_stroke_color(), GREY, 0.75))
        self[1].set_opacity(0)
        return self

class Test_5(FrameScene):
    def construct(self):
        # coin = Talisman("Sleep_Bunny.svg", side_color = YELLOW, svg_color = PURPLE)
        # self.add(coin)
        # self.wait()
        # self.play(coin.dimming())
        # self.wait()
        # self.play(coin.animate.restore())
        # self.wait()

        ratio = 0.4
        head_chicken, head_rabbit, leg_chicken, leg_rabbit = [Talisman("head_chicken.svg", side_color = YELLOW, svg_color = RED).scale(ratio), Talisman("head_rabbit.svg", side_color = YELLOW, svg_color = PURPLE_B).scale(ratio), Talisman("leg_chicken.svg", side_color = GREEN, svg_color = RED).scale(ratio), Talisman("leg_rabbit.svg", side_color = GREEN, svg_color = PURPLE_B).scale(ratio)]
        offset_h = 6
        template_h_c = head_chicken.copy().shift(offset_h*LEFT + 3*UP)
        template_l_c = VGroup(leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*UP), leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*DOWN))
        template_h_r = head_rabbit.copy().shift(offset_h*RIGHT + 3*UP)
        template_l_r = VGroup(*[leg_rabbit.copy().shift(offset_h*RIGHT + 0.5*DOWN + (i-1.5)*UP) for i in range(4)])

        list_heads = [head_chicken.copy().dimmed() for _ in range(6)] + [head_rabbit.copy().dimmed() for _ in range(4)]
        heads = VGroup(*[list_heads[i].shift((i-4.5)*0.9*RIGHT + 2.5*UP) for i in range(10)])
        list_legs_1 = [leg_chicken.copy().dimmed() for _ in range(6)] + [leg_rabbit.copy().dimmed() for _ in range(4)]
        list_legs_2 = [leg_chicken.copy().dimmed() for _ in range(6)] + [leg_rabbit.copy().dimmed() for _ in range(4)]
        list_legs_3 = [leg_rabbit.copy().dimmed() for _ in range(8)]
        legs = VGroup(*[list_legs_1[i].shift((i-4.5)*0.9*RIGHT + 0.45*UP) for i in range(10)], *[list_legs_2[i].shift((i-4.5)*0.9*RIGHT + 0.45*DOWN) for i in range(10)], *[list_legs_3[i].shift((i-4.5)*0.9*RIGHT + 1.35*DOWN) for i in range(8)])
        self.add(template_h_c, template_l_c, template_h_r, template_l_r, heads, legs)

class Video_6(FrameScene):
    def construct(self):

        self.wait()

        ratio = 0.4
        head_chicken, head_rabbit, leg_chicken, leg_rabbit = [Talisman("head_chicken.svg", side_color = YELLOW, svg_color = GREEN).scale(ratio), Talisman("head_rabbit.svg", side_color = YELLOW, svg_color = BLUE).scale(ratio), Talisman("leg_chicken.svg", side_color = ORANGE, svg_color = GREEN).scale(ratio), Talisman("leg_rabbit.svg", side_color = ORANGE, svg_color = BLUE).scale(ratio)]
        offset_h = 4.5
        template_h_c = head_chicken.copy().shift(offset_h*LEFT + 3*UP)
        template_l_c = VGroup(leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*UP), leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*DOWN))
        template_h_r = head_rabbit.copy().shift(offset_h*RIGHT + 3*UP)
        template_l_r = VGroup(*[leg_rabbit.copy().shift(offset_h*RIGHT + 0.5*DOWN + (i-1.5)*UP) for i in range(4)])

        def small_icon(mob: Talisman, offset = ORIGIN):
            copy_mob = mob.copy().scale(0.6).shift(offset)
            copy_mob[0].set_stroke(width = 5)
            return copy_mob.dimmed()
        space = 0.6
        list_heads = [small_icon(head_chicken, offset = (i-4.5)*space*RIGHT + 4*space*UP) for i in range(6)] + [small_icon(head_rabbit, offset = (i+1.5)*space*RIGHT + 4*space*UP) for i in range(4)]
        heads = VGroup(*list_heads)
        list_legs_1 = [small_icon(leg_chicken, offset = (i-4.5)*space*RIGHT + 0.5*space*UP) for i in range(6)] + [small_icon(leg_rabbit, offset = (i+1.5)*space*RIGHT + 0.5*space*UP) for i in range(4)]
        list_legs_2 = [small_icon(leg_chicken, offset = (i-4.5)*space*RIGHT + 0.5*space*DOWN) for i in range(6)] + [small_icon(leg_rabbit, offset = (i+1.5)*space*RIGHT + 0.5*space*DOWN) for i in range(4)]
        list_legs_3 = [small_icon(leg_rabbit, offset = (i-4.5)*space*RIGHT + 1.5*space*DOWN) for i in range(8)]
        legs = VGroup(*list_legs_1, *list_legs_2, *list_legs_3)
        
        self.play(*[GrowFromCenter(mob) for mob in [template_h_c, *template_l_c, template_h_r, *template_l_r]])
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in heads], lag_ratio = 0.1, run_time = 2, group = heads))
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in legs], lag_ratio = 0.1, run_time = 2, group = legs))
        self.wait()

        self.play(*[mob.animate.fade().shift(0.5*space*DOWN) for mob in list_legs_3])
        self.wait()
        self.play(IndicateAround(legs[:20]))
        self.wait()
        self.play(*[mob[0].animate.set_opacity(1) for mob in list_legs_3])
        self.wait()
        self.play(IndicateAround(legs[20:]), *[mob.animate.restore().shift(0.3*DOWN) for mob in list_legs_3])
        self.wait()

        anims_1 = [list_legs_3[4+i].animating(path_arc = PI/6).move_to((i+1.5)*space*RIGHT + 2.5*space*DOWN) for i in range(4)]
        anims_2 = [list_legs_3[i].animating(path_arc = -PI/10, run_time = 1.5).move_to((i+1.5)*space*RIGHT + 1.5*space*DOWN) for i in range(4)]
        self.play(*anims_1, *anims_2)
        self.wait()
        line = DashedLine(3*UP + space*RIGHT, 2*DOWN + space*RIGHT, color = YELLOW)
        self.play(ShowCreation(line))
        self.wait()
        self.play(*[mob.animate.restore().shift(0.3*RIGHT) for mob in list_heads[6:] + list_legs_1[6:] + list_legs_2[6:]], *[mob.animate.shift(0.3*RIGHT) for mob in list_legs_3])
        self.wait()
        self.play(*[mob.animate.restore().shift(0.3*LEFT) for mob in list_heads[:6] + list_legs_1[:6] + list_legs_2[:6]])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [heads, legs, line]])
        self.wait()

class Video_7(FrameScene):
    def construct(self):
        
        ratio = 0.4
        head_chicken, head_rabbit, leg_chicken, leg_rabbit = [Talisman("head_chicken.svg", side_color = YELLOW, svg_color = GREEN).scale(ratio), Talisman("head_rabbit.svg", side_color = YELLOW, svg_color = BLUE).scale(ratio), Talisman("leg_chicken.svg", side_color = ORANGE, svg_color = GREEN).scale(ratio), Talisman("leg_rabbit.svg", side_color = ORANGE, svg_color = BLUE).scale(ratio)]
        offset_h = 4.5
        template_h_c = head_chicken.copy().shift(offset_h*LEFT + 3*UP)
        template_l_c = VGroup(leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*UP), leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*DOWN))
        template_h_r = head_rabbit.copy().shift(offset_h*RIGHT + 3*UP)
        template_l_r = VGroup(*[leg_rabbit.copy().shift(offset_h*RIGHT + 0.5*DOWN + (i-1.5)*UP) for i in range(4)])
        self.add(template_h_c, *template_l_c, template_h_r, *template_l_r)

        color_map = {r"x": GREEN, r"y": BLUE}
        x = MTex(r"x", color = GREEN).shift(offset_h*LEFT + 2*UP).scale(1.5).set_stroke(width = 8, color = BLACK, background = True)
        y = MTex(r"y", color = BLUE).shift(offset_h*RIGHT + 2*UP).scale(1.5).set_stroke(width = 8, color = BLACK, background = True)
        self.play(Write(x), Write(y))
        self.wait()

        heads = MTex(r"1x+1y = 10", color = YELLOW, tex_to_color_map = color_map)
        heads.shift(0.5*RIGHT + 3*UP -heads[5].get_center())
        tails = MTex(r"2x+4y = 28", color = ORANGE, tex_to_color_map = color_map)
        tails.shift(0.5*RIGHT + 0.5*DOWN -tails[5].get_center())
        self.play(Write(heads))
        self.wait()
        self.play(Write(tails))
        self.wait()

        solution = MTex(r"\Rightarrow\begin{cases}x=6\\y=4\end{cases}", tex_to_color_map = color_map).shift(2.5*UP)
        self.play(heads.animate.shift((solution[4].get_y() - heads[5].get_y())*UP), tails.animate.shift((solution[7].get_y() - tails[5].get_y())*UP))
        self.wait()
        equations = VGroup(heads, tails)
        solution.set_x(equations.get_x(RIGHT), RIGHT)
        shade = BackgroundRectangle(solution, fill_opacity = 1, buff = 0.2)
        self.add(solution, shade, equations).play(equations.animate.shift(1.3*LEFT), follow(shade, equations), solution.animate.shift(1.3*RIGHT))
        self.remove(shade).wait()

        offset = 2*DOWN + 1.8*LEFT
        ratio = 0.2
        axes = VGroup(Arrow(-3*ratio*RIGHT, 21*ratio*RIGHT, buff = 0), Arrow(-3*ratio*UP, 15*ratio*UP, buff = 0)).shift(offset)
        line_1 = Line(ratio*(-3*RIGHT + 13*UP), ratio*(13*RIGHT-3*UP), color = YELLOW).shift(offset)
        line_2 = Line(ratio*(-3*RIGHT + 8.5*UP), ratio*(20*RIGHT-3*UP), color = ORANGE).shift(offset)
        dot = Dot(ratio*(6*RIGHT + 4*UP)).shift(offset)
        coordinate = MTex(r"(6, 4)", tex_to_color_map = {r"6": GREEN, r"4": BLUE}).scale(0.8).next_to(dot, UR, buff = 0.1)
        self.play(ShowCreation(axes, lag_ratio = 0.5))
        self.wait()
        self.play(IndicateAround(heads), ShowCreation(line_1), run_time = 2)
        self.wait()
        self.play(IndicateAround(tails), ShowCreation(line_2), run_time = 2)
        self.wait()
        self.play(ShowCreation(dot))
        self.play(Write(coordinate))
        self.wait()

        self.play(*[FadeOut(mob) for mob in [axes, line_1, line_2, dot, coordinate]], equations.animate.set_x(0).shift(0.5*UP), follow(solution, equations, OverFadeOut))
        self.wait()

        text = VGroup(Heiti("线性").scale(0.8).shift(0.3*UP + 0.2*LEFT), Heiti("映射").scale(0.8).shift(0.3*DOWN + 0.2*RIGHT)).shift(0.5*DOWN)
        box_0 = BlackBox().shift(0.5*DOWN)
        self.play(*[FadeIn(mob, 0.5*DOWN) for mob in [box_0, text]], *[FadeOut(mob, LEFT) for mob in [template_h_c, *template_l_c, x]], *[FadeOut(mob, RIGHT) for mob in [template_h_r, *template_l_r, y]])
        self.wait()

        name = Heiti(r"数头数脚", t2c = {r"头": YELLOW, r"脚": ORANGE}).scale(0.8).next_to(UP, UP)
        self.play(FadeIn(name, 0.5*DOWN))
        self.wait()

        color_map = {r"{x}": GREEN, r"{y}": BLUE}
        vector_1 = MTex(r"\begin{bmatrix}{x}\\{y}\end{bmatrix}", tex_to_color_map = color_map).scale(0.8).next_to(2*LEFT + 0.5*DOWN, LEFT)
        vector_2 = MTex(r"\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}", tex_to_color_map = {r"1{x}+1{y}": YELLOW, r"2{x}+4{y}": ORANGE, **color_map}).scale(0.8).next_to(2*RIGHT + 0.5*DOWN, RIGHT)
        self.play(Write(vector_1))
        self.wait()
        middle = vector_1.copy()
        self.bring_to_back(middle).play(middle.animate.move_to(LEFT + 0.5*DOWN).scale(0.5), rate_func = rush_into)
        middle.become(vector_2).move_to(RIGHT + 0.5*DOWN).scale(0.5)
        self.play(ReplacementTransform(middle, vector_2), rate_func = rush_from)
        self.wait()
        self.play(vector_1.animate.move_to(5*LEFT + 2.5*UP), vector_2.animate.move_to(5*RIGHT + 2.5*UP))
        self.wait()
        
        vector_3 = MTex(r"\begin{bmatrix}3{x}\\3{y}\end{bmatrix}", tex_to_color_map = color_map).scale(0.8).next_to(2*LEFT + 0.5*DOWN, LEFT)
        vector_4 = MTex(r"\begin{bmatrix}3(1{x}+1{y})\\3(2{x}+4{y})\end{bmatrix}", tex_to_color_map = {r"1{x}+1{y}": YELLOW, r"2{x}+4{y}": ORANGE, **color_map}).scale(0.8).next_to(2*RIGHT + 0.5*DOWN, RIGHT)
        self.play(Write(vector_3))
        self.wait()
        middle = vector_3.copy()
        self.bring_to_back(middle).play(middle.animate.move_to(LEFT + 0.5*DOWN).scale(0.5), rate_func = rush_into)
        middle.become(vector_4).move_to(RIGHT + 0.5*DOWN).scale(0.5)
        self.play(ReplacementTransform(middle, vector_4), rate_func = rush_from)
        self.wait()
        self.play(vector_3.animate.move_to(5*LEFT + 1*UP), vector_4.animate.move_to(5*RIGHT + 1*UP))
        self.wait()

        color_map = {r"x_1": GREEN, r"x_2": GREEN_E, r"y_1": BLUE, r"y_2": BLUE_E}
        vector_5 = MTex(r"\begin{bmatrix}x_1+x_2\\y_1+y_2\end{bmatrix}", tex_to_color_map = color_map).scale(0.8).next_to(2*LEFT + 0.5*DOWN, LEFT)
        vector_6 = MTex(r"\begin{bmatrix}(1x_1+1y_1)+(1x_2+1y_2)\\(2x_1+4y_1)+(2x_2+4y_2)\end{bmatrix}", tex_to_color_map = {r"(1x_1+1y_1)": YELLOW, r"(1x_2+1y_2)": YELLOW_E, r"(2x_1+4y_1)": ORANGE, r"(2x_2+4y_2)": interpolate_color(ORANGE, BLACK, 0.3), **color_map}).scale(0.8).next_to(2*RIGHT + 0.5*DOWN, RIGHT)
        self.play(Write(vector_5))
        self.wait()
        middle = vector_5.copy()
        self.bring_to_back(middle).play(middle.animate.move_to(LEFT + 0.5*DOWN).scale(0.5), rate_func = rush_into)
        middle.become(vector_6).move_to(RIGHT + 0.5*DOWN).scale(0.5)
        self.play(ReplacementTransform(middle, vector_6), rate_func = rush_from)
        self.wait()
        self.play(*[FadeOut(mob) for mob in [vector_3, vector_4, vector_5, vector_6]])
        self.wait()


        vector_7 = MTex(r"\begin{bmatrix}?\\?\end{bmatrix}").scale(0.8).next_to(2*LEFT + 0.5*DOWN, LEFT)
        vector_7[1].set_color(GREEN), vector_7[2].set_color(BLUE)
        vector_8 = MTex(r"\begin{bmatrix}10\\28\end{bmatrix}", tex_to_color_map = {r"10": YELLOW, r"28": ORANGE}).scale(0.8).next_to(2*RIGHT + 0.5*DOWN, RIGHT)
        self.play(Write(vector_8))
        self.wait()
        middle = vector_8.copy()
        self.bring_to_back(middle).play(middle.animate.move_to(RIGHT + 0.5*DOWN).scale(0.5), rate_func = rush_into)
        middle.become(vector_7).move_to(LEFT + 0.5*DOWN).scale(0.5)
        self.play(ReplacementTransform(middle, vector_7), rate_func = rush_from)
        self.wait()
        solution.set_x(equations.get_x(RIGHT), RIGHT).shift(0.5*UP)
        shade = BackgroundRectangle(solution, fill_opacity = 1, buff = 0.2)
        self.add(solution, shade, equations).play(equations.animate.shift(1.3*LEFT), follow(shade, equations), solution.animate.shift(1.3*RIGHT))
        self.remove(shade).wait()

        self.play(*[mob.animate.shift(2*DOWN) for mob in [equations, solution]], *[mob.animate.shift(DOWN) for mob in [box_0, text]], *[OverFadeOut(mob, 1.5*DOWN) for mob in [vector_7, vector_8, name, vector_1, vector_2]])
        self.wait()
        
class Video_8(FrameScene):
    def construct(self):

        text = VGroup(Heiti("线性").scale(0.8).shift(0.3*UP + 0.2*LEFT), Heiti("映射").scale(0.8).shift(0.3*DOWN + 0.2*RIGHT)).shift(1.5*DOWN)
        box = BlackBox().shift(1.5*DOWN)
        box.set_fill(opacity = 0).remove(box[0])
        color_map = {r"x": GREEN, r"y": BLUE}
        solution = MTex(r"\Rightarrow\begin{cases}x=6\\y=4\end{cases}", tex_to_color_map = color_map).shift(UP)
        heads = MTex(r"1x+1y = 10", color = YELLOW, tex_to_color_map = color_map)
        heads.shift(-heads[5].get_center()).shift((solution[4].get_y() - heads[5].get_y())*UP)
        tails = MTex(r"2x+4y = 28", color = ORANGE, tex_to_color_map = color_map)
        tails.shift(-tails[5].get_center()).shift((solution[7].get_y() - tails[5].get_y())*UP)
        equations = VGroup(heads, tails).set_x(-1.3)
        solution.set_x(equations.get_x(RIGHT), RIGHT).set_x(equations.get_x(RIGHT) + 2.6, RIGHT)
        self.add(solution, equations, text, box)
        paras = [heads[0], heads[3], tails[0], tails[3]]
        results = [heads[6:], tails[6:]]
        self.play(*[IndicateAround(mob) for mob in paras])
        self.wait()
        self.play(*[IndicateAround(mob) for mob in results])
        self.wait()

        underline_1, underline_2 = Underline(heads), Underline(tails)
        self.play(ShowCreation(underline_1), ShowCreation(underline_2))
        self.wait()
        self.play(FadeOut(underline_1), FadeOut(underline_2))
        self.wait()

        column_1, column_2 = SurroundingRectangle(VGroup(heads[0], tails[0])), SurroundingRectangle(VGroup(heads[3], tails[3]))
        self.play(IndicateAround(VGroup(heads[0], tails[0])), IndicateAround(VGroup(heads[3], tails[3])))
        self.wait()

        texts = [r"\begin{bmatrix}1\\2\end{bmatrix}", r"\begin{bmatrix}1\\4\end{bmatrix}", r"=\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}"]
        formula = MTex(r"{x}\begin{bmatrix}1\\2\end{bmatrix}+{y}\begin{bmatrix}1\\4\end{bmatrix}=\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}", isolate = texts + [r"+{y}"], tex_to_color_map = {r"{x}": BLUE, r"{y}": GREEN, r"1": YELLOW, (r"2", r"4"): ORANGE}).shift(3*UP)
        vector_1, vector_2 = formula.get_part_by_tex(texts[0]).save_state().set_x(column_1.get_x()), formula.get_part_by_tex(texts[1]).save_state().set_x(column_2.get_x())
        rest = VGroup(*formula.get_part_by_tex(r"{x}").submobjects, *formula.get_part_by_tex(r"+{y}").submobjects, *formula.get_part_by_tex(texts[2]).submobjects)
        self.play(Write(vector_1), ShowCreation(column_1))
        self.wait()
        self.play(Write(vector_2), ShowCreation(column_2))
        self.wait()
        
        self.play(vector_1.animate.restore(), vector_2.animate.restore())
        self.play(Write(rest))
        self.wait()

        title = Title("线性组合").shift(UP)
        titleline = TitleLine()
        self.bring_to_back(box).play(title.animate.shift(DOWN), GrowFromPoint(titleline, 4*UP), box.animate.shift(1.5*UP).scale(np.array([4, 3, 1])).set_stroke(width = 10, color = GREY), OverFadeOut(text, shift = 1.5*UP, scale = 3), *[mob.animate.shift(DOWN) for mob in [vector_1, vector_2]], FadeOut(rest, DOWN), *[OverFadeOut(mob, DOWN) for mob in [equations, solution, column_1, column_2]], run_time = 2)
        self.wait()

        ratio = 0.2
        head_chicken, head_rabbit, leg_chicken, leg_rabbit = [Talisman("head_chicken.svg", side_color = YELLOW, svg_color = GREEN).scale(ratio), Talisman("head_rabbit.svg", side_color = YELLOW, svg_color = BLUE).scale(ratio), Talisman("leg_chicken.svg", side_color = ORANGE, svg_color = GREEN).scale(ratio), Talisman("leg_rabbit.svg", side_color = ORANGE, svg_color = BLUE).scale(ratio)]
        for mob in [head_chicken, head_rabbit, leg_chicken, leg_rabbit]:
            mob[0].set_stroke(width = 6)
        template_c = VGroup(head_chicken.copy().shift(UP), VMobject(), leg_chicken.copy().shift(0.25*DOWN), leg_chicken.copy().shift(0.75*DOWN), VMobject()).shift(0.2*DOWN).set_x(vector_1.get_x())
        template_r = VGroup(head_rabbit.copy().shift(UP), *[leg_rabbit.copy().shift(0.5*DOWN + (i-1.5)*0.5*DOWN) for i in range(4)]).shift(0.2*DOWN).set_x(vector_2.get_x())
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in template_c], lag_ratio = 0.5, run_time = 1), IndicateAround(vector_1))
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in template_r], lag_ratio = 0.5, run_time = 1), IndicateAround(vector_2))
        self.wait()

        rest.shift(DOWN)
        color_map = {r"{x}": GREEN, r"{y}": BLUE}
        vector_in = MTex(r"\begin{bmatrix}{x}\\{y}\end{bmatrix}", tex_to_color_map = color_map).scale(0.8).move_to(5.6*LEFT)
        vector_out = MTex(r"\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}", tex_to_color_map = {r"1": YELLOW, (r"2", r"4"): ORANGE, **color_map}).scale(0.8).move_to(5.6*RIGHT)
        self.play(FadeIn(rest[0], 0.2*RIGHT), FadeIn(rest[2], 0.2*RIGHT), Write(vector_in))
        self.wait()
        self.play(FadeIn(rest[1], 0.2*DOWN))
        self.wait()
        self.play(Write(rest[3:]), FadeIn(vector_out))
        self.wait()

        result = MTex(r"\begin{bmatrix}10\\28\end{bmatrix}", tex_to_color_map = {r"10": YELLOW, r"28": ORANGE}).scale(0.8).move_to(5.6*RIGHT)
        self.play(FadeOut(template_c), FadeOut(template_r), IndicateAround(vector_1), IndicateAround(vector_2))
        self.wait()
        self.play(Flip(vector_out, result), IndicateAround(vector_out))
        self.wait()
        self.play(IndicateAround(rest[0]), IndicateAround(rest[2]))
        self.wait()
        self.play(IndicateAround(vector_in))
        self.wait()

        texts = [r"\begin{bmatrix}1&1\\2&4\end{bmatrix}", r"\begin{bmatrix}{x}\\{y}\end{bmatrix}", r"=\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}"]
        matrix = MTex(r"\begin{bmatrix}1&1\\2&4\end{bmatrix}\begin{bmatrix}{x}\\{y}\end{bmatrix}=\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}", isolate = texts, tex_to_color_map = {r"{x}": BLUE, r"{y}": GREEN, r"1": YELLOW, (r"2", r"4"): ORANGE})
        parts = [matrix.get_part_by_tex(text) for text in texts]
        anim_0 = TransformFromCopy(vector_1[0], matrix[0])
        self.play(anim_0, TransformFromCopy(vector_1[1], matrix[1]), TransformFromCopy(vector_1[2], matrix[3]), follow(vector_1[3].copy(), anim_0, FadeOut))
        anim_0 = TransformFromCopy(vector_2[3], matrix[5])
        self.play(anim_0, TransformFromCopy(vector_2[1], matrix[2]), TransformFromCopy(vector_2[2], matrix[4]), follow(vector_2[0].copy(), anim_0, FadeOut))
        self.wait()
        self.play(TransformFromCopy(vector_in, parts[1], path_arc = -PI/2))
        self.wait()
        self.play(TransformFromCopy(rest[3:], parts[2]))
        self.wait()

        backs = BackgroundRectangle(parts[0], color = YELLOW, fill_opacity = 0.1, buff = 0.1), BackgroundRectangle(parts[1], color = GREEN, fill_opacity = 0.1, buff = 0.1), BackgroundRectangle(parts[2][1:], color = ORANGE, fill_opacity = 0.1, buff = 0.1)
        form = MTex(r"A\vec{x}=\vec{y}", tex_to_color_map = {r"A": YELLOW, r"\vec{x}": GREEN, r"=": WHITE, r"\vec{y}": ORANGE}).save_state()
        charas = [form.get_part_by_tex(text).set_x(mob.get_x()).shift(1.5*DOWN) for text, mob in zip([r"A", r"\vec{x}", r"=", r"\vec{y}"], [backs[0], backs[1], parts[2][0], backs[2]])]
        self.bring_to_back(backs[0]).play(FadeIn(backs[0]), IndicateAround(parts[0]))
        self.wait()
        self.play(Write(charas[0]))
        self.wait()
        self.bring_to_back(backs[1]).play(FadeIn(backs[1]), Write(charas[1]))
        self.wait()
        self.bring_to_back(backs[2]).play(FadeIn(backs[2]), Write(charas[3]))
        self.wait()
        self.add(charas[2].set_opacity(0)).play(form.animate.restore(), formula.animating(remover = True).scale(np.array([1, 0, 1]), about_point = 3*UP), *[mob.animate.shift(2*UP) for mob in [matrix, *backs]])
        self.wait()

        multi = MTex(r"A(k\vec{x})=kA\vec{x}", tex_to_color_map = {r"A": YELLOW, r"\vec{x}": GREEN, r"k": TEAL})
        multi.shift(1*DOWN).shift((charas[2].get_x() - multi[6].get_x())*RIGHT)
        adding = MTex(r"A(\vec{x}_1+\vec{x}_2)=A\vec{x}_1+A\vec{x}_2", tex_to_color_map = {r"A": YELLOW, r"\vec{x}_1": GREEN, r"\vec{x}_2": GREEN_E})
        adding.shift(1.75*DOWN).shift((charas[2].get_x() - adding[10].get_x())*RIGHT)
        self.play(Write(multi))
        self.wait()
        self.play(Write(adding))
        self.wait()
        self.fade_out()
        self.wait()

class Video_9(FrameScene):
    def construct(self):
        camera = self.camera.frame
        ratio = 0.4
        offset = ratio*(5*UP + 14*RIGHT)
        camera.shift(offset)
        left, right, up, down = 50*ratio*LEFT, 50*ratio*RIGHT, 50*ratio*DOWN, 50*ratio*UP
        axis_x, axis_y = Line(up, down), Line(left, right)
        lines_h = VGroup(*[Line(left + i*ratio*UP, right + i*ratio*UP, stroke_width = 2, color = BLUE_E) for i in range(-40, 40)])
        lines_v = VGroup(*[Line(up + i*ratio*RIGHT, down + i*ratio*RIGHT, stroke_width = 2, color = BLUE_E) for i in range(-70, 70)])
        points = [Dot(i*ratio*UP + j*ratio*RIGHT, radius = 0.06, color = GREY) for i in range(16) for j in range(40)]
        grid = VGroup(lines_h, lines_v)
        arrows = Arrow(ORIGIN, ratio*UP, color = GREEN, buff = 0), Arrow(ORIGIN, ratio*RIGHT, color = BLUE, buff = 0)
        background = VGroup(lines_h.copy().set_stroke(GREY, width = 1), lines_v.copy().set_stroke(GREY, width = 1), axis_x.copy(), axis_y.copy())
        x_mark = Songti("兔数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(RIGHT_SIDE + 14*ratio*RIGHT, UL)
        y_mark = Songti("鸡数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(TOP + 5*ratio*UP, DL)
        example = Dot(5*ratio*UP + 7*ratio*RIGHT, color = YELLOW)
        self.play(FadeIn(grid), ShowCreation(axis_x), ShowCreation(axis_y), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
        self.wait()
        self.play(Write(x_mark), Write(y_mark))
        self.wait()
        self.bring_to_back(background).add(*points, *arrows).play(*[GrowFromCenter(mob) for mob in points])
        self.wait()
        self.play(GrowFromCenter(example), IndicateAround(example))
        self.wait()
        self.play(FadeOut(x_mark), FadeOut(y_mark), FadeOut(example))
        self.wait()
        self.play(*[mob.animate.apply_matrix(np.array([[4, 2], [1, 1]])) for mob in [grid, *arrows]], *[mob.animate.move_to(np.dot(np.array([[4, 2, 0], [1, 1, 0], [0, 0, 0]]), mob.get_center())) for mob in points], run_time = 4)
        self.wait()

        position = 28*ratio*RIGHT + 10*ratio*UP
        line_x = Line(position + 20*ratio*DOWN, position + 10*ratio*UP, color = YELLOW)
        line_y = Line(position + 40*ratio*LEFT, position + 30*ratio*RIGHT, color = YELLOW)
        dot = Dot(position, color = ORANGE)
        x_mark = Songti("腿数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(RIGHT_SIDE + 14*ratio*RIGHT, UL)
        y_mark = Songti("头数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(TOP + 5*ratio*UP, DL)
        example = Dot(5*ratio*UP + 7*ratio*RIGHT)
        region = Polygon(ORIGIN, 20*ratio*(UP+2*RIGHT), 20*ratio*(2*UP+6*RIGHT), 20*ratio*(UP+4*RIGHT), fill_opacity = 0.2, fill_color = YELLOW, stroke_width = 0)
        mark_x = MTex(r"28", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(28*ratio*RIGHT, DOWN)
        mark_y = MTex(r"10", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(10*ratio*UP, LEFT)
        self.play(Write(x_mark), Write(y_mark))
        self.wait()
        self.bring_to_back(region).play(FadeIn(region, remover = True, rate_func = double_there_and_back), run_time = 2)
        self.wait()
        self.add(line_x, line_y, *points, *arrows).play(Write(mark_x), Write(mark_y), GrowFromPoint(line_x, position, run_time = 2), GrowFromPoint(line_y, position, run_time = 2), GrowFromCenter(dot), *[mob.animate.scale(2/3) for mob in points])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [x_mark, y_mark, mark_x, mark_y]])
        self.play(*[mob.animate.apply_matrix(np.array([[0.5, -1], [-0.5, 2]])) for mob in [grid, *arrows, line_x, line_y]], *[mob.animate.move_to(np.dot(np.array([[0.5, -1, 0], [-0.5, 2, 0], [0, 0, 0]]), mob.get_center())) for mob in points + [dot]], run_time = 4)
        self.wait()
        x_mark = Songti("兔数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(RIGHT_SIDE + 14*ratio*RIGHT, UL)
        y_mark = Songti("鸡数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(TOP + 5*ratio*UP, DL)
        mark_x = MTex(r"4", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(4*ratio*RIGHT, DOWN)
        mark_y = MTex(r"6", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(6*ratio*UP, LEFT)
        line_x = Line(4*ratio*RIGHT + 6*ratio*UP, 4*ratio*RIGHT, color = YELLOW)
        line_y = Line(4*ratio*RIGHT + 6*ratio*UP, 6*ratio*UP, color = YELLOW)
        self.add(line_x, line_y, *points, dot, *arrows).play(ShowCreation(line_x), ShowCreation(line_y), Write(mark_x), Write(mark_y), FadeIn(x_mark), FadeIn(y_mark))
        self.wait()
        self.fade_out()
        self.wait()

class Video_10(FrameScene):
    def construct(self):
        box = BlackBox()
        box.set_fill(opacity = 0).set_stroke(width = 10, color = GREY).remove(box[0]).scale(np.array([4, 4, 0]))
        self.fade_in(box)

        texts = r"C_2H_5OH", r"O_2", r"CO_2", r"H_2O"
        formula = MTex(r"{x}C_2H_5OH+{y}O_2 = {z}CO_2+{w}H_2O", isolate = texts, tex_to_color_map = {(r"{x}", r"{y}", r"{z}", r"{w}"): GREEN}).scale(0.8).shift(3*UP)
        parts = [formula.get_part_by_tex(text).set_color(YELLOW) for text in texts]
        formula[:11].shift(0.3*LEFT)
        formula[12:].shift(0.3*RIGHT)
        formula[11].set_width(formula[11].get_width() + 0.6, stretch = True)
        formula.refresh_bounding_box()
        self.play(Write(formula))
        self.wait()

        vector_in = MTex(r"\begin{bmatrix}x\\y\\z\\w\end{bmatrix}", color = GREEN).scale(0.8).move_to(5.6*LEFT)
        self.play(Write(vector_in), *[IndicateAround(formula.get_part_by_tex(text)) for text in [r"{x}", r"{y}", r"{z}", r"{w}"]])
        self.wait()
        texts = r"2\\1\\6", r"0\\2\\0", r"1\\2\\0", r"0\\1\\2"
        vector_1, vector_2, vector_3, vector_4 = [MTex(r"\begin{bmatrix}" + texts[i] + r"\end{bmatrix}", color = YELLOW, tex_to_color_map = {r"0": GREY}).scale(0.8).set_x(parts[i].get_x()).shift(1.5*UP) for i in range(4)]
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in [vector_1, vector_2, vector_3, vector_4]], run_time = 2, lag_ratio = 1/3))
        self.wait()
        rest = MTex(r"x+y=z+w", color = GREEN, tex_to_color_map = {(r"+", r"="): WHITE}).scale(0.8)
        rest.shift((1.5 - rest[3].get_y())*UP)
        rest[0].set_x(vector_1.get_x(LEFT) -0.2, RIGHT), rest[2].set_x(vector_2.get_x(LEFT) -0.2, RIGHT), rest[4].set_x(vector_3.get_x(LEFT) -0.2, RIGHT), rest[6].set_x(vector_4.get_x(LEFT) -0.2, RIGHT)
        rest[1].set_x((vector_1.get_x(RIGHT) + rest[2].get_x(LEFT))/2), rest[3].set_x((vector_2.get_x(RIGHT) + rest[4].get_x(LEFT))/2), rest[5].set_x((vector_3.get_x(RIGHT) + rest[6].get_x(LEFT))/2)
        self.play(Write(rest))
        self.wait()

        vector_out = MTex(r"\begin{bmatrix}0\\0\\0\end{bmatrix}", color = ORANGE).scale(0.8).move_to(5.6*RIGHT)
        texts = r"\begin{bmatrix}2&0&-1&-0\\1&2&-2&-1\\6&0&-0&-2\end{bmatrix}", r"\begin{bmatrix}x\\y\\z\\w\end{bmatrix}", r"=\begin{bmatrix}0\\0\\0\end{bmatrix}"
        matrix = MTex(r"\begin{bmatrix}2&0&-1&-0\\1&2&-2&-1\\6&0&-0&-2\end{bmatrix}\begin{bmatrix}x\\y\\z\\w\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}", tex_to_color_map = {texts[0]: YELLOW, texts[1]: GREEN, (r"0", r"-0"): GREY, texts[2]: ORANGE, r"=": WHITE}).scale(0.8).shift(DOWN)
        parts = [matrix.get_part_by_tex(text) for text in texts]
        anim_0 = TransformFromCopy(vector_1[0], matrix[0])
        anims_1 = AnimationGroup(anim_0, TransformFromCopy(vector_1[1], matrix[1]), TransformFromCopy(vector_1[2], matrix[2]), TransformFromCopy(vector_1[3], matrix[8]), TransformFromCopy(vector_1[4], matrix[14]), follow(vector_1[5:].copy(), anim_0, OverFadeOut))
        self.play(anims_1, run_time = 1)
        self.wait()
        anim_0 = TransformFromCopy(vector_2[2], matrix[3])
        anims_2 = AnimationGroup(anim_0, TransformFromCopy(vector_2[3], matrix[9]), TransformFromCopy(vector_2[4], matrix[15]), *[follow(mob.copy(), anim_0, OverFadeOut) for mob in [vector_2[:2], vector_2[5:]]])
        self.play(anims_2, run_time = 1)
        self.wait()
        anim_0 = TransformFromCopy(vector_3[2], matrix[5])
        anims_3 = AnimationGroup(anim_0, TransformFromCopy(vector_3[3], matrix[11]), TransformFromCopy(vector_3[4], matrix[17]), *[follow(mob.copy(), anim_0, OverFadeOut) for mob in [vector_3[:2], vector_3[5:]]], *[follow(mob, anim_0, OverFadeIn) for mob in [matrix[4], matrix[10], matrix[16]]])
        self.play(anims_3, run_time = 1)
        self.play(*[IndicateAround(mob) for mob in [matrix[4], matrix[10], matrix[16]]])
        self.wait()
        anim_0 = TransformFromCopy(vector_4[2], matrix[7])
        anims_4 = AnimationGroup(anim_0, TransformFromCopy(vector_4[3], matrix[13]), TransformFromCopy(vector_4[4], matrix[19]), TransformFromCopy(vector_4[5], matrix[20]), TransformFromCopy(vector_4[6], matrix[21]), *[follow(mob.copy(), anim_0, OverFadeOut) for mob in [vector_4[:2]]], *[follow(mob, anim_0, OverFadeIn) for mob in [matrix[6], matrix[12], matrix[18]]])
        self.play(anims_4, run_time = 1)
        self.wait()
        self.play(FadeIn(matrix.get_part_by_tex(texts[1]), 0.5*LEFT))
        self.wait()
        self.play(FadeIn(matrix.get_part_by_tex(texts[2]), 0.5*LEFT), Write(vector_out))
        self.wait()

class Video_11(FrameScene):
    def construct(self):
        ratio = 0.4
        head_chicken, head_rabbit, leg_chicken, leg_rabbit = [Talisman("head_chicken.svg", side_color = YELLOW, svg_color = GREEN).scale(ratio), Talisman("head_rabbit.svg", side_color = YELLOW, svg_color = BLUE).scale(ratio), Talisman("leg_chicken.svg", side_color = ORANGE, svg_color = GREEN).scale(ratio), Talisman("leg_rabbit.svg", side_color = ORANGE, svg_color = BLUE).scale(ratio)]
        offset_h = 4.5
        template_c = VGroup(head_chicken.copy().shift(offset_h*LEFT + 3*UP), leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*UP), leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*DOWN))
        template_r = VGroup(head_rabbit.copy().shift(offset_h*RIGHT + 3*UP), *[leg_rabbit.copy().shift(offset_h*RIGHT + 0.5*DOWN + (i-1.5)*UP) for i in range(4)])
        text = VGroup(Heiti("线性").scale(0.8).shift(0.3*UP + 0.2*LEFT), Heiti("映射").scale(0.8).shift(0.3*DOWN + 0.2*RIGHT)).shift(0.5*DOWN)
        box = BlackBox().shift(0.5*DOWN)
        box.set_fill(opacity = 0).remove(box[0]).add(text)
        self.play(FadeIn(template_c, RIGHT), FadeIn(template_r, LEFT), FadeIn(box, 0.5*UP))
        self.wait()

        self.play(FadeOut(template_r), run_time = 0.5, rate_func = rush_into)
        template_r = VGroup(head_chicken.copy().shift(offset_h*RIGHT + 3*UP), leg_chicken.copy().shift(offset_h*RIGHT + 0.5*DOWN + 0.5*UP), leg_chicken.copy().shift(offset_h*RIGHT + 0.5*DOWN + 0.5*DOWN))
        for mob in template_r:
            mob[1].set_color(GREY)
        self.play(FadeIn(template_r), run_time = 0.5, rate_func = rush_from)
        self.wait()

        vectors = MTex(r"\begin{bmatrix}1\\2\end{bmatrix}", color = GREEN).shift(2*UP + LEFT), MTex(r"\begin{bmatrix}1\\2\end{bmatrix}", color = GREY).shift(2*UP + RIGHT)
        self.play(*[Write(mob) for mob in vectors])
        self.wait()

class Patch_11(FrameScene):
    def construct(self):
        bunny = SVGMobject("rabbit.svg", height = 8, color = interpolate_color(BLACK, BLUE, 0.2), stroke_width = 0).shift(8*LEFT)
        human = ImageMobject("human.png", height = 8, opacity = 0.5).shift(5.5*LEFT)
        self.play(FadeIn(bunny, RIGHT))
        self.wait()
        self.play(FadeOut(bunny, run_time = 0.5), rate_func = rush_into)
        self.play(FadeIn(human, run_time = 0.5), rate_func = rush_from)
        self.wait()

class Video_12(FrameScene):
    def construct(self):
        camera = self.camera.frame
        ratio = 0.6
        offset_x = 10*ratio*RIGHT
        offset_y = 4*ratio*UP
        offset = offset_x + offset_y
        camera.shift(offset)
        left, right, up, down = 70*ratio*LEFT, 70*ratio*RIGHT, 40*ratio*DOWN, 40*ratio*UP
        axis_x, axis_y = Line(up, down), Line(left, right)
        lines_h = VGroup(*[Line(left + i*ratio*UP, right + i*ratio*UP, stroke_width = 2, color = BLUE_E) for i in range(-40, 41)])
        lines_v = VGroup(*[Line(up + i*ratio*RIGHT, down + i*ratio*RIGHT, stroke_width = 2, color = BLUE_E) for i in range(-70, 71)])
        points = [Dot(i*ratio*UP + j*ratio*RIGHT, radius = 0.06, color = GREY) for i in range(16) for j in range(40)]
        grid = VGroup(lines_h, lines_v)
        arrows = Arrow(ORIGIN, ratio*UP, color = GREEN, buff = 0), Arrow(ORIGIN, ratio*RIGHT, color = GREY, buff = 0)
        background = VGroup(lines_h.copy().set_stroke(GREY, width = 1), lines_v.copy().set_stroke(GREY, width = 1), axis_x.copy(), axis_y.copy())
        x_mark = Songti("人数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(RIGHT_SIDE + offset_x, UL)
        y_mark = Songti("鸡数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(TOP + offset_y, DL)
        # example = Dot(5*ratio*UP + 7*ratio*RIGHT, color = YELLOW)
        self.play(FadeIn(grid), ShowCreation(axis_x), ShowCreation(axis_y), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
        self.wait()
        self.play(Write(x_mark), Write(y_mark))
        self.wait()
        self.bring_to_back(background).add(*points, *arrows).play(*[GrowFromCenter(mob) for mob in points])
        self.wait()
        # self.play(GrowFromCenter(example), IndicateAround(example))
        # self.wait()
        self.play(FadeOut(x_mark), FadeOut(y_mark))# , FadeOut(example)
        self.wait()
        self.play(*[mob.save_state().animate.apply_matrix(np.array([[2, 2], [1, 1]])) for mob in [grid, *arrows]], *[mob.save_state().animate.move_to(np.dot(np.array([[2, 2, 0], [1, 1, 0], [0, 0, 0]]), mob.get_center())) for mob in points], run_time = 4)
        self.wait()

        x_mark = Songti("腿数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(RIGHT_SIDE + offset_x, UL)
        y_mark = Songti("头数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(TOP + offset_y, DL)
        example = Dot(5*ratio*UP + 7*ratio*RIGHT)
        self.play(Write(x_mark), Write(y_mark))
        self.wait()
        
        example_dots = [Dot(i*ratio*UP + (6-i)*ratio*RIGHT, color = ORANGE) for i in range(7)]
        for dot in example_dots:
            dot.save_state().move_to(np.dot(np.array([[2, 2, 0], [1, 1, 0], [0, 0, 0]]), dot.get_center()))
        self.play(ShowCreation(example_dots[0]))
        self.wait()
        self.play(FadeOut(x_mark), FadeOut(y_mark))
        self.wait()

        self.play(*[mob.animate.restore() for mob in [grid, *arrows] + points + example_dots], run_time = 4)
        self.wait()

        self.play(*[mob.save_state().animate.apply_matrix(np.array([[2, 2], [1, 1]])) for mob in [grid, *arrows]], *[mob.save_state().animate.move_to(np.dot(np.array([[2, 2, 0], [1, 1, 0], [0, 0, 0]]), mob.get_center())) for mob in points + example_dots], run_time = 4)
        self.wait()

        not_dot = Dot(ratio*(3*UP + 8*RIGHT), color = RED)
        equation = MTex(r"\begin{cases}1x+1y = 3\\2x+2y = 8\end{cases}", tex_to_color_map = {r"x": GREEN, r"y": GREY}).shift(ratio*(4*RIGHT + 8*UP)).set_stroke(width = 8, color = BLACK, background = True)
        cross_1, cross_2 = VGroup(Line(equation.get_corner(UL), equation.get_corner(DR), color = RED), Line(equation.get_corner(UR), equation.get_corner(DL), color = RED)), VGroup(Line(not_dot.get_corner(UL), not_dot.get_corner(DR), color = RED), Line(not_dot.get_corner(UR), not_dot.get_corner(DL), color = RED))
        self.play(ShowCreation(not_dot), IndicateAround(not_dot))
        self.wait()
        self.play(Write(equation))
        self.wait()
        self.play(ShowCreation(cross_1), ShowCreation(cross_2))
        self.play(*[FadeOut(mob, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)) for mob in [not_dot, equation, cross_1, cross_2]])
        self.wait()

        # position = 28*ratio*RIGHT + 10*ratio*UP
        # line_x = Line(position + 20*ratio*DOWN, position + 10*ratio*UP, color = YELLOW)
        # line_y = Line(position + 40*ratio*LEFT, position + 30*ratio*RIGHT, color = YELLOW)
        # dot = Dot(position, color = ORANGE)
        # x_mark = Songti("腿数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(RIGHT_SIDE + offset_x, UL)
        # y_mark = Songti("头数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(TOP + offset_y, DL)
        # example = Dot(5*ratio*UP + 7*ratio*RIGHT)
        # mark_x = MTex(r"28", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(28*ratio*RIGHT, DOWN)
        # mark_y = MTex(r"10", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(10*ratio*UP, LEFT)
        # self.play(Write(x_mark), Write(y_mark))
        # self.wait()
        # self.bring_to_back(region).play(FadeIn(region, remover = True, rate_func = double_there_and_back), run_time = 2)
        # self.wait()
        # self.add(line_x, line_y, *points, *arrows).play(Write(mark_x), Write(mark_y), GrowFromPoint(line_x, position, run_time = 2), GrowFromPoint(line_y, position, run_time = 2), GrowFromCenter(dot), *[mob.animate.scale(2/3) for mob in points])
        # self.wait()
        # self.play(*[FadeOut(mob) for mob in [x_mark, y_mark, mark_x, mark_y]])
        # self.play(*[mob.animate.apply_matrix(np.array([[0.5, -1], [-0.5, 2]])) for mob in [grid, *arrows, line_x, line_y]], *[mob.animate.move_to(np.dot(np.array([[0.5, -1, 0], [-0.5, 2, 0], [0, 0, 0]]), mob.get_center())) for mob in points + [dot]], run_time = 4)
        # self.wait()
        # x_mark = Songti("兔数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(RIGHT_SIDE + offset_x, UL)
        # y_mark = Songti("鸡数").scale(0.5).set_stroke(width = 8, color = BLACK, background = True).next_to(TOP + offset_y, DL)
        # mark_x = MTex(r"4", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(4*ratio*RIGHT, DOWN)
        # mark_y = MTex(r"6", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).next_to(6*ratio*UP, LEFT)
        # line_x = Line(4*ratio*RIGHT + 6*ratio*UP, 4*ratio*RIGHT, color = YELLOW)
        # line_y = Line(4*ratio*RIGHT + 6*ratio*UP, 6*ratio*UP, color = YELLOW)
        # self.add(line_x, line_y, *points, dot, *arrows).play(ShowCreation(line_x), ShowCreation(line_y), Write(mark_x), Write(mark_y), FadeIn(x_mark), FadeIn(y_mark))
        # self.wait()
        # self.fade_out()
        # self.wait()

class Video_13(FrameScene):
    def cheese(self, *mobs):
        orientation = self.camera.frame.get_orientation().as_matrix()
        util = lambda t: np.dot(orientation, t)
        for mob in mobs:
            position = mob.get_center()
            mob.restore().apply_function(util, about_point = position)
        return self

    def construct(self):
        
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/4 + 2*DEGREES), quad(RIGHT, PI/2))
        camera.quadternion = quadternion
        camera.set_orientation(Rotation(quadternion)).shift(2*OUT).save_state()# .set_focal_distance(8)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(mob.quadternion, quad(UP, DEGREES*dt))
            mob.set_orientation(Rotation(mob.quadternion))
        camera.add_updater(camera_updater)

        anchors = 5*UP + 2.5*IN, 5*RIGHT + 5*OUT
        plane = Polygon(anchors[0] + anchors[1], anchors[0] - anchors[1], - anchors[0] - anchors[1], - anchors[0] + anchors[1], depth_test = True, side_length = 10, fill_opacity = 0.5, color = BLUE)
        vector_1 = Arrow(ORIGIN, 0.5*np.array([1, 2, 1]), color = GREEN, buff = 0, depth_test = True)
        vector_2 = Arrow(ORIGIN, 0.5*np.array([1, 4, 0]), color = BLUE, buff = 0, depth_test = True)
        coordinate = ThreeDAxes(depth_test = True)
        text = MTex(r"{x}\begin{bmatrix}1\\2\\1\end{bmatrix}+{y}\begin{bmatrix}1\\4\\0\end{bmatrix}", tex_to_color_map = {r"{x}": GREEN, r"{y}": BLUE}).scale(0.8).shift(2.5*UP + 4.5*RIGHT).set_stroke(width = 8, color = BLACK, background = True).fix_in_frame()
        self.shade.fix_in_frame()
        self.fade_in(coordinate, plane, vector_1, vector_2, text)
        self.wait()

        alpha = ValueTracker(0)
        dot = Dot(np.array([-2, 1, 1]), color = ORANGE).save_state().add_updater(lambda mob: self.cheese(mob)).add_updater(lambda mob: mob.set_opacity(alpha.get_value()))
        equation = MTex(r"\begin{cases}1x+1y={-2}\\2x+1y={1}\\1x+0y={1}\end{cases}", tex_to_color_map = {r"x": GREEN, r"y": BLUE, (r"{-2}", r"{1}", r"{1}"): ORANGE}).scale(0.8).shift(2.5*UP + 4*LEFT).set_stroke(width = 8, color = BLACK, background = True).fix_in_frame()
        cross = VGroup(Line(equation.get_corner(UL), equation.get_corner(DR), color = RED), Line(equation.get_corner(UR), equation.get_corner(DL), color = RED)).fix_in_frame()
        self.add(dot).play(alpha.animate.set_value(1), Write(equation))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait(10)
        self.fade_out()

class Shake(Rotate):
    pass

class Loop(FrameScene):
    def construct(self):
        shaft_left = Shaft(4*LEFT + DOWN)
        shaft_right = Shaft(4*RIGHT + DOWN)
        belt = Line(4*LEFT + 0.15*DOWN, 4*RIGHT + 0.15*DOWN).append_points(ArcBetweenPoints(4*RIGHT + 0.15*DOWN, 4*RIGHT + 1.85*DOWN, angle = -PI).get_points()).add_line_to(4*LEFT + 1.85*DOWN).append_points(ArcBetweenPoints(4*LEFT + 1.85*DOWN, 4*LEFT + 0.15*DOWN, angle = -PI).get_points())
        mould = Rectangle(height = 1.5, width = 2.5, fill_opacity = 1, fill_color = BLACK).next_to(0.1*DOWN, UP, buff = 0).shift(2*UP)
        arm = Rectangle(height = 6, width = 1.5, fill_opacity = 1, fill_color = BLACK).next_to(mould, UP, buff = 0)
        mould.add(arm)
        self.shaft = [shaft_left, shaft_right]
        self.mould = mould
        self.on_belt = []
        self.beats: int = 0

        self.add(shaft_left, shaft_right, belt, mould)

        strawberry = SVGMobject("strawberry.svg", fill_color = RED, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        orange = SVGMobject("orange.svg", fill_color = ORANGE, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        lemon = SVGMobject("lemon.svg", fill_color = YELLOW, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        apple = SVGMobject("apple.svg", fill_color = GREEN, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        grape = SVGMobject("grape.svg", fill_color = PURPLE, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        self.fruits = [strawberry, orange, lemon, apple, grape]
        juice_strawberry = SVGMobject("juice.svg", fill_color = RED, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        juice_orange = SVGMobject("juice.svg", fill_color = ORANGE, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        juice_lemon = SVGMobject("juice.svg", fill_color = YELLOW, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        juice_apple = SVGMobject("juice.svg", fill_color = GREEN, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        juice_grape = SVGMobject("juice.svg", fill_color = PURPLE, fill_opacity = 1, stroke_width = 4, stroke_color = BLACK, draw_stroke_behind_fill = True, height = 0.5).next_to(ORIGIN, UP)
        self.juices = [juice_strawberry, juice_orange, juice_lemon, juice_apple, juice_grape]
        
        # fruit_1 = apple.copy()
        # fruit_1.product = juice_apple.copy()
        # self.form(fruit_1)
        # fruit_2 = lemon.copy()
        # fruit_2.product = juice_lemon.copy()
        # self.form(fruit_2)
        # fruit_3 = apple.copy().shift(0.2*LEFT)
        # fruit_3.product = juice_apple.copy().shift(0.2*LEFT)
        # fruit_4 = apple.copy().shift(0.2*RIGHT)
        # fruit_4.product = juice_apple.copy().shift(0.2*RIGHT)
        # fruit_5 = apple.copy().shift(0.3*UP)
        # fruit_5.product = juice_apple.copy().shift(0.3*UP)
        # self.form(fruit_3, fruit_4, fruit_5)
        # fruit_6 = apple.copy().shift(0.2*LEFT)
        # fruit_6.product = juice_apple.copy().shift(0.2*LEFT)
        # fruit_7 = lemon.copy().shift(0.2*RIGHT)
        # fruit_7.product = juice_lemon.copy().shift(0.2*RIGHT)
        # self.form(fruit_6, fruit_7)
        # self.form(*self.arrange([0]))
        self.form(*self.arrange([1]))
        self.form(*self.arrange([2]))
        self.form(*self.arrange([3]))
        self.form(*self.arrange([4]))
        self.form(*self.arrange([0, 0]))
        self.form(*self.arrange([1, 2]))
        self.form(*self.arrange([2, 4]))
        self.form(*self.arrange([3, 1]))
        self.form(*self.arrange([4, 3]))
        
        for _ in range(250):
            t = min((np.log10(self.beats) -1)/2, 0.9)
            mark = random.random()
            if mark <= (1-t)**3:
                number = 1
            else:
                mark -= (1-t)**3
                if mark <= 3*t*(1-t)**2:
                    number = 2
                else:
                    mark -= 3*t*(1-t)**2
                    if mark <= 3*t**2*(1-t):
                        number = 3
                    else:
                        number = 4
            indices = [random.randint(0, 4) for _ in range(number)]
            self.form(*self.arrange(indices))
        for _ in range(5):
            self.form()
        # self.form(*self.arrange([0, 1, 2]))
        # self.form(*self.arrange([2, 3, 4]))
        # self.form()
        # self.form()
        # self.form()
        # self.form()
        # self.form()
    
    def arrange(self, indices: list[int]):
        length = len(indices)
        if length == 1:
            fruit = self.fruits[indices[0]].copy()
            fruit.product = self.juices[indices[0]].copy()
            return [fruit]
        if length == 2:
            fruit_1, fruit_2 = self.fruits[indices[0]].copy().shift(0.2*LEFT), self.fruits[indices[1]].copy().shift(0.2*RIGHT)
            fruit_1.product, fruit_2.product = self.juices[indices[0]].copy().shift(0.2*LEFT), self.juices[indices[1]].copy().shift(0.2*RIGHT)
            return [fruit_1, fruit_2]
        if length == 3:
            fruit_1, fruit_2, fruit_3 = self.fruits[indices[2]].copy().shift(0.3*UP), self.fruits[indices[0]].copy().shift(0.2*LEFT), self.fruits[indices[1]].copy().shift(0.2*RIGHT)
            fruit_1.product, fruit_2.product, fruit_3.product = self.juices[indices[2]].copy().shift(0.3*UP), self.juices[indices[0]].copy().shift(0.2*LEFT), self.juices[indices[1]].copy().shift(0.2*RIGHT)
            return [fruit_1, fruit_2, fruit_3]
        if length == 4:
            fruit_1, fruit_2, fruit_3, fruit_4 = self.fruits[indices[2]].copy().shift(0.3*UP + 0.1*LEFT), self.fruits[indices[3]].copy().shift(0.3*UP + 0.3*RIGHT), self.fruits[indices[0]].copy().shift(0.2*LEFT), self.fruits[indices[1]].copy().shift(0.2*RIGHT)
            fruit_1.product, fruit_2.product, fruit_3.product, fruit_4.product = self.juices[indices[2]].copy().shift(0.3*UP + 0.1*LEFT), self.juices[indices[3]].copy().shift(0.3*UP + 0.3*RIGHT), self.juices[indices[0]].copy().shift(0.2*LEFT), self.juices[indices[1]].copy().shift(0.2*RIGHT)
            return [fruit_1, fruit_2, fruit_3, fruit_4]
        return []

    def timer(self):
        self.beats += 1
        return int(1800/123*self.beats) - int(1800/123*(self.beats-1))

    def form(self, *mobs):
        for mob in mobs:
            mob.counter = -3
            self.on_belt.append(mob)
            self.add(mob)
            if not hasattr(mob, "product") or mob.product is None:
                mob.product = mob
        self.add(self.mould)
        anims = []
        old = self.on_belt
        self.on_belt = []
        for mob in old:
            mob.counter += 1
            if mob.counter == -2:
                mob.shift(4*LEFT)
                anims.append(FadeIn(mob, 2*RIGHT))
            elif mob.counter == 3:
                anims.append(FadeOut(mob, 2*RIGHT))
                continue
            else:
                anims.append(mob.animate.shift(2*RIGHT))
            self.on_belt.append(mob)
        frames = self.timer()
        self.play(*anims, *[Rotate(mob, -1.25) for mob in self.shaft], rate_func = linear, run_time = frames/60, frames = frames)
        frames = self.timer()
        anims = [Rotate(mob, about_point = mob.get_corner(DR), angle = -PI/12) for mob in self.on_belt]
        if not anims:
            anims = [Animation(VMobject())]
        self.play(*anims, rate_func = squish_rate_func(lambda t: 1-abs(2*t-1), 0, 0.5), run_time = frames/60, frames = frames) #squish_rate_func(there_and_back, 0, 0.5) #lambda t: 1-abs(2*t-1)
        frames = self.timer()
        self.play(self.mould.animate.shift(2*DOWN), run_time = frames/60, frames = frames, rate_func = squish_rate_func(rush_into, 0, 0.5))
        for mob in self.on_belt:
            if mob.counter == 0:
                mob.become(mob.product)
        frames = self.timer()
        self.play(self.mould.animate.shift(2*UP), run_time = frames/60, frames = frames, rate_func = squish_rate_func(rush_from, 0, 0.5))


"""
class Video_8(FrameScene):
    def construct(self):
        pass

class Video_9(FrameScene):
    def construct(self):
        texts = r"C_2H_5OH", r"O_2", r"CO_2", r"H_2O"
        formula = MTex(r"{x}C_2H_5OH+{y}O_2 = {z}CO_2+{w}H_2O", isolate = texts, tex_to_color_map = {(r"{x}", r"{y}", r"{z}", r"{w}"): YELLOW}).shift(1.5*UP)
        parts = [formula.get_part_by_tex(text).set_color(GREEN) for text in texts]
        formula[:11].shift(0.3*LEFT)
        formula[12:].shift(0.3*RIGHT)
        formula[11].set_width(formula[11].get_width() + 0.6, stretch = True)
        formula.refresh_bounding_box()
        self.play(Write(formula))
        self.wait()
        box = BlackBox().shift(DOWN)
        text = VGroup(Heiti("线性").scale(0.8).shift(0.3*UP + 0.2*LEFT), Heiti("映射").scale(0.8).shift(0.3*DOWN + 0.2*RIGHT)).shift(DOWN)
        self.play()
        self.wait()

        texts = r"2\\1\\6", r"0\\2\\0", r"1\\2\\0", r"0\\1\\2"
        vectors = [MTex(r"\begin{bmatrix}" + texts[i] + r"\end{bmatrix}", color = GREEN).scale(0.8).set_x(parts[i].get_x()).shift(3*UP) for i in range(4)]
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in vectors]))
        self.wait()

        vector_1 = MTex(r"\begin{bmatrix}x\\y\\z\\w\end{bmatrix}", color = YELLOW).scale(0.8).next_to(2*LEFT + DOWN, LEFT)
        text_1, text_2 = r"\begin{bmatrix}2{x}+0{y}-1{z}-0{w}\\1{x}+2{y}-2{z}-1{w}\\6{x}+0{y}-0{z}-2{w}\end{bmatrix}", r"=\begin{bmatrix}0\\0\\0\end{bmatrix}"
        mtex_2 = MTex(text_1 + text_2, isolate = [text_1, text_2], tex_to_color_map = {(r"{x}", r"{y}", r"{z}", r"{w}"): YELLOW, (r"1", r"2", r"6", r"0"): GREEN, re.compile(r"0{.}"): GREY}).scale(0.8).next_to(2*RIGHT + DOWN, RIGHT)
        vector_2, result = mtex_2.get_part_by_tex(text_1), mtex_2.get_part_by_tex(text_2)
        self.play(Write(vector_1))
        self.wait()
        middle = vector_1.copy()
        self.bring_to_back(middle).play(middle.animate.move_to(LEFT + DOWN).scale(0.5), rate_func = rush_into)
        middle.become(vector_2).move_to(RIGHT + DOWN).scale(0.5)
        self.play(ReplacementTransform(middle, vector_2), rate_func = rush_from)
        self.wait()

        offset = vector_2.get_x(RIGHT) - result.get_x(RIGHT)
        result.set_x(vector_2.get_x(RIGHT), RIGHT)
        shade = BackgroundRectangle(result, fill_opacity = 1, buff = 0.2)
        self.bring_to_back(result, shade).play(*[mob.animate.shift(offset*RIGHT) for mob in [vector_2, vector_1, box, text, shade]])
        self.wait()

class Video_10(FrameScene):
    def construct(self):
    
        ratio = 0.4
        head_chicken, head_rabbit, leg_chicken, leg_rabbit = [Talisman("head_chicken.svg", side_color = YELLOW, svg_color = GREEN).scale(ratio), Talisman("head_rabbit.svg", side_color = YELLOW, svg_color = BLUE).scale(ratio), Talisman("leg_chicken.svg", side_color = ORANGE, svg_color = GREEN).scale(ratio), Talisman("leg_rabbit.svg", side_color = ORANGE, svg_color = BLUE).scale(ratio)]
        offset_h = 4.5
        template_h_c = head_chicken.copy().shift(offset_h*LEFT + 3*UP)
        template_l_c = VGroup(leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*UP), leg_chicken.copy().shift(offset_h*LEFT + 0.5*DOWN + 0.5*DOWN))
        template_h_r = head_rabbit.copy().shift(offset_h*RIGHT + 3*UP)
        template_l_r = VGroup(*[leg_rabbit.copy().shift(offset_h*RIGHT + 0.5*DOWN + (i-1.5)*UP) for i in range(4)])
        box = BlackBox()
        text = VGroup(Heiti("线性").scale(0.8).shift(0.3*UP + 0.2*LEFT), Heiti("映射").scale(0.8).shift(0.3*DOWN + 0.2*RIGHT))
        self.play(*[FadeIn(mob, RIGHT) for mob in [template_h_c, *template_l_c]], *[FadeIn(mob, LEFT) for mob in [template_h_r, *template_l_r]], *[FadeIn(mob, 0.5*UP) for mob in [box, text]])
        self.wait()

        color_map = {r"{x}": GREEN, r"{y}": BLUE}
        vector_1 = MTex(r"\begin{bmatrix}{x}\\{y}\end{bmatrix}", tex_to_color_map = color_map).scale(0.8).next_to(2*LEFT, LEFT)
        vector_2 = MTex(r"\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}", tex_to_color_map = {r"1{x}+1{y}": YELLOW, r"2{x}+4{y}": ORANGE, **color_map}).scale(0.8).next_to(2*RIGHT, RIGHT)
        self.play(Write(vector_1))
        self.wait()
        middle = vector_1.copy()
        self.bring_to_back(middle).play(middle.animate.move_to(LEFT).scale(0.5), rate_func = rush_into)
        middle.become(vector_2).move_to(RIGHT).scale(0.5)
        self.play(ReplacementTransform(middle, vector_2), rate_func = rush_from)
        self.wait()
        
        box.set_fill(opacity = 0).remove(box[0])
        def util(t: float):
            if t < 1/3:
                return 2/3*smooth(1.5*t)
            else:
                return 1-4/3*(1-smooth(1-0.75*(1-t)))
        self.add(template_h_c, template_l_c, template_h_r, template_l_r).play(*[mob.animate.scale(2/3, about_point = 3*UP) for mob in [template_h_c, template_l_c, template_h_r, template_l_r]], *[OverFadeOut(mob, scale = 4, over_factor = 3, about_point = ORIGIN) for mob in [text, vector_1, vector_2]], box.animate.scale(4, about_point = ORIGIN).set_stroke(width = 10, color = GREY), run_time = 3, rate_func = util)
        self.wait()

        texts = [r"\begin{bmatrix}1\\2\end{bmatrix}", r"\begin{bmatrix}1\\4\end{bmatrix}", r"=\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}"]
        formula = MTex(r"{x}\begin{bmatrix}1\\2\end{bmatrix}+{y}\begin{bmatrix}1\\4\end{bmatrix}=\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}", isolate = texts + [r"+{y}"], tex_to_color_map = {r"{x}": BLUE, r"{y}": GREEN, r"1": YELLOW, (r"2", r"4"): ORANGE}).shift(3*UP)
        vector_1, vector_2 = formula.get_part_by_tex(texts[0]), formula.get_part_by_tex(texts[1])
        self.play(*[mob.animating(path_arc = PI/2).set_x(vector_1.get_x()).shift(1.5*DOWN) for mob in [template_h_c, template_l_c]], Write(vector_1))
        self.wait()
        self.play(*[mob.animating(path_arc = -PI/3).set_x(vector_2.get_x()).shift(1.5*DOWN) for mob in [template_h_r, template_l_r]], Write(vector_2))
        self.wait()

        vector_in = MTex(r"\begin{bmatrix}{x}\\{y}\end{bmatrix}", tex_to_color_map = color_map).scale(0.8).move_to(5.6*LEFT)
        self.play(Write(vector_in))
        self.wait()
        parameters = VGroup(formula.get_part_by_tex(r"{x}"), formula.get_part_by_tex(r"+{y}"))
        self.play(Write(parameters))
        self.wait()

        rest = formula.get_part_by_tex(texts[2])
        rest.save_state().set_x(vector_2.get_x(RIGHT), RIGHT)
        vector_out = MTex(r"\begin{bmatrix}1{x}+1{y}\\2{x}+4{y}\end{bmatrix}", tex_to_color_map = {r"1": YELLOW, (r"2", r"4"): ORANGE, **color_map}).scale(0.8).move_to(5.6*RIGHT)
        shade = BackgroundRectangle(rest, fill_opacity = 1)
        self.bring_to_back(rest, shade).play(rest.animate.restore(), Write(vector_out))
        self.wait()

        title = Title("线性组合").shift(UP)
        titleline = TitleLine()
        self.play(title.animate.shift(DOWN), GrowFromPoint(titleline, 4*UP), box.animate.scale(np.array([1, 0.75, 1])), *[mob.animate.shift(DOWN) for mob in [formula]], *[FadeOut(mob, DOWN) for mob in [template_h_c, template_l_c, template_h_r, template_l_r]])
        self.wait()

        self.play(IndicateAround(vector_1))
        self.wait()

"""

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]