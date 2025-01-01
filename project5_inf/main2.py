from manim import *
import numpy as np
from functools import partial
import math

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
        self.wait(2)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class ArcEqLine(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        # Draw a half circle and flip down, and mark the center
        hc = Arc(radius=1, angle=PI, arc_center=ORIGIN, color=BLUE, stroke_width=2)
        # Rotate the half circle 180 degrees around the center
        hc.rotate(PI, about_point=ORIGIN).shift(UP*1.5)
        hc_center = Dot(UP*1.5, color=RED, stroke_width=0.5)

        # draw two little hollow circle at the terminal points of the half circle
        hc_t1 = Circle(radius=0.05, color=BLUE, stroke_width=0.5).move_to(hc.get_start())
        hc_t2 = Circle(radius=0.05, color=BLUE, stroke_width=0.5).move_to(hc.get_end())
        line = Line(LEFT*10, RIGHT*10, color=GOLD, stroke_width=2).shift(DOWN*0.5)
        self.play(
            DrawBorderThenFill(hc),
            DrawBorderThenFill(hc_t1),
            DrawBorderThenFill(hc_t2),
            Create(line),
            run_time=2
        )
        
        self.wait(3)
        self.play(Create(hc_center), run_time=1)
        self.wait(1)

        theta = ValueTracker(PI/3)
        # Draw a ray from the center to illustrate the corresponding relationship between every point on the circle and the line
        # The ray direction is cos(theta)*LEFT+sin(theta)*DOWN

        ray = always_redraw(
            lambda: Line(UP*1.5, 0.5*DOWN + 2/math.tan(theta.get_value()) * LEFT, color=WHITE, stroke_width=2, buff=0)
        )
        inter1 = always_redraw(
            lambda: Dot(0.5*DOWN + 2/math.tan(theta.get_value())*LEFT, color=GOLD, stroke_width=4)
        )
        inter2 = always_redraw(
            lambda: Dot(math.cos(theta.get_value())*LEFT + math.sin(theta.get_value())*DOWN + 1.5*UP, color=BLUE, stroke_width=4)
        )

        self.play(LaggedStart(
            Create(ray),
            Create(inter1),
            Create(inter2)), run_time=2, lag_ratio=0.5)
        self.wait(2)
        self.play(
            Flash(inter1),
            Flash(inter2),
            run_time=1
        )
        self.wait(2)
        self.play(theta.animate.set_value(0.1), run_time=3, rate_func=there_and_back)
        self.play(theta.animate.set_value(PI-0.1), run_time=6, rate_func=there_and_back)
        self.wait(2)


class HotelLight(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        # set numpy random seed
        np.random.seed(233)

        room = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\room.svg")
        def create_room(i):
            return room.copy().scale(0.6).shift(LEFT*6+i*1.2*RIGHT)
        
        random_bits = np.random.randint(0, 2, 40)
        HT = VGroup()
        for i in range(40):
            opacity = 1 if random_bits[i] == 1 else 0.1
            HT.add(create_room(i).set_opacity(opacity))
        
        product_rule = MathTex("2", r"\times 2", r"\times 2", r"\times 2 \times 2 \times 2 \times 2 \times \cdots", color=YELLOW).shift(DOWN*1.5)

        for i in range(3):
            time = 1 if i == 0 else 0.2
            opc = 0.1 if random_bits[i] else 1
            self.play(FadeIn(HT[i]), run_time=1)
            self.wait()
            self.play(HT[i].animate.set_opacity(opc), run_time=0.3)
            self.wait(time)
            self.play(HT[i].animate.set_opacity(1.1 - opc), run_time=0.3)
            self.wait(time)
            self.play(Write(product_rule[i]), run_time=time)
            self.wait(time)
        
        self.play(
            LaggedStart(
                *[FadeIn(HT[i]) for i in range(3, 40)],
                lag_ratio=0.7
            ),
            Write(product_rule[3]),
            run_time=3
        )
        self.wait(2)

        for _ in range(16):
            random_bits = np.random.randint(0, 2, 40)
            self.play(
                *[HT[i].animate.set_opacity(1 if random_bits[i] else 0.1) for i in range(40)],
                run_time=0.3
            )
            self.wait(0.2)
        
        self.wait(2)
        underbrace = Brace(product_rule, DOWN, color=YELLOW)
        ub_text = MathTex(r"\aleph_0", color=YELLOW).scale(1.5).next_to(underbrace, DOWN)
        self.play(
            GrowFromCenter(underbrace),
            Write(ub_text),
            run_time=1
        )
        self.wait(2)
        self.play(FadeOut(underbrace), FadeOut(ub_text), run_time=1)
        self.wait(2)
        result = MathTex(r"2^{\aleph_0}", color=BLUE).scale(2).move_to(product_rule)
        self.play(
            ReplacementTransform(product_rule, result),
            run_time=2
        )
        self.wait()
        self.play(Circumscribe(result))
        self.wait(2)

        # Transform each HT[i] into a mathtex 0 or 1 based on random_bits[i]
        translate_result = VGroup()
        for i in range(40):
            translate_result.add(MathTex(str(random_bits[i]), color=GOLD).scale(2).move_to(HT[i]))
        
        for i in range(3):
            self.play(
                TransformFromCopy(HT[i], translate_result[i]),
            )
            self.wait(0.5)
        
        self.play(
            LaggedStart(
                *[TransformFromCopy(HT[i], translate_result[i]) for i in range(3, 40)],
                lag_ratio=0.7
            ),
            run_time=5
        )

        # Create destination digits that are compactly arranged as a sequence, and scale 0.5
        dest = VGroup()
        dest.add(MathTex(str(random_bits[0]), color=RED).shift(UP*2+LEFT*4))
        for i in range(1, 40):
            dest.add(MathTex(str(random_bits[i]), color=RED).next_to(dest[-1], RIGHT, buff=0.1))

        self.wait(2)
        self.play(
            LaggedStart(
                *[ReplacementTransform(translate_result[i], dest[i]) for i in range(40)],
                lag_ratio=0.7
            ),
            run_time=5
        )
        self.wait(5)
        # Add a "0." in front of the sequence
        pre = MathTex("0.", color=RED).scale(2).next_to(dest[0], LEFT, buff=0.2)
        self.play(Write(pre), run_time=2)
        self.wait(2)
        # FadeOut the HT, and create a number line instead.
        nline = NumberLine(x_range=[-0.1, 1.1, 0.1], 
                           length=10, 
                           include_numbers=True, 
                           label_direction=DOWN,
                           include_ticks=True, 
                           include_tip=True,
                           color=BLUE
                           )
        self.play(
            FadeOut(HT),
            run_time=1
        )
        self.wait(2)
        self.play(
            DrawBorderThenFill(nline),
            run_time=2
        )
        self.wait(2)

        # Calculate the decimal value of the binary sequence
        def seq2value(bits):
            decimal = 0
            for i in range(40):
                decimal += bits[i] * 2**(-i-1)
            return decimal
        
        decimal = seq2value(random_bits)
        x_value = ValueTracker(decimal)
        # Write the decimal value on the number line, and draw an arrow pointing to the position on the number line
        arrow = always_redraw(
            lambda: Arrow(nline.number_to_point(x_value.get_value())+UP*0.8, nline.number_to_point(x_value.get_value()), color=BLUE, buff=0.05)
        )
        decimal_text = always_redraw(
            lambda: MathTex(r"\approx"+format(x_value.get_value(), '.3f'), color=BLUE).next_to(arrow, UP, buff=0.1)
        )
        self.play(
            Write(decimal_text),
            Create(arrow),
            run_time=2
        )
        self.wait(2)

        seq_list = []
        decimal_list = []
        # Switch the random sequence several times and change the decimal value and arrow accordingly
        for _ in range(3):
            bits = np.random.randint(0, 2, 40)
            decimal = seq2value(bits)
            _dest = VGroup()
            _dest.add(MathTex(str(bits[0]), color=RED).shift(UP*2+LEFT*4))
            for i in range(1, 40):
                _dest.add(MathTex(str(bits[i]), color=RED).next_to(_dest[-1], RIGHT, buff=0.1))
            seq_list.append(_dest)
            decimal_list.append(decimal)
        
        for i in range(3):
            self.play(
                Transform(dest, seq_list[i]),
                x_value.animate.set_value(decimal_list[i]),
                run_time=1
            )
            self.wait(0.5)
        
        self.wait(2)
        # Draw a line from 0 to 1
        line01 = Line(nline.number_to_point(0), nline.number_to_point(1), color=YELLOW, stroke_width=8).shift(DOWN*0.1)
        self.play(Create(line01), run_time=2)
        rect = SurroundingRectangle(result, color=YELLOW)
        self.play(Create(rect), run_time=1)
        self.wait(2)

class BaseIrrelevant(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        n1 = MathTex(r"2^{\aleph_0}", color=BLUE).scale(2).shift(UP + LEFT)
        eq_sign = MathTex(r"=", color=BLUE).scale(2).next_to(n1, RIGHT)
        q1 = MathTex(r"2^{\aleph_0}", color=GREEN).scale(2).next_to(eq_sign, RIGHT, buff=1)
        q2 = MathTex(r"3^{\aleph_0}", color=GREEN).scale(2).next_to(eq_sign, RIGHT, buff=1)
        q3 = MathTex(r"4^{\aleph_0}", color=GREEN).scale(2).next_to(eq_sign, RIGHT, buff=1)
        q4 = MathTex(r"10^{\aleph_0}", color=GREEN).scale(2).next_to(eq_sign, RIGHT, buff=1)
        q5 = MathTex(r"114514^{\aleph_0}", color=ORANGE).scale(2).next_to(eq_sign, RIGHT, buff=1)
        self.play(
            DrawBorderThenFill(n1),
            run_time=2
        )
        self.wait(2)
        self.play(
            Write(eq_sign),
            TransformFromCopy(n1, q1),
            run_time=1
        )
        self.wait(2)
        self.play(
            Transform(q1, q2),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            Transform(q1, q3),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            Transform(q1, q4),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            Transform(q1, q5),
            run_time=1
        )
        self.wait(2)

class ArbLarge(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()
        text = Text("无穷大不是任意大的有限", color=YELLOW).scale(2)
        self.play(DrawBorderThenFill(text), run_time=2)
        self.wait(2)
        self.play(FadeOut(text), run_time=1)
        self.wait(2)    
        # 这里需要强调一个很重要的问题：无穷大不是可以任意大的有限。
        # 这句话有些抽象，我们来找个例子。
        # 比如上期视频我们说过，给定一个语言的词汇符号表，所有这个语言能够说出的句子、诗歌乃至于文学作品都是可数无穷多的。
        # 所以，你可以一一枚举每一个整数，然后逐一将它们翻译，查看它的文学价值。

        # 这就是刘慈欣所说的“诗云”。
        shiyun = Text("诗云", color=BLUE).scale(2)
        self.play(DrawBorderThenFill(shiyun), run_time=2)
        self.wait(2)
        self.play(FadeOut(shiyun), run_time=1)
        self.wait(2)
        # 只要是用的字都在约定好的词汇表以内，哪怕是曹雪芹的红楼、或者是莎士比亚伟大的戏剧，
        honglou = Text("第一回 甄士隐梦幻识通灵 贾雨村风尘怀闺秀 ...", color=GOLD).scale(0.8).shift(UP*2)
        self.play(Write(honglou), run_time=2)
        self.wait()
        romeo = Text("Two households, both alike in dignity, In fair Verona, ...", color=MAROON).scale(0.8).shift(DOWN*1.5)
        self.play(Write(romeo), run_time=2)
        self.wait(2)
        # 总会在你数到某一个天文数字的时候被如此翻译出来，
        calc_honglou = MathTex(r"2^{46328}\times 3^{45217} \times 5^{47582} \times 7^{32} \times 11^{54716} \cdots", 
                               color=ORANGE).scale(0.6).next_to(honglou, DOWN, buff=0.2)
        self.play(Write(calc_honglou), run_time=2)
        calc_romeo = MathTex(r"2^{84}\times  3^{119} \times 5^{111} \times 7^{32} \times 11^{104} \times 13^{111} \times \cdots", 
                             color=TEAL).scale(0.6).next_to(romeo, DOWN, buff=0.2)
        self.play(Write(calc_romeo), run_time=2)
        self.wait(4)
        # 因为归根结底一部作品都唯一对应到了一个有限大的整数而已。
        # 实际上，这里暗含了一个重要、却又常常被我们忽略的假设：
        # 那就是，所有人类的作品都是有限长度的。
        finite_len_text = Text("人类的作品长度都是有限的", color=WHITE).scale(1.2).set_stroke(background=True)
        self.play(Write(finite_len_text), run_time=3)
        self.wait(5)
        # 这听起来很废话，但正是这个重要的假设，导出了所有的文学作品和数学证明都是可数无穷多这个论断。
        # 刚才这个希尔伯特旅馆开灯的问题已经向你展示了，一旦这个长度达到了阿列夫0这么长，
        # 那么即使我们的词汇表里只有两个词，0或者1，
        # 那么所有无限长句子的数量也立刻达到的不可数的实数无穷，而远远超过了可数无穷的大小。
        # 2的阿列夫0次方，不等于2的n次方，在n趋近于无穷大的极限，千万不要在这里和微积分混淆
        self.play(FadeOut(finite_len_text))
        self.wait(2)
        noteq = MathTex(r"2^{\aleph_0}", r"\neq", r"\lim_{n\to \infty} 2^n", color=RED).scale(2)
        self.play(Write(noteq), run_time=2)
        self.wait(3)

class MiddleLine(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        px = ValueTracker(0)
        aux_pt = Dot(color=RED, stroke_width=0.5).add_updater(lambda m: m.move_to(px.get_value()*RIGHT+UP*2))

        ratio = ValueTracker(0.5)
        line = Line(LEFT*3, RIGHT*3, color=BLUE, stroke_width=5).shift(DOWN*2)
        
        inter_line = always_redraw(
            lambda: Line(ratio.get_value()*(3*LEFT+2*DOWN)+(1-ratio.get_value())*(px.get_value()*RIGHT+UP*2), 
                         ratio.get_value()*(3*RIGHT+2*DOWN)+(1-ratio.get_value())*(px.get_value()*RIGHT+UP*2), 
                         color=GREEN, stroke_width=5)
        )
        
        aux_l1 = always_redraw(
            lambda: DashedLine(line.get_start(), px.get_value()*RIGHT+UP*2, color=YELLOW, stroke_width=2)
        )
        aux_l2 = always_redraw(
            lambda: DashedLine(line.get_end(), px.get_value()*RIGHT+UP*2, color=YELLOW, stroke_width=2)
        )

        self.play(
            LaggedStart(
                Create(inter_line),
                Create(line),
                lag_ratio=0.5
            ), run_time=2
        )
        self.wait()
        self.play(
            LaggedStart(
                Create(aux_l1),
                Create(aux_l2),
                Create(aux_pt),
                lag_ratio=0.3
            ), run_time=2
        )
        self.wait(2)
        
        t = ValueTracker(0.1)
        ray = always_redraw(
            lambda: Line(aux_pt.get_center(), line.get_start()+t.get_value()*(line.get_end()-line.get_start()), color=WHITE, stroke_width=2)
        )
        intersect_p1 = always_redraw(
            lambda: Dot(line.get_start()+t.get_value()*(line.get_end()-line.get_start()), color=RED, stroke_width=4)
        )
        intersect_p2 = always_redraw(
            lambda: Dot(color=RED, stroke_width=4).move_to(
                (1-t.get_value())*(ratio.get_value()*(3*LEFT+2*DOWN)+(1-ratio.get_value())*(px.get_value()*RIGHT+UP*2))
                +t.get_value()*(ratio.get_value()*(3*RIGHT+2*DOWN)+(1-ratio.get_value())*(px.get_value()*RIGHT+UP*2))
            )
        )
        self.play(
            LaggedStart(
                Create(ray),
                Create(intersect_p1),
                Create(intersect_p2),
                lag_ratio=0.3
            ), run_time=2
        )
        self.wait(2)
        self.play(t.animate.set_value(0.99), run_time=4, rate_func=there_and_back)
        self.play(t.animate.set_value(0.4), run_time=1.5, rate_func=smooth)
        self.wait()
        self.play(px.animate.set_value(1.5), run_time=3, rate_func=there_and_back)
        self.wait()
        self.play(ratio.animate.set_value(0.1), t.animate.set_value(0.05),
                  run_time=1, rate_func=smooth)
        self.play(ratio.animate.set_value(0.85),  t.animate.set_value(0.95),
                  run_time=3, rate_func=smooth)
        self.play(ratio.animate.set_value(0.5),  t.animate.set_value(0.5),
                  run_time=1.5, rate_func=smooth)
        self.wait(2)

        two_alenull = MathTex(r"2^{\aleph_0}", color=GREEN).next_to(inter_line, RIGHT, buff=0.1)
        two_alenull_plus1 = MathTex(r"2\times 2^{\aleph_0}", color=BLUE).next_to(line, RIGHT, buff=0.1)
        _eq2 = MathTex(r"2^",r"{\aleph_0+1}", color=BLUE).next_to(line, RIGHT, buff=0.1)
        rect = SurroundingRectangle(_eq2[1], color=YELLOW)
        eq_aleph0 = MathTex(r"=\aleph_0", color=YELLOW).scale(0.7).next_to(rect, RIGHT, buff=0.1)
        _eq3 = MathTex(r"2^{\aleph_0}", color=BLUE).next_to(line, RIGHT, buff=0.1)
        self.play(Write(two_alenull), run_time=1)
        self.wait()
        self.play(Write(two_alenull_plus1), run_time=1)
        self.wait()
        self.play(Transform(two_alenull_plus1, _eq2), run_time=1)
        self.wait()
        self.play(Create(rect), Write(eq_aleph0), run_time=1)
        self.wait()
        self.play(FadeOut(rect), FadeOut(eq_aleph0), run_time=1)
        self.wait()
        self.play(Transform(two_alenull_plus1, _eq3), run_time=1)
        self.wait(2)
        self.play(
            *[FadeOut(obj) for obj in self.mobjects]
        )

class BinaryDecimal(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        Decimal = MathTex("0.", "1", "2", "3", "4", "5", color=BLUE).scale(1.5).shift(UP*2+LEFT*3)
        fractal = VGroup()
        for i in range(1, 6):
            fractal.add(MathTex(r"\times \frac{1}{10^{" + str(i) +"}}").scale(0.6).set_color(GOLD))
        final_eq = MathTex(r"=1\times \frac{1}{10^1}+2\times \frac{1}{10^2}+3\times \frac{1}{10^3}+4\times \frac{1}{10^4}+5\times \frac{1}{10^5}", color=BLUE).scale(0.8)
        final_eq.align_to(Decimal, LEFT)
        self.play(
            Write(Decimal),
            run_time=1
        )
        self.wait()
        self.play(
            LaggedStart(
                *[Decimal[i].animate.shift(RIGHT*i*0.5) for i in range(6)], 
            ),
            lag_ratio=0.3, run_time=1
        )
        for i in range(5):
            fractal[i].next_to(Decimal[i+1], DOWN, buff=0.1)
        self.play(
            LaggedStart(
                *[Write(fractal[i]) for i in range(5)],
                lag_ratio=0.3
            ),
            run_time=1
        )
        self.wait(0.5)
        self.play(Write(final_eq), run_time=2)
        self.wait(2)
        self.play(
            *[FadeOut(obj) for obj in self.mobjects if obj not in [text_1, text_2]]
        )
        binary_dec = MathTex("0.", "1", "0", "1", "0", "1", "1", "0", color=BLUE).scale(1.5).shift(UP*2+LEFT*3)
        binary_fractal = VGroup()
        for i in range(1, 8):
            binary_fractal.add(MathTex(r"\times \frac{1}{2^{" + str(i) +"}}").scale(0.6).set_color(GOLD))
        calc_equation = MathTex(r"=1\times \frac{1}{2^1}+0\times \frac{1}{2^2}+1\times \frac{1}{2^3}+0\times \frac{1}{2^4}+1\times \frac{1}{2^5}+1\times \frac{1}{2^6}+0\times \frac{1}{2^7}", color=ORANGE).scale(0.7).next_to(binary_dec, DOWN, buff=1)
        calc_equation.align_to(final_eq, LEFT)
        result = MathTex(r"=0.671875", color=ORANGE).next_to(calc_equation, DOWN, buff=0.3).align_to(calc_equation, LEFT)
        self.play(
            Write(binary_dec),
            run_time=1
        )
        self.wait()
        self.play(
            LaggedStart(
                *[binary_dec[i].animate.shift(RIGHT*i*0.5) for i in range(8)], 
            ),
            lag_ratio=0.3, run_time=1
        )
        for i in range(7):
            binary_fractal[i].next_to(binary_dec[i+1], DOWN, buff=0.1)
        self.play(
            LaggedStart(
                *[Write(binary_fractal[i]) for i in range(7)],
                lag_ratio=0.3
            ),
            run_time=1
        )
        self.wait(0.5)
        self.play(Write(calc_equation), run_time=1)
        self.wait()
        self.play(Write(result), run_time=1)
        self.wait(2)

class DimInf(Scene):
    def EnlargeIndicate(self, obj_list, scale_factor=1.2, color=YELLOW, pause_time=1, run_time=0.5):
        """Play animations that first enlarge all the obj in obj_list by scale_factor and turn into color,
         stay for run_time, then return to the original size."""
        orig_color_list = [obj.get_color() for obj in obj_list]
        anims = []
        for obj in obj_list:
            anims.append(obj.animate.scale(scale_factor).set_color(color))
        self.play(*anims, run_time=run_time)
        self.wait(pause_time)
        anims = []
        for obj, orig_color in zip(obj_list, orig_color_list):
            anims.append(obj.animate.scale(1/scale_factor).set_color(orig_color))
        self.play(*anims, run_time=run_time)
        return
        
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()
        # 这可能会让你很吃惊，毕竟，看起来无限长的线显然比有限长的线拥有的点的数量更多。
        # 但实际上把有限长变成无限长，无法进一步提高无穷大的势。
        # 那么，升高维度可不可以提升呢？比如说，线动成面，用实数无穷多根线段组成一个正方形，能不能获得更多的点呢？
        # Draw a line, and move it downwards, it brushes out a square
        pos = ValueTracker(0)
        line = Line(LEFT*2, RIGHT*2, color=ORANGE, stroke_width=1).add_updater(lambda m: m.move_to(UP*2+DOWN*pos.get_value()))
        self.play(Create(line), run_time=2)
        self.wait()
        grow_rectangle = always_redraw(
            lambda: Rectangle(height=pos.get_value(), width=4, color=BLUE, fill_color=BLUE, fill_opacity=0.5,
                              stroke_width=0.).shift(UP*2+DOWN*pos.get_value()/2)
        )
        self.play(Create(grow_rectangle), run_time=0.5)
        self.play(pos.animate.set_value(4), run_time=4, rate_func=smooth)
        self.wait(2)
        gr_aleph1 = MathTex(r"> 2^{\aleph_0}", color=BLUE).scale(1.5).next_to(grow_rectangle, RIGHT, buff=0.2)
        fact_eq = MathTex(r"= 2^{\aleph_0}", color=GREEN).scale(1.5).next_to(grow_rectangle, RIGHT, buff=0.2)
        question = MathTex(r"?", color=YELLOW).scale(4).move_to(gr_aleph1).add_background_rectangle()
        self.play(Write(gr_aleph1), run_time=1)
        self.wait()
        self.play(Write(question), run_time=1)
        self.wait(2)

        # 很可惜，答案是否定的。一根一维的线和一个二维的正方形的点是完全一样多的。
        self.play(FadeOut(question))
        self.play(Transform(gr_aleph1, fact_eq), run_time=2)
        self.wait(2)
        # 这个事实有三种不同的理解方式，
        self.play(FadeOut(gr_aleph1))
        # 第一种，直接计算：任何一个正方形内的点可以用两个坐标表示，
        pt = Dot(color=RED, stroke_width=3).move_to(UP+RIGHT*0.5)
        pt_lbl = MathTex("(x,y)", color=YELLOW).next_to(pt, DOWN, buff=0.1).add_background_rectangle()
        self.play(Create(pt), Write(pt_lbl), run_time=1)
        self.wait(2)
        # 所以根据乘法原理，一共有2的aleph0次方乘以2的aleph0次方个点，
        prod = MathTex(r"2^{\aleph_0}\times 2^{\aleph_0}", color=BLUE).scale(2).next_to(grow_rectangle, DOWN, buff=0.2)
        _e1 = MathTex(r"2^", r"{2\aleph_0}", color=BLUE).scale(2).next_to(grow_rectangle, DOWN, buff=0.2)
        _e2 = MathTex(r"=2^", r"{\aleph_0}", color=BLUE).scale(2).next_to(_e1, RIGHT, buff=0.2)
        # 指数上是2aleph0，而我们刚才已经证明了，它依然是aleph0本身，
        rect = SurroundingRectangle(_e1[1], color=YELLOW)
        eq_aleph0 = MathTex(r"=\aleph_0", color=YELLOW).scale(0.7).next_to(rect, RIGHT, buff=0.1)
        self.play(Write(prod), run_time=1)
        self.wait(2)
        self.play(Transform(prod, _e1), run_time=2)
        self.wait(2)
        self.play(Create(rect), Write(eq_aleph0), run_time=2)
        self.wait(2)
        self.play(FadeOut(rect), FadeOut(eq_aleph0), run_time=2)
        self.wait(2)
        self.play(DrawBorderThenFill(_e2), run_time=2)
        self.wait(2)
        # 所以最终的结果还是实数无穷。
        self.play(Circumscribe(_e2), run_time=1)
        self.wait(2)
        # 第二种方法，我们来构造一个单位线段上的坐标和正方形内部坐标的一一对应，
        static_square = Rectangle(height=2, width=2, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=0.).shift(UP*2+LEFT*3)
        seg = Line(LEFT, RIGHT, color=ORANGE, stroke_width=5).shift(UP*2+RIGHT*3)
        _pt = pt.copy().scale(0.5).move_to(static_square.get_center()+0.5*UP+0.25*RIGHT)
        _pt_lbl = pt_lbl.copy().scale(0.5).next_to(_pt, DOWN, buff=0.05).add_background_rectangle()

        self.play(FadeOut(prod), FadeOut(_e2), FadeOut(line), run_time=1)
        self.wait(2)
        self.play(ReplacementTransform(grow_rectangle, static_square),
                  Transform(pt, _pt),
                  Transform(pt_lbl, _pt_lbl), 
                  Create(seg),
                  run_time=2)
        self.wait(2)

        # 具体方法是，我们写出一维线段上点坐标的小数形式，
        x_dec = MathTex(r"0.", "2", "3", "1", "7", "5", "8", "0", "9", "2", "4", r"\cdots", color=BLUE).scale(1.5).shift(LEFT*3)
        y_dec = MathTex(r"0.", "5", "8", "6", "1", "3", "5", "4", "2", "7", "6", r"\cdots", color=YELLOW).scale(1.5).next_to(x_dec, DOWN, buff=0.1).align_to(x_dec, LEFT)
        x_dengyu = MathTex(r"x=", color=BLUE).scale(1.5).next_to(x_dec, LEFT, buff=0.1)
        y_dengyu = MathTex(r"y=", color=YELLOW).scale(1.5).next_to(y_dec, LEFT, buff=0.1)
        self.play(LaggedStart(Write(x_dengyu), Write(x_dec), Write(y_dengyu),
                               Write(y_dec), lag_ratio=0.3), run_time=2)
        # 什么进制都可以，然后把奇数位提取出来，作为横坐标的小数，
        self.wait()
        self.play(FadeOut(x_dengyu), FadeOut(y_dengyu), run_time=1)
        self.play(
            *[x_dec[i].animate.shift(RIGHT*(i-1)*0.6) for i in range(2, 12)],
            *[y_dec[i].animate.shift(RIGHT*i*0.6+0.1*LEFT) for i in range(1, 12)],
            run_time=3
        )
        self.wait(2)
        # 偶数位提取出来，作为纵坐标的小数。
        self.play(
            FadeOut(y_dec[0]), FadeOut(y_dec[-1]),
            x_dec.animate.shift(DOWN*0.3),
            y_dec[1:-1].animate.shift(UP*0.32),
        )
        self.wait(2)
        # 你可以很容易地验证，这的确是一个线段上点和正方形内部点的一一对应。
        x_eqs = MathTex("z=", color=ORANGE).scale(1.5).next_to(x_dec, LEFT, buff=0.1)
        pos = seg.get_start() + 0.2538*(seg.get_end()-seg.get_start())
        arr = Arrow(pos+DOWN*0.8, pos, color=ORANGE, buff=0.05)
        x_note = MathTex("z", color=ORANGE).next_to(arr, DOWN, buff=0.1)
        self.play(Write(x_eqs), Create(arr), run_time=2)
        self.wait()
        self.play(Circumscribe(x_dec), Write(x_note), run_time=2)
        # 细心的观众可能发现了，这个过程正是我们之前希尔伯特的旅馆里安排所有负整数住进旅馆的过程，
        # (插入之前片段的视频）
        # 上述两个证明的方法都不谋而合地描述着2aleph0=aleph0的本质。
        self.wait(2)
        # 如果前两种方法还是有些抽象的话，那么我还有第三种方法帮你直观地理解这一点。
        # 核心的思想还是构造一一对应，但这次用更直观的办法。
        self.play(*[FadeOut(obj) for obj in [x_dec, y_dec[1:-1], x_eqs, arr, pt, pt_lbl, x_note]]
                  , run_time=1)
        self.wait(2)
        # 假设我们现在要构造这根线段上的点和正方形内部点的一一对应，我们可以每次把线段均匀分成四份，并把正方形同样等分成四份。
        sq2d = static_square.copy().scale(1.5).move_to(ORIGIN + LEFT*3)
        seg1d = seg.copy().scale(1.5).move_to(ORIGIN + RIGHT*3)
        self.play(
            ReplacementTransform(static_square, sq2d),
            ReplacementTransform(seg, seg1d),
            run_time=2
        )
        self.wait(2)

        def get_comp_list(sq2d, seg1d):
            """
            Receieve a square and a line, return a list of 4 sub-squares and a list of 4 sub-lines.
            The position of these sub-squares and sub-lines should align perfectly with the position of the square and the line.
            """
            # Break square into 4 equal parts, same for the line
            square_list = VGroup()
            seg_list = VGroup()
            l_sq = sq2d.get_width()
            seg_dir = seg1d.get_end()-seg1d.get_start()
            for i in range(4):
                # Compute the position of the 4 sub-squares, then copy square, scale it down, and move it to the position
                square_list.add(sq2d.copy().scale(0.5).move_to(sq2d.get_center() + (i//2-0.5)*DOWN*l_sq/2 + (i%2-0.5)*RIGHT*l_sq/2))
                # Compute the position of the 4 sub-lines, then copy line, scale it down, and move it to the position
                seg_list.add(Line(seg1d.get_start() + i/4*seg_dir, 
                                seg1d.get_start() + (i+1)/4*seg_dir,
                                color=ORANGE, stroke_width=7.5, buff=0.))    


            # Add dashed lines to divide the square into 4 equal parts, same for the line
            square_dashed_list = VGroup()
            seg_dashed_list = VGroup()
            square_dashed_list.add(
                DashedLine(sq2d.get_center() + UP*0.7*l_sq, sq2d.get_center() + DOWN*0.7*l_sq, color=YELLOW, stroke_width=2)
            )
            square_dashed_list.add(
                DashedLine(sq2d.get_center() + LEFT*0.7*l_sq, sq2d.get_center() + RIGHT*0.7*l_sq, color=YELLOW, stroke_width=2)
            )
            for i in range(3):
                seg_dashed_list.add(
                    DashedLine(seg1d.get_start() + (i+1)/4*seg_dir + UP*0.3, 
                            seg1d.get_start() + (i+1)/4*seg_dir + DOWN*0.3, 
                            color=YELLOW, stroke_width=1)
                )
            
            return square_list, seg_list, square_dashed_list, seg_dashed_list


        idx_list = [0, 1, 3, 2]
        cur_sq = sq2d
        cur_seg = seg1d
        obj_buffer = VGroup()

        # At each round, divide the current square and line into 4 equal parts, and add dashed lines to indicate the division.
        # Substitude the current square and line with the 4 sub-squares and sub-lines, and add them to the buffer.
        # EnlargeIndicate the selected idx_list[i]_th square and line, then fade out the dashed lines, and set the rest 3 unselected sub-squares and sub-lines' opacity down to 0.2
        # use buffer to preserve last rounds' objects
        for i in range(4):
            time = 2 if i == 0 else 0.5
            sq_list, seg_list, sq_dash, seg_dash = get_comp_list(cur_sq, cur_seg)
            obj_buffer.add(sq_list, seg_list)
            self.play(
                Create(sq_dash),
                Create(seg_dash),
                run_time=time
            )
            self.wait(time)
            # Do the substitution. Remove the current square and line, add the 4 sub-squares and sub-lines to the scene.
            self.play(
                *[FadeOut(obj) for obj in [cur_sq, cur_seg]],
                *[FadeIn(obj) for obj in sq_list],
                *[FadeIn(obj) for obj in seg_list],
                run_time=time
            )
            self.wait(time)
            # EnlargeIndicate the selected sub-square and sub-line, then fade out the dashed lines, and set the rest 3 unselected sub-squares and sub-lines' opacity down to 0.2
            self.EnlargeIndicate([sq_list[idx_list[i]], seg_list[idx_list[i]]], pause_time=0.5, run_time=1)
            self.play(
                *[FadeOut(obj) for obj in [sq_dash, seg_dash]],
                *[obj.animate.set_opacity(0.1) for obj in sq_list if obj != sq_list[idx_list[i]]],
                *[obj.animate.set_opacity(0.1) for obj in seg_list if obj != seg_list[idx_list[i]]],
                run_time=time
            )
            self.wait(time)
            cur_sq.become(sq_list[idx_list[i]])
            cur_seg.become(seg_list[idx_list[i]])
        
        self.wait(2)


        # 接下来，我们只需要依次构建每个1/4长线段和小正方形的一一对应就可以了。
        # 而这件事情，你会注意到，和我们最开始要做的事情是完全一样的。
        # 因此，我们可以不断重复这个过程，让需要对应的线段区间和小正方形不断缩小。
        # 这里就需要提到我们之前视频说过的知识，左边的这个过程是区间套，
        interval_series = Text("区间套", color=YELLOW).scale(2).shift(DOWN*2.5)
        self.play(DrawBorderThenFill(interval_series), run_time=2)
        self.wait(4)
        # 不断细化缩小的区间在无穷的意义下定义了一个唯一确定的实数；
        # 而左边也是一样，无穷细化的正方形唯一定位了一个正方形内的点。
        # 所以，我们构建起了线段上的实数和正方形内部二维坐标的一一对应，线段和正方形内部的点的数量是一样多的。
        # Draw a corresponding double arrow between the current square and line
        double_arrow = DoubleArrow(sq2d, seg1d, color=ORANGE, buff=0.1, stroke_width=4)
        self.play(GrowFromCenter(double_arrow), run_time=2)
        self.wait(2)
        # 停顿）你可以很自然地想到，这个过程也可以应用到三维和更高的任意有限维度。
        # Write 2^aleph0's any k_th power is still 2^aleph0
        equation = MathTex(r"\left(2^{\aleph_0}\right)^k=2^{\aleph_0}", color=BLUE).scale(2).shift(UP*3)
        self.play(Write(equation), run_time=2)
        self.wait(2)

class InfScale(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()
        # Draw a balance scale with lines 
        theta = ValueTracker(0)

        plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            }
        ).shift(DOWN*2)

        hengliang = always_redraw(
            lambda: Line(
                plane.c2p(-4*math.cos(theta.get_value()), -4*math.sin(theta.get_value())), 
                plane.c2p(4*math.cos(theta.get_value()), 4*math.sin(theta.get_value())),
                color=GOLD, stroke_width=6)
        )

        left_col = always_redraw(
            lambda: Line(
                plane.c2p(-4*math.cos(theta.get_value()), -4*math.sin(theta.get_value())), 
                plane.c2p(-4*math.cos(theta.get_value()), -4*math.sin(theta.get_value())+1),
                color=GOLD, stroke_width=10)
        )
        
        right_col = always_redraw(
            lambda: Line(
                plane.c2p(4*math.cos(theta.get_value()), 4*math.sin(theta.get_value())), 
                plane.c2p(4*math.cos(theta.get_value()), 4*math.sin(theta.get_value())+1),
                color=GOLD, stroke_width=10)
        )

        left_plate = always_redraw(
            lambda: Line(
                plane.c2p(-4*math.cos(theta.get_value())-2, -4*math.sin(theta.get_value())+1), 
                plane.c2p(-4*math.cos(theta.get_value())+2, -4*math.sin(theta.get_value())+1),
                color=LIGHT_BROWN, stroke_width=3)
        )

        right_plate = always_redraw(
            lambda: Line(
                plane.c2p(4*math.cos(theta.get_value())-2, 4*math.sin(theta.get_value())+1), 
                plane.c2p(4*math.cos(theta.get_value())+2, 4*math.sin(theta.get_value())+1),
                color=LIGHT_BROWN, stroke_width=3)
        )

        left_bar1 = always_redraw(
            lambda: Line(
                plane.c2p(-4*math.cos(theta.get_value())-2, -4*math.sin(theta.get_value())+1), 
                plane.c2p(-4*math.cos(theta.get_value())-2.5, -4*math.sin(theta.get_value())+1.5),
                color=LIGHT_BROWN, stroke_width=3)
        )

        left_bar2 = always_redraw(
            lambda: Line(
                plane.c2p(-4*math.cos(theta.get_value())+2, -4*math.sin(theta.get_value())+1), 
                plane.c2p(-4*math.cos(theta.get_value())+2.5, -4*math.sin(theta.get_value())+1.5),
                color=LIGHT_BROWN, stroke_width=3)
        )

        right_bar1 = always_redraw(
            lambda: Line(
                plane.c2p(4*math.cos(theta.get_value())-2, 4*math.sin(theta.get_value())+1), 
                plane.c2p(4*math.cos(theta.get_value())-2.5, 4*math.sin(theta.get_value())+1.5),
                color=LIGHT_BROWN, stroke_width=3)
        )

        right_bar2 = always_redraw(
            lambda: Line(
                plane.c2p(4*math.cos(theta.get_value())+2, 4*math.sin(theta.get_value())+1), 
                plane.c2p(4*math.cos(theta.get_value())+2.5, 4*math.sin(theta.get_value())+1.5),
                color=LIGHT_BROWN, stroke_width=3)
        )

        scale_note = Text("无穷天平", color=BLUE).scale(1.2).move_to(plane.c2p(0, 0)).set_stroke(background=True, width=5)

        self.play(
            LaggedStart(
                Create(hengliang),
                Create(left_col),
                Create(right_col),
                Create(left_plate),
                Create(right_plate),
                Create(VGroup(left_bar1, left_bar2, right_bar1, right_bar2)),
                DrawBorderThenFill(scale_note),
                lag_ratio=0.3
            ), run_time=4
        )
        self.wait(2)

        # Draw two circle, one with notation $\mathbb{Z}$, one with notation $2\mathbb{Z}$
        z_circle = Circle(radius=1.2, color=BLUE, stroke_width=0.1).set_opacity(0.7).shift(UP*2+LEFT*3)
        z_note = MathTex(r"\mathbb{Z}", color=WHITE).scale(2).add_updater(lambda m: m.move_to(z_circle))
        z2_circle = Circle(radius=1.2, color=BLUE_B, stroke_width=0.1).set_opacity(0.7).shift(UP*2+RIGHT*3)
        z2_note = MathTex(r"2\mathbb{Z}", color=WHITE).scale(2).add_updater(lambda m: m.move_to(z2_circle))
        q_circle = Circle(radius=1.2, color=GREEN, stroke_width=0.1).set_opacity(0.7).shift(UP*2+RIGHT*3)
        q_note = MathTex(r"\mathbb{Q}", color=ORANGE).scale(2).add_updater(lambda m: m.move_to(q_circle))
        r_circle = Circle(radius=1.2, color=MAROON, stroke_width=0.1).set_opacity(0.7).shift(UP*2+RIGHT*3)
        r_note = MathTex(r"\mathbb{R}", color=YELLOW).scale(2).add_updater(lambda m: m.move_to(r_circle))
        subset_sign = MathTex(r"\subset", color=YELLOW).scale(2).shift(UP*2)
        contain_sign = MathTex(r"\supset", color=YELLOW).scale(2).shift(UP*2)

        self.play(
            LaggedStart(
                Create(z_circle),
                Create(z2_circle),
                lag_ratio=0.3
            ), run_time=2
        )
        self.play(
            Write(z_note), Write(z2_note),
        )
        self.wait()
        self.play(Write(contain_sign), run_time=1)
        self.wait()
        self.play(
            FadeOut(contain_sign), 
            z_circle.animate.next_to(left_plate, UP, buff=0.1),
            z2_circle.animate.next_to(right_plate, UP, buff=0.1),
            run_time=2
        )
        self.wait(2)
        # Restore two circle to original position, substitute the z2 with q
        self.play(
            z_circle.animate.move_to(UP*2+LEFT*3),
            z2_circle.animate.move_to(UP*2+RIGHT*3),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(z2_circle, q_circle),
            ReplacementTransform(z2_note, q_note),
        )
        self.wait()
        self.play(Write(subset_sign), run_time=1)
        self.wait(3)
        self.play(FadeOut(subset_sign), run_time=1)
        self.wait(2)
        self.play(
            z_circle.animate.next_to(left_plate, UP, buff=0.1),
            q_circle.animate.next_to(right_plate, UP, buff=0.1),
            run_time=2
        )
        self.wait(2)

        r_circle.move_to(q_circle)
        self.play(
            ReplacementTransform(q_circle, r_circle),
            ReplacementTransform(q_note, r_note),
        )
        z_circle.add_updater(lambda m: m.next_to(left_plate, UP, buff=0.1))
        r_circle.add_updater(lambda m: m.next_to(right_plate, UP, buff=0.1))

        self.play(
            theta.animate.set_value(-PI/9),
            rate_func = rate_functions.ease_out_bounce,
            run_time=3
        )
        self.wait(3)

        # Cardinality of Infinity
        text = Text("无穷大的势", color=YELLOW).scale(1.5).shift(UP*2.5)
        self.play(DrawBorderThenFill(text), run_time=2)
        self.wait(4)

class StepsOfInf(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        # 知道了这一点，我们可以进一步构造比实数无穷更大的无穷。
        # 方法是，考虑[0,1]区间里所有实数的子集，你可以挑选其中的一些实数，再丢掉剩下来的。
        note = MathTex(r"P_R", r"=\left\{A:", r"A \subseteq [0, 1]", r"\right\}", color=BLUE).scale(1.2).shift(UP*2)
        self.play(Write(note[2]), run_time=1)
        self.wait(2)
        self.play(Write(note[0:2]), Write(note[3]), run_time=2)
        # 你能够找到的子集的数量，就是比实数无穷的势更高的无穷。
        # 你也可以这么理解，定义一个函数值只有0或者1的函数，它的定义域是区间[0,1]，
        
        rect = SurroundingRectangle(note[0])
        self.play(Create(rect), run_time=1)
        self.wait(3)
        self.play(FadeOut(rect), run_time=1)
        self.wait(3)
        # 你无法构建它和[0,1]之间实数的一一对应。
        # 至于原因嘛，其实还是用之前康托对角线的方法
        # 假设存在这样的一一对应，也就是说，对于每一个实数r，都存在一个唯一对应的[0,1]的子集A_r
        # Write it down
        r_note = MathTex(r"\forall r\in [0,1],\quad \exists A_r\subseteq [0,1]", color=GOLD).next_to(note, DOWN, buff=0.5)
        self.play(Write(r_note), run_time=2)
        self.wait(4)
        
        # 那么我们可以构造一个新的子集B，它到底包不包含任何一个实数r，都和A_r不同。
        # 也就是说，A_r如果有r，B就没有r，A_r如果没有r，B就有r。
        B_def = MathTex(r"B=\{r\in [0,1]: r\notin A_r\}", color=BLUE).scale(1.2).next_to(r_note, DOWN, buff=0.5)
        self.play(Write(B_def), run_time=2)
        self.wait(4)
        # 那么B和所有的A_r都不同，因为它们在r这个点上的取值不同。
        not_eq_Ar = MathTex(r"\not= A_r, \forall r\in [0,1]", color=RED).scale(0.8).next_to(B_def,DOWN, buff=0.2).shift(RIGHT*2.5)

        ded1 = MathTex(r"r\in A_r \Rightarrow r\notin B", color=YELLOW).shift(DOWN*2+LEFT*3)
        ded2 = MathTex(r"r\notin A_r \Rightarrow r\in B", color=YELLOW).shift(DOWN*2+RIGHT*3)
        self.play(Write(ded1), run_time=2)
        self.wait(2)
        self.play(Write(ded2), run_time=2)
        self.wait(5)
        self.play(Write(not_eq_Ar))
        self.wait(2)

        # 所以不存在这样的一一对应，也就是说，这样的A_r的数量一定比实数还要多。
        # 你可能立刻发现了，这个构造和理发师悖论有些类似。
        # 其实，这正揭示了无穷中的逻辑悖论意义的深邃和广泛

        # FadeOut everything except for text1 and text2
        self.play(
            *[FadeOut(obj) for obj in self.mobjects if obj not in [text_1, text_2]],
            run_time=1
        )
        # 这套流程其实
        # 现在我们发现了，无穷大的势有一级一级上升的阶梯，

        a0 = MathTex(r"\aleph_0", color=YELLOW_A).scale(2).shift(LEFT*3.5)
        a1 = MathTex(r"2^{\aleph_0}", color=YELLOW_B).scale(2)
        a2 = MathTex(r"2^{2^{\aleph_0}}", color=YELLOW_C).scale(2.5).shift(RIGHT*3.5)
        etc_dots = MathTex(r"\cdots", color=WHITE).scale(2).next_to(a2, RIGHT, buff=0.5)
        self.play(Write(a0))
        self.wait(1)
        self.play(TransformFromCopy(a0, a1), run_time=2)
        self.wait(1)
        self.play(TransformFromCopy(a1, a2), run_time=2)
        self.wait(1)
        self.play(Write(etc_dots), run_time=1)
        self.wait(2)

        # 只需要每次数一下前一个集合的子集一共有多少个就可以了。
        # 这意味着不同无穷大的势也有可数无穷多，接下来，我们来看看细分的刻度：
        # 数学家提出了这样一个问题：在可数无穷和实数无穷之间，是不是还存在着其他的无穷？
        # Create a question mark between a0 and a1  
        question_mark = MathTex(r"?", color=YELLOW).scale(2).move_to(a0.get_center()*0.5 + a1.get_center()*0.5).set_stroke(background=True, width=5)
        self.play(Write(question_mark), run_time=2)
        self.wait(2)

        aleph1 = MathTex(r"\aleph_1", "=", color=YELLOW_A).scale(1.5).next_to(a1, LEFT, buff=0.1)
        new_qm = MathTex(r"?", color=YELLOW).scale(2).move_to(aleph1[1]).set_stroke(background=True, width=5)
        self.play(Transform(question_mark, new_qm), Write(aleph1), run_time=2)
        self.wait(4)
        # 暂停视频，你的猜想是什么呢？
        # FadeOut everything except for a1, aleph1, question_mark, text1 and text2
        # Move a1, aleph1, question_mark to the center of the screen

        # Final statement
        fs = MathTex(r"\aleph_1", "=", r"2^{\aleph_0}", color=TEAL).scale(3.5)
        large_qm = MathTex(r"?", color=RED).scale(3.5).move_to(fs[1]).set_stroke(background=True, width=5)

        self.play(
            *[FadeOut(obj) for obj in self.mobjects if obj not in [a1, aleph1, question_mark, text_1, text_2]],
            ReplacementTransform(question_mark, large_qm),
            ReplacementTransform(a1, fs[1:3]),
            ReplacementTransform(aleph1, fs[0]),
            run_time=2
        )
        self.wait(3)
        CH = Text("连续统假设", color=YELLOW).scale(2).shift(DOWN*2.5)
        ch_eng = Text("Continuum Hypothesis", color=YELLOW).scale(1.5).to_edge(UP)
        self.play(Write(CH), Write(ch_eng), run_time=2)
        self.wait(2)

class CantorSet(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()
        # 在上期视频的评论区我看到很多人说，这个结论一点都不难理解，
        # 有理数是一堆互不连通的散乱的点，无理数连成一片，所以肯定是无理数的概率是1了。
        # Emm……怎么说呢，这样想固然可以帮助你理解，但其实过度依赖于感官的直观认识会带来很多危险。
        # 比如，接下来我就给大家介绍一个例子，这个集合的点同样非常零散、不占地方，
        # 你如果在0到1内随机采样一个点，采样到这个集合中的点的概率是0。
        # 【但是】，这个集合却有着不可数无穷多的点，而它就是大名鼎鼎的“康托尔集”。
        title = Text("康托尔集", color=YELLOW).scale(1.5).shift(UP*3)
        self.play(DrawBorderThenFill(title), run_time=2)
        # 康托尔集怎么构造呢？非常简单，先取一段单位长度的线段，然后去掉中间1/3，
        l0 = Line(LEFT*4.5, RIGHT*4.5, color=GREEN_D, stroke_width=10).shift(UP*1.5)
        self.play(Create(l0), run_time=2)   
        self.wait(2)
        def get_broke_part(seg):
            """Receive a set, divide it into 3 equal parts, return the left and right parts.
            put two parts just beneath the original set by buff=0.2
            """
            
            return Line(seg.get_start(), seg.point_from_proportion(1/3), color=GREEN_D, stroke_width=10).shift(DOWN*0.8), \
                Line(seg.point_from_proportion(2/3), seg.get_end(), color=GREEN_D, stroke_width=10).shift(DOWN*0.8)
        
        buffer = VGroup(l0)
        last_st = 0

        for i in range(5):
            time = 2 if i == 0 else 1
            this_round = VGroup()
            for j in range(last_st, len(buffer)):
                l1, l2 = get_broke_part(buffer[j])
                buffer.add(l1, l2)
                this_round.add(l1, l2)

            self.play(
                FadeIn(this_round),
                run_time=time
            )
            self.wait(time)
            last_st = len(buffer) - len(this_round)

        # 这样就剩下了左右两段1/3的部分。
        # 接下来，我们再删去这两段各自中间的1/3，这样就变成了四段，每段是原来长度的1/9。
        # 你可以很容易发现，每次操作，线段的总长度都会乘以2/3，
        s0 = MathTex("1", color=ORANGE).scale(1.2).next_to(l0, LEFT, buff=0.3)
        s1 = MathTex(r"\frac{2}{3}", color=ORANGE).scale(0.5).next_to(buffer[1], LEFT, buff=0.3)
        s2 = MathTex(r"\left(\frac{2}{3}\right)^2", color=ORANGE).scale(0.5).next_to(buffer[3], LEFT, buff=0.3)
        s3 = MathTex(r"\left(\frac{2}{3}\right)^3", color=ORANGE).scale(0.5).next_to(buffer[7], LEFT, buff=0.3)
        s4 = MathTex(r"\left(\frac{2}{3}\right)^4", color=ORANGE).scale(0.5).next_to(buffer[15], LEFT, buff=0.3)
        s5 = MathTex(r"\left(\frac{2}{3}\right)^5", color=ORANGE).scale(0.5).next_to(buffer[31], LEFT, buff=0.3)
        self.play(
            LaggedStart(
                *[Write(si) for si in [s0, s1, s2, s3, s4, s5]], lag_ratio=0.1
            ), run_time=4,
        )
        self.wait(2)
        # 所以当我们无穷地进行这个过程之后，康托尔集在数轴上是不占地方的，
        # 或者用上一次视频的话说，是一个“零测集”。
        # 可是问题来了，康托尔集所包含的点的数量是多少呢？
        # 既然是一个零测集，感觉好像……是可数无穷多……吗？
        # 不，康托尔集的势是阿列夫1，或者说2的阿列夫0次方。
        two_aleph0 = MathTex(r"2^{\aleph_0}", color=ORANGE).scale(1.5)
        self.play(Write(two_aleph0), run_time=2)
        self.wait(2)
        self.play(FadeOut(two_aleph0), run_time=1)
        self.wait(2)
        # 为什么呢？很简单，因为要确定一个康托尔集的点，
        down_trace = [0, 2, 5, 12, 25, 52]
        # Create a list of arrows pointing from buffer[down_trace[i]] to buffer[down_trace[i+1]]
        arrows = VGroup()
        for i in range(len(down_trace)-1):
            arrows.add(Arrow(buffer[down_trace[i]].get_center(), buffer[down_trace[i+1]].get_center(), buff=0.05, color=YELLOW))
        self.play(Create(arrows), run_time=4)
        self.wait(6)
        self.play(FadeOut(arrows), run_time=1)
        self.wait(2)
        # 你必须要同时给出它构造过程中每一次到底在原来线段的左边1/3还是右边1/3，
        # 而构造过程有可数无穷多次，所以，这同样是一个“可数无穷次决策”，
        # 或者说“无穷长的句子”，其无穷大的势是不可数的。
        # 有一个更简单的方法可以迅速证明，因为所有康托尔集中的数，就是写成三进制小数，
        # 数码里没有1、只能有0或者2的小数，每一次去掉中间一段，就是去掉了往后一位数码里有1的小数。
        d00 = MathTex(r"0.0\cdots", color=BLUE).scale(0.8).next_to(buffer[1], UP, buff=0.1)
        d02 = MathTex(r"0.2\cdots", color=BLUE).scale(0.8).next_to(buffer[2], UP, buff=0.1)
        d01 = MathTex(r"0.1\cdots", color=BLUE).scale(0.8).move_to(d00.get_center()*0.5+d02.get_center()*0.5)
        self.play(
            LaggedStart(
                *[Write(di) for di in [d00, d01, d02]], lag_ratio=0.1
            ), run_time=3,
        )
        self.play(FadeOut(d01))
        self.wait(2)
        d000 = MathTex(r"0.00\cdots", color=BLUE).scale(0.4).next_to(buffer[3], UP, buff=0.1)
        d002 = MathTex(r"0.02\cdots", color=BLUE).scale(0.4).next_to(buffer[4], UP, buff=0.1)
        d001 = MathTex(r"0.01\cdots", color=BLUE).scale(0.4).move_to(d000.get_center()*0.5+d002.get_center()*0.5)
        d020 = MathTex(r"0.20\cdots", color=BLUE).scale(0.4).next_to(buffer[5], UP, buff=0.1)
        d022 = MathTex(r"0.22\cdots", color=BLUE).scale(0.4).next_to(buffer[6], UP, buff=0.1)
        d021 = MathTex(r"0.21\cdots", color=BLUE).scale(0.4).move_to(d020.get_center()*0.5+d022.get_center()*0.5)
        self.play(
            LaggedStart(
                *[Write(di) for di in [d000, d001, d002, d020, d021, d022]], lag_ratio=0.1
            ), run_time=3,
        )
        self.wait(2)
        self.play(FadeOut(d001), FadeOut(d021))
        self.wait(5)
        
        # 那么所有小数的个数，自然是2的阿列夫0次方，还是实数无穷了。
        # 所以啊，不要觉得只有可数无穷才是破碎的、不占地方的，不可数无穷一样可以。

class CountAdd(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()
        nline = NumberLine(
            x_range=[-0.2, 1.2, 0.1],
            length=10,
            include_numbers=True,
            include_tip=True,
            include_ticks=True,
        ).set_color(BLUE).shift(UP*1.5)
        # 比如考虑这样一个例子，在0到1里均匀采样，采样到任何一个具体的实数单点的概率是多少呢？
        self.play(Create(nline), run_time=2)
        self.wait(2)

        x_spc = 0.233
        x_arr = Arrow(nline.n2p(x_spc) + 0.3*UP, nline.n2p(x_spc), buff=0.05, color=WHITE)
        x_note = MathTex(r"x_0=0.233", color=YELLOW).scale(0.6).next_to(x_arr, UP, buff=0.1)
        self.play(Create(x_arr), Write(x_note), run_time=2)
        # 答案当然是0，一个点不占长度，这很自然。
        Px = MathTex(r"P(x\in \{x_0\})=", "0", color=ORANGE).scale(1.2)
        Pxi = MathTex(r"P(x\in \{x_i\})=", "0", color=ORANGE).scale(1.2)
        self.play(Write(Px[0]), run_time=2)
        self.wait(2)
        self.play(Write(Px[1]), run_time=2)
        self.wait(2)
        # 可是如果我们此时考虑0到1以内所有这样单点集合的并集，按照概率的意义来说，概率应该是1。
        # Create some arrows pointing at random points on the number line
        # with notes x1, x2, x3, x4, x5...
        num = 10
        arrows = VGroup()
        notes = VGroup()
        notes.add(MathTex(r"\{x_0\}", color=YELLOW).scale(0.6).shift(UP*3 + LEFT*4))
        for i in range(num):
            x = np.random.rand()
            arrows.add(Arrow(nline.n2p(x) + 0.3*UP, nline.n2p(x), buff=0.05, color=WHITE))
            notes.add(MathTex("\{x_{"+str(i+1)+"}\}", color=YELLOW).scale(0.6).next_to(notes[-1], RIGHT, buff=0.3))
        notes.add(MathTex(r"\cdots", color=YELLOW).scale(0.6).next_to(notes[-1], RIGHT, buff=0.3))
        
        self.play(ReplacementTransform(x_note, notes[0]), run_time=1)
        self.play(
            LaggedStart(
                *[Create(arrows[i]) for i in range(num)],
                *[Write(notes[i]) for i in range(1, len(notes))], lag_ratio=0.1
            ), run_time=4
        )
        self.wait(2)
        # 可是从求和来说，这是一堆0加在一起，请注意，这些0不是无穷小量，而是干干脆脆的0，
        sum_eq = MathTex(r"P(\{x_0\})", r"+P(\{x_1\})", r"+P(\{x_2\})", r"+P(\{x_3\})", r"+P(\{x_4\})", r"+P(\{x_5\})", r"+\cdots",
                          color=ORANGE).scale(0.8).shift(DOWN*1.5)
        self.play(Write(sum_eq), run_time=3)
        self.wait(2)
        zeros = VGroup()
        for i in range(6):
            zeros.add(MathTex(r"0", color=BLUE).scale(1.2).next_to(sum_eq[i], DOWN, buff=0.2))
        # 所以加和应该是0。无数多个概率为0的集合加在一起，
        eqzero = MathTex("=0", color=YELLOW).scale(1.2).next_to(sum_eq, RIGHT, buff=0.2)  
        self.play(LaggedStart(*[Write(zeros[i]) for i in range(6)], lag_ratio=0.1),
                  Transform(Px, Pxi),
                   run_time=2)
        self.wait(2)
        self.play(Write(eqzero), run_time=2)
        self.wait(2)

        sum2 = MathTex(r"P(x\in [0,1])", color=ORANGE).scale(0.8).shift(DOWN*1.5)
        _eqzero = eqzero.copy().next_to(sum2, RIGHT, buff=0.2)
        # 为什么有的时候还能保持总概率为0，有的时候却甚至变成了1呢？
        eqone = MathTex("=1", color=YELLOW).scale(1.2).next_to(sum2, DOWN, buff=0.2)
        r1 = SurroundingRectangle(eqone)
        r0 = SurroundingRectangle(_eqzero)
        self.play(ReplacementTransform(sum_eq, sum2), 
                  Transform(eqzero, _eqzero),
                  FadeOut(zeros),
                  run_time=2)
        self.wait()
        self.play(Write(eqone), run_time=2)
        self.wait()
        self.play(Create(r1), Create(r0), run_time=2)
        qm = MathTex(r"?", color=YELLOW).scale(2).next_to(eqone, RIGHT, buff=1.2).set_stroke(background=True, width=5)
        self.play(Write(qm), run_time=1)
        self.wait(2)
        self.play(FadeOut(r1), FadeOut(r0), FadeOut(qm), run_time=1)

        # 归根结底就是因为，想要让概率加起来有意义，你并在一起的集合数量至多只能是可数无穷多，
        self.play(
            LaggedStart(
                *[Indicate(xi) for xi in notes], lag_ratio=0.3
            ), run_time=3
        )
        # 不可数无穷多的概率加和是有根本问题、容易导致悖论的。
        # 这种性质就被称作概率的“可数可加性”，
        self.wait(2)
        countadd = Text("可数可加性", color=YELLOW).scale(2).shift(UP*2.5).set_stroke(background=True, width=5)
        self.play(Write(countadd), 
                  FadeOut(sum2), FadeOut(eqone), FadeOut(eqzero), FadeOut(qm), FadeOut(Px),
                  run_time=2)
        self.wait(3)
        # 学过测度论的同学知道，这跟一个叫做σ-代数的东西关系很大。
        sigma_algebra = MathTex(r"\sigma-\text{algebra}", color=TEAL).scale(2).shift(DOWN).set_stroke(background=True, width=5)
        self.play(Write(sigma_algebra), run_time=2)
        self.wait(2)
        # 这个例子也能帮你们更好的理解，为什么数学的各个分支，
        # 包括各种分析和拓扑一直都在强调可数无穷多个集合。原因即在此。