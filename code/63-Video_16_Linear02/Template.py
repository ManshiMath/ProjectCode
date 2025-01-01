from __future__ import annotations

from manimlib import *
import numpy as np

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

class Test_1(FrameScene):
    def construct(self):
        arrow_1 = Arrow(LEFT, RIGHT, buff = 0, stroke_width = 10)
        # self.add(arrow_1)
        # for i in range(len(arrow_1.get_points())):
        #     self.add(MTex(str(i)).scale(0.8).shift(arrow_1.get_points()[i]))
        n = 7
        ratio = 0.8
        for i in range(n):
            arrow_i = arrow_1.copy().pointwise_become_partial(arrow_1, 0, i/(n-1)).shift(((n-1)/2-i)*ratio*DOWN)
            mtex_i = MTex(str(i)).next_to(((n-1)/2-i)*ratio*DOWN + LEFT, LEFT)
            self.add(arrow_i, mtex_i)
        # self.play(ShowCreation(arrow_1, run_time = 5))
          
#################################################################### 
  
class Video_1(FrameScene):

    def cheese(self, *mobs):
        orientation = self.camera.frame.get_orientation().as_matrix()
        util = lambda t: np.dot(orientation, t)
        for mob in mobs:
            position = mob.get_center()
            mob.restore().apply_function(util, about_point = position)
        return self
    
    def construct(self):
        axis_x = Line(7.5*LEFT, 7.5*RIGHT)
        axis_y = Line(7.5*DOWN, 7.5*UP)
        ratio = 1.5
        arrows = [Arrow(ORIGIN, (i+0.5)*ratio*RIGHT + (j+0.5)*ratio*DOWN, buff = 0, color = BLUE) for i in range(-int(64/9/ratio+0.5), int(64/9/ratio+0.5)) for j in range(-int(4/ratio+0.5), int(4/ratio+0.5))]
        sorted_arrows = arrows.copy()
        sorted_arrows.sort(key = lambda t: get_norm(t.get_end()), reverse = True)
        self.play(GrowFromCenter(axis_x), GrowFromCenter(axis_y))
        self.wait()
        self.add(*sorted_arrows, axis_x, axis_y).play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], group = Group(), lag_ratio = 0.02, run_time = 3, rate_func = less_smooth))
        self.wait()
        example_arrow = Arrow(ORIGIN, 2.25*RIGHT + -0.75*DOWN, buff = 0, color = BLUE)
        text = MTex(r"\begin{bmatrix}3\\1\end{bmatrix}").next_to(2.25*RIGHT + -0.75*DOWN)
        self.add(example_arrow, axis_x, axis_y).play(*[mob.animate.set_color(interpolate_color(BLACK, BLUE, 1/3)) for mob in sorted_arrows], Write(text))
        self.wait()
        shade = Shade(height = 15, width = 15, fill_color = interpolate_color(BLACK, BLUE, 1/4))
        self.add(shade, axis_x, axis_y).play(FadeIn(shade))
        self.remove(*sorted_arrows, example_arrow, text).wait()
        
        axis_z = Line(3.75*OUT, 3.75*IN)
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/6), quad(RIGHT, PI/2 - PI/20))
        background = Surface(u_range = (-7.5, 7.5), v_range = (-7.5, 7.5), color = BLUE, opacity = 0.5, depth_test = False)
        self.add(background, shade, axis_x, axis_y, axis_z).play(GrowFromCenter(axis_z), shade.animate.set_fill(opacity = 1/2, color = BACK).scale(0.5), *[mob.animate.scale(0.5) for mob in [background, axis_x, axis_y]], camera.animating(rate_func = less_smooth).set_focal_distance(8).shift(1*OUT).set_orientation(Rotation(quadternion)), run_time = 3)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(quad(OUT, DEGREES*dt), mob.quadternion)
            mob.set_orientation(Rotation(mob.quadternion))
        camera.quadternion = quadternion
        camera.add_updater(camera_updater)
        self.wait()
        self.play(shade.animate.shift(1.5*OUT))
        self.wait()

        position_1 = Point(UP + 2*RIGHT)
        position_2 = Point(3*UP + RIGHT)
        BLUE_G = interpolate_color(BLUE, GREY, 0.5)
        GREEN_G = interpolate_color(GREEN, GREY, 0.5)
        TEAL_G = interpolate_color(TEAL, GREY, 0.5)
        text_1 = Songti("是线性空间", color = interpolate_color(BLUE, WHITE, 0.5)).set_stroke(width = 8, color = BLACK, background = True).fix_in_frame().shift(5*LEFT + 1.5*DOWN)
        text_2 = Songti("不是线性空间", color = GREY_A).set_stroke(width = 8, color = BLACK, background = True).fix_in_frame().shift(5*LEFT + 0.5*UP)
        offset = 1.5*OUT
        arrows = VGroup(Polyline(position_1.get_location(), position_1.get_location(), ORIGIN, color = interpolate_color(TEAL, GREY, 0.5), stroke_width = 2), Polyline(position_1.get_location() + offset, position_1.get_location() + offset, ORIGIN, color = interpolate_color(TEAL_G, GREY, 0.5), stroke_width = 2), 
                        Arrow(ORIGIN, position_1.get_location(), color = BLUE, buff = 0), Arrow(ORIGIN, position_1.get_location() + offset, color = BLUE_G, buff = 0), 
                        Arrow(ORIGIN, position_2.get_location(), color = GREEN, buff = 0), Arrow(ORIGIN, position_2.get_location() + offset, color = GREEN_G, buff = 0), 
                        Arrow(ORIGIN, position_1.get_location() + position_2.get_location(), color = TEAL, buff = 0), Arrow(ORIGIN, position_1.get_location() + position_2.get_location() + 2*offset, color = TEAL_G, buff = 0))
        self.play(GrowArrow(arrows[2]), GrowArrow(arrows[3]))
        self.add(*arrows).play(Write(text_1), Write(text_2), arrows[0].animate.set_points_as_corners([position_1.get_location(), position_1.get_location() + position_2.get_location(), position_2.get_location()]), arrows[1].animate.set_points_as_corners([position_1.get_location() + offset, position_1.get_location() + position_2.get_location() + 2*offset, position_2.get_location() + offset]), GrowArrow(arrows[4]), GrowArrow(arrows[5]), TransformFromCopy(arrows[2], arrows[6]), TransformFromCopy(arrows[3], arrows[7]))
        self.wait()
        def arrows_updater(mob: VGroup):
            point_1 = position_1.get_location()
            point_2 = position_2.get_location()
            mob[0].set_points_as_corners([point_1, point_1 + point_2, point_2])
            mob[1].set_points_as_corners([point_1 + offset, point_1 + point_2 + 2*offset, point_2 + offset])
            mob[2].set_points(Arrow(ORIGIN, point_1, buff = 0).get_points())
            mob[3].set_points(Arrow(ORIGIN, point_1 + offset, buff = 0).get_points())
            mob[4].set_points(Arrow(ORIGIN, point_2, buff = 0).get_points())
            mob[5].set_points(Arrow(ORIGIN, point_2 + offset, buff = 0).get_points())
            mob[6].set_points(Arrow(ORIGIN, point_1 + point_2, buff = 0).get_points())
            mob[7].set_points(Arrow(ORIGIN, point_1 + point_2 + 2*offset, buff = 0).get_points())
        self.add(arrows.add_updater(arrows_updater)).play(position_2.animate.set_location(1.5*UP + 2.5*LEFT))
        self.wait()
        self.play(position_1.animate.set_location(2.5*DOWN + 1.5*RIGHT))
        self.wait()
        self.play(Rotate(position_1, PI/3, about_point = ORIGIN), Rotate(position_2, TAU/3, about_point = ORIGIN))
        self.wait()
        self.play(position_1.animate.scale(0.5, about_point = ORIGIN), position_2.animate.scale(0.5, about_point = ORIGIN))
        self.wait()
        arrows.clear_updaters()
        self.play(FadeOut(arrows))
        self.wait()

        ratio = 0.5
        lines_h = [Line(3.75*LEFT + i*ratio*UP, 3.75*RIGHT + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE_E).insert_n_curves(50) for i in range(-7, 8)]
        lines_v = [Line(3.75*UP + i*ratio*RIGHT, 3.75*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE_E).insert_n_curves(50) for i in range(-7, 8)]
        grid = VGroup(*lines_h, *lines_v)
        self.add(grid, axis_x, axis_y, axis_z).play(*[FadeOut(mob) for mob in [shade, text_1, text_2]], FadeIn(grid))
        self.wait()
        target = ParametricSurface(u_range = (-3.75, 3.75), v_range = (-3.75, 3.75), uv_func = lambda u, v: np.array([u, v, 1/4*np.sin(2*u)*np.sin(2*v)]), color = GREY, opacity = 0.5, depth_test = False)
        self.play(Transform(background.save_state(), target), grid.save_state().animate.apply_function(lambda t: np.array([t[0], t[1], 1/4*np.sin(2*t[0])*np.sin(2*t[1])])), run_time = 2)
        self.wait()
        
        line_example = lines_h[3].copy().set_stroke(color = YELLOW, width = 4)
        point_1, point_2 = 2*DOWN + PI*3/4*LEFT - 1/4*np.sin(4)*OUT, 2*DOWN + PI/4*RIGHT - 1/4*np.sin(4)*OUT
        dot_1 = Dot(point_1, radius = 0.06, color = YELLOW).save_state()
        dot_2 = Dot(point_2, radius = 0.06, color = YELLOW).save_state()
        line = Line(point_1, point_2, color = YELLOW)
        vector_1, vector_2 = Arrow(ORIGIN, point_1, color = BLUE, buff = 0), Arrow(ORIGIN, point_2, color = GREEN, buff = 0)
        vector_3 = Arrow(ORIGIN, (point_1 + point_2)/2, color = TEAL, buff = 0)
        vector_4, vector_5 = Arrow(ORIGIN, point_1/2, color = BLUE, buff = 0), Arrow(ORIGIN, point_2/2, color = GREEN, buff = 0)
        polyline = Polyline(ORIGIN, point_2, point_2, color = TEAL)
        self.play(ShowCreation(line_example))
        self.wait()
        self.cheese(dot_1, dot_2)
        self.play(ShowCreation(dot_1), ShowCreation(dot_2))
        dot_1.add_updater(lambda t: self.cheese(t))
        dot_2.add_updater(lambda t: self.cheese(t))
        self.play(ShowCreation(line), GrowArrow(vector_1), GrowArrow(vector_2))
        self.wait()
        self.add(polyline, vector_1, vector_2, vector_3, vector_4, vector_5).play(vector_1.animate.set_color(interpolate_color(BLUE, GREY, 0.5)), vector_2.animate.set_color(interpolate_color(GREEN, GREY, 0.5)),
                  GrowFromCenter(vector_4), TransformFromCopy(vector_2, vector_5), TransformFromCopy(vector_2, vector_3),
                  polyline.animate.set_points_as_corners([point_1/2, (point_1+point_2)/2, point_2/2]))
        self.wait()

        cross = VGroup(Line(UL, DR, color = RED), Line(UR, DL, color = RED)).scale(0.2).shift((point_1+point_2)/2).save_state()
        self.cheese(cross).play(ShowCreation(cross))
        cross.add_updater(lambda t: self.cheese(t))
        self.wait()
        for mob in [dot_1, dot_2, cross]:
            mob.clear_updaters()
        self.play(background.animate.restore(), grid.animate.restore(), *[FadeOut(mob, scale = np.array([1, 1, 0]), about_point = ORIGIN) for mob in [grid, polyline, vector_1, vector_2, vector_3, vector_4, vector_5, dot_1, dot_2, cross, line_example, line]])
        self.wait()

        vector = Arrow(ORIGIN, UR, buff = 0, color = GREEN)
        prototype = VGroup(vector.copy().set_color(interpolate_color(GREEN, GREY, 0.8)).save_state(), vector.copy().set_color(interpolate_color(GREEN, GREY, 0.5)).save_state())
        afterimage = VGroup()
        alpha = ValueTracker(-1)
        last = [1]
        def prototype_updater(mob: VGroup):
            value = alpha.get_value()
            if value < 1:
                value = 1-(1-value)/2
                value = (-value+2)*value**3
            mob[0].restore().shift(value*UR)
            mob[1].restore().shift(value*DL)
            if value > last[0]:
                afterimage.add(vector.copy().set_color(interpolate_color(GREEN, GREY, 0.5)).shift(last[0]*UR), vector.copy().set_color(interpolate_color(GREEN, GREY, 0.5)).shift(last[0]*DL))
                last[0] += 1
        self.play(GrowArrow(vector))
        self.wait()
        prototype.add_updater(prototype_updater)
        self.add(afterimage, prototype, vector)
        for _ in range(12):
            self.play(alpha.animate.increment_value(1), run_time = 0.5, rate_func = linear)
        prototype.clear_updaters()
        self.wait()
        self.play(*[FadeOut(mob) for mob in [vector, prototype, afterimage]])
        self.wait()

        ball = Sphere(color = RED, radius = 0.1)
        self.play(ShowCreation(ball))
        self.wait()
        self.play(Rotate(background, axis = np.array([1, 1, 1]), angle = PI/3))
        self.wait()
        self.play(Rotate(background, axis = np.array([1, -1, -1]), angle = PI/3))
        self.wait()
        self.play(Rotate(background, axis = np.array([-1, 1, -1]), angle = PI/3))
        self.wait()

class Video_2(FrameScene):

    def construct(self):
        title = Title("线性空间")
        titleline = TitleLine()
        text_1 = MTexText(r"$\bullet$线性空间$V$：").next_to(2*UP + 6*LEFT, RIGHT)
        text_2 = MTexText(r"$\bullet$性质：").next_to(2*UP, RIGHT)
        subtexts_1 = [MTex(r"\bullet\ \vec{u}+\vec{v}=\vec{v}+\vec{u}").scale(0.8).next_to(0.8*UP + 5.5*LEFT, RIGHT),
                      MTex(r"\bullet\ (\vec{u}+\vec{v})+\vec{w}=\vec{u}+(\vec{v}+\vec{w})").scale(0.8).next_to(5.5*LEFT, RIGHT),
                      MTex(r"\bullet\ \exists \vec{0}\in V,\ \vec{v}+\vec{0}=\vec{v}").scale(0.8).next_to(0.8*DOWN + 5.5*LEFT, RIGHT),
                      MTex(r"\bullet\ \cdots").scale(0.8).next_to(1.6*DOWN + 5.5*LEFT, RIGHT),]
        subtexts_2 = [MTexText(r"$\bullet$在线性组合下封闭").scale(0.8).next_to(0.8*UP + 0.5*RIGHT, RIGHT),
                      MTexText(r"$\bullet$平直空间").scale(0.8).next_to(0.5*RIGHT, RIGHT),
                      MTexText(r"$\bullet$没有边界").scale(0.8).next_to(0.8*DOWN + 0.5*RIGHT, RIGHT),
                      MTex(r"\bullet\ \cdots").scale(0.8).next_to(1.6*DOWN + 0.5*RIGHT, RIGHT),]
        shade = Shade(fill_color = BLACK, fill_opacity = 0.5)
        self.play(*[FadeIn(mob) for mob in [shade, title, titleline, text_1, text_2, *subtexts_1, *subtexts_2]])
        self.wait()

class BlackBox(VGroup):
    def __init__(self, **kwargs):
        
        core = Square(side_length = 2, fill_color = BLACK, fill_opacity = 1)
        entrance = Polygon(1.1*LEFT + 0.5*UP, 1.7*LEFT + UP, 1.7*LEFT + DOWN, 1.1*LEFT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        export = Polygon(1.1*RIGHT + 0.5*UP, 1.7*RIGHT + UP, 1.7*RIGHT + DOWN, 1.1*RIGHT + 0.5*DOWN, fill_color = BLACK, fill_opacity = 1)
        # background = Rectangle(width = 3, height = 2, stroke_width = 0, fill_color = BLACK, fill_opacity = 1)
        super().__init__(core, entrance, export, **kwargs)# background, 

class Video_3(FrameScene):

    def construct(self):
        axis_x = Line(7.5*LEFT, 7.5*RIGHT)
        axis_y = Line(7.5*DOWN, 7.5*UP)
        ratio = 1.5
        arrows = [Arrow(ORIGIN, (i+0.5)*ratio*RIGHT + (j+0.5)*ratio*DOWN, buff = 0, color = TEAL) for i in range(-int(64/9/ratio+0.5), int(64/9/ratio+0.5)) for j in range(-int(4/ratio+0.5), int(4/ratio+0.5))]
        sorted_arrows = arrows.copy()
        sorted_arrows.sort(key = lambda t: get_norm(t.get_end()), reverse = True)
        self.add(*sorted_arrows, axis_x, axis_y)
        self.wait()

        base_1, base_2 = Arrow(ORIGIN, 0.5*ratio*UR, color = BLUE, stroke_width = 8, buff = 0), Arrow(ORIGIN, 0.5*ratio*UL, color = GREEN, stroke_width = 8, buff = 0)
        shade = Shade(fill_opacity = 0.75, fill_color = BLACK)
        self.add(shade, axis_x, axis_y).play(FadeIn(shade), TransformFromCopy(sorted_arrows[-2], base_1), TransformFromCopy(sorted_arrows[-4], base_2))
        self.wait()

        copy_1, copy_2 = Arrow(ORIGIN, 0.5*ratio*UR, color = interpolate_color(BLUE, BLACK, 2/3), buff = 0), Arrow(ORIGIN, 0.5*ratio*UL, color = interpolate_color(GREEN, BLACK, 2/3), buff = 0)
        afterimage_1, afterimage_2 = VGroup(copy_1.copy().save_state(), copy_1.copy().save_state(), copy_1.copy()), VGroup(copy_2.copy().save_state(), copy_2.copy().save_state(), copy_2.copy())
        afterimage_1.prototype, afterimage_2.prototype = copy_1, copy_2
        afterimage_1.direction, afterimage_2.direction = 0.5*ratio*UR, 0.5*ratio*UL
        afterimage_1.last, afterimage_2.last = 1, 1
        alpha = ValueTracker(0)
        def afterimage_updater(mob: VGroup):
            value = alpha.get_value()
            mob[0].restore().shift(value*mob.direction)
            mob[1].restore().shift(-value*mob.direction)
            while value > mob.last:
                mob.add(mob.prototype.copy().shift(mob.direction*mob.last), mob.prototype.copy().shift(-mob.direction*mob.last))
                mob.last += 1
        afterimage_1.add_updater(afterimage_updater), afterimage_2.add_updater(afterimage_updater)
        self.add(afterimage_1, afterimage_2, axis_x, axis_y, base_1, base_2)
        self.play(alpha.animating(run_time = 4, rate_func = smooth_boot(1/11)).increment_value(11), *[FadeOut(mob) for mob in sorted_arrows])
        afterimage_1.clear_updaters(), afterimage_2.clear_updaters()

        alpha.set_value(0)
        grid_1, grid_2 = VGroup(afterimage_1.copy().save_state(), afterimage_1.copy().save_state()), VGroup(afterimage_2.copy().save_state(), afterimage_2.copy().save_state())
        grid_1.prototype, grid_2.prototype = afterimage_1, afterimage_2
        grid_1.direction, grid_2.direction = 0.5*ratio*UL, 0.5*ratio*UR
        grid_1.last, grid_2.last = 1, 1
        grid_1.add_updater(afterimage_updater), grid_2.add_updater(afterimage_updater)
        self.remove(shade).add(grid_1, grid_2, afterimage_1, afterimage_2, axis_x, axis_y, base_1, base_2)
        self.play(alpha.animating(run_time = 4, rate_func = linear).increment_value(12))
        grid_1.clear_updaters(), grid_2.clear_updaters()
        self.wait()

        arrow = Arrow(ORIGIN, ratio*(UR+0.5*UL), color = TEAL, buff = 0, stroke_width = 8)
        self.play(GrowArrow(arrow))
        self.wait()

        group = VGroup(arrow.copy(), MTex("="), MTex("2", color = YELLOW), base_1.copy(), MTex("+"), MTex("1", color = YELLOW), base_2.copy()).arrange().shift(4*LEFT + 2*UP)
        back_1 = BackgroundRectangle(group)
        self.play(FadeIn(back_1, DOWN), FadeIn(group, DOWN))
        self.wait()

        equation = VGroup(MTex(r"\begin{bmatrix}1\\3\end{bmatrix}", color = TEAL), MTex("="), MTex("2", color = YELLOW), MTex(r"\begin{bmatrix}1\\1\end{bmatrix}", color = BLUE), MTex("+"), MTex("1", color = YELLOW), MTex(r"\begin{bmatrix}-1\\1\end{bmatrix}", color = GREEN))
        for i in range(7):
            equation[i].set_x(group[i].get_x()).set_y(-2).set_stroke(width = 8, color = BLACK, background = True)
        back_2 = BackgroundRectangle(equation)
        shade = Shade(fill_color = BLACK)
        self.bring_to_back(grid_1, grid_2, afterimage_1, afterimage_2, shade).add(back_1, back_2, group).play(FadeIn(shade, run_time = 2), TransformFromCopy(back_1, back_2), *[FadeTransform(group[i].copy(), equation[i], stretch = False) for i in range(7)])
        self.remove(back_1, back_2, afterimage_1, afterimage_2, grid_1, grid_2, shade).wait()

        vector_form = MTex(r"\vec{x}=c_1\vec{v}_1+c_2\vec{v}_2").set_stroke(width = 8, color = BLACK, background = True)
        parts = VGroup(vector_form[0:2].set_fill(color = TEAL), vector_form[2], vector_form[3:5].set_fill(color = YELLOW), vector_form[5:8].set_fill(color = BLUE), vector_form[8], vector_form[9:11].set_fill(color = YELLOW), vector_form[11:].set_fill(color = GREEN)).shift(3*RIGHT + 2*DOWN)
        self.play(*[TransformFromCopy(equation[i], parts[i], path_arc = PI/6) for i in range(7)])
        self.remove(*parts).add(vector_form).wait()
        box = BlackBox().set_fill(opacity = 0).save_state().shift(0.5*DOWN).set_stroke(width = 10, color = GREY).scale(np.array([4, 3, 0]))
        equation.generate_target().shift(5.2*UP + RIGHT)
        for i in [0, 3, 6]:
            equation.target[i].scale(0.8)

        matrix = MTex(r"\begin{bmatrix}1&-1\\1&1\end{bmatrix}").shift(0.5*DOWN)
        vector = MTex(r"\begin{bmatrix}2\\1\end{bmatrix}").shift(5.5*LEFT + 0.5*DOWN)
        vector_row = MTex(r"\begin{bmatrix}2&1\end{bmatrix}").shift(0.5*UP)
        for i in (1, 4):
            matrix[i].set_color(BLUE)
        for i in (2, 3, 5):
            matrix[i].set_color(GREEN)
        vector[1:3].set_color(YELLOW)
        shadow = matrix.copy().save_state().set_color(GREY_D)
        offset_1 = matrix[1].get_x() - vector_row[1].set_color(YELLOW).get_x() + 0.3
        vector_row[0:2].shift(offset_1*RIGHT)
        offset_2 = matrix[5].get_x() - vector_row[2].set_color(YELLOW).get_x() + 0.5
        vector_row[2:].shift(offset_2*RIGHT)
        offset_3 = matrix[3].get_y() - vector_row[2].set_color(YELLOW).get_y()
        offset_4 = matrix[5].get_y() - vector_row[2].set_color(YELLOW).get_y()
        self.add(self.shade, box, equation, vector_form).play(FadeIn(self.shade, run_time = 1), MoveToTarget(equation, run_time = 2), vector_form.animating(run_time = 2).shift(5.2*UP + 0.5*LEFT), *[OverFadeIn(mob, run_time = 2) for mob in [box, matrix, vector]])
        self.clear().add(shadow, box, equation, vector_form, vector, matrix).wait()
        self.play(TransformFromCopy(vector, vector_row, path_arc = PI/2), matrix[-1].animate.set_x(vector_row[-1].get_x()))
        self.wait()
        back = BackgroundRectangle(matrix.refresh_bounding_box(), fill_opacity = 1, buff = 0.05)
        self.bring_to_back(vector_row[0], vector_row[3], back)
        copy_1, copy_2 = vector_row[1].copy().shift(offset_3*UP), vector_row[2].copy().shift(offset_3*UP)
        dot = MTex(r"\cdot")
        dot_1 = dot.copy().set_x((copy_1.get_x()+matrix[1].get_x())/2).set_y(copy_1.get_y())
        dot_2 = dot.copy().set_x((copy_2.get_x()+matrix[3].get_x())/2).set_y(copy_2.get_y())
        dot_3 = dot.copy().set_x((copy_1.get_x()+matrix[1].get_x())/2).set_y(matrix[4].get_y())
        dot_4 = dot.copy().set_x((copy_2.get_x()+matrix[3].get_x())/2).set_y(matrix[4].get_y())
        def down_updater(mob: Mobject):
            if vector_row[1].get_y() < copy_1.get_y():
                self.add(copy_1, copy_2).remove(mob)
                mob.clear_updaters()
        self.add(Mobject().add_updater(down_updater)).play(*[mob.animate.shift(offset_4*UP) for mob in vector_row], *[FadeIn(mob) for mob in [dot_1, dot_2, dot_3, dot_4]])
        self.remove(vector_row[0], vector_row[3], back).wait()
        
        output = MTex(r"\begin{bmatrix}1\\3\end{bmatrix}", tex_to_color_map = {(r"1", r"3"): TEAL}).shift(3*RIGHT + 0.5*DOWN)
        mobs = matrix[0], VGroup(matrix[1], dot_1, copy_1, matrix[2], matrix[3], dot_2, copy_2), VGroup(matrix[4], dot_3, vector_row[1], matrix[5], dot_4, vector_row[2]), matrix[6]
        self.play(*[ReplacementTransform(mobs[i], output[i]) for i in range(4)], rate_func = rush_into)
        self.play(output.animating(rate_func = rush_from).shift(2.5*RIGHT), shadow.animate.restore())
        self.wait()

        space_in = ImageMobject("Patch3_1.png", height = 3).shift(4*LEFT)
        space_out = ImageMobject("Patch3_2.png", height = 3).shift(4*RIGHT)
        self.play(*[OverFadeIn(mob, scale = 1/3, about_point = ORIGIN) for mob in [space_in, space_out]], box.animate.restore(), shadow.animate.shift(0.5*UP), OverFadeOut(vector, 0.75*(5.5*RIGHT + 0.5*UP)), OverFadeOut(output, 0.75*(5.5*LEFT + 0.5*UP)), run_time = 2)
        self.wait()
        self.play(IndicateAround(VGroup(shadow[1], shadow[4])), IndicateAround(VGroup(shadow[2], shadow[3], shadow[5])), WiggleOutThenIn(equation[3]), WiggleOutThenIn(equation[6]), FadeOut(vector_form))
        self.wait()

        text = MTex(r"\mbox{span}\{\}")
        span = VGroup(text[:-1], Arrow(ORIGIN, 1/3*(UR), buff = 0, color = BLUE), MTex(r","), Arrow(ORIGIN, 1/3*(UL), buff = 0, color = GREEN), text[-1]).arrange().shift(3*UP + 4*RIGHT)
        span[1].position, span[3].position = span[1].get_center().copy(), span[3].get_center().copy()
        self.play(FadeOut(equation), Write(span))
        self.remove(space_out).wait()

        point_1, point_2 = Point(1/3*UR), Point(1/3*UL)
        def span_updater(mob: VGroup):
            mob[1].become(Arrow(ORIGIN, point_1.get_location(), buff = 0, color = BLUE)).move_to(mob[1].position)
            mob[3].become(Arrow(ORIGIN, point_2.get_location(), buff = 0, color = GREEN)).move_to(mob[3].position)
        span.add_updater(span_updater)
        parts = [shadow[0], shadow[1], shadow[2:4], shadow[4], shadow[5], shadow[6]]
        target = MTex(r"\begin{bmatrix}2&1\\1&2\end{bmatrix}")
        target[1].set_color(BLUE), target[2].set_color(GREEN), target[3].set_color(BLUE), target[4].set_color(GREEN)
        self.play(point_1.animate.set_location(1/3*(np.array([2, 1, 0]))), point_2.animate.set_location(1/3*(np.array([1, 2, 0]))), *[ReplacementTransform(parts[i], target[i]) for i in range(6)])
        span.clear_updaters()
        self.wait()

        column = MTexText("列空间", color = BLUE).next_to(3*UP + 2*RIGHT, UP)
        out_1 = ImageMobject("Patch3_3.png", height = 3).shift(4*RIGHT)
        out_2 = ImageMobject("Patch3_4.png", height = 6).shift(2*RIGHT)
        self.play(FadeTransform(span, column), out_1.animate.shift(2*LEFT), FadeIn(out_2, 2*LEFT), FadeOut(space_in, 6*LEFT), *[mob.animate.shift(4*LEFT) for mob in [box, target]])
        self.wait()
        self.remove(out_1, out_2)

        def long_coloring(mob: MTex, *negs):
            parts = [mob[0:2]]
            index = 2
            for i in range(6):
                if i in negs:
                    parts.append(mob[index:index+2].set_color(GREEN if i%2 else BLUE))
                    index += 1
                else:
                    parts.append(mob[index].set_color(GREEN if i%2 else BLUE))
                index += 1
            parts.append(mob[index:])
            return parts
            # mob[2].set_color(BLUE), mob[4].set_color(BLUE), mob[6].set_color(BLUE)
            # mob[3].set_color(GREEN), mob[5].set_color(GREEN), mob[7].set_color(GREEN)
        long_0 = long_coloring(MTex(r"\begin{bmatrix}2&1\\1&2\\0&0\end{bmatrix}").shift(4*LEFT))
        offset = long_0[1].get_center() - target[1].get_center()
        self.play(box.animate.scale(np.array([4/3, 1.5, 1])), *[ReplacementTransform(target[i], long_0[i]) for i in range(5)], FadeIn(long_0[5], offset), FadeIn(long_0[6], offset), ReplacementTransform(target[-1], long_0[-1]))
        self.wait()

        self.play(long_0[6].save_state().animate.become(long_0[2]).set_y(long_0[5].get_y()).set_color(YELLOW))
        self.wait()
        self.play(long_0[6].animate.restore())
        self.wait()

        
        long_1 = long_coloring(MTex(r"\begin{bmatrix}1&-3\\2&2\\-1&-1\end{bmatrix}").shift(4*LEFT), 1, 4, 5)
        self.play(*[ReplacementTransform(long_0[i], long_1[i]) for i in range(8)])
        self.wait()
        long_2 = long_coloring(MTex(r"\begin{bmatrix}-1&-1\\0&1\\0&-1\end{bmatrix}").shift(4*LEFT), 0, 1, 5)
        self.play(*[ReplacementTransform(long_1[i], long_2[i]) for i in range(8)])
        self.wait()
        long_3 = long_coloring(MTex(r"\begin{bmatrix}1&2\\1&-1\\-2&-1\end{bmatrix}").shift(4*LEFT), 3, 4, 5)
        self.play(*[ReplacementTransform(long_2[i], long_3[i]) for i in range(8)])
        self.wait()
        long_4 = long_coloring(MTex(r"\begin{bmatrix}-1&2\\2&-1\\-1&-1\end{bmatrix}").shift(4*LEFT), 0, 3, 4, 5)
        self.play(*[ReplacementTransform(long_3[i], long_4[i]) for i in range(8)])
        self.wait()
        long_5 = long_coloring(MTex(r"\begin{bmatrix}-1&-1\\-2&1\\3&0\end{bmatrix}").shift(4*LEFT), 0, 1, 2)
        self.play(*[ReplacementTransform(long_4[i], long_5[i]) for i in range(8)])
        self.wait()
        long_6 = long_coloring(MTex(r"\begin{bmatrix}-2&3\\2&-1\\0&-2\end{bmatrix}").shift(4*LEFT), 0, 3, 5)
        self.play(*[ReplacementTransform(long_5[i], long_6[i]) for i in range(8)])
        self.wait()
        long_7 = long_coloring(MTex(r"\begin{bmatrix}-2&1\\1&1\\1&-2\end{bmatrix}").shift(4*LEFT), 0, 5)
        self.play(*[ReplacementTransform(long_6[i], long_7[i]) for i in range(8)])
        self.wait()
        long_8 = long_coloring(MTex(r"\begin{bmatrix}2&3\\1&-3\\-3&0\end{bmatrix}").shift(4*LEFT), 3, 4)
        self.play(*[ReplacementTransform(long_7[i], long_8[i]) for i in range(8)])
        self.wait()

class Patch3_1(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (3.0, 3.0)}, 
            }
    }
    def construct(self):
        ratio = 1/3
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%4 else 2, color = YELLOW_D if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%4 else 2, color = YELLOW_D if i else WHITE) for i in range(-10, 10)]
        lines = VGroup(*lines_h, *lines_v)
        self.add(lines, lines_h[10])

class Patch3_2(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (3.0, 3.0)}, 
            }
    }
    def construct(self):
        ratio = 1/3
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines = VGroup(*lines_h, *lines_v).apply_matrix(np.array([[1, 1], [-1, 1]]))
        arrow_1 = Arrow(ORIGIN, ratio*(UR), buff = 0, color = BLUE)
        arrow_2 = Arrow(ORIGIN, ratio*(UL), buff = 0, color = GREEN)
        self.add(lines, lines_h[10], arrow_1, arrow_2)

class Patch3_3(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (3.0, 3.0)}, 
            }
    }
    def construct(self):
        ratio = 1/3
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines = VGroup(*lines_h[:10], *lines_h[11:], *lines_v).apply_matrix(np.array([[1, 1], [-1, 1]]))
        lines_h[10].apply_matrix(np.array([[1, 1], [-1, 1]]))
        arrow_1 = Arrow(ORIGIN, ratio*(UR), buff = 0, color = BLUE)
        arrow_2 = Arrow(ORIGIN, ratio*(UL), buff = 0, color = GREEN)
        self.add(lines, lines_h[10], arrow_1, arrow_2).play(*[mob.animate.apply_matrix(np.array([[1/2, 3/2], [-1/2, 3/2]])) for mob in [lines, lines_h[10], arrow_1, arrow_2]])

class Patch3_4(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (6.0, 6.0)}, 
            },
        "camera_class": AACamera
    }
    def construct(self):
        ratio = 1/3
        lines_h = [Line(10/3*LEFT + i*ratio*UP, 10/3*RIGHT + i*ratio*UP, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(10/3*UP + i*ratio*RIGHT, 10/3*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 11)]
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([2, 1, 0])), buff = 0, color = BLUE).apply_matrix(np.array([[2/3, -1/3], [-1/3, 2/3]]))
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([1, 2, 0])), buff = 0, color = GREEN).apply_matrix(np.array([[2/3, -1/3], [-1/3, 2/3]]))
        lines = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10], arrow_1, arrow_2).scale(0.5).save_state().scale(2).apply_matrix(np.array([[2, 1], [1, 2]]))
        self.add(lines)
        
        axis_x = Line(4*LEFT, 4*RIGHT, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_y = Line(4*DOWN, 4*UP, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_z = Line(4*OUT, 4*IN, color = YELLOW, stroke_width = 2, depth_test = True)
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        self.add(axis_x, axis_y, axis_z, lines).play(lines.animate.scale(0.5), *[GrowFromCenter(mob) for mob in [axis_x, axis_y, axis_z]], camera.animating(rate_func = less_smooth).set_focal_distance(16).shift(1*OUT).set_orientation(Rotation(quadternion)), run_time = 3)
        self.wait()
        self.play(lines.animate.restore().apply_matrix(np.array([[2, 1, 0], [1, 2, 0], [0, 1, 0]])))
        self.wait()
        self.play(lines.animate.restore().apply_matrix(np.array([[2, 1, 0], [1, 2, 0], [0, 0, 0]])))
        self.wait()

        self.play(lines.animate.restore().apply_matrix(np.array([[1, -3, 0], [2, 2, 0], [-1, -1, 0]])))
        self.wait()
        self.play(lines.animate.restore().apply_matrix(np.array([[-1, -1, 0], [0, 1, 0], [0, -1, 0]])))
        self.wait()
        self.play(lines.animate.restore().apply_matrix(np.array([[1, 2, 0], [1, -1, 0], [-2, -1, 0]])))
        self.wait()
        plane = Polygon(np.array([1, 1, -2]), np.array([-1, 2, -1]), np.array([-2, 1, 1]), np.array([-1, -1, 2]), np.array([1, -2, 1]), np.array([2, -1, -1]), stroke_width = 0, fill_color = BLUE, fill_opacity = 0, anti_alias_width = 150, depth_test = True).scale(2)
        lines.generate_target().restore().apply_matrix(np.array([[-1, 2, 0], [2, -1, 0], [-1, -1, 0]])).set_opacity(0.8)
        lines.target[-2:].set_opacity(1)
        plane.generate_target().set_opacity(0.06)
        plane.target.anti_alias_width = 120
        self.add(plane, lines).play(MoveToTarget(lines), MoveToTarget(plane))
        self.wait()
        lines.generate_target().restore().apply_matrix(np.array([[-1, -1, 0], [-2, 1, 0], [3, 0, 0]])).set_opacity(0.6)
        lines.target[-2:].set_opacity(1)
        plane.generate_target().set_opacity(0.12)
        plane.target.anti_alias_width = 90
        self.play(MoveToTarget(lines), MoveToTarget(plane))
        self.wait()
        lines.generate_target().restore().apply_matrix(np.array([[-2, 3, 0], [2, -1, 0], [0, -2, 0]])).set_opacity(0.4)
        lines.target[-2:].set_opacity(1)
        plane.generate_target().set_opacity(0.18)
        plane.target.anti_alias_width = 60
        self.play(MoveToTarget(lines), MoveToTarget(plane))
        self.wait()
        lines.generate_target().restore().apply_matrix(np.array([[-2, 1, 0], [1, 1, 0], [1, -2, 0]])).set_opacity(0.2)
        lines.target[-2:].set_opacity(1)
        plane.generate_target().set_opacity(0.24)
        plane.target.anti_alias_width = 30
        self.play(MoveToTarget(lines), MoveToTarget(plane))
        self.wait()
        lines.generate_target().restore().apply_matrix(np.array([[2, 3, 0], [1, -3, 0], [-3, 0, 0]])).set_opacity(0.0)
        lines.target[-2:].set_opacity(1)
        plane.generate_target().set_opacity(0.3)
        plane.target.anti_alias_width = 0
        self.play(MoveToTarget(lines), MoveToTarget(plane))
        arrows = VGroup(arrow_1, arrow_2)
        self.remove(lines).add(arrows).wait()

class Video3_2(FrameScene):
    # CONFIG = {
    #     "camera_config": {
    #         "frame_config": {"frame_shape": (6.0, 6.0)}, 
    #         },
    #     "camera_class": AACamera
    # }
    def construct(self):
        ratio = 1/3
        lines_h = [Line(10/3*LEFT + i*ratio*UP, 10/3*RIGHT + i*ratio*UP, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 11)]
        lines_v = [Line(10/3*UP + i*ratio*RIGHT, 10/3*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-10, 11)]
        arrow_1 = Arrow(ORIGIN, ratio*(np.array([1, 0, 0])), buff = 0, color = BLUE)
        arrow_2 = Arrow(ORIGIN, ratio*(np.array([0, 1, 0])), buff = 0, color = GREEN)
        lines = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10], arrow_1, arrow_2).save_state().apply_matrix(np.array([[1, 0, 0], [0, 1, 0], [-0.2, -0.2, 0]]))
        self.add(lines)
        
        axis_x = Line(4*LEFT, 4*RIGHT, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_y = Line(4*DOWN, 4*UP, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_z = Line(4*OUT, 4*IN, color = YELLOW, stroke_width = 2, depth_test = True)
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(1*OUT).set_orientation(Rotation(quadternion))
        plane = Square(side_length = 8, stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE, depth_test = True).apply_matrix(np.array([[1, 0, 0], [0, 1, 0], [-0.2, -0.2, 0]]))
        self.add(axis_x, axis_y, axis_z, plane, lines)

        for _ in range(5):
            self.play(lines.animate.restore().apply_matrix(np.array([[0.5, 0.5, 0], [-0.5, 0.5, 0], [0, -0.2, 0]])))
            self.wait()
            self.play(lines.animate.restore().apply_matrix(np.array([[0.9, 0.3, 0], [0.3, 0.9, 0], [-0.24, -0.24, 0]])))
            self.wait()
            self.play(lines.animate.restore().apply_matrix(np.array([[1, 0, 0], [0, 1, 0], [-0.2, -0.2, 0]])))
            self.wait()
        # self.play(lines.animate.restore().apply_matrix(np.array([[-1, -1, 0], [0, 1, 0], [0, -1, 0]])))
        # self.wait()
        # self.play(lines.animate.restore().apply_matrix(np.array([[1, 2, 0], [1, -1, 0], [-2, -1, 0]])))
        # self.wait()
        # plane = Polygon(np.array([1, 1, -2]), np.array([-1, 2, -1]), np.array([-2, 1, 1]), np.array([-1, -1, 2]), np.array([1, -2, 1]), np.array([2, -1, -1]), stroke_width = 0, fill_color = BLUE, fill_opacity = 0, anti_alias_width = 150, depth_test = True).scale(2)
        # lines.generate_target().restore().apply_matrix(np.array([[-1, 2, 0], [2, -1, 0], [-1, -1, 0]])).set_opacity(0.8)
        # lines.target[-2:].set_opacity(1)
        # plane.generate_target().set_opacity(0.06)
        # plane.target.anti_alias_width = 120
        # self.add(plane, lines).play(MoveToTarget(lines), MoveToTarget(plane))
        # self.wait()
        # lines.generate_target().restore().apply_matrix(np.array([[-1, -1, 0], [-2, 1, 0], [3, 0, 0]])).set_opacity(0.6)
        # lines.target[-2:].set_opacity(1)
        # plane.generate_target().set_opacity(0.12)
        # plane.target.anti_alias_width = 90
        # self.play(MoveToTarget(lines), MoveToTarget(plane))
        # self.wait()
        # lines.generate_target().restore().apply_matrix(np.array([[-2, 3, 0], [2, -1, 0], [0, -2, 0]])).set_opacity(0.4)
        # lines.target[-2:].set_opacity(1)
        # plane.generate_target().set_opacity(0.18)
        # plane.target.anti_alias_width = 60
        # self.play(MoveToTarget(lines), MoveToTarget(plane))
        # self.wait()
        # lines.generate_target().restore().apply_matrix(np.array([[-2, 1, 0], [1, 1, 0], [1, -2, 0]])).set_opacity(0.2)
        # lines.target[-2:].set_opacity(1)
        # plane.generate_target().set_opacity(0.24)
        # plane.target.anti_alias_width = 30
        # self.play(MoveToTarget(lines), MoveToTarget(plane))
        # self.wait()
        # lines.generate_target().restore().apply_matrix(np.array([[2, 3, 0], [1, -3, 0], [-3, 0, 0]])).set_opacity(0.0)
        # lines.target[-2:].set_opacity(1)
        # plane.generate_target().set_opacity(0.3)
        # plane.target.anti_alias_width = 0
        # self.play(MoveToTarget(lines), MoveToTarget(plane))
        # arrows = VGroup(arrow_1, arrow_2)
        # self.remove(lines).add(arrows).wait()

#################################################################### 

class Video_4(FrameScene):

    def construct(self):
        axis_x = Line(4*LEFT, 4*RIGHT, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_y = Line(4*DOWN, 4*UP, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_z = Line(4*OUT, 4*IN, color = YELLOW, stroke_width = 2, depth_test = True)
        vector = Arrow(ORIGIN, np.array([1, 1, 1]), color = BLUE, buff = 0, width_to_tip_len = 0.02)
        line = Line(np.array([-4, -4, -4]), np.array([4, 4, 4]), color = BLUE_B)
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(1*OUT).set_orientation(Rotation(quadternion))
        self.add(axis_x, axis_y, axis_z, line, vector)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(quad(OUT, DEGREES*dt), mob.quadternion)
            mob.set_orientation(Rotation(mob.quadternion))
        camera.quadternion = quadternion
        camera.add_updater(camera_updater)
        self.wait(10)

class Video_5(FrameScene):

    def construct(self):
        axis_x = Line(4*LEFT, 4*RIGHT, color = YELLOW, stroke_width = 2)
        axis_y = Line(4*DOWN, 4*UP, color = YELLOW, stroke_width = 2)
        axis_out = Line(ORIGIN, 4*OUT, color = YELLOW, stroke_width = 2)
        axis_in = Line(ORIGIN, 4*IN, color = YELLOW, stroke_width = 2)
        vector_1 = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, width_to_tip_len = 0.01)
        vector_2 = Arrow(ORIGIN, UP, color = GREEN, buff = 0, width_to_tip_len = 0.01)
        vector_3 = Arrow(ORIGIN, UL, color = PURPLE, buff = 0, width_to_tip_len = 0.01)
        plane = Square(side_length = 8, color = BLUE, stroke_width = 0, fill_opacity = 0.5, depth_test = True)
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        camera.set_focal_distance(16).shift(1*OUT).set_orientation(Rotation(quadternion))
        self.add(axis_x, axis_y, axis_in, plane, axis_out, vector_1, vector_2, vector_3)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(quad(OUT, DEGREES*dt), mob.quadternion)
            mob.set_orientation(Rotation(mob.quadternion))
        camera.quadternion = quadternion
        camera.add_updater(camera_updater)
        self.wait(10)

class Video_6(FrameScene):

    def construct(self):
        axis_x = Line(4*LEFT, 4*RIGHT, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_y = Line(4*DOWN, 4*UP, color = YELLOW, stroke_width = 2, depth_test = True)
        axis_z = Line(4*OUT, 4*IN, color = YELLOW, stroke_width = 2, depth_test = True)
        lines = []
        for i in range(3):
            for j in (1, -1):
                for k in (1, -1):
                    point = np.array([2, 2, 2])
                    point[(i+1)%3]*= j
                    point[(i-1)%3]*= k
                    start, end = point.copy(), point.copy()
                    end[i] *= -1
                    lines.append(Line(start, end))
        cube = VGroup(*lines, depth_test = True)
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, TAU/3), quad(RIGHT, PI/2 - PI/20))
        vector_1 = Arrow(ORIGIN, RIGHT, color = BLUE, buff = 0, width_to_tip_len = 0.01, depth_test = True)
        vector_2 = Arrow(ORIGIN, UP, color = GREEN, buff = 0, width_to_tip_len = 0.01, depth_test = True)
        vector_3 = Arrow(ORIGIN, OUT, color = PURPLE, buff = 0, width_to_tip_len = 0.01, depth_test = True)
        camera.set_focal_distance(16).set_orientation(Rotation(quadternion))
        self.add(axis_x, axis_y, axis_z, cube, vector_1, vector_2, vector_3)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(quad(OUT, DEGREES*dt), mob.quadternion)
            mob.set_orientation(Rotation(mob.quadternion))
        camera.quadternion = quadternion
        camera.add_updater(camera_updater)
        self.wait(5)
        self.play(*[mob.save_state().animate.apply_matrix(np.array([[1, 0, -1], [0, 1, 1], [0, 0, 0]])) for mob in [cube, vector_3]], run_time = 2)
        self.wait(2)
        self.play(*[mob.animate.restore() for mob in [cube, vector_3]], run_time = 2)
        self.wait(2)
        self.play(*[mob.animate.apply_matrix(np.array([[1, 0, -1], [0, 1, 1], [0, 0, 0]])) for mob in [cube, vector_3]], run_time = 2)
        self.wait(2)

        nil = Line(np.array([2, -2, 2]), np.array([-2, 2, -2]), color = GREY, depth_test = True).save_state().apply_matrix(np.array([[1, 0, -1], [0, 1, 1], [0, 0, 0]]))
        self.play(*[mob.animate.restore() for mob in [cube, vector_3, nil]], run_time = 2)
        self.wait(2)
        self.play(*[mob.animate.apply_matrix(np.array([[1, 0, -1], [0, 1, 1], [0, 0, 0]])) for mob in [cube, vector_3, nil]], run_time = 2)
        self.wait(2)
        nils = [Line(np.array([2, -2, 2]), np.array([-2, 2, -2]), color = GREY, depth_test = True).shift(i*2*UP + j*2*RIGHT).save_state().apply_matrix(np.array([[1, 0, -1], [0, 1, 1], [0, 0, 0]])) for i in (1, 0, -1) for j in (1, 0, -1)]
        self.remove(nil).play(*[mob.animate.restore() for mob in [cube, vector_3, *nils]], run_time = 2)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in nils[:4] + nils[5:]])
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in [cube, nils[4]]])
        self.wait(2)
        self.play(vector_3.animate.apply_matrix(np.array([[1, 0, -1], [0, 1, 1], [0, 0, 0]])), run_time = 2)
        self.wait(2)

        plane = Square(side_length = 8, color = BLUE, stroke_width = 0, fill_opacity = 0.5, depth_test = True)
        self.play(FadeIn(plane, rate_func = double_there_and_back, remover = True, run_time = 2))
        self.wait()

        equation = VGroup(MTex(r"1", color = YELLOW), Arrow(ORIGIN, RIGHT, buff = 0, color = BLUE), MTex(r"-", color = YELLOW), MTex(r"1", color = YELLOW), Arrow(ORIGIN, UP, buff = 0, color = GREEN), MTex(r"+", color = YELLOW), MTex(r"1", color = YELLOW), Arrow(ORIGIN, UL, buff = 0, color = PURPLE), MTex(r"="), MTex(r"\vec{0}", color = GREY)).fix_in_frame().arrange()
        equation[-1].shift(equation[-1][1].get_y()*DOWN)
        equation.scale(0.8).shift(3*UP + 4*LEFT)
        tex_1, tex_2 = r"\begin{bmatrix}1\\-1\\1\end{bmatrix}", r"\begin{bmatrix}0\\0\\0\end{bmatrix}"
        matrix = MTex(r"\begin{bmatrix}1&0&-1\\0&1&1\\0&0&0\end{bmatrix}\begin{bmatrix}1\\-1\\1\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}", tex_to_color_map = {tex_1: YELLOW, tex_2: GREY}).scale(0.8).fix_in_frame().next_to(equation, DOWN).set_stroke(width = 8, color = BLACK, background = True)
        matrix[2].set_fill(BLUE), matrix[6].set_fill(BLUE), matrix[9].set_fill(BLUE)
        matrix[3].set_fill(GREEN), matrix[7].set_fill(GREEN), matrix[10].set_fill(GREEN)
        matrix[4:6].set_fill(PURPLE_B), matrix[8].set_fill(PURPLE_B), matrix[11].set_fill(PURPLE_B)
        self.play(Write(equation))
        self.wait()
        self.play(FadeIn(matrix, UP))
        self.wait()

        tex = MTex(r"\mbox{span}\{\}")
        comma = MTex(r",")
        span = VGroup(tex[:-1].copy(), vector_1.copy(), comma.copy(), vector_2.copy(), comma.copy(), vector_3.copy(), tex[-1].copy(), MTex(r"="), tex[:-1].copy(), vector_1.copy(), comma.copy(), vector_2.copy(), tex[-1].copy()).arrange().scale(0.7).fix_in_frame()
        span.next_to(3*UP, RIGHT)
        self.play(Write(span))
        self.wait()

        back = BackgroundRectangle(matrix[0:14])
        arrow = Arrow(ORIGIN, 0.8*UP).next_to(back, DOWN, buff = 0.15)
        tip = MTexText("秩为2").set_stroke(width = 8, color = BLACK, background = True).scale(0.5).next_to(arrow, DOWN, buff = 0.15).add(arrow).fix_in_frame()
        self.play(FadeIn(tip, 0.5*UP))
        self.wait(10)

class Video_7(FrameScene):

    def construct(self):
        array = np.zeros(20)
        array[0], array[1] = 2, 1
        for i in range(2, 20):
            array[i] = array[i-1] + 2*array[i-2]
        terms = [MTex(str(int(array[i])), color = BLUE).shift(UP + 6*LEFT + (0.5*i + 0.05*i**2)*RIGHT) for i in range(11)] + [MTex(r"\cdots", color = BLUE).shift(UP + 6*RIGHT)]
        equation_1 = MTex(r"2\times {2}+1=5", tex_to_color_map = {(r"{2}", r"1", r"5"): BLUE}).next_to(terms[2], DOWN).scale(0.8)
        equation_2 = MTex(r"2\times 1+5=7", tex_to_color_map = {(r"1", r"5", r"7"): BLUE}).next_to(terms[3], DOWN).scale(0.8)
        equation = MTex(r"a_{n}=2a_{n-2}+a_{n-1}", tex_to_color_map = {(r"a_{n-2}", r"a_{n-1}", r"a_{n}"): BLUE}).shift(3*UP)
        self.play(FadeIn(terms[0], 0.5*DOWN))
        self.wait()
        self.play(FadeIn(terms[1], 0.5*DOWN))
        self.wait()
        self.play(Write(equation_1), FadeIn(terms[2], 0.5*DOWN))
        self.wait()
        self.play(FadeOut(equation_1))
        self.wait()
        self.play(Write(equation_2), FadeIn(terms[3], 0.5*DOWN))
        self.wait()
        self.play(FadeOut(equation_2), Write(equation))
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in terms[4:]], lag_ratio = 0.1, run_time = 2))
        self.wait()

        question = MTex(r"a_{10000}=?", tex_to_color_map = {r"a_{10000}": BLUE}).shift(DOWN)
        self.play(FadeIn(question, 0.5*UP))
        self.wait()

        vec_a = MTex(r"\vec{a}\ =\ (", tex_to_color_map = {r"\vec{a}": BLUE}).shift(2.02*UP + 7*LEFT)
        terms_a = [MTex(r"a_{" + str(i) + r"}", color = BLUE).shift(2*UP + 6*LEFT + (0.5*i + 0.05*i**2)*RIGHT) for i in range(11)] + [MTex(r"\cdots", color = BLUE).shift(2*UP + 6*RIGHT)]
        self.play(FadeIn(vec_a.shift(RIGHT), RIGHT), *[FadeIn(mob.shift(RIGHT), RIGHT) for mob in terms_a], *[mob.animate.shift(RIGHT) for mob in terms])
        self.wait()

        theset = MTex(r"\{\ \vec{a}\ |\ a_{n}=2a_{n-2}+a_{n-1}\}", tex_to_color_map = {(r"\vec{a}", r"a_{n-2}", r"a_{n-1}", r"a_{n}"): BLUE}).shift(3*UP)
        self.play(*[FadeOut(mob, DOWN) for mob in terms], FadeOut(question, DOWN), *[mob.animate.shift(DOWN) for mob in [equation, vec_a] + terms_a], FadeIn(theset))
        self.wait()

        mul = MTex(r"k\vec{a}:\ ka_{n}=2ka_{n-2}+ka_{n-1}", tex_to_color_map = {(r"\vec{a}", r"a_{n-2}", r"a_{n-1}", r"a_{n}"): BLUE, r"k": YELLOW}).shift(DOWN)
        self.play(FadeIn(mul, RIGHT))
        self.wait()

        add = MTex(r"\vec{a}+\vec{b}:\ a_{n}+b_{n}=2(a_{n-2}+b_{n-2})+(a_{n-1}+b_{n-1})", tex_to_color_map = {(r"\vec{a}", r"a_{n-2}", r"a_{n-1}", r"a_{n}"): BLUE, (r"\vec{b}", r"b_{n-2}", r"b_{n-1}", r"b_{n}"): GREEN}).shift(2*DOWN)
        self.play(FadeIn(add, RIGHT))
        self.wait()

        arrow_1,arrow_2 = Arrow(ORIGIN, 0.8*DOWN, color = YELLOW).next_to(terms_a[0], UP, buff = 0.15), Arrow(ORIGIN, 0.8*DOWN, color = YELLOW).next_to(terms_a[1], UP, buff = 0.15)
        tex = MTex(r"a_0=2,\ a_1=1", color = BLUE, tex_to_color_map ={r"=": WHITE}).scale(0.5).next_to(VGroup(arrow_1, arrow_2), UP, buff = 0.15).add(arrow_1, arrow_2)
        arrow_3 = Arrow(ORIGIN, 0.8*DR, color = YELLOW).next_to(terms_a[11], UL, buff = 0.15)
        question = MTex(r"a_{10000}=?", tex_to_color_map = {r"a_{10000}": BLUE}).scale(0.5).next_to(arrow_3, UL).add(arrow_3)
        self.play(FadeIn(tex, 0.5*DOWN))
        self.wait()
        self.play(FadeIn(question, 0.5*DOWN))
        self.wait()

        self.play(FadeOut(mul), FadeOut(add))
        self.wait()

        geometry = MTex(r"\vec{q}\ =\ (", tex_to_color_map = {r"\vec{q}": PURPLE_B}).shift(0.02*UP + 6*LEFT)
        terms_q = [MTex(r"q^{" + str(i) + r"}", color = PURPLE_B).shift(5*LEFT + (0.5*i + 0.05*i**2)*RIGHT) for i in range(11)] + [MTex(r"\cdots", color = PURPLE_B).shift(7*RIGHT)]
        self.play(LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in [geometry] + terms_q], lag_ratio = 0.1, run_time = 2))
        self.wait()

        texts = r"q^{n}", r"=2q^{n-2}+q^{n-1}", r"q^2-q-2", r"=0", r"q=2", r",\ q=-1"
        equation = MTex(r"q^{n}&=2q^{n-2}+q^{n-1}\\q^2-q-2&=0\\q=2&,\ q=-1", isolate = texts, tex_to_color_map = {r"q": PURPLE_B}).scale(0.8).next_to(0.5*DOWN, DOWN)
        slices = [equation.get_part_by_tex(text) for text in texts]
        parts = [VGroup(slices[0], slices[1]), VGroup(slices[2], slices[3]), VGroup(slices[4], slices[5])]
        self.play(Write(parts[0]))
        self.wait()
        self.play(FadeIn(parts[1], 0.3*DOWN))
        self.wait()
        self.play(FadeIn(parts[2], 0.3*DOWN))
        self.wait()
        rest = VGroup(slices[0], slices[1], slices[2], slices[3])

        base_1 = MTex(r"\vec{q}_1\ =\ (", tex_to_color_map = {r"\vec{q}_1": PURPLE_B}).shift(0.02*DOWN + 6*LEFT)
        terms_1 = [MTex(r"2^{" + str(i) + r"}", color = PURPLE_B).shift(5*LEFT + (0.5*i + 0.05*i**2)*RIGHT) for i in range(11)] + [MTex(r"\cdots", color = PURPLE_B).shift(7*RIGHT)]
        base_2 = MTex(r"\vec{q}_2\ =\ (", tex_to_color_map = {r"\vec{q}_2": PURPLE}).shift(DOWN + 6*LEFT)
        terms_2 = [MTex(r"-1" if i%2 else r"1", color = PURPLE).shift(DOWN + 5*LEFT + (0.5*i + 0.05*i**2)*RIGHT) for i in range(11)] + [MTex(r"\cdots", color = PURPLE).shift(DOWN + 7*RIGHT)]
        self.remove(geometry, *terms_q).play(FadeOut(rest, scale = np.array([1, 0, 1]), about_point = rest.get_corner(DOWN)), 
                                            LaggedStart(AnimationGroup(TransformFromCopy(geometry, base_1), TransformFromCopy(geometry, base_2)), *[AnimationGroup(TransformFromCopy(terms_q[i], terms_1[i]), TransformFromCopy(terms_q[i], terms_2[i])) for i in range(12)], lag_ratio = 0.1, run_time = 2))
        self.wait()

        add = MTex(r"+").set_x(base_1[0].get_x()).set_y(-0.5)
        equal = MTex(r"=").rotate(PI/2).set_x(base_1[0].get_x()).set_y(-1.5)
        self.play(Write(add))
        self.wait()
        solution = MTex(r"\vec{a}\ =\ (", tex_to_color_map = {r"\vec{a}": BLUE}).shift(2*DOWN + 6*LEFT)
        terms_a = [MTex(str(int(array[i])), color = BLUE).shift(2*DOWN + 5*LEFT + (0.5*i + 0.05*i**2)*RIGHT) for i in range(11)] + [MTex(r"\cdots", color = BLUE).shift(2*DOWN + 7*RIGHT)]
        self.play(LaggedStart(AnimationGroup(FadeIn(equal, 0.5*DOWN), FadeIn(solution, 0.5*DOWN)), *[FadeIn(mob, 0.5*DOWN) for mob in terms_a], lag_ratio = 0.1, run_time = 2), FadeOut(parts[2], 0.5*DOWN))
        self.wait()

        result = MTex(r"a_{10000}=2^{10000}+{1}", tex_to_color_map = {r"a_{10000}": BLUE, r"2^{10000}": PURPLE_B, r"{1}": PURPLE}).scale(0.8).next_to(question, UP).shift(0.5*LEFT)
        around = SurroundingRectangle(result)
        self.play(Write(result))
        self.play(ShowCreation(around))
        self.wait()

class Video_7_1(FrameScene):
    def construct(self):
        ratio = 0.5
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE_E if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10])
        self.add(lines)

        vector_a = Arrow(ORIGIN, 2*RIGHT + UP, color = BLUE, buff = 0)
        label_a = MTex(r"\begin{bmatrix}2\\1\end{bmatrix}", color = BLUE).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).next_to(2*RIGHT + 0.5*UP, RIGHT)
        self.play(GrowArrow(vector_a), Write(label_a))
        self.wait()
        array = np.zeros(20)
        array[0], array[1] = 2, 1
        for i in range(2, 20):
            array[i] = array[i-1] + 2*array[i-2]
        terms = [MTex(str(int(array[i])), color = BLUE).scale(0.8).set_stroke(width = 8, color = BLACK, background = True) for i in range(9)] + [MTex(r"\cdots", color = BLUE).shift(UP + 6*RIGHT)]
        terms_a = VGroup(*terms).arrange().next_to(UP, UP).set_x(1.7, LEFT)
        self.play(FadeIn(terms[0], 0.3*DOWN), FadeIn(terms[1], 0.3*DOWN))
        self.wait()
        self.play(LaggedStart(*[FadeIn(terms[i], DOWN) for i in range(2, 10)], run_time = 3, lag_ratio = 0.5))
        self.wait()

        vector_b = Arrow(ORIGIN, 2*UP + LEFT, color = GREEN, buff = 0)
        label_b = MTex(r"\begin{bmatrix}-1\\2\end{bmatrix}", color = GREEN).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).next_to(LEFT + 1.5*UP, LEFT)
        self.play(GrowArrow(vector_b), Write(label_b))
        self.wait()
        array = np.zeros(20)
        array[0], array[1] = -1, 2
        for i in range(2, 20):
            array[i] = array[i-1] + 2*array[i-2]
        terms = [MTex(str(int(array[i])), color = GREEN).scale(0.8).set_stroke(width = 8, color = BLACK, background = True) for i in range(13)] + [MTex(r"\cdots", color = GREEN).shift(UP + 6*RIGHT)]
        terms_b = VGroup(*terms).arrange().next_to(2*UP, UP).set_x(-1.7, LEFT)
        self.play(FadeIn(terms[0], 0.3*DOWN), FadeIn(terms[1], 0.3*DOWN))
        self.wait()
        self.play(LaggedStart(*[FadeIn(terms[i], DOWN) for i in range(2, 14)], run_time = 3, lag_ratio = 0.5))
        self.wait()

        self.remove(vector_a, label_a, terms_a, vector_b, label_b, terms_b)

        vector_1 = Arrow(ORIGIN, 2*UP + RIGHT, color = PURPLE_A, buff = 0)
        label_1 = MTex(r"\begin{bmatrix}1\\2\end{bmatrix}", color = PURPLE_A).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).next_to(1.5*UP + 0.5*RIGHT, LEFT)
        terms = [MTex(r"2^{" + str(i) + r"}", color = PURPLE_A).scale(0.8).set_stroke(width = 8, color = BLACK, background = True) for i in range(10)] + [MTex(r"\cdots", color = PURPLE_A).shift(UP + 6*RIGHT)]
        terms_1 = VGroup(*terms).arrange().next_to(2*UP, UP).set_x(0.7, LEFT)

        vector_2 = Arrow(ORIGIN, DOWN + RIGHT, color = PURPLE_D, buff = 0)
        label_2 = MTex(r"\begin{bmatrix}1\\-1\end{bmatrix}", color = PURPLE_D).scale(0.8).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).next_to(0.5*DOWN, LEFT)
        self.play(GrowArrow(vector_2), Write(label_2), GrowArrow(vector_1), Write(label_1))
        terms = [MTex(r"-1" if i%2 else r"1", color = PURPLE_D).scale(0.8).set_stroke(width = 8, color = BLACK, background = True) for i in range(12)] + [MTex(r"\cdots", color = PURPLE_D).shift(UP + 6*RIGHT)]
        terms_2 = VGroup(*terms).arrange().next_to(DOWN, DOWN).set_x(0.3, LEFT)
        self.play(LaggedStart(*[FadeIn(terms_1[i], DOWN) for i in range(11)], run_time = 3, lag_ratio = 0.5), LaggedStart(*[FadeIn(terms_2[i], DOWN) for i in range(13)], run_time = 3, lag_ratio = 0.5))
        self.wait()

        self.play(GrowArrow(vector_a), Write(label_a))
        self.wait()
        self.play(LaggedStart(*[FadeIn(terms_a[i], DOWN) for i in range(10)], run_time = 3, lag_ratio = 0.5))
        self.wait()

        equation = MTex(r"\begin{bmatrix}1\\2\end{bmatrix}+\begin{bmatrix}1\\-1\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}", tex_to_color_map = {r"\begin{bmatrix}1\\2\end{bmatrix}": PURPLE_A, r"\begin{bmatrix}1\\-1\end{bmatrix}": PURPLE_D, r"\begin{bmatrix}2\\1\end{bmatrix}": BLUE}).set_stroke(width = 8, color = BLACK, background = True)
        self.play(Write(equation.shift(3*LEFT + UP)))
        self.wait()

#################################################################### 

class Video_8(FrameScene):

    def construct(self):
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
        current = MTex(r"\begin{bmatrix}I_1\\I_2\\I_3\end{bmatrix}", color = GREEN).shift(4*RIGHT)
        self.play(FadeIn(circuit), FadeIn(notices), Write(current))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [circuit, notices, current]])
        self.wait()

        e_l, e_r = 0.075*LEFT, 0.075*RIGHT
        source = Line(LEFT, e_l).append_points(Line(e_r, RIGHT).get_points()).add(Line(0.3*UP, 0.3*DOWN).shift(e_l), Line(0.15*UP, 0.15*DOWN).shift(e_r))
        nonsource = Line(LEFT, e_l).append_points(Line(e_r, RIGHT).get_points()).add(Line(0.3*LEFT, 0.3*RIGHT).shift(e_l), Line(0.15*LEFT, 0.15*RIGHT).shift(e_r))
        circuit = VGroup(resistance.copy().shift(RIGHT + 1.5*UP), resistance.copy().shift(RIGHT), resistance.copy().shift(RIGHT + 1.5*DOWN), source.copy().shift(LEFT + 1.5*UP), source.copy().shift(LEFT), Line(2*LEFT, ORIGIN).shift(1.5*DOWN), Line(1.5*UP, 1.5*DOWN).shift(2*RIGHT), Line(1.5*UP, 1.5*DOWN).shift(2*LEFT))
        v_1, v_2 = MTex(r"5V", color = LIGHT_BROWN).scale(0.6).next_to(circuit[3], UP), MTex(r"3V", color = LIGHT_BROWN).scale(0.6).next_to(circuit[4], UP)
        r_1, r_2, r_3 = MTex(r"2\Omega", color = YELLOW).scale(0.6).next_to(circuit[0], UP), MTex(r"1\Omega", color = YELLOW).scale(0.6).next_to(circuit[1], UP), MTex(r"1\Omega", color = YELLOW).scale(0.6).next_to(circuit[2], UP)
        arrow = Arrow(0.3*RIGHT, 0.3*LEFT, buff = 0, color = GREEN)
        arrow_1 = arrow.copy().next_to(2*UP, DOWN)
        notice_1 = MTex(r"I_1", color = GREEN).scale(0.6).next_to(arrow_1, DOWN, buff = 0.15).add(arrow_1)
        arrow_2 = arrow.copy().next_to(ORIGIN, DOWN)
        notice_2 = MTex(r"I_2", color = GREEN).scale(0.6).next_to(arrow_2, DOWN, buff = 0.15).add(arrow_2)
        arrow_3 = arrow.copy().next_to(2*DOWN, DOWN).rotate(PI)
        notice_3 = MTex(r"I_1+I_2", color = GREEN).scale(0.6).next_to(arrow_3, DOWN, buff = 0.15).add(arrow_3)
        label_A, label_B = MTex("A").scale(0.8).next_to(2*LEFT, LEFT), MTex("B").scale(0.8).next_to(2*RIGHT, RIGHT)
        labels = VGroup(v_1, v_2, r_1, r_2, r_3, label_A, label_B)
        labels_current = VGroup(notice_1, notice_2, notice_3)
        self.play(FadeIn(circuit), FadeIn(labels))
        self.wait()

        solution = MTex(r"\begin{cases}V_{AB}=5V-2\Omega I_1\\V_{AB}=3V-1\Omega I_2\\V_{AB}=1\Omega(I_1+I_2)\end{cases}\Rightarrow\begin{cases}I_1=1.6A\\I_2=0.6A\\V_{AB}=2.2V\end{cases}", tex_to_color_map = {(r"1\Omega", r"2\Omega"): YELLOW, (r"I_1", r"I_2", r"1.6A", r"0.6A"): GREEN, (r"V_{AB}", r"2.2V", r"3V", r"5V"): LIGHT_BROWN}).scale(0.8).shift(3*RIGHT)
        self.play(*[mob.animate.shift(4*LEFT) for mob in [circuit, labels]], FadeIn(labels_current.shift(4*LEFT), 4*LEFT))
        self.play(Write(solution))
        self.wait()
        self.play(FadeOut(solution))

        t_1, t_2 = MTex(r"aV", color = LIGHT_BROWN).scale(0.6).next_to(circuit[3], UP), MTex(r"bV", color = LIGHT_BROWN).scale(0.6).next_to(circuit[4], UP)
        linear = MTex(r"\begin{bmatrix}I_1\\I_2\end{bmatrix}=\begin{bmatrix}?&?\\?&?\end{bmatrix}\begin{bmatrix}{a}\\{b}\end{bmatrix}", tex_to_color_map = {(r"I_1", r"I_2"): GREEN, (r"{a}", r"{b}"): LIGHT_BROWN}).shift(2*RIGHT)
        self.play(Transform(v_1.save_state(), t_1), Transform(v_2.save_state(), t_2))
        self.wait()
        self.play(FadeIn(linear, 0.5*UP))
        self.wait()
        condition = MTex(r"\begin{bmatrix}{a}\\{b}\end{bmatrix}=\begin{bmatrix}5\\3\end{bmatrix}, V_{AB}=1\Omega(I_1+I_2)=?", tex_to_color_map = {(r"I_1", r"I_2"): GREEN, (r"{a}", r"{b}", r"5", r"3"): LIGHT_BROWN, r"1\Omega": YELLOW}).scale(0.8).shift(2*RIGHT + 1*DOWN)
        self.play(linear.animate.shift(UP), FadeIn(condition, UP), v_1.animate.restore(), v_2.animate.restore())
        self.wait()
        self.play(FadeOut(linear), FadeOut(condition), FadeOut(labels_current))
        self.wait()

        circuit_1 = circuit.copy()
        circuit_1[3].become(nonsource).shift(5*LEFT + 1.5*UP)
        circuit_1.scale(0.8).move_to(3*RIGHT + 2*UP)
        v_1, v_2 = MTex(r"5V", color = LIGHT_BROWN, fill_opacity = 0).scale(0.6).next_to(circuit_1[3], UP), MTex(r"3V", color = LIGHT_BROWN).scale(0.6).next_to(circuit_1[4], UP)
        r_1, r_2, r_3 = MTex(r"2\Omega", color = YELLOW).scale(0.6).next_to(circuit_1[0], UP), MTex(r"1\Omega", color = YELLOW).scale(0.6).next_to(circuit_1[1], UP), MTex(r"1\Omega", color = YELLOW).scale(0.6).next_to(circuit_1[2], UP)
        label_A, label_B = MTex("A").scale(0.8).next_to(circuit_1, LEFT), MTex("B").scale(0.8).next_to(circuit_1, RIGHT)
        labels_1 = VGroup(v_1, v_2, r_1, r_2, r_3, label_A, label_B)
        circuit_2 = circuit.copy()
        circuit_2[4].become(nonsource).shift(5*LEFT)
        circuit_2.scale(0.8).move_to(3*RIGHT + 1.5*DOWN)
        v_1, v_2 = MTex(r"5V", color = LIGHT_BROWN).scale(0.6).next_to(circuit_2[3], UP), MTex(r"3V", color = LIGHT_BROWN, fill_opacity = 0).scale(0.6).next_to(circuit_2[4], UP)
        r_1, r_2, r_3 = MTex(r"2\Omega", color = YELLOW).scale(0.6).next_to(circuit_2[0], UP), MTex(r"1\Omega", color = YELLOW).scale(0.6).next_to(circuit_2[1], UP), MTex(r"1\Omega", color = YELLOW).scale(0.6).next_to(circuit_2[2], UP)
        label_A, label_B = MTex("A").scale(0.8).next_to(circuit_2, LEFT), MTex("B").scale(0.8).next_to(circuit_2, RIGHT)
        labels_2 = VGroup(v_1, v_2, r_1, r_2, r_3, label_A, label_B)
        self.play(TransformFromCopy(circuit, circuit_1), TransformFromCopy(labels, labels_1))
        self.play(TransformFromCopy(circuit, circuit_2), TransformFromCopy(labels, labels_2))
        self.wait()
        arrow_4 = arrow.copy().next_to(3*RIGHT + 2*UP + 1.2*DOWN, UP).rotate(PI)
        notice_4 = MTex(r"1.2A", color = GREEN).scale(0.6).next_to(arrow_4, UP, buff = 0.15).add(arrow_4)
        arrow_5 = arrow.copy().next_to(3*RIGHT + 1.5*DOWN + 1.2*DOWN, UP).rotate(PI)
        notice_5 = MTex(r"1A", color = GREEN).scale(0.6).next_to(arrow_5, UP, buff = 0.15).add(arrow_5)
        self.add(notice_4, notice_5)
        add, equal = MTex(r"+", color = RED).scale(1.5).shift(3*RIGHT + 0.25*UP), MTex(r"=", color = RED).scale(1.5)
        self.play(FadeIn(notice_4, 0.3*RIGHT), FadeIn(notice_5, 0.3*RIGHT))
        self.wait()
        self.play(Write(add), Write(equal))
        self.wait()

        arrow_6 = arrow.copy().next_to(4*LEFT + 1.5*DOWN, UP).rotate(PI)
        notice_6 = MTex(r"2.2A", color = GREEN).scale(0.6).next_to(arrow_6, UP, buff = 0.15).add(arrow_6)
        solution = MTex(r"V_{AB}=(1\Omega)(2.2A)=2.2V", tex_to_color_map = {(r"V_{AB}", r"2.2V"): LIGHT_BROWN, r"1\Omega": YELLOW, r"2.2A": GREEN}).scale(0.8).next_to(circuit, DOWN)
        self.play(FadeIn(notice_6, 0.3*RIGHT))
        self.wait()
        self.play(Write(solution))
        self.wait()

class Video_9(FrameScene):

    def construct(self):

        texts = r"C_2H_5OH", r"O_2", r"CO_2", r"H_2O"
        formula = MTex(r"{x}C_2H_5OH+{y}O_2 = {z}CO_2+{w}H_2O", isolate = texts, tex_to_color_map = {(r"{x}", r"{y}", r"{z}", r"{w}"): GREEN}).scale(0.8).shift(3*UP)
        parts = [formula.get_part_by_tex(text).set_color(YELLOW) for text in texts]
        formula[:11].shift(0.3*LEFT)
        formula[12:].shift(0.3*RIGHT)
        formula[11].set_width(formula[11].get_width() + 0.6, stretch = True)
        formula.refresh_bounding_box()

        texts = r"2\\1\\6", r"0\\2\\0", r"1\\2\\0", r"0\\1\\2"
        vector_1, vector_2, vector_3, vector_4 = [MTex(r"\begin{bmatrix}" + texts[i] + r"\end{bmatrix}", color = YELLOW, tex_to_color_map = {r"0": GREY}).scale(0.8).set_x(parts[i].get_x()).shift(1.5*UP) for i in range(4)]
        rest = MTex(r"x+y=z+w", color = GREEN, tex_to_color_map = {(r"+", r"="): WHITE}).scale(0.8)
        rest.shift((1.5 - rest[3].get_y())*UP)
        rest[0].set_x(vector_1.get_x(LEFT) -0.2, RIGHT), rest[2].set_x(vector_2.get_x(LEFT) -0.2, RIGHT), rest[4].set_x(vector_3.get_x(LEFT) -0.2, RIGHT), rest[6].set_x(vector_4.get_x(LEFT) -0.2, RIGHT)
        rest[1].set_x((vector_1.get_x(RIGHT) + rest[2].get_x(LEFT))/2), rest[3].set_x((vector_2.get_x(RIGHT) + rest[4].get_x(LEFT))/2), rest[5].set_x((vector_3.get_x(RIGHT) + rest[6].get_x(LEFT))/2)

        texts = r"\begin{bmatrix}2&0&-1&-0\\1&2&-2&-1\\6&0&-0&-2\end{bmatrix}", r"\begin{bmatrix}x\\y\\z\\w\end{bmatrix}", r"=\begin{bmatrix}0\\0\\0\end{bmatrix}"
        matrix = MTex(r"\begin{bmatrix}2&0&-1&-0\\1&2&-2&-1\\6&0&-0&-2\end{bmatrix}\begin{bmatrix}x\\y\\z\\w\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}", tex_to_color_map = {texts[0]: YELLOW, texts[1]: GREEN, (r"0", r"-0"): GREY, texts[2]: ORANGE, r"=": WHITE}).scale(0.8).shift(DOWN)

        self.fade_in(formula, vector_1, vector_2, vector_3, vector_4, rest, matrix)
        self.wait()
        self.fade_out()
        self.wait()

        formula_l = MTex(r"{x}Cu = {y}Au", tex_to_color_map = {(r"{x}", r"{y}"): GREEN, (r"Cu", r"Au"): YELLOW}).scale(0.8).shift(2*UP + 3*LEFT)
        formula_l[:3].shift(0.3*LEFT)
        formula_l[4:].shift(0.3*RIGHT)
        formula_l[3].set_width(formula_l[3].get_width() + 0.6, stretch = True)
        texts = r"\begin{bmatrix}1&0\\0&-1\end{bmatrix}", r"\begin{bmatrix}x\\y\end{bmatrix}", r"=\begin{bmatrix}0\\0\end{bmatrix}"
        matrix_l = MTex(r"\begin{bmatrix}1&0\\0&-1\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix}", tex_to_color_map = {texts[0]: YELLOW, texts[1]: GREEN, (r"0", r"0"): GREY, texts[2]: ORANGE, r"=": WHITE}).scale(0.8).shift(0.5*DOWN + 3*LEFT)
        self.play(Write(formula_l))
        self.wait()
        self.play(FadeIn(matrix_l, 0.5*UP))
        self.wait()

        formula_r = MTex(r"{x}Au = {y}Cl_2", tex_to_color_map = {(r"{x}", r"{y}"): GREEN, (r"Cl_2", r"Au"): YELLOW}).scale(0.8).shift(2*UP + 3*RIGHT)
        formula_r[:3].shift(0.3*LEFT)
        formula_r[4:].shift(0.3*RIGHT)
        formula_r[3].set_width(formula_r[3].get_width() + 0.6, stretch = True)
        texts = r"\begin{bmatrix}1&0\\0&-2\end{bmatrix}", r"\begin{bmatrix}x\\y\end{bmatrix}", r"=\begin{bmatrix}0\\0\end{bmatrix}"
        matrix_r = MTex(r"\begin{bmatrix}1&0\\0&-2\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix}", tex_to_color_map = {texts[0]: YELLOW, texts[1]: GREEN, r"0": GREY, texts[2]: ORANGE, r"=": WHITE}).scale(0.8).shift(0.5*DOWN + 3*RIGHT)
        self.play(Write(formula_r))
        self.wait()
        self.play(FadeIn(matrix_r, 0.5*UP))
        self.wait()

        self.fade_out()
        self.wait()
        formula = MTex(r"x_1Na_2CO_3+x_2HCl = x_3NaCl + x_4NaHCO_3 + x_5H_2O + x_6CO_2", tex_to_color_map = {(re.compile(r"x_.")): GREEN, (r"Na_2CO_3", r"HCl", r"NaCl", r"NaHCO_3", r"H_2O", r"CO_2"): YELLOW}).scale(0.8).shift(3*UP)
        formula[:14].shift(0.3*LEFT)
        formula[15:].shift(0.3*RIGHT)
        formula[14].set_width(formula[14].get_width() + 0.6, stretch = True)
        self.play(Write(formula))
        self.wait()

        solution_1 = MTex(r"{2}Na_2CO_3+{3}HCl = {3}NaCl + {1}NaHCO_3 + {1}H_2O + {1}CO_2", tex_to_color_map = {(re.compile(r"{.}")): GREEN, (r"Na_2CO_3", r"HCl", r"NaCl", r"NaHCO_3", r"H_2O", r"CO_2"): YELLOW}).scale(0.5).shift(2.3*UP + 2*LEFT)
        solution_1[:12].shift(0.2*LEFT)
        solution_1[13:].shift(0.2*RIGHT)
        solution_1[12].set_width(solution_1[12].get_width() + 0.4, stretch = True)
        solution_2 = MTex(r"{3}Na_2CO_3+{4}HCl = {4}NaCl + {2}NaHCO_3 + {1}H_2O + {1}CO_2", tex_to_color_map = {(re.compile(r"{.}")): GREEN, (r"Na_2CO_3", r"HCl", r"NaCl", r"NaHCO_3", r"H_2O", r"CO_2"): YELLOW}).scale(0.5).shift(1.7*UP + 2*RIGHT)
        solution_2[:12].shift(0.2*LEFT)
        solution_2[13:].shift(0.2*RIGHT)
        solution_2[12].set_width(solution_2[12].get_width() + 0.4, stretch = True)
        self.play(FadeIn(solution_1, 0.5*RIGHT))
        self.wait()
        self.play(FadeIn(solution_2, 0.5*LEFT))
        self.wait()

        texts = r"\begin{bmatrix}0&1&0&-1&-2&0\\1&0&0&-1&0&-1\\3&0&0&-3&-1&-2\\2&0&-1&-1&0&0\\0&1&-1&0&0&0\end{bmatrix}", r"\begin{bmatrix}x_1\\x_2\\x_3\\x_4\\x_5\\x_6\end{bmatrix}", r"=\begin{bmatrix}0\\0\\0\\0\\0\end{bmatrix}", r"\Rightarrow \begin{bmatrix}x_1\\x_2\\x_3\\x_4\\x_5\\x_6\end{bmatrix}={a}\begin{bmatrix}1\\1\\1\\1\\0\\0\end{bmatrix}+{b}\begin{bmatrix}0\\1\\1\\-1\\1\\1\end{bmatrix}"
        matrix = MTex(r"".join(texts), isolate = [texts[0]+texts[1]+texts[2], texts[3]], tex_to_color_map = {texts[0]: YELLOW, r"0": GREY, (texts[1], r"\begin{bmatrix}1\\1\\1\\1\\0\\0\end{bmatrix}", r"\begin{bmatrix}0\\1\\1\\-1\\1\\1\end{bmatrix}"): GREEN, texts[2]: ORANGE, r"=": WHITE, r"{a}": BLUE, r"{b}": PURPLE_B}).scale(0.8).shift(0.5*DOWN)
        part_0, part_1 = matrix.get_part_by_tex(texts[0]+texts[1]+texts[2]), matrix.get_part_by_tex(texts[3])
        part_0.save_state().set_x(0)
        part_1.save_state().set_x(part_0.get_x(RIGHT), RIGHT)
        shade = BackgroundRectangle(part_1, buff = 0.2, fill_opacity = 1)
        self.play(FadeIn(part_0, 0.5*UP))
        self.wait()
        self.add(part_1, shade, part_0).play(part_0.animate.restore(), part_1.animate.restore(), follow(shade, part_0, remover = True))
        self.wait()

        basic_1 = MTex(r"Na_2CO_3+HCl=NaHCO_3+NaCl", color = BLUE).scale(0.6).shift(2.5*DOWN + 3*LEFT)
        basic_1[:10].shift(0.2*LEFT)
        basic_1[11:].shift(0.2*RIGHT)
        basic_1[10].set_width(basic_1[10].get_width() + 0.4, stretch = True)
        basic_2 = MTex(r"NaHCO_3+HCl=NaCl+H_2O+CO_2", color = PURPLE_B).scale(0.6).shift(2.5*DOWN + 3*RIGHT)
        basic_2[:10].shift(0.2*LEFT)
        basic_2[11:].shift(0.2*RIGHT)
        basic_2[10].set_width(basic_2[10].get_width() + 0.4, stretch = True)
        self.play(Write(basic_1), IndicateAround(matrix.get_part_by_tex(r"\begin{bmatrix}1\\1\\1\\1\\0\\0\end{bmatrix}")))
        self.wait()
        self.play(Write(basic_2), IndicateAround(matrix.get_part_by_tex(r"\begin{bmatrix}0\\1\\1\\-1\\1\\1\end{bmatrix}")))
        self.wait()

        tip_1 = MTex(r"a=2, b=1", tex_to_color_map = {(r"a", r"2"): BLUE, (r"b", r"1"): PURPLE_B}).scale(0.5).next_to(solution_1, RIGHT, buff = 0.5)
        tip_2 = MTex(r"a=3, b=1", tex_to_color_map = {(r"a", r"3"): BLUE, (r"b", r"1"): PURPLE_B}).scale(0.5).next_to(solution_2, LEFT, buff = 0.5)
        self.play(FadeIn(tip_1, 0.5*LEFT), FadeIn(tip_2, 0.5*RIGHT))
        self.wait()

class Video_10(FrameScene):

    def construct(self):
        axis_x = Arrow(3*LEFT, 3*RIGHT, buff = 0, color = GREY)
        axis_y = Arrow(0.5*DOWN, 2*UP, buff = 0, color = GREY)
        coordinates = VGroup(axis_x.copy().shift(1.5*UP), axis_y.copy().shift(1.5*UP), axis_x.copy().shift(1.5*DOWN), axis_y.copy().shift(1.5*DOWN))
        self.fade_in(coordinates)

        square = Polyline(2.5*LEFT, PI/2*LEFT, PI/2*LEFT + UP, PI/2*RIGHT + UP, PI/2*RIGHT, 2.5*RIGHT).set_stroke(width = 6, color = WHITE).insert_n_curves(20).shift(1.5*UP)
        self.play(ShowCreation(square))
        self.wait()

        graph_0 = FunctionGraph(lambda t: 0.5, [-2.5, 2.5, 0.002], color = YELLOW).shift(1.5*DOWN)
        self.play(ShowCreation(graph_0))
        self.wait()
        self.play(graph_0.animate.shift(3*UP))
        self.wait()

        for i in range(50):
            color = ratio_color(np.sqrt(i)/4 - int(np.sqrt(i)/4), YELLOW, GREEN, BLUE, PURPLE, RED, ORANGE)
            graph_i = FunctionGraph(lambda t: (-1)**(i%2)*2/((2*i+1)*PI)*np.cos((2*i+1)*t), [-2.5, 2.5, 0.002], color = color).shift(1.5*DOWN)
            self.play(ShowCreation(graph_i))
            self.wait(0, int(30/max(i, 1)))
            self.add(graph_0.copy().set_stroke(width = 2, color = color, opacity = 0.2), graph_0)
            new_points = [a+b[1]*UP+1.5*UP for a, b in zip(graph_0.get_points(), graph_i.get_points())]
            self.play(FadeOut(graph_i, 3*UP), graph_0.animate.set_points(new_points))
            self.wait(0, int(30/max(i, 1)))
        self.wait()

class Patch_11(FrameScene):
    def construct(self):
        base_1 = MTex(r"(1, 2, 4, 8, 16, \cdots)", color = BLUE).shift(2*UP + 4*LEFT).set_stroke(width = 8, color = BLACK, background = True)
        base_2 = MTex(r"(1, -1, 1, -1, 1, \cdots)", color = GREEN).shift(DOWN + 4*LEFT).set_stroke(width = 8, color = BLACK, background = True)
        vector = MTex(r"(2, 1, 5, 7, 17, \cdots)", color = TEAL).shift(0.5*UP + 4*RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        self.play(*[FadeIn(mob) for mob in [base_1, base_2, vector]])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [base_1, base_2, vector]])
        self.wait()

        resistance = Line(LEFT, 0.375*LEFT).append_points(Rectangle(height = 0.2, width = 0.75).get_points()).append_points(Line(0.375*RIGHT, RIGHT).get_points())
        e_l, e_r = 0.075*LEFT, 0.075*RIGHT
        source = Line(LEFT, e_l).append_points(Line(e_r, RIGHT).get_points()).add(Line(0.3*UP, 0.3*DOWN).shift(e_l), Line(0.15*UP, 0.15*DOWN).shift(e_r))
        nonsource = Line(LEFT, e_l).append_points(Line(e_r, RIGHT).get_points()).add(Line(0.3*LEFT, 0.3*RIGHT).shift(e_l), Line(0.15*LEFT, 0.15*RIGHT).shift(e_r))
        vector = VGroup(resistance.copy().shift(RIGHT + 1.5*UP), resistance.copy().shift(RIGHT), resistance.copy().shift(RIGHT + 1.5*DOWN), source.copy().shift(LEFT + 1.5*UP), source.copy().shift(LEFT), Line(2*LEFT, ORIGIN).shift(1.5*DOWN), Line(1.5*UP, 1.5*DOWN).shift(2*RIGHT), Line(1.5*UP, 1.5*DOWN).shift(2*LEFT)).set_color(TEAL)
        base_1 = vector.copy()
        base_1[3].become(nonsource).shift(LEFT + 1.5*UP)
        base_1.set_color(BLUE).move_to(2*UP + 4*LEFT).scale(0.8)
        base_2 = vector.copy()
        base_2[4].become(nonsource).shift(LEFT)
        base_2.set_color(GREEN).move_to(DOWN + 4*LEFT).scale(0.8)
        vector.move_to(0.5*UP + 4*RIGHT)
        self.play(*[FadeIn(mob) for mob in [base_1, base_2, vector]])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [base_1, base_2, vector]])
        self.wait()
        
        base_1 = MTex(r"Na_2CO_3+HCl=NaHCO_3+NaCl", color = BLUE).scale(0.6).shift(2.5*DOWN + 3*LEFT).set_stroke(width = 8, color = BLACK, background = True)
        base_1[:10].shift(0.2*LEFT)
        base_1[11:].shift(0.2*RIGHT)
        base_1[10].set_width(base_1[10].get_width() + 0.4, stretch = True)
        base_2 = MTex(r"NaHCO_3+HCl=NaCl+H_2O+CO_2", color = GREEN).scale(0.6).shift(2.5*DOWN + 3*RIGHT).set_stroke(width = 8, color = BLACK, background = True)
        base_2[:10].shift(0.2*LEFT)
        base_2[11:].shift(0.2*RIGHT)
        base_2[10].set_width(base_2[10].get_width() + 0.4, stretch = True)
        vector = MTex(r"xNa_2CO_3+(x+y)HCl = (x+y)NaCl + (x-y)NaHCO_3 + yH_2O + yCO_2", color = TEAL).scale(0.6).shift(3*UP).set_stroke(width = 8, color = BLACK, background = True)
        self.play(*[FadeIn(mob) for mob in [base_1, base_2, vector]])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [base_1, base_2, vector]])
        self.wait()

class Video_11(FrameScene):
    def construct(self):
        vector_1 = Arrow(ORIGIN, 2*RIGHT + 3*UP, buff = 0, color = BLUE, stroke_width = 8)
        vector_2 = Arrow(ORIGIN, LEFT + 2*UP, buff = 0, color = GREEN, stroke_width = 8)
        vector_3 = Arrow(ORIGIN, RIGHT + 5*UP, buff = 0, color = TEAL, stroke_width = 8)
        line = Polyline(2*RIGHT + 3*UP, RIGHT + 5*UP, LEFT + 2*UP, stroke_width = 2, stroke_color = [BLUE, TEAL, GREEN])
        group = VGroup(line, vector_1, vector_2, vector_3).rotate(np.arctan(1/5), about_point = ORIGIN)

        camera = self.camera.frame
        def camera_updater(mob: CameraFrame):
            mob.move_to((2.2 + 0.05*np.sin(self.time*PI))*UP)
        def rotate_updater(mob: VGroup, dt):
            mob.rotate(dt*PI/4, axis = UP, about_point = ORIGIN)
        self.add(camera.add_updater(camera_updater), group.add_updater(rotate_updater)).wait(60)

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]