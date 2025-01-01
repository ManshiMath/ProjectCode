from __future__ import annotations

from manimlib import *
import numpy as np
from pydub import AudioSegment

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        
#################################################################### 

class Video_2(FrameScene):
    def construct(self):
        basic = MTex(r"(-2)\times (-2)=4", tex_to_color_map = {r"(-2)": RED, r"4": GREEN}).shift(2*UP)
        self.wait(1)
        self.play(Write(basic))
        self.wait()

        general = MTex(r"x\times x \ge 0", tex_to_color_map = {r"x": [RED, GREEN], r"\ge 0": GREEN}).shift(UP)
        general[0].match_x(basic[:4]), general[1].match_x(basic[4]), general[2].match_x(basic[5:9]), general[3].match_x(basic[9]), general[4].match_x(basic[10])
        anims_1 = AnimationGroup(*[TransformFromCopy(basic[i], general[0].copy(), remover = True) for i in range(4)])
        anims_2 = TransformFromCopy(basic[4], general[1])
        anims_3 = AnimationGroup(*[TransformFromCopy(basic[i], general[2].copy(), remover = True) for i in range(5, 9)])
        anims_4 = TransformFromCopy(basic[9], general[3])
        anims_5 = TransformFromCopy(basic[10], general[4])
        self.play(LaggedStart(anims_1, anims_2, anims_3, anims_4, anims_5, lag_ratio = 1/4))
        self.add(general).wait()

        offset = 3.5*LEFT + 1.5*DOWN
        axis = VGroup(Arrow(1.5*DOWN, 5*UP, buff = 0), Arrow(3*LEFT, 3*RIGHT, buff = 0)).shift(offset)
        self.play(*[mob.animate.shift(3*RIGHT) for mob in [basic, general]], FadeIn(axis, 3*RIGHT), run_time = 2)
        self.wait(1)
        graph = FunctionGraph(lambda x: x**2, [-2.2, 2.2, 0.01]).shift(offset)
        label = MTex(r"y=x^2", color = YELLOW).next_to(graph.get_corner(UR), RIGHT).set_stroke(**stroke_dic)#tex_to_color_map = {r"x": [RED, GREEN], r"y": GREEN})
        self.play(ShowCreation(graph), Write(label))
        self.wait()

        half = Rectangle(height = 5, width = 6, stroke_width = 0, fill_opacity = 0.2, color = GREEN).next_to(offset, UP, buff = 0)
        line_h = VMobject().set_points(DashedLine(4*UP + 3*LEFT, 4*UP + 3*RIGHT).shift(offset).get_all_points())
        line_v1, line_v2 = DashedLine(2*LEFT, 4*UP + 2*LEFT).shift(offset), DashedLine(2*RIGHT, 4*UP + 2*RIGHT).shift(offset)
        self.add_background(half).play(half.save_state().scale([1, 0, 1], about_edge = DOWN).animate.restore(), ShowCreation(line_h, start = 0.5), ShowCreation(line_v1), ShowCreation(line_v2))
        label_1 = MTex(r"4", color = GREEN).scale(0.8).next_to(4*UP + offset, RIGHT).set_stroke(**stroke_dic)
        label_2, label_3 = MTex(r"2", color = GREEN).scale(0.6).next_to(2*RIGHT + offset, DOWN, buff = 0.1).set_stroke(**stroke_dic), MTex(r"-2", color = RED).scale(0.6).next_to(2*LEFT + offset, DOWN, buff = 0.1).set_stroke(**stroke_dic)
        self.add_text(label_1, label_2, label_3).play(Write(label_1), Write(label_2), Write(label_3))
        self.wait()

        group = VGroup(line_h, line_v1, line_v2)
        copy_group = group.copy().set_color(GREY)
        alpha = ValueTracker(4.0)
        label_4 = MTex(r"-1", color = RED).scale(0.8).next_to(DOWN + offset, DR).set_stroke(**stroke_dic)
        def line_updater(mob: VGroup):
            y = alpha.get_value()
            mob[0].set_y(y + offset[1])
            if y >= 0:
                x = np.sqrt(y)
                mob[1].become(DashedLine(np.array([-x, 0, 0]), np.array([-x, y, 0])).shift(offset))
                mob[2].become(DashedLine(np.array([x, 0, 0]), np.array([x, y, 0])).shift(offset))
            else:
                if len(mob.submobjects) > 1:
                    mob.remove(mob[1], mob[2])
                    mob[0].set_color(RED)
        group.add_updater(line_updater)
        self.add_text(label_4).add(copy_group, group).play(alpha.animate.set_value(-1), OverFadeIn(label_4), run_time = 2)
        group.clear_updaters()
        self.wait()

        negative = MTexText(r"$x^2=-1$无解", tex_to_color_map = {r"x": [RED, GREEN], r"-1": RED}).shift(DOWN + 3*RIGHT).set_stroke(**stroke_dic)
        self.play(ShowCreation(negative))
        self.wait()

        new_def = MTex(r"x=\sqrt{-1}=", tex_to_color_map = {r"x": YELLOW, r"-1": RED}).shift(1.5*UP)
        new_def.set_x(negative[2].get_x() - new_def[1].get_x())
        self.play(*[OverFadeOut(mob, 2*UP) for mob in [basic, general]], negative.animate.shift(3.5*UP), OverFadeIn(new_def[:-1], 3.5*UP), run_time = 2)
        self.wait()
        notation = MTex(r"=i", tex_to_color_map = {r"i": YELLOW})
        notation.shift(new_def[-1].get_center() - notation[0].get_center())
        new_def.remove(new_def[-1])
        book_1 = LabelPicture("book_1.png", "人教A版数学必修二　第七章复数　第68页", picture_config = {"height": 4/3}).shift(1.5*DOWN).match_x(new_def[4])
        self.play(Write(notation), FadeIn(book_1, UP))
        self.wait()

        books = Group(*[ImageMobject(r"book_"+str(i)+r".png").set_width(5) for i in range(2, 6)]).arrange(direction = DOWN).shift(offset[0]*RIGHT + 0.5*UP)
        self.add_text(books).play(FadeIn(books, RIGHT, lag_ratio = 1/3, run_time = 2), *[FadeOut(mob) for mob in [axis, group, copy_group, label, label_1, label_2, label_3, label_4, half, graph]])
        self.add(books).wait()

        euler = MTex(r"e^{\pi i}=-1", tex_to_color_map = {r"e": BLUE, r"i": YELLOW, r"\pi": RED}).scale(2).set_stroke(**stroke_dic)
        back_1 = BackgroundRectangle(euler, stroke_width = 4, stroke_opacity = 1, stroke_color = WHITE)
        back_2 = BackgroundRectangle(back_1, stroke_width = 4, stroke_opacity = 1, stroke_color = YELLOW_E, buff = 0.08)
        euler = VGroup(back_2, back_1, euler)
        self.play(GrowFromCenter(euler), *[mob.animate.fade() for mob in [books, book_1]])
        self.play(Flash(euler[2][2], flash_radius = 0.5))
        self.wait()

        surr_1 = SurroundingRectangle(VGroup(negative.copy(), new_def.copy().shift(UP), notation.copy().shift(UP)), color = RED)
        text_1 = Songti("无意义？", color = RED).next_to(surr_1.get_top(), UR)
        surr_2 = surr_1.copy().shift(DOWN).set_color(GREEN)
        text_2 = Songti("有意义？", color = GREEN).next_to(surr_2.get_bottom(), DR)
        target = euler.generate_target()
        target[0].set_stroke(color = interpolate_color(YELLOW_E, BLACK, 0.5)), target[1].set_stroke(color = interpolate_color(WHITE, BLACK, 0.5)), target[2].fade()
        self.play(ShowCreation(surr_1), Write(text_1), MoveToTarget(euler))
        self.wait()
        self.play(ShowCreation(surr_2), Write(text_2))
        self.wait()

class Video_3(FrameScene):
    def construct(self):
        buff_h = 1.8
        apple_0, apple_1 = ImageMobject("apple_yellow.png", height = 1.2), ImageMobject("apple_white.png", height = 1.2)
        apples = [(apple_0 if i>=3 else apple_1).copy().move_to(((i-2)*buff_h*RIGHT)) for i in range(5)]
        texts = [MTex(str(i+1), color = YELLOW if i >= 3 else WHITE).move_to(((i-2)*buff_h*RIGHT) + DOWN) for i in range(5)]
        formula = MTex(r"3+2=5", tex_to_color_map = {r"2": YELLOW, r"5": YELLOW_A}).scale(2).shift(1.5*UP)
        formula[0].set_x(-1*buff_h), formula[1].set_x(0.25*buff_h), formula[2].set_x(1.5*buff_h), formula[3:].set_x(3*buff_h)
        self.wait()
        sound_pop = AudioSegment.from_file("pop.ogg")
        for i in range(3):
            self.add(apples[i])
            self.file_writer.add_audio_segment(sound_pop, time = self.get_time())
            self.wait(0, 10)
        self.wait()
        for i in range(3):
            self.play(ShowCreation(texts[i]))
        self.play(Write(formula[0]))
        self.wait()

        self.file_writer.add_audio_segment(sound_pop, time = self.get_time())
        apples[3].time = self.get_time()
        def adding_updater(mob: Mobject):
            if self.get_time() >= mob.time + 1/3:
                self.add(apples[4])
                self.file_writer.add_audio_segment(sound_pop, time = self.get_time())
                mob.clear_updaters()
        self.add(apples[3].add_updater(adding_updater))
        self.play(Write(formula[2]))
        self.wait()    

        self.play(ShowCreation(texts[3]))
        self.play(ShowCreation(texts[4]))
        self.play(Write(formula[1]), Write(formula[3]), Write(formula[4]))
        self.wait()

        apple_2 = ImageMobject("apple_yellow_a.png", height = 1.2)
        apples_2 = [apple_2.copy().move_to(((i-2)*buff_h*RIGHT)) for i in range(5)]
        self.play(*[FadeIn(mob) for mob in apples_2], formula[4].animating(remover = True).set_x(0), follow(formula[:4], formula[4], OverFadeOut), *[mob.animate.set_color(YELLOW_A) for mob in texts])
        self.remove(*apples)
        formula = MTex(r"5-1=4", tex_to_color_map = {r"5": YELLOW_A, r"-1": RED, r"4": ORANGE}).scale(2).shift(1.5*UP)
        formula[0].set_x(0*buff_h), formula[1:3].set_x(2*buff_h), formula[3:].set_x(3*buff_h)
        self.add(formula[0]).wait()

        eats = [AudioSegment.from_file("eat1.ogg"), AudioSegment.from_file("eat2.ogg"), AudioSegment.from_file("eat3.ogg")]
        burp = AudioSegment.from_file("burp.ogg")
        position = 2*buff_h*RIGHT
        def fall_updater(mob: ImageMobject, dt):
            mob.shift(dt*mob.v)
            mob.v += 5*dt*DOWN
            opacity = mob.data["opacity"][0] - 2*dt
            mob.set_opacity(opacity)
            if opacity <= 0:
                self.remove(mob)
        def eaten_updater(mob: ImageMobject):
            piece = ImageMobject("apple_enlarged.png", height = 0.3).shift(position)
            x, y = 0.8*random.random()+0.1, 0.8*random.random()+0.1
            piece.data["im_coords"] = np.array([(x-0.1, y-0.1), (x-0.1, y+0.1), (x+0.1, y-0.1), (x+0.1, y+0.1)])
            piece.v = 3*unit(TAU*random.random())
            self.add_background(piece.add_updater(fall_updater).shift(0.2*piece.v))
            shake = np.array([2*random.random()-1, 2*random.random()-1, 0])*0.1
            mob.move_to(interpolate(mob.get_center(), shake + position, 0.2))
            if self.frames % 5 == 0:
                self.file_writer.add_audio_segment(random.choice(eats), time = self.get_time())
        apples_2[4].add_updater(eaten_updater)
        self.play(Write(formula[1:3]))
        apples_2[4].clear_updaters().set_opacity(0.2).move_to(position), texts[4].set_opacity(0.2)
        self.file_writer.add_audio_segment(random.choice(eats), time = self.get_time())
        self.file_writer.add_audio_segment(burp, time = self.get_time())
        self.wait(1)
        self.play(Write(formula[3:]))
        self.wait()
        self.file_writer.add_audio_segment(sound_pop[:0], time = self.get_time())

        self.play(*[mob.animate.shift(1.5*buff_h*RIGHT) for mob in apples_2[:2] + texts[:2]], 
                  *[OverFadeOut(mob, 1.5*buff_h*RIGHT) for mob in apples_2[2:] + texts[2:] + [formula]], run_time = 2)
        self.wait()

        formula = MTex(r"2-3=?", tex_to_color_map = {r"2": YELLOW_A, r"-3": RED, r"?": ORANGE}).scale(2).shift(1.5*UP)
        self.play(Write(formula))
        self.wait()

        apple_3, stroke = ImageMobject("apple_enlarged.png", height = 1.2).shift(-1.5*buff_h*RIGHT), ImageMobject("apple_stroke.png", height = 1.2).shift(-1.5*buff_h*RIGHT)
        def blink_updater(mob: ImageMobject):
            if self.frames % 20 == 5:
                self.add(apple_3)
            if self.frames % 20 == 15:
                self.remove(apple_3)
        self.add(stroke.add_updater(blink_updater))
        question = MTex(r"???", color = GREY).shift(-1.5*buff_h*RIGHT + DOWN)
        self.play(Write(question))
        self.wait(1)
        stroke.clear_updaters(), self.remove(apple_3)
        self.wait()

class Patch_6(FrameScene):
    def construct(self):
        buff_h = 1.8
        formula = MTex(r"2-3=?", tex_to_color_map = {r"2": GREEN, r"-3": RED, r"?": ORANGE}).scale(2).shift(1.5*UP)
        apples = [ImageMobject("apple_green.png", height = 1.2).shift((i-0)*buff_h*RIGHT) for i in range(2)]
        texts = [MTex(str(i+1), color = GREEN).move_to(((i-0)*buff_h*RIGHT) + DOWN) for i in range(2)]
        stroke = ImageMobject("apple_stroke.png", height = 1.2).shift(-1*buff_h*RIGHT)
        question = MTex(r"???", color = GREY).shift(-1*buff_h*RIGHT + DOWN)
        self.add(formula, *apples, *texts, stroke, question)

class Video_6(FrameScene):
    def construct(self):
        equation_0 = MTex(r"2-3+4={3}", tex_to_color_map = {(r"2", r"+4", r"{3}"): GREEN, r"-3": RED}).scale(2).shift(2*UP)
        self.wait()
        self.play(Write(equation_0))
        self.wait()

        surr = SurroundingRectangle(equation_0[:3])
        pic = ImageMobject("Patch_6.png", height = 2).match_x(surr).set_y(-1)
        ratio = 0.5
        pic.data["im_coords"] = np.array([(0.5-ratio/2, 0.5-ratio/2), (0.5-ratio/2, 0.5+ratio/2), (0.5+ratio/2, 0.5-ratio/2), (0.5+ratio/2, 0.5+ratio/2)])
        surr_2 = SurroundingRectangle(pic, color = RED)
        self.play(equation_0[-2:].animate.shift(0.2*DOWN).set_fill(opacity = 0.2), ShowCreation(surr), FadeIn(pic, UP), FadeIn(surr_2, UP))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [surr, pic, surr_2]])
        self.wait()
        
        part_1, part_2 = equation_0[1:3].save_state(), equation_0[3:5].save_state()
        self.play(part_1.animating(path_arc = PI).match_x(part_2), part_2.animating(path_arc = PI).match_x(part_1))
        branch = MTex(r"=6", tex_to_color_map = {r"6": GREEN}).scale(1.5)
        branch[0].rotate(PI/4).next_to(part_2, UR, buff = 0.1), branch[1].next_to(branch[0], UR, buff = 0.1)
        self.play(Write(branch))
        self.wait()
        self.play(equation_0[-2:].animate.shift(0.2*UP).set_fill(opacity = 1))
        self.wait()

        # randoms, sums = [], []
        # sum_of_all = 0
        # for _ in range(30):
        #     integer = random.randint(-9, 9)
        #     if integer != 0 and abs(sum_of_all + integer) < 10:
        #         randoms.append(integer)
        #         sum_of_all += integer
        #         sums.append(sum_of_all)
        # print(randoms, sums)
        randoms = [3, 4, -8, -1, 7, 3, -3, -5, -5, -1, 8, -5, -6, 1, 6, 8, -6, 2, 4, 1]
        sums = [3, 7, -1, -2, 5, 8, 5, 0, -5, -6, 2, -3, -9, -8, -2, 6, 0, 2, 6, 7]
        texs = []
        for i, number in enumerate(randoms):
            str_form = str(number)
            if i > 0 and number > 0:
                str_form = "+" + str_form
            tex_i = MTex(str_form, color = GREEN if number > 0 else RED).scale(1.25).shift(1*DOWN + (-6+i*1)*RIGHT).set_stroke(**stroke_dic)
            texs.append(tex_i)
        randoms_copy, texs_copy = randoms[:], [mob.copy() for mob in texs]
        self.play(LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in texs], lag_ratio = 0.2))
        self.add_text(*texs).wait()

        the_sum = randoms[0]
        length = len(randoms)
        equals = []
        for i in range(1, length):
            new_sum = the_sum + randoms[i]
            if new_sum < 0:
                equal = MTex(r"=???", tex_to_color_map = {r"?": RED})
                equal[0].rotate(PI/4).move_to(1*DOWN + (-6+i*1)*RIGHT + 0.5*UR), equal[1:].move_to(1*DOWN + (-6+i*1)*RIGHT + 0.9*UR)
                self.play(Write(equal))
                for j in range(i+1, length):
                    if the_sum + randoms[j] >= 0:
                        randoms[i], randoms[j] = randoms[j], randoms[i]
                        self.play(FadeOut(equal), texs[i].animating(path_arc = PI).match_x(texs[j]), texs[j].animating(path_arc = PI).match_x(texs[i]))
                        texs[i], texs[j] = texs[j], texs[i]
                        new_sum = the_sum + randoms[i]
                        break
            the_sum = new_sum
            str_sum = str(the_sum)
            equal = MTex(r"="+str_sum, tex_to_color_map = {str_sum: GREEN})
            equal[0].rotate(PI/4).move_to(1*DOWN + (-6+i*1)*RIGHT + 0.5*UR), equal[1:].move_to(1*DOWN + (-6+i*1)*RIGHT + 0.9*UR)
            self.play(Write(equal))
            equals.append(equal)
        self.wait()

        self.remove(*texs, *equals, branch).add(*texs_copy), part_1.restore(), part_2.restore()
        branch = MTex(r"=-1", tex_to_color_map = {r"-1": RED}).scale(1.5)
        branch[0].rotate(-PI/4).next_to(part_1, DR, buff = 0.1), branch[1:].next_to(branch[0], DR, buff = 0.1)
        self.add(branch).wait()
        the_sum = randoms_copy[0]
        length = len(randoms_copy)
        for i in range(1, length):
            the_sum += randoms_copy[i]
            str_sum = str(the_sum)
            if the_sum < 0:
                equal = MTex(r"="+str_sum, tex_to_color_map = {str_sum: RED})
                equal[0].rotate(-PI/4).move_to(1*DOWN + (-6+i*1)*RIGHT + 0.5*DR), equal[1:].move_to(1*DOWN + (-6+i*1)*RIGHT + 0.9*DR)
            else:
                equal = MTex(r"="+str_sum, tex_to_color_map = {str_sum: GREEN})
                equal[0].rotate(PI/4).move_to(1*DOWN + (-6+i*1)*RIGHT + 0.5*UR), equal[1:].move_to(1*DOWN + (-6+i*1)*RIGHT + 0.9*UR)
            self.play(Write(equal))
        self.wait()
        
class Patch6_1(FrameScene):
    def construct(self):
        self.wait()
        self.play(FadeIn(ImageMobject("Video_6.png", height = 8)))
        self.wait()

class Patch9_1(FrameScene):
    def construct(self):
        buff_h = 1.8
        #formula = MTex(r"2-3=?", tex_to_color_map = {r"2": GREEN, r"-3": RED, r"?": ORANGE}).scale(2).shift(1.5*UP)
        apples = [ImageMobject("apple_green.png", height = 1.2).shift((i-0)*buff_h*RIGHT) for i in range(2)]
        texts = [MTex(str(i+1), color = GREEN).move_to(((i-0)*buff_h*RIGHT) + DOWN) for i in range(2)]
        stroke = ImageMobject("apple_stroke.png", height = 1.2).shift(-1*buff_h*RIGHT)
        question = MTex(r"???", color = GREY).shift(-1*buff_h*RIGHT + DOWN)
        Group(*apples, *texts, stroke, question).center()
        self.add(*apples, *texts, stroke, question)

class Patch9_2(FrameScene):
    def construct(self):
        offset = 1.75*DOWN
        axis = VGroup(Arrow(1.5*DOWN, 5*UP, buff = 0, stroke_width = 8), Arrow(3*LEFT, 3*RIGHT, buff = 0, stroke_width = 8)).shift(offset)
        graph = FunctionGraph(lambda x: x**2, [-2.2, 2.2, 0.01], stroke_width = 8).shift(offset)
        label = MTex(r"y=x^2", color = YELLOW).next_to(graph.get_corner(UR), RIGHT).set_stroke(**stroke_dic)
        half = Rectangle(height = 5, width = 6, stroke_width = 0, fill_opacity = 0.2, color = GREEN).next_to(offset, UP, buff = 0)
        line_h1 = VMobject(stroke_width = 8).set_points(DashedLine(4*UP + 3*LEFT, 4*UP + 3*RIGHT).shift(offset).get_all_points())
        line_v1, line_v2 = DashedLine(2*LEFT, 4*UP + 2*LEFT, stroke_width = 8).shift(offset), DashedLine(2*RIGHT, 4*UP + 2*RIGHT, stroke_width = 8).shift(offset)
        line_h2 = VMobject(color = RED, stroke_width = 8).set_points(DashedLine(DOWN + 3*LEFT, DOWN + 3*RIGHT).shift(offset).get_all_points())
        label_1 = MTex(r"4", color = GREEN).scale(1.5).next_to(4*UP + offset, RIGHT).set_stroke(**stroke_dic)
        label_2, label_3 = MTex(r"2", color = GREEN).scale(1.5).next_to(2*RIGHT + offset, DOWN).set_stroke(**stroke_dic), MTex(r"-2", color = RED).scale(1.5).next_to(2*LEFT + offset, DOWN).set_stroke(**stroke_dic)
        label_4 = MTex(r"-1", color = RED).scale(1.5).next_to(DOWN + offset, DR).set_stroke(**stroke_dic)
        self.add(half, axis, graph, label, line_h1, line_v1, line_v2, line_h2).add_text(label_1, label_2, label_3, label_4)

class Video_9(FrameScene):
    def construct(self):
        mtex_1 = MTex(r"2-3+4={3}", tex_to_color_map = {r"2": GREEN, r"-3": RED, r"+4": GREEN, r"{3}": GREEN}).scale(2).shift(2.2*UP + 3*LEFT)
        mtex_2 = MTex(r"\sqrt[3]{2+11\sqrt{-1}}+\sqrt[3]{2-11\sqrt{-1}}=4", tex_to_color_map = {(r"2", r"4"): GREEN, r"\sqrt{-1}": RED}).shift(1.5*DOWN + 3*LEFT)

        pic_1 = ImageMobject("Patch9_1.png", height = 3).move_to(2.2*UP + 4*RIGHT)
        ratio = 0.5
        pic_1.data["im_coords"] = np.array([(0.5-ratio/2, 0.5-ratio/2), (0.5-ratio/2, 0.5+ratio/2), (0.5+ratio/2, 0.5-ratio/2), (0.5+ratio/2, 0.5+ratio/2)])
        pic_2 = ImageMobject("Patch9_2.png", height = 3).move_to(1.5*DOWN + 4*RIGHT)
        surr_1, surr_2 = SurroundingRectangle(pic_1, color = RED), SurroundingRectangle(pic_2, color = RED)
        self.add(mtex_1, mtex_2, pic_1, pic_2, surr_1, surr_2).wait()

        indicate_1, indicate_2 = SurroundingRectangle(mtex_1[:3]), VGroup(*[SurroundingRectangle(mob) for mob in mtex_2.get_parts_by_tex(r"\sqrt{-1}")])
        self.play(ShowCreation(indicate_1), ShowCreation(indicate_2, lag_ratio = 0))
        self.wait()
        self.play(*[mob.save_state().animate.fade(0.8).scale(0.8).shift(RIGHT) for mob in [pic_1, surr_1]])
        self.wait()

        checkmark_1, checkmark_2 = MTex(r"\checkmark", color = YELLOW).next_to(indicate_1, DOWN), MTex(r"\checkmark", color = YELLOW).next_to(indicate_2[0], DOWN)
        branch_1, branch_2 = MTex(r"=-1", tex_to_color_map = {r"-1": YELLOW}).scale(1.5), MTex(r"=i", tex_to_color_map = {r"i": YELLOW}).scale(1.5) 
        branch_1[0].rotate(-PI/4).next_to(indicate_1, DR, buff = 0.1), branch_1[1:].next_to(branch_1[0], DR, buff = 0.1)
        branch_2[0].rotate(-PI/4).next_to(indicate_2[0], DR, buff = 0.1), branch_2[1:].next_to(branch_2[0], DR, buff = 0.1)
        self.play(ShowCreation(checkmark_1))
        self.wait()
        self.play(Write(branch_1))
        self.wait()

        self.play(Flash(mtex_1[-1], flash_radius = 0.5))
        self.wait()

        self.play(*[mob.animate.restore() for mob in [pic_1, surr_1]], ShowCreation(checkmark_2), Write(branch_2))
        self.wait()

        arrow_1, arrow_2 = Arrow(surr_1.get_corner(UL), indicate_1.get_corner(UR), color = RED, path_arc = PI/6), Arrow(surr_2.get_corner(UL), indicate_2.get_corner(UR), color = RED, path_arc = PI/6)
        cross_1, cross_2 = Cross(Square()).move_to(arrow_1.point_from_proportion(0.5)).scale(0.5), Cross().move_to(arrow_2.point_from_proportion(0.5)).scale(0.5)
        self.play(ShowCreation(arrow_1), ShowCreation(arrow_2))
        self.play(ShowCreation(cross_1), ShowCreation(cross_2))
        self.wait()

        window = FloatWindow(width = 16, inner_dic = {"fill_opacity": 1,  "fill_color": GREY_E, "stroke_color": WHITE}).shift(3.7*DOWN)
        randoms = [3, 4, -8, -1, 7, 3, -3, -5, -5, -1, 8, -5, -6, 1, 6, 8, -6, 2, 4, 1]
        texs = []
        for i, number in enumerate(randoms):
            str_form = str(number)
            if i > 0 and number > 0:
                str_form = "+" + str_form
            tex_i = MTex(str_form, color = GREEN if number > 0 else RED).scale(1.25).shift(1*DOWN + (-6+i*1)*RIGHT).set_stroke(width = 8, color = GREY_E, background = True)
            texs.append(tex_i)
        buff_h = 0.7
        numberline = VGroup(Line(LEFT_SIDE, RIGHT_SIDE), *[Line(0.1*UP, 0.1*DOWN).shift(buff_h*i*RIGHT) for i in range(-10, 11)], *[MTex(str(i), color = YELLOW).scale(0.8).next_to(buff_h*i*RIGHT + 0.1*DOWN, DOWN) for i in range(-10, 11)]).shift(2.5*DOWN)
        dot = Dot(color = DARK_BROWN, stroke_width = 4, stroke_color = YELLOW).shift(3*buff_h*RIGHT + 2.5*DOWN)
        self.play(*[mob.shift(4.5*DOWN).animate.shift(4.5*UP) for mob in [window, *texs, numberline, dot]])
        self.wait()

        equals = []
        length = len(randoms)
        the_sum = randoms[0]
        p_old = the_sum*buff_h*RIGHT + 2.5*DOWN
        surr = SurroundingRectangle(texs[1])
        the_sum += randoms[1]
        p_new = the_sum*buff_h*RIGHT + 2.5*DOWN
        n, m = 100, 10
        widths = [5]*(3*(n-m)) + [0]*(3*m)
        decrease = [20*i/(2*m) for i in range(2*m, -1, -1)]
        widths[3*(n-m)::3] = decrease[:-2:2]
        widths[3*(n-m)+1::3] = decrease[1::2]
        widths[3*(n-m)+2::3] = decrease[2::2]
        arrow = ArcBetweenPoints(p_old, p_new, angle = -4*np.arctan(1/randoms[1]), buff = 0.2, n_components = n+20)
        arrow.set_points(arrow.get_points()[30:-30]).set_stroke(width = widths).set_color(GREEN)
        self.play(ShowCreation(surr), ShowCreation(arrow))
        self.wait(1)
        equal = MTex(r"="+str(7), tex_to_color_map = {str(7): YELLOW})
        equal[0].rotate(PI/4).move_to(1*DOWN + (-6+1)*RIGHT + 0.5*UR), equal[1:].move_to(1*DOWN + (-6+1)*RIGHT + 0.9*UR)
        self.play(Write(equal), Uncreate(arrow, start = 1), dot.animating(path_arc = -4*np.arctan(1/randoms[1])).move_to(p_new))
        self.wait(1)
        equals.append(equal)
        p_old = p_new
        for i in range(2, length):
            the_sum += randoms[i]
            p_new = the_sum*buff_h*RIGHT + 2.5*DOWN
            arrow = ArcBetweenPoints(p_old, p_new, angle = -4*np.arctan(1/randoms[i]), buff = 0.2, n_components = n+20)
            arrow.set_points(arrow.get_points()[30:-30]).set_stroke(width = widths).set_color(GREEN if randoms[i] > 0 else RED)
            self.add(arrow, dot).play(Transform(surr, SurroundingRectangle(texs[i])), ShowCreation(arrow))
        
            str_sum = str(the_sum)
            equal = MTex(r"="+str_sum, tex_to_color_map = {str_sum: YELLOW})
            equal[0].rotate(PI/4).move_to(1*DOWN + (-6+i*1)*RIGHT + 0.5*UR), equal[1:].move_to(1*DOWN + (-6+i*1)*RIGHT + 0.9*UR)
            self.play(Write(equal), Uncreate(arrow, start = 1), dot.animating(path_arc = -4*np.arctan(1/randoms[i])).move_to(p_new))
            equals.append(equal)
            p_old = p_new
        self.wait()

class Patch9_3(FrameScene):
    def construct(self):
        # back = ImageMobject("Video_9.png", height = 8)
        # self.add(back)
        window = FloatWindow(inner_dic = {"fill_opacity": 1,  "fill_color": GREY_E, "stroke_color": WHITE}).shift(4.4*UP + 7.5*RIGHT)
        integral = MTex(r"\int_2^1f(x)\,dx=-\int_1^2f(x)\,dx", tex_to_color_map = {r"\int_2^1f(x)\,dx": RED, r"\int_1^2f(x)\,dx": GREEN}).shift(2.0*UP + 3.75*RIGHT)
        self.play(*[mob.shift(4*UP + 7.5*RIGHT).animate.shift(4*DOWN + 7.5*LEFT) for mob in [window, integral]])
        self.wait(1)
        self.play(*[mob.animate.shift(4*UP + 7.5*RIGHT) for mob in [window, integral]])

class Patch9_4(FrameScene):
    def construct(self):
        self.wait()
        self.play(FadeIn(ImageMobject("Video_10.png", height = 8)))
        self.wait()

class FlushInY(Transform):
    def __init__(
        self,
        mobject: VMobject,
        top: float | None = None,
        bottom: float | None = None,
        middle: float | None = None,
        buff: float = 0.2, 
        **kwargs
    ):
        if top is None:
            top = mobject.get_top()[0] - buff
        if bottom is None:
            bottom = mobject.get_bottom()[0] + buff
        if middle is None:
            middle = mobject.get_center()[0]

        for mob in mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("flushin_fill_y")
            mob.stroke_shader_wrapper.reset_shader("flushin_stroke_y")
            mob.uniforms["mask_t"] = middle
            mob.uniforms["mask_b"] = middle
        target = mobject.copy()
        for mob in target.get_family():
            mob.uniforms["mask_t"] = top
            mob.uniforms["mask_b"] = bottom
        
        super().__init__(mobject, target, **kwargs)

    def finish(self) -> None:
        for mob in self.mobject.get_family():
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
            mob.uniforms.pop("mask_t"), mob.uniforms.pop("mask_b")
        super().finish()

def poly(x, coefs):
    return sum(coefs[k] * x**k for k in range(len(coefs)))

def dpoly(x, coefs):
    return sum(k * coefs[k] * x**(k - 1) for k in range(1, len(coefs)))

def find_root(func, dfunc, seed=complex(1, 1), tol=1e-8, max_steps=100):
    # Use newton's method
    last_seed = np.inf
    for n in range(max_steps):
        if abs(seed - last_seed) < tol:
            break
        last_seed = seed
        seed = seed - func(seed) / dfunc(seed)
    return seed

def coefficients_to_roots(coefs):
    if len(coefs) == 0:
        return []
    elif coefs[-1] == 0:
        return coefficients_to_roots(coefs[:-1])
    roots = []
    # Find a root, divide out by (x - root), repeat
    for i in range(len(coefs) - 1):
        root = find_root(
            lambda x: poly(x, coefs),
            lambda x: dpoly(x, coefs),
        )
        roots.append(root)
        new_reversed_coefs, rem = np.polydiv(coefs[::-1], [1, -root])
        coefs = new_reversed_coefs[::-1]
    return roots

class Video_10(FrameScene):
    #复数那段
    def construct(self):
        # back = ImageMobject("Video_9.png", height = 8)
        # self.add(back)
        window = FloatWindow(width = 20, 
                             outer_dic = {"fill_opacity": 1, "fill_color": "#222222", "stroke_color": WHITE}, 
                             inner_dic = {"fill_opacity": 1,  "fill_color": BLACK, "stroke_color": YELLOW_E}).shift(4.3*UP)
        buff_h = 0.7
        n = 15
        numberline = VGroup(Line(buff_h*(n+1/2)*LEFT, buff_h*(n+1/2)*RIGHT), *[Line(0.1*UP, 0.1*DOWN).shift(buff_h*i*RIGHT) for i in range(-n, n+1)], *[MTex(str(i), color = YELLOW).scale(0.8).next_to(buff_h*i*RIGHT + 0.1*DOWN, DOWN).set_stroke(**stroke_dic) for i in range(-n, n+1)]).shift(2.5*DOWN)
        self.add_background(numberline).add(window).wait(1)

        offset_r = RIGHT_SIDE/2
        imaginary = MTex(r"\sqrt{-1}=i", tex_to_color_map = {r"\sqrt{-1}": YELLOW, r"i": YELLOW}).scale(1.5).shift(3*UP)
        self.play(Write(imaginary))
        self.wait()
        example = MTex(r"3+4i", tex_to_color_map = {(r"3", r"4"): GREEN, r"i": YELLOW}).shift(1.5*UP + offset_r).set_stroke(**stroke_dic)
        example_origin = MTex(r"3+4\sqrt{-1}", tex_to_color_map = {(r"3", r"4"): GREEN, r"\sqrt{-1}": YELLOW}).shift(1.5*UP).set_stroke(**stroke_dic)
        self.play(Write(example_origin))
        self.wait()
        
        offset_l = 4*LEFT + 2.5*DOWN
        target = numberline.generate_target()
        for mob in target[2*n+2:]:
            mob.scale(0.8, about_edge = UP).shift(0.1*UP)
        target.scale(0.8, about_point = 2.5*DOWN).shift(4*LEFT)
        target = example_origin.generate_target()
        for i in range(3):
            target[i].become(example[i])
        for mob in target[3:]:
            mob.become(example[3])
        text_complex = Songti(r"复数", color = YELLOW).next_to(example, RIGHT, buff = 1)
        surr_complex = SurroundingRectangle(text_complex, color = WHITE)
        surr_complex_2 = SurroundingRectangle(surr_complex, color = YELLOW_E)
        self.play(Rotate(window, angle = -PI/2, about_point = 0.3*UP), imaginary.animate.shift(offset_r), MoveToTarget(numberline), MoveToTarget(example_origin), run_time = 2)
        self.remove(example_origin).add(example).play(Write(text_complex), ShowCreation(surr_complex), ShowCreation(surr_complex_2))
        self.wait()

        imaginaryline = VGroup(Line(buff_h*(n+1/2)*DOWN, buff_h*(n+1/2)*UP), *[Line(0.1*LEFT, 0.1*RIGHT).shift(buff_h*i*UP) for i in range(-n, n+1)], *[MTex(str(i)+"i", color = YELLOW).scale(0.64).next_to(buff_h*i*UP + 0.1*LEFT, LEFT, buff = 0.1).set_stroke(**stroke_dic) for i in list(range(-n, 0))+list(range(1, n+1))]).scale(0.8, about_point = ORIGIN).shift(offset_l)
        buff_h *= 0.8
        def small(x, y):
            return buff_h*x*RIGHT + buff_h*y*UP
        def coor(x, y):
            return buff_h*x*RIGHT + buff_h*y*UP + offset_l
        #cover the plane with grid
        grid = VGroup(*[Line(coor(-n, i), coor(n, i), stroke_width = 2, color = GREY_E) for i in range(-n, n+1)], *[Line(coor(i, -n), coor(i, n), stroke_width = 2, color = GREY_E) for i in range(-n, n+1)])
        self.add_background(grid, imaginaryline, numberline, numberline[3*n+2]).play(FadeIn(grid), numberline[3*n+2].animate.next_to(offset_l + 0.1*DL, DL, buff = 0.1), FlushInY(imaginaryline, 4, -4, -2.5))
        part_1, part_2 = example[0], example[2:]
        line_1, line_2 = Line(coor(3, 0), coor(3, 4), color = GREEN, stroke_width = 4), Line(coor(0, 4), coor(3, 4), color = GREEN, stroke_width = 4)
        dot = Dot(color = GREEN).move_to(coor(3, 4))
        label = example.copy().scale(0.8).next_to(dot, UR, buff = 0.1)
        self.play(TransformFromCopy(VGroup(part_1), numberline[3*n+5].copy()), TransformFromCopy(part_2, imaginaryline[3*n+5]).copy(), remover = True)
        self.add_background(line_1, line_2).play(ShowCreation(line_1), ShowCreation(line_2))
        self.play(ShowCreation(dot), TransformFromCopy(example, label))
        self.add_background(dot, label).wait()

        titleback, title, titleline = TitleBack(), Title("复平面"), TitleLine()
        self.add_top(titleback, title, titleline).play(*[mob.shift(UP).animate.shift(DOWN) for mob in [title, titleback]], GrowFromPoint(titleline, 4*UP), imaginary.animate.scale(2/3).next_to(surr_complex_2, UP))
        self.wait()

        shade_up, shade_down = Shade(fill_opacity = 0.75).next_to(2.5*DOWN, UP, buff = 0.5), Shade(fill_opacity = 0.75).next_to(2.5*DOWN, DOWN, buff = 0.5)
        dot_real = Dot(color = GREEN, stroke_width = 4, stroke_color = RED).move_to(coor(3, 0))
        self.add_background(shade_up, shade_down).play(FadeIn(shade_up, 6*DOWN), FadeIn(shade_down, 6*UP), GrowFromCenter(dot_real), run_time = 2)
        self.wait()

        # n, m = 100, 10
        # widths = [5]*(3*(n-m)) + [0]*(3*m)
        # decrease = [20*i/(2*m) for i in range(2*m, -1, -1)]
        # widths[3*(n-m)::3] = decrease[:-2:2]
        # widths[3*(n-m)+1::3] = decrease[1::2]
        # widths[3*(n-m)+2::3] = decrease[2::2]
        # arrow = ArcBetweenPoints(coor(3, 0), coor(-1, 0), angle = -4*np.arctan(1/-4), buff = 0.2, n_components = n+20)
        # arrow.set_points(arrow.get_points()[30:-30]).set_stroke(width = widths).set_color(GREEN)
        text_1 = MTex(r"-5", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(dot_real)
        self.play(dot_real.animating(path_arc = -4*np.arctan(1/-5)).move_to(coor(-2, 0)), FadeOut(text_1, UP))
        text_2 = MTex(r"+4", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(dot_real, LEFT)
        self.play(dot_real.animating(path_arc = -4*np.arctan(1/4)).move_to(coor(2, 0)), FadeOut(text_2, UP))
        text_3 = MTex(r"\times 3", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(dot_real, LEFT)
        self.play(dot_real.animating(path_arc = -4*np.arctan(1/4)).move_to(coor(6, 0)), FadeOut(text_3, UP))
        text_4 = MTex(r"\divisionsymbol 2", color = GREEN).scale(0.8).set_stroke(**stroke_dic).next_to(dot_real)
        self.play(dot_real.animating(path_arc = -4*np.arctan(1/-3)).move_to(coor(3, 0)), FadeOut(text_4, UP))
        arrow_1 = Arrow(coor(0, 0), coor(3, 4), buff = 0, color = GREEN)
        self.play(*[FadeOut(mob) for mob in [shade_up, shade_down, dot_real]], *[mob.animating(remover = True).scale(0, about_point = coor(3, 4)) for mob in [line_1, line_2, dot]], GrowArrow(arrow_1))
        self.wait()

        label_2 = MTex(r"2-i", tex_to_color_map = {r"2": BLUE, r"i": YELLOW}).scale(0.8).next_to(coor(2, -1), DL, buff = 0.1)
        arrow_2 = Arrow(coor(0, 0), coor(2, -1), buff = 0, color = BLUE)
        text_add = MTex(r"&(3+4i)+(2-i)\\=&(3+2)+(4-1)i\\=&\ 5+{3}i", tex_to_color_map = {(r"3", r"4"): GREEN, (r"2", r"1"): BLUE, (r"5", r"{3}"): TEAL, r"i": YELLOW}).shift(0.5*DOWN + offset_r)
        part_1, part_2, part_3 = text_add[:12], text_add[12:25], text_add[25:]
        self.play(GrowArrow(arrow_2), Write(label_2), Write(part_1))
        self.wait()

        copy_1, copy_2 = arrow_1.copy(), arrow_2.copy()
        frame = VGroup(*[part_2[i] for i in [0, 1, 5, 6, 7, 11, 12]])
        self.play(copy_1.animate.shift(small(2, -1)), copy_2.animate.shift(small(3, 4)), Write(frame))
        self.play(*[TransformFromCopy(part_1[i], part_2[j].copy(), remover = True) for (i, j) in [(1, 2), (3, 8), (6, 3), (8, 4), (9, 9), (9, 10)]])
        self.add(part_2).wait()

        label_3 = MTex(r"5+3i", tex_to_color_map = {(r"5", r"3"): TEAL, r"i": YELLOW}).scale(0.8).next_to(coor(5, 3), RIGHT, buff = 0.1)
        arrow_3 = Arrow(coor(0, 0), coor(5, 3), buff = 0, color = TEAL)
        self.play(GrowArrow(arrow_3), Write(label_3), Write(part_3))
        self.wait()

        self.play(*[FadeOut(mob) for mob in [label_2, label_3, arrow_2, arrow_3, copy_1, copy_2, text_add]])
        label_2 = MTex(r"1+i", tex_to_color_map = {r"1": BLUE, r"i": YELLOW}).scale(0.8).next_to(coor(1, 1), RIGHT, buff = 0.1).set_stroke(**stroke_dic)
        arrow_2 = Arrow(coor(0, 0), coor(1, 1), buff = 0, color = BLUE)
        self.play(*[FadeIn(mob) for mob in [label_2, arrow_2]])
        self.wait()

        text_mul = MTex(r"&(3+4i)(1+i)\\=&\ {3}+i+{4}i+{4}i^2\\=&-1+7i", tex_to_color_map = {(r"3", r"4"): GREEN, (r"1"): BLUE, (r"{3}", r"{4}", r"-1", r"7"): TEAL, r"i": YELLOW}).shift(0.5*DOWN + offset_r)
        part_1, part_2, part_3 = text_mul[:11], text_mul[11:22], text_mul[22:]
        indicate = SurroundingRectangle(part_2[-2:])
        branch = MTex(r"=-1", tex_to_color_map = {r"-1": GREEN})
        branch[0].rotate(-PI/4).next_to(indicate, DR, buff = 0.1), branch[1:].next_to(branch[0], DR, buff = 0.1)
        label_3 = MTex(r"-1+7i", tex_to_color_map = {(r"-1", r"7"): TEAL, r"i": YELLOW}).scale(0.8).next_to(coor(-1, 7), UL, buff = 0.1).set_stroke(**stroke_dic)
        arrow_3 = Arrow(coor(0, 0), coor(-1, 7), buff = 0, color = BLUE)
        self.play(Write(part_1))
        self.play(Write(part_2))
        self.play(ShowCreation(indicate), Write(branch))
        self.play(Write(part_3), GrowArrow(arrow_3), Write(label_3))
        self.wait()

        length_1, length_2, length_3 = MTex(r"5", color = GREEN).scale(0.8).next_to(arrow_1.get_center(), UL, buff = 0.1).set_stroke(**stroke_dic), MTex(r"\sqrt2", color = BLUE).scale(0.8).next_to(arrow_2.get_center(), DR, buff = 0.1).set_stroke(**stroke_dic), MTex(r"5\sqrt2", color = TEAL).scale(0.8).next_to(arrow_3.get_center(), DL, buff = 0.1).set_stroke(**stroke_dic)
        norm = MTex(r"{5\sqrt2}=5\times \sqrt2", tex_to_color_map = {r"5": GREEN, r"\sqrt2": BLUE, r"{5\sqrt2}": TEAL}).shift(2.25*DOWN + offset_r)
        self.add_lower(length_1, length_2, length_3, label, label_2, label_3).play(Write(length_1), Write(length_2), Write(length_3), Write(norm))
        self.wait()

        axes, coors = VGroup(*numberline[:2*n+2], imaginaryline[:2*n+2]), VGroup(*numberline[2*n+2:], imaginaryline[2*n+2:])
        copy_axes, copy_arrow_1 = axes.copy().set_color(GREY_E), arrow_1.copy().set_color(GREEN_E)
        triangle_1, trialgle_2 = Polygon(coor(0, 0), coor(1, 0), coor(1, 1), stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE), Polygon(coor(0, 0), coor(3, 4), coor(-1, 7), stroke_width = 0, fill_opacity = 0.2, fill_color = GREEN)
        self.add_background(copy_axes, axes, coors, copy_arrow_1, arrow_1, arrow_2, arrow_3).play(*[Rotate(mob.save_state(), angle = PI/4, about_point = coor(0, 0)) for mob in [axes, arrow_1]])
        self.bring_to_back(grid, copy_axes, triangle_1, trialgle_2).play(*[mob.animate.scale(np.sqrt(2), about_point = coor(0, 0)) for mob in [axes, arrow_1]], *[GrowFromPoint(mob, coor(0, 0)) for mob in [triangle_1, trialgle_2]])
        self.wait()

        self.play(*[FadeOut(mob, remover = False) for mob in [axes, arrow_1]])
        self.play(*[FadeIn(mob.restore()) for mob in [axes, arrow_1]])
        self.remove(copy_axes, copy_arrow_1).wait()

        self.play(*[FadeOut(mob) for mob in [length_1, length_2, length_3, norm, label_2, label_3, arrow_2, arrow_3, text_mul, triangle_1, trialgle_2, indicate, branch]])
        self.wait()

        text_mul = MTex(r"&(3+4i)(\frac{1}{2}+\frac{\sqrt3}{2}i)\\=&\frac{3}{2}+\frac{3\sqrt3}{2}i+2i-2\sqrt3\\=&\ \frac{3-4\sqrt3}{2}+\frac{3\sqrt3+4}{2}i", 
                        tex_to_color_map = {(r"3", r"4"): GREEN, (r"\frac{1}{2}", r"\frac{\sqrt3}{2}"): BLUE, (r"\frac{3}{2}", r"\frac{3\sqrt3}{2}", r"2i", r"2\sqrt3", r"\frac{3-4\sqrt3}{2}", r"\frac{3\sqrt3+4}{2}"): TEAL, r"i": YELLOW}).set_stroke(**stroke_dic).scale(0.8).shift(0.8*DOWN + offset_r)
        part_1, part_2, part_3 = text_mul[:11], text_mul[11:22], text_mul[22:]
        label_2 = MTex(r"\frac{1}{2}+\frac{\sqrt3}{2}i", tex_to_color_map = {r"\frac{1}{2}": BLUE, r"\frac{\sqrt3}{2}": BLUE, r"i": YELLOW}).set_stroke(**stroke_dic).scale(0.8).next_to(coor(np.cos(PI/3), np.sin(PI/3)), RIGHT, buff = 0.1)
        arrow_2 = Arrow(coor(0, 0), coor(np.cos(PI/3), np.sin(PI/3)), buff = 0, color = BLUE)
        label_3 = MTex(r"\frac{3-4\sqrt3}{2}+\frac{3\sqrt3+4}{2}i", tex_to_color_map = {r"\frac{3-4\sqrt3}{2}": TEAL, r"\frac{3\sqrt3+4}{2}": TEAL, r"i": YELLOW}).set_stroke(**stroke_dic).scale(0.8).next_to(coor((3-4*np.sqrt(3))/2, (3*np.sqrt(3)+4)/2), UP, buff = 0.1)
        arrow_3 = arrow_1.copy().rotate(PI/3, about_point = coor(0, 0)).set_color(TEAL)

        arrow_rotate = Arrow(arrow_1.get_center(), arrow_3.get_center(), path_arc = PI/3)
        label_rotate = MTex(r"60^\circ").set_stroke(**stroke_dic).scale(0.8).shift(3*buff_h*unit(np.arctan(4/3)+PI/6) + offset_l)
        self.play(ShowCreation(arrow_rotate), TransformFromCopy(arrow_1, arrow_3, path_arc = -PI/3), Write(label_rotate))
        self.play(GrowArrow(arrow_2), Write(label_2), Write(text_mul[:16]))
        self.play(Write(text_mul[16:]))
        self.play(Write(label_3), run_time = 1)
        self.wait()

        def new_coor(x, y):
            return 3*buff_h*x*RIGHT + 3*buff_h*y*UP + offset_l + UP
        self.add_lower(arrow_1, arrow_2, arrow_3, label, label_2, label_3, arrow_rotate, label_rotate).play(
            *[OverFadeOut(mob, scale = 3, about_point = coor(0, 0) + 0.5*DOWN, run_time = 2) for mob in [arrow_1, arrow_2, arrow_3, label, label_2, label_3, arrow_rotate, label_rotate]], 
            *[mob.animating(run_time = 2).scale(3, about_point = coor(0, 0) + 0.5*DOWN) for mob in [axes, grid]], coors.animating(run_time = 2).scale(3, about_point = coor(0, 0) + 0.5*DOWN).set_fill(color = YELLOW_E), 
            *[FadeOut(mob) for mob in [text_mul]], *[mob.animate.set_x(offset_r[0]) for mob in [imaginary, surr_complex, surr_complex_2, text_complex]], follow(example, imaginary, OverFadeOut))
        arrow_1, arrow_2 = Arrow(new_coor(0, 0), new_coor(1, 0), buff = 0, color = GREEN, stroke_width = 15), Arrow(new_coor(0, 0), new_coor(0, 1), buff = 0, color = BLUE, stroke_width = 15)
        label_1, label_2 = MTex(r"1", color = GREEN).scale(1.5).next_to(new_coor(1, 0), RIGHT).set_stroke(**stroke_dic), MTex(r"i", color = BLUE).scale(1.5).next_to(new_coor(0, 1), UP).set_stroke(**stroke_dic)
        self.play(GrowArrow(arrow_2), GrowArrow(arrow_1), Write(label_1), Write(label_2))
        self.wait()
        
        results = [MTex(r"i^1=i", tex_to_color_map = {r"i": YELLOW}), MTex(r"i^2=-1", tex_to_color_map = {r"i": YELLOW, r"-1": GREEN}), MTex(r"i^3=-i", tex_to_color_map = {r"i": YELLOW}), MTex(r"i^4=1", tex_to_color_map = {r"i": YELLOW, r"1": GREEN})]
        for i, result in enumerate(results):
            result.shift(offset_r + (0.5-0.8*i)*UP - result[2].get_center()).set_stroke(**stroke_dic)

        copy_arrow = arrow_1.copy().set_color(GREEN_E)
        mul_1 = Arrow(new_coor(1.25, 0), new_coor(0, 1.25), path_arc = PI/2, buff = 0.5, stroke_width = 10)
        shadow_1 = mul_1.copy().set_color(BLACK).set_stroke(width = [width + 8 for width in mul_1.get_stroke_widths()])
        cal_1 = MTex(r"\times i", color = YELLOW).set_stroke(**stroke_dic).shift(new_coor(0, 0) + 1.6*3*buff_h*unit(PI/4))
        self.add(copy_arrow, arrow_2, arrow_1).play(Rotate(arrow_1, PI/2, about_point = new_coor(0, 0)), ShowCreation(shadow_1), ShowCreation(mul_1), Write(cal_1), Write(results[0]))
        self.wait()

        arrow_3, arrow_4 = Arrow(new_coor(0, 0), new_coor(-1, 0), buff = 0, color = PURPLE_B, stroke_width = 15), Arrow(new_coor(0, 0), new_coor(0, -1), buff = 0, color = ORANGE, stroke_width = 15)
        label_3, label_4 = MTex(r"-1", color = PURPLE_B).scale(1.5).next_to(new_coor(-1, 0), LEFT).set_stroke(**stroke_dic), MTex(r"-i", color = ORANGE).scale(1.5).next_to(new_coor(0, -1), DOWN).set_stroke(**stroke_dic)
        mul_2 = Arrow(new_coor(0, 1.25), new_coor(-1.25, 0), path_arc = PI/2, buff = 0.5, stroke_width = 10)
        shadow_2 = mul_2.copy().set_color(BLACK).set_stroke(width = [width + 8 for width in mul_2.get_stroke_widths()])
        cal_2 = MTex(r"\times i", color = YELLOW).set_stroke(**stroke_dic).shift(new_coor(0, 0) + 1.6*3*buff_h*unit(3*PI/4))
        self.play(Rotate(arrow_1, PI/2, about_point = new_coor(0, 0)), ShowCreation(shadow_2), ShowCreation(mul_2), Write(cal_2), Write(results[1]), Write(label_3))
        self.add(arrow_3, arrow_1).wait()
        mul_3 = Arrow(new_coor(-1.25, 0), new_coor(0, -1.25), path_arc = PI/2, buff = 0.5, stroke_width = 10)
        shadow_3 = mul_3.copy().set_color(BLACK).set_stroke(width = [width + 8 for width in mul_3.get_stroke_widths()])
        cal_3 = MTex(r"\times i", color = YELLOW).set_stroke(**stroke_dic).shift(new_coor(0, 0) + 1.6*3*buff_h*unit(5*PI/4))
        self.play(Rotate(arrow_1, PI/2, about_point = new_coor(0, 0)), ShowCreation(shadow_3), ShowCreation(mul_3), Write(cal_3), Write(results[2]), Write(label_4))
        self.add(arrow_4, arrow_1).wait()
        mul_4 = Arrow(new_coor(0, -1.25), new_coor(1.25, 0), path_arc = PI/2, buff = 0.5, stroke_width = 10)
        shadow_4 = mul_4.copy().set_color(BLACK).set_stroke(width = [width + 8 for width in mul_4.get_stroke_widths()])
        cal_4 = MTex(r"\times i", color = YELLOW).set_stroke(**stroke_dic).shift(new_coor(0, 0) + 1.6*3*buff_h*unit(7*PI/4))
        self.play(Rotate(arrow_1, PI/2, about_point = new_coor(0, 0)), ShowCreation(shadow_4), ShowCreation(mul_4), Write(cal_4), Write(results[3]))
        self.remove(copy_arrow).wait()

        self.play(*[OverFadeOut(mob, scale = 1/4, about_point = coor(0, 0) + 0.5*DOWN, run_time = 2) for mob in [arrow_1, arrow_2, arrow_3, arrow_4, label_1, label_2, label_3, label_4, mul_1, mul_2, mul_3, mul_4, shadow_1, shadow_2, shadow_3, shadow_4, cal_1, cal_2, cal_3, cal_4]], 
                  *[mob.animating(run_time = 2).scale(1/4, about_point = coor(0, 0) + 0.5*DOWN) for mob in [axes, coors]], grid.animating(run_time = 2).scale(1/4, about_point = coor(0, 0) + 0.5*DOWN).set_fill(color = YELLOW), *[FadeOut(mob) for mob in results])
        self.wait()

        def coor(x, y):
            return 3/4*buff_h*x*RIGHT + 3/4*buff_h*y*UP + offset_l + 0.125*DOWN
        arrow_1, arrow_2 = Arrow(coor(0, 0), coor(1, 0), buff = 0, color = GREEN), Arrow(coor(0, 0), coor(2, 1), buff = 0, color = BLUE)
        label_2 = MTex(r"2+i", tex_to_color_map = {r"i": YELLOW, r"2": GREEN}).scale(0.8).set_stroke(**stroke_dic).next_to(coor(2, 1), RIGHT)
        triangle_1 = Polygon(coor(0, 0), coor(1, 0), coor(2, 1), stroke_width = 0, fill_opacity = 1, fill_color = interpolate_color(BLACK, BLUE, 0.2))
        results = [MTex(r"(2+i)^1=2+i", tex_to_color_map = {r"i": YELLOW, r"2": GREEN}), MTex(r"({2}+i)^2=3+4i", tex_to_color_map = {r"i": YELLOW, (r"{2}", r"3", r"4"): GREEN}), MTex(r"(2+i)^3=2+11i", tex_to_color_map = {r"i": YELLOW, (r"2", r"11"): GREEN})]
        for i, result in enumerate(results):
            result.shift(offset_r + (0.5-0.8*i)*UP - result[6].get_center()).set_stroke(**stroke_dic)
        self.add_lower(arrow_1, arrow_2).add_background(triangle_1).play(GrowArrow(arrow_1), GrowArrow(arrow_2), GrowFromPoint(triangle_1, coor(0, 0)), Write(label_2), Write(results[0]))
        self.wait(1)

        arrow_3, label_3 = Arrow(coor(0, 0), coor(3, 4), buff = 0, color = PURPLE_B), MTex(r"3+4i", tex_to_color_map = {(r"3", r"4"): GREEN, r"i": YELLOW}).scale(0.8).set_stroke(**stroke_dic).next_to(coor(3, 4), RIGHT)
        triangle_2 = Polygon(coor(0, 0), coor(2, 1), coor(3, 4), stroke_width = 0, fill_opacity = 1, fill_color = interpolate_color(BLACK, PURPLE_B, 0.2))
        self.add_lower(arrow_3).add_background(triangle_2).play(TransformFromCopy(triangle_1, triangle_2), TransformFromCopy(arrow_1, arrow_2.copy(), remover = True), TransformFromCopy(arrow_2, arrow_3), Write(label_3), Write(results[1]))
        self.wait(1)

        arrow_4, label_4 = Arrow(coor(0, 0), coor(2, 11), buff = 0, color = ORANGE), MTex(r"2+11i", tex_to_color_map = {r"i": YELLOW, (r"11", r"2"): GREEN}).scale(0.8).set_stroke(**stroke_dic).next_to(coor(2, 11), LEFT)
        triangle_3 = Polygon(coor(0, 0), coor(3, 4), coor(2, 11), stroke_width = 0, fill_opacity = 1, fill_color = interpolate_color(BLACK, ORANGE, 0.2))
        copy_2 = triangle_2.copy()
        self.add_lower(arrow_4).add_background(copy_2, triangle_3).play(TransformFromCopy(triangle_2, triangle_3), TransformFromCopy(arrow_3, arrow_4), Write(label_4), Write(results[2]), 
                                                                         TransformFromCopy(arrow_1, arrow_2.copy(), remover = True), TransformFromCopy(arrow_2, arrow_3.copy(), remover = True), TransformFromCopy(triangle_1, copy_2, remover = True))
        self.wait(1)

        sqrt = MTex(r"&\sqrt[3]{2+11i}+\sqrt[3]{2-11i}\\=&(2+i)+(2-i)=4", tex_to_color_map = {(r"2", r"11", r"4"): GREEN, r"i": YELLOW}).scale(0.8).shift(offset_r + 2.2*DOWN + 0.2*LEFT)
        self.play(Write(sqrt))
        self.wait()

        new_title = Title("代数基本定理")
        self.add_lower(label_2, label_3, label_4).add_top(new_title).play(
            *[OverFadeOut(mob, scale = 4, about_point = coor(0, 0) + 0.125*UP + 0.5*DOWN, run_time = 2) for mob in [arrow_1, arrow_2, arrow_3, arrow_4, label_2, label_3, label_4, triangle_1, triangle_2, triangle_3, coors]], 
            *[mob.animating(run_time = 2).scale(4, about_point = coor(0, 0) + 0.125*UP + 0.5*DOWN) for mob in [axes, grid]], 
            *[OverFadeOut(mob, run_time = 2) for mob in results + [title, sqrt, imaginary, surr_complex, surr_complex_2, text_complex]], OverFadeIn(new_title))
        self.wait()

        function_1 = MTex(r"x^2+x+1=0", tex_to_color_map = {r"x": BLUE}).scale(1.5).shift(offset_r + 2*UP)
        positions = [new_coor(np.cos(TAU/3), np.sin(TAU/3)), new_coor(np.cos(-TAU/3), np.sin(-TAU/3))]
        colors = [BLUE, PURPLE_B]
        roots = [Dot(positions[i], color = colors[i]) for i in range(2)]
        labels = [MTex(r"x_"+str(i+1), color = colors[i]).scale(0.8).next_to(roots[i], DOWN, buff = 0.1).set_stroke(**stroke_dic) for i in range(2)]
        self.play(Write(function_1), *[ShowCreation(mob) for mob in roots], *[Write(mob) for mob in labels])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [function_1, *roots, *labels]])
        self.wait()

        function_2 = MTex(r"x^4+x+1=0", tex_to_color_map = {r"x": BLUE}).scale(1.5).shift(offset_r + 2*UP)
        roots = coefficients_to_roots([1, 0, 0, 1, 1])
        positions = [new_coor(root.real, root.imag) for root in roots]
        colors = color_gradient([BLUE, PURPLE_B], 4)
        roots = [Dot(positions[i], color = colors[i]) for i in range(4)]
        labels = [MTex(r"x_"+str(i+1), color = colors[i]).scale(0.8).next_to(roots[i], DOWN, buff = 0.1).set_stroke(**stroke_dic) for i in range(4)]
        self.play(Write(function_2), *[ShowCreation(mob) for mob in roots], *[Write(mob) for mob in labels])
        self.wait()
        self.play(*[FadeOut(mob) for mob in [function_2, *roots, *labels]])
        self.wait()
        
#################################################################### 

class Video_5(FrameScene):
    def construct(self):
        a, b = 1.5, 3.5
        ah, bh, av, bv = a*RIGHT, b*RIGHT, a*UP, b*UP
        p_00, p_01, p_02, p_10, p_11, p_12, p_20, p_21, p_22 = ORIGIN, ah, ah+bh, av, ah+av, ah+bh+av, av+bv, ah+av+bv, ah+bh+av+bv
        left = VGroup(Polygon(p_00, p_02, p_22, p_20), Polygon(p_01, p_21, p_10, p_12), 
                      Polygon(p_00, p_01, p_11, p_10, **background_dic, fill_color = BLUE), 
                      Polygon(p_00, p_01, p_11, p_10, **background_dic, fill_color = GREEN), 
                      Polygon(p_00, p_01, p_11, p_10, **background_dic, fill_color = BLUE), ).shift(-ah-bh + LEFT)
        p_0a, p_a0, p_2a, p_a2 = p_01, bv, bh+av+bv, p_12
        right = VGroup(Polygon(p_00, p_02, p_22, p_20), Polygon(p_0a, p_a0, p_2a, p_a2))
        pythagoras = VGroup(left, right).scale(0.6).center()
        self.add(pythagoras)



        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        