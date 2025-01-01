from __future__ import annotations

from functools import wraps
import platform
import time

import numbers
import numpy as np
from tqdm import tqdm as ProgressDisplay

from manimlib.mobject.mobject import Mobject, Group
from manimlib.mobject.types.vectorized_mobject import VMobject, VGroup
from manimlib.mobject.types.image_mobject import ImageMobject
from manimlib.mobject.svg.text_mobject import Text
from manimlib.mobject.svg.mtex_mobject import MTex
from manimlib.mobject.geometry import Line, Arrow, Circle, ArcBetweenPoints, Polygon, Rectangle, RegularPolygon
from manimlib.mobject.shape_matchers import SurroundingRectangle
from manimlib.camera.camera import Camera
from manimlib.scene.scene import Scene, EndSceneEarlyException
from manimlib.animation.animation import Animation
from manimlib.animation.animation import prepare_animation
from manimlib.animation.movement import Homotopy
from manimlib.animation.creation import Write, ShowPartial
from manimlib.animation.fading import Fade, FadeIn, FadeOut, FadeInFromPoint
from manimlib.animation.transform import Transform, TransformFromCopy

from manimlib.logger import log

from manimlib.utils.color import interpolate_color
from manimlib.utils.bezier import interpolate, integer_interpolate, bezier
from manimlib.utils.space_ops import get_norm
from manimlib.utils.config_ops import digest_config
from manimlib.utils.rate_functions import smooth, linear
from manimlib.utils.simple_functions import clip

from manimlib.constants import ORIGIN, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR
from manimlib.constants import PI, TAU
from manimlib.constants import FRAME_HEIGHT, FRAME_WIDTH
from manimlib.constants import RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE, BLACK, BLUE_E

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Iterable
    import numpy.typing as npt


# from manimlib import *

#################################################################### 

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

def ellipse_unit(angle, a=1, b=1/2):
    return np.array([a*np.cos(angle), b*np.sin(angle), 0])

def ratio_color(ratio: float, *colors, circulate: bool = True):
    
    if len(colors) == 0:
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    if circulate:
        colors = [*colors, colors[0]]

    number_colors = len(colors) - 1
    index, interpolate = integer_interpolate(0, number_colors, ratio)

    return interpolate_color(colors[index], colors[index+1], interpolate)

def bounce(t: float):
    return 1- abs(bezier([0, 0, 0, 1.5, 1.5, 1])(t) - 1)

def double_bounce(t: float):
    return 1- abs(bezier([0, 0, 0, 1.6, 1.6, 0.9, 0.9, 1])(t) - 1)

def breath(t: float):
    return bezier([0, 0, 0, 1.5, 1.5, 1])(t)

def double_there_and_back(t: float):
    new_t = 1-abs(1-abs(4*t-2))
    return smooth(new_t)

def double_v_end(t: float):
    return (2-t)*t**3

def smooth_boot(alpha: float, delta: float = 0):
    beta = delta + alpha
    alpha = clip(alpha, 0, 1)
    beta = clip(beta, 0, 1-alpha)
    delta = beta - alpha
    ratio = 1/(1-alpha-delta/2)
    def util(t: float):
        if t < alpha:
            return double_v_end(t/alpha)/2*ratio*alpha
        elif t > 1-beta:
            return 1 - double_v_end((1-t)/beta)/2*ratio*beta
        else:
            return (t-alpha)*ratio + ratio*alpha/2
    return util

def less_smooth(t: float):
    # Zero and first derivatives at t=0 and t=1.
    # Equivalent to bezier([0, 0, 1, 1])
    return (t**2) * (3 - 2 * t)

def fore(t: float):
    return t*(3-t**2)/2

def back(t: float):
    return t**2*(3-t)/2
        
OMEGA = unit(-PI/6)

BACK = "#333333"
LIME = "#BFFF00"

DEFAULT_WAIT_TIME = 1

stroke_dic = {r"width": 8, r"color": BLACK, r"background": True}

#################################################################### 

class Notice(VGroup):
    def __init__(self, m_text1: str = "", m_text2: str = "", **kwargs):

        row1 = Text(m_text1, font = 'FZShuSong-Z01S')
        row2 = Text(m_text2, font = 'FZShuSong-Z01S')
        if row1.get_height() < 0.5:
            row1.scale(1.25)
        if row2.get_height() < 0.5:
            row2.scale(1.25)
        row2.next_to(row1, DOWN)
        super().__init__(row1, row2, **kwargs)
        self.scale(0.5).shift(np.array([5.8,2.9,0])).set_stroke(**stroke_dic)

class FixedNotice(VMobject):
    def __init__(self, m_text1: str = "", m_text2: str = ""):
        super().__init__(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        notice = Notice(m_text1, m_text2)
        self.set_points(notice.get_all_points())

class FixedText(VMobject):
    def __init__(self, text, **kwargs):
        super().__init__(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        notice = Text(text, **kwargs)
        for mob in notice.submobjects:
            new_submob = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(mob.get_all_points())
            self.add(new_submob)

class FixedTex(VMobject):
    def __init__(self, text, **kwargs):
        super().__init__(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        notice = MTex(text, **kwargs)
        self.set_points(notice.get_all_points())

class Shade(Rectangle):
    CONFIG = {
        "height": FRAME_HEIGHT,
        "width": FRAME_WIDTH,
        "fill_opacity": 1,
        "fill_color": BACK, 
        "stroke_width": 0
    }

class Songti(Text):
    CONFIG = {
        "font": "FZShuSong-Z01S"
    }

class Heiti(Text):
    CONFIG = {
        "font": "FZHei-B01"
    }

class Title(Text):
    def __init__(self, text):
        super().__init__(text, font = "FZShuSong-Z01S", color = YELLOW)
        self.next_to(3*UP, UP)

class TitleLine(Line):
    def __init__(self):
        super().__init__(3*UP+6*LEFT, 3*UP+6*RIGHT)

class LabelPicture(Group):
    CONFIG = {
        "picture_config": {"height": 4},
        "text_config": {"font": "FZShuSong-Z01S"},
        "text_scale": 0.4,
    }
    def __init__(self, picture, text, **kwargs):
        digest_config(self, kwargs)
        image = ImageMobject(picture, **self.picture_config)
        text = Text(text, **self.text_config).scale(self.text_scale).next_to(image, DOWN)
        super().__init__(image, text)

class BVCover(Group):
    def __init__(self, picture, text, **kwargs):
        image = ImageMobject(picture, height = 2)
        text = Text(text, font = "Times New Roman").scale(0.5).next_to(image, UP, buff = 0.1)
        super().__init__(image, text)

class Digit(VGroup):
    def __init__(self, digit):

        super().__init__()
        self.number = []
        self.digit = digit
        for i in range (10):
            numberi = MTex(r"%d"%i).set_opacity(0)
            self.add(numberi)
            self.number.append(numberi)
        self.number[self.digit].set_opacity(1)

    def set_number(self, digit, opacity):
        self.number[self.digit].set_opacity(0)
        self.digit = digit
        self.number[self.digit].set_opacity(opacity)
        return self

class Value(VGroup):
    def __init__(self, decimal):

        super().__init__()
        distance = 0.12
        self.neg = MTex(r"-").shift(4*distance*LEFT).set_opacity(0)
        self.one = Digit(0).shift(2*distance*LEFT)
        self.point = MTex(r"\cdot").shift(0.5*distance*RIGHT + distance*DOWN)
        self.dec = Digit(0).shift(distance*RIGHT)
        self.cent = Digit(0).shift(3*distance*RIGHT)
        self.add(self.neg, self.one, self.point, self.dec, self.cent)
        self.set_value(decimal)

    def set_value(self, value, opacity = 1):
        if value < -0.01:
            self.neg.set_opacity(opacity)
            value = -value
        else:
            self.neg.set_opacity(0)
        value = int(value*100 + 0.3)
        self.cent.set_number(value % 10, opacity)
        value = int(value / 10)
        self.dec.set_number(value % 10, opacity)
        value = int(value / 10)
        self.one.set_number(value % 10, opacity)

class SnowFlake(VGroup):
    def __init__(self):

        snows = [SnowHex(2,1), SnowRing(3), SnowRing(4), SnowRing(5), SnowHex(6,2), SnowHex(6,3), SnowHex(6,4)]

        outer_radius = 12
        ratio = 2/3
        arc = ArcBetweenPoints(outer_radius * unit(PI/6), outer_radius * unit(-PI/6), angle = PI + PI/12, n_components = 24).scale(np.array([ratio, 1, 1]), about_edge = RIGHT)
        arcs = [arc.copy().rotate(i*PI/3, about_point = ORIGIN) for i in range(6)]
        
        super().__init__(*snows, *arcs)
        self.scale(0.3)

class SnowRing(VGroup):
    def __init__(self, radius):
        super().__init__(*[SnowHex(radius, i) for i in range(radius)])

class SnowHex(VGroup):
    def __init__(self, x_position, omega_position):
        super().__init__(*[Snow().shift(x_position * unit(i*PI/3 + PI/2) + omega_position*unit(i*PI/3 - PI/6)) for i in range(6)])

class Snow(RegularPolygon):
    def __init__(self):
        super().__init__(n = 6, stroke_width = 2)
        self.scale(0.5)

class StarrySky(VGroup):
    def __init__(self):

        like = Text("", font = 'vanfont')
        coin = Text("", font = 'vanfont')
        star = Text("", font = 'vanfont')
        share = Text("", font = 'vanfont')

        land = Line(np.array([-8,0,0]), np.array([8,0,0]))
        water = Polygon(np.array([-4,0,0]), np.array([-6,0,0]), np.array([-5,-4,0]), np.array([6,-4,0]), fill_color = BLUE_E, fill_opacity = 0.5, stroke_width = 0)
        band1 = Line(np.array([-6,0,0]), np.array([-5,-4,0]), color = BLUE)
        band2 = Line(np.array([-4,0,0]), np.array([6,-4,0]), color = BLUE)
        river = VGroup(water, band1, band2)
        moon = Circle(radius = 1.2, arc_center = np.array([-5,2,0]), fill_color = WHITE, fill_opacity = 0.9, stroke_width = 0)

        star0 = star.copy().set_color(BLUE).save_state().shift(UP)
        star2 = star0.copy().shift(1.3*UP-1.7*RIGHT)
        star3 = star0.copy().shift(2.2*UP+2.6*RIGHT)
        star4 = star0.copy().shift(0.3*UP+2.2*RIGHT)
        star5 = star0.copy().shift(-0.2*UP+6.0*RIGHT)
        star5_1 = coin.copy().set_color(BLUE).shift(2.7*UP+1.6*RIGHT)
        bigstars = [star2, star3, star4, star5, star5_1]
        star00 = star0.copy().scale(0.7)
        star6 = star00.copy().shift(1.4*UP+4.0*RIGHT)
        star7 = star00.copy().shift(1.7*UP+0.2*RIGHT)
        star8 = star00.copy().shift(0.4*UP+4.3*RIGHT)
        star9 = star00.copy().shift(0.1*UP-3.2*RIGHT)
        star10 = star00.copy().shift(-0.1*UP-2.5*RIGHT)
        star10_1 = like.copy().set_color(BLUE).scale(0.7).shift(2.5*UP-2.7*RIGHT)
        star10_2 = share.copy().set_color(BLUE).scale(0.7).shift(3.2*UP-0.7*RIGHT)
        smallstars = [star6, star7, star8, star9, star10, star10_1, star10_2]
        star000 = star0.copy().scale(0.4)
        star11 = star000.copy().shift(0.5*UP-1.3*RIGHT)
        star12 = star000.copy().shift(0.8*UP+0.8*RIGHT)
        star13 = star000.copy().shift(-0.2*UP+3.1*RIGHT)
        star14 = star000.copy().shift(1.1*UP+2.7*RIGHT)
        star15 = star000.copy().shift(1.2*UP-0.5*RIGHT)
        star16 = star000.copy().shift(2.2*UP-1.8*RIGHT)
        stardust = [star11, star12, star13, star14, star15, star16]

        super().__init__(star0, river, land, moon, *bigstars, *smallstars, *stardust)
        self.star = star0
        self.others = VGroup(river, land, moon, *bigstars, *smallstars, *stardust)

class Testboard(VGroup):
    def __init__(self):
        
        texts = [r"\begin{pmatrix}\hat{r} \\ \hat{\theta}\end{pmatrix}", 
                 r"=\begin{pmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}", 
                 r"\Rightarrow\begin{pmatrix}\dot{\hat{r}}\\\dot{\hat{\theta}}\end{pmatrix}", 
                 r"=\frac{d}{dt}\begin{pmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}", 
                 r"=\begin{pmatrix}-\dot\theta\sin\theta & \dot\theta\cos\theta \\ -\dot\theta\cos\theta & -\dot\theta\sin\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}", 
                 r"=\dot\theta\begin{pmatrix}\hat{\theta} \\ -\hat{r}\end{pmatrix}"]
        mtex_1 = MTex("".join(texts)).scale(0.5).next_to(3.6*UP + 7*LEFT)
        text = r"\Rightarrow\vec{v}=\frac{d}{dt}\vec{r}=\frac{d}{dt}(r\hat{r})=\dot{r}\hat{r}+r\dot{\hat{r}}=\dot{r}\hat{r}+r\dot\theta\hat\theta"
        mtex_2 = MTex(text).scale(0.5).next_to(2.96*UP + 7*LEFT)
        texts = [r"\Rightarrow\vec{a}=\frac{d}{dt}\vec{v}=\frac{d}{dt}(\dot{r}\hat{r}+r\dot\theta\hat\theta)", 
                 r"=(\ddot{r}\hat{r}+\dot{r}\dot{\hat{r}})+(\dot{r}\dot{\theta}\hat{\theta}+r\ddot\theta\hat\theta+r\dot\theta(-\dot\theta\hat{r}))", 
                 r"=(\ddot{r}-r\dot\theta^2)\hat{r}+(2\dot{r}\dot\theta+r\ddot\theta)\hat\theta=:a_r\hat{r}+a_\theta\hat\theta"]
        mtex_3 = MTex("".join(texts)).scale(0.5).next_to(2.32*UP + 7*LEFT)
        line_1 = Line(64/9*LEFT+1.9*UP, 64/9*RIGHT+1.9*UP).insert_n_curves(64)
        texts = [r"\vec{F}=-\frac{GMm}{r^2}\hat{r}\Rightarrow\begin{cases}a_r=-\frac{GM}{r^2}\\a_\theta=0\end{cases}", 
                 r"\Rightarrow 0=a_\theta=2\dot{r}\dot\theta+r\ddot\theta=\frac{1}{r}\frac{d}{dt}(r^2\dot\theta)\qquad\Rightarrow r^2\dot\theta = h", 
                 r"\qquad\Rightarrow \frac{d}{dt}=\frac{d\theta}{dt}\frac{d}{d\theta}=\frac{h}{r^2}\frac{d}{d\theta}"]
        mtex_4 = MTex("".join(texts)).scale(0.5).next_to(1.4*UP + 7*LEFT)
        texts = [r"u:=\frac{1}{r}\qquad \Rightarrow \dot{r}=\frac{d}{dt}\left(\frac{1}{u}\right)=-\frac{1}{u^2}\frac{d}{dt}u=-r^2\left(\frac{h}{r^2}\frac{du}{d\theta}\right)=-h\frac{du}{d\theta}", 
                 r"\qquad \Rightarrow \ddot{r}=\frac{d}{dt}\dot{r}=\left(\frac{h}{r^2}\frac{d}{d\theta}\right)\left(-h\frac{du}{d\theta}\right)=-\frac{h^2}{r^2}\frac{d^2u}{d\theta^2}"]
        mtex_5 = MTex("".join(texts)).scale(0.5).next_to(0.7*UP + 7*LEFT)
        texts = [r"\Rightarrow -\frac{GM}{r^2}=a_r=\ddot{r}-r\dot\theta^2 = -\frac{h^2}{r^2}\frac{d^2u}{d\theta^2}-r\left(\frac{h}{r^2}\right)^2=-\frac{h^2}{r^2}\left(\frac{d^2u}{d\theta^2} + u\right)", 
                 r"\qquad\Rightarrow \frac{d^2u}{d\theta^2}+u = \frac{GM}{h^2}"]
        mtex_6 = MTex("".join(texts)).scale(0.5).next_to(7*LEFT)
        texts = [r"\Rightarrow u=\frac{GM}{h^2}-A\cos(\theta + \phi)\qquad\Rightarrow ", 
                 r"r=\frac{ep}{1-e\cos(\theta + \phi)}", 
                 r",\ (e, p):=\left(\frac{h^2}{GM}A,\ \frac{1}{A}\right)"]
        mtex_7 = MTex("".join(texts)).scale(0.5).next_to(0.7*DOWN + 7*LEFT)
        line_2 = Line(64/9*LEFT+1.15*DOWN, 64/9*RIGHT+1.15*DOWN).insert_n_curves(64)
        texts = [r"\Rightarrow A=\frac{1}{p}=\frac{c}{b^2},\ h=\sqrt{GM\frac{e}{A}}=\sqrt{GM\frac{b^2}{a}} \qquad\Rightarrow ", 
                 r"r^2\dot\theta = \sqrt{GM\frac{b^2}{a}}"]
        mtex_8 = MTex("".join(texts)).scale(0.5).next_to(1.6*DOWN + 7*LEFT)
        texts = [r"\frac{1}{2}hT=S=\pi ab\qquad\Rightarrow T=\frac{2\pi ab}{h}=2\pi ab\sqrt{\frac{a}{GMb^2}}=\sqrt{\frac{4\pi^2 a^3}{GM}}\qquad\Rightarrow ",
                 r"\frac{T^2}{a^3}=\frac{4\pi^2}{GM}"]
        mtex_9 = MTex("".join(texts)).scale(0.5).next_to(2.4*DOWN + 7*LEFT)

        super().__init__(mtex_1, mtex_2, mtex_3, line_1, mtex_4, mtex_5, mtex_6, mtex_7, line_2, mtex_8, mtex_9)

###################################################################

class SpreadOut(Animation):
    # 本部分代码来自一碗星空汤（b站ID：一碗星空咕）
    # 另外感谢不愿意透露姓名的群友（群内ID：嘤）的帮助，虽然他的代码最后没用上（）
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, **kwargs)

        self.center = mobject.get_center()
        self.radius = get_norm(mobject.get_corner(UL) - self.center)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        points = starting_submobject.data["points"] - self.center
        dr = self.radius * alpha

        to_delete = np.where(np.linalg.norm(points[1::3], axis = 1) > dr)
        deleted = np.delete(points.reshape((int(points.shape[0]/3), 3, 3)), to_delete, axis = 0) + self.center
        submobject.data["points"] = deleted.reshape(deleted.shape[0]*3, 3)

class UnRolled(Homotopy):
    CONFIG = {
        "run_time": 3,
        "major": 0.5,
        "minor": 0.25
    }

    def __init__(self, mobject, left_bound = -8, right_bound = 8, **kwargs):
        digest_config(self, kwargs, locals())
        a = self.major
        b = self.minor
        def homotopy(x, y, z, t):
            
            bottom = t * left_bound + (1-t) * right_bound
            if x >= bottom:
                return np.array([x, y, 0])
            else:
                angle = (x - bottom) / a
                return np.array([bottom, y, 0]) + b*UP + ellipse_unit(-PI/2 + angle, a, b)

        super().__init__(homotopy, mobject, **kwargs)

class RollUp(Homotopy):
    CONFIG = {
        "run_time": 3,
        "remover": True,
        "major": 0.5,
        "minor": 0.25
    }

    def __init__(self, mobject, left_bound = -8, right_bound = 8, **kwargs):
        digest_config(self, kwargs, locals())
        a = self.major
        b = self.minor
        def homotopy(x, y, z, t):
            
            bottom = t * left_bound + (1-t) * right_bound
            if x <= bottom:
                return np.array([x, y, 0])
            else:
                angle = (x - bottom) / a
                return np.array([bottom, y, 0]) + b*UP + ellipse_unit(-PI/2 + angle, a, b)

        super().__init__(homotopy, mobject, **kwargs)

class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
        "remover": True, 
        "target": None,
        "stretch": True, 
        "norm_func": get_norm,
        "speed": 1,
        "apply_function_kwargs": {}
    }

    def __init__(self, mobject: VMobject, **kwargs):
        digest_config(self, kwargs, locals())
        if self.target is None:
            self.target = mobject.get_center()
            self.apply_function_kwargs["about_point"] = self.target
        if self.stretch:
            scales = np.array([mobject.get_width() if mobject.get_width()>1e-8 else 1, 
                               mobject.get_height() if mobject.get_height()>1e-8 else 1, 
                               mobject.get_depth() if mobject.get_depth()>1e-8 else 1])
            def make_fn(fn, scales):
                return lambda t: fn(t / scales)
            self.norm_func = make_fn(self.norm_func, scales)
        else:
            scales = np.ones([3])
        
        max_distance = max(*[self.norm_func((mobject.get_corner(position)-self.target)) for position in [UL, UR, DL, DR]])
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            distance_ratio = self.norm_func(position) / max_distance
            if t >= distance_ratio:
                return ORIGIN
            else:
                length = 1 - t/distance_ratio
                angle = np.log(length)*self.speed
                rotation_matrix = np.array([unit(angle), unit(angle+PI/2), np.zeros(3)])
                moved = length * np.dot(position/scales, rotation_matrix)*scales
                return moved

        super().__init__(homotopy, mobject, **kwargs)

class PullOpen(Transform):
    def __init__(
        self,
        mobject: Mobject,
        shift: np.ndarray = ORIGIN,
        scale: float | npt.ArrayLike = 1,
        along_axis: int = 0,
        **kwargs
    ):
        self.shift_vect = shift
        if isinstance(scale, numbers.Number):
            self.scale_factor = np.ones(3)*scale
        else:
            self.scale_factor = scale
        self.scale_factor[along_axis] = np.inf
        super().__init__(mobject, **kwargs)
    
    def create_target(self) -> Mobject:
        return self.mobject

    def create_starting_mobject(self) -> Mobject:
        start = super().create_starting_mobject()
        start.scale(1.0 / self.scale_factor)
        start.shift(-self.shift_vect)
        return start
    
class Expand(Transform):
    def __init__(
        self,
        mobject: Mobject,
        **kwargs
    ):
        super().__init__(mobject, **kwargs)
    
    def create_target(self) -> Mobject:
        return self.mobject

    def create_starting_mobject(self) -> Mobject:
        start = super().create_starting_mobject()
        return start.scale(0)
    
class Grow(FadeInFromPoint):
    def __init__(
        self,
        mobject: Arrow, 
        **kwargs
    ):
        point = mobject.get_start()
        super().__init__(mobject, point, **kwargs)

class IndicateAround(FadeIn):
    CONFIG = {
        "run_time": 2, 
        "rate_func": double_there_and_back, 
        "remover": True
    }
    def __init__(
        self,
        mobject: Mobject,
        **kwargs
    ):
        super().__init__(SurroundingRectangle(mobject))

class OverFadeIn(FadeIn):
    CONFIG = {
        "over_factor": 2
    }
    def interpolate_submobject(
        self,
        submob: Mobject,
        start: Mobject,
        target_copy: Mobject,
        alpha: float
    ):
        submob.interpolate(start, target_copy, alpha, self.path_func)
        for key in submob.data:
            if key in ['rgbas', 'fill_rgba', 'stroke_rgba']:
                submob.data[key][:] = interpolate(
                start.data[key],
                target_copy.data[key],
                clip(1-(self.over_factor*(1-alpha)), 0, 1)
                )
        return self
    
class OverFadeOut(FadeOut):
    CONFIG = {
        "over_factor": 2
    }
    def interpolate_submobject(
        self,
        submob: Mobject,
        start: Mobject,
        target_copy: Mobject,
        alpha: float
    ):
        submob.interpolate(start, target_copy, alpha, self.path_func)
        for key in submob.data:
            if key in ['rgbas', 'fill_rgba', 'stroke_rgba', 'opacity']:
                submob.data[key][:] = interpolate(
                start.data[key],
                target_copy.data[key],
                clip(self.over_factor*alpha, 0, 1)
                )
        return self
    
def follow(mob: Mobject, guide, anim_class: type | None = None, direction: np.ndarray = ORIGIN, **kwargs):
    if isinstance(guide, Transform):
        offset = guide.create_target().get_bounding_box_point(direction) - guide.create_starting_mobject().get_bounding_box_point(direction)
        if isinstance(guide, TransformFromCopy):
            offset = -offset
    elif isinstance(guide, Mobject):
        if not hasattr(guide, "target") or guide.target is None:
            raise Exception("Trying to follow a mobject without its target")
        offset = guide.target.get_bounding_box_point(direction) - guide.get_bounding_box_point(direction)
    else:
        try:
            guide = prepare_animation(guide)
        except TypeError:
            raise TypeError(f"Unexpected argument {guide} passed to follow()")
        offset = guide.create_target().get_bounding_box_point(direction) - guide.create_starting_mobject().get_bounding_box_point(direction)
    if anim_class is None:
        return mob.animate.shift(offset)
    elif issubclass(anim_class, Fade):
        return anim_class(mob, shift = offset, **kwargs)
    else:
        raise TypeError(f"Unexpected animation class {anim_class} passed to follow()")

class ShowOut(ShowPartial):
    CONFIG = {
        "rate_func": linear,
        "remover": True,
    }

    def get_bounds(self, alpha: float) -> tuple[float, float]:
        return (back(alpha), fore(alpha))

    def finish(self) -> None:
        super().finish()
        for submob, start in self.get_all_families_zipped():
            submob.pointwise_become_partial(start, 0, 1)

class Erase(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
        "int_func": np.round,
    }

    def __init__(self, group: Mobject, **kwargs):
        self.all_submobs = list(group.submobjects)
        super().__init__(group, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        n_submobs = len(self.all_submobs)
        index = int(self.int_func(alpha * n_submobs))
        self.update_submobject_list(index)

    def update_submobject_list(self, index: int) -> None:
        self.mobject.set_submobjects(self.all_submobs[index:])

#################################################################### 

class AACamera(Camera):
    CONFIG = {
        "default_anti_alias_width": 1.5
    }
    def capture(self, *mobjects: Mobject, **kwargs) -> None:
        for mobject in mobjects:
            self.anti_alias_width = getattr(mobject, "anti_alias_width", self.default_anti_alias_width)
            self.refresh_perspective_uniforms()
            for render_group in self.get_render_group_list(mobject):
                self.render(render_group)

class CoverScene(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (16, 10)}, 
            },
        "camera_class": AACamera
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain: Rectangle = Rectangle(height = 9, width = 40/3, fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        self.add(self.domain)

class FrameScene(Scene):
    CONFIG = {
        "extra_frames": True,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frames: int = 0
        self.shade = Shade(is_fixed_in_frame = True, fill_color = BLACK)
        self.test_line = Line(3*DOWN+6*LEFT, 3*DOWN+6*RIGHT)

    def run(self) -> None:
        self.virtual_animation_start_time: float = 0
        self.real_animation_start_time: float = time.time()
        self.file_writer.begin()

        self.setup()
        try:
            if self.extra_frames:
                self.emit_frame() #将.mp4视频导入到Premiere中会被删去头尾两帧
            self.construct()
            self.print_mark()
            if self.extra_frames:
                self.emit_frame()
        except EndSceneEarlyException:
            pass
        self.tear_down()

    def print_mark(self):
        print(self.num_plays, self.time)

    def fade_out(self, excepts = [], **kwargs):
        self.add(self.shade, *excepts)
        anims = [FadeIn(self.shade)]
        self.play(*anims, **kwargs)
        self.clear().add(*excepts)
        return self
    
    def fade_in(self, *mobjects, excepts = [], **kwargs):
        anims = [FadeOut(self.shade)]
        self.add(*mobjects, self.shade, *excepts).play(*anims, **kwargs)
        return self

    def update_frame(self, df: int = 0, ignore_skipping: bool = False) -> None:
        dt = df / self.camera.frame_rate
        self.increment_time(df)
        self.update_mobjects(dt)
        if self.skip_animations and not ignore_skipping:
            return

        if self.window:
            self.window.clear()
        self.camera.clear()
        self.camera.capture(*self.mobjects)

        if self.window:
            self.window.swap_buffers()
            vt = self.time - self.virtual_animation_start_time
            rt = time.time() - self.real_animation_start_time
            if rt < vt:
                self.update_frame(0)

    def increment_time(self, df: int) -> None:
        self.frames += df
        self.time = self.frames / self.camera.frame_rate

    def get_time_progression(
        self,
        run_frames: int,
        n_iterations: int | None = None,
        desc: str = "",
        override_skip_animations: bool = False
    ) -> list[float] | np.ndarray | ProgressDisplay:
        if self.skip_animations and not override_skip_animations:
            return [run_frames]
        else:
            frames = [i+1 for i in range(run_frames)]

        if self.file_writer.has_progress_display:
            self.file_writer.set_progress_display_subdescription(desc)
            return frames

        return ProgressDisplay(
            frames,
            total=n_iterations,
            leave=self.leave_progress_bars,
            ascii=True if platform.system() == 'Windows' else None,
            desc=desc,
        )
    
    def handle_play_like_call(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.inside_embed:
                self.save_state()

            self.update_skipping_status()
            should_write = not self.skip_animations
            if should_write:
                self.file_writer.begin_animation()

            if self.window:
                self.real_animation_start_time = time.time()
                self.virtual_animation_start_time = self.time

            self.refresh_static_mobjects()
            func(self, *args, **kwargs)

            if should_write:
                self.file_writer.end_animation()

            if self.inside_embed:
                self.save_state()

            self.num_plays += 1
            return self
        return wrapper
    
    @handle_play_like_call
    def wait(
        self,
        seconds: int = DEFAULT_WAIT_TIME,
        frames: int = 0,
        stop_condition: Callable[[], bool] = None,
        note: str = None,
        ignore_presenter_mode: bool = False
    ):
        self.update_mobjects(dt=0)  # Any problems with this?
        if self.presenter_mode and not self.skip_animations and not ignore_presenter_mode:
            if note:
                log.info(note)
            while self.hold_on_wait:
                self.update_frame(dt=1 / self.camera.frame_rate)
            self.hold_on_wait = True
        else:
            time_progression = self.get_wait_time_progression(seconds*self.camera.frame_rate + frames, stop_condition)
            last_f = 0
            for f in time_progression:
                df = f - last_f
                last_f = f
                self.update_frame(df)
                self.emit_frame()
                if stop_condition is not None and stop_condition():
                    break
        self.refresh_static_mobjects()
        return self
    
    def get_animation_time_progression(
        self,
        animations: Iterable[Animation],
        frames: None
    ) -> list[float] | np.ndarray | ProgressDisplay:
        
        run_time = self.get_run_time(animations)
        if frames is not None:
            if run_time > frames / self.camera.frame_rate:
                log.warning("Not enough frames for the longest animation")
        else:
            frames = int(run_time * self.camera.frame_rate)

        description = f"{self.num_plays} {animations[0]}"
        if len(animations) > 1:
            description += ", etc."
        time_progression = self.get_time_progression(frames, desc=description)
        return time_progression
    
    def progress_through_animations(self, animations: Iterable[Animation], frames = None) -> None:
        last_f = 0
        for f in self.get_animation_time_progression(animations, frames):
            df = f - last_f
            last_f = f
            dt = df / self.camera.frame_rate
            for animation in animations:
                animation.update_mobjects(dt)
                alpha = f / self.camera.frame_rate / animation.run_time
                animation.interpolate(alpha)
            self.update_frame(df)
            self.emit_frame()

    @handle_play_like_call
    def play(self, *args, **kwargs) -> None:
        if len(args) == 0:
            log.warning("Called Scene.play with no animations")
            return
        if "frames" in kwargs:
            frames = kwargs.pop("frames")
        else:
            frames = None
        animations = self.anims_from_play_args(*args, **kwargs)
        self.begin_animations(animations)
        self.progress_through_animations(animations, frames)
        self.finish_animations(animations)

class NoticeScene(FrameScene):
    CONFIG = {
        "extra_frames": True,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frames: int = 0
        self.shade = Shade(is_fixed_in_frame = True)
        self.test_line = Line(3*DOWN+6*LEFT, 3*DOWN+6*RIGHT)

    def show_notice(self, animation = Write):
        return animation(self.notices[0])

    def change_notice(self, **kwargs):
        i = self.notice_index
        self.notice_index += 1
        return Transform(self.notices[0], self.notices[i+1], **kwargs)

    def fade_out(self, change_notice = False, end = False, excepts = [], **kwargs):
        if not end:
            self.add(self.shade, *excepts, self.notices[0])
        anims = [FadeIn(self.shade)]
        if change_notice:
            anims.append(self.change_notice())
        self.play(*anims, **kwargs)
        self.clear()
        if not end:
            self.add(*excepts, self.notices[0])
        return self
    
    def fade_in(self, *mobjects, change_notice = False, excepts = [], **kwargs):
        anims = [FadeOut(self.shade)]
        if change_notice:
            anims.append(self.change_notice())
        self.add(*mobjects, self.shade, *excepts, self.notices[0]).play(*anims, **kwargs)
        return self
