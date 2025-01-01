from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

def perspective(camera: CameraFrame, return_ratio: bool = False):
    position = camera.get_center()
    distance = camera.get_focal_distance()
    orientation = camera.get_orientation().as_matrix()
    coordinate = [np.dot(orientation.T, base) for base in [RIGHT, UP, OUT]]
    def util_0(point: np.ndarray):
        return np.dot(orientation, point) + position
    def util(point: np.ndarray):
        point -= position
        return np.dot(orientation.T, point)
        # point -= position
        # vector = np.array([np.dot(point, base) for base in coordinate])
        # return (vector - distance*coordinate[2])*(distance)/(-distance + vector[2]) + distance*coordinate[2]
    def util_2(point: np.ndarray):
        raw = np.dot(orientation.T, point - position) - distance*OUT
        if math.isclose(raw[2], 0):
            ratio = 0
            point = np.array([10000*raw[0], 10000*raw[1], 0])
            return 
        else:
            ratio = -distance/raw[2]
            point = raw*ratio + distance*OUT
        if return_ratio:
            # print(raw, ratio, point)
            return point, ratio
        else:
            return point
    return util_2

#################################################################### 

class Test_1(FrameScene):
    def cheese(self, *mobs):
        orientation = self.camera.frame.get_orientation().as_matrix()
        util = lambda t: np.dot(orientation, t)
        for mob in mobs:
            position = mob.get_center()
            # mob.restore().apply_function(util, about_point = position)
            # mob.move_to(position)
            mob.apply_function(util, about_point = position)
        return self

    def construct(self):
        self.notices = [Notice()]
        self.notice = self.notices[0]
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/4 + 2*DEGREES), quad(RIGHT, PI/2))
        camera.set_focal_distance(8).set_orientation(Rotation(quadternion))# .shift(2*OUT)
        
        numbers = 50
        ratio = 2
        lines_h = [Line(i*ratio*UP, np.sqrt(numbers**2-i**2)*ratio*RIGHT + i*ratio*UP) for i in range(0, numbers+1)]
        lines_v = [Line(i*ratio*RIGHT, np.sqrt(numbers**2-i**2)*ratio*UP + i*ratio*RIGHT) for i in range(0, numbers+1)]

        BLUE_G = interpolate_color(GREY, BLUE, 0.25)
        PURPLE_G = interpolate_color(GREY, PURPLE_B, 0.25)
        distance = 3
        lines_h_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_h]
        lines_v_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_v]
        lines_h_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_h]
        lines_v_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_v]
        self.play(*[LaggedStart(*[ShowCreation(mob) for mob in the_list], run_time = 3, rate_func = rush_into, lag_ratio = 1/numbers) for the_list in [lines_h_out, lines_v_out, lines_h_in, lines_v_in]])
        background = VGroup(*lines_h_out, *lines_v_out, *lines_h_in, *lines_v_in)
        self.remove(*lines_h_out, *lines_v_out, *lines_h_in, *lines_v_in).add(background).wait(1)

        def points_out(index: int):
            return [np.array([ratio*i, ratio*(index-i), distance]) for i in range(index+1)]
        def points_in(index: int):
            return [np.array([ratio*i, ratio*(index-i), -distance]) for i in range(index+1)]
        
        groups_lines = []
        for index in range(20):
            points_o = [Dot(point, radius = 0.2) for point in points_out(index)]
            points_i = [Dot(point, radius = 0.2) for point in points_in(index)]
            points = points_o + points_i
            lines = [Line(point_o, point_i, color = YELLOW, stroke_width = 8) for point_o, point_i in zip(points_out(index), points_in(index))]
            self.cheese(*points_o, *points_i).play(*[FadeIn(point) for point in points], rate_func = double_there_and_back, remover = True, run_time = 2)
            colors = color_gradient([WHITE, BLUE], index)
            anims = []
            for i in range(index):
                for line in groups_lines[i]:
                    anims.append(line.animate.set_color(colors[i]).set_stroke(width = 6))
            self.bring_to_back(background, *lines).play(*[ShowCreation(line) for line in lines], *anims)#.add(*points_o, *points_i, *lines_0)
            groups_lines.append(lines)
            self.wait(1)

class Test_2(FrameScene):
    def cheese(self, *mobs):
        orientation = self.camera.frame.get_orientation().as_matrix()
        util = lambda t: np.dot(orientation, t)
        for mob in mobs:
            position = mob.get_center()
            # mob.restore().apply_function(util, about_point = position)
            # mob.move_to(position)
            mob.apply_function(util, about_point = position)
        return self

    def construct(self):
        self.notices = [Notice()]
        self.notice = self.notices[0]
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/4), quad(RIGHT, PI/2))
        camera.set_focal_distance(8).set_orientation(Rotation(quadternion))# .shift(2*OUT)
        
        numbers = 50
        ratio = 2
        lines_h = [Line(i*ratio*UP, np.sqrt(numbers**2-i**2)*ratio*RIGHT + i*ratio*UP) for i in range(0, numbers+1)]
        lines_v = [Line(i*ratio*RIGHT, np.sqrt(numbers**2-i**2)*ratio*UP + i*ratio*RIGHT) for i in range(0, numbers+1)]

        BLUE_G = interpolate_color(GREY, BLUE, 0.25)
        PURPLE_G = interpolate_color(GREY, PURPLE_B, 0.25)
        distance = 3
        lines_h_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_h]
        lines_v_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_v]
        lines_h_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_h]
        lines_v_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_v]
        self.play(*[LaggedStart(*[ShowCreation(mob) for mob in the_list], run_time = 3, rate_func = rush_into, lag_ratio = 1/numbers) for the_list in [lines_h_out, lines_v_out, lines_h_in, lines_v_in]])
        background = VGroup(*lines_h_out, *lines_v_out, *lines_h_in, *lines_v_in)
        self.wait(1)
        self.play(camera.animate.shift(6*unit(PI/4)).set_focal_distance(6), *[mob.animate.shift(IN) for mob in lines_h_out + lines_v_out], *[mob.animate.shift(OUT) for mob in lines_h_in + lines_v_in], run_time = 3)
        self.remove(*lines_h_out, *lines_v_out, *lines_h_in, *lines_v_in).add(background).wait(1)

        distance = 2
        def points_out(index: int):
            return [np.array([ratio*i, ratio*(index-i), distance]) for i in range(index+1)]
        def points_in(index: int):
            return [np.array([ratio*i, ratio*(index-i), -distance]) for i in range(index+1)]
        
        groups_lines = []
        for index in range(1, 20):
            points_o = [Dot(point, radius = 0.2) for point in points_out(index)]
            points_i = [Dot(point, radius = 0.2) for point in points_in(index)]
            points = points_o + points_i
            lines = [Line(point_o, point_i, color = YELLOW, stroke_width = 8) for point_o, point_i in zip(points_out(index), points_in(index))]
            self.cheese(*points_o, *points_i).play(*[FadeIn(point) for point in points], rate_func = double_there_and_back, remover = True, run_time = 2)
            colors = color_gradient([WHITE, BLUE], index)
            anims = []
            for i in range(index-1):
                for line in groups_lines[i]:
                    anims.append(line.animate.set_color(colors[i]).set_stroke(width = 6))
            self.bring_to_back(background, *lines).play(*[ShowCreation(line) for line in lines], *anims)#.add(*points_o, *points_i, *lines_0)
            groups_lines.append(lines)
            self.wait(1)

class Test_3(FrameScene):
    def cheese(self, *mobs):
        orientation = self.camera.frame.get_orientation().as_matrix()
        util = lambda t: np.dot(orientation, t)
        for mob in mobs:
            position = mob.get_center()
            # mob.restore().apply_function(util, about_point = position)
            # mob.move_to(position)
            mob.apply_function(util, about_point = position)
        return self

    def construct(self):
        self.notices = [Notice()]
        self.notice = self.notices[0]
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/4))
        camera.set_focal_distance(8).set_orientation(Rotation(quadternion))# .shift(2*OUT)
        
        numbers = 100
        ratio = 2
        lines_h = [Line(i*ratio*UP, np.sqrt(numbers**2-i**2)*ratio*RIGHT + i*ratio*UP) for i in range(0, numbers+1)]
        lines_v = [Line(i*ratio*RIGHT, np.sqrt(numbers**2-i**2)*ratio*UP + i*ratio*RIGHT) for i in range(0, numbers+1)]

        self.play(*[LaggedStart(*[ShowCreation(mob) for mob in the_list], run_time = 3, rate_func = rush_into, lag_ratio = 1/numbers) for the_list in [lines_h, lines_v]])
        base_line = Line(ratio*0.5*UR + 7.5*unit(PI*3/4), ratio*0.5*UR + 7.5*unit(-PI/4), color = YELLOW)
        interval = Polyline(ratio*LEFT + ratio*0.2*UR, ratio*LEFT, ratio*DOWN, ratio*DOWN + ratio*0.2*UR)
        base_left = Line(7*LEFT, 7*RIGHT, color = GREY)
        base_right = Line(7*UP, 7*DOWN, color = GREY)
        self.add(base_left, base_right, base_line, *lines_h, *lines_v).play(ShowCreation(base_line), FadeIn(interval, ratio*DL), FadeIn(base_left), FadeIn(base_right))
        base = VGroup(base_left, base_right, base_line)
        background = VGroup(*lines_h, *lines_v).save_state()
        self.remove(*lines_h, *lines_v, base_left, base_right, base_line).add(base, background, interval)

        def points_up(index: int):
            if index == 0:
                return [ORIGIN]
            else:
                return [interpolate(ratio*UP, ratio*RIGHT, i/index) for i in range(index+1)]
        def points_down(index: int):
            if index == 0:
                return [ORIGIN]
            else:
                return [interpolate(ratio*DOWN, ratio*LEFT, i/index) for i in range(index+1)]
        fore = lambda t: t*(3-t**2)/2
        back = lambda t: t**2*(3-t)/2
        alpha = ValueTracker(0.0)
        def ray_updater(mob: Arrow):
            ratio = alpha.get_value()
            mob.restore()
            start, end = mob.get_start(), mob.get_end()
            mob.put_start_and_end_on(interpolate(start, end, back(ratio)), interpolate(start, end, fore(ratio)))
        
        groups_lines = []
        for index in range(20):
            points_o = [Dot(point, radius = min(0.08, 0.6/max(index, 1))) for point in points_up(index)]
            points_i = [Dot(point, radius = min(0.08, 0.6/max(index, 1))) for point in points_down(index)]
            points = points_o + points_i
            self.play(*[FadeIn(point) for point in points], rate_func = double_there_and_back, remover = True, run_time = 2)
            if index >= 1:
                rays = [Line(point_o, point_i, color = YELLOW, stroke_width = 3).save_state().add_updater(ray_updater) for point_o, point_i in zip(points_up(index), points_down(index))]
                lines = [Line(point + 0.8/index*UR, point + 0.8/index*DL, color = YELLOW, stroke_width = 4) for point in points_down(index)]
                colors = color_gradient([WHITE, BLUE], index-1)
                anims = []
                for i in range(index-1):
                    for line in groups_lines[i]:
                        anims.append(line.animate.set_color(colors[i]).set_stroke(width = 2))
                self.add(*rays).bring_to_back(base, background, *lines).play(alpha.animating(run_time = 2).set_value(1), *[GrowFromCenter(line, rate_func = squish_rate_func(smooth, 0.5, 1), run_time = 2) for line in lines], *anims, background.animating(rate_func = squish_rate_func(smooth, 0.5, 1), run_time = 2).restore().scale(1/(index+1), about_point = ORIGIN).set_stroke(width = min(4, 20/index)))#.add(*points_o, *points_i, *lines_0)
                groups_lines.append(lines)
                alpha.set_value(0)
                self.remove(*rays)
            else:
                self.wait(2)
        # distance = 0
        # def points_out(index: int):
        #     return [np.array([ratio*i, ratio*(index-i), distance]) for i in range(index+1)]
        # def points_in(index: int):
        #     return [np.array([ratio*i, ratio*(index-i), -distance]) for i in range(index+1)]
        
        # groups_lines = []
        # for index in range(1, 20):
        #     points_o = [Dot(point, radius = 0.2) for point in points_out(index)]
        #     points_i = [Dot(point, radius = 0.2) for point in points_in(index)]
        #     points = points_o + points_i
        #     lines = [Line(point_o, point_i, color = YELLOW, stroke_width = 8) for point_o, point_i in zip(points_out(index), points_in(index))]
        #     self.cheese(*points_o, *points_i).play(*[FadeIn(point) for point in points], rate_func = double_there_and_back, remover = True, run_time = 2)
        #     colors = color_gradient([WHITE, BLUE], index-1)
        #     anims = []
        #     for i in range(index-1):
        #         for line in groups_lines[i]:
        #             anims.append(line.animate.set_color(colors[i]).set_stroke(width = 6))
        #     self.bring_to_back(background, *lines).play(*[ShowCreation(line) for line in lines], *anims)#.add(*points_o, *points_i, *lines_0)
        #     groups_lines.append(lines)
        #     self.wait(1)

class Video_0(FrameScene):
    def construct(self):
        interval = Line(4*LEFT, 4*RIGHT)
        self.play(GrowFromCenter(interval))
        self.wait(1)

        ratio = lambda t: interpolate(4*LEFT, 4*RIGHT, t)
        group = VGroup(VGroup())
        def lines_updater(mob: VGroup):
            mark = self.time - 2
            i = 1
            mob.remove(mob.submobjects[-1])
            old_i = len(mob.submobjects)
            while mark >= 1/i:
                if i >= old_i - 1:
                    new_group = VGroup(*[Line(1.5/i*UP, 1.5/i*DOWN, stroke_width = min(4, 20/i), color = BLUE).shift(ratio(j/i)) for j in range(i+1)])
                    mob.add(new_group)
                mark -= 1/i
                i += 1
            new_group = VGroup(*[Line(1.5/i*UP, 1.5/i*DOWN, stroke_width = min(4, 20/i), color = BLUE).scale(smooth(mark*i)).shift(ratio(j/i)) for j in range(i+1)])
            mob.add(new_group)
        group.add_updater(lines_updater)
        self.add(group).wait(6)
        group.clear_updaters().insert_submobject(0, interval)
        self.remove(interval).wait(1)

        def tuple_mark(i: int, j: int):
            line = group[i+2][j].copy().set_stroke(color = YELLOW, width = 4)
            mark = MTex(r"\frac{"+str(j)+r"}{"+str(i)+r"}").set_stroke(width = 8, color = BACK, background = True).move_to(line).shift(1.5*DOWN)
            height = MTex(r"\frac{1}{"+str(i)+r"}", color = YELLOW).scale(0.75).set_stroke(width = 8, color = BACK, background = True).next_to(line)
            return (line, mark, height)
        tuples = VGroup(*tuple_mark(3, 1), *tuple_mark(4, 3), *tuple_mark(7, 4))
        self.play(FadeIn(tuples))
        self.wait(1)
        self.play(FadeOut(tuples))
        self.wait(1)

        pic_1 = ImageMobject("trees.jpg", height = 4).shift(0.5*DOWN)
        pic_2 = ImageMobject("trunks.png", height = 4).shift(0.5*DOWN)
        self.play(group.animate.scale(np.array([1, 2/3, 1]), about_point = 9*UP), OverFadeIn(pic_1, 3*UP), run_time = 2)
        self.wait(1)
        self.add(pic_2).play(pic_1.animate.set_opacity(0.25))
        self.wait(1)
        self.add(self.shade, group).play(FadeIn(self.shade), group.animate.scale(np.array([1, 0.5, 1])))
        self.wait(1)

class Video_1(FrameScene):
    def construct(self):
        interval = Line(4*LEFT, 4*RIGHT).shift(3*UP)

        ratio = lambda t: interpolate(4*LEFT, 4*RIGHT, t)
        group = VGroup(interval)
        mark = 6
        i = 1
        while mark >= 1/i:
            new_group = VGroup(*[Line(0.5/i*UP, 0.5/i*DOWN, stroke_width = min(4, 20/i), color = BLUE).shift(ratio(j/i) + 3*UP) for j in range(i+1)])
            group.add(new_group)
            mark -= 1/i
            i += 1
        self.add(group).wait(1)
        self.play(FadeOut(group))
        self.wait(1)
        self.play(FadeIn(group))
        self.wait(1)

class Video_2(FrameScene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/4 + 2*DEGREES), quad(RIGHT, PI/2))
        camera.quadternion = quadternion
        camera.set_focal_distance(8).set_orientation(Rotation(quadternion)).save_state()# .shift(2*OUT)
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(mob.quadternion, quad(UP, 0.2*DEGREES*dt))
            mob.set_orientation(Rotation(mob.quadternion))
        camera.add_updater(camera_updater)
        
        numbers = 50
        ratio = 2
        lines_h = [Line(ratio*RIGHT, numbers*ratio*RIGHT)] + [Line(i*ratio*UP, np.sqrt(numbers**2-i**2)*ratio*RIGHT + i*ratio*UP) for i in range(1, numbers+1)]
        lines_v = [Line(ratio*UP, numbers*ratio*UP)] + [Line(i*ratio*RIGHT, np.sqrt(numbers**2-i**2)*ratio*UP + i*ratio*RIGHT) for i in range(1, numbers+1)]

        BLUE_G = interpolate_color(interpolate_color(GREY, BLUE, 0.5), BACK, 0.8)
        PURPLE_G = interpolate_color(interpolate_color(GREY, PURPLE_B, 0.5), BACK, 0.8)
        distance = 1.5
        lines_h_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_h]
        lines_v_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_v]
        lines_h_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_h]
        lines_v_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_v]
        self.add(camera).play(*[LaggedStart(*[ShowCreation(mob) for mob in the_list], run_time = 3, rate_func = rush_into, lag_ratio = 1/numbers) for the_list in [lines_h_in, lines_v_in]])
        background = VGroup(*lines_h_out, *lines_v_out, *lines_h_in, *lines_v_in)
        background_out = VGroup(*lines_h_out, *lines_v_out)
        background_in = VGroup(*lines_h_in, *lines_v_in)
        self.remove(*lines_h_in, *lines_v_in).add(background_in).wait(1)

        def points_out(index: int):
            return [np.array([ratio*i, ratio*(index-i), distance]) for i in range(index+1)]
        def points_in(index: int):
            return [np.array([ratio*i, ratio*(index-i), -distance]) for i in range(index+1)]

        group = VGroup(VGroup())
        def lines_updater(mob: VGroup):
            mark = self.time - 4
            i = 1
            mob.remove(mob.submobjects[-1])
            old_i = len(mob.submobjects)
            while mark >= 1/i:
                if i >= old_i - 1:
                    new_group = VGroup(*[Line(point_o, point_i, color = BLUE, stroke_width = 8) for point_o, point_i in zip(points_out(i), points_in(i))])
                    mob.add(new_group)
                mark -= 1/i
                i += 1
            new_group = VGroup(*[Line(interpolate(point_i, point_o, mark*i), point_i, color = BLUE, stroke_width = 8) for point_o, point_i in zip(points_out(i), points_in(i))])
            mob.add(new_group)
        group.add_updater(lines_updater)
        self.add(group).wait(5)
        group.clear_updaters()
        self.wait(1)

        self.bring_to_back(background_out).play(FadeIn(background_out), run_time = 0.4)
        self.play(background_out.animate.set_opacity(0), run_time = 1.6, rate_func = double_there_and_back)
        self.wait(1)

        quadternion = quaternion_mult(quad(OUT, -PI/4), quad(RIGHT, PI/2))
        camera.clear_updaters()
        self.play(camera.animate.shift(4*unit(PI/4)).set_focal_distance(4).set_orientation(Rotation(quadternion)), *[mob.save_state().animate.scale([1, 1, 1/2], about_point = ORIGIN) for mob in [background_in, background_out, group]], run_time = 3)
        self.wait(1)

        self.play(camera.animate.restore().set_orientation(Rotation(quadternion)), background_in.animate.restore().set_color(interpolate_color(WHITE, PURPLE_B, 0.3)), background_out.animate.restore().set_color(interpolate_color(WHITE, BLUE, 0.3)), OverFadeOut(group, scale = np.array([1, 1, 2]), about_point = ORIGIN), run_time = 3)
        self.wait(1)

class Video_3(FrameScene):
    def perspective(self, point: np.ndarray):
        camera = self.camera.frame
        position = camera.get_center()
        distance = camera.get_focal_distance()
        orientation = camera.get_orientation().as_matrix()

        raw = np.dot(orientation.T, point - position) - distance*OUT
        if math.isclose(raw[2], 0):
            ratio = 0
            point = np.array([10000*raw[0], 10000*raw[1], 0])
            return 
        else:
            ratio = -distance/raw[2]
            point = raw*ratio + distance*OUT
        return point
    
    def construct(self):
        self.notices = [Notice()]
        self.notice = self.notices[0]
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/4), quad(RIGHT, PI/2))
        camera.set_focal_distance(8).set_orientation(Rotation(quadternion))# .shift(2*OUT)
        
        numbers = 50
        ratio = 2
        lines_h = [Polyline(ratio*UR, ratio*RIGHT, numbers*ratio*RIGHT)] + [Line(i*ratio*UP, np.sqrt(numbers**2-i**2)*ratio*RIGHT + i*ratio*UP) for i in range(1, numbers+1)]
        lines_v = [Polyline(ratio*UR, ratio*UP, numbers*ratio*UP)] + [Line(i*ratio*RIGHT, np.sqrt(numbers**2-i**2)*ratio*UP + i*ratio*RIGHT) for i in range(1, numbers+1)]

        BLUE_G = interpolate_color(WHITE, BLUE, 0.3)
        PURPLE_G = interpolate_color(WHITE, PURPLE_B, 0.3)
        distance = 1.5
        lines_h_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_h]
        lines_v_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_v]
        lines_h_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_h]
        lines_v_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_v]
        background_out = VGroup(*lines_h_out, *lines_v_out)
        background_in = VGroup(*lines_h_in, *lines_v_in)
        self.add(background_out, background_in).wait(1)

        line_1 = Line(color = YELLOW).fix_in_frame()
        line_2 = Line(color = YELLOW).fix_in_frame()
        def pers(line: Line, proj: Line):
            start, end = line.get_start(), line.get_end()
            proj.put_start_and_end_on(self.perspective(start), self.perspective(end))
        pers(lines_h_out[2], line_1)
        pers(lines_v_in[3], line_2)
        def line_updater(line: Line):
            return lambda t: pers(line, t)
        alpha = ValueTracker(1.0)
        def fade_updater(mob: Line):
            opacity = alpha.get_value()
            mob.set_opacity(opacity)
        self.play(ShowCreation(line_1), ShowCreation(line_2))
        self.wait(1)
        line_1.add_updater(line_updater(lines_h_out[2])).add_updater(fade_updater)
        line_2.add_updater(line_updater(lines_v_in[3])).add_updater(fade_updater)

        self.play(camera.animate.shift(2*RIGHT).increment_theta(PI/6), background_out.animate.shift(0.5*OUT), background_in.animate.shift(0.5*IN), run_time = 2)
        self.wait(1)
        self.play(camera.animate.set_focal_distance(6).shift(2*LEFT).set_orientation(Rotation(quadternion)), alpha.animate.set_value(0.0), run_time = 2)
        self.remove(line_1, line_2).wait(1)

        lines = []
        for i in range(8):
            line_out = Line(self.perspective(lines_h_out[i*(i+1)//2].get_start()), 6*RIGHT, color = YELLOW).fix_in_frame()
            line_in = Line(self.perspective(lines_h_in[i*(i+1)//2].get_start()), 6*RIGHT, color = YELLOW).fix_in_frame()
            lines.append(line_out)
            lines.append(line_in)
        lines = VGroup(*lines)
        self.play(ShowCreation(lines, lag_ratio = 0.3), run_time = 2)
        self.wait(1)
        dot = Dot(6*RIGHT, color = ORANGE).fix_in_frame()
        anim = Flash(dot, flash_radius = 0.4, color = ORANGE)
        anim.lines.fix_in_frame()
        self.play(ShowCreation(dot), anim)
        self.wait(1)

        for line in lines:
            line.reverse_points()
        lines_y = []
        for i in range(8):
            line_out = Line(self.perspective(lines_v_out[i*(i+1)//2].get_start()), 6*LEFT, color = YELLOW).fix_in_frame()
            line_in = Line(self.perspective(lines_v_in[i*(i+1)//2].get_start()), 6*LEFT, color = YELLOW).fix_in_frame()
            lines_y.append(line_out)
            lines_y.append(line_in)
        lines_y = VGroup(*lines_y)
        self.play(Uncreate(lines, lag_ratio = 0.3, run_time = 2, rate_func = lambda t: rush_from(1-t)), dot.animating(remover = True, run_time = 2, rate_func = rush_into).scale(0), ShowCreation(lines_y, lag_ratio = 0.3, run_time = 3, rate_func = squish_rate_func(rush_from, 1/3, 1)))
        self.wait(1)
        dot = Dot(6*LEFT, color = ORANGE).fix_in_frame()
        anim = Flash(dot, flash_radius = 0.4, color = ORANGE)
        anim.lines.fix_in_frame()
        self.play(ShowCreation(dot), anim)
        self.wait(1)

        for line in lines_y:
            line.reverse_points()
        lines_d = []
        for i in range(9):
            line_out = Line(self.perspective(lines_v_out[i*(i+1)//2].get_start()), self.perspective(lines_h_out[i*(i+1)//2].get_start()), color = YELLOW).fix_in_frame()
            line_in = Line(self.perspective(lines_v_in[i*(i+1)//2].get_start()), self.perspective(lines_h_in[i*(i+1)//2].get_start()), color = YELLOW).fix_in_frame()
            lines_d.append(line_out)
            lines_d.append(line_in)
        lines_d = VGroup(*lines_d)
        self.play(Uncreate(lines_y, lag_ratio = 0.3, run_time = 2, rate_func = lambda t: rush_from(1-t)), dot.animating(remover = True, run_time = 2, rate_func = rush_into).scale(0), ShowCreation(lines_d, lag_ratio = 0.3, run_time = 3, rate_func = squish_rate_func(rush_from, 1/3, 1)))
        self.wait(1)

        self.play(FadeOut(lines_d))
        self.wait(1)
        self.play(background_out.animate.shift(1.25*IN), background_in.animate.shift(1.25*OUT), camera.animate.shift(4*unit(PI/4)).set_focal_distance(4).set_orientation(Rotation(quadternion)), run_time = 3)
        self.wait(1)

        distance = 0.75
        def points_out(index: int):
            return [np.array([ratio*i, ratio*(index-i), distance]) for i in range(index+1)]
        def points_in(index: int):
            return [np.array([ratio*i, ratio*(index-i), -distance]) for i in range(index+1)]
        trees_0 = [Line(point_i, point_o, color = YELLOW, stroke_width = 6) for point_o, point_i in zip(points_out(1), points_in(1))]
        mark_0 = MTex(r"(0, 1)", color = YELLOW).fix_in_frame().next_to(self.perspective(trees_0[1].get_start()), UR)
        mark_1 = MTex(r"(1, 0)", color = YELLOW).fix_in_frame().next_to(self.perspective(trees_0[0].get_start()), UL)
        self.play(ShowCreation(trees_0[0]), ShowCreation(trees_0[1]), Write(mark_0), Write(mark_1))
        self.wait(1)
        self.play(*[mob.save_state().animate.fade() for mob in trees_0])
        self.wait(1)
        self.play(*[mob.animate.restore() for mob in trees_0])
        self.wait(1)
        dot_x = Dot(4*RIGHT, color = ORANGE).fix_in_frame()
        dot_y = Dot(4*LEFT, color = ORANGE).fix_in_frame()
        self.play(ShowCreation(dot_x), ShowCreation(dot_y))
        infs = [dot_x, dot_y]
        self.wait(1)

        BLUE_G = interpolate_color(interpolate_color(GREY, BLUE, 0.5), BACK, 0.8)
        PURPLE_G = interpolate_color(interpolate_color(GREY, PURPLE_B, 0.5), BACK, 0.8)
        trees_1 = [Line(point_i, point_o, color = YELLOW, stroke_width = 6) for point_o, point_i in zip(points_out(2), points_in(2))]
        mark_2 = MTex(r"(1, 1)", color = YELLOW).fix_in_frame().next_to(self.perspective(trees_1[1].get_start()), DOWN)
        self.play(Write(mark_2), *[mob.animate.set_color(BLUE) for mob in trees_0], background_out.animate.set_color(BLUE_G), background_in.animate.set_color(PURPLE_G), )
        self.wait(1)

        def coor_lines(x: int, y: int):
            x_out = Line(self.perspective(lines_v_out[x].get_start()), 4*LEFT, color = WHITE).fix_in_frame()
            x_in = Line(self.perspective(lines_v_in[x].get_start()), 4*LEFT, color = WHITE).fix_in_frame()
            y_out = Line(self.perspective(lines_h_out[y].get_start()), 4*RIGHT, color = WHITE).fix_in_frame()
            y_in = Line(self.perspective(lines_h_in[y].get_start()), 4*RIGHT, color = WHITE).fix_in_frame()
            return [x_out, x_in, y_out, y_in]
        lines_1 = coor_lines(1, 1)
        self.add(*lines_1[:2], *trees_0, *infs).play(ShowCreation(lines_1[0]), ShowCreation(lines_1[1]))
        self.wait(1)
        self.add(*lines_1, *trees_0, *infs).play(ShowCreation(lines_1[2]), ShowCreation(lines_1[3]))
        self.wait(1)

        self.play(*[FadeOut(mob) for mob in [mark_0, mark_1]], ShowCreation(trees_1[1]))
        self.wait(1)

        dot_1 = Dot(color = ORANGE).fix_in_frame()
        line_1 = Line(4*LEFT, 4*RIGHT).fix_in_frame()
        self.add(line_1, dot_1, *infs).play(FadeOut(mark_2), FadeIn(line_1), FadeIn(dot_1))
        label_a = MTex("A").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[0].get_end()), LEFT).fix_in_frame()
        label_b = MTex("B", color = GREY).set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[0].get_start()), LEFT).fix_in_frame()
        label_m = MTex("M").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[0].get_center()), LEFT).fix_in_frame()
        label_c = MTex("C").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[1].get_end()), RIGHT).fix_in_frame()
        label_d = MTex("D", color = GREY).set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[1].get_start()), RIGHT).fix_in_frame()
        label_n = MTex("N").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[1].get_center()), RIGHT).fix_in_frame()
        label_e = MTex("E").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_1[1].get_end()), UP).fix_in_frame()
        label_f = MTex("F", color = GREY).set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_1[1].get_start()), DOWN).fix_in_frame()
        label_o = MTex("O").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_1[1].get_center()), UR).fix_in_frame()
        labels = VGroup(label_a, label_b, label_m, label_c, label_d, label_n, label_e, label_f, label_o)
        solution = MTex(r"\triangle AEM\sim\triangle NEC \Rightarrow &\ \frac{ME}{CE}=\frac{AM}{CN}=1\\\triangle MOE\sim\triangle MCN \Rightarrow&\ \frac{OE}{CN}=\frac{MO}{MN}=\frac{ME}{MC}=\frac{1}{2}\\").fix_in_frame().next_to(4.5*UP, DOWN).scale(0.5)
        self.play(FadeIn(labels), FadeIn(solution))
        self.wait(1)
        self.bring_to_back(background_in, background_out, line_1).play(FadeOut(labels), FadeOut(solution), *[FadeOut(mob) for mob in lines_1], FadeOut(dot_1))
        self.wait(1)

        label_0 = MTex(r"\frac01").scale(0.75).next_to(self.perspective(trees_0[0].get_start()), DOWN).fix_in_frame()
        label_1 = MTex(r"\frac12").scale(0.75).next_to(self.perspective(trees_1[1].get_start()), DOWN).fix_in_frame()
        label_2 = MTex(r"\frac11").scale(0.75).next_to(self.perspective(trees_0[1].get_start()), DOWN).fix_in_frame()
        label_3 = MTex(r"\frac02").scale(0.75).next_to(self.perspective(trees_1[0].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        label_4 = MTex(r"\frac22").scale(0.75).next_to(self.perspective(trees_1[2].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        self.play(FadeIn(label_0), FadeIn(label_1), FadeIn(label_2))
        self.wait(1)
        line_out = Line(trees_1[0].get_end(), trees_1[2].get_end(), color = WHITE)
        line_in = Line(trees_1[0].get_start(), trees_1[2].get_start(), color = WHITE)
        self.bring_to_back(background_in, background_out, line_1, line_out, line_in).play(GrowFromCenter(line_out), GrowFromCenter(line_in))
        self.wait(1)
        self.bring_to_back(background_in, background_out, line_1, line_out, line_in, *trees_1).play(*[mob.save_state().animate.fade() for mob in trees_0], *[FadeOut(mob, rate_func = rush_into, run_time = 0.5) for mob in [label_0, label_2]], *[FadeIn(mob, rate_func = squish_rate_func(rush_from, 0.5, 1)) for mob in [label_3, label_4]])
        self.wait(1)
        self.play(*[mob.animate.restore() for mob in trees_0], *[FadeOut(mob, rate_func = rush_into, run_time = 0.5) for mob in [label_3, label_4]], *[FadeIn(mob, rate_func = squish_rate_func(rush_from, 0.5, 1)) for mob in [label_0, label_2]], *[FadeOut(mob) for mob in [line_out, line_in]])
        self.wait(1)
        
class Video_4(FrameScene):
    def perspective(self, point: np.ndarray):
        camera = self.camera.frame
        position = camera.get_center()
        distance = camera.get_focal_distance()
        orientation = camera.get_orientation().as_matrix()

        raw = np.dot(orientation.T, point - position) - distance*OUT
        if math.isclose(raw[2], 0):
            ratio = 0
            point = np.array([10000*raw[0], 10000*raw[1], 0])
            return 
        else:
            ratio = -distance/raw[2]
            point = raw*ratio + distance*OUT
        return point
    
    def cheese(self, *mobs):
        orientation = self.camera.frame.get_orientation().as_matrix()
        util = lambda t: np.dot(orientation, t)
        for mob in mobs:
            position = mob.get_center()
            # mob.restore().apply_function(util, about_point = position)
            # mob.move_to(position)
            mob.apply_function(util, about_point = position)
        return self
    
    def construct(self):
        self.notices = [Notice()]
        self.notice = self.notices[0]
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, -PI/4), quad(RIGHT, PI/2))
        camera.shift(4*unit(PI/4)).set_focal_distance(4).set_orientation(Rotation(quadternion))

        numbers = 50
        ratio = 2
        lines_h = [Polyline(ratio*UR, ratio*RIGHT, numbers*ratio*RIGHT)] + [Line(i*ratio*UP, np.sqrt(numbers**2-i**2)*ratio*RIGHT + i*ratio*UP) for i in range(1, numbers+1)]
        lines_v = [Polyline(ratio*UR, ratio*UP, numbers*ratio*UP)] + [Line(i*ratio*RIGHT, np.sqrt(numbers**2-i**2)*ratio*UP + i*ratio*RIGHT) for i in range(1, numbers+1)]

        BLUE_G = interpolate_color(interpolate_color(GREY, BLUE, 0.5), BACK, 0.8)
        PURPLE_G = interpolate_color(interpolate_color(GREY, PURPLE_B, 0.5), BACK, 0.8)
        distance = 0.75
        def points_out(index: int):
            return [np.array([ratio*i, ratio*(index-i), distance]) for i in range(index+1)]
        def points_in(index: int):
            return [np.array([ratio*i, ratio*(index-i), -distance]) for i in range(index+1)]
        lines_h_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_h]
        lines_v_out = [line.copy().shift(distance*OUT).set_color(BLUE_G) for line in lines_v]
        lines_h_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_h]
        lines_v_in = [line.copy().shift(distance*IN).set_color(PURPLE_G) for line in lines_v]
        line_inf = Line(4*LEFT, 4*RIGHT).fix_in_frame()
        background = VGroup(*lines_h_out, *lines_v_out, *lines_h_in, *lines_v_in)
        
        trees_0 = [Line(point_i, point_o, color = BLUE, stroke_width = 6) for point_o, point_i in zip(points_out(1), points_in(1))]
        trees_1 = [Line(point_i, point_o, color = YELLOW, stroke_width = 6) for point_o, point_i in zip(points_out(2), points_in(2))]
        dot_x = Dot(4*RIGHT, color = ORANGE).fix_in_frame()
        dot_y = Dot(4*LEFT, color = ORANGE).fix_in_frame()
        infs = [dot_x, dot_y]
        label_0 = MTex(r"\frac01").scale(0.75).next_to(self.perspective(trees_0[0].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        label_1 = MTex(r"\frac12").scale(0.75).next_to(self.perspective(trees_1[1].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        label_2 = MTex(r"\frac11").scale(0.75).next_to(self.perspective(trees_0[1].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        labels = [label_0, label_1, label_2]
        self.add(background, line_inf, *trees_1, *trees_0, *infs, *labels).wait(1)

        groups_lines = [trees_1, trees_0]
        points_o = [Dot(point, color = YELLOW) for point in points_out(3)]
        points_i = [Dot(point, color = YELLOW) for point in points_in(3)]
        points = points_o + points_i
        trees_2 = [Line(point_i, point_o, color = YELLOW, stroke_width = 6) for point_o, point_i in zip(points_out(3), points_in(3))]
        self.cheese(*points_o, *points_i).play(*[FadeIn(point) for point in points], rate_func = double_there_and_back, remover = True, run_time = 2)
        self.wait(1)
        self.bring_to_back(background, line_inf, *trees_2).play(*[ShowCreation(line) for line in trees_2], *[mob.animate.set_color(BLUE) for mob in trees_1])
        groups_lines.insert(0, trees_2)
        self.wait(1)

        def coor_lines(x: int, y: int):
            x_out = Line(self.perspective(lines_v_out[x].get_start()), 4*LEFT, color = WHITE).fix_in_frame()
            x_in = Line(self.perspective(lines_v_in[x].get_start()), 4*LEFT, color = WHITE).fix_in_frame()
            y_out = Line(self.perspective(lines_h_out[y].get_start()), 4*RIGHT, color = WHITE).fix_in_frame()
            y_in = Line(self.perspective(lines_h_in[y].get_start()), 4*RIGHT, color = WHITE).fix_in_frame()
            return [x_out, x_in, y_out, y_in]
        lines_1 = coor_lines(1, 2)
        mark_2 = MTex(r"(1, 2)", color = YELLOW).scale(0.8).fix_in_frame().next_to(self.perspective(trees_2[1].get_start()), DOWN).set_stroke(width = 8, color = BACK, background = True)
        anims = []
        for i in range(1, 4):
            for j in range(i+1):
                if (i, j) not in [(1, 1), (2, 0), (3, 1)]:
                    anims.append(groups_lines[3-i][j].save_state().animate.fade(0.8))
        self.bring_to_back(background, line_inf, *lines_1).play(*[ShowCreation(mob) for mob in lines_1], Write(mark_2), *anims)
        self.wait(1)

        label_a = MTex("A").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_1[0].get_end()), LEFT).fix_in_frame()
        label_b = MTex("B", color = GREY).set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_1[0].get_start()), LEFT).fix_in_frame()
        label_m = MTex("M").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_1[0].get_center()), LEFT).fix_in_frame()
        label_c = MTex("C").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[1].get_end()), RIGHT).fix_in_frame()
        label_d = MTex("D", color = GREY).set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[1].get_start()), RIGHT).fix_in_frame()
        label_n = MTex("N").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_0[1].get_center()), RIGHT).fix_in_frame()
        label_e = MTex("E").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_2[1].get_end()), UP).fix_in_frame()
        label_f = MTex("F", color = GREY).set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_2[1].get_start()), DOWN).fix_in_frame()
        label_o = MTex("O").set_stroke(width = 8, color = BACK, background = True).next_to(self.perspective(trees_2[1].get_center()), RIGHT).fix_in_frame()
        labels = VGroup(label_a, label_b, label_m, label_c, label_d, label_n, label_e, label_f, label_o)
        solution = MTex(r"\triangle AEM\sim\triangle NEC \Rightarrow &\ \frac{ME}{CE}=\frac{AM}{CN}=\frac12\\\triangle MOE\sim\triangle MCN \Rightarrow&\ \frac{OE}{CN}=\frac{MO}{MN}=\frac{ME}{MC}=\frac13\\").fix_in_frame().next_to(4.5*UP, DOWN).scale(0.5)
        self.play(FadeIn(labels), FadeIn(solution), OverFadeOut(mark_2))
        self.wait(1)
        anims = []
        for i in range(1, 4):
            for j in range(i+1):
                if (i, j) not in [(1, 1), (2, 0), (3, 1)]:
                    anims.append(groups_lines[3-i][j].animate.restore())
        label_3 = MTex(r"\frac13").scale(0.6).next_to(self.perspective(trees_2[1].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        self.play(FadeOut(labels), FadeOut(solution), *[FadeOut(mob) for mob in lines_1], *anims, OverFadeIn(label_3))
        self.wait(1)

        def coor_lines(x: int, y: int):
            x_out = Line(self.perspective(lines_v_out[x].get_start()), 4*LEFT, color = WHITE).fix_in_frame()
            x_in = Line(self.perspective(lines_v_in[x].get_start()), 4*LEFT, color = WHITE).fix_in_frame()
            y_out = Line(self.perspective(lines_h_out[y].get_start()), 4*RIGHT, color = WHITE).fix_in_frame()
            y_in = Line(self.perspective(lines_h_in[y].get_start()), 4*RIGHT, color = WHITE).fix_in_frame()
            return [x_out, x_in, y_out, y_in]
        lines_1 = coor_lines(2, 1)
        mark_2 = MTex(r"(2, 1)", color = YELLOW).scale(0.8).fix_in_frame().next_to(self.perspective(trees_2[2].get_start()), DOWN).set_stroke(width = 8, color = BACK, background = True)
        anims = []
        for i in range(1, 4):
            for j in range(i+1):
                if (i, j) not in [(1, 0), (2, 2), (3, 2)]:
                    anims.append(groups_lines[3-i][j].save_state().animate.fade(0.8))
        label_a.next_to(self.perspective(trees_0[0].get_end()), LEFT)
        label_b.next_to(self.perspective(trees_0[0].get_start()), LEFT)
        label_m .next_to(self.perspective(trees_0[0].get_center()), LEFT)
        label_c.next_to(self.perspective(trees_1[2].get_end()), RIGHT)
        label_d.next_to(self.perspective(trees_1[2].get_start()), RIGHT)
        label_n.next_to(self.perspective(trees_1[2].get_center()), RIGHT)
        label_e.next_to(self.perspective(trees_2[2].get_end()), UP)
        label_f.next_to(self.perspective(trees_2[2].get_start()), DOWN)
        label_o.next_to(self.perspective(trees_2[2].get_center()), RIGHT)
        solution = MTex(r"\triangle AEM\sim\triangle NEC \Rightarrow &\ \frac{ME}{CE}=\frac{AM}{CN}=2\\\triangle MOE\sim\triangle MCN \Rightarrow&\ \frac{OE}{CN}=\frac{MO}{MN}=\frac{ME}{MC}=\frac23\\").fix_in_frame().next_to(4.5*UP, DOWN).scale(0.5)
        label_4 = MTex(r"\frac23").scale(0.6).next_to(self.perspective(trees_2[2].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        self.bring_to_back(background, line_inf, *lines_1).play(FadeIn(labels), FadeIn(solution), *[FadeIn(mob) for mob in lines_1], Write(mark_2), *anims, OverFadeOut(mark_2))
        self.wait(1)
        anims = []
        for i in range(1, 4):
            for j in range(i+1):
                if (i, j) not in [(1, 0), (2, 2), (3, 2)]:
                    anims.append(groups_lines[3-i][j].animate.restore())
        self.play(FadeOut(labels), FadeOut(solution), *[FadeOut(mob) for mob in lines_1], *anims, OverFadeIn(label_4))
        self.wait(1)

        points_o = [Dot(point, color = YELLOW) for point in points_out(4)]
        points_i = [Dot(point, color = YELLOW) for point in points_in(4)]
        points = points_o + points_i
        trees_3 = [Line(point_i, point_o, color = YELLOW, stroke_width = 6) for point_o, point_i in zip(points_out(4), points_in(4))]
        self.cheese(*points_o, *points_i).play(*[FadeIn(point) for point in points], rate_func = double_there_and_back, remover = True, run_time = 2)
        self.wait(1)
        self.bring_to_back(background, line_inf, *trees_3).play(*[ShowCreation(line) for line in trees_3], *[mob.animate.set_color(BLUE) for mob in trees_2])
        groups_lines.insert(0, trees_3)
        self.wait(1)

        for i in range(1, 5):
            for j in range(i+1):
                if (i, j) not in [(4, 0)]:
                    groups_lines[4-i][j].set_opacity(0.1)
        self.wait(0, 6)
        for i in range(1, 5):
            for j in range(i+1):
                if (i, j) not in [(1, 1), (3, 0), (4, 1)]:
                    groups_lines[4-i][j].set_opacity(0.1)
                else: 
                    groups_lines[4-i][j].set_opacity(1)
        lines_1 = coor_lines(1, 3)
        self.bring_to_back(background, line_inf, *lines_1).wait(0, 6)
        for i in range(1, 5):
            for j in range(i+1):
                if (i, j) not in [(2, 0), (2, 2), (4, 2)]:
                    groups_lines[4-i][j].set_opacity(0.1)
                else: 
                    groups_lines[4-i][j].set_opacity(1)
        lines_2 = coor_lines(2, 2)
        self.remove(*lines_1).bring_to_back(background, line_inf, *lines_2).wait(0, 6)
        for i in range(1, 5):
            for j in range(i+1):
                if (i, j) not in [(3, 3), (1, 0), (4, 3)]:
                    groups_lines[4-i][j].set_opacity(0.1)
                else: 
                    groups_lines[4-i][j].set_opacity(1)
        lines_3 = coor_lines(3, 1)
        self.remove(*lines_2).bring_to_back(background, line_inf, *lines_3).wait(0, 6)
        for i in range(1, 5):
            for j in range(i+1):
                if (i, j) not in [(4, 4)]:
                    groups_lines[4-i][j].set_opacity(0.1)
                else: 
                    groups_lines[4-i][j].set_opacity(1)
        self.remove(*lines_3).wait(0, 6)
        for i in range(1, 5):
            for j in range(i+1):
                groups_lines[4-i][j].set_opacity(1)
        self.wait(1)
        label_5 = MTex(r"\frac14").scale(0.6).next_to(self.perspective(trees_3[1].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        label_6 = MTex(r"\frac34").scale(0.6).next_to(self.perspective(trees_3[3].get_start()), DOWN).fix_in_frame().set_stroke(width = 8, color = BACK, background = True)
        self.play(Write(label_5), Write(label_6))
        self.wait(1)

        group = VGroup(VGroup())
        def lines_updater(mob: VGroup):
            mark = self.time - 25 + 13/7
            i = 1
            mob.set_submobjects(mob.submobjects[1:])
            old_i = len(mob.submobjects)
            while mark >= 1/i:
                if i >= old_i - 1:
                    new_group = VGroup(*[Line(point_o, point_i, color = BLUE, stroke_width = 6) for point_o, point_i in zip(points_out(i), points_in(i))])
                    mob.insert_submobject(0, new_group)
                mark -= 1/i
                i += 1
            new_group = VGroup(*[Line(point_o, point_i, color = YELLOW, stroke_width = 6) for point_o, point_i in zip(points_out(i), points_in(i))])
            mob.insert_submobject(0, new_group)
        group.add_updater(lines_updater)
        self.remove(*trees_0, *trees_1, *trees_2, *trees_3).bring_to_back(background, line_inf, group).wait(3)
        group.clear_updaters()
        self.wait(1)
        
        distance = 0.25
        self.play(*[mob.animate.scale(np.array([1, 1, 1/3])) for mob in [background, group]], line_inf.animate.set_stroke(width = 2), *[FadeOut(mob) for mob in infs], *[OverFadeOut(mob, shift = mob.get_y()*DOWN*2/3) for mob in [label_0, label_1, label_2, label_3, label_4, label_5, label_6]], run_time = 2)
        self.wait(1)
        direction = unit(np.arctan((np.sqrt(5)-1)/2))
        alpha = ValueTracker(0.0)
        def line_updater(mob: Line):
            mob.put_start_and_end_on(0.25*direction, 0.25*2**alpha.get_value()*direction).shift(distance*IN)
        line = Line(color = ORANGE).add_updater(line_updater)
        self.add(line).play(alpha.animate.set_value(8), run_time = 8, rate_func = linear)
        line.clear_updaters()
        self.wait(1)
        self.play(FadeOut(line))
        self.wait(1)

class Video_5(FrameScene):
    def construct(self):
        interval = Line(4*LEFT, 4*RIGHT).shift(3*UP)

        ratio = lambda t: interpolate(4*LEFT, 4*RIGHT, t)
        group = VGroup()
        mark = 6
        i = 1
        while mark >= 1/i:
            new_group = VGroup(*[Line(0.5/i*UP, 0.5/i*DOWN, stroke_width = min(4, 20/i), color = BLUE).shift(ratio(j/i) + 3*UP) for j in range(i+1)])
            group.add(new_group)
            mark -= 1/i
            i += 1
        self.add(interval, group).wait(1)
        self.play(group.animate.scale(np.array([1, 3, 1]), about_point = 3.5*UP), interval.animate.set_stroke(width = 8).shift(DOWN), run_time = 2)
        self.wait(1)

        phi = (np.sqrt(5)-1)/2
        position = interpolate(-4, 4, phi)
        def ratio(t, value):
            raw = interpolate(-4, 4, t)
            return ((raw-position)*value+position)*RIGHT
        alpha = ValueTracker(0.0)
        def interval_updater(mob: Line):
            value = 2**alpha.get_value()
            mob.put_start_and_end_on(((-4-position)*value+position)*RIGHT + 2*UP, ((4-position)*value+position)*RIGHT + 2*UP)
            if value > 4:
                mob.clear_updaters()
        interval.add_updater(interval_updater)
        def group_updater(mob: VGroup):
            mob.set_submobjects([])
            value = alpha.get_value()
            enlarge = 2**alpha.get_value()
            start, end = max(0, (-0.5-phi)/enlarge + phi), min(1, (1.5-phi)/enlarge + phi)
            scales = int(enlarge/2)+1
            height_factor = enlarge*((np.log(value+1)+1)/(value+1))**3
            threshold = int((np.sqrt(scales**2+40000*scales)-scales))
            for i in range(1, scales+threshold):
                if int(start*i)<=int(end*i):
                    new_group = VGroup(*[Line(1.5/i*UP*height_factor, 1.5/i*DOWN*height_factor, stroke_width = min(4, 20/i*height_factor), color = BLUE).shift(ratio(j/i, enlarge) + 2*UP) for j in range(int(start*i), int(end*i)+1)])
                    mob.add(new_group)
        group.add_updater(group_updater)
        self.play(alpha.animate.set_value(10), run_time = 11, rate_func = smooth_boot(1/11))
        group.clear_updaters()
        self.wait(1)
            


class Cover(CoverScene):
    def construct(self):
        pic_1 = ImageMobject("trees.jpg", height = 6).shift(LEFT + 0.4*UP + 0.2*RIGHT)
        shade = Shade(fill_color = BLACK).copy().next_to(LEFT, RIGHT, buff = 0)

        interval = Line(ORIGIN, 4*RIGHT)
        ratio = lambda t: interpolate(4*LEFT, 4*RIGHT, t)
        group = VGroup(interval)
        mark = 6
        i = 1
        while mark >= 1/i:
            new_group = VGroup(*[Line(2.5/i*UP, 2.5/i*DOWN, stroke_width = min(8, 40/i), color = BLUE).shift(ratio(j/i)) for j in range((i+1)//2, i+1)])
            group.insert_submobject(1, new_group)
            mark -= 1/i
            i += 1
        group.shift(LEFT)

        text = Text(r"有理树", font = "FZDaHei-B02S").set_stroke(width = 20, color = BLACK, background = True).scale(3.5)
        text[0].move_to(5*RIGHT + 2.5*UP)
        text[1].move_to(5*RIGHT)
        text[2].move_to(5*RIGHT + 2.5*DOWN).set_fill(color = GREEN).set_stroke(color = GREY_E).rotate(-PI/9)
        self.add(pic_1, shade, group, text)
        

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]