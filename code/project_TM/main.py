from manim import *
import numpy as np

# from __future__ import annotations


class TuringMachine(VMobject):
    def __init__(self, config, init_tape, **kwargs):
        """A turing machine object. 
        Config: a dictionary of the form {state: {symbol: (new_state, new_symbol, direction)}}
        init_tape: a list of symbols to be written on the tape at the start of the simulation.
        """
        VMobject.__init__(self, **kwargs)
        self.config = config
        self.init_tape = init_tape

        # Write

class Intro(Scene):
    def construct(self):
        tm = TuringMachine({"q0": {"0": ("q0", "0", "R"), "1": ("q1", "1", "R")},
                            "q1": {"0": ("q1", "0", "R"), "1": ("q0", "1", "R")}},
                            "0"*20)
        


def pos2idx(pos):
    return (20 - pos[1])*40 + (20-pos[0])

# a moving camera scene called LangtonAnt
class LangtonAnt(MovingCameraScene):
    def construct(self):
        # Tile the whole plane with white squares, each of size 0.2. No stroke, fill with white.
        width = 0.5
        self.squares = VGroup(*[Square(width*0.95, stroke_width=0, fill_color=WHITE, fill_opacity=1).shift(DOWN*i*width + LEFT*j*width) for i in range(-20, 20) for j in range(-20, 20)])
        self.play(LaggedStart(
            Create(self.squares),
        ), run_time=3, lag_ratio=0.3)
        self.wait(2)
        # Load ant.svg from the assets folder
        self.ant = SVGMobject("ant2.svg").set_stroke(width=3, background=True)
        self.play(Create(self.ant))
        self.wait(2)
        # animate and shrink the ant to 0.2 scale
        self.play(self.ant.animate.scale(0.2))
        self.wait()

        # Move the camera closer
        self.play(self.camera.frame.animate.scale(0.3).move_to(self.ant.get_center()), run_time=3)
        self.wait()

        self.canvas = np.zeros((40, 40))
        self.dir_list = [width*UP, width*RIGHT, width*DOWN, width*LEFT]
        self.pos_change_list = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])]
        self.dir_idx = 0
        self.current_pos = np.array([0, 0])
        # The rule of Langton's ant is as follows:
        # If the ant is on a white square, turn left, flip the color of the square, and move forward one unit.
        # If the ant is on a black square, turn right, flip the color of the square, and move forward one unit.

        # Indicate the first rule
        self.play(Indicate(self.squares[pos2idx(self.current_pos)]))
        self.wait()
        # ant turn left
        self.play(Rotate(self.ant, PI/2))
        self.wait(0.5)
        # flip the color of the square
        self.play(self.squares[pos2idx(self.current_pos)].animate.set_fill(GREY_E))
        self.wait(0.5)
        # move forward one unit
        self.play(self.ant.animate.shift(self.dir_list[3]))
        self.wait()

        # Put the ant back to the center and heads to the up
        self.play(self.ant.animate.move_to(ORIGIN).rotate(-PI/2))
        self.wait()
        self.play(Indicate(self.squares[pos2idx(self.current_pos)]))
        self.wait()
        # ant turn left
        self.play(Rotate(self.ant, -PI/2))
        self.wait(0.5)
        # flip the color of the square
        self.play(self.squares[pos2idx(self.current_pos)].animate.set_fill(WHITE))
        self.wait(0.5)
        # move forward one unit
        self.play(self.ant.animate.shift(self.dir_list[1]))
        self.wait()
        self.play(self.ant.animate.move_to(ORIGIN).rotate(PI/2))
        self.wait(3)

        # Move the camera back
        self.play(self.camera.frame.animate.scale(4).move_to(ORIGIN), run_time=1)
        for _ in range(40):
            self.update(time=0.4)
    
    def update(self, time=0.5):
        """ Update the canvas, the ant's position and direction. """
        # Get the current square color
        current_square = self.canvas[self.current_pos[0]+20][self.current_pos[1]+20]
        rot_theta = PI/2 if current_square == 0 else -PI/2
        # Flip the color of the current square
        print(self.current_pos)
        self.canvas[self.current_pos[0]+20][self.current_pos[1]+20] = 1 - current_square
        # Turn left or right according to the current square color
        if current_square == 0:
            self.dir_idx = (self.dir_idx + 3) % 4
        else:
            self.dir_idx = (self.dir_idx + 1) % 4
        # Move forward one unit
        # Rotate the ant
        to_color = GREY_E if current_square == 0 else WHITE
        self.play(Rotate(self.ant, rot_theta), 
                  self.squares[pos2idx(self.current_pos)].animate.set_fill(to_color), 
                  run_time=time)
        self.current_pos = self.current_pos + self.pos_change_list[self.dir_idx]
        # Move forward the ant
        self.play(self.ant.animate.shift(self.dir_list[self.dir_idx]), run_time=time)


#################################################################### 
LEFT_SIDE = 7*LEFT
RIGHT_SIDE = 7*RIGHT

class TuringMachineNoTable(Scene):

    def setup(self):
        # file = open("test.txt",'r',encoding='UTF-8')
        file = open("BB.txt",'r',encoding='UTF-8')
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
        self.MathTex_chars, self.MathTex_states = [MathTex(text, color = BLUE) for text in chars], [MathTex(text, color = GREEN) for text in states]
        self.MathTex_states[accept_state].set_color(YELLOW), self.MathTex_states[reject_state].set_color(GREY), 
        self.codes = [dic_chars[char] for char in tape_codes]
        self.state, self.position, self.accept_state, self.reject_state = start_state, start_position, accept_state, reject_state
        self.trans_func = trans_func
        self.steps = 0
        self.halt = False
    
    def construct(self):
        size = 1.4
        offset = 1*size*DOWN
        # half_width = self.camera.frame.frame_shape[0]/2
        half_width = self.camera.frame_width / 2
        visible = int(2 + half_width // size)
        height = (size - 0.1)*0.5

        tape = VGroup(Line(LEFT_SIDE + 2*size*LEFT, RIGHT_SIDE + 2*size*RIGHT).shift((size/2 + 0.2)*UP), 
                      Line(LEFT_SIDE + 2*size*LEFT, RIGHT_SIDE + 2*size*RIGHT).shift((size/2 + 0.2)*DOWN), 
                      *[Square(side_length = size - 0.1).shift(i*size*RIGHT) for i in range(-visible, visible + 1)]).shift(offset).save_state()
        start, end = max(0, self.position - visible - 1), min(len(self.codes), self.position + visible + 1)
        memory = VGroup(*[self.MathTex_chars[self.codes[i]].copy().set_height(height).shift((i - self.position)*size*RIGHT + offset) for i in range(start, end)])
        memory.now = self.position - start

        pointer = VGroup(*[Elbow(width = size/4, color = YELLOW).shift((size/4 - 0.2)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)], 
                         Polygon(ORIGIN, 0.5*RIGHT + 0.3*UP, 0.5*LEFT + 0.3*UP, stroke_width = 0, fill_color = YELLOW_A, fill_opacity = 1).scale(size, about_point = ORIGIN).shift((size*0.6 + 0.2)*UP), 
                         Square(side_length = size - 0.1, stroke_color = YELLOW_B).shift((1.5*size + 0.2)*UP)).shift(offset)
        state = self.MathTex_states[self.state].copy().set_height(height).shift((1.5*size + 0.2)*UP + offset)
        
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
                          *[self.MathTex_chars[i].copy().set_height(buff_d/2).next_to(0.5*buff_d*DOWN, buff = 0.2).shift(full_a*(i-(n-1)/2)*RIGHT) for i in range(n)], 
                          ).shift(offset_a)
        possible_states = VGroup(self.MathTex_states[self.state].copy().set_height(height_a).shift(position_u + offset_a), 
                                 *[VGroup(self.MathTex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                          self.MathTex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                          Text([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
                                          ).shift(positions_d[i] + offset_a) for i in range(n)])

        def step():
            if self.halt:
                raise Exception(f"Already halted. Total steps: {self.steps}")
            
            target = self.trans_func[self.state][self.codes[self.position]]
            if target == 0:
                raise Exception(f"Unexpected state for state and character {(self.all_states[self.state], self.all_chars[self.codes[self.position]])}")
            self.state, self.codes[self.position] = target[0], target[1]
            self.play(Flip(memory[memory.now], self.MathTex_chars[target[1]].copy().set_height(height).shift((offset))), 
                      Flip(state, self.MathTex_states[target[0]].copy().set_height(height).shift((1.5*size + 0.2)*UP+ offset))
                      )
            self.remove(memory[memory.now]).add(memory)

            if self.state != self.accept_state and self.state != self.reject_state:
                self.position += int(target[2] - 1)
                replace_states = VGroup(self.MathTex_states[self.state].copy().set_height(height_a).shift(position_u + offset_a), 
                                 *[VGroup(self.MathTex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                          self.MathTex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                          Text([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
                                          ).shift(positions_d[i] + offset_a) for i in range(n)])
                self.play(*[mob.animate.shift((target[2] - 1)*size*LEFT) for mob in [tape, memory]], 
                          FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), 
                          FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from))
                self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))
            
                start, end = max(0, self.position - visible - 1), min(len(self.codes), self.position + visible + 1)
                memory.set_submobjects([self.MathTex_chars[self.codes[i]].copy().set_height(height).shift((i - self.position)*size*RIGHT + offset) for i in range(start, end)])
                memory.now = self.position - start
                tape.restore()
            
                self.steps += 1
                self.wait()
            else:
                self.steps += 1
                self.halt = True
                replace_states = VGroup(self.MathTex_states[self.state].copy().set_height(height_a).shift(position_u + offset_a), 
                                 *[MathTex(r"\not", color = GREY).set_height(height_a).shift(positions_d[i] + offset_a) for i in range(n)])
                self.play(FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), 
                          FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from))
                self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))
                self.wait()
            
        self.add(tape, memory, pointer, state, automata, possible_states)
        for _ in range(80):
            step()


class Flip(Animation):
    # CONFIG = {
    #     "dim": 0,
    #     "color_interpolate": False
    # }

    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject | None = None,
        dim = 0,
        color_interpolate: bool = False,
        **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.target_mobject = target_mobject
        self.dim = dim
        self.color_interpolate = color_interpolate

    def interpolate_mobject(self, alpha: float) -> None:
        if alpha <= 0.5:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 1-2*alpha
            self.mobject.become(self.starting_mobject).scale(vector)
        else:
            vector = np.array([1., 1., 1.])
            vector[self.dim] = 2*alpha-1
            self.mobject.become(self.target_mobject).scale(vector)
        if self.color_interpolate:
            self.mobject.set_color(interpolate_color(self.starting_mobject.get_color(), self.target_mobject.get_color(), alpha))
        return self

#################################################################### 

class TuringMachineBB(Scene):

    def setup(self):
        # file = open("test.txt",'r',encoding='UTF-8')
        file = open("BB.txt",'r',encoding='UTF-8')
        # file = open("ikun.txt",'r',encoding='UTF-8')
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
        self.mtex_chars, self.mtex_states = [MathTex(text, color = BLUE) for text in chars], [MathTex(text, color = GREEN) for text in states]
        self.mtex_states[accept_state].set_color(YELLOW), self.mtex_states[reject_state].set_color(GREY)
        self.normal_states = list(range(self.num_states))
        if accept_state in self.normal_states:
            self.normal_states.remove(accept_state)
        # self.normal_states.remove(accept_state)
        if reject_state in self.normal_states:
            self.normal_states.remove(reject_state)
        # self.normal_states.remove(reject_state)
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
        half_width, half_height = self.camera.frame_width / 2, self.camera.frame_height / 2
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
                                          Text([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
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
                                    Text([r"向左", r"不动", r"向右"][self.trans_func[self.normal_states[j]][i][2]], color = PURPLE_B).set_height(height_b/2).shift(height_b*0.4*DOWN)
                                    ).shift(size_b*(j-(m-3)/2)*RIGHT + size_b*(i-(n-3)/2)*DOWN) for i in range(n) for j in range(m)]).shift(offset_b)
            cursor = VGroup(*[Elbow(width = size_b/5, color = RED).shift((size_b/4 - 0.05)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)]
                            ).shift(size_b*(self.dic_normal[self.state]-(m-3)/2)*RIGHT + size_b*(self.codes[self.position]-(n-3)/2)*DOWN + offset_b)
        else:
            table = VMobject()
            cursor = VMobject()

        def step():
            if self.halt:
                # raise Exception(f"Already halted. Total steps: {self.steps}")
                return 
            
            now_code = self.codes[self.position]
            target = self.trans_func[self.state][now_code]
            if target == 0:
                raise Exception(f"Unexpected state for state and character {(self.all_states[self.state], self.all_chars[now_code])}")
            self.state, self.codes[self.position] = target[0], target[1]
            self.play(Flip(memory[memory.now], self.mtex_chars[target[1]].copy().set_height(height).shift((offset))), 
                      Flip(state, self.mtex_states[target[0]].copy().set_height(height).shift((1.5*size + 0.2)*UP+ offset)),
                      run_time = 0.5
                      )
            self.remove(memory[memory.now]).add(memory)

            if self.state != self.accept_state and self.state != self.reject_state:
                self.position += int(target[2] - 1)
                replace_states = VGroup(self.mtex_states[self.state].copy().set_height(height_a).shift(position_u), 
                                        *[VGroup(self.mtex_states[self.trans_func[self.state][i][0]].copy().set_height(height_a/2).shift(height_a*0.35*UL), 
                                                 self.mtex_chars[self.trans_func[self.state][i][1]].copy().set_height(height_a/2).shift(height_a*0.35*UR), 
                                                 Text([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
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
                                 *[MathTex(r"\not", color = GREY).set_height(height_a).shift(positions_d[i] + offset_a) for i in range(n)])
                self.play(FadeOut(possible_states, run_time = 0.5, rate_func = rush_into), 
                          FadeIn(replace_states, run_time = 0.5, delay = 0.5, rate_func = rush_from), 
                          FadeOut(cursor))
                self.remove(replace_states).add(possible_states.set_submobjects(replace_states.submobjects))
                self.wait()
            
        self.add(tape, memory, pointer, state, automata, possible_states, table, cursor)
        for _ in range(20):
            step()


class TMExplain(Scene):
    def setup(self):
        file = open("test.txt",'r',encoding='UTF-8')
        # file = open("BB.txt",'r',encoding='UTF-8')
        # file = open("ikun.txt",'r',encoding='UTF-8')
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
        self.mtex_chars, self.mtex_states = [MathTex(text, color = BLUE) for text in chars], [MathTex(text, color = GREEN) for text in states]
        self.mtex_states[accept_state].set_color(YELLOW), self.mtex_states[reject_state].set_color(GREY)
        self.normal_states = list(range(self.num_states))
        if accept_state in self.normal_states:
            self.normal_states.remove(accept_state)
        # self.normal_states.remove(accept_state)
        if reject_state in self.normal_states:
            self.normal_states.remove(reject_state)
        # self.normal_states.remove(reject_state)
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
        half_width, half_height = self.camera.frame_width / 2, self.camera.frame_height / 2
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
                                          Text([r"向左", r"不动", r"向右"][self.trans_func[self.state][i][2]], color = PURPLE_B).set_height(height_a/2).shift(height_a*0.4*DOWN)
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
                                    Text([r"向左", r"不动", r"向右"][self.trans_func[self.normal_states[j]][i][2]], color = PURPLE_B).set_height(height_b/2).shift(height_b*0.4*DOWN)
                                    ).shift(size_b*(j-(m-3)/2)*RIGHT + size_b*(i-(n-3)/2)*DOWN) for i in range(n) for j in range(m)]).shift(offset_b)
            cursor = VGroup(*[Elbow(width = size_b/5, color = RED).shift((size_b/4 - 0.05)*UR).rotate(i*PI/2, about_point = ORIGIN) for i in range(4)]
                            ).shift(size_b*(self.dic_normal[self.state]-(m-3)/2)*RIGHT + size_b*(self.codes[self.position]-(n-3)/2)*DOWN + offset_b)
        else:
            table = VMobject()
            cursor = VMobject()
            
        # self.play(FadeIn(tape), FadeIn(memory))
        # self.play(Create(pointer))
        # self.play(FadeIn(table))
        self.play(
            LaggedStart(
                FadeIn(tape), FadeIn(memory),
                Create(pointer), FadeIn(state),
                FadeIn(table)
            ), run_time=2
        )
        self.wait(1.5)

        tape_lbl = Text("纸带", color = YELLOW).next_to(tape, UP, buff=0.2).shift(LEFT*4)
        pointer_lbl = Text("表头", color = YELLOW).next_to(pointer, LEFT+UP)
        table_lbl = Text("操作规则", color = YELLOW).move_to(table).set_stroke(width=5, background=True)
        self.play(
            LaggedStart(Write(tape_lbl), Write(pointer_lbl), Write(table_lbl), lag_ratio = 0.5),
            run_time=2
        )
        self.wait(2)

        # FadeOut everything except tape, memory, and tape_lbl
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [tape, memory, tape_lbl]]
        )
        self.wait(3)

        # FadeIn pointer and state
        self.play(
            FadeOut(tape_lbl),
            LaggedStart(
                FadeIn(pointer), FadeIn(state),
                FadeIn(pointer_lbl), 
                lag_ratio = 0.5
            )
        )
        self.wait(3)
        self.play(
            FadeIn(table)
        )
        self.wait(3)
        
  
from manim import *
import numpy as np

class TaiGang(Scene):
    def construct(self):
        t1 = Text("毕导,").scale(1.5).shift(LEFT*4).set_color(RED)
        t2 = Text("你讲的").scale(1.5).next_to(t1, RIGHT, buff=0.2).set_color(ORANGE)
        t3 = Text("太落后了", font='heiti').scale(2).next_to(t2, RIGHT, buff=0.2).set_color(YELLOW)

        self.play(FadeIn(t1), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(t2), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(t3), run_time=1)
        self.wait(1.5)

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

        self.wait(3)

        notmath = Text("数学", color=BLUE).scale(1.5).shift(LEFT*3)
        cross1 = Cross(notmath, stroke_width=10, color=RED)
        notlogic = Text("逻辑学", color=MAROON).scale(1.5).shift(RIGHT*3)
        cross2 = Cross(notlogic, stroke_width=10, color=RED)
        self.play(Write(notmath), run_time=0.5)
        self.play(Create(cross1), run_time=0.5)
        self.wait(0.5)
        self.play(Write(notlogic), run_time=0.5)
        self.play(Create(cross2), run_time=0.5)
        self.wait(0.8)

        iscomputer = Text("计算机", font='heiti', color=YELLOW).scale(2.5).shift(UP)
        tick = MathTex(r"\checkmark", color=GREEN).scale(2.5).next_to(iscomputer, RIGHT, buff=0.5)
        self.play(
            notmath.animate.shift(DOWN*2),
            notlogic.animate.shift(DOWN*2),
            cross1.animate.shift(DOWN*2),
            cross2.animate.shift(DOWN*2),
            DrawBorderThenFill(iscomputer), 
            run_time=2)
        self.play(Write(tick), run_time=0.5)
        self.wait(1.5)


class Prelude(Scene):
    def construct(self):
        tg = Tex("M", "athematic", "S").scale(2.5)
        tg[0].set_color(BLUE)
        #tg[1].set_color(GREEN)
        tg[2].set_color(MAROON_A)
        self.play(
            DrawBorderThenFill(tg),
            run_time=2
        )

        self.wait(1)
        name = Text("漫士沉思录", color=YELLOW).scale(1.8).shift(DOWN*0.5)
        self.play(
            FadeOut(tg[1]),
            tg[0].animate.shift(RIGHT * 3+UP*2),
            tg[2].animate.shift(LEFT * 3+UP*1.8),
            DrawBorderThenFill(name),
            run_time=2,
            lag_ratio=0.7
        )
        self.wait(1)
        t2 = Text("踢馆sub(n,n,17)", font='heiti', color=RED).next_to(name, DOWN, buff=0.5)
        self.play(
            Write(t2),
            run_time=1
        )
        self.wait(1.5)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class ThreeLines(Scene):
    def construct(self):
        line1 = Text("可以构造一个图灵机K，为F中任何可判定的命题给出证明").scale(0.8).shift(UP*1.5).set_color(YELLOW)
        line2 = Text("如果F完备，则K能够对任何命题停机并给出回答").scale(0.8).set_color(YELLOW).align_to(line1, LEFT)
        line3 = Text("是否停机也是命题，所以K能够判定停机问题，矛盾").scale(0.8).shift(DOWN*1.5).set_color(YELLOW).align_to(line1, LEFT)

        self.play(
            LaggedStart(Write(line1),
                        Write(line2),
                        Write(line3),
                        lag_ratio=0.5,
                        run_time=3
                        )
        )
        self.wait(4)

        # grey_line1 = line1.copy().set_color(DARK_GREY)
        # grey_line2 = line2.copy().set_color(DARK_GREY)
        # grey_line3 = line3.copy().set_color(DARK_GREY)

        self.play(
            # line1.animate.scale(1.25),
            line2.animate.set_color(DARK_GREY),
            line3.animate.set_color(DARK_GREY),
            run_time=1.5
        )
        self.wait(2)

        self.play(
            line1.animate.set_color(DARK_GREY),
            line2.animate.set_color(YELLOW),
            run_time=1.5
        )
        self.wait(2)

        self.play(
            line2.animate.set_color(DARK_GREY),
            line3.animate.set_color(YELLOW),
            run_time=1.5
        )
        self.wait(2)

class TMDemo(Scene):
    def construct(self):
        text = Text("人是如何思考和计算的？", font='heiti').scale(1.5).set_color(YELLOW)
        self.wait(2)
        self.play(Write(text))
        self.wait(2)

class Fuse(Scene):
    def construct(self):
        brain = SVGMobject("brain.svg").set_color(PINK).shift(LEFT*2)

        model = Text("模型").scale(2).shift(RIGHT*3).set_color(BLUE)
        self.play(
            FadeIn(brain),
            run_time=1
        )
        self.wait(1)
        Arr = Arrow(brain.get_right(), model.get_left(), buff=0.1)
        self.play(
            TransformFromCopy(brain, model),
            GrowArrow(Arr),
            run_time=1.5
        )
        self.wait(2)

        TM = Text("图灵机 Turing Machine", font='heiti').scale(1.2).set_color(YELLOW).to_edge(UP)
        self.play(
            Write(TM),
            run_time=1.5
        )
        self.wait(2)


class UnivTM(Scene):
    def construct(self):
        question = Text("这个世界上真的有图灵机吗？").set_color(RED).shift(UP*3)

        answer = Text("有", font='heiti').set_color(GREEN).scale(2).shift(LEFT*2.5)
        answer2 = Text("也没有", font='heiti').set_color(BLUE).scale(2).next_to(answer, RIGHT, buff=1)

        self.play(Write(question))
        self.wait(2)
        self.play(Write(answer))
        self.play(Write(answer2))
        self.wait(3)

class Undecide(Scene):
    def construct(self):
        text = Text("会停吗？不知道").set_color(YELLOW).scale(2)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1.5)
        self.play(FadeOut(text))

class BusyBeaver(Scene):
    def construct(self):
        
        ten = MathTex(r"10", color=YELLOW).scale(3).shift(DOWN+LEFT*2)
        greater = MathTex(r">", color=RED).scale(3).next_to(ten, LEFT, buff=0.2)
        ten1 = ten.copy().scale(0.8).next_to(ten, UP+RIGHT, buff=0.1)
        ten2 = ten1.copy().scale(0.8).next_to(ten1, UP+RIGHT, buff=0.1)
        ten3 = ten2.copy().scale(0.8).next_to(ten2, UP+RIGHT, buff=0.1)
        dots = MathTex(r"\ddots", color=YELLOW).scale(2).next_to(ten3, UP+RIGHT, buff=0.1).rotate(-0.6*PI)
        last_ten = ten3.copy().scale(0.8).next_to(dots, UP+RIGHT, buff=0.1)
        
        bracket = BraceLabel(VGroup(ten,ten1,ten2,ten3,last_ten), "15", DOWN, buff=0.1, font_size=60).set_color(BLUE)

        self.add(greater)
        self.play(Write(ten), run_time=0.4)
        self.wait(0.2)
        self.play(Write(ten1), run_time=0.4)
        self.wait(0.2)
        self.play(Write(ten2), run_time=0.4)
        self.wait(0.4)
        self.play(Write(ten3), run_time=0.4)
        self.wait(0.2)
        self.play(Write(dots), run_time=1)
        self.play(Write(last_ten), run_time=0.5)
        self.wait(0.3)
        self.play(Write(bracket), run_time=1.5)
        self.wait(2)

class Reduction(Scene):
    def construct(self):
        title = Text("规约").set_color(YELLOW).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN, buff=0.1)
        self.play(
            Write(title),
            GrowFromCenter(line),
        )
        self.wait(1)
        questiona = Text("A").scale(4).set_color(MAROON).shift(LEFT*3)
        questionb = Text("B").scale(4).set_color(RED).shift(RIGHT*3)
        arr = Arrow(questiona.get_right(), questionb.get_left(), buff=0.2).set_color(YELLOW)
        arr_lbl = Text("简单应用").scale(0.6).next_to(arr, UP, buff=0.1).set_color(BLUE)
        A_lbl = Text("判断停机").scale(0.8).next_to(questiona, DOWN, buff=0.2)
        B_lbl = Text("哥德巴赫猜想").scale(0.8).set_color(YELLOW).next_to(questionb, DOWN, buff=0.2)

        self.play(Write(questiona), run_time=1)
        self.wait(1)
        self.play(
            LaggedStart(
                GrowArrow(arr),
                Write(arr_lbl),
            )
        )
        self.wait()
        self.play(Write(questionb), run_time=1)
        self.wait(1)
        self.play(
            Indicate(questionb),
            Write(B_lbl),
        )
        self.wait(2)
        self.play(
            Indicate(questiona),
            Write(A_lbl),
        )
        self.wait()
        rect = SurroundingRectangle(questiona, buff=0.1)
        self.play(Create(rect))
        self.wait(2)
        self.play(FadeOut(rect))

        _A_lbl = Text("预知未来").scale(0.8).set_color(YELLOW).next_to(questiona, DOWN, buff=0.2)
        _B_lbl = Text("中彩票暴富").scale(0.8).set_color(GREEN).next_to(questionb, DOWN, buff=0.2)
        self.wait(2)
        self.play(
            Transform(A_lbl, _A_lbl),
            Transform(B_lbl, _B_lbl),
        )

        self.wait(2)


class UndecideProof(Scene):
    def construct(self):
        text = Text("停机问题").set_color(YELLOW).scale(2).shift(UP*2)
        cross = Cross(text, stroke_width=10, color=RED)
        # 停机问题是人类找到的第一个不可判定的问题。所谓不可判定，
        self.play(
            Write(text),
            run_time=1
        )
        self.wait(1.5)
        
        # 就是人类用严格的数学证明了，不可能有任何计算方法能够有限步内判断一个图灵机会不会停机。
        self.play(Create(cross), run_time=1)

        title = Text("不可判定性").set_color(YELLOW).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN, buff=0.2)
        self.wait()
        self.play(
            ReplacementTransform(text, title),
            GrowFromCenter(line),
            FadeOut(cross),
            run_time=1.5
        )
        self.wait(2)
        # 为什么呢？答案是用反证法，假设存在这么一个图灵机M，
        fanzheng = Text("反证法", font='heiti').scale(0.7).set_color(YELLOW).to_edge(LEFT).shift(UP*2)
        self.play(Write(fanzheng))

        self.wait(2)
        # A square stands for a TM
        M = Square(side_length=2, color=GOLD_D, stroke_width=10)
        M_lbl = MathTex("M").scale(1.5).set_color(BLUE).add_updater(lambda m: m.move_to(M))
        self.play(
            DrawBorderThenFill(M),
            Write(M_lbl),
            run_time=1
        )
        self.wait(2)

        # 它能够判断任何一个输入的图灵机会不会停机。
        code = SVGMobject("note_text.svg").set_color(ORANGE).next_to(M, LEFT, buff=3).set_stroke(width=10)
        self.play(
            FadeIn(code),
            run_time=1
        )
        self.wait()
        code_lbl = Text("Any code").scale(0.6).set_color(GREEN).add_updater(lambda m: m.next_to(code, DOWN, buff=0.1))
        self.play(Write(code_lbl), run_time=1)
        self.wait(2)

        feedin_arr = Arrow(code.get_right(), M.get_left(), buff=0.5).set_color(BLUE).set_stroke(width=15)
        result_brace = MathTex(r"\begin{cases} \text{Will Halt.} \\ \text{Never Halt.} \end{cases}", 
                               color=YELLOW).scale(1.2).next_to(M, RIGHT, buff=1)
        self.play(
            GrowArrow(feedin_arr),
            run_time=1
        )
        self.wait(1)
        self.play(Write(result_brace), run_time=1)
        self.wait(2)
        # 那么我们写一段新代码M’，它是这么工作的：
        self.play(
            *[FadeOut(mob)for mob in self.mobjects if mob not in [title, line, fanzheng, M, M_lbl]],
            M.animate.shift(LEFT*2),
            run_time=1.5
        )
        self.wait(2)

        # 如果它判断，输入的图灵机代码会永远运行，那么M’就立刻停机；
        
        large_rect = Rectangle(height=4, width=7, color=GREEN, stroke_width=6)
        M_prime = MathTex("M'", color=RED).scale(1.5).next_to(large_rect, DOWN, buff=0.2)
        self.play(
            Write(M_prime),
            DrawBorderThenFill(large_rect),
            run_time=1.5
        )
        self.wait(2)
        append_steps = MathTex(r"\begin{cases} \text{Halt:}\quad\texttt{Loop} \\ \text{Loop:}\quad\texttt{Halt}\end{cases}",
                               color=ORANGE).scale(0.8).next_to(M, RIGHT, buff=0.2)
        self.play(Write(append_steps), run_time=2)
        self.wait(3)

        # 如果判断输入的程序会停机，那自己就死循环。
        # 接下来最精彩的地方来了，我们给M’以自己的代码为输入，它到底是停机还是循环呢？
        another_Mp_lbl = M_prime.copy().next_to(large_rect, LEFT, buff=0.2)
        
        self.play(
            TransformFromCopy(M_prime, another_Mp_lbl),
            run_time=1
        )
        self.wait(2)
        arr = Arrow(another_Mp_lbl.get_right(), large_rect.get_left()+RIGHT*2, buff=0.2).set_color(GOLD).set_stroke(width=10)
        self.play(GrowArrow(arr), 
                  *[mobj.animate.shift(RIGHT*2) for mobj in [ M, M_lbl, M_prime, large_rect, append_steps]],
                  run_time=1.5)
        self.wait(2)
        ques = MathTex(r"?", color=YELLOW).scale(4).set_stroke(width=15, background=True).next_to(append_steps, RIGHT, buff=0.2)
        self.play(Write(ques), run_time=1.5)
        self.wait(2)
        # 如果停机，那根据构造就会进入循环；如果循环，那根据构造就会停机，不管怎样都是矛盾的。
        # 这意味着，输出是否能在有限步停机的这个问题，是不可能被任何图灵机本身的计算过程解决的。

class S3(Scene):
    def construct(self):
        text = Text("三句话证明").set_color(YELLOW).scale(2)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1.5)

class Digit(VGroup):
    def __init__(self, digit):

        super().__init__()
        self.number = []
        self.digit = digit
        for i in range (10):
            numberi = Text(r"%d"%i, font='Consolas').set_color(YELLOW).set_opacity(0)
            self.add(numberi)
            self.number.append(numberi)
        self.number[self.digit].set_opacity(1)

    def set_number(self, digit, opacity):
        self.number[self.digit].set_opacity(0)
        self.digit = digit
        self.number[self.digit].set_opacity(opacity)
        return self

class IncompleteProof(Scene):
    def construct(self):
        lock = SVGMobject("lock_icon.svg").scale(1.2).shift(UP*2)  
        self.play(DrawBorderThenFill(lock), run_time=1.5)
        self.wait(2)
        
        digit_windows = VGroup()
        for i in range(6):
            digit_windows.add(
                RoundedRectangle(
                    height=0.5, width=0.4, color=WHITE, 
                    stroke_width=0, corner_radius=0.05
                ).set_fill(color=BLUE).set_opacity(0.6).move_to(lock.get_center()+DOWN*2+(i-2.5)*RIGHT*0.44)
            )
        
        self.play(FadeIn(digit_windows), run_time=0.5)
        self.wait(2)

        digits_value = [ValueTracker(0) for _ in range(6)]
        digits = VGroup()

        
        for i in range(6):
            digits.add(
                Digit(0).scale(0.5).move_to(digit_windows[i]).add_updater(lambda m, idx=i: m.set_number(int(digits_value[idx].get_value()), 1))
            )
        self.play(Create(digits), run_time=1)
        self.wait(2)

        for _ in range(5):
            passwd = np.random.randint(0, 999999)
            new_digits = [int(d) for d in str(passwd)]
            # prepend 0s if new passwd is shorter than 6 digits
            new_digits = [0]*(6-len(new_digits)) + new_digits
            self.play(
                *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
                run_time=0.3
            )
            self.wait(0.7)
        
        self.wait(2)

        mingti = Text("1是存在的").set_color(ORANGE).scale(1.2).shift(LEFT*3+DOWN*2)
        proof_text = MathTex(r"(\exists x)(x=sy)", r"\ (\exists x)(x=s0)").scale(0.8).set_color(YELLOW).shift(RIGHT*3+DOWN)
        big2 = MathTex("2", color=BLUE).scale(3).next_to(proof_text[0], DOWN, buff=0.1)
        proof_int1 = MathTex(
            r"2^8\times 3^4\times 5^{13}\times 7^{9} \times 11^8\times 13^{13}\\ \times  17^5 \times 19^7\times 23^{17} \times 29^9"
        ).scale(0.6).set_color(BLUE).next_to(big2, RIGHT, buff=0.1).align_to(big2, UP)
        bigtimes3 = MathTex(r"\times 3", color=BLUE).scale(3).next_to(big2, DOWN, buff=0.1).shift(LEFT*0.3)
        proof_int2 = MathTex(
            r"2^8\times 3^4\times 5^{13}\times 7^{9} \times 11^8\times 13^{13} \\ \times  17^5 \times 19^7\times 23^{6} \times 29^9"
        ).scale(0.6).set_color(BLUE).next_to(bigtimes3, RIGHT, buff=0.1).align_to(bigtimes3, UP)
        proofnumber = VGroup(big2, proof_int1, bigtimes3, proof_int2)

        self.play(Write(mingti), run_time=1)
        self.wait(2)
        self.play(Write(proof_text), run_time=1)
        self.wait(1)
        self.play(Write(proofnumber), run_time=1)
        self.wait(2)

        self.play(
            FadeOut(proofnumber), 
            proof_text.animate.shift(DOWN),
            run_time=1
        )
        self.wait(2)

        new_digits = [0,0,0,0,0,0]
        self.play(
            *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
            run_time=1
        )
        self.wait(0.5)
        self.play(Wiggle(lock), run_time=1)
        self.wait(2)

        rect1 = SurroundingRectangle(proof_text[0], buff=0.1).set_color(GREEN)
        rect2 = SurroundingRectangle(proof_text[1], buff=0.1).set_color(GREEN)
        self.play(Create(rect1), run_time=1)
        self.wait(0.5)
        self.play(Transform(rect1, rect2), run_time=1)
        self.wait(3)
        self.play(
            FadeOut(rect1), 
            run_time=1)

        unknown_passwd = VGroup()
        passwd_digits = VGroup()
        for i in range(6):
            unknown_passwd.add(
                RoundedRectangle(
                    height=0.5, width=0.4, color=WHITE, 
                    stroke_width=0, corner_radius=0.05
                ).set_fill(color=GREEN).set_opacity(0.6).next_to(digit_windows[i], DOWN, 0.3)
            )
            passwd_digits.add(
                Text("?").scale(0.5).set_color(YELLOW).move_to(unknown_passwd[i])
            )
        self.play(
            TransformFromCopy(digit_windows, unknown_passwd),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            Write(passwd_digits),
            run_time=1
        )
        self.wait(2)


        for i in range(114514 // 1973):
            new_digits = [int(d) for d in str(i*1973)]
            # prepend 0s if new passwd is shorter than 6 digits
            new_digits = [0]*(6-len(new_digits)) + new_digits
            self.play(
                *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
                run_time=0.15
            )
        new_digits = [1,1,4,5,1,4]
        self.play(
            *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
            run_time=0.5
        )
        
        self.wait(0.5)
        self.play(Wiggle(lock), run_time=1)

        result_digits = VGroup()
        for i in range(6):
            result_digits.add(
                Text(str(new_digits[i]), font='Consolas').set_color(YELLOW).scale(0.5).move_to(unknown_passwd[i])
            )

        self.play(
            *[Flash(mob) for mob in unknown_passwd],
            *[Transform(passwd_digits[i], result_digits[i]) for i in range(6)],
            run_time=0.6
        )
        self.play(
            Rotate(lock[0], angle=-PI/6, about_point=lock[0].get_edge_center(RIGHT+DOWN)),
        )
        self.wait(2)

            
class TestLock(Scene):
    def construct(self):
        lock = SVGMobject("lock_icon.svg").scale(1.2).shift(UP*2)  
        self.play(DrawBorderThenFill(lock), run_time=1.5)
        self.wait(2)
        
        # self.add(index_labels(lock))
        self.play(
            Rotate(lock[0], angle=-PI/6, about_point=lock[0].get_edge_center(RIGHT+DOWN)),
        )
        self.wait(2)


class EnumProof(MovingCameraScene):
    def construct(self):
        question = Text("1是存在的").set_color(ORANGE).scale(1.2).to_edge(UP)
        hor_line = Line(LEFT*7, RIGHT*7).next_to(question, DOWN, buff=0.2)
        ver_line = Line(UP*3, DOWN*9).next_to(hor_line, DOWN, buff=0.).shift(LEFT*3)

        grid_lines = [hor_line.copy().set_color(GOLD).set_stroke(width=2).shift(DOWN*(i+1)*1.2) for i in range(10)]
        grid_lines = VGroup(*grid_lines)

        self.play(
            LaggedStart(
            Write(question),
            GrowFromCenter(hor_line),
            Create(ver_line)),
            run_time=1.5
        )
        self.wait()
        self.play(
            LaggedStart(
                *[Create(line) for line in grid_lines],
                lag_ratio=0.5,
                run_time=2
            )
        )
        self.wait(2)

        vocab = [r"\lnot", r"\lor", r"\supset", r"\exits", "=", "0", "s", "(", ")", ",", "+", "x", "y", "z"]

        proof_num = ["1", "2", "3", "319428", r"\hdots", "N"]
        proof_num_lbl = VGroup()
        for i in range(5):
            proof_num_lbl.add(
                MathTex(proof_num[i], color=BLUE).next_to(grid_lines[i], UP, buff=0.2).shift(LEFT*5).scale(1.2)
            )
        proof_num_lbl.add(
            MathTex(proof_num[5], color=ORANGE).next_to(grid_lines[5], UP, buff=0.2).scale(1.2).shift(LEFT*5)
        )

        text_list = [r"\lnot", r"\lor", r"\supset", r"\exists )", r"\hdots", r"(\exists x)(x=sy) (\exists x)(x=s0)"]
        proof_text = VGroup()
        for i in range(5):
            proof_text.add(
                MathTex(text_list[i], color=RED).next_to(grid_lines[i], UP, buff=0.2).shift(RIGHT*2).scale(1.2)
            )
        proof_text.add(
            MathTex(text_list[5], color=GREEN).next_to(grid_lines[5], UP, buff=0.2).scale(1.2).shift(RIGHT*2)
        )

        for i in range(5):
            self.play(
                Write(proof_num_lbl[i]),
                Write(proof_text[i]),
                run_time=1
            )
            self.wait(0.5)
        self.wait(2)

        self.play(
            self.camera.frame.animate.move_to(grid_lines[5].get_center()),
            run_time=1
        )
        self.wait()
        self.play(
            Write(proof_num_lbl[5]),
            Write(proof_text[5]),
            run_time=1.5
        )
        self.wait(1)

        tick_sign = MathTex(r"\checkmark", color=RED).scale(2).next_to(proof_text[5], RIGHT, buff=0.2)
        self.play(Write(tick_sign), run_time=1)
        self.wait(2)

class KaisuoWanbei(Scene):
    def construct(self):
        turing_K = VGroup(RoundedRectangle(width = 4, height = 4, color = BLUE_B, stroke_width = 8), 
                          MathTex(r"K", color = BLUE)[0].scale(2).next_to(2*UP + 2*LEFT, DR), 
                          RoundedRectangle(width = 3.5, height = 2.5, color = BLUE_B, stroke_width = 8).shift(0.5*DOWN), )
        self.add(turing_K)
        text = Text("开锁师傅", font='heiti').scale(1.2).set_color(YELLOW).next_to(turing_K, DOWN, buff=0.2)
        self.add(text)

        lock = SVGMobject("lock_icon.svg").shift(LEFT*4)
        self.play(DrawBorderThenFill(lock), run_time=0.5)
        self.wait(0.5)
        _lock = lock.copy().scale(0.6).move_to(turing_K[2].get_center())
        self.play(Transform(lock, _lock), run_time=1)
        self.wait(0.5)

        self.play(
            Rotate(lock[0], angle=-PI/6, about_point=lock[0].get_edge_center(RIGHT+DOWN)),
            run_time=0.5
        )

        self.wait(0.2)

        true_text = Text("真").scale(1.2).set_color(GREEN).next_to(turing_K, RIGHT, buff=0.2).shift(UP*0.5)
        false_text = Text("假").scale(1.2).set_color(RED).next_to(turing_K, RIGHT, buff=0.2).shift(DOWN*0.5)
        self.play(
            LaggedStart(
                Write(true_text),
                Write(false_text),
                run_time=0.5
            )
        )
        self.wait(1)

        self.play(FadeOut(lock), run_time=0.5)

        lock = SVGMobject("lock_icon.svg").shift(LEFT*5)
        _lock = lock.copy().scale(0.6).move_to(turing_K[2].get_center())
        
        self.play(DrawBorderThenFill(lock), run_time=0.5)
        self.play(TransformFromCopy(lock, _lock), run_time=1)
        self.wait()
        self.play(Wiggle(_lock), run_time=1)
        self.wait(2)

        cross_on_lock = Cross(lock, stroke_width=15, color=RED)
        self.play(Create(cross_on_lock), run_time=1)

        incomp_text = Text("无法判断").set_color(RED).scale(0.9).next_to(lock, DOWN, buff=0.2)
        self.play(Write(incomp_text), run_time=1)
        self.wait(2)
        
        Complete_text = Text("完备性").set_color(YELLOW).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(Complete_text, DOWN, buff=0.2)
        self.play(
            Write(Complete_text),
            GrowFromCenter(line),
            run_time=1.5
        )
        self.wait()
        self.play(
            FadeOut(cross_on_lock),
            FadeOut(incomp_text),
            run_time=1
        )
        self.wait(2)
        tick_sign = MathTex(r"\checkmark", color=RED).scale(4).move_to(lock).set_stroke(width=10, background=True)
        self.play(Write(tick_sign), run_time=1)
        self.wait(2)

        self.play(
            *[FadeOut(mob)for mob in [tick_sign, lock, _lock, true_text, false_text]]
        )
        self.wait()

        halo_ring = Ellipse(width=5, height=1.3, color=YELLOW_C,stroke_width=15).set_fill(opacity=0).next_to(turing_K, UP).shift(DOWN*0.4)
        god_name = Text("神", font='heiti').scale(1.2).set_color(YELLOW).next_to(turing_K, DOWN, buff=0.2)
        self.play(
            FadeIn(halo_ring),
            Transform(text, god_name),
            run_time=2)
        self.wait(4)


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

        proposition = MTex(r"&\text{对于图灵机}T, \\&\text{存在自然数}n\in\mathbb{N}, \\&\text{以及}n+1\text{个历史记录}C_0,C_1, \cdots, C_n,\\&\text{使得}C_n\text{停机，且}C_{i+1}=T(C_i),\ i=0, 1, \cdots, n-1", 
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
        

class SelfRef(Scene):
    def construct(self):
        text = Text("自我指涉").set_color(YELLOW).scale(2)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1.5)

        title = text.copy().scale(0.5).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN, buff=0.2)
        self.play(
            ReplacementTransform(text, title),
            GrowFromCenter(line),
            run_time=1.5
        )
        self.wait(4)

        sent = Text("这句话是假的").set_color(RED).scale(1.5)
        rect = SurroundingRectangle(sent, buff=0.1).set_color(YELLOW)
        
        russo_para = MathTex(r"A=\{X: X\notin X\}").scale(1.5).set_color(BLUE).shift(UP*1.5+LEFT*4)

        self.play(Write(sent), run_time=1)
        self.wait(1.5)
        self.play(Create(rect), run_time=1)
        self.wait(2)
        self.play(Write(russo_para), run_time=1)
        self.wait(5)

