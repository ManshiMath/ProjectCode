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
        self.mtex_states[accept_state].set_color(YELLOW), self.mtex_states[reject_state].set_color(GREY), 
        self.codes = [dic_chars[char] for char in tape_codes]
        self.state, self.position, self.accept_state, self.reject_state = start_state, start_position, accept_state, reject_state
        self.trans_func = trans_func
        self.steps = 0
        self.halt = False
    
    def construct(self):
        size = 1.4
        offset = 1*size*DOWN
        half_width = self.camera.frame.frame_shape[0]/2
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
        
        width = half_width - size*2
        n = self.num_chars
        size_a = min(width/n - 0.2, size) - 0.2
        space_a = max((width - size_a*n)/(n), size_a)

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
        possible_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u + offset_a), 
                                 *[VGroup(self.mtex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                          self.mtex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                          MTexText([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
                                          ).shift(positions_d[i] + offset_a) for i in range(n)])

        def step():
            if self.halt:
                raise Exception(f"Already halted. Total steps: {self.steps}")
            
            target = self.trans_func[self.state][self.codes[self.position]]
            if target == 0:
                raise Exception(f"Unexpected state for state and character {(self.all_states[self.state], self.all_chars[self.codes[self.position]])}")
            self.state, self.codes[self.position] = target[0], target[1]
            self.play(Flip(memory[memory.now], self.mtex_chars[target[1]].copy().set_height(height).shift((offset))), 
                      Flip(state, self.mtex_states[target[0]].copy().set_height(height).shift((1.5*size + 0.2)*UP+ offset))
                      )
            self.remove(memory[memory.now]).add(memory)

            if self.state != self.accept_state and self.state != self.reject_state:
                self.position += int(target[2] - 1)
                replace_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u + offset_a), 
                                 *[VGroup(self.mtex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                          self.mtex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                          MTexText([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
                                          ).shift(positions_d[i] + offset_a) for i in range(n)])
                self.play(*[mob.animate.shift((target[2] - 1)*size*LEFT) for mob in [tape, memory]], 
                          FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), 
                          FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from))
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
                          FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from))
                self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))
                self.wait()
            
        self.add(tape, memory, pointer, state, automata, possible_states)
        for _ in range(8):
            step()