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

class TuringMachine(Scene):

    def setup(self):
        file = open("test.txt",'r',encoding='UTF-8')
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
        size = 1.4
        show_table = True
        offset = 1*size*DOWN
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
        else:
            table = VMobject()
            cursor = VMobject()

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
                replace_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u), 
                                        *[VGroup(self.mtex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                                 self.mtex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                                 MTexText([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
                                                 ).shift(positions_d[i]) for i in range(n)], 
                                        chosen.copy().shift(positions_d[self.codes[self.position]])).shift(offset_a)
                self.play(*[mob.animate.shift((target[2] - 1)*size*LEFT) for mob in [tape, memory]], 
                          FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), 
                          FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from), 
                          cursor.animate.move_to(size_b*((self.dic_normal[self.state]-(m-3)/2)*RIGHT + (self.codes[self.position]-(n-3)/2)*DOWN) + offset_b))
                self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))
            
                start, end = max(0, self.position - visible - 1), min(len(self.codes), self.position + visible + 1)
                memory.set_submobjects([self.mtex_chars[self.codes[i]].copy().set_height(height).shift((i - self.position)*size*RIGHT + offset) for i in range(start, end)])
                memory.now = self.position - start
                tape.restore()
            
                self.steps += 1
                self.wait()
            else:
                self.steps += 1
                self.halt = True
                replace_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u + offset_a), 
                                 *[MTex(r"\not", color = GREY).set_height(height_a).shift(positions_d[i] + offset_a) for i in range(n)])
                self.play(FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), 
                          FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from), 
                          FadeOut(cursor))
                self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))
                self.wait()
            
        self.add(tape, memory, pointer, state, automata, possible_states, table, cursor)
        for _ in range(8):
            step()