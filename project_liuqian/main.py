from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class CardBack(ImageMobject):
    def __init__(self, **kwargs):
        super().__init__("2B.svg", **kwargs)

class Test1(FrameScene):
    def construct(self):
        mob = CardBack(fill_opacity = 1)
        self.add(mob[1])

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        step_1 = Songti("四张牌洗混\n对折撕成两半").scale(0.6)
        step_1.add(SurroundingRectangle(step_1)).move_to(RIGHT + 3*UP)
        step_2 = Songti("按自己名字字数\n每个字搬一张牌").scale(0.6)
        step_2.add(SurroundingRectangle(step_2)).move_to(RIGHT + 1.2*UP)
        step_3 = Songti("将最上方3张牌\n任意插入牌堆").scale(0.6)
        step_3.add(SurroundingRectangle(step_3)).move_to(RIGHT + 0.6*DOWN)
        step_4 = Songti("拿起最上面的牌\n收好").scale(0.6)
        step_4.add(SurroundingRectangle(step_4)).move_to(RIGHT + 2.4*DOWN)
        step_5 = Songti("根据南北方选择数量\n将最上方的牌插入牌堆").scale(0.6)
        step_5.add(SurroundingRectangle(step_5)).move_to(5*RIGHT + 2.4*DOWN)
        step_6 = Songti("根据性别选择数量\n将最上方的牌丢掉").scale(0.6)
        step_6.add(SurroundingRectangle(step_6)).move_to(5*RIGHT + 0.6*DOWN)
        step_7 = Songti("根据7字真言\n每个字搬一张牌").scale(0.6)
        step_7.add(SurroundingRectangle(step_7)).move_to(5*RIGHT + 1.2*UP)
        step_8 = Songti("好运留下来（搬牌）\n烦恼丢出去（丢牌）").scale(0.6)
        step_8.add(SurroundingRectangle(step_8)).move_to(5*RIGHT + 3*UP)
        steps = [step_1, step_2, step_3, step_4, step_5, step_6, step_7, step_8]
        arrows = [Arrow(steps[i], steps[i+1], color = GREY, buff = 0.1) for i in range(7)]
        self.play(GrowFromCenter(step_1))
        self.wait()
        self.play(GrowArrow(arrows[0]), rate_func = rush_into)
        self.play(GrowFromEdge(step_2, UP))
        self.wait()
        self.play(GrowArrow(arrows[1]), rate_func = rush_into)
        self.play(GrowFromEdge(step_3, UP))
        self.wait()
        self.play(GrowArrow(arrows[2]), rate_func = rush_into)
        self.play(GrowFromEdge(step_4, UP))
        self.wait()
        self.play(GrowArrow(arrows[3]), rate_func = rush_into)
        self.play(GrowFromEdge(step_5, LEFT))
        self.wait()
        self.play(GrowArrow(arrows[4]), rate_func = rush_into)
        self.play(GrowFromEdge(step_6, DOWN))
        self.wait()
        self.play(GrowArrow(arrows[5]), rate_func = rush_into)
        self.play(GrowFromEdge(step_7, DOWN))
        self.wait()
        self.play(GrowArrow(arrows[6]), rate_func = rush_into)
        self.play(GrowFromEdge(step_8, DOWN))
        self.wait()

        arrow = Arrow(ORIGIN, 0.8*DL, color = GOLD, stroke_width = 8).next_to(step_4, UR, buff = 0.1)
        self.play(FadeIn(arrow, 0.3*DL))
        self.wait()
    
class Cut(Animation):
    def __init__(self, position: np.ndarray = ORIGIN, length: float = 4, line_color = YELLOW, offset = 0, **kwargs):
        width = [length*4/2500*i*(100-i) for i in range(50)]
        mobject = Line(position + length/2*LEFT, position + length/2*RIGHT, stroke_width = width + width[::-1], color = line_color).insert_n_curves(99)
        self.offset = offset
        super().__init__(mobject, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        start, end = starting_submobject.get_start(), starting_submobject.get_end()
        head, tail = interpolate(start, end, fore(alpha)), interpolate(start, end, back(alpha))
        submobject.become(starting_submobject).put_start_and_end_on(head, tail).shift(self.offset*(0.5-alpha)*RIGHT)

class Video_2(FrameScene):
    def construct(self):
        cards = [ImageMobject("AH.png", height = 3).shift(4.5*LEFT), ImageMobject("3S.png", height = 3).shift(1.5*LEFT), 
                 ImageMobject("8D.png", height = 3).shift(1.5*RIGHT), ImageMobject("KC.png", height = 3).shift(4.5*RIGHT), ]
        n_backs = ["back_r.png", "back_y.png", "back_g.png", "back_b.png"]
        n_halves = ["half_r.png", "half_b.png", "half_g.png", "half_y.png"]
        targets = [ImageMobject(n_backs[i], height = 3).shift((i-1.5)*3*RIGHT) for i in range(4)]
        self.add(*cards).wait()
        self.play(*[cards[i].animating(delay = 1/3*i, remover = True, run_time = 1/2, rate_func = rush_into).scale(np.array([0, 1, 1])) for i in range(4)], 
                  *[targets[i].save_state().scale(np.array([0, 1, 1])).animating(delay = 1/3*i + 1/2, run_time = 1/2, rate_func = rush_from).restore() for i in range(4)], )
        self.wait()

        self.add(*targets[::-1]).play(*[mob.animate.center() for mob in targets])
        self.wait()
        halves = [ImageMobject(n_halves[0], height = 1.5).shift(0.75*UP), ImageMobject(n_halves[1], height = 1.5).shift(0.75*UP), 
                 ImageMobject(n_halves[2], height = 1.5).shift(0.75*UP), ImageMobject(n_halves[3], height = 1.5).shift(0.75*UP), 
                 ImageMobject(n_halves[0], height = 1.5).shift(0.75*DOWN), ImageMobject(n_halves[1], height = 1.5).shift(0.75*DOWN), 
                 ImageMobject(n_halves[2], height = 1.5).shift(0.75*DOWN), ImageMobject(n_halves[3], height = 1.5).shift(0.75*DOWN)]
        self.remove(*targets).add(*halves[::-1])
        def anchor(mob: VMobject):
            mob.restore()
            mob.move_to(mob.position.get_location())
            mob.rotate(mob.angle.get_value())
        for i in range(8):
            layer, position = i//4, (i%4 - 1.5) * 0.25*RIGHT
            halves[i].position = Point(halves[i].get_center())
            halves[i].angle = ValueTracker(layer * PI)
            halves[i].save_state().add_updater(anchor)
            halves[i].position.generate_target().shift(position)
        self.play(*[MoveToTarget(mob.position) for mob in halves])
        self.wait()
        self.play(Cut(ORIGIN, length = 5, line_color = BLACK, offset = 1), Cut(ORIGIN), *[mob.position.animating(delay = 0.5).shift(0.5*UP) for mob in halves[:4]], *[mob.position.animating(delay = 0.5).shift(0.5*DOWN) for mob in halves[4:]])
        self.wait()
        self.play(*[halves[i].angle.animating(delay = i/7).set_value(PI/6) for i in range(8)], 
                  *[halves[i].position.animating(delay = i/7).move_to(0.5*UP + (i-3.5)*0.5*RIGHT) for i in range(8)])
        for mob in halves:
            mob.clear_updaters()
        self.wait()

        colors = [RED, BLUE, GREEN, GOLD]
        squares = [Square(side_length = 0.8, **background_dic, color = colors[i]).shift(1.5*DOWN + (i-1.5)*RIGHT) for i in range(4)]
        self.play(*[FadeIn(mob, 0.5*UP) for mob in squares])
        self.wait()
        def sort_updater(scene):
            scene.mobjects.sort(key = lambda mob: mob.get_x(), reverse = True)
        self.updaters = [sort_updater]
        self.play(halves[0].animating(path_arc = -PI).move_to(0.5*UP + 3.5*0.5*RIGHT), 
                  *[halves[i+1].animate.move_to(0.5*UP + (i-3.5)*0.5*RIGHT) for i in range(7)], 
                  squares[0].animating(path_arc = PI/2).move_to(1.5*DOWN + 1.5*RIGHT), 
                  *[squares[i+1].animate.move_to(1.5*DOWN + (i-1.5)*RIGHT) for i in range(3)], )
        halves.sort(key = lambda mob: mob.get_x()), squares.sort(key = lambda mob: mob.get_x())
        self.wait()
        self.play(halves[0].animating(path_arc = -PI).move_to(0.5*UP + 3.5*0.5*RIGHT), 
                  *[halves[i+1].animate.move_to(0.5*UP + (i-3.5)*0.5*RIGHT) for i in range(7)], 
                  squares[0].animating(path_arc = PI/2).move_to(1.5*DOWN + 1.5*RIGHT), 
                  *[squares[i+1].animate.move_to(1.5*DOWN + (i-1.5)*RIGHT) for i in range(3)], )
        halves.sort(key = lambda mob: mob.get_x()), squares.sort(key = lambda mob: mob.get_x())
        self.wait()

        surr = SurroundingRectangle(squares[-1], buff = 0.1)
        self.play(halves[3].animate.shift(0.2*UP + 0.1*LEFT), halves[7].animate.shift(0.2*UP + 0.1*LEFT), ShowCreation(surr))
        self.wait()
        self.play(halves[3].animate.shift(0.2*DOWN + 0.1*RIGHT), halves[7].animate.shift(0.2*DOWN + 0.1*RIGHT))
        self.wait()

        self.play(*[halves[i].animate.shift(1.5*UP) for i in range(3)])
        self.play(*[halves[i].animate.shift(1*RIGHT) for i in range(3)], *[halves[i].animate.shift(1.5*LEFT) for i in [3, 4]])
        self.play(*[halves[i].animate.shift(1.5*DOWN) for i in range(3)])
        halves.sort(key = lambda mob: mob.get_x())
        self.wait()

        self.play(halves[0].animate.move_to(4*LEFT + 2*UP), *[halves[i].animate.shift(0.25*LEFT) for i in range(1, 7)], 
                  halves[7].animate.shift(0.25*RIGHT))
        self.wait()

        halves.remove(halves[0])
        self.play(*[halves[i].animate.shift(1.5*UP) for i in range(3)])
        self.play(*[halves[i].animate.shift(0.5*RIGHT) for i in range(3)], *[halves[i].animate.shift(1.5*LEFT) for i in [3]])
        self.play(*[halves[i].animate.shift(1.5*DOWN) for i in range(3)])
        halves.sort(key = lambda mob: mob.get_x())
        self.wait()

        def falling_updater(mob: VMobject, dt):
            mob.v += dt
            mob.shift(mob.v*0.5*DOWN).rotate(-2*dt)
        halves[0].v = 0
        halves[0].add_updater(falling_updater)
        self.wait(5)
        self.remove(halves[0])
        indicate = SurroundingRectangle(halves[-1].copy().rotate(-PI/6)).rotate(PI/6)
        self.bring_to_back(indicate).play(FadeIn(indicate, rate_func = double_there_and_back, remover = True, run_time = 2))
        self.wait()

        halves.remove(halves[0])
        halves.sort(key = lambda mob: mob.get_x())
        self.play(*[halves[i].animate.move_to(0.5*UP + (i-2.5)*0.5*RIGHT) for i in range(6)], *[mob.animate.shift(0.5*DOWN) for mob in squares + [surr]])
        self.wait()

        text = Heiti("见证奇迹的时刻", color = YELLOW)
        for mob in text:
            mob.scale(2).move_to(4*RIGHT + 0.5*UP)
        for i in range(7):
            self.play(halves[0].animating(path_arc = -PI).move_to(0.5*UP + 2.5*0.5*RIGHT), 
                  *[halves[i+1].animate.move_to(0.5*UP + (i-2.5)*0.5*RIGHT) for i in range(5)], 
                  FadeIn(text[i], rate_func = there_and_back_with_pause(), remover = True))
            halves.sort(key = lambda mob: mob.get_x())
        self.wait()
        keep, kill = Heiti("好运留下来", color = RED).shift(4.5*RIGHT + UP).save_state(), Heiti("烦恼丢出去", color = GREY).shift(4.5*RIGHT).save_state(),
        for i in range(5):
            j = len(halves)
            self.play(halves[0].animating(path_arc = -PI).move_to(0.5*UP + 2.5*0.5*RIGHT), 
                  *[halves[i+1].animate.move_to(0.5*UP + (i-j+3.5)*0.5*RIGHT) for i in range(j-1)], 
                  FadeIn(keep.restore(), rate_func = there_and_back_with_pause(), remover = True))
            halves.sort(key = lambda mob: mob.get_x())
            halves[0].v = 0
            halves[0].add_updater(falling_updater)
            self.play(FadeIn(kill.restore(), rate_func = there_and_back_with_pause(), remover = True))
            self.remove(halves[0]), halves.remove(halves[0])
        self.wait()

#################################################################### 

class Video_3(FrameScene):
    def construct(self):
        shade_l, shade_r = self.shade.copy().next_to(6*RIGHT, LEFT, buff = 0).set_opacity(0), self.shade.copy().next_to(6*RIGHT, RIGHT, buff = 0)
        n = 5
        halves_5 = [ImageMobject("half_n.png", height = 1) for _ in range(n-1)] + [ImageMobject("half_b.png", height = 1)]
        func_5 = lambda t: 0.5*DOWN + 3*LEFT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_5[i].rotate(PI/6).move_to(func_5(i))
        copy_5 = [mob.copy().set_y(2.5) for mob in halves_5]
        n = 6
        halves_6 = [ImageMobject("half_n.png", height = 1) for _ in range(n-1)] + [ImageMobject("half_b.png", height = 1)]
        func_6 = lambda t: 0.5*DOWN + 3*RIGHT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_6[i].rotate(PI/6).move_to(func_6(i))
        copy_6 = [mob.copy().set_y(2.5) for mob in halves_6]
        def sort_updater(scene):
            scene.mobjects.sort(key = lambda mob: mob.get_x(), reverse = True)
            scene.add(shade_l, shade_r)
        self.updaters = [sort_updater]
        self.add(*copy_5, *copy_6, *halves_5[::-1], *halves_6[::-1]).wait()
        text = Heiti("见证奇迹的时刻", color = YELLOW)
        for mob in text:
            mob.scale(2).move_to(1*UP)
        for i in range(7):
            self.play(halves_5[0].animating(path_arc = -PI).move_to(func_5(4)), 
                  *[halves_5[i+1].animate.move_to(func_5(i)) for i in range(4)], 
                  halves_6[0].animating(path_arc = -PI).move_to(func_6(5)), 
                  *[halves_6[i+1].animate.move_to(func_6(i)) for i in range(5)], 
                  FadeIn(text[i], rate_func = there_and_back_with_pause(), remover = True))
            halves_5.sort(key = lambda mob: mob.get_x()), halves_6.sort(key = lambda mob: mob.get_x())
        result_5 = [mob.copy() for mob in halves_5]
        result_6 = [mob.copy() for mob in halves_6]
        self.add(*result_5, *result_6).play(*[mob.animate.shift(1.2*UP) for mob in halves_5 + halves_6], 
                                            *[mob.animate.shift(1.8*DOWN) for mob in result_5 + result_6], )
        keep, kill = Heiti("好运留下来", color = RED).shift(0.8*DOWN).save_state(), Heiti("烦恼丢出去", color = GREY).shift(0.8*DOWN).save_state(),
        def falling_updater(mob: VMobject, dt):
            mob.v += dt
            mob.shift(mob.v*(0.5*DOWN + 0.1*LEFT)).rotate(-2*dt)
        for i in range(4):
            j_5, j_6 = len(result_5), len(result_6)
            self.play(result_5[0].animating(path_arc = -PI).move_to(func_5(4) + 1.8*DOWN), 
                  *[result_5[i+1].animate.move_to(func_5(5-j_5+i) + 1.8*DOWN) for i in range(j_5-1)], 
                  result_6[0].animating(path_arc = -PI).move_to(func_6(5) + 1.8*DOWN), 
                  *[result_6[i+1].animate.move_to(func_6(6-j_6+i) + 1.8*DOWN) for i in range(j_6-1)], 
                  FadeIn(keep.restore(), rate_func = there_and_back_with_pause(), remover = True))
            result_5.sort(key = lambda mob: mob.get_x()), result_6.sort(key = lambda mob: mob.get_x())
            result_5[0].v, result_6[0].v = 0, 0
            result_5[0].add_updater(falling_updater), result_6[0].add_updater(falling_updater)
            self.play(FadeIn(kill.restore(), rate_func = there_and_back_with_pause(), remover = True))
            self.remove(result_5[0], result_6[0]), result_5.remove(result_5[0]), result_6.remove(result_6[0])
        j_6 = len(result_6)
        self.play(result_6[0].animating(path_arc = -PI).move_to(func_6(5) + 1.8*DOWN), 
                *[result_6[i+1].animate.move_to(func_6(6-j_6+i) + 1.8*DOWN) for i in range(j_6-1)], 
                FadeIn(keep.restore(), rate_func = there_and_back_with_pause(), remover = True))
        result_6.sort(key = lambda mob: mob.get_x())
        result_6[0].v = 0
        result_6[0].add_updater(falling_updater)
        self.play(FadeIn(kill.restore(), rate_func = there_and_back_with_pause(), remover = True))
        self.remove(result_6[0]), result_6.remove(result_6[0])
        self.wait()
        
        n = 7
        halves_7 = [ImageMobject("half_n.png", height = 1) for _ in range(n-1)] + [ImageMobject("half_b.png", height = 1)]
        func_7 = lambda t: 2.3*DOWN + 9*RIGHT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_7[i].rotate(PI/6).move_to(func_7(i)).set_y(0.7)
        copy_7 = [mob.copy().set_y(2.5) for mob in halves_7]
        result_7 = [mob.copy().set_y(-2.3) for mob in halves_7]
        n = 8
        halves_8 = [ImageMobject("half_b.png", height = 1)] + [ImageMobject("half_n.png", height = 1) for _ in range(n-1)]
        func_8 = lambda t: 2.3*DOWN + 15*RIGHT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_8[i].rotate(PI/6).move_to(func_8(i)).set_y(0.7)
        copy_8 = [mob.copy().set_y(2.5) for mob in halves_8]
        result_8 = [mob.copy().set_y(-2.3) for mob in halves_8]
        self.add(*copy_7, *copy_8, *halves_7, *halves_8, *result_7, *result_8)
        time = self.time
        shade_l.add_updater(lambda mob: mob.set_opacity(smooth((self.time - time)/3))).unfix_from_frame()
        shade_r.add_updater(lambda mob: mob.set_opacity(1-smooth((self.time - time)/3))).unfix_from_frame()
        self.camera.frame.add_updater(lambda mob: mob.move_to(smooth((self.time - time)/3)*12*RIGHT))
        for i in range(3):
            waste_7, waste_8 = result_7[1], result_8[1]
            result_7.remove(waste_7), result_8.remove(waste_8)
            waste_7.v, waste_8.v = 0, 0
            waste_7.add_updater(falling_updater), waste_8.add_updater(falling_updater)
            j_7, j_8 = len(result_7), len(result_8)
            self.play(result_7[0].animating(path_arc = -PI).move_to(func_7(6)), 
                  *[result_7[i+1].animate.move_to(func_7(7-j_7+i)) for i in range(j_7-1)], 
                  result_8[0].animating(path_arc = -PI).move_to(func_8(7)), 
                  *[result_8[i+1].animate.move_to(func_8(8-j_8+i)) for i in range(j_8-1)], 
                  )
            result_7.sort(key = lambda mob: mob.get_x()), result_8.sort(key = lambda mob: mob.get_x())
            self.remove(waste_7, waste_8)
        for mob in [shade_l, shade_r, self.camera.frame]:
            mob.clear_updaters()
        for i in range(3):
            waste_7, waste_8 = result_7[1], result_8[1]
            result_7.remove(waste_7), result_8.remove(waste_8)
            waste_7.v, waste_8.v = 0, 0
            waste_7.add_updater(falling_updater), waste_8.add_updater(falling_updater)
            j_7, j_8 = len(result_7), len(result_8)
            self.play(result_7[0].animating(path_arc = -PI).move_to(func_7(6)), 
                  *[result_7[i+1].animate.move_to(func_7(7-j_7+i)) for i in range(j_7-1)], 
                  result_8[0].animating(path_arc = -PI).move_to(func_8(7)), 
                  *[result_8[i+1].animate.move_to(func_8(8-j_8+i)) for i in range(j_8-1)], 
                  )
            result_7.sort(key = lambda mob: mob.get_x()), result_8.sort(key = lambda mob: mob.get_x())
            self.remove(waste_7, waste_8)
        waste_8 = result_8[1]
        result_8.remove(waste_8)
        waste_8.v = 0
        waste_8.add_updater(falling_updater)
        j_8 = len(result_8)
        self.play(result_8[0].animating(path_arc = -PI).move_to(func_8(7)), 
                *[result_8[i+1].animate.move_to(func_8(8-j_8+i)) for i in range(j_8-1)], 
                )
        result_8.sort(key = lambda mob: mob.get_x())
        self.remove(waste_8)
        self.wait()

class Video_4(FrameScene):
    def construct(self):
        n_halves = ["half_n.png", "half_b.png"]
        n = 6
        halves_6 = [ImageMobject(n_halves[i == 5], height = 1) for i in range(n)]
        func_6 = lambda t: 0.5*DOWN + 3*LEFT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_6[i].rotate(PI/6).move_to(func_6(i))
        copy_6 = [mob.copy().set_y(2.5) for mob in halves_6]
        n = 7
        halves_7 = [ImageMobject(n_halves[i == 6], height = 1) for i in range(n)]
        func_7 = lambda t: 2.3*DOWN + 3*RIGHT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_7[i].rotate(PI/6).move_to(func_7(i)).set_y(0.7)
        copy_7 = [mob.copy().set_y(2.5) for mob in halves_7]
        result_7 = [mob.copy().set_y(-2.3) for mob in halves_7]
        def sort_updater(scene):
            scene.mobjects.sort(key = lambda mob: mob.get_x(), reverse = True)
        self.updaters = [sort_updater]
        self.add(*copy_6, *copy_7, *halves_6, *halves_7, *result_7).wait()
        
        text = Heiti("见证奇迹的时刻", color = YELLOW)
        for mob in text:
            mob.scale(2).move_to(2.3*DOWN + 4*LEFT)
        def falling_updater(mob: VMobject, dt):
            mob.v += dt
            mob.shift(mob.v*(0.5*DOWN + 0.1*LEFT)).rotate(-2*dt)
        waste_7 = result_7[1]
        result_7.remove(waste_7)
        waste_7.v = 0
        waste_7.add_updater(falling_updater)
        j_7 = len(result_7)
        self.play(halves_6[0].animating(path_arc = -PI).move_to(func_6(5)), 
                *[halves_6[i+1].animate.move_to(func_6(i)) for i in range(5)], 
                result_7[0].animating(path_arc = -PI).move_to(func_7(6)), 
                *[result_7[i+1].animate.move_to(func_7(7-j_7+i)) for i in range(j_7-1)], 
                FadeIn(text[0], rate_func = there_and_back_with_pause(), remover = True))
        self.remove(waste_7)
        halves_6.sort(key = lambda mob: mob.get_x())
        for i in range(1, 7):
            self.play(halves_6[0].animating(path_arc = -PI).move_to(func_6(5)), 
                  *[halves_6[i+1].animate.move_to(func_6(i)) for i in range(5)], 
                  FadeIn(text[i], rate_func = there_and_back_with_pause(), remover = True))
            halves_6.sort(key = lambda mob: mob.get_x())
        self.wait()
        self.play(IndicateAround(Group(*halves_6)), IndicateAround(Group(*result_7)))

        result_6 = [mob.copy() for mob in halves_6]
        n = 5
        halves_5 = [ImageMobject(n_halves[i == 4], height = 1) for i in range(n)]
        func_5 = lambda t: 0.5*DOWN + 9*LEFT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_5[i].rotate(PI/6).move_to(func_5(i))
        copy_5 = [mob.copy().set_y(2.5) for mob in halves_5]
        self.play(*[OverFadeIn(mob, run_time = 2) for mob in halves_5 + copy_5], *[OverFadeOut(mob, run_time = 2) for mob in halves_7 + copy_7 + result_7], 
                  self.camera.frame.animating(run_time = 2).shift(6*LEFT), *[mob.animate.shift(1.2*UP) for mob in halves_6], *[mob.animate.shift(1.8*DOWN) for mob in result_6])
        self.wait()

        text = Heiti("见证奇迹的时刻", color = YELLOW)
        for mob in text:
            mob.scale(2).move_to(2.3*DOWN + 10*LEFT)
        waste_6 = result_6[1]
        result_6.remove(waste_6)
        waste_6.v = 0
        waste_6.add_updater(falling_updater)
        j_6 = len(result_6)
        self.play(halves_5[0].animating(path_arc = -PI).move_to(func_5(4)), 
                *[halves_5[i+1].animate.move_to(func_5(i)) for i in range(4)], 
                result_6[0].animating(path_arc = -PI).move_to(func_6(5) + 1.8*DOWN), 
                *[result_6[i+1].animate.move_to(func_6(6-j_6+i) + 1.8*DOWN) for i in range(j_6-1)], 
                FadeIn(text[0], rate_func = there_and_back_with_pause(), remover = True))
        self.remove(waste_6)
        halves_5.sort(key = lambda mob: mob.get_x())
        for i in range(1, 7):
            self.play(halves_5[0].animating(path_arc = -PI).move_to(func_5(4)), 
                  *[halves_5[i+1].animate.move_to(func_5(i)) for i in range(4)], 
                  FadeIn(text[i], rate_func = there_and_back_with_pause(), remover = True))
            halves_5.sort(key = lambda mob: mob.get_x())
        self.wait()
        self.play(IndicateAround(Group(*halves_5), rect_kwargs = {"if_fixed_in_frame": False}), IndicateAround(Group(*result_6), rect_kwargs = {"if_fixed_in_frame": False}))

        result_5 = [mob.copy() for mob in halves_5]
        n = 4
        halves_4 = [ImageMobject(n_halves[i == 0], height = 1) for i in range(n)]
        copy_4 = [ImageMobject(n_halves[i == 3], height = 1) for i in range(n)]
        func_4 = lambda t: 0.5*DOWN + 15*LEFT + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_4[i].rotate(PI/6).move_to(func_4(i))
            copy_4[i].rotate(PI/6).move_to(func_4(i)).set_y(2.5)
        self.play(*[OverFadeIn(mob, run_time = 2) for mob in copy_4], *[OverFadeOut(mob, run_time = 2) for mob in halves_6 + copy_6 + result_6], 
                  self.camera.frame.animating(run_time = 2).shift(6*LEFT), *[mob.animate.shift(1.2*UP) for mob in halves_5], *[mob.animate.shift(1.8*DOWN) for mob in result_5])
        self.wait()

        waste_5 = result_5[1]
        result_5.remove(waste_5)
        waste_5.v = 0
        waste_5.add_updater(falling_updater)
        j_5 = len(result_5)
        self.play(result_5[0].animating(path_arc = -PI).move_to(func_5(4) + 1.8*DOWN), 
                *[result_5[i+1].animate.move_to(func_5(5-j_5+i) + 1.8*DOWN) for i in range(j_5-1)], )
        result_5.sort(key = lambda mob: mob.get_x())
        self.remove(waste_5)
        self.wait()
        self.play(*[TransformFromCopy(result_5[i], halves_4[i]) for i in range(4)])
        self.wait()
        self.play(*[OverFadeOut(mob, run_time = 2) for mob in halves_5 + copy_5 + result_5], 
                  self.camera.frame.animating(run_time = 2).shift(3*LEFT), *[FadeOut(mob) for mob in copy_4], 
                  *[TransformFromCopy(mob, mob.copy().set_y(2.5).shift(4*LEFT), path_arc = PI/2, run_time = 2) for mob in halves_4])
        self.wait()

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

class Video_5(FrameScene):
    def construct(self):
        n_halves = ["half_n.png", "half_b.png"]
        n = 4
        halves_4 = [ImageMobject(n_halves[i == 0], height = 1) for i in range(n)]
        func_4 = lambda t: 0.5*DOWN + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_4[i].rotate(PI/6).move_to(func_4(i))
        copy_4 = [mob.copy().set_y(2.5).shift(4*LEFT) for mob in halves_4]
        def sort_updater(scene):
            scene.mobjects.sort(key = lambda mob: mob.get_x(), reverse = True)
        self.updaters = [sort_updater]
        self.add(*copy_4, *halves_4).wait()

        labels = [MTex(str(i+1), color = WHITE if i else BLUE).set_stroke(**stroke_dic) for i in range(4)]
        for i in range(4):
            labels[i].reference = halves_4[i]
            labels[i].next_to(labels[i].reference, UP).shift(0.3*RIGHT)
        self.play(Write(VGroup(*labels)))
        self.wait()
        for i in range(4):
            labels[i].add_updater(lambda mob: mob.next_to(mob.reference, UP).shift(0.3*RIGHT).set_fill(opacity = min(mob.get_y()/2 + 1, 1)))
        def falling_updater(mob: VMobject, dt):
            mob.v += dt
            mob.shift(mob.v*(0.5*DOWN + 0.1*LEFT)).rotate(-2*dt)
        for i in range(2):
            j_4 = len(halves_4)
            self.play(halves_4[0].animating(path_arc = -PI).move_to(func_4(3)), 
                  *[halves_4[i+1].animate.move_to(func_4(4-j_4+i)) for i in range(j_4-1)], )
            halves_4.sort(key = lambda mob: mob.get_x())
            halves_4[0].v = 0
            halves_4[0].add_updater(falling_updater)
            self.wait()
            self.remove(halves_4[0]), halves_4.remove(halves_4[0])
        for i in range(4):
            labels[i].suspend_updating()
        self.remove(labels[1], labels[3]).wait()
        self.play(Flip(labels[2], MTex(r"2").move_to(labels[2]).set_stroke(**stroke_dic)))
        self.wait()
        for i in [0, 2]:
            labels[i].resume_updating()
        j_4 = len(halves_4)
        self.play(halves_4[0].animating(path_arc = -PI).move_to(func_4(3)), 
                *[halves_4[i+1].animate.move_to(func_4(4-j_4+i)) for i in range(j_4-1)], )
        halves_4.sort(key = lambda mob: mob.get_x())
        halves_4[0].v = 0
        halves_4[0].add_updater(falling_updater)
        self.wait()
        self.remove(halves_4[0]), halves_4.remove(halves_4[0])
        for i in [0, 2]:
            labels[i].clear_updaters()
        self.remove(labels[2]).wait()
        
#################################################################### 

class Video_6(FrameScene):
    def construct(self):
        n = 13
        halves_13 = [ImageMobject("half_n.png", height = 1) for _ in range(n-1)] + [ImageMobject("half_b.png", height = 1)]
        func_13 = lambda t: 1*DOWN + (t-(n-1)/2)*0.5*RIGHT
        for i in range(n):
            halves_13[i].rotate(PI/6).move_to(func_13(i))
        def sort_updater(scene):
            scene.mobjects.sort(key = lambda mob: mob.get_x(), reverse = True)
        self.updaters = [sort_updater]
        title = Title("约瑟夫问题")
        titleline = TitleLine()
        self.play(Write(title), GrowFromCenter(titleline), *[FadeIn(mob) for mob in halves_13])
        self.wait()

        text = Heiti("祝大家新年快乐万事如意心想事成", color = YELLOW)
        for mob in text:
            mob.scale(3).move_to(5*LEFT + 1.5*UP)
        for i in range(15):
            self.play(halves_13[0].animating(path_arc = -PI*2/3).move_to(func_13(12)), 
                  *[halves_13[i+1].animate.move_to(func_13(i)) for i in range(12)], 
                  FadeIn(text[i], rate_func = there_and_back_with_pause(), remover = True))
            halves_13.sort(key = lambda mob: mob.get_x())
        def falling_updater(mob: VMobject, dt):
            mob.v += dt
            mob.shift(mob.v*(0.5*DOWN + 0.1*LEFT)).rotate(-2*dt)
        keep, kill = Heiti("好运留下来", color = RED).next_to(3*UP + 3*LEFT, DOWN).save_state(), Heiti("烦恼丢出去", color = GREY).next_to(3*UP + 3*RIGHT, DOWN).save_state(),
        for i in range(12):
            waste_13 = halves_13[1]
            halves_13.remove(waste_13)
            waste_13.v = 0
            waste_13.add_updater(falling_updater)
            j_13 = len(halves_13)
            anims = [halves_13[i+1].animate.move_to(func_13(13-j_13+i)) for i in range(j_13-1)] + [halves_13[0].animating(path_arc = -PI*2/3).move_to(func_13(12))]
            if i == 0:
                anims.extend([FadeIn(keep), FadeIn(kill)])
            if i == 11:
                anims.extend([FadeOut(keep), FadeOut(kill)])
            self.play(*anims)
            halves_13.sort(key = lambda mob: mob.get_x())
            self.remove(waste_13)
        self.wait()
        
        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]