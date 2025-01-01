from manim import *
import numpy as np
import math

def interval_seg(st, ed, seg_color=WHITE):
    result = VGroup()
    result.add(
        Line(st,ed, stroke_width=4).set_color(seg_color),
        Line(st, st+0.1*UP, stroke_width=2).set_color(seg_color),
        Line(ed, ed+0.1*UP, stroke_width=2).set_color(seg_color),
    )
    return result

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
        self.wait(1.5)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class Question(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        

        self.wait(3) # 在小学的时候，我们接触了无限循环小数
        text1 = MathTex(r"1 \div 9=",r"0.1111\cdots", color=BLUE).shift(UP*2.5)
        self.play(DrawBorderThenFill(text1[0]))
        self.wait(3) # 比如说，1除以9，是永远除不尽的
        self.play(Create(text1[1]), run_time=2) # 算出来，小数点后是无穷无尽的1
        t2 = MathTex(r"0.\dot{1}", color=YELLOW).next_to(text1[0], RIGHT, buff=0.1)
        self.wait(5) # 写成无穷循环的记号，就是这样加一个点，表示小数点后无穷多个1
        self.play(Transform(text1[1], t2))
        self.wait(4) # 于是，小学一个争论不休的经典神棍问题就来了

        text2 = MathTex(r"0.\dot{9}","\ ?\ \ ", "1").scale(1.5)
        text2[1].set_color(RED)
        self.play(DrawBorderThenFill(VGroup(text2[0], text2[2])), run_time=2)
        # 一个0.9无限循环，一个1
        self.wait(2)
        self.play(Write(text2[1]), run_time=2) # 它们两个究竟谁更大呢？
        self.wait(2) # 这个问题引起了很大的争议

        self.play(
            FadeOut(text1),
            text2.animate.shift(UP*2.5),
            run_time=2
        )

        equal = MathTex(r"0.\dot{9} = 1", color = BLUE).next_to(text2, DOWN, buff=0.8).shift(LEFT*5)
        deduce = MathTex(r"0.\dot{9}", r"=9\times 0.\dot{1}", r"=9\times \frac{1}{9}", "=1",
                          color = BLUE).shift(UP)
        self.play(Write(equal))
        self.wait()
        self.play(Write(deduce[0]))
        for _ in range(1, len(deduce)):
            self.wait(2)
            self.play(Write(deduce[_]))
        self.wait(4) # 听起来挺有道理的哈

        self.play(FadeOut(deduce))
        less = MathTex(r"0.\dot{9} < 1", color = GREEN).next_to(equal, DOWN, buff=1).align_to(equal, LEFT)
        self.play(Write(less))
        self.wait(3) # 可有人说是小于，为什么呢

        nines_digit = MathTex("0", r".9999999 \cdots", color=BLUE).shift(DOWN*0.5)
        one_digit   = MathTex("1", r".0000000 \cdots", color=ORANGE).next_to(nines_digit, DOWN, buff=0.3).align_to(nines_digit)
        self.play(Write(nines_digit), Write(one_digit), run_time=2) # 他们说，你把小数点展开
        self.wait()
        self.play(Circumscribe(nines_digit[0]), Circumscribe(one_digit[0]), run_time=1) #根据小数比较大小的规则
        self.wait(2) # 第一位已经分出了胜负，后面就算再怎么接近也不用看了，胜负已分
        sfyf = Text("胜负已分", color=RED).scale(0.8).next_to(one_digit, DOWN, buff=1)
        gougou = MathTex(r"\checkmark", color=RED).next_to(one_digit, RIGHT, buff=1)
        self.play(Write(gougou), Write(sfyf))
        self.wait(5) # 两种说法各有各自的道理，究竟谁才是对的呢？
        
        self.play(FadeOut(VGroup(text2, one_digit, nines_digit, equal,
                                 gougou, sfyf, less)))
        
        self.wait(6) # 事实上，回答这个问题远远比想象中复杂，因为我们首先需要回答这样一个非常根本的问题
        definition = Text("定义", color=YELLOW).scale(2)
        self.play(Write(definition))
        self.wait(2)
        self.play(FadeOut(definition))
        self.wait(2)

        xunhuan_def = MathTex(r"0.\dot{9}", "=", "0.9999999 \cdots", color=GREEN).scale(2).shift(UP*2)
        self.play(Write(xunhuan_def), 
                  run_time=3, lag_ratio=0.5)
        # 那就是，当我们写下这个循环小数的时候，我们究竟在说什么？
        self.wait(3)
        # 以上两种阐释所产生的矛盾，本质上是我们对于这个无限循环表示的含义不清晰
        self.play(Circumscribe(xunhuan_def), run_time=2)
        self.wait(2)
        # 甚至，我们曾经最习以为常相等关系a=b，现在面临这样一个抽象的问题，都需要重新审视并严格地定义它

        real_equal_def = MathTex(r"\frac{1}{9} \quad ","=",r"\quad 0.1111\cdots", color=BLUE).scale(2)
        rect = SurroundingRectangle(real_equal_def[1], color=YELLOW)
        self.play(Create(real_equal_def))
        self.wait(2)
        self.play(Create(rect))
        question_mark = MathTex("?", color=RED).scale(2.5).next_to(real_equal_def[1], DOWN, buff=0.5)
        self.wait()
        self.play(Create(question_mark))
        self.wait(3)

def add_tick(line, num, st=None, ed=None):
    result = VGroup()
    if st is None:
        st = line.get_start()
        ed = line.get_end()
    for i in range(0, num+1):
        result.add(Line(
            st + i / num * (ed - st),
            st + i / num * (ed - st) + UP*0.1,
            stroke_width=1
        ))
    return result

class GeoSqrt2(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        self.wait(5) # 让我们暂且按下不表，先把时钟拨回古希腊
        profile = ImageMobject(
            "bdgls.png",
        ).shift(LEFT*4)

        capt = Text("毕达哥拉斯 Pythagoras").scale(0.7).next_to(profile, DOWN, buff=0.2)

        self.play(FadeIn(profile), Write(capt), run_time=2, lag_ratio=0.7)
        # 古希腊有一个著名的哲学家和数学家，叫毕达哥拉斯
        self.wait(4)
        # 他最有名的成就，就是发现了毕达哥拉斯定理，也就是我们说的勾股定理

        tri = Polygon(ORIGIN + RIGHT*2, ORIGIN+RIGHT*5, ORIGIN+RIGHT*2+UP*2, stroke_color=ORANGE,
                        fill_color=BLUE_C, fill_opacity=0.7)
        a_ = MathTex("a", color=GREEN).next_to(tri, LEFT)
        b_ = MathTex("b", color=GREEN).next_to(tri, DOWN)
        c_ = MathTex("c", color=GREEN).move_to(b_.get_center()+ UP * 2.3+ RIGHT*0.2)
        ggdl = MathTex(r"a^2+b^2=c^2", color=YELLOW).next_to(tri, DOWN*4.5, buff=0.3)

        self.play(DrawBorderThenFill(tri),
                  Write(VGroup(a_, b_, c_)),
                  Write(ggdl),
                  run_time=3)
        
        self.wait(2)

        rect = Rectangle(height=1, width=1, stroke_color=PURE_RED).shift(LEFT*4.7+DOWN*0.8)
        self.play(Create(rect))
        self.wait(3) # 你看这个图上在他旁边画的，就是我们熟知的勾三股四弦五

        self.play(*[FadeOut(mob)for mob in self.mobjects])
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        self.wait(5 + 3) # 毕达哥拉斯他不仅自己厉害，而且还引领着一帮小弟，叫毕达哥拉斯学派
        # 毕达哥拉斯学派呢有两个朴素的信仰，第一个信仰呢叫万物皆数

        etin = Text("1. 万物皆数 (All things are numbers)", color=YELLOW).shift(UP*2.5)
        self.play(Write(etin), run_time=2)
        self.wait(8) # 啥意思呢？就是说这个宇宙中的万物和一切啊，本质上都是由数字
        self.wait(8)
        # 以及数字对应的概念组合而成的。这个信仰其实在计算机里得到了很大的应用
        # 比如说音频啊，视频啊，游戏啊，其实在计算机的世界里就是一堆0和1，然后到物理的世界里
        # 给你演绎，变成各种各样的东西。

        self.wait(3) # 但是另外有一个信仰就很抽象了，叫数字皆可公比
        etid = Text("2. 数字皆可公度 ", color=YELLOW).shift(UP*0.5).align_to(etin, LEFT)
        self.play(Write(etid))
        self.wait(4) # 这个说起来就非常抽象了，什么叫做公度，又为什么数字皆可公度呢？

        self.play(FadeOut(etin), etid.animate.shift(UP*2.5), run_time=1.5)
        self.wait(4)
        # 公度，展开来说就是“公共度量”
        
        self.wait(4) # 所谓度量，说的就是可以表示成同一个单位的整数倍
        #self.play(FadeOut(ratio_text))

        line1 = Line(LEFT*2.5, RIGHT*2.5, stroke_color=BLUE_C)
        line2 = Line(LEFT*2, RIGHT*2, stroke_color=MAROON).next_to(line1, DOWN, buff=1.5).align_to(line1, LEFT)
        self.play(Create(VGroup(line1, line2)), run_time=1.5, lag_ratio=0.5)

        self.wait(3)
        ticks1 = add_tick(line1, 5)
        ticks2 = add_tick(line2, 4)

        self.play(Create(ticks1), run_time=2, lag_ratio=0.5)
        self.wait()
        self.play(Create(ticks2), run_time=2, lag_ratio=0.5)
        self.wait(2)

        line_seg = Line(LEFT*2.5, LEFT*1.5, stroke_color=YELLOW).shift(UP*0.5)
        self.play(Create(line_seg))

        five_times = MathTex(r"5\times").scale(0.8).next_to(line1, RIGHT)
        seg1 = Line(ORIGIN, RIGHT, stroke_color=YELLOW).next_to(five_times, RIGHT, buff=0.1)

        four_times = MathTex(r"4\times").scale(0.8).next_to(line2, RIGHT).align_to(five_times, LEFT)
        seg2 = Line(ORIGIN, RIGHT, stroke_color=YELLOW).next_to(four_times, RIGHT, buff=0.1)

        st = line1.get_start()
        ed = line1.get_end()
        for i in range(5):
            pos = st + (i+0.5) / 5 * (ed - st)
            self.play(line_seg.animate.move_to(pos+0.4*UP),
                    rate_func=smooth,
                    run_time=0.5)
            self.wait(0.5)
        
        self.play(Create(VGroup(five_times, seg1)), lag_ratio=0.5)
    
        st = line2.get_start()
        ed = line2.get_end()
        for i in range(4):
            pos = st + (i+0.5) / 4 * (ed - st)
            self.play(line_seg.animate.move_to(pos+0.4*UP),
                    rate_func=smooth,
                    run_time=0.5)
            self.wait(0.5)
        
        self.play(Create(VGroup(four_times, seg2)), lag_ratio=0.5)
        self.wait(3)
        self.play(FadeOut(line_seg))
        self.wait(2)
        self.play(Circumscribe(five_times),Circumscribe(four_times))
        self.wait(3)

class Ratio(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        a_ = ValueTracker(16)
        b_ = ValueTracker(10)

        self.wait(4) # 其实，这里找到一根单位的线段
        line1 = always_redraw(
            lambda: Line(LEFT*3.2, LEFT*3.2+RIGHT*a_.get_value()*0.4, 
                         stroke_width=5,
                         stroke_color=BLUE_C)
            )

        line2 = always_redraw(
            lambda: Line(LEFT*2, LEFT*2+RIGHT*b_.get_value()*0.4,stroke_width=5,stroke_color=MAROON)
            .next_to(line1, DOWN, buff=1.5)
            .align_to(line1, LEFT)
        )

        a_value = always_redraw(
            lambda: DecimalNumber(a_.get_value(), 1).set_color(BLUE_C)
            .move_to(LEFT*5)
        )

        b_value = always_redraw(
            lambda: DecimalNumber(b_.get_value(), 1).set_color(GREEN_C)
            .move_to(LEFT*5 + DOWN*1.5)
        )

        self.play(Create(VGroup(line1, line2)), run_time=1.5, lag_ratio=0.5)
        self.play(Create(VGroup(a_value, b_value)))
        self.wait(3) # 那么， 到底该怎么找到这个公比呢？
        zzxj = Text("辗转相减法", color=YELLOW_C).shift(UP*3)
        self.play(Write(zzxj), run_time=2) # 答案其实很经典，那就是辗转相减法
        self.wait(2)
        
        for _ in range(8):

            if a_.get_value() > b_.get_value():
                move = a_
                dest = a_.get_value() - b_.get_value()
            elif a_.get_value() < b_.get_value():
                move = b_
                dest = b_.get_value() - a_.get_value()
            else:
                break
            
            text = MathTex(f"{int(move.get_value())}-{int(move.get_value()-dest)}={int(dest)}").shift(UP*1.5)

            self.play(
                Write(text),
                move.animate.set_value(dest),
                rate_func=smooth,
                run_time=1
            )
            self.play(FadeOut(text), run_time=0.5)
            self.wait()
        
        self.wait()
        r1, r2 = SurroundingRectangle(a_value), SurroundingRectangle(b_value)
        self.play(Create(r1), Create(r2))

        equal_text = MathTex("2=2", color=YELLOW).shift(UP*1.5)
        self.play(Write(equal_text))
        self.wait(2)
        self.play(FadeOut(equal_text), FadeOut(r1), FadeOut(r2))
        danwei = Line(ORIGIN, ORIGIN + line1.get_end()-line1.get_start(), stroke_width=5).set_color(YELLOW_C).shift(UP*1)
        self.wait(1) # 于是，我们就得到了一个可以同时整除一开始的单位长线段
        self.play(TransformFromCopy(line1, danwei))
        self.wait(2)

        self.play(a_.animate.set_value(16),
                  b_.animate.set_value(10),
                  rate_func=smooth, run_time=1)
        self.wait(2)

        n1 = ValueTracker(0.)
        n2 = ValueTracker(0.)
        number1 = always_redraw(
            lambda: DecimalNumber(n1.get_value(), 0).shift(5*RIGHT)
        )
        number2 = always_redraw(
            lambda: DecimalNumber(n2.get_value(), 0).shift(5*RIGHT+1.5*DOWN)
        )

        # 用这根最终得到的线段作为单位，就可以“度量”一开始的两个线段了
        # 我们一一比对就可以发现，第一条线段的长度是这个单位的8倍
        st = line1.get_start()
        ed = line1.get_end()
        self.play(Write(number1))
        for i in range(8):
            pos = st + (i+0.5) / 8 * (ed - st)
            self.play(
                    danwei.animate.move_to(pos+0.4*UP),
                    n1.animate.set_value(i+1),
                    rate_func=smooth,
                    run_time=0.3)
            self.wait(0.2)
        self.wait(1)

        # 而第二条线段的长度是单位的5倍
        st = line2.get_start()
        ed = line2.get_end()
        self.play(Write(number2))
        for i in range(5):
            pos = st + (i+0.5) / 5 * (ed - st)
            self.play(danwei.animate.move_to(pos+0.4*UP),
                    n2.animate.set_value(i+1),
                    rate_func=smooth,
                    run_time=0.3)
            self.wait(0.2)

        self.wait()
        self.play(Circumscribe(number1), Circumscribe(number2))
        self.wait(8)
        # 为什么毕达哥拉斯学派对于找一个单位这么着迷于找单位呢？刚才我们说他们信奉“万物皆数”
        # 历史资料证明，他们说的“数”其实都是整数，因为在他们眼里，整数是最自然、最完美、最没有人为的痕迹的数
        # 对于不是整数的数，他们因此想方设法总想找到一个单位，让这个数在此单位下成为整数

        self.play(*[FadeOut(mob)for mob in self.mobjects])
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        self.wait(5)
        # 这里我们就有很多事情值得说道一下，比如说
        # 为什么明明用整数就能表示的辗转相减，我这里要用线段呢？
        profile = ImageMobject("Euklid.jpg").shift(LEFT*4)
        jhyb = ImageMobject("jhyb.png",).shift(RIGHT*3)

        capt = Text("欧几里得 Euklid").next_to(profile, DOWN, buff=0.2)

        self.play(FadeIn(profile), Write(capt), run_time=2, lag_ratio=0.5)   
        self.wait(4)
        # 其实，这是来自于古希腊的悠久传统
        # 早在几何和公理系统宗师 欧几里得开始，你翻开他那本最经典的几何原本就能看到
        self.play(FadeIn(jhyb))
        # 这些有关数字之间的关系的证明，其实全部是用线段完成的
        self.wait(4 + 5)
        # 比如这个定理其实就是说，如果a比b等于c比d，c比d等于e比f，那么a比b等于e比f
        # 在古希腊的数学体系里，比值，也就是这里你能看到的ratio，占据着非常重要的位置
        # 我们通常说的有理数, rational number
        # 这里其实中文的翻译有些误导，rational虽然是西方启蒙主义的理性同一个词
        # 但词根应该来源于ratio比值，所以相比有理数更好的说法是“比值数”
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        # 这里就有一个有意思的表情包，利用这双关梗
        bqb = ImageMobject("real_ration.jpg",).scale(1.5)
        self.play(FadeIn(bqb))
        self.wait(7)
        # 虚数单位i和π在那吵架，π说你“现实一点”，因为虚数imaginary他不是实数real
        # 虚数单位对π说“你理性一点”，玩的梗就是刚才说的这个“可比”和“理性”
        
class Triangle(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        self.wait(3) # 理解了古希腊那个时候人们都用几何的语言来讨论代数的问题

        axis_orig = ORIGIN + LEFT*2 + DOWN*2
        A_pos = axis_orig + 4 * UP
        B_pos = axis_orig
        C_pos = axis_orig + 4 * RIGHT

        triangle = Polygon(A_pos, B_pos, C_pos,
                           stroke_color=BLUE,
                           fill_color=BLUE_C,
                            fill_opacity=0.5)

        A_label = MathTex(r"A", color=WHITE).scale(0.8).move_to(A_pos + 0.3 * UP + 0.4 * LEFT)
        B_label = MathTex(r"B", color=WHITE).scale(0.8).move_to(B_pos + 0.3 * DOWN + 0.4 * LEFT)
        C_label = MathTex(r"C", color=WHITE).scale(0.8).move_to(C_pos + 0.3 * DOWN + 0.4 * RIGHT)
        point_labels = VGroup(A_label, B_label, C_label)

        one_label = MathTex(r"1", color=YELLOW).next_to(triangle, LEFT, buff=0.5)
        sqrt2_label = MathTex(r"\sqrt{2}", color=YELLOW).move_to(axis_orig + 2.4*UP+2.4*RIGHT)

        self.play(DrawBorderThenFill(triangle), run_time=3) 
        # 我们就可以穿越千年的时间，切身体会一下当年希帕索斯是怎么发现根号二是无理数的
        self.wait(4)
        self.play(Create(point_labels), run_time=3, lag_ratio=0.5)
        # 众所周知，根号二来自等腰直角三角形，我们这里就做一个等腰直角三角形ABC
        self.wait(2) # 
        self.play(Write(VGroup(one_label, sqrt2_label)),
                  run_time=2, lag_ratio=0.8)
        self.wait() 
        self.play(FadeOut(one_label), FadeOut(sqrt2_label))
        # 那么如果直角边的长度是1呢，斜边长就是根号2
        self.wait(8)
        # 现在我们要干什么呢？没错，我们就用刚才找单位的方法，显式的做辗转相减
        # 直角边和斜边

        AB_line = Line(A_pos, B_pos, stroke_width=8).set_color(PURE_RED)
        AC_line = Line(A_pos, C_pos, stroke_width=8).set_color(PURE_GREEN)
        self.play(Create(VGroup(AB_line, AC_line)), run_time=2)
        self.wait(3)

        # 来试着找一个小的单位，让1和根号2都是这个单位的整数倍
        # 第一步，斜边大于直角边，所以我们要在斜边上减去直角边，怎么减呢？
        D_pos = axis_orig + RIGHT * 4 * (np.sqrt(2)-1)
        D_dot = Dot().move_to(D_pos).set_color(ORANGE)
        aux_line = DashedLine(
            A_pos, D_pos, stroke_width=5, color=YELLOW
        )
        D_label = MathTex(r"D", color=YELLOW).scale(0.8).move_to(D_pos + 0.3 * DOWN)
        self.play(Create(aux_line), run_time=1.5)
        self.play(Create(D_dot), Write(D_label))
        self.wait()

        E_pos = axis_orig + RIGHT * 2 * np.sqrt(2) + UP * 4 * (1-np.sqrt(0.5))
        E_dot = Dot().move_to(E_pos).set_color(GREEN)
        aux_line2 = DashedLine(
            D_pos, E_pos, stroke_width=5, color=YELLOW
        )
        E_label = MathTex(r"E", color=YELLOW).scale(0.8).move_to(E_pos + 0.3 * UP + 0.3*RIGHT)
        perp = Elbow(color=YELLOW, angle=5*PI/4).move_to(E_pos+0.2*DOWN)
        self.play(Create(aux_line2), run_time=1)
        self.play(Create(perp))
        self.play(Create(E_dot), Write(E_label))
        self.wait(3) # 一些简单的全等知识告诉我们，

        tri_ABD = Polygon(A_pos, D_pos, B_pos,
                           stroke_color=BLUE,
                           fill_color=BLUE_C,
                            fill_opacity=0.5)

        tri_ADE = Polygon(A_pos, D_pos, E_pos,
                           stroke_color=BLUE,
                           fill_color=BLUE_C,
                            fill_opacity=0.5)
        
        self.play(Indicate(tri_ABD), run_time=1)
        self.play(Indicate(tri_ADE), run_time=1)
        # 三角形ADB和三角形ADE是全等的
        self.play(FadeOut(tri_ABD), FadeOut(tri_ADE), run_time=0.5)
        self.wait(3)

        note1 = MathTex(r"AB=AE", color=YELLOW).scale(0.8).shift(LEFT*4.5 + UP)
        note2 = MathTex(r"BD=DE", color=YELLOW).scale(0.8).next_to(note1, DOWN, buff=0.5)
        note = VGroup(note1, note2)
        self.play(Create(note), run_time=2)

        # 所以，我们可以把AB搬运到AE这里
        AB_move = AB_line.copy()
        self.play(Create(AB_move), run_time=0.5)
        self.play(
            Rotate(AB_move, PI/4, about_point=A_pos),
            run_time=2
            )
        AC_1 = Line(E_pos, C_pos, stroke_width=8).set_color(PURE_GREEN)
        self.play(
            FadeOut(AB_move),
            Transform(AC_line, AC_1),
            run_time=2
        )

        self.wait(3)
        # 现在我们把AB利用等腰的性质移动到BC上来
        self.play(
            Rotate(AB_line, -PI/2, about_point=B_pos),
            run_time=2)
        self.wait(2)
        tri_CDE = Polygon(C_pos, D_pos, E_pos,
                           stroke_color=BLUE,
                           fill_color=BLUE_C,
                           stroke_width=1,
                            fill_opacity=0.5)
        self.play(Indicate(tri_CDE))
        note_3 = MathTex("CE=DE", color=YELLOW).scale(0.8).next_to(note, DOWN, buff=0.5)
        self.play(FadeOut(tri_CDE))
        self.wait(3)
        self.play(Write(note_3))
        self.wait(2)

        AC_move = AC_line.copy()
        self.play(Circumscribe(note_3), Create(AC_move))
        self.play(Rotate(AC_move, -PI/2, about_point=E_pos), run_time=2)
        self.wait(2)
        self.play(Circumscribe(note2))
        self.play(Rotate(AC_move, 3*PI/4, about_point=D_pos), run_time=2)
        self.wait(3)
        # 所以这一步辗转相减得到了什么呢？
        AB_2 = Line(C_pos, D_pos, stroke_width=8).set_color(PURE_RED)
        self.play(
            FadeOut(AC_move), Transform(AB_line, AB_2),
            run_time=2, lag_ratio=0.5
            )

        self.wait(2)

        self.play(
            FadeOut(VGroup(triangle, A_label, B_label, C_label,
                            D_label, E_label, perp, D_dot, E_dot, 
                            note, note_3, aux_line, aux_line2)),
            run_time=1.5
            ) # 仔细看这两条线，你发现了什么？

        self.wait(3)

        _AB_line = Line(B_pos, A_pos, stroke_width=8).set_color(PURE_GREEN)
        _AC_line = Line(A_pos, C_pos, stroke_width=8).set_color(PURE_RED)
        self.play(
            #Create(triangle),
            Transform(AB_line, _AC_line),
            Transform(AC_line, _AB_line),
            run_time=2
        )

        self.play(Create(triangle), FadeOut(AB_line), FadeOut(AC_line), run_time=1)
        self.play(Indicate(triangle), run_time=1)
        sametext = Text("完全一致", color=YELLOW).to_edge(UP)
        self.play(Write(sametext))
        self.wait()
        self.play(FadeOut(sametext))

        for _ in range(8):
            time = 0.3 if _ > 0 else 1
            self.wait(time)
            self.play(Create(VGroup(aux_line, aux_line2)), rum_time=time)
            self.wait(time)
            small_tri = Polygon(C_pos, E_pos, D_pos,
                           stroke_color=BLUE,
                           fill_color=BLUE_C,
                           stroke_width=5,
                            fill_opacity=0.)
            self.play(Create(small_tri), run_time=time)
            self.play(Indicate(small_tri), run_time=0.5)
            self.wait(time)
            self.play(FadeOut(aux_line), FadeOut(aux_line2), Transform(small_tri, triangle.copy()),
                FadeOut(triangle), run_time=1
            )
            triangle = small_tri
        
        self.wait(3) # 这个过程无穷无尽
        self.play(*[FadeOut(mob)for mob in self.mobjects])

class ModernProof(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        self.wait(4) # 这就是为什么，在希帕索斯那个年代
        # 人们虽然连实数的体系都没有建立好，却能够意识到根号2不能表示成两个整数之比
        # 事实上，今天这期视频就是想告诉大家。隐藏在这个几何证明背后的深层含义
        # 其实触动着无限这个概念最深刻的所在
        # 现代证明根号2是无理数的方式是这样的

        eq1 = MathTex(r"\sqrt{2}=\frac{p}{q}").shift(UP*2)
        self.play(Write(eq1)); self.wait(4)

        frac_eqs = MathTex(r"\frac{2}{3}=\frac{4}{6}=\frac{6}{9}=\frac{200}{300}=\cdots", color=YELLOW).scale(0.8)
        self.play(Write(frac_eqs), run_time=2)
        self.wait()
        minpq = Text("p+q最小", color=GREEN).shift(UP*2 + RIGHT*5)
        self.play(Write(minpq)); self.wait()
        self.play(FadeOut(frac_eqs))
        eq2 = MathTex(r"2=\frac{p^2}{q^2}").shift(UP*2)
        self.play(ReplacementTransform(eq1, eq2))
        self.wait(2)
        eq3 = MathTex("2q^2","=","p^2").shift(UP*2)
        self.play(ReplacementTransform(eq2, eq3))
        self.wait(2)
        note1 = MathTex("p = 2 p_1", color=BLUE).shift(LEFT*5)
        self.play(Circumscribe(eq3[0])); self.wait(4)
        # 因为只有偶数的平方才能得到偶数，所以我们知道p可以写成2p1的形式
        self.play(Write(note1)); self.wait()
        eq4 = MathTex("2q^2","=","(2p_1)^2").shift(UP*2)
        self.play(ReplacementTransform(eq3, eq4))
        self.wait(2)
        eq5 = MathTex("2q^2","=","(2p_1)^2").shift(UP*2)
        self.play(ReplacementTransform(eq4, eq5))
        self.wait(2)
        eq6 = MathTex("2q^2","=","4p_1^2").shift(UP*2)
        self.play(ReplacementTransform(eq5, eq6))
        self.wait(2)
        eq7 = MathTex("q^2","=","2p_1^2").shift(UP*2)
        self.play(ReplacementTransform(eq6, eq7))
        self.wait(2)
        eq8 = MathTex("(2q_1)^2","=","2p_1^2").shift(UP*2)
        self.play(Circumscribe(eq7[2])); self.wait(2)
        note2 = MathTex("q = 2 q_1", color=GREEN).shift(LEFT*5+1.5*DOWN)
        self.play(Write(note2))
        self.play(ReplacementTransform(eq7, eq8))
        self.wait(2)
        eq9 = MathTex("4 q_1^2","=","2p_1^2").shift(UP*2)
        self.play(ReplacementTransform(eq8, eq9))
        self.wait(2)
        eq10 = MathTex("2 q_1^2","=","p_1^2").shift(UP*2)
        self.play(ReplacementTransform(eq9, eq10))
        self.wait(2)
        eq11 = MathTex(r"\sqrt{2}=\frac{p_1}{q_1}").shift(UP*2)
        self.play(ReplacementTransform(eq10, eq11))
        self.wait(2)

        rect1 = SurroundingRectangle(minpq)
        rect2 = SurroundingRectangle(eq11)

        conclu = Text("不可能有这样的p和q", color=RED)
        self.play(Create(rect1), Create(rect2))
        self.wait(2)
        self.play(Write(conclu))
        self.wait()

        self.play(*[FadeOut(mob)for mob in self.mobjects])
        # text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        # text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        # self.add(text_1, text_2)

class HolesInNumberLine(MovingCameraScene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        # 现在让我们来仔细品味一下这个令人惊奇的反例蕴含着什么
        # 很多时候，忘掉现有的知识，设身处地的代入历史中角色的视角
        # 体会他们面临的困境、疑惑，思索解决办法，是非常有益处的。
        # 它有助于你深入体会某一个定义、概念乃至学科的本质。最妙的是，历史给出了标准答案供你参考。
        # 在这样的练习和追问中，你的思辨能力会大幅提升，
        # 因为这样的思考本身就是最好的创新练习，对当时的人而言，分析这个问题背后的本质
        # 解决这种危机和困惑 创造出全新的理论，就是创新
        self.wait(5)

        nl = NumberLine(
            color=BLUE,
            include_numbers=True,
            include_tip=True,
            label_direction=DOWN,
        )
        self.play(DrawBorderThenFill(nl), run_time=2)
        self.wait(2)
        # 我们考虑数轴，上面连续分布着形形色色各种各样的数字

        num_list = [0, 1, -3, 2.5]
        num_group = VGroup()
        label_group = VGroup()
        for num in num_list:
            num_group.add(Dot().set_color(GREEN).move_to(nl.n2p(num)))
            label_group.add(MathTex(f"{num}", color=BLUE).next_to(num_group[-1], UP, buff=0.2))
        self.play(Create(num_group), Create(label_group),
                  run_time=3, lag_ratio=0.5)
        self.wait(2)
        self.play(FadeOut(num_group), FadeOut(label_group))
        self.wait(2)
        # 因为单位1可以分成任意小的所谓单位，所以呢，分的单位越细，你可以表示的精确程度就越高
        danwei = NumberLine(
            color=YELLOW,
            x_range = [0,1],
            length = 1,
            include_ticks=True,
            include_numbers=True
        ).shift(UP*2.5)

        # 看起来，对于数轴上任何一个数字，你总可以把1先分成足够小的单位，再用这个单位的整数倍来表示它
        # 吗？
        self.play(Create(danwei), run_time=2)
        self.wait(2)
        ticks = add_tick(danwei, 10)
        nl_ticks = add_tick(line=None, num=130, st=nl.n2p(-7), ed=nl.n2p(6))
        self.play(Create(ticks), run_time=2)
        self.play(Create(nl_ticks), run_time=2)
        self.wait(8)

        # 事实上，希帕索斯已经证明了，根号二就是用这种整数比值方式表示不了的数
        sqrt2 = MathTex(r"\sqrt{2}", color=YELLOW).scale(0.8).move_to(nl.n2p(np.sqrt(2))+UP)
        arr = Arrow(sqrt2.get_center()+0.2*DOWN, nl.n2p(np.sqrt(2)), stroke_width=1,
                     buff=0.03, color=YELLOW)
        self.play(Write(sqrt2), Create(arr), run_time=2, lag_ratio=0.5)
        # 无论你分的多密，它总是不可能完美的落在任何一个刻度上

        ticks2 = add_tick(danwei, 20)
        nl_ticks2 = add_tick(line=None, num=260, st=nl.n2p(-7), ed=nl.n2p(6))
        self.play(FadeOut(ticks), FadeOut(nl_ticks))
        self.play(Create(ticks2), run_time=1)
        self.play(Create(nl_ticks2), run_time=3)
        self.wait(2)
        # 所以，尽管比值数，也就是有理数，在这根数轴上无处不在、极其稠密，
        self.play(ApplyWave(
            nl_ticks2,
            direction=UP,
            time_width=0.5,
            amplitude=0.3
        ),run_time=2)
        self.wait(2)

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=2).move_to(nl.n2p(np.sqrt(2))))
        self.wait(3)
        self.play(Restore(self.camera.frame))

        # 你在任何一小段数轴上能找到无数个有理数
        # 可是，百密终有一疏，数轴上有“洞”，那就是无理数，它不能表示成整数比值的
        # 在你不断用有理数接近根号2的过程中，每一步都是有理数，可最后终点的极限却不是有理数
        # 这就好比你是张三，在长跑比赛里跑了十公里，到达终点线的那一刻却变成了李四，奖牌是李四的了
        # 这就被称作有理数的不完备性。
        incomplete = Text("Incompleteness of Rational Numbers", color=RED).scale(0.8).shift(DOWN*2)
        self.wait(8)
        self.play(DrawBorderThenFill(incomplete), run_time=3)
        self.wait(3)

        # 这里顺带一提，后面的视频我会告诉大家，假如你在0到1之间均匀随机一个数字
        # 它是有理数的概率是0，是无理数的概率是1。也就是说，用有理数去覆盖数轴不是有洞的问题
        # 是几乎啥也没覆盖到。具体的原理和测度论有关，我们之后会说
        self.wait(10)
        # 这里就有一个很矛盾的问题，那就是，明明看起来有理数这么多，
        # 就像随便踩一脚能踩死无数个蚂蚁一样，任意小的区间都有无数的有理数
        # 可是，数轴居然遍地都是根号2这样的无理数。这是怎么回事呢？
        # 从这个例子你就能发现，我们人类感性的感觉和判断是不靠谱的，数学是讲究严谨的逻辑的。
        # 那我们该怎么建立最严格的逻辑框架，在之后指代数轴上任何一个实数的时候，
        x = ValueTracker(0)
        arr = always_redraw(
            lambda: Arrow(nl.n2p(x.get_value())+0.8*UP, nl.n2p(x.get_value())+0.1*UP, stroke_width=2,
                     buff=0.03, color=ORANGE)
        )
        x_value = always_redraw(
            lambda: DecimalNumber(x.get_value(), 2, color=BLUE).scale(0.8).move_to(nl.n2p(x.get_value())+UP)
        )
        self.play(Create(VGroup(arr, x_value)))
        self.play(x.animate.set_value(-PI), run_time=2)
        self.wait()
        self.play(x.animate.set_value(2.718), run_time=2)
        self.wait(2)

        # 都能精确严谨地描述这个数呢？

        self.play(*[FadeOut(mob)for mob in self.mobjects], run_time=2)
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        # 答案是，用“过程”，我们可以借力打力，用一个无穷的过程去定义每一个实数

        prcd = Text("过程", color=YELLOW).scale(2)
        self.play(Write(prcd), run_time=2)
        self.wait()
        self.play(FadeOut(prcd))
        self.wait(2)
        # 如果说，除去定义式，我要你精确的写出根号二，你能怎么办呢？
        sqrt2_decimal = MathTex(r"\sqrt{2}=","1.414213",r"562373095\cdots", color=BLUE).scale(1.2)

        # 你可能会一位一位的把这个数字写出来
        self.play(Write(sqrt2_decimal), run_time=5)
        self.wait(3)

        # 我们必须用无限多位不循环的小数才能定义根号二，在任何有限的时候停下
        self.play(Circumscribe(sqrt2_decimal), run_time=2)
        # 都是一个有限小数，不是无理数根号2的定义。
        # 也就是说，根号2是在这个无穷逼近的过程中达成和定义的
        not_eq = MathTex(r"\not=\sqrt{2}", color=RED).next_to(sqrt2_decimal[1], DOWN, buff=0.2)
        rect = SurroundingRectangle(sqrt2_decimal[1])
        self.wait(4)
        self.play(Create(rect))
        self.wait()
        self.play(Write(not_eq))
        self.wait(3)

        self.play(FadeOut(VGroup(not_eq, rect, sqrt2_decimal)))
        self.wait(2)

        # 因此，为了解决有理数不完备的问题，数学采用了一个“完备化”的过程
        # 来把有理数扩充到充满数轴上的每一个点。
        # 具体方式有好几个等价的定义，这里我们就用区间套定理来说明
        qjt = Text("区间套定理", color=RED).shift(UP*3)
        self.play(Write(qjt), run_time=2)

        nl = NumberLine(
            x_range=[-0.5,2.5],
            length=8,
            color=BLUE,
            include_numbers=True,
            include_tip=True,
            label_direction=DOWN,
        ).shift(UP*1.5)
        self.wait(2)
        self.play(DrawBorderThenFill(nl), run_time=2)
        sqrt2_lbl = MathTex(r"\sqrt{2}", color=YELLOW).move_to(nl.n2p(np.sqrt(2))+UP*0.6)
        arr_to =  Arrow(sqrt2_lbl.get_center()+0.1*DOWN, nl.n2p(np.sqrt(2)), stroke_width=1,
                     buff=0.03, color=YELLOW)
        vline = DashedLine(nl.n2p(np.sqrt(2)), nl.n2p(np.sqrt(2))+5*DOWN, color=YELLOW,
                           stroke_width=1)
        self.play(Create(VGroup(sqrt2_lbl, arr_to, vline)), run_time=2)
        self.wait(2)

        L, R = ValueTracker(1.), ValueTracker(2.)
        # L_val = always_redraw(lambda: DecimalNumber(L.get_value, 3, color=BLUE))
        # R_val = always_redraw(lambda: DecimalNumber(L.get_value, 3, color=BLUE))
        sqrt2_in = always_redraw( lambda:
            MathTex(f"\\sqrt{2}\\in[{L.get_value():.3f}, {R.get_value():.3f})", color=BLUE).shift(LEFT*4)
        )
        self.play(Write(sqrt2_in))

        seg_group = VGroup()
        for i in range(1, 6):
            lf, rt = L.get_value(), R.get_value()
            time = 1 if i < 3 else 0.3
            mid = (lf + rt) / 2
            _line_l = interval_seg(nl.n2p(lf)+(i*0.5+1)*DOWN, nl.n2p(mid)+(i*0.5+1)*DOWN)
            _line_r = interval_seg(nl.n2p(mid)+(i*0.5+1)*DOWN, nl.n2p(rt)+(i*0.5+1)*DOWN)
            self.play(Create(VGroup(_line_l, _line_r)), run_time=2*time)
            self.wait(time)
            if np.sqrt(2) > mid:
                self.play(Indicate(_line_r), run_time=time)
                self.play(L.animate.set_value(mid), run_time=time)
            else:
                self.play(Indicate(_line_l), run_time=time)
                self.play(R.animate.set_value(mid), run_time=time)
            seg_group.add(_line_l, _line_r)
            self.wait(time*2)


        somedots = MathTex(r"\cdots", color=WHITE).move_to(nl.n2p(np.sqrt(2))+4*DOWN)
        seg_group.add(somedots)
        self.play(Write(somedots))
        self.wait(6)
        
        # 从此之后，希望各位理解的小伙伴眼里，当你看到一个实数的时候
        # 脑海中的概念不应该是一个“点”，一个不言自明的、位置任意精确的点
        # 而应该是有一个逐渐缩小、无限精确定位的过程，是这个过程“定义”了数
        self.play(Indicate(seg_group), run_time=2)
        rect = SurroundingRectangle(seg_group)
        self.wait()
        self.play(Create(rect), run_time=2)
        self.wait(2)
        
class SolveQuestion(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        nl = NumberLine(
            x_range=[-0.3, 1.2, 0.2],
            length=8,
            color=GREEN,
            include_numbers=True,
            include_tip=True,
            label_direction=DOWN,
        ).shift(UP*1.5)
        self.wait(2)
        self.play(DrawBorderThenFill(nl), run_time=2)

        
        # sqrt2_in = always_redraw( lambda:
        #     MathTex(f"\\sqrt{2}\\in[{L.get_value():.3f}, {R.get_value():.3f})", color=BLUE).shift(LEFT*4)
        # )
        # self.play(Write(sqrt2_in))
        number = MathTex("0.","9","9","9",r"\cdots", color=RED).shift(UP*3)
        #self.play(Write(number[0]))
        x = 0

        seg_group = VGroup()
        for i in range(1,5):
            time = 1 
            
            _seg = interval_seg(nl.n2p(x)+(1+i*0.8)*DOWN, nl.n2p(1)+(1+i*0.8)*DOWN, BLUE)
            seg_group.add(_seg)
            self.play(Create(_seg), Write(number[i-1]), run_time=time)
            self.wait(time*2)
            x = (x+9) / 10

        somedots = MathTex(r"\cdots", color=YELLOW).move_to(nl.n2p(1)+5*DOWN)
        seg_group.add(somedots)
        self.play(Write(somedots), Write(number[4]))
        self.wait(3)
        rect = SurroundingRectangle(seg_group)
        self.play(Create(rect), run_time=2)
        self.wait(2)

        x = ValueTracker(0.)
        arr = always_redraw(
            lambda: Arrow(nl.n2p(x.get_value())+0.4*UP, nl.n2p(x.get_value()),
                          color=YELLOW, stroke_width=1)
        )
        value = always_redraw(
            lambda: DecimalNumber(x.get_value(), 4).set_color(BLUE).next_to(arr, UP, buff=0.1)
        )
        self.play(Create(arr), Create(value), run_time=2)
        self.play(x.animate.set_value(1.), rate_func=slow_into, 
                  run_time=8)
        self.wait(3) 
        self.play(Circumscribe(value))
        self.wait(5)

class ProcedureAndLimit(MovingCameraScene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        aa = MathTex(r"\lim_{x\to 0} \frac{\sin x}{x}=1", color=BLUE).shift(UP)
        bb = MathTex(r"\lim_{n\to \infty} \left(1+\frac{1}{n}\right)^n=e", color=GREEN).shift(DOWN)
        self.wait(2)
        self.play(DrawBorderThenFill(aa), run_time=3)
        self.wait(2)
        self.play(DrawBorderThenFill(bb), run_time=3)
        self.wait(3)

class InfiniteDescent(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        
