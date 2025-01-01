from __future__ import annotations

from manimlib import *
import numpy as np
from pydub import AudioSegment

#################################################################### 

class Video_1(FrameScene):
    def construct(self):
        FALL, RAISE = unit(-TAU/3), unit(-PI/3)
        offset, ratio = 2.5*UP, 1.2
        
        def position(i, j):
            return offset + ratio*(i*FALL + j*RIGHT)
        pascal = VGroup(*[VGroup(*[Tex(str(choose(i, j))).shift(position(i, j)).set_stroke(**stroke_dic) for j in range(i+1)]) for i in range(9)])
        self.wait(1)
        self.play(LaggedStart(*[Write(mob, lag_ratio = 0) for mob in pascal], lag_ratio = 0.5, run_time = 2))
        self.wait()

        target = pascal.generate_target()
        for mob in target:
            mob[1:-1].fade(0.8), mob[0].set_fill(color = BLUE), mob[-1].set_fill(color = BLUE)
        self.play(MoveToTarget(pascal))
        self.wait()

        part_add = VGroup(*[Circle(radius = 0.3).move_to(position(i, j)) for i, j in [(1, 0), (1, 1), (2, 1)]])
        part_add.add(Arrow(part_add[0], part_add[2], buff = 0, stroke_color = YELLOW), Arrow(part_add[1], part_add[2], buff = 0, stroke_color = YELLOW), MTex("+", color = YELLOW)[0].next_to(part_add[2], UP))
        self.play(*[ShowCreation(mob) for mob in part_add[:3]])
        self.play(*[Write(mob) for mob in part_add[3:]], ShowCreation(pascal[2][1].copy().set_fill(opacity = 1), remover = True))
        pascal[2][1].set_fill(opacity = 1)
        self.add(part_add).wait()

        copy_add = part_add.copy()
        copy_add[:3].set_color(interpolate_color(RED, BLACK, 0.6)), copy_add[3:].set_color(interpolate_color(YELLOW, BLACK, 0.6))
        copy_add_2_1 = part_add.copy().match_style(copy_add)
        self.add(copy_add_2_1, part_add).play(part_add.animate.shift(ratio*FALL))
        self.play(ShowCreation(pascal[3][1].copy().set_fill(opacity = 1), remover = True))
        pascal[3][1].set_fill(opacity = 1)
        self.wait(1)
        copy_add_3_1 = part_add.copy().match_style(copy_add)
        self.add(copy_add_3_1, part_add).play(part_add.animate.shift(ratio*RIGHT))
        self.play(ShowCreation(pascal[3][2].copy().set_fill(opacity = 1), remover = True))
        pascal[3][2].set_fill(opacity = 1)
        self.wait()

        copy_add_3_2 = part_add.copy().match_style(copy_add)
        copies_add_4 = [part_add.copy().shift(ratio*(FALL + (i-2)*RIGHT)) for i in (1, 2, 3)]
        self.add(copy_add_3_2).remove(part_add).play(LaggedStart(*[TransformFromCopy(part_add, mob) for mob in copies_add_4], lag_ratio = 1/3, run_time = 2))
        self.play(*[ShowCreation(pascal[4][i].copy().set_fill(opacity = 1), remover = True) for i in (1, 2, 3)])
        pascal[4][1:-1].set_fill(opacity = 1)
        self.wait()

        part_add.shift(ratio*2*LEFT).match_style(copy_add)
        copies_add_5 = [part_add.match_style(copy_add).copy().shift(ratio*(2*FALL + i*RIGHT)) for i in (1, 2, 3, 4)]
        self.play(*[mob.animate.match_style(copy_add) for mob in copies_add_4], *[FadeIn(mob) for mob in copies_add_5])
        self.play(*[ShowCreation(pascal[5][i].copy().set_fill(opacity = 1), remover = True) for i in (1, 2, 3, 4)])
        pascal[5][1:-1].set_fill(opacity = 1)
        self.wait(1)
                  
        copies_add_6 = [part_add.match_style(copy_add).copy().shift(ratio*(3*FALL + i*RIGHT)) for i in (1, 2, 3, 4, 5)]
        self.play(*[FadeIn(mob) for mob in copies_add_6])
        self.play(*[ShowCreation(pascal[6][i].copy().set_fill(opacity = 1), remover = True) for i in (1, 2, 3, 4, 5)])
        pascal[6][1:-1].set_fill(opacity = 1)
        self.wait(1)

        copies_add_7 = [part_add.match_style(copy_add).copy().shift(ratio*(4*FALL + i*RIGHT)) for i in (1, 2, 3, 4, 5, 6)]
        self.play(*[FadeIn(mob) for mob in copies_add_7])
        self.play(*[ShowCreation(pascal[7][i].copy().set_fill(opacity = 1), remover = True) for i in (1, 2, 3, 4, 5, 6)])
        pascal[7][1:-1].set_fill(opacity = 1)
        self.wait(1)

        copies_add = [copy_add_2_1, copy_add_3_1, copy_add_3_2] + copies_add_4 + copies_add_5 + copies_add_6 + copies_add_7
        self.play(*[mob.animate.shift(3*LEFT) for mob in copies_add + [pascal]])
        self.wait()

        expand = MTex(r"&(1+x)^4\\=&\ 1+4x+6x^2+4x^3+1x^4", tex_to_color_map = {r"x": GREEN}).shift(3*RIGHT)
        self.play(Write(expand))
        self.wait()

        circles = VGroup(*[Circle(radius = 0.3).move_to(expand[i].get_center()) for i in (7, 9, 12, 16, 20)])
        back = BackgroundRectangle(pascal[4], color = YELLOW, fill_opacity = 0.2, buff = 0.3)
        self.add_background(back).play(Write(circles), FlushInX(back))
        self.wait()

class Video_2(FrameScene):
    def construct(self):
        FALL, RAISE = unit(-TAU/3), unit(-PI/3)
        offset, ratio = 2.5*UP, 1
        
        def position(i, j):
            return offset + ratio*(i*FALL + j*RIGHT)
        pascal = VGroup(*[VGroup(*[Tex(str(choose(i, j))).shift(position(i, j)).set_stroke(**stroke_dic) for j in range(i+1)]) for i in range(9)])
        self.add_text(*[submob for mob in pascal for submob in mob])
        self.wait()

        hexagon = Polygon(*[ratio*0.5*unit(i*PI/3 + PI/6) for i in range(6)], fill_opacity = 0.2)
        hexagons = VGroup(*[VGroup(*[hexagon.copy().shift(position(i, j)).set_color(YELLOW if choose(i, j)%2 else GREY_D) for j in range(i+1)]) for i in range(9)])

        hexagon_0 = hexagons[0][0].copy().set_color(WHITE).set_fill(opacity = 0)
        self.play(ShowCreation(hexagon_0))
        self.play(ReplacementTransform(hexagon_0, hexagons[0][0]), pascal[0][0].animate.set_fill(color = YELLOW))
        self.wait()

        self.play(*[Flip(pascal[i][j], pascal[i][j].copy().set_fill(color = YELLOW), delay = (i-1)/3, run_time = 2/3, replace = False) for i in range(1, 9) for j in (0, i)], 
                  *[Flip(pascal[i][j].copy(), hexagons[i][j], remover = True, delay = (i-1)/3, run_time = 2/3) for i in range(1, 9) for j in (0, i)], 
                  frames = 120)
        self.add(*[hexagons[i][0] for i in range(1, 9)], *[hexagons[i][-1] for i in range(1, 9)]).wait()

        hexagon_2 = hexagons[2][1].copy().set_color(WHITE).set_fill(opacity = 0)
        self.play(ShowCreation(hexagon_2))
        self.wait(1)
        self.play(ReplacementTransform(hexagon_2, hexagons[2][1]), pascal[2][1].animate.set_fill(color = GREY_D))
        self.wait()

        self.play(*[Flip(pascal[i][j], pascal[i][j].copy().set_fill(color = YELLOW if choose(i, j)%2 else GREY_D), delay = (i-3)/3, run_time = 2/3, replace = False) for i in range(3, 9) for j in range(1, i)], 
                  *[Flip(pascal[i][j].copy(), hexagons[i][j], remover = True, delay = (i-3)/3, run_time = 2/3) for i in range(3, 9) for j in range(1, i)], 
                  frames = 90)
        self.add(*[hexagons[i][j] for i in range(1, 9) for j in range(1, i)]).wait()

        self.play(FadeOut(pascal))
        self.wait()

        self.remove(hexagons)
        hexagons = VGroup(*[VGroup(*[hexagon.copy().shift(position(i, j)).set_color(YELLOW if choose(i, j)%2 else GREY_D) for j in range(i+1)]) for i in range(168)])
        scale, log_scale = 64/(5/np.sqrt(3)), np.log2(64/(5/np.sqrt(3)))
        self.add(hexagons).play(hexagons.animate.set_fill(opacity = 0.5), self.camera.frame.animate.set_height(FRAME_HEIGHT*scale).shift(((offset + ratio*UP/np.sqrt(3)) - scale*2.5*UP)), rate_func = lambda t: less_smooth((2**(log_scale*t)-1)/(scale-1)), run_time = 10)
        self.wait()

        self.play(hexagons.animate.shift(scale*LEFT_SIDE/2), run_time = 2)
        self.wait()

        vertices = [5/3*2*unit(i*TAU/3+PI/2) + 5/6*DOWN + RIGHT_SIDE/2 for i in range(3)]
        triangle_0 = Polygon(*vertices, stroke_width = 2/scale*2**6, fill_opacity = 0.5, color = YELLOW).fix_in_frame()
        triangle_0.uniforms["anti_alias_width"] = 0
        self.play(Write(triangle_0))
        self.wait()
        triangle_old = triangle_0
        for i in range(6):
            stroke_width = triangle_old.get_stroke_width()/2 if i<5 else 0
            triangles_new = VGroup(*[triangle_old.copy().scale(0.5, about_point = v) for v in vertices]).set_stroke(width = stroke_width)
            self.remove(triangle_old).play(*[TransformFromCopy(triangle_old.set_fill(opacity = 1 - 1/np.cbrt(2)), triangle_new) for triangle_new in triangles_new])
            triangle_old = triangles_new
        self.wait()

        copy_triangles = triangle_old.set_fill(opacity = 1 - 1/np.sqrt(2)).copy()
        self.play(copy_triangles.animating(run_time = 2).shift(LEFT_SIDE).set_fill(opacity = 0.5), triangle_old.animate.set_fill(opacity = 0.5))
        self.wait()

####################################################################      

class Video_3(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        
#################################################################### 

class Video_4(FrameScene):
    def construct(self):
        size = 1.2 #1.4
        size_v = np.sqrt(3)*size
        offset = ORIGIN #(0.75*size)*DOWN #1*size*DOWN
        half_width, half_height = self.camera.frame.frame_shape[0]/2, self.camera.frame.frame_shape[1]/2
        visible = int(2 + half_width // size)
        side_len = size - 0.1

        cell_p = SVGMobject("bacteria.svg", height = side_len - 0.1, fill_color = YELLOW).set_stroke(**stroke_dic)
        sound_pop = AudioSegment.from_file("pop.ogg")

        pointer_p = VGroup(*[Elbow(width = size/4, color = YELLOW).shift((size/4 - 0.2)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)])
        
        tape_p = VGroup(Line(LEFT_SIDE + 2*size*LEFT, RIGHT_SIDE + 2*size*RIGHT).shift((size/2 + 0.2)*UP), 
                      Line(LEFT_SIDE + 2*size*LEFT, RIGHT_SIDE + 2*size*RIGHT).shift((size/2 + 0.2)*DOWN), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-visible, visible + 1)]).shift(offset).save_state()
        def limit_h(mob):
            mob.fill_shader_wrapper.reset_shader("mask_fill_u")
            mob.stroke_shader_wrapper.reset_shader("mask_stroke_u")
            mob.uniforms["mask_u"] = size/2 + 0.3
        tape_0 = tape_p.copy()
        self.wait()
        self.play(FlushInX(tape_0, left = -64/9, right = 64/9, middle = -64/9), run_time = 2)
        self.wait()

        cell_0 = cell_p.copy().shift(offset)
        limit_h(cell_0[0])
        pop_updater = lambda mob: mob.restore().scale(breath(alpha.get_value()))
        alpha = ValueTracker(0.0)
        cell_0.save_state().add_updater(pop_updater)
        self.file_writer.add_audio_segment(sound_pop, time = self.get_time() + 0.5)
        self.add_text(cell_0).play(alpha.animating(remover = True).set_value(1.0))
        cell_0.clear_updaters()
        self.wait()
        
        ratio = 0.5
        tape_small_0 = VGroup(#Line(2*size*LEFT, 2*size*RIGHT).shift((size/2 + 0.2)*UP), 
                      #Line(2*size*LEFT, 2*size*RIGHT).shift((size/2 + 0.2)*DOWN), 
                      Polyline(side_len/2*UP, side_len/2*UR, side_len/2*DR, side_len/2*DOWN).shift(2*size*LEFT), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-1, 2)], 
                      Polyline(side_len/2*UP, side_len/2*UL, side_len/2*DL, side_len/2*DOWN).shift(2*size*RIGHT)).scale(ratio)
        offset_l, offset_m, offset_r, offset_u, offset_d = LEFT_SIDE*0.75, LEFT_SIDE*0.25, RIGHT_SIDE*0.25, 2.7*UP, 1.3*UP
        tapes = [VGroup(*[tape_small_0.copy().shift(offset_h + offset_v) for offset_v in [offset_u, offset_d]]) for offset_h in [offset_l, offset_m, offset_r]]
        for tape in tapes:
            tape.add(Arrow(tape[0], tape[1]))
        tapes[0][0].shift(0.4*UP), tapes[1][0].shift(0.4*UP)
        self.play(FlushInX(tapes[0][0], middle = tapes[0][0].get_x(LEFT)))
        rule_cells_1 = [cell_p.copy().scale(ratio + 0.1).move_to(mob).set_fill(color = RED) for mob in [tapes[0][0][1], tapes[0][0][3]]]
        alpha = ValueTracker(0.0)
        [cell.save_state().add_updater(pop_updater) for cell in rule_cells_1]
        self.file_writer.add_audio_segment(sound_pop, time = self.get_time() + 0.5)
        self.add_text(*rule_cells_1).play(alpha.animating(remover = True).set_value(1.0), *[mob.animate.set_color(RED) for mob in [tapes[0][0][1], tapes[0][0][3]]])
        [cell.clear_updaters() for cell in rule_cells_1]
        self.wait()

        tapes[0][1][2].set_color(RED)
        self.play(FadeIn(tapes[0][1], 0.5*DOWN), ShowCreation(tapes[0][2]))
        self.wait()

        tapes[1][0][1].set_color(ORANGE), tapes[1][0][3].set_color(ORANGE)
        self.play(FlushInX(tapes[1][0], middle = tapes[1][0].get_x(LEFT)))
        self.wait()
        tapes[1][1][2].set_color(ORANGE)
        self.play(FadeIn(tapes[1][1], 0.5*DOWN), ShowCreation(tapes[1][2]))
        self.wait()

        extra = tape_small_0.copy().shift(offset_r + offset_u + 0.8*UP)
        rule_cells_3 = [cell_p.copy().scale(ratio + 0.1).move_to(mob) for mob in [tapes[2][0][1], extra[3], tapes[2][1][2]]]
        tapes[2][0][1].set_color(YELLOW), tapes[2][0][3].set_color(YELLOW), extra[1].set_color(YELLOW), extra[3].set_color(YELLOW)
        self.play(*[FlushInX(mob, left = tapes[2][0].get_x(LEFT + 0.02), right = tapes[2][0].get_x(RIGHT + 0.02), middle = tapes[2][0].get_x(LEFT)) for mob in [tapes[2][0], extra] + rule_cells_3[:2]])
        self.wait()
        tapes[2][1][2].set_color(YELLOW)
        self.play(FadeIn(tapes[2][1], 0.5*DOWN), FadeIn(rule_cells_3[2], 0.5*DOWN), ShowCreation(tapes[2][2]))
        self.wait()

        t = MTex(r"t=0")
        t.shift(0.7*RIGHT_SIDE + 2.25*UP - t[1].get_center())
        tape_1 = tape_p.copy().shift(size_v*DOWN)
        self.play(FlushInX(tape_1, left = -64/9, right = 64/9, middle = -64/9, run_time = 2), FadeIn(t))
        self.wait()

        surr_2 = SurroundingRectangle(VGroup(tapes[2], extra), color = YELLOW)
        surr_0, surr_1 = surr_2.copy().set_color(RED).match_x(tapes[0]), surr_2.copy().set_color(ORANGE).match_x(tapes[1])
        def coor(x, y):
            return x*size*RIGHT + y*size_v*DOWN + offset
        pointer = VGroup(*[pointer_p.copy().shift(p) for p in [coor(-1, 0), coor(1, 0), coor(0, 1)]]).shift(2*size*LEFT).set_color(ORANGE)
        limit_h(cell_p[0])
        cells_1 = [cell_p.copy().shift(p) for p in [coor(-1, 1), coor(1, 1)]]
        # self.add_text(*cells_1).play(*[TransformFromCopy(cell_0, cell) for cell in cells_1])
        # pointers = [pointer_p.copy().shift(p) for p in [coor(-2, 0), coor(0, 0), coor(2, 0), coor(-1, 1), coor(1, 1)]]
        self.play(FadeIn(pointer, size*RIGHT), FadeIn(surr_1))
        self.wait(1)
        self.play(pointer.animate.shift(size*RIGHT).set_color(YELLOW), FadeOut(surr_1), FadeIn(surr_2))
        self.add_text(cells_1[0]).play(TransformFromCopy(cell_0, cells_1[0]))
        self.wait(1)
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_2), FadeIn(surr_1))
        self.wait(1)
        self.play(pointer.animate.shift(size*RIGHT).set_color(YELLOW), FadeOut(surr_1), FadeIn(surr_2))
        self.add_text(cells_1[1]).play(TransformFromCopy(cell_0, cells_1[1]))
        self.wait(1)
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_2), FadeIn(surr_1))
        self.wait(1)
        self.play(FadeOut(pointer, size*RIGHT), FadeOut(surr_1))
        self.wait()

        for mob in tape_p.get_family() + tape_0.get_family() + tape_1.get_family():
            limit_h(mob)
        target = MTex(r"t=1")
        target.shift(0.7*RIGHT_SIDE + 2.25*UP - target[1].get_center())
        self.play(*[mob.animating(remover = True).shift(size_v*UP) for mob in [tape_0, cell_0]], 
                  *[mob.animate.shift(size_v*UP) for mob in [tape_1] + cells_1], Transform(t, target))
        self.wait()

        tape_2 = tape_p.copy().shift(size_v*DOWN)
        self.play(FlushInX(tape_2, left = -64/9, right = 64/9, middle = -64/9, run_time = 2))
        for mob in tape_2.get_family():
            limit_h(mob)
        self.wait()

        # pointers = [pointer_p.copy().shift(p) for p in [coor(-3, 0), coor(-1, 0), coor(1, 0), coor(3, 0), coor(-2, 1), coor(2, 1)]]
        cells_2 = [cell_p.copy().shift(p) for p in [coor(-2, 1), coor(2, 1)]]
        wastes = [cell_p.copy().shift(p).set_fill(color = RED).scale(0) for p in [coor(0, 1), coor(0, 1)]]
        pointer.shift(5*size*LEFT)
        self.play(FadeIn(pointer, size*RIGHT), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(YELLOW), FadeOut(surr_1), FadeIn(surr_2))
        self.add_text(cells_1[0]).play(TransformFromCopy(cells_1[0], cells_2[0]))
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_2), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(RED), FadeOut(surr_1), FadeIn(surr_0))
        self.add_text(*wastes).play(TransformFromCopy(cells_1[0], wastes[0], remover = True), TransformFromCopy(cells_1[1], wastes[1], remover = True))
        self.wait(1)
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_0), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(YELLOW), FadeOut(surr_1), FadeIn(surr_2))
        self.add_text(cells_1[1]).play(TransformFromCopy(cells_1[1], cells_2[1]))
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_2), FadeIn(surr_1))
        self.play(FadeOut(pointer, size*RIGHT), FadeOut(surr_1))
        self.wait()

        target = MTex(r"t=2")
        target.shift(0.7*RIGHT_SIDE + 2.25*UP - target[1].get_center())
        self.play(*[mob.animating(remover = True).shift(size_v*UP) for mob in [tape_1] + cells_1], 
                  *[mob.animate.shift(size_v*UP) for mob in [tape_2] + cells_2], Transform(t, target))
        self.wait()

        bools_2 = [False, True, False, True, False]
        bools_3 = [False] + [bools_2[i] ^ bools_2[i+1] for i in range(2+2)] + [False]
        tape_3 = tape_p.copy().shift(size_v*DOWN)
        self.play(FlushInX(tape_3, left = -64/9, right = 64/9, middle = -64/9, run_time = 2))
        for mob in tape_3.get_family():
            limit_h(mob)
        self.wait()
        all_3, cells_3, wastes = [], [], []
        anims = []
        counter = 0
        for i in range(5):
            if bools_2[i]:
                cell = cell_p.copy().shift(coor(2*(i-1)-3, 1))
                if bools_3[i]:
                    cells_3.append(cell)
                else:
                    wastes.append(cell.set_fill(color = RED).scale(0))
                all_3.append(cell)
                anims.append(TransformFromCopy(cells_2[counter], cell))
                cell = cell_p.copy().shift(coor(2*i-3, 1))
                if bools_3[i+1]:
                    cells_3.append(cell)
                else:
                    wastes.append(cell.set_fill(color = RED).scale(0))
                all_3.append(cell)
                anims.append(TransformFromCopy(cells_2[counter], cell, remover = True))
                counter += 1
        self.add_text(*all_3).play(*anims)
        self.remove(*cells_2)

        target = MTex(r"t=3")
        target.shift(0.7*RIGHT_SIDE + 2.25*UP - target[1].get_center())
        self.play(*[mob.animating(remover = True).shift(size_v*UP) for mob in [tape_2] + cells_2], 
                  *[mob.animate.shift(size_v*UP) for mob in [tape_3] + cells_3], Transform(t, target))
        self.wait()
            
        old_tape, old_bool, old_cells = tape_3, bools_3, cells_3
        for n in range(4, 17):
            tape_i = tape_p.copy().shift(size_v*DOWN)
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            all_i, cells_i, wastes = [], [], []
            anims = []
            counter = 0
            for i in range(n+2):
                if old_bool[i]:
                    cell = cell_p.copy().shift(coor(2*(i-1)-n, 1))
                    if bools_i[i]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    cell = cell_p.copy().shift(coor(2*i-n, 1))
                    if bools_i[i+1]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    counter += 1
            self.add_text(*all_i).play(*anims, FadeIn(tape_i))

            target = MTex(r"t="+str(i))
            target.shift(0.7*RIGHT_SIDE + 2.25*UP - target[1].get_center())
            self.play(*[mob.animating(remover = True).shift(size_v*UP) for mob in [old_tape] + old_cells], 
                    *[mob.animate.shift(size_v*UP) for mob in [tape_i] + cells_i], Transform(t, target))
            if i < 8:
                self.wait(1)
            if i == 9:
                t.add(t[-1].copy())
            old_tape, old_bool, old_cells = tape_i, bools_i, cells_i

        self.file_writer.add_audio_segment(sound_pop, time = self.get_time())

class Video_5(FrameScene):
    def construct(self):
        size = 1.2 #1.4
        size_v = np.sqrt(3)*size
        offset = ORIGIN #(0.75*size)*DOWN #1*size*DOWN
        visible = 16
        side_len = size - 0.1

        cell_p = SVGMobject("bacteria.svg", height = side_len - 0.1, fill_color = YELLOW).set_stroke(**stroke_dic).set_fill(opacity = 1)

        pointer_p = VGroup(*[Elbow(width = size/4, color = YELLOW).shift((size/4 - 0.2)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)])
        
        tape_p = VGroup(Line((visible+0.5)*size*LEFT, (visible+0.5)*size*RIGHT).shift((size/2 + 0.2)*UP), 
                      Line((visible+0.5)*size*LEFT, (visible+0.5)*size*RIGHT).shift((size/2 + 0.2)*DOWN), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-visible, visible + 1)]).shift(offset).save_state()
        
        ratio = 0.5
        tape_small_0 = VGroup(Polyline(side_len/2*UP, side_len/2*UR, side_len/2*DR, side_len/2*DOWN).shift(2*size*LEFT), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-1, 2)], 
                      Polyline(side_len/2*UP, side_len/2*UL, side_len/2*DL, side_len/2*DOWN).shift(2*size*RIGHT)).scale(ratio)
        offset_l, offset_m, offset_r, offset_u, offset_d = LEFT_SIDE*0.75, LEFT_SIDE*0.25, RIGHT_SIDE*0.25, 2.7*UP, 1.3*UP
        tapes = [VGroup(*[tape_small_0.copy().shift(offset_h + offset_v) for offset_v in [offset_u, offset_d]]) for offset_h in [offset_l, offset_m, offset_r]]
        for tape in tapes:
            tape.add(Arrow(tape[0], tape[1]))
        tapes[0][0].shift(0.4*UP), tapes[1][0].shift(0.4*UP)
        extra = tape_small_0.copy().shift(offset_r + offset_u + 0.8*UP)
        tapes[2].set_submobjects([extra, *tapes[2].submobjects])
        rule_cells_1 = [cell_p.copy().scale(ratio + 0.1).move_to(mob).set_fill(color = RED) for mob in [tapes[0][0][1], tapes[0][0][3]]]
        [mob.set_color(RED) for mob in [tapes[0][0][1], tapes[0][0][3], tapes[0][1][2]]]
        tapes[1][0][1].set_color(ORANGE), tapes[1][0][3].set_color(ORANGE), tapes[1][1][2].set_color(ORANGE)
        rule_cells_3 = [cell_p.copy().scale(ratio + 0.1).move_to(mob) for mob in [tapes[2][0][3], tapes[2][1][1], tapes[2][2][2]]]
        tapes[2][0][1].set_color(YELLOW), tapes[2][0][3].set_color(YELLOW), tapes[2][1][1].set_color(YELLOW), tapes[2][1][3].set_color(YELLOW), tapes[2][2][2].set_color(YELLOW)
        self.add(*tapes, *rule_cells_1, *rule_cells_3)

        def coor(x, y):
            return x*size*RIGHT + y*size_v*DOWN + offset
        tape_0, cells_0 = tape_p.copy(), [cell_p.copy().shift(coor(0, 0))]
        t = MTex(r"t=0")
        t.shift(0.7*RIGHT_SIDE + 2.25*UP - t[1].get_center())
        self.add(tape_0, t).add_text(*cells_0).wait()

        tapes_all, cells_all = [tape_0], [cells_0[0]]
        old_tape, old_bool, old_cells = tape_0, [False, True, False], cells_0
        for n in range(1, 5):
            tape_i = old_tape.copy().shift(size_v*DOWN)
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            all_i, cells_i, wastes = [], [], []
            anims = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    cell = cell_p.copy().shift(coor(2*(i-1)-n, n))
                    if bools_i[i]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    cell = cell_p.copy().shift(coor(2*i-n, n))
                    if bools_i[i+1]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    counter += 1
            target = MTex(r"t="+str(n))
            target.shift(0.7*RIGHT_SIDE + 2.25*UP - target[1].get_center())
            anim_camera = self.camera.frame.animate.set_height(max(7, size_v*(n+2))).shift(size_v/2*DOWN)
            self.add_text(*all_i).play(*anims, FadeIn(tape_i), Transform(t, target), anim_camera, 
                                       *[mob.animate.set_stroke(opacity = mob.get_stroke_opacity() - 1/4) for mob in tapes], 
                                       *[mob.animate.set_fill(opacity = mob.get_fill_opacity() - 1/4) for mob in rule_cells_1 + rule_cells_3], 
                                       rate_func = smooth if n < 3 else less_smooth)
            old_tape, old_bool, old_cells = tape_i, bools_i, cells_i
            tapes_all.append(tape_i), cells_all.extend(cells_i)
        self.remove(*tapes, *rule_cells_1, *rule_cells_3, t)

        alpha = ValueTracker(1.0)
        # def fadeout_updater(mob: VMobject):
        #     mob.set_stroke(opacity = (alpha.get_value()) * mob.get_stroke_opacity())
        fadeout_updater = lambda mob: mob.set_stroke(opacity = (alpha.get_value()) * mob.get_stroke_opacity())
        for mob in tapes_all:
            mob.add_post_updater(fadeout_updater)
        for n in range(5, 9):
            tape_i = old_tape.copy().shift(size_v*DOWN)
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            all_i, cells_i, wastes = [], [], []
            anims = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    cell = cell_p.copy().shift(coor(2*(i-1)-n, n))
                    if bools_i[i]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    cell = cell_p.copy().shift(coor(2*i-n, n))
                    if bools_i[i+1]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    counter += 1
            anim_camera = self.camera.frame.animate.set_height(size_v*(n+2)).shift(size_v/2*DOWN)
            self.add_text(*all_i).play(*anims, FadeIn(tape_i), anim_camera, alpha.animate.increment_value(-0.25), 
                                       rate_func = linear, run_time = 0.5)
            old_tape, old_bool, old_cells = tape_i, bools_i, cells_i
            tapes_all.append(tape_i), cells_all.extend(cells_i)
        self.remove(*tapes_all, alpha)

        hexagon_p = Polygon(*[size*2*0.5*unit(i*PI/3 + PI/6) for i in range(6)], fill_opacity = 0.2, color = YELLOW)
        alpha = ValueTracker(1.0)
        beta = ValueTracker(0.0)
        fadein_updater = lambda mob: mob.fade(1 - beta.get_value())
        fadeout_updater = lambda mob: mob.set_fill(opacity = (alpha.get_value()) * mob.get_fill_opacity())
        hexagons_all = [hexagon_p.copy().add_post_updater(fadein_updater).move_to(mob.add_post_updater(fadeout_updater).set_stroke(width = 0)) for mob in cells_all]
        cell_p.add_post_updater(fadeout_updater)
        self.add(*hexagons_all)
        for n in range(9, 17):
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            all_i, all_h, cells_i, hexes_i, wastes = [], [], [], [], []
            anims = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    cell = cell_p.copy().set_stroke(width = 0).shift(coor(2*(i-1)-n, n))
                    hexagon = hexagon_p.copy().shift(coor(2*(i-1)-n, n))
                    if bools_i[i]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                        hexes_i.append(hexagon), anims.append(FadeIn(hexagon))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell), all_h.append(hexagon)
                    cell = cell_p.copy().set_stroke(width = 0).shift(coor(2*i-n, n))
                    hexagon = hexagon_p.copy().shift(coor(2*i-n, n))
                    if bools_i[i+1]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                        hexes_i.append(hexagon), anims.append(FadeIn(hexagon))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell), all_h.append(hexagon)
                    counter += 1
            anim_camera = self.camera.frame.animate.set_height(size_v*(n+2)).shift(size_v/2*DOWN)
            if n < 13:
                self.add_text(*all_i).play(*anims, anim_camera, beta.animate.increment_value(0.25), rate_func = linear, run_time = 0.5)
            else:
                self.add_text(*all_i).play(*anims, anim_camera, alpha.animate.increment_value(-0.25), rate_func = linear, run_time = 0.5)
            old_tape, old_bool, old_cells = tape_i, bools_i, cells_i
            cells_all.extend(cells_i), hexagons_all.extend(hexes_i)
        self.remove(*cells_all)

        gamma = ValueTracker(0.2)
        for mob in hexagons_all:
            mob.clear_post_updaters().add_updater(lambda mob: mob.set_fill(opacity = gamma.get_value()))
        hexagon_p.add_updater(lambda mob: mob.set_fill(opacity = gamma.get_value()))
        def fadein_updater(mob: VMobject):
            mob.counter += 1/30
            mob.fade(1 - mob.counter)
            if mob.counter >= 1:
                mob.clear_post_updaters()
        self.camera.frame.add_updater(lambda mob, dt: mob.scale(2**(dt/4), about_point = ORIGIN))
        def gamma_updater(mob, dt):
            mob.increment_value(0.4*dt/4)
            if mob.get_value() >= 0.6:
                mob.clear_updaters()
        gamma.add_updater(gamma_updater)
        self.add(self.camera.frame, gamma)

        frames, residue = int(0), 0.
        for n in range(17, 33):
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            hexes_i = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    if bools_i[i]:
                        hexagon = hexagon_p.copy().shift(coor(2*(i-1)-n, n))
                        hexes_i.append(hexagon)
                    if bools_i[i+1]:
                        hexagon = hexagon_p.copy().shift(coor(2*i-n, n))
                        hexes_i.append(hexagon)
                    counter += 1
            anim_camera = self.camera.frame.animate.set_height(size_v*(n+2)).shift(size_v/2*DOWN)
            for mob in hexes_i:
                mob.counter = - residue / 30
                mob.add_post_updater(fadein_updater)
            time = np.log2(n/16) * 120
            new_frame, residue = time//1, time%1
            self.add(*hexes_i).wait(0, int(new_frame - frames))
            frames = new_frame
            old_tape, old_bool, old_cells = tape_i, bools_i, cells_i
            hexagons_all.extend(hexes_i)

        for mob in hexagons_all:
            mob.clear_updaters().set_fill(opacity = 0.6)
        hexagon_p.clear_updaters().set_fill(opacity = 0.6)

        for p in range(5, 10):
            self.camera.frame.clear_updaters().add_updater(lambda mob, dt: mob.scale(2**(dt/4), about_point = ORIGIN))
            frames, residue = int(0), 0.
            for n in range((2**p)+1, 2*(2**p)+1):
                bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
                hexes_i = []
                counter = 0
                for i in range(1, n+2):
                    if old_bool[i]:
                        if bools_i[i]:
                            hexagon = hexagon_p.copy().shift(coor(2*(i-1)-n, n))
                            hexes_i.append(hexagon)
                        if bools_i[i+1]:
                            hexagon = hexagon_p.copy().shift(coor(2*i-n, n))
                            hexes_i.append(hexagon)
                        counter += 1
                anim_camera = self.camera.frame.animate.set_height(size_v*(n+2)).shift(size_v/2*DOWN)
                for mob in hexes_i:
                    mob.counter = - residue / 30
                    mob.add_post_updater(fadein_updater)
                time = np.log2(n/(2**p)) * 120
                new_frame, residue = time//1, time%1
                if new_frame > frames:
                    self.add(*hexes_i).wait(0, int(new_frame - frames))
                frames = new_frame
                old_tape, old_bool, old_cells = tape_i, bools_i, cells_i
                hexagons_all.extend(hexes_i)

#################################################################### 

class Video_6(FrameScene):
    def construct(self):
        size = 1.2 #1.4
        size_v = np.sqrt(3)*size
        offset = ORIGIN #(0.75*size)*DOWN #1*size*DOWN
        visible = 16
        side_len = size - 0.1

        cell_p = SVGMobject("bacteria.svg", height = side_len - 0.1, fill_color = YELLOW).set_stroke(**stroke_dic).set_fill(opacity = 1)

        ratio = 0.5
        tape_small_0 = VGroup(Polyline(side_len/2*UP, side_len/2*UR, side_len/2*DR, side_len/2*DOWN).shift(2*size*LEFT), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-1, 2)], 
                      Polyline(side_len/2*UP, side_len/2*UL, side_len/2*DL, side_len/2*DOWN).shift(2*size*RIGHT)).scale(ratio)
        offset_l, offset_r, offset_u, offset_m, offset_d = LEFT_SIDE*0.65 + 0.5*DOWN, LEFT_SIDE*0.65 + 4*DOWN, 3.5*UP, 2.7*UP, 1.3*UP
        tapes = [VGroup(*[tape_small_0.copy().shift(offset_h + offset_v) for offset_v in [offset_u, offset_m, offset_d]]) for offset_h in [offset_l, offset_r]]
        for tape in tapes:
            tape.add(Arrow(tape[1], tape[2]))
        rule_cells_1 = [cell_p.copy().scale(ratio + 0.1).move_to(mob).set_fill(color = RED) for mob in [tapes[0][0][1], tapes[0][0][3]]]
        [mob.set_color(RED) for mob in [tapes[0][0][1], tapes[0][0][3], tapes[0][1][1], tapes[0][1][3], tapes[0][2][2]]]
        rule_cells_3 = [cell_p.copy().scale(ratio + 0.1).move_to(mob) for mob in [tapes[1][0][1], tapes[1][1][3], tapes[1][2][2]]]
        tapes[1][0][1].set_color(YELLOW), tapes[1][0][3].set_color(YELLOW), tapes[1][1][1].set_color(YELLOW), tapes[1][1][3].set_color(YELLOW), tapes[1][2][2].set_color(YELLOW)
        self.add(*tapes, *rule_cells_1, *rule_cells_3)

        surr_0, surr_1 = SurroundingRectangle(tapes[0], buff = 0.2, color = RED), SurroundingRectangle(tapes[1], buff = 0.2, color = YELLOW)
        subsurr_0, subsurr_1, subsurr_2, subsurr_3 = [SurroundingRectangle(mob, color = BLUE, buff = 0.1) for mob in [tapes[0][0], tapes[0][1], tapes[1][0], tapes[1][1]]]
        surrs, subsurrs = [surr_0, surr_1], [subsurr_0, subsurr_1, subsurr_2, subsurr_3]
        FALL, RAISE = unit(-TAU/3), unit(-PI/3)
        offset, ratio = 3*UP + RIGHT_SIDE/2 + 1.8*LEFT, 1.2
        
        def position(i, j):
            return offset + ratio*(i*FALL + j*RIGHT)
        def relative(i, j):
            return ratio*(i*FALL + j*RIGHT)
        pascal = VGroup(*[VGroup(*[Tex(str(choose(i, j))).shift(position(i, j)).set_stroke(**stroke_dic) for j in range(i+1)]) for i in range(9)])
        self.add_text(*[submob for mob in pascal for submob in mob])

        hexagon = Polygon(*[ratio*0.5*unit(i*PI/3 + PI/6) for i in range(6)], fill_opacity = 0.2)
        hexagons = VGroup(*[VGroup(*[hexagon.copy().shift(position(i, j)).set_color(YELLOW if choose(i, j)%2 else GREY_D) for j in range(i+1)]) for i in range(32)])
        part_add = VGroup(*[Circle(radius = 0.3, color = BLUE).move_to(position(i, j)) for i, j in [(1, 0), (1, 1), (2, 1)]])
        part_add.add(Arrow(part_add[0], part_add[2], buff = 0, stroke_color = BLUE), Arrow(part_add[1], part_add[2], buff = 0, stroke_color = BLUE), MTex("+", color = BLUE)[0].next_to(part_add[2], UP).set_stroke(**stroke_dic))
        self.add(hexagons[0][0], *[hexagons[i][j] for i in range(1, 9) for j in (0, i)]).wait()

        self.add_text(*part_add[:3]).play(*[ShowCreation(mob) for mob in part_add[:3]], FadeIn(surr_0), FadeIn(subsurr_0))
        self.add_text(*part_add[3:]).play(*[Write(mob) for mob in part_add[3:]])
        self.play(ShowCreation(hexagons[2][1]))
        self.wait()

        def change(i: int, j: int) -> list[Animation]:
            if i == j:
                return []
            elif i//2 == j//2:
                return [FadeOut(subsurrs[i]), FadeIn(subsurrs[j])]
            else:
                return [FadeOut(surrs[i//2]), FadeIn(surrs[j//2]), FadeOut(subsurrs[i]), FadeIn(subsurrs[j])]
        self.add_text(part_add).play(part_add.animate.shift(relative(1, 0)), *change(0, 2))
        self.play(ShowCreation(hexagons[3][1]))
        self.wait()

        self.play(part_add.animate.shift(relative(0, 1)), *change(2, 3))
        self.play(ShowCreation(hexagons[3][2]))
        self.wait()

        self.play(part_add.animate.shift(relative(1, -1)), *change(3, 0))
        self.play(ShowCreation(hexagons[4][1]))
        self.play(part_add.animate.shift(relative(0, 1)), *change(0, 0))
        self.play(ShowCreation(hexagons[4][2]))
        self.play(part_add.animate.shift(relative(0, 1)), *change(0, 0))
        self.play(ShowCreation(hexagons[4][3]))
        self.wait()

        self.play(part_add.animate.shift(relative(1, -2)), *change(0, 2), FadeIn(hexagons[5][1]))
        self.play(part_add.animate.shift(relative(0, 1)), *change(2, 1), FadeIn(hexagons[5][2]))
        self.play(part_add.animate.shift(relative(0, 1)), *change(1, 1), FadeIn(hexagons[5][3]))
        self.play(part_add.animate.shift(relative(0, 1)), *change(1, 3), FadeIn(hexagons[5][4]))
        self.wait()

        self.play(FadeOut(surr_1), FadeOut(subsurr_3), FadeOut(part_add))
        self.play(FadeIn(hexagons[6][1:-1]))
        self.play(FadeIn(hexagons[7][1:-1]))
        self.add_background(hexagons).wait()

        old_bool, old_cells = [False, True, False], [cell_p.scale(0.6).copy().shift(position(0, 0))]
        t_0 = MTex(r"t=0").shift(position(0, 0))
        t_0.shift((RIGHT_SIDE[0] - 0.8 - t_0[1].get_x())*RIGHT)
        cells_all, t_all = [*old_cells], [t_0.set_stroke(**stroke_dic).fix_in_frame()]
        for n in range(1, 32):
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            cells_i = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    if bools_i[i]:
                        cell = cell_p.copy().shift(position(n, i-1))
                        cells_i.append(cell)
                    if bools_i[i+1]:
                        cell = cell_p.copy().shift(position(n, i))
                        cells_i.append(cell)
                    counter += 1
            old_bool, old_cells = bools_i, cells_i
            cells_all.extend(cells_i)
            t = MTex(r"t="+str(n)).shift(position(n, 0))
            t.shift((RIGHT_SIDE[0] - 0.8 - t[1].get_x())*RIGHT)
            t_all.append(t.set_stroke(**stroke_dic).fix_in_frame())
        self.play(FadeOut(pascal), *[FadeOut(mob) for mob in tapes + rule_cells_1 + rule_cells_3], self.camera.frame.animating(rate_func = rush_into).shift(offset[0]/2*RIGHT))
        self.add_text(*cells_all, *t_all).play(*[FadeIn(mob) for mob in cells_all + t_all], self.camera.frame.animating(rate_func = rush_from).shift(offset[0]/2*RIGHT))
        for mob in [self.camera.frame, hexagons] + cells_all:
            mob.shift(offset[0]*LEFT)
        for mob in t_all + [self.camera.frame]:
            mob.unfix_from_frame()
        self.wait()

        size = ratio/2
        size_v = np.sqrt(3)*size
        offset[0] = 0
        visible = 6
        side_len = size - 0.1
        tape_p = VGroup(Line((visible+1)*size*LEFT, (visible+1)*size*RIGHT).shift((size/2 + 0.1)*UP), 
                      Line((visible+1)*size*LEFT, (visible+1)*size*RIGHT).shift((size/2 + 0.1)*DOWN), 
                      Polyline(side_len/2*UP, side_len/2*UR, side_len/2*DR, side_len/2*DOWN).shift((visible + 1)*size*LEFT), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-visible, visible + 1)], 
                      Polyline(side_len/2*UP, side_len/2*UL, side_len/2*DL, side_len/2*DOWN).shift((visible + 1)*size*RIGHT)).set_stroke(color = GREY, width = 3).shift(offset)
        tape_3, tape_4 = tape_p.copy().shift(3*size_v*DOWN), tape_p.copy().shift(4*size_v*DOWN)
        shadow_3, shadow_4 = tape_3.copy().set_color(BLACK).set_stroke(width = 11), tape_4.copy().set_fill(color = GREY_D).set_color(BLACK).set_stroke(width = 11)
        self.play(*[FlushInX(mob, left = mob.get_x(LEFT)-0.1, right = mob.get_x(RIGHT)+.1, middle = mob.get_x(LEFT)-0.1) for mob in [shadow_3, shadow_4, tape_3, tape_4]])
        self.wait()

        def right_updater(mob: VMobject):
            width = self.camera.frame.get_width() / 2
            mob.shift((width - 0.8 - t[1].get_x())*RIGHT)
        for mob in t_all:
            mob.add_updater(right_updater)
        self.play(self.camera.frame.animate.shift(offset + size_v*7.5*DOWN).set_height(12), run_time = 2)
        visible = 10
        tape_p = VGroup(Line((visible+1)*size*LEFT, (visible+1)*size*RIGHT).shift((size/2 + 0.1)*UP), 
                      Line((visible+1)*size*LEFT, (visible+1)*size*RIGHT).shift((size/2 + 0.1)*DOWN), 
                      Polyline(side_len/2*UP, side_len/2*UR, side_len/2*DR, side_len/2*DOWN).shift((visible + 1)*size*LEFT), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-visible, visible + 1)], 
                      Polyline(side_len/2*UP, side_len/2*UL, side_len/2*DL, side_len/2*DOWN).shift((visible + 1)*size*RIGHT)).set_stroke(color = GREY, width = 3).shift(offset)
        tape_7, tape_8 = tape_p.copy().shift(7*size_v*DOWN), tape_p.copy().shift(8*size_v*DOWN)
        shadow_7, shadow_8 = tape_7.copy().set_color(BLACK).set_stroke(width = 11), tape_8.copy().set_fill(color = GREY_D).set_color(BLACK).set_stroke(width = 11)
        self.play(*[FlushInX(mob, left = mob.get_x(LEFT)-0.1, right = mob.get_x(RIGHT)+.1, middle = mob.get_x(LEFT)-0.1) for mob in [shadow_7, shadow_8, tape_7, tape_8]])
        self.wait()

        self.play(self.camera.frame.animate.shift(size_v*8*DOWN).set_height(20), run_time = 2)
        visible = 18
        tape_p = VGroup(Line((visible+1)*size*LEFT, (visible+1)*size*RIGHT).shift((size/2 + 0.1)*UP), 
                      Line((visible+1)*size*LEFT, (visible+1)*size*RIGHT).shift((size/2 + 0.1)*DOWN), 
                      Polyline(side_len/2*UP, side_len/2*UR, side_len/2*DR, side_len/2*DOWN).shift((visible + 1)*size*LEFT), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-visible, visible + 1)], 
                      Polyline(side_len/2*UP, side_len/2*UL, side_len/2*DL, side_len/2*DOWN).shift((visible + 1)*size*RIGHT)).set_stroke(color = GREY, width = 3).shift(offset)
        tape_15, tape_16 = tape_p.copy().shift(15*size_v*DOWN), tape_p.copy().shift(16*size_v*DOWN)
        shadow_15, shadow_16 = tape_15.copy().set_color(BLACK).set_stroke(width = 11), tape_16.copy().set_fill(color = GREY_D).set_color(BLACK).set_stroke(width = 11)
        self.play(*[FlushInX(mob, left = mob.get_x(LEFT)-0.1, right = mob.get_x(RIGHT)+.1, middle = mob.get_x(LEFT)-0.1) for mob in [shadow_15, shadow_16, tape_15, tape_16]])
        self.wait()
        
#################################################################### 

class Video_7(FrameScene):
    def construct(self):
        size = 1.2 #1.4
        size_v = np.sqrt(3)*size
        offset = ORIGIN #(0.75*size)*DOWN #1*size*DOWN
        visible = 16
        side_len = size - 0.1

        cell_p = SVGMobject("bacteria.svg", height = side_len - 0.1, fill_color = YELLOW).set_stroke(**stroke_dic).set_fill(opacity = 1)

        ratio = 0.5
        tape_small_0 = VGroup(Polyline(side_len/2*UP, side_len/2*UR, side_len/2*DR, side_len/2*DOWN).shift(2*size*LEFT), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-1, 2)], 
                      Polyline(side_len/2*UP, side_len/2*UL, side_len/2*DL, side_len/2*DOWN).shift(2*size*RIGHT)).scale(ratio)
        offset_l, offset_m, offset_r, offset_u, offset_d = LEFT_SIDE*0.75, LEFT_SIDE*0.25, RIGHT_SIDE*0.25, 2.7*UP, 1.3*UP
        tapes = [VGroup(*[tape_small_0.copy().shift(offset_h + offset_v) for offset_v in [offset_u, offset_d]]) for offset_h in [offset_l, offset_m, offset_r]]
        for tape in tapes:
            tape.add(Arrow(tape[0], tape[1]))
        tapes[0][0].shift(0.4*UP), tapes[1][0].shift(0.4*UP)
        extra = tape_small_0.copy().shift(offset_r + offset_u + 0.8*UP)
        tapes[2].set_submobjects([extra, *tapes[2].submobjects])
        rule_cells_1 = [cell_p.copy().scale(ratio + 0.1).move_to(mob).set_fill(color = RED) for mob in [tapes[0][0][1], tapes[0][0][3]]]
        [mob.set_color(RED) for mob in [tapes[0][0][1], tapes[0][0][3], tapes[0][1][2]]]
        tapes[1][0][1].set_color(ORANGE), tapes[1][0][3].set_color(ORANGE), tapes[1][1][2].set_color(ORANGE)
        rule_cells_3 = [cell_p.copy().scale(ratio + 0.1).move_to(mob) for mob in [tapes[2][0][3], tapes[2][1][1], tapes[2][2][2]]]
        tapes[2][0][1].set_color(YELLOW), tapes[2][0][3].set_color(YELLOW), tapes[2][1][1].set_color(YELLOW), tapes[2][1][3].set_color(YELLOW), tapes[2][2][2].set_color(YELLOW)
        surr_2 = SurroundingRectangle(VGroup(tapes[2], extra), color = YELLOW)
        surr_0, surr_1 = surr_2.copy().set_color(RED).match_x(tapes[0]), surr_2.copy().set_color(ORANGE).match_x(tapes[1])

        def coor(x, y):
            return x*size*RIGHT + y*size_v*DOWN + offset
        pointer_p = VGroup(*[Elbow(width = size/4, color = YELLOW).shift((size/4 - 0.2)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)])
        pointer = VGroup(*[pointer_p.copy().shift(p) for p in [coor(-1, 0), coor(1, 0), coor(0, 1)]]).shift(5*size*LEFT).set_color(ORANGE)
        self.add(*tapes, *rule_cells_1, *rule_cells_3)

        tape_p = VGroup(Line((visible+0.5)*size*LEFT, (visible+0.5)*size*RIGHT).shift((size/2 + 0.2)*UP), 
                      Line((visible+0.5)*size*LEFT, (visible+0.5)*size*RIGHT).shift((size/2 + 0.2)*DOWN), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-visible, visible + 1)]).shift(offset).save_state()
        tape_3, tape_4, t = tape_p.copy(), tape_p.copy().shift(size_v*DOWN), MTex(r"t=3")
        t.shift(0.7*RIGHT_SIDE + 2.25*UP - t[1].get_center())
        old_cells = [cell_p.copy().shift(coor(2*i-3, 0)) for i in range(3+1)]
        new_cells = [cell_p.copy().shift(coor(2*i-4, 1)) for i in (0, 4)]
        self.add(tape_3, tape_4, t).add_text(*old_cells).wait()
        self.play(FadeIn(pointer, size*RIGHT), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(YELLOW), FadeOut(surr_1), FadeIn(surr_2))
        self.add_text(new_cells[0]).play(TransformFromCopy(old_cells[0], new_cells[0]))
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_2), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(RED), FadeOut(surr_1), FadeIn(surr_0))
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_0), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(RED), FadeOut(surr_1), FadeIn(surr_0))
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_0), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(RED), FadeOut(surr_1), FadeIn(surr_0))
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_0), FadeIn(surr_1))
        self.play(pointer.animate.shift(size*RIGHT).set_color(YELLOW), FadeOut(surr_1), FadeIn(surr_2))
        self.add_text(new_cells[1]).play(TransformFromCopy(old_cells[-1], new_cells[1]))
        self.play(pointer.animate.shift(size*RIGHT).set_color(ORANGE), FadeOut(surr_2), FadeIn(surr_1))
        self.play(FadeOut(pointer, size*RIGHT), FadeOut(surr_1))
        self.wait()
            
#################################################################### 

class BackUp_8(FrameScene):
    def construct(self):
        size = 0.8 #1.4
        size_v = np.sqrt(3)*size
        offset = 3*UP #(0.75*size)*DOWN #1*size*DOWN
        visible = 16
        side_len = size - 0.1

        cell_p = SVGMobject("bacteria.svg", height = side_len, fill_color = YELLOW).set_stroke(**stroke_dic).set_fill(opacity = 1)
        tape_p = VGroup(Line((visible+0.5)*size*LEFT, (visible+0.5)*size*RIGHT).shift((size/2 + 0.2)*UP), 
                      Line((visible+0.5)*size*LEFT, (visible+0.5)*size*RIGHT).shift((size/2 + 0.2)*DOWN), 
                      *[Square(side_length = side_len).shift(i*size*RIGHT) for i in range(-visible, visible + 1)]).shift(offset).set_color(GREY).save_state()
        
        def coor(x, y):
            return x*size*RIGHT + y*size_v*DOWN + offset
        tape_0, cells_0 = tape_p.copy(), [cell_p.copy().shift(coor(0, 0))]
        self.add(tape_0).add_text(*cells_0)

        tapes_all, cells_all = [tape_0], [cells_0[0]]
        old_tape, old_bool, old_cells = tape_0, [False, True, False], cells_0
        def next_row(tape: VMobject, bools: list[bool]):

            tape_i = tape.copy().shift(size_v*DOWN)
            n = len(bools) - 2
            bools_i = [False] + [bools[i] ^ bools[i+1] for i in range(n+1)] + [False]
            cells_i = []
            counter = 0
            for i in range(1, n+2):
                if bools[i]:
                    cell = cell_p.copy().shift(coor(2*(i-1)-n, n))
                    if bools_i[i]:
                        cells_i.append(cell)
                    cell = cell_p.copy().shift(coor(2*i-n, n))
                    if bools_i[i+1]:
                        cells_i.append(cell)
                    counter += 1
            return tape_i, bools_i, cells_i

        for n in range(1, 5):
            tape_i = old_tape.copy().shift(size_v*DOWN)
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            cells_i = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    cell = cell_p.copy().shift(coor(2*(i-1)-n, n))
                    if bools_i[i]:
                        cells_i.append(cell)
                    cell = cell_p.copy().shift(coor(2*i-n, n))
                    if bools_i[i+1]:
                        cells_i.append(cell)
                    counter += 1
            self.add(tape_i).add_text(*cells_i)
            old_tape, old_bool, old_cells = tape_i, bools_i, cells_i
            tapes_all.append(tape_i), cells_all.extend(cells_i)
        self.wait()

class Video_8(FrameScene):
    def construct(self):
        camera = self.camera.frame
        size = 0.8 #1.4
        size_v = np.sqrt(3)*size
        offset = 3*UP #(0.75*size)*DOWN #1*size*DOWN
        visible = 16
        side_len = size - 0.1
        camera.shift(3*UP).set_height(22*size_v).shift(9*size_v*DOWN)

        cell_p = SVGMobject("bacteria.svg", height = 2*side_len - 0.1, fill_color = YELLOW).set_fill(opacity = 1)
        hexagon_p = Polygon(*[size*2*0.5*unit(i*PI/3 + PI/6) for i in range(6)], fill_opacity = 1, stroke_width = 12, stroke_color = YELLOW, fill_color = interpolate_color(BLACK, YELLOW, 0.2))
        
        def coor(x, y):
            return x*size*RIGHT + y*size_v*DOWN + offset
        def relative(x, y):
            return x*size*RIGHT + y*size_v*DOWN
        hexagons_0 = [hexagon_p.copy().shift(coor(0, 0))]
        old_bool, old_hexes = [False, True, False], hexagons_0
        all_hexes = [*hexagons_0]
        all_groups = [hexagons_0]
        for n in range(1, 9):
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            hexes_i = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    hex_i = hexagon_p.copy().shift(coor(2*(i-1)-n, n))
                    if bools_i[i]:
                        hexes_i.append(hex_i)
                    hex_i = hexagon_p.copy().shift(coor(2*i-n, n))
                    if bools_i[i+1]:
                        hexes_i.append(hex_i)
                    counter += 1
            old_bool, old_hexes = bools_i, hexes_i
            all_hexes.extend(hexes_i), all_groups.append(hexes_i)
        self.add_background(*all_hexes)
        # Animation
        self.play(*[IndicateAround(mob, rect_kwargs = {r"stroke_width": 20, "buff": 0.5, "color": RED}, layer = self.top) for mob in all_groups[-1]], 
                  *[mob.animating(run_time = 2, rate_func = double_there_and_back).scale(1.2) for mob in all_groups[-1]])
        self.wait()

        def fadein_updater(mob: VMobject):
            mob.counter += 1/30
            mob.fade(1 - mob.counter)
            if mob.counter >= 1:
                mob.clear_post_updaters()
        all_grey = []
        frames, residue = int(0), 0.
        for n in range(9, 16):
            hexes_i = []
            for i in range(n+1):
                hex_i = hexagon_p.copy().set_stroke(color = GREY_D).set_fill(color = GREY_E).shift(coor(2*i-n, n))
                hexes_i.append(hex_i)
            for mob in hexes_i:
                mob.counter = - residue / 30
                mob.add_post_updater(fadein_updater)
            time = np.log2(n/16) * 120
            new_frame, residue = time//1, time%1
            self.add(*hexes_i).wait(0, int(new_frame - frames))
            frames = new_frame
            old_bool, old_hexes = bools_i, hexes_i
            all_grey.append(hexes_i)
        questionmark = MTex(r"?", fill_color = YELLOW).shift(DOWN).scale(3).fix_in_frame().set_stroke(width = 20, color = BLACK, background = True).fix_in_frame()
        self.play(Write(questionmark))
        self.wait()

        line = Line(all_groups[-1][0], all_groups[-1][1], buff = 0.5, color = RED, stroke_width = 20)
        self.play(ShowCreation(line, start = 0.5), FadeOut(questionmark))
        self.wait()

        all_anims = []
        for n, hexes in enumerate(all_grey):
            anims = []
            for i in range(n+2):
                anims.append(hexes[i].animate.set_stroke(color = GREY_B).set_fill(color = GREY_D))
                anims.append(hexes[-i-1].animate.set_stroke(color = GREY_B).set_fill(color = GREY_D))
            all_anims.append(AnimationGroup(*anims))
        self.play(LaggedStart(*all_anims, lag_ratio = 1/4, rate_func = linear), frames = 90)
        self.wait()

        offset_l, offset_r, offset_u = coor(-8, 8), coor(8, 8), coor(0, 0)
        cell_l_0, cell_r_0, cell_u_0 = cell_p.copy().shift(offset_l), cell_p.copy().shift(offset_r), cell_p.copy().shift(offset_u)
        self.add_text(cell_l_0, cell_r_0).play(*[FadeIn(mob, scale = 0.2) for mob in [cell_l_0, cell_r_0]])
        self.wait()

        triangle_u = Polygon(all_groups[0][0].get_center() + size*2*0.5*unit(PI/2), all_groups[-1][0].get_center() + size*2*0.5*unit(PI/2), all_groups[-1][-1].get_center() + size*2*0.5*unit(PI/2), stroke_width = 12, stroke_color = BLUE_D)
        triangle_l, triangle_r = triangle_u.copy().shift(relative(-8, 8)), triangle_u.copy().shift(relative(8, 8))
        shadow_l, shadow_r, shadow_u = triangle_l.copy().set_color(BLACK).set_stroke(width = 36), triangle_r.copy().set_color(BLACK).set_stroke(width = 36), triangle_u.copy().set_color(BLACK).set_stroke(width = 36)
        self.add_text(shadow_l, shadow_r, triangle_l, triangle_r).play(ShowCreation(shadow_l), ShowCreation(shadow_r), ShowCreation(triangle_l), ShowCreation(triangle_r))
        self.wait()

        self.add_text(cell_u_0).play(FadeIn(cell_u_0, scale = 0.2))
        self.add_text(shadow_u, triangle_u).play(ShowCreation(shadow_u), ShowCreation(triangle_u.set_color(PURPLE)))
        self.wait()

        self.play(*[FadeOut(mob) for mob in [shadow_l, shadow_r, shadow_u, triangle_l, triangle_r, triangle_u, line] + [mob for mobs in all_grey for mob in mobs]])
        self.wait()

        cells_u_all, cells_l_all, cells_r_all = [cell_u_0], [cell_l_0], [cell_r_0]
        old_bool, old_cells_u, old_cells_l, old_cells_r = [False, True, False], [cell_u_0], [cell_l_0], [cell_r_0]  
        for n in range(1, 8):
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            all_i, cells_u_i, cells_l_i, cells_r_i, wastes = [], [], [], [], []
            anims = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    cell_u, cell_l, cell_r = cell_p.copy().shift(coor(2*(i-1)-n, n)), cell_p.copy().shift(coor(2*(i-1)-n, n) + relative(-8, 8)), cell_p.copy().shift(coor(2*(i-1)-n, n) + relative(8, 8))
                    if bools_i[i]:
                        cells_u_i.append(cell_u), cells_l_i.append(cell_l), cells_r_i.append(cell_r)
                        anims.append(TransformFromCopy(old_cells_u[counter], cell_u)), anims.append(TransformFromCopy(old_cells_l[counter], cell_l)), anims.append(TransformFromCopy(old_cells_r[counter], cell_r))
                    else:
                        wastes.append(cell_u.set_fill(color = RED).scale(0)), wastes.append(cell_l.set_fill(color = RED).scale(0)), wastes.append(cell_r.set_fill(color = RED).scale(0))
                        anims.append(TransformFromCopy(old_cells_u[counter], cell_u, remover = True)), anims.append(TransformFromCopy(old_cells_l[counter], cell_l, remover = True)), anims.append(TransformFromCopy(old_cells_r[counter], cell_r, remover = True))
                    all_i.append(cell_u), all_i.append(cell_l), all_i.append(cell_r)
                    cell_u, cell_l, cell_r = cell_p.copy().shift(coor(2*i-n, n)), cell_p.copy().shift(coor(2*i-n, n) + relative(-8, 8)), cell_p.copy().shift(coor(2*i-n, n) + relative(8, 8))
                    if bools_i[i+1]:
                        cells_u_i.append(cell_u), cells_l_i.append(cell_l), cells_r_i.append(cell_r)
                        anims.append(TransformFromCopy(old_cells_u[counter], cell_u)), anims.append(TransformFromCopy(old_cells_l[counter], cell_l)), anims.append(TransformFromCopy(old_cells_r[counter], cell_r))
                    else:
                        wastes.append(cell_u.set_fill(color = RED).scale(0)), wastes.append(cell_l.set_fill(color = RED).scale(0)), wastes.append(cell_r.set_fill(color = RED).scale(0))
                        anims.append(TransformFromCopy(old_cells_u[counter], cell_u, remover = True)), anims.append(TransformFromCopy(old_cells_l[counter], cell_l, remover = True)), anims.append(TransformFromCopy(old_cells_r[counter], cell_r, remover = True))
                    all_i.append(cell_u), all_i.append(cell_l), all_i.append(cell_r)
                    counter += 1
            self.add_text(*all_i).play(*anims)
            old_bool, old_cells_u, old_cells_l, old_cells_r = bools_i, cells_u_i, cells_l_i, cells_r_i
        self.wait()

        self.play(#*[ShowCreation(mob) for mob in [shadow_l, shadow_r, shadow_u, triangle_l, triangle_r, triangle_u]], 
                  *[FadeOut(mob) for mob in [mob for mobs in all_groups[1:7] for mob in mobs]])
        self.wait()

        copy_l, copy_r = [mob.copy().shift(relative(-8, 8)) for mob in all_groups[7]], [mob.copy().shift(relative(8, 8)) for mob in all_groups[7]]
        self.add_background(*copy_l).play(#TransformFromCopy(shadow_u, shadow_l.copy(), remover = True), TransformFromCopy(triangle_u, triangle_l.copy(), remover = True), 
                  *[TransformFromCopy(mob_1, mob_2, path_arc = PI/3) for mob_1, mob_2 in zip(all_groups[7], copy_l)])
        self.add_background(*copy_r).play(#TransformFromCopy(shadow_u, shadow_r.copy(), remover = True), TransformFromCopy(triangle_u, triangle_r.copy(), remover = True), 
                  *[TransformFromCopy(mob_1, mob_2, path_arc = -PI/3) for mob_1, mob_2 in zip(all_groups[7], copy_r)])
        self.wait()

        cells_all = old_cells_l + old_cells_r
        old_bool, old_cells = [False] + [True]*16 + [False], cells_all
        for n in range(16, 24):
            bools_i = [False] + [old_bool[i] ^ old_bool[i+1] for i in range(n+1)] + [False]
            all_i, cells_i, wastes = [], [], []
            anims = []
            counter = 0
            for i in range(1, n+2):
                if old_bool[i]:
                    cell = cell_p.copy().shift(coor(2*(i-1)-n, n))
                    if bools_i[i]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    cell = cell_p.copy().shift(coor(2*i-n, n))
                    if bools_i[i+1]:
                        cells_i.append(cell), anims.append(TransformFromCopy(old_cells[counter], cell))
                    else:
                        wastes.append(cell.set_fill(color = RED).scale(0)), anims.append(TransformFromCopy(old_cells[counter], cell, remover = True))
                    all_i.append(cell)
                    counter += 1
            if n == 16:
                anims.append(TransformFromCopy(copy_l[0], copy_l[0].copy().shift(relative(-1, 1))))
                anims.append(TransformFromCopy(copy_r[-1], copy_r[-1].copy().shift(relative(1, 1))))
            self.add_text(*all_i).play(*anims)
            if n == 16:
                self.wait(5)
            old_bool, old_cells = bools_i, cells_i
            cells_all.extend(cells_i)

        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        