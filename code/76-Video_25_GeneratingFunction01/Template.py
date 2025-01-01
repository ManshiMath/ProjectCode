from __future__ import annotations

from manimlib import *
import numpy as np
#################################################################### 

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
    
    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.mobject).add(self.target_mobject)
        super().clean_up_from_scene(scene)

class Video_3(FrameScene):
    def construct(self):
        n = 11
        texts = [r"a", r"xa"] + [r"x^{" + str(i) + r"}a" for i in range(2, n)]
        color_map = {r"x": RED, r"a": YELLOW}
        geometric = [MTex(texts[i], tex_to_color_map = color_map) for i in range(n)]
        VGroup(*geometric).arrange(buff = 1).next_to(6*LEFT)
        for mob in geometric:
            mob.set_y(3, DOWN)
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in geometric], lag_ratio = 0.5, run_time = 2))
        self.wait()

        steps = [Arrow(geometric[i][-1].get_corner(DOWN), geometric[i+1][0].get_corner(DOWN), path_arc = PI/3) for i in range(n-1)]
        multiplies = [MTex(r"\times x", tex_to_color_map = {r"x": RED}).next_to(steps[i], DOWN).scale(0.8).save_state() for i in range(n-1)]
        self.play(LaggedStart(*[ShowCreation(mob) for mob in steps], lag_ratio = 0.75, run_time = 3), 
                  LaggedStart(*[Write(mob) for mob in multiplies], lag_ratio = 0.75, run_time = 3))
        self.wait()

        operations = [MTex(r"P", color = ORANGE).next_to(steps[i], DOWN) for i in range(n-1)]
        self.play(LaggedStart(*[Flip(multiplies[i], operations[i]) for i in range(n-1)], lag_ratio = 0.75, run_time = 3))
        self.wait()

        for mob in multiplies:
            mob.restore()
        texts = [r"a", r"Pa"] + [r"P^{" + str(i) + r"}a" for i in range(2, n)]
        color_map = {r"P": ORANGE, r"a": YELLOW}
        operator_form = [MTex(texts[i], tex_to_color_map = color_map) for i in range(n)]
        for i in range(n):
            operator_form[i].set_y(0.8, DOWN).match_x(geometric[i], RIGHT)
        steps_2 = [Arrow(geometric[i][-1].get_corner(UP), geometric[i+1][0].get_corner(UP), path_arc = -PI/3).shift(2.0*DOWN) for i in range(n-1)]
        iterations = [MTex(r"P", color = ORANGE).next_to(steps_2[i], UP) for i in range(n-1)]
        board = BackgroundRectangle(VGroup(*operator_form, *steps_2, *operations))
        self.add(*multiplies, board, *operator_form, *steps_2, *operations).play(
            *[operations[i].animate.move_to(iterations[i]) for i in range(n-1)], 
            follow(board, operations[0], remover = True), *[follow(mob, operations[0], FadeIn) for mob in steps_2 + operator_form]
        )
        self.wait()

        color_map = {(r"I", r"P"): ORANGE, r"a": YELLOW, r"s": TEAL}
        sum_0 = MTex(r"s="+"+".join(texts[:8])+r"+\cdots", tex_to_color_map = color_map).next_to(6*LEFT)
        operators = [r"I", r"P"] + [r"P^{" + str(i) + r"}" for i in range(2, n)]
        sum_1 = MTex(r"=\left("+"+".join(operators[:8])+r"+\cdots\right)a", tex_to_color_map = color_map)
        sum_1.shift(sum_0[1].get_center() - sum_1[0].get_center() + 0.8*DOWN)
        self.play(Write(sum_0))
        self.wait()
        self.play(FadeIn(sum_1, 0.5*DOWN, lag_ratio = 0.1, run_time = 2))
        self.wait()
        sum_2 = MTex(r"s=\frac{1}{I-P}a", tex_to_color_map = color_map)
        sum_2.shift(sum_1[0].get_center() - sum_2[1].get_center() + 1.2*DOWN)
        self.play(Write(sum_2))
        self.wait()

        inverse = MTex(r"a=(I-P)s=s-Ps", tex_to_color_map = color_map).shift(2*RIGHT)
        inverse.shift((sum_2[1].get_y() - inverse[1].get_y())*UP)
        self.play(FadeIn(inverse, 0.5*LEFT, lag_ratio = 0.1))
        self.wait()

        sum_3 = MTex(r"s=\left(I-P\right)^{-1}a", tex_to_color_map = color_map)
        sum_3.shift(sum_1[0].get_center() - sum_3[1].get_center() + 1.2*DOWN)
        arrow = Arrow(inverse[0], sum_3[-1], buff = 0.3)
        anim = ReplacementTransform(sum_2[4:7], sum_3[3:6])
        self.play(ShowCreation(arrow), anim, *[follow(mob, anim, OverFadeOut) for mob in sum_2[2:4]], 
                  *[follow(mob, anim, OverFadeIn) for mob in [sum_3[2], sum_3[6:9]]], ReplacementTransform(sum_2[-1], sum_3[-1]))
        self.wait()

        line = Line(2.45*UP + 6*LEFT, 2.45*UP + 6*RIGHT)
        self.play(*[mob.animate.shift(0.5*UP).fade() for mob in geometric + steps + multiplies], GrowFromPoint(line, 2.2*UP))
        self.wait()

        title = Title("抽象等比求和").scale(1.2).next_to(line, UP, buff = 0.4)
        self.play(Write(title), *[FadeOut(mob) for mob in geometric + steps + multiplies])
        self.wait()
        
#################################################################### 

class Test_0(FrameScene):
    def construct(self):
        ratio = 0.5
        
        offset_r = RIGHT_SIDE/2 + 0.5*DOWN
        dic_mask = {"stroke_shader_folder": "sector_stroke", "fill_shader_folder": "mask_fill"}
        lines_h_a = [Line(LEFT_SIDE + i*ratio*DOWN, RIGHT_SIDE + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-10, 11)]
        lines_v_a = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-20, 21)]
        dic_a = {"half_1": unit(PI), "center_1": offset_r, "half_2": unit(TAU/3), "center_2": offset_r}
        for mob in lines_h_a + lines_v_a:
            mob.uniforms.update(dic_a)
        self.add(*lines_h_a, *lines_v_a)

class RotateIn(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(
        self,
        mobject: Mobject,
        axis: np.ndarray = OUT,
        **kwargs
    ):
        self.axis = axis
        if "mask_radius" in mobject.uniforms:
            self.handle_radius = True
            self.mask_radius = mobject.uniforms["mask_radius"]
            self.stroke_width = mobject.get_stroke_width()
        else:
            self.handle_radius = False
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for sm1, sm2 in self.get_all_families_zipped():
            sm1.set_points(sm2.get_points())
        ratio = interpolate(1, 1/np.sqrt(2), alpha)
        self.mobject.scale(ratio, about_point = ORIGIN).rotate(alpha * PI/4, axis = OUT, about_point = ORIGIN)
        if self.handle_radius:
            self.mobject.uniforms["mask_radius"] = self.mask_radius*ratio
            self.mobject.set_stroke(width = self.stroke_width*interpolate(1, 2**(-1/4), alpha))

class Test_1(FrameScene):
    def construct(self):
        ratio = 0.5
        
        dic_mask = {"stroke_shader_folder": "bounded_stroke", "fill_shader_folder": "bounded_fill"}
        width, height = 10, 10
        lines_h_a = [Line(width*ratio*LEFT + i*ratio*DOWN, width*ratio*RIGHT + i*ratio*DOWN, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-height, height + 1)]
        lines_v_a = [Line(height*ratio*UP + i*ratio*RIGHT, height*ratio*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE, **dic_mask) for i in range(-width, width + 1)]
        dic_a = {"mask_radius": 4.5}
        for mob in lines_h_a + lines_v_a:
            mob.uniforms.update(dic_a)
        self.add(*lines_h_a, *lines_v_a)
        circle = Circle(radius = 3)
        self.add(circle)
        self.wait()
        for _ in range(3):
            self.play(*[RotateIn(mob) for mob in lines_h_a + lines_v_a + [circle]])
            self.wait()

class FloatWindow(VGroup):
    CONFIG = {
        "height": FRAME_HEIGHT,
        "width": FRAME_WIDTH,
        "buff": 0.1,
        "outer_dic": {"fill_opacity": 1, 
                      "fill_color": "#222222",
                      "stroke_color": YELLOW_E},
        "inner_dic":{"fill_opacity": 1, 
                      "fill_color": BLACK,
                      "stroke_color": WHITE}
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        outer = Rectangle(height = self.height + self.buff, width = self.width + self.buff, **self.outer_dic)
        inner = Rectangle(height = self.height - self.buff, width = self.width - self.buff, **self.inner_dic)
        super().__init__(outer, inner, **kwargs)

class Video_4(FrameScene):
    def construct(self):
        ratio = 0.25
        width, height = 40, 20
        lines_h_b = [Line((width+0.5)*ratio*LEFT + i*ratio*DOWN, (width+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 0.5 if i%4 else 2, color = GREY if i else WHITE) for i in range(-height, height + 1)]
        lines_v_b = [Line((height+0.5)*ratio*UP + i*ratio*RIGHT, (height+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 0.5 if i%4 else 2, color = GREY if i else WHITE) for i in range(-width, width + 1)]
        self.add_background(*lines_h_b, *lines_v_b).bring_to_front(self.shade)

        ratio = 1
        dic_mask = {"stroke_shader_folder": "bounded_stroke", "fill_shader_folder": "bounded_fill"}
        width, height = 10, 10
        lines_h_a = [Line((width+0.5)*ratio*LEFT + i*ratio*DOWN, (width+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 3 if i%2 else 3, color = BLUE_E if i else WHITE, **dic_mask) for i in range(-height, height + 1)]
        lines_v_a = [Line((height+0.5)*ratio*UP + i*ratio*RIGHT, (height+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 3 if i%2 else 3, color = BLUE_E if i else WHITE, **dic_mask) for i in range(-width, width + 1)]
        dic_a = {"mask_radius": 10}
        for mob in lines_h_a + lines_v_a:
            mob.uniforms.update(dic_a)
        basis = VGroup(Vector(2*RIGHT, color = BLUE, stroke_width = 10), Vector(2*UP, color = GREEN, stroke_width = 10)) #max_width_to_length_ratio = 30
        self.add_background(*lines_h_a[:10], *lines_h_a[11:], *lines_v_a, lines_h_a[10]).add(basis)
        matrix = MTex(r"P=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\-\frac{1}{2}&\frac{1}{2}\end{pmatrix}", color = ORANGE).set_stroke(**stroke_dic).shift(4*LEFT + 3*UP)
        self.wait()
        self.play(FadeOut(self.shade))
        self.wait()

        shadows_1, shadows_2 = [], []
        def process(*extras: Animation):
            shadow = basis.copy()
            shadow[0].set_color(BLUE_E), shadow[1].set_color(GREEN_E)
            self.add_background(shadow[0], shadow[1])
            shadows_1.append(shadow[0]), shadows_2.append(shadow[1])
            self.play(*[RotateIn(mob) for mob in lines_h_a + lines_v_a + [basis]], *extras)
        process(Write(matrix))
        self.wait()

        vector = MTex(r"\vec{a}=\begin{pmatrix}1\\0\end{pmatrix}", color = BLUE).set_stroke(**stroke_dic).shift(4*LEFT + 2*DOWN)
        color_map = {r"P": ORANGE, r"\vec{a}": BLUE}
        labels = [MTex(r"\vec{a}", color = BLUE).move_to(2.4*RIGHT).set_stroke(**stroke_dic), MTex(r"P\vec{a}", tex_to_color_map = color_map).set_stroke(**stroke_dic).move_to(1.25*UR)]
        self.add_text(*labels).play(*[Write(mob) for mob in [vector] + labels])
        self.wait()

        i = 2
        new_label = MTex(r"P^2\vec{a}", tex_to_color_map = color_map).set_stroke(**stroke_dic).scale(2**(-(i-1)/2)).move_to(2.5*unit(i*PI/4)*2**(-i/2)).set_stroke(width = 8*2**(-(i-2)/2))
        source = VGroup(labels[1][0].copy(), labels[1][0].copy(), labels[1][1].copy(), labels[1][2].copy())
        self.add_text(source)
        process(ReplacementTransform(source, new_label))
        self.add_text(new_label)
        labels.append(new_label)
        self.wait()

        for _ in range(3):
            i += 1
            new_label = MTex(r"P^" + str(i) + r"\vec{a}", tex_to_color_map = color_map).set_stroke(**stroke_dic).scale(2**(-(i-1)/2)).move_to(2.6*unit(i*PI/4)*2**(-i/2)).set_stroke(width = 8*2**(-(i-2)/2))
            self.add_text(new_label)
            process(TransformFromCopy(labels[-1], new_label))
            labels.append(new_label)
            self.wait()
        for _ in range(8):
            i += 1
            new_label = MTex(r"P^{" + str(i) + r"}\vec{a}", tex_to_color_map = color_map).set_stroke(**stroke_dic).scale(2**(-(i-1)/2)).move_to(2.6*unit(i*PI/4)*2**(-i/2)).set_stroke(width = 8*2**(-(i-2)/2))
            self.add_text(new_label)
            process(TransformFromCopy(labels[-1], new_label))
            labels.append(new_label)
        self.remove().wait()

        curve = ParametricCurve(lambda t: 2*2**(2*t/PI)*unit(-t), [-2*TAU, PI, PI/100], color = YELLOW, stroke_width = 8)
        formula = MTex(r"\rho = e^{-\frac{2\theta}{\pi}}", tex_to_color_map = {r"\rho": RED, r"\theta": YELLOW}).next_to(2*RIGHT, DL).set_stroke(**stroke_dic)
        self.play(ShowCreation(curve, run_time = 2), Write(formula))
        self.wait()

        offset_l = LEFT_SIDE/2 + LEFT
        window = FloatWindow(height = 9, width = 15).shift(6.5*RIGHT)
        color_map = {(r"I", r"P"): ORANGE, r"\vec{a}": BLUE, r"\vec{s}": TEAL, r"\vec{x}": PURPLE_B}
        operators = [r"I", r"P"] + [r"P^{" + str(i) + r"}" for i in range(2, 11)]
        ratio = 0.25
        left, right, up, down = 1, 13, 11, 1
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 0.5 if i%4 else 2, color = GREY if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 0.5 if i%4 else 2, color = GREY if i else WHITE) for i in range(-left, right + 1)]
        offset_r = RIGHT_SIDE/2 + 1.5*LEFT + 0.5*DOWN + 2.2*LEFT
        small_coordinate = VGroup(*lines_h[:left], *lines_h[left+1:], *lines_v, lines_h[left]).shift(offset_r)
        series = MTex(r"\vec{s}=\left("+"+".join(operators[:4])+r"+\cdots\right)\vec{a}", tex_to_color_map = color_map).scale(0.8).next_to(3*UP + 0.5*LEFT)
        sequential = [shadows_1[i].copy().shift(offset_r + 2*UR + 2*np.sqrt(2)*unit((i-3)*PI/4)*2**(-i/2)) for i in range(len(shadows_1))]
        base_line = Polyline(*[offset_r + 2*UR + 2*np.sqrt(2)*unit((i-3)*PI/4)*2**(-i/2) for i in range(len(shadows_1) + 2)], stroke_width = 8, color = interpolate_color(BLUE_E, BLACK, 0.5))
        base_line_2 = Polyline(*[offset_r + 2*UR + 2*np.sqrt(2)*unit((i-3)*PI/4)*2**(-i/2) for i in range(len(shadows_1) + 2)], color = BLUE)
        sum_vector = Vector(2*UR, color = TEAL, stroke_width = 10).shift(offset_r)
        self.add_background(window, small_coordinate).play(*[mob.animate.shift(offset_l) for mob in lines_h_b + lines_v_b + lines_h_a + lines_v_a + shadows_1 + labels], 
                  *[OverFadeOut(mob, offset_l) for mob in [curve, formula] + shadows_2], 
                  *[mob.shift(8.5*RIGHT).animate.shift(8.5*LEFT) for mob in [window, series, small_coordinate]], run_time = 2)
        self.add_background(base_line, base_line_2, small_coordinate).play(
            LaggedStart(*[TransformFromCopy(shadows_1[i], sequential[i]) for i in range(len(shadows_1))], run_time = 2, lag_ratio = 1/3), 
            ShowCreation(base_line, run_time = 2), ShowCreation(base_line_2, run_time = 2))
        self.play(GrowArrow(sum_vector))
        self.play(FadeOut(sum_vector))
        self.wait()

        equation = MTex("+".join(operators[:4])+r"+\cdots=(I-P)^{-1}", tex_to_color_map = color_map).scale(0.8).shift(1.5*DOWN + RIGHT_SIDE/2 + 0.5*LEFT)
        self.play(Write(equation))
        self.wait()

        left, right, up, down = 1, 10, 11, 1
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 0.5 if i%4 else 2, color = GREY if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 0.5 if i%4 else 2, color = GREY if i else WHITE) for i in range(-left, right + 1)]
        offset_r_2 = RIGHT_SIDE/2 + 1.5*LEFT + 0.5*DOWN + 2.0*RIGHT
        # small_coordinate_2 = VGroup(*lines_h[:left], *lines_h[left+1:], *lines_v, lines_h[left]).shift(offset_r)
        # sum_vector_2 = Vector(2*UR, color = TEAL, stroke_width = 10).shift(offset_r)
        # label_s = MTex(r"\vec{s}", color = TEAL).next_to(offset_r_2 + 2*UR, UP).set_stroke(**stroke_dic)
        # inverse_sum = MTex(r"(I-P)\vec{s}=\vec{a}", tex_to_color_map = color_map).scale(0.8).next_to(1.5*DOWN + 3.5*RIGHT)
        # self.add_background(small_coordinate_2).play(*[mob.animate.shift(offset_r_2 - offset_r) for mob in [sum_vector_2, small_coordinate_2]], 
        #                                              follow(label_s, sum_vector_2, FadeIn), Write(inverse_sum))
        # self.wait()
        small_coordinate_2 = VGroup(*lines_h[:left], *lines_h[left+1:], *lines_v, lines_h[left]).shift(offset_r_2)
        sum_vector_2 = Vector(2*UR, color = PURPLE_B, stroke_width = 10).shift(offset_r_2)
        label_s = MTex(r"\vec{x}", color = PURPLE_B).next_to(offset_r_2 + 2*UR, UP).set_stroke(**stroke_dic)
        #inverse_sum = MTex(r"(I-P)\vec{s}=\vec{a}", tex_to_color_map = color_map).scale(0.8).next_to(1.5*DOWN + 3.5*RIGHT)
        self.add_background(small_coordinate_2).play(*[FadeIn(mob, 0.5*LEFT) for mob in [sum_vector_2, small_coordinate_2, label_s]])#, Write(inverse_sum))
        self.wait()

        ps = Vector(2*UP, color = PURPLE_B, stroke_width = 10).shift(offset_r_2)
        tex_ps = MTex(r"P\vec{x}", tex_to_color_map = color_map).next_to(offset_r_2 + 2*UP, UP).set_stroke(**stroke_dic)
        anim = TransformFromCopy(label_s, tex_ps[1:])
        self.play(TransformFromCopy(sum_vector_2, ps), anim, follow(tex_ps[0], anim, FadeIn))
        self.wait()

        subtraction = Vector(2*RIGHT, color = MAROON, stroke_width = 10).shift(offset_r_2 + 2*UP)
        self.play(GrowArrow(subtraction))
        tex_subtraction = MTex(r"(I-P)\vec{x}", tex_to_color_map = color_map).scale(0.8).next_to(subtraction, UP).shift(2*DOWN).set_stroke(**stroke_dic)
        subtraction_base = Vector(2*RIGHT, color = MAROON_E, stroke_width = 10).shift(offset_r_2 + 2*UP)
        self.add(subtraction_base, sum_vector_2, ps, subtraction).add_text(tex_subtraction).play(subtraction.animate.shift(2*DOWN), FadeIn(tex_subtraction, 2*DOWN))
        self.wait()

        copy_s = sum_vector_2.copy()
        self.play(Rotate(copy_s, -PI/4, about_point = offset_r_2))
        self.play(Transform(copy_s.save_state(), subtraction, remover = True))
        self.wait()

        # equation = MTex("+".join(operators[:4])+r"+\cdots=(I-P)^{-1}", tex_to_color_map = color_map).scale(0.8).shift(2.5*DOWN + RIGHT_SIDE/2 + 0.5*LEFT)
        # self.play(Write(equation))
        # self.wait()

        copy_a = subtraction.copy()
        self.play(Transform(copy_a, copy_s.restore()))
        self.play(Rotate(copy_a, PI/4, about_point = offset_r_2, remover = True))
        self.wait()

        inverse_sum = MTex(r"(I-P)\vec{s}=\vec{a}", tex_to_color_map = color_map).scale(0.8).next_to(2.5*DOWN + 0*RIGHT)
        a_1 = Vector(2*RIGHT, color = BLUE_E, stroke_width = 10).shift(offset_r)
        # copy_a = a_1.copy()
        self.play(Transform(a_1, sum_vector.copy().rotate(-PI/4, about_point = offset_r)), Write(inverse_sum))
        self.play(Rotate(a_1, PI/4, about_point = offset_r))
        self.play(Flash(offset_r + 2*UR))
        self.wait()

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        