from __future__ import annotations

from manimlib import *
import numpy as np
from pydub import AudioSegment

#################################################################### 

class FlushIn_0(Transform):
    def __init__(
        self,
        mobject: VMobject,
        left: float | None = None,
        right: float | None = None,
        buff: float = 0.2, 
        **kwargs
    ):
        if left is None:
            left = mobject.get_left()[0] - buff
        if right is None:
            right = mobject.get_right()[0] + buff

        for mob in mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("mask_fill")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke")
            mob.uniforms["mask_x"] = left
        target = mobject.copy()
        for mob in target.get_family():
            mob.uniforms["mask_x"] = right
        
        super().__init__(mobject, target, **kwargs)

    def finish(self) -> None:
        for mob in self.mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        super().finish()

    # def interpolate_mobject(self, alpha: float) -> None:
    #     super().interpolate_mobject(alpha)
    #     print(self.mobject.uniforms["mask_x"])
    #     for i, mobs in enumerate(self.families):
    #         sub_alpha = self.get_sub_alpha(alpha, i, len(self.families))
    #         self.interpolate_submobject(*mobs, sub_alpha)

class FlushIn_1(Transform):
    def __init__(
        self,
        mobject: VMobject,
        top: float | None = None,
        bottom: float | None = None,
        buff: float = 0.2, 
        **kwargs
    ):
        if top is None:
            top = mobject.get_top()[1] + buff
        if bottom is None:
            bottom = mobject.get_bottom()[1] - buff

        for mob in mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("mask_fill_1")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_1")
            mob.uniforms["mask_y"] = top
        target = mobject.copy()
        for mob in target.get_family():
            mob.uniforms["mask_y"] = bottom
        
        super().__init__(mobject, target, **kwargs)

    def finish(self) -> None:
        for mob in self.mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        super().finish()

class FlushIn(Transform):
    def __init__(
        self,
        mobject: VMobject,
        left: float | None = None,
        right: float | None = None,
        middle: float | None = None,
        buff: float = 0.2, 
        **kwargs
    ):
        if left is None:
            left = mobject.get_left()[0] - buff
        if right is None:
            right = mobject.get_right()[0] + buff
        if middle is None:
            middle = mobject.get_center()[0]

        for mob in mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("strip_fill")
            mob.stroke_shader_wrapper.reset_shader("strip_stroke")
            mob.uniforms["mask_l"] = middle
            mob.uniforms["mask_r"] = middle
        target = mobject.copy()
        for mob in target.get_family():
            mob.uniforms["mask_l"] = left
            mob.uniforms["mask_r"] = right
        
        super().__init__(mobject, target, **kwargs)

    def finish(self) -> None:
        for mob in self.mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        super().finish()

class RotateIn(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(
        self,
        mobject: Mobject,
        angle: float = TAU,
        axis: np.ndarray = OUT,
        **kwargs
    ):
        self.angle = angle
        self.axis = axis
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for sm1, sm2 in self.get_all_families_zipped():
            sm1.set_points(sm2.get_points())
        self.mobject.scale(alpha).rotate(alpha * self.angle, axis=self.axis)

class Test1(FrameScene):
    def construct(self):
        testboard = Testboard()
        self.add(testboard)
        self.wait()
        # self.play(FlushIn(testboard), run_time = 3)
        self.play(FlushIn(testboard, -4, 4, 0), run_time = 3)
        self.wait()

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        quote_english = Songti("「」").scale(1.2).shift(1.5*UP)
        quote_chinese = Songti("『』").scale(1.2).shift(0.5*DOWN)
        self.wait()
        self.play(RotateIn(quote_english), RotateIn(quote_chinese))
        #self.wait()

        english = Roman("I am the storm that is approaching").shift(1.5*UP)
        chinese = Songti("我是那即将迫近的风暴").shift(0.5*DOWN)
        
        target_e, target_c = quote_english.generate_target(), quote_chinese.generate_target()
        target_e[0].next_to(english.get_corner(DL), UL)
        target_e[1].next_to(english.get_corner(UR), DR)
        target_c[0].next_to(chinese.get_corner(DL), UL)
        target_c[1].next_to(chinese.get_corner(UR), DR)
        self.play(MoveToTarget(quote_english), MoveToTarget(quote_chinese), FlushIn(english), FlushIn(chinese))

        default_aaw = 1.5/(1080/8)
        for mob in english:
            mob.uniforms["anti_alias_width"] = 0.1
        for mob in chinese:
            mob.uniforms["anti_alias_width"] = 0.1
        target_e = english.generate_target().scale(1.2)
        for mob in target_e:
            mob.uniforms["anti_alias_width"] = default_aaw
        target_e[0].set_color(YELLOW_B)
        target_e[1:3].set_color(RED_B)
        target_e[3:11].set_color(BLUE)
        target_e[11:].set_color(GREEN_B)
        target_c = chinese.generate_target().scale(1.2)
        for mob in target_c:
            mob.uniforms["anti_alias_width"] = default_aaw
        target_c[0].set_color(YELLOW_B)
        target_c[1].set_color(RED_B)
        target_c[8:].set_color(BLUE)
        target_c[2:8].set_color(GREEN_B)
        self.play(MoveToTarget(english), MoveToTarget(chinese), FadeOut(quote_english, scale = 1.1), FadeOut(quote_chinese, scale = 1.1), rate_func = rush_from)
        self.wait()

        line_0_e = Underline(english[0], stroke_width = 4, color = YELLOW)
        line_1_e = Underline(english[1:3], stroke_width = 4, color = RED).match_y(line_0_e)
        line_2_e = Underline(english[3:11], stroke_width = 4, color = BLUE).match_y(line_0_e)
        line_3_e = Underline(english[11:], stroke_width = 4, color = GREEN).match_y(line_0_e)
        text_0_e = Songti("主语", color = YELLOW).scale(0.4).next_to(line_0_e, DOWN, buff = 0.15).save_state().next_to(line_0_e, UP, buff = 0.125)
        text_1_e = Songti("系动词", color = RED).scale(0.4).next_to(line_1_e, DOWN, buff = 0.15).save_state().next_to(line_1_e, UP, buff = 0.125)
        text_2_e = Songti("宾语", color = BLUE).scale(0.4).next_to(line_2_e, DOWN, buff = 0.15).save_state().next_to(line_2_e, UP, buff = 0.125)
        text_3_e = Songti("定语", color = GREEN).scale(0.4).next_to(line_3_e, DOWN, buff = 0.15).save_state().next_to(line_3_e, UP, buff = 0.125)
        back_e = BackgroundRectangle(VGroup(english, line_0_e, line_1_e, line_2_e, line_3_e, text_0_e, text_1_e, text_2_e, text_3_e), buff = 0.05)
        
        line_0_c = Underline(chinese[0], stroke_width = 4, color = YELLOW)
        line_1_c = Underline(chinese[1], stroke_width = 4, color = RED).match_y(line_0_c)
        line_2_c = Underline(chinese[2:8], stroke_width = 4, color = GREEN).match_y(line_0_c)
        line_3_c = Underline(chinese[8:], stroke_width = 4, color = BLUE).match_y(line_0_c)
        text_0_c = Songti("主语", color = YELLOW).scale(0.4).next_to(line_0_c, DOWN, buff = 0.15).save_state().next_to(line_0_c, UP, buff = 0.125)
        text_1_c = Songti("谓语动词", color = RED).scale(0.4).next_to(line_1_c, DOWN, buff = 0.15).save_state().next_to(line_1_c, UP, buff = 0.125)
        text_2_c = Songti("定语", color = GREEN).scale(0.4).next_to(line_2_c, DOWN, buff = 0.15).save_state().next_to(line_2_c, UP, buff = 0.125)
        text_3_c = Songti("宾语", color = BLUE).scale(0.4).next_to(line_3_c, DOWN, buff = 0.15).save_state().next_to(line_3_c, UP, buff = 0.125)
        back_c = BackgroundRectangle(VGroup(chinese, line_0_c, line_1_c, line_2_c, line_3_c, text_0_c, text_1_c, text_2_c, text_3_c), buff = 0.00)
        # self.play(LaggedStart(*[GrowFromPoint(mob, mob[0].get_center(), rate_func = rush_from) for mob in [text_0, text_1, text_2, text_3]], rate_func = linear, lag_ratio = 1/3))
        self.add_background(text_0_e, text_1_e, text_2_e, text_3_e, text_0_c, text_1_c, text_2_c, text_3_c, back_e, back_c
            ).play(LaggedStart(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0_e, line_1_e, line_2_e, line_3_e]], rate_func = linear, lag_ratio = 1/3), 
                   LaggedStart(*[mob.animating(rate_func = rush_from).restore() for mob in [text_0_e, text_1_e, text_2_e, text_3_e]], rate_func = linear, lag_ratio = 1/3, group = VGroup()), 
                   LaggedStart(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0_c, line_1_c, line_2_c, line_3_c]], rate_func = linear, lag_ratio = 1/3), 
                   LaggedStart(*[mob.animating(rate_func = rush_from).restore() for mob in [text_0_c, text_1_c, text_2_c, text_3_c]], rate_func = linear, lag_ratio = 1/3, group = VGroup()))
        self.remove(back_e, back_c).wait()

        self.play(*[IndicateAround(mob, rect_kwargs = {"stroke_color": WHITE}) for mob in [english[0], english[1:3], english[3:11], chinese[0], chinese[1], chinese[8:]]])
        self.wait()

class Cursor(Line):
    CONFIG = {
        "buff": 0.05,
    }
    def __init__(self, mobject: Mobject, **kwargs):
        super().__init__(LEFT, RIGHT, **kwargs)
        self.mobject = mobject
        self.match_width(mobject[0])
        def corner_updater(mob):
            mob.next_to(mobject[-1].get_corner(DR), DR, buff = mob.buff)
        self.updater = corner_updater
        self.add_updater(self.updater)
        
class Video_2(FrameScene):
    def construct(self):
        sound_0, sound_1, sound_2 = AudioSegment.from_file("sound_0.mp3"), AudioSegment.from_file("sound_1.mp3"), AudioSegment.from_file("sound_2.mp3")
        def blink_updater(mob):
            mob.set_opacity((self.frames - 1) % 30 + 1 < 15)

        source_1 = Songti("只因你实在是太美")
        text_1 = VGroup().add(*source_1[:6])
        cursor_0 = Cursor(text_1).add_updater(blink_updater)
        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.add(text_1, cursor_0).play(ShowIncreasingSubsets(text_1), rate_func = linear)
        self.wait(3)

        text_1.add(source_1[6])
        self.file_writer.add_audio_segment(sound_2, time = self.get_time())
        self.wait(3)

        alter_1 = Songti("只因你实在是太美", color = GOLD_A).shift(1.5*UP).scale(0.8)
        alter_1[-1].set_color(GOLD)
        cursor_1 = Cursor(alter_1, color = GOLD_A).add_updater(blink_updater)
        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.add(alter_1, cursor_1).play(ShowIncreasingSubsets(alter_1, rate_func = linear), text_1.animate.shift(0.5*DOWN))
        source_1[-1].shift(0.5*DOWN)
        cursor_1.remove_updater(cursor_1.updater).next_to(alter_1[-1], DOWN, buff = cursor_1.buff)
        self.wait(3)

        alter_2 = Songti("只因你实在是太狠心", color = BLUE_A).shift(2.5*UP + 4*LEFT).scale(0.6)
        line_2 = Line(alter_2.get_left() + 0.2*LEFT, alter_2.get_right() + 0.2*RIGHT, color = GREY)
        last_2 = alter_2[-1].set_color(BLUE_E)
        alter_2.set_submobjects(alter_2.submobjects[:-1])[-1].set_color(BLUE)
        cursor_2 = Cursor(alter_2, color = BLUE_A, stroke_width = 2).add_updater(blink_updater)
        alter_3 = Songti("只因你实在是太抽象", color = interpolate_color(PURPLE_B, WHITE, 0.5)).shift(2.5*UP + 4*RIGHT).scale(0.6)
        line_3 = Line(alter_3.get_left() + 0.2*LEFT, alter_3.get_right() + 0.2*RIGHT, color = GREY)
        last_3 = alter_3[-1].set_color(PURPLE_E)
        alter_3.set_submobjects(alter_3.submobjects[:-1])[-1].set_color(PURPLE_B)
        cursor_3 = Cursor(alter_3, color = interpolate_color(PURPLE_B, WHITE, 0.5), stroke_width = 2).add_updater(blink_updater)
        alter_4 = Songti("只因你实在是太可恨", color = RED_A).shift(1.5*DOWN + 4*LEFT).scale(0.6)
        line_4 = Line(alter_4.get_left() + 0.2*LEFT, alter_4.get_right() + 0.2*RIGHT, color = GREY)
        last_4 = alter_4[-1].set_color(interpolate_color(RED, BLACK, 0.5))
        alter_4.set_submobjects(alter_4.submobjects[:-1])[-1].set_color(RED)
        cursor_4 = Cursor(alter_4, color = RED_A, stroke_width = 2).add_updater(blink_updater)
        alter_5 = Songti("只因你实在是太贪婪", color = GREEN_A).shift(1.5*DOWN + 4*RIGHT).scale(0.6)
        line_5 = Line(alter_5.get_left() + 0.2*LEFT, alter_5.get_right() + 0.2*RIGHT, color = GREY)
        last_5 = alter_5[-1].set_color(GREEN_E)
        alter_5.set_submobjects(alter_5.submobjects[:-1])[-1].set_color(GREEN)
        cursor_5 = Cursor(alter_5, color = GREEN_A, stroke_width = 2).add_updater(blink_updater)

        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.add(alter_2, cursor_2, alter_3, cursor_3, alter_4, cursor_4, alter_5, cursor_5).play(*[ShowIncreasingSubsets(mob) for mob in [alter_2, alter_3, alter_4, alter_5]], rate_func = linear)
        for mob in [cursor_2, cursor_3, cursor_4, cursor_5]:
            mob.remove_updater(mob.updater).next_to(mob.mobject[-1], DOWN, buff = mob.buff)
        self.add(last_2, last_3, last_4, last_5)
        self.wait(3)

        text_0 = Songti("迎面走来的你让我如此蠢蠢欲动，").next_to(text_1, UP)
        text_0.shift((text_1[0].get_x() - text_0[3].get_x())*RIGHT)
        self.play(FlushIn_0(text_0))
        self.wait(3)

        text_1.add(source_1[-1].set_color(GOLD))
        self.file_writer.add_audio_segment(sound_2, time = self.get_time())
        self.play(*[ShowCreation(mob) for mob in [line_2, line_3, line_4, line_5]])
        self.remove(cursor_2, cursor_3, cursor_4, cursor_5)
        self.wait(3)

        text_2 = Songti("美。")
        text_2.shift(text_1[-1].get_center() - text_2[0].get_center())
        self.add(text_2[-1])
        self.wait(3)

class Video_3(FrameScene):
    def construct(self):
        file = open("sentences.txt",'r',encoding='UTF-8')
        lines = [line.strip() for line in file.readlines()]
        random.shuffle(lines)
        file.close()

        def show_updater(mob: Text):
            mob.counter += 1
            length = len(mob.submobjects)
            if length < mob.len:
                if mob.counter >= mob.threshold:
                    mob.counter = 0
                    mob.add(mob.clone[length])
            else:
                if mob.counter >= 30:
                    mob.set_opacity(mob.opacity * (60-mob.counter)/30)
            if mob.counter >= 60:
                self.remove(mob)

        for line in lines:
            alpha = random.random()
            offset = (1.6*random.random() - 0.4*random.random() - 0.6)*TOP*0.9 + (1.6*random.random() - 0.4*random.random() - 0.6)*RIGHT_SIDE*0.8
            text_i = Text(line, font = "Microsoft YaHei", fill_opacity = 0.2+0.8*alpha).scale(0.8*(0.5+0.5*alpha)).shift(offset)
            text_i.len = len(text_i.submobjects)
            text_i.clone = text_i.copy()
            text_i.counter = 0
            text_i.opacity = 0.2+0.8*alpha
            if text_i.len <= 15:
                text_i.threshold = 4
            elif text_i.len <= 30:
                text_i.threshold = 2
            else:
                text_i.threshold = 1
            text_i.set_submobjects([]).add_updater(show_updater)
            self.add(text_i).wait(0, 10)
        self.wait(5)

class Patch_3_0(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8, 8)}, 
            },
    }
    def construct(self):
        dot = TrueDot(ORIGIN, color = BLACK, radius = 1)
        dot.uniforms["anti_alias_width"] = 1
        self.add(dot)

class Patch_3(FrameScene):
    def construct(self):
        dot = ImageMobject("Patch_3_0.png", height = 8)
        self.wait()
        self.play(FadeIn(dot))
        self.wait()

        token = Roman("token")
        self.play(Write(token))
        self.wait()

        title = Title("语素")
        titleline = TitleLine()
        self.add_background(self.shade).play(FadeIn(self.shade), ShowCreation(titleline, start = 0.5), Write(title), token.animate.shift(2.5*UP), dot.animate.shift(2.5*UP))
        self.remove(dot).wait()

        sentence = Songti("我是那即将迫近的风暴").scale(1.5)
        sentence[0].set_color(YELLOW_B)
        sentence[1].set_color(RED_B)
        sentence[8:].set_color(BLUE)
        sentence[2:8].set_color(GREEN_B)
        for i in range(10):
            sentence[i].set_x((i-4.5)*1.25)
        color_map = [YELLOW_B, RED_B, GREEN_B, GREEN_B, GREEN_B, GREEN_B, GREEN_B, GREEN_B, BLUE, BLUE]
        meanings_text = "第一人称\n代词", "表示\n领属关系", "较远事物\n的代词", "接近；\n靠近", "很快会；\n马上就", "靠近；\n接近", "空间距离\n小", "连接定语\n和中心词", "空气流动\n的现象", "突然\n而且猛烈"
        meanings = [Heiti(meanings_text[i], color = color_map[i]).set_x((i-4.5)*1.25).set_y(0.5, DOWN).scale(0.4) for i in range(10)]
        self.play(Write(sentence, run_time = 2))
        self.wait()
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in meanings], lag_ratio = 0.3, run_time = 2))
        self.wait()

        text_0 = Songti("主语", color = YELLOW).scale(0.9).set_y(-2.1).set_x(-4.5*1.25)
        text_1 = Songti("谓语", color = RED).scale(0.9).set_y(-2.1).set_x(-3.5*1.25)
        text_2 = Songti("定语", color = GREEN).scale(0.9).set_y(-2.1).set_x(0*1.25)
        text_3 = Songti("宾语", color = BLUE).scale(0.9).set_y(-2.1).set_x(4*1.25)
        texts = [text_0, text_1, text_2, text_3]
        self.play(*[Write(mob) for mob in texts])
        self.wait()

        line_1 = Line(1.2*LEFT, 1.2*RIGHT, color = GREEN_E).shift(0.55*DOWN + 1.25*LEFT)
        combine_1 = Heiti("正要；\n就要", color = GREEN_D).scale(0.6).next_to(line_1, DOWN)
        line_2 = Line(1.2*LEFT, 1.2*RIGHT, color = GREEN_E).shift(0.55*DOWN + 1.25*RIGHT)
        combine_2 = Heiti("相离不远，\n非常靠近", color = GREEN_D).scale(0.6).next_to(line_2, DOWN)
        line_3 = Line(1.2*LEFT, 1.2*RIGHT, color = BLUE_E).shift(0.55*DOWN + 4*1.25*RIGHT)
        combine_3 = Heiti("伴有强风或强降水\n的天气系统", color = BLUE_D).scale(0.6).next_to(line_3, DOWN)
        self.play(*[ShowCreation(mob, start = 0.5) for mob in [line_1, line_2, line_3]], *[Write(mob) for mob in [combine_1, combine_2, combine_3]])
        self.wait()

        aux = Heiti("助词", color = GREY)
        aux[0].move_to(0.4*UP), aux[1].move_to(0.4*DOWN)
        aux.add(SurroundingRectangle(aux, color = GREY, buff = 0.2)).scale(0.5)
        aux_1, aux_2 = aux.copy().next_to(sentence[2], DOWN), aux.copy().next_to(sentence[7], DOWN)
        self.play(*[FadeIn(mob, 0.3*DOWN) for mob in [aux_1, aux_2]])
        self.wait()

        title_2 = Title("语言模型")
        combine_4 = Heiti("并列结构", color = GREEN_D).scale(0.6).next_to(line_1, DOWN).shift(UP)
        combine_5 = Heiti("并列结构", color = GREEN_D).scale(0.6).next_to(line_2, DOWN).shift(UP)
        combine_6 = Heiti("偏正结构", color = BLUE_D).scale(0.6).next_to(line_3, DOWN).shift(UP)
        self.play(OverFadeOut(token), OverFadeOut(title), *[OverFadeOut(mob, UP) for mob in meanings + [combine_1, combine_2, combine_3]], 
                  *[mob.animate.shift(UP) for mob in [sentence, line_1, line_2, line_3, aux_1, aux_2] + texts], 
                  *[OverFadeIn(mob, UP) for mob in [combine_4, combine_5, combine_6]], 
                  OverFadeIn(title_2))
        self.wait()
        grammar = Songti("语法").next_to(titleline, DOWN)
        self.play(Write(grammar))
        self.wait()

        self.play(*[FadeOut(mob) for mob in [sentence, line_1, combine_4, line_2, combine_5, line_3, combine_6, aux_1, aux_2] + texts])
        self.wait()

class Video_4(FrameScene):
    def construct(self):
        title = Title("语言模型")
        titleline = TitleLine()
        grammar = Songti("语法").next_to(titleline, DOWN)
        self.add(title, titleline, grammar)
        self.wait()

        def blink_updater(mob):
            mob.set_opacity((self.frames - 1) % 30 + 1 < 15)

        source_0 = Songti("只因你实在是太美").next_to(0.8*UP + 6*LEFT)
        source_0[-1].set_color(GOLD)
        text_0 = VGroup().add(*source_0[:-1])
        cursor_0 = Cursor(text_0).add_updater(blink_updater)
        self.add(text_0, cursor_0).play(ShowIncreasingSubsets(text_0), rate_func = linear)
        self.wait(3)

        texts = "美", "狠心", "抽象", "可恨", "贪婪"
        colors = GOLD, BLUE, PURPLE_B, RED, GREEN
        mtexs = [Songti("只因你实在是太" + text, color = GREY_B) for text in texts]
        for i in range(5):
            mtexs[i].scale(0.8).next_to(UP + 1*RIGHT + 0.8*i*DOWN)
            mtexs[i][7:].set_color(colors[i])
        adj = Heiti("形容词").set_color(YELLOW).next_to(mtexs[0], UP)
        self.play(Write(adj), LaggedStart(*[FadeIn(mob, 0.5*LEFT) for mob in mtexs], lag_ratio = 0.2, run_time = 2))
        self.wait()

        alter = Songti("只因你实在是太篮球").next_to(0.8*DOWN + 6*LEFT)
        alter[7:].set_color(TEAL)
        self.play(FadeIn(alter, 0.5*DOWN))
        self.wait()
        cross = Cross(alter[7:]).set_stroke(width = 6)
        self.play(ShowCreation(cross))
        self.wait()

        self.fade_out(excepts = [title, titleline, grammar])
        self.wait()

        example = Songti("没人曾经说过这个句子").scale(1.2).set_y(1.2)
        for i in range(10):
            example[i].set_x((i-4.5)*1.25)
        target = example.generate_target()
        target[0].set_color(GREEN_B)
        target[1].set_color(YELLOW_B)
        target[2:4].set_color(ORANGE)
        target[4].set_color(RED_B)
        target[5].set_color(PURPLE_B)
        target[6:8].set_color(GREEN_B)
        target[8:].set_color(BLUE_B)
        line_0 = Underline(example[0])
        lines_0 = [line_0.copy().set_color(mob.get_color()).match_x(mob) for mob in target]
        lines_0[2].put_start_and_end_on(lines_0[2].get_start(), lines_0[3].get_end())
        lines_0[6].put_start_and_end_on(lines_0[6].get_start(), lines_0[7].get_end())
        lines_0[8].put_start_and_end_on(lines_0[8].get_start(), lines_0[9].get_end())
        lines_0.remove(lines_0[9])
        lines_0.remove(lines_0[7])
        lines_0.remove(lines_0[3])
        texts = "定语", "主语", "状语", "谓语", "补语", "定语", "宾语"
        colors = GREEN, YELLOW, ORANGE, RED, PURPLE, GREEN, BLUE
        xs = -4.5*1.25, -3.5*1.25, -2*1.25, -0.5*1.25, 0.5*1.25, 2*1.25, 4*1.25
        parts = [Songti(texts[i], color = colors[i]).set_x(xs[i]).set_y(1.85).scale(0.5) for i in range(7)]
        self.play(Write(example))
        self.play(*[FadeIn(mob) for mob in parts + lines_0], MoveToTarget(example))
        self.wait()
        
        buff_v = 0.2
        space_v = -1.0
        texts = "形容词", "名词", "副词", "动词", "助词", "代词", "名词"
        colors = GREEN, YELLOW, ORANGE, RED, PURPLE, GREEN, BLUE
        parts_1 = [Heiti(texts[i], color = colors[i], layer = 0).scale(0.4).set_x(xs[i]).set_y(0.5) for i in range(7)]
        self.play(*[Write(mob) for mob in parts_1])

        def combine(token_1, token_2):
            x_1, layer_1, color_1 = token_1.get_x(), token_1.layer, token_1[0].get_color()
            x_2, layer_2, color_2 = token_2.get_x(), token_2.layer, token_2[0].get_color()
            layer = max(layer_1, layer_2) + 1
            points = [np.array([x_1, 0.5 + layer_1*space_v - buff_v, 0]), 
                      np.array([x_1, 0.5 + layer*space_v + buff_v, 0]), 
                      np.array([x_2, 0.5 + layer*space_v + buff_v, 0]), 
                      np.array([x_2, 0.5 + layer_2*space_v - buff_v, 0])]
            line = Polyline(*points).set_color([color_1, color_2])
            line.middle = (points[1] + points[2])/2
            line.middle_color = interpolate_color(color_1, color_2, 0.5)
            return line
        
        lines_1 = [combine(parts_1[0], parts_1[1]), combine(parts_1[3], parts_1[4]), combine(parts_1[5], parts_1[6])]
        colors = [line.middle_color for line in lines_1]
        middles = [line.middle for line in lines_1]
        texts = "偏正结构", "动补结构", "偏正结构"
        rules_1 = [Heiti(texts[i], color = colors[i]).scale(0.4).next_to(middles[i], UP, buff = 0.1) for i in range(3)]
        texts = "名词短语", "动词复合词", "名词短语"
        parts_2 = [Heiti(texts[i], color = colors[i], layer = 1).scale(0.4).set_x(middles[i][0]).set_y(0.5 + space_v) for i in range(3)]
        self.play(*[FlushIn_1(mob, rate_func = rush_from) for mob in lines_1], 
                  *[Write(mob, rate_func = rush_into) for mob in rules_1 + parts_2])
        
        lines_2 = [combine(parts_1[2], parts_2[1])]
        colors = [line.middle_color for line in lines_2]
        middles = [line.middle for line in lines_2]
        texts = ["偏正结构"]
        rules_2 = [Heiti(texts[i], color = colors[i]).scale(0.4).next_to(middles[i], UP, buff = 0.1) for i in range(1)]
        texts = ["动词短语"]
        parts_3 = [Heiti(texts[i], color = colors[i], layer = 2).scale(0.4).set_x(middles[i][0]).set_y(0.5 + 2*space_v) for i in range(1)]
        self.play(*[FlushIn_1(mob, rate_func = rush_from) for mob in lines_2], 
                  *[Write(mob, rate_func = rush_into) for mob in rules_2 + parts_3])
        
        lines_3 = [combine(parts_2[0], parts_3[0]), combine(parts_3[0], parts_2[2])]
        self.play(*[FlushIn_1(mob, rate_func = rush_from) for mob in lines_3])
        self.wait()

        self.fade_out(excepts = [title, titleline, grammar])
        self.wait()

class Video_5(FrameScene):
    def construct(self):
        title = Title("语言模型")
        titleline = TitleLine()
        grammar = Songti("语法").next_to(titleline, DOWN)
        self.add(title, titleline, grammar)
        self.wait()

        chomsky = LabelPicture("Chomsky.jpg", "艾弗拉姆·诺姆·乔姆斯基（1928.12.7-）").shift(4.5*LEFT)
        self.play(FadeIn(chomsky, 0.5*UP))
        self.wait()

        english = Roman("Colorless green ideas sleep furiously").scale(0.8).shift(UP + 2.5*RIGHT)
        chinese = Songti("无色的绿点子狂暴地睡觉").shift(DOWN + 2.5*RIGHT)
        target_e, target_c = english.generate_target(), chinese.generate_target()
        english[:14].set_color(GREEN_B)
        english[14:19].set_color(YELLOW_B)
        english[19:24].set_color(RED_B)
        english[24:].set_color(ORANGE)
        chinese[:4].set_color(GREEN_B)
        chinese[4:6].set_color(YELLOW_B)
        chinese[6:9].set_color(ORANGE)
        chinese[9:].set_color(RED_B)
        self.play(Write(english), Write(chinese), run_time = 2)
        self.wait()

        line_0_e = Underline(english[:14], stroke_width = 4, color = GREEN)
        line_1_e = Underline(english[14:19], stroke_width = 4, color = YELLOW).match_y(line_0_e)
        line_2_e = Underline(english[19:24], stroke_width = 4, color = RED).match_y(line_0_e)
        line_3_e = Underline(english[24:], stroke_width = 4, color = ORANGE).match_y(line_0_e)
        text_0_e = Songti("定语", color = GREEN).scale(0.4).next_to(line_0_e, DOWN, buff = 0.15).save_state().next_to(line_0_e, UP, buff = 0.125)
        text_1_e = Songti("主语", color = YELLOW).scale(0.4).next_to(line_1_e, DOWN, buff = 0.15).save_state().next_to(line_1_e, UP, buff = 0.125)
        text_2_e = Songti("谓语", color = RED).scale(0.4).next_to(line_2_e, DOWN, buff = 0.15).save_state().next_to(line_2_e, UP, buff = 0.125)
        text_3_e = Songti("状语", color = ORANGE).scale(0.4).next_to(line_3_e, DOWN, buff = 0.15).save_state().next_to(line_3_e, UP, buff = 0.125)
        back_e = BackgroundRectangle(VGroup(english, line_0_e, line_1_e, line_2_e, line_3_e, text_0_e, text_1_e, text_2_e, text_3_e), buff = 0.05)
        
        line_0_c = Underline(chinese[:4], stroke_width = 4, color = GREEN)
        line_1_c = Underline(chinese[4:6], stroke_width = 4, color = YELLOW).match_y(line_0_c)
        line_2_c = Underline(chinese[6:9], stroke_width = 4, color = ORANGE).match_y(line_0_c)
        line_3_c = Underline(chinese[9:], stroke_width = 4, color = RED).match_y(line_0_c)
        text_0_c = Songti("定语", color = GREEN).scale(0.4).next_to(line_0_c, DOWN, buff = 0.15).save_state().next_to(line_0_c, UP, buff = 0.125)
        text_1_c = Songti("主语", color = YELLOW).scale(0.4).next_to(line_1_c, DOWN, buff = 0.15).save_state().next_to(line_1_c, UP, buff = 0.125)
        text_2_c = Songti("状语", color = ORANGE).scale(0.4).next_to(line_2_c, DOWN, buff = 0.15).save_state().next_to(line_2_c, UP, buff = 0.125)
        text_3_c = Songti("谓语", color = RED).scale(0.4).next_to(line_3_c, DOWN, buff = 0.15).save_state().next_to(line_3_c, UP, buff = 0.125)
        back_c = BackgroundRectangle(VGroup(chinese, line_0_c, line_1_c, line_2_c, line_3_c, text_0_c, text_1_c, text_2_c, text_3_c), buff = 0.1)
        # self.play(LaggedStart(*[GrowFromPoint(mob, mob[0].get_center(), rate_func = rush_from) for mob in [text_0, text_1, text_2, text_3]], rate_func = linear, lag_ratio = 1/3))
        self.add_background(text_0_e, text_1_e, text_2_e, text_3_e, text_0_c, text_1_c, text_2_c, text_3_c, back_e, back_c
            ).play(LaggedStart(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0_e, line_1_e, line_2_e, line_3_e]], rate_func = linear, lag_ratio = 1/3), 
                   LaggedStart(*[mob.animating(rate_func = rush_from).restore() for mob in [text_0_e, text_1_e, text_2_e, text_3_e]], rate_func = linear, lag_ratio = 1/3, group = VGroup()), 
                   LaggedStart(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0_c, line_1_c, line_2_c, line_3_c]], rate_func = linear, lag_ratio = 1/3), 
                   LaggedStart(*[mob.animating(rate_func = rush_from).restore() for mob in [text_0_c, text_1_c, text_2_c, text_3_c]], rate_func = linear, lag_ratio = 1/3, group = VGroup()))
        self.remove(back_e, back_c).wait()

#################################################################### 

def random_bright_color(
    hue_range: tuple[float, float] = (0.0, 1.0),
    saturation_range: tuple[float, float] = (0.5, 0.8),
    luminance_range: tuple[float, float] = (0.5, 1.0),
) -> Color:
    return Color(hsl=(
        interpolate(*hue_range, random.random()),
        interpolate(*saturation_range, random.random()),
        interpolate(*luminance_range, random.random()),
    ))

class ContextAnimation(LaggedStart):
    # From 3blue1brown
    def __init__(
        self,
        target,
        sources,
        direction=UP,
        hue_range=(0.1, 0.3),
        time_width=2,
        min_stroke_width=0,
        max_stroke_width=5,
        lag_ratio=None,
        strengths=None,
        run_time=3,
        fix_in_frame=False,
        path_arc=PI / 2,
        **kwargs,
    ):
        arcs = VGroup()
        if strengths is None:
            strengths = np.random.random(len(sources))**2
        for source, strength in zip(sources, strengths):
            sign = direction[1] * (-1)**int(source.get_x() < target.get_x())
            arcs.add(Line(
                source.get_edge_center(direction),
                target.get_edge_center(direction),
                path_arc=sign * path_arc,
                stroke_color=random_bright_color(hue_range=hue_range),
                stroke_width=interpolate(
                    min_stroke_width,
                    max_stroke_width,
                    strength,
                )
            ))
        if fix_in_frame:
            arcs.fix_in_frame()
        arcs.shuffle()
        lag_ratio = 0.5 / len(arcs) if lag_ratio is None else lag_ratio

        super().__init__(
            *(
                VShowPassingFlash(arc, time_width=time_width)
                for arc in arcs
            ),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )

class Video_6(FrameScene):
    def construct(self):
        title = Title("接话尾")
        titleline = TitleLine()
        self.wait()
        self.play(Write(title), ShowCreation(titleline, start = 0.5))
        self.wait()

        def blink_updater(mob):
            mob.set_opacity((self.frames - 1) % 30 + 1 < 15)
        source_1 = Songti("我在厕所打原神怎么你了吗。").scale(0.8).move_to(0.8*UP)
        text_1 = VGroup().add(source_1[0])
        cursor_1 = Cursor(text_1, buff = 0.10).add_updater(blink_updater)
        
class Video_7(FrameScene):
    def construct(self):
        title = Title("预测下一个语素")
        titleline = TitleLine()
        title_english = Roman("next-token-prediction").next_to(titleline, DOWN)
        self.wait()
        self.play(Write(title, run_time = 2), ShowCreation(titleline, start = 0.5), Write(title_english))
        self.wait()

        def blink_updater(mob):
            mob.set_opacity((self.frames - 1) % 30 + 1 < 15)

        source_0 = Songti("他放下了书，因为它太重").move_to(0.8*UP)
        text_0 = VGroup().add(*source_0[:-1])
        cursor_0 = Cursor(text_0, buff = 0.10).add_updater(blink_updater)
        self.add(text_0, cursor_0).play(ShowIncreasingSubsets(text_0), rate_func = linear)
        self.wait(3)

        target = text_0.generate_target()
        target[0:5].set_color(GREY)
        target[6:8].set_color(MAROON_B)
        target[8].set_color(YELLOW_B)
        target[9].set_color(TEAL_B)

        line_0_c = Underline(source_0[0:5], stroke_width = 4, color = GREY)
        line_1_c = Underline(source_0[6:8], stroke_width = 4, color = MAROON_B).match_y(line_0_c)
        line_2_c = Underline(source_0[8], stroke_width = 4, color = YELLOW_B).match_y(line_0_c)
        line_3_c = Underline(source_0[9], stroke_width = 4, color = TEAL_B).match_y(line_0_c)
        text_0_c = Songti("主句", color = GREY).scale(0.4).next_to(line_0_c, DOWN, buff = 0.15).save_state().next_to(line_0_c, UP, buff = 0.125)
        text_1_c = Songti("连词", color = MAROON).scale(0.4).next_to(line_1_c, DOWN, buff = 0.15).save_state().next_to(line_1_c, UP, buff = 0.125)
        text_2_c = Songti("主语", color = YELLOW).scale(0.4).next_to(line_2_c, DOWN, buff = 0.15).save_state().next_to(line_2_c, UP, buff = 0.125)
        text_3_c = Songti("副词", color = TEAL).scale(0.4).next_to(line_3_c, DOWN, buff = 0.15).save_state().next_to(line_3_c, UP, buff = 0.125)
        back_c = BackgroundRectangle(VGroup(source_0, line_0_c, line_1_c, line_2_c, line_3_c, text_0_c, text_1_c, text_2_c, text_3_c), buff = 0.1)
        self.add_background(text_0_c, text_1_c, text_2_c, text_3_c, back_c
            ).play(MoveToTarget(text_0), 
                LaggedStart(*[ShowCreation(mob, start = 0.5, rate_func = rush_from) for mob in [line_0_c, line_1_c, line_2_c, line_3_c]], rate_func = linear, lag_ratio = 1/3), 
                LaggedStart(*[mob.animating(rate_func = rush_from).restore() for mob in [text_0_c, text_1_c, text_2_c, text_3_c]], rate_func = linear, lag_ratio = 1/3, group = VGroup()))
        self.remove(back_c).wait()

        point_1 = MTex(r"\bullet\text{形容词}").scale(0.8).next_to(1.5*LEFT + 0.8*DOWN)
        point_2 = MTex(r"\bullet\text{造成负面影响}").scale(0.8).next_to(1.5*LEFT + 1.5*DOWN)
        point_3 = MTex(r"\bullet\cdots").scale(0.8).next_to(1.5*LEFT + 2.2*DOWN)
        self.play(Write(point_1))
        self.wait()
        self.play(Write(point_2))
        self.wait()
        self.play(Write(point_3))
        self.wait()

        alter_1 = Songti("重", color = GREEN).move_to(4*RIGHT + 1.3*UP)
        alter_2 = Songti("难", color = GREEN).move_to(4*RIGHT + 0.5*UP)
        alter_3 = Songti("...", color = GREEN).move_to(4*RIGHT + 0.3*DOWN)
        self.play(LaggedStart(*[FadeIn(mob, 0.5*LEFT) for mob in [alter_1, alter_2, alter_3]], lag_ratio = 1/3), run_time = 1)
        self.wait()

        self.play(text_0.save_state().animate.set_color(WHITE), 
                  *[FadeOut(mob) for mob in [line_0_c, line_1_c, line_2_c, line_3_c, text_0_c, text_1_c, text_2_c, text_3_c, point_1, point_2, point_3, alter_1, alter_2, alter_3]])
        self.wait()

        self.play(
            LaggedStart(*[ContextAnimation(cursor_0, text_0,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=3,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3,
                ) for _ in range(3)], lag_ratio=0.5), run_time=5)
        self.wait()

        self.play(LaggedStart(*[FadeIn(mob.set_color(WHITE), 0.3*RIGHT) for mob in [alter_1, alter_2, alter_3]], lag_ratio = 0.2), run_time = 1)
        self.wait()

        self.fade_out(excepts = [title, titleline, title_english])
        self.wait()

class Video_8(FrameScene):
    def construct(self):
        title = Title("预测下一个语素")
        titleline = TitleLine()
        title_english = Roman("next-token-prediction").next_to(titleline, DOWN)
        self.wait()
        self.play(Write(title, run_time = 2), ShowCreation(titleline, start = 0.5), Write(title_english))
        self.wait()

        sound_0, sound_1, sound_2 = AudioSegment.from_file("sound_0.mp3"), AudioSegment.from_file("sound_1.mp3"), AudioSegment.from_file("sound_2.mp3")
        def blink_updater(mob):
            mob.set_opacity((self.frames - 1) % 30 + 1 < 15)

        source_0 = Songti("我觉得有些热，然后就").move_to(0.8*UP)
        text_0 = VGroup().add(*source_0[:-1])
        cursor_0 = Cursor(text_0, buff = 0.10).add_updater(blink_updater)
        self.add(text_0, cursor_0).play(ShowIncreasingSubsets(text_0), rate_func = linear)
        self.wait(3)

        self.play(
            LaggedStart(*[ContextAnimation(cursor_0, text_0,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=3,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3,
                ) for _ in range(3)], lag_ratio=0.5), run_time=5)
        self.wait()
        
        alter_1 = Songti("打开了空调").scale(0.8).move_to(0.3*DOWN)
        alter_2 = Songti("脱了件衣服").scale(0.8).move_to(1.0*DOWN)
        alter_3 = Songti("买了根冰棍").scale(0.8).move_to(1.7*DOWN)
        alter_4 = Songti("...").scale(0.8).move_to(2.4*DOWN)
        
        self.play(LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in [alter_1, alter_2, alter_3, alter_4]], lag_ratio = 0.2), run_time = 1)
        self.wait()
        
        self.fade_out(excepts = [title, titleline, title_english])
        self.wait()

        source_1 = Songti("春天来了，万物复苏，大地上充满了生机与活力。").scale(0.8).move_to(0.8*UP)
        text_1 = VGroup().add(source_1[0])
        cursor_1 = Cursor(text_1, buff = 0.10).add_updater(blink_updater)
        self.add(text_1, cursor_1)
        self.file_writer.add_audio_segment(sound_2, time = self.get_time())
        self.wait()
        for i in range(1, len(source_1.submobjects)):
            self.play(ContextAnimation(cursor_1, text_1,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=2,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3), run_time = 2)
            text_1.add(source_1[i])
            cursor_1.update()
            self.file_writer.add_audio_segment(sound_2, time = self.get_time())
            # self.wait()
        self.wait()

        self_rec = Heiti("自回归生成", color = YELLOW).shift(DOWN)
        surr = SurroundingRectangle(self_rec).scale([-1, 1, 0], min_scale_factor = -1)
        self.play(Write(self_rec), ShowCreation(surr))
        self.wait()

class Video_9(FrameScene):
    def construct(self):
        title = Title("预测下一个语素")
        titleline = TitleLine()
        title_english = Roman("next-token-prediction").next_to(titleline, DOWN)
        self.add(title, titleline, title_english)
        self.wait()

        sound_0, sound_1, sound_2 = AudioSegment.from_file("sound_0.mp3"), AudioSegment.from_file("sound_1.mp3"), AudioSegment.from_file("sound_2.mp3")
        def blink_updater(mob):
            mob.set_opacity((self.frames - 1) % 30 + 1 < 15)
        
        question = Songti("·中国最高的山峰是哪座？").scale(0.8).next_to(UP + 4*LEFT)
        self.file_writer.add_audio_segment(sound_0[:1000], time = self.get_time())
        self.play(ShowIncreasingSubsets(question), rate_func = linear)
        self.wait()

        source = Songti("·中国最高的山峰是珠穆朗玛峰。").scale(0.8).next_to(DOWN + 4*LEFT)
        self.add(source[0])
        answer = VGroup().add(source[1].copy().move_to(source[0]).set_opacity(0))
        cursor_1 = Cursor(answer, buff = 0.10).add_updater(blink_updater)
        self.add(cursor_1, answer)

        self.file_writer.add_audio_segment(sound_2, time = self.get_time())
        self.wait()
        for i in range(1, len(source.submobjects)):
            self.play(ContextAnimation(cursor_1, [*question, *answer[1:]],
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=2,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3), run_time = 2)
            answer.add(source[i])
            cursor_1.update()
            self.file_writer.add_audio_segment(sound_2, time = self.get_time())
            # self.wait()
        self.wait()

class Video_10(FrameScene):
    def construct(self):

        lines = VGroup(*[Line(0.5*UP, 1.2*UP, stroke_width = 16).rotate(TAU/12*i, about_point = ORIGIN) for i in range(12)]).shift(DOWN + 3.5*LEFT)
        def lines_updater(mob: VGroup):
            runtime = self.time
            for i in range(12):
                alpha = (runtime + i/12)%1
                mob[i].set_color(interpolate_color(BLACK, WHITE, alpha))
        lines.add_updater(lines_updater)
        self.add(lines)

        clock_0 = MTex(r"15\text{时}00\text{分}00\text{秒}").shift(2*UP + 3.5*LEFT)
        rectangle = Rectangle(height = 0.4, width = 4.2, stroke_width = 2, color = BLUE_B).shift(UP + 3.5*LEFT)
        clock = VGroup(Digit(1).move_to(clock_0[0]), Digit(5).move_to(clock_0[1]), clock_0[2], 
                       Digit(0).move_to(clock_0[3]), Digit(0).move_to(clock_0[4]), clock_0[5], 
                       Digit(0).move_to(clock_0[6]), Digit(0).move_to(clock_0[7]), clock_0[8], Line(UP + 5.5*LEFT, UP + 1.5*LEFT, stroke_width = 20)).set_color(BLUE_A)
        clock.numbers = [1, 4, 5, 7, 5, 9]
        thresholds = [10, 10, 6, 10, 6, 10]
        def clock_updater(mob: VGroup):
            runtime = self.time
            if runtime <= 4:
                speed = 1
            elif runtime <= 5:
                speed = 2
            elif runtime <= 6:
                speed = 4
            elif runtime <= 7:
                speed = 6
            elif runtime <= 8:
                speed = 8
            elif runtime <= 50:
                speed = 10
            mob.numbers[5] += speed
            for i in range(5):
                j = 5-i
                while mob.numbers[j] >= thresholds[j]:
                    mob.numbers[j-1] += 1
                    mob.numbers[j] -= thresholds[j]
            mob[0].set_number(mob.numbers[0])
            mob[1].set_number(mob.numbers[1])
            mob[3].set_number(mob.numbers[2])
            mob[4].set_number(mob.numbers[3])
            mob[6].set_number(mob.numbers[4])
            mob[7].set_number(mob.numbers[5])
            ratio = ((((mob.numbers[5]/10 + mob.numbers[4])/6 + mob.numbers[3])/10 + mob.numbers[2])/3) % 1
            mob[9].put_start_and_end_on(UP + 5.5*LEFT, UP + 5.5*LEFT + 4*ratio*RIGHT)
        clock.add_updater(clock_updater)
        self.add(rectangle, clock)
        
        def blink_updater(mob):
            mob.set_opacity((self.frames - 1) % 30 + 1 < 15)

        source = Songti("GPT是“Generative Pre-trained\nTransformer”的缩写，指的是\n生成式预训练变换模型。它是\n一种深度学习算法，属于自然\n语言处理（NLP）领域的人工\n智能模型，旨在生成具有连贯\n性和逻辑性的自然语言文本。"
                      ).scale(0.8).next_to(LEFT)
        text = VGroup().add(source[3], *source[0:3], *source[4:-7])
        cursor = Cursor(text).add_updater(blink_updater)
        self.add(text, cursor).play(ContextAnimation(cursor, text,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=2,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3, run_time = 4), FadeOut(self.shade, delay = 1))
        text.add(source[-7])
        cursor.update()
        offset = 0.6*UP
        copy_1 = clock_0.copy().shift(offset).set_color(GREY)
        self.play(FadeIn(copy_1, offset, rate_func = rush_from, run_time = 0.5), LaggedStart(*[ContextAnimation(cursor, text,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=2,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3, run_time = 4) for _ in range(3)], lag_ratio = 0.5, run_time = 8))
        text.add(source[-6])
        cursor.update()
        copy_2 = MTex(r"15\text{时}30\text{分}07\text{秒}", color = GREY).shift(2*UP + 3.5*LEFT + offset)
        self.play(FadeIn(copy_2, offset, rate_func = rush_from, run_time = 0.5), copy_1.animating(rate_func = rush_from, run_time = 0.5).shift(offset), 
                  LaggedStart(*[ContextAnimation(cursor, text,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=2,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3, run_time = 3) for _ in range(3)], lag_ratio = 0.5, run_time = 6))
        text.add(source[-5])
        cursor.update()
        copy_3 = MTex(r"15\text{时}59\text{分}52\text{秒}", color = GREY).shift(2*UP + 3.5*LEFT + offset)
        self.play(FadeIn(copy_3, offset, rate_func = rush_from, run_time = 0.5), *[mob.animating(rate_func = rush_from, run_time = 0.5).shift(offset) for mob in [copy_1, copy_2]], 
                  LaggedStart(*[ContextAnimation(cursor, text,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=2,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3, run_time = 3) for _ in range(3)], lag_ratio = 0.5, run_time = 6))
        text.add(source[-4])
        cursor.update()
        copy_4 = MTex(r"16\text{时}29\text{分}54\text{秒}", color = GREY).shift(2*UP + 3.5*LEFT + offset)
        self.play(FadeIn(copy_4, offset, rate_func = rush_from, run_time = 0.5), *[mob.animating(rate_func = rush_from, run_time = 0.5).shift(offset) for mob in [copy_1, copy_2, copy_3]], 
                  LaggedStart(*[ContextAnimation(cursor, text,
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=2,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3, run_time = 3) for _ in range(3)], lag_ratio = 0.5, run_time = 6))
        
class Video_10(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]

#################################################################### 


class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        