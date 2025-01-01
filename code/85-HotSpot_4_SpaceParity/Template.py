from __future__ import annotations

from manimlib import *
import numpy as np

class Patch_1(FrameScene):
    def construct(self):
        camera = self.camera.frame.set_height(4)
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion))

        earth = TexturedSurface(Sphere(), "Grid_2.png")
        earth.phase, earth.amplitude, earth.point = 0, 0.02, ORIGIN
        def shake_updater(mob: TexturedSurface):
            angle = -self.time*TAU/2
            # position = earth.point
            # shake = np.array([2*random.random()-1, 2*random.random()-1, 2*random.random()-1])*1
            # earth.point = interpolate(position, shake, 0.01)
            mob.restore().rotate(angle)#.shift(earth.point)
        

        width, height = 2.8, 0.2
        # arrow = Polygon(ORIGIN, height*UL, width*RIGHT + height*UP + 1.5*height*LEFT, width*RIGHT + 1.5*height*UL, width*RIGHT, width*RIGHT + 1.5*height*DL, width*RIGHT + height*DOWN + 1.5*height*DL, height*DL, fill_color = RED, fill_opacity = 0.5, stroke_width = 0)
        factor = 1/2
        height_extra = (1-factor)/factor*height
        threshold = 1 - height_extra/width
        def uv_func(u, v):
            # h = 2*v-1
            # if abs(h) < factor:
            #     ratio = abs(h)/factor
            #     w_low, w_high = -height*ratio, width-height*ratio
            # else:
            #     ratio = abs(h)/factor
            #     w_low, w_high = width-height/factor, width-height*ratio
            # return np.array([interpolate(w_low, w_high, u), h*height/factor, 0])
            h = 2*v-1
            if u < threshold:
                w_low, w_high = 0, height
            else:
                alpha = (u-threshold)/(1-threshold)
                w_low, w_high = 0, height + alpha*height_extra
            return u*width*RIGHT + interpolate(w_low, w_high, h)*(UL if h>0 else UR)
        r = 1.2
        def polar_function(p):
            theta, phi = -p[0], p[1]
            return r*np.array([np.cos(theta)*np.cos(phi), np.sin(theta)*np.cos(phi), np.sin(phi)])  
        arrow_1 = ParametricSurface(uv_func, color = RED, fill_opacity = 1, stroke_width = 0).apply_function(polar_function)
        arrow_2 = arrow_1.copy().rotate(PI, OUT, about_point = ORIGIN)
        earth.add(arrow_1, arrow_2).save_state().add_updater(shake_updater)
        self.add(earth).wait(60)

class Patch_2(FrameScene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion))

        particle_up = TexturedSurface(Sphere(), "Grid_2.png")
        particle_down = TexturedSurface(Sphere(), "Grid_2.png")
        particle_up.direction, particle_down.direction = 1, -1
        def shake_updater(mob: TexturedSurface):
            angle = self.time*TAU/2*mob.direction
            mob.restore().rotate(angle)#.shift(earth.point)
        
        width, height = 2.8, 0.2
        factor = 1/2
        height_extra = (1-factor)/factor*height
        threshold = 1 - height_extra/width
        def uv_func(u, v):
            h = 2*v-1
            if u < threshold:
                w_low, w_high = 0, height
            else:
                alpha = (u-threshold)/(1-threshold)
                w_low, w_high = 0, height + alpha*height_extra
            return u*width*RIGHT + interpolate(w_low, w_high, h)*(UL if h>0 else UR)
        r = 1.2
        def polar_function(p):
            theta, phi = p[0], p[1]
            return r*np.array([np.cos(theta)*np.cos(phi), np.sin(theta)*np.cos(phi), np.sin(phi)])  
        arrow_1 = ParametricSurface(uv_func, color = RED, fill_opacity = 1, stroke_width = 0).apply_function(polar_function)
        arrow_2 = arrow_1.copy().rotate(PI, OUT, about_point = ORIGIN)
        particle_up.add(arrow_1.copy(), arrow_2.copy()).shift(3*DOWN).save_state().add_updater(shake_updater)
        particle_down.add(arrow_1.copy(), arrow_2.copy()).scale(np.array([1, -1, 1]), min_scale_factor = -1).shift(3*UP).save_state().add_updater(shake_updater)
        plane = Rectangle(width = 5, height = 5, fill_opacity = 0.2, stroke_width = 0, fill_color = WHITE).rotate(PI/2, axis = RIGHT)

        alpha = ValueTracker(0)
        particle_down.add_post_updater(lambda m: m.set_opacity(alpha.get_value()))
        self.add(particle_up, particle_down).wait(4)
        self.add(particle_up, plane, particle_down).play(FadeIn(plane, OUT), alpha.animate.set_value(1), run_time = 1)
        particle_down.clear_post_updaters()
        self.wait(55)

class Patch_3(FrameScene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion))

        particle_up = TexturedSurface(Sphere(), "Grid_2.png")
        particle_down = TexturedSurface(Sphere(), "Grid_2.png")
        particle_up.direction, particle_down.direction = 1, 1
        def shake_updater(mob: TexturedSurface):
            angle = self.time*TAU/2*mob.direction
            mob.restore().rotate(angle)
        
        width, height = 2.8, 0.2
        factor = 1/2
        height_extra = (1-factor)/factor*height
        threshold = 1 - height_extra/width
        def uv_func(u, v):
            h = 2*v-1
            if u < threshold:
                w_low, w_high = 0, height
            else:
                alpha = (u-threshold)/(1-threshold)
                w_low, w_high = 0, height + alpha*height_extra
            return u*width*RIGHT + interpolate(w_low, w_high, h)*(UL if h>0 else UR)
        r = 1.2
        def polar_function(p):
            theta, phi = p[0], p[1]
            return r*np.array([np.cos(theta)*np.cos(phi), np.sin(theta)*np.cos(phi), np.sin(phi)])  
        arrow_1 = ParametricSurface(uv_func, color = RED, fill_opacity = 1, stroke_width = 0).apply_function(polar_function)
        arrow_2 = arrow_1.copy().rotate(PI, OUT, about_point = ORIGIN)
        particle_up.add(arrow_1.copy(), arrow_2.copy()).shift(3*UP).save_state().add_updater(shake_updater)
        particle_down.add(arrow_1.copy(), arrow_2.copy()).shift(3*DOWN).save_state().add_updater(shake_updater)


        arrows_grey = SGroup(arrow_1, arrow_2).set_color(GREY).set_opacity(0.2).rotate(PI/2, axis = LEFT).scale(2).shift(3*DOWN)
        alpha = ValueTracker(0)
        particle_down.add_updater(lambda m: m.rotate(alpha.get_value(), axis = UP))
        self.add(particle_up, particle_down).wait(3)
        self.play(FadeIn(arrows_grey))
        self.play(alpha.animate.set_value(PI), run_time = 2)
        self.play(FadeOut(arrows_grey))
        self.wait(3)
        particle_down.clear_updaters().save_state()
        particle_down.direction = -1
        particle_down.add_updater(shake_updater)
        self.wait(50)



#################################################################### 

class Patch_0(FrameScene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2 - PI/10))
        camera.set_orientation(Rotation(quadternion))

        earth = TexturedSurface(Sphere(), "Grid_2.png")
        earth.phase, earth.amplitude, earth.point = 0, 0.02, ORIGIN
        def shake_updater(mob: TexturedSurface):
            angle = self.time*TAU/2
            position = earth.point
            shake = np.array([2*random.random()-1, 2*random.random()-1, 2*random.random()-1])*1
            earth.point = interpolate(position, shake, 0.01)
            mob.restore().rotate(angle)#.shift(earth.point)
        
        width, height = 2.8, 0.2
        factor = 1/2
        height_extra = (1-factor)/factor*height
        threshold = 1 - height_extra/width
        def uv_func(u, v):
            h = 2*v-1
            if u < threshold:
                w_low, w_high = 0, height
            else:
                alpha = (u-threshold)/(1-threshold)
                w_low, w_high = 0, height + alpha*height_extra
            return u*width*RIGHT + interpolate(w_low, w_high, h)*(UL if h>0 else UR)
        r = 1.2
        def polar_function(p):
            theta, phi = p[0], p[1]
            return r*np.array([np.cos(theta)*np.cos(phi), np.sin(theta)*np.cos(phi), np.sin(phi)])  
        arrow_1 = ParametricSurface(uv_func, color = RED, fill_opacity = 1, stroke_width = 0).apply_function(polar_function)
        arrow_2 = arrow_1.copy().rotate(PI, OUT, about_point = ORIGIN)
        earth.add(arrow_1, arrow_2).save_state().add_updater(shake_updater)
        self.add(earth).wait(60)

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]
        