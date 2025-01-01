from manim import *
import numpy as np
from functools import wraps

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])



#################################################################### 

class Video(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (2.5, 2.5)}, 
            }
    }
    def construct(self):
        a = 0.5
        circle = Circle(color = WHITE)
        def phase(a, theta):
            perp = abs(a*np.sin(theta))
            alpha = np.arccos(perp)
            if theta % TAU <= PI:
                init_phase = theta + PI/2 + alpha
                angle_increase = -2*alpha
            else:
                init_phase = theta - PI/2 - alpha
                angle_increase = 2*alpha
            if angle_increase == 0:
                unit_time = 0
                init_ratio = 0
                if theta % TAU <= PI:
                    angle_increase = -1
                else:
                    angle_increase = 1
            else:
                unit_time = 2*np.sin(alpha)
                init_ratio = np.linalg.norm(a*LEFT - unit(init_phase))/unit_time
            return [unit_time, init_ratio, init_phase, angle_increase]
        def position(t, paras):
            if paras[0] == 0:
                return unit(PI + t*paras[3])
            else:
                integer = int(t / paras[0] + paras[1])
                residue = t / paras[0] + paras[1] - integer
                start, end = unit(paras[2] + integer*paras[3]), unit(paras[2] + (integer+1)*(paras[3]))
                return interpolate(start, end, residue)
        number = 360
        paras = [phase(a, i*TAU/number) for i in range(number)]
        frametime = ValueTracker(0.0)
        def graph_updater(mob: VMobject):
            points = [position(frametime.get_value() / 2.5, para) for para in paras]
            mob.set_points_as_corners(points).close_path()
        graph = VMobject(stroke_color = YELLOW, stroke_width = 1).add_updater(graph_updater)
        self.add(circle, graph)
        self.play(frametime.animate.set_value(60), run_time = 60, rate_func = linear)
        
        # para = phase(0.5, 3*PI/2)
        # def point_updater(mob: Dot):
        #     mob.move_to(position(self.time, para))
        # point = Dot().add_updater(point_updater)
        # self.add(circle, point).wait(10)

class Video(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (2.5, 2.5)}, 
            }
    }
    def construct(self):
        a = 0.5
        circle = Circle(color = WHITE)
        def phase(a, theta):
            perp = abs(a*np.sin(theta))
            alpha = np.arccos(perp)
            if theta % TAU <= PI:
                init_phase = theta + PI/2 + alpha
                angle_increase = -2*alpha
            else:
                init_phase = theta - PI/2 - alpha
                angle_increase = 2*alpha
            if angle_increase == 0:
                unit_time = 0
                init_ratio = 0
                if theta % TAU <= PI:
                    angle_increase = -1
                else:
                    angle_increase = 1
            else:
                unit_time = 2*np.sin(alpha)
                init_ratio = np.linalg.norm(a*LEFT - unit(init_phase))/unit_time
            return [unit_time, init_ratio, init_phase, angle_increase]
        def position(t, paras):
            if paras[0] == 0:
                return unit(PI + t*paras[3])
            else:
                integer = int(t / paras[0] + paras[1])
                residue = t / paras[0] + paras[1] - integer
                start, end = unit(paras[2] + integer*paras[3]), unit(paras[2] + (integer+1)*(paras[3]))
                return interpolate(start, end, residue)
        number = 360
        paras = [phase(a, i*TAU/number) for i in range(number)]
        frametime = ValueTracker(0.0)
        def graph_updater(mob: VMobject):
            points = [position(frametime.get_value() / 2.5, para) for para in paras]
            mob.set_points_as_corners(points).close_path()
        graph = VMobject(stroke_color = YELLOW, stroke_width = 1).add_updater(graph_updater)
        self.add(circle, graph)
        self.play(frametime.animate.set_value(60), run_time = 60, rate_func = linear)
