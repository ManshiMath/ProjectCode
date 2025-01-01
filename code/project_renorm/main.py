from manim import *

class s1(Scene):
    def construct(self):
        # Draw a pyramid by five rectangles
        r1 = Rectangle(height=1, width=1.5, color=PURPLE).shift(UP*3).set_fill(PURPLE, opacity=0.8)
        r2 = Rectangle(height=1, width=3.5, color=MAROON).next_to(r1, DOWN, buff=0.2).set_fill(MAROON, opacity=0.8)
        r3 = Rectangle(height=1, width=5.5, color=GREEN).next_to(r2, DOWN, buff=0.2).set_fill(GREEN, opacity=0.8)
        r4 = Rectangle(height=1, width=7.5, color=BLUE).next_to(r3, DOWN, buff=0.2).set_fill(BLUE, opacity=0.8)
        r5 = Rectangle(height=1, width=9.5, color=RED).next_to(r4, DOWN, buff=0.2).set_fill(RED, opacity=0.8)

        self.add(r1, r2, r3, r4, r5)
        self.wait(1.5)

        # same color as r5
        center_rect = Rectangle(height=2, width=9, color=RED).set_opacity(0.9)
        text = Text("第一层：玄学世界", font="heiti").scale(1.2).set_color(YELLOW)

        self.play(Transform(r5, center_rect))
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1)

class s2(Scene):
    def construct(self):
        # Draw a pyramid by five rectangles
        r1 = Rectangle(height=1, width=1.5, color=PURPLE).shift(UP*3).set_fill(PURPLE, opacity=0.8)
        r2 = Rectangle(height=1, width=3.5, color=MAROON).next_to(r1, DOWN, buff=0.2).set_fill(MAROON, opacity=0.8)
        r3 = Rectangle(height=1, width=5.5, color=GREEN).next_to(r2, DOWN, buff=0.2).set_fill(GREEN, opacity=0.8)
        r4 = Rectangle(height=1, width=7.5, color=BLUE).next_to(r3, DOWN, buff=0.2).set_fill(BLUE, opacity=0.8)
        r5 = Rectangle(height=1, width=9.5, color=RED).next_to(r4, DOWN, buff=0.2).set_fill(RED, opacity=0.8)

        self.add(r1, r2, r3, r4, r5)
        self.wait(1.5)

        # same color as r5
        center_rect = Rectangle(height=2, width=9, color=BLUE).set_opacity(0.9)
        text = Text("第二层：柯西的审判", font="heiti").scale(1.2).set_color(YELLOW)

        self.play(Transform(r4, center_rect))
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1)

class s3(Scene):
    def construct(self):
        # Draw a pyramid by five rectangles
        r1 = Rectangle(height=1, width=1.5, color=PURPLE).shift(UP*3).set_fill(PURPLE, opacity=0.8)
        r2 = Rectangle(height=1, width=3.5, color=MAROON).next_to(r1, DOWN, buff=0.2).set_fill(MAROON, opacity=0.8)
        r3 = Rectangle(height=1, width=5.5, color=GREEN).next_to(r2, DOWN, buff=0.2).set_fill(GREEN, opacity=0.8)
        r4 = Rectangle(height=1, width=7.5, color=BLUE).next_to(r3, DOWN, buff=0.2).set_fill(BLUE, opacity=0.8)
        r5 = Rectangle(height=1, width=9.5, color=RED).next_to(r4, DOWN, buff=0.2).set_fill(RED, opacity=0.8)

        self.add(r1, r2, r3, r4, r5)
        self.wait(1.5)

        center_rect = Rectangle(height=2, width=9, color=GREEN).set_opacity(0.9)
        text = Text("第三层：物理世界", font="heiti").scale(1.2).set_color(YELLOW)

        self.play(Transform(r3, center_rect))
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1)

class s4(Scene):
    def construct(self):
        # Draw a pyramid by five rectangles
        r1 = Rectangle(height=1, width=1.5, color=PURPLE).shift(UP*3).set_fill(PURPLE, opacity=0.8)
        r2 = Rectangle(height=1, width=3.5, color=MAROON).next_to(r1, DOWN, buff=0.2).set_fill(MAROON, opacity=0.8)
        r3 = Rectangle(height=1, width=5.5, color=GREEN).next_to(r2, DOWN, buff=0.2).set_fill(GREEN, opacity=0.8)
        r4 = Rectangle(height=1, width=7.5, color=BLUE).next_to(r3, DOWN, buff=0.2).set_fill(BLUE, opacity=0.8)
        r5 = Rectangle(height=1, width=9.5, color=RED).next_to(r4, DOWN, buff=0.2).set_fill(RED, opacity=0.8)

        self.add(r1, r2, r3, r4, r5)
        self.wait(1.5)

        center_rect = Rectangle(height=2, width=9, color=MAROON).set_opacity(0.9)
        text = Text("第四层：青蛙科学家", font="heiti").scale(1.2).set_color(YELLOW)

        self.play(Transform(r2, center_rect))
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1)

class s5(Scene):
    def construct(self):
        # Draw a pyramid by five rectangles
        r1 = Rectangle(height=1, width=1.5, color=PURPLE).shift(UP*3).set_fill(PURPLE, opacity=0.8)
        r2 = Rectangle(height=1, width=3.5, color=MAROON).next_to(r1, DOWN, buff=0.2).set_fill(MAROON, opacity=0.8)
        r3 = Rectangle(height=1, width=5.5, color=GREEN).next_to(r2, DOWN, buff=0.2).set_fill(GREEN, opacity=0.8)
        r4 = Rectangle(height=1, width=7.5, color=BLUE).next_to(r3, DOWN, buff=0.2).set_fill(BLUE, opacity=0.8)
        r5 = Rectangle(height=1, width=9.5, color=RED).next_to(r4, DOWN, buff=0.2).set_fill(RED, opacity=0.8)

        self.add(r1, r2, r3, r4, r5)
        self.wait(1.5)

        center_rect = Rectangle(height=2, width=9, color=PURPLE).set_opacity(0.9)
        text = Text("第五层：重整化", font="heiti").scale(1.2).set_color(YELLOW)

        self.play(Transform(r1, center_rect))
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1)