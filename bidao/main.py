from manim import *

import numpy as np

class Video(Scene):
    def construct(self):
        a = 1
        circle = Circle(color=WHITE)
        self.add(circle)

        def phase(a, theta):
            perp = abs(a * np.sin(theta))
            alpha = np.arccos(perp)
            if theta % TAU <= PI:
                init_phase = theta + PI / 2 + alpha
                angle_increase = -2 * alpha
            else:
                init_phase = theta - PI / 2 - alpha
                angle_increase = 2 * alpha
            if angle_increase == 0:
                unit_time = 0
                init_ratio = 0
                if theta % TAU <= PI:
                    angle_increase = -1
                else:
                    angle_increase = 1
            else:
                unit_time = 2 * np.sin(alpha)
                init_ratio = np.linalg.norm(a * LEFT - np.array([np.cos(init_phase), np.sin(init_phase), 0])) / unit_time
            return [unit_time, init_ratio, init_phase, angle_increase]

        def position(t, paras):
            if paras[0] == 0:
                return np.array([np.cos(PI + t * paras[3]), np.sin(PI + t * paras[3]), 0])
            else:
                integer = int(t / paras[0] + paras[1])
                residue = t / paras[0] + paras[1] - integer
                start = np.array([np.cos(paras[2] + integer * paras[3]), np.sin(paras[2] + integer * paras[3]), 0])
                end = np.array([np.cos(paras[2] + (integer + 1) * paras[3]), np.sin(paras[2] + (integer + 1) * paras[3]), 0])
                return interpolate(start, end, residue)

        number = 360
        paras = [phase(a, i * TAU / number) for i in range(number)]

        def graph_updater(mob, dt):
            mob.increment_time(dt)
            points = [position(mob.time / 2.5, para) for para in paras]
            mob.set_points_as_corners([*points, points[0]])

        graph = VMobject(stroke_color=YELLOW, stroke_width=1)
        graph.time = 0
        graph.add_updater(graph_updater)
        self.add(graph)
        self.wait(12)
