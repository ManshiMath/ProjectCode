from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Test_1(FrameScene):
    def construct(self):
        T = 2
        N = 20
        buff = 0.2
        positions = [[buff*(i-(N-1)/2)*UP + buff*(j-(N-1)/2)*RIGHT for i in range(N)] for j in range(N)]
        # arrow_up, arrow_down = Arrow(buff*0.4*DOWN, buff*0.4*UP, buff = 0, color = RED), Arrow(buff*0.4*UP, buff*0.4*DOWN, buff = 0, color = BLUE)
        arrow_up, arrow_down = Line(buff*0.4*DOWN, buff*0.4*UP, stroke_width = [buff*80, buff*40, 0], color = RED), Line(buff*0.4*UP, buff*0.4*DOWN, stroke_width = [buff*80, buff*40, 0], color = "#0000FF")
        arrows = VGroup(*[VGroup(*[arrow_up.copy().shift(positions[i][j]) for i in range(N)]) for j in range(N)]) 
        for i in range(N):
            for j in range(N):
                arrows[i][j].up, arrows[i][j].down, arrows[i][j].left, arrows[i][j].right = arrows[i][(j+1)%N], arrows[i][(j-1)%N], arrows[(i-1)%N][j], arrows[(i+1)%N][j]
                arrows[i][j].state = 1
                arrows[i][j].i, arrows[i][j].j = i, j
        def flip_updater(mob: Arrow):
            states = [mob.up.state, mob.down.state, mob.left.state, mob.right.state] #错的，之后的箭头会使用更新后的状态
            energy_p = -1*(sum(states))/T
            energy_m = -energy_p
            parts = np.exp(-energy_p), np.exp(-energy_m)
            probability = parts[0]/(parts[0]+parts[1])
            print(probability)
            if np.random.rand() < probability:
                mob.state = 1
                mob.become(arrow_up).shift(positions[mob.i][mob.j])
            else:
                mob.state = -1
                mob.become(arrow_down).shift(positions[mob.i][mob.j])
        for i in range(N):
            for j in range(N):
                self.add(arrows[i][j].add_updater(flip_updater))
        self.wait(20)

class Test_2(FrameScene):
    def construct(self):
        T = ValueTracker(3)
        N = 40
        buff = 0.2
        positions = [[buff*(i-(N-1)/2)*UP + buff*(j-(N-1)/2)*RIGHT for i in range(N)] for j in range(N)]
        # arrow_up, arrow_down = Arrow(buff*0.4*DOWN, buff*0.4*UP, buff = 0, color = RED), Arrow(buff*0.4*UP, buff*0.4*DOWN, buff = 0, color = BLUE)
        arrow_up, arrow_down = Line(buff*0.4*DOWN, buff*0.4*UP, stroke_width = [buff*80, buff*40, 0], color = RED), Line(buff*0.4*UP, buff*0.4*DOWN, stroke_width = [buff*80, buff*40, 0], color = BLUE)
        arrows = VGroup(*[VGroup(*[arrow_up.copy().shift(positions[i][j]) for i in range(N)]) for j in range(N)]) 
        arrows.states = np.ones((N, N))
        # for i in range(N):
        #     for j in range(N):
        #         arrows[i][j].up, arrows[i][j].down, arrows[i][j].left, arrows[i][j].right = arrows[i][(j+1)%N], arrows[i][(j-1)%N], arrows[(i-1)%N][j], arrows[(i+1)%N][j]
        #         arrows[i][j].state = 1
        #         arrows[i][j].i, arrows[i][j].j = i, j
        def flip_updater(mob: VGroup):
            state = mob.states
            # states_near = np.roll(state, 1, axis = 0) + np.roll(state, -1, axis = 0) + np.roll(state, 1, axis = 1) + np.roll(state, -1, axis = 1)
            state_ud, state_lr = np.roll(state, 1, axis = 0) + np.roll(state, -1, axis = 0), np.roll(state, 1, axis = 1) + np.roll(state, -1, axis = 1)
            states_near = state_ud + state_lr + np.roll(state_ud, 1, axis = 1)*0.5 + np.roll(state_ud, -1, axis = 1)*0.5
            # print(state, states_near)
            energy_p = -1*states_near/T.get_value()
            energy_m = -energy_p
            parts = np.exp(-energy_p), np.exp(-energy_m)
            probability = parts[0]/(parts[0]+parts[1])
            # print(probability)
            randoms = np.random.rand(N, N)
            for i in range(N):
                for j in range(N):
                    if randoms[i][j] < probability[i][j]:
                        mob.states[i][j] = 1
                        mob[i][j].become(arrow_up).shift(positions[i][j])
                    else:
                        mob.states[i][j] = -1
                        mob[i][j].become(arrow_down).shift(positions[i][j])
            # if np.random.rand() < probability:
            #     mob.state = 1
            #     mob.become(arrow_up).shift(positions[mob.i][mob.j])
            # else:
            #     mob.state = -1
            #     mob.become(arrow_down).shift(positions[mob.i][mob.j])
        # for i in range(N):
        #     for j in range(N):
        #         self.add(arrows[i][j].add_updater(flip_updater))
        self.add(arrows.add_updater(flip_updater))
        self.wait(5)
        self.play(T.animate.set_value(20), run_time = 5)
        self.wait(5)
        self.play(T.animate.set_value(3), run_time = 5)
        self.wait(5)
        # np.random.binomial()
        
        
#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        T = ValueTracker(3)
        N, M = 40, 30
        buff = 0.2
        offset_l = 2*LEFT
        C_DOWN = "#0000FF"
        positions = [[buff*(i-(M-1)/2)*DOWN + buff*(j-(N-1)/2)*RIGHT + offset_l for i in range(M)] for j in range(N)]
        arrow_up, arrow_down = Line(buff*0.4*DOWN, buff*0.4*UP, stroke_width = [buff*80, buff*40, 0], color = RED), Line(buff*0.4*UP, buff*0.4*DOWN, stroke_width = [buff*80, buff*40, 0], color = C_DOWN)
        arrows = VGroup(*[VGroup(*[arrow_up.copy().shift(positions[j][i]) for i in range(M)]) for j in range(N)]) 
        arrows.states, arrows.outlook = np.ones((N, M)), np.zeros((N, M), dtype = int)

        alpha = ValueTracker(0.0)
        beta = ValueTracker(0.0)
        interpolate_frame = 1
        arrows_interpolate = [Line(buff*0.4*interpolate(DOWN, UP, alpha), buff*0.4*interpolate(UP, DOWN, alpha), stroke_width = [buff*80, buff*40, 0], color = interpolate_color(RED, C_DOWN, alpha)) for alpha in np.linspace(0, 1, interpolate_frame + 1)]
        def flip_updater(mob: VGroup):

            state = mob.states
            state_ud, state_lr = np.roll(state, 1, axis = 0) + np.roll(state, -1, axis = 0), np.roll(state, 1, axis = 1) + np.roll(state, -1, axis = 1)
            states_near = state_ud + state_lr + np.roll(state_ud, 1, axis = 1)*0.5 + np.roll(state_ud, -1, axis = 1)*0.5
            energy_p = -1*states_near/T.get_value()
            energy_m = -energy_p
            parts = np.exp(-energy_p), np.exp(-energy_m)
            probability = parts[0]/(parts[0]+parts[1])
            randoms = np.random.rand(N, M)

            value = alpha.get_value()
            threshold = int(value*(M + N))

            for i in range(N):
                for j in range(M):
                    if randoms[i][j] < probability[i][j]:
                        mob.states[i][j] = 1
                        if arrows.outlook[i][j] > 0:
                            arrows.outlook[i][j] -= 1
                        mob[i][j].become(arrows_interpolate[arrows.outlook[i][j]]).shift(positions[i][j])
                    else:
                        mob.states[i][j] = -1
                        if arrows.outlook[i][j] < interpolate_frame:
                            arrows.outlook[i][j] += 1
                        mob[i][j].become(arrows_interpolate[arrows.outlook[i][j]]).shift(positions[i][j])
                    if i + j > threshold:
                        mob[i][j].set_opacity(0)
        # def submob_post_updater(mob: VGroup):
            # int_j, residue_j = int(value*M), value - int(value*M)
            # int_i, residue_i = int(residue_j*N), residue_j - int(residue_j*N)
            # for j in range(int_j, M):
            #     interval = range(N) if j > int_j else range(int_i, N)
            #     for i in interval:
            #         mob[i][j].set_opacity(0)
            # for i in range(N):
            #     for j in range(M):
            #         if i + j < threshold:
            #             mob[i][j].set_opacity(0)
        self.add(arrows.add_updater(flip_updater))
        self.wait(1)
        self.play(alpha.animate.set_value(1), run_time = 2)
        self.wait(5)

        offset_r = 4.5*RIGHT
        center_text = offset_r + 1.75*UP
        label_p = VGroup(Polygon(buff*0.8*DL, buff*0.8*DR, buff*0.8*UP, fill_color = RED, fill_opacity = 1), *MTex(r":+1", color = RED)).arrange().shift(center_text + 0.6*UP).set_stroke(width = 8, color = BLACK, background = True)
        label_m = VGroup(Polygon(buff*0.8*UL, buff*0.8*UR, buff*0.8*DOWN, fill_color = C_DOWN, fill_opacity = 1), *MTex(r":-1", color = C_DOWN)).arrange().shift(center_text + 0.6*DOWN).set_stroke(width = 8, color = WHITE, background = True)
        ratio = 0.2
        magnetic_p = VGroup(Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0), 
                            Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0), 
                            MTex("N", color = BLACK)[0].scale(0.5).shift(0.7*ratio*UP), 
                            MTex("S", color = WHITE)[0].scale(0.5).shift(0.7*ratio*DOWN)).shift(center_text + 0.6*UP + 1.5*LEFT)
        magnetic_m = VGroup(Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = RED, fill_opacity = 1, stroke_width = 0), 
                            Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0), 
                            MTex("N", color = BLACK)[0].scale(0.5).shift(0.7*ratio*DOWN), 
                            MTex("S", color = WHITE)[0].scale(0.5).shift(0.7*ratio*UP)).shift(center_text + 0.6*DOWN + 1.5*LEFT)
        surr = SurroundingRectangle(VGroup(label_p, label_m), stroke_color = WHITE, buff = 0.4, fill_color = BACK, fill_opacity = 1)
        self.play(Write(surr))
        self.wait(1)
        self.play(Write(label_p))
        self.wait(1)
        self.play(Write(label_m))
        self.wait()
        self.add_background(magnetic_p, magnetic_m).play(magnetic_p.shift(0.5*RIGHT).animate.shift(0.5*LEFT), magnetic_m.shift(0.5*RIGHT).animate.shift(0.5*LEFT))
        self.wait(5)
        self.print_mark()
        self.play(T.animate.set_value(1), run_time = 3)
        self.print_mark()
        self.wait(5)

        ratio = 0.5
        center_magnetic = offset_r + 1.5*DOWN + LEFT
        center_number = offset_r + 1.5*DOWN + RIGHT
        magnetic_needle = VGroup(Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0), 
                                 Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0)).shift(center_magnetic)
        text_ns = VGroup(MTex("N", color = RED)[0].set_stroke(width = 8, color = BLACK, background = True).shift(0.35*UP), 
                         MTex("S", color = C_DOWN)[0].set_stroke(width = 8, color = WHITE, background = True).shift(0.35*DOWN)).shift(center_magnetic)
        cavity = Polygon(ratio*LEFT, ratio*2*UP, ratio*RIGHT, ratio*2*DOWN, fill_color = BLACK, fill_opacity = 1).set_stroke(width = 20, color = GREY, background = True).shift(center_magnetic)
        number_line = VGroup(Line(0.2*LEFT, 0.2*RIGHT, color = RED).shift(UP), Line(0.2*LEFT, 0.2*RIGHT, color = C_DOWN).shift(DOWN), 
                             Line(UP, DOWN, color = [RED, C_DOWN])).set_stroke(width = 8).shift(center_number)
        poles = VGroup(MTex(r"+1", color = RED).scale(0.8).next_to(number_line, UP), MTex(r"-1", color = C_DOWN).scale(0.8).next_to(number_line, DOWN))
        point = Dot(color = WHITE).shift(center_number)
        # gamma = ValueTracker(0.0)
        # opacity_post = lambda mob: mob.set_opacity(gamma.get_value())
        def scale_post(mob: VMobject):
            avg = np.average(arrows.states)
            mob.scale(avg, about_point = center_magnetic, min_scale_factor = -1)
        for mob in magnetic_needle.submobjects + text_ns.submobjects:
            mob.add_post_updater(scale_post)
        def shift_post(mob: VMobject):
            avg = np.average(arrows.states)
            mob.shift(avg*UP)
        point.add_post_updater(shift_post)
        shade = BackgroundRectangle(VGroup(magnetic_needle, text_ns, cavity, number_line, poles, point))
        # for mob in [magnetic_needle, text_ns, cavity, number_line, poles, point]:
        #     mob.add_post_updater(opacity_post)
        self.add(cavity, magnetic_needle, text_ns, number_line, poles, point).add_top(shade).play(FadeOut(shade))
        self.wait(5)
        interpolate_frame = 5
        arrows_interpolate = [Line(buff*0.4*interpolate(DOWN, UP, alpha), buff*0.4*interpolate(UP, DOWN, alpha), stroke_width = [buff*80, buff*40, 0], color = interpolate_color(RED, C_DOWN, alpha)) for alpha in np.linspace(0, 1, interpolate_frame + 1)]
        self.print_mark()
        self.play(T.animate.set_value(9), run_time = 20)
        self.print_mark()
        self.wait(5)

        # self.play(T.animate.set_value(20), run_time = 5)
        # self.wait(5)
        # self.play(T.animate.set_value(3), run_time = 5)
        # self.wait(5)

#################################################################### 

class Video_2(FrameScene):
    def construct(self):
        ratio = 0.3
        C_DOWN = "#0000FF"
        offset_l, offset_r = LEFT_SIDE/2 + 0.5*UP, RIGHT_SIDE/2 + 0.5*UP
        ul, ur, dl, dr = 1.5*UL, 1.5*UR, 1.5*DL, 1.5*DR
        buff = 0.4
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        energy_low, energy_high = 1, 3
        def shake_post(energy: float):
            def util(mob: VMobject):
                angle = interpolate(mob.angle, PI/12*energy*random.uniform(-1, 1), 0.1)
                mob.rotate(angle)
                mob.angle = angle
            return util
        low_post, high_post = shake_post(energy_low), shake_post(energy_high)
        low_ul = [arrow_up.copy().shift(offset_l + ul + buff*UP), arrow_up.copy().shift(offset_l + ul + buff*DOWN)]
        low_ur = [arrow_down.copy().shift(offset_l + ur + buff*UP), arrow_down.copy().shift(offset_l + ur + buff*DOWN)]
        low_dl = [arrow_up.copy().shift(offset_l + dl + buff*LEFT), arrow_up.copy().shift(offset_l + dl + buff*RIGHT)]
        low_dr = [arrow_down.copy().shift(offset_l + dr + buff*LEFT), arrow_down.copy().shift(offset_l + dr + buff*RIGHT)]
        text_low = MTex(r"E_{\text{磁}}=-J", tex_to_color_map = {(r"E_{\text{磁}}", r"-J"): YELLOW}).shift(offset_l + 2.5*DOWN)
        for mob in low_ul + low_ur + low_dl + low_dr:
            mob.angle = 0
            mob.add_post_updater(low_post)
        self.wait(1)
        self.play(*[GrowFromCenter(mob) for mob in low_ul + low_ur + low_dl + low_dr])
        self.play(Write(text_low))
        self.wait()

        high_ul = [arrow_up.copy().shift(offset_r + ul + buff*UP), arrow_down.copy().shift(offset_r + ul + buff*DOWN)]
        high_ur = [arrow_down.copy().shift(offset_r + ur + buff*UP), arrow_up.copy().shift(offset_r + ur + buff*DOWN)]
        high_dl = [arrow_up.copy().shift(offset_r + dl + buff*LEFT), arrow_down.copy().shift(offset_r + dl + buff*RIGHT)]
        high_dr = [arrow_down.copy().shift(offset_r + dr + buff*LEFT), arrow_up.copy().shift(offset_r + dr + buff*RIGHT)]
        text_high = MTex(r"E_{\text{磁}}=J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).shift(offset_r + 2.5*DOWN)
        for mob in high_ul + high_ur + high_dl + high_dr:
            mob.angle = 0
            mob.add_post_updater(high_post) 
        self.wait(1)
        self.play(*[GrowFromCenter(mob) for mob in high_ul + high_ur + high_dl + high_dr])
        self.play(Write(text_high))
        self.wait(5)
        
class Video_3(FrameScene):
    def construct(self):
        centers = [RIGHT_SIDE*(i-2)*0.4 for i in range(5)]
        texts = [MTexText(str(4-i)+"同"+str(i)+"异").scale(0.8).shift(centers[i] + 2*UP) for i in range(5)]
        energies = [MTex(r"E_{\text{磁}}=" + str(2*i-4) + "J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).scale(0.8).shift(centers[i] + 2*DOWN) for i in range(5)]
        
        ratio = 0.25
        C_DOWN = "#3333FF"
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [0.65*UP, 0.65*LEFT, 0.65*DOWN, 0.65*RIGHT]
        def shake_post(energy: float):
            def util(mob: VMobject):
                angle = interpolate(mob.angle, PI/12*energy*random.uniform(-1, 1), 0.1*interpolate(1, energy, 0.5))
                mob.rotate(angle)
                mob.angle = angle
            return util
        groups = []
        for i in range(5):
            group = VGroup(arrow_up.copy().add_post_updater(shake_post(i+1)))
            updater = shake_post((i+1)/2)
            for j in range(4):
                group.add((arrow_down if j < i else arrow_up).copy().shift(offsets[j]).set_opacity(0.5).add_post_updater(updater))
            for mob in group:
                mob.angle = 0
            groups.append(group.shift(centers[i]))
        # self.add(*texts, *energies, *groups)
        self.wait(1)
        for i in range(5):
            self.play(*[FadeIn(mob, UP if i%2 else DOWN) for mob in [texts[i], energies[i], groups[i]]])
        self.wait(5)
                  
        formula = MTex(r"E_{\text{磁}}=\sigma_{\text{自身}}\left(\sigma_{\text{上}}+\sigma_{\text{下}}+\sigma_{\text{左}}+\sigma_{\text{右}}\right)J", 
                       tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW, (r"\sigma", r"自身", r"上", r"下", r"左", r"右"): PURPLE_A}).shift(3*UP)
        self.play(ShowIncreasingSubsets(formula), rate_func = linear)
        self.wait(5)

class Video_4(FrameScene):
    def construct(self):
        centers = [LEFT_SIDE/2, RIGHT_SIDE/2]
        ratio = 0.5
        C_DOWN = "#0000FF"
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [1.4*UP, 1.4*LEFT, 1.4*DOWN, 1.4*RIGHT]
        def shake_post(mob: VMobject):
            energy = mob.uniforms["energy"]
            angle = interpolate(mob.angle, PI/12*energy*random.uniform(-1, 1), 0.1*interpolate(1, energy, 0.5))
            mob.rotate(angle)
            mob.angle = angle
        before = VGroup(arrow_up.copy(), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[0])
        before[0].angle, before[0].uniforms["energy"] = 0, 5
        before[0].add_post_updater(shake_post)
        for mob in before[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 3
            mob.add_post_updater(shake_post)
        self.add(before).wait(5)

        after = VGroup(arrow_down.copy(), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[1])
        after[0].angle, after[0].uniforms["energy"] = 0, 1
        after[0].add_post_updater(shake_post)
        for mob in after[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 1
            mob.add_post_updater(shake_post)
        arrow_back = Polygon(2.5*RIGHT, 1*RIGHT + 1.5*UP, 1*RIGHT + 0.5*UP, 2.5*LEFT + 0.5*UP, 2.5*LEFT + 0.5*DOWN, 1*RIGHT + 0.5*DOWN, 1*RIGHT + 1.5*DOWN, stroke_width = 0, fill_opacity = 1, fill_color = GREY_E)
        self.add_background(arrow_back).play(TransformFromCopy(before, after), FlushInX(arrow_back, middle = arrow_back.get_x(LEFT) - 0.2))
        self.wait(5)

class Patch_4(FrameScene):
    def construct(self):
        T = ValueTracker(11)
        N, M = 48, 30
        buff = 0.2
        offset_l = ORIGIN
        C_DOWN = "#0000FF"
        positions = [[buff*(i-(M-1)/2)*DOWN + buff*(j-(N-1)/2)*RIGHT + offset_l for i in range(M)] for j in range(N)]
        arrow_up, arrow_down = Line(buff*0.4*DOWN, buff*0.4*UP, stroke_width = [buff*80, buff*40, 0], color = RED), Line(buff*0.4*UP, buff*0.4*DOWN, stroke_width = [buff*80, buff*40, 0], color = C_DOWN)
        arrows = VGroup(*[VGroup(*[arrow_up.copy().shift(positions[j][i]) for i in range(M)]) for j in range(N)]) 
        arrows.states, arrows.outlook = np.ones((N, M)), np.zeros((N, M), dtype = int)

        interpolate_frame = 5
        arrows_interpolate = [Line(buff*0.4*interpolate(DOWN, UP, alpha), buff*0.4*interpolate(UP, DOWN, alpha), stroke_width = [buff*80, buff*40, 0], color = interpolate_color(RED, C_DOWN, alpha)) for alpha in np.linspace(0, 1, interpolate_frame + 1)]
        def flip_updater(mob: VGroup):

            state = mob.states
            state_ud, state_lr = np.roll(state, 1, axis = 0) + np.roll(state, -1, axis = 0), np.roll(state, 1, axis = 1) + np.roll(state, -1, axis = 1)
            states_near = state_ud + state_lr + np.roll(state_ud, 1, axis = 1)*0.5 + np.roll(state_ud, -1, axis = 1)*0.5
            energy_p = -1*states_near/T.get_value()
            energy_m = -energy_p
            parts = np.exp(-energy_p), np.exp(-energy_m)
            probability = parts[0]/(parts[0]+parts[1])
            randoms = np.random.rand(N, M)

            for i in range(N):
                for j in range(M):
                    if randoms[i][j] < probability[i][j]:
                        mob.states[i][j] = 1
                        if arrows.outlook[i][j] > 0:
                            arrows.outlook[i][j] -= 1
                        mob[i][j].become(arrows_interpolate[arrows.outlook[i][j]]).shift(positions[i][j])
                    else:
                        mob.states[i][j] = -1
                        if arrows.outlook[i][j] < interpolate_frame:
                            arrows.outlook[i][j] += 1
                        mob[i][j].become(arrows_interpolate[arrows.outlook[i][j]]).shift(positions[i][j])
        self.add(arrows.add_updater(flip_updater))
        # self.wait(1)
        self.play(T.animate.set_value(1), run_time = 5)
        self.wait(5)

class Video_5(FrameScene):
    def construct(self):
        centers = [2.4*UP, 0.6*DOWN + 5*LEFT, 0.6*DOWN + 5*RIGHT]
        ratio = 0.4
        C_DOWN = "#0000FF"
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [1.0*UP, 1.0*LEFT, 1.0*DOWN, 1.0*RIGHT]
        def shake_post(mob: VMobject):
            energy = mob.uniforms["energy"]
            angle = interpolate(mob.angle, PI/12*energy*random.uniform(-1, 1), 0.1*interpolate(1, energy, 0.5))
            mob.rotate(angle)
            mob.angle = angle
        before = VGroup(arrow_up.copy(), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[0])
        before[0].angle, before[0].uniforms["energy"] = 0, 5
        before[0].add_post_updater(shake_post)
        for mob in before[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 3
            mob.add_post_updater(shake_post)
        
        ratio = 0.3
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [0.8*UP, 0.8*LEFT, 0.8*DOWN, 0.8*RIGHT]
        case_l = VGroup(arrow_up.copy(), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[1])
        case_l[0].angle, case_l[0].uniforms["energy"] = 0, 5
        case_l[0].add_post_updater(shake_post)
        for mob in case_l[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 3
            mob.add_post_updater(shake_post)
        text_l = MTex(r"E_{\text{磁}}=4J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).next_to(case_l, DOWN)
        case_r = VGroup(arrow_down.copy(), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[2])
        case_r[0].angle, case_r[0].uniforms["energy"] = 0, 1
        case_r[0].add_post_updater(shake_post)
        for mob in case_r[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 1
            mob.add_post_updater(shake_post)
        text_r = MTex(r"E_{\text{磁}}=-4J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).next_to(case_r, DOWN)
        self.add(before, case_l, case_r, text_l, text_r).wait()

        arrow_l, arrow_r = Arrow(before, case_l, path_arc = PI/2), Arrow(before, case_r, path_arc = -PI/2)
        self.play(ShowCreation(arrow_l), ShowCreation(arrow_r))
        p_l, p_r = MTex(r"\frac{e^{-\frac{-4J}{kT}}}{e^{-\frac{-4J}{kT}}+e^{-\frac{4J}{kT}}}", tex_to_color_map = {(r"4J", r"-4J"): YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).scale(0.8).next_to(arrow_l.get_center(), DR).shift(0.5*UL), MTex(r"\frac{e^{-\frac{4J}{kT}}}{e^{-\frac{-4J}{kT}}+e^{-\frac{4J}{kT}}}", tex_to_color_map = {(r"4J", r"-4J"): YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).scale(0.8).next_to(arrow_r.get_center(), DL).shift(0.5*UR)
        e = np.exp(1)
        alpha_0 = (e)/(e+1/e)
        middle = interpolate(3.5, -3.5, alpha_0)
        bar_l, bar_r = Line(3.5*LEFT, 3.5*RIGHT, stroke_width = 100, color = RED).shift(0.6*DOWN), Line(3.5*LEFT, 3.5*RIGHT, stroke_width = 100, color = C_DOWN).shift(0.6*DOWN)
        percent_l = MTex(f"{(1-alpha_0)*100:.1f}"+r"\%", color = BLACK).save_state().set_width(middle-(-3.5)-0.2).next_to(middle*RIGHT + 0.6*DOWN, LEFT, buff = 0.1)
        percent_r = MTex(f"{alpha_0*100:.1f}"+r"\%", color = WHITE).save_state().next_to(middle*RIGHT + 0.6*DOWN, RIGHT, buff = 0.1)
        for mob in [bar_l] + percent_l.submobjects:
            mob.fill_shader_wrapper.reset_shader("mask_fill_r")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_r")
            mob.uniforms["mask_x"] = -3.6
        bar_l.generate_target().uniforms["mask_x"] = middle
        for mob in [bar_r] + percent_r.submobjects:
            mob.fill_shader_wrapper.reset_shader("mask_fill_l")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_l")
            mob.uniforms["mask_x"] = 3.6
        bar_r.generate_target().uniforms["mask_x"] = middle
        for mob in percent_l.generate_target().submobjects + percent_r.generate_target().submobjects:
            mob.uniforms["mask_x"] = middle
        
        self.play(Write(p_l), Write(p_r), *[MoveToTarget(mob, run_time = 2, rate_func = rush_into) for mob in [bar_l, bar_r, percent_l, percent_r]])
        self.wait()

        notice = MTex(r"J:&\text{单位能量}\\T:&\text{环境温度}\\k:&\text{玻尔兹曼常数}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).scale(0.8).shift(5*RIGHT + 2.25*UP)
        text_T = MTex(r"T=04.00\frac{J}{k}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).shift(5*LEFT + 2.25*UP)
        text_T[2].set_opacity(0).shift(8*UP)
        self.play(FadeIn(notice, 0.5*LEFT), Write(text_T))
        text_T[2].shift(8*DOWN)
        self.wait()

        T = ValueTracker(1.0)
        digits = [MTex(str(i)) for i in range(10)]
        def digit_raplace(mob: VMobject, index: int):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
        def text_T_updater(mob: MTex):
            value = 4*T.get_value()
            if value < 10:
                mob[2].set_opacity(0)
            else:
                digit_raplace(mob[2], int(value/10))
            index, residue = int(value%10), 10*(value - int(value))
            digit_raplace(mob[3], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[5], index)
            index = int(residue)
            digit_raplace(mob[6], index)
        text_T.add_updater(text_T_updater)

        for mob in percent_l.submobjects + percent_r.submobjects:
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        
        def mask_updater(mob: VMobject):
            value = T.get_value()
            if value <= 1e-3:
                alpha = 1
            else:
                e = np.exp(1/value)
                alpha = e/(e+1/e)
            mob.uniforms["mask_x"] = interpolate(3.5, -3.5, alpha)
        bar_l.add_updater(mask_updater), bar_r.add_updater(mask_updater)
        def left_updater(mob: VMobject):
            value = T.get_value()
            if value <= 1e-3:
                alpha = 0
            else:
                e = np.exp(1/value)
                alpha = 1 - e/(e+1/e)
            middle = interpolate(-3.5, 3.5, alpha)
            value = min(alpha * 10, 9.99)
            mob.restore()
            if value < 1:
                mob[0].set_opacity(0)
                residue = value * 10
            else:
                index, residue = int(value), 10*(value - int(value))
                digit_raplace(mob[0], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[1], index)
            index = int(residue)
            digit_raplace(mob[3], index)
            mob.set_color(BLACK).set_width(min(middle-(-3.5)-0.2, mob.get_width())).next_to(middle*RIGHT + 0.6*DOWN, LEFT, buff = 0.1)
        percent_l.add_updater(left_updater)
        def right_updater(mob: VMobject):
            value = T.get_value()
            if value <= 1e-3:
                alpha = 1
            else:
                e = np.exp(1/value)
                alpha = e/(e+1/e)
            middle = interpolate(3.5, -3.5, alpha)
            value = min(alpha * 10, 9.99)
            mob.restore()
            if value < 1:
                mob[0].set_opacity(0)
                residue = value * 10
            else:
                index, residue = int(value), 10*(value - int(value))
                digit_raplace(mob[0], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[1], index)
            index = int(residue)
            digit_raplace(mob[3], index)
            mob.set_width(min(3.5-middle-0.2, mob.get_width())).next_to(middle*RIGHT + 0.6*DOWN, RIGHT, buff = 0.1)
        percent_l.add_updater(left_updater), percent_r.add_updater(right_updater)
        self.play(T.animate.set_value(2))
        self.wait()
        self.play(T.animate.set_value(5))
        self.wait()
        self.play(T.animate.set_value(1))
        self.wait()
        self.play(T.animate.set_value(0))
        self.wait()

class Video_6(FrameScene):
    def construct(self):
        T = ValueTracker(1.0)
        N, M = 40, 30
        buff = 0.2
        offset_l = 2*LEFT
        C_DOWN = "#0000FF"
        positions = [[buff*(i-(M-1)/2)*DOWN + buff*(j-(N-1)/2)*RIGHT + offset_l for i in range(M)] for j in range(N)]
        arrow_up, arrow_down = Line(buff*0.4*DOWN, buff*0.4*UP, stroke_width = [buff*80, buff*40, 0], color = RED), Line(buff*0.4*UP, buff*0.4*DOWN, stroke_width = [buff*80, buff*40, 0], color = C_DOWN)
        states, outlook = np.random.randint(2, size = (N, M), dtype = int)*2-1, np.zeros((N, M), dtype = int)
        arrows = VGroup(*[VGroup(*[(arrow_up if states[j][i] == 1 else arrow_down).copy().shift(positions[j][i]) for i in range(M)]) for j in range(N)])
        arrows.states, arrows.outlook, arrows.avg = states, outlook, np.average(states)
        
        offset_r = 4.5*RIGHT
        center_number = offset_r + 1.5*LEFT + 2*UP
        number_line = VGroup(Line(0.2*LEFT, 0.2*RIGHT, color = RED).shift(UP), Line(0.2*LEFT, 0.2*RIGHT, color = C_DOWN).shift(DOWN), 
                             Line(UP, DOWN, color = [RED, C_DOWN])).set_stroke(width = 8).shift(center_number)
        poles = VGroup(MTex(r"+1", color = RED).scale(0.8).next_to(number_line, UP), MTex(r"-1", color = C_DOWN).scale(0.8).next_to(number_line, DOWN))
        point = Dot(color = WHITE).shift(center_number)
        def shift_post(mob: VMobject):
            avg = arrows.avg
            mob.shift(avg*UP)
        point.add_post_updater(shift_post)

        digits = [MTex(str(i)) for i in range(10)]
        text_T = MTex(r"T=1.000\frac{J}{k}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).shift(offset_r + 2*UP + 0.5*RIGHT)
        def digit_raplace(mob: VMobject, index: int):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
        def text_T_updater(mob: MTex):
            value = 1*T.get_value()
            index, residue = int(value%10), 10*(value - int(value))
            digit_raplace(mob[2], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[4], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[5], index)
            index = int(residue)
            digit_raplace(mob[6], index)
        text_T.add_updater(text_T_updater)

        shade = BackgroundRectangle(VGroup(number_line, poles, point, text_T))

        alpha = ValueTracker(0.0)
        def showup_updater(mob: VGroup):
            value = alpha.get_value()
            threshold = int(value*(M + N))
            for i in range(N):
                for j in range(M):
                    mob[i][j].set_opacity(0 if i + j > threshold else 1)
        self.wait(1)
        self.add(arrows.add_updater(showup_updater), number_line, poles, point, text_T).add_top(shade).play(alpha.animating(run_time = 2).set_value(1), FadeOut(shade))
        arrows.clear_updaters()
        self.wait()

        interpolate_frame = 5
        arrows_interpolate = [Line(buff*0.4*interpolate(DOWN, UP, alpha), buff*0.4*interpolate(UP, DOWN, alpha), stroke_width = [buff*80, buff*40, 0], color = interpolate_color(RED, C_DOWN, alpha)) for alpha in np.linspace(0, 1, interpolate_frame + 1)]
        beta = ValueTracker(1.0)
        gamma = ValueTracker(0.25)
        thershold = 2/np.log(1+np.sqrt(2))
        factor = 3.2/thershold
        np.random.random(800)
        def flip_updater(mob: VGroup):

            state = mob.states
            state_ud, state_lr = np.roll(state, 1, axis = 0) + np.roll(state, -1, axis = 0), np.roll(state, 1, axis = 1) + np.roll(state, -1, axis = 1)
            states_near = (state_ud + state_lr + (np.roll(state_ud, 1, axis = 1) + np.roll(state_ud, -1, axis = 1))*beta.get_value())/(1+beta.get_value()) + gamma.get_value()
            tempreture = T.get_value()*factor
            if tempreture > 0.01:
                energy_p = -1*states_near/tempreture
                energy_m = -energy_p
                parts = np.exp(-energy_p), np.exp(-energy_m)
                probability = parts[0]/(parts[0]+parts[1])
            else:
                probability = np.zeros((N, M))
                for i in range(N):
                    for j in range(M):
                        if states_near[i][j] == 0:
                            probability[i][j] = 0.5
                        else:
                            probability[i][j] = int(states_near[i][j] > 0)
            randoms = np.random.rand(N, M)

            for i in range(N):
                for j in range(M):
                    if randoms[i][j] < probability[i][j]:
                        mob.states[i][j] = 1
                        if mob.outlook[i][j] > 0:
                            mob.outlook[i][j] -= 1
                        mob[i][j].become(arrows_interpolate[mob.outlook[i][j]]).shift(positions[i][j])
                    else:
                        mob.states[i][j] = -1
                        if mob.outlook[i][j] < interpolate_frame:
                            mob.outlook[i][j] += 1
                        mob[i][j].become(arrows_interpolate[mob.outlook[i][j]]).shift(positions[i][j])
            mob.avg = np.average(state)
        arrows.add_updater(flip_updater)
        self.wait(5)
        gamma.set_value(0)
        beta.set_value(0.2)

        center_d = offset_r + 1.6*LEFT + 1.5*DOWN
        axis_x = Line(ORIGIN, 3.5*RIGHT, color = [interpolate_color(RED, C_DOWN, 0.5), WHITE]).shift(center_d)
        axis_y = VGroup(Line(ORIGIN, 0.2*RIGHT, color = RED).shift(UP), Line(ORIGIN, 0.2*RIGHT, color = C_DOWN).shift(DOWN), 
                             Line(UP, DOWN, color = [RED, C_DOWN]), Line(UP, 1.2*UP, color = RED), Line(DOWN, 1.2*DOWN, color = C_DOWN)).shift(center_d)
        labels_y = VGroup(MTex(r"+1", color = RED).set_stroke(**stroke_dic).scale(0.8).next_to(axis_y[0], LEFT), MTex(r"-1", color = C_DOWN).set_stroke(**stroke_dic).scale(0.8).next_to(axis_y[1], LEFT))
        label_x = MTex(r"T", color = TEAL).scale(0.8).next_to(axis_x, RIGHT)
        point_down = Dot(color = WHITE).shift(center_d)
        def get_color(t: float):
            if t > 0:
                return interpolate_color(WHITE, RED, t)
            else:
                return interpolate_color(WHITE, C_DOWN, -t)
        def shift_post_d(mob: VMobject):
            avg = arrows.avg
            mob.shift(avg*UP + T.get_value()*RIGHT).set_color(get_color(avg))
        point_down.add_post_updater(shift_post_d)
        point_cloud = DotCloud(radius = 0.01)
        def shift_post_d(mob: DotCloud):
            avg = arrows.avg
            mob.add_point(avg*UP + T.get_value()*RIGHT + center_d, color = get_color(avg))
        point_cloud.add_updater(shift_post_d)
        shade = BackgroundRectangle(VGroup(axis_x, axis_y, labels_y, label_x, point_down))
        self.add_background(point_cloud).add(axis_x, axis_y, labels_y, label_x, point_down).add_top(shade).play(FadeOut(shade))
        self.wait(5)

        self.play(T.animate.set_value(0), run_time = 2)
        self.wait()
        self.play(T.animate.set_value(1.5), run_time = 3, rate_func = linear)
        # self.wait()
        # beta.set_value(0)
        # self.play(T.animate.set_value(thershold), run_time = 5, rate_func = linear)
        T.add_updater(lambda mob: mob.increment_value(0.001))
        self.wait(50)
        # self.play(T.animate.set_value(thershold + 0.1), run_time = 2)
        # self.wait()
        T.clear_updaters()
        self.wait()
        T.add_updater(lambda mob: mob.increment_value(-0.001))
        self.wait(25)
        def gamma_updater(mob: ValueTracker):
            value = mob.get_value() - 0.2/60
            if value < -0.2:
                mob.clear_updaters().add_updater(updater_2)
                value = -0.2
            mob.set_value(value)
        def updater_2(mob: ValueTracker):
            value = mob.get_value() + 0.2/500
            if value > 0:
                mob.clear_updaters()
                value = 0
            mob.set_value(value)
        # gamma.set_value(-0.1).add_updater(gamma_updater)
        self.wait(25)
        # self.wait(30)
        # self.play(T.animate.set_value(3), run_time = 2)
        # self.wait()

class Video_6_2(FrameScene):
    def construct(self):
        T = ValueTracker(1.0)
        N, M = 40, 30
        buff = 0.2
        offset_l = 2*LEFT
        C_DOWN = "#0000FF"
        positions = [[buff*(i-(M-1)/2)*DOWN + buff*(j-(N-1)/2)*RIGHT + offset_l for i in range(M)] for j in range(N)]
        arrow_up, arrow_down = Line(buff*0.4*DOWN, buff*0.4*UP, stroke_width = [buff*80, buff*40, 0], color = RED), Line(buff*0.4*UP, buff*0.4*DOWN, stroke_width = [buff*80, buff*40, 0], color = C_DOWN)
        states, outlook = np.random.randint(2, size = (N, M), dtype = int)*2-1, np.zeros((N, M), dtype = int)
        arrows = VGroup(*[VGroup(*[(arrow_up if states[j][i] == 1 else arrow_down).copy().shift(positions[j][i]) for i in range(M)]) for j in range(N)])
        arrows.states, arrows.outlook, arrows.avg = states, outlook, np.average(states)
        
        offset_r = 4.5*RIGHT
        center_number = offset_r + 1.5*LEFT + 2*UP
        number_line = VGroup(Line(0.2*LEFT, 0.2*RIGHT, color = RED).shift(UP), Line(0.2*LEFT, 0.2*RIGHT, color = C_DOWN).shift(DOWN), 
                             Line(UP, DOWN, color = [RED, C_DOWN])).set_stroke(width = 8).shift(center_number)
        poles = VGroup(MTex(r"+1", color = RED).scale(0.8).next_to(number_line, UP), MTex(r"-1", color = C_DOWN).scale(0.8).next_to(number_line, DOWN))
        point = Dot(color = WHITE).shift(center_number)
        def shift_post(mob: VMobject):
            avg = arrows.avg
            mob.shift(avg*UP)
        point.add_post_updater(shift_post)

        digits = [MTex(str(i)) for i in range(10)]
        text_T = MTex(r"T=1.000\frac{J}{k}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).shift(offset_r + 2*UP + 0.5*RIGHT)
        def digit_raplace(mob: VMobject, index: int):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
        def text_T_updater(mob: MTex):
            value = 1*T.get_value()
            index, residue = int(value%10), 10*(value - int(value))
            digit_raplace(mob[2], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[4], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[5], index)
            index = int(residue)
            digit_raplace(mob[6], index)
        text_T.add_updater(text_T_updater)

        shade = BackgroundRectangle(VGroup(number_line, poles, point, text_T))

        alpha = ValueTracker(0.0)
        def showup_updater(mob: VGroup):
            value = alpha.get_value()
            threshold = int(value*(M + N))
            for i in range(N):
                for j in range(M):
                    mob[i][j].set_opacity(0 if i + j > threshold else 1)
        self.wait(1)
        self.add(arrows.add_updater(showup_updater), number_line, poles, point, text_T).add_top(shade).play(alpha.animating(run_time = 2).set_value(1), FadeOut(shade))
        arrows.clear_updaters()
        self.wait()

        interpolate_frame = 1
        arrows_interpolate = [Line(buff*0.4*interpolate(DOWN, UP, alpha), buff*0.4*interpolate(UP, DOWN, alpha), stroke_width = [buff*80, buff*40, 0], color = interpolate_color(RED, C_DOWN, alpha)) for alpha in np.linspace(0, 1, interpolate_frame + 1)]
        beta = ValueTracker(0.0)
        gamma = ValueTracker(0.0)
        np.random.random(200)
        def flip_updater(mob: VGroup):

            state = mob.states
            state_ud, state_lr = np.roll(state, 1, axis = 0) + np.roll(state, -1, axis = 0), np.roll(state, 1, axis = 1) + np.roll(state, -1, axis = 1)
            states_near = (state_ud + state_lr)# + (np.roll(state_ud, 1, axis = 1) + np.roll(state_ud, -1, axis = 1))*beta.get_value())/(1+beta.get_value()) + gamma.get_value()
            cost = 2*states_near*state
            temperature = T.get_value()
            if temperature > 0.01:
                # energy_p = -1*states_near/T.get_value()
                # energy_m = -energy_p
                # parts = np.exp(-energy_p), np.exp(-energy_m)
                # probability = parts[0]/(parts[0]+parts[1])
                # probability = np.zeros((N, M))
                probability = 1/(1+np.exp(cost/temperature))
            else:
                probability = np.zeros((N, M))
                for i in range(N):
                    for j in range(M):
                        if states_near[i][j] == 0:
                            probability[i][j] = 0.5
                        else:
                            probability[i][j] = int(states_near[i][j] > 0)
            # print(temperature, probability)

            randoms = np.random.rand(N, M)
            for i in range(N):
                for j in range(M):
                    # if cost[i][j] < 0:
                    #     mob.states[i][j] *= -1
                    # elif randoms[i][j] < probability[i][j]:
                    #     mob.states[i][j] *= -1
                    if randoms[i][j] < probability[i][j]:
                        mob.states[i][j] *= -1
                    if mob.states[i][j] == 1:
                        if mob.outlook[i][j] > 0:
                            mob.outlook[i][j] -= 1
                    else:
                        if mob.outlook[i][j] < interpolate_frame:
                            mob.outlook[i][j] += 1
                    mob[i][j].become(arrows_interpolate[mob.outlook[i][j]]).shift(positions[i][j])
            mob.avg = np.average(mob.states)
        arrows.add_updater(flip_updater)
        self.wait(5)
        gamma.set_value(0)
        # beta.set_value(0.2)

        center_d = offset_r + 1.6*LEFT + 1.5*DOWN
        axis_x = Line(ORIGIN, 3.5*RIGHT, color = [interpolate_color(RED, C_DOWN, 0.5), WHITE]).shift(center_d)
        axis_y = VGroup(Line(ORIGIN, 0.2*RIGHT, color = RED).shift(UP), Line(ORIGIN, 0.2*RIGHT, color = C_DOWN).shift(DOWN), 
                             Line(UP, DOWN, color = [RED, C_DOWN]), Line(UP, 1.2*UP, color = RED), Line(DOWN, 1.2*DOWN, color = C_DOWN)).shift(center_d)
        labels_y = VGroup(MTex(r"+1", color = RED).set_stroke(**stroke_dic).scale(0.8).next_to(axis_y[0], LEFT), MTex(r"-1", color = C_DOWN).set_stroke(**stroke_dic).scale(0.8).next_to(axis_y[1], LEFT))
        label_x = MTex(r"T", color = TEAL).scale(0.8).next_to(axis_x, RIGHT)
        point_down = Dot(color = WHITE).shift(center_d)
        def get_color(t: float):
            if t > 0:
                return interpolate_color(WHITE, RED, t)
            else:
                return interpolate_color(WHITE, C_DOWN, -t)
        def shift_post_d(mob: VMobject):
            avg = arrows.avg
            mob.shift(avg*UP + T.get_value()*RIGHT).set_color(get_color(avg))
        point_down.add_post_updater(shift_post_d)
        point_cloud = DotCloud(radius = 0.01)
        def shift_post_d(mob: DotCloud):
            avg = arrows.avg
            mob.add_point(avg*UP + T.get_value()*RIGHT + center_d, color = get_color(avg))
        point_cloud.add_updater(shift_post_d)
        shade = BackgroundRectangle(VGroup(axis_x, axis_y, labels_y, label_x, point_down))
        self.add_background(point_cloud).add(axis_x, axis_y, labels_y, label_x, point_down).add_top(shade).play(FadeOut(shade))
        self.wait(5)

        thershold = 2/np.log(1+np.sqrt(2))
        self.play(T.animate.set_value(0), run_time = 2)
        self.wait()
        self.play(T.animate.set_value(1.5), run_time = 3, rate_func = linear)
        # self.wait()
        # beta.set_value(0)
        # self.play(T.animate.set_value(thershold), run_time = 5, rate_func = linear)
        T.add_updater(lambda mob: mob.increment_value(0.001))
        self.wait(55)
        # self.play(T.animate.set_value(thershold + 0.1), run_time = 2)
        # self.wait()
        T.clear_updaters()
        self.wait()
        T.add_updater(lambda mob: mob.increment_value(-0.001))
        self.wait(5)
        def gamma_updater(mob: ValueTracker):
            value = mob.get_value() + 0.2/60
            if value > 0.2:
                mob.clear_updaters().add_updater(updater_2)
                value = 0.2
            mob.set_value(value)
        def updater_2(mob: ValueTracker):
            value = mob.get_value() - 0.2/500
            if value < 0:
                mob.clear_updaters()
                value = 0
            mob.set_value(value)
        gamma.set_value(0.1).add_updater(gamma_updater)
        self.wait(50)
        # self.wait(30)
        # self.play(T.animate.set_value(3), run_time = 2)
        # self.wait()

#################################################################### 

class Video_7(FrameScene):
    def construct(self):
        centers = [LEFT_SIDE/2, RIGHT_SIDE/2]
        ratio = 0.5
        C_UP, C_DOWN = "#00AEEC", RED_E
        like = SVGMobject("like.svg", fill_opacity = 1, stroke_width = 8, stroke_color = BLACK, height = 2*ratio)[0]
        thumb_up, thumb_down = like.copy().set_fill(color = C_UP), like.copy().scale(np.array([1, -1, 1]), min_scale_factor = -1).set_fill(color = C_DOWN)
        offsets = [1.4*UP, 1.4*LEFT, 1.4*DOWN, 1.4*RIGHT]
        def shake_post(mob: VMobject):
            energy = mob.uniforms["energy"]
            angle = interpolate(mob.angle, PI/12*energy*random.uniform(-1, 1), 0.1*interpolate(1, energy, 0.5))
            mob.rotate(angle)
            mob.angle = angle
        before = VGroup(thumb_down.copy(), *[thumb_up.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = interpolate_color(C_UP, WHITE, 0.2)) for j in range(4)]).shift(centers[0])
        before[0].angle, before[0].uniforms["energy"] = 0, 5
        before[0].add_post_updater(shake_post)
        for mob in before[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 3
            mob.add_post_updater(shake_post)
        self.add(before).wait(5)

        after = VGroup(thumb_up.copy(), *[thumb_up.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = interpolate_color(C_UP, WHITE, 0.2)) for j in range(4)]).shift(centers[1])
        after[0].angle, after[0].uniforms["energy"] = 0, 1
        after[0].add_post_updater(shake_post)
        for mob in after[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 1
            mob.add_post_updater(shake_post)
        arrow_back = Polygon(2.5*RIGHT, 1*RIGHT + 1.5*UP, 1*RIGHT + 0.5*UP, 2.5*LEFT + 0.5*UP, 2.5*LEFT + 0.5*DOWN, 1*RIGHT + 0.5*DOWN, 1*RIGHT + 1.5*DOWN, stroke_width = 0, fill_opacity = 1, fill_color = GREY_E)
        self.add_background(arrow_back).play(TransformFromCopy(before, after), FlushInX(arrow_back, middle = arrow_back.get_x(LEFT) - 0.2))
        self.wait(5)

class Video_8(FrameScene):
    def construct(self):
        T = ValueTracker(4)
        np.random.random(700)
        N, M = 40, 30
        buff = 0.2
        offset_l = 2*LEFT
        C_UP, C_DOWN = "#00AEEC", RED_E
        positions = [[buff*(i-(M-1)/2)*DOWN + buff*(j-(N-1)/2)*RIGHT + offset_l for i in range(M)] for j in range(N)]
        arrow_up, arrow_down = Line(buff*0.4*DOWN, buff*0.4*UP, stroke_width = [buff*80, buff*40, 0], color = C_UP), Line(buff*0.4*UP, buff*0.4*DOWN, stroke_width = [buff*80, buff*40, 0], color = C_DOWN)
        states, outlook = np.random.randint(2, size = (N, M), dtype = int)*2-1, np.zeros((N, M), dtype = int)
        arrows = VGroup(*[VGroup(*[(arrow_up if states[j][i] == 1 else arrow_down).copy().shift(positions[j][i]) for i in range(M)]) for j in range(N)])
        arrows.states, arrows.outlook, arrows.avg = states, outlook, np.average(states)
        ratio = 0.5
        like = SVGMobject("like.svg", fill_opacity = 1, stroke_width = 8, stroke_color = BLACK, height = ratio)[0]
        thumb_up, thumb_down = like.copy().set_fill(color = C_UP), like.copy().scale(np.array([1, -1, 1]), min_scale_factor = -1).refresh_bounding_box().set_fill(color = C_DOWN)
        
        interpolate_frame = 5
        arrows_interpolate = [Line(buff*0.4*interpolate(DOWN, UP, alpha), buff*0.4*interpolate(UP, DOWN, alpha), stroke_width = [buff*80, buff*40, 0], color = interpolate_color(C_UP, C_DOWN, alpha)) for alpha in np.linspace(0, 1, interpolate_frame + 1)]
        def flip_updater(mob: VGroup):

            state = mob.states
            state_ud, state_lr = np.roll(state, 1, axis = 0) + np.roll(state, -1, axis = 0), np.roll(state, 1, axis = 1) + np.roll(state, -1, axis = 1)
            states_near = (state_ud + state_lr + np.roll(state_ud, 1, axis = 1)*0.5 + np.roll(state_ud, -1, axis = 1)*0.5)/(1+0.5)
            energy_p = -1*states_near/T.get_value()
            energy_m = -energy_p
            parts = np.exp(-energy_p), np.exp(-energy_m)
            probability = parts[0]/(parts[0]+parts[1])
            randoms = np.random.rand(N, M)

            for i in range(N):
                for j in range(M):
                    if randoms[i][j] < probability[i][j]:
                        mob.states[i][j] = 1
                        if arrows.outlook[i][j] > 0:
                            arrows.outlook[i][j] -= 1
                    else:
                        mob.states[i][j] = -1
                        if arrows.outlook[i][j] < interpolate_frame:
                            arrows.outlook[i][j] += 1
                    mob[i][j].become(arrows_interpolate[arrows.outlook[i][j]]).shift(positions[i][j])
                    mob.avg = np.average(state)

        offset_r = 4.5*RIGHT
        center_text = offset_r + 1.75*UP
        label_p = VGroup(Polygon(buff*0.8*DL, buff*0.8*DR, buff*0.8*UP, fill_color = C_UP, fill_opacity = 1), *MTex(r":", color = C_UP), thumb_up.copy()).arrange().shift(center_text + 0.6*UP).set_stroke(width = 8, color = BLACK, background = True)
        label_m = VGroup(Polygon(buff*0.8*UL, buff*0.8*UR, buff*0.8*DOWN, fill_color = C_DOWN, fill_opacity = 1), *MTex(r":", color = C_DOWN), thumb_down.copy()).arrange().shift(center_text + 0.6*DOWN).set_stroke(width = 8, color = WHITE, background = True)
        surr = SurroundingRectangle(VGroup(label_p, label_m), stroke_color = WHITE, buff = 0.4, fill_color = BACK, fill_opacity = 1)
        
        center_number = offset_r + 1.5*LEFT + 1.5*DOWN
        number_line = VGroup(Line(0.2*LEFT, 0.2*RIGHT, color = C_UP).shift(UP), Line(0.2*LEFT, 0.2*RIGHT, color = C_DOWN).shift(DOWN), 
                             Line(UP, DOWN, color = [C_UP, C_DOWN])).set_stroke(width = 8).shift(center_number)
        poles = VGroup(thumb_up.copy().next_to(number_line, UP).set_stroke(width = 0), thumb_down.copy().next_to(number_line, DOWN).set_stroke(width = 0))
        point = Dot(color = WHITE).shift(center_number)
        def shift_post(mob: VMobject):
            avg = arrows.avg
            mob.shift(avg*UP)
        point.add_post_updater(shift_post)

        digits = [MTex(str(i)) for i in range(10)]
        text_T = MTexText(r"独立性：$4.000$", tex_to_color_map = {r"独立性":YELLOW}).shift(offset_r + 1.5*DOWN + 0.5*RIGHT)
        def digit_raplace(mob: VMobject, index: int):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
        def text_T_updater(mob: MTex):
            value = 1*T.get_value()
            index, residue = int(value%10), 10*(value - int(value))
            digit_raplace(mob[4], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[6], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[7], index)
            index = int(residue)
            digit_raplace(mob[8], index)
        text_T.add_updater(text_T_updater)
        self.add_background(surr).add(arrows.add_updater(flip_updater), label_p, label_m, number_line, poles, point, text_T).wait(5)
        self.play(T.animate.set_value(1), run_time = 5)
        self.wait(10)
        self.play(T.animate.set_value(4), run_time = 5)
        self.wait(10)
        
#################################################################### 

class Video_9(FrameScene):
    def construct(self):
        offset_l = 2*DOWN + 5*LEFT
        axis_x = Arrow(0.5*LEFT, 4.5*RIGHT).shift(offset_l)
        axis_y = Arrow(0.5*DOWN, 4.5*UP).shift(offset_l)
        label_x = Songti("规模").scale(0.8).next_to(axis_x.get_end(), DOWN)
        label_y = Songti("准确率").scale(0.8).next_to(axis_y.get_end(), UP)
        graph = FunctionGraph(lambda x: x**5, [0, 1, 0.01]).scale(4, about_point = ORIGIN).shift(offset_l)
        equation = MTex(r"16384+32768=49152").shift(3*RIGHT)
        point = Dot(4*np.array([np.sqrt(1/2), np.sqrt(1/2)/4, 0]), color = YELLOW).shift(offset_l)
        line = VMobject().set_points(DashedLine(ORIGIN, 4*UP).get_all_points()).shift(offset_l + 4*np.sqrt(1/2)*RIGHT)
        self.add(axis_x, axis_y, label_x, label_y, graph, line, point, equation).wait()

        self.play(LaggedStart(*[mob.animate.set_color(GREEN).shift(0.1*UP) for mob in equation[-5:]], run_time = 2, lag_ratio = 1/4))
        self.wait()

        digits = [MTex(str(i)) for i in range(10)]
        def digit_raplace(mob: VMobject, index: int):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
            return mob
        digit_raplace(equation[-3].generate_target(), 4).set_color(RED).shift(0.2*DOWN)
        self.play(MoveToTarget(equation[-3]))
        self.wait()

        def flush_out(mob):
            mob.fill_shader_wrapper.reset_shader("mask_fill_l")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_l")
            mob.uniforms["mask_x"] = offset_l[0] - 0.2
            mob.generate_target().uniforms["mask_x"] = offset_l[0] + 4 + 0.2
        def flush_in(mob):
            mob.fill_shader_wrapper.reset_shader("mask_fill_r")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_r")
            mob.uniforms["mask_x"] = offset_l[0] - 0.2
            mob.generate_target().uniforms["mask_x"] = offset_l[0] + 4 + 0.2
        def reset(mob):
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        for mob in [graph, line, point]:
            flush_out(mob)
        graph_1 = FunctionGraph(lambda x: x, [0, 1, 0.01]).scale(4, about_point = ORIGIN).shift(offset_l)
        equation_1 = MTex(r"1+3=4").shift(3*RIGHT)
        for mob in [graph_1]:
            flush_in(mob)
        self.play(*[MoveToTarget(mob, rate_func = linear) for mob in [graph, line, point, graph_1]], Flip(equation, equation_1))
        self.remove(graph, line, point)
        for mob in [graph_1]:
            reset(mob)
        func_1 = MTex(r"y=x", color = YELLOW)
        func_1.shift(offset_l + 4*UR + 0.5*UP - func_1[1].get_center())
        tip = Songti("*为方便演示，比例尺有拉伸").scale(0.5).shift(3*LEFT + 3.5*UP)
        self.play(Write(func_1), FadeIn(tip))
        self.wait()

        copy_1 = graph_1.copy().set_stroke(color = GREY, width = 2)
        flush_out(graph_1)
        graph_2 = FunctionGraph(lambda x: x**2, [0, 1, 0.01]).scale(4, about_point = ORIGIN).shift(offset_l)
        equation_2 = MTex(r"16+32=48").shift(3*RIGHT)
        func_2 = MTex(r"y=x^2", color = YELLOW)
        func_2.shift(offset_l + 4*UR + 0.5*UP - func_2[1].get_center())
        flush_in(graph_2)
        self.add_background(copy_1).play(*[MoveToTarget(mob, rate_func = linear) for mob in [graph_1, graph_2]], 
                                   Flip(equation, equation_2), ReplacementTransform(func_1.add(func_1[-1].copy()), func_2))
        self.remove(graph_1), reset(graph_2)
        self.wait()

        copy_2 = graph_2.copy().set_stroke(color = GREY, width = 2)
        flush_out(graph_2)
        graph_3 = FunctionGraph(lambda x: x**3, [0, 1, 0.01]).scale(4, about_point = ORIGIN).shift(offset_l)
        equation_3 = MTex(r"163+327=490").shift(3*RIGHT)
        func_3 = MTex(r"y=x^3", color = YELLOW)
        func_3.shift(offset_l + 4*UR + 0.5*UP - func_3[1].get_center())
        flush_in(graph_3)
        self.add_background(copy_2).play(*[MoveToTarget(mob, rate_func = linear) for mob in [graph_2, graph_3]], 
                                   Flip(equation, equation_3), ReplacementTransform(func_2, func_3))
        self.remove(graph_2), reset(graph_3)
        self.wait()

        old_graph, old_func = graph_3, func_3
        texts = ["", "", "", "", "1638+3276=4914", "16384+32768=49152", "131072+262144=393216", "1048576+2097152=3145728", "16777216+33554432=50331648"]
        for i in range(4, 8):
            copy_i = old_graph.copy().set_stroke(color = GREY, width = 2)
            flush_out(old_graph)
            graph_i = FunctionGraph(lambda x: x**(i), [0, 1, 0.01]).scale(4, about_point = ORIGIN).shift(offset_l)
            equation_i = MTex(texts[i]).shift(3*RIGHT)
            func_i = MTex(r"y=x^"+str(i), color = YELLOW)
            func_i.shift(offset_l + 4*UR + 0.5*UP - func_i[1].get_center())
            flush_in(graph_i)
            self.add_background(copy_i).play(*[MoveToTarget(mob, rate_func = linear) for mob in [old_graph, graph_i]], 
                                       Flip(equation, equation_i), ReplacementTransform(old_func, func_i))
            self.remove(old_graph), reset(graph_i)
            old_graph, old_func = graph_i, func_i
            self.wait(1)

#################################################################### 

class Video_5_2(FrameScene):
    def construct(self):
        centers = [2.4*UP, 0.6*DOWN + 5*LEFT, 0.6*DOWN + 5*RIGHT]
        ratio = 0.4
        n = 0
        C_DOWN = "#0000FF"
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [1.0*UP, 1.0*LEFT, 1.0*DOWN, 1.0*RIGHT]
        def shake_post(mob: VMobject):
            energy = mob.uniforms["energy"]
            angle = interpolate(mob.angle, PI/12*energy*random.uniform(-1, 1), 0.1*interpolate(1, energy, 0.5))
            mob.rotate(angle)
            mob.angle = angle
        before = VGroup(arrow_up.copy(), *[(arrow_down if j < n else arrow_up).copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF" if j < n else interpolate_color(RED, WHITE, 0.2)) for j in range(4)]).shift(centers[0])
        before[0].angle, before[0].uniforms["energy"] = 0, n+1
        before[0].add_post_updater(shake_post)
        for mob in before[1:]:
            mob.angle, mob.uniforms["energy"] = 0, n/2+1
            mob.add_post_updater(shake_post)
        
        ratio = 0.3
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [0.8*UP, 0.8*LEFT, 0.8*DOWN, 0.8*RIGHT]
        energy_l = n
        case_l = VGroup(arrow_up.copy(), *[(arrow_down if j < n else arrow_up).copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF" if j < n else interpolate_color(RED, WHITE, 0.2)) for j in range(4)]).shift(centers[1])
        case_l[0].angle, case_l[0].uniforms["energy"] = 0, energy_l+1
        case_l[0].add_post_updater(shake_post)
        for mob in case_l[1:]:
            mob.angle, mob.uniforms["energy"] = 0, (energy_l)/2+1
            mob.add_post_updater(shake_post)
        text_l = MTex(r"E_{\text{磁}}="+str(energy_l*2-4)+"J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).next_to(case_l, DOWN)
        energy_r = 4-n
        case_r = VGroup(arrow_down.copy(), *[(arrow_down if j < n else arrow_up).copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF" if j < n else interpolate_color(RED, WHITE, 0.2)) for j in range(4)]).shift(centers[2])
        case_r[0].angle, case_r[0].uniforms["energy"] = 0, energy_r+1
        case_r[0].add_post_updater(shake_post)
        for mob in case_r[1:]:
            mob.angle, mob.uniforms["energy"] = 0, (energy_r)/2+1
            mob.add_post_updater(shake_post)
        text_r = MTex(r"E_{\text{磁}}="+str(energy_r*2-4)+"J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).next_to(case_r, DOWN)
        self.add(before, case_l, case_r, text_l, text_r).wait()

        arrow_l, arrow_r = Arrow(before, case_l, path_arc = PI/2), Arrow(before, case_r, path_arc = -PI/2)
        self.play(ShowCreation(arrow_l), ShowCreation(arrow_r))
        color_dic = {(str(energy_l*2-4)+r"J", str(energy_r*2-4)+r"J"): YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}
        p_l, p_r = MTex(r"\frac{e^{-\frac{"+str(energy_l*2-4)+r"J}{kT}}}{e^{-\frac{"+str(energy_l*2-4)+r"J}{kT}}+e^{-\frac{"+str(energy_r*2-4)+r"J}{kT}}}", tex_to_color_map = color_dic).scale(0.8).next_to(arrow_l.get_center(), DR).shift(0.5*UL), MTex(r"\frac{e^{-\frac{"+str(energy_r*2-4)+r"J}{kT}}}{e^{-\frac{"+str(energy_l*2-4)+r"J}{kT}}+e^{-\frac{"+str(energy_r*2-4)+r"J}{kT}}}", tex_to_color_map = color_dic).scale(0.8).next_to(arrow_r.get_center(), DL).shift(0.5*UR)
        e = np.exp(1)**((2*energy_l-4)/4)
        alpha_0 = (e)/(e+1/e)
        middle = interpolate(3.5, -3.5, alpha_0)
        bar_l, bar_r = Line(3.5*LEFT, 3.5*RIGHT, stroke_width = 100, color = RED).shift(0.6*DOWN), Line(3.5*LEFT, 3.5*RIGHT, stroke_width = 100, color = C_DOWN).shift(0.6*DOWN)
        percent_l = MTex(f"{(1-alpha_0)*100:.1f}"+r"\%", color = BLACK).save_state()
        percent_l.set_width(min(middle-(-3.5)-0.2, percent_l.get_width())).next_to(middle*RIGHT + 0.6*DOWN, LEFT, buff = 0.1)
        percent_r = MTex(f"{alpha_0*100:.1f}"+r"\%", color = WHITE).save_state()
        percent_r.set_width(min(3.5-middle-0.2, percent_r.get_width())).next_to(middle*RIGHT + 0.6*DOWN, RIGHT, buff = 0.1)
        for mob in [bar_l] + percent_l.submobjects:
            mob.fill_shader_wrapper.reset_shader("mask_fill_r")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_r")
            mob.uniforms["mask_x"] = -3.6
        bar_l.generate_target().uniforms["mask_x"] = middle
        for mob in [bar_r] + percent_r.submobjects:
            mob.fill_shader_wrapper.reset_shader("mask_fill_l")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_l")
            mob.uniforms["mask_x"] = 3.6
        bar_r.generate_target().uniforms["mask_x"] = middle
        for mob in percent_l.generate_target().submobjects + percent_r.generate_target().submobjects:
            mob.uniforms["mask_x"] = middle
        
        self.play(Write(p_l), Write(p_r), *[MoveToTarget(mob, run_time = 2, rate_func = rush_into) for mob in [bar_l, bar_r, percent_l, percent_r]])
        self.wait()

        notice = MTex(r"J:&\text{单位能量}\\T:&\text{环境温度}\\k:&\text{玻尔兹曼常数}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).scale(0.8).shift(5*RIGHT + 2.25*UP)
        text_T = MTex(r"T=04.00\frac{J}{k}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).shift(5*LEFT + 2.25*UP)
        text_T[2].set_opacity(0).shift(8*UP)
        self.play(FadeIn(notice, 0.5*LEFT), Write(text_T))
        text_T[2].shift(8*DOWN)
        self.wait()

        T = ValueTracker(1.0)
        digits = [MTex(str(i)) for i in range(10)]
        def digit_raplace(mob: VMobject, index: int):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
        def text_T_updater(mob: MTex):
            value = 4*T.get_value()
            if value < 10:
                mob[2].set_opacity(0)
            else:
                digit_raplace(mob[2], int(value/10))
            index, residue = int(value%10), 10*(value - int(value))
            digit_raplace(mob[3], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[5], index)
            index = int(residue)
            digit_raplace(mob[6], index)
        text_T.add_updater(text_T_updater)

        for mob in percent_l.submobjects + percent_r.submobjects:
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        
        def mask_updater(mob: VMobject):
            value = T.get_value()
            if 2*energy_l-4 == 0:
                    alpha = 0.5
            elif value <= 1e-3:
                alpha = int(2*energy_l-4 > 0)
            else:
                e = np.exp(1/(value/(2*energy_l-4)*4))
                alpha = e/(e+1/e)
            mob.uniforms["mask_x"] = interpolate(3.5, -3.5, alpha)
        bar_l.add_updater(mask_updater), bar_r.add_updater(mask_updater)
        def left_updater(mob: VMobject):
            value = T.get_value()
            if 2*energy_l-4 == 0:
                    alpha = 0.5
            elif value <= 1e-3:
                alpha = 1 - int(2*energy_l-4 > 0)
            else:
                e = np.exp(1/(value/(2*energy_l-4)*4))
                alpha = 1 - e/(e+1/e)
            middle = interpolate(-3.5, 3.5, alpha)
            value = min(alpha * 10, 9.99)
            mob.restore()
            if value < 1:
                mob[0].set_opacity(0)
                residue = value * 10
            else:
                index, residue = int(value), 10*(value - int(value))
                digit_raplace(mob[0], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[1], index)
            index = int(residue)
            digit_raplace(mob[3], index)
            mob.set_color(BLACK).set_width(min(middle-(-3.5)-0.2, mob.get_width())).next_to(middle*RIGHT + 0.6*DOWN, LEFT, buff = 0.1)
        percent_l.add_updater(left_updater)
        def right_updater(mob: VMobject):
            value = T.get_value()
            if 2*energy_l-4 == 0:
                    alpha = 0.5
            elif value <= 1e-3:
                alpha = int(2*energy_l-4 > 0)
            else:
                e = np.exp(1/(value/(2*energy_l-4)*4))
                alpha = e/(e+1/e)
            middle = interpolate(3.5, -3.5, alpha)
            value = min(alpha * 10, 9.99)
            mob.restore()
            if value < 1:
                mob[0].set_opacity(0)
                residue = value * 10
            else:
                index, residue = int(value), 10*(value - int(value))
                digit_raplace(mob[0], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[1], index)
            index = int(residue)
            digit_raplace(mob[3], index)
            mob.set_width(min(3.5-middle-0.2, mob.get_width())).next_to(middle*RIGHT + 0.6*DOWN, RIGHT, buff = 0.1)
        percent_l.add_updater(left_updater), percent_r.add_updater(right_updater)
        self.play(T.animate.set_value(2))
        self.wait()
        self.play(T.animate.set_value(5))
        self.wait()
        self.play(T.animate.set_value(1))
        self.wait()
        self.play(T.animate.set_value(0))
        self.wait()

class Video_5_0(FrameScene):
    def construct(self):
        centers = [2.4*UP, 0.6*DOWN + 5*LEFT, 0.6*DOWN + 5*RIGHT]
        ratio = 0.4
        C_DOWN = "#0000FF"
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [1.0*UP, 1.0*LEFT, 1.0*DOWN, 1.0*RIGHT]
        def shake_post(mob: VMobject):
            energy = mob.uniforms["energy"]
            angle = interpolate(mob.angle, PI/12*energy*random.uniform(-1, 1), 0.1*interpolate(1, energy, 0.5))
            mob.rotate(angle)
            mob.angle = angle
        before = VGroup(Polygon(ratio*UL, ratio*UR, ratio*DR, ratio*DL, stroke_width = 8, stroke_color = GREY), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[0])
        # before[0].angle, before[0].uniforms["energy"] = 0, 5
        # before[0].add_post_updater(shake_post)
        for mob in before[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 2
            mob.add_post_updater(shake_post)
        
        ratio = 0.3
        arrow_up, arrow_down = Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*UP, fill_color = RED, fill_opacity = 1, stroke_width = 0).center(), Polygon(ratio*LEFT, ratio*RIGHT, ratio*2*DOWN, fill_color = C_DOWN, fill_opacity = 1, stroke_width = 0).center()
        offsets = [0.8*UP, 0.8*LEFT, 0.8*DOWN, 0.8*RIGHT]
        case_l = VGroup(arrow_up.copy(), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[1])
        case_l[0].angle, case_l[0].uniforms["energy"] = 0, 5
        case_l[0].add_post_updater(shake_post)
        for mob in case_l[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 3
            mob.add_post_updater(shake_post)
        text_l = MTex(r"E_{\text{磁}}=4J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).next_to(case_l, DOWN)
        case_r = VGroup(arrow_down.copy(), *[arrow_down.copy().shift(offsets[j]).set_fill(opacity = 0.5, color = "#3333FF") for j in range(4)]).shift(centers[2])
        case_r[0].angle, case_r[0].uniforms["energy"] = 0, 1
        case_r[0].add_post_updater(shake_post)
        for mob in case_r[1:]:
            mob.angle, mob.uniforms["energy"] = 0, 1
            mob.add_post_updater(shake_post)
        text_r = MTex(r"E_{\text{磁}}=-4J", tex_to_color_map = {(r"E_{\text{磁}}", r"J"): YELLOW}).next_to(case_r, DOWN)
        self.add(before, case_l, case_r, text_l, text_r).wait()

        arrow_l, arrow_r = Arrow(before, case_l, path_arc = PI/2), Arrow(before, case_r, path_arc = -PI/2)
        self.play(ShowCreation(arrow_l), ShowCreation(arrow_r))
        p_l, p_r = MTex(r"\frac{e^{-\frac{4J}{kT}}}{e^{-\frac{-4J}{kT}}+e^{-\frac{4J}{kT}}}", tex_to_color_map = {(r"4J", r"-4J"): YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).scale(0.8).next_to(arrow_l.get_center(), DR).shift(0.5*UL), MTex(r"\frac{e^{-\frac{-4J}{kT}}}{e^{-\frac{-4J}{kT}}+e^{-\frac{4J}{kT}}}", tex_to_color_map = {(r"4J", r"-4J"): YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).scale(0.8).next_to(arrow_r.get_center(), DL).shift(0.5*UR)
        e = np.exp(1)
        alpha_0 = (e)/(e+1/e)
        middle = interpolate(3.5, -3.5, alpha_0)
        bar_l, bar_r = Line(3.5*LEFT, 3.5*RIGHT, stroke_width = 100, color = RED).shift(0.6*DOWN), Line(3.5*LEFT, 3.5*RIGHT, stroke_width = 100, color = C_DOWN).shift(0.6*DOWN)
        percent_l = MTex(f"{(1-alpha_0)*100:.1f}"+r"\%", color = BLACK).save_state().set_width(middle-(-3.5)-0.2).next_to(middle*RIGHT + 0.6*DOWN, LEFT, buff = 0.1)
        percent_r = MTex(f"{alpha_0*100:.1f}"+r"\%", color = WHITE).save_state().next_to(middle*RIGHT + 0.6*DOWN, RIGHT, buff = 0.1)
        for mob in [bar_l] + percent_l.submobjects:
            mob.fill_shader_wrapper.reset_shader("mask_fill_r")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_r")
            mob.uniforms["mask_x"] = -3.6
        bar_l.generate_target().uniforms["mask_x"] = middle
        for mob in [bar_r] + percent_r.submobjects:
            mob.fill_shader_wrapper.reset_shader("mask_fill_l")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_l")
            mob.uniforms["mask_x"] = 3.6
        bar_r.generate_target().uniforms["mask_x"] = middle
        for mob in percent_l.generate_target().submobjects + percent_r.generate_target().submobjects:
            mob.uniforms["mask_x"] = middle
        
        self.play(Write(p_l), Write(p_r), *[MoveToTarget(mob, run_time = 2, rate_func = rush_into) for mob in [bar_l, bar_r, percent_l, percent_r]])
        self.wait()

        notice = MTex(r"J:&\text{单位能量}\\T:&\text{环境温度}\\k:&\text{玻尔兹曼常数}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).scale(0.8).shift(5*RIGHT + 2.25*UP)
        text_T = MTex(r"T=04.00\frac{J}{k}", tex_to_color_map = {r"J":YELLOW, r"T": TEAL, r"k": LIGHT_BROWN}).shift(5*LEFT + 2.25*UP)
        text_T[2].set_opacity(0).shift(8*UP)
        self.play(FadeIn(notice, 0.5*LEFT), Write(text_T))
        text_T[2].shift(8*DOWN)
        self.wait()

        T = ValueTracker(1.0)
        digits = [MTex(str(i)) for i in range(10)]
        def digit_raplace(mob: VMobject, index: int):
            center = mob.get_center()
            mob.become(digits[index]).move_to(center)
        def text_T_updater(mob: MTex):
            value = 4*T.get_value()
            if value < 10:
                mob[2].set_opacity(0)
            else:
                digit_raplace(mob[2], int(value/10))
            index, residue = int(value%10), 10*(value - int(value))
            digit_raplace(mob[3], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[5], index)
            index = int(residue)
            digit_raplace(mob[6], index)
        text_T.add_updater(text_T_updater)

        for mob in percent_l.submobjects + percent_r.submobjects:
            mob.fill_shader_wrapper.reset_shader("quadratic_bezier_fill")
            mob.stroke_shader_wrapper.reset_shader("quadratic_bezier_stroke")
        
        def mask_updater(mob: VMobject):
            value = T.get_value()
            if value <= 1e-3:
                alpha = 1
            else:
                e = np.exp(1/value)
                alpha = e/(e+1/e)
            mob.uniforms["mask_x"] = interpolate(3.5, -3.5, alpha)
        bar_l.add_updater(mask_updater), bar_r.add_updater(mask_updater)
        def left_updater(mob: VMobject):
            value = T.get_value()
            if value <= 1e-3:
                alpha = 0
            else:
                e = np.exp(1/value)
                alpha = 1 - e/(e+1/e)
            middle = interpolate(-3.5, 3.5, alpha)
            value = min(alpha * 10, 9.99)
            mob.restore()
            if value < 1:
                mob[0].set_opacity(0)
                residue = value * 10
            else:
                index, residue = int(value), 10*(value - int(value))
                digit_raplace(mob[0], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[1], index)
            index = int(residue)
            digit_raplace(mob[3], index)
            mob.set_color(BLACK).set_width(min(middle-(-3.5)-0.2, mob.get_width())).next_to(middle*RIGHT + 0.6*DOWN, LEFT, buff = 0.1)
        percent_l.add_updater(left_updater)
        def right_updater(mob: VMobject):
            value = T.get_value()
            if value <= 1e-3:
                alpha = 1
            else:
                e = np.exp(1/value)
                alpha = e/(e+1/e)
            middle = interpolate(3.5, -3.5, alpha)
            value = min(alpha * 10, 9.99)
            mob.restore()
            if value < 1:
                mob[0].set_opacity(0)
                residue = value * 10
            else:
                index, residue = int(value), 10*(value - int(value))
                digit_raplace(mob[0], index)
            index, residue = int(residue), 10*(residue - int(residue))
            digit_raplace(mob[1], index)
            index = int(residue)
            digit_raplace(mob[3], index)
            mob.set_width(min(3.5-middle-0.2, mob.get_width())).next_to(middle*RIGHT + 0.6*DOWN, RIGHT, buff = 0.1)
        percent_l.add_updater(left_updater), percent_r.add_updater(right_updater)
        self.play(T.animate.set_value(2))
        self.wait()
        self.play(T.animate.set_value(5))
        self.wait()
        self.play(T.animate.set_value(1))
        self.wait()
        self.play(T.animate.set_value(0))
        self.wait()
        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        