from __future__ import annotations

from manimlib import *
import numpy as np

class Flip(Animation):
    CONFIG = {
        "dim": 1,
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
        self.shift = self.target_mobject.get_center() - self.mobject.get_center()
    
    def interpolate_mobject(self, alpha: float) -> None:
        if alpha <= 0.5:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 1-2*alpha
            self.mobject.become(self.starting_mobject).scale(vector, min_scale_factor = 0).shift(alpha * self.shift)
        else:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 2*alpha-1
            self.mobject.become(self.target_mobject).scale(vector, min_scale_factor = 0).shift((alpha-1) * self.shift)
        if self.color_interpolate:
            self.mobject.set_color(interpolate_color(self.starting_mobject.get_color(), self.target_mobject.get_color(), alpha))
        return self
    
    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.mobject).add(self.target_mobject)
        super().clean_up_from_scene(scene)
        
#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        ball = Dot(radius = 0.2, color = BLUE)
        self.play(ShowCreation(ball))
        self.wait(0, 16) #我们都知道

        alpha = ValueTracker(0.0)
        def shake_updater(mob: VMobject):
            position = mob.get_center()
            shake = np.array([2*random.random()-1, 2*random.random()-1, 0])*0.1
            mob.move_to(interpolate(position, shake, alpha.get_value()))
        ball.add_updater(shake_updater)
        lines = VGroup()
        threshold = 10
        def line_updater(mob: Line):
            start, end = interpolate(mob.begin, mob.ending, fore(mob.frames/threshold)), interpolate(mob.begin, mob.ending, back(mob.frames/threshold))
            mob.put_start_and_end_on(start, end)
            mob.frames += 1
        def line_generater():
            position = np.array([2*random.random()-1, 2*random.random()-1, 0])*np.array([3, 2, 0]) + np.array([2*random.random()-1, 2*random.random()-1, 0])*np.array([3, 2, 0])
            line = Line(stroke_width = 1)
            line.begin, line.ending = position + 2.5*DOWN*(random.random()+random.random()+1)*alpha.get_value(), position + 2.5*UP*(random.random()+random.random()+1)*alpha.get_value()
            line.frames = 0
            line.add_updater(line_updater)
            return line
        def lines_updater(mob: VGroup):
            mob.add(line_generater(), line_generater(), line_generater())
            copy_submobjects = mob.submobjects.copy()
            mob.submobjects = list(filter(lambda t: t.frames < threshold, copy_submobjects))
        lines.add_updater(lines_updater)
        self.bring_to_back(lines).play(alpha.animate.set_value(0.2), rate_func = linear, run_time = 2)
        self.wait(2, 14) #重力加速度g表示物体在自由落体运动时的加速度

        arrow = Arrow(ORIGIN, 1.5*DOWN, color = ORANGE, buff = 0)
        g = MTex(r"g\approx 9.8m/s^2", color = ORANGE).next_to(arrow, RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        left, right = g[:5], g[5:].shift(0.1*RIGHT)
        self.add(arrow, ball).play(ShowCreation(arrow), Write(g))
        self.wait(2, 7) #数值约为9.8m/s^2
        self.play(FadeOut(right, UP), rate_func = back)
        self.wait(3, 20) #这意味着自由落体的物体每秒钟速度都会增加9.8m/s
        self.wait(0, 18) #（空闲）

        pi = MTex(r"\pi=3.1415926535 8979323846 2643383279 5028841971 \cdots", color = TEAL).next_to(3*UP + 6*LEFT, RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        for i in range(47):
            pi[i].shift(0.018*i*RIGHT)
        self.play(FadeIn(pi, 0.5*DOWN), lag_ratio = 0.05, run_time = 3)
        self.wait(0, 26) #我们又都知道 圆周率π的小数长这样
        pi2 = MTex(r"\pi=9.8696044010 8935861883 4490999876 1511353136 \cdots", color = GREEN).next_to(2.4*UP + 6*LEFT, RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        head = MTex(r"\pi^2=", color = GREEN)
        head.shift(pi2[1].get_center() - head[2].get_center())
        for i in range(47):
            pi2[i].shift(0.018*i*RIGHT)
        pi2[0].become(head[:2]).refresh_bounding_box()
        self.play(LaggedStart(*[Flip(pi[i].copy(), pi2[i]) for i in range(47)], run_time = 3, lag_ratio = 0.05))
        self.wait(1+2-3, 10+24) #所以如果你无聊地给π平方的话 就能发现它的小数表示长这样
        self.wait(0, 22) #（空闲）

        approx = MTex(r"\pi^2\approx g", tex_to_color_map = {r"\pi^2": GREEN, r"g": ORANGE}).scale(1.5).shift(1.3*UP).set_stroke(width = 8, color = BLACK, background = True)
        self.play(Write(approx), pi.animate.set_fill(opacity = 0.5), pi2[5:].animate.set_fill(opacity = 0.5))
        self.wait(1, 3) #是不是和g还挺接近的

        roots = MTex(r"\sqrt{\pi^2}\approx \sqrt{g}", tex_to_color_map = {r"\sqrt{\pi^2}": GREEN, r"\sqrt{g}": ORANGE}).scale(1.5).shift(1.3*UP).set_stroke(width = 8, color = BLACK, background = True)
        self.play(Write(roots[:2]), Write(roots[5:7]), *[ReplacementTransform(approx[i], roots[j]) for i, j in zip([0, 1, 2, 3], [2, 3, 4, 7])])
        self.wait(1, 21) #这意味着 如果我们对g开根号

        alter = MTex(r"\pi\approx \sqrt{g}", tex_to_color_map = {r"\pi": TEAL, r"\sqrt{g}": ORANGE}).scale(1.5).shift(1.3*UP).set_stroke(width = 8, color = BLACK, background = True)
        self.play(FadeOut(roots[:2], 0.2*UP), FadeOut(roots[3], 0.2*UP), *[ReplacementTransform(roots[i], alter[j]) for i, j in zip([2, 4], [0, 1])], ReplacementTransform(roots[5:], alter[2:]), FadeOut(pi2, scale = np.array([1, 0, 1]), about_point = 2.7*UP, run_time = 2, lag_ratio = 0.05), pi.animate.set_fill(opacity = 1))
        self.wait(1, 11) #那么得到的数值就会非常接近于π
        self.wait(0, 24) #（空闲）

        self.wait(0, 16) #诶...
        self.play(IndicateAround(alter[0]), run_time = 1.5)
        self.wait(0, 11) #...一个是精确的数学常数...
        self.play(IndicateAround(alter[2:]), run_time = 1.5)
        self.wait(1, 13) #...另一个则是真实世界测量的物理量
        self.wait(1, 26) #这真的仅仅是一个巧合吗
        self.wait(0, 22) #（空闲）

        self.wait(2, 24) #今天的视频会告诉你 在历史的某一刻...
        old = MTex(r"\pi= \sqrt{g}", tex_to_color_map = {r"\pi": TEAL, r"\sqrt{g}": ORANGE}).scale(1.5).shift(1.3*UP).set_stroke(width = 8, color = BLACK, background = True)
        for m_1, m_2 in zip(old, alter):
            m_1.move_to(m_2)
        old.save_state()
        shade_0 = BackgroundRectangle(old, buff = 0.2, fill_opacity = 0)
        shade_1 = BackgroundRectangle(alter, buff = 0.2, fill_color = GREY_E, stroke_color = YELLOW_E, stroke_opacity = 1, stroke_width = 2)
        def showing_updater(mob: VGroup):
            mob.restore()
            for submob in mob:
                submob.set_points(Intersection(submob, shade_0).get_points())
        old.add_updater(showing_updater)
        self.add(shade_1, old).play(shade_0.save_state().scale(np.array([0, 1, 0]), about_point = shade_0.get_left()).animate.restore(), shade_1.save_state().scale(np.array([0, 1, 0]), about_point = shade_1.get_left()).animate.restore())
        old.clear_updaters().restore()
        self.wait(0, 28) #...这曾经根本不是一个巧合
        self.wait(1, 15) #甚至是精确相等的
        self.wait(0, 24) #（空闲）

        self.wait(1, 11) #不过 在此之前
        camera = self.camera.frame
        sqrt = MTex(r"\sqrt{9.8}", color = ORANGE).scale(1.5).shift(6*LEFT + 3*UP + 15*RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        self.play(camera.animating(run_time = 3).shift(15*RIGHT), TransformFromCopy(alter[2:4], sqrt[:2], run_time = 3, rate_func = squish_rate_func(smooth, 1/6, 1)), TransformFromCopy(left[2:], sqrt[2:], run_time = 3, rate_func = squish_rate_func(smooth, 1/4, 1)))
        self.wait(2+3-3, 23+21) #先让我向你仔细地分析和介绍一下 该怎么优雅地手算根号g的数值表示
        self.wait()

class Video_2(FrameScene):
    def construct(self):
        goal = MTex(r"\sqrt{9.8}", color = ORANGE).scale(1.5).shift(6*LEFT + 3*UP)
        self.add(goal)
        result = MTex(r"\sqrt{9.8}\approx 3.1304951684", color = ORANGE).scale(1.5)
        result.shift(goal[0].get_center() - result[0].get_center())

        offset = 6*LEFT + 2*DOWN
        position = lambda t: np.array([t, np.sqrt(t), 0])*0.75 + offset
        p_x = lambda t: np.array([t, 0, 0])*0.75 + offset
        p_y = lambda t: np.array([0, np.sqrt(t), 0])*0.75 + offset
        axes = VGroup(Arrow(0.5*LEFT, 12.5*RIGHT, stroke_width = 3), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3)).shift(offset)
        graph = FunctionGraph(lambda t: np.sqrt(t), [0, 16.5, 0.01]).scale(0.75, about_point = ORIGIN).shift(offset)
        func = MTex(r"y=\sqrt{x}", color = YELLOW).next_to(graph.get_corner(UR), UL)
        self.play(ShowCreation(graph), ShowCreation(axes, lag_ratio = 0))
        self.play(Write(func))
        self.wait()
        x_0 = MTex("9.8", color = YELLOW).scale(0.6).rotate(PI/2).next_to(p_x(9.8), DOWN, buff = 0.1)
        p_0 = Point(position(9.8))
        def dash_updater(target: Point):
            def util(mob: VMobject):
                point = target.get_location()
                line = Polyline(np.array([point[0], offset[1], 0]), point, np.array([offset[0], point[1], 0]))
                line.insert_n_curves(18)
                mob.set_points(DashedVMobject(line, stroke_width = 2, num_dashes = 30).get_all_points())
            return util
        dash_0 = VMobject(stroke_width = 2).add_updater(dash_updater(p_0)).clear_updaters()
        y_0 = MTex(r"\sqrt{9.8}", color = ORANGE).scale(0.5).next_to(p_y(9.8), LEFT, buff = 0.1).save_state()
        self.play(Write(x_0))
        self.wait()
        self.bring_to_back(dash_0).play(ShowCreation(dash_0))
        self.wait()
        dash_0.add_updater(dash_updater(p_0))
        self.play(TransformFromCopy(goal, y_0))
        self.wait()

        x_1 = MTex("9").scale(0.6).rotate(PI/2).next_to(p_x(9), DOWN, buff = 0.1)
        x_2 = MTex("16").scale(0.6).rotate(PI/2).next_to(p_x(16), DOWN, buff = 0.1)
        p_1 = Point(position(9))
        p_2 = Point(position(16))
        dash_1 = VMobject(stroke_width = 2).add_updater(dash_updater(p_1)).clear_updaters()
        dash_2 = VMobject(stroke_width = 2).add_updater(dash_updater(p_2)).clear_updaters()
        y_1 = MTex(r"3").scale(0.5).next_to(p_y(9), LEFT, buff = 0.1).save_state().next_to(y_0, DOWN, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        y_2 = MTex(r"4").scale(0.5).next_to(p_y(16), LEFT, buff = 0.1).save_state()
        self.play(Write(x_1), Write(x_2))
        self.wait()
        self.bring_to_back(dash_1, dash_2).play(ShowCreation(dash_1), ShowCreation(dash_2))
        self.wait()
        dash_1.add_updater(dash_updater(p_1)), dash_2.add_updater(dash_updater(p_2))
        self.play(Write(y_1), Write(y_2))
        self.wait()
        self.play(Write(result[5]), TransformFromCopy(y_1[-1], result[6], path_arc = -PI/6))
        self.wait()

        def p2c(x_1, x_2):
            point_1, point_2 = position(x_1), position(x_2)
            def s(mob: VMobject):
                point_m = (point_1 + point_2)/2
                ratio = point_2-point_1
                ratio[2] = 1
                mob.scale(np.array([10, 3, 0])/ratio, about_point = point_m).shift(- point_m)
            def x(mob: VMobject):
                alpha = inverse_interpolate(point_1[0], point_2[0], mob.get_x())
                mob.set_x(interpolate(-5, 5, alpha))
            def y(mob: VMobject):
                alpha = inverse_interpolate(point_1[1], point_2[1], mob.get_y())
                mob.set_y(interpolate(-1.5, 1.5, alpha))
            return s, x, y
        func_s, func_x, func_y = p2c(9, 16)
        y_1.restore()
        for mob in [graph, p_0, p_1, p_2]:
            func_s(mob.save_state().generate_target())
        for mob in [x_0, x_1, x_2]:
            func_x(mob.save_state().generate_target())
        for mob in [y_0, y_1, y_2]:
            func_y(mob.generate_target())
        y_1.next_to(y_0, DOWN, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        shade = Shade(fill_color = BLACK).append_points(Rectangle(width = 12.5, height = 4.5).shift(0.25*UR).reverse_points().get_points())
        self.remove(goal).add(shade, axes, result[:7], x_0, x_1, x_2, y_0, y_1, y_2, func).play(*[MoveToTarget(mob) for mob in [graph, x_0, x_1, x_2, y_0, y_1, y_2, p_0, p_1, p_2]], func.animate.next_to(6.5*RIGHT + 2*UP, UL), run_time = 2)
        self.wait()

        x_3 = MTex("9.61").scale(0.6).rotate(PI/2).next_to(p_x(9.61), DOWN, buff = 0.1).save_state()
        x_4 = MTex("10.24").scale(0.6).rotate(PI/2).next_to(p_x(10.24), DOWN, buff = 0.1).save_state()
        p_3 = Point(position(9.61)).save_state()
        p_4 = Point(position(10.24)).save_state()
        for mob in [p_3, p_4]:
            func_s(mob)
        dash_3 = VMobject(stroke_width = 2).add_updater(dash_updater(p_3)).clear_updaters().reverse_points()
        dash_4 = VMobject(stroke_width = 2).add_updater(dash_updater(p_4)).clear_updaters().reverse_points()
        y_3 = MTex(r"3.1").scale(0.5).next_to(p_y(9.61), LEFT, buff = 0.1).save_state()
        y_4 = MTex(r"3.2").scale(0.5).next_to(p_y(10.24), LEFT, buff = 0.1).save_state()
        for mob in [x_3, x_4]:
            func_x(mob)
        for mob in [y_3, y_4]:
            func_y(mob)
        y_3.next_to(y_0, DOWN, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        y_4.next_to(y_0, UP, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        self.bring_to_back(dash_3, dash_4).play(Write(y_3), Write(y_4), y_1.animate.next_to(y_3, DOWN, coor_mask = np.array([0, 1, 0]), buff = 0.05), ShowCreation(dash_3), ShowCreation(dash_4))
        self.wait()
        dash_3.add_updater(dash_updater(p_3)), dash_4.add_updater(dash_updater(p_4))
        self.play(Write(x_3), Write(x_4))
        self.wait()
        self.play(Write(result[7]), TransformFromCopy(y_3[-1], result[8], path_arc = -PI/6))
        self.wait()

        func_s, func_x, func_y = p2c(9.61, 10.24)
        for mob in [graph, p_0, p_1, p_2, p_3, p_4]:
            func_s(mob.generate_target().restore())
        for mob in [x_0, x_1, x_2, x_3, x_4]:
            func_x(mob.generate_target().restore())
        for mob in [y_0, y_1, y_2, y_3, y_4]:
            func_y(mob.generate_target().restore())
        big_shade = Shade(fill_color = BLACK).shift(6.5*UP)
        self.add(big_shade, result[:9], func).play(*[MoveToTarget(mob) for mob in [graph, x_0, x_1, x_2, x_3, x_4, y_0, y_1, y_2, y_3, y_4, p_0, p_1, p_2, p_3, p_4]], run_time = 2)
        self.remove(x_1, y_1, dash_1, x_2, y_2, dash_2).wait()
        
        x_5 = MTex("9.7969").scale(0.6).rotate(PI/2).next_to(p_x(3.13**2), DOWN, buff = 0.1).save_state()
        x_6 = MTex("9.8596").scale(0.6).rotate(PI/2).next_to(p_x(3.14**2), DOWN, buff = 0.1).save_state()
        p_5 = Point(position(3.13**2)).save_state()
        p_6 = Point(position(3.14**2)).save_state()
        for mob in [p_5, p_6]:
            func_s(mob)
        dash_5 = VMobject(stroke_width = 2).add_updater(dash_updater(p_5)).clear_updaters().reverse_points()
        dash_6 = VMobject(stroke_width = 2).add_updater(dash_updater(p_6)).clear_updaters().reverse_points()
        y_5 = MTex(r"3.13").scale(0.5).next_to(p_y(3.13**2), LEFT, buff = 0.1).save_state()
        y_6 = MTex(r"3.14").scale(0.5).next_to(p_y(3.14**2), LEFT, buff = 0.1).save_state()
        for mob in [x_5, x_6]:
            func_x(mob)
        for mob in [y_5, y_6]:
            func_y(mob)
        y_5.next_to(y_0, DOWN, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        y_6.next_to(y_0, UP, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        x_5.next_to(x_0, LEFT, coor_mask = np.array([1, 0, 0]), buff = 0.05)
        self.bring_to_back(dash_5, dash_6).play(Write(y_5), Write(y_6), ShowCreation(dash_5), ShowCreation(dash_6))
        self.wait()
        dash_5.add_updater(dash_updater(p_5)), dash_6.add_updater(dash_updater(p_6))
        self.play(Write(x_5), Write(x_6))
        self.wait()
        self.play(TransformFromCopy(y_5[-1], result[9], path_arc = -PI/6))
        self.wait()

        func_s, func_x, func_y = p2c(3.13**2, 3.14**2)
        for mob in [graph, p_0, p_3, p_4, p_5, p_6]:
            func_s(mob.generate_target().restore())
        for mob in [x_0, x_3, x_4, x_5, x_6]:
            func_x(mob.generate_target().restore())
        for mob in [y_0, y_3, y_4, y_5, y_6]:
            func_y(mob.generate_target().restore())
        y_5.target.next_to(y_0.target, DOWN, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        self.add(big_shade, result[:10], func).play(*[MoveToTarget(mob) for mob in [graph, x_0, x_3, x_4, x_5, x_6, y_0, y_3, y_4, y_5, y_6, p_0, p_3, p_4, p_5, p_6]], run_time = 2)
        self.remove(x_3, y_3, dash_3, x_4, y_4, dash_4).wait()

        x_7 = MTex("9.803161").scale(0.6).rotate(PI/2).next_to(p_x(3.131**2), DOWN, buff = 0.1).save_state()
        p_7 = Point(position(3.131**2)).save_state()
        for mob in [p_7]:
            func_s(mob)
        dash_7 = VMobject(stroke_width = 2).add_updater(dash_updater(p_7)).clear_updaters().reverse_points()
        y_7 = MTex(r"3.131").scale(0.5).next_to(p_y(3.131**2), LEFT, buff = 0.1).save_state()
        for mob in [x_7]:
            func_x(mob)
        for mob in [y_7]:
            func_y(mob)
        y_7.next_to(y_0, UP, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        self.bring_to_back(dash_7).play(Write(y_7), ShowCreation(dash_7))
        self.wait()
        dash_7.add_updater(dash_updater(p_7))
        self.play(Write(x_7))
        self.wait()
        self.play(ReplacementTransform(MTex("0").scale(0.5).next_to(y_5, buff = 0).set_opacity(0), result[10], path_arc = -PI/6))
        self.wait()

        func_s, func_x, func_y = p2c(3.13**2, 3.131**2)
        for mob in [graph, p_0, p_5, p_6, p_7]:
            func_s(mob.generate_target().restore())
        for mob in [x_0, x_5, x_6, x_7]:
            func_x(mob.generate_target().restore())
        for mob in [y_0, y_5, y_6, y_7]:
            func_y(mob.generate_target().restore())
        self.add(big_shade, result[:11], func).play(*[MoveToTarget(mob) for mob in [graph, x_0, x_5, x_6, x_7, y_0, y_5, y_6, y_7, p_0, p_5, p_6, p_7]], run_time = 2)
        self.remove(x_6, y_6, dash_6).wait()

        y_8 = MTex(r"3.1301").scale(0.5).next_to(p_y(3.1301**2), LEFT, buff = 0.1).save_state().next_to(y_5, UP, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        x_8 = MTex("9.79752601").scale(0.6).rotate(PI/2).next_to(p_x(3.1301**2), DOWN, buff = 0.1).save_state()
        p_8 = Point(position(3.1301**2)).save_state()
        func_s(p_8)
        func_x(x_8)
        func_y(y_8)
        dash_8 = VMobject(stroke_width = 2).add_updater(dash_updater(p_8)).clear_updaters().reverse_points()
        y_8.next_to(y_5, UP, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        self.bring_to_back(dash_8).play(Write(y_8), ShowCreation(dash_8))
        self.play(Write(x_8))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [x_8, y_8, dash_8]])
        self.wait()

        y_8 = MTex(r"3.1302").scale(0.5).next_to(p_y(3.1302**2), LEFT, buff = 0.1).save_state()
        x_8 = MTex("9.79815204").scale(0.6).rotate(PI/2).next_to(p_x(3.1302**2), DOWN, buff = 0.1).save_state()
        p_8 = Point(position(3.1302**2)).save_state()
        func_s(p_8)
        func_x(x_8)
        func_y(y_8)
        dash_8 = VMobject(stroke_width = 2).add_updater(dash_updater(p_8)).clear_updaters().reverse_points()
        self.bring_to_back(dash_8).play(Write(y_8), ShowCreation(dash_8))
        self.play(Write(x_8))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [x_8, y_8, dash_8]])
        self.wait()
        
        y_8 = MTex(r"3.1303").scale(0.5).next_to(p_y(3.1303**2), LEFT, buff = 0.1).save_state()
        x_8 = MTex("9.79877809").scale(0.6).rotate(PI/2).next_to(p_x(3.1303**2), DOWN, buff = 0.1).save_state()
        p_8 = Point(position(3.1303**2)).save_state()
        func_s(p_8)
        func_x(x_8)
        func_y(y_8)
        dash_8 = VMobject(stroke_width = 2).add_updater(dash_updater(p_8)).clear_updaters().reverse_points()
        self.bring_to_back(dash_8).play(Write(y_8), ShowCreation(dash_8))
        self.play(Write(x_8))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [x_8, y_8, dash_8]])
        self.wait()

        y_8 = MTex(r"3.1304").scale(0.5).next_to(p_y(3.1304**2), LEFT, buff = 0.1).save_state().next_to(y_0, DOWN, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        x_8 = MTex("9.79940416").scale(0.6).rotate(PI/2).next_to(p_x(3.1304**2), DOWN, buff = 0.1).save_state()
        p_8 = Point(position(3.1304**2)).save_state()
        func_s(p_8)
        func_x(x_8)
        func_y(y_8)
        dash_8 = VMobject(stroke_width = 2).add_updater(dash_updater(p_8)).clear_updaters().reverse_points()
        self.play(Write(y_8))
        self.wait()
        self.bring_to_back(dash_8).play(ShowCreation(dash_8))
        self.play(Write(x_8))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [x_8, y_8, dash_8]])
        self.wait()

        y_8 = MTex(r"3.1305").scale(0.5).next_to(p_y(3.1304**2), LEFT, buff = 0.1).save_state().next_to(y_0, UP, coor_mask = np.array([0, 1, 0]), buff = 0.05)
        x_8 = MTex("9.80003025").scale(0.6).rotate(PI/2).next_to(p_x(3.1304**2), DOWN, buff = 0.1).save_state()
        p_8 = Point(position(3.1304**2)).save_state()
        func_s(p_8)
        func_x(x_8)
        func_y(y_8)
        dash_8 = VMobject(stroke_width = 2).add_updater(dash_updater(p_8)).clear_updaters().reverse_points()
        self.bring_to_back(dash_8).play(Write(y_8), ShowCreation(dash_8))
        self.play(Write(x_8))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [x_8, y_8, dash_8]])
        self.wait()
      
#################################################################### 

def get_series(n: int, min: int = 0):
    series = []
    temp = n
    i = 0
    while temp > 0 or i <= min:
        series.append(temp % 10)
        temp = temp // 10
        i += 1
    return series[::-1]

def get_terms(series: list, h_space: float, dot: bool = False):
    group = VGroup(*[MTex(str(series[i])).shift(h_space*i*RIGHT) for i in range(len(series))])
    if dot:
        group.insert_submobject(1, MTex(r".").move_to(group[0].get_corner(DR) + 0.08*RIGHT))
    return group

class LongMultiplication(VGroup):
    def __init__(self, input: int, h_space = 0.4, v_space = 0.6, min = 0):
        
        self.input_1, self.input_2 = input, input
        self.series_1, self.series_2 = get_series(self.input_1), get_series(self.input_2)
        self.length_1, self.length_2 = len(self.series_1), len(self.series_2)
        self.h_space,self.v_space  = h_space, v_space
        self.terms_1, self.terms_2 = get_terms(self.series_1, self.h_space, True).next_to(v_space*UP, UL), get_terms(self.series_2, self.h_space, True).next_to(ORIGIN, UL)
        super().__init__(self.terms_1, self.terms_2)
        self.mul = MTex(r"\times").next_to(self.h_space*self.length_1*LEFT, UL)
        self.upper_line = Line(self.h_space*(self.length_1+1.5)*LEFT, self.h_space*0.1*RIGHT)
        self.add(self.mul, self.upper_line)

        self.layers = []
        for i in range(self.length_2):
            series_i = get_series(self.input_1*self.series_2[i], min)
            terms_i = get_terms(series_i, self.h_space).next_to((1.5+i)*v_space*DOWN + i*h_space*RIGHT, UL)
            self.add(terms_i), self.layers.append(terms_i)
        self.lower_line = Line(self.h_space*(self.length_1+1.5)*LEFT + self.v_space*(self.length_2+0.5)*DOWN, self.h_space*(self.length_2-1)*RIGHT + self.v_space*(self.length_2+0.5)*DOWN)
        self.add(self.lower_line)
        self.series_3 = get_series(self.input_1*self.input_2)
        self.result = get_terms(self.series_3, self.h_space, True).next_to(self.h_space*(self.length_2-1)*RIGHT + self.v_space*(self.length_2+2)*DOWN, UL)
        self.add(self.result)

class Video_3(FrameScene):
    def construct(self):
        h_space = 0.4
        v_space = 0.6*UP
        mul_1 = LongMultiplication(31301, min = 4).center().shift(3*LEFT).shift(v_space)
        mul_2 = LongMultiplication(31302, min = 4).center().shift(3*RIGHT).shift(v_space)
        mul_0 = LongMultiplication(3130, min = 3).center().shift(1.5*v_space)
        self.add(mul_1, mul_2).wait()
        for mob in mul_1.generate_target(), mul_2.generate_target(), mul_0:
            for i in [0, 1]:
                mob[i][:5].set_color(GREEN)
            for i in [4, 5, 6, 7]:
                mob[i][:4].set_color(TEAL)
        mul_0[9].set_color(TEAL)
        self.play(MoveToTarget(mul_1), MoveToTarget(mul_2))
        self.wait()
        self.play(mul_1.animate.shift(1.5*LEFT), mul_2.animate.shift(1.5*RIGHT), FadeIn(mul_0, 0.5*DOWN))
        self.wait()

        main_1, main_2 = mul_0[9].copy(), mul_0[9].copy()
        all_1, all_2 = mul_1[10], mul_2[10]
        main_1.shift(all_1[0].get_center() - main_1[0].get_center()), main_2.shift(all_2[0].get_center() - main_2[0].get_center())
        s_1, s_2 = get_series(31301**2-31300**2, 8), get_series(31302**2-31300**2, 8)
        add_1, add_2 = get_terms(s_1, h_space, True).set_color(PURPLE_B), get_terms(s_2, h_space, True).set_color(PURPLE_B)
        add_1.shift(all_1[0].get_center() - add_1[0].get_center() - v_space), add_2.shift(all_2[0].get_center() - add_2[0].get_center() - v_space)
        mul_1.remove(all_1), mul_2.remove(all_2)
        for mob in mul_1.generate_target(), mul_2.generate_target():
            for i in [0, 1]:
                mob[i][5].set_color(BLUE)
            for i in [4, 5, 6, 7]:
                mob[i][4].set_color(PURPLE_B)
            mob[8].set_color(PURPLE_B)
        self.play(MoveToTarget(mul_1), MoveToTarget(mul_2), FadeTransform(all_1, main_1, stretch = False), FadeTransform(all_2, main_2, stretch = False), FadeTransform(all_1.copy(), add_1), FadeTransform(all_2.copy(), add_2), mul_0[8:].animate.shift(-v_space))
        self.wait()

        camera = self.camera.frame
        self.play(camera.animate.shift(5*RIGHT), *[mob.animate.shift(RIGHT) for mob in [mul_2, main_2, add_2]], *[mob.animating(remover = True).shift(LEFT) for mob in [mul_1, main_1, add_1]], run_time = 2)
        self.wait()

        formula = VGroup(Dot(radius = 0.2, color = PURPLE_B), MTex("=")[0], MTex("2")[0], Dot(radius = 0.2, color = GREEN), MTex(r"\times")[0], Dot(radius = 0.2, color = BLUE), MTex("+")[0], Dot(radius = 0.2, color = BLUE), MTex(r"1^2")[1]).arrange(buff = 0.15).shift(9*RIGHT + 1.5*UP)
        formula[-1].next_to(formula[-2].get_corner(UR), RIGHT, buff = 0.1)
        for mob in [mul_2.generate_target()]:
            for i in [4, 5, 6, 7]:
                mob[i][:4].set_opacity(0.5)
        self.play(MoveToTarget(mul_2), Write(formula), main_2.animate.set_opacity(0.5))
        self.wait()
        
class Video_4(FrameScene):
    def construct(self):
        v_stack = 0.6*DOWN
        h_stack = 0.4*RIGHT
        goal = MTex(r"\sqrt{9.8}").shift(5*LEFT + 3*UP)
        base = goal[2].get_center()
        def grid(h, v):
            return base + h*h_stack + v*v_stack
        def align(mob, h, v):
            mob.shift(grid(h, v) - mob[0].get_center())
            return mob
        square = align(get_terms(get_series(98000000000), 0.4, True).set_color(ORANGE), 0, 0)
        sqrt_symbol = goal[:2]
        formula = VGroup(Dot(radius = 0.2, color = PURPLE_B), MTex("=")[0], MTex("2")[0], Dot(radius = 0.2, color = GREEN), MTex(r"\times")[0], Dot(radius = 0.2, color = BLUE), MTex("+")[0], Dot(radius = 0.2, color = BLUE), MTex(r"1^2")[1]).arrange(buff = 0.15).shift(4*RIGHT + 1.5*UP)
        formula[-1].next_to(formula[-2].get_corner(UR), RIGHT, buff = 0.1)
        formula_2 = VGroup(Dot(radius = 0.2, color = YELLOW), MTex("=")[0], Dot(radius = 0.2, color = ORANGE), MTex("-")[0], Dot(radius = 0.2, color = GREEN), MTex(r"1^2")[1]).arrange(buff = 0.15)
        formula_2.shift(formula[0].get_center() - formula_2[0].get_center() + DOWN)
        formula_2[-1].next_to(formula_2[-2].get_corner(UR), RIGHT, buff = 0.1)
        self.add(sqrt_symbol, square[:3], formula).wait()

        root = align(get_terms(get_series(313049), 0.8, True), 0, -1)
        purples, lines, yellows = [], [], []
        purple_0 = align(get_terms(get_series(9), 0.4), 0, 1).set_color(PURPLE_B)
        line_0 = Line(grid(-0.75, 1.5), grid(1.75, 1.5))
        yellow_0 = align(get_terms(get_series(80, 2), 0.4), 0, 2).set_color(YELLOW)
        purples.append(purple_0), lines.append(line_0), yellows.append(yellow_0)
        self.play(Write(root[:2].set_color(BLUE)))
        self.play(IndicateAround(formula), Write(purple_0))
        self.play(ShowCreation(line_0), Write(yellow_0[:2]), FadeIn(formula_2, 0.5*UP))
        self.wait()

        self.play(goal[1].animate.set_width(3*0.4, stretch = True, about_point = goal[1].get_corner(LEFT)), Write(square[3]), Write(yellow_0[2].set_color(interpolate_color(YELLOW, WHITE, 0.8))), *[mob.animate.set_color(interpolate_color(mob.get_color(), WHITE, 0.8)) for mob in [purple_0, *yellow_0[:2]]], root[:2].animate.set_color(GREEN))
        self.wait()
        try_1, p_1 = MTex(r"1", color = BLUE).move_to(root[2]), align(get_terms(get_series(61), 0.4), 1, 3).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"2", color = BLUE).move_to(root[2]), align(get_terms(get_series(124), 0.4), 0, 3).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(p_1.animate.set_color(RED))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        purple_1 = align(get_terms(get_series(61), 0.4), 1, 3).set_color(PURPLE_B)
        line_1 = Line(grid(0.25, 3.5), grid(2.75, 3.5))
        yellow_1 = align(get_terms(get_series(1900, 2), 0.4), 1, 4).set_color(YELLOW)
        purples.append(purple_1), lines.append(line_1), yellows.append(yellow_1)
        self.play(Write(root[2].set_color(BLUE)))
        self.play(IndicateAround(formula), Write(purple_1))
        self.play(ShowCreation(line_1), Write(yellow_1[:2]), IndicateAround(formula_2))
        self.wait()

        self.play(goal[1].animate.set_width(5*0.4, stretch = True, about_point = goal[1].get_corner(LEFT)), Write(square[4:6]), Write(yellow_1[2:].set_color(interpolate_color(YELLOW, WHITE, 0.8))), *[mob.animate.set_color(interpolate_color(mob.get_color(), WHITE, 0.8)) for mob in [purple_1, *yellow_1[:2]]], root[2].animate.set_color(GREEN))
        self.wait()
        try_1, p_1 = MTex(r"1", color = BLUE).move_to(root[3]), align(get_terms(get_series(621), 0.4), 2, 5).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"2", color = BLUE).move_to(root[3]), align(get_terms(get_series(1244), 0.4), 1, 5).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"3", color = BLUE).move_to(root[3]), align(get_terms(get_series(1869), 0.4), 1, 5).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"4", color = BLUE).move_to(root[3]), align(get_terms(get_series(2496), 0.4), 1, 5).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(p_1.animate.set_color(RED))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        purple_2 = align(get_terms(get_series(1869), 0.4), 1, 5).set_color(PURPLE_B)
        line_2 = Line(grid(0.25, 5.5), grid(4.75, 5.5))
        yellow_2 = align(get_terms(get_series(310000, 2), 0.4), 3, 6).set_color(YELLOW)
        purples.append(purple_2), lines.append(line_2), yellows.append(yellow_2)
        self.play(Write(root[3].set_color(BLUE)))
        self.play(IndicateAround(formula), Write(purple_2))
        self.play(ShowCreation(line_2), Write(yellow_2[:2]), IndicateAround(formula_2))
        self.wait()

        self.play(goal[1].animate.set_width(7*0.4, stretch = True, about_point = goal[1].get_corner(LEFT)), Write(square[6:8]), Write(yellow_2[2:4].set_color(interpolate_color(YELLOW, WHITE, 0.8))), *[mob.animate.set_color(interpolate_color(mob.get_color(), WHITE, 0.8)) for mob in [purple_2, *yellow_2[:2]]], root[3].animate.set_color(GREEN))
        self.wait()
        try_1, p_1 = MTex(r"1", color = BLUE).move_to(root[4]), align(get_terms(get_series(6261), 0.4), 3, 7).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(p_1.animate.set_color(RED))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        self.play(Write(root[4].set_color(BLUE)))
        self.wait()

        self.play(goal[1].animate.set_width(9*0.4, stretch = True, about_point = goal[1].get_corner(LEFT)), Write(square[8:10]), Write(yellow_2[4:].set_color(interpolate_color(YELLOW, WHITE, 0.8))), root[4].animate.set_color(GREEN))
        self.wait()
        try_1, p_1 = MTex(r"1", color = BLUE).move_to(root[5]), align(get_terms(get_series(62601), 0.4), 4, 7).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"2", color = BLUE).move_to(root[5]), align(get_terms(get_series(125204), 0.4), 3, 7).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"3", color = BLUE).move_to(root[5]), align(get_terms(get_series(187809), 0.4), 3, 7).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"4", color = BLUE).move_to(root[5]), align(get_terms(get_series(250416), 0.4), 3, 7).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        try_1, p_1 = MTex(r"5", color = BLUE).move_to(root[5]), align(get_terms(get_series(313025), 0.4), 3, 7).set_color(PURPLE_B)
        self.play(FadeIn(try_1), FadeIn(p_1), IndicateAround(formula))
        self.play(p_1.animate.set_color(RED))
        self.play(FadeOut(try_1), FadeOut(p_1))
        self.wait()
        purple_3 = align(get_terms(get_series(250416), 0.4), 3, 7).set_color(PURPLE_B)
        line_3 = Line(grid(2.25, 7.5), grid(8.75, 7.5))
        yellow_3 = align(get_terms(get_series(5958400, 2), 0.4), 4, 8).set_color(YELLOW)
        purples.append(purple_3), lines.append(line_3), yellows.append(yellow_3)
        self.play(Write(root[5].set_color(BLUE)))
        self.play(IndicateAround(formula), Write(purple_3))
        self.play(ShowCreation(line_3), Write(yellow_3[:5]), IndicateAround(formula_2))
        self.wait()

        self.play(goal[1].animate.set_width(11*0.4, stretch = True, about_point = goal[1].get_corner(LEFT)), Write(square[10:12]), Write(yellow_3[5:].set_color(interpolate_color(YELLOW, WHITE, 0.8))), *[mob.animate.set_color(interpolate_color(mob.get_color(), WHITE, 0.8)) for mob in [purple_3, *yellow_3[:5]]], root[5].animate.set_color(GREEN))
        self.wait()
        purple_4 = align(get_terms(get_series(5634801), 0.4), 4, 9).set_color(PURPLE_B)
        line_4 = Line(grid(3.25, 9.5), grid(10.75, 9.5))
        yellow_4 = align(get_terms(get_series(32359900, 2), 0.4), 5, 10).set_color(YELLOW)
        purples.append(purple_4), lines.append(line_4), yellows.append(yellow_4)
        self.play(Write(root[6].set_color(BLUE)))
        self.play(IndicateAround(formula), Write(purple_4))
        self.play(ShowCreation(line_4), Write(yellow_4[:6]), IndicateAround(formula_2))
        self.wait()

#################################################################### 

class Video_5(FrameScene):
    def construct(self):
        texts = [r"f(x+a)", r"f(a)", r"\frac{f'(a)}{1!}x", r"\frac{f''(a)}{2!}x^2", r"\frac{f^{(3)}(a)}{3!}x^3", r"\frac{f^{(4)}(a)}{4!}x^4", r"\cdots"]
        taylor_0 = MTex(texts[0] + r"=" + r"+".join(texts[1:]), tex_to_color_map = {r"a": GREEN, r"x": BLUE, r"f": YELLOW}, isolate = texts + [r"+", r"="]).scale(0.8).shift(3*UP)
        terms_0, adds_0, equal_0 = [taylor_0.get_part_by_tex(text) for text in texts], taylor_0.get_parts_by_tex(r"+")[1:], taylor_0.get_parts_by_tex(r"=")
        parts_0 = [terms_0[0], equal_0, terms_0[1], adds_0[0], terms_0[2], adds_0[1], terms_0[3], adds_0[2], terms_0[4], adds_0[3], terms_0[5], adds_0[4], terms_0[6]]
        self.play(FadeIn(taylor_0, 0.5*DOWN))
        self.wait()

        substitute = MTex(r"f(x)=\sqrt{x},\ a=9", tex_to_color_map = {(r"a", r"9"): GREEN, r"x": BLUE, (r"f", r"\sqrt{x}"): YELLOW}).scale(0.8).shift(2*UP)
        self.play(Write(substitute))
        self.wait()
        
        texts = [r"\sqrt{x+{9}}", r"3", r"\frac{1}{6}x", r"\frac{1}{216}x^2", r"\frac{1}{3888}x^3", r"\frac{5}{279936}x^4", r"\cdots"]
        taylor_1 = MTex(texts[0] + r"=" + texts[1] + r"+" + texts[2] + r"-" + texts[3] + r"+" + texts[4] + r"-" + texts[5] + r"+" + texts[6], tex_to_color_map = {r"\sqrt{x+{9}}": YELLOW, r"{9}": GREEN, r"x": BLUE, r"+": WHITE}, isolate = texts + [r"+", r"-", r"="]).scale(0.8).shift(1*UP)
        terms_1, adds_1, equal_1 = [taylor_1.get_part_by_tex(text) for text in texts], taylor_1.get_parts_by_tex(re.compile(r"[+-]"))[1:], taylor_1.get_parts_by_tex(r"=")
        parts_1 = [terms_1[0], equal_1, terms_1[1], adds_1[0], terms_1[2], adds_1[1], terms_1[3], adds_1[2], terms_1[4], adds_1[3], terms_1[5], adds_1[4], terms_1[6]]
        for p_1, p_0 in zip(parts_1, parts_0):
            p_1.set_x(p_0.get_x())
        self.play(LaggedStart(*[TransformFromCopy(p_0, p_1, path_arc = PI/4) for p_0, p_1 in zip(parts_0, parts_1)], lag_ratio = 0.2, run_time = 3))
        self.wait()

        substitute_2 = MTex(r"x=0.8", tex_to_color_map = {(r"x", r"0.8"): BLUE}).scale(0.8)
        self.play(Write(substitute_2))
        self.wait()

        texts = [r"\sqrt{9.8}", r"3", r"\frac{0.8}{6}", r"\frac{(0.8)^2}{216}", r"\frac{(0.8)^3}{3888}", r"\frac{5\times(0.8)^4}{279936}", r"\cdots"]
        taylor_2 = MTex(texts[0] + r"=" + texts[1] + r"+" + texts[2] + r"-" + texts[3] + r"+" + texts[4] + r"-" + texts[5] + r"+" + texts[6], tex_to_color_map = {r"\sqrt{9.8}": YELLOW, r"9.8": ORANGE, r"0.8": BLUE}, isolate = texts + [r"+", r"-", r"="]).scale(0.8).shift(1*DOWN)
        terms_2, adds_2, equal_2 = [taylor_2.get_part_by_tex(text) for text in texts], taylor_2.get_parts_by_tex(re.compile(r"[+-]")), taylor_2.get_parts_by_tex(r"=")
        parts_2 = [terms_2[0], equal_2, terms_2[1], adds_2[0], terms_2[2], adds_2[1], terms_2[3], adds_2[2], terms_2[4], adds_2[3], terms_2[5], adds_2[4], terms_2[6]]
        for p_2, p_0 in zip(parts_2, parts_0):
            p_2.set_x(p_0.get_x())
        self.play(LaggedStart(*[TransformFromCopy(p_1, p_2, path_arc = PI/4) for p_1, p_2 in zip(parts_1, parts_2)], lag_ratio = 0.2, run_time = 3))
        self.wait()

        lines = [Line(ORIGIN, (0.5+i*0.2)*DOWN, stroke_width = 2).shift(adds_2[i].get_left() + 0.2*LEFT) for i in range(5)]
        lines[4].shift(0.15*RIGHT)
        texts = "3.00000\cdots", "3.13333\cdots", "3.13037\cdots", "3.13050\cdots", "3.13049\cdots"
        approxs = [MTex(texts[i], color = YELLOW_A).scale(0.5).next_to(lines[i].get_end(), LEFT, buff = 0.1) for i in range(5)]
        self.play(ShowCreation(lines[0]), Write(approxs[0]))
        self.wait()
        self.play(TransformFromCopy(lines[0], lines[1]), TransformFromCopy(approxs[0], approxs[1]))
        self.wait()
        self.play(TransformFromCopy(lines[1], lines[2]), TransformFromCopy(approxs[1], approxs[2]))
        self.wait()
        self.play(TransformFromCopy(lines[2], lines[3]), TransformFromCopy(approxs[2], approxs[3]))
        self.wait()
        self.play(TransformFromCopy(lines[3], lines[4]), TransformFromCopy(approxs[3], approxs[4]))
        self.wait()

        result = MTex(r"\sqrt{9.8}=3.1304951684997\cdots", tex_to_color_map = {r"\sqrt{9.8}": YELLOW, r"9.8": ORANGE, r"3.1304951684997\cdots": YELLOW}).scale(0.8)
        result.shift(taylor_2[6].get_center() - result[6].get_center() + UP)
        for i in range(6):
            result[i].set_x(taylor_2[i].get_x())
        self.play(Write(result), substitute_2.animate.shift((substitute[-2].get_x() - substitute_2[1].get_x())*RIGHT))
        self.wait()

class Video_6(FrameScene):
    def construct(self):
        offset = 6*LEFT + 2*DOWN
        position = lambda t: np.array([t, np.sqrt(t), 0])*0.75 + offset
        p_x = lambda t: np.array([t, 0, 0])*0.75 + offset
        p_y = lambda t: np.array([0, np.sqrt(t), 0])*0.75 + offset
        axes = VGroup(Arrow(0.5*LEFT, 12.5*RIGHT, stroke_width = 3), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3)).shift(offset)
        graph = FunctionGraph(lambda t: np.sqrt(t), [0, 16.5, 0.01], stroke_width = 3).scale(0.75, about_point = ORIGIN).shift(offset)
        func = MTex(r"y=\sqrt{x}", color = YELLOW).next_to(graph.get_corner(UR), UL)
        self.add(graph, axes, func)
        self.wait()

        texts = [r"\sqrt{x+{9}}", r"\approx3", r"+\frac{1}{6}x", r"-\frac{1}{216}x^2", r"+\frac{1}{3888}x^3", r"-\frac{5}{279936}x^4", r"+\cdots"]
        colors = [GREEN, TEAL, BLUE, PURPLE_B, RED]
        taylor = MTex("".join(texts), tex_to_color_map = {r"\sqrt{x+{9}}": YELLOW, r"{9}": GREEN, **{texts[i+1]: colors[i] for i in range(5)}, (r"+", r"-", r"\approx"): WHITE}, isolate = texts).shift(3*UP)
        terms = [taylor.get_part_by_tex(text) for text in texts]
        coefficients = [1]
        for i in range(20):
            coefficients.append(coefficients[i]*(1/2-i))
        line_0 = DashedLine(p_x(9), position(9))
        dot_0 = Dot(position(9), color = YELLOW)
        base_0 = MTex("9").scale(0.5).next_to(p_x(9), DOWN, buff = 0.1)
        line_1 = DashedLine(p_x(9.8), position(9.8))
        dot_1 = Dot(position(9.8), color = BLUE)
        goal_1 = MTex("9.8").scale(0.5).next_to(p_x(9.8), DOWN, buff = 0.1)
        self.bring_to_back(line_0).play(Write(terms[0]), ShowCreation(line_0), ShowCreation(dot_0))
        self.play(Write(base_0))
        self.wait()
        self.bring_to_back(line_1).play(ShowCreation(line_1), ShowCreation(dot_1))
        self.play(Write(goal_1))
        self.wait()

        def taylors(point, order):
            def util(t: float):
                sum = 0
                diff = (t-point)/point
                for i in range(order):
                    sum += coefficients[order - i]
                    sum *= diff
                sum += coefficients[0]
                return sum*np.sqrt(point)
            return util
        curves = [FunctionGraph(taylors(9, i), [0, 16.5, 0.01], color = colors[i], stroke_width = 2).scale(0.75, about_point = ORIGIN).shift(offset) for i in range(5)]
        curve = VMobject(color = WHITE, stroke_width = 4).set_points(curves[0].get_points())
        texts = "3.00000\cdots", "3.13333\cdots", "3.13037\cdots", "3.13050\cdots", "3.13049\cdots"
        colors_a = [GREEN_A, TEAL_A, BLUE_A, PURPLE_A, RED_A]
        approxs = [MTex(texts[i], color = colors_a[i]).scale(0.5).next_to(dot_1, DR, buff = 0.1).shift(0.25*i*DOWN).set_stroke(width = 4, color = BLACK, background = True) for i in range(5)]
        result = MTex(r"3.13049\cdots", color = YELLOW).scale(0.5).next_to(dot_1, UR, buff = 0.1)
        self.add(curve, dot_0, dot_1).play(ShowCreation(curve), Write(terms[1]), Write(approxs[0]))
        self.wait()
        self.bring_to_back(curves[0]).play(curve.animate.set_points(curves[1].get_points()), Write(terms[2]), Write(approxs[1]))
        self.wait()
        self.bring_to_back(curves[1]).play(curve.animate.set_points(curves[2].get_points()), Write(terms[3]), Write(approxs[2]))
        self.wait()
        self.bring_to_back(curves[2]).play(curve.animate.set_points(curves[3].get_points()), Write(terms[4]), Write(approxs[3]))
        self.wait()
        self.bring_to_back(curves[3]).play(curve.animate.set_points(curves[4].get_points()), Write(terms[5]), Write(approxs[4]))
        self.wait()
        self.bring_to_back(curves[4]).play(curve.animating(remover = True).set_stroke(opacity = 0, width = 0), Write(terms[6]), Write(result))
        self.wait()

        texts = "3.00000\cdots", "3.40856\cdots", "3.38074\cdots", "3.08453\cdots", "3.38388\cdots"
        line_2, dot_2, goal_2 = DashedLine(p_x(11.4), position(11.4)), Dot(position(11.4), color = BLUE), MTex("11.4").scale(0.5).next_to(p_x(11.4), DOWN, buff = 0.1)
        approxs_2 = [MTex(texts[i], color = colors_a[i]).scale(0.5).next_to(dot_2, DR, buff = 0.1).shift(0.25*i*DOWN).set_stroke(width = 4, color = BLACK, background = True) for i in range(5)]
        result_2 = MTex(r"3.38399\cdots", color = YELLOW).scale(0.5).next_to(dot_2, UR, buff = 0.1)
        self.play(Transform(line_1, line_2), Transform(dot_1, dot_2), Transform(goal_1, goal_2), Transform(result, result_2), *[Transform(a_1, a_2) for a_1, a_2 in zip(approxs, approxs_2)])
        self.wait()

        alpha = ValueTracker(9)
        def expansion_updater(order):
            def util(mob: VMobject):
                value = alpha.get_value()
                curve = FunctionGraph(taylors(value, order), [0, 16.5, 0.01]).scale(0.75, about_point = ORIGIN).shift(offset)
                mob.set_points(curve.get_points())
            return util
        for i in range(5):
            curves[i].add_updater(expansion_updater(i))
        texts = [r"\sqrt{x+\frac{100}{9}}", r"\approx\frac{10}{3}", r"+\frac{3x}{20}", r"-\frac{27x^2}{8000}", r"+\frac{243x^3}{1600000}", r"-\frac{137781x^4}{256000000000}", r"+\cdots"]
        taylor_2 = MTex("".join(texts), tex_to_color_map = {r"\sqrt{x+\frac{100}{9}}": YELLOW, r"\frac{100}{9}": GREEN, **{texts[i+1]: colors[i] for i in range(5)}, (r"+", r"-", r"\approx"): WHITE}).shift(3*UP)
        line_2, dot_2, base_2 = DashedLine(p_x(100/9), position(100/9)), Dot(position(100/9), color = YELLOW), MTex(r"\frac{100}{9}").scale(0.5).next_to(p_x(100/9), DOWN, buff = 0.1).shift(0.12*LEFT)
        texts = "3.33333\cdots", "3.38437\cdots", "3.38398\cdots", "3.38399\cdots", "3.38399\cdots"
        approxs_2 = [MTex(texts[i], color = colors_a[i]).scale(0.5).next_to(dot_1, DR, buff = 0.1).shift(0.25*i*DOWN).set_stroke(width = 4, color = BLACK, background = True) for i in range(5)]
        self.play(FadeTransform(taylor, taylor_2), alpha.animate.set_value(100/9), Transform(line_0, line_2), Transform(dot_0, dot_2),  Transform(base_0, base_2), goal_1.animate.shift(0.12*RIGHT), *[Transform(a_1, a_2) for a_1, a_2 in zip(approxs, approxs_2)])
        for mob in curves:
            mob.clear_updaters()
        self.wait()

class Video_7(FrameScene):
    def construct(self):
        offset = 6*LEFT + 0.5*DOWN
        position = lambda t: np.array([t, np.log(t), 0]) + offset
        p_x = lambda t: np.array([t, 0, 0]) + offset
        p_y = lambda t: np.array([0, np.log(t), 0]) + offset
        axes = VGroup(Arrow(0.5*LEFT, 12.5*RIGHT, stroke_width = 3), Arrow(2*DOWN, 3*UP, stroke_width = 3)).shift(offset)
        graph = FunctionGraph(lambda t: np.log(t), [0.2, 12, 0.01], stroke_width = 3).shift(offset)
        func = MTex(r"y=\mbox{ln}{x}", color = YELLOW).next_to(graph.get_corner(UR), DOWN).set_stroke(width = 8, color = BLACK, background = True)
        texts = [r"\mbox{ln}(x+{1})", r"\approx 0", r"+x", r"-\frac{x^2}{2}", r"+\frac{x^3}{3}", r"-\frac{x^4}{4}", r"+\cdots"]
        colors = [GREEN, TEAL, BLUE, PURPLE_B, RED]
        taylor = MTex("".join(texts), tex_to_color_map = {r"\mbox{ln}": YELLOW, r"{1}": GREEN, **{texts[i+1]: colors[i] for i in range(5)}, (r"+", r"-", r"\approx"): WHITE}).shift(3*UP).set_stroke(width = 8, color = BLACK, background = True)
        line_0 = DashedLine(p_x(1), position(1))
        dot_0 = Dot(position(1), color = YELLOW)
        base_0 = MTex("1").scale(0.5).next_to(p_x(1), DOWN, buff = 0.1)
        line_1 = DashedLine(p_x(3), position(3))
        dot_1 = Dot(position(3), color = BLUE)
        goal_1 = MTex("3").scale(0.5).next_to(p_x(3), DOWN, buff = 0.1)
        self.add(line_0, line_1, graph, axes, func, dot_0, base_0, dot_1, goal_1)
        self.wait()

        coefficients = [0] + [(1 if i%2 else -1)/i for i in range(1, 20)]
        def taylors(point, order):
            def util(t: float):
                sum = 0
                diff = t/point - 1
                for i in range(order):
                    sum += coefficients[order - i]
                    sum *= diff
                return sum + np.log(point)
            return util
        curves = [FunctionGraph(taylors(1, i), [0.2, 12, 0.01], color = colors[i], stroke_width = 2).shift(offset) for i in range(5)]
        self.bring_to_back(*curves).play(LaggedStart(*[ShowCreation(curve, start = 0.8/11.8) for curve in curves], lag_ratio = 0.5, run_time = 3, group = VGroup()), Write(taylor))
        self.wait()

        alpha = ValueTracker(1)
        def expansion_updater(order):
            def util(mob: VMobject):
                value = alpha.get_value()
                curve = FunctionGraph(taylors(value, order), [0.2, 12, 0.01]).shift(offset)
                mob.set_points(curve.get_points())
            return util
        def dot_updater(mob: Dot):
            mob.move_to(position(alpha.get_value()))
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.set_points(DashedLine(position(value), p_x(value)).get_all_points())
        for i in range(5):
            curves[i].add_updater(expansion_updater(i))
        dot_0.add_updater(dot_updater)
        line_0.add_updater(line_updater)
        texts = [r"\mbox{ln}(x+{2})", r"\approx\mbox{ln}{2}", r"+\frac{x}{2}", r"-\frac{x^2}{8}", r"+\frac{x^3}{24}", r"-\frac{x^4}{64}", r"+\cdots"]
        taylor_2 = MTex("".join(texts), tex_to_color_map = {r"\mbox{ln}": YELLOW, r"{2}": GREEN, **{texts[i+1]: colors[i] for i in range(5)}, (r"+", r"-", r"\approx"): WHITE}).shift(3*UP).set_stroke(width = 8, color = BLACK, background = True)
        self.play(FadeTransform(taylor, taylor_2), alpha.animate.set_value(2), Transform(base_0, MTex(r"2").scale(0.5).next_to(p_x(2), DOWN, buff = 0.1)), run_time = 2)
        for mob in curves + [dot_0, line_0]:
            mob.clear_updaters()
        self.wait()

        anim = IndicateAround(taylor_2[8:11])
        anim.mobject.set_color(RED)
        self.play(anim)
        self.wait()

class Video_8(FrameScene):
    def construct(self):
        offset = 1*LEFT + 2*DOWN
        position = lambda t: np.array([t, np.log((1+t)/(1-t)), 0]) + offset
        p_x = lambda t: np.array([t, 0, 0]) + offset
        p_y = lambda t: np.array([0, np.log((1+t)/(1-t)), 0]) + offset
        axes = VGroup(Arrow(2.5*LEFT, 4.5*RIGHT, stroke_width = 3), Arrow(0.5*DOWN, 4.5*UP, stroke_width = 3)).shift(offset)
        graph = FunctionGraph(lambda t: np.log((1+t)/(1-t)), [-0.2, 0.88, 0.01], stroke_width = 3).scale(1.5, about_point = ORIGIN).shift(offset)
        func = MTex(r"y=\mbox{ln}\left(\frac{1+x}{1-x}\right)", color = YELLOW).scale(0.8).next_to(graph.get_corner(UR), DR).set_stroke(width = 8, color = BLACK, background = True)
        texts = [r"\mbox{ln}\left(\frac{{1}+{x}}{{1}-{x}}\right)", r"\approx 2x", r"+\frac{2}{3}x^3", r"+\frac{2}{5}x^5", r"+\frac{2}{7}x^7", r"+\frac{2}{9}x^9", r"+\cdots"]
        colors = [GREEN, TEAL, BLUE, PURPLE_B, RED]
        taylor = MTex("".join(texts), tex_to_color_map = {r"\mbox{ln}": YELLOW, r"{1}": GREEN, r"{x}": BLUE, **{texts[i+1]: colors[i] for i in range(5)}, (r"+", r"\approx"): WHITE}).shift(3*UP).set_stroke(width = 8, color = BLACK, background = True)
        line_0 = DashedLine(p_x(0), position(0))
        dot_0 = Dot(position(0), color = YELLOW)
        base_0 = MTex("0").scale(0.5).next_to(p_x(0), DR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        substitute = MTex(r"3=\frac{1+0.5}{1-0.5}", tex_to_color_map = {r"3": ORANGE, r"1": GREEN, r"0.5": BLUE}).scale(0.8).shift(3*LEFT)
        line_1 = DashedLine(p_x(0.5), position(0.5))
        dot_1 = Dot(position(0.5), color = BLUE)
        goal_1 = MTex("0.5").scale(0.5).next_to(p_x(0.5), DOWN, buff = 0.1)
        self.add(line_0, graph, axes, func, dot_0, base_0).wait()
        self.play(Write(substitute))
        self.wait()
        self.bring_to_back(line_1).play(ShowCreation(dot_1), Write(goal_1), ShowCreation(line_1))
        self.wait()

        coefficients = [2/(2*i+1) for i in range(20)]
        def taylors(order):
            def util(t: float):
                sum = 0
                for i in range(order):
                    sum += coefficients[order - i]
                    sum *= t**2
                return sum * t + 2*t
            return util
        curves = [FunctionGraph(taylors(i), [-0.2, 0.88, 0.01], color = colors[i], stroke_width = 2).scale(1.5, about_point = ORIGIN).shift(offset) for i in range(5)]
        texts = "1.00000\cdots", "1.08333\cdots", "1.09583\cdots", "1.09806\cdots", "1.09849\cdots"
        colors_a = [GREEN_A, TEAL_A, BLUE_A, PURPLE_A, RED_A]
        approxs = [MTex(texts[i], color = colors_a[i]).scale(0.5).next_to(dot_1, DR, buff = 0.1).shift((0.25*i-0.1)*DOWN).set_stroke(width = 4, color = BLACK, background = True) for i in range(5)]
        result = MTex(r"1.09861\cdots", color = YELLOW).scale(0.5).next_to(dot_1, UR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        self.bring_to_back(*curves).play(LaggedStart(*[ShowCreation(curve, start = 0.2) for curve in curves], lag_ratio = 0.5, run_time = 3, group = VGroup()), Write(taylor), Write(result), LaggedStart(*[FadeIn(mob, 0.2*DOWN) for mob in approxs], lag_ratio = 0.5, run_time = 2))
        self.wait()
        
#################################################################### 

class Video_9(FrameScene):
    def construct(self):
        def newton(start, order):
            array = [start]
            for i in range(order):
                array.append(array[i]/2+4.9/array[i])
            return array
        array = newton(2, 5)
        offset = 1*LEFT + 3*DOWN
        ratio = 0.5
        axes = VGroup(Arrow(2.5*LEFT, 4.5*RIGHT, stroke_width = 3), Arrow(0.5*DOWN, 6.5*UP, stroke_width = 3)).shift(offset)
        graph = FunctionGraph(lambda t: t**2, [-3.5, 3.5, 0.01], stroke_width = 3).scale(ratio, about_point = ORIGIN).shift(offset)
        func = MTex(r"y=x^2-9.8", color = YELLOW).scale(0.8).next_to(graph.get_corner(UR), UP).set_stroke(width = 8, color = BLACK, background = True)
        offset = 1*LEFT + 3*DOWN + 9.8*ratio*UP
        position = lambda t: np.array([t, t**2 - 9.8, 0])*ratio + offset
        p_x = lambda t: np.array([t, 0, 0])*ratio + offset
        p_y = lambda t: np.array([0, t**2 - 9.8, 0])*ratio + offset
        p_l = lambda t, **kwargs: Line(position(t) + 1*np.array([1, 2*t, 0]), position(t) - 1*np.array([1, 2*t, 0]), **kwargs)
        dot_0 = Dot(position(np.sqrt(9.8)), color = YELLOW)
        goal_0 = MTex(r"\sqrt{9.8}", color = ORANGE).scale(0.5).next_to(p_x(np.sqrt(9.8)), UP, buff = 0.1).shift(0.1*LEFT).set_stroke(width = 4, color = BLACK, background = True)
        self.add(graph, axes, func[:4]).wait()
        self.play(FadeIn(Line(2.5*LEFT, 4.5*RIGHT, color = YELLOW).shift(offset), rate_func = there_and_back, remover = True))
        self.wait()
        self.play(axes[0].animating(run_time = 2).shift(9.8*ratio*UP), Write(func[4:]))
        self.wait()
        self.play(ShowCreation(dot_0), Write(goal_0))
        self.wait()
        texts = "2.00000\cdots", "3.45000\cdots", "3.14528\cdots", "3.13052\cdots", "3.13049\cdots"
        colors_a = [GREEN_A, TEAL_A, BLUE_A, PURPLE_A, RED_A]
        approxs = [MTex(texts[i], color = colors_a[i]).scale(0.8).next_to(UP + 3*RIGHT, DR, buff = 0.1).shift((0.5*i)*DOWN).set_stroke(width = 8, color = BLACK, background = True) for i in range(5)]
        dash_1 = DashedLine(p_x(array[0]), position(array[0]))
        dot_1 = Dot(position(array[0]), color = GREEN)
        goal_1 = MTex("2", color = GREEN).scale(0.5).next_to(p_x(array[0]), UP, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        line_1 = p_l(array[0], color = GREEN)
        self.bring_to_back(dash_1).play(Write(approxs[0]), Write(goal_1), ShowCreation(dash_1))
        self.play(ShowCreation(dot_1))
        self.wait()
        self.add(line_1, dot_0, dot_1, goal_0, goal_1, func).play(ShowCreation(line_1, start = 0.5))
        self.wait()

        dash_2 = DashedLine(p_x(array[1]), position(array[1]))
        dot_2 = Dot(position(array[1]), color = TEAL)
        goal_2 = MTex("3.45", color = TEAL).scale(0.5).next_to(p_x(array[1]), DR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        line_2 = p_l(array[1], color = TEAL)
        self.bring_to_back(dash_2).play(*[FadeOut(mob) for mob in [dash_1, dot_1, goal_1]], Write(approxs[1]), Write(goal_2), ShowCreation(dash_2))
        self.play(ShowCreation(dot_2), FadeOut(line_1))
        self.wait()
        self.add(line_2, dot_0, dot_2, goal_0, goal_2, func).play(ShowCreation(line_2, start = 0.5), goal_0.animate.shift(0.4*LEFT))
        self.wait()
        dash_3 = DashedLine(p_x(array[2]), position(array[2]))
        dot_3 = Dot(position(array[2]), color = BLUE)
        goal_3 = MTex("3.14", color = BLUE).scale(0.5).next_to(p_x(array[2]), DR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        line_3 = p_l(array[2], color = BLUE)
        self.bring_to_back(dash_3).play(*[FadeOut(mob) for mob in [dash_2, dot_2, goal_2]], Write(approxs[2]), Write(goal_3), ShowCreation(dash_3))
        self.play(ShowCreation(dot_3), FadeOut(line_2))
        self.wait()
        self.add(line_3, dot_0, dot_3, goal_0, goal_3, func).play(ShowCreation(line_3, start = 0.5))
        self.wait()

        self.play(*[FadeOut(mob) for mob in [dash_3, dot_3, goal_3, line_3]], Write(approxs[3]), Write(approxs[4]))
        self.wait()
        self.remove(approxs[3], approxs[4]).bring_to_back(dash_3).add(line_3, dot_0, dot_3, goal_0, goal_3, func)
        self.wait()

        dash_4 = DashedLine(p_x(array[3]), position(array[3]))
        dot_4 = Dot(position(array[3]), color = PURPLE_B)
        goal_4 = MTex("3.13", color = PURPLE_B).scale(0.5).next_to(p_x(array[3]), DR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        line_4 = p_l(array[3], color = PURPLE_B)
        self.bring_to_back(dash_4).play(*[FadeOut(mob) for mob in [dash_3, dot_3, goal_3]], Write(approxs[3]), Write(goal_4), ShowCreation(dash_4))
        self.play(ShowCreation(dot_4), FadeOut(line_3))
        self.wait()
        self.add(line_4, dot_0, dot_4, goal_0, goal_4, func).play(ShowCreation(line_4, start = 0.5))
        self.wait()
        dash_5 = DashedLine(p_x(array[4]), position(array[4]))
        dot_5 = Dot(position(array[4]), color = RED)
        goal_5 = MTex("3.13", color = RED).scale(0.5).next_to(p_x(array[4]), DR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        line_5 = p_l(array[4], color = RED)
        self.bring_to_back(dash_5).play(*[FadeOut(mob) for mob in [dash_4, dot_4, goal_4]], Write(approxs[4]), Write(goal_5), ShowCreation(dash_5))
        self.play(ShowCreation(dot_5), FadeOut(line_4))
        self.wait()
        self.add(line_5, dot_0, dot_5, goal_0, goal_5, func).play(ShowCreation(line_5, start = 0.5))
        self.wait()

        self.remove(dash_5, dot_5, goal_5, line_5, *approxs)
        goal_0.next_to(p_x(np.sqrt(9.8)), UP, buff = 0.1).shift(0.1*LEFT)
        dash_a = DashedLine(p_x(array[0]), position(array[0]))
        dot_a = Dot(position(array[0]), color = GREEN)
        goal_a = MTex("a", color = GREEN).scale(0.5).next_to(p_x(array[0]), UP, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        line_a = p_l(array[0], color = GREEN)
        self.bring_to_back(dash_a).play(Write(goal_a), ShowCreation(dash_a))
        self.play(ShowCreation(dot_a))
        self.wait()
        self.add(line_a, dot_0, dot_a, goal_0, goal_a, func).play(ShowCreation(line_a, start = 0.5))
        self.wait()
        goal_b = MTex(r"\frac{a}{2}+\frac{4.9}{a}", color = TEAL).scale(0.5).next_to(p_x(array[1]), DR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        dot_b = Dot(p_x(array[1]), color = TEAL)
        self.play(Write(goal_b), ShowCreation(dot_b))
        self.wait()
        
class Video_10(FrameScene):
    def construct(self):
        def newton(start, order):
            array = [start]
            for i in range(order):
                array.append(array[i]/2+4.9/array[i])
            return array
        array = newton(2, 6)
        offset = 3*LEFT + 3*DOWN
        ratio = 0.75
        axes = VGroup(Arrow(1.5*LEFT, 6.5*RIGHT, stroke_width = 3), Arrow(0.5*DOWN, 6.5*UP, stroke_width = 3)).shift(offset)
        graph = FunctionGraph(lambda t: t/2+4.9/t, [0.6, 8, 0.01], stroke_width = 3).scale(ratio, about_point = ORIGIN).shift(offset)
        func = MTex(r"\frac{x}{2}+\frac{4.9}{x}", color = YELLOW).scale(0.8).next_to(graph.get_end(), UP).set_stroke(width = 8, color = BLACK, background = True)
        self.add(graph, axes, func).wait()

        position = lambda t: np.array([t, t/2+4.9/t, 0])*ratio + offset
        p_x = lambda t: np.array([t, 0, 0])*ratio + offset
        p_y = lambda t: np.array([0, t/2+4.9/t, 0])*ratio + offset
        p_d = lambda t: np.array([t, t, 0])*ratio + offset
        x = FunctionGraph(lambda t: t, [-0.5, 8, 0.01], color = ORANGE, stroke_width = 3).scale(ratio, about_point = ORIGIN).shift(offset)
        dot = Dot(color = ORANGE).shift(position(np.sqrt(9.8)))
        self.play(ShowCreation(x))
        self.play(ShowCreation(dot))
        self.wait()

        texts = "2.00000\cdots", "3.45000\cdots", "3.14528\cdots", "3.13052\cdots", "3.13049\cdots"
        colors_a = [GREEN_A, TEAL_A, BLUE_A, PURPLE_A, RED_A]
        approxs = [MTex(texts[i], color = colors_a[i]).scale(0.8).next_to(1.5*UP + 5.5*LEFT, DR, buff = 0.1).shift((0.5*i)*DOWN).set_stroke(width = 8, color = BLACK, background = True) for i in range(5)]
        dx_1 = DashedLine(p_x(array[0]), position(array[0]), color = GREEN)
        dot_1 = Dot(position(array[0]), color = GREEN)
        dy_1 = DashedLine(position(array[0]), p_d(array[1]), color = GREEN)
        self.bring_to_back(dx_1).play(Write(approxs[0]), ShowCreation(dx_1))
        self.play(ShowCreation(dot_1))
        self.wait()
        self.bring_to_back(dy_1).play(ShowCreation(dy_1, start = 0.5))
        self.wait()

        dx_2 = DashedLine(p_d(array[1]), position(array[1]), color = TEAL)
        dot_2 = Dot(position(array[1]), color = TEAL)
        dy_2 = DashedLine(position(array[1]), p_d(array[2]), color = TEAL)
        self.bring_to_back(dx_2).play(Write(approxs[1]), ShowCreation(dx_2))
        self.play(ShowCreation(dot_2))
        self.wait()
        self.bring_to_back(graph, dy_2).play(ShowCreation(dy_2, start = 0.5))
        self.wait()
        dx_3 = DashedLine(p_d(array[2]), position(array[2]), color = BLUE)
        dot_3 = Dot(position(array[2]), color = BLUE)
        dy_3 = DashedLine(position(array[2]), p_d(array[3]), color = BLUE)
        self.bring_to_back(dx_3).play(Write(approxs[2]), ShowCreation(dx_3))
        self.play(ShowCreation(dot_3))
        self.wait()
        self.bring_to_back(dy_3).play(ShowCreation(dy_3, start = 0.5))
        self.wait()
        dx_4 = DashedLine(p_d(array[3]), position(array[3]), color = PURPLE_B)
        dot_4 = Dot(position(array[3]), color = PURPLE_B)
        dy_4 = DashedLine(position(array[3]), p_d(array[4]), color = PURPLE_B)
        self.bring_to_back(dx_4).play(Write(approxs[3]), ShowCreation(dx_4))
        self.play(ShowCreation(dot_4))
        self.wait()
        self.bring_to_back(dy_4).play(ShowCreation(dy_4, start = 0.5))
        self.wait()
        dx_5 = DashedLine(p_d(array[4]), position(array[4]), color = RED)
        dot_5 = Dot(position(array[4]), color = RED)
        dy_5 = DashedLine(position(array[4]), p_d(array[5]), color = RED)
        self.bring_to_back(dx_5).play(Write(approxs[4]), ShowCreation(dx_5))
        self.play(ShowCreation(dot_5))
        self.wait()
        self.bring_to_back(dy_5).play(ShowCreation(dy_5, start = 0.5))
        self.wait()

class Video_11(FrameScene):
    def construct(self):
        camera = self.camera.frame
        camera.shift(3*LEFT)
        def original(t: float):
            return np.exp(t)-t**2-2
        def derivative(t: float):
            return np.exp(t)-2*t
        def newton(start, order):
            array = [start]
            for i in range(order):
                array.append(array[i] - original(array[i])/derivative(array[i]))
            return array
        array = newton(1, 5)
        texts = "1.00000\cdots", "1.39221\cdots", "1.32323\cdots", "1.31908\cdots", "1.31907\cdots"
        colors_a = [GREEN_A, TEAL_A, BLUE_A, PURPLE_A, RED_A]
        approxs = [MTex(texts[i], color = colors_a[i]).scale(0.8).next_to(1.5*UP, DOWN, buff = 0.1).shift((0.5*i)*DOWN).set_stroke(width = 8, color = BLACK, background = True) for i in range(5)]
        offset_l = 5*LEFT + 0.5*DOWN # 2*LEFT + 0.5*DOWN
        ratio_l = 1.5
        axes_l = VGroup(Arrow(1.5*LEFT, 4*RIGHT, stroke_width = 3), Arrow(3*DOWN, 4*UP, stroke_width = 3)).shift(offset_l)
        graph_l = FunctionGraph(original, [-0.5, 2.2, 0.01], stroke_width = 3).scale(ratio_l, about_point = ORIGIN).shift(offset_l)
        func_l = MTex(r"y=e^x-x^2-2", color = YELLOW).scale(0.8).next_to(graph_l.get_corner(UR), UL).shift(0.5*RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        position_l = lambda t: np.array([t, original(t), 0])*ratio_l + offset_l
        p_x_l = lambda t: np.array([t, 0, 0])*ratio_l + offset_l
        p_y_l = lambda t: np.array([0, original(t), 0])*ratio_l + offset_l
        p_l_l = lambda t, **kwargs: Line(position_l(t) + 1*np.array([1, derivative(t), 0]), position_l(t) - 1*np.array([1, derivative(t), 0]), **kwargs)
        self.add(graph_l, axes_l, func_l).wait()

        offset_r = 2.5*RIGHT + 0.5*DOWN
        ratio_r = 1.5
        axes_r = VGroup(Arrow(1.5*LEFT, 4*RIGHT, stroke_width = 3), Arrow(3*DOWN, 4*UP, stroke_width = 3)).shift(offset_r)
        graph_r = FunctionGraph(lambda t: t - original(t)/derivative(t), [-0.6, 1.7, 0.01], stroke_width = 3).scale(ratio_r, about_point = ORIGIN).shift(offset_r)
        func_r = MTex(r"y=x-\frac{e^x-x^2-2}{e^x-2x}", color = YELLOW).scale(0.8).next_to(graph_r.get_corner(UR), UP).set_stroke(width = 8, color = BLACK, background = True)
        x_r = FunctionGraph(lambda t: t, [-0.6, 1.6, 0.01], color = ORANGE, stroke_width = 3).scale(ratio_r, about_point = ORIGIN).shift(offset_r)
        position_r = lambda t: np.array([t, t - original(t)/derivative(t), 0])*ratio_r + offset_r
        p_x_r = lambda t: np.array([t, 0, 0])*ratio_r + offset_r
        p_y_r = lambda t: np.array([0, t - original(t)/derivative(t), 0])*ratio_r + offset_r
        p_d_r = lambda t: np.array([t, t, 0])*ratio_r + offset_r
        
        dash_0_l = DashedLine(p_x_l(array[0]), position_l(array[0]))
        dot_0_l = Dot(position_l(array[0]), color = GREEN)
        goal_a = MTex("a", color = GREEN).scale(0.5).next_to(p_x_l(array[0]), UP, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        line_0_l = p_l_l(array[0], color = GREEN)
        dx_0_r = DashedLine(p_x_r(array[0]), position_r(array[0]), color = GREEN)
        dot_0_r = Dot(position_r(array[0]), color = GREEN)
        dy_0_r = DashedLine(position_r(array[0]), p_d_r(array[1]), color = GREEN)
        self.bring_to_back(dash_0_l).play(Write(goal_a), ShowCreation(dash_0_l), Write(approxs[0]))
        self.play(ShowCreation(dot_0_l))
        self.wait()
        self.add(line_0_l, dot_0_l, goal_a).play(ShowCreation(line_0_l, start = 0.5))
        self.wait()
        goal_b = MTex(r"a-\frac{e^a-a^2-2}{e^a-2a}", color = TEAL).scale(0.5).next_to(p_x_l(array[1]), DR, buff = 0.1).set_stroke(width = 4, color = BLACK, background = True)
        dot_b = Dot(p_x_l(array[1]), color = TEAL)
        self.play(Write(goal_b), ShowCreation(dot_b), Write(approxs[1]))
        self.wait()

        self.play(camera.animate.shift(3*RIGHT), *[OverFadeIn(mob) for mob in [dx_0_r, dy_0_r, graph_r, x_r, axes_r, func_r, dot_0_r]], run_time = 2)
        self.wait()
        self.play(FadeOut(goal_a), FadeOut(goal_b))
        self.wait()

        dash_1_l = DashedLine(p_x_l(array[1]), position_l(array[1]))
        dot_1_l = Dot(position_l(array[1]), color = TEAL)
        line_1_l = p_l_l(array[1], color = TEAL)
        dx_1_r = DashedLine(p_d_r(array[1]), position_r(array[1]), color = TEAL)
        dot_1_r = Dot(position_r(array[1]), color = TEAL)
        dy_1_r = DashedLine(position_r(array[1]), p_d_r(array[2]), color = TEAL)
        self.bring_to_back(dash_1_l).play(*[FadeOut(mob) for mob in [dash_0_l, dot_0_l, dot_b]], ShowCreation(dash_1_l), ShowCreation(dx_1_r))
        self.play(ShowCreation(dot_1_r), ShowCreation(dot_1_l), FadeOut(line_0_l))
        self.wait()
        self.bring_to_back(dx_0_r, dy_0_r, graph_r, dy_1_r).add(line_1_l, dot_1_l).play(ShowCreation(line_1_l, start = 0.5), ShowCreation(dy_1_r, start = 0.5))
        self.wait()
        dash_2_l = DashedLine(p_x_l(array[2]), position_l(array[2]))
        dot_2_l = Dot(position_l(array[2]), color = BLUE)
        line_2_l = p_l_l(array[2], color = BLUE)
        dx_2_r = DashedLine(p_d_r(array[2]), position_r(array[2]), color = BLUE)
        dot_2_r = Dot(position_r(array[2]), color = BLUE)
        dy_2_r = DashedLine(position_r(array[2]), p_d_r(array[3]), color = BLUE)
        self.bring_to_back(dash_2_l).play(*[FadeOut(mob) for mob in [dash_1_l, dot_1_l]], Write(approxs[2]), ShowCreation(dash_2_l), ShowCreation(dx_2_r))
        self.play(ShowCreation(dot_2_r), ShowCreation(dot_2_l), FadeOut(line_1_l))
        self.wait()
        self.bring_to_back(dx_0_r, dy_0_r, graph_r, dy_2_r).add(line_2_l, dot_2_l).play(ShowCreation(line_2_l, start = 0.5), ShowCreation(dy_2_r, start = 0.5))
        self.wait()
        dash_3_l = DashedLine(p_x_l(array[3]), position_l(array[3]))
        dot_3_l = Dot(position_l(array[3]), color = PURPLE_B)
        line_3_l = p_l_l(array[3], color = PURPLE_B)
        dx_3_r = DashedLine(p_d_r(array[3]), position_r(array[3]), color = PURPLE_B)
        dot_3_r = Dot(position_r(array[3]), color = PURPLE_B)
        dy_3_r = DashedLine(position_r(array[3]), p_d_r(array[4]), color = PURPLE_B)
        self.bring_to_back(dash_3_l).play(*[FadeOut(mob) for mob in [dash_2_l, dot_2_l]], Write(approxs[3]), ShowCreation(dash_3_l), ShowCreation(dx_3_r))
        self.play(ShowCreation(dot_3_r), ShowCreation(dot_3_l), FadeOut(line_2_l))
        self.wait()
        self.bring_to_back(dx_0_r, dy_0_r, graph_r, dy_3_r).add(line_3_l, dot_3_l).play(ShowCreation(line_3_l, start = 0.5), ShowCreation(dy_3_r, start = 0.5))
        self.wait()
        dash_4_l = DashedLine(p_x_l(array[4]), position_l(array[4]))
        dot_4_l = Dot(position_l(array[4]), color = RED)
        line_4_l = p_l_l(array[4], color = RED)
        dx_4_r = DashedLine(p_d_r(array[4]), position_r(array[4]), color = RED)
        dot_4_r = Dot(position_r(array[4]), color = RED)
        dy_4_r = DashedLine(position_r(array[4]), p_d_r(array[5]), color = RED)
        self.bring_to_back(dash_4_l).play(*[FadeOut(mob) for mob in [dash_3_l, dot_3_l]], Write(approxs[4]), ShowCreation(dash_4_l), ShowCreation(dx_4_r))
        self.play(ShowCreation(dot_4_r), ShowCreation(dot_4_l), FadeOut(line_3_l))
        self.wait()
        self.bring_to_back(dx_0_r, dy_0_r, graph_r, dy_4_r).add(line_4_l, dot_4_l).play(ShowCreation(line_4_l, start = 0.5), ShowCreation(dy_4_r, start = 0.5))
        self.wait()

#################################################################### 

class Video_12(FrameScene):
    def construct(self):
        ball = Dot(radius = 0.2, color = BLUE).shift(2.5*UP)
        line = Line(2.5*UP, 2.5*DOWN, stroke_width = 2)
        base = line.copy().set_color(GREY)
        tex = MTex(r"1m").next_to(line)
        self.play(ShowCreation(ball))
        self.wait()
        self.bring_to_back(line).play(ShowCreation(line), ball.animate.shift(5*DOWN))
        self.wait()
        self.bring_to_back(base, tex).play(Write(tex))
        self.wait()

        time = MTex(r"t=0.00s").shift(3.5*LEFT)
        times = [MTex(r"t=" + str(i+1) + r"0.00s") for i in range(5)]
        for i in range(5):
            times[i].shift(time[0].get_center() - times[i][0].get_center())
        counter = Value(0)
        for i in range(4):
            counter[i+1].move_to(time[i+2])
        alpha = ValueTracker(0.0)
        def ball_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(2.5*UP + 5*unit(-PI/2 - value))
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(2.5*UP, 2.5*UP + 5*unit(-PI/2 - value))
        ball.add_updater(ball_updater)
        line.add_updater(line_updater)
        line_r = Line(0.2*UP, 0.2*DOWN, color = GREY_E).move_to(2.5*UP + 5*unit(-PI/2 + PI/18) + 0.2*RIGHT)
        line_l = Line(0.2*UP, 0.2*DOWN, color = GREY_E).move_to(2.5*UP + 5*unit(-PI/2 - PI/18) + 0.2*LEFT)
        self.bring_to_back(alpha, line_l, line_r).play(alpha.animating(run_time = 2).set_value(PI/18), base.animate.set_stroke(width = 4), tex.animate.set_color(GREY), Write(time), FadeIn(line_r), FadeIn(line_l))
        def counter_updater(mob: Value):
            frames = self.frames - 240
            mob.set_value(frames / 30)
        counter.add_updater(counter_updater)
        def alpha_updater(mob: ValueTracker):
            frames = self.frames - 240
            mob.set_value(np.cos(frames / 60 * TAU)*PI/18)
        alpha.add_updater(alpha_updater)
        anim_l, anim_r = FadeOut(line_l.copy().set_color(YELLOW), 0.2*LEFT, run_time = 0.5), FadeOut(line_r.copy().set_color(YELLOW), 0.2*RIGHT, run_time = 0.5)
        self.remove(time[2:6]).add(counter).wait()
        
        for i in range(1, 10):
            tex = MTex(r"t=" + str(i) + r".00")
            tex.shift(time[0].get_center() - tex[0].get_center())
            self.play(FadeOut(tex, 0.5*UP, run_time = 0.5), anim_r if i%2 else anim_l, frames = 30)
        self.remove(time).add(times[0][:3], times[0][7])
        for i in range(4):
            counter[i+1].move_to(times[0][i+3])
        for i in range(10, 20):
            tex = MTex(r"t=" + str(i) + r".00")
            tex.shift(time[0].get_center() - tex[0].get_center())
            self.play(FadeOut(tex, 0.5*UP, run_time = 0.5), anim_r if i%2 else anim_l, frames = 30)
        self.remove(times[0][:3]).add(times[1][:3])
        for i in range(20, 30):
            tex = MTex(r"t=" + str(i) + r".00")
            tex.shift(time[0].get_center() - tex[0].get_center())
            self.play(FadeOut(tex, 0.5*UP, run_time = 0.5), anim_r if i%2 else anim_l, frames = 30)
        self.remove(times[1][:3]).add(times[2][:3])
        for i in range(30, 40):
            tex = MTex(r"t=" + str(i) + r".00")
            tex.shift(time[0].get_center() - tex[0].get_center())
            self.play(FadeOut(tex, 0.5*UP, run_time = 0.5), anim_r if i%2 else anim_l, frames = 30)
        self.remove(times[2][:3]).add(times[3][:3])
        for i in range(40, 50):
            tex = MTex(r"t=" + str(i) + r".00")
            tex.shift(time[0].get_center() - tex[0].get_center())
            self.play(FadeOut(tex, 0.5*UP, run_time = 0.5), anim_r if i%2 else anim_l, frames = 30)
        self.remove(times[3][:3]).add(times[4][:3])
        for i in range(50, 60):
            tex = MTex(r"t=" + str(i) + r".00")
            tex.shift(time[0].get_center() - tex[0].get_center())
            self.play(FadeOut(tex, 0.5*UP, run_time = 0.5), anim_r if i%2 else anim_l, frames = 30)

class Patch_12(FrameScene):
    def construct(self):
        formula = MTex(r"T=2\pi\sqrt{\frac{l}{g}}", tex_to_color_map = {r"T": BLUE, r"l": YELLOW, r"\pi": TEAL, r"g": ORANGE})
        formula.shift(3*RIGHT + 2*UP - formula[1].get_center())
        self.play(Write(formula))
        self.wait()
        values = MTex(r"2s=2\pi\sqrt{\frac{1m}{g}}", tex_to_color_map = {r"2s": BLUE, r"1m": YELLOW, r"\pi": TEAL, r"g": ORANGE})
        values.shift(3*RIGHT + 0.5*UP - values[2].get_center())
        not_1, not_2 = Line(0.1*LEFT + 0.2*UP, 0.1*RIGHT + 0.2*DOWN, color = GREY).move_to(values[0]), Line(0.1*LEFT + 0.2*UP, 0.1*RIGHT + 0.2*DOWN, color = GREY).move_to(values[3])
        self.play(FadeIn(values, 0.5*DOWN))
        self.wait()
        self.play(ShowCreation(not_1), ShowCreation(not_2))
        self.wait()
        self.play(values[1].animate.set_opacity(0.2), values[8].animate.set_opacity(0.2))
        self.wait()
        result = MTex(r"\sqrt{g}=\pi", tex_to_color_map = {r"\pi": TEAL, r"g": ORANGE})
        result.shift(3*RIGHT + DOWN - result[3].get_center())
        self.play(FadeIn(result, 0.5*DOWN))
        self.wait()

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        