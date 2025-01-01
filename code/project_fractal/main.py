import numpy as np
from manim import *

class Video3(Scene):
    def construct(self):
        sent0 = Text("n!含有素数2的幂次为").scale(0.6).to_corner(UL, buff=0.5)
        sent1 = MathTex(r"\nu_2(n!)=\sum_{i=1}^{\infty} \left\lfloor \frac{n}{2^i} \right\rfloor", color=BLUE).scale(0.6).next_to(sent0, RIGHT, buff=0.1)
        sent2 = Text("(勒让德定理)", color=YELLOW).scale(0.6).next_to(sent1, RIGHT, buff=1)
        self.play(Write(sent0), Write(sent1), Write(sent2))
        sent3 = MathTex(r"S_p(n)", color=ORANGE).scale(0.6).next_to(sent2, DOWN, buff=0.5).align_to(sent0, LEFT)
        sent3_2 = Text("表示n!在p进制下的数码和").scale(0.6).next_to(sent3, RIGHT, buff=0.1)
        sent4 = MathTex(r"S_p(n)=\sum_{i\geq 0} \left\lfloor \frac{n}{p^i} \right\rfloor-\left\lfloor \frac{n}{p^{i+1}} \right\rfloor p", color=BLUE).scale(0.6).next_to(sent3, DOWN, buff=0.2).align_to(sent0, LEFT)
        self.play(Write(sent3), Write(sent3_2))
        self.play(Write(sent4))
        sent5 = MathTex(r"=n+\nu_2(n!)-2\nu_2(n!)", color=BLUE).scale(0.6).next_to(sent4, RIGHT, buff=0.2)
        self.play(Write(sent5))

        sent6 = Text("所以我们知道").scale(0.6).next_to(sent5, DOWN, buff=0.5).align_to(sent0, LEFT)
        sent7 = MathTex(r"S_2(n)=n-\nu_2(n!)", color=BLUE).scale(0.6).next_to(sent6, RIGHT, buff=0.2)
        self.play(Write(sent6), Write(sent7))
        sent8 = MathTex(r"\nu_2\left( \binom{n}{m} \right)=\nu_2(n!)-\nu_2(m!)-\nu_2((m-n)!)=S_2(m)+S_2(n-m)-S_2(n)", color=BLUE).scale(0.6).next_to(sent7, DOWN, buff=0.3).align_to(sent0, LEFT)
        self.play(Write(sent8))

        sent8 = Text("而p进制下n减去m第i位（从1开始）需要借位，当且仅当").scale(0.6).next_to(sent8, DOWN, buff=0.3).align_to(sent0, LEFT)
        sent9 = MathTex(r"\left\lfloor\frac{n}{p^i}\right\rfloor-\left\lfloor\frac{m}{p^i}\right\rfloor=\left\lfloor\frac{n-m}{p^i}\right\rfloor+1", color=BLUE).scale(0.6).next_to(sent8, DOWN, buff=0.2).align_to(sent0, LEFT)
        self.play(Write(sent8), Write(sent9))

        sent10 = Text("所以在p进制下n-m需要借位的次数刚好是").scale(0.6).next_to(sent9, DOWN, buff=0.3).align_to(sent0, LEFT)
        sent11 = MathTex(r"\left\lfloor\frac{n}{p^i}\right\rfloor-\left\lfloor\frac{m}{p^i}\right\rfloor-\left\lfloor\frac{n-m}{p^i}\right\rfloor=S_2(m)+S_2(n-m)-S_2(n)", color=YELLOW).scale(0.6).next_to(sent10, DOWN, buff=0.2).align_to(sent0, LEFT)
        self.play(Write(sent10), Write(sent11))
        self.wait(2)