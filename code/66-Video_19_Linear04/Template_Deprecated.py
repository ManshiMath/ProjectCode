from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Video_1(FrameScene):
    def construct(self):

        def indicate_line(start, end, color = YELLOW, **kwargs):
            return Line(start, end).animating(rate_func = there_and_back, remover = True).scale(1.2).set_color(color)
        
        p1_A = np.array([1, 1.5, 0])
        p1_B = np.array([2.5, -1.5, 0])
        p1_C = np.array([-2.5, -1.5, 0])
        p1_H = np.array([1, -1.5, 0])

        triangle_1 = Polygon(p1_A, p1_B, p1_C, fill_color = YELLOW)
        height_line1 = Line(p1_A, p1_H)
        elbow = Elbow().shift(p1_H)
        height_1 = VGroup(height_line1, elbow)

        label_base = MTex(r"w", color = GREEN).move_to((p1_B+p1_C)/2).shift(0.4*DOWN)
        label_height = MTex(r"h", color = BLUE).move_to(height_line1.get_center()).shift(0.3*LEFT)
        text_area = MTex(r"S=\frac{wh}{2}", tex_to_color_map = {r"S": YELLOW, r"w": GREEN, r"h": BLUE}).shift(2.5*UP)

        self.wait(0, 12) #（空闲）
        self.play(ShowCreation(triangle_1))
        self.play(ShowCreation(height_1))
        self.wait(1, 7) #三角形的面积计算公式想必大家都很熟悉了

        self.play(Write(text_area), triangle_1.animate.set_fill(opacity = 0.2), indicate_line(p1_B, p1_C, GREEN), FadeIn(label_base), indicate_line(p1_A, p1_H, BLUE, run_time = 1.5, squish_interval = (1/3, 1)), FadeIn(label_height, run_time = 1.5, squish_interval = (1/3, 1)))
        self.wait(1+0-1, 13+25-15) #底乘高除以2 （空闲）
        offset = 2.5*DOWN + 6*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 5.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p2_A = offset + np.array([5, 2, 0])
        p2_B = offset + np.array([2, 4, 0])
        p2_C = offset
        p2_H = offset + np.array([5, 2, 0])*18/29
        alpha = ValueTracker(0.0)
        def height_updater(mob: VGroup):
            value = alpha.get_value()
            p_A, p_B, p_C = interpolate(p1_A, p2_B, value), interpolate(p1_B, p2_A, value), interpolate(p1_C, p2_C, value)
            p_A -= p_C
            p_B -= p_C
            p_H = np.dot(p_A, p_B)/np.dot(p_B, p_B)*p_B + p_C
            mob[0].put_start_and_end_on(p_A + p_C, p_H)
            angle = np.arctan(p_B[1]/p_B[0])
            mob[1].become(Elbow().rotate(angle, about_point = ORIGIN).shift(p_H))
            mob[2].move_to(p_B/2 + p_C).shift(0.4*unit(angle-PI/2))
            mob[3].move_to(mob[0]).shift(-0.3*unit(angle))
        changing_group = VGroup(height_line1, elbow, label_base, label_height).add_updater(height_updater)
        self.bring_to_back(axis_x, axis_y).add(changing_group).play(alpha.animate.set_value(1), FadeIn(axis_x, offset - p1_C), FadeIn(axis_y, offset - p1_C), Transform(triangle_1, Polygon(p2_B, p2_A, p2_C, fill_color = YELLOW)), run_time = 2)
        changing_group.clear_updaters()
        self.wait(0, 15) #但如果把三角形放到坐标系里面

        label_A = MTex(r"A(a, b)").next_to(p2_A, DOWN).set_stroke(**stroke_dic)
        label_B = MTex(r"B(c, d)").next_to(p2_B, UP).set_stroke(**stroke_dic)
        label_O = MTex(r"O").next_to(p2_C, UL)
        label_H = MTex(r"H").next_to(p2_H, DOWN)
        self.play(*[Write(mob) for mob in [label_A, label_B, label_O, label_H]])
        self.wait(0, 19) #这个公式就不那么好用了
        self.wait(0, 23) #（空闲）

        tex_1 = MTex(r"H\ (\,\frac{ac+bd}{a^2+b^2}a,\ \frac{ac+bd}{a^2+b^2}b\,)").scale(0.8).shift(3.5*RIGHT + 1.5*UP)
        tex_2 = MTex(r"h=\frac{|ad-bc|}{\sqrt{a^2+b^2}}", tex_to_color_map = {r"h": BLUE}).scale(0.8).shift(3.5*RIGHT + 0*UP)
        tex_3 = MTex(r"S=\frac{1}{2}wh=\frac{1}{2}|ad-bc|", tex_to_color_map = {r"S": YELLOW, r"w": GREEN, r"h": BLUE}).scale(0.8).shift(3.5*RIGHT + 1.5*DOWN)
        self.play(Write(VGroup(tex_1, tex_2, tex_3)), run_time = 4)
        self.wait(1+1+1-4, 11+15+22) #我们倒是也可以给它作高 再把底和高都算出来 最后求得面积
        # self.play(tex_3[11:].animate.set_color(YELLOW), IndicateAround(tex_3[11:]))
        # self.wait()

        # branch = [label_base, label_height, text_area, height_line1, elbow, label_H, tex_1, tex_2, tex_3]
        # self.play(*[FadeOut(mob) for mob in branch])
        # self.wait(0, 16)
        # self.add(*branch).wait()
        self.play(FadeOut(tex_1), FadeOut(tex_2), FadeOut(label_H))
        self.wait(0, 16) #但这样计算量就会非常大
        self.wait(0, 25) #（空闲）

        tex_1 = MTex(r"OA:\ bx-ay=0").scale(0.8).shift(3.5*RIGHT + 1.5*UP)
        tex_2 = MTex(r"h=\frac{|bc-ad+0|}{\sqrt{b^2+a^2}}", tex_to_color_map = {r"h": BLUE}).scale(0.8).shift(3.5*RIGHT + 0*UP)
        self.play(Write(VGroup(tex_1, tex_2)), run_time = 3)
        self.wait(0, 12) #如果用上高中会学的点到直线距离公式
        self.wait(1, 20) #计算量就会小一些
        self.wait(0, 24) #（空闲）

        branch = [label_base, label_height, text_area, height_line1, elbow, tex_1, tex_2, tex_3]
        self.play(*[FadeOut(mob) for mob in branch])
        self.wait(1, 4) #我们还有计算量更小的方法
        p2_H = offset + np.array([2, 0.8, 0])
        p2_D = offset + np.array([5, 0, 0])
        height_line2 = Line(p2_B, p2_H, color = BLUE)
        label_height.next_to(height_line2, LEFT)
        label_H.next_to(p2_H, DOWN)
        width_line2 = Line(p2_C, p2_D, color = GREEN)
        label_base.next_to(width_line2, DOWN)
        dash = DashedLine(p2_A, p2_D)
        tex_1 = MTex(r"H\ (\,c,\ \frac{bc}{a}\,)").scale(0.8).shift(3.5*RIGHT + 1.5*UP)
        tex_2 = MTex(r"h=\frac{|ad-bc|}{a}", tex_to_color_map = {r"h": BLUE}).scale(0.8).shift(3.5*RIGHT + 0*UP)
        tex_3 = MTex(r"S=\frac{1}{2}wh=\frac{1}{2}|ad-bc|", tex_to_color_map = {r"S": YELLOW, r"w": GREEN, r"h": BLUE}).scale(0.8).shift(3.5*RIGHT + 1.5*DOWN)
        configs = {r"run_time": 2, r"squish_interval": (1/2, 1)}
        self.bring_to_back(height_line2, dash).play(Write(VGroup(tex_1, tex_2, tex_3), run_time = 3), ShowCreation(height_line2), ShowCreation(width_line2), ShowCreation(dash), 
                  Write(label_height, **configs), Write(label_base, **configs), Write(label_H, **configs), Write(text_area, **configs))
        self.wait(2+0-3, 22+24) #那就是水平宽乘铅垂高/2 （空闲）
        self.play(tex_3[11:].animate.set_color(YELLOW), IndicateAround(tex_3[11:]))
        self.wait(1, 18) #三种计算理所当然会都得到一模一样的式子
        self.wait(3, 1) #1/2|ad-bc|
        self.wait(1, 11) #（空闲）

        self.wait(4, 27) #甚至 即使我们既不懂勾股定理 也不知道水平宽乘铅垂高是什么
        self.wait(1, 26) #一样能算出这个结果
        branch = [label_base, label_height, text_area, height_line2, width_line2, dash, label_H, tex_1, tex_2, tex_3]
        self.play(*[FadeOut(mob) for mob in branch])
        self.wait(2, 9) #方法就是我们从小学就开始用的割补法
        self.wait(0, 23) #（空闲）
        p2_E = offset + np.array([5, 4, 0])
        p2_F = offset + np.array([0, 4, 0])
        rectangle = Polygon(p2_C, p2_D, p2_E, p2_F, color = GREY)
        s1 = Polygon(p2_C, p2_D, p2_A, color = BLUE, stroke_width = 0, fill_opacity = 0.5)
        s2 = Polygon(p2_A, p2_E, p2_B, color = TEAL, stroke_width = 0, fill_opacity = 0.5)
        s3 = Polygon(p2_B, p2_F, p2_C, color = GREEN, stroke_width = 0, fill_opacity = 0.5)
        self.bring_to_back(rectangle).play(ShowCreation(rectangle))
        self.wait(1, 21) #先画一个矩形把这个三角形围起来
        paras = {r"stroke_width": 0, r"fill_opacity": 1}
        formula = VGroup(rectangle.copy().scale(0.2).set_style(**paras), MTex(r"=")[0], triangle_1.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s1.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s2.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s3.copy().scale(0.2).set_style(**paras)).arrange().shift(3*UP)
        self.bring_to_back(s1, s2, s3).play(*[FadeIn(mob) for mob in [s1, s2, s3]], triangle_1.animate.set_fill(opacity = 0.8), Write(formula))
        self.wait(0, 23) #然后去掉多余的部分
        self.wait(1, 24) #去掉的这三个三角形
        self.wait(2, 11) #底和高都平行于坐标轴
        tex = MTex(r"S&={ad}-\frac{ab}{2}-\frac{(a-c)(d-b)}{2}-\frac{cd}{2}\\&=\frac{1}{2}(ad-bc)", tex_to_color_map = {r"S": YELLOW, r"{ad}": GREY, r"\frac{ab}{2}": BLUE, r"\frac{(a-c)(d-b)}{2}": TEAL, r"\frac{cd}{2}": GREEN}).scale(0.8).shift(3.5*RIGHT + UP)
        self.play(Write(tex[:-7]))
        self.wait(0, 10) #它们的面积是能算的
        self.play(Write(tex[-7:]))
        self.wait(1, 21) #矩形的面积减三个三角形的面积
        self.play(tex[-7:].animate.set_color(YELLOW), IndicateAround(tex[-7:]))
        self.wait(0, 11) #就能得到我们要的三角形的面积
        self.wait(1, 6) #（空闲）
        
        self.wait(1, 27) #但美中不足的是
        self.wait(2, 4) #割补法有它自己的缺陷
        self.wait(3, 14) #那就是过程和图形有关
        self.wait(0, 19) #（空闲）
        camera = self.camera.frame
        offset = 10.5*DOWN + 4*LEFT
        axis2_x, axis2_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p3_A = offset + np.array([3, 4, 0])
        p3_B = offset + np.array([-2, 2, 0])
        p3_C = offset
        p3_D = offset + np.array([3, 0, 0])
        p3_E = offset + np.array([-2, 4, 0])
        p3_F = offset + np.array([-2, 0, 0])
        label2_A = MTex(r"A(a, b)").next_to(p3_A, UP).set_stroke(**stroke_dic)
        label2_B = MTex(r"B(c, d)").next_to(p3_B, UP).set_stroke(**stroke_dic)
        label2_O = MTex(r"O").next_to(p3_C, DL)
        triangle_2 = Polygon(p3_A, p3_B, p3_C, fill_color = YELLOW, fill_opacity = 0.8)
        rectangle_2 = Polygon(p3_D, p3_A, p3_E, p3_F, color = GREY)
        s4 = Polygon(p3_C, p3_D, p3_A, color = BLUE, stroke_width = 0, fill_opacity = 0.5)
        s5 = Polygon(p3_A, p3_E, p3_B, color = TEAL, stroke_width = 0, fill_opacity = 0.5)
        s6 = Polygon(p3_B, p3_F, p3_C, color = GREEN, stroke_width = 0, fill_opacity = 0.5)
        formula_2 = VGroup(rectangle_2.copy().scale(0.2).set_style(**paras), MTex(r"=")[0], triangle_2.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s4.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s5.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s6.copy().scale(0.2).set_style(**paras)).arrange().shift(5*DOWN)
        self.add(s4, s5, s6, rectangle_2, axis2_x, axis2_y, triangle_2, label2_A, label2_B, label2_O, formula_2).play(camera.animate.shift(8*DOWN), run_time = 2)
        self.wait(1, 18) #比如说 要是三角形的两个顶点不都在第一象限
        self.wait(2, 16) #我们就会框出来不一样的矩形
        self.wait(1, 23) #而这三个三角形
        self.wait(1, 6) #也会有所差别
        self.wait(0, 24) #（空闲）
        tex_2 = MTex(r"S&=(a-c)b-\frac{ab}{2}-\frac{(a-c)(b-d)}{2}+\frac{cd}{2}\\&=\frac{1}{2}(ad-bc)", tex_to_color_map = {r"S": YELLOW, r"(a-c)b": GREY, r"\frac{ab}{2}": BLUE, r"\frac{(a-c)(b-d)}{2}": TEAL, r"\frac{cd}{2}": GREEN}).scale(0.8).shift(3.5*RIGHT + 7*DOWN)
        self.play(Write(tex_2))
        self.play(tex_2[-7:].animate.set_color(YELLOW), IndicateAround(tex_2[-7:]))
        self.wait(1+2-4, 9+22) #根据这个图形 也能写出对应的式子 得到正确的结果
        tex_3 = MTex(r"S={ad}-\frac{ab}{2}-\frac{(a-c)(d-b)}{2}-\frac{cd}{2}=\frac{1}{2}(ad-bc)", isolate = [r"(d-b)", r"-"], tex_to_color_map = {r"S": YELLOW, r"{ad}": GREY, r"\frac{ab}{2}": BLUE, r"\frac{(a-c)(d-b)}{2}": TEAL, r"\frac{cd}{2}": GREEN, r"(ad-bc)": YELLOW}).scale(0.8).next_to(2*RIGHT + UP, LEFT)
        tex_4 = MTex(r"S=(a-c)b-\frac{ab}{2}-\frac{(a-c)(b-d)}{2}+\frac{cd}{2}=\frac{1}{2}(ad-bc)", isolate = [r"(b-d)", r"+"], tex_to_color_map = {r"S": YELLOW, r"(a-c)b": GREY, r"\frac{ab}{2}": BLUE, r"\frac{(a-c)(b-d)}{2}": TEAL, r"\frac{cd}{2}": GREEN, r"(ad-bc)": YELLOW}).scale(0.8).next_to(3*LEFT + 2.5*DOWN)
        formula.next_to(2*RIGHT + 2.5*UP, LEFT)
        list_1 = [s1, s2, s3, rectangle, axis_x, axis_y, triangle_1, label_A, label_B, label_O.next_to(p2_C, DL)]
        for mob in list_1:
            mob.scale(0.5, about_point = 11*RIGHT + 4*UP)
        self.remove(tex).add(tex_3).play(*[mob.animate.scale(0.5, about_point = 6.5*LEFT + 5*UP) for mob in [s4, s5, s6, rectangle_2, axis2_x, axis2_y, triangle_2, label2_A, label2_B, label2_O]], 
                  formula_2.animate.next_to(2*LEFT + 1*DOWN), ReplacementTransform(tex_2, tex_4, path_arc = PI/4), 
                  camera.animate.shift(8*UP), run_time = 2)
        self.wait(1+2-2, 17+23) #但这个式子不一样 你需要根据具体的情况去调整它
        self.play(IndicateAround(tex_3.get_part_by_tex(r"{ad}")), IndicateAround(tex_4.get_part_by_tex(r"(a-c)b")),
                  IndicateAround(tex_3.get_part_by_tex(r"(d-b)")), IndicateAround(tex_4.get_part_by_tex(r"(b-d)")),
                  IndicateAround(tex_3.get_parts_by_tex(r"-")[4]), IndicateAround(tex_4.get_part_by_tex(r"+")))
        self.wait(1+1-2, 11+0) #二者之间有很大差别
        
        self.wait(1, 10) #那这该怎么办呢
        self.wait(4, 9) #难道对于每种情况都要单独列个式子分类讨论吗
        self.wait(0, 28) #这也太麻烦了
        self.wait(0, 16) #（空闲）
        self.play(*[OverFadeOut(mob, 6*LEFT + 4*UP) for mob in [tex_3, formula]], *[OverFadeOut(mob, 6*RIGHT + 4*DOWN) for mob in [tex_4, formula_2]],
                  *[mob.animate.scale(2, about_point = 4*RIGHT + 3.5*UP) for mob in list_1], 
                  *[mob.animate.scale(2, about_point = 6.5*LEFT + 3.5*DOWN) for mob in [axis2_x, axis2_y, triangle_2, label2_A, label2_B, label2_O]],
                  *[mob.animating(remover = True).scale(2, about_point = 6.5*LEFT + 3.5*DOWN).set_opacity(0) for mob in [s4, s5, s6, rectangle_2]],
                  triangle_2.animate.scale(2, about_point = 6.5*LEFT + 3.5*DOWN).set_fill(opacity = 0).set_stroke(color = YELLOW),
                  run_time = 2)
        self.wait(1+1-2, 15+18) #其实不用 我们只需要想想办法
        self.wait(2, 20) #把式子凑成一样的就行了
        self.wait(1, 4) #（空闲）
        
        offset = RIGHT + 2*DOWN
        p2_A = offset + np.array([5, 2, 0])
        p2_B = offset + np.array([2, 4, 0])
        p2_C = offset
        p2_D = offset + np.array([5, 0, 0])
        p2_E = offset + np.array([5, 4, 0])
        p2_F = offset + np.array([0, 4, 0])
        offset = 4*LEFT + 2*DOWN
        p3_A = offset + np.array([3, 4, 0])
        p3_B = offset + np.array([-2, 2, 0])
        p3_C = offset
        p3_D = offset + np.array([3, 0, 0])
        p3_E = offset + np.array([3, 2, 0])
        p3_F = offset + np.array([0, 2, 0])
        l_1 = Line(p2_E, p2_D, stroke_width = 8, color = YELLOW)
        self.add(l_1, label_A).play(ShowOut(l_1, rate_func = smooth), label_A.animating(rate_func = double_there_and_back).scale(1.1).set_fill(color = YELLOW))
        self.wait(1, 26) #右边图里 矩形的右端是经过A点的
        line_1 = Line(p3_A, p3_D, color = GREY)
        self.bring_to_back(line_1).add(l_1, label_A).play(ShowCreation(line_1), ShowOut(l_1, rate_func = smooth), label2_A.animating(rate_func = double_there_and_back).scale(1.1).set_fill(color = YELLOW))
        self.wait(1, 19) #那么左边就也让它经过A点
        l_2 = Line(p2_F, p2_E, stroke_width = 8, color = YELLOW)
        self.add(l_2, label_B).play(ShowOut(l_2, rate_func = smooth), label_B.animating(rate_func = double_there_and_back).scale(1.1).set_fill(color = YELLOW))
        self.wait(0, 24) #右边矩形的上端是经过B点的
        line_2 = Line(p3_B, p3_E, color = GREY)
        self.bring_to_back(line_2).add(l_2, label_B).play(ShowCreation(line_2), ShowOut(l_2, rate_func = smooth), label2_B.animating(rate_func = double_there_and_back).scale(1.1).set_fill(color = YELLOW))
        self.wait(1, 5) #左边就也让它经过B点
        self.wait(0, 18) #（空闲）

        l_3, l_4 = Line(p2_C, p2_D, stroke_width = 8, color = YELLOW), Line(p2_C, p2_F, stroke_width = 8, color = YELLOW)
        self.play(ShowOut(l_3, rate_func = smooth), ShowOut(l_4, rate_func = smooth))
        self.wait(1, 22) #右边矩形另外两条边在坐标轴上
        rectangle_2 = Polygon(p3_C, p3_D, p3_E, p3_F, color = GREY, stroke_width = 0, fill_opacity = 0.5)
        s4 = Polygon(p3_C, p3_D, p3_A, color = BLUE, stroke_width = 8)
        s5 = Polygon(p3_A, p3_E, p3_B, color = TEAL, stroke_width = 0, fill_opacity = 0.5)
        s6 = Polygon(p3_B, p3_F, p3_C, color = GREEN, stroke_width = 0, fill_opacity = 0.5)
        self.bring_to_back(rectangle_2).add(l_1, l_2, l_3.reverse_points(), l_4, label_A, label_B).play(GrowFromPoint(rectangle_2, p3_C), *[ShowOut(l, rate_func = smooth) for l in [l_1, l_2, l_3, l_4]])
        self.wait(1, 0) #左边就也让它在坐标轴上
        self.wait(0, 17) #（空闲）
        self.wait(2, 4) #这样 左边的矩形面积
        self.wait(1, 5) #就和右边一样
        self.wait(0, 26) #也是ad了
        self.wait(1, 10) #（空闲）

        self.wait(3, 3) #这么一来 割补法也有了差别
        self.wait(2, 9-15) #左边需要关心的三角形 分别是
        self.add(s4, triangle_2, label2_A, label2_B).bring_to_back(s5, s6).play(
            WiggleOutThenIn(s1), ShowCreation(s4, delay = 0.5), ShowPassingFlash(s4.copy(), delay = 0.5),
            WiggleOutThenIn(s2, delay = 0.5 + 32/30), GrowFromCenter(s5, delay = 0.5 + 32/30),
            WiggleOutThenIn(s3, delay = 0.5 + 32/30 + 24/30), GrowFromCenter(s6, delay = 0.5 + 32/30 + 24/30), frames = 15+32+24+24+19) #这个 这个 和这个 （空闲）

        formula = VGroup(triangle_1.copy().scale(0.2).set_style(**paras), MTex(r"=")[0], rectangle.copy().scale(0.2).set_style(**paras), MTex(r"-")[0], s1.copy().scale(0.2).set_style(**paras), MTex(r"-")[0], s2.copy().scale(0.2).set_style(**paras), MTex(r"-")[0], s3.copy().scale(0.2).set_style(**paras)).arrange().scale(0.8).move_to(2.5*DOWN + 3.5*RIGHT)
        formula_2 = VGroup(triangle_2.copy().scale(0.2).set_style(**paras), MTex(r"=")[0], rectangle_2.copy().scale(0.2).set_style(**paras), MTex(r"-")[0], s4.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s5.copy().scale(0.2).set_style(**paras), MTex(r"+")[0], s6.copy().scale(0.2).set_style(**paras)).arrange().scale(0.8).shift(2.5*DOWN + 3.5*LEFT)
        list_2 = [s4, s5, s6, rectangle_2, line_1, line_2, axis2_x, axis2_y, triangle_2, label2_A, label2_B, label2_O]
        self.play(*[mob.animate.scale(0.8, about_point = 4*UP + 3.5*RIGHT) for mob in list_1],
                  *[mob.animate.scale(0.8, about_point = 4*UP + 3.5*LEFT) for mob in list_2],
                  FadeIn(formula, 0.5*UP), FadeIn(formula_2, 0.5*UP))
        self.wait(1, 23) #而面积的计算公式 长这样
        self.wait(1, 3) #（空闲）
        self.wait(1, 11) #由于图形的区别
        self.wait(3, 6) #两边对应区域的加减也是不一样的
        text_1, text_2 = r"S={ad}-\frac{ab}{2}-\frac{(a-c)(d-b)}{2}-\frac{cd}{2}", r"=\frac{1}{2}(ad-bc)"
        tex = MTex(text_1 + text_2, isolate = [text_1, text_2], tex_to_color_map = {r"S": YELLOW, r"{ad}": GREY, r"-\frac{ab}{2}": BLUE, r"-\frac{(a-c)(d-b)}{2}": TEAL, r"-\frac{cd}{2}": GREEN, r"(ad-bc)": YELLOW}).shift(3*UP)
        tex_1, tex_2 = tex.get_part_by_tex(text_1), tex.get_part_by_tex(text_2)
        tex_1.save_state().set_x(0)
        tex_2.save_state().match_x(tex_1, RIGHT)
        shade = BackgroundRectangle(tex_2, buff = 0.1)
        self.play(*[mob.animate.scale(0.875, about_point = 4*DOWN + 3.5*RIGHT) for mob in list_1],
                  *[mob.animate.scale(0.875, about_point = 4*DOWN + 3.5*LEFT) for mob in list_2],
                  FadeIn(tex_1, 0.5*DOWN))
        self.wait(1, 2) #但我们要是把式子写出来
        self.wait(2, 8) #奇迹般的事情就出现了
        self.wait(3, 0) #两幅图面积的表达式是一模一样的
        self.wait(0, 15) #（空闲）
        self.add(tex_2, shade, tex_1).play(tex_1.animate.restore(), tex_2.animate.restore(), follow(shade, tex_1, remover = True))
        self.wait(2, 0) #于是 结果也理所当然地一样
        self.wait(1, 21) #（空闲）
        
        list_area = [s1, s2, rectangle_2, s5, triangle_1]
        for mob in [tex, formula, formula_2, s3, s4, s6, triangle_2] + list_area:
            mob.save_state()
        self.play(*[mob.animate.set_opacity(0.2) for mob in [tex_1[:-5], tex_2, formula[:-2], formula_2[:-2]]], *[mob.animate.set_fill(opacity = 1) for mob in [s3, s6]], s4.animate.set_stroke(color = GREY, width = 4), triangle_2.animate.set_stroke(color = WHITE), *[mob.animate.set_fill(opacity = 0) for mob in list_area])
        self.wait(1, 0) #我们来仔细看看这是为什么
        self.wait(2, 18) #请大家关注绿色的这块区域

        self.wait(1, 17) #在右边这幅图里面
        self.wait(2, 2) #绿色区域是要被减掉的
        c_1, d_1, s_1 = MTex(r"c", color = GREEN).scale(0.8).next_to(s3, UP, buff = 0.1).set_stroke(**stroke_dic), MTex(r"d", color = GREEN).scale(0.8).next_to(s3, LEFT, buff = 0.1).set_stroke(**stroke_dic), MTex(r"\frac{cd}{2}", color = GREEN).scale(0.7).move_to((s3.get_corner(RIGHT)/4+s3.get_center()/4+s3.get_corner(UL)/2)).set_stroke(**stroke_dic)
        self.play(ShowCreation(c_1))
        self.wait(0, 9) #它的底是c
        self.play(ShowCreation(d_1))
        self.play(Write(s_1))
        self.wait(0+2-2, 27+11) #高是d 面积自然就是cd/2

        self.wait(1, 16) #而左边这幅图里面
        self.wait(2, 9) #绿色区域是被加起来的
        c_2, d_2, s_2 = MTex(r"-c", color = RED).scale(0.8).next_to(s6, UP, buff = 0.1).set_stroke(**stroke_dic), MTex(r"d", color = GREEN).scale(0.8).next_to(s6, RIGHT, buff = 0.1).set_stroke(**stroke_dic), MTex(r"-\frac{cd}{2}", color = GREEN).scale(0.7).move_to((s6.get_corner(UL)/3+s6.get_corner(DR)/3+s6.get_corner(UR)/3)).set_stroke(**stroke_dic)
        s_3 = MTex(r"\frac{cd}{2}", color = RED).scale(0.7).move_to(s_2).set_stroke(**stroke_dic)
        self.play(ShowCreation(d_2))
        self.wait(0, 15) #它的高还是d
        l = Line(s6.get_corner(UL), s6.get_corner(DL), stroke_width = 8, color = YELLOW)
        self.play(ShowOut(l, rate_func = smooth))
        self.wait(1, 21) #但是这个时候 B的横坐标是负的
        self.play(ShowCreation(c_2))
        self.wait(1, 22) #所以它的底其实是-c
        self.play(Write(s_2))
        self.wait(1+2-1, 17+15) #这块区域的面积 其实是-cd/2
        self.wait(0, 23) #（空闲）
        self.play(IndicateAround(s_2[0]), IndicateAround(formula[-2]))
        self.wait(0, 5) #两边各出现了一处负号
        self.play(IndicateAround(tex_1[-5:]))
        self.wait(0, 18) #表达式里这一项自然就一样了
        self.wait(1, 20) #（空闲）

        self.wait(3, 5) #由此 我们可以有一种更大胆的思路
        self.play(IndicateAround(VGroup(*list_1)), IndicateAround(VGroup(*list_2)))
        self.wait(1, 13) #既然左右两边画的图是一样的
        self.play(IndicateAround(tex_1[-5:]), run_time = 53/30, frames = 53)#表达式也是一样的
        self.play(IndicateAround(formula[-2]), IndicateAround(formula_2[-2]))
        self.wait(0, 20) #只有割补法的正负号不一样
        self.wait(1, 26) #那有没有一种可能
        self.wait(2, 22) #是我们看待割补法的思路错了呢
        self.wait(0, 22) #（空闲）

        self.wait(1, 10) #有没有一种可能
        self.play(ReplacementTransform(s_2[1:], s_3), s_2[0].animating(remover = True).scale(0), s6.animate.set_fill(color = RED), formula_2[-1].animate.set_fill(RED), Transform(formula_2[-2], MTex(r"-").scale(0.8).move_to(formula_2[-2])))
        self.wait(2, 7) #这个三角一直应该被减掉
        self.wait(2, 23) #而它的面积也一直是cd/2呢
        self.wait(0, 23) #（空闲）
        self.wait(1, 8) #也就是说
        self.wait(3, 14) #也许 我们可以考虑一种负数的面积
        self.wait(1, 10) #（空闲）

        title = Heiti("有向面积", color = RED).scale(0.8)
        box = SurroundingRectangle(title, color = RED)
        self.play(*[mob.animate.restore() for mob in list_area + [tex, formula, s3, s4, triangle_2]], formula_2.animate.set_opacity(1), s6.animate.set_opacity(0.5), *[FadeOut(mob) for mob in [c_1, d_1, c_2, d_2]], Write(title), ShowCreation(box))
        self.wait(1, 20) #这种思路被称为“有向面积”
        self.wait(2, 2) #它会为我们带来很多好处
        self.wait(0, 22) #比如说
        ORANGE_R = interpolate_color(RED, ORANGE, 0.5)
        p0, p1, p2 = s5.get_corner(DR), s5.get_corner(UR), s5.get_corner(DL)
        lines = Line(p0, p1, color = RED, stroke_width = 8), Line(p1, p2, color = RED, stroke_width = 8), Line(p2, p0, color = RED, stroke_width = 8)
        self.play(s5.animate.set_color(ORANGE), formula_2[-3].animate.set_fill(ORANGE_R), *[ShowOut(line) for line in lines], Transform(formula_2[-4], MTex(r"-").scale(0.8).move_to(formula_2[-4])))
        self.wait(2, 13) #它可以处理割补式中所有的正负号问题
        self.wait(0, 22) #（空闲）
        self.play(IndicateAround(formula), IndicateAround(formula_2))
        self.wait(1, 16) #从而面积公式可以彻底统一
        self.wait(0, 21) #（空闲）
        self.wait(2, 0) #而且不只是三角形
        self.wait(2, 8) #任何繁琐的割补法
        tex_3 = MTex(r"S=\frac{1}{2}(ad-bc)", tex_to_color_map = {(r"S", r"(ad-bc)"): YELLOW}).shift(3*UP)
        tex_1_2 = tex_1[1:]
        shade = BackgroundRectangle(tex_1_2, buff = 0.1).match_x(tex_2.refresh_bounding_box(), LEFT).shift(0.1*LEFT)
        anim_1, anim_2 = ReplacementTransform(tex_1[0], tex_3[0]), ReplacementTransform(tex_2, tex_3[1:])
        self.add(tex_1_2, shade, tex_2).play(*[FadeOut(mob) for mob in [formula, formula_2, s1, s2, s3, s4, s5, s6, s_1, s_3, rectangle, rectangle_2, line_1, line_2]], 
                  anim_1, follow(tex_1_2, anim_1, remover = True), anim_2, follow(shade, anim_2, remover = True),
                  triangle_2.animate.set_style(stroke_color = WHITE, fill_opacity = 0.8))
        self.wait(1, 19) #都可以用负面积来简化统一
        self.wait(1, 6) #（空闲）
        def color_updater(mob: VMobject):
            mob.set_color(interpolate_color(RED, WHITE, (np.sin((self.time-mob.time)*PI))**2))
        for mob in [box]:
            mob.time = self.time
            mob.add_updater(color_updater)
        self.wait(3, 0) #但它看上去同样很危险
        self.wait(3, 23) #因为......怎么去理解一块区域的面积是负数呢
        self.wait(1, 12) #（空闲）

        self.wait(1, 21) #为了认真考虑这个问题

#################################################################### 

class Video_2(FrameScene):
    def construct(self):
        formula = MTex(r"S=ad-bc", tex_to_color_map = {(r"S", r"ad-bc"): YELLOW}).shift(3*UP)
        offset = 2*DOWN + 0.5*LEFT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        p_E = offset + np.array([3, 0, 0])
        p_F = offset + np.array([3, 4, 0])
        p_G = offset + np.array([-2, 4, 0])
        p_H = offset + np.array([-2, 0, 0])
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.8)
        label_A = MTex(r"(a, b)").next_to(p_A, RIGHT)
        label_B = MTex(r"(c, d)").next_to(p_C, LEFT)
        self.fade_in(formula, axis_x, axis_y, parallelogram, label_A, label_B)
        self.wait(0, 28) #我们来看另一种图形
        self.wait(1, 21) #平行四边形
        line = Line(p_A, p_C, stroke_width = 6)
        self.play(ShowCreation(line))
        self.wait(1, 12) #它的面积是三角形的两倍
        self.play(FadeOut(line))
        self.wait(1, 22) #所以面积公式是ad-bc
        self.wait(0, 26) #（空闲）

        self.wait(1, 21) #按照三角形的思路
        rectangle = Polygon(p_E, p_F, p_G, p_H, color = GREY)
        s1 = Polygon(p_D, p_E, p_A, fill_color = BLUE, fill_opacity = 0.5, stroke_width = 0)
        s2 = Polygon(p_A, p_F, p_B, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0)
        s3 = Polygon(p_B, p_G, p_C, fill_color = BLUE, fill_opacity = 0.5, stroke_width = 0)
        s4 = Polygon(p_C, p_H, p_D, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0)
        self.bring_to_back(s1, s2, s3, s4, rectangle).play(ShowCreation(rectangle, run_time = 2), LaggedStart(*[FadeIn(mob) for mob in [s1, s2, s3, s4]], run_time = 2, lag_ratio = 1/3, group = VGroup(), remover = True))
        self.wait(1, 6) #这个公式的证明过程大概是把平行四边形框起来
        self.wait(1, 6) #再把四个角减掉
        self.wait(0, 23) #（空闲）
        self.play(*[FadeOut(mob) for mob in [s1, s2, s3, s4, rectangle]])
        self.wait(1, 28) #但其实平行四边形比三角形简单多了
        self.wait(2, 19) #它有另外一套更好的割补法
        self.wait(2, 20) #更有助于我们理解有向面积的本质
        self.wait(1, 3) #（空闲）

class Video_3(FrameScene):
    def construct(self):
        
        self.wait(0, 5) #（空闲）
        def indicate_line(start, end, color = YELLOW, opacity = 1, **kwargs):
            return Line(start, end, stroke_opacity = opacity).animating(rate_func = there_and_back, remover = True, **kwargs).scale(1.2).set_stroke(color = color, opacity = 1)
        
        offset = 2*UP
        camera = self.camera.frame
        camera.shift(offset)
        parallelogram_0 = Rectangle(height = 4, width = 2, fill_color = interpolate_color(YELLOW, BLACK, 0.5), fill_opacity = 1).shift(offset)
        def shear(t: float):
            return parallelogram_0.copy().apply_matrix(np.array([[1, t], [0, 1]]))
        parallelogram = shear(1/4)
        self.fade_in(parallelogram).wait(1, 22) #平行四边形的面积公式想必大家都很熟悉了

        height_line1 = Line(ORIGIN, 4*UP)
        elbow = Elbow()
        height_1 = VGroup(height_line1, elbow)
        label_base = MTex(r"w", color = GREEN).next_to(ORIGIN, DOWN).set_stroke(**stroke_dic)
        label_height = MTex(r"h", color = BLUE).next_to(2*UP, LEFT).set_stroke(**stroke_dic)
        text_area = MTex(r"S=wh", tex_to_color_map = {r"S": YELLOW, r"w": GREEN, r"h": BLUE}).shift(3*UP + offset)

        self.play(indicate_line(1*LEFT, 1*RIGHT, GREEN), FadeIn(label_base), Write(text_area), indicate_line(ORIGIN, 4*UP, BLUE, 0), FadeIn(label_height), FadeIn(height_1))
        self.wait(0, 11) #那就是底乘高
        self.wait(0, 28) #（空闲）

        line_base = Line(1*LEFT, 1*RIGHT, color = GREEN, stroke_width = 8)
        line_up, line_down = Line(LEFT_SIDE, RIGHT_SIDE, color = GREY).shift(4*UP), Line(LEFT_SIDE, RIGHT_SIDE, color = GREY)
        self.bring_to_back(line_up, line_down).play(ShowCreation(line_base), GrowFromCenter(line_up, run_time = 2), GrowFromCenter(line_down, run_time = 2), label_height.animating(run_time = 2).shift(6*LEFT), height_1.animating(run_time = 2).shift(6*LEFT).set_stroke(color = BLUE, width = 8))
        self.wait()
        self.play(Transform(parallelogram, shear(-1)))
        self.wait()
        copies = []
        alpha = ValueTracker(-1)
        step = 2/3
        parallelogram.counter = -1/step
        def fan_updater(mob: Rectangle):
            value = alpha.get_value()
            number = math.floor(value/step + 0.5)
            mob.become(shear(value))
            while number >= mob.counter:
                new = shear(mob.counter*step).set_fill(color = interpolate_color(YELLOW, BLACK, 0.8)).set_stroke(color = GREY)
                copies.append(new)
                self.add(new, mob, line_base)
                mob.counter += 1
        parallelogram.add_updater(fan_updater)
        self.play(alpha.animate.set_value(1), run_time = 2)
        self.wait(1+4+1-7, 23+0+25) #这就意味着这么一件事 当平行四边形的一条边在平行线上滑动的时候 它的面积是不变的
        self.wait(0, 14) #（空闲）

class Video_4(FrameScene):
    def construct(self):
        formula = MTex(r"S=ad-bc", tex_to_color_map = {(r"S", r"ad-bc"): YELLOW}).shift(3*UP)
        offset = 2*DOWN + 0.5*LEFT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        p_E = offset + np.array([3, 0, 0])
        p_F = offset + np.array([3, 1, 0])*9/11
        p_G = offset + np.array([3, 1, 0])*9/11 + np.array([-2, 3, 0])
        p_H = offset + np.array([1, 3, 0])
        p_I = offset + np.array([0, 1, 0])
        parallelogram = Polygon(p_A, p_B, p_C, p_D)
        fill_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        label_A = MTex(r"(a, b)").next_to(p_A, RIGHT)
        label_B = MTex(r"(c, d)").next_to(p_C, LEFT)
        vector = Arrow(p_D, p_A, color = YELLOW, buff = 0, stroke_width = 8)
        self.add(formula, axis_x, axis_y, parallelogram_0, fill_0, parallelogram, label_A, label_B, vector).wait(0, 22) #据此......

        vector_1 = Arrow(p_D, p_E, color = GREEN, buff = 0, stroke_width = 8)
        vector_2 = Arrow(p_E, p_A, color = ORANGE, buff = 0, stroke_width = 8)
        self.play(ReplacementTransform(Line.set_stroke(Arrow(p_D, p_F, color = YELLOW, buff = 0, stroke_width = 6), width = 6), vector_1), ReplacementTransform(Arrow(p_F, p_A, color = YELLOW, buff = 0, stroke_width = 6), vector_2))
        self.wait(2, 5) #我们可以把(a,b)拆成两个向量

        line = Line(p_E, p_G)
        line_2 = Line(p_G, p_H, color = GREY)
        self.add(line, vector, vector_1, vector_2).play(ShowCreation(line))
        self.wait(1, 9) #然后作一条平行线

        parallelogram_1 = Polygon(p_F, p_G, p_C, p_D)
        parallelogram_2 = Polygon(p_A, p_B, p_G, p_F)
        fill_1 = Polygon(p_F, p_G, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        fill_2 = Polygon(p_A, p_B, p_G, p_F, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        self.remove(parallelogram, fill_0).bring_to_back(fill_1, fill_2).add(line_2, parallelogram_1, parallelogram_2, line, vector, vector_1, vector_2).play(
            Transform(parallelogram_1, Polygon(p_E, p_H, p_C, p_D)),
            Transform(parallelogram_2, Polygon(p_A, p_B, p_H, p_E)),
            Transform(fill_1, Polygon(p_E, p_H, p_C, p_D, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0)),
            Transform(fill_2, Polygon(p_A, p_B, p_H, p_E, fill_color = ORANGE, fill_opacity = 0.5, stroke_width = 0)),
            line.animate.put_start_and_end_on(p_E, p_H), ShowCreation(line_2))
        self.wait(1, 19) #把这个平行四边形分成两个
        self.wait(0, 28) #（空闲）
        
        list_0 = [axis_x, axis_y, parallelogram_0, label_A, label_B, vector, vector_1, vector_2, line, line_2, parallelogram_1, parallelogram_2, fill_1, fill_2]
        list_1 = [axis_x.copy(), axis_y.copy(), fill_1.copy(), parallelogram_1.copy(), label_B.copy(), MTex(r"(a, 0)", tex_to_color_map = {r"a": GREEN}).next_to(p_E, UR), vector_1.copy()]
        list_2 = [Arrow(2.5*LEFT, 1.5*RIGHT, stroke_width = 3).shift(offset), axis_y.copy(), fill_2.copy().shift(3*LEFT), parallelogram_2.copy().shift(3*LEFT), label_B.copy(), MTex(r"(0, b)", tex_to_color_map = {r"b": ORANGE}).next_to(p_I, RIGHT), vector_2.copy().shift(3*LEFT)]
        label_a = MTex(r"a", color = GREEN).next_to((offset + np.array([3, 0, 0])/2), DOWN).set_stroke(**stroke_dic)
        label_d = MTex(r"d", color = GREEN).next_to((offset + np.array([0, 3, 0])/2), RIGHT).set_stroke(**stroke_dic)
        label_b = MTex(r"b", color = ORANGE).next_to((offset + np.array([0, 1, 0])*0.4), RIGHT).set_stroke(**stroke_dic)
        label_c = MTex(r"-c", color = ORANGE).next_to((offset + np.array([-2, 0, 0])/2), DOWN).set_stroke(**stroke_dic)
        l = Line(p_C, (offset + np.array([-2, 0, 0])), color = GREY)
        for mob in list_1 + [label_a, label_d]:
            mob.scale(0.6, about_point = ORIGIN).shift(RIGHT + DOWN)
        for mob in list_2 + [label_b, label_c, l]:
            mob.scale(0.6, about_point = ORIGIN).shift(6*RIGHT + DOWN)
        self.play(*[mob.animating(path_arc = -PI/3).scale(0.8, about_point = ORIGIN).shift(4*LEFT + UP) for mob in list_0], *[FadeIn(mob, 3*DL, path_arc = -PI/2) for mob in list_1 + list_2], run_time = 2)
        self.wait(1+3-2, 22+5) #这两个平行四边形 就分别有边和坐标轴平行了
        self.bring_to_back(l).play(*[Write(mob) for mob in [label_a, label_d, label_b, label_c]], FadeIn(l))
        self.wait(1, 26) #于是我们可以分别计算出它们的面积
        self.wait(1, 11) #（空闲）
        self.wait(2, 16) #如果我们不考虑有向面积
        self.wait(1, 24) #那这两部分面积应该加起来
        self.wait(0, 21) #（空闲）
        tex_1 = MTex(r"ad", color = GREEN).move_to(RIGHT + UP)
        tex_2 = MTex(r"-bc", color = ORANGE).move_to(5*RIGHT + UP)
        self.play(Write(tex_1), Write(tex_2))
        self.wait(1, 24) #于是在有向面积的视角下
        self.wait(2, 4) #它们应该都是正的
        self.wait(2, 4) #绿色的这个面积是ad
        self.wait(3, 1) #橙色的这个则是-bc
        self.wait(1, 0) #（空闲）

        self.fade_out(excepts = [formula])
        offset = 2*DOWN + 2*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 4.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([4, 4, 0])
        p_C = offset + np.array([1, 3, 0])
        p_D = offset
        p_E = offset + np.array([3, 0, 0])
        p_F = offset + np.array([3, 1, 0])*9/8
        p_G = offset + np.array([3, 1, 0])*9/8 + np.array([1, 3, 0])
        p_H = offset + np.array([4, 3, 0])
        p_I = offset + np.array([0, 1, 0])
        parallelogram = Polygon(p_A, p_B, p_C, p_D)
        fill_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        label_A = MTex(r"(a, b)").next_to(p_A, RIGHT).set_stroke(**stroke_dic)
        label_B = MTex(r"(c, d)").next_to(p_C, UP).set_stroke(**stroke_dic)
        vector = Arrow(p_D, p_A, color = YELLOW, buff = 0, stroke_width = 8)
        vector_1 = Arrow(p_D, p_E, color = GREEN, buff = 0, stroke_width = 8)
        vector_2 = Arrow(p_E, p_A, color = ORANGE, buff = 0, stroke_width = 8)
        self.fade_in(formula, axis_x, axis_y, parallelogram_0, fill_0, parallelogram, label_A, label_B, vector, vector_1, vector_2, excepts = [formula])
        self.wait(1, 8) #当然 它们的面积不总应该加起来
        
        line_a = DashedLine(p_A, p_F)
        line_b = DashedLine(p_B, p_G)
        line = Line(p_E, p_G)
        line_2 = Line(p_G, p_H, color = GREY)
        self.add(line_a, line_b, line, vector, vector_1, vector_2, label_A, label_B).play(ShowCreation(line), ShowCreation(line_a), ShowCreation(line_b), fill_0.animate.set_points_as_corners([p_F, p_G, p_C, p_D]).close_path())
        self.wait(0, 7) #这种情况下

        parallelogram_1 = Polygon(p_F, p_G, p_C, p_D)
        parallelogram_2 = Polygon(p_A, p_B, p_G, p_F)
        fill_1 = Polygon(p_F, p_G, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        fill_2 = Polygon(p_A, p_B, p_G, p_F, fill_color = YELLOW, fill_opacity = 0, stroke_width = 0)
        self.remove(parallelogram, fill_0).bring_to_back(fill_1, fill_2).add(line_2, parallelogram_1, parallelogram_2, line, vector, vector_1, vector_2, label_A, label_B).play(
            Transform(parallelogram_1, Polygon(p_E, p_H, p_C, p_D)),
            Transform(parallelogram_2, Polygon(p_A, p_B, p_H, p_E)),
            Transform(fill_1, Polygon(p_E, p_H, p_C, p_D, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0)),
            Transform(fill_2, Polygon(p_A, p_B, p_H, p_E, fill_color = ORANGE, fill_opacity = 0.5, stroke_width = 0)),
            line.animate.put_start_and_end_on(p_E, p_H), ShowCreation(line_2), line_a.animate.set_color(GREY), line_b.animate.set_color(GREY))
        self.wait(2, 2) #要是不考虑有向面积 两部分就该相减了

        self.wait(0+1-2, 22+27) #（空闲）...
        list_0 = [axis_x, axis_y, parallelogram_0, label_A, label_B, vector, vector_1, vector_2, line_a, line_b, line, line_2, parallelogram_1, parallelogram_2, fill_1, fill_2]
        list_1 = [axis_x.copy(), axis_y.copy(), fill_1.copy(), parallelogram_1.copy(), label_B.copy(), MTex(r"(a, 0)", tex_to_color_map = {r"a": GREEN}).next_to(p_E, DR), vector_1.copy()]
        list_2 = [Arrow(1.5*LEFT, 2.5*RIGHT, stroke_width = 3).shift(offset), axis_y.copy(), fill_2.copy().shift(3*LEFT), parallelogram_2.copy().shift(3*LEFT), label_B.copy().next_to(p_C, RIGHT), MTex(r"(0, b)", tex_to_color_map = {r"b": ORANGE}).next_to(p_I, LEFT), vector_2.copy().shift(3*LEFT)]
        for mob in list_1:
            mob.scale(0.6, about_point = ORIGIN).shift(RIGHT + DOWN)
        for mob in list_2:
            mob.scale(0.6, about_point = ORIGIN).shift(6*RIGHT + DOWN)
        self.play(*[mob.animating(path_arc = -PI/3).scale(0.8, about_point = ORIGIN).shift(4*LEFT + UP) for mob in list_0], *[FadeIn(mob, 3*DL, path_arc = -PI/2) for mob in list_1 + list_2], run_time = 2)
        #self.wait() #于是考虑有向面积的时候

        tex_1 = MTex(r"ad", color = GREEN).move_to(RIGHT + UP)
        tex_2 = MTex(r"-bc", color = ORANGE).move_to(5*RIGHT + UP)
        self.play(Write(tex_1), Write(tex_2))
        self.wait(1, 8) #绿色部分是正的 面积是ad
        self.wait(3, 4) #而橙色部分是负的 面积是-bc
        self.wait(0, 22) #（空闲）
        self.play(IndicateAround(formula))
        self.wait(3, 2) #无论什么时候 我们都能正确地得到面积公式
        self.wait(1, 19) #（空闲）

        self.wait(2, 23) #我们讨论到现在的面积公式
        title = Title("行列式")
        titleline = TitleLine()
        vector_cd = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8).scale(0.8, about_point = ORIGIN).shift(4*LEFT)
        self.play(title.shift(UP).animate.shift(DOWN), GrowFromPoint(titleline, 4*UP), formula.animate.shift(DOWN), 
                  *[FadeOut(mob) for mob in list_1 + list_2 + [tex_1, tex_2]], *[FadeOut(mob, DOWN) for mob in [vector_1, vector_2, line_a, line_b, line, line_2, parallelogram_1, parallelogram_2, fill_1, fill_2]],
                  *[mob.animate.shift(DOWN) for mob in [axis_x, axis_y]], label_A.animate.shift(DOWN).set_fill(color = BLUE), label_B.animate.shift(DOWN).set_fill(color = GREEN), FadeIn(vector_cd, DOWN), vector.animate.shift(DOWN).set_color(BLUE), parallelogram_0.animate.shift(DOWN).set_style(fill_opacity = 0.8, stroke_color = WHITE))
        self.wait(2, 22) #其实就是大名鼎鼎的行列式

#################################################################### 

class Video_5(FrameScene):
    def construct(self):
        title = Title("行列式")
        titleline = TitleLine()
        formula = MTex(r"S=ad-bc", tex_to_color_map = {(r"S", r"ad-bc"): YELLOW}).shift(2*UP)

        offset = 2*DOWN + 2*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 4.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([4, 4, 0])
        p_C = offset + np.array([1, 3, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.8)
        label_A = MTex(r"(a, b)", fill_color = BLUE).next_to(p_A, RIGHT).set_stroke(**stroke_dic)
        label_B = MTex(r"(c, d)", fill_color = GREEN).next_to(p_C, UP).set_stroke(**stroke_dic)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        example = [axis_x, axis_y, parallelogram, label_A, label_B, vector_a, vector_b]
        for mob in example:
            mob.scale(0.8, about_point = ORIGIN).shift(4*LEFT)
        self.add(title, titleline, formula, *example).wait(1, 4) #它一般被写成

        tex_a, tex_b = r"\begin{bmatrix}{a}\\{b}\end{bmatrix}", r"\begin{bmatrix}{c}\\{d}\end{bmatrix}"
        texs = r"\begin{vmatrix}{a}&{c}\\{b}&{d}\end{vmatrix}=", r"\det\left(" + tex_a + r"," + tex_b + r"\right)", r"=\det\left(\begin{bmatrix}{a}&{c}\\{b}&{d}\end{bmatrix}\right)", 
        text = MTex("".join(texs), isolate = texs, tex_to_color_map = {(r"{a}", r"{b}", tex_a): BLUE, (r"{c}", r"{d}", tex_b): GREEN}).scale(0.8).next_to(1.3*LEFT, buff = 0)
        parts = [text.get_part_by_tex(tex) for tex in texs]
        right = VGroup(*parts[1], *parts[2]).save_state().set_x(-1.3, LEFT)
        parts[2].save_state().match_x(parts[1], RIGHT)
        shade = BackgroundRectangle(parts[2], buff = 0.1)
        self.play(Write(parts[1]))
        # self.wait() #这样...
        self.add(parts[2], shade, parts[1]).play(parts[2].animate.restore())
        self.remove(shade).wait(0+1-2, 29+13) #...或者这样
        shade = BackgroundRectangle(parts[0], buff = 0.1)
        self.add(parts[0], shade, right).play(right.animate.restore(), follow(shade, right, remover = True))
        self.wait(1, 4) #或者我们最熟悉的这样
        self.wait(0, 28) #（空闲）
        text_2 = MTex(r"=ad-bc", tex_to_color_map = {(r"a", r"b"): BLUE, (r"c", r"d"): GREEN}).scale(0.8)
        text_2.shift(parts[0][-1].get_center() - text_2[0].get_center() + DOWN)
        self.play(Write(text_2))
        self.wait(2, 3) #它在二维时的值 我们已经知道了

        self.fade_out(excepts = [title, titleline])
        axes = ImageMobject(r"Patch_5.png", height = 6).shift(4*LEFT)
        texs = r"\vec{v}_1=\begin{bmatrix}x_1\\y_1\\z_1\end{bmatrix}", r"\vec{v}_2=\begin{bmatrix}x_2\\y_2\\z_2\end{bmatrix}", r"\vec{v}_3=\begin{bmatrix}x_3\\y_3\\z_3\end{bmatrix}"
        vectors = MTex(r",\ ".join(texs), tex_to_color_map = {texs[0]: BLUE, texs[1]: GREEN, texs[2]: PURPLE_B}).scale(0.8).next_to(1*LEFT + 2*UP)
        self.play(FadeIn(axes), FadeIn(vectors))
        self.wait(0, 21) #行列式可以定义在任何维度上

        text = MTex(r"\det(\vec{v}_1, \vec{v}_2, \vec{v}_3)=\begin{vmatrix}x_1&x_2&x_3\\y_1&y_2&y_3\\z_1&z_2&z_3\end{vmatrix}", isolate = texs, tex_to_color_map = {(r"x_1", r"y_1", r"z_1", r"\vec{v}_1"): BLUE, (r"x_2", r"y_2", r"z_2", r"\vec{v}_2"): GREEN, (r"x_3", r"y_3", r"z_3", r"\vec{v}_3"): PURPLE}).scale(0.8).next_to(0.8*LEFT + 0.5*DOWN, buff = 0)
        self.play(FadeIn(text, LEFT))
        self.wait(0, 18) #比如说 在三维的时候
        self.wait(3, 12) #它就表示一个平行六面体的体积
        expand = MTex(r"=x_1y_2z_3-x_1z_2y_3-y_1x_2z_3+y_1z_2x_3+z_1x_2y_3-z_1y_2x_3", tex_to_color_map = {(r"x_1", r"y_1", r"z_1"): BLUE, (r"x_2", r"y_2", r"z_2"): GREEN, (r"x_3", r"y_3", r"z_3"): PURPLE}).scale(0.8)
        expand.shift(2*DOWN + 2*RIGHT)
        self.play(Write(expand))
        self.wait(1+1-2, 29+10) #具体的展开式长这样 一共有6项
        self.wait(1, 2) #（空闲）
        
        self.wait(3, 1) #既然二维情况我们能算出正确结果
        
class Patch_5(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*OUT)

        x, y, z = np.array([1, -2, 1]), np.array([1, 2, 1]), np.array([0, 1, 2])
        vector_a, vector_b, vector_c = Arrow(ORIGIN, x, buff = 0, color = BLUE, stroke_width = 8), Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True, stroke_width = 8), depth_test = True)
        volume_1 = Parallelepiped(x=x, y=y, z=z, opacity = 0.8, color = BLUE)
        self.add(axes, volume_1, vector_a, vector_b, vector_c)

#################################################################### 
        
class Parallelogram3D(Surface):
    CONFIG = {
        "u_range": (0, 1),
        "v_range": (0, 1),
        "resolution": (2, 2),
    }

    def __init__(self, x: np.ndarray = RIGHT, y: np.ndarray = UP, **kwargs):
        self.x, self.y = x, y
        super().__init__(**kwargs)
        
    def uv_func(self, u: float, v: float) -> np.ndarray:
        return u*self.x + v*self.y
        
class Parallelepiped(SGroup):
    CONFIG = {
        "reflectiveness": 0,
        "gloss": 0.3,
        "shadow": 0.6,
        "opacity": 0.5,
    }
    def __init__(self, x: np.ndarray = RIGHT, y: np.ndarray = UP, z: np.ndarray = OUT, **kwargs):
        self.x, self.y, self.z = x, y, z
        super().__init__(*self.square_to_cube_faces(**kwargs))

    def square_to_cube_faces(self, **kwargs) -> list[Parallelogram3D]:
        xy, yz, zx = Parallelogram3D(self.x, self.y, **kwargs), Parallelogram3D(self.y, self.z, **kwargs), Parallelogram3D(self.z, self.x, **kwargs)
        z, x, y = xy.copy().shift(self.z), yz.copy().shift(self.x), zx.copy().shift(self.y)
        return [xy, yz, zx, z, x, y]

class Video_6(FrameScene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*OUT)

        x, y, z = np.array([1, -2, 1]), np.array([1, 2, 1]), np.array([0, 1, 2])
        vector_a, vector_b, vector_c = Arrow(ORIGIN, x, buff = 0, color = BLUE), Arrow(ORIGIN, y, buff = 0, color = GREEN), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        volume_0 = Parallelepiped(x=x, y=y, z=z, opacity = 0.3, color = BLUE, depth_test = True)
        self.add(axes, volume_0[5], volume_0[0], volume_0[1], volume_0[2], volume_0[3], volume_0[4], vector_a, vector_b, vector_c)
        self.wait(2+1-2, 11+8) #那三维应该也不难 和二维情况一样
        self.play(camera.animate.set_orientation(Rotation(quaternion_mult(quad(OUT, -PI/8), quad(RIGHT, PI/2 - PI/10)))), run_time = 2)

        volume_1, volume_2, volume_3 = Parallelepiped(x=x*3/8, y=y, z=z, opacity = 0.3, color = BLUE, depth_test = True), Parallelepiped(x=x*4/8, y=y, z=z, opacity = 0.3, color = BLUE, depth_test = True).shift(3/8*x), Parallelepiped(x=x*1/8, y=y, z=z, opacity = 0.3, color = BLUE, depth_test = True).shift(7/8*x)
        vector_1, vector_2, vector_3 = Arrow(ORIGIN, x*RIGHT, buff = 0, color = RED), Arrow(x*RIGHT, x*UR, buff = 0, color = ORANGE), Arrow(x*UR, x, buff = 0, color = YELLOW)
        self.play(ShowCreation(VGroup(vector_1, vector_2, vector_3)))
        self.wait(1, 18) #我们首先还是把一个向量按坐标分解
        old = [volume_1[5], volume_2[5], volume_3[5], volume_1[0], volume_2[0], volume_3[0], volume_1[1], volume_1[2], volume_2[2], volume_3[2], volume_1[3], volume_2[3], volume_3[3], volume_3[4]]
        extra = [volume_1[4], volume_2[1], volume_2[4], volume_3[1]]
        self.remove(*volume_0).add(*extra, *old).play(*[FadeIn(mob, -1.5*z) for mob in extra])
        self.wait(2, 9) #然后过这些向量的端点作平行平面

        volume_4, volume_5, volume_6 = Parallelepiped(x=x*RIGHT, y=y, z=z, opacity = 0.3, color = RED, depth_test = True), Parallelepiped(x=x*UP, y=y, z=z, opacity = 0.3, color = ORANGE, depth_test = True).shift(x*RIGHT), Parallelepiped(x=OUT, y=y, z=z, opacity = 0.3, color = YELLOW, depth_test = True).shift(x*UR)
        self.play(*[Transform(mob_1, mob_2) for mob_1, mob_2 in zip(volume_1, volume_4)], *[Transform(mob_1, mob_2) for mob_1, mob_2 in zip(volume_2, volume_5)], *[Transform(mob_1, mob_2) for mob_1, mob_2 in zip(volume_3, volume_6)])
        self.wait(0, 17) #把平行六面体分成三块
        last = ImageMobject("Video_6.png", height = 8).fix_in_frame()
        self.play(FadeIn(last))

class Video_6_2(FrameScene):
    def construct(self):
        last = ImageMobject("Video_6.png", height = 8)
        self.add(last)

        tex = MTex(r"&\begin{vmatrix}x_1\\y_1&\vec{v}_2&\vec{v}_3\\z_1\end{vmatrix}\\=&\begin{vmatrix}{x_1}\\0&\vec{v}_2&\vec{v}_3\\0\end{vmatrix}+\begin{vmatrix}0\\{y_1}&\vec{v}_2&\vec{v}_3\\0\end{vmatrix}+\begin{vmatrix}0\\0&\vec{v}_2&\vec{v}_3\\{z_1}\end{vmatrix}", tex_to_color_map = {(r"x_1", r"y_1", r"z_1"): BLUE, r"{x_1}": RED, r"{y_1}": ORANGE, r"{z_1}": YELLOW, r"\vec{v}_2": GREEN, r"\vec{v}_3": PURPLE, r"0": GREY}).shift(3*LEFT + 1*UP).scale(0.8).fix_in_frame()
        self.play(last.animate.shift(4*RIGHT), OverFadeIn(tex, 2*RIGHT), run_time = 2)
        self.wait(0, 11) #如果把式子写出来会是这个样子的
        self.wait(0, 16) #（空闲）

        self.fade_out()
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/8), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*OUT)
        x, y, z = np.array([0, 0, 1]), np.array([1, 2, 1]), np.array([0, 1, 2])
        vector_a, vector_b, vector_c = Arrow(ORIGIN, x, buff = 0, color = YELLOW), Arrow(ORIGIN, y, buff = 0, color = GREEN), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True)
        volume_0 = Parallelepiped(x=x, y=y, z=z, opacity = 0.3, color = YELLOW, depth_test = True)
        tex = MTex(r"\begin{vmatrix}0&x_2&x_3\\0&y_2&y_3\\z_1&z_2&z_3\end{vmatrix}", tex_to_color_map = {r"z_1": YELLOW, r"0": GREY, (r"x_2", r"y_2", r"z_2"): GREEN, (r"x_3", r"y_3", r"z_3"): PURPLE}).shift(5*LEFT + 2*UP).fix_in_frame()
        tex_2 = MTex(r"&\begin{vmatrix}0&x_2&x_3\\0&y_2&y_3\\z_1&0&0\end{vmatrix}\\=&z_1\begin{vmatrix}x_2&x_3\\y_2&y_3\end{vmatrix}", tex_to_color_map = {r"z_1": YELLOW, r"0": GREY, (r"x_2", r"y_2"): GREEN, (r"x_3", r"y_3"): PURPLE}).fix_in_frame()
        tex_2.shift(tex[0].get_center() - tex_2[0].get_center())
        self.fade_in(axes, *volume_0, vector_a, vector_b, vector_c, tex)
        self.wait(0, 17) #接着我们就和二维情况一样

        y2, z2 = np.array([1, 2, 0]), np.array([0, 1, 0])
        line = VMobject().set_points(DashedLine(z, z2).get_all_points())
        self.play(camera.animate.set_orientation(Rotation(quaternion_mult(quad(OUT, -PI/3), quad(RIGHT, PI/2 - PI/10)))))
        self.wait(1, 3) #去看其中一块的体积
        self.wait(1, 1) #（空闲）

        vector_b2, vector_c2 = Arrow(ORIGIN, y2, buff = 0, color = GREEN), Arrow(ORIGIN, z2, buff = 0, color = PURPLE_B)
        volume_1 = Parallelepiped(x=x, y=y, z=z2, opacity = 0.3, color = YELLOW, depth_test = True)
        volume_1[0].set_color(RED).set_opacity(0.5), volume_1[3].set_color(RED).set_opacity(0.5)
        volume_2 = Parallelepiped(x=x, y=y2, z=z2, opacity = 0.3, color = YELLOW, depth_test = True)
        volume_2[2].set_color(RED).set_opacity(0.5), volume_2[5].set_color(RED).set_opacity(0.5)
        self.play(volume_0[0].animate.set_color(RED).set_opacity(0.5), volume_0[3].animate.set_color(RED).set_opacity(0.5), IndicateAround(tex[20:22]), ShowCreation(line), 
                  Transform(tex[20], tex_2[19], delay = 1), Transform(tex[21], tex_2[19], remover = True, delay = 1), *[Transform(mob1, mob2, delay = 1) for mob1, mob2 in zip(volume_0, volume_1)], Transform(vector_c, vector_c2, delay = 1), Uncreate(line.reverse_points(), delay = 1))
        self.play(volume_0[0].animate.set_color(YELLOW).set_opacity(0.3), volume_0[3].animate.set_color(YELLOW).set_opacity(0.3), camera.animate.set_orientation(Rotation(quaternion_mult(quad(OUT, -PI*2/3), quad(RIGHT, PI/2 - PI/10)))))
        line = VMobject().set_points(DashedLine(y, y2).get_all_points())
        self.play(volume_0[2].animate.set_color(RED).set_opacity(0.5), volume_0[5].animate.set_color(RED).set_opacity(0.5), IndicateAround(tex[18:20]), ShowCreation(line), 
                  Transform(tex[18], tex_2[18], delay = 1), Transform(tex[19], tex_2[18], remover = True, delay = 1), *[Transform(mob1, mob2, delay = 1) for mob1, mob2 in zip(volume_0, volume_2)], Transform(vector_b, vector_b2, delay = 1), Uncreate(line.reverse_points(), delay = 1))
        self.play(volume_0[2].animate.set_color(YELLOW).set_opacity(0.3), volume_0[5].animate.set_color(YELLOW).set_opacity(0.3), camera.animate.set_orientation(Rotation(quaternion_mult(quad(OUT, -PI/2-PI/12), quad(RIGHT, PI/2 - PI/10)))))
        self.wait(2+0+1+2-6, 29+17+12+2) #这块平行六面体没办法直接底乘高 （空闲） 我们可以将它的面平移 让它的底移动到xOy平面上

        tex_3 = MTex(r"\begin{vmatrix}x_2&x_3\\y_2&y_3\end{vmatrix}", color = RED).set_stroke(**stroke_dic).scale(0.8).move_to(1.5*DOWN + 2*LEFT).fix_in_frame()
        tex_4 = MTex(r"z_1", color = YELLOW).set_stroke(**stroke_dic).scale(0.8).next_to(ORIGIN, RIGHT).fix_in_frame()
        self.play(*[volume_0[i].animate.set_opacity(0.1) for i in [0, 2, 3, 4, 5]], volume_0[1].animate.set_color(RED).set_opacity(0.5), Write(tex_3), Write(tex_4), run_time = 1)
        self.play(Write(tex_2[26:]), run_time = 1)
        self.wait(0, 11) #再使用底乘高 就能求出这一块的体积了
        self.wait(0, 18) #（空闲）

        camera.set_orientation(Rotation(np.array([0, 0, 0, 1]))).shift(0.5*IN)
        tex = MTex(r"&\begin{vmatrix}x_1&x_2&x_3\\y_1&y_2&y_3\\z_1&z_2&z_3\end{vmatrix}\\=&\begin{vmatrix}{x_1}&x_2&x_3\\0&y_2&y_3\\0&z_2&z_3\end{vmatrix}+\begin{vmatrix}0&x_2&x_3\\{y_1}&y_2&y_3\\0&z_2&z_3\end{vmatrix}+\begin{vmatrix}0&x_2&x_3\\0&y_2&y_3\\{z_1}&z_2&z_3\end{vmatrix}\\&+{x_1}\begin{vmatrix}y_2&y_3\\z_2&z_3\end{vmatrix}-{y_1}\begin{vmatrix}x_2&x_3\\z_2&z_3\end{vmatrix}+{z_1}\begin{vmatrix}x_2&x_3\\y_2&y_3\end{vmatrix}", tex_to_color_map = {(r"x_1", r"y_1", r"z_1"): BLUE, r"{x_1}": RED, r"{y_1}": ORANGE, r"{z_1}": YELLOW, (r"x_2", r"y_2", r"z_2"): GREEN, (r"x_3", r"y_3", r"z_3"): PURPLE, r"0": GREY}).shift(3*LEFT + UP).scale(0.8).fix_in_frame()
        part_0, part_1, part_2, part_3, other = tex[:117], tex[118:136], tex[137:155], tex[156:], VGroup(tex[117], tex[136], tex[155])
        tex[30:117].shift(0.5*DOWN), tex[117:136].match_x(tex[31:59]).shift(1.5*DOWN), tex[136:155].match_x(tex[60:88]).shift(1.5*DOWN), tex[155:].match_x(tex[89:117]).shift(1.5*DOWN)
        self.clear().fade_in(last, part_0, part_3)
        self.play(FadeIn(part_1, 0.5*DOWN), FadeIn(part_2, 0.5*DOWN, delay = 0.2), frames = 36)
        self.wait(0, 4) #剩下两块也是一样 有类似的公式
        self.wait(0, 19) #（空闲）
        self.play(IndicateAround(tex[117]), IndicateAround(tex[117].copy().move_to(tex[136])), IndicateAround(tex[155]))
        self.wait(2, 4) #但现在问题在于 这三块体积的符号该如何确定呢
        self.wait(0, 24) #（空闲）

        # def perspective(point: np.ndarray):
        #     position = 0.5*OUT
        #     distance = 16
        #     orientation = Rotation(quaternion_mult(quad(OUT, -PI/8), quad(RIGHT, PI/2 - PI/10))).as_matrix()
        #     raw = np.dot(orientation.T, point - position) - distance*OUT
        #     if math.isclose(raw[2], 0):
        #         ratio = 0
        #         point = np.array([10000*raw[0], 10000*raw[1], 0])
        #     else:
        #         ratio = -distance/raw[2]
        #         point = raw*ratio + distance*OUT
        #     return point + 4*RIGHT
        # p0, p1, p2, p3 = perspective(np.array([0, 0, 0])), perspective(np.array([1, 0, 0])), perspective(np.array([1, -2, 0])), perspective(np.array([1, -2, 1]))
        # self.play(IndicateAround(Line(p0, p1)), IndicateAround(Line(p2, p3)))
        # self.wait()
        # self.play(Write(tex[117]), Write(tex[155]))
        # self.wait()
        # self.play(IndicateAround(Line(p1, p2)))
        # self.wait()
        # self.play(Write(tex[136]))
        # self.wait()

        self.wait(3, 17) #要知道 三维情况很难像二维那样看图说话
        self.wait(2, 1) #我们知道这三块应该加起来
        self.wait(2, 3) #所以有向体积应该都是正的
        self.play(IndicateAround(part_1[2:]), IndicateAround(part_2[2:]), IndicateAround(part_3[2:]))
        self.wait(1+3-2, 20+6) #但我们现在甚至不知道 这三个二阶行列式应该被看做正面积还是负面积
        self.wait(0, 16) #（空闲）
        self.wait(2, 17) #而这也就说明 我们需要转换思路了
        self.wait(1, 8) #（空闲）

#################################################################### 

"""
class Video_7(FrameScene):
    def construct(self):
        formula = MTex(r"\det\left(\vec{u}, \vec{v}\right)", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": GREEN}).shift(3*UP)

        offset = 2.5*DOWN + 0.5*LEFT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        label_A = MTex(r"(a, b)", color = BLUE).next_to(p_A, RIGHT)
        label_B = MTex(r"(c, d)", color = GREEN).next_to(p_C, LEFT)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        vector_s = Arrow(p_D, p_A, color = TEAL, buff = 0, stroke_width = 8)
        vector_d = Arrow(p_A, p_A, color = GREEN_E, buff = 0, stroke_width = 8)
        group = VGroup(parallelogram, vector_s, vector_d)
        list_1 = [axis_x, axis_y, parallelogram_0, group, label_A, label_B, vector_a, vector_b]
        self.add(formula, *list_1).wait()

        alpha = ValueTracker(0.0)
        def group_updater(mob: VGroup):
            value = alpha.get_value()
            diff = -value*np.array([-2, 3, 0])
            mob[0].match_points(Polygon(p_A+diff, p_B+diff, p_C, p_D))
            mob[1].become(Arrow(p_D, p_A+diff, color = TEAL, buff = 0, stroke_width = 8))
            mob[2].become(Arrow(p_A, p_A+diff, color = GREEN_E, buff = 0, stroke_width = 8))
        group.add_updater(group_updater)
        self.play(alpha.animate.set_value(1/6))
        self.wait()
        self.play(alpha.animate.set_value(-1/3))
        group.clear_updaters()
        self.wait()

        axiom_1 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=\det\left(\vec{u}+k\vec{v}, \vec{v}\right)", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": GREEN, r"k": YELLOW}).scale(0.8).shift(4*LEFT + 2*DOWN)
        self.play(*[mob.animate.scale(0.5, about_point = ORIGIN).shift(4*LEFT + 0.5*UP) for mob in list_1])
        self.wait()
        self.play(Write(axiom_1))
        self.wait()

        offset = 2*DOWN + 2*RIGHT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        p_E1, p_E2, p_E3 = offset + np.array([1, 0, 0]), offset + np.array([2, 0, 0]), offset + np.array([3, 0, 0])
        p_F1, p_F2, p_F3 = offset + np.array([3, 1, 0])*3/11, offset + np.array([3, 1, 0])*6/11, offset + np.array([3, 1, 0])*9/11
        p_G1, p_G2, p_G3 = offset + np.array([3, 1, 0])*3/11 + np.array([-2, 3, 0]), offset + np.array([3, 1, 0])*6/11 + np.array([-2, 3, 0]), offset + np.array([3, 1, 0])*9/11 + np.array([-2, 3, 0])
        p_H1, p_H2, p_H3 = offset + np.array([1, 0, 0]) + np.array([-2, 3, 0]), offset + np.array([2, 0, 0]) + np.array([-2, 3, 0]), offset + np.array([3, 0, 0]) + np.array([-2, 3, 0])
        parallelogram = Polygon(p_A, p_B, p_C, p_D)
        fill_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        label_A = MTex(r"(a, b)", color = BLUE).next_to(p_A, RIGHT)
        label_B = MTex(r"(c, d)", color = GREEN).next_to(p_C, LEFT)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        self.fade_in(axis_x, axis_y, parallelogram_0, fill_0, parallelogram, label_A, label_B, vector_a, vector_b, excepts = [formula, axiom_1] + list_1).wait()

        line_0 = [Line(p_F1, p_G1), Line(p_F2, p_G2), Line(p_F3, p_G3)]
        self.add(*line_0, vector_a, vector_b).play(*[ShowCreation(mob) for mob in line_0])
        self.wait()
        line_1 = [Line(p_G1, p_H1, color = GREY), Line(p_G2, p_H2, color = GREY), Line(p_G3, p_H3, color = GREY)]
        points_1 = [[p_F1, p_G1, p_C, p_D], [p_F2, p_G2, p_G1, p_F1], [p_F3, p_G3, p_G2, p_F2], [p_A, p_B, p_G3, p_F3]]
        points_2 = [[p_E1, p_H1, p_C, p_D], [p_E2, p_H2, p_H1, p_E1], [p_E3, p_H3, p_H2, p_E2], [p_A, p_B, p_H3, p_E3]]
        parallelograms = [Polygon(*points) for points in points_1]
        fills = [Polygon(*points, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0) for points in points_1]
        nodes_1 = [[p_D, p_E1], [p_E1, p_E2], [p_E2, p_E3]]
        vectors = [Arrow(*nodes, color = TEAL, buff = 0, stroke_width = 8) for nodes in nodes_1] + [Arrow(p_E3, p_A, color = PURPLE_B, buff = 0, stroke_width = 8)]
        nodes_2 = [[p_D, p_F1], [p_F1, p_F2], [p_F2, p_F3]]
        sources = [Line.set_stroke(Arrow(*nodes, color = BLUE, buff = 0), width = 8) for nodes in nodes_2] + [Arrow(p_F3, p_A, color = BLUE, buff = 0, stroke_width = 8)]
        self.remove(parallelogram, fill_0, *line_0).bring_to_back(*fills).add(*line_1, *parallelograms, vector_a, vector_b).play(
            *[ReplacementTransform(source, vector) for source, vector in zip(sources, vectors)],
            *[Transform(stroke, Polygon(*points)) for stroke, points in zip(parallelograms, points_2)],
            *[Transform(fill, Polygon(*points, fill_color = TEAL if i<3 else PURPLE_B, fill_opacity = 0.5, stroke_width = 0)) for fill, points, i in zip(fills, points_2, [0, 1, 2, 3])],
            *[ShowCreation(mob) for mob in line_1])
        self.wait()

        list_2 = [axis_x, axis_y, parallelogram_0, *fills, *line_1, *parallelograms, label_A, label_B, vector_a, vector_b, *vectors]
        axiom_2 = MTex(r"\det\left(\vec{u}_1+k\vec{u}_2, \vec{v}\right)=\det\left(\vec{u}_1, \vec{v}\right)+k\det\left(\vec{u}_2, \vec{v}\right)", tex_to_color_map = {(r"\vec{u}_1", r"\vec{u}_2"): BLUE, r"\vec{v}": GREEN, r"k": YELLOW}).scale(0.8).shift(3*RIGHT + 2*DOWN)
        self.play(*[mob.animate.scale(0.5, about_point = 0.5*DOWN).shift(3*RIGHT + 0.5*UP) for mob in list_2])
        self.wait()
        self.play(Write(axiom_2))
        self.wait()

        offset = 0.5*UP + 0.5*LEFT
        axis_x, axis_y = Arrow(0.5*LEFT, 1.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 1.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([1, 0, 0])
        p_B = offset + np.array([1, 1, 0])
        p_C = offset + np.array([0, 1, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.6)
        label_A = MTex(r"(1, 0)").scale(0.5).next_to(p_A, DR, buff = 0.1)
        label_B = MTex(r"(0, 1)").scale(0.5).next_to(p_C, LEFT, buff = 0.1)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        axiom_3 = MTex(r"\begin{vmatrix}1&0\\0&1\end{vmatrix}=1").scale(0.8).shift(0.5*DOWN)
        axiom_3[4].set_color(BLUE), axiom_3[5].set_color(GREEN), axiom_3[6].set_color(BLUE), axiom_3[7].set_color(GREEN), axiom_3[-1].set_color(YELLOW)
        divides = Polyline(2.5*UP + 2*LEFT, 1.25*DOWN + 2*LEFT, 1.25*DOWN + 2*RIGHT, 2.5*UP + 2*RIGHT, color = GREY).append_points(Line(1.25*DOWN + 1.25*LEFT, 2.5*DOWN + 1.25*LEFT).get_points())
        list_3 = [axis_x, axis_y, parallelogram, label_A, label_B, vector_a, vector_b, axiom_3, divides]
        self.fade_in(*list_3, excepts = [formula, axiom_1, axiom_2] + list_1 + list_2).wait()

        title = Title(r"唯一确定行列式的三条公理")
        titleline = TitleLine()
        self.play(title.shift(UP).animate.shift(DOWN), GrowFromPoint(titleline, 4*UP), FadeOut(formula, 0.5*DOWN))
        self.wait()

        self.fade_out(excepts = list_3 + [title, titleline])
        self.wait()

        offset = 2.5*DOWN + 0.5*LEFT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        diff = 1/3*np.array([3, 1, 0])
        parallelogram = Polygon(p_A, p_B + diff, p_C + diff, p_D, fill_color = YELLOW, fill_opacity = 0.5)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        label_A = MTex(r"(a, b)", color = BLUE).next_to(p_A, RIGHT)
        label_B = MTex(r"(c, d)", color = GREEN).next_to(p_C, LEFT)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        vector_s = Arrow(p_D, p_C + diff, color = TEAL, buff = 0, stroke_width = 8)
        vector_d = Arrow(p_C, p_C + diff, color = BLUE_E, buff = 0, stroke_width = 8)
        group = VGroup(parallelogram, vector_s, vector_d)
        list_1 = [axis_x, axis_y, parallelogram_0, group, label_A, label_B, vector_a, vector_b]
        for mob in list_1:
            mob.scale(0.5, about_point = ORIGIN).shift(4.5*LEFT + 0.5*UP)
        axiom_1 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=\det\left(\vec{u}, \vec{v}+k\vec{u}\right)", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": GREEN, r"k": YELLOW}).scale(0.8).shift(4*LEFT + 2*DOWN)
        
        offset = 2*DOWN + 2*RIGHT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        x, y = np.array([3, 1, 0]), np.array([-2, 3, 0])
        p_A = offset + x
        p_B = offset + x + y
        p_C = offset + y
        p_D = offset
        p_E1, p_E2, p_E3, p_E4 = offset + np.array([-1, 0, 0]), offset + np.array([-2, 0, 0]), offset + np.array([-2, 1, 0]), offset + np.array([-2, 2, 0])
        p_F1, p_F2, p_F3, p_F4 = offset + y*1/11, offset + y*2/11, offset + y*5/11, offset + y*8/11
        p_G1, p_G2, p_G3, p_G4 = offset + y*1/11 + x, offset + y*2/11 + x, offset + y*5/11 + x, offset + y*8/11 + x
        p_H1, p_H2, p_H3, p_H4 = offset + np.array([-1, 0, 0]) + x, offset + np.array([-2, 0, 0]) + x, offset + np.array([-2, 1, 0]) + x, offset + np.array([-2, 2, 0]) + x
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        label_A = MTex(r"(a, b)", color = BLUE).next_to(p_A, RIGHT)
        label_B = MTex(r"(c, d)", color = GREEN).next_to(p_C, LEFT)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)

        line_1 = [Line(p_G1, p_H1, color = GREY), Line(p_G2, p_H2, color = GREY), Line(p_G3, p_H3, color = GREY), Line(p_G4, p_H4, color = GREY)]
        points_2 = [[p_E1, p_H1, p_A, p_D], [p_E2, p_H2, p_H1, p_E1], [p_E3, p_H3, p_H2, p_E2], [p_E4, p_H4, p_H3, p_E3], [p_C, p_B, p_H4, p_E4]]
        parallelograms = [Polygon(*points) for points in points_2]
        fills = [Polygon(*points, fill_color = TEAL if i<2 else LIME, fill_opacity = 0.5, stroke_width = 0) for i, points in enumerate(points_2)]
        nodes_1 = [[p_D, p_E1], [p_E1, p_E2], [p_E2, p_E3], [p_E3, p_E4], [p_E4, p_C]]
        vectors = [Arrow(*nodes, color = TEAL if i<2 else LIME, buff = 0, stroke_width = 8) for i, nodes in enumerate(nodes_1)]
        list_2 = [axis_x, axis_y, parallelogram_0, *fills, *line_1, *parallelograms, label_A, label_B, vector_a, vector_b, *vectors]
        for mob in list_2:
            mob.scale(0.5, about_point = 0.5*DOWN).shift(3*RIGHT + 0.5*UP)
        axiom_2 = MTex(r"\det\left(\vec{u}, \vec{v}_1+k\vec{v}_2\right)=\det\left(\vec{u}, \vec{v}_1\right)+k\det\left(\vec{u}, \vec{v}_2\right)", tex_to_color_map = {r"\vec{u}": BLUE, (r"\vec{v}_1", r"\vec{v}_2"): GREEN, r"k": YELLOW}).scale(0.8).shift(3*RIGHT + 2*DOWN)
        
        self.fade_in(*list_1, axiom_1, *list_2, axiom_2, excepts = list_3 + [title, titleline])
        self.wait()
"""

class Patch7_1(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        offset = 2*DOWN
        axis_x, axis_y = Arrow(3.5*LEFT, 3.5*RIGHT, stroke_width = 4).shift(offset), Arrow(1*DOWN, 5*UP, stroke_width = 4).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        diff = 1/3*np.array([-2, 3, 0])
        parallelogram = Polygon(p_A+diff, p_B+diff, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 6)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY, stroke_width = 6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 10)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 10)
        vector_s = Arrow(p_D, p_A+diff, color = TEAL, buff = 0, stroke_width = 10)
        vector_d = Arrow(p_A, p_A+diff, color = GREEN_E, buff = 0, stroke_width = 10)
        group = VGroup(parallelogram, vector_s, vector_d)
        list_1 = [axis_x, axis_y, parallelogram_0, group, vector_a, vector_b]
        self.add(*list_1)

class Patch7_2(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        offset = 2*DOWN
        axis_x, axis_y = Arrow(3.5*LEFT, 3.5*RIGHT, stroke_width = 4).shift(offset), Arrow(1*DOWN, 5*UP, stroke_width = 4).shift(offset)
        x, y = np.array([3, 1, 0]), np.array([-2, 3, 0])
        p_A = offset + x
        p_B = offset + x + y
        p_C = offset + y
        p_D = offset
        p_E1, p_E2, p_E3 = offset + np.array([1, 0, 0]), offset + np.array([2, 0, 0]), offset + np.array([3, 0, 0])
        p_F1, p_F2, p_F3 = offset + x*3/11, offset + x*6/11, offset + x*9/11
        p_G1, p_G2, p_G3 = offset + x*3/11 + y, offset + x*6/11 + y, offset + x*9/11 + y
        p_H1, p_H2, p_H3 = offset + np.array([1, 0, 0]) + y, offset + np.array([2, 0, 0]) + y, offset + np.array([3, 0, 0]) + y
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY, stroke_width = 6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 10)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 10)
        
        line_1 = [Line(p_G1, p_H1, color = GREY, stroke_width = 6), Line(p_G2, p_H2, color = GREY, stroke_width = 6), Line(p_G3, p_H3, color = GREY, stroke_width = 6)]
        points_2 = [[p_E1, p_H1, p_C, p_D], [p_E2, p_H2, p_H1, p_E1], [p_E3, p_H3, p_H2, p_E2], [p_A, p_B, p_H3, p_E3]]
        parallelograms = [Polygon(*points, fill_color = TEAL if i<3 else PURPLE_B, fill_opacity = 0.5, stroke_width = 6) for i, points in enumerate(points_2)]
        nodes_1 = [[p_D, p_E1], [p_E1, p_E2], [p_E2, p_E3]]
        vectors = [Arrow(*nodes, color = TEAL, buff = 0, stroke_width = 10) for nodes in nodes_1] + [Arrow(p_E3, p_A, color = PURPLE_B, buff = 0, stroke_width = 10)]
        list_2 = [axis_x, axis_y, parallelogram_0, *line_1, *parallelograms, vector_a, vector_b, *vectors]
        self.add(*list_2)

class Patch7_3(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        offset = 2*DOWN + LEFT
        axis_x, axis_y = Arrow(1.5*LEFT, 3.5*RIGHT, stroke_width = 4).shift(offset), Arrow(1*DOWN, 3.5*UP, stroke_width = 4).shift(offset)
        p_A = offset + np.array([2, 0, 0])
        p_B = offset + np.array([2, 2, 0])
        p_C = offset + np.array([0, 2, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.6, stroke_width = 6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 10)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 10)
        list_3 = [axis_x, axis_y, parallelogram, vector_a, vector_b]
        self.add(*list_3)

class Patch7_4(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        offset = 2*DOWN
        axis_x, axis_y = Arrow(3.5*LEFT, 3.5*RIGHT, stroke_width = 4).shift(offset), Arrow(1*DOWN, 5*UP, stroke_width = 4).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        diff = 1/3*np.array([3, 1, 0])
        parallelogram = Polygon(p_A, p_B + diff, p_C + diff, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 6)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY, stroke_width = 6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 10)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 10)
        vector_s = Arrow(p_D, p_C + diff, color = TEAL, buff = 0, stroke_width = 10)
        vector_d = Arrow(p_C, p_C + diff, color = BLUE_E, buff = 0, stroke_width = 10)
        group = VGroup(parallelogram, vector_s, vector_d)
        list_1 = [axis_x, axis_y, parallelogram_0, group, vector_a, vector_b]
        self.add(*list_1)

class Patch7_5(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        offset = 2*DOWN
        axis_x, axis_y = Arrow(3.5*LEFT, 3.5*RIGHT, stroke_width = 4).shift(offset), Arrow(1*DOWN, 5*UP, stroke_width = 4).shift(offset)
        x, y = np.array([3, 1, 0]), np.array([-2, 3, 0])
        p_A = offset + x
        p_B = offset + x + y
        p_C = offset + y
        p_D = offset
        p_E1, p_E2, p_E3, p_E4 = offset + np.array([-1, 0, 0]), offset + np.array([-2, 0, 0]), offset + np.array([-2, 1, 0]), offset + np.array([-2, 2, 0])
        p_F1, p_F2, p_F3, p_F4 = offset + y*1/11, offset + y*2/11, offset + y*5/11, offset + y*8/11
        p_G1, p_G2, p_G3, p_G4 = offset + y*1/11 + x, offset + y*2/11 + x, offset + y*5/11 + x, offset + y*8/11 + x
        p_H1, p_H2, p_H3, p_H4 = offset + np.array([-1, 0, 0]) + x, offset + np.array([-2, 0, 0]) + x, offset + np.array([-2, 1, 0]) + x, offset + np.array([-2, 2, 0]) + x
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY, stroke_width = 6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 10)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 10)

        line_1 = [Line(p_G1, p_H1, color = GREY, stroke_width = 6), Line(p_G2, p_H2, color = GREY, stroke_width = 6), Line(p_G3, p_H3, color = GREY, stroke_width = 6), Line(p_G4, p_H4, color = GREY, stroke_width = 6)]
        points_2 = [[p_E1, p_H1, p_A, p_D], [p_E2, p_H2, p_H1, p_E1], [p_E3, p_H3, p_H2, p_E2], [p_E4, p_H4, p_H3, p_E3], [p_C, p_B, p_H4, p_E4]]
        parallelograms = [Polygon(*points, fill_color = TEAL if i<2 else LIME, fill_opacity = 0.5, stroke_width = 6) for i, points in enumerate(points_2)]
        nodes_1 = [[p_D, p_E1], [p_E1, p_E2], [p_E2, p_E3], [p_E3, p_E4], [p_E4, p_C]]
        vectors = [Arrow(*nodes, color = TEAL if i<2 else LIME, buff = 0, stroke_width = 10) for i, nodes in enumerate(nodes_1)]
        list_2 = [axis_x, axis_y, parallelogram_0, *line_1, *parallelograms, vector_a, vector_b, *vectors]
        self.add(*list_2)
        
class Video_7(FrameScene):
    def construct(self):

        self.wait(0, 9) #（空闲）
        previous = ImageMobject("Video_1.png", height = 8)
        self.fade_in(previous)
        self.wait(1, 6) #之前我们发现过这样一件事
        self.wait(2, 27) #割补法和表达式总是保持一致
        self.wait(2, 18) #会变化的只有图像
        self.wait(2, 0) #那既然图像不靠谱
        self.wait(1, 26) #我们能不能直接从割补法出发
        self.wait(1, 21) #得到表达式呢
        self.wait(1, 10) #（空闲）

        self.fade_out()
        formula = MTex(r"\det\left(\vec{u}, \vec{v}\right)", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": GREEN}).shift(3*UP)

        offset = 2*DOWN + LEFT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        vector_s = Arrow(p_D, p_A, color = TEAL, buff = 0, stroke_width = 8)
        vector_d = Arrow(p_A, p_A, color = GREEN_E, buff = 0, stroke_width = 8)
        group = VGroup(parallelogram, vector_s, vector_d)
        list_1 = [axis_x, axis_y, parallelogram_0, group, vector_a, vector_b]
        self.fade_in(formula, *list_1).wait(0, 23) #让我们回到二维情况仔细思考一下啊
        self.wait(1, 16) #当我们提到面积
        self.wait(2, 6) #或者说体积这个概念的时候
        self.wait(1, 6) #我们究竟在说什么
        self.wait(2, 2) #它究竟有什么性质呢
        self.wait(2, 25) #比如说 在割补平行四边形的时候
        self.wait(2, 0) #我们利用了面积的这么两个性质
        self.wait(0, 18) #（空闲）

        self.clear()
        offset = 2*UP
        camera = self.camera.frame
        camera.shift(offset)
        parallelogram_0 = Rectangle(height = 4, width = 2, fill_color = interpolate_color(YELLOW, BLACK, 0.5), fill_opacity = 1).shift(offset)
        def shear(t: float):
            return parallelogram_0.copy().apply_matrix(np.array([[1, t], [0, 1]]))
        parallelogram = shear(-1)

        height_line1 = Line(ORIGIN, 4*UP)
        elbow = Elbow()
        height_1 = VGroup(height_line1, elbow).shift(6*LEFT).set_stroke(color = BLUE, width = 8)
        label_base = MTex(r"w", color = GREEN).next_to(ORIGIN, DOWN).set_stroke(**stroke_dic)
        label_height = MTex(r"h", color = BLUE).next_to(2*UP, LEFT).set_stroke(**stroke_dic).shift(6*LEFT)
        text_area = MTex(r"S=wh", tex_to_color_map = {r"S": YELLOW, r"w": GREEN, r"h": BLUE}).shift(3*UP + offset)
        line_base = Line(1*LEFT, 1*RIGHT, color = GREEN, stroke_width = 8)
        line_up, line_down = Line(LEFT_SIDE, RIGHT_SIDE, color = GREY).shift(4*UP), Line(LEFT_SIDE, RIGHT_SIDE, color = GREY)
        self.add(line_up, line_down, parallelogram, label_base, text_area, label_height, height_1, line_base).wait()
        copies = []
        alpha = ValueTracker(-1)
        step = 2/3
        parallelogram.counter = -1/step
        def fan_updater(mob: Rectangle):
            value = alpha.get_value()
            number = math.floor(value/step + 0.5)
            mob.become(shear(value))
            while number >= mob.counter:
                new = shear(mob.counter*step).set_fill(color = interpolate_color(YELLOW, BLACK, 0.8)).set_stroke(color = GREY)
                copies.append(new)
                self.add(new, mob, line_base)
                mob.counter += 1
        parallelogram.add_updater(fan_updater)
        self.play(alpha.animate.set_value(1), run_time = 2)
        parallelogram.clear_updaters()
        self.wait(1, 27) #第一个 是在一条边平行滑动的时候
        self.wait(2, 17) #平行四边形的的面积不变

        self.fade_out(run_time = 0.5)
        camera.shift(-offset)
        axiom_1 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=\det\left(\vec{u}+k\vec{v}, \vec{v}\right)", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": GREEN, r"k": YELLOW}).shift(3*RIGHT + UP)
        for mob in list_1:
            mob.shift(2*LEFT)
        offset = 2*DOWN + 3*LEFT
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        self.fade_in(formula, *list_1, axiom_1, run_time = 0.5)
        self.wait(1, 10) #这个操作如果用向量表示的话
        
        alpha = ValueTracker(0.0)
        def group_updater(mob: VGroup):
            value = alpha.get_value()
            diff = -value*np.array([-2, 3, 0])
            mob[0].match_points(Polygon(p_A+diff, p_B+diff, p_C, p_D))
            mob[1].become(Arrow(p_D, p_A+diff, color = TEAL, buff = 0, stroke_width = 8))
            mob[2].become(Arrow(p_A, p_A+diff, color = GREEN_E, buff = 0, stroke_width = 8))
        group.add_updater(group_updater)
        self.play(alpha.animate.set_value(-1/6))
        self.wait()
        self.play(alpha.animate.set_value(1/3))
        self.wait(1, 12) #那就是一个向量加上了另一个向量的倍数
        self.wait(1, 2) #这个体积是不变的
        self.wait(0, 23) #（空闲）

        p_W, p_H = offset + np.array([-2, 3, 0])/2, offset + np.array([-2, 3, 0])/2 + np.array([3, 2, 0])*11/13
        tex_w, tex_h = MTex(r"w", color = GREEN).scale(0.8).next_to(p_W, DL), MTex(r"h", color = ORANGE).scale(0.8).next_to((p_W+p_H)/2, UL).set_stroke(**stroke_dic)
        line_h = Line(p_W, p_H, color = ORANGE, stroke_width = 8)
        self.add(line_h, vector_b).play(FadeIn(line_h), Write(tex_w), Write(tex_h))
        self.wait(1, 3) #你很容易理解 它本质上就是说
        self.play(alpha.animate.set_value(-1/3))
        group.clear_updaters()
        self.wait(1, 24) #同一个底 高不变 所以面积是不变的
        self.wait(0, 28) #（空闲）

        self.play(IndicateAround(axiom_1))
        self.wait(0, 6) #于是我们就得到了这样一个式子
        self.wait(0, 25) #（空闲）
        text_1 = Heiti(r"平移不变性", color = YELLOW).next_to(axiom_1, DOWN)
        self.play(Write(text_1))
        self.wait(2, 16) #我们把它叫作行列式的平移不变性
        self.wait(1, 13) #（空闲）

        self.fade_out(excepts = [formula], run_time = 0.5)

        offset = 2*DOWN + 0.5*LEFT
        axis_x, axis_y = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        p_E = offset + np.array([3, 0, 0])
        p_F = offset + np.array([3, 1, 0])*9/11
        p_G = offset + np.array([3, 1, 0])*9/11 + np.array([-2, 3, 0])
        p_H = offset + np.array([1, 3, 0])
        p_I = offset + np.array([0, 1, 0])
        parallelogram = Polygon(p_A, p_B, p_C, p_D)
        fill_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
        label_A = MTex(r"(a, b)").next_to(p_A, RIGHT)
        label_B = MTex(r"(c, d)").next_to(p_C, LEFT)
        vector = Arrow(p_D, p_A, color = YELLOW, buff = 0, stroke_width = 8)
        self.fade_in(axis_x, axis_y, parallelogram_0, fill_0, parallelogram, label_A, label_B, vector, excepts = [formula], run_time = 0.5)
        vector_1 = Arrow(p_D, p_E, color = GREEN, buff = 0, stroke_width = 8)
        vector_2 = Arrow(p_E, p_A, color = ORANGE, buff = 0, stroke_width = 8)
        self.play(ReplacementTransform(Line.set_stroke(Arrow(p_D, p_F, color = YELLOW, buff = 0, stroke_width = 6), width = 6), vector_1), ReplacementTransform(Arrow(p_F, p_A, color = YELLOW, buff = 0, stroke_width = 6), vector_2))
        line = Line(p_E, p_G)
        line_2 = Line(p_G, p_H, color = GREY)
        self.add(line, vector, vector_1, vector_2).play(ShowCreation(line))
        parallelogram_1 = Polygon(p_F, p_G, p_C, p_D)
        parallelogram_2 = Polygon(p_A, p_B, p_G, p_F)
        fill_1 = Polygon(p_F, p_G, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        fill_2 = Polygon(p_A, p_B, p_G, p_F, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        self.remove(parallelogram, fill_0).bring_to_back(fill_1, fill_2).add(line_2, parallelogram_1, parallelogram_2, line, vector, vector_1, vector_2).play(
            Transform(parallelogram_1, Polygon(p_E, p_H, p_C, p_D)),
            Transform(parallelogram_2, Polygon(p_A, p_B, p_H, p_E)),
            Transform(fill_1, Polygon(p_E, p_H, p_C, p_D, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0)),
            Transform(fill_2, Polygon(p_A, p_B, p_H, p_E, fill_color = ORANGE, fill_opacity = 0.5, stroke_width = 0)),
            line.animate.put_start_and_end_on(p_E, p_H), ShowCreation(line_2))
        self.wait(3+3-4, 16+9) #另一个性质 是我们把一个平行四边形 表示成了两个小平行四边形的面积和
        self.wait(1, 2) #（空闲）
        color_map = {(r"\vec{u}_1", r"\vec{u}_2", r"\vec{u}_3", r"\vec{u}"): BLUE, r"\vec{v}": GREEN, r"k": YELLOW}
        equation_2 = MTex(r"\det\left(\vec{u}_1+\vec{u}_2, \vec{v}\right)=\det\left(\vec{u}_1, \vec{v}\right) + \det\left(\vec{u}_2, \vec{v}\right)", tex_to_color_map = color_map).shift(2.5*DOWN)
        self.play(Write(equation_2))
        self.wait(0, 17) #用式子表现出来 是这样的
        self.wait(1, 1) #（空闲）

        self.fade_out(excepts = [formula], run_time = 0.5)
        offset_l, offset_r = 1.5*DOWN + 4*LEFT, 1.5*DOWN + 3*RIGHT
        y = np.array([-2, 3, 0])
        axisx_l, axisy_l = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset_l), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset_l)
        axisx_r, axisy_r = Arrow(2.5*LEFT, 3.5*RIGHT, stroke_width = 3).shift(offset_r), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3).shift(offset_r)
        vector_b_l = Arrow(ORIGIN, y, color = GREEN, buff = 0, stroke_width = 8).shift(offset_l)
        vector_b_r = Arrow(ORIGIN, y, color = GREEN, buff = 0, stroke_width = 8).shift(offset_r)
        self.fade_in(axisx_l, axisy_l, axisx_r, axisy_r, vector_b_l, vector_b_r, excepts = [formula], run_time = 0.5)
        self.wait(0, 12) #当然 这个性质还能做一些拓展
        x1 = np.array([3, 1, 0])/3
        vector_a0_l = Arrow(ORIGIN, x1, color = BLUE, buff = 0, stroke_width = 8).shift(offset_l)
        vector_a1_r = Arrow(ORIGIN, x1, color = TEAL, buff = 0, stroke_width = 8).shift(offset_r)
        para_l = Polygon(ORIGIN, y, y, ORIGIN, fill_color = BLUE, fill_opacity = 0.5).shift(offset_l)
        para_r1 = Polygon(ORIGIN, y, y, ORIGIN, fill_color = TEAL, fill_opacity = 0.5).shift(offset_r)
        self.add(para_l, para_r1, vector_a0_l, vector_a1_r, vector_b_l, vector_b_r
                 ).play(GrowArrow(vector_a0_l), GrowArrow(vector_a1_r), 
                        para_l.animate.match_points(Polygon(x1, y+x1, y, ORIGIN).shift(offset_l)), 
                        para_r1.animate.match_points(Polygon(x1, y+x1, y, ORIGIN).shift(offset_r)))
        
        self.wait(0, 15) #比如说...
        line1_r, line2_r = Line(ORIGIN, y).shift(offset_r + x1), Line(ORIGIN, y).shift(offset_r + x1)
        vector_a2_r, vector_a3_r = Arrow(ORIGIN, x1, color = TEAL, buff = 0, stroke_width = 8).shift(offset_r + x1), Arrow(ORIGIN, x1, color = TEAL, buff = 0, stroke_width = 8).shift(offset_r + 2*x1)
        equation_1 = MTex(r"\det\left(k\vec{u}, \vec{v}\right)=k\det\left(\vec{u}, \vec{v}\right)", tex_to_color_map = color_map).shift(2.5*DOWN)
        self.add(line1_r, line2_r, vector_a0_l, vector_a1_r, vector_a2_r, vector_b_l, vector_b_r
                 ).play(Transform(vector_a0_l, Arrow(ORIGIN, 3*x1, color = BLUE, buff = 0, stroke_width = 8).shift(offset_l)), 
                        GrowArrow(vector_a2_r, rate_func = squish_rate_func(rush_into, 0, 0.5)), 
                        GrowArrow(vector_a3_r, rate_func = squish_rate_func(rush_from, 0.5, 1)), 
                        line2_r.animating(rate_func = squish_rate_func(rush_into, 0, 0.5)).shift(x1), 
                        para_l.animate.match_points(Polygon(3*x1, y+3*x1, y, ORIGIN).shift(offset_l)), 
                        para_r1.animate.match_points(Polygon(3*x1, y+3*x1, y, ORIGIN).shift(offset_r)), 
                        Write(equation_1), run_time = 2)
        self.wait(0, 16) #...当我们缩放一个向量的时候
        self.wait(2, 15) #面积也会缩放对应的倍数
        self.wait(0, 21) #（空闲）

        for mob in vector_a1_r, vector_a2_r:
            Line.set_stroke(mob.generate_target(), width = 8)
        self.play(FadeOut(equation_1), MoveToTarget(vector_a1_r), MoveToTarget(vector_a2_r), Uncreate(line1_r), Uncreate(line2_r))
        self.remove(vector_a1_r, vector_a2_r, vector_a3_r)
        x2 = np.array([3, 1, 0])
        x3 = np.array([2, 0, 0])
        vector_a0_r = Arrow(ORIGIN, x2, color = BLUE, buff = 0, stroke_width = 8).shift(offset_r)
        vector_a4_l = Arrow(ORIGIN, x2, color = TEAL, buff = 0, stroke_width = 8).shift(offset_l)
        vector_a4_r = Arrow(ORIGIN, x2, color = TEAL, buff = 0, stroke_width = 8).shift(offset_r)
        vector_a5_l = Arrow(ORIGIN, x2, color = PURPLE_B, buff = 0, stroke_width = 8).shift(offset_l)
        vector_a5_r = Arrow(ORIGIN, x2, color = PURPLE_B, buff = 0, stroke_width = 8).shift(offset_r)
        para_r2 = Polygon(ORIGIN, y, y, ORIGIN, fill_color = PURPLE_B, fill_opacity = 0.5).shift(offset_r + x2)
        group = VGroup(para_l, para_r1, para_r2, vector_a5_l, vector_a4_l, vector_a0_l, vector_a0_r, vector_a5_r, vector_a4_r)
        p, q = Point(x2), Point(x2)
        def group_updater(mob: VGroup):
            xp, xq = p.get_location(), q.get_location()
            mob[0].match_points(Polygon(xq, y+xq, y, ORIGIN).shift(offset_l))
            mob[1].match_points(Polygon(xp, y+xp, y, ORIGIN).shift(offset_r))
            mob[2].match_points(Polygon(xq, y+xq, y+xp, xp).shift(offset_r))
            mob[3].match_points(Arrow(xp, xq, buff = 0, stroke_width = 8).shift(offset_l))
            mob[4].match_points(Arrow(ORIGIN, xp, buff = 0, stroke_width = 8).shift(offset_l))
            mob[5].match_points(Arrow(ORIGIN, xq, buff = 0, stroke_width = 8).shift(offset_l))
            mob[6].match_points(Arrow(ORIGIN, xq, buff = 0, stroke_width = 8).shift(offset_r))
            mob[7].match_points(Arrow(xp, xq, buff = 0, stroke_width = 8).shift(offset_r))
            mob[8].match_points(Arrow(ORIGIN, xp, buff = 0, stroke_width = 8).shift(offset_r))
        group.add_updater(group_updater)
        equation_2 = MTex(r"\det(\vec{u}_1+\vec{u}_2, \vec{v})=\det(\vec{u}_1, \vec{v}) + \det(\vec{u}_2, \vec{v})", tex_to_color_map = color_map).shift(2.5*DOWN)
        equation_2_2 = MTex(r"\det(\vec{u}_1+\vec{u}_2+\vec{u}_3, \vec{v})=\det(\vec{u}_1, \vec{v}) + \det(\vec{u}_2, \vec{v}) + \det(\vec{u}_3, \vec{v})", tex_to_color_map = color_map).shift(2.5*DOWN)
        self.add(group, vector_b_l, vector_b_r).play(p.animating(path_arc = -PI/6).move_to(x3), FadeIn(equation_2, 0.5*UP))
        self.wait(0, 11) #并且 既然两个向量能加
        self.remove(group)
        vector_a6_l = Arrow(ORIGIN, x3, color = LIME, buff = 0, stroke_width = 8).shift(offset_l)
        vector_a6_r = Arrow(ORIGIN, x3, color = LIME, buff = 0, stroke_width = 8).shift(offset_r)
        para_r3 = Polygon(ORIGIN, y, y, ORIGIN, fill_color = LIME, fill_opacity = 0.5).shift(offset_r + x3)
        group = VGroup(para_l, para_r1, para_r2, para_r3, vector_a6_l, vector_a5_l, vector_a4_l, vector_a0_l, vector_a0_r, vector_a6_r, vector_a5_r, vector_a4_r)
        r = Point(x3)
        def group_updater(mob: VGroup):
            xp, xq, xr = p.get_location(), q.get_location(), r.get_location()
            mob[0].match_points(Polygon(xq, y+xq, y, ORIGIN).shift(offset_l))
            mob[1].match_points(Polygon(xp, y+xp, y, ORIGIN).shift(offset_r))
            mob[2].match_points(Polygon(xq, y+xq, y+xr, xr).shift(offset_r))
            mob[3].match_points(Polygon(xr, y+xr, y+xp, xp).shift(offset_r))
            mob[4].match_points(Arrow(xp, xr, buff = 0, stroke_width = 8).shift(offset_l))
            mob[5].match_points(Arrow(xr, xq, buff = 0, stroke_width = 8).shift(offset_l))
            mob[6].match_points(Arrow(ORIGIN, xp, buff = 0, stroke_width = 8).shift(offset_l))
            mob[7].match_points(Arrow(ORIGIN, xq, buff = 0, stroke_width = 8).shift(offset_l))
            mob[8].match_points(Arrow(ORIGIN, xq, buff = 0, stroke_width = 8).shift(offset_r))
            mob[9].match_points(Arrow(xp, xr, buff = 0, stroke_width = 8).shift(offset_r))
            mob[10].match_points(Arrow(xr, xq, buff = 0, stroke_width = 8).shift(offset_r))
            mob[11].match_points(Arrow(ORIGIN, xp, buff = 0, stroke_width = 8).shift(offset_r))
            diff = xq-xr
            if diff[0]*3+diff[1]*2<0:
                mob[2].set_fill(color = ORANGE), mob[5].set_stroke(color = ORANGE), mob[10].set_stroke(color = ORANGE)
            else:
                mob[2].set_fill(color = PURPLE_B), mob[5].set_stroke(color = PURPLE_B), mob[10].set_stroke(color = PURPLE_B)
        x4, x5, x6 = np.array([1.5, 0, 0]), np.array([2.5, 1, 0]), np.array([2.5, 2, 0])
        equation_2.set_submobjects([*equation_2[:11]] + [equation_2_2[i].copy().scale(0, about_point = equation_2[10].get_right()) for i in [11, 12, 13, 14]] + [*equation_2[11:]] + [equation_2_2[i].copy().scale(0, about_point = equation_2[38].get_right()) for i in range(43, 55)])
        self.add(group.add_updater(group_updater), vector_b_l, vector_b_r).play(p.animate.move_to(x4), r.animate.move_to(x5), q.animate.move_to(x6), ReplacementTransform(equation_2, equation_2_2))
        self.wait(0, 3) #那三个向量自然也能加
        self.wait(0, 18) #（空闲）

        x7, x8, x9 = np.array([2, 0, 0]), np.array([2, 2, 0]), np.array([1, 2, 0])
        self.add(group.add_updater(group_updater), vector_b_l, vector_b_r).play(p.animate.move_to(x7), r.animate.move_to(x8), q.animate.move_to(x9), run_time = 2)
        self.wait(1, 21) #无论这些小平行四边形的面积是正是负
        self.wait(2, 4) #我们都一视同仁地把它加起来
        self.wait(2, 0) #正的是正面积 负的是负面积
        self.wait(0, 21) #（空闲）
        self.play(equation_2_2.animating(run_time = 2, rate_func = there_and_back, lag_ratio = 0.1).shift(0.2*UP)) 
        self.wait(1, 11) #但最后加起来 这个等式性质一直是成立的
        self.wait(0, 19) #（空闲）

        x10, x11, x12 = np.array([1, 0, 0]), np.array([2, 0, 0]), np.array([3, 1, 0])
        self.add(group.add_updater(group_updater), vector_b_l, vector_b_r).play(p.animating(run_time = 2).move_to(x10), r.animating(run_time = 2).move_to(x11), q.animating(run_time = 2).move_to(x12), FadeOut(equation_2_2))
        self.wait(1+1-2, 9+13) #这样的性质表明 在v不变的时候
        # text_2 = Heiti(r"线性性", color = YELLOW).next_to(3*UP + 3*RIGHT)
        # self.play(Write(text_2))
        self.wait(2, 8) #行列式对u
        self.wait(0, 24) #是线性的
        self.wait(0, 17) #（空闲）

        group.clear_updaters().generate_target()
        equation_3 = MTex(r"\det\left(\vec{u}_1+k\vec{u}_2, \vec{v}\right)=\det\left(\vec{u}_1, \vec{v}\right)+k\det\left(\vec{u}_2, \vec{v}\right)", tex_to_color_map = color_map).shift(2.5*DOWN)
        group.target[3].set_fill(color = TEAL), group.target[4].set_stroke(color = TEAL), group.target[9].set_stroke(color = TEAL)
        self.play(Write(equation_3), MoveToTarget(group))
        self.wait(1+0-2, 13+29) #写得紧凑一些的话 大概是这个样子
        self.wait(1, 10) #（空闲）
        
        self.fade_out(run_time = 0.5)
        graph_1, graph_2 = ImageMobject(r"Patch7_2.png", height = 3.5).shift(1.5*UP + 3*LEFT), ImageMobject(r"Patch7_1.png", height = 3.5).shift(1.5*UP + 3*RIGHT)
        surr_1, surr_2 = SurroundingRectangle(graph_1, color = GREEN), SurroundingRectangle(graph_2, color = YELLOW)
        axiom_1 = MTex(r"\det\left(\vec{u}_1+k\vec{u}_2, \vec{v}\right)=\det\left(\vec{u}_1, \vec{v}\right)+k\det\left(\vec{u}_2, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8).next_to(1.5*DOWN + 5*LEFT)
        axiom_2 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=\det\left(\vec{u}+k\vec{v}, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8).next_to(2.5*DOWN + 5*LEFT)
        lamp_1, lamp_2 = [Circle(radius = 0.2, stroke_color = WHITE, fill_color = color, fill_opacity = 1).next_to(mob, LEFT) for color, mob in zip([GREEN, YELLOW], [axiom_1, axiom_2])]
        text_1, text_2 = Songti(r"线性性", color = YELLOW).scale(0.8).next_to(1.5*DOWN + 3*RIGHT), Songti(r"平移不变性", color = YELLOW).scale(0.8).next_to(2.5*DOWN + 3*RIGHT)
        self.fade_in(graph_1, graph_2, surr_1, surr_2, axiom_1, axiom_2, lamp_1, lamp_2, text_1, text_2, run_time = 0.5)
        self.wait(1, 25) #于是 我们从面积的两条性质出发
        self.wait(5, 15) #总结出了行列式的两条性质
        self.wait(0, 26) #（空闲）

        self.wait(1, 1) #需要注意的是
        excepts = [surr_1, surr_2, lamp_1, lamp_2, text_1, text_2]
        self.fade_out(excepts = excepts, run_time = 0.5)
        graph_4, graph_5 = ImageMobject(r"Patch7_5.png", height = 3.5).shift(1.5*UP + 3*LEFT), ImageMobject(r"Patch7_4.png", height = 3.5).shift(1.5*UP + 3*RIGHT)
        axiom_4 = MTex(r"\det\left(\vec{u}, \vec{v}_1+k\vec{v}_2\right)=\det\left(\vec{u}, \vec{v}_1\right)+k\det\left(\vec{u}, \vec{v}_2\right)", tex_to_color_map = color_map).scale(0.8).next_to(1.5*DOWN + 5*LEFT)
        axiom_5 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=\det\left(\vec{u}, \vec{v}+k\vec{u}\right)", tex_to_color_map = color_map).scale(0.8).next_to(2.5*DOWN + 5*LEFT)
        self.fade_in(graph_4, graph_5, axiom_4, axiom_5, excepts = excepts, run_time = 0.5)
        self.wait(0, 28) #我们虽然只对u演示了这些性质
        self.wait(2, 5) #但它们对v也是成立的
        self.fade_out(excepts = excepts, run_time = 0.5)
        self.fade_in(graph_1, graph_2, axiom_1, axiom_2, excepts = excepts, run_time = 0.5)
        self.wait(1, 8) #为了简便起见 屏幕上就只写一个了
        self.wait(1, 2) #（空闲）

        self.wait(2, 19) #不过到此为止还有一点小问题
        self.wait(2, 6) #因为我们还没有定义单位面积
        self.fade_out(run_time = 0.5)
        offset = DOWN + 4*LEFT
        axis_x, axis_y = Arrow(1.5*LEFT, 3.5*RIGHT, stroke_width = 4).shift(offset), Arrow(1*DOWN, 3.5*UP, stroke_width = 4).shift(offset)
        p_A = offset + np.array([2, 0, 0])
        p_B = offset + np.array([2, 2, 0])
        p_C = offset + np.array([0, 2, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.6, stroke_width = 6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 10)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 10)
        list_3 = [axis_x, axis_y, parallelogram, vector_a, vector_b]
        self.fade_in(*list_3, run_time = 0.5)
        self.wait(1, 3) #我们定义单位面积的方式是
        self.wait(4, 18) #如果u和v分别是单位向量
        axiom_3 = MTex(r"\begin{vmatrix}1&0\\0&1\end{vmatrix}=1").shift(3*RIGHT + UP)
        axiom_3[4].set_color(BLUE), axiom_3[5].set_color(GREEN), axiom_3[6].set_color(BLUE), axiom_3[7].set_color(GREEN), axiom_3[-1].set_color(YELLOW)
        self.play(Write(axiom_3))
        self.wait(2, 29) #那么这个平行四边形就变成了一个单位正方形
        self.wait(2, 4) #我们定义它的行列式是1
        self.wait(1, 5) #（空闲）
        
        self.fade_out(run_time = 0.5)
        color_map = {(r"\vec{u}", r"\vec{u}_1", r"\vec{u}_2"): BLUE, (r"\vec{v}", r"\vec{v}_1", r"\vec{v}_2"): GREEN, r"k": YELLOW, (r"\vec{0}", r"0"): GREY}
        title = Title(r"唯一确定行列式的三条公理")
        titleline = TitleLine()
        graph_1, graph_2, graph_3 = ImageMobject(r"Patch7_2.png", height = 3.5).shift(UP + 4.5*LEFT), ImageMobject(r"Patch7_1.png", height = 3.5).shift(UP), ImageMobject(r"Patch7_3.png", height = 3.5).shift(UP + 4.5*RIGHT)
        surr_1, surr_2, surr_3 = SurroundingRectangle(graph_1, color = GREEN), SurroundingRectangle(graph_2, color = YELLOW), SurroundingRectangle(graph_3, color = RED)
        axiom_1 = MTex(r"\det\left(\vec{u}_1+k\vec{u}_2, \vec{v}\right)=\det\left(\vec{u}_1, \vec{v}\right)+k\det\left(\vec{u}_2, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8).next_to(1.5*DOWN + 6*LEFT)
        axiom_2 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=\det\left(\vec{u}+k\vec{v}, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8).next_to(2.5*DOWN + 6*LEFT)
        axiom_3 = MTex(r"\begin{vmatrix}1&0\\0&1\end{vmatrix}=1").scale(0.8).next_to(2*DOWN + 3*RIGHT)
        axiom_3[4].set_color(BLUE), axiom_3[5].set_color(GREEN), axiom_3[6].set_color(BLUE), axiom_3[7].set_color(GREEN), axiom_3[-1].set_color(YELLOW)
        lamp_1, lamp_2, lamp_3 = [Circle(radius = 0.2, stroke_color = WHITE, fill_color = color, fill_opacity = 1).next_to(mob, LEFT) for color, mob in zip([GREEN, YELLOW, RED], [axiom_1, axiom_2, axiom_3])]
        self.fade_in(graph_1, graph_2, graph_3, surr_1, surr_2, surr_3, axiom_1, axiom_2, axiom_3, lamp_1, lamp_2, lamp_3, run_time = 0.5)
        self.wait(1, 13) #有这三条性质就完全够用了
        self.wait(4, 0) #实际上 它们唯一确定了行列式的表达式
        self.wait(2, 21) #就是我们所熟知的ad-bc
        self.play(FadeIn(title, DOWN), GrowFromPoint(titleline, 4*UP))
        self.wait(6, 4) #所以 以上这三条面积需要被满足的性质 就被称为行列式的三条公理
        self.wait(1, 17) #（空闲）
        self.wait(3, 12) #这三条公理看起来离我们的目标很远很远
        self.wait(4, 1) #至少它们完全没有告诉我们面积什么时候应该是负的
        self.wait(4, 24) #你也很难从中一眼看出来 为什么它的展开式是我们学到的那个样子
        self.wait(0, 22) #（空闲）

        self.play(*[FadeOut(mob, 4.5*UP) for mob in [title, titleline, graph_1, graph_2, graph_3, surr_1, surr_2, surr_3]], *[mob.animate.shift(4.5*UP) for mob in [axiom_1, axiom_2, axiom_3]], *[mob.animate.shift(4.5*UP).set_fill(opacity = 0) for mob in [lamp_1, lamp_2, lamp_3]], run_time = 2)
        self.wait(1+2-2, 14+17) #不过不用担心 这是三条非常强大的公理
        self.wait(3, 2) #我们能从中推出一切

class Video_8(FrameScene):
    def construct(self):
        self.frames += 181*30+5
        color_map = {(r"\vec{u}", r"\vec{u}_1", r"\vec{u}_2"): BLUE, (r"\vec{v}", r"\vec{v}_1", r"\vec{v}_2"): GREEN, r"k": YELLOW, (r"\vec{0}", r"0"): GREY}
        axiom_1 = MTex(r"\det\left(\vec{u}_1+k\vec{u}_2, \vec{v}\right)=\det\left(\vec{u}_1, \vec{v}\right)+k\det\left(\vec{u}_2, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8).next_to(3*UP + 6*LEFT)
        axiom_2 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=\det\left(\vec{u}+k\vec{v}, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8).next_to(2*UP + 6*LEFT)
        axiom_3 = MTex(r"\begin{vmatrix}1&0\\0&1\end{vmatrix}=1").scale(0.8).next_to(2.5*UP + 3*RIGHT)
        axiom_3[4].set_color(BLUE), axiom_3[5].set_color(GREEN), axiom_3[6].set_color(BLUE), axiom_3[7].set_color(GREEN), axiom_3[-1].set_color(YELLOW)
        lamp_1, lamp_2, lamp_3 = [Circle(radius = 0.2, stroke_color = WHITE, fill_color = color).next_to(mob, LEFT) for color, mob in zip([GREEN, YELLOW, RED], [axiom_1, axiom_2, axiom_3])]
        self.add(axiom_1, axiom_2, axiom_3, lamp_1, lamp_2, lamp_3)

        # equation_1 = MTex(r"\det\left(\vec{0}, \vec{v}\right)=0", tex_to_color_map = color_map).scale(0.8)
        # calculate_1 = MTex(r"\det\left(\vec{0}, \vec{v}\right)=\det\left(\vec{0}+1\times\vec{0}, \vec{v}\right)=\det\left(\vec{0}, \vec{v}\right)+1\times\det\left(\vec{0}, \vec{v}\right)", color = GREY).scale(0.6).next_to(equation_1, DOWN)
        # line_1, line_2 = Line(calculate_1[:10].get_corner(UL), calculate_1[:10].get_corner(DR), color = RED), Line(calculate_1[-23:-13].get_corner(UL), calculate_1[-23:-13].get_corner(DR), color = RED)
        # self.play(Write(equation_1), lamp_1.animate.set_fill(opacity = 1))
        # self.wait()
        # self.play(ShowIncreasingSubsets(calculate_1), run_time = 2)
        # self.play(ShowCreation(line_1), ShowCreation(line_2))
        # self.remove(line_1, line_2), calculate_1.add(line_1, line_2)
        # self.wait()
        # self.play(FadeIn(BackgroundRectangle(calculate_1), remover = True))
        # self.remove(calculate_1).wait()
        # self.play(FadeOut(equation_1), lamp_1.animate.set_fill(opacity = 0))
        # self.wait()

        equation_2 = MTex(r"\det\left(\vec{u}, \vec{u}\right)=0", tex_to_color_map = color_map).scale(0.8)
        texts = r"\det\left(\vec{u}, \vec{u}\right)", r"=\det\left(\vec{u}, \vec{u}+(-1)\vec{u}\right)", r"=\det\left(\vec{u}, 0\right)", r"=0"
        calculate_2 = MTex(r"".join(texts), isolate = texts, tex_to_color_map = {r"(-1)": YELLOW, **color_map}).scale(0.8).next_to(equation_2, DOWN)
        parts = [calculate_2.get_part_by_tex(text) for text in texts]
        self.play(Write(equation_2), lamp_1.animate.set_fill(opacity = 1), lamp_2.animate.set_fill(opacity = 1))
        self.wait(1, 5) #比如说 用前两条公理
        self.wait(1, 2) #我们就可以知道
        self.wait(2, 12) #两个相等的向量的行列式是0
        self.play(TransformFromCopy(equation_2[:-2], parts[0], path_arc = PI/4))
        self.wait(0, 4) #证明很简单
        self.play(FadeIn(parts[1], 0.5*LEFT), lamp_1.animate.set_fill(opacity = 0))
        self.wait(0, 21) #只需要先用平移不变性
        self.play(FadeIn(parts[2], 0.5*LEFT))
        self.wait(0, 16) #把两个向量相减
        self.play(FadeIn(parts[3], 0.5*LEFT), lamp_2.animate.set_fill(opacity = 0), lamp_1.animate.set_fill(opacity = 1))
        self.wait(1, 9) #再用线性性 就可以算出答案
        self.wait(0, 19) #（空闲）

        offset = 1.5*DOWN + 3*RIGHT
        axis_x, axis_y = Arrow(0.5*LEFT, 2.5*RIGHT, stroke_width = 3).shift(offset), Arrow(0.5*DOWN, 2.5*UP, stroke_width = 3).shift(offset)
        p_A = offset + np.array([2, 0, 0])
        p_B = offset + np.array([2, 2, 0])
        p_C = offset + np.array([0, 2, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        group = VGroup(axis_x, axis_y, parallelogram, vector_a, vector_b)
        shade = BackgroundRectangle(group)
        self.add(group, shade, calculate_2).play(FadeOut(shade, run_time = 0.5, delay = 0.5), FadeOut(calculate_2, run_time = 0.5), lamp_2.animate.set_fill(opacity = 1))
        self.wait(0, 25) #这从图上也很好理解
        alpha = ValueTracker(0.0)
        def close_updater(mob: VGroup):
            angle = alpha.get_value()
            x, y = 2*unit(angle), 2*unit(PI/2-angle)
            A, B, C, D = offset + x, offset + x + y, offset + y, offset
            mob[2].match_points(Polygon(A, B, C, D))
            mob[3].match_points(Arrow(D, A, buff = 0, stroke_width = 8))
            mob[4].match_points(Arrow(D, C, buff = 0, stroke_width = 8)).set_color(interpolate_color(GREEN, BLUE, angle/PI*4))
            if angle == PI/4:
                mob[2].set_points_as_corners([p_D, p_D + 4*unit(PI/4)])
        group.add_updater(close_updater)
        self.play(alpha.animate.set_value(PI/4))
        group.clear_updaters()
        group[2].set_points_as_corners([p_D, p_D + 4*unit(PI/4)])
        self.wait(1, 23) #当两个向量重合的时候
        self.wait(2, 27) #它们张成的平行四边形就只剩下一条线了
        self.wait(1, 13) #而直线是没有面积的
        self.wait(1, 12) #（空闲）

        shade = BackgroundRectangle(group)
        self.add(group, shade).play(FadeIn(shade), FadeOut(equation_2), lamp_1.animate.set_fill(opacity = 0), lamp_2.animate.set_fill(opacity = 0))
        self.remove(shade, group).wait(0, 22) #接下来是重头戏

        # equation_3 = MTex(r"\det\left(\vec{u}, k\vec{v}\right)=k\det\left(\vec{u}, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8)
        # calculate_3 = MTex(r"\det\left(\vec{u}, k\vec{v}\right)=\det\left(\vec{u}, \vec{0}+k\vec{v}\right)=\det\left(\vec{u}, \vec{0}\right)+k\det\left(\vec{u}, \vec{v}\right)=k\det\left(\vec{u}, \vec{v}\right)", tex_to_color_map = color_map).scale(0.6).next_to(equation_3, DOWN)
        # self.play(Write(equation_3), lamp_1.animate.set_fill(opacity = 1))
        # self.wait()
        # self.play(ShowIncreasingSubsets(calculate_3), run_time = 2)
        # self.wait()
        # self.play(FadeOut(calculate_3))
        # self.wait()
        # self.play(FadeOut(equation_3), lamp_1.animate.set_fill(opacity = 0))
        # self.wait()

        # equation_4 = MTex(r"\begin{vmatrix}a&0\\0&b\end{vmatrix}=ab").scale(0.8)
        # equation_4[4].set_color(BLUE), equation_4[5].set_color(GREEN), equation_4[6].set_color(BLUE), equation_4[7].set_color(GREEN), equation_4[-2].set_color(BLUE), equation_4[-1].set_color(GREEN)
        # texts = r"\begin{vmatrix}a&0\\0&b\end{vmatrix}", r"=a\begin{vmatrix}1&0\\0&b\end{vmatrix}", r"=ab\begin{vmatrix}1&0\\0&1\end{vmatrix}", r"{=ab}"
        # calculate_4 = MTex(r"".join(texts), isolate = texts, tex_to_color_map = {r"(-1)": YELLOW, **color_map}).scale(0.8).next_to(equation_4, DOWN)
        # parts = [calculate_4.get_part_by_tex(text) for text in texts]
        # for i in [4, 6, 13, 18, 20, 27, 33, 35, 42]:
        #     calculate_4[i].set_color(BLUE)
        # for i in [5, 7, 19, 21, 28, 34, 36, 43]:
        #     calculate_4[i].set_color(GREEN)
        # self.play(Write(equation_4), lamp_1.animate.set_fill(opacity = 1))
        # self.wait()
        # self.play(TransformFromCopy(equation_4[:-3], parts[0], path_arc = PI/4))
        # self.wait()
        # self.play(FadeIn(parts[1], 0.5*LEFT))
        # self.wait()
        # self.play(FadeIn(parts[2], 0.5*LEFT))
        # self.wait()
        # self.play(FadeIn(parts[3], 0.5*LEFT), lamp_1.animate.set_fill(opacity = 0), lamp_3.animate.set_fill(opacity = 1))
        # self.wait()
        # self.play(FadeOut(calculate_4), lamp_3.animate.set_fill(opacity = 0), lamp_1.animate.set_fill(opacity = 1))
        # self.wait()
        # self.play(FadeOut(equation_4), lamp_1.animate.set_fill(opacity = 0))
        # self.wait()

        equation_5 = MTex(r"\det\left(\vec{u}, \vec{v}\right)=-\det\left(\vec{v}, \vec{u}\right)", tex_to_color_map = color_map).scale(0.8)
        texts = r"0=\det\left(\vec{u}+\vec{v}, \vec{u}+\vec{v}\right)", r"=\det\left(\vec{u}+\vec{v}, \vec{u}\right)+\det\left(\vec{u}+\vec{v}, \vec{v}\right)", r"=\det\left(\vec{v}, \vec{u}\right)+\det\left(\vec{u}, \vec{v}\right)"
        calculate_5 = MTex(r"".join(texts), isolate = texts, tex_to_color_map = color_map).scale(0.8).next_to(equation_5, DOWN)
        parts = [calculate_5.get_part_by_tex(text) for text in texts]
        self.play(Write(equation_5), lamp_1.animate.set_fill(opacity = 1), lamp_2.animate.set_fill(opacity = 1))
        self.wait(0, 25) #行列式最重要的一条性质就是
        self.wait(2, 11) #当我们交换u和v的时候
        self.wait(2, 11) #它的符号会取负值
        self.wait(0, 28) #（空闲）
        self.wait(1, 17) #这看起来很不可思议
        self.wait(1, 27) #但是证明却很简单
        self.play(Write(parts[0]), lamp_1.animate.set_fill(opacity = 0))
        #self.wait() #我们从这个式子出发
        self.wait(2, 21) #两个输入相等说明它的值是0
        self.play(FadeIn(parts[1], 0.5*LEFT), lamp_1.animate.set_fill(opacity = 1), lamp_2.animate.set_fill(opacity = 0))
        self.wait(3, 12) #我们首先用线性性把它分解成两个行列式的和
        self.play(FadeIn(parts[2], 0.5*LEFT), lamp_1.animate.set_fill(opacity = 0), lamp_2.animate.set_fill(opacity = 1))
        self.wait(0, 23) #再用平移不变性
        self.wait(1, 15) #整理成我们需要的形式
        self.wait(0, 17) #（空闲）
        self.play(calculate_5.animate.shift(UP), lamp_1.animate.set_fill(opacity = 1), lamp_2.animate.set_fill(opacity = 1), equation_5.animate.shift(UP))
        self.wait(2, 10) #诶你就发现 调换之后它们相加起来等于0
        self.wait(0, 20) #（空闲）

        axis_x, axis_y = Arrow(0.5*LEFT, 2*RIGHT, stroke_width = 3), Arrow(0.5*DOWN, 2*UP, stroke_width = 3)
        p_A = np.array([1, 0, 0])
        p_B = np.array([1, 1, 0])
        p_C = np.array([0, 1, 0])
        p_D = ORIGIN
        parallelogram = Line(p_D, 2*p_B)
        vector_a = Arrow(p_D, p_B, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_B, color = GREEN, buff = 0, stroke_width = 8)
        group_1 = VGroup(axis_x.copy(), axis_y.copy(), parallelogram, vector_a, vector_b).shift(2.5*DOWN + 6*LEFT)
        parallelogram_1 = Polygon(p_A, p_B+p_A, p_B, p_D, fill_color = TEAL, fill_opacity = 0.6)
        parallelogram_2 = Polygon(p_A, p_B+p_A, 2*p_B, p_B, fill_color = PURPLE_B, fill_opacity = 0.6)
        vector_a = Arrow(p_D, p_B, color = BLUE, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_B, color = GREEN, buff = 0, stroke_width = 8)
        vector_1 = Arrow(p_D, p_A, color = TEAL, buff = 0, stroke_width = 8)
        vector_2 = Arrow(p_A, p_B, color = PURPLE_B, buff = 0, stroke_width = 8)
        group_2 = VGroup(axis_x.copy(), axis_y.copy(), parallelogram_1, parallelogram_2, vector_a, vector_b, vector_1, vector_2).shift(2.5*DOWN + 3.5*LEFT)
        axis_x, axis_y = Arrow(0.5*LEFT, 1.5*RIGHT, stroke_width = 3), Arrow(0.5*DOWN, 1.5*UP, stroke_width = 3)
        parallelogram = Polygon(p_A, p_B+p_A, p_B, p_D, fill_color = TEAL, fill_opacity = 0.6)
        vector_a = Arrow(p_D, p_A, color = TEAL, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_B, color = GREEN, buff = 0, stroke_width = 8)
        group_3_1 = VGroup(axis_x.copy(), axis_y.copy(), parallelogram, vector_a, vector_b).shift(1.5*DOWN + 0.5*LEFT)
        parallelogram = Polygon(p_B, p_B+p_C, p_C, p_D, fill_color = PURPLE_B, fill_opacity = 0.6)
        vector_a = Arrow(p_D, p_C, color = PURPLE_B, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_B, color = GREEN, buff = 0, stroke_width = 8)
        group_3_2 = VGroup(axis_x.copy(), axis_y.copy(), parallelogram, vector_a, vector_b).shift(2.5*DOWN + 1*RIGHT)
        group_3 = VGroup(*group_3_1, *group_3_2)
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = TEAL, fill_opacity = 0.6)
        vector_a = Arrow(p_D, p_A, color = TEAL, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 8)
        group_4_1 = VGroup(axis_x.copy(), axis_y.copy(), parallelogram, vector_a, vector_b).shift(1.5*DOWN + 3.5*RIGHT)
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = PURPLE_B, fill_opacity = 0.6)
        vector_a = Arrow(p_D, p_C, color = PURPLE_B, buff = 0, stroke_width = 8)
        vector_b = Arrow(p_D, p_A, color = GREEN, buff = 0, stroke_width = 8)
        group_4_2 = VGroup(axis_x.copy(), axis_y.copy(), parallelogram, vector_a, vector_b).shift(2.5*DOWN + 5*RIGHT)
        group_4 = VGroup(*group_4_1, *group_4_2)
        self.play(group_4.shift(0.5*RIGHT).animating(delay = 1.5).shift(0.5*LEFT), follow(BackgroundRectangle(group_4, buff = 0.1), group_4, FadeOut, delay = 1.5),
                  group_3.shift(0.5*RIGHT).animating(delay = 1.0).shift(0.5*LEFT), follow(BackgroundRectangle(group_3, buff = 0.1), group_3, FadeOut, delay = 1.0),
                  group_2.shift(0.5*RIGHT).animating(delay = 0.5).shift(0.5*LEFT), follow(BackgroundRectangle(group_2, buff = 0.1), group_2, FadeOut, delay = 0.5),
                  group_1.shift(0.5*RIGHT).animate.shift(0.5*LEFT), follow(BackgroundRectangle(group_1, buff = 0.1), group_1, FadeOut))
        self.wait(0, 17) #如果从图上来理解的话 大概是这样一个过程
        self.wait(1, 7) #（空闲）

        lamp_4 = Circle(radius = 0.2, stroke_color = GREY, fill_color = BLUE).next_to(UP + 5*LEFT, LEFT, buff = 0)
        self.play(equation_5.animate.next_to(UP + 5*LEFT), follow(lamp_4, equation_5, FadeIn))
        self.wait(2, 7) #这个性质被称为反对称性
        self.wait(2, 21) #它非常重要 等会会多次用到它
        self.wait(1, 22) #你也可以从中看出来
        self.wait(2, 1) #负面积会很自然地出现
        self.wait(3, 27) #只需要调换这两个坐标写入函数的顺序
        self.wait(2, 0) #它的面积就会取成相反数了
        self.wait(0, 26) #（空闲）

        self.play(FadeIn(BackgroundRectangle(VGroup(group_1, group_2, group_3, group_4, calculate_5)), remover = True), lamp_1.animate.set_fill(opacity = 0), lamp_2.animate.set_fill(opacity = 0))
        self.remove(group_1, group_2, group_3, group_4, calculate_5).wait(0, 6) #好了
        equation_6 = MTex(r"\begin{vmatrix}{a}&{c}\\{b}&{d}\end{vmatrix}={a}{d}-{b}{c}", tex_to_color_map = {(r"{a}", r"{b}"): GREEN, (r"{c}", r"{d}"): BLUE}).scale(0.8)
        texts = r"\begin{vmatrix}{a}&{c}\\{b}&{d}\end{vmatrix}", r"=\begin{vmatrix}{a}&{c}\\0&{d}\end{vmatrix}+\begin{vmatrix}0&{c}\\{b}&{d}\end{vmatrix}", r"=\begin{vmatrix}{a}&0\\0&{d}\end{vmatrix}+\begin{vmatrix}0&{c}\\{b}&0\end{vmatrix}", r"=\begin{vmatrix}{a}&0\\0&{d}\end{vmatrix}-\begin{vmatrix}{c}&0\\0&{b}\end{vmatrix}", r"={a}{d}-{b}{c}"
        calculate_6 = MTex(r"".join(texts), isolate = texts, tex_to_color_map = {(r"{a}", r"{b}"): GREEN, (r"{c}", r"{d}"): BLUE, r"0": GREY}).scale(0.8).next_to(equation_6, DOWN)
        parts = [calculate_6.get_part_by_tex(text) for text in texts]
        lamp_5 = Circle(radius = 0.2, stroke_color = GREY, fill_color = PURPLE_B).next_to(1.5*UP + 3*RIGHT, LEFT, buff = 0)
        self.play(Write(equation_6))
        self.wait(0, 14) #现在 我们已经有足够的能力
        self.wait(2, 23) #来推导二阶行列式的展开式了
        self.wait(1, 18) #看好了哈 不要眨眼
        self.wait(3, 1) #接下来我们将忘掉所有的几何意义
        self.wait(4, 7) #纯粹从这几条公理去推出二维的面积公式
        self.wait(1, 1) #（空闲）
        self.play(lamp_1.animate.set_fill(opacity = 1), lamp_2.animate.set_fill(opacity = 1), lamp_3.animate.set_fill(opacity = 1), lamp_4.animate.set_fill(opacity = 1))
        self.wait(2, 2) #推导过程需要把这四条都用一遍
        self.play(TransformFromCopy(equation_6[:-6], parts[0], path_arc = PI/4), lamp_2.animate.set_fill(opacity = 0), lamp_3.animate.set_fill(opacity = 0), lamp_4.animate.set_fill(opacity = 0))
        self.wait(0, 14) #首先我们用线性性
        self.play(FadeIn(parts[1], 0.5*LEFT))
        self.wait(1, 10) #把第一列按坐标展开
        self.play(IndicateAround(VGroup(parts[1][5], parts[1][7])), IndicateAround(VGroup(parts[1][18], parts[1][20])))
        self.wait(0, 28) #就是把第一列的向量拆成(a,0)和(0,b)
        self.wait(0, 25) #（空闲）
        self.play(FadeIn(parts[2], 0.5*LEFT), lamp_1.animate.set_fill(opacity = 0), lamp_2.animate.set_fill(opacity = 1))
        self.wait(1, 15) #然后使用平移不变性
        self.play(IndicateAround(VGroup(parts[2][5], parts[2][6])), IndicateAround(VGroup(parts[2][20], parts[2][21])))
        self.wait(0, 13) #消掉对应行上的元素
        self.wait(0, 25) #（空闲）
        self.play(FadeIn(parts[3], 0.5*LEFT), lamp_2.animate.set_fill(opacity = 0), lamp_4.animate.set_fill(opacity = 1))
        self.wait(1, 5) #接着利用反对称性
        self.play(*[IndicateAround(parts[3][i]) for i in [5, 8, 18, 21]])
        self.wait(1, 17) #把非零元素都移动到主对角线上来
        self.wait(0, 22) #（空闲）
        self.play(FadeIn(parts[4], 0.5*LEFT), lamp_4.animate.set_fill(opacity = 0), lamp_1.animate.set_fill(opacity = 1), lamp_3.animate.set_fill(opacity = 1))
        self.wait(1, 9) #最后 再用线性性
        self.wait(3, 11) #可以化成某一个系数乘以两个单位的面积
        self.wait(0, 17) #（空闲）
        self.play(lamp_3.animate.set_fill(opacity = 0), lamp_1.animate.set_fill(opacity = 0))
        self.wait(1, 7) #最终 我们就得到了展开式
        self.wait(1, 11) #ad-bc
        self.wait(0, 28) #（空闲）
        self.print_mark()
        self.play(FadeOut(calculate_6), equation_6.animating(path_arc = PI/4).next_to(1.5*UP + 3*RIGHT), follow(lamp_5, equation_6, FadeIn, path_arc = PI/4), lamp_3.animate.shift(0.5*UP), axiom_3.animate.shift(0.5*UP))
        self.wait(2, 8) #得到这个展开式 我们还可以来玩一玩它

        texts = r"\begin{vmatrix}{a}+k{c}&{c}\\{b}+k{d}&{d}\end{vmatrix}", r"=({a}+k{c}){d}-({b}+k{d}){c}", r"={a}{d}+k{c}{d}-{b}{c}-k{c}{d}", r"={a}{d}-{b}{c}"
        check_1 = MTex(r"&" + texts[0] + texts[1] + r"\\&" + texts[2] + r"\\&" + texts[3], isolate =  [r"k{c}{d}", *texts], tex_to_color_map = {(r"{a}", r"{b}"): GREEN, (r"{c}", r"{d}"): BLUE, r"k": YELLOW}).scale(0.8).shift(DOWN)
        parts = [check_1.get_part_by_tex(text) for text in texts]
        parts[2].shift((parts[1][0].get_x() - parts[2][0].get_x())*RIGHT)
        parts[3].shift((parts[1][0].get_x() - parts[3][0].get_x())*RIGHT)
        cancels = check_1.get_parts_by_tex(r"k{c}{d}")
        line_1, line_2 = Line(cancels[0].get_corner(UL), cancels[0].get_corner(DR), color = RED), Line(cancels[1].get_corner(UL), cancels[1].get_corner(DR), color = RED)
        checkmark = MTex(r"\checkmark", color = YELLOW).scale(1.2).next_to(lamp_2.get_corner(DOWN), UP, buff = 0.1).shift(0.1*RIGHT)
        self.play(lamp_5.animate.set_fill(opacity = 1), lamp_2.animate.set_stroke(color = YELLOW))
        self.wait(3, 12) #比如说反过来验证一下平移不变性
        self.play(Write(parts[0]))
        self.wait(1, 22) #我们用坐标写出平移不变性的左端
        self.play(FadeIn(parts[1], 0.5*LEFT))
        self.wait(0, 22) #然后将它展开
        self.play(FadeIn(parts[2], 0.5*UP))
        self.wait(1, 29) #整理一下 诶 神奇的事情发生了
        self.play(ShowCreation(line_1), ShowCreation(line_2))
        self.wait(1, 5) #多出来的项被消掉了
        self.play(FadeIn(parts[3], 0.5*UP))
        self.wait(2, 19) #剩下的 就正好是原来的行列式
        self.play(ShowCreation(checkmark))
        self.wait(0, 8) #所以我们就验证了
        self.wait(3, 6) #这个表达式的确满足平移不变性
        self.wait(1, 20) #（空闲）
         
#################################################################### 
               
class Patch9_1(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/8), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*OUT + -0.2*unit(-PI/8))

        x, y, z = np.array([1, -2, 1]), np.array([1, 2, 1]), np.array([0, 1, 2])
        vector_a, vector_b, vector_c = Arrow(ORIGIN, x, buff = 0, color = BLUE, stroke_width = 8), Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True, stroke_width = 8)
        volume_1, volume_2, volume_3 = Parallelepiped(x=x*RIGHT, y=y, z=z, opacity = 0.3, color = RED, depth_test = True), Parallelepiped(x=x*UP, y=y, z=z, opacity = 0.3, color = ORANGE, depth_test = True).shift(x*RIGHT), Parallelepiped(x=OUT, y=y, z=z, opacity = 0.3, color = YELLOW, depth_test = True).shift(x*UR)
        vector_1, vector_2, vector_3 = Arrow(ORIGIN, x*RIGHT, buff = 0, color = RED, stroke_width = 8), Arrow(x*RIGHT, x*UR, buff = 0, color = ORANGE, stroke_width = 8), Arrow(x*UR, x, buff = 0, color = YELLOW, stroke_width = 8)
        old = [volume_1[5], volume_2[5], volume_3[5], volume_1[0], volume_2[0], volume_3[0], volume_1[1], volume_1[2], volume_2[2], volume_3[2], volume_1[3], volume_2[3], volume_3[3], volume_3[4]]
        extra = [volume_1[4], volume_2[1], volume_2[4], volume_3[1]]
        self.add(axes, vector_a, vector_b, vector_c, vector_1, vector_2, vector_3, *extra, *old)
        self.wait()

class Patch9_2(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*OUT)

        x, y, z = np.array([1, -2, 1]), np.array([1, 2, 1]), np.array([0, 1, 2])
        vector_a, vector_b, vector_c = Arrow(ORIGIN, x, buff = 0, color = BLUE, stroke_width = 8), Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True, stroke_width = 8), depth_test = True)
        volume_1 = Parallelepiped(x=x, y=y, z=z, opacity = 0.5, color = PURPLE)
        volume_1[0].set_color(YELLOW), volume_1[3].set_color(YELLOW)
        diff = x/2
        vector_d, vector_s = Arrow(z, z+diff, buff = 0, color = BLUE_E, stroke_width = 8), Arrow(ORIGIN, z+diff, buff = 0, color = interpolate_color(PURPLE_B, BLUE, 0.5), stroke_width = 8)
        volume_2 = Parallelepiped(x=x, y=y, z=z+diff, opacity = 0.5, color = TEAL)
        volume_2[0].set_color(YELLOW), volume_2[3].set_color(YELLOW)
        surfaces = [volume_1[3], volume_2[3], volume_1[5], volume_2[5], volume_1[1], volume_2[1], volume_1[4], volume_2[4], volume_1[0], volume_2[0], volume_1[1], volume_1[2], volume_1[2], volume_2[2]]
        self.add(axes, *surfaces, vector_a, vector_b, vector_c, vector_d, vector_s)

class Patch9_3(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/4), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*OUT)

        x, y, z = np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])
        vector_a, vector_b, vector_c = Arrow(ORIGIN, x, buff = 0, color = BLUE, stroke_width = 8), Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True, stroke_width = 8), depth_test = True)
        volume_1 = Parallelepiped(x=x, y=y, z=z, opacity = 0.5, color = BLUE)
        self.add(axes, volume_1, vector_a, vector_b, vector_c)

class Video_9(FrameScene):
    def construct(self):
        color_map = {(r"\vec{u}", r"\vec{u}_1", r"\vec{u}_2"): BLUE, (r"\vec{v}", r"\vec{v}_1", r"\vec{v}_2"): GREEN, (r"\vec{w}"): PURPLE_B, r"k": YELLOW, (r"\vec{0}", r"0"): GREY}
        formula = MTex(r"\det\left(\vec{u}, \vec{v}, \vec{w}\right)", tex_to_color_map = color_map).shift(3.5*UP)
        graph_1, graph_2, graph_3 = ImageMobject(r"Patch9_1.png", height = 4).shift(UP + 4.5*LEFT), ImageMobject(r"Patch9_2.png", height = 4).shift(UP), ImageMobject(r"Patch9_3.png", height = 4).shift(UP + 4.5*RIGHT)
        surr_1, surr_2, surr_3 = SurroundingRectangle(graph_1, color = GREEN), SurroundingRectangle(graph_2, color = YELLOW), SurroundingRectangle(graph_3, color = RED)
        axiom_1 = MTex(r"\det\left(\vec{u}_1+k\vec{u}_2, \vec{v}, \vec{w}\right)=\det\left(\vec{u}_1, \vec{v}, \vec{w}\right)+k\det\left(\vec{u}_2, \vec{v}, \vec{w}\right)", tex_to_color_map = color_map).scale(0.8).next_to(1.5*DOWN + 6*LEFT)
        axiom_2 = MTex(r"\det\left(\vec{u}, \vec{v}, \vec{w}\right)=\det\left(\vec{u}+k\vec{v}, \vec{v}, \vec{w}\right)", tex_to_color_map = color_map).scale(0.8).next_to(2.5*DOWN + 6*LEFT)
        axiom_3 = MTex(r"\begin{vmatrix}1&0&0\\0&1&0\\0&0&1\end{vmatrix}=1").scale(0.8).next_to(2*DOWN + 4*RIGHT)
        colors = [BLUE, GREEN, PURPLE]
        for i in range(6, 15):
            axiom_3[i].set_color(colors[i%3])
        lamp_1, lamp_2, lamp_3 = [Circle(radius = 0.2, stroke_color = WHITE, fill_color = color, fill_opacity = 1).next_to(mob, LEFT) for color, mob in zip([GREEN, YELLOW, RED], [axiom_1, axiom_2, axiom_3])]
        self.add(formula).wait(1, 17) #在三维空间中 道理也是一样的
        self.wait(2, 15) #我们一样能从体积的概念中 提炼出
        self.play(FadeIn(axiom_1), FadeIn(lamp_1), FadeIn(graph_1), FadeIn(surr_1))
        # self.wait() #线性性
        self.play(FadeIn(axiom_2), FadeIn(lamp_2), FadeIn(graph_2), FadeIn(surr_2))
        self.wait(0+1-2, 28+7) #平移不变性和
        self.play(FadeIn(axiom_3), FadeIn(lamp_3), FadeIn(graph_3), FadeIn(surr_3))
        self.wait(0, 20) #单位体积这三条公理来
        self.wait(0, 18) #（空闲）

        self.play(*[FadeOut(mob, 4.5*UP) for mob in [formula, graph_1, graph_2, graph_3, surr_1, surr_2, surr_3]], *[mob.animate.shift(4.5*UP) for mob in [axiom_1, axiom_2, axiom_3]], *[mob.animate.shift(4.5*UP).set_fill(opacity = 0) for mob in [lamp_1, lamp_2, lamp_3]], run_time = 2)
        # self.wait() #按照同样的思路

        equation_1 = MTex(r"\det\left(\vec{u}, \vec{v}, \vec{w}\right)=-\det\left(\vec{v}, \vec{u}, \vec{w}\right)", tex_to_color_map = color_map).scale(0.8)
        texts = r"0=\det\left(\vec{u}+\vec{v}, \vec{u}+\vec{v}, \vec{w}\right)=&\det\left(\vec{u}+\vec{v}, \vec{u}, \vec{w}\right)+\det\left(\vec{u}+\vec{v}, \vec{v}, \vec{w}\right)\\=&\det\left(\vec{v}, \vec{u}, \vec{w}\right)+\det\left(\vec{u}, \vec{v}, \vec{w}\right)"
        calculate_1 = MTex(texts, tex_to_color_map = color_map).scale(0.8).next_to(equation_1, DOWN)
        self.play(Write(equation_1), lamp_1.animate.set_fill(opacity = 1), lamp_2.animate.set_fill(opacity = 1), FadeIn(calculate_1, 0.5*UP))
        self.wait(1+2-3, 17+3) #我们也能证出反对称性
        lamp_4 = Circle(radius = 0.2, stroke_color = GREY, fill_color = BLUE).next_to(UP + 5*LEFT, LEFT, buff = 0)
        self.play(equation_1.animate.next_to(UP + 5*LEFT), follow(lamp_4, equation_1, FadeIn), FadeOut(calculate_1), lamp_1.animate.set_fill(opacity = 0), lamp_2.animate.set_fill(opacity = 0))
        self.wait(0, 9) #需要提醒的是
        equation_2 = MTex(r"\det\left(\vec{u}, \vec{v}, \vec{w}\right)=-\det\left(\vec{v}, \vec{u}, \vec{w}\right)=-\det\left(\vec{w}, \vec{v}, \vec{u}\right)=-\det\left(\vec{u}, \vec{w}, \vec{v}\right)", tex_to_color_map = color_map).scale(0.8)
        equation_2.shift(equation_1[0].get_center()-equation_2[0].get_center())
        self.play(FadeIn(equation_2[28:]))
        self.remove(equation_1).add(equation_2).wait(3, 2) #反对称性同样是对任意两个坐标都成立的
        self.wait(2, 2) #计算方法也一样
        self.wait(1, 8) #有了这些性质
        self.wait(3, 4) #我们就能算出三阶行列式的展开式了
        self.wait(1, 2) #（空闲）

        color_map = {(r"x_1", r"y_1", r"z_1"): BLUE, (r"x_2", r"y_2", r"z_2"): GREEN, (r"x_3", r"y_3", r"z_3"): PURPLE, r"0": GREY}
        texts = r"\begin{vmatrix}x_1&x_2&x_3\\y_1&y_2&y_3\\z_1&z_2&z_3\end{vmatrix}=\begin{vmatrix}x_1&0&0\\0&y_2&y_3\\0&z_2&z_3\end{vmatrix}+", r"\begin{vmatrix}0&x_2&x_3\\y_1&0&0\\0&z_2&z_3\end{vmatrix}", r"+\begin{vmatrix}0&x_2&x_3\\0&y_2&y_3\\z_1&0&0\end{vmatrix}"
        equation_3 = MTex("".join(texts), isolate = texts, tex_to_color_map = color_map).shift(0.5*DOWN).scale(0.8)
        parts_3 = [equation_3.get_part_by_tex(text) for text in texts]
        last = ImageMobject(r"Video_6_2.png", height = 8)
        self.play(FadeIn(self.shade), FadeIn(last))
        self.wait(1, 0) #第一步还是用线性性
        self.wait(2, 17) #把第一列按坐标展开
        lamp_1.set_fill(opacity = 1), lamp_2.set_fill(opacity = 1)
        self.add(equation_3, last).play(FadeOut(last), FadeOut(self.shade))
        self.wait(1, 8) #第二步也是用平移不变性
        self.wait(2, 6) #消掉对应行上的元素
        self.wait(0, 28) #（空闲）

        self.wait(1, 3) #但是
        self.wait(4, 7) #这个形式还没法直接化成单位体积
        texts = r"\begin{vmatrix}0&x_2&x_3\\y_1&0&0\\0&z_2&z_3\end{vmatrix}", r"=\begin{vmatrix}0&x_2&x_3\\y_1&0&0\\0&0&z_3\end{vmatrix}+\begin{vmatrix}0&0&x_3\\y_1&0&0\\0&z_2&z_3\end{vmatrix}", r"=\begin{vmatrix}0&x_2&0\\y_1&0&0\\0&0&z_3\end{vmatrix}+\begin{vmatrix}0&0&x_3\\y_1&0&0\\0&z_2&0\end{vmatrix}"
        equation_4 = MTex("".join(texts), isolate = texts, tex_to_color_map = color_map).shift(0.5*DOWN).scale(0.8)
        parts_4 = [equation_4.get_part_by_tex(text) for text in texts]
        anim = ReplacementTransform(parts_3[1], parts_4[0])
        self.play(anim, follow(parts_3[0], anim, FadeOut), follow(parts_3[2], anim, FadeOut), run_time = 2)
        self.wait(0, 28) #我们还得再展开一次
        self.wait(1, 11) #比如说中间这项
        self.play(FadeIn(parts_4[1], 0.5*LEFT), lamp_2.animate.set_fill(opacity = 0))
        self.wait(2, 21) #我们可以再次将第二列按坐标展开
        self.play(FadeIn(parts_4[2], 0.5*LEFT), lamp_1.animate.set_fill(opacity = 0), lamp_2.animate.set_fill(opacity = 1))
        self.wait(1, 18) #然后消掉对应行上的元素

        texts = r"\begin{vmatrix}0&x_2&0\\y_1&0&0\\0&0&z_3\end{vmatrix}+\begin{vmatrix}0&0&x_3\\y_1&0&0\\0&z_2&0\end{vmatrix}", r"=-\begin{vmatrix}0&x_2&0\\y_1&0&0\\0&0&z_3\end{vmatrix}+\begin{vmatrix}0&0&x_3\\y_1&0&0\\0&z_2&0\end{vmatrix}"
        equation_5 = MTex("".join(texts), isolate = texts, tex_to_color_map = color_map).shift(0.5*DOWN).scale(0.8)
        parts_5 = [equation_5.get_part_by_tex(text) for text in texts]
        parts_5[0].save_state().match_x(parts_4[2], LEFT)
        minus = parts_5[1][1].copy().move_to(parts_5[1][26])
        equation_6 = MTex(r"=-y_1x_2z_3+y_1x_3z_2", tex_to_color_map = color_map).scale(0.8)
        equation_6.shift(parts_5[1][0].get_center() - equation_6[0].get_center() + 1.5*DOWN)
        v1_1, v1_2, v1_3 = VGroup(*[parts_5[1][i] for i in (8, 12, 13, 16)]), VGroup(*[parts_5[1][i] for i in (9, 10, 14, 17)]), VGroup(*[parts_5[1][i] for i in (11, 15, 18, 19)])
        x1_1, x1_2, x1_3 = v1_1.get_x(), v1_2.get_x(), v1_3.get_x(), 
        v2_1, v2_2, v2_3 = VGroup(*[parts_5[1][i] for i in (33, 37, 38, 41)]), VGroup(*[parts_5[1][i] for i in (34, 39, 42, 43)]), VGroup(*[parts_5[1][i] for i in (35, 36, 40, 44)])
        x2_1, x2_2, x2_3 = v2_1.get_x(), v2_2.get_x(), v2_3.get_x(), 
        shade = BackgroundRectangle(parts_5[0], buff = 0.3).shift(0.2*RIGHT)
        anim = ReplacementTransform(parts_4[2][0], parts_5[1][0], run_time = 2)
        self.bring_to_back(parts_5[0], shade).play(parts_5[0].animating(run_time = 2).restore(), follow(parts_4[0], parts_5[0], FadeOut, run_time = 2), follow(parts_4[1], parts_5[0], FadeOut, run_time = 2), anim, ReplacementTransform(parts_4[2][1:], parts_5[1][2:], run_time = 2), follow(shade, anim, run_time = 2), lamp_2.animate.set_fill(opacity = 0))
        self.wait(4, 9) #这样，我们就得到了每行每列都恰好只有一个非零元素的形式
        self.play(lamp_4.animate.set_fill(opacity = 1))
        self.wait(2, 10) #然后就可以用反对称性交换列了
        self.play(v1_1.animating(path_arc = -PI/4).set_x(x1_2), v1_2.animating(path_arc = -PI/4).set_x(x1_1), ShowCreation(parts_5[1][1]))
        self.wait(1, 19) #第一项需要交换一次 所以是负的
        self.play(v2_1.animating(path_arc = -PI/4).set_x(x2_2), v2_2.animating(path_arc = -PI/4).set_x(x2_1), Transform(parts_5[1][26].save_state(), minus))
        self.play(v2_2.animating(path_arc = -PI/6).set_x(x2_3), v2_3.animating(path_arc = -PI/6).set_x(x2_1), parts_5[1][26].animate.restore())
        self.wait(0, 8) #第二项需要交换两次 负负得正
        self.wait(0, 26) #（空闲）
        self.play(lamp_4.animate.set_fill(opacity = 0), lamp_3.animate.set_fill(opacity = 1), lamp_1.animate.set_fill(opacity = 1), FadeIn(equation_6, 0.5*UP))
        self.wait(4, 5) #每次交换完后 我们就可以把对角线上这些元素用线性性提取出来
        self.wait(3, 14) #再把剩下的部分用第三条公理变成1
        self.wait(0, 24) #（空闲）

        parts_4[0].set_x(parts_5[0].get_x(LEFT) - 0.2, RIGHT)
        offset = parts_5[0][-1].get_center() - parts_4[0][-1].get_center() + LEFT
        anim = FadeIn(parts_4[0].shift(offset), offset, run_time = 2)
        self.play(anim, follow(parts_5[0], anim, remover = True, run_time = 2), *[mob.animating(run_time = 2).shift(LEFT) for mob in [parts_5[1], shade, equation_6]], lamp_2.animate.set_fill(opacity = 1), lamp_4.animate.set_fill(opacity = 1))
        self.remove(shade).wait(0, 25) #于是 我们就算出了第二项的值

        texts = r"\begin{vmatrix}x_1&x_2&x_3\\y_1&y_2&y_3\\z_1&z_2&z_3\end{vmatrix}=\begin{vmatrix}x_1&0&0\\0&y_2&y_3\\0&z_2&z_3\end{vmatrix}+", r"\begin{vmatrix}0&x_2&x_3\\y_1&0&0\\0&z_2&z_3\end{vmatrix}", r"+\begin{vmatrix}0&x_2&x_3\\0&y_2&y_3\\z_1&0&0\end{vmatrix}"
        equation_7 = MTex("".join(texts), isolate = texts, tex_to_color_map = color_map).shift(0.5*DOWN + LEFT).scale(0.8)
        parts_7 = [equation_7.get_part_by_tex(text) for text in texts]
        texts = r"=x_1y_2z_3-x_1z_2y_3", r"-y_1x_2z_3+y_1z_2x_3", r"+z_1x_2y_3-z_1y_2x_3"
        equation_8 = MTex(r"".join(texts), isolate = texts, tex_to_color_map = color_map).scale(0.8)
        equation_8.shift(equation_7[30].get_center() - equation_8[0].get_center() + 1.5*DOWN)
        parts_8 = [equation_8.get_part_by_tex(text) for text in texts]
        anim_1 = ReplacementTransform(parts_4[0], parts_7[1])
        anim_2 = ReplacementTransform(equation_6[1:], parts_8[1])
        self.play(anim_1, follow(parts_5[1], anim_1, OverFadeOut), *[follow(mob, anim_1, OverFadeIn) for mob in [parts_7[0], parts_7[2]]], anim_2, follow(equation_6[0], anim_2, OverFadeOut), *[follow(mob, anim_2, OverFadeIn) for mob in [parts_8[0], parts_8[2]]], run_time = 2)
        self.wait(0, 10) #对其它两项如法炮制
        self.wait(3, 12) #就得到三阶行列式的完全展开式了
        self.wait(0, 26) #（空闲）

        self.wait(2, 0) #第一次展开成了三项
        self.wait(2, 0) #第二次每项展开成了两项
        self.wait(3, 9) #所以三阶行列式的展开式总共会有六项
        self.wait(0, 23) #（空闲）
        self.wait(4, 22) #怎么样 是不是第一次知道了三阶行列式为什么是长成这个样子的了
        self.wait(1, 12) #（空闲）
        self.wait(2, 18) #你肯定会想到 诶 这个方法很通用
        self.wait(2, 14) #更高阶的行列式也能这么算
        self.fade_out(run_time = 0.5)

class Video_10(FrameScene):
    def construct(self):
        self.frames += 106*30
        color_map = {re.compile(r"x_{.1}"): LIME, re.compile(r"x_{.2}"): GREEN, re.compile(r"x_{.3}"): TEAL, re.compile(r"x_{.4}"): BLUE, r"0": GREY}
        text_0 = r"\begin{vmatrix}x_{11}&x_{12}&x_{13}&x_{14}\\x_{21}&x_{22}&x_{23}&x_{24}\\x_{31}&x_{32}&x_{33}&x_{34}\\x_{41}&x_{42}&x_{43}&x_{44}\end{vmatrix}"
        from itertools import permutations
        terms = []
        def unit_det(t: tuple[int]):
            rows = []
            for i in range(4):
                entries = [r"x_{" + str(i+1) + str(t[i]) + r"}" if j+1 == t[i] else r"0" for j in range(4)]
                rows.append(r"&".join(entries))
            return r"\begin{vmatrix}" + r"\\".join(rows) + r"\end{vmatrix}"
        for t in permutations([1, 2, 3, 4]):
            terms.append(unit_det(t))
        isolates = [text_0, r"=", r"+".join(terms), r"+".join(terms[:7]) ,r"+"+terms[7]+r"+", r"+".join(terms[8:])]
        expand = MTex(text_0 + r"=" + r"+".join(terms), isolate = isolates, tex_to_color_map = color_map).scale(0.6).next_to(2*UP + 6*LEFT)
        parts = [expand.get_part_by_tex(text) for text in isolates]
        self.fade_in(parts[0], run_time = 0.5)
        self.wait(0, 12) #诶 没错
        self.wait(1, 12) #比如说四阶
        parts[2].save_state().match_x(parts[1], RIGHT)
        shade_2 = BackgroundRectangle(parts[2], buff = 0.1).save_state()
        parts[2].match_x(parts[0], RIGHT)
        shade_2.move_to(parts[2])
        parts[1].save_state().match_x(parts[0], RIGHT)
        shade_1 = BackgroundRectangle(parts[1], buff = 0.1)
        self.wait(0, 13)
        self.add(parts[2], shade_2, parts[1], shade_1, parts[0]).play(parts[1].animate.restore(), shade_2.animate.restore(), parts[2].animating(run_time = 5).restore())
        # self.wait() 不过它的展开式嘛，实在是有点......长
        self.wait(0, 28) #（空闲）
        self.wait(2, 21) #对于四阶行列式来说 我们一共会得到
        self.wait(3, 23) #4×3×2=24个分行列式
        self.wait(0, 16) #（空闲）
        self.wait(3, 28) #这时候再去把展开式完全写出来就有点不现实了

        equation_2 = MTex(text_0 + r"=\cdots+"+terms[7]+r"+\cdots", isolate = [text_0, r"=", r"\cdots", r"+"+terms[7]+r"+"] + [r"x_{12}", r"x_{21}", r"x_{34}", r"x_{43}"], tex_to_color_map = color_map).scale(0.6).next_to(2*UP + 6*LEFT)
        parts_2 = [equation_2.get_part_by_tex(text) for text in [text_0, r"=", r"\cdots", r"+"+terms[7]+r"+"]] + [equation_2[-3:]]
        entries = [equation_2.get_parts_by_tex(text)[1] for text in [r"x_{12}", r"x_{21}", r"x_{34}", r"x_{43}"]]
        anim = ReplacementTransform(parts[4], parts_2[3])
        self.bring_to_back(parts[3]).play(anim, follow(parts[3], anim, OverFadeOut, over_factor = 1.1), follow(parts_2[2], anim, FadeIn), follow(parts_2[4], anim, FadeIn), run_time = 3)
        self.clear().add(equation_2).wait(0, 12) #我们得看看每一项具体会有什么特征
        self.wait(1, 3) #（空闲）

# class Video10_2(FrameScene):
#     def construct(self):
#         color_map = {re.compile(r"x_{.1}"): LIME, re.compile(r"x_{.2}"): GREEN, re.compile(r"x_{.3}"): TEAL, re.compile(r"x_{.4}"): BLUE, r"0": GREY}
#         text_0 = r"\begin{vmatrix}x_{11}&x_{12}&x_{13}&x_{14}\\x_{21}&x_{22}&x_{23}&x_{24}\\x_{31}&x_{32}&x_{33}&x_{34}\\x_{41}&x_{42}&x_{43}&x_{44}\end{vmatrix}"
#         def unit_det(t: tuple[int]):
#             rows = []
#             for i in range(4):
#                 entries = [r"x_{" + str(i+1) + str(t[i]) + r"}" if j+1 == t[i] else r"0" for j in range(4)]
#                 rows.append(r"&".join(entries))
#             return r"\begin{vmatrix}" + r"\\".join(rows) + r"\end{vmatrix}"
#         terms = ["" for _ in range(7)] + [unit_det((2, 1, 4, 3))]
#         equation_2 = MTex(text_0 + r"=\cdots+"+terms[7]+r"+\cdots", isolate = [text_0, r"=", r"\cdots", r"+"+terms[7]+r"+"] + [r"x_{12}", r"x_{21}", r"x_{34}", r"x_{43}"], tex_to_color_map = color_map).scale(0.6).next_to(2*UP + 6*LEFT)
#         parts_2 = [equation_2.get_part_by_tex(text) for text in [text_0, r"=", r"\cdots", r"+"+terms[7]+r"+"]] + [equation_2[-3:]]
#         entries = [equation_2.get_parts_by_tex(text)[1] for text in [r"x_{12}", r"x_{21}", r"x_{34}", r"x_{43}"]]
#         self.add(equation_2).wait()      #

        equation_2.set_stroke(width = 6, color = BLACK, background = True)
        surrs = [Circle(radius = 0.12, stroke_width = 0, fill_opacity = 1, fill_color = YELLOW).scale(np.array([1.8, 1.2, 1])).move_to(mob).shift(0.03*UP) for mob in entries]
        all = BackgroundRectangle(VGroup(*surrs), buff = 0)
        line_h, line_v = Line(all.get_corner(LEFT), all.get_corner(RIGHT), stroke_width = 3, color = YELLOW), Line(all.get_corner(UP), all.get_corner(DOWN), stroke_width = 3, color = YELLOW)
        lines_h = [line_h.copy().match_y(mob).shift(0.02*UP) for mob in entries]
        lines_v = [line_v.copy().match_x(mob).shift(0.02*UP) for mob in [entries[1], entries[0], entries[3], entries[2]]]
        self.bring_to_back(*surrs).play(*[GrowFromCenter(mob) for mob in surrs])
        self.wait(1, 15) #首先 因为我们的化简
        self.bring_to_back(*lines_h).play(*[ShowCreation(lines_h[i], delay = 0.2*i) for i in range(4)], frames = 60)
        self.bring_to_back(*lines_v).play(*[ShowCreation(lines_v[i], delay = 0.2*i) for i in range(4)], *[Uncreate(lines_h[i].reverse_points(), delay = 0.2*i) for i in range(4)], frames = 60)
        self.play(*[Uncreate(lines_v[i].reverse_points(), delay = 0.2*i) for i in range(4)], frames = 60)
        self.wait(2+3+1-6, 1+22+2) #我们所得到的每一项里头 都是每一行每一列都恰好只有一个非零元 （空闲）

        equation_3 = MTex(r"(-1)^0"+terms[7], isolate = [r"(-1)^0", terms[7]], tex_to_color_map = color_map).scale(0.6)
        parts_3 = [equation_3.get_part_by_tex(text) for text in [r"(-1)^0", terms[7]]]
        symbol_3 = MTex(r"=")[0].rotate(PI/2).move_to(parts_2[3]).shift(1.25*UP)
        equation_3.shift(parts_2[3][1].get_center() - parts_3[1][0].get_center())
        parts_3[0].shift(2.5*DOWN)
        shade = BackgroundRectangle(VGroup(symbol_3, parts_3[1]))
        self.bring_to_back(parts_3[1], symbol_3, shade).play(*[FadeOut(mob) for mob in surrs], parts_3[1].animate.shift(2.5*DOWN), symbol_3.animate.shift(2.5*DOWN))
        self.remove(shade).wait(0, 21) #对于这样的式子
        
        v1, v2, v3, v4 = VGroup(*[parts_3[1][i] for i in (8, 14, 15, 16, 20, 26)]), VGroup(*[parts_3[1][i] for i in (9, 10, 11, 17, 21, 27)]), VGroup(*[parts_3[1][i] for i in (12, 18, 22, 28, 29, 30)]), VGroup(*[parts_3[1][i] for i in (13, 19, 23, 24, 25, 31)])
        x1, x2, x3, x4 = v1.get_x(), v2.get_x(), v3.get_x(), v4.get_x()
        replace_1, replace_2 = MTex(r"(-1)^1", color = YELLOW).scale(0.6), MTex(r"(-1)^2", color = YELLOW).scale(0.6)
        for i in range(5):
            replace_1[i].move_to(parts_3[0][i]), replace_2[i].move_to(parts_3[0][i])
        self.play(v1.animating(path_arc = -PI/4).set_x(x2), v2.animating(path_arc = -PI/4).set_x(x1), ShowCreation(replace_1))
        self.play(v3.animating(path_arc = -PI/4).set_x(x4), v4.animating(path_arc = -PI/4).set_x(x3), Transform(replace_1, replace_2))
        self.wait(0, 14) #我们只需要通过交换列
        self.wait(1, 27) #就可以把所有非零元
        self.wait(1, 27) #都挪到主对角线上
        
        buff = symbol_3.get_y(DOWN) - parts_3[1].get_y(UP)
        symbol_4 = symbol_3.copy().next_to(parts_3[1], DOWN, buff = buff)
        equation_4 = MTex(r"(-1)^2x_{12}x_{21}x_{34}x_{43}", tex_to_color_map = {r"(-1)^2": YELLOW, **color_map}).scale(0.6).next_to(symbol_4, DOWN, buff = buff)
        group_4 = VGroup(symbol_4, equation_4).save_state().match_y(parts_3[1], DOWN)
        shade = BackgroundRectangle(group_4)
        self.bring_to_back(group_4, shade).play(group_4.animate.restore())
        self.remove(shade)# .wait()得到这一项的值
        self.wait(1, 5) #（空闲）

        self.wait(3, 13) #值是有了 那怎么表达这一项呢
        texts = r"1\to2", r"2\to1", r"3\to4", r"4\to3"
        arrows = [MTex(texts[i]).scale(0.8).shift(2.9*RIGHT + 2*UP + i*0.5*DOWN) for i in range(4)]
        for i in range(4):
            arrows[i][0].set_color(interpolate_color(RED, ORANGE, 0.5)), arrows[i][2].set_color(interpolate_color(YELLOW, ORANGE, 0.5))
        title = Title(r"置换").scale(0.8).shift(0.6*DOWN + 4*RIGHT)
        titleline = Line(2.5*UP + 2*RIGHT, 2.5*UP + 6*RIGHT)
        texts = r"\sigma(1)=2", r"\sigma(2)=1", r"\sigma(3)=4", r"\sigma(4)=3"
        mappings = [MTex(texts[i]).scale(0.8).shift(5*RIGHT + 2*UP + i*0.5*DOWN) for i in range(4)]
        for i in range(4):
            mappings[i][0].set_color(ORANGE), mappings[i][2].set_color(interpolate_color(RED, ORANGE, 0.5)), mappings[i][5].set_color(interpolate_color(YELLOW, ORANGE, 0.5))
        self.play(*[FadeIn(arrows[i], 0.3*RIGHT, delay = 0.2*i) for i in range(4)], frames = 60)
        self.wait(2, 18) #这就要看非零元行和列的对应关系了
        self.wait(3, 10) #由于每行每列都只有一个非零元
        self.play(*[FadeIn(mappings[i], 0.3*RIGHT, delay = 0.2*i) for i in range(4)], frames = 60)
        self.wait(4, 5) #这其实是从1234到1234的一个一一映射
        self.wait(0, 14) #（空闲）
        self.play(Write(title), GrowFromCenter(titleline))
        self.wait(1, 9) #或者说 这有一个专门的名词
        self.wait(1, 22) #叫做置换
        
        inv = MTex(r"\tau(\sigma)=2").shift(DOWN + 4*RIGHT)
        inv[0].set_color(PURPLE_B), inv[2].set_color(ORANGE), inv[5].set_color(PURPLE_B)
        self.play(Write(inv), replace_1[4].animate.set_color(PURPLE_B), equation_4[4].animate.set_color(PURPLE_B), IndicateAround(replace_1[4]), IndicateAround(equation_4[4]))
        self.wait(1, 14) #而-1的次数代表了我们交换了多少次
        self.wait(0, 21) #（空闲）
        tip = Songti("*视频中介绍的逆序对数\n和实际的概念有所区别，\n但不影响行列式的正负号。", color = GREY).scale(0.4).move_to(2*DOWN + 4*RIGHT)
        self.play(FadeIn(tip, 0.5*UP))
        self.wait(0, 6) #这个数字
        self.wait(2, 26) #正好叫做置换的逆序对数
        self.wait(0, 27) #（空闲）

        color_map = {r"(-1)": YELLOW, r"\tau(\sigma)": PURPLE_B, r"x_{1\sigma(1)}": GREEN, r"x_{2\sigma(2)}": LIME, r"x_{3\sigma(3)}": BLUE, r"x_{4\sigma(4)}": TEAL, r"\sigma": ORANGE}
        raw_5 = MTex(r"(-1)^{\tau(\sigma)}x_{1\sigma(1)}x_{2\sigma(2)}x_{3\sigma(3)}x_{4\sigma(4)}=(-1)^2", tex_to_color_map = color_map).scale(0.6)
        raw_5.shift(equation_4[0].get_center() - raw_5[-5].get_center())
        equation_5 = raw_5[:-5]
        self.play(Write(equation_5), FadeOut(tip))
        self.wait(3, 4) #用这些符号 我们可以把这24项都表示成统一的形式

        self.play(inv.animate.shift(1.5*DOWN), *[mob.animate.shift(2*DOWN) for mob in [title, titleline, *arrows, *mappings]])
        color_map = {r"(-1)": YELLOW, r"S_4": RED, r"\tau(\sigma)": PURPLE_B, r"x_{\sigma(1)1}": LIME, r"x_{\sigma(2)2}": GREEN, r"x_{\sigma(3)3}": TEAL, r"x_{\sigma(4)4}": BLUE, r"\sigma": ORANGE}
        raw_6 = MTex(r"\cdots=\sum_{\sigma\in S_4}(-1)^{\tau(\sigma)}x_{\sigma(1)1}x_{\sigma(2)2}x_{\sigma(3)3}x_{\sigma(4)4}", tex_to_color_map = color_map).scale(0.6)
        raw_6.shift(equation_2[-3].get_center() - raw_6[0].get_center())
        equation_6 = raw_6[3:]
        self.play(Write(equation_6))
        self.wait(1+3-3, 25+21) #再把它们都加起来 这就是书上这个很恐怖的展开式了

        self.play(IndicateAround(equation_6[4:6]))
        self.wait(1, 16) #这里的S4是所有置换组成的集合
        self.wait(0, 24) #（空闲）
        self.play(IndicateAround(equation_6[1:6]))
        self.wait(1, 19) #大sigma符号则表示对所有的置换求和
        self.wait(1, 4) #（空闲）
        
        self.wait(4, 21) #就是我们在整个线性代数最最最一开始学习的行列式展开式
        self.wait(3, 24) #底层原理真正的由来
        self.wait(5, 3) #我们的线性代数教材 不讲线性空间 不讲体积的基本原理 什么都不讲 嘿
        self.wait(1, 15) #直接上这个东西
        self.wait(2, 6) #一上来就搞晕了不知道多少同学
        self.wait(3, 28) #让无数同学一头的雾水一直学到线性代数结束
        self.wait(2, 0) #实在是让人非常痛心
        self.wait(0, 28) #（空闲）

#################################################################### 
        
class BlackBox(VGroup):
    def __init__(self, **kwargs):
        
        core = Square(side_length = 2, fill_color = BLACK, fill_opacity = 1)
        entrance = Polygon(1.1*LEFT + 0.5*UP, 1.7*LEFT + UP, 1.7*LEFT + DOWN, 1.1*LEFT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        export = Polygon(1.1*RIGHT + 0.5*UP, 1.7*RIGHT + UP, 1.7*RIGHT + DOWN, 1.1*RIGHT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        # background = Rectangle(width = 3, height = 2, stroke_width = 0, fill_color = BLACK, fill_opacity = 1)
        super().__init__(core, entrance, export, **kwargs)# background, 

class Patch11_1(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        offset = 2*DOWN
        axis_x, axis_y = Arrow(3.5*LEFT, 3.5*RIGHT, stroke_width = 4).shift(offset), Arrow(1*DOWN, 5*UP, stroke_width = 4).shift(offset)
        p_A = offset + np.array([3, 1, 0])
        p_B = offset + np.array([1, 4, 0])
        p_C = offset + np.array([-2, 3, 0])
        p_D = offset
        parallelogram = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 6)
        vector_a = Arrow(p_D, p_A, color = BLUE, buff = 0, stroke_width = 10)
        vector_b = Arrow(p_D, p_C, color = GREEN, buff = 0, stroke_width = 10)
        list_1 = [axis_x, axis_y, parallelogram, vector_a, vector_b]
        self.add(*list_1)

class Patch11_2(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*OUT)

        x, y, z = np.array([1, -2, 1]), np.array([1, 2, 1]), np.array([0, 1, 2])
        vector_a, vector_b, vector_c = Arrow(ORIGIN, x, buff = 0, color = BLUE, stroke_width = 8), Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True, stroke_width = 8), depth_test = True)
        volume = Parallelepiped(x=x, y=y, z=z, opacity = 0.8, color = BLUE)
        self.add(axes, volume, vector_a, vector_b, vector_c)

class Video_11(FrameScene):
    def construct(self):

        self.wait(0, 19) #（空闲）
        color_map = {re.compile(r"x_{.1}"): BLUE, re.compile(r"x_{.2}"): GREEN, re.compile(r"x_{.3}"): PURPLE}
        title = Title(r"行列式")
        titleline = TitleLine()
        graph_1, graph_2 = ImageMobject(r"Patch11_1.png", height = 3.5).shift(1*UP + 3*LEFT), ImageMobject(r"Patch11_2.png", height = 3.5).shift(1*UP + 3*RIGHT)
        det_2 = MTex(r"\begin{vmatrix}x_{11}&x_{12}\\x_{21}&x_{22}\end{vmatrix}", tex_to_color_map = color_map).shift(2*DOWN + 3*LEFT)
        det_3 = MTex(r"\begin{vmatrix}x_{11}&x_{12}&x_{13}\\x_{21}&x_{22}&x_{23}\\x_{31}&x_{32}&x_{33}\end{vmatrix}", tex_to_color_map = color_map).shift(2*DOWN + 3*RIGHT)
        self.fade_in(graph_1, graph_2, title, titleline, det_2, det_3)
        self.wait(0, 25) #相信有很多小伙伴会问
        self.wait(4, 13) #那除了算一个平行n面体的体积 行列式到底有什么用呢
        self.wait(3, 11) #我们实际面对的需要计算面积 体积的情况
        self.wait(2, 10) #可能远远要比一个平行四边形复杂
        self.wait(0, 25) #（空闲）

        paras = {"fill_color": YELLOW, "fill_opacity": 0.2, "stroke_color": WHITE, "stroke_width": 4}
        matrix = MTex(r"\begin{bmatrix}2&-1\\1&{1}\end{bmatrix}", tex_to_color_map = {(r"2", r"1"): BLUE, (r"-1", r"{1}"): GREEN}).shift(2.5*UP + 5*LEFT).set_stroke(**stroke_dic)
        det = MTex(r"\begin{vmatrix}2&-1\\1&{1}\end{vmatrix}=3", tex_to_color_map = {(r"2", r"1"): BLUE, (r"-1", r"{1}"): GREEN, r"3": YELLOW}).shift(2.5*UP + 2*LEFT).set_stroke(**stroke_dic)
        ratio = 0.5
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        back = grid.copy().set_color(GREY)
        self.fade_out(run_time = 0.5).fade_in(back, grid, matrix, run_time = 0.5)
        self.wait(3, 5) #这里 大家可以回想之前我们提到的线性映射

        arrow_1, arrow_2, parallelogram = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8), Polygon(ORIGIN, RIGHT, UR, UP, **paras)
        self.play(GrowFromPoint(parallelogram, ORIGIN), GrowArrow(arrow_1), GrowArrow(arrow_2))
        self.wait(2, 23) #一个矩阵A本质上是对于一个空间进行线性变换

        operator = np.array([[2, -1], [1, 1]])
        self.play(*[mob.save_state().animate.apply_matrix(operator) for mob in [grid, arrow_1, arrow_2, parallelogram]], run_time = 2)
        self.wait(0, 21) #它会拉伸 旋转整个空间
        self.play(*[mob.animate.restore() for mob in [grid, arrow_1, arrow_2, parallelogram]], run_time = 2)
        self.wait(2, 4) #一个单位矩阵所代表的正方原本的面积是1
        self.play(*[mob.animate.apply_matrix(operator) for mob in [grid, arrow_1, arrow_2, parallelogram]], run_time = 2)
        self.wait(0, 29) #被映射之后得到的平行四边形
        vec_1, vec_2 = MTex(r"\begin{bmatrix}2\\1\end{bmatrix}", color = BLUE).next_to(arrow_1, RIGHT).set_stroke(**stroke_dic), MTex(r"\begin{bmatrix}-2\\1\end{bmatrix}", color = GREEN).next_to(arrow_2, LEFT).set_stroke(**stroke_dic)
        self.play(Write(vec_1), Write(vec_2))
        self.wait(2, 3) #刚好就是原来的方阵A每一列所对应的向量
        self.wait(0, 15) #（空闲）
        self.play(Write(det, run_time = 1))
        self.wait(1, 3) #它的面积是A的行列式
        self.wait(0, 24) #（空闲）

        self.fade_out(run_time = 0.5)
        matrix = MTex(r"\begin{bmatrix}4&{2}\\2&{1}\end{bmatrix}", tex_to_color_map = {(r"4", r"2"): BLUE, (r"{2}", r"{1}"): GREEN}).shift(2.5*UP + 5*LEFT).set_stroke(**stroke_dic)
        det = MTex(r"\begin{vmatrix}4&{2}\\2&{1}\end{vmatrix}=0", tex_to_color_map = {(r"4", r"2"): BLUE, (r"{2}", r"{1}"): GREEN, r"0": GREY}).shift(2.5*UP + 2*LEFT).set_stroke(**stroke_dic)
        ratio = 0.5
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        back = grid.copy().set_color(GREY)
        arrow_1, arrow_2, parallelogram = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8), Polygon(ORIGIN, RIGHT, UR, UP, **paras)
        self.fade_in(back, grid, parallelogram, arrow_1, arrow_2, matrix, det, run_time = 0.5).wait(0, 16) #所以 你就很容易理解了
        
        operator = np.array([[4, 2], [2, 1]])
        self.play(*[mob.save_state().animate.apply_matrix(operator) for mob in [grid, parallelogram, arrow_1, arrow_2]], run_time = 2)
        self.wait(1+2-2, 13+19) #为什么行列式为0 等于整个线性映射不可逆了
        self.play(*[mob.animate.restore() for mob in [grid, parallelogram, arrow_1, arrow_2]], run_time = 2)
        self.wait(1, 6) #因为不可逆就等价于出现了空间的压缩
        self.wait(2, 9) #也就是说一个单位矩阵
        self.play(*[mob.save_state().animate.apply_matrix(operator) for mob in [grid, parallelogram, arrow_1, arrow_2]], run_time = 2)
        self.wait(1, 14) #经过映射之后没有充满整个空间的维度
        self.wait(3, 1) #在n维空间中体积为0
        self.wait(1, 19) #而这等价于说
        self.wait(1, 18) #A的行列式是0
        self.wait(1, 9) #（空闲）

        matrix = MTex(r"\begin{bmatrix}2&-1\\1&{1}\end{bmatrix}", tex_to_color_map = {(r"2", r"1"): BLUE, (r"-1", r"{1}"): GREEN}).shift(2.5*UP + 5*LEFT).set_stroke(**stroke_dic)
        det = MTex(r"\begin{vmatrix}2&-1\\1&{1}\end{vmatrix}=3", tex_to_color_map = {(r"2", r"1"): BLUE, (r"-1", r"{1}"): GREEN, r"3": YELLOW}).shift(2.5*UP + 2*LEFT).set_stroke(**stroke_dic)
        ratio = 0.5
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        back = grid.copy().set_color(GREY)
        arrow_1, arrow_2, parallelogram = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8), Polygon(ORIGIN, RIGHT, UR, UP, **paras)
        self.fade_out(run_time = 0.5).fade_in(back, grid, matrix, det, parallelogram, arrow_1, arrow_2, run_time = 0.5)
        self.wait(1, 19) #实际上 不光是这个单位正方形
        self.wait(0, 23) #（空闲）

        region_1 = Polygon(1.5*LEFT + 0.5*UP, 1.5*LEFT + DOWN, 3*LEFT + DOWN, 3*LEFT + 0.5*UP, **paras)
        region_2 = Circle(radius = 0.5, **paras).shift(0.5*LEFT + DOWN)
        region_3 = SVGMobject("apple.svg", height = 1, **paras).move_to(UP + 2*RIGHT)
        region_4 = SVGMobject("rabbit.svg", height = 1.5, **paras).move_to(2*DOWN + RIGHT)
        operator = np.array([[2, -1], [1, 1]])
        self.play(FadeIn(region_1), FadeIn(region_2, delay = 0.2), FadeIn(region_3, delay = 0.4), FadeIn(region_4, delay = 0.6), frames = 48)
        self.wait(1-1, 29-18) #这个平面上无论是什么图形
        self.add(matrix, det).play(*[mob.save_state().animate.apply_matrix(operator) for mob in [grid, arrow_1, arrow_2, parallelogram, region_1, region_2, region_3, region_4]], run_time = 2)
        self.wait(0, 29) #在经历了一个线性变换后
        self.wait(3, 2) #面积都会变换成一个相同的倍数
        self.wait(3, 16) #而这个倍数正是A的行列式的值

        self.fade_out(run_time = 0.5)

        matrix = MTex(r"\begin{bmatrix}{a}&{0}\\0&{b}\end{bmatrix}", tex_to_color_map = {(r"{a}", r"0"): BLUE, (r"{b}", r"{0}"): GREEN}).shift(2.5*UP + 5*LEFT).set_stroke(**stroke_dic)
        det = MTex(r"\begin{vmatrix}{a}&{0}\\0&{b}\end{vmatrix}={a}{b}", tex_to_color_map = {(r"{a}", r"0"): BLUE, (r"{b}", r"{0}"): GREEN, r"3": YELLOW}).shift(2.5*UP + 2*LEFT).set_stroke(**stroke_dic)
        ratio = 0.5
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-30, 30)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-50, 50)]
        grid = VGroup(*lines_h[:30], *lines_h[31:], *lines_v, lines_h[30])
        back = grid.copy().set_color(GREY)
        arrow_1, arrow_2, circle = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8), Circle(radius = 1, **paras)
        self.fade_in(back, grid, circle, arrow_1, arrow_2, matrix, det, run_time = 0.5)
        self.wait(3, 29) #特别的，我们如果把这个矩阵设置成一个对角阵
        self.wait(1, 14) #[a,b]

        operator = np.array([[3, 0], [0, 2]])
        self.play(*[mob.save_state().animate.apply_matrix(operator) for mob in [grid, circle, arrow_1, arrow_2]], run_time = 2)
        self.wait(0, 13) #再让它作用于一个单位圆
        function_1 = MTex(r"x^2+y^2=1", tex_to_color_map = {r"x^2": BLUE, r"y^2": GREEN}).shift(1*UP + 5*RIGHT).set_stroke(**stroke_dic)
        function_2 = MTex(r"\frac{x^2}{a^2}+\frac{y^2}{b^2}=1", tex_to_color_map = {r"\frac{x^2}{a^2}": BLUE, r"\frac{y^2}{b^2}": GREEN}).shift(1*DOWN + 5*RIGHT).set_stroke(**stroke_dic)
        arrow = Arrow(function_1, function_2, color = YELLOW)
        self.play(FadeIn(function_1), FadeIn(function_2), FadeIn(arrow))
        self.wait(3, 28) #那么新的坐标就变成了(ax,by)
        self.wait(3, 26) #满足的方程就变成了
        self.wait(4, 21) #x^2/a^2+y^2/b^2=1
        self.wait(2, 6) #高中的小伙伴肯定很熟悉了
        self.wait(3, 24) #这是一个a为半长轴 b为半短轴的椭圆
        self.wait(1, 3) #（空闲）
        self.play(IndicateAround(det))
        self.wait(1, 20) #这个矩阵的行列式是ab
        formula = MTex(r"S_{\text{椭圆}}=\pi ab", tex_to_color_map = {r"S_{\text{椭圆}}": YELLOW, r"a": BLUE, r"b": GREEN}).shift(2.5*UP + 3*RIGHT).set_stroke(**stroke_dic)
        self.play(Write(formula), run_time = 1)
        self.wait(5, 10) #我们立刻得到 它的面积是映射之前那个图形面积的ab倍
        self.wait(2, 21) #而之前那个图形我们知道是个单位圆
        self.wait(1, 15) #它的面积是π
        self.wait(1, 17) #所以我们立刻得到
        self.wait(1, 24) #一个半长轴为a
        self.wait(1, 11) #半短轴为b的椭圆
        self.wait(1, 23) #面积等于πab
        self.wait(0, 21) #（空闲）
        
        self.wait(1, 15) #怎么用 没有用微积分
        self.wait(2, 26) #也能得到这样一个简洁的结果 是不是很神奇呢
        self.wait(1, 11) #（空闲）

class Video_12(FrameScene):
    def construct(self):
        self.frames += 131*30 + 10
        title = Title(r"克莱默法则")
        titleline = TitleLine()
        self.fade_in(title, titleline).wait(3, 23) #整个视频的最后 我们来讲一讲一个有关行列式重要的结论
        self.wait(1, 27) #克莱默法则

        color_map = {re.compile(r"a_{.1}"): BLUE, re.compile(r"a_{.2}"): TEAL, re.compile(r"a_{.n}"): GREEN, re.compile(r"x_."): YELLOW, re.compile(r"b_."): ORANGE}
        equations = MTex(r"\begin{bmatrix}a_{11}&a_{12}&\cdots&a_{1n}\\a_{21}&a_{22}&\cdots&a_{2n}\\\vdots&\vdots&\ddots&\vdots\\a_{n1}&a_{n2}&\cdots&a_{nn}\end{bmatrix}\begin{bmatrix}x_1\\x_2\\\vdots\\x_n\end{bmatrix}=\begin{bmatrix}b_1\\b_2\\\vdots\\b_n\end{bmatrix}", tex_to_color_map = color_map).scale(0.8).shift(3*LEFT)
        self.play(FadeIn(equations, 0.5*RIGHT))
        self.wait(2, 12) #它说 解方程Ax=b时

        tex = r"\begin{vmatrix}a_{11}&b_1&\cdots&a_{1n}\\a_{21}&b_2&\cdots&a_{2n}\\\vdots&\vdots&\ddots&\vdots\\a_{n1}&b_n&\cdots&a_{nn}\end{vmatrix}", r"\begin{vmatrix}a_{11}&a_{12}&\cdots&a_{1n}\\a_{21}&a_{22}&\cdots&a_{2n}\\\vdots&\vdots&\ddots&\vdots\\a_{n1}&a_{n2}&\cdots&a_{nn}\end{vmatrix}"
        solution = MTex(r"x_2=\frac{" + tex[0] + r"}{" + tex[1] + r"}", tex_to_color_map = color_map, isolate = tex).scale(0.8).shift(3.5*RIGHT)
        self.play(FadeIn(solution.get_part_by_tex(tex[0]), 0.5*DOWN))
        self.wait(3, 24) #如果用b替换A的第i列 算出这个新矩阵的行列式
        self.play(FadeIn(solution.get_part_by_tex(tex[1]), 0.5*UP), FadeIn(solution[66], 0.5*RIGHT))
        self.wait(1, 24) #再除以A的行列式
        self.play(Write(solution[:3]))
        self.wait(3, 8) #一定刚好等于x的第i个分量
        self.wait(2, 3) #也就是第i个未知数的解
        self.wait(0, 28) #（空闲）

        self.wait(5, 8) #这个结论 如果用计算的方法来证明是非常繁琐的
        self.wait(4, 10) #但是如果你深入理解了行列式的几何含义
        self.wait(3, 6) #那么几乎是显然的事情

        self.fade_out(run_time = 0.5)
        paras = {"fill_color": YELLOW, "fill_opacity": 0.2, "stroke_color": WHITE, "stroke_width": 4}
        texts = r"\begin{bmatrix}2&-1\\1&{1}\end{bmatrix}", r"\begin{bmatrix}x\\y\end{bmatrix}", r"\begin{bmatrix}1\\1.4\end{bmatrix}"
        matrix = MTex(texts[0] + texts[1] + r"=" + texts[2], isolate = texts, tex_to_color_map = {(r"2", r"1"): BLUE, (r"-1", r"{1}"): GREEN, texts[1]: YELLOW, texts[2]: ORANGE}).shift(2.5*UP + 3*LEFT).set_stroke(**stroke_dic)
        formula = MTex(r"x=\frac{\begin{vmatrix}1&-1\\1.4&{1}\end{vmatrix}}{\begin{vmatrix}2&-1\\1&1\end{vmatrix}}").shift(1.5*DOWN + 3*LEFT).set_stroke(**stroke_dic)
        for i, color in [(0, YELLOW)] + [(i, ORANGE) for i in [6, 9, 10, 11]] + [(i, BLUE) for i in [22, 25]] + [(i, GREEN) for i in [7, 8, 12, 23, 24, 26]]:
            formula[i].set_fill(color = color)
        ratio = 0.5
        n_h, n_v = 10, 15
        lines_h = [Line(3*LEFT_SIDE + i*ratio*DOWN, 3*RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-n_h, n_h+1)]
        lines_v = [Line(3*4*UP + i*ratio*RIGHT, 3*4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 3, color = BLUE_E if i else WHITE) for i in range(-n_v, n_v+1)]
        grid = VGroup(*lines_h[:n_h], *lines_h[n_h+1:], *lines_v, lines_h[n_h])
        back = grid.copy().set_color(GREY)
        
        arrow_1, arrow_2, arrow_x, parallelogram = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, stroke_width = 8), Arrow(ORIGIN, UP, color = GREEN, buff = 0, stroke_width = 8), Arrow(ORIGIN, np.array([0.8, 0.6, 0]), color = YELLOW, buff = 0, stroke_width = 8), Polygon(ORIGIN, np.array([0.8, 0.6, 0]), UP + np.array([0.8, 0.6, 0]), UP, **paras)
        change = [grid, arrow_1, arrow_2, arrow_x, parallelogram]
        operator = np.array([[2, -1], [1, 1]])
        for mob in change:
            mob.save_state().apply_matrix(operator)
        arrow_x.set_color(ORANGE)
        self.fade_in(back, matrix, formula, parallelogram, arrow_1, arrow_2, arrow_x, run_time = 0.5)
        self.wait(2, 11) #以二维为例 我们来看x分量的解
        label_0 = MTex(r"S_{\text{变换前}} \to", tex_to_color_map = {r"S_{\text{变换前}}": YELLOW}).scale(0.8).next_to(formula[0], LEFT).set_stroke(**stroke_dic)
        label_1 = MTex(r"\leftarrow S_{\text{变换后}}", tex_to_color_map = {r"S_{\text{变换后}}": YELLOW}).scale(0.8).next_to(formula[2:17]).set_stroke(**stroke_dic)
        label_2 = MTex(r"\leftarrow \text{比例系数}", tex_to_color_map = {r"\text{比例系数}": YELLOW}).scale(0.8).next_to(formula[18:]).set_stroke(**stroke_dic)
        self.play(FadeIn(label_1, 0.5*LEFT))
        self.wait(0, 16) #分子上的行列式
        self.wait(2, 16) #是这个平行四边形的面积
        self.wait(0, 23) #（空闲）

        self.bring_to_back(back, *lines_h[:n_h], *lines_h[n_h+1:], *lines_v, lines_h[n_h]).play(
            LaggedStart(*[ShowCreation(line) for line in lines_h], run_time = 2, lag_ratio = 0.05, group = VGroup()), 
            LaggedStart(*[ShowCreation(line) for line in lines_v], run_time = 2, lag_ratio = 0.05, group = VGroup()), 
        )
        self.wait(1, 26) #那这个平行四边形 在线性变换之前长什么样呢
        self.bring_to_back(back, grid).play(*[mob.animate.restore() for mob in change], run_time = 2)
        self.wait(0, 24) #我们可以倒回去看看
        self.wait(3, 2) #张成平行四边形的两个向量
        self.play(WiggleOutThenIn(arrow_x))
        self.wait(1, 6) #分别回到了未知的(x,y)
        self.play(WiggleOutThenIn(arrow_2))
        self.wait(0, 24) #与单位向量(0,1)
        before = MTex(r"\begin{vmatrix}{x}&0\\y&1\end{vmatrix}={x}", tex_to_color_map = {(r"{x}", r"y"): YELLOW, (r"0", r"1"): GREEN}).set_stroke(**stroke_dic).next_to(parallelogram, UR)
        self.play(Write(before), run_time = 1)
        self.wait(2, 9) #线性变换之前的这个平行四边形
        self.play(FadeIn(label_0, 0.5*RIGHT))
        self.wait(2, 6) #面积恰好是x
        self.play(FadeIn(label_2, 0.5*LEFT))
        self.wait(4, 11) #而我们又知道 线性变换前后的面积比 就是A的行列式
        self.wait(4, 9) #于是x的值 就正好是这两个行列式相除了
        self.wait(2, 28)
        self.play(FadeOut(before)) #因为 变换之前我们知道 它的这个面积是x
        self.play(*[mob.animate.apply_matrix(operator) for mob in [grid, arrow_1, arrow_2, parallelogram]], arrow_x.animate.apply_matrix(operator).set_color(ORANGE), run_time = 2)
        self.wait(2, 9) #变换之后的面积是A的行列式乘以这个式子
        self.wait(1, 24) #（空闲）

        texts = r"\begin{bmatrix}\vec{a}_1&\vec{a}_2&\cdots&\vec{a}_n\end{bmatrix}", r"\begin{bmatrix}x_1\\x_2\\\vdots\\x_n\end{bmatrix}", r"=", r"\vec{b}"
        equation = MTex("".join(texts), isolate = texts, tex_to_color_map = {re.compile(r"\\vec{a}_."): GREEN, re.compile(r"x_."): YELLOW, r"\vec{b}": ORANGE}).scale(0.8).shift(4*LEFT + 0.5*DOWN)
        parts = [equation.get_part_by_tex(text) for text in texts]
        texts = r"A", r"\vec{x}"
        matrix = MTex("".join(texts), tex_to_color_map = {r"A": GREEN, r"\vec{x}": YELLOW, r"=": WHITE, r"\vec{b}": ORANGE}).shift(1.5*UP)
        for i in range(2):
            matrix.get_part_by_tex(texts[i]).match_x(parts[i])
        self.fade_out(run_time = 0.5).fade_in(title, titleline, equation, matrix, run_time = 0.5)
        self.wait(2, 0) #同样的道理一样可以应用于n维

        formula = MTex(r"\det(A\vec{v}_1, A\vec{v}_2, \cdots, A\vec{v}_n)=\det(A)\det(\vec{v}_1, \vec{v}_2, \cdots, \vec{v}_n)", isolate = r"=", tex_to_color_map = {r"A": GREEN, re.compile(r"\\vec{v}_."): BLUE}).scale(0.8).next_to(3*UP, DOWN)
        self.play(FadeIn(formula, 0.5*LEFT))
        self.wait(2, 13) #当我们对n个向量做A这个线性映射的时候
        explain = MTex(r"\Rsh\text{其实就是}\det(AB)=\det(A)\det(B)\text{按列展开}", color = GREY).scale(0.6).next_to(formula, DOWN)
        explain[0].rotate(PI/2)
        explain.shift((formula.get_part_by_tex(r"=").get_x() - explain[0].get_x())*RIGHT + 0.06*RIGHT)
        self.play(FadeIn(explain, 0.3*UL))
        self.wait(3, 29) #变换后的行列式是变换前的行列式乘以乘以A的行列式
        self.wait(0, 23) #（空闲）

        x_i = MTex(r"x_i=\det(\vec{e}_1, \cdots, \vec{e}_{i-1}, \vec{x}, \vec{e}_{i+1}, \cdots, \vec{e}_n)", tex_to_color_map = {(r"\vec{x}", r"x_i"): YELLOW, (r"\vec{e}_1", r"\vec{e}_n", r"\vec{e}_{i-1}", r"\vec{e}_{i+1}"): BLUE}).scale(0.7).shift(2.5*RIGHT + 1*UP)
        self.play(FadeIn(x_i, 0.5*UP))
        self.wait(2, 9) #想知道哪个x_i的值
        Ax_i = MTex(r"\det(A)x_i=\det(A\vec{e}_1, \cdots, A\vec{e}_{i-1}, A\vec{x}, A\vec{e}_{i+1}, \cdots, A\vec{e}_n)", tex_to_color_map = {(r"\vec{a}_1", r"\vec{a}_n", r"\vec{a}_{i-1}", r"\vec{a}_{i+1}", r"A"): GREEN, (r"\vec{e}_1", r"\vec{e}_n", r"\vec{e}_{i-1}", r"\vec{e}_{i+1}"): BLUE, (r"x_i", r"\vec{x}"): YELLOW, r"\vec{b}": ORANGE}).scale(0.7)
        Ax_i.shift(x_i[2].get_center() - Ax_i[8].get_center() + 0.8*DOWN)
        b = MTex(r"=\det(\vec{a}_1, \cdots, \vec{a}_{i-1}, \vec{b}, \vec{a}_{i+1}, \cdots, \vec{a}_n)", tex_to_color_map = {(r"\vec{a}_1", r"\vec{a}_n", r"\vec{a}_{i-1}", r"\vec{a}_{i+1}", r"A"): GREEN, (r"\vec{e}_1", r"\vec{e}_n", r"\vec{e}_{i-1}", r"\vec{e}_{i+1}"): BLUE, r"\vec{b}": ORANGE}).scale(0.7)
        b.shift(x_i[2].get_center() - b[0].get_center() + 1.6*DOWN)
        self.play(FadeIn(Ax_i, 0.5*UP), FadeIn(b, 0.5*UP))
        self.wait(1, 17) #就把用b替换掉哪个x_i
        self.wait(2, 17) #把这些向量逆映射回去
        self.wait(3, 0) #得到的体积正好就是x_i
        self.wait(0, 19) #（空闲）
        
        self.wait(3, 7) #所以x_i正好可以表示成
        self.play(IndicateAround(b[1:]), IndicateAround(Ax_i[:6], delay = 1.5))
        self.wait(4-3, 19-15) #后来的体积 除以这个体积变换过程当中的倍数
        self.wait(0, 25) #（空闲）
        self.wait(2, 9) #而这个倍数 是另一个行列式
        solution = MTex(r"x_i=\frac{\det(\vec{a}_1, \cdots, \vec{a}_{i-1}, \vec{b}, \vec{a}_{i+1}, \cdots, \vec{a}_n)}{\det(\vec{a}_1, \cdots, \vec{a}_{i-1}, \vec{a}_i, \vec{a}_{i+1}, \cdots, \vec{a}_n)}", tex_to_color_map = {(r"\vec{a}_1", r"\vec{a}_n", r"\vec{a}_{i-1}", r"\vec{a}_{i+1}", r"\vec{a}_i", r"A"): GREEN, (r"\vec{e}_1", r"\vec{e}_n", r"\vec{e}_{i-1}", r"\vec{e}_{i+1}"): BLUE, (r"x_i", r"\vec{x}"): YELLOW, r"\vec{b}": ORANGE}).scale(0.7)
        solution.shift(x_i[2].get_center() - solution[2].get_center() + 3*DOWN)
        self.play(FadeIn(solution))
        self.wait(2, 18) #所以 x_i总是可以写成两个行列式的商
        
        self.wait(0, 25) #（空闲）
        self.wait(3, 23) #这样 我们就非常清晰直观的借助行列式的性质
        self.wait(1, 18) #理解了克莱默法则
        self.wait(1, 13) #（空闲）

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        