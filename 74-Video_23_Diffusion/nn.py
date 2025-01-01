from __future__ import annotations

from manimlib import *

#################################################################### 

class NN(Scene):
    def construct(self):
        buff_h, buff_v = 1, 0.35
        m, n = 5, (12, 8, 6, 8, 12)
        dots = [VGroup(*[Dot((i-(m-1)/2)*buff_h*RIGHT + (j-(n[i]-1)/2)*buff_v*UP, stroke_width = 2, fill_opacity = 0, radius = 0.12) for j in range(n[i])]) for i in range(m)]
        lines = []
        for i in range(m-1):
            line = VGroup(*[Line(dot_1, dot_2, stroke_width = 1) for dot_1 in dots[i] for dot_2 in dots[i+1]])
            lines.append(line)
        nn = VGroup(*lines, *dots)
        self.add(nn)