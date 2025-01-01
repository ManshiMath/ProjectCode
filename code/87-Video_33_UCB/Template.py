from __future__ import annotations

from manimlib import *
import numpy as np
from scipy.stats import beta

#################################################################### 

class NixieTube(Polygon):
    CONFIG = {
        "fill_opacity": 1, 
        "stroke_width": 0,
        "light_color": YELLOW, 
        "dark_color": GREY_E, 
    }
    def __init__(self, length = 1, width = 0.2, buff = 0.02, vertical = False, **kwargs):
        nudge = (width / 2 - buff)
        if vertical:
            half = (length / 2 - buff) * UP
            points = [half, half + nudge * DR, -half + nudge * UR, -half, -half + nudge * UL, half + nudge * DL]
        else:
            half = (length / 2 - buff) * RIGHT
            points = [half, half + nudge * UL, -half + nudge * UR, -half, -half + nudge * DR, half + nudge * DL]
        super().__init__(*points, **kwargs)
        self.set_fill(color = self.dark_color)

    def light_up(self):
        self.set_fill(color = self.light_color)
        return self

    def dim_down(self):
        self.set_fill(color = self.dark_color)
        return self

class NixieDigit(VGroup):

    digit_dic = {0: [0, 1, 2, 4, 5, 6], 1: [2, 5], 2: [0, 2, 3, 4, 6], 3: [0, 2, 3, 5, 6], 4: [1, 2, 3, 5], 5: [0, 1, 3, 5, 6], 6: [0, 1, 3, 4, 5, 6], 7: [0, 2, 5], 8: [0, 1, 2, 3, 4, 5, 6], 9: [0, 1, 2, 3, 5, 6]}

    def __init__(self, length = 1, width = 0.25, buff = 0.04, colors = [YELLOW, GREY_E], **kwargs):
        tube_h = NixieTube(length, width, buff, light_color = colors[0], dark_color = colors[1])
        tube_v = NixieTube(length, width, buff, light_color = colors[0], dark_color = colors[1],  vertical = True)
        super().__init__(tube_h.copy().shift(length*UP), tube_v.copy().shift(length/2*UL), tube_v.copy().shift(length/2*UR), 
                         tube_h.copy(), tube_v.copy().shift(length/2*DL), tube_v.copy().shift(length/2*DR), 
                         tube_h.copy().shift(length*DOWN), **kwargs)
        self.lit = [False]*7
        
    def light_up(self, *indices):
        for i in range(7):
            if i in indices:
                self[i].light_up()
                self.lit[i] = True
            else:
                self[i].dim_down()
                self.lit[i] = False
        return self
    
    def set_digit(self, digit):
        self.light_up(*self.digit_dic[digit])
        return self
    
class Test_1(FrameScene):
    def construct(self):
        digit_0 = NixieDigit()
        digits = [digit_0.copy().shift((i-4.5)*1.2*RIGHT).scale(0.5).set_digit(i) for i in range(10)]
        self.add(*digits)
        self.wait()

class Switch(VGroup):
    def __init__(self, height = 1, width = 0.4, space = 1, surr = 0.1,
                 radius = 0.25, 
                 colors = [RED, interpolate_color(RED, BLACK, 0.5)], **kwargs):
        left, right = [Rectangle(width, height, stroke_width = 0, fill_opacity = 1, fill_color = colors[1]).shift(position) for position in [space/2*LEFT, space/2*RIGHT]]
        left2, right2 = [Rectangle(width + surr, height + surr, stroke_width = 0, fill_opacity = 1, fill_color = BLACK).shift(position) for position in [space/2*LEFT, space/2*RIGHT]]
        left3, right3 = [Rectangle(width + 2*surr, height + 2*surr, stroke_width = 0, fill_opacity = 1, fill_color = colors[1]).shift(position) for position in [space/2*LEFT, space/2*RIGHT]]
        def oval(space, radius, color):
            points = [space/2*RIGHT + radius*DOWN, space/2*RIGHT + radius*RIGHT, space/2*RIGHT + radius*UP, space/2*LEFT + radius*UP, space/2*LEFT + radius*LEFT, space/2*LEFT + radius*DOWN]
            return VMobject(stroke_width = 0, fill_opacity = 1, fill_color = color).append_points(ArcBetweenPoints(points[0], points[1], angle = PI/2).get_points()
                 ).append_points(ArcBetweenPoints(points[1], points[2], angle = PI/2).get_points()).add_line_to(points[3]
                 ).append_points(ArcBetweenPoints(points[3], points[4], angle = PI/2).get_points()
                 ).append_points(ArcBetweenPoints(points[4], points[5], angle = PI/2).get_points()).add_line_to(points[0])
        switch, switch_2, switch_3 = oval(space, radius - surr, colors[0]), oval(space, radius - surr/2, BLACK), oval(space, radius, colors[0])
        super().__init__(left3, right3, left2, right2, left, right, switch_3, switch_2, switch, **kwargs)

class Bulb(Dot):
    CONFIG = {
        "light_color": YELLOW, 
        "dark_color": GREY_E, 
    }
    def light_up(self):
        self.set_fill(color = self.light_color)
        return self

    def dim_down(self):
        self.set_fill(color = self.dark_color)
        return self
    
class Strip(Rectangle):
    CONFIG = {
        "light_color": YELLOW, 
        "dark_color": GREY_E, 
    }
    def light_up(self):
        self.set_stroke(color = self.light_color)
        return self

    def dim_down(self):
        self.set_stroke(color = self.dark_color)
        return self

class Bandit(VGroup):
    def __init__(self, switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [YELLOW, interpolate_color(YELLOW, BLACK, 0.5)]}, 
                digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [YELLOW, GREY_E]},
                slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP}, 
                digits_dic = {"buff": 0.2, "colors_0": [YELLOW, interpolate_color(YELLOW, BLACK, 0.8)], "colors_1": [WHITE, GREY_E], "offset": 1.5*DOWN}, 
                simplify = False, **kwargs):
        
        offset = slot_dic["offset"]
        self.switch = Switch(**switch_dic)

        width_small, height_small, space, buff, color = switch_dic["width"], slot_dic["height"], switch_dic["space"], slot_dic["buff"], slot_dic["color"]  
        width, height = width_small + space + buff*2, height_small + buff*2
        self.slot = VGroup(Rectangle(width, height, stroke_width = 0, fill_opacity = 1, fill_color = color), 
                           *[Rectangle(width_small, height_small, stroke_width = 0, fill_opacity = 1, fill_color = BLACK).shift(position) for position in [space/2*LEFT, space/2*RIGHT]]).shift(offset)
        self.up, self.down = offset + (height_small - switch_dic["height"])/2*UP, offset + (height_small - switch_dic["height"])/2*DOWN
        self.switch.move_to(self.up)

        offset = digits_dic["offset"]
        width_small, length_small, buff = digit_dic["width"], digit_dic["length"], digits_dic["buff"]
        space, height_medium = length_small + width_small + buff, 2*length_small + width_small
        self.digits = VGroup(*[NixieDigit(**digit_dic).shift((i-1)*space*RIGHT + offset) for i in range(3)])

        width, height = space * 3 + buff, height_medium + buff*2
        colors_0, colors_1 = digits_dic["colors_0"], digits_dic["colors_1"]
        stroke_width = 12
        self.strip_inner = Strip(width, height, light_color = colors_0[0], dark_color = colors_0[1], stroke_width = stroke_width).dim_down().shift(offset)
        if not simplify:
            self.strip_outer = Strip(width + 4*buff, height + 4*buff, light_color = colors_0[0], dark_color = colors_0[1], stroke_width = stroke_width).dim_down().shift(offset)
            
            ul, ur, dl, dr = width/2*LEFT + height/2*UP + buff*UL, width/2*RIGHT + height/2*UP + buff*UR, width/2*LEFT + height/2*DOWN + buff*DL, width/2*RIGHT + height/2*DOWN + buff*DR
            h, v = round((width + 2*buff)/buff), round((height + 2*buff)/buff)
            positions = [ul + i*buff*RIGHT for i in range(h)] + [ur + i*buff*DOWN for i in range(v)] + [dr + i*buff*LEFT for i in range(h)] + [dl + i*buff*UP for i in range(v)]
            self.dots = VGroup(*[Bulb(light_color = colors_0[0] if i%2 else colors_1[0], dark_color = colors_0[1] if i%2 else colors_1[1]).shift(position + offset).dim_down() for i, position in enumerate(positions)])
            self.number = len(self.dots)
            super().__init__(self.slot, self.switch, self.digits, self.strip_inner, self.strip_outer, self.dots, **kwargs)
        else:
            super().__init__(self.slot, self.switch, self.digits, self.strip_inner, **kwargs)

    def set_value(self, value):
        value %= 1
        for digit in self.digits:
            value *= 10
            digit.set_digit(int(value))
            value %= 1

class Test_2(FrameScene):
    def construct(self):
        # switch = Switch()
        # self.add(switch)
        # self.wait()
        bandit = Bandit()
        self.add(bandit)
        self.wait()
        
#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        bandit_2 = Bandit(**dic_gen(RED, WHITE))#.shift(ORIGIN)
        bandit_3 = Bandit(**dic_gen(BLUE, WHITE)).shift(4.5*RIGHT)
        bandit_1.offset, bandit_2.offset, bandit_3.offset = 4.5*LEFT, ORIGIN, 4.5*RIGHT
        self.wait()

        bandits = [bandit_1, bandit_2, bandit_3]
        shades = [SurroundingRectangle(mob, **background_dic) for mob in bandits]
        self.play(*[bandits[i].shift(0.5*DOWN).animating(delay = i*0.5).shift(0.5*UP) for i in range(3)], *[FadeOut(shades[i].shift(0.5*DOWN), 0.5*UP, delay = i*0.5) for i in range(3)])
        self.wait()

        self.add_sound("sound_2.wav")
        alpha = ValueTracker(0)
        def start_updater(mob: Bandit, dt: float):
            value = alpha.get_value()
            mob.switch.move_to(interpolate(mob.up, mob.down, value) + mob.offset)
            color = interpolate_color(mob.strip_inner.dark_color, mob.strip_inner.light_color, value)
            mob.strip_inner.set_stroke(color = color), mob.strip_outer.set_stroke(color = color)
            if dt > 0:
                mob.dots[mob.index].light_up(), mob.dots[mob.number//2 + mob.index].light_up()
                mob.index += 1
        for mob in bandits:
            mob.index = 0
            mob.add_updater(start_updater)
        self.play(alpha.animate.set_value(1), run_time = 1/3, frames = 10)
        def running_updater(mob: Bandit, dt: float):
            if dt > 0:
                mob.switch.shift((mob.up - mob.down)/170)
                mob.dots[(mob.index) % mob.number].light_up(), mob.dots[(mob.number//2 + mob.index) % mob.number].light_up()
                mob.dots[(mob.index - 10) % mob.number].dim_down(), mob.dots[(mob.number//2 + mob.index - 10) % mob.number].dim_down()
                mob.index += 1
                for digit in mob.digits:
                    randoms = np.random.rand(7)
                    for i in range(7):
                        if randoms[i] < 0.2:
                            digit.lit[i] = not digit.lit[i]
                        if digit.lit[i]:
                            digit[i].light_up()
                        else:
                            digit[i].dim_down()
        for mob in bandits:
            mob.clear_updaters()
            mob.add_updater(running_updater)
        self.wait(0, 110)

        digit_dic = {0: [True, True, True, False, True, True, True], 1: [False, False, True, False, False, True, False], 2: [True, False, True, True, True, False, True], 3: [True, False, True, True, False, True, True], 4: [False, True, True, True, False, True, False], 5: [True, True, False, True, False, True, True], 6: [True, True, False, True, True, True, True], 7: [True, False, True, False, False, True, False], 8: [True, True, True, True, True, True, True], 9: [True, True, True, True, False, True, True]}
        alpha.set_value(0)
        def damping_updater(mob: Bandit, dt: float):
            if dt > 0:
                mob.switch.shift((mob.up - mob.down)/170)
                mob.dots[(mob.index) % mob.number].light_up(), mob.dots[(mob.number//2 + mob.index) % mob.number].light_up()
                mob.dots[(mob.index - 10) % mob.number].dim_down(), mob.dots[(mob.number//2 + mob.index - 10) % mob.number].dim_down()
                mob.index += 1
                random_result = beta.rvs(*mob.betas) % 1
                for digit in mob.digits:
                    random_result *= 10
                    lit_list = digit_dic[int(random_result)]
                    random_result %= 1

                    thresholds, randoms = np.random.rand(7), np.random.rand(7)
                    for i in range(7):
                        if thresholds[i] < alpha.get_value():
                            digit.lit[i] = lit_list[i]
                        else:
                            if randoms[i] < 0.2:
                                digit.lit[i] = not digit.lit[i]
                        if digit.lit[i]:
                            digit[i].light_up()
                        else:
                            digit[i].dim_down()
        bandit_1.betas, bandit_2.betas, bandit_3.betas = (2, 3), (8, 2), (5, 3)
        for mob in bandits:
            mob.clear_updaters()
            mob.add_updater(damping_updater)
        self.play(alpha.animate.set_value(1))
        alpha.set_value(0)
        gamma = ValueTracker(0)
        def stop_updater(mob: Bandit, dt: float):
            if dt > 0:
                mob.switch.shift((mob.up - mob.down)/170)
                color = interpolate_color(mob.strip_inner.light_color, mob.strip_inner.dark_color, gamma.get_value())
                mob.strip_inner.set_stroke(color = color), mob.strip_outer.set_stroke(color = color)
            value = alpha.get_value()
            counter = int(value*10)
            if counter > mob.counter:
                mob.counter += 1
                mob.dots[(mob.index - 10) % mob.number].dim_down(), mob.dots[(mob.number//2 + mob.index - 10) % mob.number].dim_down()
                mob.index += 1
                mob.set_value(beta.rvs(*mob.betas))
        for mob in bandits:
            mob.clear_updaters()
            mob.counter = 0
            mob.add_updater(stop_updater)
        self.play(alpha.animating(rate_func = lambda t: 1 - (1-t)**3).set_value(1), gamma.animate.set_value(1))
        for mob in bandits:
            mob.clear_updaters()
            mob.switch.move_to(mob.up + mob.offset), mob.strip_inner.dim_down(), mob.strip_outer.dim_down()
            for dot in mob.dots:
                dot.dim_down()
        self.wait()

        def replay(mob: Bandit):
            target = mob.generate_target()
            target.switch.move_to(mob.down + mob.offset), target.strip_inner.light_up(), target.strip_outer.light_up()
            self.add_sound("sound_0.wav")
            self.play(MoveToTarget(mob), run_time = 1/3, frames = 10)
            mob.set_value(beta.rvs(*mob.betas))
            target = mob.generate_target()
            target.switch.move_to(mob.up + mob.offset), target.strip_inner.dim_down(), target.strip_outer.dim_down()
            self.play(MoveToTarget(mob), run_time = 1/3, frames = 10)
            self.wait(0, 10)
        for _ in range(15):
            replay(random.choice(bandits))
        self.wait(1)

class Video_2(FrameScene):
    def construct(self):
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        self.add(bandit_1).wait()

        digits = [MTex(str(i))[0] for i in range(10)]
        template = MTex(r"0.00")
        for i in range(30):
            string = f"{beta.rvs(2, 3):.3f}"
            tex = template.copy()
            [tex[i].become(digits[int(string[j])]).move_to(template[i]) for i, j in [(0,2), (2,3), (3,4)]]
            tex.shift((i%5*1.5 - 0.5)*RIGHT + (i//5 - 3)*DOWN)
            for k, digit in enumerate(bandit_1.digits):
                digit.set_digit(int(string[k+2]))
            self.add(tex).wait(1)
        
        self.wait()

class Video_3(FrameScene):
    def construct(self):
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        interval = Rectangle(height = 4, width = 0.8, fill_opacity = 1, fill_color = BLACK).shift(RIGHT)
        inf, sup = MTex(r"0", color = YELLOW).next_to(interval, DOWN), MTex(r"10", color = YELLOW).next_to(interval, UP)
        up, down = interval.get_top(), interval.get_bottom()
        text_avg = Songti("平均值：").scale(0.8).shift(3.5*RIGHT + UP)
        mu = Line(color = RED).shift(interpolate(down, up, 0.4))    
        self.add_lower(mu, interval).add(bandit_1, text_avg, inf, sup).wait()

        digits = [MTex(str(i), color = GREEN)[0] for i in range(10)]
        template = MTex(r"0.00", color = GREEN)

        sample = beta.rvs(2, 3)
        avg = sample
        string = f"{avg:.3f}"
        tex = template.copy()
        [tex[i].become(digits[int(string[j])]).move_to(template[i]) for i, j in [(0,2), (2,3), (3,4)]]
        tex.next_to(text_avg, RIGHT)
        dot = Dot(color = GREEN_E).move_to(interpolate(down, up, sample) + (random.random()*2-1)*0.3*RIGHT)
        line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN)).shift(interpolate(down, up, avg))
        self.add_lower(dot).play(GrowFromCenter(dot), Write(tex), ShowCreation(line, start = 0.5, lag_ratio = 0))
        self.wait(1)
        for i in range(1, 30):
            sample = beta.rvs(2, 3)
            string = f"{sample:.3f}"
            for k, digit in enumerate(bandit_1.digits):
                digit.set_digit(int(string[k+2]))

            avg = interpolate(avg, sample, 1/(i+1))
            string = f"{avg:.3f}"
            new_tex = template.copy()
            [new_tex[i].become(digits[int(string[j])]).move_to(template[i]) for i, j in [(0,2), (2,3), (3,4)]]
            tex.become(new_tex).next_to(text_avg, RIGHT)
            dot = Dot(color = GREEN_E).move_to(interpolate(down, up, sample) + (random.random()*2-1)*0.3*RIGHT)
            line.move_to(interpolate(down, up, avg))
            self.add_lower(dot).wait(1)

        self.wait()
        
class Video_4(FrameScene):
    def construct(self):
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        interval = Rectangle(height = 4, width = 0.8, stroke_width = 0, fill_opacity = 1, fill_color = BLACK).shift(RIGHT)
        interval_surr = Rectangle(height = 4, width = 0.8).shift(RIGHT)
        inf, sup = MTex(r"0", color = YELLOW).next_to(interval, DOWN), MTex(r"10", color = YELLOW).next_to(interval, UP)
        up, down = interval.get_top(), interval.get_bottom()
        text_avg = Songti("平均值：").scale(0.8).shift(3.5*RIGHT + UP)
        text_con = Songti("乐观加分：").scale(0.8).shift(3.5*RIGHT + DOWN).match_x(text_avg, RIGHT)
        mu = Line(color = RED).shift(interpolate(down, up, 0.4))    
        self.add_lower(mu, interval).add(interval_surr, bandit_1, text_avg, text_con, inf, sup).wait()

        digits = [MTex(str(i), color = GREEN)[0] for i in range(10)]
        template = MTex(r"0.00", color = GREEN)

        avg = 0
        tex_avg, tex_con = template.copy().next_to(text_avg, RIGHT), template.copy().next_to(text_con, RIGHT).set_color(BLUE)
        line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN))
        rect = Rectangle(height = 4*0.6, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(3.5*RIGHT + DOWN)
        self.add_lower(rect).add(line, tex_avg, tex_con)
        for i in range(30):
            sample = beta.rvs(2, 3)
            string = f"{sample:.3f}"
            for k, digit in enumerate(bandit_1.digits):
                digit.set_digit(int(string[k+2]))

            avg = interpolate(avg, sample, 1/(i+1))
            string = f"{avg:.3f}"
            new_tex = template.copy()
            [new_tex[i].become(digits[int(string[j])]).move_to(template[i]) for i, j in [(0,2), (2,3), (3,4)]]
            tex_avg.become(new_tex).next_to(text_avg, RIGHT)
            line.move_to(interpolate(down, up, avg))
            
            con = 0.6/np.sqrt(i+1)
            string = f"{con*5:.3f}"
            new_tex = template.copy()
            [new_tex[i].become(digits[int(string[i])]).move_to(template[i]) for i in [0, 2, 3]]
            tex_con.become(new_tex).next_to(text_con, RIGHT).set_color(BLUE)
            rect.set_height(4*con, stretch = True).move_to(interpolate(down, up, avg))

            dot = Dot(color = GREEN_E).move_to(interpolate(down, up, sample) + (random.random()*2-1)*0.3*RIGHT)
            self.add_lower(dot).wait(1)

        self.wait()

class Video_5(FrameScene):
    def construct(self):
        width_0 = 0.5
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP + RIGHT}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        bandit_2 = Bandit(**dic_gen(RED, WHITE))#.shift(ORIGIN)
        bandit_3 = Bandit(**dic_gen(BLUE, WHITE)).shift(4.5*RIGHT)
        bandit_1.offset, bandit_2.offset, bandit_3.offset = 4.5*LEFT, ORIGIN, 4.5*RIGHT
        bandits = [bandit_1, bandit_2, bandit_3]
        offset_i = 2*UP + 1*LEFT
        interval_1 = Rectangle(height = 2.5, width = 0.8, **background_dic).shift(offset_i + bandit_1.offset)
        interval_surr_1 = Rectangle(height = 2.5, width = 0.8).shift(offset_i + bandit_1.offset)
        bandit_1.top, bandit_1.bottom = interval_1.get_top(), interval_1.get_bottom()
        interval_surr_1.add(#Rectangle(height = 0.6, width = 0.8, **background_dic).next_to(interval_1, DOWN, buff = 0), Rectangle(height = 0.8, width = 0.8, **background_dic).next_to(interval_1, UP, buff = 0), 
                            MTex(r"0", color = YELLOW).next_to(interval_1, DOWN).set_stroke(**stroke_dic), MTex(r"10", color = YELLOW).next_to(interval_1, UP).set_stroke(**stroke_dic))
        mu_1 = Line(0.8*LEFT, 0.8*RIGHT, color = RED).shift(interpolate(bandit_1.bottom, bandit_1.top, 0.4))    
        interval_2 = Rectangle(height = 2.5, width = 0.8, **background_dic).shift(offset_i + bandit_2.offset)
        interval_surr_2 = Rectangle(height = 2.5, width = 0.8).shift(offset_i + bandit_2.offset)
        bandit_2.top, bandit_2.bottom = interval_2.get_top(), interval_2.get_bottom()
        interval_surr_2.add(#Rectangle(height = 0.6, width = 0.8, **background_dic).next_to(interval_2, DOWN, buff = 0), Rectangle(height = 0.8, width = 0.8, **background_dic).next_to(interval_2, UP, buff = 0), 
                            MTex(r"0", color = RED).next_to(interval_2, DOWN).set_stroke(**stroke_dic), MTex(r"10", color = RED).next_to(interval_2, UP).set_stroke(**stroke_dic))
        mu_2 = Line(0.8*LEFT, 0.8*RIGHT, color = RED).shift(interpolate(bandit_2.bottom, bandit_2.top, 0.8))    
        interval_3 = Rectangle(height = 2.5, width = 0.8, **background_dic).shift(offset_i + bandit_3.offset)
        interval_surr_3 = Rectangle(height = 2.5, width = 0.8).shift(offset_i + bandit_3.offset)
        bandit_3.top, bandit_3.bottom = interval_3.get_top(), interval_3.get_bottom()
        interval_surr_3.add(#Rectangle(height = 0.6, width = 0.8, **background_dic).next_to(interval_3, DOWN, buff = 0), Rectangle(height = 0.8, width = 0.8, **background_dic).next_to(interval_3, UP, buff = 0), 
                            MTex(r"0", color = BLUE).next_to(interval_3, DOWN).set_stroke(**stroke_dic), MTex(r"10", color = BLUE).next_to(interval_3, UP).set_stroke(**stroke_dic))
        mu_3 = Line(0.8*LEFT, 0.8*RIGHT, color = RED).shift(interpolate(bandit_3.bottom, bandit_3.top, 5/8))    
        self.add_lower(mu_1, mu_2, mu_3, interval_1, interval_2, interval_3).add(*bandits, interval_surr_1, interval_surr_2, interval_surr_3).wait()

        bandit_1.avg, bandit_2.avg, bandit_3.avg = 0, 0, 0
        bandit_1.betas, bandit_2.betas, bandit_3.betas = (2, 3), (8, 2), (5, 3)
        bandit_1.N, bandit_2.N, bandit_3.N = 0, 0, 0

        #beta.rvs(2, 3)
        sample = beta.rvs(*bandit_1.betas)
        bandit_1.N += 1
        bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
        bandit_1.con = width_0/np.sqrt(bandit_1.N)
        bandit_1.line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN)).shift(interpolate(bandit_1.bottom, bandit_1.top, sample))    
        bandit_1.rect = Rectangle(height = 2.5*2*bandit_1.con, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(interpolate(bandit_1.bottom, bandit_1.top, sample)).set_height(2.5*2*bandit_1.con, stretch = True)
        bandit_1.rect.uniforms["anti_alias_width"] = 0
        dot = Dot(color = GREEN_E).move_to(interpolate(bandit_1.bottom, bandit_1.top, sample) + (random.random()*2-1)*0.3*RIGHT)
        string = f"{sample:.3f}"
        target = bandit_1.digits.generate_target()
        [target[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_sound("sound_0.wav")
        rate_func_1, rate_func_2 = lambda t: 1 if t > 1/3 else 0, squish_rate_func(smooth, 1/3, 1)
        self.add_lower(dot, bandit_1.rect).add(bandit_1.line).play(
            bandit_1.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_1.down + bandit_1.offset), 
            bandit_1.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_1.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
            MoveToTarget(bandit_1.digits, rate_func = rate_func_1), 
            ShowCreation(bandit_1.line, start = 0.5, lag_ratio = 0, rate_func = rate_func_2), bandit_1.rect.save_state().scale(np.array([1, 0, 1]), min_scale_factor = 0).animating(rate_func = rate_func_2).restore(), GrowFromCenter(dot, rate_func = rate_func_1), 
        )
        self.wait(1)

        sample = beta.rvs(*bandit_2.betas)
        bandit_2.N += 1
        bandit_2.avg = interpolate(bandit_2.avg, sample, 1/bandit_2.N)
        bandit_2.con = width_0/np.sqrt(bandit_2.N)
        bandit_2.line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN)).shift(interpolate(bandit_2.bottom, bandit_2.top, sample))    
        bandit_2.rect = Rectangle(height = 2.5*2*bandit_2.con, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(interpolate(bandit_2.bottom, bandit_2.top, sample)).set_height(2.5*2*bandit_2.con, stretch = True)
        bandit_2.rect.uniforms["anti_alias_width"] = 0
        dot = Dot(color = GREEN_E).move_to(interpolate(bandit_2.bottom, bandit_2.top, sample) + (random.random()*2-1)*0.3*RIGHT)
        string = f"{sample:.3f}"
        target = bandit_2.digits.generate_target()
        [target[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_sound("sound_0.wav")
        self.add_lower(dot, bandit_2.rect).add(bandit_2.line).play(
            bandit_2.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_2.down + bandit_2.offset), 
            bandit_2.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_2.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
            MoveToTarget(bandit_2.digits, rate_func = rate_func_1), 
            ShowCreation(bandit_2.line, start = 0.5, lag_ratio = 0, rate_func = rate_func_2), bandit_2.rect.save_state().scale(np.array([1, 0, 1]), min_scale_factor = 0).animating(rate_func = rate_func_2).restore(), GrowFromCenter(dot, rate_func = rate_func_1), 
        )
        self.wait(1)

        sample = beta.rvs(*bandit_3.betas)
        bandit_3.N += 1
        bandit_3.avg = interpolate(bandit_3.avg, sample, 1/bandit_3.N)
        bandit_3.con = width_0/np.sqrt(bandit_3.N)
        bandit_3.line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN)).shift(interpolate(bandit_3.bottom, bandit_3.top, sample))    
        bandit_3.rect = Rectangle(height = 2.5*2*bandit_3.con, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(interpolate(bandit_3.bottom, bandit_3.top, sample)).set_height(2.5*2*bandit_3.con, stretch = True)
        bandit_3.rect.uniforms["anti_alias_width"] = 0
        dot = Dot(color = GREEN_E).move_to(interpolate(bandit_3.bottom, bandit_3.top, sample) + (random.random()*2-1)*0.3*RIGHT)
        string = f"{sample:.3f}"
        target = bandit_3.digits.generate_target()
        [target[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_sound("sound_0.wav")
        self.add_lower(dot, bandit_3.rect).add(bandit_3.line).play(
            bandit_3.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_3.down + bandit_3.offset), 
            bandit_3.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_3.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
            MoveToTarget(bandit_3.digits, rate_func = rate_func_1), 
            ShowCreation(bandit_3.line, start = 0.5, lag_ratio = 0, rate_func = rate_func_2), bandit_3.rect.save_state().scale(np.array([1, 0, 1]), min_scale_factor = 0).animating(rate_func = rate_func_2).restore(), GrowFromCenter(dot, rate_func = rate_func_1), 
        )
        self.wait(1)
        
        beta.rvs(2, 3)
        for _ in range(30):
            bandit = max(bandits, key = lambda x: x.avg + x.con)
            sample = beta.rvs(*bandit.betas)
            bandit.N += 1
            bandit.avg = interpolate(bandit.avg, sample, 1/bandit.N)
            bandit.con = width_0/np.sqrt(bandit.N)
            bandit.line.generate_target().move_to(interpolate(bandit.bottom, bandit.top, bandit.avg))
            bandit.rect.generate_target().set_height(2.5*2*bandit.con, stretch = True).move_to(interpolate(bandit.bottom, bandit.top, bandit.avg))
            dot = Dot(color = GREEN_E).move_to(interpolate(bandit.bottom, bandit.top, sample) + (random.random()*2-1)*0.3*RIGHT)
            string = f"{sample:.3f}"
            target = bandit.digits.generate_target()
            [target[i].set_digit(int(string[i+2])) for i in range(3)]
            self.add_sound("sound_0.wav")
            self.add_lower(dot, bandit.rect).add(bandit.line).play(
                bandit.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit.down + bandit.offset), 
                bandit.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
                *[MoveToTarget(mob, rate_func = rate_func_1) for mob in [bandit.digits, bandit.line, bandit.rect]], 
                GrowFromCenter(dot, rate_func = rate_func_1), 
            )
            self.wait(0, 10)

class Video_5_2(FrameScene):
    def construct(self):
        width_0 = 0.5
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP + RIGHT}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        bandit_2 = Bandit(**dic_gen(RED, WHITE))#.shift(ORIGIN)
        bandit_3 = Bandit(**dic_gen(BLUE, WHITE)).shift(4.5*RIGHT)
        bandit_1.offset, bandit_2.offset, bandit_3.offset = 4.5*LEFT, ORIGIN, 4.5*RIGHT
        bandits = [bandit_1, bandit_2, bandit_3]
        offset_i = 2*UP + 1*LEFT
        interval_1 = Rectangle(height = 2.5, width = 0.8, **background_dic).shift(offset_i + bandit_1.offset)
        interval_surr_1 = Rectangle(height = 2.5, width = 0.8).shift(offset_i + bandit_1.offset)
        bandit_1.top, bandit_1.bottom = interval_1.get_top(), interval_1.get_bottom()
        interval_surr_1.add(#Rectangle(height = 0.6, width = 0.8, **background_dic).next_to(interval_1, DOWN, buff = 0), Rectangle(height = 0.8, width = 0.8, **background_dic).next_to(interval_1, UP, buff = 0), 
                            MTex(r"0", color = YELLOW).next_to(interval_1, DOWN), MTex(r"10", color = YELLOW).next_to(interval_1, UP))
        mu_1 = Line(0.8*LEFT, 0.8*RIGHT, color = RED).shift(interpolate(bandit_1.bottom, bandit_1.top, 0.4))    
        interval_2 = Rectangle(height = 2.5, width = 0.8, **background_dic).shift(offset_i + bandit_2.offset)
        interval_surr_2 = Rectangle(height = 2.5, width = 0.8).shift(offset_i + bandit_2.offset)
        bandit_2.top, bandit_2.bottom = interval_2.get_top(), interval_2.get_bottom()
        interval_surr_2.add(#Rectangle(height = 0.6, width = 0.8, **background_dic).next_to(interval_2, DOWN, buff = 0), Rectangle(height = 0.8, width = 0.8, **background_dic).next_to(interval_2, UP, buff = 0), 
                            MTex(r"0", color = RED).next_to(interval_2, DOWN), MTex(r"10", color = RED).next_to(interval_2, UP))
        mu_2 = Line(0.8*LEFT, 0.8*RIGHT, color = RED).shift(interpolate(bandit_2.bottom, bandit_2.top, 0.8))    
        interval_3 = Rectangle(height = 2.5, width = 0.8, **background_dic).shift(offset_i + bandit_3.offset)
        interval_surr_3 = Rectangle(height = 2.5, width = 0.8).shift(offset_i + bandit_3.offset)
        bandit_3.top, bandit_3.bottom = interval_3.get_top(), interval_3.get_bottom()
        interval_surr_3.add(#Rectangle(height = 0.6, width = 0.8, **background_dic).next_to(interval_3, DOWN, buff = 0), Rectangle(height = 0.8, width = 0.8, **background_dic).next_to(interval_3, UP, buff = 0), 
                            MTex(r"0", color = BLUE).next_to(interval_3, DOWN), MTex(r"10", color = BLUE).next_to(interval_3, UP))
        mu_3 = Line(0.8*LEFT, 0.8*RIGHT, color = RED).shift(interpolate(bandit_3.bottom, bandit_3.top, 5/8))    
        self.add_lower(mu_1, mu_2, mu_3, interval_1, interval_2, interval_3).add(*bandits, interval_surr_1, interval_surr_2, interval_surr_3).wait()

        bandit_1.avg, bandit_2.avg, bandit_3.avg = 0, 0, 0
        bandit_1.betas, bandit_2.betas, bandit_3.betas = (2, 3), (8, 2), (5, 3)
        bandit_1.N, bandit_2.N, bandit_3.N = 0, 0, 0

        sample = 0.703
        bandit_1.N += 1
        bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
        bandit_1.con = width_0/np.sqrt(bandit_1.N)
        bandit_1.line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN)).shift(interpolate(bandit_1.bottom, bandit_1.top, sample))    
        bandit_1.rect = Rectangle(height = 2.5*2*bandit_1.con, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(interpolate(bandit_1.bottom, bandit_1.top, sample)).set_height(2.5*2*bandit_1.con, stretch = True)
        bandit_1.rect.uniforms["anti_alias_width"] = 0
        dot = Dot(color = GREEN_E).move_to(interpolate(bandit_1.bottom, bandit_1.top, sample) + (random.random()*2-1)*0.3*RIGHT)
        string = f"{sample:.3f}"
        target = bandit_1.digits.generate_target()
        [target[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_sound("sound_0.wav")
        rate_func_1, rate_func_2 = lambda t: 1 if t > 1/3 else 0, squish_rate_func(smooth, 1/3, 1)
        self.add_lower(dot, bandit_1.rect).add(bandit_1.line).play(
            bandit_1.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_1.down + bandit_1.offset), 
            bandit_1.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_1.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
            MoveToTarget(bandit_1.digits, rate_func = rate_func_1), 
            ShowCreation(bandit_1.line, start = 0.5, lag_ratio = 0, rate_func = rate_func_2), bandit_1.rect.save_state().scale(np.array([1, 0, 1]), min_scale_factor = 0).animating(rate_func = rate_func_2).restore(), GrowFromCenter(dot, rate_func = rate_func_1), 
        )
        self.wait(1)

        sample = 0.386
        bandit_2.N += 1
        bandit_2.avg = interpolate(bandit_2.avg, sample, 1/bandit_2.N)
        bandit_2.con = width_0/np.sqrt(bandit_2.N)
        bandit_2.line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN)).shift(interpolate(bandit_2.bottom, bandit_2.top, sample))    
        bandit_2.rect = Rectangle(height = 2.5*2*bandit_2.con, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(interpolate(bandit_2.bottom, bandit_2.top, sample)).set_height(2.5*2*bandit_2.con, stretch = True)
        bandit_2.rect.uniforms["anti_alias_width"] = 0
        dot = Dot(color = GREEN_E).move_to(interpolate(bandit_2.bottom, bandit_2.top, sample) + (random.random()*2-1)*0.3*RIGHT)
        string = f"{sample:.3f}"
        target = bandit_2.digits.generate_target()
        [target[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_sound("sound_0.wav")
        self.add_lower(dot, bandit_2.rect).add(bandit_2.line).play(
            bandit_2.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_2.down + bandit_2.offset), 
            bandit_2.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_2.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
            MoveToTarget(bandit_2.digits, rate_func = rate_func_1), 
            ShowCreation(bandit_2.line, start = 0.5, lag_ratio = 0, rate_func = rate_func_2), bandit_2.rect.save_state().scale(np.array([1, 0, 1]), min_scale_factor = 0).animating(rate_func = rate_func_2).restore(), GrowFromCenter(dot, rate_func = rate_func_1), 
        )
        self.wait(1)

        sample = 0.612
        bandit_3.N += 1
        bandit_3.avg = interpolate(bandit_3.avg, sample, 1/bandit_3.N)
        bandit_3.con = width_0/np.sqrt(bandit_3.N)
        bandit_3.line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN)).shift(interpolate(bandit_3.bottom, bandit_3.top, sample))    
        bandit_3.rect = Rectangle(height = 2.5*2*bandit_3.con, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(interpolate(bandit_3.bottom, bandit_3.top, sample)).set_height(2.5*2*bandit_3.con, stretch = True)
        bandit_3.rect.uniforms["anti_alias_width"] = 0
        dot = Dot(color = GREEN_E).move_to(interpolate(bandit_3.bottom, bandit_3.top, sample) + (random.random()*2-1)*0.3*RIGHT)
        string = f"{sample:.3f}"
        target = bandit_3.digits.generate_target()
        [target[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_sound("sound_0.wav")
        self.add_lower(dot, bandit_3.rect).add(bandit_3.line).play(
            bandit_3.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_3.down + bandit_3.offset), 
            bandit_3.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_3.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
            MoveToTarget(bandit_3.digits, rate_func = rate_func_1), 
            ShowCreation(bandit_3.line, start = 0.5, lag_ratio = 0, rate_func = rate_func_2), bandit_3.rect.save_state().scale(np.array([1, 0, 1]), min_scale_factor = 0).animating(rate_func = rate_func_2).restore(), GrowFromCenter(dot, rate_func = rate_func_1), 
        )
        self.wait(1)

        def play(bandit, sample):
            bandit.N += 1
            bandit.avg = interpolate(bandit.avg, sample, 1/bandit.N)
            bandit.con = width_0/np.sqrt(bandit.N)
            bandit.line.generate_target().move_to(interpolate(bandit.bottom, bandit.top, bandit.avg))
            bandit.rect.generate_target().set_height(2.5*2*bandit.con, stretch = True).move_to(interpolate(bandit.bottom, bandit.top, bandit.avg))
            dot = Dot(color = GREEN_E).move_to(interpolate(bandit.bottom, bandit.top, sample) + (random.random()*2-1)*0.3*RIGHT)
            string = f"{sample:.3f}"
            target = bandit.digits.generate_target()
            [target[i].set_digit(int(string[i+2])) for i in range(3)]
            self.add_sound("sound_0.wav")
            self.add_lower(dot, bandit.rect).add(bandit.line).play(
                bandit.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit.down + bandit.offset), 
                bandit.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
                *[MoveToTarget(mob, rate_func = rate_func_1) for mob in [bandit.digits, bandit.line, bandit.rect]], 
                GrowFromCenter(dot, rate_func = rate_func_1), 
            )
            
        for _ in range(30):
            bandit = max(bandits, key = lambda x: x.avg + x.con)
            sample = beta.rvs(*bandit.betas)
            play(bandit, sample)
            self.wait(0, 10)
                
#################################################################### 

class ShowDot(Animation):
    CONFIG = {
        "rate_func": linear
    }

    def __init__(
        self,
        mobject: Mobject,
        **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.target_mobject = mobject.copy().set_color(YELLOW)
    
    def interpolate_mobject(self, alpha: float) -> None:
        if alpha <= 1/3:
            self.mobject.set_opacity(0)
        else:
            t = smooth((1-alpha)*1.5)
            self.mobject.interpolate(self.starting_mobject, self.target_mobject, t)
        return self
    
class Video_6(FrameScene):
    def construct(self):
        N = 15
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        bandit_1.offset = 4.5*LEFT
        interval = Rectangle(height = 5, width = 0.6, fill_opacity = 1, fill_color = BLACK).shift(0.4*UP + 1.2*LEFT)
        inf, sup = MTex(r"0", color = YELLOW).next_to(interval, DOWN), MTex(r"10", color = YELLOW).next_to(interval, UP)
        bandit_1.top, bandit_1.bottom = interval.get_top(), interval.get_bottom()
        mu = Line(0.6*LEFT, 0.6*RIGHT, color = RED).shift(interpolate(bandit_1.bottom, bandit_1.top, 0.4))
        offset_r = bandit_1.bottom + 1.2*RIGHT
        axes = VGroup(Arrow(0.5*LEFT, 7*RIGHT), Arrow(0.5*DOWN, 5.5*UP)).shift(offset_r)
        labels = VGroup(Songti("采样次数", color = YELLOW).scale(0.6).next_to(axes[0].get_right(), DL), Songti("平均值", color = GREEN).scale(0.6).next_to(axes[1].get_top(), UP))
        self.add_lower(mu, interval).add(bandit_1, inf, sup).wait()

        bandit_1.avg, bandit_1.N = 0., 0
        beta.rvs(2, 3)#, beta.rvs(2, 3)
        
        sample = beta.rvs(2, 3)
        bandit_1.N += 1
        bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
        position = interpolate(bandit_1.bottom, bandit_1.top, sample)
        bandit_1.line = VGroup(Line(0.26*LEFT, 0.26*RIGHT, color = BLACK, stroke_width = 12), Line(0.22*LEFT, 0.22*RIGHT, color = GREEN)).shift(position)    
        position_graph = np.array([offset_r[0] + 6.5/N, position[1], 0])
        graph = VMobject(stroke_color = GREEN).set_points([position_graph])
        now_node = Dot(color = GREEN_E).move_to(position_graph)
        alpha = ValueTracker(0.0)
        bandit_1.line.add_post_updater(lambda mob: mob.set_stroke(opacity = alpha.get_value()))
        shade = Polygon(0.1*UR, 7*RIGHT + 0.1*UL, 7*RIGHT + 5*UP + 0.1*DL, 5*UP + 0.1*DR, **background_dic).shift(offset_r)
        axes.add_updater(lambda mob: mob.set_stroke(opacity = alpha.get_value())), labels.add_updater(lambda mob: mob.set_fill(opacity = alpha.get_value()))
        #, graph.add_updater(lambda mob: mob.set_stroke(opacity = alpha.get_value())), now_node.add_updater(lambda mob: mob.set_fill(opacity = alpha.get_value())), 
        shade.add_updater(lambda mob: mob.set_fill(opacity = 1 - alpha.get_value()))
        dot = Dot(color = GREEN_E).move_to(position + (random.random()*2-1)*0.2*RIGHT)
        dots = [dot]
        string = f"{sample:.3f}"
        target = bandit_1.digits.generate_target()
        [target[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_sound("sound_0.wav")
        rate_func_1 = lambda t: 1 if t > 1/3 else 0#, squish_rate_func(lambda t: smooth(1-t), 1/3, 1)#, squish_rate_func(smooth, 1/3, 1)
        self.add_lower(dot).add(bandit_1.line, axes, labels, graph, now_node, shade).play(
            bandit_1.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_1.down + bandit_1.offset), 
            bandit_1.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_1.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
            MoveToTarget(bandit_1.digits, rate_func = rate_func_1), 
            ShowDot(dot), 
        )
        self.wait(1)

        def play(sample):
            bandit_1.N += 1
            bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
            position = interpolate(bandit_1.bottom, bandit_1.top, bandit_1.avg)
            bandit_1.line.generate_target().move_to(position)
            position_graph = np.array([offset_r[0] + bandit_1.N*6.5/N, position[1], 0])
            graph.add_line_to(position_graph), now_node.move_to(position_graph)
            dot = Dot(color = GREEN_E).move_to(interpolate(bandit_1.bottom, bandit_1.top, sample) + (random.random()*2-1)*0.2*RIGHT)
            dots.append(dot)
            string = f"{sample:.3f}"
            target = bandit_1.digits.generate_target()
            [target[i].set_digit(int(string[i+2])) for i in range(3)]
            self.add_sound("sound_0.wav")
            self.add_lower(dot).play(
                bandit_1.switch.animating(rate_func = there_and_back, run_time = 2/3).move_to(bandit_1.down + bandit_1.offset), 
                bandit_1.strip_inner.animating(rate_func = there_and_back, run_time = 2/3).light_up(), bandit_1.strip_outer.animating(rate_func = there_and_back, run_time = 2/3).light_up(),
                *[MoveToTarget(mob, rate_func = rate_func_1) for mob in [bandit_1.digits, bandit_1.line]], 
                ShowDot(dot), 
            )

        for _ in range(4):
            sample = beta.rvs(2, 3)
            play(sample)
            self.wait(1)
        self.bring_to_back(alpha.add_updater(lambda mob: mob.increment_value(0.01)))
        for _ in range(2):
            sample = beta.rvs(2, 3)
            play(sample)
            self.wait(1)
        self.remove(alpha, shade)
        for mob in [bandit_1.line, axes, labels]:#, graph, now_node
            mob.clear_updaters()
        for _ in range(2):
            sample = beta.rvs(2, 3)
            play(sample)
            self.wait(1)
        for _ in range(6):
            sample = beta.rvs(2, 3)
            play(sample)
            self.wait(0, 10)
        # print(bandit_1.N) #15

        position_avg = np.array([offset_r[0], interpolate(bandit_1.bottom, bandit_1.top, 0.4)[1], 0])
        line_avg = Line(position_avg, position_avg + 7*RIGHT, color = RED)
        self.add_lower(line_avg).play(ShowCreation(line_avg))
        self.wait()
        self.play(LaggedStart(*[mob.animating(remover = True).scale(0) for mob in dots], lag_ratio = 0.1, run_time = 2, group = VGroup(), remover = True), 
                  *[mob.animating(remover = True).scale(0) for mob in [now_node, bandit_1.line]], 
                  graph.animate.set_stroke(color = GREEN_E, width = 2))
        self.wait()

        graphs = [graph]
        sample = beta.rvs(2, 3)
        bandit_1.avg, bandit_1.N = 0., 0
        bandit_1.N += 1
        bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
        position = interpolate(bandit_1.bottom, bandit_1.top, sample)
        bandit_1.line = VGroup(Line(0.26*LEFT, 0.26*RIGHT, color = BLACK, stroke_width = 12), Line(0.22*LEFT, 0.22*RIGHT, color = BLUE)).move_to(position)
        position_graph = np.array([offset_r[0] + 6.5/N, position[1], 0])
        graph = VMobject(stroke_color = BLUE).set_points([position_graph])
        dot = Dot(color = BLUE_E).move_to(position + (random.random()*2-1)*0.2*RIGHT)
        dots = [dot]
        string = f"{sample:.3f}"
        [bandit_1.digits[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_lower(dot).add(bandit_1.line, graph).wait(0, 3)
        for _ in range(N-1):
            sample = beta.rvs(2, 3)
            bandit_1.N += 1
            bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
            position = interpolate(bandit_1.bottom, bandit_1.top, bandit_1.avg)
            bandit_1.line.move_to(position)
            position_graph = np.array([offset_r[0] + bandit_1.N*6.5/N, position[1], 0])
            graph.add_line_to(position_graph), now_node.move_to(position_graph)
            dot = Dot(color = BLUE_E).move_to(interpolate(bandit_1.bottom, bandit_1.top, sample) + (random.random()*2-1)*0.2*RIGHT)
            dots.append(dot)
            string = f"{sample:.3f}"
            [bandit_1.digits[i].set_digit(int(string[i+2])) for i in range(3)]
            self.add_lower(dot).wait(0, 3)
        self.wait(0, 15)
        self.play(*[mob.animating(remover = True).scale(0) for mob in dots + [bandit_1.line]], graph.animate.set_stroke(color = BLUE_E, width = 2))
        self.wait()

        graphs.append(graph)
        sample = beta.rvs(2, 3)
        bandit_1.avg, bandit_1.N = 0., 0
        bandit_1.N += 1
        bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
        position = interpolate(bandit_1.bottom, bandit_1.top, sample)
        bandit_1.line = VGroup(Line(0.26*LEFT, 0.26*RIGHT, color = BLACK, stroke_width = 12), Line(0.22*LEFT, 0.22*RIGHT, color = PURPLE_B)).move_to(position)
        position_graph = np.array([offset_r[0] + 6.5/N, position[1], 0])
        graph = VMobject(stroke_color = PURPLE_B).set_points([position_graph])
        dot = Dot(color = PURPLE_E).move_to(position + (random.random()*2-1)*0.2*RIGHT)
        dots = [dot]
        string = f"{sample:.3f}"
        [bandit_1.digits[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_lower(dot).add(bandit_1.line, graph).wait(0, 2)
        for _ in range(N-1):
            sample = beta.rvs(2, 3)
            bandit_1.N += 1
            bandit_1.avg = interpolate(bandit_1.avg, sample, 1/bandit_1.N)
            position = interpolate(bandit_1.bottom, bandit_1.top, bandit_1.avg)
            bandit_1.line.move_to(position)
            position_graph = np.array([offset_r[0] + bandit_1.N*6.5/N, position[1], 0])
            graph.add_line_to(position_graph), now_node.move_to(position_graph)
            dot = Dot(color = PURPLE_E).move_to(interpolate(bandit_1.bottom, bandit_1.top, sample) + (random.random()*2-1)*0.2*RIGHT)
            dots.append(dot)
            string = f"{sample:.3f}"
            [bandit_1.digits[i].set_digit(int(string[i+2])) for i in range(3)]
            self.add_lower(dot).wait(0, 2)
        self.wait(0, 30)
        self.remove(*dots, bandit_1.line), graph.set_stroke(color = PURPLE_E, width = 2)
        graphs.append(graph)

        color_light, color_dark = [RED, RED_E]
        samples, avgs = np.zeros(N), np.zeros(N)
        bandit_1.avg = 0.
        for i in range(N):
            sample = beta.rvs(2, 3)
            samples[i] = sample
            bandit_1.avg = interpolate(bandit_1.avg, sample, 1/(i+1))
            avgs[i] = bandit_1.avg
        positions = [interpolate(bandit_1.bottom, bandit_1.top, sample) + (random.random()*2-1)*0.2*RIGHT for sample in samples]
        positions_graph = [np.array([offset_r[0] + (i+1)*6.5/N, interpolate(bandit_1.bottom, bandit_1.top, avgs[i])[1], 0]) for i in range(N)]
        graph = Polyline(*positions_graph, stroke_color = color_light)
        dots = [Dot(position, color = color_dark) for position in positions]
        string = f"{samples[-1]:.3f}"
        [bandit_1.digits[i].set_digit(int(string[i+2])) for i in range(3)]
        self.add_lower(*dots).add(graph).wait(1)
        self.remove(*dots), graph.set_stroke(color = color_dark, width = 2)
        graphs.append(graph)

        def resample(color_light, color_dark, wait_time = 1, remove = True):
            samples, avgs = np.zeros(N), np.zeros(N)
            bandit_1.avg = 0.
            for i in range(N):
                sample = beta.rvs(2, 3)
                samples[i] = sample
                bandit_1.avg = interpolate(bandit_1.avg, sample, 1/(i+1))
                avgs[i] = bandit_1.avg
            positions = [interpolate(bandit_1.bottom, bandit_1.top, sample) + (random.random()*2-1)*0.2*RIGHT for sample in samples]
            positions_graph = [np.array([offset_r[0] + (i+1)*6.5/N, interpolate(bandit_1.bottom, bandit_1.top, avgs[i])[1], 0]) for i in range(N)]
            graph = Polyline(*positions_graph, stroke_color = color_light)
            dots = [Dot(position, color = color_dark) for position in positions]
            string = f"{samples[-1]:.3f}"
            [bandit_1.digits[i].set_digit(int(string[i+2])) for i in range(3)]
            self.add_lower(*dots).add(graph).wait(wait_time)
            if remove:
                self.remove(*dots), graph.set_stroke(color = color_dark, width = 2)
            graphs.append(graph)
            if not remove:
                graphs.extend(dots)

        resample(TEAL, TEAL_E)
        resample(YELLOW, YELLOW_E)
        resample(MAROON, MAROON_E)
        resample(LIGHT_BROWN, DARK_BROWN)
        resample(LIGHT_PINK, PINK)
        resample(GREEN, GREEN_E, wait_time = 0), resample(TEAL, TEAL_E)
        resample(BLUE, BLUE_E, wait_time = 0), resample(PURPLE_B, PURPLE_E, wait_time = 0), resample(RED, RED_E)
        ORANGE_E, LIME_E = interpolate_color(ORANGE, BLACK, 0.5), interpolate_color(LIME, BLACK, 0.5)
        resample(ORANGE, ORANGE_E, wait_time = 0), resample(YELLOW, YELLOW_E, wait_time = 0), resample(GOLD, GOLD_E, wait_time = 0), resample(LIME, LIME_E)
        resample(GREEN, GREEN_E, wait_time = 0), resample(TEAL, TEAL_E, wait_time = 0), resample(BLUE, BLUE_E, wait_time = 0), resample(PURPLE_B, PURPLE_E, wait_time = 0), resample(RED, RED_E, remove = False)
        
        function_graph_p = FunctionGraph(lambda x: 1.5/np.sqrt(x), [6.5/N, 6.5, 6.5/N]).shift(position_avg)
        function_graph_m = FunctionGraph(lambda x: -1.5/np.sqrt(x), [6.5/N, 6.5, 6.5/N]).shift(position_avg)
        shade_p = function_graph_p.copy().set_stroke(width = 12, color = BLACK)
        shade_m = function_graph_m.copy().set_stroke(width = 12, color = BLACK)
        self.play(*[ShowCreation(mob) for mob in [shade_p, shade_m, function_graph_p, function_graph_m]])
        self.wait()

        tex = MTex(r"\Delta \mu=\frac{c}{\sqrt n}", tex_to_color_map = {r"\mu": GREEN, r"n": YELLOW, r"c": RED}).shift(4*RIGHT + 2*UP)
        self.play(Write(tex))
        self.wait()

        region = VMobject(stroke_width = 0, fill_opacity = 0.5, fill_color = BLUE).match_points(function_graph_p).reverse_points(
                ).add_line_to(function_graph_m.get_points()[0]).append_points(function_graph_m.get_points()).close_path()
        self.add_lower(region, line_avg).play(FadeIn(region, run_time = 2, rate_func = blink(5)))
        self.wait()
        self.play(*[FadeOut(mob) for mob in graphs])
        self.wait()

class Video_4_2(FrameScene):
    def construct(self):
        def dic_gen(color_0, color_1):
            switch_dic = {"height": 1, "width": 0.4, "space": 1, "surr": 0.1, "radius": 0.25, "colors": [color_0, interpolate_color(color_0, BLACK, 0.5)]}
            digit_dic = {"length": 0.6, "width": 0.2, "buff": 0.04, "colors": [color_0, GREY_E]}
            slot_dic = {"height": 3, "buff": 0.2, "color": GREY_E, "offset": 2*UP}
            digits_dic = {"buff": 0.2, "colors_0": [color_0, interpolate_color(color_0, BLACK, 0.8)], "colors_1": [color_1, interpolate_color(color_1, BLACK, 0.8)], "offset": 1.5*DOWN}
            return {"switch_dic": switch_dic, "digit_dic": digit_dic, "slot_dic": slot_dic, "digits_dic": digits_dic}
        bandit_1 = Bandit(**dic_gen(YELLOW, WHITE)).shift(4.5*LEFT)
        interval = Rectangle(height = 4, width = 0.8, stroke_width = 0, fill_opacity = 1, fill_color = BLACK).shift(ORIGIN)
        interval_surr = Rectangle(height = 4, width = 0.8).shift(RIGHT)
        inf, sup = MTex(r"0", color = YELLOW).next_to(interval, DOWN), MTex(r"10", color = YELLOW).next_to(interval, UP)
        up, down = interval.get_top(), interval.get_bottom()
        text_avg = Songti("平均值：").scale(0.8).shift(3.5*RIGHT + UP)
        text_con = Songti("乐观加分：").scale(0.8).shift(3.5*RIGHT + DOWN).match_x(text_avg, RIGHT)
        mu = Line(color = RED).shift(interpolate(down, up, 0.4))    
        self.add_lower(mu, interval).add(interval_surr, bandit_1, text_avg, text_con, inf, sup).wait()

        digits = [MTex(str(i), color = GREEN)[0] for i in range(10)]
        template = MTex(r"0.00", color = GREEN)

        avg = 0
        tex_avg, tex_con = template.copy().next_to(text_avg, RIGHT), template.copy().next_to(text_con, RIGHT).set_color(BLUE)
        line = VGroup(Line(0.36*LEFT, 0.36*RIGHT, color = BLACK, stroke_width = 12), Line(0.3*LEFT, 0.3*RIGHT, color = GREEN))
        rect = Rectangle(height = 4*0.6, width = 0.8, fill_opacity = 0.5, fill_color = BLUE, stroke_width = 0).shift(3.5*RIGHT + DOWN)
        self.add_lower(rect).add(line, tex_avg, tex_con)
        for i in range(30):
            sample = beta.rvs(2, 3)
            string = f"{sample:.3f}"
            for k, digit in enumerate(bandit_1.digits):
                digit.set_digit(int(string[k+2]))

            avg = interpolate(avg, sample, 1/(i+1))
            string = f"{avg:.3f}"
            new_tex = template.copy()
            [new_tex[i].become(digits[int(string[j])]).move_to(template[i]) for i, j in [(0,2), (2,3), (3,4)]]
            tex_avg.become(new_tex).next_to(text_avg, RIGHT)
            line.move_to(interpolate(down, up, avg))
            
            con = 0.6/np.sqrt(i+1)
            string = f"{con*5:.3f}"
            new_tex = template.copy()
            [new_tex[i].become(digits[int(string[i])]).move_to(template[i]) for i in [0, 2, 3]]
            tex_con.become(new_tex).next_to(text_con, RIGHT).set_color(BLUE)
            rect.set_height(4*con, stretch = True).move_to(interpolate(down, up, avg))

            dot = Dot(color = GREEN_E).move_to(interpolate(down, up, sample) + (random.random()*2-1)*0.3*RIGHT)
            self.add_lower(dot).wait(1)

        self.wait()

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        