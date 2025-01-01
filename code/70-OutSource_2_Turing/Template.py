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

class TuringMachine(FrameScene):
    # CONFIG = {
    #     "camera_config": {
    #         "frame_config": {"frame_shape": (FRAME_WIDTH/2, FRAME_HEIGHT/2)}, 
    #         },
    # }

    def setup(self):
        file = open("toy.txt",'r',encoding='UTF-8')
        lines = [line.strip() for line in file.readlines()]
        file.close()
        num_chars, num_states = [int(piece) for piece in lines[0].split(" ")]
        chars, states = lines[1].split(" "), lines[2].split(" ")
        dic_chars, dic_states = {chars[i]: i for i in range(num_chars)}, {states[i]: i for i in range(num_states)}
        tape_codes = lines[3].split(" ")
        for i, char in enumerate(tape_codes):
            if char not in chars:
                raise Exception(f"Unexpected tape code {char} at position {i}")
        inits = lines[4].split(" ")
        try:
            start_state = dic_states[inits[0]]
        except:
            raise Exception(f"Unexpected start state {inits[0]}")
        try:
            start_position = int(inits[1])
        except:
            raise Exception(f"Unexpected start position {inits[1]}")
        try:
            accept_state = dic_states[inits[2]]
        except:
            raise Exception(f"Unexpected accept state {inits[2]}")
        try:
            reject_state = dic_states[inits[3]]
        except:
            raise Exception(f"Unexpected reject state {inits[3]}")
        
        trans_func = [[0]*num_chars for _ in range(num_states)]
        for line in lines[5:]:
            inits = line.split(" ")
            a, b, c, d = dic_states[inits[0]], dic_chars[inits[1]], dic_states[inits[2]], dic_chars[inits[3]]
            if inits[4] == "L":
                e = 0
            elif inits[4] == "M":
                e = 1
            elif inits[4] == "R":
                e = 2
            else:
                raise Exception(f"Unexpected moving direction {inits[4]}")
            trans_func[a][b] = (c, d, e)

        self.num_chars, self.num_states = num_chars, num_states
        self.all_chars, self.all_states = chars, states
        self.dic_chars, self.dic_states = dic_chars, dic_states
        self.mtex_chars, self.mtex_states = [MTex(text, color = BLUE) for text in chars], [MTex(text, color = GREEN) for text in states]
        self.mtex_states[accept_state].set_color(YELLOW), self.mtex_states[reject_state].set_color(GREY)
        self.normal_states = list(range(self.num_states))
        self.normal_states.remove(accept_state)
        self.normal_states.remove(reject_state)
        self.dic_normal = {self.normal_states[i]: i for i in range(num_states - 2)}
        self.codes = [dic_chars[char] for char in tape_codes]
        self.state, self.position, self.accept_state, self.reject_state = start_state, start_position, accept_state, reject_state
        self.trans_func = trans_func
        self.steps = 0
        self.halt = False
    
    def construct(self):
        size = 1.2 #1.4
        show_automata = False
        show_table = False
        offset = (0.75*size)*DOWN #1*size*DOWN
        half_width, half_height = self.camera.frame.frame_shape[0]/2, self.camera.frame.frame_shape[1]/2
        visible = int(2 + half_width // size)
        height = (size - 0.1)*0.5
        
        tape = VGroup(Line(LEFT_SIDE + 2*size*LEFT, RIGHT_SIDE + 2*size*RIGHT).shift((size/2 + 0.2)*UP), 
                      Line(LEFT_SIDE + 2*size*LEFT, RIGHT_SIDE + 2*size*RIGHT).shift((size/2 + 0.2)*DOWN), 
                      *[Square(side_length = size - 0.1).shift(i*size*RIGHT) for i in range(-visible, visible + 1)]).shift(offset).save_state()
        start, end = max(0, self.position - visible - 1), min(len(self.codes), self.position + visible + 1)
        memory = VGroup(*[self.mtex_chars[self.codes[i]].copy().set_height(height).shift((i - self.position)*size*RIGHT + offset) for i in range(start, end)])
        memory.now = self.position - start

        pointer = VGroup(*[Elbow(width = size/4, color = YELLOW).shift((size/4 - 0.2)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)], 
                         Polygon(ORIGIN, 0.5*RIGHT + 0.3*UP, 0.5*LEFT + 0.3*UP, stroke_width = 0, fill_color = YELLOW_A, fill_opacity = 1).scale(size, about_point = ORIGIN).shift((size*0.6 + 0.2)*UP), 
                         Square(side_length = size - 0.1, stroke_color = YELLOW_B).shift((1.5*size + 0.2)*UP)).shift(offset)
        state = self.mtex_states[self.state].copy().set_height(height).shift((1.5*size + 0.2)*UP + offset)
        
        max_width = half_width - size*1.5
        n = self.num_chars
        m = self.num_states - 2
        size_a = min(max_width/n - 0.2, size) - 0.2
        space_a = max((max_width - size_a*n)/(n), size_a)
        full_a = size_a - 0.2 + space_a
        offset_a = half_width/2*LEFT + 0.25*LEFT + 1.75*UP
        height_a = (size_a - 0.1)*0.5
        buff_u, buff_d = 0.25*size_a + 0.3, 0.3*size_a + 0.3
        position_u, positions_d = (buff_u + (size_a-0.2)/2)*UP, [(buff_d + (size_a-0.2)/2)*DOWN + full_a*(i-(n-1)/2)*RIGHT for i in range(n)]
        if show_automata:
            automata = VGroup(Square(side_length = size_a - 0.2, stroke_color = YELLOW_B).shift(position_u), 
                            Line((n-1)/2*full_a*LEFT, (n-1)/2*full_a*RIGHT), Line(buff_u*UP, ORIGIN,), 
                            *[Square(side_length = size_a - 0.2, stroke_color = YELLOW_B).shift(positions_d[i]) for i in range(n)], 
                            *[Arrow(ORIGIN, buff_d*DOWN, buff = 0).shift(full_a*(i-(n-1)/2)*RIGHT) for i in range(n)], 
                            *[self.mtex_chars[i].copy().set_height(buff_d/2).next_to(0.5*buff_d*DOWN, buff = 0.2).shift(full_a*(i-(n-1)/2)*RIGHT) for i in range(n)], 
                            ).shift(offset_a)
            chosen = VGroup(*[Elbow(width = size_a/5, color = RED).shift((size_a/4 - 0.125)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)])
            possible_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u), 
                                    *[VGroup(self.mtex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                            self.mtex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                            MTexText([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
                                            ).shift(positions_d[i]) for i in range(n)], 
                                    chosen.copy().shift(positions_d[self.codes[self.position]])).shift(offset_a)
        
        max_height = half_height - 0.5*size
        size_b = min(max_width/(m+1), max_height/(n+1), size_a)
        height_b = (size_b - 0.1)*0.5
        offset_b = half_width/2*RIGHT + 0.25*LEFT + 2.5*UP
        if show_table:
            table = VGroup(*[self.mtex_states[self.normal_states[i]].copy().set_height(height_b).shift(size_b*(i-(m-3)/2)*RIGHT + size_b*(0-(n-1)/2)*DOWN) for i in range(m)], 
                        *[self.mtex_chars[i].copy().set_height(height_b).shift(size_b*(0-(m-1)/2)*RIGHT + size_b*(i-(n-3)/2)*DOWN) for i in range(n)], 
                        *[Line(size_b*(m/2-1)*LEFT, size_b*(m/2+1)*RIGHT).shift(size_b*(i-n/2+1)*DOWN) for i in range(n+1)], 
                        *[Line(size_b*(n/2-1)*DOWN, size_b*(n/2+1)*DOWN).shift(size_b*(i-m/2+1)*RIGHT) for i in range(m+1)], 
                        *[VGroup(self.mtex_states[self.trans_func[self.normal_states[j]][i][0]].copy().set_height(height_b/2).shift(height_b*0.35*UL), 
                                    self.mtex_chars[self.trans_func[self.normal_states[j]][i][1]].copy().set_height(height_b/2).shift(height_b*0.35*UR), 
                                    MTexText([r"向左", r"不动", r"向右"][self.trans_func[self.normal_states[j]][i][2]], color = PURPLE_B).set_height(height_b/2).shift(height_b*0.4*DOWN)
                                    ).shift(size_b*(j-(m-3)/2)*RIGHT + size_b*(i-(n-3)/2)*DOWN) for i in range(n) for j in range(m)]).shift(offset_b)
            cursor = VGroup(*[Elbow(width = size_b/5, color = RED).shift((size_b/4 - 0.05)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)]
                            ).shift(size_b*(self.dic_normal[self.state]-(m-3)/2)*RIGHT + size_b*(self.codes[self.position]-(n-3)/2)*DOWN + offset_b)

        def step():
            if self.halt:
                raise Exception(f"Already halted. Total steps: {self.steps}")
            
            now_code = self.codes[self.position]
            target = self.trans_func[self.state][now_code]
            if target == 0:
                raise Exception(f"Unexpected state for state and character {(self.all_states[self.state], self.all_chars[now_code])}")
            self.state, self.codes[self.position] = target[0], target[1]
            self.play(Flip(memory[memory.now], self.mtex_chars[target[1]].copy().set_height(height).shift((offset))), 
                      Flip(state, self.mtex_states[target[0]].copy().set_height(height).shift((1.5*size + 0.2)*UP+ offset))
                      )
            self.remove(memory[memory.now]).add(memory)

            if self.state != self.accept_state and self.state != self.reject_state:
                self.position += int(target[2] - 1)
                anims = [mob.animate.shift((target[2] - 1)*size*LEFT) for mob in [tape, memory]]
                if show_automata:
                    replace_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u), 
                                            *[VGroup(self.mtex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                                    self.mtex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                                    MTexText([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
                                                    ).shift(positions_d[i]) for i in range(n)], 
                                            chosen.copy().shift(positions_d[self.codes[self.position]])).shift(offset_a)
                    anims.extend([FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from)])
                if show_table:
                    anims.append(cursor.animate.move_to(size_b*((self.dic_normal[self.state]-(m-3)/2)*RIGHT + (self.codes[self.position]-(n-3)/2)*DOWN) + offset_b))
                self.play(*anims)
                self.wait()
                if show_automata:
                    self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))
            
                start, end = max(0, self.position - visible - 1), min(len(self.codes), self.position + visible + 1)
                memory.set_submobjects([self.mtex_chars[self.codes[i]].copy().set_height(height).shift((i - self.position)*size*RIGHT + offset) for i in range(start, end)])
                memory.now = self.position - start
                tape.restore()
            
                self.steps += 1
            else:
                anims = []
                if show_automata:
                    replace_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u + offset_a), 
                                    *[MTex(r"\not", color = GREY).set_height(height_a).shift(positions_d[i] + offset_a) for i in range(n)])
                    anims.extend([FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from)])
                if show_table:
                    anims.append(FadeOut(cursor))
                if len(anims) > 0:
                    self.play(*anims)
                    self.wait()
                if show_automata:
                    self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))

                self.halt = True
                self.steps += 1
                
        self.add(tape, memory, pointer, state)
        if show_automata:
            self.add(automata, possible_states)
        if show_table:
            self.add(table, cursor)
        self.wait()
        for _ in range(3):
            step()
        self.wait()
        
        
#################################################################### 

class Fragment_1(FrameScene):
    def construct(self):
        pic_0, pic_1, pic_2, pic_3 = [ImageMobject(f"{i}.png", height = 4).shift(1.6*UP) for i in range(4)]
        surr_big, surr_small = SurroundingRectangle(pic_0), SurroundingRectangle(pic_0.copy().scale(0.5))
        surr_0, surr_1, surr_2, surr_3 = [surr_big.copy() for _ in range(4)]
        pos_0, pos_1, pos_2, pos_3 = 1.8*DOWN + 5*LEFT, 1.8*DOWN + 1*LEFT, 1.8*DOWN + 2*RIGHT, 1.8*DOWN + 5*RIGHT
        ellipsis = MTex(r"\cdots").move_to(pos_2)
        self.wait()
        self.add(pic_0).play(ShowCreation(surr_0))
        self.wait()
        self.play(pic_0.animate.move_to(pos_0).scale(0.5), surr_0.animate.become(surr_small).move_to(pos_0))
        self.wait()
        self.add(pic_1).play(ShowCreation(surr_1))
        self.wait()
        self.play(pic_1.animate.move_to(pos_1).scale(0.5), surr_1.animate.become(surr_small).move_to(pos_1))
        self.wait()
        self.add(pic_2).play(ShowCreation(surr_2))
        self.wait()
        self.play(pic_2.animating(remover = True).move_to(pos_2).scale(0), surr_2.animating(remover = True).move_to(pos_2).scale(0), Write(ellipsis))
        self.wait()
        self.add(pic_3).play(ShowCreation(surr_3))
        self.wait()
        self.play(pic_3.animate.move_to(pos_3).scale(0.5), surr_3.animate.become(surr_small).move_to(pos_3))
        self.wait()

        pic = ImageMobject(f"TuringMachine.png", height = 8).shift(1.6*UP)
        table = ImageMobject(f"Table.png", height = 4).shift(5.5*DOWN + 3*LEFT)
        texs = MTex(r"C_0", color = YELLOW).shift(pos_0 + 1.5*DOWN), MTex(r"C_1", color = YELLOW).shift(pos_1 + 1.5*DOWN), MTex(r"\cdots").shift(pos_2 + 1.5*DOWN), MTex(r"C_n", color = YELLOW).shift(pos_3 + 1.5*DOWN)
        arrow = Arrow(texs[0], texs[1])
        self.bring_to_back(pic).play(OverFadeOut(pic, run_time = 2), self.camera.frame.animating(run_time = 2).shift(4*DOWN), *[Write(mob) for mob in texs])
        self.wait()
        self.play(IndicateAround(VGroup(surr_0, texs[0]), rect_kwargs = {"color": WHITE, "is_fixed_in_frame": False}))
        self.wait()
        self.play(IndicateAround(VGroup(surr_3, texs[3]), rect_kwargs = {"color": WHITE, "is_fixed_in_frame": False}))
        self.wait()
        self.bring_to_back(table).play(FadeIn(table, UP), GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(table), FadeOut(arrow))
        self.wait()

        proposition = MTex(r"&\text{对于图灵机}T\text{和初始格局}C_0, \\&\text{存在自然数}n\in\mathbb{N}, \\&\text{以及}n\text{个格局}C_1, \cdots, C_n,\\&\text{使得}C_n\text{停机，且}C_{i+1}=T(C_i),\ i=0, 1, \cdots, n-1", 
                           tex_to_color_map = {r"T": BLUE, (r"0", r"1", r"n", r"n+1"): GREEN, r"\mathbb{N}": PURPLE_B, (r"C_0", r"C_1", r"C_n", r"C_{i+1}", r"C_i"): YELLOW, (r"i", r"i+1"): TEAL}).scale(0.75).shift(5.5*DOWN)
        self.play(Write(proposition))
        self.wait()
        lock = SVGMobject("lock_icon.svg")
        surr = RoundedRectangle(width = proposition.get_width() + 0.5, height = proposition.get_height() + 0.5, stroke_width = 8, stroke_color = lock[1].get_fill_color()).move_to(proposition)
        lock[0].next_to(surr, UP, buff = 0)
        self.play(FadeIn(lock[0]), ShowCreation(surr), *[mob.animate.shift(0.2*UP) for mob in [pic_0, pic_1, pic_3, surr_0, surr_1, surr_3, ellipsis, *texs]])
        self.wait()
        
        
class Fragment_2(FrameScene):
    def construct(self):
        self.camera.frame.shift(1.5*LEFT)
        text = MTex(r"Q\text{会停机}", tex_to_color_map = {r"Q": YELLOW}).shift(6*LEFT)
        lock = SVGMobject("lock_icon.svg")
        surr = RoundedRectangle(width = text.get_width() + 0.5, height = text.get_height() + 0.5, stroke_width = 8, stroke_color = lock[1].get_fill_color()).move_to(text)
        lock[0].next_to(surr, UP, buff = 0)
        proposition = VGroup(lock[0], surr, text)
        # self.add(proposition)
        
        turing_K = VGroup(RoundedRectangle(width = 4, height = 4, color = BLUE_B, stroke_width = 8), 
                          MTex(r"K", color = BLUE)[0].scale(2).next_to(2*UP + 2*LEFT, DR), 
                          RoundedRectangle(width = 3.5, height = 2.5, color = BLUE_B, stroke_width = 8).shift(0.5*DOWN), )
        turing_Q = VGroup(RoundedRectangle(width = 7, height = 6, color = YELLOW_A, stroke_width = 8).shift(0.5*LEFT), 
                          MTex(r"Q", color = YELLOW)[0].scale(2).next_to(3*UP + 4*LEFT, DR), 
                          turing_K.shift(1.5*LEFT + 0.5*DOWN), )
        arrow_t = Arrow(2*RIGHT + 0.04*UP, 2*RIGHT + UP, buff = 0, color = GREEN, stroke_width = 8).reverse_points().add_line_to(1*RIGHT + 0.04*UP).reverse_points()
        arrow_t.set_stroke(width = [8, 8, 8, *arrow_t.get_stroke_widths()])
        arrow_f = Arrow(2*RIGHT + 0.04*DOWN, 2*RIGHT + DOWN, buff = 0, color = RED, stroke_width = 8).reverse_points().add_line_to(1*RIGHT + 0.04*DOWN).reverse_points()
        arrow_f.set_stroke(width = [8, 8, 8, *arrow_f.get_stroke_widths()])
        tex_t = Heiti("真", color = GREEN).next_to(1.5*RIGHT, UP)
        tex_f = Heiti("假", color = RED).next_to(1.5*RIGHT, DOWN)
        symbol_t = SVGMobject("cycle.svg", color = PURPLE_B, height = 1.2).move_to(1.8*UP + 2*RIGHT)
        symbol_f = SVGMobject("halt.svg", color = PURPLE_B, height = 1.2).move_to(1.8*DOWN + 2*RIGHT)
        self.play(FadeIn(turing_Q, LEFT))
        self.wait()
        self.play(ShowCreation(arrow_t), Write(tex_t))
        self.play(DrawBorderThenFill(symbol_t))
        self.wait()
        self.play(ShowCreation(arrow_f), Write(tex_f))
        self.play(DrawBorderThenFill(symbol_f))
        self.wait()

        self.play(Write(proposition))
        self.wait()
        base = proposition.copy()
        self.bring_to_back(base, self.shade.set_fill(opacity = 0.5)).play(proposition.animating(path_arc = PI/6).move_to(turing_K[2]))
        self.wait()

        indicate_t = Polyline(1*RIGHT + 0.04*UP, 2*RIGHT + 0.04*UP, 2*RIGHT + UP, stroke_width = 12, color = YELLOW)
        indicate_f = Polyline(1*RIGHT + 0.04*DOWN, 2*RIGHT + 0.04*DOWN, 2*RIGHT + DOWN, stroke_width = 12, color = YELLOW)
        shade_t = Rectangle(width = 1.9, height = 2.5, stroke_width = 0, fill_color = BLACK, fill_opacity = 0.5).next_to(0.9*RIGHT, UR, buff = 0)
        shade_f = Rectangle(width = 1.9, height = 2.5, stroke_width = 0, fill_color = BLACK, fill_opacity = 0.5).next_to(0.9*RIGHT, DR, buff = 0)
        self.play(ShowPassingFlash(indicate_t), FadeIn(shade_f))
        self.play(ShowPassingFlash(indicate_t))
        self.wait()
        self.play(ShowPassingFlash(indicate_f), FadeIn(shade_t), FadeOut(shade_f))
        self.play(ShowPassingFlash(indicate_f))
        self.wait()
        self.play(FadeOut(shade_t), ShowCreation(VGroup(Line(0.6*UL, 0.6*DR), Line(0.6*UR, 0.6*DL)).set_stroke(color = GREY, width = 16).shift(1.5*RIGHT)))
        self.wait()
        
        
class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        