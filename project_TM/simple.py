from manim import *
import numpy as np

class TaiGang(Scene):
    def construct(self):
        t1 = Text("毕导,").scale(1.5).shift(LEFT*4).set_color(RED)
        t2 = Text("你讲的").scale(1.5).next_to(t1, RIGHT, buff=0.2).set_color(ORANGE)
        t3 = Text("太落后了", font='heiti').scale(2).next_to(t2, RIGHT, buff=0.2).set_color(YELLOW)

        self.play(FadeIn(t1), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(t2), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(t3), run_time=1)
        self.wait(1.5)

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

        self.wait(3)

        notmath = Text("数学", color=BLUE).scale(1.5).shift(LEFT*3)
        cross1 = Cross(notmath, stroke_width=10, color=RED)
        notlogic = Text("逻辑学", color=MAROON).scale(1.5).shift(RIGHT*3)
        cross2 = Cross(notlogic, stroke_width=10, color=RED)
        self.play(Write(notmath), run_time=0.5)
        self.play(Create(cross1), run_time=0.5)
        self.wait(0.5)
        self.play(Write(notlogic), run_time=0.5)
        self.play(Create(cross2), run_time=0.5)
        self.wait(0.8)

        iscomputer = Text("计算机", font='heiti', color=YELLOW).scale(2.5).shift(UP)
        tick = MathTex(r"\checkmark", color=GREEN).scale(2.5).next_to(iscomputer, RIGHT, buff=0.5)
        self.play(
            notmath.animate.shift(DOWN*2),
            notlogic.animate.shift(DOWN*2),
            cross1.animate.shift(DOWN*2),
            cross2.animate.shift(DOWN*2),
            DrawBorderThenFill(iscomputer), 
            run_time=2)
        self.play(Write(tick), run_time=0.5)
        self.wait(1.5)


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
        self.wait(1)
        t2 = Text("踢馆sub(n,n,17)", font='heiti', color=RED).next_to(name, DOWN, buff=0.5)
        self.play(
            Write(t2),
            run_time=1
        )
        self.wait(1.5)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class ThreeLines(Scene):
    def construct(self):
        line1 = Text("可以构造一个图灵机K，为F中任何可判定的命题给出证明").scale(0.8).shift(UP*1.5).set_color(YELLOW)
        line2 = Text("如果F完备，则K能够对任何命题停机并给出回答").scale(0.8).set_color(YELLOW).align_to(line1, LEFT)
        line3 = Text("是否停机也是命题，所以K能够判定停机问题，矛盾").scale(0.8).shift(DOWN*1.5).set_color(YELLOW).align_to(line1, LEFT)

        self.play(
            LaggedStart(Write(line1),
                        Write(line2),
                        Write(line3),
                        lag_ratio=0.5,
                        run_time=3
                        )
        )
        self.wait(4)

        # grey_line1 = line1.copy().set_color(DARK_GREY)
        # grey_line2 = line2.copy().set_color(DARK_GREY)
        # grey_line3 = line3.copy().set_color(DARK_GREY)

        self.play(
            # line1.animate.scale(1.25),
            line2.animate.set_color(DARK_GREY),
            line3.animate.set_color(DARK_GREY),
            run_time=1.5
        )
        self.wait(2)

        self.play(
            line1.animate.set_color(DARK_GREY),
            line2.animate.set_color(YELLOW),
            run_time=1.5
        )
        self.wait(2)

        self.play(
            line2.animate.set_color(DARK_GREY),
            line3.animate.set_color(YELLOW),
            run_time=1.5
        )
        self.wait(2)

class TMDemo(Scene):
    def construct(self):
        text = Text("人是如何思考和计算的？", font='heiti').scale(1.5).set_color(YELLOW)
        self.wait(2)
        self.play(Write(text))
        self.wait(2)

class Fuse(Scene):
    def construct(self):
        brain = SVGMobject("brain.svg").set_color(PINK).shift(LEFT*2)

        model = Text("模型").scale(2).shift(RIGHT*3).set_color(BLUE)
        self.play(
            FadeIn(brain),
            run_time=1
        )
        self.wait(1)
        Arr = Arrow(brain.get_right(), model.get_left(), buff=0.1)
        self.play(
            TransformFromCopy(brain, model),
            GrowArrow(Arr),
            run_time=1.5
        )
        self.wait(2)

        TM = Text("图灵机 Turing Machine", font='heiti').scale(1.2).set_color(YELLOW).to_edge(UP)
        self.play(
            Write(TM),
            run_time=1.5
        )
        self.wait(2)


class UnivTM(Scene):
    def construct(self):
        question = Text("这个世界上真的有图灵机吗？").set_color(RED).shift(UP*3)

        answer = Text("有", font='heiti').set_color(GREEN).scale(2).shift(LEFT*2.5)
        answer2 = Text("也没有", font='heiti').set_color(BLUE).scale(2).next_to(answer, RIGHT, buff=1)

        self.play(Write(question))
        self.wait(2)
        self.play(Write(answer))
        self.play(Write(answer2))
        self.wait(3)

class Undecide(Scene):
    def construct(self):
        text = Text("会停吗？不知道").set_color(YELLOW).scale(2)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1.5)
        self.play(FadeOut(text))

class BusyBeaver(Scene):
    def construct(self):
        
        ten = MathTex(r"10", color=YELLOW).scale(3).shift(DOWN+LEFT*2)
        greater = MathTex(r">", color=RED).scale(3).next_to(ten, LEFT, buff=0.2)
        ten1 = ten.copy().scale(0.8).next_to(ten, UP+RIGHT, buff=0.1)
        ten2 = ten1.copy().scale(0.8).next_to(ten1, UP+RIGHT, buff=0.1)
        ten3 = ten2.copy().scale(0.8).next_to(ten2, UP+RIGHT, buff=0.1)
        dots = MathTex(r"\ddots", color=YELLOW).scale(2).next_to(ten3, UP+RIGHT, buff=0.1).rotate(-0.6*PI)
        last_ten = ten3.copy().scale(0.8).next_to(dots, UP+RIGHT, buff=0.1)
        
        bracket = BraceLabel(VGroup(ten,ten1,ten2,ten3,last_ten), "15", DOWN, buff=0.1, font_size=60).set_color(BLUE)

        self.add(greater)
        self.play(Write(ten), run_time=0.4)
        self.wait(0.2)
        self.play(Write(ten1), run_time=0.4)
        self.wait(0.2)
        self.play(Write(ten2), run_time=0.4)
        self.wait(0.4)
        self.play(Write(ten3), run_time=0.4)
        self.wait(0.2)
        self.play(Write(dots), run_time=1)
        self.play(Write(last_ten), run_time=0.5)
        self.wait(0.3)
        self.play(Write(bracket), run_time=1.5)
        self.wait(2)

class Reduction(Scene):
    def construct(self):
        title = Text("规约").set_color(YELLOW).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN, buff=0.1)
        self.play(
            Write(title),
            GrowFromCenter(line),
        )
        self.wait(1)
        questiona = Text("A").scale(4).set_color(MAROON).shift(LEFT*3)
        questionb = Text("B").scale(4).set_color(RED).shift(RIGHT*3)
        arr = Arrow(questiona.get_right(), questionb.get_left(), buff=0.2).set_color(YELLOW)
        arr_lbl = Text("简单应用").scale(0.6).next_to(arr, UP, buff=0.1).set_color(BLUE)
        A_lbl = Text("判断停机").scale(0.8).next_to(questiona, DOWN, buff=0.2)
        B_lbl = Text("哥德巴赫猜想").scale(0.8).set_color(YELLOW).next_to(questionb, DOWN, buff=0.2)

        self.play(Write(questiona), run_time=1)
        self.wait(1)
        self.play(
            LaggedStart(
                GrowArrow(arr),
                Write(arr_lbl),
            )
        )
        self.wait()
        self.play(Write(questionb), run_time=1)
        self.wait(1)
        self.play(
            Indicate(questionb),
            Write(B_lbl),
        )
        self.wait(2)
        self.play(
            Indicate(questiona),
            Write(A_lbl),
        )
        self.wait()
        rect = SurroundingRectangle(questiona, buff=0.1)
        self.play(Create(rect))
        self.wait(2)
        self.play(FadeOut(rect))

        _A_lbl = Text("预知未来").scale(0.8).set_color(YELLOW).next_to(questiona, DOWN, buff=0.2)
        _B_lbl = Text("中彩票暴富").scale(0.8).set_color(GREEN).next_to(questionb, DOWN, buff=0.2)
        self.wait(2)
        self.play(
            Transform(A_lbl, _A_lbl),
            Transform(B_lbl, _B_lbl),
        )

        self.wait(2)


class UndecideProof(Scene):
    def construct(self):
        text = Text("停机问题").set_color(YELLOW).scale(2).shift(UP*2)
        cross = Cross(text, stroke_width=10, color=RED)
        # 停机问题是人类找到的第一个不可判定的问题。所谓不可判定，
        self.play(
            Write(text),
            run_time=1
        )
        self.wait(1.5)
        
        # 就是人类用严格的数学证明了，不可能有任何计算方法能够有限步内判断一个图灵机会不会停机。
        self.play(Create(cross), run_time=1)

        title = Text("不可判定性").set_color(YELLOW).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN, buff=0.2)
        self.wait()
        self.play(
            ReplacementTransform(text, title),
            GrowFromCenter(line),
            FadeOut(cross),
            run_time=1.5
        )
        self.wait(2)
        # 为什么呢？答案是用反证法，假设存在这么一个图灵机M，
        fanzheng = Text("反证法", font='heiti').scale(0.7).set_color(YELLOW).to_edge(LEFT).shift(UP*2)
        self.play(Write(fanzheng))

        self.wait(2)
        # A square stands for a TM
        M = Square(side_length=2, color=GOLD_D, stroke_width=10)
        M_lbl = MathTex("M").scale(1.5).set_color(BLUE).add_updater(lambda m: m.move_to(M))
        self.play(
            DrawBorderThenFill(M),
            Write(M_lbl),
            run_time=1
        )
        self.wait(2)

        # 它能够判断任何一个输入的图灵机会不会停机。
        code = SVGMobject("note_text.svg").set_color(ORANGE).next_to(M, LEFT, buff=3).set_stroke(width=10)
        self.play(
            FadeIn(code),
            run_time=1
        )
        self.wait()
        code_lbl = Text("Any code").scale(0.6).set_color(GREEN).add_updater(lambda m: m.next_to(code, DOWN, buff=0.1))
        self.play(Write(code_lbl), run_time=1)
        self.wait(2)

        feedin_arr = Arrow(code.get_right(), M.get_left(), buff=0.5).set_color(BLUE).set_stroke(width=15)
        result_brace = MathTex(r"\begin{cases} \text{Will Halt.} \\ \text{Never Halt.} \end{cases}", 
                               color=YELLOW).scale(1.2).next_to(M, RIGHT, buff=1)
        self.play(
            GrowArrow(feedin_arr),
            run_time=1
        )
        self.wait(1)
        self.play(Write(result_brace), run_time=1)
        self.wait(2)
        # 那么我们写一段新代码M’，它是这么工作的：
        self.play(
            *[FadeOut(mob)for mob in self.mobjects if mob not in [title, line, fanzheng, M, M_lbl]],
            M.animate.shift(LEFT*2),
            run_time=1.5
        )
        self.wait(2)

        # 如果它判断，输入的图灵机代码会永远运行，那么M’就立刻停机；
        
        large_rect = Rectangle(height=4, width=7, color=GREEN, stroke_width=6)
        M_prime = MathTex("M'", color=RED).scale(1.5).next_to(large_rect, DOWN, buff=0.2)
        self.play(
            Write(M_prime),
            DrawBorderThenFill(large_rect),
            run_time=1.5
        )
        self.wait(2)
        append_steps = MathTex(r"\begin{cases} \text{Halt:}\quad\texttt{Loop} \\ \text{Loop:}\quad\texttt{Halt}\end{cases}",
                               color=ORANGE).scale(0.8).next_to(M, RIGHT, buff=0.2)
        self.play(Write(append_steps), run_time=2)
        self.wait(3)

        # 如果判断输入的程序会停机，那自己就死循环。
        # 接下来最精彩的地方来了，我们给M’以自己的代码为输入，它到底是停机还是循环呢？
        another_Mp_lbl = M_prime.copy().next_to(large_rect, LEFT, buff=0.2)
        
        self.play(
            TransformFromCopy(M_prime, another_Mp_lbl),
            run_time=1
        )
        self.wait(2)
        arr = Arrow(another_Mp_lbl.get_right(), large_rect.get_left()+RIGHT*2, buff=0.2).set_color(GOLD).set_stroke(width=10)
        self.play(GrowArrow(arr), 
                  *[mobj.animate.shift(RIGHT*2) for mobj in [ M, M_lbl, M_prime, large_rect, append_steps]],
                  run_time=1.5)
        self.wait(2)
        ques = MathTex(r"?", color=YELLOW).scale(4).set_stroke(width=15, background=True).next_to(append_steps, RIGHT, buff=0.2)
        self.play(Write(ques), run_time=1.5)
        self.wait(2)
        # 如果停机，那根据构造就会进入循环；如果循环，那根据构造就会停机，不管怎样都是矛盾的。
        # 这意味着，输出是否能在有限步停机的这个问题，是不可能被任何图灵机本身的计算过程解决的。

class S3(Scene):
    def construct(self):
        text = Text("三句话证明").set_color(YELLOW).scale(2)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1.5)

class Digit(VGroup):
    def __init__(self, digit):

        super().__init__()
        self.number = []
        self.digit = digit
        for i in range (10):
            numberi = Text(r"%d"%i, font='Consolas').set_color(YELLOW).set_opacity(0)
            self.add(numberi)
            self.number.append(numberi)
        self.number[self.digit].set_opacity(1)

    def set_number(self, digit, opacity):
        self.number[self.digit].set_opacity(0)
        self.digit = digit
        self.number[self.digit].set_opacity(opacity)
        return self

class IncompleteProof(Scene):
    def construct(self):
        lock = SVGMobject("lock_icon.svg").scale(1.2).shift(UP*2)  
        self.play(DrawBorderThenFill(lock), run_time=1.5)
        self.wait(2)
        
        digit_windows = VGroup()
        for i in range(6):
            digit_windows.add(
                RoundedRectangle(
                    height=0.5, width=0.4, color=WHITE, 
                    stroke_width=0, corner_radius=0.05
                ).set_fill(color=BLUE).set_opacity(0.6).move_to(lock.get_center()+DOWN*2+(i-2.5)*RIGHT*0.44)
            )
        
        self.play(FadeIn(digit_windows), run_time=0.5)
        self.wait(2)

        digits_value = [ValueTracker(0) for _ in range(6)]
        digits = VGroup()

        
        for i in range(6):
            digits.add(
                Digit(0).scale(0.5).move_to(digit_windows[i]).add_updater(lambda m, idx=i: m.set_number(int(digits_value[idx].get_value()), 1))
            )
        self.play(Create(digits), run_time=1)
        self.wait(2)

        for _ in range(5):
            passwd = np.random.randint(0, 999999)
            new_digits = [int(d) for d in str(passwd)]
            # prepend 0s if new passwd is shorter than 6 digits
            new_digits = [0]*(6-len(new_digits)) + new_digits
            self.play(
                *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
                run_time=0.3
            )
            self.wait(0.7)
        
        self.wait(2)

        mingti = Text("1是存在的").set_color(ORANGE).scale(1.2).shift(LEFT*3+DOWN*2)
        proof_text = MathTex(r"(\exists x)(x=sy)", r"\ (\exists x)(x=s0)").scale(0.8).set_color(YELLOW).shift(RIGHT*3+DOWN)
        big2 = MathTex("2", color=BLUE).scale(3).next_to(proof_text[0], DOWN, buff=0.1)
        proof_int1 = MathTex(
            r"2^8\times 3^4\times 5^{13}\times 7^{9} \times 11^8\times 13^{13}\\ \times  17^5 \times 19^7\times 23^{17} \times 29^9"
        ).scale(0.6).set_color(BLUE).next_to(big2, RIGHT, buff=0.1).align_to(big2, UP)
        bigtimes3 = MathTex(r"\times 3", color=BLUE).scale(3).next_to(big2, DOWN, buff=0.1).shift(LEFT*0.3)
        proof_int2 = MathTex(
            r"2^8\times 3^4\times 5^{13}\times 7^{9} \times 11^8\times 13^{13} \\ \times  17^5 \times 19^7\times 23^{6} \times 29^9"
        ).scale(0.6).set_color(BLUE).next_to(bigtimes3, RIGHT, buff=0.1).align_to(bigtimes3, UP)
        proofnumber = VGroup(big2, proof_int1, bigtimes3, proof_int2)

        self.play(Write(mingti), run_time=1)
        self.wait(2)
        self.play(Write(proof_text), run_time=1)
        self.wait(1)
        self.play(Write(proofnumber), run_time=1)
        self.wait(2)

        self.play(
            FadeOut(proofnumber), 
            proof_text.animate.shift(DOWN),
            run_time=1
        )
        self.wait(2)

        new_digits = [0,0,0,0,0,0]
        self.play(
            *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
            run_time=1
        )
        self.wait(0.5)
        self.play(Wiggle(lock), run_time=1)
        self.wait(2)

        rect1 = SurroundingRectangle(proof_text[0], buff=0.1).set_color(GREEN)
        rect2 = SurroundingRectangle(proof_text[1], buff=0.1).set_color(GREEN)
        self.play(Create(rect1), run_time=1)
        self.wait(0.5)
        self.play(Transform(rect1, rect2), run_time=1)
        self.wait(3)
        self.play(
            FadeOut(rect1), 
            run_time=1)

        unknown_passwd = VGroup()
        passwd_digits = VGroup()
        for i in range(6):
            unknown_passwd.add(
                RoundedRectangle(
                    height=0.5, width=0.4, color=WHITE, 
                    stroke_width=0, corner_radius=0.05
                ).set_fill(color=GREEN).set_opacity(0.6).next_to(digit_windows[i], DOWN, 0.3)
            )
            passwd_digits.add(
                Text("?").scale(0.5).set_color(YELLOW).move_to(unknown_passwd[i])
            )
        self.play(
            TransformFromCopy(digit_windows, unknown_passwd),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            Write(passwd_digits),
            run_time=1
        )
        self.wait(2)


        for i in range(114514 // 1973):
            new_digits = [int(d) for d in str(i*1973)]
            # prepend 0s if new passwd is shorter than 6 digits
            new_digits = [0]*(6-len(new_digits)) + new_digits
            self.play(
                *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
                run_time=0.15
            )
        new_digits = [1,1,4,5,1,4]
        self.play(
            *[digits_value[idx].animate.set_value(new_digits[idx]) for idx in range(6)],
            run_time=0.5
        )
        
        self.wait(0.5)
        self.play(Wiggle(lock), run_time=1)

        result_digits = VGroup()
        for i in range(6):
            result_digits.add(
                Text(str(new_digits[i]), font='Consolas').set_color(YELLOW).scale(0.5).move_to(unknown_passwd[i])
            )

        self.play(
            *[Flash(mob) for mob in unknown_passwd],
            *[Transform(passwd_digits[i], result_digits[i]) for i in range(6)],
            run_time=0.6
        )
        self.play(
            Rotate(lock[0], angle=-PI/6, about_point=lock[0].get_edge_center(RIGHT+DOWN)),
        )
        self.wait(2)

            
class TestLock(Scene):
    def construct(self):
        lock = SVGMobject("lock_icon.svg").scale(1.2).shift(UP*2)  
        self.play(DrawBorderThenFill(lock), run_time=1.5)
        self.wait(2)
        
        # self.add(index_labels(lock))
        self.play(
            Rotate(lock[0], angle=-PI/6, about_point=lock[0].get_edge_center(RIGHT+DOWN)),
        )
        self.wait(2)


class EnumProof(MovingCameraScene):
    def construct(self):
        question = Text("1是存在的").set_color(ORANGE).scale(1.2).to_edge(UP)
        hor_line = Line(LEFT*7, RIGHT*7).next_to(question, DOWN, buff=0.2)
        ver_line = Line(UP*3, DOWN*9).next_to(hor_line, DOWN, buff=0.).shift(LEFT*3)

        grid_lines = [hor_line.copy().set_color(GOLD).set_stroke(width=2).shift(DOWN*(i+1)*1.2) for i in range(10)]
        grid_lines = VGroup(*grid_lines)

        self.play(
            LaggedStart(
            Write(question),
            GrowFromCenter(hor_line),
            Create(ver_line)),
            run_time=1.5
        )
        self.wait()
        self.play(
            LaggedStart(
                *[Create(line) for line in grid_lines],
                lag_ratio=0.5,
                run_time=2
            )
        )
        self.wait(2)

        vocab = [r"\lnot", r"\lor", r"\supset", r"\exits", "=", "0", "s", "(", ")", ",", "+", "x", "y", "z"]

        proof_num = ["1", "2", "3", "319428", r"\hdots", "N"]
        proof_num_lbl = VGroup()
        for i in range(5):
            proof_num_lbl.add(
                MathTex(proof_num[i], color=BLUE).next_to(grid_lines[i], UP, buff=0.2).shift(LEFT*5).scale(1.2)
            )
        proof_num_lbl.add(
            MathTex(proof_num[5], color=ORANGE).next_to(grid_lines[5], UP, buff=0.2).scale(1.2).shift(LEFT*5)
        )

        text_list = [r"\lnot", r"\lor", r"\supset", r"\exists )", r"\hdots", r"(\exists x)(x=sy) (\exists x)(x=s0)"]
        proof_text = VGroup()
        for i in range(5):
            proof_text.add(
                MathTex(text_list[i], color=RED).next_to(grid_lines[i], UP, buff=0.2).shift(RIGHT*2).scale(1.2)
            )
        proof_text.add(
            MathTex(text_list[5], color=GREEN).next_to(grid_lines[5], UP, buff=0.2).scale(1.2).shift(RIGHT*2)
        )

        for i in range(5):
            self.play(
                Write(proof_num_lbl[i]),
                Write(proof_text[i]),
                run_time=1
            )
            self.wait(0.5)
        self.wait(2)

        self.play(
            self.camera.frame.animate.move_to(grid_lines[5].get_center()),
            run_time=1
        )
        self.wait()
        self.play(
            Write(proof_num_lbl[5]),
            Write(proof_text[5]),
            run_time=1.5
        )
        self.wait(1)

        tick_sign = MathTex(r"\checkmark", color=RED).scale(2).next_to(proof_text[5], RIGHT, buff=0.2)
        self.play(Write(tick_sign), run_time=1)
        self.wait(2)

class KaisuoWanbei(Scene):
    def construct(self):
        turing_K = VGroup(RoundedRectangle(width = 4, height = 4, color = BLUE_B, stroke_width = 8), 
                          MathTex(r"K", color = BLUE)[0].scale(2).next_to(2*UP + 2*LEFT, DR), 
                          RoundedRectangle(width = 3.5, height = 2.5, color = BLUE_B, stroke_width = 8).shift(0.5*DOWN), )
        self.add(turing_K)
        text = Text("开锁师傅", font='heiti').scale(1.2).set_color(YELLOW).next_to(turing_K, DOWN, buff=0.2)
        self.add(text)

        lock = SVGMobject("lock_icon.svg").shift(LEFT*4)
        self.play(DrawBorderThenFill(lock), run_time=0.5)
        self.wait(0.5)
        _lock = lock.copy().scale(0.6).move_to(turing_K[2].get_center())
        self.play(Transform(lock, _lock), run_time=1)
        self.wait(0.5)

        self.play(
            Rotate(lock[0], angle=-PI/6, about_point=lock[0].get_edge_center(RIGHT+DOWN)),
            run_time=0.5
        )

        self.wait(0.2)

        true_text = Text("真").scale(1.2).set_color(GREEN).next_to(turing_K, RIGHT, buff=0.2).shift(UP*0.5)
        false_text = Text("假").scale(1.2).set_color(RED).next_to(turing_K, RIGHT, buff=0.2).shift(DOWN*0.5)
        self.play(
            LaggedStart(
                Write(true_text),
                Write(false_text),
                run_time=0.5
            )
        )
        self.wait(1)

        self.play(FadeOut(lock), run_time=0.5)

        lock = SVGMobject("lock_icon.svg").shift(LEFT*5)
        _lock = lock.copy().scale(0.6).move_to(turing_K[2].get_center())
        
        self.play(DrawBorderThenFill(lock), run_time=0.5)
        self.play(TransformFromCopy(lock, _lock), run_time=1)
        self.wait()
        self.play(Wiggle(_lock), run_time=1)
        self.wait(2)

        cross_on_lock = Cross(lock, stroke_width=15, color=RED)
        self.play(Create(cross_on_lock), run_time=1)

        incomp_text = Text("无法判断").set_color(RED).scale(0.9).next_to(lock, DOWN, buff=0.2)
        self.play(Write(incomp_text), run_time=1)
        self.wait(2)
        
        Complete_text = Text("完备性").set_color(YELLOW).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(Complete_text, DOWN, buff=0.2)
        self.play(
            Write(Complete_text),
            GrowFromCenter(line),
            run_time=1.5
        )
        self.wait()
        self.play(
            FadeOut(cross_on_lock),
            FadeOut(incomp_text),
            run_time=1
        )
        self.wait(2)
        tick_sign = MathTex(r"\checkmark", color=RED).scale(4).move_to(lock).set_stroke(width=10, background=True)
        self.play(Write(tick_sign), run_time=1)
        self.wait(2)

        self.play(
            *[FadeOut(mob)for mob in [tick_sign, lock, _lock, true_text, false_text]]
        )
        self.wait()

        halo_ring = Ellipse(width=5, height=1.3, color=YELLOW_C,stroke_width=15).set_fill(opacity=0).next_to(turing_K, UP).shift(DOWN*0.4)
        god_name = Text("神", font='heiti').scale(1.2).set_color(YELLOW).next_to(turing_K, DOWN, buff=0.2)
        self.play(
            FadeIn(halo_ring),
            Transform(text, god_name),
            run_time=2)
        self.wait(4)

class SelfRef(Scene):
    def construct(self):
        text = Text("自我指涉").set_color(YELLOW).scale(2)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(1.5)

        title = text.copy().scale(0.5).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN, buff=0.2)
        self.play(
            ReplacementTransform(text, title),
            GrowFromCenter(line),
            run_time=1.5
        )
        self.wait(4)

        sent = Text("这句话是假的").set_color(RED).scale(1.5)
        rect = SurroundingRectangle(sent, buff=0.1).set_color(YELLOW)
        
        russo_para = MathTex(r"A=\{X: X\notin X\}").scale(1.5).set_color(BLUE).shift(UP*1.5+LEFT*4)

        self.play(Write(sent), run_time=1)
        self.wait(1.5)
        self.play(Create(rect), run_time=1)
        self.wait(2)
        self.play(Write(russo_para), run_time=1)
        self.wait(5)


class Factorial(Scene):
    def construct(self):
        conv_def = MathTex(r"n! = n\times (n-1)\times (n-2)\times \cdots \times 2\times 1").scale(1.2).set_color(YELLOW).shift(UP*2)
        self.play(Write(conv_def), run_time=1.5)
        self.wait(2)
        recur_def = MathTex(r"n! = n\times (n-1)!").scale(2).set_color(ORANGE).shift(DOWN)
        self.play(Write(recur_def), run_time=1.5)
        self.wait(2)

class Banner(Scene):
    def construct(self):
        nplane = NumberPlane(            
        )