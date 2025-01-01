from manim import *
import numpy as np

#################################################################### 

class NN(Scene):
    def construct(self):
        buff_h, buff_v = 1, 0.35
        m, n = 5, (8, 6, 3, 6, 8)
        dots = [VGroup(*[Dot((i-(m-1)/2)*buff_h*RIGHT + (j-(n[i]-1)/2)*buff_v*UP, stroke_width = 2, fill_opacity = 0, radius = 0.12) for j in range(n[i])]) for i in range(m)]
        lines = []
        for i in range(m-1):
            line = VGroup(*[Line(dot_1, dot_2, stroke_width = 1) for dot_1 in dots[i] for dot_2 in dots[i+1]])
            lines.append(line)
        nn = VGroup(*lines, *dots)        

        img = ImageMobject("dog.png").scale(0.25).move_to(4*LEFT)
        # get dog image array
        img_arr = img.pixel_array / 255.0
        noise = np.random.randn(*img_arr.shape)
        alpha = 0.5
        noisy_array = np.clip(img_arr + alpha * noise, 0, 1)
        img_add_noise = ImageMobject(np.uint8(noisy_array*255)).scale(0.25).move_to(4*RIGHT)

        noise_clip = np.clip(noise / 2 + 0.5, 0, 1)
        img_noise = ImageMobject(np.uint8(noise_clip*255)).scale(0.25)

        plus_sign = MathTex("+").scale(2).shift(2 * LEFT)
        equal_sign = MathTex("=", color=YELLOW).scale(2).shift(2 * RIGHT)

        self.play(FadeIn(img), run_time = 1)
        self.wait()
        self.play(FadeIn(img_noise), run_time = 1)
        self.wait()
        self.play(Create(plus_sign), run_time = 1)
        self.wait()
        self.play(Create(equal_sign), run_time = 1)
        self.wait()
        self.play(FadeIn(img_add_noise), run_time = 1)
        self.wait(3)

        _img = img.copy().scale(0.6).shift(2*UP)
        _img_add_noise = img_add_noise.copy().scale(0.6).shift(2*UP)
        _img_noise = img_noise.copy().scale(0.6).shift(2*UP)
        _plus_sign = plus_sign.copy().shift(2*UP).scale(0.6)
        _equal_sign = equal_sign.copy().shift(2*UP).scale(0.6)

        self.play(
            *[Transform(m1, m2) for m1, m2 in zip([img, img_add_noise, img_noise, plus_sign, equal_sign], [_img, _img_add_noise, _img_noise, _plus_sign, _equal_sign])],
        )
        self.wait(2)

        for obj in nn:
            obj.shift(1.5*DOWN)
        self.play(FadeIn(nn), run_time = 2)

        input_img = ImageMobject(np.uint8(noisy_array*255)).scale(0.25).shift(1.5*DOWN + 4 * LEFT)
        output_img = ImageMobject("dog.png").scale(0.25).shift(1.5*DOWN + 4 * RIGHT)
        self.wait(2)

        self.play(TransformFromCopy(_img_add_noise, input_img), run_time = 1)
        self.wait()

        # show passing flash of nn's lines
        self.play(
            *[ShowPassingFlash(line.copy().set_color(YELLOW), time_width = 0.5, run_time = 1) for line in lines],
        )
        self.wait()
        self.play(GrowFromCenter(output_img), run_time = 1)
        self.wait(3)

        UNet = Text("U-Net", font = "Arial", color=BLUE).scale(1.2).next_to(nn, UP, buff = 0.2)
        name = Text("去噪模型 Denoising Model", color=YELLOW).set_stroke(width=8, background=True).to_edge(UP)
        sep_line = Line(7*LEFT, 7*RIGHT, color = WHITE).next_to(name, DOWN, buff = 0.2)

        self.play(Write(UNet), 
                  *[FadeOut(obj) for obj in [img, img_add_noise, img_noise, plus_sign, equal_sign]],
                  run_time = 1)
        self.wait()
        self.play(Write(name), GrowFromCenter(sep_line), run_time = 1)
        self.wait(3)
