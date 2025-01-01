from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Video_0(FrameScene):
    def construct(self):
        euler = MTex(r"e^{\pi i}+1=0").scale(2).set_stroke(**stroke_dic)
        self.play(Write(euler))
        self.wait()

        back_e, back_pi, back_i = BackgroundRectangle(euler[0], buff = 0.08, color = BLUE_E), BackgroundRectangle(euler[1], buff = 0.04, color = RED_E), BackgroundRectangle(euler[2], buff = 0.04, color = YELLOW_E)
        back_pi.match_height(back_i, stretch = True).match_y(back_i)
        self.add_background(back_e, back_pi, back_i).play(*[ShowCreation(mob) for mob in [back_e, back_pi, back_i]], 
                                                          euler[0].animate.set_fill(color = BLUE), euler[1].animate.set_fill(color = RED), euler[2].animate.set_fill(color = YELLOW))
        self.wait()
        notice_e, notice_pi, notice_i = Line(ORIGIN, 1*DOWN, color = BLUE_E), Line(ORIGIN, 0.5*UL, color = RED_E), Line(ORIGIN, 0.5*UR, color = YELLOW_E)
        notice_e.add(MTex("???", color = BLUE).next_to(notice_e, DOWN)).next_to(back_e, DOWN, buff = 0)
        notice_pi.add(MTex("???", color = RED).next_to(notice_pi, UL, buff = 0.1)).next_to(back_pi, UL, buff = 0)
        notice_i.add(MTex("???", color = YELLOW).next_to(notice_i, UR, buff = 0.1)).next_to(back_i, UR, buff = 0)
        self.play(*[GrowArrow(mob) for mob in [notice_e, notice_pi, notice_i]])
        self.wait()

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

class Video_1(FrameScene):
    def construct(self):

        zero, one = MTex("0")[0].scale(2).move_to(3*LEFT + 0.5*UP).set_stroke(**stroke_dic), MTex("1")[0].scale(2).move_to(3*RIGHT + 0.5*UP).set_stroke(**stroke_dic)
        zero_s, one_s = zero.copy().scale(7).set_fill(color = GREY_E), one.copy().scale(7).set_fill(color = GREY_E)
        self.add_background(zero_s).play(DrawBorderThenFill(zero), FadeIn(zero_s), run_time = 1)
        self.add_background(one_s).play(DrawBorderThenFill(one), FadeIn(one_s), run_time = 1)
        self.wait()

        meaning_0 = MTexText(r"$\bullet$无\\$\bullet$不存在\\$\bullet$没有", alignment = "").set_stroke(**stroke_dic).next_to(4*LEFT + 1.5*DOWN)
        meaning_1 = MTexText(r"$\bullet$单位").set_stroke(**stroke_dic).next_to(2*RIGHT + 1.5*DOWN)
        self.play(Write(meaning_0), run_time = 1)
        self.wait(1)
        self.play(Write(meaning_1))
        self.wait()

        target_0, target_1 = zero.copy().move_to(3*LEFT + DOWN).scale(0.8), one.copy().move_to(1.5*LEFT + DOWN).scale(0.8)
        self.play(Transform(zero, target_0), zero_s.animating(remover = True).become(target_0).set_opacity(0), 
                  Transform(one, target_1), one_s.animating(remover = True).become(target_1).set_opacity(0), 
                  meaning_0.animate.scale(1/2).next_to(3.5*LEFT + 2*DOWN, buff = 0.1), meaning_1.animate.scale(1/2).next_to(2*LEFT + 2*DOWN, buff = 0.1), run_time = 2)
        self.wait(1)

        plus = VGroup(Arrow(LEFT, 1.2*RIGHT, buff = 0), MTexText("加1").scale(1.2).next_to(ORIGIN, UP)).set_color(ORANGE).move_to(4*LEFT + 2*UP)
        self.play(FadeIn(plus, RIGHT), TransformFromCopy(zero, one.copy(), remover = True))
        self.wait(1)

        numbers = [zero, one]
        new_number = MTex("2")[0].scale(1.6).move_to(0*LEFT + DOWN).set_stroke(**stroke_dic)
        anims = [FadeOut(plus.copy(), RIGHT)]
        anims.append(numbers[0].copy().set_opacity(1/3).animating(remover = True, layer = self.backgrounds).become(numbers[1]).set_opacity(1/3))
        anims.append(TransformFromCopy(numbers[1], new_number))
        numbers.append(new_number)
        self.play(*anims)
        self.wait(1)

        for n in range(3, 9):
            new_number = MTex(str(n))[0].scale(1.6).move_to((-3+1.5*n)*RIGHT + DOWN).set_stroke(**stroke_dic)
            anims = [FadeOut(plus.copy(), RIGHT)]
            anims.extend([numbers[i].copy().set_opacity(1/3).animating(remover = True, layer = self.backgrounds, rate_func = less_smooth).become(numbers[i+1]).set_opacity(1/3) for i in range(n-1)])
            anims.append(TransformFromCopy(numbers[n-1], new_number, rate_func = less_smooth))
            numbers.append(new_number)
            self.play(*anims)
        self.wait(1)

        alien = SVGMobject("frog_face.svg", height = 1, stroke_width = 0).shift(5*LEFT + 0.2*UP)
        colon = MTex(":").next_to(alien)
        self.play(FadeIn(alien.add(colon), 0.5*RIGHT))
        self.wait()

        apple_0 = ImageMobject("apple_yellow.png", height = 1)
        apple_1 = ImageMobject("apple_white.png", height = 1)

        apples_1 = Group(apple_0.copy().move_to(1.5*LEFT + 0.2*UP))
        self.play(FadeIn(apples_1, 1.5*RIGHT), FadeOut(plus.copy(), RIGHT), rate_func = less_smooth)

        groups = [apples_1]
        for n in range(2, 8):
            new_apples = groups[-1].copy().set_opacity(0.5).shift(1.5*RIGHT)
            target = (apple_0 if n%2 else apple_1).move_to(new_apples[-1].copy()).shift(1.2*UP)
            self.play(FadeIn(new_apples, 1.5*RIGHT, rate_func = less_smooth), FadeIn(target, 1.5*RIGHT + 1.2*UP, rate_func = less_smooth), 
                      FadeOut(plus.copy(), RIGHT))
            self.remove(target)
            groups.append(new_apples.add(target.copy()))
        self.wait()

        minus = VGroup(Arrow(RIGHT, 1.2*LEFT, buff = 0), MTexText("减1").scale(1.2).next_to(ORIGIN, UP)).set_color(TEAL).move_to(2*LEFT + 2*UP)
        line = Line(8*LEFT, 8*RIGHT, stroke_width = 8)
        short_lines = [Line(0.3*UP, 0.3*DOWN, stroke_width = 8).shift((6-i)*1.5*RIGHT) for i in range(7)]
        self.play(*[mob.animate.shift(3*RIGHT) for mob in numbers], plus.animate.shift(6*RIGHT), FadeIn(minus, 6*RIGHT), 
                  *[OverFadeOut(mob, 3*RIGHT) for mob in [alien, meaning_0, meaning_1] + groups], OverFadeIn(line), 
                  *[OverFadeIn(mob, 3*RIGHT) for mob in short_lines], run_time = 2)
        self.wait()
        
        numbers = [numbers[6-i] for i in range(7)]
        for n in range(1, 7):
            new_number = VMobject(fill_opacity = 1, fill_color = WHITE, stroke_width = 8, stroke_color = BLACK, draw_stroke_behind_fill = True).set_points(MTex(str(-n)).scale(1.6).move_to((-1.5*n)*RIGHT + DOWN).get_all_points())
            new_short_line = Line(0.3*UP, 0.3*DOWN, stroke_width = 8).shift((-1.5*n)*RIGHT)
            anims = [FadeOut(minus.copy(), LEFT)]
            m = n+5
            anims.extend([numbers[i].copy().set_opacity(1/3).animating(remover = True, layer = self.backgrounds, rate_func = less_smooth).become(numbers[i+1]).set_opacity(1/3) for i in range(m)])
            anims.extend([short_lines[i].copy().set_opacity(1/3).animating(remover = True, layer = self.backgrounds, rate_func = less_smooth).become(short_lines[i+1]).set_opacity(1/3) for i in range(m)])
            anims.append(TransformFromCopy(numbers[m], new_number, rate_func = less_smooth))
            anims.append(TransformFromCopy(short_lines[m], new_short_line, rate_func = less_smooth))
            numbers.append(new_number), short_lines.append(new_short_line)
            self.play(*anims)
        self.wait(1)

        plus_example = MTex("+3", color = ORANGE).scale(2).shift(3*UP)
        self.remove(*short_lines)
        short_lines = VGroup(*[Line(0.3*UP, 0.3*DOWN, stroke_width = 8).shift(i*1.5*RIGHT) for i in range(-15, 15)]).save_state()
        self.add(short_lines).play(Write(plus_example), short_lines[15].animate.set_color(RED))
        self.play(short_lines.animating(run_time = 2).shift(3*1.5*RIGHT), LaggedStart(*[FadeOut(plus.copy(), RIGHT) for _ in range(3)], run_time = 2, lag_ratio = 1/2))
        self.wait()

        minus_example = MTex("-5", color = TEAL).scale(2).shift(3*UP)
        short_lines.generate_target()
        short_lines.target.set_color(WHITE)[11].set_color(YELLOW)
        self.play(Flip(plus_example, minus_example))
        self.play(short_lines.animating(run_time = 2).shift(5*1.5*LEFT), LaggedStart(*[FadeOut(minus.copy(), LEFT) for _ in range(4)], run_time = 2, lag_ratio = 1/4))
        self.wait()
        self.add(plus_example)

class Patch2_0(FrameScene):
    def construct(self):
        alien = SVGMobject("frog_face.svg", height = 1, stroke_width = 0).shift(5*LEFT)
        colon = MTex(":").next_to(alien)
        numbers = [MTex(str(n))[0].scale(1.6).move_to((-3+1.5*n)*RIGHT + 2*DOWN).set_stroke(**stroke_dic) for n in range(8)]

        apple_0 = ImageMobject("apple_yellow.png", height = 1)
        apple_1 = ImageMobject("apple_white.png", height = 1)

        apples_1 = Group(apple_0.copy().move_to(1.5*LEFT + 0.5*DOWN))

        groups = [apples_1]
        for n in range(2, 8):
            new_apples = groups[-1].copy().set_opacity(0.5).shift(1.5*RIGHT)
            target = (apple_0 if n%2 else apple_1).move_to(new_apples[-1].copy()).shift(1.2*UP)
            groups.append(new_apples.add(target.copy()))
        self.wait()
        self.add(*numbers, *groups, alien.add(colon))
        self.wait()

        minus = MTex("2-3=?").scale(1.6).next_to(2.5*UP + 5*LEFT)
        back = Rectangle(width = 1, height = 5.5, fill_color = GREY_E, **background_dic).shift(1.25*UP)
        surr = Square(side_length = 1).shift(2*DOWN)
        self.add_background(back, surr).play(Write(minus), back.save_state().scale(np.array([0, 1, 1])).animate.restore(), ShowCreation(surr))
        self.wait()

        shade = surr.copy().set_color(GREY_D)
        undefined = MTex(r"???", color = RED).scale(1.3).set_stroke(**stroke_dic).move_to(4.5*LEFT + 2*DOWN)
        self.add_background(shade, surr).play(surr.animate.shift(4.5*LEFT))
        self.wait(1)
        self.play(Write(undefined))
        self.wait()

class Patch2_1(FrameScene):
    def construct(self):
        minus = MTex("2-3=?").scale(1.6).next_to(2.5*UP + 2*LEFT)

        numbers = [MTex(str(i)).scale(1.6).shift(i*1.5*RIGHT + DOWN) for i in range(10)]
        line = Line(ORIGIN, 12*RIGHT, stroke_width = 8)
        short_lines = [Line(0.3*UP, 0.3*DOWN, stroke_width = 8).shift(i*1.5*RIGHT) for i in range(10)]
        axis_0 = VGroup(line, *short_lines)
        axis_back = axis_0.copy().set_color(GREY)
        axis_undefined = axis_0.copy().set_color(RED_E)
        axis_undefined[3].set_color(ORANGE)
        axis_half = axis_0.copy()
        axis_half[3].set_color(YELLOW)
        for mob in axis_half:
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_1")
            mob.uniforms["mask_x"] = -0.04
        self.add(minus, axis_back, axis_undefined, axis_half, *numbers).wait()
        self.play(*[mob.animate.shift(4.5*LEFT) for mob in [axis_undefined, axis_half]], run_time = 2)
        self.wait()

class Patch2_2(FrameScene):
    def construct(self):
        minus = MTex("2-3=-1").scale(1.6).next_to(2.5*UP + 2*LEFT)

        numbers = [MTex(str(i)).scale(1.6).shift(i*1.5*RIGHT + DOWN) for i in range(-10, 10)]
        line = Line(12*LEFT, 12*RIGHT, stroke_width = 8)
        short_lines = [Line(0.3*UP, 0.3*DOWN, stroke_width = 8).shift(i*1.5*RIGHT) for i in range(-10, 10)]
        axis_0 = VGroup(line, *short_lines)
        axis_back = axis_0.copy().set_color(GREY)
        axis_half = axis_0.copy()
        axis_half[13].set_color(YELLOW)
        self.add(minus, axis_back, axis_half, *numbers).wait()
        self.play(*[mob.animate.shift(4.5*LEFT) for mob in [axis_half]], run_time = 2)
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

class Video_2_0(FrameScene):
    def construct(self):
        definition = MTex(r"i=\sqrt{-1}", tex_to_color_map = {"i": YELLOW, r"\sqrt{-1}": GOLD}).scale(2).set_stroke(**stroke_dic)
        part_0, part_1 = definition[0].save_state(), definition[1:]
        part_0.set_x(0)
        back = part_0.copy().scale(8).move_to(0.5*UP).set_fill(color = GREY_E)
        for mob in part_1:
            mob.fill_shader_wrapper.reset_shader("mask_fill_r")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_r")
            mob.uniforms["mask_x"] = part_1.get_x(LEFT) - 0.05
        part_1.save_state().match_x(part_0, RIGHT)
        for mob in part_1:
            mob.uniforms["mask_x"] = part_1.get_x(RIGHT) + 0.05
        self.add_background(back).play(DrawBorderThenFill(part_0), FadeIn(back), run_time = 1)
        self.wait()
        self.play(part_0.animate.restore(), part_1.animate.restore())
        for mob in part_1:
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        self.wait()

        bob = SVGMobject("Bob.svg", height = 3, color = BLUE, **background_dic).rotate(-PI/6).shift(3*DOWN + 6*LEFT)
        text = Songti("这么做没有意义！\n负数不能开平方！", color = BLUE).scale(0.8).shift(0*DOWN + 5*LEFT)
        line = Line(bob.get_corner(UR) + 0.2*UP + 0.3*LEFT, text.get_corner(DOWN) + 0.2*DOWN, color = BLUE)
        self.play(bob.shift(2.5*DL).animate.shift(2.5*UR), *[GrowFromPoint(mob, LEFT_SIDE + 4*DOWN) for mob in [text, line]])
        self.wait()

        window = FloatWindow(width = 16).shift(DOWN*0.5)
        text_title = Songti(r"数字的扩张", color = YELLOW).shift(1.5*UP)
        text_1 = MTex(r"\mathbb{C}=\mathbb{R}[i]=\mathbb{R}[x]/(x^2+1)", tex_to_color_map = {r"\mathbb{C}": GOLD, r"\mathbb{R}": BLUE_E, (r"i", r"x"): YELLOW}).shift(0.5*UP)
        text_2 = MTex(r"4+4x+x^2\equiv 3+4x\ (\bmod\  1 + x^2)", tex_to_color_map = {r"x": YELLOW}).shift(0.5*DOWN)
        self.add_text(self.shade, window).play(window.add(text_title, text_1, text_2).shift(8*DOWN).animate.shift(8*UP), FadeIn(self.shade.set_opacity(0.8)), run_time = 2)
        self.wait()

        self.remove(bob, text, line, definition)
        title_left, title_right = MTexText("不引入$i=\sqrt{-1}$", tex_to_color_map = {"i": YELLOW, r"\sqrt{-1}": GOLD}).set_stroke(**stroke_dic).shift(3*LEFT + 2.5*UP), MTexText("引入$i=\sqrt{-1}$", tex_to_color_map = {"i": YELLOW, r"\sqrt{-1}": GOLD}).set_stroke(**stroke_dic).shift(3*RIGHT + 2.5*UP)
        explain_left, explain_right = Heiti("维持复数没有平方根的性质").scale(0.6).next_to(title_left, DOWN).set_stroke(**stroke_dic), Heiti("更多知识和更优美的数学结构").set_stroke(**stroke_dic).scale(0.6).next_to(title_right, DOWN)
        self.add(title_left.add(explain_left), title_right.add(explain_right)).play(window.animate.shift(8*DOWN), FadeOut(self.shade), run_time = 2)
        self.wait()

        quadratic_1 = MTex("ax^2+bx+c=0", tex_to_color_map = {(r"a", r"b", r"c"): GREEN, "x": BLUE}).set_stroke(**stroke_dic).shift(0.5*UP + 3*LEFT)
        quadratic_2 = MTex("\Delta=b^2-4ac", tex_to_color_map = {r"\Delta": ORANGE, (r"a", r"b", r"c"): GREEN}).set_stroke(**stroke_dic).next_to(quadratic_1, DOWN)
        quadratic_3 = MTex(r"\Delta>0\ :\ &2\text{个实根}\\\Delta=0\ :\ &1\text{个实根}\\\Delta<0\ :\ &0\text{个实根}", tex_to_color_map = {r"\Delta": ORANGE}).set_stroke(**stroke_dic).scale(0.6).next_to(quadratic_2, DOWN)
        quadratic = VGroup(quadratic_1, quadratic_2, quadratic_3)

        cubic_1 = MTex("x^3+px+q=0", tex_to_color_map = {(r"p", r"q"): GREEN, "x": BLUE}).set_stroke(**stroke_dic).shift(0.5*UP + 3*RIGHT)
        cubic_2 = MTex("\Delta=-4p^3-27q^2", tex_to_color_map = {r"\Delta": ORANGE, (r"p", r"q"): GREEN}).set_stroke(**stroke_dic).next_to(cubic_1, DOWN)
        cubic_3 = MTex(r"\Delta>0\ :\ &3\text{个实根}\\\Delta=0\ :\ &\text{有重根}\\\Delta<0\ :\ &1\text{个实根}", tex_to_color_map = {r"\Delta": ORANGE}).set_stroke(**stroke_dic).scale(0.6).next_to(cubic_2, DOWN)
        cubic = VGroup(cubic_1, cubic_2, cubic_3)

        self.play(title_left.animate.shift(3*RIGHT), title_right.save_state().animate.shift(2*RIGHT).scale(0.6).fade())
        self.play(FadeIn(quadratic, UP), FadeIn(cubic, UP))
        self.wait()

        example_cubic = MTex("x^3-15x-4=0", tex_to_color_map = {(r"15", r"4"): GREEN, "x": BLUE}).set_stroke(**stroke_dic).shift(1*UP)
        solution_1 = MTex("x_1=\sqrt[3]{2+\sqrt{-121}}+\sqrt[3]{2-\sqrt{-121}}", tex_to_color_map = {"x_1": BLUE, "\sqrt{-121}": RED}).set_stroke(**stroke_dic).scale(0.8).next_to(example_cubic, DOWN, buff = 0.5)
        self.play(FadeOut(quadratic), FadeOut(cubic), run_time = 0.5)
        self.play(FadeIn(example_cubic), FadeIn(solution_1))
        self.wait()

        failure = [SurroundingRectangle(mob) for mob in solution_1.get_parts_by_tex("\sqrt{-121}")]
        self.play(*[ShowCreation(mob) for mob in failure])
        self.wait()

def number(i):
            if i == 1:
                return ""
            elif i == -1:
                return "-"
            else:
                return str(i)
            
class Video_2(FrameScene):
    def construct(self):
        i_symbol = MTex(r"i", color = YELLOW)[0].scale(2).set_stroke(**stroke_dic)
        background_i = i_symbol.copy().scale(8).move_to(0.5*UP).set_fill(color = GREY_E)
        self.add_background(background_i).play(DrawBorderThenFill(i_symbol), FadeIn(background_i), run_time = 1)
        self.wait()

        back = Mobject(shader_folder = "test5", render_primitive = moderngl.TRIANGLES).set_points([UR, UL, DR, DL])
        back.shader_indices = np.array([0, 1, 2, 1, 2, 3])
        back.uniforms.update({"opacity": 0.0, "center": 0.0})
        back.generate_target().uniforms["opacity"] = 1.0
        i_sqrt = MTex(r"i=\sqrt{-1}", tex_to_color_map = {"i": YELLOW, r"\sqrt{-1}": GOLD}).scale(2).set_stroke(**stroke_dic).move_to(2*UP + 3*LEFT)
        barrages = [ImageMobject(str(i)+".png").set_width(7).shift(3*RIGHT + 2*UP + 0.75*(i-2)*DOWN) for i in (1, 2, 3)]
        self.bring_to_back(back).play(MoveToTarget(back), ReplacementTransform(i_symbol, i_sqrt[0]), 
                                      LaggedStart(*[FadeIn(mob, LEFT) for mob in barrages], lag_ratio = 0.5, run_time = 1))
        book_1 = LabelPicture("book.png", "人教A版数学必修二　第七章复数　第68页", picture_config = {"height": 4/3}).shift(3*RIGHT + 1.5*DOWN)
        self.play(FadeIn(book_1, UP))
        self.wait()

        alpha = ValueTracker(0.0)
        def shift_updater(mob: VMobject):
            mob.shift(alpha.get_value()*LEFT)
        i_sqrt.add_post_updater(shift_updater)
        self.play(Write(i_sqrt[1:]), alpha.animate.set_value(1))
        i_sqrt.clear_post_updaters().shift(LEFT)
        cancel = Line(i_sqrt.get_left() + 0.2*LEFT, i_sqrt.get_right() + 0.2*RIGHT, color = RED)#.match_y(i_sqrt[1])
        back_cancel = cancel.copy().set_stroke(color = BLACK, width = 12)
        self.add(i_sqrt).play(ShowCreation(back_cancel), ShowCreation(cancel))
        self.wait()

        i_square = MTex("i^2=-1", tex_to_color_map = {"i": YELLOW, r"-1": RED}).scale(2).set_stroke(**stroke_dic).move_to(4*LEFT).match_y(book_1[0])
        self.play(Write(i_square))
        self.wait()

        window = FloatWindow(width = 15, height = 10, 
                             outer_dic = {"fill_opacity": 1, "fill_color": "#222222", "stroke_color": WHITE}, 
                             inner_dic = {"fill_opacity": 1,  "fill_color": BLACK, "stroke_color": YELLOW_E})
        offset_l = 3.5*LEFT + 2.5*DOWN
        ratio = 0.8
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(offset_l)
        label_0 = MTex("0").scale(0.8).set_stroke(**stroke_dic).next_to(offset_l, DL, buff = 0.1)
        labels_real = [MTex(str(i)).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + i*ratio*RIGHT, DOWN, buff = 0.1) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + i*ratio*UP, LEFT, buff = 0.1) for i in range(-down, up + 1) if i != 0] 
        labels = VGroup(label_0, *labels_real, *labels_imag)
        back.generate_target().shift(7.5/(64/9)*RIGHT).uniforms["center"] = 2.0
        self.bring_to_back(complex_plane, labels, window).play(*[mob.animate.shift(7.5*RIGHT) for mob in [window, i_sqrt, i_square, back_cancel, cancel]],
                                        *[FadeOut(mob, 7.5*RIGHT) for mob in [book_1, *barrages]], 
                                        MoveToTarget(back), background_i.animate.shift(RIGHT_SIDE/2), run_time = 2)
        self.wait()

class Video2_2(FrameScene):
    def construct(self):
        window = FloatWindow(width = 15, height = 10, 
                             outer_dic = {"fill_opacity": 1, "fill_color": "#222222", "stroke_color": WHITE}, 
                             inner_dic = {"fill_opacity": 1,  "fill_color": BLACK, "stroke_color": YELLOW_E}).shift(7.5*RIGHT)
        i_symbol = MTex(r"i", color = GREY_E)[0].scale(16).move_to(0.5*UP + RIGHT_SIDE/2).set_stroke(**stroke_dic)
        offset_l = 3.5*LEFT + 2.5*DOWN
        ratio = 0.8
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(offset_l)
        label_0 = MTex("0").scale(0.8).set_stroke(**stroke_dic).next_to(offset_l, DL, buff = 0.1)
        labels_real = [MTex(str(i)).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + i*ratio*RIGHT, DOWN, buff = 0.1) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).next_to(offset_l + i*ratio*UP, LEFT, buff = 0.1) for i in range(-down, up + 1) if i != 0] 
        labels = VGroup(label_0, *labels_real, *labels_imag)
        self.add_background(complex_plane, labels).add_lower(window, i_symbol).wait()

        def coor(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP + offset_l
        def relative(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP
        vec_1 = Vector(relative(2, 1), color = BLUE).shift(offset_l)
        vec_2 = Vector(relative(1, 3), color = GREEN).shift(offset_l)
        label_1 = MTex("a+bi", color = BLUE).scale(0.8).next_to(coor(2, 1), UR, buff = 0.1).set_stroke(**stroke_dic)
        label_2 = MTex("c+di", color = GREEN).scale(0.8).next_to(coor(1, 3), UR, buff = 0.1).set_stroke(**stroke_dic)
        self.play(ShowCreation(vec_1), ShowCreation(vec_2))
        self.play(Write(label_1), Write(label_2))
        self.wait()

        mul_0 = MTex(r"=(a+bi)(c+di)", tex_to_color_map = {r"a+bi": BLUE, r"c+di": GREEN}).set_stroke(**stroke_dic)
        mul_0.shift(RIGHT + 3*UP - mul_0[0].get_center()).remove(mul_0[0])
        def path_func_copy(start: np.ndarray, end: np.ndarray, alpha: float):
            factor = unit(alpha*PI/2)**0.5
            factor_starts, factor_ends = np.array([factor[0], 1 - factor[1], 0]), np.array([1 - factor[0], factor[1], 0])
            return start*factor_starts + end*factor_ends
        def path_func(start: np.ndarray, end: np.ndarray, alpha: float):
            factor = unit(alpha*PI/2)**0.5
            factor_starts, factor_ends = np.array([1 - factor[1], factor[0], 0]), np.array([factor[1], 1 - factor[0], 0])
            return start*factor_starts + end*factor_ends
        
        anim_1, anim_2 = TransformFromCopy(label_1, mul_0[1:5], path_func = path_func_copy), TransformFromCopy(label_2, mul_0[7:11], path_func = path_func_copy, run_time = 1.5, rate_func = squish_rate_func(smooth, 0, 2/3))
        self.play(anim_1, follow(mul_0[0], anim_1, OverFadeIn, path_func = path_func), follow(mul_0[5], anim_1, OverFadeIn, path_func = path_func), 
                  anim_2, follow(mul_0[6], anim_2, OverFadeIn, path_func = path_func, delay = 0.5), follow(mul_0[11], anim_2, OverFadeIn, path_func = path_func, delay = 0.5), frames = 45)
        # self.wait(1, 15)

        mul_1 = MTex(r"=ac+adi+bci+bdi^2", tex_to_color_map = {r"a": BLUE, r"c": GREEN, r"b": BLUE, r"d": GREEN, r"i": YELLOW}).set_stroke(**stroke_dic)
        mul_1.shift(RIGHT + 2.25*UP - mul_1[0].get_center())
        def anim_gen(i, j):
            if j == -1:
                return Write(mul_1[i])
            else:
                return TransformFromCopy(mul_0[j], mul_1[i])
        j_s = [-1, 1, 7, -1, 1, 9, 10, -1, 3, 7, 4, -1, 3, 9, 4, 10]
        self.play(LaggedStart(*[anim_gen(i, j) for i, j in enumerate(j_s)], lag_ratio = 1/3, run_time = 2))
        self.add(mul_1)#.wait()

        mul_2 = MTex(r"=(ac-bd)+(ad+bc)i", tex_to_color_map = {r"a": BLUE, r"c": GREEN, r"b": BLUE, r"d": GREEN, r"i": YELLOW}).set_stroke(**stroke_dic)
        mul_2.shift(RIGHT + 1.5*UP - mul_2[0].get_center())
        def anim_gen(i, j):
            if j == -1:
                return Write(mul_2[i])
            elif isinstance(j, int):
                return TransformFromCopy(mul_1[j], mul_2[i])
            else:
                return TransformFromCopy(mul_1[j[0]:j[1]], mul_2[i[0]:i[1]], remover = True)
        ij_s = [(0, -1), (1, -1), ((2, 4), (1, 3)), ((4, 5), (14, 16)), ((5, 7), (12, 14)), (7, -1), (8, -1), (9, -1), ((10, 12), (4, 6)), (12, -1), ((13, 15), (8, 10)), (15, -1), (16, -1)]
        self.play(LaggedStart(*[anim_gen(i, j) for i, j in ij_s], lag_ratio = 1/3, run_time = 2, remover = True))
        self.add(mul_2).wait()

        for mob in mul_1:
            mob.fill_shader_wrapper.reset_shader("mask_fill_u")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_u")
            mob.uniforms["mask_u"] = 2.625
        vec_3 = Vector(relative(-1, 7), color = TEAL).shift(offset_l)
        label_3 = MTex("(ac-bd)+(ad+bc)i", color = TEAL).scale(0.8).next_to(coor(-1, 7), UP, buff = 0.1).set_stroke(**stroke_dic)
        self.play(TransformFromCopy(mul_2[1:], label_3), ShowCreation(vec_3))
        self.wait()

        equation = MTex(r"|a+bi||c+di|=|(ac-bd)+(ad+bc)i|", tex_to_color_map = {r"a+bi": BLUE, r"c+di": GREEN, r"(ac-bd)+(ad+bc)i": TEAL}).set_stroke(**stroke_dic)
        equation.scale(0.7).shift(RIGHT_SIDE/2 + 1.3*UP)
        self.play(mul_1.animating(remover = True).shift(0.75*UP), mul_2.animate.shift(0.75*UP), FadeIn(equation, 0.75*UP))
        self.wait()

        texs = r"(ac-bd)^2+(ad+bc)^2", r"a^2c^2-2abcd+b^2d^2+a^2d^2+2abcd+b^2c^2", r"a^2c^2+b^2d^2+a^2d^2+b^2c^2", r"(a^2+b^2)(c^2+d^2)"
        calculate = MTex(r"&\ "+texs[0]+r"\\=&\ "+texs[1]+r"\\=&\ "+texs[2]+r"\\=&\ "+texs[3], isolate = [*texs, r"="], tex_to_color_map = {r"a": BLUE, r"c": GREEN, r"b": BLUE, r"d": GREEN}).set_stroke(**stroke_dic)
        calculate.scale(0.7).shift(RIGHT_SIDE/2 + 0.5*DOWN)
        parts, equals = [calculate.get_part_by_tex(tex) for tex in texs], calculate.get_parts_by_tex("=")
        anim_1, anim_2 = TransformFromCopy(equation[14:21], parts[0][:7]), TransformFromCopy(equation[22:29], parts[0][9:16])
        self.play(anim_1, anim_2, follow(parts[0][7], anim_1, OverFadeIn), follow(parts[0][16], anim_2, OverFadeIn), TransformFromCopy(equation[21], parts[0][8]))
        self.add(parts[0])#.wait()
        self.play(Write(VGroup(equals[0], *parts[1])))
        # self.wait()
        subparts_1 = [parts[1][:4], parts[1][10:15], parts[1][15:20], parts[1][26:]]#, parts[1][4:10], parts[1][26:]
        cancels = [parts[1][4:10], parts[1][20:26]]
        lines = [Line(mob.get_corner(DL), mob.get_corner(UR), color = RED) for mob in cancels]
        subparts_2 = [parts[2][:4], parts[2][4:9], parts[2][9:14], parts[2][14:]]
        self.add(*subparts_1).play(Write(equals[1]), *[mob.animate.set_fill(color = GREY) for mob in cancels], *[ShowCreation(line) for line in lines], 
                  LaggedStart(*[TransformFromCopy(mob_1, mob_2) for mob_1, mob_2 in zip(subparts_1, subparts_2)], lag_ratio = 1/3, run_time = 2))
        self.play(Write(VGroup(equals[2], *parts[3])))
        self.wait()

        texs = r"(a^2+b^2)(c^2+d^2)", r"\ge", r"(ad+bc)^2"
        cauchy = MTex(r" ".join(texs), isolate = texs, tex_to_color_map = {r"a": BLUE, r"c": GREEN, r"b": BLUE, r"d": GREEN}).set_stroke(**stroke_dic)
        cauchy.scale(0.7).shift(RIGHT_SIDE/2 + 2*DOWN)
        parts_cauchy = [cauchy.get_part_by_tex(tex) for tex in texs]
        self.play(TransformFromCopy(parts[3], parts_cauchy[0]), Write(parts_cauchy[1]), TransformFromCopy(parts[0][9:], parts_cauchy[2]))
        self.wait()
        tex_cauchy = Songti(r"柯西不等式", color = YELLOW).scale(0.6).next_to(cauchy, DOWN, buff = 0.1)
        self.play(Write(tex_cauchy))
        self.wait()

        new_offset_l = 4.2*LEFT + 1*DOWN
        new_ratio = 1.5
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*new_ratio*LEFT + i*new_ratio*DOWN, (right+0.5)*new_ratio*RIGHT + i*new_ratio*DOWN, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*new_ratio*UP + i*new_ratio*RIGHT, (down+0.5)*new_ratio*DOWN + i*new_ratio*RIGHT, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane.target = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(new_offset_l)
        new_stroke_dic = {r"width": 20, r"color": BLACK, r"background": True}
        label_0 = MTex("0").set_stroke(**new_stroke_dic).next_to(new_offset_l, DL, buff = 0.2)
        labels_real = [MTex(str(i)).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*RIGHT, DOWN, buff = 0.2) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*UP, LEFT, buff = 0.2) for i in range(-down, up + 1) if i != 0] 
        labels.target = VGroup(label_0, *labels_real, *labels_imag)
        def coor(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP + new_offset_l
        def relative(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP
        vec_1.target = Vector(relative(2, 1), color = BLUE, stroke_width = 10).shift(new_offset_l)
        vec_2.target = Vector(relative(1, 3), color = GREEN, stroke_width = 10).shift(new_offset_l).set_opacity(0.0)
        vec_3.target = Vector(relative(-1, 7), color = TEAL, stroke_width = 10).shift(new_offset_l).set_opacity(0.0)
        label_1.target = MTex("a+bi", color = BLUE).next_to(coor(2, 1), UR, buff = 0.1).set_stroke(**stroke_dic).set_opacity(0.0)
        label_2.target = MTex("c+di", color = GREEN).next_to(coor(1, 3), UR, buff = 0.1).set_stroke(**stroke_dic).set_opacity(0.0)
        label_3.target = MTex("(ac-bd)+(ad+bc)i", color = TEAL).next_to(coor(-1, 7), UP, buff = 0.1).set_stroke(**stroke_dic).set_opacity(0.0)
        
        self.add_background(vec_1, vec_2, vec_3, label_1, label_2, label_3).add(mul_0, mul_2, equation, calculate, cauchy, tex_cauchy, *lines
                            ).play(*[FadeOut(mob) for mob in [mul_0, mul_2, equation, calculate, cauchy, tex_cauchy, *lines]], 
                                   *[MoveToTarget(mob) for mob in [complex_plane, labels, vec_1, vec_2, vec_3, label_1, label_2, label_3]], run_time = 2)
        self.remove(vec_2, vec_3, label_1, label_2, label_3).wait()

class Video2_3(FrameScene):
    def construct(self):
        window = FloatWindow(width = 15, height = 10, 
                             outer_dic = {"fill_opacity": 1, "fill_color": "#222222", "stroke_color": WHITE}, 
                             inner_dic = {"fill_opacity": 1,  "fill_color": BLACK, "stroke_color": YELLOW_E}).shift(7.5*RIGHT)
        i_symbol = MTex(r"i", color = GREY_E)[0].scale(16).move_to(0.5*UP + RIGHT_SIDE/2).set_stroke(**stroke_dic)
        offset_l = 4.8*LEFT + 1*DOWN
        ratio = 1.5
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(offset_l)
        new_stroke_dic = {r"width": 20, r"color": BLACK, r"background": True}
        label_0 = MTex("0").set_stroke(**new_stroke_dic).next_to(offset_l, DL, buff = 0.2)
        labels_real = [MTex(str(i)).set_stroke(**new_stroke_dic).next_to(offset_l + i*ratio*RIGHT, DOWN, buff = 0.2) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).set_stroke(**new_stroke_dic).next_to(offset_l + i*ratio*UP, LEFT, buff = 0.2) for i in range(-down, up + 1) if i != 0] 
        labels = VGroup(label_0, *labels_real, *labels_imag)
        
        def coor(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP + offset_l
        def relative(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP
        vec_1 = Vector(relative(2, 1), color = BLUE, stroke_width = 10).shift(offset_l)
        self.add_background(complex_plane, labels).add_lower(window, i_symbol, vec_1).wait()

        triangle = Polygon(coor(0, 0), coor(2, 0), coor(2, 1), stroke_width = 0, fill_color = BLUE, fill_opacity = 0.2)
        r = MTex(r"r", color = BLUE).set_stroke(**stroke_dic).next_to(coor(1, 0.5), UL, buff = 0.1)
        angle = np.arctan(1/2)
        theta_arc = Arc(angle = angle, radius = 0.8, start_angle = 0).shift(coor(0, 0))
        theta = MTex(r"\theta", color = BLUE).set_stroke(**stroke_dic).scale(0.8).shift(coor(0, 0) + 1.0*unit(angle/2))
        z = MTex(r"z", color = BLUE).set_stroke(**stroke_dic).next_to(coor(2, 1), UR, buff = 0.1)
        self.add_background(triangle, theta_arc).play(FadeIn(triangle), Write(r), ShowCreation(theta_arc), Write(theta), Write(z))
        self.wait()

        tex_cos = MTex(r"r\cos\theta", tex_to_color_map = {r"r": RED, r"\cos\theta": RED}).set_stroke(**new_stroke_dic).next_to(triangle, DOWN, buff = 0.15)
        line_cos = Line(coor(0, 0), coor(2, 0), stroke_width = 8, color = RED)
        tex_sin = MTex(r"r\sin\theta", tex_to_color_map = {r"r": ORANGE, r"\sin\theta": ORANGE}).set_stroke(**new_stroke_dic).next_to(triangle, RIGHT, buff = 0.15)
        line_sin = Line(coor(2, 0), coor(2, 1), stroke_width = 8, color = ORANGE)

        self.add_lower(line_cos, vec_1).play(Write(tex_cos), ShowCreation(line_cos))
        self.wait()
        self.add_lower(line_sin, vec_1).play(Write(tex_sin), ShowCreation(line_sin))
        self.wait()

        tex_z = MTex(r"z=r\cos\theta+r\sin\theta i", tex_to_color_map = {(r"r", r"z", r"\theta"): BLUE, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).set_stroke(**stroke_dic).shift(RIGHT_SIDE/2 + 2*UP)
        self.play(Write(VGroup(tex_z[0], tex_z[1], tex_z[7], tex_z[13])), TransformFromCopy(tex_cos, tex_z[2:7]), TransformFromCopy(tex_sin, tex_z[8:13]))
        self.wait()

        tex_z_2 = MTex(r"=r(\cos\theta+\sin\theta i)", tex_to_color_map = {(r"r", r"z", r"\theta"): BLUE, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).set_stroke(**stroke_dic)
        tex_z_2.shift(tex_z[1].get_center() - tex_z_2[0].get_center() + DOWN)
        anim = TransformFromCopy(tex_z[1], tex_z_2[0])
        self.play(anim, TransformFromCopy(tex_z[2], tex_z_2[1]), TransformFromCopy(tex_z[8], tex_z_2[1].copy(), remover = True), follow(tex_z_2[2], anim, OverFadeIn),  follow(tex_z_2[13], anim, OverFadeIn))
        # self.wait()
        self.play(TransformFromCopy(tex_z[3:8], tex_z_2[3:8]), TransformFromCopy(tex_z[9:14], tex_z_2[8:13]))
        self.wait()

        indicate = SurroundingRectangle(tex_z_2[2:], color = YELLOW)
        notice = MTexText(r"不需要使用$e^{i\theta}=\cos\theta+\sin\theta i$", tex_to_color_map = {r"e": BLUE, r"i": YELLOW, r"\cos": RED, r"\sin": ORANGE, r"\theta": BLUE}).scale(0.5).next_to(indicate, DOWN, buff = 0.1).set_stroke(**stroke_dic)
        self.add_text(indicate).play(ShowCreation(indicate), Write(notice))
        self.wait()

        vec_2 = Vector(relative(1, 3), color = GREEN, stroke_width = 10, stroke_opacity = 0).shift(offset_l)
        r_2 = MTex(r"r_2", color = GREEN).set_stroke(**stroke_dic).set_opacity(0).next_to(coor(0.5, 1.5), UL, buff = 0.1)
        angle_2 = np.arctan(3)
        beta_arc = Arc(angle = angle_2, radius = 0.4, start_angle = 0).set_opacity(0).shift(coor(0, 0))
        beta = MTex(r"\beta", color = GREEN).set_stroke(**stroke_dic).set_opacity(0).scale(0.8).shift(coor(0, 0) + 0.7*unit((angle_2 + angle)/2))
        z_2 = MTex(r"z_2", color = GREEN).set_stroke(**stroke_dic).set_opacity(0).next_to(coor(1, 3), UR, buff = 0.1)
        new_offset_l = 3.5*LEFT + 2.5*DOWN
        new_ratio = 0.8
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*new_ratio*LEFT + i*new_ratio*DOWN, (right+0.5)*new_ratio*RIGHT + i*new_ratio*DOWN, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*new_ratio*UP + i*new_ratio*RIGHT, (down+0.5)*new_ratio*DOWN + i*new_ratio*RIGHT, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane.target = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(new_offset_l)
        new_stroke_dic = {r"width": 8, r"color": BLACK, r"background": True}
        label_0 = MTex("0").scale(0.8).set_stroke(**new_stroke_dic).next_to(new_offset_l, DL, buff = 0.2)
        labels_real = [MTex(str(i)).scale(0.8).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*RIGHT, DOWN, buff = 0.2) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).scale(0.8).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*UP, LEFT, buff = 0.2) for i in range(-down, up + 1) if i != 0] 
        labels.target = VGroup(label_0, *labels_real, *labels_imag)
        def coor(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP + new_offset_l
        def relative(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP
        vec_1.target = Vector(relative(2, 1), color = BLUE).shift(new_offset_l)
        triangle.target = Polygon(coor(0, 0), coor(2, 0), coor(2, 1), stroke_width = 0, fill_color = BLUE, fill_opacity = 0)
        r.add(r[0].copy()).target = MTex(r"r_1", color = BLUE).scale(0.8).set_stroke(**stroke_dic).next_to(coor(1, 0.5), UP, buff = 0.16)
        angle_1 = np.arctan(1/2)
        theta_arc.target = Arc(angle = angle_1, radius = 0.8, start_angle = 0).shift(coor(0, 0))
        theta.target = MTex(r"\alpha", color = BLUE).set_stroke(**stroke_dic).scale(0.8).shift(coor(0, 0) + 1.0*unit(angle/2))
        z.add(z[0].copy()).target = MTex(r"z_1", color = BLUE).set_stroke(**stroke_dic).scale(0.8).next_to(coor(2, 1), UR, buff = 0.1)
        r_1, alpha, alpha_arc, z_1 = r, theta, theta_arc, z
        tex_cos.target = MTex(r"r\cos\alpha", tex_to_color_map = {r"r": RED, r"\cos\alpha": RED}).set_stroke(**new_stroke_dic).scale(0.6).next_to(triangle.target, DOWN, buff = 0.15).set_opacity(0)
        line_cos.target = Line(coor(0, 0), coor(2, 0), stroke_width = 0, color = RED)
        tex_sin.target = MTex(r"r\sin\alpha", tex_to_color_map = {r"r": ORANGE, r"\sin\alpha": ORANGE}).set_stroke(**new_stroke_dic).scale(0.6).next_to(triangle.target, RIGHT, buff = 0.15).set_opacity(0)
        line_sin.target = Line(coor(2, 0), coor(2, 1), stroke_width = 0, color = ORANGE)
        
        vec_2.target = Vector(relative(1, 3), color = GREEN).shift(new_offset_l)
        r_2.target = MTex(r"r_2", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(coor(0.5, 1.5), UL, buff = 0.1)
        beta_arc.target = Arc(angle = angle_2, radius = 0.4, start_angle = 0).shift(coor(0, 0))
        beta.target = MTex(r"\beta", color = GREEN).set_stroke(**stroke_dic).scale(0.8).shift(coor(0, 0) + 0.7*unit((angle_2 + angle_1)/2))
        z_2.target = MTex(r"z_2", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(coor(1, 3), UR, buff = 0.1)
        # vec_2.target = Vector(relative(1, 3), color = GREEN, stroke_width = 10).shift(new_offset_l).set_opacity(0.0)
        # vec_3.target = Vector(relative(-1, 7), color = TEAL, stroke_width = 10).shift(new_offset_l).set_opacity(0.0)
        # label_1.target = MTex("a+bi", color = BLUE).next_to(coor(2, 1), UR, buff = 0.1).set_stroke(**stroke_dic).set_opacity(0.0)
        # label_2.target = MTex("c+di", color = GREEN).next_to(coor(1, 3), UR, buff = 0.1).set_stroke(**stroke_dic).set_opacity(0.0)
        # label_3.target = MTex("(ac-bd)+(ad+bc)i", color = TEAL).next_to(coor(-1, 7), UP, buff = 0.1).set_stroke(**stroke_dic).set_opacity(0.0)
        
        self.add_lower(alpha_arc, beta_arc, line_cos, line_sin, vec_1, vec_2, r_1, r_2, alpha, beta
            ).play(*[FadeOut(mob) for mob in [tex_z, tex_z_2, indicate, notice]], 
                *[MoveToTarget(mob) for mob in [complex_plane, labels, vec_1, triangle, r_1, alpha, alpha_arc, z_1, tex_cos, line_cos, tex_sin, line_sin, vec_2, r_2, beta_arc, beta, z_2]], run_time = 2)
        tex_z1, tex_z2 = MTex(r"z_1=r_1(\cos\alpha+\sin\alpha i)", tex_to_color_map = {(r"r_1", r"z_1", r"\alpha"): BLUE, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).set_stroke(**stroke_dic), MTex(r"z_2=r_2(\cos\beta+\sin\beta i)", tex_to_color_map = {(r"r_2", r"z_2", r"\beta"): GREEN, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).set_stroke(**stroke_dic)
        tex_z1.shift(RIGHT_SIDE/2 + 2.75*UP), tex_z2.shift(RIGHT_SIDE/2 + 2*UP)
        self.remove(tex_cos, line_cos, tex_sin, line_sin).play(Write(tex_z1), Write(tex_z2))
        self.wait()

        cal_0 = MTex(r"=z_1z_2", tex_to_color_map = {r"z_1": BLUE, r"z_2": GREEN}).set_stroke(**stroke_dic)
        cal_0.scale(0.8).shift(1*UP + 0.5*RIGHT - cal_0[0].get_center()).remove(cal_0[0])
        cal_1 = MTex(r"=r_1r_2(\cos\alpha+\sin\alpha i)(\cos\beta+\sin\beta i)", tex_to_color_map = {(r"r_1", r"z_1", r"\alpha"): BLUE, (r"r_2", r"z_2", r"\beta"): GREEN, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).set_stroke(**stroke_dic)
        cal_1.scale(0.8).shift(0.4*UP + 0.5*RIGHT - cal_1[0].get_center())
        self.play(Write(VGroup(*cal_0, cal_1[0])))
        self.play(TransformFromCopy(tex_z1[3:5], cal_1[1:3]), TransformFromCopy(tex_z2[3:5], cal_1[3:5]))
        self.play(TransformFromCopy(tex_z1[5:], cal_1[5:17]), TransformFromCopy(tex_z2[5:], cal_1[17:29]))
        self.wait()

        cal_2 = MTex(r"=r_1r_2((\cos\alpha\cos\beta-\sin\alpha\sin\beta)+(\cos\alpha\sin\beta +\sin\alpha\cos\beta) i)", tex_to_color_map = {(r"r_1", r"\alpha"): BLUE, (r"r_2", r"\beta"): GREEN, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).set_stroke(**stroke_dic)  
        cal_2.scale(0.8).shift(0.2*DOWN + 0.5*RIGHT - cal_2[0].get_center())
        cal_2[25:].shift(cal_2[6].get_center() - cal_2[26].get_center() + 0.6*DOWN)
        def anim_gen(i, j):
            if j == -1:
                return Write(cal_2[i])
            elif isinstance(j, int):
                return TransformFromCopy(cal_1[i], cal_2[j])
            else:
                return TransformFromCopy(cal_1[i[0]:i[1]], cal_2[j[0]:j[1]])
        ij_s = [(0, -1), ((1,3), (1,3)), ((3,5), (3,5)), (5, -1), (6, -1), ((6,10), (7,11)), ((18,22), (11,15)), (15, -1), ((11,15), (16,20)), ((23,27), (20,24)), (24, -1), 
                (25, -1), (26, -1), ((6,10), (27,31)), ((23,27), (31,35)), (35, -1), ((11,15), (36,40)), ((23,27), (40,44)), (44, -1), (45, -1), (46, -1)]
        self.play(LaggedStart(*[anim_gen(i, j) for i, j in ij_s], lag_ratio = 1/3, run_time = 3))
        self.wait()
        # self.add(cal_1, index_labels(cal_1))
        # self.add(cal_2, index_labels(cal_2))

        back_1, back_2 = BackgroundRectangle(cal_2[6:25], fill_color = RED_E, buff = 0.05, fill_opacity = 0.2), BackgroundRectangle(cal_2[26:45], fill_color = TEAL_E, buff = 0.05, fill_opacity = 0.2)
        cal_3 = MTex(r"=r_1r_2(\cos(\alpha+\beta)+\sin(\alpha+\beta)i)", tex_to_color_map = {(r"r_1", r"\alpha"): BLUE, (r"r_2", r"\beta"): GREEN, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).set_stroke(**stroke_dic)
        cal_3.scale(0.8).shift(1.4*DOWN + 0.5*RIGHT - cal_3[0].get_center())
        back_3, back_4 = BackgroundRectangle(cal_3[6:14], fill_color = RED_E, buff = 0.05, fill_opacity = 0.2), BackgroundRectangle(cal_3[15:23], fill_color = TEAL_E, buff = 0.05, fill_opacity = 0.2)
        self.add_lower(back_1, back_2, back_3, back_4).play(FadeIn(back_1), FadeIn(back_2), Write(cal_3), FadeIn(back_3, delay = 1), FadeIn(back_4, delay = 1))
        self.wait()

        vec_3 = Vector(relative(-1, 7), color = TEAL).shift(new_offset_l)
        r_3 = MTex(r"r_1r_2", color = TEAL).scale(0.8).set_stroke(**stroke_dic).next_to(coor(-0.5, 3.5), DL, buff = 0.1)
        angle_3 = angle_1 + angle_2
        theta_arc = Arc(angle = angle_3, radius = 0.2, start_angle = 0).shift(coor(0, 0))
        position = coor(0, 0) + 0.1*unit(angle_3/2)
        dot_arc = Dot(radius = 0.04, color = WHITE).set_stroke(width = 4, color = BLACK, background = True).move_to(position)
        theta = MTex(r"\alpha + \beta", color = TEAL).set_stroke(**stroke_dic).scale(0.8).shift(position + 0.5*DOWN)#.next_to(theta_arc, DOWN, buff = 0.4)#.shift(coor(0, 0) + 0.4* DOWN)
        line_arc, shadow_line = Line(position, theta, stroke_width = 3, color = WHITE), Line(position, theta, stroke_width = 6, color = BLACK) 
        line_arc.uniforms["anti_alias_width"] = 0
        z_3 = MTex(r"z_1z_2", color = TEAL).scale(0.8).set_stroke(**stroke_dic).next_to(coor(-1, 7), UL, buff = 0.1)
        self.play(ShowCreation(vec_3), Write(z_3))
        self.add(theta_arc, vec_3).play(TransformFromCopy(cal_3[1:5], r_3), ShowCreation(theta_arc), TransformFromCopy(cal_3[10:13], theta), TransformFromCopy(cal_3[19:22], theta.copy(), remover = True), shadow_line.save_state().scale(0, about_point = position).set_stroke(width = 0).animate.restore(), GrowFromCenter(dot_arc), line_arc.save_state().scale(0, about_point = position).set_stroke(width = 0).animate.restore())
        self.wait()

        self.play(*[WiggleOutThenIn(mob) for mob in [back_1, back_2, back_3, back_4, cal_2[6:25], cal_2[26:45], cal_3[6:14], cal_3[15:23]]])
        self.wait()

        i_square = MTex(r"i^2=-1", tex_to_color_map = {r"i": YELLOW, r"-1": RED}).shift(3*UP + RIGHT_SIDE/2).set_stroke(**stroke_dic)
        self.play(FadeIn(i_square, DOWN), *[mob.animate.shift(0.8*DOWN) for mob in [tex_z1, tex_z2]], *[mob.animate.shift(0.6*DOWN) for mob in [cal_0, cal_1, cal_2, cal_3, back_1, back_2, back_3, back_4]])
        self.wait()

        new_offset_l = 4.2*LEFT + 1.5*DOWN
        new_ratio = 1.5
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*new_ratio*LEFT + i*new_ratio*DOWN, (right+0.5)*new_ratio*RIGHT + i*new_ratio*DOWN, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*new_ratio*UP + i*new_ratio*RIGHT, (down+0.5)*new_ratio*DOWN + i*new_ratio*RIGHT, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane.target = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(new_offset_l)
        new_stroke_dic = {r"width": 20, r"color": BLACK, r"background": True}
        label_0 = MTex("0").set_stroke(**new_stroke_dic).next_to(new_offset_l, DL, buff = 0.2)
        labels_real = [MTex(str(i)).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*RIGHT, DOWN, buff = 0.2) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*UP, LEFT, buff = 0.2) for i in range(-down, up + 1) if i != 0] 
        labels.target = VGroup(label_0, *labels_real, *labels_imag)
        def coor(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP + new_offset_l
        def relative(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP
        
        vec_1.target = Vector(relative(2, 1), color = BLUE).shift(new_offset_l).set_opacity(0)
        r_1.target = MTex(r"r_1", color = BLUE).set_stroke(**stroke_dic).next_to(coor(1, 0.5), UL, buff = 0.1).set_opacity(0)
        alpha_arc.target = Arc(angle = angle_1, radius = 0.8, start_angle = 0).shift(coor(0, 0)).set_opacity(0)
        alpha.target = MTex(r"\alpha", color = BLUE).set_stroke(**stroke_dic).shift(coor(0, 0) + 1.0*unit(angle_1/2)).set_opacity(0)
        z_1.target = MTex(r"z_1", color = BLUE).set_stroke(**stroke_dic).next_to(coor(2, 1), UR, buff = 0.1).set_opacity(0)
        vec_2.target = Vector(relative(1, 3), color = GREEN).shift(new_offset_l).set_opacity(0)
        r_2.target = MTex(r"r_2", color = GREEN).set_stroke(**stroke_dic).next_to(coor(0.5, 1.5), UL, buff = 0.1).set_opacity(0)
        beta_arc.target = Arc(angle = angle_2, radius = 0.4, start_angle = 0).shift(coor(0, 0)).set_opacity(0)
        beta.target = MTex(r"\beta", color = GREEN).set_stroke(**stroke_dic).shift(coor(0, 0) + 0.7*unit((angle_2 + angle_1)/2)).set_opacity(0)
        z_2.target = MTex(r"z_2", color = GREEN).set_stroke(**stroke_dic).next_to(coor(1, 3), UR, buff = 0.1).set_opacity(0)
        vec_3.target = Vector(relative(-1, 7), color = TEAL).shift(new_offset_l).set_opacity(0)
        r_3.target = MTex(r"r_1r_2", color = TEAL).set_stroke(**stroke_dic).next_to(coor(-0.5, 3.5), DL, buff = 0.1).set_opacity(0)
        theta_arc.target = Arc(angle = angle_3, radius = 0.2, start_angle = 0).shift(coor(0, 0)).set_opacity(0)
        position = coor(0, 0) + 0.1*unit(angle_3/2)
        dot_arc.target = Dot(radius = 0.04, color = WHITE).set_stroke(width = 4, color = BLACK, background = True).move_to(position).set_opacity(0)
        theta.target = MTex(r"\alpha + \beta", color = TEAL).set_stroke(**stroke_dic).shift(position + 0.5*DOWN).set_opacity(0)
        line_arc.target, shadow_line.target = Line(position, theta.target, stroke_width = 3, color = WHITE).set_opacity(0), Line(position, theta.target, stroke_width = 6, color = BLACK).set_opacity(0)
        line_arc.target.uniforms["anti_alias_width"] = 0
        z_3.target = MTex(r"z_1z_2", color = TEAL).set_stroke(**stroke_dic).next_to(coor(-1, 7), UL, buff = 0.1).set_opacity(0)

        self.play(*[FadeOut(mob) for mob in [tex_z1, tex_z2, cal_0, cal_1, cal_2, cal_3, back_1, back_2, back_3, back_4]],
            *[MoveToTarget(mob) for mob in [complex_plane, labels, vec_1, r_1, alpha_arc, alpha, z_1, vec_2, r_2, beta_arc, beta, z_2, vec_3, r_3, theta_arc, dot_arc, theta, line_arc, shadow_line, z_3]], run_time = 2)
        self.wait()
        
class Video2_4(FrameScene):
    def construct(self):
        window = FloatWindow(width = 15, height = 10, 
                             outer_dic = {"fill_opacity": 1, "fill_color": "#222222", "stroke_color": WHITE}, 
                             inner_dic = {"fill_opacity": 1,  "fill_color": BLACK, "stroke_color": YELLOW_E}).shift(7.5*RIGHT)
        i_symbol = MTex(r"i", color = GREY_E)[0].scale(16).move_to(0.5*UP + RIGHT_SIDE/2).set_stroke(**stroke_dic)
        i_square = MTex(r"i^2=-1", tex_to_color_map = {r"i": YELLOW, r"-1": RED}).shift(3*UP + RIGHT_SIDE/2).set_stroke(**stroke_dic)
        offset_l = 4.2*LEFT + 1.5*DOWN
        ratio = 1.5
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 2 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(offset_l)
        new_stroke_dic = {r"width": 20, r"color": BLACK, r"background": True}
        label_0 = MTex("0").set_stroke(**new_stroke_dic).next_to(offset_l, DL, buff = 0.2)
        labels_real = [MTex(str(i)).set_stroke(**new_stroke_dic).next_to(offset_l + i*ratio*RIGHT, DOWN, buff = 0.2) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).set_stroke(**new_stroke_dic).next_to(offset_l + i*ratio*UP, LEFT, buff = 0.2) for i in range(-down, up + 1) if i != 0] 
        labels = VGroup(label_0, *labels_real, *labels_imag)
        
        def coor(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP + offset_l
        def relative(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP
        self.add_background(complex_plane, labels).add_lower(window, i_symbol).add(i_square).wait()

        tex_u_1 = MTex(r"u = a+bi", tex_to_color_map = {r"u": BLUE, r"a": GREEN, r"b": RED, r"i": YELLOW}).set_stroke(**stroke_dic).shift(2*UP + RIGHT_SIDE/2)
        self.play(Write(tex_u_1))
        self.wait()

        new_stroke_dic = {r"width": 12, r"color": BLACK, r"background": True}
        line_a = Line(coor(0, 0), coor(2, 0), stroke_width = 8, color = GREEN)
        label_a = MTex(r"a", tex_to_color_map = {r"a": GREEN}).set_stroke(**new_stroke_dic).next_to(line_a, DOWN, buff = 0.2)
        line_b = Line(coor(2, 0), coor(2, 1), stroke_width = 8, color = RED)
        label_b = MTex(r"b", tex_to_color_map = {r"b": RED}).set_stroke(**new_stroke_dic).next_to(line_b, RIGHT, buff = 0.2)
        vec_1 = Vector(relative(2, 1), color = BLUE, stroke_width = 10).shift(offset_l)
        u = MTex(r"u", color = BLUE).set_stroke(**stroke_dic).next_to(coor(2, 1), UR, buff = 0.1)
        
        dot = Dot(color = YELLOW).set_stroke(**stroke_dic).shift(coor(0, 0))
        self.play(dot.save_state().scale(0).set_stroke(width = 0).animate.restore())
        # self.wait(1)
        self.add(line_a, dot).play(ShowCreation(line_a), dot.animate.move_to(coor(2, 0)), Write(label_a))
        # self.wait(1)
        self.add(line_b, dot).play(ShowCreation(line_b), dot.animate.move_to(coor(2, 1)), Write(label_b))
        self.wait(1)
        self.play(ShowCreation(vec_1), Write(u), dot.animating(remover = True).scale(0).set_stroke(width = 0))
        self.wait()

        tex_u_2 = MTex(r"iu = ai+bi^2", tex_to_color_map = {r"u": BLUE, r"a": GREEN, r"b": RED, r"i": YELLOW}).set_stroke(**stroke_dic)
        tex_u_2.shift(tex_u_1[1].get_center() - tex_u_2[2].get_center() + 0.75*DOWN)
        tex_u_3 = MTex(r"=-b+ai", tex_to_color_map = {r"u": BLUE, r"a": GREEN, r"b": RED, r"i": YELLOW}).set_stroke(**stroke_dic)
        tex_u_3.shift(tex_u_2[2].get_center() - tex_u_3[0].get_center() + 0.75*DOWN)
        anim = TransformFromCopy(tex_u_1[0], tex_u_2[1])
        self.play(anim, follow(tex_u_2[0], anim, OverFadeIn), TransformFromCopy(tex_u_1[1], tex_u_2[2]))
        self.play(Write(tex_u_2[3:]))
        def anim_gen(i, j):
            if j == -1:
                return Write(tex_u_3[i], remover = True)
            elif isinstance(i, int):
                return TransformFromCopy(tex_u_2[i], tex_u_3[j].copy(), remover = True)
            else:
                # return TransformFromCopy(tex_z_2[i[0]:i[1]], tex_z_3[j[0]:j[1]], remover = True)
                return TransformFromCopy(tex_u_2[i[0]:i[1]], VGroup(tex_u_3[1], tex_u_3[1].copy()), remover = True)
        ij_s = [(0, -1), ((7, 8), 1), (6, 2), (5, 3), (3, 4), (4, 5)]
        self.play(LaggedStart(*[anim_gen(i, j) for i, j in ij_s], lag_ratio = 1/3, run_time = 2, remover = True))
        self.add(tex_u_3).wait()

        line_ai = Line(coor(0, 0), coor(0, 2), stroke_width = 8, color = GREEN)
        label_ai = MTex(r"a", tex_to_color_map = {r"a": GREEN}).set_stroke(**new_stroke_dic).next_to(line_ai, RIGHT, buff = 0.2)
        line_bi = Line(coor(0, 2), coor(-1, 2), stroke_width = 8, color = RED)
        label_bi = MTex(r"b", tex_to_color_map = {r"b": RED}).set_stroke(**new_stroke_dic).next_to(line_bi, UP, buff = 0.2)
        vec_2 = Vector(relative(-1, 2), color = BLUE, stroke_width = 10).shift(offset_l)
        ui = MTex(r"iu", tex_to_color_map = {r"i": YELLOW, r"u": BLUE}).set_stroke(**stroke_dic).next_to(coor(-1, 2), UL, buff = 0.1)
        
        dot = Dot(color = YELLOW).set_stroke(**stroke_dic).shift(coor(0, 0))
        self.play(dot.save_state().scale(0).set_stroke(width = 0).animate.restore())
        # self.wait(1)
        self.add(line_ai, vec_1, dot).play(ShowCreation(line_ai), dot.animate.move_to(coor(0, 2)), Write(label_ai))
        # self.wait(1)
        self.add(line_bi, vec_1, dot).play(ShowCreation(line_bi), dot.animate.move_to(coor(-1, 2)), Write(label_bi))
        self.wait(1)
        self.play(ShowCreation(vec_2), Write(ui), dot.animating(remover = True).scale(0).set_stroke(width = 0))
        self.wait()

        half_opacity = 1 - 0.8**(1/2)
        triangle_u, triangle_ui = Polygon(coor(0, 0), coor(2, 0), coor(2, 1), stroke_width = 0, fill_color = BLUE, fill_opacity = 0.2), Polygon(coor(0, 0), coor(0, 2), coor(-1, 2), stroke_width = 0, fill_color = BLUE, fill_opacity = 0.2)
        self.add_background(triangle_u, triangle_ui).play(FadeIn(triangle_u), FadeIn(triangle_ui))
        self.wait()

        copy_triangle = triangle_u.copy().set_fill(color = BLUE, opacity = half_opacity)
        copy_line_a, copy_line_b, copy_label_a, copy_label_b = line_a.copy(), line_b.copy(), label_a.copy(), label_b.copy()
        self.add_background(copy_triangle).add(copy_line_a, copy_line_b, vec_1, vec_2).add_text(label_a, label_b, label_ai, label_bi, copy_label_a, copy_label_b).play(
                  Transform(copy_line_a, line_ai, path_arc = PI/2, remover = True), 
                  Transform(copy_line_b, line_bi, path_arc = PI/2, remover = True),
                  Transform(copy_label_a, label_ai, path_arc = PI/2, remover = True),
                  Transform(copy_label_b, label_bi, path_arc = PI/2, remover = True),
                  copy_triangle.animating(path_arc = PI/2, remover = True).rotate(PI/2, about_point = coor(0, 0)), 
                  triangle_u.set_fill(opacity = half_opacity).animate.set_fill(opacity = 0.2),
                  triangle_ui.animate.set_fill(opacity = half_opacity), run_time = 2)
        triangle_ui.set_fill(opacity = 0.2)
        self.wait()

        point = Point(np.array([2, 1, 0]))
        def geometry_updater(mob: VGroup):
            p = point.get_location()
            p0, p1, p2, p3, p4 = coor(0, 0), coor(p[0], 0), coor(p[0], p[1]), coor(0, p[0]), coor(-p[1], p[0])
            mob[0].set_points_as_corners([p0, p1, p2, p0])
            mob[1].set_points_as_corners([p0, p3, p4, p0])
            mob[2].put_start_and_end_on(p0, p1)
            mob[3].put_start_and_end_on(p1, p2)
            mob[4].put_start_and_end_on(p0, p3)
            mob[5].put_start_and_end_on(p3, p4)
            mob[6].put_start_and_end_on(p0, p2)
            mob[7].put_start_and_end_on(p0, p4)
        group_geometry = VGroup(triangle_u, triangle_ui, line_a, line_b, line_ai, line_bi, vec_1, vec_2).add_updater(geometry_updater)
        def tex_updater(mob: VGroup):
            p = point.get_location()
            d = [UP if p[1] < 0 else DOWN, LEFT if p[0] < 0 else RIGHT, LEFT if p[1] < 0 else RIGHT, DOWN if p[0] < 0 else UP]
            mob[0].next_to(line_a, d[0], buff = 0.2)
            mob[1].next_to(line_b, d[1], buff = 0.2)
            mob[2].next_to(line_ai, d[2], buff = 0.2)
            mob[3].next_to(line_bi, d[3], buff = 0.2)
            mob[4].next_to(coor(p[0], p[1]), d[1]-d[0], buff = 0.1)
            mob[5].next_to(coor(-p[1], p[0]), d[3]-d[2], buff = 0.1)
        group_texs = VGroup(label_a, label_b, label_ai, label_bi, u, ui).add_updater(tex_updater)
        self.add(group_geometry).add_text(group_texs).play(point.animate.set_location(np.array([np.sqrt(2), np.sqrt(2), 0])))
        self.wait(1)
        self.play(point.animate.set_location(np.array([np.sqrt(2), -np.sqrt(2), 0])), path_arc = -PI/2)
        self.wait(1)
        self.play(point.animate.set_location(np.array([-1, -0.5, 0])), path_arc = -PI/2)
        self.wait(1)
        self.play(point.animate.set_location(np.array([2, 1, 0])), path_arc = -PI, run_time = 2)
        for mob in [group_geometry, group_texs]:
            mob.clear_updaters()
        self.wait()
        
        text_i = MTexText("乘$i$：逆时针旋转$90$度", tex_to_color_map = {("i", "90"): YELLOW}).set_stroke(**stroke_dic).shift(RIGHT_SIDE/2 + 1.5*DOWN)
        arrow = Arrow(0.6*relative(2, 1), 0.6*relative(-1, 2), path_arc = PI/2, color = YELLOW, stroke_width = 8).shift(coor(0, 0))
        angle = MTex(r"90^\circ", color = YELLOW).scale(0.8).set_stroke(**stroke_dic).shift(coor(0, 0) + 2.4*unit(np.arctan(3)))
        self.play(ShowCreation(arrow), Write(angle), Write(text_i))
        self.wait()

        indicate = SurroundingRectangle(VGroup(tex_u_2, tex_u_3))
        notice = MTex(r"1\times i = i, i\times i = -1", tex_to_color_map = {r"1": GREEN, r"i": YELLOW, r"-1": RED}).scale(0.8).set_stroke(**stroke_dic).next_to(indicate, DOWN)
        self.play(ShowCreation(indicate), Write(notice))
        self.wait()

        new_offset_l = 4*LEFT + 2.5*DOWN
        new_ratio = 0.8
        left, right, up, down = 8, 8, 15, 10
        lines_h = [Line((left+0.5)*new_ratio*LEFT + i*new_ratio*DOWN, (right+0.5)*new_ratio*RIGHT + i*new_ratio*DOWN, stroke_width = 1 if i else 3, color = GREY if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*new_ratio*UP + i*new_ratio*RIGHT, (down+0.5)*new_ratio*DOWN + i*new_ratio*RIGHT, stroke_width = 1 if i else 3, color = GREY if i else WHITE) for i in range(-left, right + 1)]
        complex_plane.target = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(new_offset_l)
        new_stroke_dic = {r"width": 8, r"color": BLACK, r"background": True}
        label_0 = MTex("0").scale(0.8).set_stroke(**new_stroke_dic).shift(new_offset_l + 0.25*new_ratio*np.array([1, -2, 0]) + 0.25*new_ratio*np.array([-2, -1, 0]))
        labels_real = [MTex(str(i)).scale(0.8).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*RIGHT, DOWN, buff = 0.2).set_opacity(0) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).scale(0.8).set_stroke(**new_stroke_dic).next_to(new_offset_l + i*new_ratio*UP, LEFT, buff = 0.1).set_opacity(0) for i in range(-down, up + 1) if i != 0] 
        labels.target = VGroup(label_0, *labels_real, *labels_imag)
        def coor(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP + new_offset_l
        def relative(x: float, y: float):
            return x*new_ratio*RIGHT + y*new_ratio*UP
        
        # triangle_u, triangle_ui, line_a, line_b, line_ai, line_bi, vec_1, vec_2
        # label_a, label_b, label_ai, label_bi, u, ui
        # arrow, angle
        triangle_u.target = Polygon(coor(0, 0), coor(2, 0), coor(2, 1), stroke_width = 0, fill_color = BLUE, fill_opacity = 0)
        triangle_ui.target = Polygon(coor(0, 0), coor(0, 2), coor(-1, 2), stroke_width = 0, fill_color = BLUE, fill_opacity = 0)
        line_a.target = Line(coor(0, 0), coor(2, 0), stroke_width = 0, color = WHITE)
        line_b.target = Line(coor(2, 0), coor(2, 1), stroke_width = 0, color = GREY)
        line_ai.target = Line(coor(0, 0), coor(0, 2), stroke_width = 0, color = WHITE)
        line_bi.target = Line(coor(0, 2), coor(-1, 2), stroke_width = 0, color = WHITE)
        vec_1.target = Vector(relative(2, 1), color = BLUE, stroke_width = 10).shift(new_offset_l)
        vec_2.target = Vector(relative(-1, 2), color = BLUE, stroke_width = 10).shift(new_offset_l)
        label_a.target = MTex(r"a", tex_to_color_map = {r"a": GREEN}).scale(0.8).set_stroke(**new_stroke_dic).next_to(line_a.target, DOWN, buff = 0.2).set_opacity(0)
        label_b.target = MTex(r"b", tex_to_color_map = {r"b": RED}).scale(0.8).set_stroke(**new_stroke_dic).next_to(line_b.target, RIGHT, buff = 0.2).set_opacity(0)
        label_ai.target = MTex(r"a", tex_to_color_map = {r"a": GREEN}).scale(0.8).set_stroke(**new_stroke_dic).next_to(line_ai.target, RIGHT, buff = 0.2).set_opacity(0)
        label_bi.target = MTex(r"b", tex_to_color_map = {r"b": RED}).scale(0.8).set_stroke(**new_stroke_dic).next_to(line_bi.target, UP, buff = 0.2).set_opacity(0)
        u.target = MTex(r"u", color = BLUE).scale(0.8).set_stroke(**stroke_dic).shift(coor(2, 1) + 0.25*new_ratio*np.array([1, -2, 0]))
        ui.target = MTex(r"iu", tex_to_color_map = {r"i": YELLOW, r"u": BLUE}).scale(0.8).set_stroke(**stroke_dic).shift(coor(-1, 2) + 0.25*new_ratio*np.array([-2, -1, 0]))
        arrow.target = Arrow(0.6*relative(2, 1), 0.6*relative(-1, 2), path_arc = PI/2, color = YELLOW, stroke_width = 8).shift(coor(0, 0))
        angle.target = MTex(r"90^\circ", color = YELLOW).scale(0.8).set_stroke(**stroke_dic).shift(coor(0, 0) + 1.6*unit(np.arctan(3)))
        
        tex_u_2.generate_target().shift(1.25*UP)
        indicate.target = SurroundingRectangle(tex_u_2.target).set_opacity(0)
        mask_u = indicate.get_y(UP) - 0.05 #-4#tex_u_2.get_y(UP) + 0.05
        for mob in tex_u_2:
            mob.fill_shader_wrapper.reset_shader("mask_fill_u")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_u")
            mob.uniforms["mask_u"] = mask_u
        for mob in tex_u_2.target:
            mob.fill_shader_wrapper.reset_shader("mask_fill_u")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_u")
            mob.shift(0.75*UP)
            mob.uniforms["mask_u"] = mask_u + 1.25
        tex_u_2.target[0].shift(0.75*DOWN), tex_u_2.target[1].shift(0.75*DOWN)
        # notice.generate_target().next_to(indicate.target, DOWN).set_opacity(0)
        self.play(*[MoveToTarget(mob, remover = True, run_time = 2) for mob in [triangle_u, triangle_ui, line_a, line_b, line_ai, line_bi, label_a, label_b, label_ai, label_bi, indicate]], 
                  *[MoveToTarget(mob, run_time = 2) for mob in [complex_plane, labels, vec_1, vec_2, u, ui, arrow, angle]], 
                  OverFadeOut(i_square, 0.5*UP), tex_u_1.animate.shift(1.25*UP), MoveToTarget(tex_u_2), tex_u_3.animate.shift(2*UP), OverFadeOut(notice, 2*UP), text_i.animate.set_y(1.75), run_time = 2)
        for mob in [tex_u_2[0], tex_u_2[1]]:
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        tex_u_3.set_submobjects([tex_u_2[0], tex_u_2[1], *tex_u_3])
        self.remove(tex_u_2).add(tex_u_3).wait()

class Video2_5(FrameScene):
    def construct(self):

        window = FloatWindow(width = 15, height = 10, 
                             outer_dic = {"fill_opacity": 1, "fill_color": "#222222", "stroke_color": WHITE}, 
                             inner_dic = {"fill_opacity": 1,  "fill_color": BLACK, "stroke_color": YELLOW_E}).shift(7.5*RIGHT)
        i_symbol = MTex(r"i", color = GREY_E)[0].scale(16).move_to(0.5*UP + RIGHT_SIDE/2).set_stroke(**stroke_dic)
        
        offset_l = 4*LEFT + 2.5*DOWN
        ratio = 0.8
        unit_l, unit_r, unit_u, unit_d = ratio*LEFT, ratio*RIGHT, ratio*UP, ratio*DOWN
        left, right, up, down = 8, 8, 15, 10
        bound_l, bound_r, bound_u, bound_d = (left+0.5)*unit_l, (right+0.5)*unit_r, (up+0.5)*unit_u, (down+0.5)*unit_d
        lines_h = [Line(bound_l + i*unit_d, bound_r + i*unit_d, stroke_width = 1 if i else 3, color = GREY if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line(bound_u + i*unit_r, bound_d + i*unit_r, stroke_width = 1 if i else 3, color = GREY if i else WHITE) for i in range(-left, right + 1)]
        complex_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(offset_l)
        label_0 = MTex("0").scale(0.8).set_stroke(**stroke_dic).shift(offset_l + 0.25*ratio*np.array([1, -2, 0]) + 0.25*ratio*np.array([-2, -1, 0])) #.next_to(offset_l, DL, buff = 0.2).shift(0.1*RIGHT)
        def coor(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP + offset_l
        def relative(x: float, y: float):
            return x*ratio*RIGHT + y*ratio*UP
        u = MTex(r"u", color = BLUE).scale(0.8).set_stroke(**stroke_dic).shift(coor(2, 1) + 0.25*ratio*np.array([1, -2, 0]))#.next_to(coor(2, 1), DR, buff = 0.1)
        ui = MTex(r"iu", tex_to_color_map = {r"i": YELLOW, r"u": BLUE}).scale(0.8).set_stroke(**stroke_dic).shift(coor(-1, 2) + 0.25*ratio*np.array([-2, -1, 0]))#.next_to(coor(-1, 2), DL, buff = 0.1)
        vec_1 = Vector(relative(2, 1), color = BLUE, stroke_width = 10).shift(offset_l)
        vec_2 = Vector(relative(-1, 2), color = BLUE, stroke_width = 10).shift(offset_l)
        arrow = Arrow(0.6*relative(2, 1), 0.6*relative(-1, 2), path_arc = PI/2, color = YELLOW, stroke_width = 8).shift(coor(0, 0))
        angle = MTex(r"90^\circ", color = YELLOW).scale(0.8).set_stroke(**stroke_dic).shift(coor(0, 0) + 1.6*unit(np.arctan(3)))

        tex_u_1 = MTex(r"u = a+bi", tex_to_color_map = {r"u": BLUE, r"a": GREEN, r"b": RED, r"i": YELLOW}).set_stroke(**stroke_dic).shift(3.25*UP + RIGHT_SIDE/2)
        tex_u_2 = MTex(r"iu = -b+ai", tex_to_color_map = {r"u": BLUE, r"a": GREEN, r"b": RED, r"i": YELLOW}).set_stroke(**stroke_dic)
        tex_u_2.shift(tex_u_1[1].get_center() - tex_u_2[2].get_center() + 0.75*DOWN)
        text_i = MTexText("乘$i$：逆时针旋转$90$度", tex_to_color_map = {("i", "90"): YELLOW}).set_stroke(**stroke_dic).shift(RIGHT_SIDE/2 + 1.75*UP)
        self.add_background(complex_plane).add_lower(window, i_symbol).add(label_0, u, ui, vec_1, vec_2, arrow, angle, tex_u_1, tex_u_2, text_i).wait()
        
        new_offset_l = 4*LEFT + 2.5*DOWN
        new_ratio = 0.8
        unit_l, unit_r, unit_u, unit_d = new_ratio*np.array([-2, -1, 0]), new_ratio*np.array([2, 1, 0]), new_ratio*np.array([-1, 2, 0]), new_ratio*np.array([1, -2, 0])
        u_l, u_r, u_u, u_d = unit_l, unit_r, unit_u, unit_d
        left, right, up, down = 8, 8, 15, 10
        bound_l, bound_r, bound_u, bound_d = (left+0.5)*unit_l, (right+0.5)*unit_r, (up+0.5)*unit_u, (down+0.5)*unit_d
        lines_h = [Line(bound_l + i*unit_d, bound_r + i*unit_d, stroke_width = 2 if i else 3, color = BLUE_E if i else BLUE_A) for i in range(-up, down + 1)]
        lines_v = [Line(bound_u + i*unit_r, bound_d + i*unit_r, stroke_width = 2 if i else 3, color = BLUE_E if i else BLUE_A) for i in range(-left, right + 1)]
        u_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(new_offset_l)
        new_stroke_dic = {r"width": 8, r"color": BLACK, r"background": True}
        def number(i):
            if i == 1:
                return ""
            elif i == -1:
                return "-"
            else:
                return str(i)
        labels_real = [MTex(number(i)+"u", tex_to_color_map = {"u": BLUE}, anchor = abs(i)).scale(0.8).set_stroke(**new_stroke_dic).shift(new_offset_l + i*unit_r + 0.25*u_d) for i in range(-left, right + 1) if i != 0 and i != 1] #.next_to(new_offset_l + i*unit_r, DR, buff = 0.1)
        labels_imag = [MTex(number(i)+"iu", tex_to_color_map = {r"i": YELLOW, "u": BLUE}, anchor = abs(i)).scale(0.8).set_stroke(**new_stroke_dic).shift(new_offset_l + i*unit_u + 0.25*u_l) for i in range(-up, down + 1) if i != 0 and i != 1] #new_offset_l + i*unit_u, DL, buff = 0.1
        labels_u = VGroup(label_0, u, ui, *labels_real, *labels_imag).save_state()
        def coor_u(x: float, y: float):
            return x*u_r + y*u_u + new_offset_l
        def relative_u(x: float, y: float):
            return x*u_r + y*u_u
        coefficients = {"mask_center": new_offset_l, "mask_r": 0, "dir_x": unit_r/(5*new_ratio**2), "dir_y": unit_u/(5*new_ratio**2)}
        alpha = ValueTracker(0)
        def mask_updater(mob: VMobject):
            mob.uniforms["mask_r"] = alpha.get_value()
        for mob in u_plane:
            mob.fill_shader_wrapper.reset_shader("mask_fill_1norm")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_1norm")
            mob.uniforms.update(coefficients)
            mob.add_updater(mask_updater)
        def fadein_updater(mob: VMobject):
            value = alpha.get_value()
            mob.set_opacity(inverse_interpolate(mob.anchor - 0.4, mob.anchor + 0.4, value))
        for mob in labels_u[3:]:
            mob.add_updater(fadein_updater)
        self.add_background(u_plane, labels_u).add_lower(vec_1, vec_2, arrow, angle).wait()
        self.play(alpha.animate.set_value(8), run_time = 5)
        for mob in u_plane:
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
            mob.clear_updaters()
        for mob in labels_u[3:]:
            mob.clear_updaters()
        self.add_background(labels_u.restore()).wait()

        ratio = 0.8
        offset_r = RIGHT_SIDE/2 - 0.5*ratio*RIGHT + 2.5*DOWN
        unit_l, unit_r, unit_u, unit_d = ratio*LEFT, ratio*RIGHT, ratio*UP, ratio*DOWN
        left, right, up, down = 2, 3, 4, 1
        bound_l, bound_r, bound_u, bound_d = (left+0.5)*unit_l, (right+0.5)*unit_r, (up+0.5)*unit_u, (down+0.5)*unit_d
        lines_h = [Line(bound_l + i*unit_d, bound_r + i*unit_d, stroke_width = 1 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line(bound_u + i*unit_r, bound_d + i*unit_r, stroke_width = 1 if i else 3, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        v_plane = VGroup(*lines_h[:up], *lines_h[up+1:], *lines_v, lines_h[up]).shift(offset_r)
        label_0 = MTex("0").scale(0.8).set_stroke(**stroke_dic).next_to(offset_r, DL, buff = 0.2)
        labels_real = [MTex(str(i)).scale(0.8).set_stroke(**stroke_dic).next_to(offset_r + i*unit_r, DOWN, buff = 0.2) for i in range(-left, right + 1) if i != 0]
        labels_imag = [MTex(number(i)+"i", tex_to_color_map = {r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).next_to(offset_r + i*unit_u, LEFT, buff = 0.2) for i in range(-down, up + 1) if i != 0] 
        labels_v = VGroup(label_0, *labels_real, *labels_imag)
        def coor_v(x: float, y: float):
            return x*unit_r + y*unit_u + offset_r
        def relative_v(x: float, y: float):
            return x*unit_r + y*unit_u
        self.add_lower(v_plane, labels_v).play(FadeIn(v_plane), FadeIn(labels_v))
        self.wait()

        new_stroke_dic = {r"width": 20, r"color": BLACK, r"background": True}
        line_x_u = Line(coor_u(0, 0), coor_u(1, 0), stroke_width = 8, color = GREEN)
        line_x_v = Line(coor_v(0, 0), coor_v(1, 0), stroke_width = 8, color = GREEN)
        tex_x_u = MTex(r"xu", tex_to_color_map = {r"x": GREEN, r"u": BLUE}).scale(0.8).set_stroke(**new_stroke_dic).shift(line_x_u.get_center() + 0.25*u_d)#.next_to(line_x_u.get_center(), DR, buff = 0.1)
        tex_x_v = MTex(r"x", tex_to_color_map = {r"x": GREEN}).scale(0.8).set_stroke(**stroke_dic).next_to(line_x_v, DOWN, buff = 0.2)
        self.play(ShowCreation(line_x_u), ShowCreation(line_x_v), Write(tex_x_u), Write(tex_x_v))
        self.wait()

        line_y_u = Line(coor_u(0, 0), coor_u(0, 3), stroke_width = 8, color = RED)
        line_y_v = Line(coor_v(0, 0), coor_v(0, 3), stroke_width = 8, color = RED)
        tex_y_u = MTex(r"yiu", tex_to_color_map = {r"y": RED, r"i": YELLOW, r"u": BLUE}).scale(0.8).set_stroke(**new_stroke_dic).shift(line_y_u.get_center() + 0.25*u_l)#.next_to(line_y_u.get_center(), DL, buff = 0.1)
        tex_y_v = MTex(r"yi", tex_to_color_map = {r"y": RED, r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).next_to(line_y_v, LEFT, buff = 0.2)
        self.play(ShowCreation(line_y_u), ShowCreation(line_y_v), Write(tex_y_u), Write(tex_y_v))
        self.wait()

        line_y_u.target = Line(coor_u(1, 0), coor_u(1, 3), stroke_width = 8, color = RED)
        line_y_v.target = Line(coor_v(1, 0), coor_v(1, 3), stroke_width = 8, color = RED)
        tex_y_u.target = MTex(r"yiu", tex_to_color_map = {r"y": RED, r"i": YELLOW, r"u": BLUE}).scale(0.8).set_stroke(**new_stroke_dic).shift(line_y_u.target.get_center() + 0.25*u_r)#.next_to(line_y_u.target.get_center(), UR, buff = 0.1)
        tex_y_v.target = MTex(r"yi", tex_to_color_map = {r"y": RED, r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).next_to(line_y_v.target, RIGHT, buff = 0.2)
        self.play(*[MoveToTarget(mob) for mob in [line_y_u, line_y_v, tex_y_u, tex_y_v]])
        vec_v_u = Vector(relative_u(1, 3), color = TEAL, stroke_width = 10).shift(coor_u(0, 0))
        vec_v_v = Vector(relative_v(1, 3), color = TEAL, stroke_width = 10).shift(coor_v(0, 0))
        tex_v_u = MTex(r"(x+yi)u", tex_to_color_map = {r"x+yi": TEAL, r"u": BLUE}).scale(0.8).set_stroke(**stroke_dic).next_to(coor_u(1, 3), UP, buff = 0.1)
        tex_v_v = MTex(r"x+yi", color = TEAL).scale(0.8).set_stroke(**stroke_dic).next_to(coor_v(1, 3), UP, buff = 0.2)
        self.play(ShowCreation(vec_v_u), ShowCreation(vec_v_v), Write(tex_v_u), Write(tex_v_v))
        self.wait()

        triangle_u = Polygon(coor_u(0, 0), coor_u(1, 0), coor_u(1, 3), stroke_width = 0, fill_color = TEAL, fill_opacity = 0.2)
        triangle_v = Polygon(coor_v(0, 0), coor_v(1, 0), coor_v(1, 3), stroke_width = 0, fill_color = TEAL, fill_opacity = 0.2)
        self.add_background(triangle_u).add_lower(triangle_v).play(*[FadeOut(mob) for mob in [arrow, angle]], *[FadeIn(mob) for mob in [triangle_u, triangle_v]])
        self.wait()

        angle_1, angle_2 = np.arctan(1/2), np.arctan(3)
        angle_arc_beta_u = Arc(start_angle = angle_1, angle = angle_2, radius = 0.6).shift(coor_u(0, 0))
        angle_arc_beta_v = Arc(start_angle = 0, angle = angle_2, radius = 0.4).shift(coor_v(0, 0))
        angle_tex_beta_u = MTex(r"\beta", color = TEAL).set_stroke(**stroke_dic).shift(1.0*unit(angle_1 + angle_2/2) + coor_u(0, 0))
        angle_tex_beta_v = MTex(r"\beta", color = TEAL).scale(0.8).set_stroke(**stroke_dic).shift(0.7*unit(angle_2/2) + coor_v(0, 0))
        self.add(angle_arc_beta_u, line_x_u, line_y_u, vec_v_u, angle_arc_beta_v, line_x_v, line_y_v, vec_v_v).play(
            ShowCreation(angle_arc_beta_u), ShowCreation(angle_arc_beta_v), Write(angle_tex_beta_u), Write(angle_tex_beta_v), *[FadeOut(mob) for mob in [tex_x_u, tex_x_v, tex_y_u, tex_y_v]]
        )
        self.wait()

        angle_arc_alpha_u = Arc(start_angle = 0, angle = angle_1, radius = 0.8).shift(coor_u(0, 0))
        angle_tex_alpha_u = MTex(r"\alpha", color = BLUE).set_stroke(**stroke_dic).shift(1.2*unit(angle_1/2) + coor_u(0, 0))
        tex_u = MTex(r"u=r_1(\cos\alpha+i\sin\alpha)", tex_to_color_map = {r"u": BLUE, r"r_1": BLUE, r"\alpha": BLUE, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).shift(RIGHT_SIDE/2 + 3.25*UP) 
        tex_v = MTex(r"v=r_2(\cos\beta+i\sin\beta)", tex_to_color_map = {r"v": TEAL, r"r_2": TEAL, r"\beta": TEAL, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).shift(RIGHT_SIDE/2 + 2.65*UP) 
        tex_uv = MTex(r"uv=r_1r_2(\cos(\alpha+\beta)+i\sin(\alpha+\beta))", tex_to_color_map = {r"u": BLUE, r"v": TEAL, r"r_1": BLUE, r"r_2": TEAL, r"\alpha": BLUE, r"\beta": TEAL, r"\cos": RED, r"\sin": ORANGE, r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).shift(RIGHT_SIDE/2 + 1.75*UP)
        self.add_lower(angle_arc_alpha_u).play(ShowCreation(angle_arc_alpha_u), Write(angle_tex_alpha_u), *[FadeOut(mob) for mob in [tex_u_1, tex_u_2, text_i]])
        self.play(*[FadeIn(mob) for mob in [tex_u, tex_v]])
        self.wait()

        angle_arc_sum_u = Arc(start_angle = 0, angle = angle_1 + angle_2, radius = 0.4).shift(coor_u(0, 0))
        position = coor(0, 0) + 0.2*unit((angle_1 + angle_2)/2)
        dot_arc = Dot(radius = 0.06, color = WHITE).set_stroke(width = 4, color = BLACK, background = True).move_to(position)
        theta = MTex(r"\alpha + \beta", tex_to_color_map = {r"\alpha": BLUE, r"\beta": TEAL}).set_stroke(**new_stroke_dic).scale(0.8).shift(position + 0.6*DOWN)#.next_to(theta_arc, DOWN, buff = 0.4)#.shift(coor(0, 0) + 0.4* DOWN)
        line_arc, shadow_line = Line(position, theta, stroke_width = 4, color = WHITE), Line(position, theta, stroke_width = 8, color = BLACK) 
        line_arc.uniforms["anti_alias_width"] = 0
        theta.generate_target()
        alpha, beta = angle_tex_alpha_u[0], angle_tex_beta_u[0]
        theta[0].become(alpha), theta[2].become(beta), theta[1].scale(0).move_to((alpha.get_center() + beta.get_center())/2)
        self.add_lower(angle_arc_sum_u).play(ShowCreation(angle_arc_sum_u), shadow_line.save_state().scale(0, about_point = position).set_stroke(width = 0).animate.restore(), GrowFromCenter(dot_arc), line_arc.save_state().scale(0, about_point = position).set_stroke(width = 0).animate.restore(), 
                                             MoveToTarget(theta, path_arc = -PI/2, lag_ratio = 1/3, run_time = 2), Write(tex_uv))
        self.wait()

#################################################################### 

class Video_3(FrameScene):
    def construct(self):
        e_symbol = MTex(r"e", color = BLUE).scale(2).set_stroke(**stroke_dic)
        background_e = e_symbol.copy().scale(10).move_to(0.0*UP).set_fill(color = GREY_E)
        self.add_background(background_e).play(DrawBorderThenFill(e_symbol), FadeIn(background_e), run_time = 1)
        self.wait()
        
        e_limit = MTex(r"e=\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n", tex_to_color_map = {r"e": BLUE, r"n": GREEN}).scale(1.5).set_stroke(**stroke_dic)
        part_0, part_1 = e_limit[0], e_limit[1:].save_state().match_x(e_symbol, RIGHT)
        def flushin_updater(mob: VMobject):
            mob.uniforms["mask_x"] = e_symbol.get_x(RIGHT)  + 0.1
        for mob in part_1:
            mob.fill_shader_wrapper.reset_shader("mask_fill_r")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_r")
            mob.add_updater(flushin_updater)
        self.add_text(part_1).play(e_symbol.animate.match_x(part_0, RIGHT), part_1.animate.restore())
        for mob in part_1:
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        part_0.become(e_symbol)
        self.remove(e_symbol).add(e_limit).wait()
        
        e_derivative = MTex(r"\left(e^x\right)'=e^x", tex_to_color_map = {r"e": BLUE}).scale(1.5).shift(RIGHT_SIDE/2 + 3*UP).set_stroke(**stroke_dic)
        self.play(e_limit.animate.shift(LEFT_SIDE/2 + 3*UP).scale(2/3), OverFadeIn(e_derivative, LEFT_SIDE/2 + 3*UP), run_time = 2)
        self.wait()

        bank = SVGMobject("bank.svg", height = 2).set_stroke(**stroke_dic).shift(5.5*LEFT + 1*UP)
        cash = SVGMobject("cash_money.svg", height = 1).set_stroke(**stroke_dic).shift(5.5*LEFT + 2*DOWN)
        # surr = SurroundingRectangle(cash, color = GREY)
        surr = BackgroundRectangle(cash, fill_color = GREY_E, buff = 0.1)
        self.add_background(surr).play(ShowCreation(bank), ShowCreation(cash), FadeIn(surr))
        self.wait()

        offset_m = 2.3*DOWN + 3*LEFT
        axis_x, axis_y = Arrow(ORIGIN, 3*RIGHT, buff = 0, stroke_width = 4), Arrow(0.5*DOWN, 4*UP, stroke_width = 4)
        axes_m = VGroup(axis_x, axis_y).shift(offset_m)
        label_0 = MTex("0").set_stroke(**stroke_dic).next_to(offset_m, LEFT, buff = 0.1)
        label_x = MTexText("时间").set_stroke(**stroke_dic).scale(0.8).next_to(axis_x.get_end(), RIGHT, buff = 0.2)
        label_y = MTexText("资金").set_stroke(**stroke_dic).scale(0.8).next_to(axis_y.get_end(), UP, buff = 0.2)
        self.play(GrowFromPoint(axes_m, offset_m))
        self.play(*[Write(mob) for mob in [label_0, label_x, label_y]])
        axes_m.add(label_0, label_x, label_y)
        self.add_text(axes_m).wait()

        line = Line(UP, 2.5*RIGHT + 2*UP, stroke_width = 4, color = YELLOW).shift(offset_m)
        line_2 = line.copy()
        lines = [Line(i/5*UP, 2.5*RIGHT + i/5*2*UP, stroke_width = 1, color = YELLOW_A).shift(offset_m) for i in range(20)]
        mask_u = offset_m[1] + 3.8
        for mob in lines:
            mob.fill_shader_wrapper.reset_shader("mask_fill_u")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_u")
            mob.uniforms["mask_u"] = mask_u
        dash_x, dash_y = DashedLine(2.5*RIGHT + 2*UP, 2.5*RIGHT).shift(offset_m), DashedLine(2.5*RIGHT + 2*UP, 2*UP).shift(offset_m)
        label_0 = MTex("1").set_stroke(**stroke_dic).scale(0.8).next_to(line.get_start(), LEFT, buff = 0.1)
        label_x, label_y = MTexText("1年").set_stroke(**stroke_dic).scale(0.8).next_to(dash_x.get_end(), DOWN, buff = 0.1), MTex("2").set_stroke(**stroke_dic).scale(0.8).next_to(dash_y.get_end(), LEFT, buff = 0.1)
        # self.add(line, dash_x, dash_y, label_0, label_x, label_y)
        self.add_background(*lines).play(Write(label_0), ShowCreation(line), *[ShowCreation(mob) for mob in lines])
        self.play(ShowCreation(dash_x), Write(label_x), ShowCreation(dash_y), Write(label_y))
        self.wait()

        offset_r = 2.3*DOWN + 2*RIGHT
        copy_axes = axes_m.copy().shift(offset_r - offset_m)
        copy_line = line.copy().shift(offset_r - offset_m).set_stroke(color = GREY, width = 2)
        copy_path = line.copy().shift(offset_r - offset_m).set_color(YELLOW_A)
        copy_0 = label_0.copy().shift(offset_r - offset_m)
        copy_x = label_x.copy().shift(offset_r - offset_m)
        self.add_text(copy_axes, copy_0, copy_x).play(TransformFromCopy(axes_m, copy_axes), TransformFromCopy(line, copy_path), TransformFromCopy(label_0, copy_0), TransformFromCopy(label_x, copy_x))
        self.add_background(copy_line).wait() 

        cashes = [1.25**i*1*UP for i in range(5)]
        width_h = 2.5*RIGHT
        points = [offset_r + 0.25*i*2.5*RIGHT + 1.25**i*1*UP for i in range(5)]
        dot = Dot(color = YELLOW).shift(points[0])
        self.add_text(dot).play(ShowCreation(dot), cash.save_state().animate.shift(2*UP).scale(0.5))
        polyline = Line(points[0], points[1], stroke_width = 4, color = YELLOW)
        self.play(ShowCreation(polyline), dot.animate.move_to(points[1]))
        self.play(cash.animate.restore())
        self.wait()

        dashed_1 = VMobject(stroke_width = 1, color = YELLOW).set_points(DashedLine(points[1], cashes[1] + offset_m).get_all_points())
        self.play(*[FadeOut(mob) for mob in [dash_x, dash_y, label_0, label_y]], 
                  Transform(line, Line(cashes[1], 2.5*RIGHT + 2*cashes[1], stroke_width = 4, color = YELLOW).shift(offset_m)), 
                  ShowCreation(dashed_1), 
                  copy_path.animate.put_start_and_end_on(points[1] - 0.25*cashes[1] - 0.25*width_h, points[1] + 0.75*cashes[1] + 0.75*width_h))
        self.wait()

        self.play(cash.save_state().animate.shift(2*UP).scale(0.5))
        polyline.generate_target().add_line_to(points[2])
        self.play(MoveToTarget(polyline.add_line_to(points[1])), dot.animate.move_to(points[2]))
        dashed_2 = VMobject(stroke_width = 1, color = YELLOW).set_points(DashedLine(points[2], cashes[2] + offset_m).get_all_points())
        self.play(cash.animate.restore(), 
                  Transform(line, Line(cashes[2], 2.5*RIGHT + 2*cashes[2], stroke_width = 4, color = YELLOW).shift(offset_m)), 
                  ShowCreation(dashed_2), Uncreate(dashed_1.reverse_points()),
                  copy_path.animate.put_start_and_end_on(points[2] - 0.5*cashes[2] - 0.5*width_h, points[2] + 0.5*cashes[2] + 0.5*width_h))
        self.wait()

        self.play(cash.save_state().animate.shift(2*UP).scale(0.5))
        polyline.generate_target().add_line_to(points[3])
        self.play(MoveToTarget(polyline.add_line_to(points[2])), dot.animate.move_to(points[3]))
        dashed_3 = VMobject(stroke_width = 1, color = YELLOW).set_points(DashedLine(points[3], cashes[3] + offset_m).get_all_points())
        self.play(cash.animate.restore(), 
                  Transform(line, Line(cashes[3], 2.5*RIGHT + 2*cashes[3], stroke_width = 4, color = YELLOW).shift(offset_m)), 
                  ShowCreation(dashed_3), Uncreate(dashed_2.reverse_points()),
                  copy_path.animate.put_start_and_end_on(points[3] - 0.75*cashes[3] - 0.75*width_h, points[3] + 0.25*cashes[3] + 0.25*width_h))
        self.wait()

        self.play(cash.save_state().animate.shift(2*UP).scale(0.5))
        polyline.generate_target().add_line_to(points[4])
        self.play(MoveToTarget(polyline.add_line_to(points[3])), dot.animate.move_to(points[4]))
        text_0, text_1 = MTex(r"\mathbf{2.000}").scale(0.4).next_to(copy_line.get_end(), RIGHT), MTex(r"\mathbf{"+f"{1.25**4:.3f}"+r"}").scale(0.4).next_to(polyline.get_end(), RIGHT)
        self.play(cash.animate.restore(), 
                  FadeOut(dashed_3), polyline.animate.set_stroke(width = 2, color = GREY), FadeOut(copy_path), FadeOut(line), 
                  dot.animate.scale(0).set_color(GREY), 
                  Write(text_0), Write(text_1))
        self.add_background(polyline).wait()

        dot = Dot(color = YELLOW).shift(points[0])
        copy_path = line.copy().shift(offset_r - offset_m).set_color(YELLOW_A)
        dash = VMobject(stroke_width = 1, color = YELLOW).set_points(DashedLine(points[0], cashes[0] + offset_m).get_all_points())
        trace = TracedPath(dot.get_center, stroke_width = 4, stroke_color = YELLOW)
        cash.other = cash.copy().shift(2*UP).scale(0.5)
        self.add_text(dot).play(ShowCreation(dot), FadeIn(copy_path), ShowCreation(dash), FadeIn(line_2))
        self.wait()

        alpha = ValueTracker(0.0)
        def dot_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(offset_r + value*width_h + np.exp(value)*UP)
        def path_updater(mob: Line):
            value = alpha.get_value()
            center, slope = offset_r + value*width_h + np.exp(value)*UP, width_h + np.exp(value)*UP
            mob.put_start_and_end_on(center - value*slope, center + (1-value)*slope)    
        def dash_updater(mob: VMobject):
            value = alpha.get_value()
            mob.set_points(DashedLine(offset_m + np.exp(value)*UP, offset_r + value*width_h + np.exp(value)*UP).get_all_points())
        cash_1 = VGroup(*[cash.copy().shift(2*UP*i/4).scale(interpolate(1, 0.5, i/4)).set_opacity(interpolate(1, 0.2, i/4)) for i in range(5)])
        cash_2 = VGroup(*[cash.copy().shift(2*UP*i/4).scale(interpolate(1, 0.5, i/4)).set_opacity(interpolate(0.2, 1, i/4)) for i in range(5)])
        def cash_updater(mob: SVGMobject):
            if mob.flip:
                mob.become(cash_1)
            else:
                mob.become(cash_2)
            mob.state = not mob.state
            # if seed:
            #     mob.set_opacity(0.2)
            #     mob.other.set_opacity(1)
            # else:
            #     mob.set_opacity(1)
            #     mob.other.set_opacity(0.2)
        def line_2_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(offset_m + np.exp(value)*UP, offset_m + width_h + 2*np.exp(value)*UP)
        cash.state = True
        dot.add_updater(dot_updater), copy_path.add_updater(path_updater), dash.add_updater(dash_updater), cash.add_updater(cash_updater), line_2.add_updater(line_2_updater)
        self.add(trace).play(alpha.animate.set_value(1), run_time = 5, rate_func = smooth_boot(1/9))
        for mob in [dot, copy_path, dash, cash, trace]:
            mob.clear_updaters()
        cash.restore()
        self.wait()

        text_3 = MTex(r"\mathbf{2.718}").scale(0.4).next_to(trace.get_end(), RIGHT)
        self.play(Write(text_3))
        self.wait()
        surr = SurroundingRectangle(text_3, color = BLUE, buff = 0.1, stroke_width = 2)
        equal = MTex("=e", tex_to_color_map = {r"e": BLUE}).scale(0.8).next_to(surr, RIGHT, buff = 0.1)
        self.play(ShowCreation(surr), Write(equal))
        self.wait()

        dot.add_updater(dot_updater), copy_path.add_updater(path_updater), dash.add_updater(dash_updater), line_2.add_updater(line_2_updater)
        back_e = BackgroundRectangle(e_derivative, fill_color = GREY_D, buff = 0.1)
        self.play(alpha.animate.set_value(0), FadeIn(SurroundingRectangle(e_derivative, buff = 0.2), rate_func = blink(6), remover = True), run_time = 3)
        self.add_background(back_e).play(alpha.animating(run_time = 3).set_value(1), FadeIn(SurroundingRectangle(e_derivative, buff = 0.2), rate_func = blink(6), run_time = 3), FadeIn(back_e))
        self.wait()

#################################################################### 

class Video_4(FrameScene):
    def construct(self):
        function = MTex(r"f(x)=e^{ix}", tex_to_color_map = {r"i": YELLOW, r"f": BLUE}).scale(1.5).shift(2*UP).set_stroke(**stroke_dic)#, ("f", r"e"): BLUE, r"x": RED
        self.wait(1)
        self.play(Write(function))
        self.wait(1)

        value = MTex(r"e^{i\pi}=-1", color = RED_A).next_to(function, UP, buff = 0.5).set_stroke(**stroke_dic)
        self.play(Write(value))
        self.wait(1)

        derivitave_exp = MTex(r"\left(e^x\right)'=e^x", color = TEAL).scale(0.8).set_stroke(**stroke_dic).shift(3*LEFT).match_y(value)
        derivitave_expi = MTex(r"f'(x)=\left(e^{ix}\right)'=\left(e^{ix}\right)(i)=ie^{ix}", tex_to_color_map = {r"i": YELLOW, r"f'": GREEN}).set_stroke(**stroke_dic).shift(0.5*UP)
        result = MTex(r"=if(x)", tex_to_color_map = {r"i": YELLOW, r"f": BLUE}).set_stroke(**stroke_dic)
        result.shift(derivitave_expi[5].get_center() + DOWN - result[0].get_center())
        self.play(FadeIn(derivitave_exp, 0.5*RIGHT))
        self.wait()
        self.play(Write(derivitave_expi))
        self.wait()

        self.play(FadeIn(result, 0.5*DOWN))
        self.wait()

        board = FloatWindow(height = 9, width = 15)
        offset_l = LEFT_SIDE/2
        offset_r = RIGHT_SIDE/2
        ratio = 1
        left, right, up, down = 4, 4, 4, 4
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 0 if i%2 else 4, color = YELLOW_E if i else WHITE) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 0 if i%2 else 4, color = YELLOW_E if i else WHITE) for i in range(-left, right + 1)]
        complex_plane = VGroup(*lines_h[:left], *lines_h[left+1:], *lines_v, lines_h[left]).shift(offset_r)
        lines_h = [Line((left+0.5)*ratio*LEFT + i*ratio*DOWN, (right+0.5)*ratio*RIGHT + i*ratio*DOWN, stroke_width = 1 if i%2 else 0, color = GREY) for i in range(-up, down + 1)]
        lines_v = [Line((up+0.5)*ratio*UP + i*ratio*RIGHT, (down+0.5)*ratio*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 0, color = GREY) for i in range(-left, right + 1)]
        back = VGroup(*lines_h[:left], *lines_h[left+1:], *lines_v, lines_h[left]).shift(offset_r)

        all_expi = VGroup(derivitave_expi, result)
        self.add_text(function, value, derivitave_exp, all_expi).add_background(back, complex_plane
                      ).play(board.animate.shift(7.5*LEFT), *[mob.animate.shift(2*LEFT) for mob in [value, derivitave_exp]], 
                             function.animate.scale(2/3).shift(offset_l), all_expi.animate.scale(0.8).shift(offset_l + 0.5*UP), run_time = 2)
        self.wait()

        # vec_0 = Vector(2*RIGHT + UP, color = BLUE, stroke_width = 10).shift(offset_r)
        # tex_0 = MTex("a+bi", color = BLUE).scale(0.8).set_stroke(**stroke_dic).next_to(vec_0, UR, buff = 0.1)
        # self.play(GrowArrow(vec_0), Write(tex_0))
        # self.wait()

        # calculation = MTex(r"i(a+bi)=ai+b(-1)=-b+ai", tex_to_color_map = {r"i": YELLOW, r"(-1)": GOLD, r"a+bi": BLUE, r"-b+ai": GREEN}).scale(0.8).shift(offset_l + 0.8*DOWN)
        # self.play(Write(calculation))
        # self.wait()

        # line_1, line_2 = Line(ORIGIN, 2*RIGHT, stroke_width = 8, color = RED).shift(offset_r), Line(ORIGIN, 2*UP, stroke_width = 8, color = ORANGE).shift(offset_r)
        # self.add_background(line_1, line_2).play(ShowCreation(line_1), ShowCreation(line_2))
        # line_1.generate_target().add_line_to(line_1.get_end() + UP), line_2.generate_target().add_line_to(line_2.get_end() + LEFT)
        # self.play(MoveToTarget(line_1.add_line_to(line_1.get_end())), MoveToTarget(line_2.add_line_to(line_2.get_end())))
        # self.wait()

        # vec_1 = Vector(2*UP + LEFT, color = GREEN, stroke_width = 10).shift(offset_r)
        # tex_1 = MTex("-b+ai", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(vec_1, UL, buff = 0.1)
        # copy_0 = VGroup(tex_0[0].copy(), *tex_0.copy().submobjects)
        # self.play(TransformFromCopy(vec_0, vec_1, path_arc = -PI/2), ReplacementTransform(copy_0, tex_1, path_arc = PI/2))
        # self.wait()

        text_i = MTexText("乘$i$：逆时针旋转$90$度", tex_to_color_map = {("i", "90"): YELLOW}).scale(0.8).shift(offset_l + 1.5*DOWN)
        # arrow = Arrow(1.2*(RIGHT+UP/2), 1.2*(UP+LEFT/2), path_arc = PI/2).shift(offset_r)
        # angle = MTex(r"90^\circ").scale(0.8).set_stroke(**stroke_dic).shift(offset_r + 1.8*unit(np.arctan(3)))
        # self.play(ShowCreation(arrow), Write(angle), Write(text_i))
        # self.wait()
        self.play(Write(text_i))
        self.wait()

        # i = Vector(UP, color = YELLOW, stroke_width = 10).shift(offset_r)
        # tex_i = MTex(r"i", color = YELLOW).set_stroke(**stroke_dic).scale(0.8).next_to(UP, RIGHT).shift(offset_r)
        # angle_0 = Elbow(width = 0.25, color = GOLD, stroke_width = 6).shift(offset_r + 0.05*UR)
        # self.add(angle_0, i, tex_i).play(GrowArrow(i), GrowFromPoint(tex_i, offset_r), ShowCreation(angle_0))
        # self.wait()

        # self.play(FadeOut(calculation), *[mob.animate.scale(2, about_point = offset_r) for mob in [complex_plane, back]], 
        #           *[OverFadeOut(mob, scale = 2, about_point = offset_r) for mob in [vec_0, tex_0, line_1, line_2, vec_1, tex_1, arrow, angle, i, tex_i, angle_0]], )
        # self.wait()

        zero = MTex(r"f(0)=e^{i0}=e^0=1", color = BLUE, tex_to_color_map = {r"0": GREY, r"i": YELLOW}).scale(0.8).shift(offset_l + 0.8*DOWN)
        vector_f = Vector(2*RIGHT, stroke_width = 10, color = BLUE).shift(offset_r)
        label_0 = MTex("f(0)=1", color = BLUE_E).scale(0.6).set_stroke(**stroke_dic).next_to(vector_f, DOWN, buff = 0.3)
        self.add_text(label_0).play(GrowArrow(vector_f), FadeIn(label_0, 2*RIGHT), FadeIn(zero, 0.5*RIGHT))
        self.wait()

        vector_df = Vector(2*UP, stroke_width = 10, color = GREEN).shift(offset_r)
        label_df = MTex("f'(x)", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(offset_r + 2*UP, UP, buff = 0.3)
        label_f = MTex("f(x)", color = BLUE).scale(0.8).set_stroke(**stroke_dic).next_to(offset_r + 2*RIGHT, RIGHT, buff = 0.3)
        self.add_text(label_df).play(TransformFromCopy(vector_f, vector_df, path_arc = -PI/2), label_df.save_state().next_to(offset_r + 2*RIGHT, UP, buff = 0.5).set_opacity(0).animating(path_arc = PI/2).restore())
        self.add_text(label_f).play(vector_df.animate.shift(2*RIGHT), label_df.animate.shift(2*RIGHT), FadeIn(label_f, 2*RIGHT))
        self.wait()

        shadow_f, shadow_df = vector_f.copy().set_color(BLUE_E), vector_df.copy().set_color(GREEN_E)
        alpha = ValueTracker(0.0)
        def rotate_updater(mob: VMobject):
            mob.rotate(alpha.get_value(), about_point = offset_r)
        vector_f.add_post_updater(rotate_updater), vector_df.add_post_updater(rotate_updater)
        label_df.offset, label_f.offset = label_df.get_center() - offset_r, label_f.get_center() - offset_r
        def label_updater(mob: VMobject):
            rot_matrix_T = rotation_matrix_transpose(alpha.get_value(), OUT)
            mob.move_to(np.dot(mob.offset, rot_matrix_T) + offset_r)
        label_df.add_updater(label_updater), label_f.add_updater(label_updater)
        self.add_lower(shadow_f, shadow_df).play(alpha.animate.set_value(TAU), rate_func = smooth_boot(1/9), run_time = 10)
        alpha.set_value(0)
        self.wait()

        circle = Circle(radius = 2, color = GREY).shift(offset_r)
        self.play(FadeIn(circle, layer = self.backgrounds))
        self.wait()

        text = MTex(r"x = 0.00", color = YELLOW).scale(1.5).shift(offset_l + 2.3*DOWN)
        self.play(Write(text))
        self.wait()
        digits = [MTex(str(i), color = YELLOW).scale(1.5)[0] for i in range(10)]
        def digit_raplace(mob: VMobject, index: int, residue: float = 0):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
            return int(residue%10), 10*(residue%1)
        def text_updater(mob: MTex):
            value = alpha.get_value()
            index, residue = digit_raplace(mob[2], int(value), 10*(value%1))
            index, residue = digit_raplace(mob[4], index, residue)
            index, residue = digit_raplace(mob[5], index, residue)
        text.add_updater(text_updater)
        arc = VMobject(stroke_color = "#4000FF", stroke_width = 6)
        arc_back = VMobject(stroke_color = LIME, stroke_width = 12)
        def arc_updater(mob: VMobject):
            mob.match_points(Arc(start_angle = 0, angle = alpha.get_value(), radius = 2).shift(offset_r))
        arc.add_updater(arc_updater), arc_back.add_updater(arc_updater)
        self.add_lower(arc_back, arc).play(alpha.animate.set_value(PI/4), run_time = 4)
        self.wait()

        label_x = MTex(r"x", color = PURPLE_B).set_stroke(**stroke_dic).scale(0.8).shift(offset_r + 2.4*unit(PI/8))
        self.add_text(label_x).play(Write(label_x))
        self.wait()

        line_cos, line_sin = DashedLine(offset_r + 2*unit(PI/4), offset_r + 2*np.sin(PI/4)*UP, color = RED), DashedLine(offset_r + 2*unit(PI/4), offset_r + 2*np.cos(PI/4)*RIGHT, color = ORANGE)
        text_cos, text_sin = MTex(r"\cos x", color = RED).set_stroke(**stroke_dic).scale(0.6).next_to(line_cos, DOWN, buff = 0.1), MTex(r"\sin x", color = ORANGE).set_stroke(**stroke_dic).scale(0.6).next_to(line_sin, LEFT, buff = 0.1)
        self.add_lower(line_cos, line_sin).play(ShowCreation(line_cos), ShowCreation(line_sin))
        self.add_text(text_cos, text_sin).play(Write(text_cos), Write(text_sin)) 
        self.wait()

        mtex_all = MTex(r"f(x)=e^{ix}=\cos x + i\sin x", tex_to_color_map = {r"i": YELLOW, r"f": BLUE, r"\cos": RED, r"\sin": ORANGE}).move_to(function)
        part_1, part_2 = mtex_all[:8].save_state(), mtex_all[8:].save_state()
        mtex_all.shift(function[0].get_center() - mtex_all[0].get_center())
        part_2.match_x(part_1, RIGHT)
        shade = BackgroundRectangle(part_2, buff = 0.1)
        self.remove(function).add(part_2, shade, part_1).play(part_1.animate.restore(), part_2.animate.restore(), follow(shade, part_1, remover = True))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [line_cos, line_sin, text_cos, text_sin]])
        self.wait()

        def half_updater(mob: MTex):
            mob.move_to(offset_r + 2.4*unit(alpha.get_value()/2))
        label_x.add_updater(half_updater)
        self.play(alpha.animate.set_value(PI), run_time = 5, rate_func = smooth_boot(1/4))
        for mob in [label_x]:
            mob.clear_updaters()
        self.wait()

        label_pi = MTex(r"x = \pi", tex_to_color_map = {r"\pi": RED}).set_stroke(**stroke_dic).scale(0.8).shift(offset_r + 2.4*unit(PI/2))
        part_2 = label_pi[1:].save_state().match_x(label_x, RIGHT)
        def flushin_updater(mob: VMobject):
            mob.uniforms["mask_x"] = label_x.get_x(RIGHT)  + 0.1
        for mob in label_pi[1:]:
            mob.fill_shader_wrapper.reset_shader("mask_fill_r")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_r")
            mob.add_updater(flushin_updater)
        self.add_text(part_2).play(label_x.animate.move_to(label_pi[0]), part_2.animate.restore())
        self.wait()

        indicate = Circle(radius = 0.2, color = YELLOW).shift(offset_r + 2*LEFT)
        back = Circle(radius = 0.2, color = BLACK, stroke_width = 8).shift(offset_r + 2*LEFT)
        label_1 = MTex("f(\pi)=-1", color = BLUE_E).scale(0.6).set_stroke(**stroke_dic).next_to(vector_f, DOWN, buff = 0.3).shift(2*LEFT)
        self.add_text(label_1).play(ShowCreation(back), ShowCreation(indicate), Write(label_1))
        self.wait()
        self.play(FadeOut(back), FadeOut(indicate))
        self.wait()

        result = MTex(r"e^{i\pi}=-1", tex_to_color_map = {r"e": BLUE, r"i": YELLOW, r"\pi": RED}).scale(1.5).set_stroke(**stroke_dic).shift(offset_r + 3.4*UP)
        self.play(Write(result))
        self.wait()


#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]