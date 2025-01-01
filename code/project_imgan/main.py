import numpy as np
from manim import *
import numpy as np
import math

class Video1(Scene):
    def construct(self):
        eq1 = MathTex(r"(-2)",r"\times","(-2)"," = 4", tex_to_color_map={"(-2)": RED, "4": GREEN}).scale(1.2).shift(UP*2)
        eq2 = MathTex("x",r"\times","x", r"\geq 0", tex_to_color_map={"x": BLUE, r"\geq 0": GREEN}).scale(1.2).next_to(eq1, DOWN, buff=1)
        self.play(Write(eq1))
        self.wait(2)
        self.play(
            LaggedStart(
            TransformFromCopy(eq1[0], eq2[0]),
            TransformFromCopy(eq1[1], eq2[1]),
            TransformFromCopy(eq1[2], eq2[2]),
            TransformFromCopy(eq1[3], eq2[3])
            ), run_time=2
        )
        self.wait(2)

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 8, 1],
            x_length=6,
            y_length=7.5,
            background_line_style={
                "stroke_color": WHITE,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            },
            axis_config={"color": TEAL,
                         "stroke_width": 5,
                         }
        ).to_edge(LEFT, buff=1)
        plane.add_coordinates()
        self.play(
            eq1.animate.shift(RIGHT*4),
            eq2.animate.shift(RIGHT*4),
            Create(plane),
            run_time=2
        )
        quadr_curve = plane.plot(lambda x: x**2, x_range=[-2.7, 2.7], color=RED)
        self.wait(2)
        self.play(Create(quadr_curve))
        self.wait(2)
        lbl = MathTex("y = x^2", color=YELLOW).next_to(quadr_curve, RIGHT, buff=0.5).shift(UP*3).set_stroke(width=4, background=True)
        self.play(Write(lbl))
        self.wait(2)

        rect = Rectangle(width=6, height=6, color=BLUE, fill_opacity=0.5).move_to(plane.coords_to_point(0, 4))
        self.play(FadeIn(rect))
        self.wait()
        self.play(Indicate(rect))
        self.wait(2)

        m1_line = DashedLine(plane.coords_to_point(-5, -1), plane.coords_to_point(5, -1), color=YELLOW, stroke_width=4)
        y_eq_minus1 = MathTex("y = -1", color=RED).next_to(m1_line, UP+RIGHT, buff=0.2).set_stroke(width=4, background=True)
        self.play(Create(m1_line))
        self.play(Write(y_eq_minus1))
        self.wait(2)

        xsq_eq_m1 = MathTex("x^2 = -1", tex_to_color_map={"x": BLUE, "-1": RED}).next_to(eq2, DOWN, buff=1.5).align_to(eq2, LEFT)
        no_solu = Text("无解").next_to(xsq_eq_m1, RIGHT, buff=0.2)
        xsq_noslu = VGroup(xsq_eq_m1, no_solu)
        self.play(Write(xsq_noslu))
        self.wait(2)

        self.play(
            FadeOut(eq1),
            FadeOut(eq2),
            xsq_noslu.animate.shift(UP*3.5),
        )
        self.wait(2)

        idef = MathTex(r"x=\sqrt{-1}", tex_to_color_map={"x":YELLOW}).scale(1.2).next_to(xsq_noslu, DOWN, buff=1)
        self.play(Write(idef))
        self.wait(2)

class Video0(Scene):
    def construct(self):
        text = Text("没有意义", font="heiti", color=YELLOW).scale(1.8)
        eq1 = MathTex(r"\sqrt{-1}", tex_to_color_map={"-1": BLUE}).scale(1.5).shift(UP*2.5+LEFT*3.5)
        eq2 = MathTex(r"1\div 0", tex_to_color_map={"-1": ORANGE}).scale(1.5).shift(UP*2.5+RIGHT*3.5)
        eq3 = MathTex(r"\arcsin(-2)", tex_to_color_map={"-2": GREEN}).scale(1.5).shift(DOWN*2.5+LEFT*3.5)
        eq4 = MathTex(r"\ln(-1)", tex_to_color_map={"0": YELLOW}).scale(1.5).shift(DOWN*2.5+RIGHT*3.5)
        self.play(Write(text))
        self.wait(1.5)

        self.play(LaggedStart(
            Write(eq1),
            Write(eq2),
            Write(eq3),
            Write(eq4),
        ), run_time=2, lag_ratio=0.5)
        self.wait(2)

        self.play(
            eq2.animate.scale(1.5),
            eq1.animate.set_opacity(0.2),
            eq3.animate.set_opacity(0.2),
            eq4.animate.set_opacity(0.2),
        )
        self.wait(1.5)

        # a RED cross
        cross = Cross(eq2, color=PURE_RED)
        self.play(Create(cross))
        self.wait(2)
        self.play(eq1.animate.set_opacity(1).scale(1.5))
        self.wait()

        eq_i = MathTex(r"= i", tex_to_color_map={"i": BLUE}).scale(2.3).next_to(eq1, RIGHT, buff=0.2)
        self.play(Write(eq_i))
        self.wait(2)

        tick = MathTex(r"\checkmark", color=GREEN).scale(4).move_to(eq_i).shift(DOWN*0.4)
        self.play(Write(tick))

        self.wait(2)
        ques_mark = MathTex(r"?", color=ORANGE).scale(5).set_stroke(width=5, background=True)
        self.play(Write(ques_mark))
        self.wait(2)
        

class Video7(Scene):
    def construct(self):
        eq = MathTex(r"x^3=px+q", color=BLUE).scale(1.5).shift(UP*2)
        cardano = MathTex(r"x = \sqrt[3]{\frac{q}{2}+\sqrt{\frac{q^2}{4}-\frac{p^3}{27}}}+\sqrt[3]{\frac{q}{2}-\sqrt{\frac{q^2}{4}-\frac{p^3}{27}}}", color=RED).next_to(eq, DOWN, buff=1)
        self.play(Write(eq))
        self.wait(2)
        self.play(Write(cardano))
        self.wait()
        title = Text("卡尔达诺公式", color=YELLOW).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7, color=WHITE).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), GrowFromCenter(line))
        self.wait(2)

        p15q4 = MathTex(r"p=15, q=4", color=GREEN).next_to(eq, RIGHT, buff=1)
        self.play(Write(p15q4), eq.animate.shift(LEFT*2))
        self.wait()
        _eq = MathTex(r"x^3=15x+4", color=YELLOW).scale(1.5).move_to(eq).align_to(eq, LEFT)
        self.play(TransformMatchingShapes(eq, _eq))
        self.wait(2)

        plug_value_cardano = MathTex(r"x = \sqrt[3]{\frac{4}{2}+\sqrt{\frac{4^2}{4}-\frac{15^3}{27}}}+\sqrt[3]{\frac{4}{2}-\sqrt{\frac{4^2}{4}-\frac{15^3}{27}}}", color=RED).move_to(cardano)
        self.play(TransformMatchingShapes(cardano, plug_value_cardano))
        final_eq = MathTex(r"\sqrt[3]{2+\sqrt{-121}}-\sqrt[3]{2-\sqrt{-121}}", color=TEAL).move_to(cardano)
        self.wait(2)
        self.play(TransformMatchingShapes(plug_value_cardano, final_eq))
        self.wait(2)

        # Create surrounding rectangles around the two sqrt{-121}
        rect1 = SurroundingRectangle(final_eq[0][5:7], color=YELLOW, buff=0.1)
        rect2 = SurroundingRectangle(final_eq[0][17:19], color=YELLOW, buff=0.1)

        self.play(Create(rect1), Create(rect2))
        self.wait(2)

        xeq4 = MathTex(r"4^3=15\times 4+4").next_to(_eq, RIGHT, buff=1)
        self.play(FadeOut(p15q4))
        self.play(Write(xeq4))
        self.wait(4)

        self.play(FadeOut(rect1), FadeOut(rect2))

        eq2 = MathTex(r"\ \sqrt[3]{2+11\sqrt{-1}}","+",r"\sqrt[3]{2-11\sqrt{-1}}", color=TEAL).move_to(final_eq)
        self.play(TransformMatchingShapes(final_eq, eq2))

        final_result = MathTex(r"=2+",r"\sqrt{-1}","+2",r"-\sqrt{-1}", color=TEAL).next_to(eq2, DOWN, buff=0.4).align_to(eq2, LEFT)
        self.play(Write(final_result))
        self.wait(2)

        cancel_line1 = Line(final_result[1].get_corner(UL), final_result[1].get_corner(DR), color=PURE_RED)
        cancel_line2 = Line(final_result[3].get_corner(UL), final_result[3].get_corner(DR), color=PURE_RED)
        self.play(Create(cancel_line1), Create(cancel_line2))
        self.wait()

        eqto4 = MathTex(r"=4", color=RED).next_to(final_result, DOWN, buff=0.4).align_to(final_result, LEFT)
        rect = SurroundingRectangle(eqto4, color=YELLOW, buff=0.1)
        self.play(Write(eqto4))
        self.wait(2)
        self.play(Create(rect))
        self.wait(2)



class Jumping(Scene):
    def construct(self):
        line = NumberLine(x_range=[-8, 8, 1], include_numbers=True, include_tip=True, include_ticks=True).shift(DOWN)
        self.play(Create(line))

        value = ValueTracker(1)

        dot = Dot(color=RED, radius=0.1).add_updater(lambda x: x.move_to(line.n2p(value.get_value())))
        self.play(FadeIn(dot))

        upd_val = [2, 3, -1, -5, -3, -2, 6, -3]

        whole_eq = VGroup(MathTex("x=1", color=YELLOW).shift(UP*2.5+LEFT*3.5))
        self.play(Write(whole_eq))
        self.wait()
        for val in upd_val:
            if val > 0:
                s = "+"+str(val)
            else:
                s = str(val)
            new_term = MathTex(s, color=ORANGE if val > 0 else BLUE).next_to(whole_eq[-1], RIGHT, buff=0.2)
            new_val = value.get_value() + val
            arr = Arrow(dot.get_center() + UP*0.2, line.n2p(new_val)+ UP*0.2, color=ORANGE, buff=0.05)
            calc = MathTex(s, color=BLUE).next_to(arr, UP, buff=0.3)
            self.play(Create(arr), Write(calc), Write(new_term))
            self.play(value.animate.set_value(value.get_value()+val), 
                      FadeOut(arr), FadeOut(calc), run_time=1)
            self.wait(0.5)
            whole_eq.add(new_term)
        self.wait(2)
        


class Video5(Scene):
    def construct(self):
        time = ValueTracker(0)
        icon1 = VGroup()
        cord1 = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
        ).shift(LEFT*4 + UP*2)
        
        # self.play(Create(cord1))
        # self.wait(2)
        square = Square(side_length=3, color=BLUE).move_to(cord1.coords_to_point(0, 0)).set_fill(color=GREEN, opacity=0.3)
        sq1 = Square(side_length=1, color=WHITE, fill_opacity=0.7).set_fill(color=GOLD).move_to(cord1.coords_to_point(0, 0))
        tri1 = Polygon(cord1.coords_to_point(-1, 1), cord1.coords_to_point(-1, 3), cord1.coords_to_point(3, 1), color=ORANGE, fill_opacity=0.7).set_fill(color=BLUE).set_stroke(width=1)
        tri2 = Polygon(cord1.coords_to_point(-1, -1), cord1.coords_to_point(-3, -1), cord1.coords_to_point(-1, 3), color=ORANGE, fill_opacity=0.7).set_fill(color=BLUE).set_stroke(width=1)
        tri3 = Polygon(cord1.coords_to_point(1, -1), cord1.coords_to_point(1, -3), cord1.coords_to_point(-3, -1), color=ORANGE, fill_opacity=0.7).set_fill(color=BLUE).set_stroke(width=1)
        tri4 = Polygon(cord1.coords_to_point(1, 1), cord1.coords_to_point(3, 1), cord1.coords_to_point(1, -3), color=ORANGE, fill_opacity=0.7).set_fill(color=BLUE).set_stroke(width=1)
        icon1.add(square, sq1, tri1, tri2, tri3, tri4)
        self.wait(2)
        self.play(FadeIn(icon1), run_time=0.5)
        self.wait(0.5)

        # icon1.add_updater(lambda x: x.move_to(cord1.c2p(0, 0.5*math.cos(time.get_value()*PI/2)-0.5)))
        # self.play(time.animate.set_value(8), run_time=8, rate_func=linear)

        icon2 = VGroup()

        cord2 = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
        ).shift(RIGHT*4 + UP*2)

        cir = Circle(radius=1.5, color=WHITE, fill_opacity=0).move_to(cord2.coords_to_point(0, 0))
        hedra = Polygon(*[cord2.c2p(3*np.cos(PI*i/6), 3*np.sin(PI*i/6)) for i in range(12)], color=BLUE, fill_opacity=0.5).move_to(cord2.coords_to_point(0, 0)).set_stroke(width=2)
        lines = VGroup(*[Line(cord2.c2p(0,0), cord2.c2p(3*np.cos(PI*i/6), 3*np.sin(PI*i/6)), color=ORANGE).set_stroke(width=2) for i in range(12)])
        icon2.add(cir, hedra, lines)
        
        self.play(FadeIn(icon2), run_time=0.5)
        self.wait(0.5)

        icon3 = VGroup()
        linear_eq = MathTex(r"\begin{cases} 3x+2y+z=39 \\ 2x+3y+z=34 \\ x+2y+3z=26 \end{cases}", color=BLUE).shift(LEFT*4 + DOWN*2)
        icon3.add(linear_eq)
        self.play(FadeIn(icon3), run_time=0.5)
        self.wait(0.5)

        icon4 = VGroup()
        cord4 = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
        ).shift(RIGHT*4 + DOWN*2)

        tri = Polygon(cord4.coords_to_point(-3, 0), cord4.coords_to_point(3, 0), cord4.coords_to_point(2, 4), color=WHITE, fill_opacity=0.5).set_fill(color=BLUE).set_stroke(width=2)
        a_sign = MathTex("a", color=ORANGE).move_to(cord4.c2p(0, -0.5))
        b_sign = MathTex("b", color=GREEN).move_to(cord4.c2p(-1.5, 2))
        c_sign = MathTex("c", color=RED).move_to(cord4.c2p(3, 2))
        Helen_formula = MathTex(r"S=\frac{1}{4}\sqrt{(a+b+c)(a+b-c)(b+c-a)(c+a-b)}", color=YELLOW).scale(0.4).next_to(tri, DOWN, buff=0.5)
        icon4.add(tri, a_sign, b_sign, c_sign, Helen_formula)
        self.play(FadeIn(icon4), run_time=0.5)
        self.wait(4)

        minus_num = MathTex(r"-3", color=MAROON).scale(4).set_stroke(width=5, background=True)
        self.play(Write(minus_num))
        rect = SurroundingRectangle(minus_num, color=YELLOW, buff=0.1)
        self.wait(2)
        self.play(Create(rect))
        self.wait(4)

class Video11(Scene):
    def construct(self):
        #     理解了人类为什么要定义i等于根号-1，我们也终于能明白为什么1/0不能享受“强行定义结果”这样的待遇。
        b_def = MathTex(r"b=1\div 0", tex_to_color_map={"b": RED}).scale(1.5).shift(UP*2)
        # 这在毕导的视频里也有提到，一旦定义了1/0=b，那么b×0就等于1，
        timebeq0 = MathTex(r"b\times 0=1", tex_to_color_map={"b": RED, "1": GREEN}).scale(1.5).next_to(b_def, DOWN, buff=0.5)
        self.play(Write(b_def))
        self.wait(2)
        self.play(Write(timebeq0))
        self.wait(2)
        # 我们在两边同乘以任何一个数a，左边先算0×a的0，就会得到1=a。
        timea = MathTex(r"b\times 0\times a=1\times a", tex_to_color_map={"b": RED, "1": GREEN, "a":BLUE}).scale(1.5).next_to(timebeq0, DOWN, buff=0.5)
        # 也就是说所有的数字都等于1，进而0也等于1。
        timea_tmp1 = MathTex(r"b\times (0\times a)=1\times a", tex_to_color_map={"b": RED, "1": GREEN, "a":BLUE}).scale(1.5).next_to(timebeq0, DOWN, buff=0.5)
        timea_tmp2 = MathTex(r"b\times 0=a", tex_to_color_map={"b": RED, "a": BLUE}).scale(1.5).next_to(timebeq0, DOWN, buff=0.5)
        timea_tmp3 = MathTex(r"1=a", tex_to_color_map={"a": BLUE}).scale(1.5).next_to(timebeq0, DOWN, buff=0.5)
        self.play(Write(timea))
        self.wait(2)
        self.play(TransformMatchingShapes(timea, timea_tmp1))
        self.wait(2)
        self.play(TransformMatchingShapes(timea_tmp1, timea_tmp2))
        self.wait(2)
        rect = SurroundingRectangle(timebeq0, color=YELLOW, buff=0.1)
        self.play(Create(rect))
        self.wait()
        self.play(TransformMatchingShapes(timea_tmp2, timea_tmp3))
        self.wait()
        self.play(FadeOut(rect))
        self.wait()

        aeq0 = MathTex(r"a=0", tex_to_color_map={"a": BLUE}).scale(1.5).next_to(timea_tmp3, RIGHT, buff=1.5)
        zeroeq1 = MathTex(r"0=1", tex_to_color_map={"0": BLUE, "1": GREEN}).scale(1.5).next_to(timea_tmp3, DOWN, buff=0.5)
        self.play(Write(aeq0))
        self.wait()
        self.play(Write(zeroeq1))
        self.wait(2)
        # 也就是说，强行容纳1/0存在一个假想结果b，并没有像虚数单位i那样兼容原来的数学系统和运算，
        # 并在此基础上开创出更多优美的知识和工具。
        rect = SurroundingRectangle(b_def, color=YELLOW, buff=0.1)
        self.play(Create(rect))
        self.wait()
        self.play(FadeOut(rect))
        self.wait()
        # 相反，它反手炸了整个数学大厦，在这个世界里，只剩下孤零零的两个对象：0和b，
        huge_0 = MathTex(r"0", color=BLUE).scale(8).set_stroke(width=5, background=True).shift(LEFT*3)
        huge_b = MathTex(r"b", color=RED).scale(8).set_stroke(width=5, background=True).shift(RIGHT*3)
        self.play(
            *[mobj.animate.set_opacity(0.2) for mobj in [b_def, timebeq0, timea_tmp3, aeq0, zeroeq1]],
            FadeIn(huge_0),
            FadeIn(huge_b),
            run_time=1.5
        )
        self.wait(2)
        # 根本没有多余的数字可言。你可以接受1/0，
        # 但代价是，为了接纳并且兼容这个结果，整个数学体系空无一物，所以被舍弃了。
        # 这才是我们不接受1/0有任何结果最根本的原因。