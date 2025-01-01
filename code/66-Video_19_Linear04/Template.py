from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Video2_1(FrameScene):
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
        texts = r"S", r"=\frac{1}{2}wh", r"=\frac{1}{2}|ad-bc|"
        tex_3 = MTex(r"S=\frac{1}{2}wh=\frac{1}{2}|ad-bc|", isolate = texts, tex_to_color_map = {r"S": YELLOW, r"w": GREEN, r"h": BLUE}).shift(3.5*RIGHT + 1.5*DOWN)
        parts_3 = [tex_3.get_part_by_tex(text) for text in texts]
        configs = {r"run_time": 2, r"squish_interval": (1/2, 1)}
        self.bring_to_back(height_line2, dash).play(Write(VGroup(tex_1, tex_2, tex_3), run_time = 3), ShowCreation(height_line2), ShowCreation(width_line2), ShowCreation(dash), 
                  Write(label_height, **configs), Write(label_base, **configs), Write(label_H, **configs), Write(text_area, **configs))
        self.wait(2+0-3, 22+24) #那就是水平宽乘铅垂高/2 （空闲）
        self.play(tex_3[11:].animate.set_color(YELLOW), IndicateAround(tex_3[11:]))
        self.wait(1, 18) #三种计算理所当然会都得到一模一样的式子

        shade = BackgroundRectangle(parts_3[1]).match_x(parts_3[2], LEFT).shift(0.1*LEFT)
        self.add(parts_3[1], shade, parts_3[2]
                 ).play(parts_3[2].animate.shift(parts_3[1][0].get_center() - parts_3[2][0].get_center() + 1.5*UP + 0.5*RIGHT), follow(shade, parts_3[2]), parts_3[0].animate.shift(1.5*UP + 0.5*RIGHT), parts_3[1].animate.shift(1.5*UP + 0.5*RIGHT), 
                        *[FadeOut(mob) for mob in [label_H, label_height, height_line2, dash, width_line2, label_base, text_area]],
                        FadeOut(tex_1, 0.5*UP), FadeOut(tex_2, 1*UP), 
                        triangle_1.animate.set_fill(color = YELLOW, opacity = 0.5), 
                        label_A.animate.next_to(p2_A, DR), label_B.animate.next_to(p2_B, UL))
        self.remove(parts_3[1], shade)
        self.wait(2, 1) #1/2|ad-bc|
        self.wait(1, 11) #（空闲）

        triangle_2 = triangle_1.copy().set_fill(opacity = 0)
        self.bring_to_back(triangle_2).play(Rotate(triangle_2, -PI, about_point = (p2_A + p2_B)/2), run_time = 2)
        self.wait()
        self.play(triangle_2.animate.set_fill(color = YELLOW, opacity = 0.5), FadeOut(parts_3[2][1:4], 0.5*UP))
        self.wait()
        
#################################################################### 

class Video3_1(FrameScene):
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

class Video3_2(FrameScene):
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
        vector_A = Arrow(p_D, p_A, color = YELLOW, buff = 0, stroke_width = 8)
        vector_B = Arrow(p_D, p_C, color = RED_B, buff = 0, stroke_width = 8)
        self.add(formula, axis_x, axis_y, parallelogram_0, fill_0, parallelogram, label_A, label_B, vector_A, vector_B).wait(0, 22) #据此......

        vector_1 = Arrow(p_D, p_E, color = GREEN, buff = 0, stroke_width = 8)
        vector_2 = Arrow(p_E, p_A, color = PURPLE_B, buff = 0, stroke_width = 8)
        self.play(ReplacementTransform(Line.set_stroke(Arrow(p_D, p_F, color = YELLOW, buff = 0, stroke_width = 6), width = 6), vector_1), ReplacementTransform(Arrow(p_F, p_A, color = YELLOW, buff = 0, stroke_width = 6), vector_2))
        self.wait(2, 5) #我们可以把(a,b)拆成两个向量

        line = Line(p_E, p_G)
        line_2 = Line(p_G, p_H, color = GREY)
        self.add(line, vector_A, vector_B, vector_1, vector_2).play(ShowCreation(line))
        self.wait(1, 9) #然后作一条平行线

        parallelogram_1 = Polygon(p_F, p_G, p_C, p_D)
        parallelogram_2 = Polygon(p_A, p_B, p_G, p_F)
        fill_1 = Polygon(p_F, p_G, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        fill_2 = Polygon(p_A, p_B, p_G, p_F, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        self.remove(parallelogram, fill_0).bring_to_back(parallelogram_0, fill_1, fill_2).add(line_2, parallelogram_1, parallelogram_2, line, vector_A, vector_B, vector_1, vector_2).play(
            Transform(parallelogram_1, Polygon(p_E, p_H, p_C, p_D)),
            Transform(parallelogram_2, Polygon(p_A, p_B, p_H, p_E)),
            Transform(fill_1, Polygon(p_E, p_H, p_C, p_D, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0)),
            Transform(fill_2, Polygon(p_A, p_B, p_H, p_E, fill_color = PURPLE_B, fill_opacity = 0.5, stroke_width = 0)),
            line.animate.put_start_and_end_on(p_E, p_H), ShowCreation(line_2))
        self.wait(1, 19) #把这个平行四边形分成两个
        self.wait(0, 28) #（空闲）
        
        list_0 = [axis_x, axis_y, parallelogram_0, label_A, label_B, vector_A, vector_B, vector_1, vector_2, line, line_2, parallelogram_1, parallelogram_2, fill_1, fill_2]
        list_1 = [axis_x.copy(), axis_y.copy(), fill_1.copy(), parallelogram_1.copy(), MTex(r"(c, d)", tex_to_color_map = {r"d": GREEN}).next_to(p_C, UP), MTex(r"(a, 0)", tex_to_color_map = {r"a": GREEN}).next_to(p_E, UR), vector_B.copy(), vector_1.copy()]
        list_2 = [Arrow(2.5*LEFT, 1.5*RIGHT, stroke_width = 3).shift(offset), axis_y.copy(), fill_2.copy().shift(3*LEFT), parallelogram_2.copy().shift(3*LEFT), MTex(r"(c, d)", tex_to_color_map = {r"c": PURPLE_B}).next_to(p_C, LEFT), MTex(r"(0, b)", tex_to_color_map = {r"b": PURPLE_B}).next_to(p_I, RIGHT), vector_B.copy(), vector_2.copy().shift(3*LEFT)]
        label_a = MTex(r"a", color = GREEN).next_to((offset + np.array([3, 0, 0])/2), DOWN).set_stroke(**stroke_dic)
        label_d = MTex(r"d", color = GREEN).next_to((offset + np.array([0, 3, 0])/2), RIGHT).set_stroke(**stroke_dic)
        label_b = MTex(r"b", color = PURPLE_B).next_to((offset + np.array([0, 1, 0])*0.4), RIGHT).set_stroke(**stroke_dic)
        label_c = MTex(r"-c", color = PURPLE_B).next_to((offset + np.array([-2, 0, 0])/2), DOWN).set_stroke(**stroke_dic)
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
        tex_2 = MTex(r"-bc", color = PURPLE_B).move_to(5*RIGHT + UP)
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
        vector_A = Arrow(p_D, p_A, color = YELLOW, buff = 0, stroke_width = 8)
        vector_B = Arrow(p_D, p_C, color = RED_B, buff = 0, stroke_width = 8)
        vector_1 = Arrow(p_D, p_E, color = GREEN, buff = 0, stroke_width = 8)
        vector_2 = Arrow(p_E, p_A, color = ORANGE, buff = 0, stroke_width = 8)
        self.fade_in(formula, axis_x, axis_y, parallelogram_0, fill_0, parallelogram, label_A, label_B, vector_A, vector_B, vector_1, vector_2, excepts = [formula])
        self.wait(1, 8) #当然 它们的面积不总应该加起来
        
        line_a = DashedLine(p_A, p_F)
        line_b = DashedLine(p_B, p_G)
        line = Line(p_E, p_G)
        line_2 = Line(p_G, p_H, color = GREY)
        self.add(line_a, line_b, line, vector_A, vector_B, vector_1, vector_2, label_A, label_B).play(ShowCreation(line), ShowCreation(line_a), ShowCreation(line_b), fill_0.animate.set_points_as_corners([p_F, p_G, p_C, p_D]).close_path())
        self.wait(0, 7) #这种情况下

        parallelogram_1 = Polygon(p_F, p_G, p_C, p_D)
        parallelogram_2 = Polygon(p_A, p_B, p_G, p_F)
        fill_1 = Polygon(p_F, p_G, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        fill_2 = Polygon(p_A, p_B, p_G, p_F, fill_color = YELLOW, fill_opacity = 0, stroke_width = 0)
        self.remove(parallelogram, fill_0).bring_to_back(parallelogram_0, fill_1, fill_2).add(line_2, parallelogram_1, parallelogram_2, line, vector_A, vector_B, vector_1, vector_2, label_A, label_B).play(
            Transform(parallelogram_1, Polygon(p_E, p_H, p_C, p_D)),
            Transform(parallelogram_2, Polygon(p_A, p_B, p_H, p_E)),
            Transform(fill_1, Polygon(p_E, p_H, p_C, p_D, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0)),
            Transform(fill_2, Polygon(p_A, p_B, p_H, p_E, fill_color = ORANGE, fill_opacity = 0.5, stroke_width = 0)),
            line.animate.put_start_and_end_on(p_E, p_H), ShowCreation(line_2), line_a.animate.set_color(GREY), line_b.animate.set_color(GREY))
        self.wait(2, 2) #要是不考虑有向面积 两部分就该相减了

        self.wait(0+1-2, 22+27) #（空闲）...
        list_0 = [axis_x, axis_y, parallelogram_0, label_A, label_B, vector_A, vector_B, vector_1, vector_2, line_a, line_b, line, line_2, parallelogram_1, parallelogram_2, fill_1, fill_2]
        list_1 = [axis_x.copy(), axis_y.copy(), fill_1.copy(), parallelogram_1.copy(), MTex(r"(c, d)", tex_to_color_map = {r"d": GREEN}).next_to(p_C, UP), MTex(r"(a, 0)", tex_to_color_map = {r"a": GREEN}).next_to(p_E, DR), vector_B.copy(), vector_1.copy()]
        list_2 = [Arrow(1.5*LEFT, 2.5*RIGHT, stroke_width = 3).shift(offset), axis_y.copy(), fill_2.copy().shift(3*LEFT), parallelogram_2.copy().shift(3*LEFT), MTex(r"(c, d)", tex_to_color_map = {r"c": ORANGE}).next_to(p_C, RIGHT), MTex(r"(0, b)", tex_to_color_map = {r"b": ORANGE}).next_to(p_I, LEFT), vector_B.copy(), vector_2.copy().shift(3*LEFT)]
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
    
def multi_smooth(n: int):
    def util(t: float):
        peroid = math.floor(t*n)
        subalpha = t*n - peroid
        return smooth(1 - subalpha) if peroid%2 else smooth(subalpha)
    return util

class Video3_3(FrameScene):
    def construct(self):
        def case(x: np.ndarray, y: np.ndarray):
            x_0 = x[0]*RIGHT
            color_2 = PURPLE_B if (x[1]*y[0])*(x[0]*y[1]) < 0 else ORANGE
            left, right = (min(0, x[0], y[0], x[0]+y[0]) - 0.6)*RIGHT, (max(0, x[0], y[0], x[0]+y[0]) + 0.6)*RIGHT
            up, down = (min(0, x[1], y[1], x[1]+y[1]) - 0.6)*UP, (max(0, x[1], y[1], x[1]+y[1]) + 0.6)*UP
            offset = -(left + right + up + down)/2 + 4*LEFT
            axis_x, axis_y = Arrow(left, right, stroke_width = 3).shift(offset), Arrow(up, down, stroke_width = 3).shift(offset)
            p_A, p_B, p_C, p_D, p_E, p_H = offset + x, offset + x + y, offset + y, offset, offset + x_0, offset + x_0 + y
            parallelogram_0 = Polygon(p_A, p_B, p_C, p_D, fill_color = YELLOW, fill_opacity = 0.2, stroke_color = GREY)
            vector_A = Arrow(p_D, p_A, color = YELLOW, buff = 0)
            vector_B = Arrow(p_D, p_C, color = RED_B, buff = 0)
            vector_1 = Arrow(p_D, p_E, color = GREEN, buff = 0)
            vector_2 = Arrow(p_E, p_A, color = color_2, buff = 0)
            parallelogram_1 = Polygon(p_E, p_H, p_C, p_D, fill_color = GREEN, fill_opacity = 0.5)
            parallelogram_2 = Polygon(p_A, p_B, p_H, p_E, fill_color = color_2, fill_opacity = 0.5)

            unit_x, unit_y = x/get_norm(x), y/get_norm(y)
            diff = (np.arctan2(y[1], y[0]) - np.arctan2(x[1], x[0]) + PI) % TAU - PI
            sign = np.sign(x[0]*y[1]-x[1]*y[0])
            angle = Arrow(unit_x, unit_y, path_arc = diff, buff = 0, color = interpolate_color(PURPLE_B if sign > 0 else ORANGE, WHITE, 0.5), stroke_opacity = 0).shift(offset)
            return VGroup(axis_x, axis_y), VGroup(parallelogram_0, parallelogram_1, parallelogram_2, vector_A, vector_B, vector_1, vector_2, angle), sign
        # axis_0, group_0, sign_0  = case(np.array([3, 1, 0]), np.array([-2, 3, 0]))
        # self.add(axis_0, group_0).wait()

        # last_axis, last_group = axis_0, group_0
        # axes, groups, signs = [axis_0], [group_0], [sign_0]
        # x = [[3, 1, 0] for _ in range(16)]
        # y = [[1, 3, 0] for _ in range(16)]
        # for i in range(4):
        #     for j in range(4):
        #         k = i*4+j
        #         axis, group, sign = case(np.array(x[k]), np.array(y[k]))
        #         axes.append(axis), groups.append(group), signs.append(sign)
        #         for mob in [last_axis, last_group]:
        #             mob.scale(0.28, about_point = 4*LEFT).shift(7*RIGHT + 0.5*UP + (i-1.5)*1.6*DOWN + (j-1.5)*1.8*RIGHT)
        #         for mob in last_axis:
        #             mob.set_stroke(width = 2)
        #         for mob in last_group[:3]:
        #             mob.set_stroke(width = 2)
        #         for mob in last_group[3:]:
        #             mob.set_stroke(width = 3)
        #         self.add(axis, group).wait()
        #         last_axis, last_group = axis, group

        axes, groups = [], []
        x = [[3, 1, 0], [3, 1, 0], [3, 2, 0], [3, 3, 0], [-3, 2, 0], [-3, 1, 0], [-2, 2, 0], [-2, 3, 0], [-3, -2, 0], [-4, -2, 0], [-3, -3, 0], [-4, -1, 0], [3, -3, 0], [3, -2, 0], [4, -2, 0], [2, -2, 0]]
        y = [[1, 3, 0], [-2, 3, 0], [2, -2, 0], [-2, -1, 0], [1, 2, 0], [-2, 3, 0], [3, -2, 0], [-3, -1, 0], [1, 2, 0], [-1, 2, 0], [2, -1, 0], [-1, -3, 0], [1, 1, 0], [-2, 2, 0], [1, -2, 0], [-3, -2, 0]]
        positives, negatives = [], []
        for i in range(4):
            for j in range(4):
                k = i*4+j
                axis, group, sign = case(np.array(x[k]), np.array(y[k]))
                axes.append(axis), groups.append(group)
                self.add(axis, group).wait()
                for mob in [axis, group]:
                    mob.center().scale(0.28).shift(3*RIGHT + 0.5*UP + (i-1.5)*1.6*DOWN + (j-1.5)*1.8*RIGHT)
                for mob in axis:
                    mob.set_stroke(width = 2)
                for mob in group[:3]:
                    mob.set_stroke(width = 2)
                for mob in group[3:]:
                    mob.set_stroke(width = 3)
                if sign > 0:
                    positives.append(k)
                else:
                    negatives.append(k)
        self.wait()

        anims = [Animation(VMobject()) for _ in range(16)]
        for k in range(8):
            i, j = k//3, k%3
            anim_p = AnimationGroup(axes[positives[k]].animate.move_to(3.5*LEFT + 0.0*DOWN + (i-1)*1.6*DOWN + (j-1)*1.8*RIGHT), 
                                    groups[positives[k]].animate.move_to(3.5*LEFT + 0.0*DOWN + (i-1)*1.6*DOWN + (j-1)*1.8*RIGHT), 
                                    group = VGroup(), run_time = 2)
            anim_n = AnimationGroup(axes[negatives[k]].animate.move_to(3.5*RIGHT + 0.0*DOWN + (i-1)*1.6*DOWN + (j-1)*1.8*RIGHT), 
                                    groups[negatives[k]].animate.move_to(3.5*RIGHT + 0.0*DOWN + (i-1)*1.6*DOWN + (j-1)*1.8*RIGHT),
                                    group = VGroup())
            anims[positives[k]], anims[negatives[k]] = anim_p, anim_n
        self.play(LaggedStart(*anims, lag_ratio = 0.1, group = VGroup()))
        self.wait()
            
        tex_p, tex_m = MTex(r"ad-bc", color = interpolate_color(PURPLE_B, WHITE, 0.5)).shift(3*UP + 3.5*LEFT), MTex(r"bc-ad", color = interpolate_color(ORANGE, WHITE, 0.5)).shift(3*UP + 3.5*RIGHT)
        tex_a, tex_b = MTex(r"A(a, b)", color = YELLOW).scale(0.8).next_to(ORIGIN, UP), MTex(r"B(c, d)", color = RED).scale(0.8).next_to(ORIGIN, DOWN)
        self.play(FadeIn(tex_a), FadeIn(tex_b))
        self.wait()
        self.play(Write(tex_p))
        self.wait()
        self.play(Write(tex_m))
        self.wait()
            
        left, right = Shade(fill_opacity = 0.8).set_color(BLACK).move_to(LEFT_SIDE), Shade(fill_opacity = 0.8).set_color(BLACK).move_to(RIGHT_SIDE)
        self.add(right, tex_a, tex_b).play(FadeIn(right))
        self.wait()
        arrows_p = []
        for k in range(8):
            arrow = groups[positives[k]][-1]
            groups[positives[k]].remove(arrow)
            arrows_p.append(arrow.set_stroke(opacity = 1))
        self.add(*arrows_p).play(LaggedStart(*[ShowCreation(arrow) for arrow in arrows_p], run_time = 2, lag_ratio = 1/7, group = VGroup(), remover = True))
        self.wait()
        self.add(left, tex_a, tex_b).play(FadeIn(left), FadeOut(right), )
        self.wait()
        arrows_n = []
        for k in range(8):
            arrow = groups[negatives[k]][-1]
            groups[negatives[k]].remove(arrow)
            arrows_n.append(arrow.set_stroke(opacity = 1))
        self.add(*arrows_n).play(LaggedStart(*[ShowCreation(arrow) for arrow in arrows_n], run_time = 2, lag_ratio = 1/7, group = VGroup(), remover = True))
        self.wait()
        self.play(FadeOut(left))
        self.wait()

        tex_all = MTex(r"S = ad-bc", tex_to_color_map = {(r"a", r"b"): YELLOW, (r"c", r"d"): RED}).shift(3.2*UP)
        self.play(Write(tex_all))
        self.wait()
        replace_m = MTex(r"|ad-bc|", color = interpolate_color(ORANGE, WHITE, 0.5)).shift(3*UP + 3.5*RIGHT)
        back = BackgroundRectangle(replace_m, buff = 0.1)
        start, end = VGroup(back.copy(), tex_m), VGroup(back.copy(), replace_m)
        self.add(back.set_color(GREY), start).play(back.animating(rate_func = there_and_back).scale(np.array([1.05, 1.1, 1])), 
                                                   Flip(start, end, dim = 1, rate_func = lambda t: np.sin(smooth(t)*(5*PI/2))**2), run_time = 2)
        self.remove(back, start).add(replace_m).wait()

class Video3_4(FrameScene):
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
        self.add(formula, *example).wait()
        self.play(Write(title), ShowCreation(titleline))
        self.wait(1, 4) #它一般被写成

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

class Video3_5(FrameScene):
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

class Video3_6(FrameScene):
    def construct(self):
        last = ImageMobject("Video_6.png", height = 8)
        volumn_1, volumn_2, volumn_3 = ImageMobject("Patch3_6_1.png", height = 3).move_to(RIGHT + 2*UP), ImageMobject("Patch3_6_2.png", height = 3).move_to(4*RIGHT + 0.5*UP), ImageMobject("Patch3_6_3.png", height = 3).move_to(RIGHT + DOWN)
        self.add(last)

        self.play(last.animate.shift(4*LEFT), OverFadeIn(volumn_1, 4*LEFT), OverFadeIn(volumn_2, 4*LEFT), OverFadeIn(volumn_3, 4*LEFT), run_time = 2)
        self.wait()

class Patch3_6_1(FrameScene):
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
        vector_b, vector_c = Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True, stroke_width = 8)
        volume_1 = Parallelepiped(x=x*RIGHT, y=y, z=z, opacity = 0.3, color = RED, depth_test = True)
        vector_1 = Arrow(ORIGIN, x*RIGHT, buff = 0, color = RED, stroke_width = 8)
        self.add(axes, vector_b, vector_c, vector_1, volume_1)

class Patch3_6_2(FrameScene):
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
        vector_b, vector_c = Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True, stroke_width = 8)
        volume_2 = Parallelepiped(x=x*UP, y=y, z=z, opacity = 0.3, color = ORANGE, depth_test = True)
        vector_2 = Arrow(ORIGIN, x*UP, buff = 0, color = ORANGE, stroke_width = 8)
        self.add(axes, vector_b, vector_c, vector_2, volume_2)

class Patch3_6_3(FrameScene):
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
        vector_b, vector_c = Arrow(ORIGIN, y, buff = 0, color = GREEN, stroke_width = 8), Arrow(ORIGIN, z, buff = 0, color = PURPLE_B, stroke_width = 8) 
        axes = VGroup(Arrow(4*LEFT, 4*RIGHT, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*DOWN, 4*UP, buff = 0, depth_test = True, stroke_width = 8), Arrow(4*IN, 4*OUT, buff = 0, depth_test = True), depth_test = True, stroke_width = 8)
        volume_3 = Parallelepiped(x=OUT, y=y, z=z, opacity = 0.3, color = YELLOW, depth_test = True)
        vector_3 = Arrow(ORIGIN, x*OUT, buff = 0, color = YELLOW, stroke_width = 8)
        self.add(axes, vector_b, vector_c, vector_3, volume_3)
        self.wait()

#################################################################### 

class Video4_1(FrameScene):
    def construct(self):

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
        equation_2_2 = MTex(r"\det(\vec{u}_1+\vec{u}_2+\vec{u}_3, \vec{v})=\det(\vec{u}_1, \vec{v}) + \det(\vec{u}_2, \vec{v}) + \det(\vec{u}_3, \vec{v})", tex_to_color_map = color_map).shift(2.5*DOWN)
        self.add(group, vector_b_l, vector_b_r).play(p.animating(path_arc = -PI/6).move_to(x3))
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
        self.add(group.add_updater(group_updater), vector_b_l, vector_b_r).play(p.animate.move_to(x4), r.animate.move_to(x5), q.animate.move_to(x6), run_time = 2)
        self.wait(0, 3) #那三个向量自然也能加
        self.wait(0, 18) #（空闲）
        x13, x14, x15 = x6*9/23, x6*19/23, x6
        self.play(p.animate.move_to(x13), r.animate.move_to(x14), q.animate.move_to(x15), run_time = 2) 
        self.wait()
        self.play(p.animate.move_to(x4), r.animate.move_to(x5), q.animate.move_to(x6))
        self.wait()
        

        x7, x8, x9 = np.array([2, 0, 0]), np.array([2, 2, 0]), np.array([1, 2, 0])
        self.add(group.add_updater(group_updater), vector_b_l, vector_b_r).play(p.animate.move_to(x7), r.animate.move_to(x8), q.animate.move_to(x9), run_time = 2)
        self.wait()
        
        camera = self.camera.frame
        offset_rr = 1.5*DOWN + 11*RIGHT
        copy = VGroup(axisx_r.copy(), axisy_r.copy(), para_r1.copy(), para_r2.copy(), para_r3.copy(), vector_b_r.copy(), vector_a6_r.copy(), vector_a5_r.copy(), vector_a4_r.copy()).set_fill(opacity = 0)
        target = VGroup(axisx_r.copy(), axisy_r.copy(), para_r1.copy(), para_r2.copy().shift(-x8), para_r3.copy().shift(-x7), vector_b_r.copy().set_color(YELLOW), vector_a6_r.copy().shift(-x7), vector_a5_r.copy().shift(-x8), vector_a4_r.copy()).shift(8*RIGHT)
        self.play(camera.animate.shift(7.5*RIGHT), formula.save_state().animate.set_opacity(0), Transform(copy, target), run_time = 2)
        self.wait()

        angle_b, angle_1, angle_2, angle_3 = np.arctan2(y[1], y[0]), np.arctan2(x7[1], x7[0]), np.arctan2(x8[1]-x7[1], x8[0]-x7[0]), np.arctan2(x9[1]-x8[1], x9[0]-x8[0])
        tip_1 = Arrow(0.3*unit(angle_1), 0.3*unit(angle_b), buff = 0, path_arc = angle_b - angle_1, color = RED).shift(offset_rr)
        tip_2 = Arrow(0.5*unit(angle_2), 0.5*unit(angle_b), buff = 0, path_arc = angle_b - angle_2, color = RED).shift(offset_rr)
        tip_3 = Arrow(0.4*unit(angle_3), 0.4*unit(angle_b), buff = 0, path_arc = angle_b - angle_3, color = GREEN).shift(offset_rr)
        self.play(ShowCreation(tip_1), ShowCreation(tip_2))
        self.wait()
        self.play(ShowCreation(tip_3))
        self.wait()

        x10, x11, x12 = np.array([1, 0, 0]), np.array([2, 0, 0]), np.array([3, 1, 0])
        self.add(group.add_updater(group_updater), vector_b_l, vector_b_r).play(p.animate.move_to(x10), r.animate.move_to(x11), q.animate.move_to(x12), camera.animate.shift(7.5*LEFT), formula.animate.restore(), run_time = 2)
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

#################################################################### 

class Cover(CoverScene):
    def construct(self):
        unseen = ImageMobject(r"unseen.png", height = 6).shift(3*LEFT + 0.5*DOWN)
        det = MTex(r"\begin{vmatrix}1&1&4&5\\1&4&1&9\\1&9&8&1\end{vmatrix}").scale(1.6).shift(3.5*RIGHT + 1.5*DOWN)
        title_0 = Heiti("无痛线代", font = "Microsoft YaHei", weight = BOLD, color = YELLOW).scale(1.8).set_stroke(background = True, width = 20, color = RED)
        title_0[0].move_to(3.5*UP + 4*LEFT)
        title_0[1].move_to(3.5*UP + 2.8*LEFT)
        title_0[2].move_to(3.5*UP + 1.6*LEFT)
        title_0[3].move_to(3.5*UP + 0.4*LEFT)
        title = Heiti("什么是行列式？", font = "Microsoft YaHei", weight = BOLD, color = BLUE).scale(1.8).set_stroke(background = True, width = 20, color = WHITE)
        title[0].move_to(3*UP + 2*RIGHT)
        title[1].move_to(3*UP + 3.2*RIGHT)
        title[2].move_to(3*UP + 4.4*RIGHT)
        title[3].move_to(1.5*UP + 2.3*RIGHT).rotate(PI/18)
        title[4].move_to(1.5*UP + 3.5*RIGHT).rotate(-PI/18)
        title[5].move_to(1.5*UP + 4.7*RIGHT).rotate(PI/18)
        title[6].move_to(1.5*UP + 5.8*RIGHT)
        self.add(unseen, det, title_0, title)

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        