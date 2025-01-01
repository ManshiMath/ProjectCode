from manim import *
import numpy as np

class ParaArc(VMobject):
    CONFIG = {
        "color": BLUE,
        "fill_opacity": 0.2,
        "scale_factor": 1,
        "closed": False,
        "height": None,
        "width": None
    }
    def __init__(self, curve = lambda x: -x*x+1, x_range = np.array([-1,1,50]), **kwargs):

        self.curve = curve
        self.range = x_range
        VMobject.__init__(self, **kwargs)
        start = np.array([x_range[0], curve(x_range[0]), 0])
        end = np.array([x_range[1], curve(x_range[1]), 0])
        if self.closed:
            for i in range(int(x_range[2]+0.01)):
                self.add_line_to(end + i*(start-end)/x_range[2])
                self.append_points(end + i*(start-end)/x_range[2])
            self.close_path()
        # self.scale(self.scale_factor)
        self.all = VGroup(self)

        if self.height is None:
            pass
        elif self.height:
            medium = (x_range[0]+x_range[1])/2
            height_value = abs(curve(medium)-(curve(x_range[0])+curve(x_range[1]))/2)
            self.height_line = ParaHeight(curve, x_range, "%d"%height_value, color = YELLOW, scale_factor=self.scale_factor)
            self.all.add(self.height_line)
        else:
            self.height_line = ParaHeight(curve, x_range, color = YELLOW, scale_factor=self.scale_factor)
            self.all.add(self.height_line)

        if self.width is None:
            pass
        elif self.width:
            width_value = abs(x_range[1]-x_range[0])
            self.width_line = UnderDoubleArrow(self, "%d"%width_value, color = YELLOW)
            self.all.add(self.width_line)
        else:
            self.width_line = UnderDoubleArrow(self, color = YELLOW)
            self.all.add(self.width_line)

    def init_points(self):
        samples = np.array([[x, self.curve(x), 0] for x in np.linspace(self.range[0], self.range[1], int(2*self.range[2]+1) )])
        shift = (samples[0]+samples[2])/2 - samples[1]
        samples[1::2] -= shift
        points = np.zeros(( int(3*self.range[2]) , 3))
        points[0::3] = samples[0:-1:2]
        points[1::3] = samples[1::2]
        points[2::3] = samples[2::2]
        points *= self.scale_factor
        self.set_points(points)

    def set_range(self, start, end):
        target = ParaArc(curve = self.curve, x_range = np.array([start,end,self.range[2]]), closed = self.closed)
        self.set_points(target.get_points())
        return self