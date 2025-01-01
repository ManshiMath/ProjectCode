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

class Cut(Scene):
    def construct(self):

        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        self.wait()
        # 设想你有一根一米长的棍子，
        seg = Line(LEFT*3, RIGHT*3, stroke_width=10, color='GOLD')
        length = MathTex("1").set_color(GOLD).next_to(seg, RIGHT+DOWN)
        self.play(Create(VGroup(seg, length)), run_time=2)

        # 随便挑一个位置，把它锯成两截。
        self.wait()
        ax = ValueTracker(0.1)
        arr = always_redraw(
            lambda: Arrow(RIGHT*(-3+6*ax.get_value())+UP, RIGHT*(-3+6*ax.get_value()), buff=0.1).set_color(BLUE)
            )
        self.play(Create(arr))
        self.play(ax.animate.set_value(0.98), 
                  run_time=3,
                  rate_func=there_and_back)
        self.play(ax.animate.set_value(0.38), 
                  run_time=1,
                  rate_func=smooth)
        self.wait(1)

        cut_line = always_redraw(
            lambda: Line(LEFT*3, RIGHT*(-3+6*ax.get_value()))
        )
        # 左边这一节的长度以米为单位，究竟是一个有理数还是无理数呢？
        brace = always_redraw(
            lambda:Brace(Line(LEFT*3, RIGHT*(-3+6*ax.get_value())), DOWN, buff=SMALL_BUFF).set_color(GOLD)
        )
        t1 = always_redraw(
            lambda: MathTex("x").next_to(brace, DOWN, buff=0.1).set_color(YELLOW)
        )
        ratioq = MathTex(r"\in\mathbb{Q}?", color=YELLOW).next_to(t1, RIGHT, buff=0.1)

        self.play(FadeIn(brace),
                  Write(t1),
                  run_time=2)
        self.wait()
        self.play(Write(ratioq), run_time=2)
        self.wait()
        self.play(FadeOut(ratioq))
        self.wait(2)
        # 答案可能会让你很吃惊，如果你是均匀随机地挑选这个锯开的位置，
        self.play(ax.animate.set_value(0.99),
                  run_time=3,
                  rate_func=there_and_back)

        self.wait(2)
        # 那么两段的长度是无理数的概率是1，是有理数的概率是0。
        note = MathTex(r"\mathbb{P}(x\in\mathbb{Q})=0", color=BLUE).shift(2*DOWN)
        note2 = MathTex(r"\mathbb{P}(x\not\in\mathbb{Q})=1", color=RED).next_to(note, DOWN, buff=0.2)
        self.play(
            Write(note),
            Write(note2),
            run_time=3,
            lag_ratio=0.5
        )
        self.wait()
        # 换句话说，这两段的长度几乎一定都是无理数。
        self.play(Circumscribe(VGroup(note, note2)))
        self.wait(2)

# class HilbertHotel(object):
#     def __init__(self):
#         pass

class MonteCarlo(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        # 这个问题棘手和困难的地方在于，它不像我们以前做过的几何概型的问题那样有容易计算的“面积比例”，
        self.wait(2)
        square = Square(side_length=4.0, fill_color=BLUE).set_opacity(0.5).shift(UP)
        circ = Circle(radius=2.0, fill_color=RED_A).set_opacity(0.8).move_to(square)
        self.play(Create(VGroup(square, circ)), run_time=2)
        self.wait(2)

        # Random sample x and y, draw dashed lines to locate the point.
        # Illustrate the x length and y length, then draw the point.
        x = 0.7
        y = 0.3
        square_origin = UP
        right_dir = RIGHT * 2
        up_dir = UP * 2
        x_line = DashedLine(square_origin, square_origin + x * right_dir, color = ORANGE, stroke_width=4)
        y_line = DashedLine(square_origin + x * right_dir, square_origin + x * right_dir + y * up_dir, color=ORANGE, stroke_width=4)
        x_note = MathTex("x", color=YELLOW).scale(0.6).next_to(x_line, DOWN, buff=0.1)
        y_note = MathTex("y", color=YELLOW).scale(0.6).next_to(y_line, RIGHT, buff=0.1)
        self.play(Create(x_line), Create(x_note), run_time=0.5)
        self.wait(0.5)
        self.play(Write(y_line), Write(y_note), run_time=0.5)
        self.wait(1)
        
        pt = Dot().scale(0.5).move_to(square_origin + x * right_dir + y * up_dir)
        self.play(Create(pt), run_time=1)
        self.wait(2)
        self.play(FadeOut(x_line), FadeOut(y_line), FadeOut(x_note), FadeOut(y_note), run_time=1)    

        # 比如，在这个正方形里随机投一个点，落在这个圆里的概率概率正比于面积，
        self.wait(2)
        description = MathTex(r"\mathbb{P}(\cdot\in\text{ Circle})=\frac{S_{\text{Circle}}}{S_{\text{Square}}}}=\frac{\pi}{4}", 
                              color=YELLOW).shift(2*DOWN)

        # 所以用圆的面积比上正方形的面积，你就得到了π/4这个结果。
        # scale down and shift up the square+circle and write the description at the same time
        self.play(
            Write(description),
            run_time=4
        )
        self.wait(2)
        self.play(Circumscribe(description))
        self.wait(2)
        self.play(FadeOut(description), FadeOut(pt))
        self.wait(3)

        # 事实上，这个方法还可以用于估算圆周率，
        # 我们用计算机采样出1000个点，
        pt_list = []
        np.random.seed(233)
        for i in range(1000):
            pt_list.append(np.random.uniform(-1, 1, 2))
        point_list = VGroup(*[Dot().scale(0.2).move_to(point[0]*RIGHT*2 + point[1]*UP*2+UP) for point in pt_list])


        # Transform all the points within the circle to red
        change_color = []
        cnt = 0
        for i in range(len(point_list)):
            if pt_list[i][0]**2 + pt_list[i][1]**2 <= 1:
                change_color.append(point_list[i])
                cnt += 1
        # Set up a counting animation, synchronize with the color change
        count = ValueTracker(0)
        number = always_redraw(
            lambda: MathTex(str(int(count.get_value())), color=BLUE).shift(4*LEFT)
        )

        # Add updater to the points within the circle, change color to red when count.value is greater than its index among change_list
        # So that each point will change color at the same time as the counting animation
        for point in change_color:
            idx = change_color.index(point)
            point.add_updater(
                lambda p, idx=idx: p.set_color(YELLOW) if count.get_value() >= idx else p.set_color(WHITE)
            )

        # 每次均匀采样横坐标和纵坐标，得到一个随机的点，
        # 统计落在圆里的点的比例，再乘以4，就得到了π的一个近似值，
        self.play(Create(point_list), run_time=2)
        self.play(Write(number))
        
        # Play the counting animation
        self.play(count.animate.set_value(cnt), run_time=3)
                    
        self.wait(2)
        # 看看，是不是还挺接近的？
        fraction = MathTex(r"4\times\frac{"+str(cnt)+"}{1000}", r"=", str(4*cnt/1000), r"\approx", r"\pi", color=BLUE).shift(2*DOWN)
        self.play(Write(fraction[:-2]), run_time=2)
        self.wait(2)
        self.play(Write(fraction[-2:]), run_time=2)
        self.wait(2)
        self.play(FadeOut(number))
        # 不过这个方法用于计算圆周率的第n位效率不高，
        # 就算随机扔一万个点，也算不明白小数点后第三位。
        
        cnt = 0
        for i in range(100000):
            x = np.random.uniform(-1, 1, 2)
            if x[0]**2 + x[1]**2 <= 1:
                cnt += 1
        ratio = MathTex(r"4\times\frac{"+str(cnt)+"}{100000}", r"=", str(4*cnt/100000), color=BLUE).shift(2*DOWN)
        self.play(ReplacementTransform(fraction, ratio), run_time=2)
        self.wait(2)
        

        # 但这个方法的好处是，简单粗暴，
        # 只需要每次随机两个坐标，用距离公式看看在不在圆里，
        self.play(*[Indicate(point) for point in change_color])
        # 然后统计一下在圆内外的比例就行，完全不需要复杂的数学知识。
        rect = SurroundingRectangle(ratio[0], color=YELLOW)
        self.play(Create(rect))
        self.wait(2)
        self.play(FadeOut(rect))
        self.wait(2)
        # 这种简单粗暴的方法，就是计算机科学里经典的“蒙特卡洛算法”。
        name = Text("蒙特卡洛算法", color=YELLOW).scale(1.5).shift(DOWN*2.5)
        self.play(FadeOut(ratio))
        self.play(DrawBorderThenFill(name), run_time=2)
        self.wait(2)
        self.play(FadeOut(name))
        self.wait()
        # 那么，我们可不可以用蒙特卡洛算法来模拟切棍子的过程，计算被切成两段的棍子是有理数的概率呢？
        # Draw an number line, add a stick, and a random arrow point to the stick
        number_line = NumberLine(x_range=[-0.4, 1.4, 0.2], length=12, include_numbers=True, include_tip=True, color=BLUE).shift(DOWN*2.5)
        stick = Line(number_line.n2p(0), number_line.n2p(1), color=YELLOW, stroke_width=10).shift(DOWN*0.1)
        x_pos = ValueTracker(0.5)
        arrow = always_redraw(
            lambda: Arrow(number_line.n2p(x_pos.get_value())+UP, number_line.n2p(x_pos.get_value()), color=ORANGE, buff=0.1)
        )
        self.play(Create(number_line), Create(stick), Create(arrow), run_time=2)
        self.wait()
        self.play(x_pos.animate.set_value(0.1),
                    run_time=2,
                    rate_func=smooth)
        self.play(x_pos.animate.set_value((np.sqrt(5)-1)/2),
                    run_time=3,
                    rate_func=smooth)
        self.wait(2)
        # 仔细想想你会发现，似乎不太行。
        # 在刚才计算π的例子里，某一个点在圆内还是外，不需要特别高的精度，
        ptx = ValueTracker(0.2163)
        pty = ValueTracker(-0.7498)
        pt =  Dot().scale(0.5).add_updater(
            lambda p: p.move_to(square_origin + ptx.get_value() * right_dir + pty.get_value() * up_dir)
        )
        
        self.play(Create(pt), run_time=1)
        xy_label = always_redraw(
            lambda: MathTex(str(round(ptx.get_value(), 4))+','+str(round(pty.get_value(), 4)), 
            color=ORANGE).scale(0.7).add_background_rectangle().next_to(pt, UP, buff=0.1)
        )

        self.wait()
        # Illustrate pt's two coordinates
        self.play(Write(xy_label), run_time=1)
        self.wait()

        # 你只需要大概取小数点后四五位，足以判断这个点在圆内还是圆外就行。
        self.play(Circumscribe(xy_label), run_time=1)
        # 可是，判断是不是有理数，一个重要的前提条件就是具有无限精度，
        # illustrate the x_pos's decimal value, with arbitrary precision gradually expanding
        self.wait(3)
        precision = ValueTracker(1.)
        x_pos_label = always_redraw(
            lambda: MathTex(str(round(x_pos.get_value(), int(precision.get_value()))),
            color=ORANGE).next_to(arrow, RIGHT, buff=0.1)
        )
        self.play(Write(x_pos_label), run_time=1)
        self.wait()
        self.play(precision.animate.set_value(8),  
                    run_time=4,
                    rate_func=linear)
        self.wait(4)

        # 如果你采样的x是有限位的小数，那么一定都是有理数，而这并不是我们的初衷。
        # indicate the finite precision of x_pos
        self.play(Indicate(x_pos_label), run_time=1)
        self.wait(3)

        dots = MathTex(r"\dots", color=ORANGE).scale(0.7).add_updater(
            lambda m: m.next_to(x_pos_label, RIGHT, buff=0.1))
        self.play(Write(dots), run_time=2)
        self.wait(7)

        # 再仔细想想你会意识到，归根结底是因为有理数在数轴上的分布实在是有些奇葩，
        # 它无处不在、又极其稠密，如果不同时写出小数点后的无数多位，你无法分辨一个数字到底是不是有理数。
        # draw some rational numbers on the number line with small vertical lines
        # the length of the line is inverse proportional to the denominator
        rational_list = []
        rational_lines = VGroup()
        for denominator in range(1, 50):
            for numerator in range(1, denominator):
                # judge whether the numerator and denominator are coprime
                if math.gcd(numerator, denominator) == 1:
                    rational_list.append(numerator/denominator)
                    rational_lines.add(Line(number_line.n2p(numerator/denominator), 
                                            number_line.n2p(numerator/denominator)+UP*1.8/denominator+UP*0.1, 
                                            stroke_width=1,
                                            color=BLUE))

        self.play(Create(rational_lines), run_time=4, lag_ratio=0.5)
        self.wait(2)

        # 你下刀的位置稍微偏移一点点，这根棍子的长度就在有理数和无理数之间来回跳跃了无数回。
        self.play(x_pos.animate.set_value(np.sqrt(5)/2-1/2+0.02),
                    run_time=3,
                    rate_func=smooth)
        # 真是让人头疼的问题，但别怕，这期视频严格的数学推导会告诉你：x是有理数的概率是0，是无理数的概率是1。
        # 只不过，在开始我们的推导之前，需要先介绍一个非常重要又非常有趣的基础概念，那就是：可数无穷。
        self.wait(2)
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.wait()
        countable_inf = Text("可数无穷", color=YELLOW).scale(2)
        self.play(DrawBorderThenFill(countable_inf), run_time=2)
        self.wait(2)
        self.play(FadeOut(countable_inf))
        # 它看起来和我们要讨论的主题很远，但其实息息相关。
        # self.play(
        #     *[FadeOut(mob)for mob in self.mobjects]
        # )

class Hotel(ThreeDScene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\man-sill.svg")
        room = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\room.svg")

        # 所谓的“可数无穷”，顾名思义，就是可以一个个数出来的无穷大。
        # 如果我们可以给集合里每个元素一个正整数编号，不重不漏、唯一对应，就像身份证一样，
        # Create a list of man, and give each of them a number
        man_list = VGroup()
        for i in range(30):
            man_list.add(man.copy().set_color(LIGHT_BROWN).scale(0.6).shift(LEFT*5+i*RIGHT))
        self.play(Create(man_list),run_time=2)
        self.wait()
        man_label = VGroup()
        for i in range(30):
            man_label.add(MathTex(str(i+1), color=YELLOW).scale(0.7).add_updater(
                lambda p, idx=i: p.next_to(man_list[idx], DOWN, buff=0.1))
            )
        self.play(
            Create(man_label), run_time=2
        )
        self.wait()
        self.move_camera(frame_center=15*RIGHT, run_time=7)
        self.wait()
        self.move_camera(frame_center=ORIGIN, run_time=2)
        self.wait(2)

        # 那么这个集合的元素数量就被称为“可数无穷”。
        keshu_note = Text("可数无穷", color=YELLOW).scale(2).shift(UP*2.5)
        count_inf = MathTex(r"\aleph_0", color=BLUE).scale(3).shift(UP*2.5)
        self.play(
            Write(keshu_note),
            run_time=2
        )
        self.wait()
        self.play(
            ReplacementTransform(keshu_note, count_inf),
            run_time=2
        )
        self.wait(5)
        # 可数无穷有一个神秘的记号，叫做阿列夫0。
        # 阿列夫是希伯来语的第一个字母，它的发音和符号形状都给人一种神秘神圣的感觉，
        # 打音游的人或许对它并不陌生。（插入阿列夫0的动画）
        # 你可能会好奇，这里的0是什么意思，不要急，后面会告诉你。
        # 有一个形象的比喻可以帮你理解这件事，它被称作“希尔伯特的旅馆”。
        # shift down the man and label
        self.play(
            *[man.animate.shift(DOWN*2) for man in man_list],
            FadeOut(count_inf),
            run_time=2
        )

        self.wait()

        def create_room(i):
            return room.copy().scale(0.6).set_opacity(1-i/40).shift(LEFT*6+i*1.5*RIGHT)
        
        HT = VGroup()
        for i in range(40):
            HT.add(create_room(i))
        
        title = Text("Hilbert's Hotel", color=ORANGE).scale(1.5).shift(UP*2.5)

        self.play(DrawBorderThenFill(title), run_time=1)
        self.play(Create(HT), FadeOut(man_list), FadeOut(man_label),
                  run_time=2, lag_ratio=0.5)
        self.wait()
        self.play(FadeOut(title))
        self.move_camera(phi=DEGREES*60, theta=-180*DEGREES, gamma=-90*DEGREES, run_time=3)
        self.wait(2)
        # Indicate every room fastly
        self.play(
            LaggedStart(*[Indicate(room) for room in HT], lag_ratio=0.5),
            run_time=3
        )
        self.move_camera(phi=0, theta=0, gamma=90*DEGREES, run_time=3)
        self.wait(2)
        # 你可以把每个正整数编号看成一个房间号，
        # Add room number to each room at top
        room_num = VGroup()
        for i in range(40):
            room_num.add(MathTex(str(int(i+1)), color=ORANGE).scale(1.2).next_to(HT[i], UP, buff=0.1))
        self.play(Write(room_num), run_time=2)
        self.wait(2)
        # 把一个无穷集合的每个元素，比如说数字当成客人，
        # 某个客人住进了某个房间，就代表我们给这个元素以这个房间号码的编号。
        self.play(
            FadeIn(man_list),
            Create(man_label)
        )
        self.wait(2)
        # move man i to room i one by one
        for i in range(10):
            self.play(
                man_list[i].animate.move_to(HT[i].get_center()),
                run_time=0.5
            )
        self.play(
            *[man_list[i].animate.move_to(HT[i].get_center()) for i in range(10, 30)],
            run_time=2
        )
        
        self.wait(2)

        # 给客人安排房间的过程，本质上就是数学构建这个集合的元素和正整数一一对应的映射关系的过程。
        # Indicate man 3 and room 3, show the mapping
        rect1 = SurroundingRectangle(man_label[2], color=YELLOW)
        rect2 = SurroundingRectangle(room_num[2], color=YELLOW)
        self.wait(2)
        self.play(Create(rect1), Create(rect2), run_time=1)
        self.wait(2)
        self.play(FadeOut(rect1), FadeOut(rect2), run_time=1)
        self.wait(2)

        # 希尔伯特的旅馆最奇特的地方在于，它有无穷无尽数量的房间，
        # 它使得我们可以做一些不可思议的事情。
        # 比如一开始，每个数字都住在等于房间号的房间里。
        self.play(
            *[Indicate(label) for label in room_num],
        )
        self.play(
            *[Indicate(label) for label in man_label]
        )
        self.wait(2)
        # 此时又来了一个0，
        newman = man.copy().set_color(LIGHT_BROWN).scale(0.6).shift(DOWN * 2.5)
        newman_label = MathTex("0", color=YELLOW).scale(0.7).add_updater(
            lambda p: p.next_to(newman, DOWN, buff=0.1)
        )
        self.play(
            Create(newman),
            Create(newman_label),
            run_time=2
        )
        self.wait(2)
        
        # 我们让每个客人都搬到右边隔壁的房间里，于是就空出了1号房。
        self.play(
            *[man.animate.shift(DOWN*0.8) for man in man_list],
        )
        self.wait(2)
    
        # move man i to room i+1 one by one
        self.play(
            LaggedStart(
                *[ApplyMethod(man_list[i].move_to, HT[i+1].get_center()) for i in range(10)],
                lag_ratio=0.5,
            ),
            run_time=4
        )
        self.play(
            *[man_list[i].animate.move_to(HT[i+1].get_center()) for i in range(10, 30)],
            run_time=2
        )
        self.wait(2)
        self.play(Circumscribe(room_num[0], color=YELLOW), run_time=1)
        self.wait()

        # 这时候，我们就可以把新来的0安排到1号房间里。
        self.play(
            newman.animate.move_to(HT[0].get_center()),
            run_time=2
        )
        self.wait(3)

        # 于是，我们在这里就回答了一个经典的小学数学的未解难题：无穷大加一等于多少，
        question = MathTex(r"\infty", "+1","=", "?", color=BLUE).scale(2).shift(UP*2.5)
        self.play(
            Write(question),
            run_time=2
        )
        # 答案就是，依然是无穷本身。
        self.wait(5)
        answer = MathTex(r"\infty", color=BLUE).scale(2).next_to(question[2], RIGHT, buff=0.1)
        self.play(
            Transform(question[3], answer),
            run_time=2
        )
        # 更准确地说，这里的无穷符号应该写成可数无穷。
        self.wait(3)
        aleph0_1 = MathTex(r"\aleph_0", color=BLUE).scale(2).move_to(question[0])
        aleph0_2 = MathTex(r"\aleph_0", color=BLUE).scale(2).move_to(answer)
        self.play(
            Transform(question[0], aleph0_1),
            Transform(question[3], aleph0_2),
            run_time=2
        )
        # 你可以立刻想到，这套办法可以应用于任何有限的整数k，

        # Add 3 new people without label, move everyone to the right by 3 room
        # Then assign the 3 new people to room 1, 2, 3
        three_newman = VGroup()
        for i in range(3):
            three_newman.add(man.copy().set_color(LIGHT_BROWN).scale(0.6).shift(DOWN * 2.5 + i*RIGHT))
        self.wait(2)
        self.play(Create(three_newman), run_time=2)
        self.wait(3)
        self.play(*[man.animate.shift(DOWN*0.8) for man in man_list],
                  newman.animate.shift(DOWN*0.8),
                   run_time=1)
        self.wait()
        self.play(*[man.animate.shift(RIGHT*3) for man in man_list],
                  newman.animate.shift(RIGHT*3),
                   run_time=1)
        # 如果来了k个新的需要入住的客人，那么只需要把所有人往右搬k个房间，
        # 就能空出足够多的空房间。
        self.play(ApplyMethod(newman.move_to, HT[3].get_center()), run_time=0.3)
        self.play(
            LaggedStart(
                *[ ApplyMethod(man_list[i].move_to, HT[i+4].get_center()) for i in range(10)],
                lag_ratio=0.5,
            ),
            run_time=2
        )
        self.play(
            *[man_list[i].animate.move_to(HT[i+4].get_center()) for i in range(10, 30)],
            run_time=1
        )
        self.wait(2)
        self.play(
            *[three_newman[i].animate.move_to(HT[i].get_center()) for i in range(3)],
            run_time=2
        )
        self.wait(2)

        # 换言之，阿列夫0加k等于阿列夫0自身。
        plusk = MathTex("+k", color=BLUE).scale(2).move_to(question[1])
        self.play(
            Transform(question[1], plusk),
            run_time=2
        )
        self.wait(2)

        # Remove the 3 new people, Restore man_list's original position
        self.play(
            *[FadeOut(man) for man in three_newman],
            FadeOut(newman), FadeOut(newman_label),
            FadeOut(question),
        )
        self.wait(2)
        self.play(
            LaggedStart(*[man_list[i].animate.move_to(HT[i].get_center()) for i in range(0, 10)], lag_ratio=0.5),
            run_time=4
        )

        # 让我们做的更多一些，如果现在突然来了可数无穷多个客人，
        # 比如说，0和所有负整数都来了，希尔伯特的旅馆还能让他们都住下来吗？
        # Create 15 new people, name them as 0, -1, -2, ..., -14
        fifteen_newman = VGroup()
        fifteen_newlabel = VGroup()
        for i in range(15):
            fifteen_newman.add(
                man.copy().set_color(LIGHT_BROWN).scale(0.6).shift(DOWN * 2.5 + 6 * LEFT+ i * RIGHT)
            )
            fifteen_newlabel.add(
                MathTex(str(-i), color=YELLOW).scale(0.7).add_updater(
                    lambda p, idx=i: p.next_to(fifteen_newman[idx], DOWN, buff=0.1)
                )
            )
        self.play(Create(fifteen_newman), lag_ratio=0.5, run_time=4)
        self.play(Write(fifteen_newlabel), lag_ratio=0.5, run_time=2)
        # 如果你想自己思考，不妨暂停视频试一试。（停顿3秒）
        self.wait(3)
        self.play(
            *[man.animate.shift(DOWN*0.8) for man in man_list],
        )
        self.wait(2)
    
        # 其实，我们可以这么做，我们让每个客人都搬到原来房间号乘以2的房间里，
        # move man i to room 2*i one by one
        self.play(
            LaggedStart(
                *[ApplyMethod(man_list[i].move_to, HT[2*i+1].get_center()) for i in range(15)],
                lag_ratio=0.5,
            ),
            run_time=3
        )
        # 比如1搬到2, 2搬到4，这样，所有的奇数号房间就都空了出来，它们一共有可数无穷多个，
        self.wait(2)
        # 每个新来的整数住进奇数号房间，我们于是给每一个整数找到了一个正整数编号的房间。
        self.play(
            LaggedStart(
                *[ApplyMethod(fifteen_newman[i].move_to, HT[2*i].get_center()) for i in range(5)],
                lag_ratio=0.5,
            ),
            run_time=5
        )
        self.play(
            *[ApplyMethod(fifteen_newman[i].move_to, HT[2*i].get_center()) for i in range(5, 15)],
            run_time=5
        )
        self.wait(2)
        # 我们来仔细品味一下这意味着什么，一开始有aleph0这么多个客人，然后又来了aleph0多个客人，
        equation = MathTex(r"\aleph_0", "+", r"\aleph_0", "=", r"\aleph_0", color=ORANGE).scale(2).shift(UP*2.5)
        self.play(Write(equation[0]), run_time=2)
        self.wait(2)
        self.play(Write(equation[1:3]), run_time=1)
        self.wait()
        
        # 最后我们用aleph0个房间把他们都放了进去，实现了每人唯一对应一个房间。
        # Indicate each person and his room's mapping
        for i in range(10):
            if i % 2 == 0:
                self.play(Indicate(room_num[i]),
                          Indicate(fifteen_newman[i//2]), run_time=0.4)
            else:
                self.play(Indicate(room_num[i]),
                          Indicate(man_list[i//2]), run_time=0.4)
            self.wait(0.1)
        self.wait()
        # 这意味着，可数无穷加可数无穷，还是可数无穷。
        self.play(Write(equation[3:]), run_time=1)
        self.wait(2)
        # 从这里开始，第一个令人费解的事情出现了：我们得到了这么一个等式，
        # 2*aleph0=aleph0，如果不知道是可数无穷的意思，你可能会解方程得到aleph0=0。
        eq2 = MathTex(r"2\times\aleph_0", "=", r"\aleph_0", color=BLUE).scale(2).shift(UP*2.5)
        self.play(Transform(equation, eq2), run_time=2)
        self.wait(2)
        eq_zero = MathTex(r"\aleph_0", "=", "0", color=ORANGE).scale(1.5).next_to(eq2, RIGHT, buff=0.1)
        self.play(Write(eq_zero), run_time=2)
        # 但这肯定是荒谬的，一个无穷多的数量怎么会等于0呢？
        rect = SurroundingRectangle(eq_zero, color=YELLOW)
        self.play(Create(rect), run_time=1)
        question_mark = MathTex("?", color=RED).scale(3).move_to(eq_zero)
        self.play(Write(question_mark), run_time=2)
        self.wait(2)

        # 这个现象还有另一个广为流传的版本：到底是正整数多还是整数多？
        which_is_larger = Text("正整数和整数哪个多？", color=ORANGE).scale(2).shift(DOWN*2.5)
        self.play(Write(which_is_larger), run_time=2)
        self.wait(5)
        # 看起来，整数完全包含了正整数，而且还剩下了一半的负整数，整数明明应该更多才对，
        # 更准确地说，感觉多了整整一倍。
        # 可是，我们刚才的安排已经证明了，可以在正整数和所有整数之间建立一一对应，一个客人一个房间，所以正整数和整数应该是一样多的。
        for i in range(10):
            if i % 2 == 0:
                self.play(Indicate(room_num[i]),
                          Indicate(fifteen_newman[i//2]), run_time=0.3)
            else:
                self.play(Indicate(room_num[i]),
                          Indicate(man_list[i//2]), run_time=0.3)
        self.wait(8)

class WholevsPart(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\man-sill.svg")
        # 这听起来非常离谱，明明丢掉了整整一半，结果居然还是和原来一样多。
        # 为什么会这样？该怎么理解这件抽象的事情？
        # 很多讲无穷的视频都会提到希尔伯特的旅馆和上面这个整体等于部分的例子，
        # 但是除了吸引眼球之外，却很少有人说透它违反直觉的关键之处在哪里。
        # 事实上，理解这件事的关键，在于怎么理解数量的“相等”和“比大小”这件事。
        eq_text = Text("数量相等", color=YELLOW).scale(2).shift(UP*3)
        self.play(Write(eq_text), run_time=2)
        self.wait(5)
        # 来到无穷的世界，原来有限的数字比较已经失效，
        # 谁更多谁更少，更本质的标准是——配对，
        pairing_text = Text("一一配对", color=BLUE).scale(2).next_to(eq_text, DOWN, buff=0.5)
        self.play(Write(pairing_text), run_time=2)
        self.wait()
        # Resize two texts smaller and move to top left and right
        _eq_text = eq_text.copy().scale(0.5).move_to(ORIGIN+UP*3+LEFT*3)
        _pairing_text = pairing_text.copy().scale(0.5).move_to(ORIGIN+UP*3+RIGHT*3)
        self.play(Transform(eq_text, _eq_text), Transform(pairing_text, _pairing_text))
        self.wait(2)
        # 你可以理解成两伙人打群架，一个个1v1，哪边配对之后还能有剩下多余的人手，哪边人就更多。
        # Create a group of 5 red men and 3 blue men
        red_men = VGroup()
        for i in range(5):
            red_men.add(man.copy().scale(0.8).set_color(RED).shift(UP + LEFT*2 + RIGHT*i))
        
        blue_men = VGroup()
        for i in range(3):
            blue_men.add(man.copy().scale(0.8).set_color(BLUE).shift(DOWN + LEFT + RIGHT*i))

        self.play(Create(red_men), run_time=3, lag_ratio=0.3)
        self.wait()
        self.play(Create(blue_men), run_time=2, lag_ratio=0.3)
        self.wait(2)
        # Draw three matching lines between the two groups
        lines = VGroup()
        for i in range(3):
            lines.add(Line(red_men[i+1].get_center(), blue_men[i].get_center(), color=WHITE))
        
        self.play(Create(lines), run_time=3, lag_ratio=0.3)
        self.wait(2)
        # 我们之所以觉得整体大于部分，归根结底，还是因为我们世界里的一切都是有限的。
        self.play(FadeOut(lines), FadeOut(blue_men))
        self.wait(2)
        # Copy transform a subset of redmen to the bottom
        subset = VGroup()
        for i in range(3):
            subset.add(red_men[i].copy().set_color(RED_B).shift(DOWN*2))

        self.play(
            LaggedStart(
                *[TransformFromCopy(red_men[i], subset[i]) for i in range(3)],
            ),
            run_time=2, lag_ratio=0.3
        )
        self.wait()
        # 因为数量有限，所以一一配对的话，部分【一定】不能匹配上整体的全部，
        pairing_rects = VGroup()
        for i in range(3):
            pairing_rects.add(SurroundingRectangle(VGroup(red_men[i], subset[i]), color=YELLOW))
        self.play(
            LaggedStart(
                *[Create(pairing_rects[i]) for i in range(3)],
            ),
            run_time=2, lag_ratio=0.3
        )        
        self.wait()

        # Enlarge the rest two and change color to yellow
        tsfm_rest2 = VGroup()
        for i in range(3, 5):
            tsfm_rest2.add(red_men[i].copy().scale(1.2).set_color(YELLOW))
        self.play(
            *[Transform(red_men[i], tsfm_rest2[i-3]) for i in range(3, 5)],
            run_time=2, lag_ratio=0.3)
        self.wait(2)
        # 所以我们习惯性形成“部分比整体更少”这种判断。
        # 整体比它的一部分要更多，并不是一个天然绝对正确的公理，
        self.wait(5)
        # 在无穷的世界里，这种习惯失效了，我们必须重回“一一配对”这种逻辑上更本质的定义，才能够考察两个无穷，究竟谁多谁少。
        rect = SurroundingRectangle(pairing_text, color=YELLOW)
        self.play(Create(rect), run_time=2)
        self.wait(2)

class CountableRational(Scene):
 

    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait()

        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\man-sill.svg")
        room = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\room.svg")
        def create_room(i):
            return room.copy().scale(0.6).set_opacity(1-i/40).shift(LEFT*6+i*1.2*RIGHT + UP*2)
        
        HT = VGroup()
        for i in range(40):
            HT.add(create_room(i))
        self.play(Create(HT), run_time=2)
        room_num = VGroup()
        for i in range(40):
            room_num.add(MathTex(str(int(i+1)), color=ORANGE).scale(1.2).next_to(HT[i], UP, buff=0.1))
        self.play(Write(room_num), run_time=2)
        self.wait(4)
        # 话说回来，现在让我们考虑一个更疯狂一些
        # 的问题：假如现在来了可数无穷多辆大巴车，每个大巴车上有可数无穷多个游客。

        # Create four list of men, each of 20 people. Each group has different colors.
        man_list1 = VGroup()
        for i in range(15):
            man_list1.add(man.copy().set_color(LIGHT_BROWN).scale(0.4).shift(LEFT*5+i*RIGHT+0.5*UP))
        man_list2 = VGroup()
        for i in range(15):
            man_list2.add(man.copy().set_color(GOLD).scale(0.4).shift(LEFT*5+i*RIGHT+0.7*DOWN))
        man_list3 = VGroup()
        for i in range(15):
            man_list3.add(man.copy().set_color(GREEN).scale(0.4).shift(LEFT*5+i*RIGHT+1.9*DOWN))
        man_list4 = VGroup()
        for i in range(15):
            man_list4.add(man.copy().set_color(MAROON).scale(0.4).shift(LEFT*5+i*RIGHT+3.1*DOWN))
        man_list5 = VGroup()
        for i in range(15):
            man_list5.add(man.copy().set_color(PURPLE).scale(0.4).shift(LEFT*5+i*RIGHT+4.3*DOWN))
        
        self.play(
            LaggedStart(
                *[Create(manlist) for manlist in [man_list1, man_list2, man_list3, man_list4, man_list5]]
            ),
            run_time=8, lag_ratio=0.3
        )
        self.wait(3)

        # 方便起见，我们用(a,b)这样的形式来表示第a辆大巴车上编号为b的游客，a和b可以为任意正整数。
        # Add labels to each one in each group.
        label_list1 = VGroup()
        for i in range(15):
            label_list1.add(MathTex(f"(1,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list1[idx].get_bottom()+0.1*DOWN))
            )
        label_list2 = VGroup()
        for i in range(15):
            label_list2.add(MathTex(f"(2,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list2[idx].get_bottom()+0.1*DOWN))
            )
        label_list3 = VGroup()
        for i in range(15):
            label_list3.add(MathTex(f"(3,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list3[idx].get_bottom()+0.1*DOWN))
            )
        label_list4 = VGroup()
        for i in range(15):
            label_list4.add(MathTex(f"(4,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list4[idx].get_bottom()+0.1*DOWN))
            )
        label_list5 = VGroup()
        for i in range(15):
            label_list5.add(MathTex(f"(5,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list5[idx].get_bottom()+0.1*DOWN))
            )

        self.play(
            LaggedStart(
                *[Create(lblist) for lblist in [label_list1, label_list2, label_list3, label_list4, label_list5]]
            ),
            run_time=4, lag_ratio=0.3
        )
        self.wait(3)

        original_pos = [[],[],[],[],[]]
        for i in range(15):
            original_pos[0].append(man_list1[i].get_center())
            original_pos[1].append(man_list2[i].get_center())
            original_pos[2].append(man_list3[i].get_center())
            original_pos[3].append(man_list4[i].get_center())
            original_pos[4].append(man_list5[i].get_center())

        # 请问，希尔伯特的旅馆可以装进去这么多人吗？你可以暂停视频，想一想办法。
        # 出乎意料的是，答案是肯定的
        # 现在，让我们按照a+b的总和把乘客重新分组，比如a+b最小等于2，只有一个人，他单独是第一组。
        head = 0
        group1 = VGroup(man_list1[0])
        self.EnlargeIndicate(group1, pause_time=2)
        self.wait()
        # Put group1 into hotel, update the head.
        self.play(
            LaggedStart(
                *[group1[i].animate.move_to(HT[head+i]) for i in range(len(group1))],
                lag_ratio=0.3
            ), run_time=2
        )
        head += len(group1)
        self.wait(2)

        group2 = VGroup(man_list1[1], man_list2[0])
        self.EnlargeIndicate(group2, pause_time=2)
        self.wait()
        # Put group2 into hotel, update the head.
        self.play(
            LaggedStart(
                *[group2[i].animate.move_to(HT[head+i]) for i in range(len(group2))],
                lag_ratio=0.5
            ), run_time=3
        )
        head += len(group2)
        self.wait()

        group3 = VGroup( man_list3[0], man_list2[1], man_list1[2])
        self.EnlargeIndicate(group3, pause_time=1, run_time=0.5)
        # Put group3 into hotel, update the head.
        self.play(
            LaggedStart(
                *[group3[i].animate.move_to(HT[head+i]) for i in range(len(group3))],
                lag_ratio=0.5
            ), run_time=1
        )
        head += len(group3)
        self.wait()  

        group4 = VGroup(man_list1[3], man_list2[2], man_list3[1], man_list4[0])
        self.EnlargeIndicate(group4, pause_time=1, run_time=0.5)
        self.wait()
        # Put group3 into hotel, update the head.
        self.play(
            LaggedStart(
                *[group4[i].animate.move_to(HT[head+i]) for i in range(len(group4))],
                lag_ratio=0.5
            ), run_time=1
        )
        head += len(group4)
        self.wait()        

        group5 = VGroup(man_list5[0], man_list4[1], man_list3[2], man_list2[3], man_list1[4])
        self.EnlargeIndicate(group5, pause_time=1, run_time=0.5)
        self.wait()
        # Put group5 into hotel, update the head.
        self.play(
            LaggedStart(
                *[group5[i].animate.move_to(HT[head+i]) for i in range(len(group5))],
                lag_ratio=0.5
            ), run_time=1.5
        )
        head += len(group5)
        self.wait(2)        

        # 这样，你就可以很直观地看出来，我们可以把所有的人都安排进旅馆里了。

        # Restore everyone to their original position.
        self.play(
            *[man_list1[i].animate.move_to(original_pos[0][i]) for i in range(5)],
            *[man_list2[i].animate.move_to(original_pos[1][i]) for i in range(4)],
            *[man_list3[i].animate.move_to(original_pos[2][i]) for i in range(3)],
            *[man_list4[i].animate.move_to(original_pos[3][i]) for i in range(2)],
            *[man_list5[i].animate.move_to(original_pos[4][i]) for i in range(1)],
            run_time=2
        )
        self.wait(2)
        # 这里最巧妙的地方在于，我们改变了原来按照大巴分组的方式，改成了斜线分组。
        self.play(
            Indicate(man_list1),
            run_time=1
        )
        self.wait()
        # Draw arrows in order [group1] -> [group2->...->] -> [group3->...->] -> [group4->...->] -> [group5->...->]
        arrow_list = VGroup()
        tail = group1[0]
        for i in range(len(group2)):
            arrow_list.add(Arrow(tail.get_center(), group2[i].get_center(), buff=0.1))
            tail = group2[i]
        for i in range(len(group3)):
            arrow_list.add(Arrow(tail.get_center(), group3[i].get_center(), buff=0.1))
            tail = group3[i]
        for i in range(len(group4)):
            arrow_list.add(Arrow(tail.get_center(), group4[i].get_center(), buff=0.1))
            tail = group4[i]
        for i in range(len(group5)):
            arrow_list.add(Arrow(tail.get_center(), group5[i].get_center(), buff=0.1))
            tail = group5[i]
        self.play(
            LaggedStart(
                *[Create(arrow) for arrow in arrow_list],
                lag_ratio=0.5
            ), run_time=4
        )

        # 这样子，每组的人数就从原来一辆大巴的可数无穷多变成了有限个，
        self.EnlargeIndicate(group1, pause_time=0.5, run_time=0.5)
        self.EnlargeIndicate(group2, pause_time=0.5, run_time=0.5)
        self.EnlargeIndicate(group3, pause_time=0.5, run_time=0.5)
        self.EnlargeIndicate(group4, pause_time=0.5, run_time=0.5)
        self.wait(2)
        self.play(FadeOut(arrow_list), run_time=1)
        # 如果按照大巴编号的顺序，第一辆大巴直接就把房间占满了，就没法继续安排。
        # Move group1 to hotel. Then move back
        self.play(
            LaggedStart(
                *[man_list1[i].animate.move_to(HT[i]) for i in range(len(man_list1))],
                lag_ratio=0.5
            ), run_time=3
        )
        self.wait()
        self.play(Indicate(room_num))
        self.wait(2)
        self.play(
            LaggedStart(
                *[man_list1[i].animate.move_to(original_pos[0][i]) for i in range(len(man_list1))],
                lag_ratio=0.5), run_time=2
        )
        self.wait(2)
        # 这个技巧，被称作康托三角形。
        cantor_text = Text("康托三角形", color=YELLOW).add_background_rectangle().scale(1.2).shift(UP*3)
        self.play(Create(arrow_list), Write(cantor_text), run_time=2)
        self.wait(2)
        self.play(FadeOut(cantor_text), run_time=1)
        self.wait(2)

        # 现在让我们仔细回味一下这个例子的启示。
        # Fadeout everything except text1 and text2.
        self.play(
            *[FadeOut(obj) for obj in self.mobjects if obj not in [text_1, text_2]],
            run_time=1
        )
        self.wait(2)

        # 我们又发现了一个新的神秘的等式，注意看，我们有aleph0辆大巴车，每辆大巴有apleh0个人，
        equation = MathTex(r"\aleph_0", r"\times", r"\aleph_0", r"=\aleph_0", color=BLUE).scale(2)
        self.play(Write(equation[0]), run_time=1)
        self.wait(2)
        self.play(Write(equation[1:3]), run_time=1)
        self.wait(2)
        self.play(Write(equation[3]), run_time=1)
        # 但最后我们一个个的全部安排到了希尔伯特旅馆的aleph0个房间里，
        # 因此我们得到了aleph0×aleph0=aleph0，可数无穷的平方还是无穷。
        self.wait(2)
        self.play(Circumscribe(equation), run_time=1)
        self.wait()
        self.play(FadeOut(equation))
        # 事实上你可以利用这个等式立刻得到，aleph0的任意有限整数次方，都是aleph0，
        # 至于原因呢，都在下面这个动画里了。
        a1 = MathTex(r"\aleph_0", r"\times", r"\aleph_0", r"\times", r"\aleph_0", r"\times", r"\aleph_0", color=BLUE).scale(3)
        a2 = MathTex(r"\aleph_0", r"\times", r"\aleph_0", r"\times", r"\aleph_0", color=BLUE).scale(3)
        a3 = MathTex(r"\aleph_0", r"\times", r"\aleph_0", color=BLUE).scale(3)
        a4 = MathTex(r"\aleph_0",  color=BLUE).scale(3)
        alist=[a1,a2,a3,a4]

        self.wait(2)
        self.play(Write(a1))
        for i in range(3):
            self.wait()
            self.play(ReplacementTransform(alist[i], alist[i+1]), run_time=1)
        self.wait()
        self.play(Circumscribe(a4))
        self.wait(2)
        
class RationalMeasure(Scene):
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
        self.wait()

        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\man-sill.svg")
        room = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project5_inf\room.svg")
        # def create_room(i):
        #     return room.copy().scale(0.6).set_opacity(1-i/40).shift(LEFT*6+i*1.2*RIGHT + UP*2)
        
        # HT = VGroup()
        # for i in range(40):
        #     HT.add(create_room(i))
        # self.play(Create(HT), run_time=2)
        # room_num = VGroup()
        # for i in range(40):
        #     room_num.add(MathTex(str(int(i+1)), color=ORANGE).scale(1.2).next_to(HT[i], UP, buff=0.1))
        # self.play(Write(room_num), run_time=2)
        
        # Create four list of men, each of 20 people. Each group has different colors.
        man_list1 = VGroup()
        for i in range(15):
            man_list1.add(man.copy().set_color(LIGHT_BROWN).scale(0.4).shift(LEFT*5+i*RIGHT+0.5*UP))
        man_list2 = VGroup()
        for i in range(15):
            man_list2.add(man.copy().set_color(GOLD).scale(0.4).shift(LEFT*5+i*RIGHT+0.7*DOWN))
        man_list3 = VGroup()
        for i in range(15):
            man_list3.add(man.copy().set_color(GREEN).scale(0.4).shift(LEFT*5+i*RIGHT+1.9*DOWN))
        man_list4 = VGroup()
        for i in range(15):
            man_list4.add(man.copy().set_color(MAROON).scale(0.4).shift(LEFT*5+i*RIGHT+3.1*DOWN))
        man_list5 = VGroup()
        for i in range(15):
            man_list5.add(man.copy().set_color(PURPLE).scale(0.4).shift(LEFT*5+i*RIGHT+4.3*DOWN))
        
        self.play(
            LaggedStart(
                *[Create(manlist) for manlist in [man_list1, man_list2, man_list3, man_list4, man_list5]]
            ),
            run_time=3, lag_ratio=0.3
        )
        self.wait(1)

        group1 = VGroup(man_list1[0])
        group2 = VGroup(man_list1[1], man_list2[0])
        group3 = VGroup(man_list3[0], man_list2[1], man_list1[2])
        group4 = VGroup(man_list1[3], man_list2[2], man_list3[1], man_list4[0])
        group5 = VGroup(man_list5[0], man_list4[1], man_list3[2], man_list2[3], man_list1[4])

        # 方便起见，我们用(a,b)这样的形式来表示第a辆大巴车上编号为b的游客，a和b可以为任意正整数。
        # Add labels to each one in each group.
        label_list1 = VGroup()
        for i in range(15):
            label_list1.add(MathTex(f"(1,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list1[idx].get_bottom()+0.1*DOWN))
            )
        label_list2 = VGroup()
        for i in range(15):
            label_list2.add(MathTex(f"(2,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list2[idx].get_bottom()+0.1*DOWN))
            )
        label_list3 = VGroup()
        for i in range(15):
            label_list3.add(MathTex(f"(3,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list3[idx].get_bottom()+0.1*DOWN))
            )
        label_list4 = VGroup()
        for i in range(15):
            label_list4.add(MathTex(f"(4,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list4[idx].get_bottom()+0.1*DOWN))
            )
        label_list5 = VGroup()
        for i in range(15):
            label_list5.add(MathTex(f"(5,{i+1})", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list5[idx].get_bottom()+0.1*DOWN))
            )

        _label_list1 = VGroup()
        for i in range(15):
            _label_list1.add(MathTex(f"1/{i+1}", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list1[idx].get_bottom()+0.1*DOWN))
            )
        _label_list2 = VGroup()
        for i in range(15):
            _label_list2.add(MathTex(f"2/{i+1}", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list2[idx].get_bottom()+0.1*DOWN))
            )
        _label_list3 = VGroup()
        for i in range(15):
            _label_list3.add(MathTex(f"3/{i+1}", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list3[idx].get_bottom()+0.1*DOWN))
            )
        _label_list4 = VGroup()
        for i in range(15):
            _label_list4.add(MathTex(f"4/{i+1}", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list4[idx].get_bottom()+0.1*DOWN))
            )
        _label_list5 = VGroup()
        for i in range(15):
            _label_list5.add(MathTex(f"5/{i+1}", color=YELLOW).scale(0.5).add_updater(
                lambda p, idx=i: p.move_to(man_list5[idx].get_bottom()+0.1*DOWN))
            )

        self.play(
            LaggedStart(
                *[Create(lblist) for lblist in [label_list1, label_list2, label_list3, label_list4, label_list5]]
            ),
            run_time=4, lag_ratio=0.3
        )
        self.wait(3)

        # 现在，让我们修改一下记号，把（a,b）改成a/b
        self.play(
            LaggedStart(
                *[ReplacementTransform(label_list1[i], _label_list1[i]) for i in range(15)]
            ),
            LaggedStart(
                *[ReplacementTransform(label_list2[i], _label_list2[i]) for i in range(15)]
            ),
            LaggedStart(
                *[ReplacementTransform(label_list3[i], _label_list3[i]) for i in range(15)]
            ),
            LaggedStart(
                *[ReplacementTransform(label_list4[i], _label_list4[i]) for i in range(15)]
            ),
            LaggedStart(
                *[ReplacementTransform(label_list5[i], _label_list5[i]) for i in range(15)]
            ),
            run_time=3, lag_ratio=0.3
        )
        
        # 你会惊奇的发现，这些游客的编号不就是所有的有理数的分数形式吗？
        # 于是，我们立刻得到一个重要的结论：那就是所有的有理数是有可数无穷多的，
        # Draw arrows in order [group1] -> [group2->...->] -> [group3->...->] -> [group4->...->] -> [group5->...->]
        arrow_list = VGroup()
        tail = group1[0]
        for i in range(len(group2)):
            arrow_list.add(Arrow(tail.get_center(), group2[i].get_center(), buff=0.1))
            tail = group2[i]
        for i in range(len(group3)):
            arrow_list.add(Arrow(tail.get_center(), group3[i].get_center(), buff=0.1))
            tail = group3[i]
        for i in range(len(group4)):
            arrow_list.add(Arrow(tail.get_center(), group4[i].get_center(), buff=0.1))
            tail = group4[i]
        for i in range(len(group5)):
            arrow_list.add(Arrow(tail.get_center(), group5[i].get_center(), buff=0.1))
            tail = group5[i]
        self.play(
            LaggedStart(
                *[Create(arrow) for arrow in arrow_list],
                lag_ratio=0.5
            ), run_time=4
        )
        self.wait(3)
        
        # 我们可以一个个的数出来每一个有理数……吗？
        # 还差一点，因为这里有很多重复的，比如1/2,2/4，3/6等等，它们都是1/2，所以我们只要数出1/2就可以了。
        # Indicate 1/2 and 2/4 and so on, then fade out the rest
        self.EnlargeIndicate([man_list1[1], man_list2[3], man_list3[5], man_list4[7], man_list5[9]], scale_factor=1.2, pause_time=1, run_time=1)
        self.wait()
        self.play(FadeOut(VGroup(man_list2[3], man_list3[5], man_list4[7], man_list5[9]),
                          _label_list2[3], _label_list3[5], _label_list4[7], _label_list5[9]), run_time=1)
        self.wait()

        # Filter out all the repeated label whose a and b are not coprime.
        fadelist = VGroup()
        for i in range(15):
            if (i+1) % 2 == 0 and (i+1) / 2 != 2:
                fadelist.add(man_list2[i])
                fadelist.add(_label_list2[i])
            if (i+1) % 3 == 0 and (i+1) / 3 != 2:
                fadelist.add(man_list3[i])
                fadelist.add(_label_list3[i])
            if (i+1) % 2 == 0  and i != 7:
                fadelist.add(man_list4[i])
                fadelist.add(_label_list4[i])
            if (i+1) % 5 == 0  and i != 9:
                fadelist.add(man_list5[i])
                fadelist.add(_label_list5[i])
        self.play(FadeOut(fadelist), run_time=2)
        self.wait(2)
        # 接下来就是最重要的部分了，可以说，我们之前全部的推导都是为了这一步。
        # Fadeout everything except for text1 and text2
        self.play(
            *[FadeOut(obj) for obj in self.mobjects if obj not in [text_1, text_2]],
            run_time=1
        )

        # 我们可以只关注于0到1之间的有理数，现在我们可以很轻松地按照一辆辆大巴的方式，
        # Draw a triangle of rational numbers
        rational = VGroup()
        fadelist = VGroup()
        final_rat = VGroup()
        numbers = []
        cnt = 0
        for j in range(2, 11):
            for i in range(1, j):
                if math.gcd(i, j) != 1:
                    fadelist.add(MathTex(r"\frac{"+str(i)+"}{"+str(j)+"}", color=BLUE).scale(0.5).set_opacity(0.5).shift(LEFT*5+i*RIGHT+4.5*UP+j*DOWN*0.8))
                else:
                    rational.add(MathTex(r"\frac{"+str(i)+"}{"+str(j)+"}", color=GOLD).scale(0.5).shift(LEFT*5+i*RIGHT+4.5*UP+j*DOWN*0.8))
                    final_rat.add(rational[-1].copy().move_to(ORIGIN+UP*3+RIGHT*cnt*0.8+LEFT*5))
                    numbers.append(i/j)
                    cnt += 1
        self.play(FadeIn(rational), FadeIn(fadelist), run_time=2)
        self.wait(2)
        self.play(FadeOut(fadelist), run_time=2)
        self.wait()

        # 把所有的有理数都安排进希尔伯特的旅馆，
        # 先是分母为1的，然后是分母为2的，分母为3的……以此类推。
        self.play(
            LaggedStart(
                *[ReplacementTransform(rational[i], final_rat[i]) for i in range(len(rational))]
            ),
            run_time=5, lag_ratio=0.5
        )
        self.wait(2)
        
        # 这样，我们就可以给每个有理数安排一个房间的编号k。
        # Add room number to each rational number below.
        # First add a opacity=0.5 background rectangle below each rational number, then write the room number.
        backboard = VGroup()
        for i in range(len(final_rat)):
            backboard.add(Rectangle(width=0.7, height=0.5, color=BLUE, fill_opacity=0.5, stroke_width=0.).next_to(final_rat[i], DOWN, buff=0.2))
        room_num = VGroup()
        for i in range(len(final_rat)):
            room_num.add(MathTex(str(i+1), color=ORANGE).scale(0.6).move_to(backboard[i]))
        self.play(
            LaggedStart(
                *[FadeIn(backboard[i]) for i in range(len(final_rat))]
            ),
            LaggedStart(
                *[Write(room_num[i]) for i in range(len(final_rat))]
            ),
            run_time=3, lag_ratio=0.5
        )
        self.wait(4)

        # Display the corresponding relationship between rational numbers and room numbers.
        rect1 = SurroundingRectangle(final_rat[2], color=YELLOW)
        rect2 = SurroundingRectangle(room_num[2], color=YELLOW)
        self.play(Create(rect1), Create(rect2), run_time=1)
        self.wait(2)
        self.play(FadeOut(VGroup(rect1, rect2)), run_time=1)
        self.wait(2)

        # 接下来，我们来给每一个有理数划分领土。
        # 这里，领土的意思是给每一个有理数左右套一个区间。
        # Draw a number line range from -0.1 to 1.1, with ticks and labels.
        nline = NumberLine(x_range=[-0.1, 1.1, 0.1], length=10, include_numbers=True, include_tip=True, include_ticks=True, 
                           tick_size=0.05).set_color(BLUE)
        self.play(Create(nline), run_time=2)
        # Indicate the each rational number, display it on the number line by an arrow and copy the label.
        eps = ValueTracker(0.1)
        arr_list = VGroup()
        domain_list = VGroup()
        bracket_list = VGroup()
        number_label_list = VGroup()
        for i in range(12):
            arr_list.add(Arrow(nline.n2p(numbers[i])+UP, nline.n2p(numbers[i]), buff=0.1, stroke_width=2).set_color(GREEN))
            domain_list.add(always_redraw(
                lambda idx=i : Line(nline.n2p(numbers[idx]-eps.get_value()/(2**idx)), nline.n2p(numbers[idx]+eps.get_value()/(2**idx)), stroke_width=5).set_color(ORANGE)
                )
            )
            bracket_list.add(always_redraw(
                lambda idx=i : MathTex("[", color=YELLOW).scale(0.8).move_to(nline.n2p(numbers[idx]-eps.get_value()/(2**idx)))
                )
            )
            bracket_list.add(always_redraw(
                lambda idx=i : MathTex("]", color=YELLOW).scale(0.8).move_to(nline.n2p(numbers[idx]+eps.get_value()/(2**idx)))
                )
            )
            number_label_list.add(final_rat[i].copy().next_to(arr_list[i], UP, buff=0.1))
        
        unit_domain = always_redraw(
            lambda : Line(nline.n2p(-eps.get_value()), nline.n2p(eps.get_value()), stroke_width=5).set_color(ORANGE).to_corner(DOWN+LEFT)
        )
        
        eps_label = always_redraw(
            lambda : MathTex(r"\epsilon="+format(eps.get_value(), ".3f"), color=ORANGE).scale(0.4).to_corner(DOWN+LEFT).shift(0.3*UP)
        )

        # 如果随机采样得到的实数落入了这个区间里，
        # 那么我们就当作，请注意是当作，这个数字就是有理数了。
        # 这里我们分配的区间长度，会以指数的方式缩减。
        # 具体来说，我们会给第一个有理数最大的领土，宽度是epsilon，这里我们先假设是0.1；
        # 到了第二个有理数1/2的时候，这个范围就只有第一个的一半，也就是epsilon/2=0.05；
        # 第三个有理数1/3的领土进一步缩小，只有0.05的一半，也就是epsilon/4=0.025。
        for i in range(12):
            time = 4 if i < 2 else 0.5
            self.play(
                LaggedStart(
                    Create(arr_list[i]),
                    ReplacementTransform(final_rat[i], number_label_list[i]),
                    Create(domain_list[i]),
                    Create(bracket_list[2*i]), Create(bracket_list[2*i+1]),
                ),
                run_time=time, lag_ratio=0.5
            )
            self.wait(time)
            if i == 0:
                self.play(
                    LaggedStart(
                        Create(unit_domain),
                        Create(eps_label)
                    ),
                    run_time=2
                )
                self.wait(2)
            if i == 1:
                # Show a text to indicate the length of the domain is divided by 2.
                underbrace = Brace(domain_list[i], DOWN, buff=0.1).shift(DOWN).set_color(BLUE)
                text = MathTex(r"\frac{\epsilon}{2}", color=BLUE).scale(0.8).next_to(underbrace, DOWN*0.5, buff=0.1)
                self.play(Create(underbrace), Write(text), run_time=1)
                self.wait(2)
                self.play(FadeOut(underbrace), FadeOut(text), run_time=1)
                self.wait()
            
        
        self.wait(2)

        # 我们用这样的方式，根据每个有理数获得的编号来分配它们各自得到的领土，编号k越大，领土epsilon/2^k越小，而且是呈指数迅速衰减。
        # Indicate each number label
        self.play(
            LaggedStart(
                *[Indicate(number_label_list[i]) for i in range(12)]
            ), run_time=3, lag_ratio=0.3
        )
        self.wait(2)

        # 给每个有理数划分领土是为了什么呢？有了这个划分之后，我们就可以用之前熟悉的几何概型的方法来估算概率了。
        # 在epsilon为0.1的情况下，我们计算一下随机数字落入有理数领土范围的概率。
        # 这实际上就是一个简单的等比数列求和，等于0.1+0.1/2+0.1/2^2+0.1/2^3等，
        eq1 = MathTex(r"P(x\in D)", "=", r"\sum_{k=0}^{\infty}\frac{\epsilon}{2^k}=2\epsilon", color=YELLOW).scale(0.8).shift(DOWN*2)
        self.play(Write(eq1), run_time=2)
        self.wait(4)
        # 根据等比数列求和公式，我们可以得到，这一系列区间范围的和等于2epsilon，也就是0.4。
        # 事实上，因为这些有理数的领土可能会有重复，而且还有些领土到了0和1的范围之外，
        # 实际上随机数字落入有理数领土的概率比这个数字更小，因此我们应该写小于等于号。
        leq_sign = MathTex(r"\leq", color=YELLOW).scale(0.8).move_to(eq1[1])
        self.play(Transform(eq1[1], leq_sign), run_time=1)
        self.wait(4)
        # 但另一方面，因为这些领土严格包含了所有0到1之间的有理数，甚至还掺杂进去了其他更多的无理数，
        # 因此这个数值应该比随机采样x得到的数字【就是】有理数的概率还要略大一些，我们写下大于等于。
        eq_rational = MathTex(r"P(x\in \mathbb{Q}) \leq ", color=YELLOW).scale(0.8).next_to(eq1, LEFT)
        self.play(Write(eq_rational), run_time=2)
        self.wait(2)
        # 因此，我们就得到，均匀随机采样一个0到1之间的实数，是有理数的概率不超过0.2。
        _eq_rational = eq_rational.copy().shift(RIGHT*2.5)
        eps_value = always_redraw(
            lambda: MathTex(format(2*eps.get_value(), ".3f"), color=YELLOW).next_to(_eq_rational, RIGHT, buff=0.2)
        )
        self.play(Transform(eq_rational, _eq_rational), ReplacementTransform(eq1, eps_value), run_time=2)
        
        # 现在最关键的地方来了，要知道，这个epsilon我们是可以任意选取的，而且无论取的多小，这些领土都严格包含了所有的有理数，
        # 所以，x落入有理数领土的概率总是大于等于x严格是有理数的概率。
        # 那么，我们就可以让epsilon越来越小，越来越小。
        self.play(eps.animate.set_value(1e-6), rate_func=smooth, run_time=8)
        self.wait(3)
        self.play(Circumscribe(VGroup(eq_rational, eps_value)), run_time=2)
        self.wait(3)
        
        # 我们于是知道，区间[0,1]内随机采样得到一个数字是有理数的概率可以任意小，
        # 当我们令epsilon趋向于0，我们终于得出结论：在0到1内均匀随机采样，得到有理数的概率是0。

class Uncountable(Scene):
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
        self.wait()

        # 不知道你看到这个证明的感受是什么样的，可以把感受打在弹幕或者评论区。
        # 我第一次看到这个证明的时候，感到一种震颤，一种不同于课本上数学的美妙。
        # 原本随机得到的数字是有理数还是无理数这个问题，它是如此抽象、难以理解，
        # 可是数学居然用严格的逻辑完美而精妙地给出了证明。现代的高等数学展现出其深邃和精妙。
        self.wait(10)
        # 但是，这个证明看起来有点蹊跷：为什么要费这么大劲把有理数一个个列出来？
        # 为什么这些领地范围必须指数衰减？这个证明到底抓住了有理数什么核心的特点，才能得到概率是0？
        # 要深入理解这个问题，
        # 我们可以试着照葫芦画瓢一下，看能不能套用这个证明的框架，证明x是一个实数的概率是0。（停顿）
        # 比如说，我们能不能把所有0到1以内的数字都一个个列出来，然后给它们划分一个指数衰减的领地，
        # Draw a numberline, randomly sample 15 numbers from 0 to 1, and mark them on the numberline.
        nline = NumberLine(x_range=[-0.1, 1.1, 0.1], length=9, include_numbers=True, include_tip=True, include_ticks=True,
                           color=BLUE).shift(UP)
        np.random.seed(10086)
        numbers = np.random.random(15)
        numbers.sort()
        x_list = VGroup()
        x_lbl_list = VGroup()
        for i in range(15):
            x_list.add(MathTex("x_{"+str(i)+"}", color=BLUE).scale(0.5).move_to(UP*3+LEFT*4+i*0.8*RIGHT))
            
        self.play(Create(nline), run_time=3)
        self.wait()
        self.play(Create(x_list), run_time=3)
        self.wait(2)

        eps = ValueTracker(0.1)
        arr_list = VGroup()
        domain_list = VGroup()
        bracket_list = VGroup()
        for i in range(6):
            arr_list.add(Arrow(nline.n2p(numbers[i*2])+0.6*UP, nline.n2p(numbers[i*2]), buff=0.1, stroke_width=2).set_color(GREEN))
            domain_list.add(always_redraw(
                lambda idx=i*2 : Line(nline.n2p(numbers[idx]-eps.get_value()/(2**idx)), nline.n2p(numbers[idx]+eps.get_value()/(2**idx)), stroke_width=5).set_color(ORANGE)
                )
            )
            bracket_list.add(always_redraw(
                lambda idx=i*2 : MathTex("[", color=YELLOW).scale(0.8).move_to(nline.n2p(numbers[idx]-eps.get_value()/(2**idx)))
                )
            )
            bracket_list.add(always_redraw(
                lambda idx=i*2 : MathTex("]", color=YELLOW).scale(0.8).move_to(nline.n2p(numbers[idx]+eps.get_value()/(2**idx)))
                )
            )
            x_lbl_list.add(x_list[i].copy().next_to(arr_list[i], UP, buff=0.1).set_color(ORANGE))
        
        for i in range(6):
            self.play(
                LaggedStart(
                    Create(arr_list[i]),
                    TransformFromCopy(x_list[i], x_lbl_list[i]),
                    Create(domain_list[i]),
                    Create(bracket_list[2*i]), Create(bracket_list[2*i+1]),
                ),
                run_time=0.8, lag_ratio=0.5
            )
            self.wait(0.)
        self.wait(2)
        # 接着让领地的总量趋于0，于是得到是x是一个实数的概率等于0？……
        self.play(eps.animate.set_value(0.001), run_time=4)
        self.wait()
        Piszero = MathTex(r"P(x\in\mathbb{R})=0", color=RED).shift(DOWN)
        rect = SurroundingRectangle(Piszero, color=YELLOW)
        question_mark = MathTex(r"?", color=YELLOW).scale(2).move_to(Piszero)
        self.play(Write(Piszero), run_time=2)
        self.wait()
        self.play(Create(rect), Write(question_mark), run_time=2)
        self.wait(2)
        # 这个结论很荒谬，因为怎么切出来都是实数，概率肯定是1。
        # 所以上述证明肯定走不通，但看起来我们完全可以用上面的流程照猫画虎，
        # 那走不通的那个地方，就是有理数概率为0的关键。
        self.play(FadeOut(question_mark), FadeOut(rect), run_time=1)
        self.wait(5)
        # 而这个关键就在于，我们照葫芦画瓢的尝试在第一步就会失败：
        # 我们不能像刚才一个个列出有理数那样，一个个列出实数。
        # Indicate x_i one by one, then add a large "Impossible" on top of these x_i.
        self.play(
            LaggedStart(
                *[Indicate(x_list[i], color=RED) for i in range(15)],
            ), run_time=3, lag_ratio=0.3
        )
        impossible = Text("Impossible", color=YELLOW).scale(2).add_background_rectangle().move_to(UP*3)
        self.play(Write(impossible), run_time=2)
        self.wait(2)

        # 这是因为，0到1以内的实数太多了，远远比有理数多，多到你不能一个个数出来。
        # 换言之，万能的希尔伯特旅馆，终于在面对区间0到1以内的所有实数时，力不从心了。
        # （停顿）
        self.wait(4)
        # FadeOut everything, except for text1 and text2 
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [text_1, text_2]]
        )
        # 为什么0到1以内的所有实数不能住进希尔伯特的旅馆呢？
        # 我们可以用反证法来证明，假设存在一种方式，将所有的0到1以内的实数全部安排进希尔伯特的旅馆。
        # Add title "酒店入住登记表"
        title = Text("酒店入住登记表", color=GOLD).scale(1.2).to_edge(UP)

        # Draw a table of 20 rows, each row is a 50-digit 0-9 sequence
        # Draw horizontal lines
        hline_list = VGroup()
        for i in range(21):
            hline_list.add(Line(LEFT*4.5, RIGHT*20, stroke_width=3, color=GREEN).shift(UP*2.5+0.6*i*DOWN))
        # Draw two vertical lines
        vline_list = VGroup(
            Line(hline_list[0].get_start(), hline_list[0].get_start()+DOWN*17.5, stroke_width=3, color=GREEN),
            Line(hline_list[0].get_start(), hline_list[0].get_start()+DOWN*17.5, stroke_width=3, color=GREEN).shift(RIGHT),
        )
        idx_note = VGroup()
        for i in range(21):
            idx_note.add(MathTex(str(i+1), color=YELLOW).scale(0.8).move_to(hline_list[i].get_start()+RIGHT*0.5+DOWN*0.3))
        
        # 我们可以列出这样的一张住宿表，其中第i行是住进编号为i这个房间的实数，我们通过无限多位小数的方式把它记录下来。
        self.play(DrawBorderThenFill(title), run_time=2)
        self.play(
            LaggedStart(*[Create(hline_list[i]) for i in range(21)]), 
            LaggedStart(*[Write(idx_note[i]) for i in range(21)]),
            *[Create(vline_list[i]) for i in range(2)],
            run_time=3, lag_ratio=0.5
        )
        
        self.wait(2)
        self.play(FadeOut(title), run_time=1)
        self.wait(2)
        
        number_list = VGroup()
        # generate 20 random numbers in (0,1)
        for i in range(20):
            # generate 50 random digits
            digits = np.random.randint(0, 10, 40)
            # convert digits to a string list of three parts: ".\ "to the first i-1 digits, the i-th digit, and the rest digits
            digits_str = ["."]+["\ "+str(digits[j]) for j in range(40)]
            # convert digits_str to a MathTex
            number_list.add(MathTex("".join(digits_str[:i+1]), digits_str[i+1], "".join(digits_str[i+2:]), color=WHITE).scale(0.8).next_to(idx_note[i], RIGHT, buff=0.6))

        self.play(
            LaggedStart(*[Write(number_list[i]) for i in range(20)]),
            run_time=3, lag_ratio=0.5
        )
        self.wait(2)
        # 现在，我们这样构造出一个新的数字：我们先看这个住宿表的第一行的数字，
        new_number = MathTex("0.","5\ ","3\ ","2\ ","6\ ","1\ ","4\ ","2\ ","3\ ","0\ ","2\ ",r"\cdots", color=ORANGE).to_edge(UP)
        self.play(Write(new_number[0]), run_time=1)
    
        highlight = SurroundingRectangle(number_list[0][1], color=YELLOW)
        self.wait()
        
        # 然后我们选择和它第一位小数不一样的一个数字，比如说原来是9，那我们就改成5；
        # 接下来，我们再看第二行的小数的第二位，是6，那我们选择第二位数字和它也不一样，
        # 比如说，我们改成3……以此类推，
        # 无穷地进行下去这个过程，

        for i in range(10):
            time = 0.5 if i else 3
            if i:
                self.play(highlight.animate.move_to(number_list[i][1]), run_time=1)
            else:
                self.play(Create(highlight), run_time=2)
            self.play(Write(new_number[i+1]), run_time=1)
            self.wait(time)

        self.play(Write(new_number[-1]), FadeOut(highlight), run_time=1)        
        self.wait(2)
        
        # 你会发现我们构造的数字，会和每一个数字在至少一位上不同。
        self.play(Circumscribe(new_number, color=YELLOW), run_time=2)
        highlight.move_to(number_list[0][1])
        # 换言之，我们构造出了一个一定不在这个住宿单上的数字。
        for i in range(10):
            self.play(highlight.animate.move_to(number_list[i][1]), 
                      Indicate(new_number[i+1]),
                      run_time=0.6)
            self.wait(0.2)
        # 这也就意味着，这个住宿单并没有给所有实数都找到住所，
        # 我们通过构造的方式已经找出了一个倒霉蛋，它肯定不在这个旅馆里，从而产生了矛盾。
        self.play(FadeOut(highlight), run_time=1)
        self.wait(3)
        rect = SurroundingRectangle(new_number, color=YELLOW)
        yuanzhong = Text("怨种：", color=YELLOW).next_to(rect, LEFT)
        self.play(Create(rect), Write(yuanzhong), run_time=2)
        # 所以，任何方式都不可能将0到1以内的实数安排进希尔伯特的旅馆。（停顿）
        self.wait(3)

        # Fadeout everything except for text1 and text2
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [text_1, text_2]]
        )

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
        self.wait(5)
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

        # 你爱他但不爱我，3245621
        code = (2**3) * (3**2) * (5**4) * (7**5) * (11**6) * (13**2) * (17**1)
        code_text = MathTex(str(code), color=PURE_GREEN).scale(1.2).shift(UP + RIGHT*3.4)
        rect = SurroundingRectangle(code_text, color=YELLOW)
        self.play(Write(code_text), run_time=2)
        self.play(Create(rect), run_time=1)
        self.wait(4)
        # 可数无穷在不可数无穷面前，就是沧海一粟。
        # 这个世界有清楚规律的毕竟是少数，更多的是无法被一一数出的混沌。
