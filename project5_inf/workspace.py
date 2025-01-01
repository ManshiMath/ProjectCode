from manim import *
import numpy as np
from functools import partial
import math

class Philo(Scene):
    def EnlargeIndicate(self, obj_list, scale_factor=1.2, color=YELLOW, pause_time=1, run_time=1):
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

        self.wait(2)
        # 因此，所有0到1之内的实数的无穷大，是无法一个个数出来的，我们称它为“不可数无穷”
        uncountable = Text("不可数无穷", color=YELLOW).scale(2).shift(UP*2.5)
        self.play(Write(uncountable), run_time=2)
        # Draw a number line and draw a yellow stick [0,1]
        nline = NumberLine(x_range=[-0.2, 1.1, 0.1], length=8, include_numbers=True, include_tip=True, color=BLUE)
        stick = Line(start=nline.n2p(0), end=nline.n2p(1), color=YELLOW, stroke_width=6).shift(DOWN*0.2)
        self.play(
            LaggedStart(
                *[Create(obj) for obj in [nline, stick]]
            ), run_time=2
        )
        self.wait(6)
        two_pow_aleph0 = MathTex(r"2^{\aleph_0}", color=BLUE).scale(2).shift(DOWN*2)
        self.play(Write(two_pow_aleph0), run_time=2)
        self.wait(4)
        self.play(FadeOut(uncountable), run_time=1)
        self.play(
            *[FadeOut(obj) for obj in [nline, stick, two_pow_aleph0]]
        )
        self.wait(2)

        # 这同时回答了刚才我们的几个问题：为什么这套证明不能用于证明x是实数的概率等于0？
        # 因为实数是不可数无穷，比可数无穷多得多，不能一个个列出来，所以整个证明过程无法进行。

        # 这反过来也告诉了我们之前那个证明的核心本质，那就是有理数可以一个个数出来；
        rational_numbers = VGroup()
        rational_strlist = []
        for i in range(2, 12):
            for j in range(1, i):
                if math.gcd(i,j) == 1:
                    rational_strlist.append(r"\frac{" + str(j) + "}{" + str(i) + "}")
        for i in range(len(rational_strlist)):
            rational_numbers.add(MathTex(rational_strlist[i], color=BLUE).shift(UP*2.5+i*0.5*RIGHT))

        # Draw rectangle with f(\cdot) written on it
        f = MathTex(r"f(\cdot)", color=WHITE).scale(1.5)
        box = Rectangle(width=1.5, height=1, color=BLUE_B, stroke_width=0, fill_opacity=0.5).move_to(f)
        self.play(Create(box), Write(f), run_time=2)

        # At each step, write integer i below the box. Move it into the box and disappear, shake/wiggle the box, 
        # move every previously written rational numbers to left by LEFT
        # then Write the i_th rational number out of the box 
        for i in range(10):
            time = 0.3 if i else 1
            new_integer = MathTex(str(i+1), color=LIGHT_BROWN).move_to(box.get_center()+DOWN)
            self.play(Write(new_integer), run_time=time)
            # Move in and diminish the integer at the same time
            self.play(
                new_integer.animate.move_to(box.get_center()+RIGHT*0.2),
                run_time=time
            )
            
            # Shake the box
            self.play(Indicate(box), Indicate(f), run_time=time)
            # Move all the rational numbers to the left
            if i > 0:
                shift = rational_numbers[i-1].get_center() - rational_numbers[i].get_center() 
                self.play(
                    *[rational_numbers[j].animate.shift(shift) for j in range(i)],
                    run_time=time
                )
            self.play(ReplacementTransform(new_integer, rational_numbers[i]), run_time=time)
        self.wait(3)
        # 能一个个数出来，所以我们可以安排上一个指数衰减的领地；
        # 只要能指数衰减，所有区间的求和就会有限；只要有限，我们就可以缩小这个有限直到接近于0。
        # 从而证明它们在数轴上没有立锥之地。
        
        # 这里剪辑用之前的视频

        # 正是因为“可以被一个个数出来”这个性质，导了它在数轴上不占地方的本质。
        self.play(
            LaggedStart(
                *[Indicate(rational_numbers[i]) for i in range(10)]
            ), run_time=3, lag_ratio=0.5
        )

        # FadeOut everything except text1 and text2
        self.play(
            *[FadeOut(obj) for obj in [box, f, *rational_numbers[:10]]]
        )
        # 可数无穷在不可数无穷面前，就是沧海一粟。
        # 细细品味，这件事有着深刻的哲学含义。
        # 有理数归根结底是有规律的，包含的信息是有限的，无论是用循环节表示，
        
        # Write a rational example in both decimal and fraction form
        example = MathTex(r"\frac{2}{7}", r"=", r"0.\overline{285714}", color=BLUE).shift(UP*2+LEFT*2)
        self.play(Write(example), run_time=2)
        self.wait(2)
        
        # 还是用分子分母的两个整数表示，其内部的信息终究是有限的。
        rect1 = SurroundingRectangle(example[0], color=YELLOW)
        rect2 = SurroundingRectangle(example[2], color=YELLOW)
        self.play(Create(rect1), Create(rect2), run_time=2)
        self.wait(2)
        self.play(FadeOut(rect1), FadeOut(rect2), run_time=1)
        self.wait(2)

        # 但是无理数的混沌、无规律，意味着一个无理数包含的信息是无穷的。
        # Write pi in decimal form of many many digits
        pi_text = MathTex(r"\pi", r"=", r"3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679", 
                          color=GOLD).align_to(example, LEFT)
        pi_text[2].set_color(RED)
        self.play(Write(pi_text), run_time=2)
        self.wait(2)

        # Gradually shift pi_text to the left to show infinite digits
        self.play(pi_text.animate.shift(LEFT*12), run_time=8)
        # 快速复位
        self.play(pi_text.animate.shift(RIGHT*12), run_time=1)
        self.wait(2)

        # Clean the screen, FadeOut everything except text1 and text2
        self.play(
            *[FadeOut(obj) for obj in self.mobjects if obj not in [text_1, text_2]]
        )

        # 实数的无穷是一种每一个元素都包含无限信息量的无穷。
        # 整数、或者有理数的无穷，终究是有涯和可以的解析的无穷

        # 你有没有思考过，在一个规定了词汇表的语言中，有多少种可能的句子、诗歌甚至是小说？
        # 答案也是可数无穷，方法是这样的
        # 首先，我们把词汇表的每个词都编上号，比如第一个词是“我”，第二个词是“爱”，第三个词是“你”……
        vocab = ["我", "爱", "你", "他", "但", "不"]
        vocab_text = VGroup()
        for i in range(len(vocab)):
            rule = Text(str(i+1)+":"+vocab[i], color=BLUE).scale(0.8).shift(UP*2.5+4*LEFT+i*RIGHT*1.5)
            rule[2].set_color(YELLOW)
            vocab_text.add(rule)
        self.play(
            LaggedStart(
                *[Write(obj) for obj in vocab_text]
            ), run_time=2
        )
        self.wait(2)

        # 那么，对于一句话，我们就可以用一个整数序列来表示，比如“我爱你”就是“0,1,2”
        sent1 = Text("我爱你", color=WHITE).scale(0.8).shift(UP*0.5 + LEFT*4)
        translate_sent1 = MathTex("1","2","3", color=ORANGE).scale(0.8).next_to(sent1, RIGHT, buff=1)
        # Put numbers on top of the words
        for i in range(3):
            translate_sent1[i].next_to(sent1[i], UP)

        # 如何把整数数列转换成一个整数呢？我们可以利用质因数分解的唯一性
        # 比如，对于“我爱你”，我们可以把它转换成“2^0*3^1*5^2=75”
        calc_eq1 = MathTex("2^", "1", r"\times", "3^", "2", r"\times", "5^", "3", "=", "2250", 
                           color=BLUE).scale(0.8).next_to(sent1, RIGHT, buff=0.3)
        calc_eq1[1].set_color(ORANGE); calc_eq1[4].set_color(ORANGE); calc_eq1[7].set_color(ORANGE)
        self.play(
            LaggedStart(
                *[Write(obj) for obj in [sent1, translate_sent1]]
            ), run_time=2
        )
        self.wait(2)
            
        self.play(
            LaggedStart(
                *[TransformFromCopy(translate_sent1[i], calc_eq1[3*i+1]) for i in range(3)]
            ), run_time=2, lag_ratio=0.5
        )
        self.wait()
        self.play(
            LaggedStart(*[Write(calc_eq1[i]) for i in [0,2,3,5,6,8,9]]),
            run_time=2, lag_ratio=0.5
        )
        self.wait(2)

        # 下面的这些句子，都可以对应的翻译成一个整数
        
        sent2 = Text("他不爱你", color=WHITE).scale(0.8).next_to(sent1, DOWN, buff=0.8)
        translated_sent2 = MathTex("3","6","1","2", color=ORANGE).scale(0.6).next_to(sent2, UP)
        for i in range(4):
            translated_sent2[i].next_to(sent2[i], UP)
        calc_eq2 = MathTex(r"2^3 \times 3^6 \times 5^1 \times 7^2 = 1428840", 
                           color=BLUE).scale(0.8).next_to(sent2, RIGHT, buff=0.2)
        
        sent3 = Text("但你爱他", color=WHITE).scale(0.8).next_to(sent2, DOWN, buff=0.8)
        translated_sent3 = MathTex("5","3","2","4", color=ORANGE).scale(0.6).next_to(sent3, UP)
        for i in range(4):
            translated_sent3[i].next_to(sent3[i], UP)
        calc_eq3 = MathTex(r"2^5 \times 3^3 \times 5^2 \times 7^4 = 51861600",
                            color=BLUE).scale(0.8).next_to(sent3, RIGHT, buff=0.2)

        sent4 = Text("你你你你你你", color=WHITE).scale(0.8).next_to(sent3, DOWN, buff=0.8)
        translated_sent4 = MathTex("3","3","3","3","3","3", color=ORANGE).scale(0.6).next_to(sent4, UP)
        for i in range(6):
            translated_sent4[i].next_to(sent4[i], UP)
        calc_eq4 = MathTex(r"2^3 \times 3^3 \times 5^3 \times 7^3 \times 11^3 \times 13^3 =", "27081081027000", 
                           color=BLUE).scale(0.8).next_to(sent4, RIGHT, buff=0.2)

        self.play(
            LaggedStart(
                *[Write(obj) for obj in [sent2, translated_sent2, calc_eq2]]
            ), run_time=2
        )
        self.wait(2)
        self.play(
            LaggedStart(
                *[Write(obj) for obj in [sent3, translated_sent3, calc_eq3]]
            ), run_time=2
        )
        self.wait(2)
        self.play(
            LaggedStart(
                *[Write(obj) for obj in [sent4, translated_sent4, calc_eq4]]
            ), run_time=2
        )
        self.wait(4)

        # 你爱他但不爱我，3215621
        code = (2**3) * (3**2) * (5**1) * (7**5) * (11**6) * (13**2) * (17**1)
        code_text = MathTex(str(code), color=PURE_GREEN).scale(1.2).shift(UP*0.7 + RIGHT*2.5)
        rect = SurroundingRectangle(code_text, color=YELLOW)
        self.play(Write(code_text), run_time=2)
        self.play(Create(rect), run_time=1)
        self.wait(4)
        # 可数无穷在不可数无穷面前，就是沧海一粟。
        # 这个世界有清楚规律的毕竟是少数，更多的是无法被一一数出的混沌。

