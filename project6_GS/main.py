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

def creategroup(man, woman):
    men = VGroup(man.copy().scale(0.3).shift(LEFT*1.5+UP*2.4), man.copy().scale(0.3).shift(LEFT*1.5+UP*0.8), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*0.8), man.copy().scale(0.3).shift(LEFT*1.5+DOWN*2.4)) 
    women = VGroup(woman.copy().scale(0.3).shift(RIGHT*1.5+UP*2.4), woman.copy().scale(0.3).shift(RIGHT*1.5+UP*0.8), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*0.8), woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*2.4))
    M_sockets = [LEFT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
    W_sockets = [RIGHT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]

    noteA = MathTex("A", color=ORANGE).scale(0.8).next_to(men[0], DOWN, buff=SMALL_BUFF)
    noteB = MathTex("B", color=ORANGE).scale(0.8).next_to(men[1], DOWN, buff=SMALL_BUFF)
    noteC = MathTex("C", color=ORANGE).scale(0.8).next_to(men[2], DOWN, buff=SMALL_BUFF)
    noteD = MathTex("D", color=ORANGE).scale(0.8).next_to(men[3], DOWN, buff=SMALL_BUFF)
    note_men = VGroup(noteA, noteB, noteC, noteD)

    note1 = MathTex("1", color=ORANGE).scale(0.8).next_to(women[0], DOWN, buff=SMALL_BUFF)
    note2 = MathTex("2", color=ORANGE).scale(0.8).next_to(women[1], DOWN, buff=SMALL_BUFF)
    note3 = MathTex("3", color=ORANGE).scale(0.8).next_to(women[2], DOWN, buff=SMALL_BUFF)
    note4 = MathTex("4", color=ORANGE).scale(0.8).next_to(women[3], DOWN, buff=SMALL_BUFF)
    note_women = VGroup(note1, note2, note3, note4)

    pm1 = MathTex("(", "3", ",",  "4",  ",",  "2", ",",  "1", ")").next_to(men[0], LEFT, buff=0.2)
    pm2 = MathTex("(", "3", ",",  "2",  ",",  "4", ",",  "1", ")").next_to(men[1], LEFT, buff=0.2)
    pm3 = MathTex("(", "1", ",",  "3",  ",",  "4", ",",  "2", ")").next_to(men[2], LEFT, buff=0.2)
    pm4 = MathTex("(", "2", ",",  "4",  ",",  "3", ",",  "1", ")").next_to(men[3], LEFT, buff=0.2)

    pw1 = MathTex("(", "A", ",",  "D",  ",",  "C", ",",  "B", ")").next_to(women[0], RIGHT, buff=0.2)
    pw2 = MathTex("(", "A", ",",  "B",  ",",  "C", ",",  "D", ")").next_to(women[1], RIGHT, buff=0.2)
    pw3 = MathTex("(", "A", ",",  "C",  ",",  "D", ",",  "B", ")").next_to(women[2], RIGHT, buff=0.2)
    pw4 = MathTex("(", "B", ",",  "A",  ",",  "D", ",",  "C", ")").next_to(women[3], RIGHT, buff=0.2)


class Setting(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)

        self.wait(3)
        # 我们首先把人类求偶的问题抽象成这样一个模型。
        men = VGroup(man.copy().scale(0.3).shift(LEFT*1.5+UP*2.4), man.copy().scale(0.3).shift(LEFT*1.5+UP*0.8), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*0.8), man.copy().scale(0.3).shift(LEFT*1.5+DOWN*2.4)) 
        women = VGroup(woman.copy().scale(0.3).shift(RIGHT*1.5+UP*2.4), woman.copy().scale(0.3).shift(RIGHT*1.5+UP*0.8), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*0.8), woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*2.4))
        self.play(LaggedStart(FadeIn(men), FadeIn(women)),
                  run_time=3)
        self.wait(5) # 假设现在有若干男性和若干女性，我们的目标是让每个人都找到自己心仪的另一半。
        
        brace = Brace(men, LEFT, buff=SMALL_BUFF)
        t1 = brace.get_text("$n$").set_color(YELLOW)
        brace2 = Brace(women, RIGHT, buff=SMALL_BUFF)
        t2 = brace2.get_text("$n$").set_color(YELLOW)
        # 为了方便起见，我们假设男性和女性的数量是一样多的，都是n个人。
        self.wait(2)
        self.play(
            GrowFromCenter(brace),
            Create(t1),
        )
        self.play(
            GrowFromCenter(brace2),
            Create(t2),
        )
        # 而且，为了让我们的问题不至于过于复杂，我们不妨假设这些男性和女性都是异性恋。
        self.wait(2)
        self.play(FadeOut(brace), FadeOut(brace2), FadeOut(t1), FadeOut(t2))
        self.wait()
        # 现在我们来当月老，给这些男男女女点鸳鸯谱。简单来说就是配个对，一个男生配一个女生。
        self.wait(2)

        M_sockets = [LEFT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
        W_sockets = [RIGHT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
        l1 = Line(M_sockets[0], W_sockets[2], stroke_width=4, color=YELLOW)
        l2 = Line(M_sockets[1], W_sockets[0], stroke_width=4, color=YELLOW)
        self.play(Create(l1), Create(l2), run_time=2, lag_ratio=0.5)
        self.wait()
        self.play(FadeOut(l1), FadeOut(l2))

        # 但是，配对不能乱配，我们得让这些人尽量满意才行。
        self.wait(2)
        # 我们假设每一个人，无论男性还是女性，都对于所有的异性有一份心中的排名。
        # 在这里，我们用字母ABCD表示男性，用数字1234表示女性。
        noteA = MathTex("A", color=ORANGE).scale(0.8).next_to(men[0], DOWN, buff=SMALL_BUFF)
        noteB = MathTex("B", color=ORANGE).scale(0.8).next_to(men[1], DOWN, buff=SMALL_BUFF)
        noteC = MathTex("C", color=ORANGE).scale(0.8).next_to(men[2], DOWN, buff=SMALL_BUFF)
        noteD = MathTex("D", color=ORANGE).scale(0.8).next_to(men[3], DOWN, buff=SMALL_BUFF)
        note_men = VGroup(noteA, noteB, noteC, noteD)

        note1 = MathTex("1", color=ORANGE).scale(0.8).next_to(women[0], DOWN, buff=SMALL_BUFF)
        note2 = MathTex("2", color=ORANGE).scale(0.8).next_to(women[1], DOWN, buff=SMALL_BUFF)
        note3 = MathTex("3", color=ORANGE).scale(0.8).next_to(women[2], DOWN, buff=SMALL_BUFF)
        note4 = MathTex("4", color=ORANGE).scale(0.8).next_to(women[3], DOWN, buff=SMALL_BUFF)
        note_women = VGroup(note1, note2, note3, note4)

        self.play(Create(note_men), Create(note_women))
        self.wait()

        pm1 = MathTex("(", "3", ",",  "4",  ",",  "2", ",",  "1", ")").next_to(men[0], LEFT, buff=0.2)
        pm2 = MathTex("(", "3", ",",  "2",  ",",  "4", ",",  "1", ")").next_to(men[1], LEFT, buff=0.2)
        pm3 = MathTex("(", "1", ",",  "3",  ",",  "4", ",",  "2", ")").next_to(men[2], LEFT, buff=0.2)
        pm4 = MathTex("(", "2", ",",  "4",  ",",  "3", ",",  "1", ")").next_to(men[3], LEFT, buff=0.2)

        pw1 = MathTex("(", "A", ",",  "D",  ",",  "C", ",",  "B", ")").next_to(women[0], RIGHT, buff=0.2)
        pw2 = MathTex("(", "A", ",",  "B",  ",",  "C", ",",  "D", ")").next_to(women[1], RIGHT, buff=0.2)
        pw3 = MathTex("(", "A", ",",  "C",  ",",  "D", ",",  "B", ")").next_to(women[2], RIGHT, buff=0.2)
        pw4 = MathTex("(", "B", ",",  "A",  ",",  "D", ",",  "C", ")").next_to(women[3], RIGHT, buff=0.2)

        self.play(Create(VGroup(pm1, pm2, pm3, pm4, pw1, pw2, pw3, pw4)), run_time=3, lag_ratio=0.5)
        self.wait(2)

        # 比如说，左边的这位编号为A的男生，在他的心中这四位女生的排名就是(3,4,2,1)，
        self.play(Indicate(pm1), run_time=1)
        self.wait(2)

        # 也就是说，他最喜欢3号女生，其次喜欢4号，然后是2号，排名最低的是1号。
        self.play(Indicate(women[2]), Indicate(pm1[1]))
        self.wait(0.3)
        self.play(Indicate(women[3]), Indicate(pm1[3]))
        self.wait(0.3)
        self.play(Indicate(women[1]), Indicate(pm1[5]))
        self.wait(0.3)
        self.play(Indicate(women[0]), Indicate(pm1[7]))
        self.wait(2)
        # 类似的，女生1也会有这样的一个排名（ADCB），表示在她心中好感由高到低的四位男生的顺序。
        self.play(Indicate(pw1), run_time=2)
        self.wait(2)
        # 怎么样配对才能让大家满意呢？最好的配对方案当然是每个人的另一半正好都是自己的“第一选择”。
        self.wait(5)
        # 这当然很完美，但绝大多数情况下都不可能实现。比方说，男 1 号的最爱是女 1 号，而女 1 号的最爱的却是男2号
        self.wait(5)
        # （放大鱼海棠），那男1和女1的最佳选择就不可能被同时满足。
        # 如果好几个男生的最爱都是同一个女生（莫妮卡点烟），在一夫一妻的制度下，这几个男人的首选也不会同时得到满足。
        # 当这种最为理想的配对方案无法实现时，怎样配对才能令人满意呢？
        # 其实，找的对象太好不见得是个好事儿，和谐才是婚姻的关键。我们只需要追求在配对完成之后，所有的配对都是“稳定”的就好。
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        # 什么叫做稳定呢？简单来说，就是没有人想要劈腿或者私奔。我们用一个简单的例子来定义一下什么叫可能劈腿。
        txt = Text("没有人想要劈腿").set_color(YELLOW)
        self.play(Write(txt), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(txt))

        # 比如在这个例子里，男A和女1配对，男B和女2配对，
        m1 = man.copy().scale(0.4).shift(LEFT*1.5 + UP)
        m2 = man.copy().scale(0.4).shift(LEFT*1.5 + DOWN)
        w1 = woman.copy().scale(0.4).shift(RIGHT*1.5 + UP)
        w2 = woman.copy().scale(0.4).shift(RIGHT*1.5 + DOWN)
        self.play(Create(VGroup(m1, m2, w1, w2)))

        prem1 = MathTex("(", "1", ",", "2", ")").next_to(m1, LEFT, buff=0.2)
        prem2 = MathTex("(", "1", ",",  "2", ")").next_to(m2, LEFT, buff=0.2)
        prew1 = MathTex("(", "B", ",", "A", ")").next_to(w1, RIGHT, buff=0.2)
        prew2 = MathTex("(", "A", ",",  "B", ")").next_to(w2, RIGHT, buff=0.2)
        self.play(Create(VGroup(prem1, prem2, prew1, prew2)))

        l1 = Line(1.2*LEFT+UP, 1.2*RIGHT+UP, stroke_width=4, color=YELLOW)
        l2 = Line(1.2*LEFT+DOWN, 1.2*RIGHT+DOWN, stroke_width=4, color=YELLOW)
        self.wait(2)
        self.play(Create(VGroup(l1, l2)), run_time=2)

        # 可是，在女1的心中，相比起现在的对象男A，她更喜欢男B；
        self.play(Indicate(prew1), run_time=2)
        self.wait(2)
        # 男B心里喜欢女1也胜过现在的对象女2。
        self.play(Indicate(prem2), run_time=2)
        self.wait(2)
        # 好家伙，干柴烈火，一拍即合。（大郎，该吃药了）
        newl = DashedLine(1.2*LEFT+DOWN, 1.2*RIGHT+UP, stroke_width=4, color=RED)
        self.play(Create(newl))
        self.wait(3)
        # 也就是说，当有一对男女，他们在彼此心目中的排名都高过自己被配对的官配的时候，一种潜在的不稳定因素就会存在，劈腿的可能性就会很高。
        
        r1 = SurroundingRectangle(m2)
        r2 = SurroundingRectangle(w1)
        self.play(Create(r1), Create(r2), run_time=2)
        self.wait()
        self.play(Indicate(prem2), Indicate(prew1), run_time=2)
        danger = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\danger.svg").shift(UP*2.5).set_opacity(0.7)
        self.play(Create(danger), run_time=2)
        self.wait(3)
        self.play(FadeOut(r1), FadeOut(r2), FadeOut(danger))

        # 虽然说，人是忠于感情的高级动物，未见得每个人都会劈腿去追逐更好的对象。
        self.wait(15)
        # 但毕竟类似的事情我们见得也不算少（放王宝强、马蓉的照片），所以相比事后选择原谅ta，最好还是在配对的一开始就消除掉所有这些不稳定的因素。
        # 简单来说，尽管我们几乎不可能让所有人都和自己心目中最完美的伴侣在一起，
        # 但是只需要让任何两个彼此没有配对的男女之中，至少有一方喜欢自己配对的伴侣胜过对方，这样，劈腿发生的可能性就被降到最低了。
        # 如果，我们可以在配对中完全消除掉所有这样的不稳定因素，那么我们就达成了一个对于这群人的稳定婚姻匹配。
        # 比如，在上面的例子里，我们如果调换一下，让男B和女1配对，男A和女2配对，那么就不会有人想要劈腿了，这个匹配就比之前的更加稳定。
        l3 = Line(1.2*LEFT+UP, 1.2*RIGHT+DOWN, stroke_width=4, color=RED)
        l4 = Line(1.2*LEFT+DOWN, 1.2*RIGHT+UP, stroke_width=4, color=RED)
        self.play(FadeOut(newl), FadeOut(l1), FadeOut(l2))
        self.play(Create(VGroup(l3, l4)))
        self.wait(2)
        self.play(Circumscribe(VGroup(m1, m2, w1, w2)), run_time=2)
        self.wait(3)

class FreeMarket(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        # （淡化，字幕：自由市场？）
        fm = Text("自由市场？", color=ORANGE).scale(2)
        self.play(FadeIn(fm))
        self.wait(2)
        self.play(FadeOut(fm))
        # 了解了稳定婚姻匹配的概念之后，一个自然的问题出现了：我们怎么样找到一个稳定的匹配呢？
        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)

        self.wait(3)
        # 我们首先把人类求偶的问题抽象成这样一个模型。
        men = VGroup(man.copy().scale(0.3).shift(LEFT*1.5+UP*2.4), man.copy().scale(0.3).shift(LEFT*1.5+UP*0.8), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*0.8), man.copy().scale(0.3).shift(LEFT*1.5+DOWN*2.4)) 
        women = VGroup(woman.copy().scale(0.3).shift(RIGHT*1.5+UP*2.4), woman.copy().scale(0.3).shift(RIGHT*1.5+UP*0.8), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*0.8), woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*2.4))
        self.play(LaggedStart(FadeIn(men), FadeIn(women)),
                  run_time=2)
        noteA = MathTex("A", color=ORANGE).scale(0.8).next_to(men[0], DOWN, buff=SMALL_BUFF)
        noteB = MathTex("B", color=ORANGE).scale(0.8).next_to(men[1], DOWN, buff=SMALL_BUFF)
        noteC = MathTex("C", color=ORANGE).scale(0.8).next_to(men[2], DOWN, buff=SMALL_BUFF)
        noteD = MathTex("D", color=ORANGE).scale(0.8).next_to(men[3], DOWN, buff=SMALL_BUFF)
        note_men = VGroup(noteA, noteB, noteC, noteD)

        note1 = MathTex("1", color=ORANGE).scale(0.8).next_to(women[0], DOWN, buff=SMALL_BUFF)
        note2 = MathTex("2", color=ORANGE).scale(0.8).next_to(women[1], DOWN, buff=SMALL_BUFF)
        note3 = MathTex("3", color=ORANGE).scale(0.8).next_to(women[2], DOWN, buff=SMALL_BUFF)
        note4 = MathTex("4", color=ORANGE).scale(0.8).next_to(women[3], DOWN, buff=SMALL_BUFF)
        note_women = VGroup(note1, note2, note3, note4)

        self.play(Create(note_men), Create(note_women))

        # 甚至有一个更根本的问题，对任何群体、每个人心中任何的排名顺序，是不是都一定存在稳定匹配呢？
        pm1 = MathTex("(", "3", ",",  "4",  ",",  "2", ",",  "1", ")").next_to(men[0], LEFT, buff=0.2)
        pm2 = MathTex("(", "3", ",",  "2",  ",",  "4", ",",  "1", ")").next_to(men[1], LEFT, buff=0.2)
        pm3 = MathTex("(", "1", ",",  "3",  ",",  "4", ",",  "2", ")").next_to(men[2], LEFT, buff=0.2)
        pm4 = MathTex("(", "2", ",",  "4",  ",",  "3", ",",  "1", ")").next_to(men[3], LEFT, buff=0.2)


        pw1 = MathTex("(", "A", ",",  "D",  ",",  "C", ",",  "B", ")").next_to(women[0], RIGHT, buff=0.2)
        pw2 = MathTex("(", "A", ",",  "B",  ",",  "C", ",",  "D", ")").next_to(women[1], RIGHT, buff=0.2)
        pw3 = MathTex("(", "A", ",",  "C",  ",",  "D", ",",  "B", ")").next_to(women[2], RIGHT, buff=0.2)
        pw4 = MathTex("(", "B", ",",  "A",  ",",  "D", ",",  "C", ")").next_to(women[3], RIGHT, buff=0.2)

        self.play(Create(VGroup(pm1, pm2, pm3, pm4, pw1, pw2, pw3, pw4)), run_time=3, lag_ratio=0.5)

        question_mark = Text("?").scale(3).set_color(RED)
        self.play(Write(question_mark))
        mpre_list = ["(1,2,3,4)", "(1,3,2,4)", "(3,4,2,1)", "(2,4,3,1)", "(3,2,4,1)"]
        wpre_list = ["(A,B,C,D)", "(A,D,C,B)", "(A,C,D,B)", "(B,A,C,D)", "(C,A,B,D)"]
        for _ in range(8):
            _pm1 = MathTex(mpre_list[np.random.randint(5)]).next_to(men[0], LEFT, buff=0.2)
            _pm2 = MathTex(mpre_list[np.random.randint(5)]).next_to(men[1], LEFT, buff=0.2)
            _pm3 = MathTex(mpre_list[np.random.randint(5)]).next_to(men[2], LEFT, buff=0.2)
            _pm4 = MathTex(mpre_list[np.random.randint(5)]).next_to(men[3], LEFT, buff=0.2)
            _pw1 = MathTex(wpre_list[np.random.randint(5)]).next_to(women[0], RIGHT, buff=0.2)
            _pw2 = MathTex(wpre_list[np.random.randint(5)]).next_to(women[1], RIGHT, buff=0.2)
            _pw3 = MathTex(wpre_list[np.random.randint(5)]).next_to(women[2], RIGHT, buff=0.2)
            _pw4 = MathTex(wpre_list[np.random.randint(5)]).next_to(women[3], RIGHT, buff=0.2)
            self.play(
                Transform(pm1, _pm1),
                Transform(pm2, _pm2),
                Transform(pm3, _pm3),
                Transform(pm4, _pm4),
                Transform(pw1, _pw1),
                Transform(pw2, _pw2),
                Transform(pw3, _pw3),
                Transform(pw4, _pw4),
                run_time=0.5
            )
            self.wait()

        _pm1 = MathTex("(", "3", ",",  "4",  ",",  "2", ",",  "1", ")").next_to(men[0], LEFT, buff=0.2)
        _pm2 = MathTex("(", "3", ",",  "2",  ",",  "4", ",",  "1", ")").next_to(men[1], LEFT, buff=0.2)
        _pm3 = MathTex("(", "1", ",",  "3",  ",",  "4", ",",  "2", ")").next_to(men[2], LEFT, buff=0.2)
        _pm4 = MathTex("(", "2", ",",  "4",  ",",  "3", ",",  "1", ")").next_to(men[3], LEFT, buff=0.2)


        _pw1 = MathTex("(", "A", ",",  "D",  ",",  "C", ",",  "B", ")").next_to(women[0], RIGHT, buff=0.2)
        _pw2 = MathTex("(", "A", ",",  "B",  ",",  "C", ",",  "D", ")").next_to(women[1], RIGHT, buff=0.2)
        _pw3 = MathTex("(", "A", ",",  "C",  ",",  "D", ",",  "B", ")").next_to(women[2], RIGHT, buff=0.2)
        _pw4 = MathTex("(", "B", ",",  "A",  ",",  "D", ",",  "C", ")").next_to(women[3], RIGHT, buff=0.2)
        self.play(
                Transform(pm1, _pm1),
                Transform(pm2, _pm2),
                Transform(pm3, _pm3),
                Transform(pm4, _pm4),
                Transform(pw1, _pw1),
                Transform(pw2, _pw2),
                Transform(pw3, _pw3),
                Transform(pw4, _pw4),
                FadeOut(question_mark),
                run_time=1
            )
        self.wait()

        self.wait(20)
        # 这个问题当然是有答案的，但我们先不急着知道它。很多时候，自己思考问题的过程比具体答案更重要。
        # 我们可以先站在上帝视角想一想，有什么办法可能可以寻找稳定匹配呢？（停顿）
        # 在刚才介绍的例子中，我们可以注意这样一件事，那就是男B和女1重组之后，如果我们让剩下被绿的男A和女2在一起，那么现在就构成了稳定的匹配。
        # 这启示我们一件事：或许，我们可以让这个恋爱市场的男男女女自由流动重组，不断调配优化。
        # 毕竟，每一次调整发生之后，总有一对男女他们各自心中的伴侣变得更加理想。每一次我们让这两个人自由地调整，然后让单出来的两个人在一起。就这样流动着流动着，最后整个市场就会来到平衡，直到每个人都不想再私奔、不想再折腾，整个群体的婚姻匹配或许也就稳定了？
        # 我们把这样的思路称作自由市场，顾名思义，就是相信市场调配这双“看不见的手”的力量，可以解决一切问题。
        # 可是，在数学的世界里，我们不能依赖一个模糊的感觉，认为“听起来差不多有道理”，就觉得一切皆大欢喜了。
        # 我们能不能证明，对于任何情况，这样市场的自由变动都能最终停止在一个稳定的婚姻匹配上呢？


        # 很可惜，答案是否定的。自由市场不是解决一切的办法，很多时候会失灵。
        # 这里有一个例子，会让这种劈腿永无止境地发生，自由市场变成了永远的NTR。
        # 我们考虑四个男生ABCD，四个女生1234，他们内心各自给对面四位异性的排序如图所示。
        # 我们假设一开始的配对是平行配对的，也就是A和1，B和2，以此类推。
        M_sockets = [LEFT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
        W_sockets = [RIGHT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
        la = Line(M_sockets[0], W_sockets[0], stroke_width=4, color=YELLOW)
        lb = Line(M_sockets[1], W_sockets[1], stroke_width=4, color=YELLOW)
        lc = Line(M_sockets[2], W_sockets[2], stroke_width=4, color=YELLOW)
        ld = Line(M_sockets[3], W_sockets[3], stroke_width=4, color=YELLOW)
        self.play(Create(VGroup(la, lb, lc, ld)))
        self.wait(5)
        # 现在，请注意看、不要眨眼，一场狗血的劈腿轮换即将开始上演。
        # 首先看A和2，在A的心目中，2比1是更高的；同样的，在女生2的心目中，A是她最理想的对象。
        self.play(Indicate(men[0]), Indicate(women[1]), run_time=2)
        self.wait(2)
        # 因此，A和2会劈腿，同时他们各自原本的对象1和B会在一起。
        _la = Line(M_sockets[0], W_sockets[1], stroke_width=4, color=YELLOW)
        _lb = Line(M_sockets[1], W_sockets[0], stroke_width=4, color=YELLOW)
        self.play(Transform(la, _la), Transform(lb, _lb), run_time=2)
        self.wait(3)
        # 接下来，还是A这个男生，他相比2号女生更喜欢4，而4相较于自己的对象D也更喜欢A，
        self.play(Indicate(men[0]), Indicate(women[3]), run_time=2)
        self.wait(2)

        # 于是A又会和4劈腿，2号女生因此和4号女生的原配D在一起；
        _la = Line(M_sockets[0], W_sockets[3], stroke_width=4, color=YELLOW)
        _ld = Line(M_sockets[3], W_sockets[1], stroke_width=4, color=YELLOW)
        self.play(Transform(la, _la), Transform(ld, _ld), run_time=2)
        self.wait(3)

        # 接下来我们把视线聚焦到B，他现在对象是1，但他更喜欢4，而刚刚劈腿的4号女生心中的No.1却是B，
        self.play(Indicate(men[1]), Indicate(women[3]), run_time=2)
        self.wait(2)

        # 所以4号女生会劈腿和B在一起，同时A也重新回到了1号女生的怀抱（1：你还好意思回来？A：别以为我不知道你做了什么，都别嫌弃）；
        _lb = Line(M_sockets[1], W_sockets[3], stroke_width=4, color=YELLOW)
        _la = Line(M_sockets[0], W_sockets[0], stroke_width=4, color=YELLOW)
        self.play(Transform(la, _la), Transform(lb, _lb), run_time=2)
        self.wait(3)

        # 最后，B男生和2号女生会再次劈腿，因为你会发现，B的排序里2号高于现在的对象4号，而2号的排序里，B也高于自己现在的对象D，
        # 所以他们又会劈腿，各自的对象男生D和4号女生重新在一起。
        _lb = Line(M_sockets[1], W_sockets[1], stroke_width=4, color=YELLOW)
        _ld = Line(M_sockets[3], W_sockets[3], stroke_width=4, color=YELLOW)
        self.play(Transform(lb, _lb), Transform(ld, _ld), run_time=2)
        self.wait(3)
        # （停顿）在这停顿，你发现了什么？
        self.play(Circumscribe(VGroup(men, women)), run_time=2)
        same_txt = Text("完全一致", color=YELLOW).scale(2).shift(UP*1.5)
        self.play(Write(same_txt))
        self.wait()
        self.play(FadeOut(same_txt))

        # 是的，一通操作猛如虎之后，一切又回到了刚开始的起点。如果他们继续闹腾，这个过程会循环往复，永恒不停。（停顿）
        # 所以，自由市场不是万能的，这里就失效了。如果我们放任自流，这些人永远不会收敛到一个稳定的状态，而是永远的这山望着那山高，分分合合、不断劈腿。

        for _ in range(8):
            _la = Line(M_sockets[0], W_sockets[1], stroke_width=4, color=YELLOW)
            _lb = Line(M_sockets[1], W_sockets[0], stroke_width=4, color=YELLOW)
            self.play(Transform(la, _la), Transform(lb, _lb), run_time=0.3)

            _la = Line(M_sockets[0], W_sockets[3], stroke_width=4, color=YELLOW)
            _ld = Line(M_sockets[3], W_sockets[1], stroke_width=4, color=YELLOW)
            self.play(Transform(la, _la), Transform(ld, _ld), run_time=0.3)

            _lb = Line(M_sockets[1], W_sockets[3], stroke_width=4, color=YELLOW)
            _la = Line(M_sockets[0], W_sockets[0], stroke_width=4, color=YELLOW)
            self.play(Transform(la, _la), Transform(lb, _lb), run_time=0.3)

            _lb = Line(M_sockets[1], W_sockets[1], stroke_width=4, color=YELLOW)
            _ld = Line(M_sockets[3], W_sockets[3], stroke_width=4, color=YELLOW)
            self.play(Transform(lb, _lb), Transform(ld, _ld), run_time=0.3)
            self.wait(0.8)

        self.wait(4)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class GS_Alg(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        # 既然完全自由不行，那么我们就需要有一个统筹的顺序来完成匹配。
        # 1962年，美国数学家 David Gale 和 Lloyd Shapley共同提出了一个方法策略，并证明了这个策略一定可以找到稳定的匹配，
        # 这个算法也因此被称为“Gale-Shapley算法”，或GS算法。
        # 非常有趣的是，他们发现的这个方法，居然和现实世界实际发生的流程非常相似。
        # 换句话说，人类似乎早已经在无意识中，一直在真实的社会里做着完全类似的事情，从而达成群体婚姻的稳定。
        # 而这个方法的核心说白了，就是“有序表白”。
        # 我们还是用之前的这个例子来实际看看GS算法的流程。
        self.wait(10)
        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)

        self.wait(3)
        # 我们首先把人类求偶的问题抽象成这样一个模型。
        men = VGroup(man.copy().scale(0.3).shift(LEFT*3+DOWN), man.copy().scale(0.3).shift(LEFT*1+DOWN), 
                     man.copy().scale(0.3).shift(RIGHT+DOWN), man.copy().scale(0.3).shift(RIGHT*3+DOWN)) 
        women = VGroup(woman.copy().scale(0.3).shift(LEFT*3+UP*2), woman.copy().scale(0.3).shift(LEFT*1+UP*2), 
                     woman.copy().scale(0.3).shift(RIGHT*1+UP*2), woman.copy().scale(0.3).shift(RIGHT*3+UP*2))
        self.play(LaggedStart(FadeIn(men), FadeIn(women)),
                  run_time=2)
        noteA = always_redraw(lambda: MathTex("A", color=ORANGE).scale(0.8).next_to(men[0], RIGHT, buff=SMALL_BUFF))
        noteB = always_redraw(lambda: MathTex("B", color=ORANGE).scale(0.8).next_to(men[1], RIGHT, buff=SMALL_BUFF))
        noteC = always_redraw(lambda: MathTex("C", color=ORANGE).scale(0.8).next_to(men[2], RIGHT, buff=SMALL_BUFF))
        noteD = always_redraw(lambda: MathTex("D", color=ORANGE).scale(0.8).next_to(men[3], RIGHT, buff=SMALL_BUFF))
        note_men = VGroup(noteA, noteB, noteC, noteD)

        note1 = always_redraw(lambda: MathTex("1", color=ORANGE).scale(0.8).next_to(women[0], RIGHT, buff=SMALL_BUFF))
        note2 = always_redraw(lambda: MathTex("2", color=ORANGE).scale(0.8).next_to(women[1], RIGHT, buff=SMALL_BUFF))
        note3 = always_redraw(lambda: MathTex("3", color=ORANGE).scale(0.8).next_to(women[2], RIGHT, buff=SMALL_BUFF))
        note4 = always_redraw(lambda: MathTex("4", color=ORANGE).scale(0.8).next_to(women[3], RIGHT, buff=SMALL_BUFF))
        note_women = VGroup(note1, note2, note3, note4)

        self.play(Create(note_men), Create(note_women))

        pm1 = always_redraw(
            lambda: MathTex("(", "3", ",",  "4",  ",",  "2", ",",  "1", ")").scale(0.7).next_to(men[0], DOWN, buff=0.2)
        )
        pm2 = always_redraw(
            lambda: MathTex("(", "3", ",",  "2",  ",",  "4", ",",  "1", ")").scale(0.7).next_to(men[1], DOWN, buff=0.2)
        )
        pm3 = always_redraw(
            lambda: MathTex("(", "1", ",",  "3",  ",",  "4", ",",  "2", ")").scale(0.7).next_to(men[2], DOWN, buff=0.2)
        )
        pm4 = always_redraw(
            lambda: MathTex("(", "2", ",",  "4",  ",",  "3", ",",  "1", ")").scale(0.7).next_to(men[3], DOWN, buff=0.2)
        )

        pw1 = always_redraw(
            lambda: MathTex("(", "A", ",",  "D",  ",",  "C", ",",  "B", ")").scale(0.7).next_to(women[0], UP, buff=0.2)
        )
        pw2 = always_redraw(
            lambda: MathTex("(", "A", ",",  "B",  ",",  "C", ",",  "D", ")").scale(0.7).next_to(women[1], UP, buff=0.2)
        )
        pw3 = always_redraw(
            lambda: MathTex("(", "A", ",",  "C",  ",",  "D", ",",  "B", ")").scale(0.7).next_to(women[2], UP, buff=0.2)
        )
        pw4 = always_redraw(
            lambda: MathTex("(", "B", ",",  "A",  ",",  "D", ",",  "C", ")").scale(0.7).next_to(women[3], UP, buff=0.2)
        )

        self.play(Create(VGroup(pm1, pm2, pm3, pm4, pw1, pw2, pw3, pw4)), run_time=1, lag_ratio=0.5)


        # 整个GS算法的流程其实就是男生表白，女生接受或者拒绝。（字幕）
        # 男生该怎么表白呢？很简单，对着自己的列表从上到下地去追求。
        self.wait(3)
        self.play(ApplyWave(pm1), ApplyWave(pm2), ApplyWave(pm3), ApplyWave(pm4), run_time=2)
        self.wait(2)
        # 在这个方法里，每个男生都会先大胆地追求自己最理想的女生，
        # 比如A和B都会去追求3，C会追求1，而D会追求2。
        self.play(
            men[0].animate.move_to(women[2].get_center()+DOWN),
            men[1].animate.move_to(women[2].get_center()+DOWN*3),
            men[2].animate.move_to(women[0].get_center()+DOWN),
            men[3].animate.move_to(women[1].get_center()+DOWN),
            run_time=2
        )
        self.wait(8)
        # 面对来自男生的追求，女生该怎么办呢？

        # 这里我们分两类，对于女生1和女生2而言，她们都只接收到一个男生的追求，
        self.play(Circumscribe(women[0]), Circumscribe(women[1]))
        # 所以不管怎么样，算法的流程会让她们先接受了再说。
        heart = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\heart.svg").scale(0.4)
        h1 = heart.copy().set_opacity(0.6).move_to(women[0].get_center()+DOWN*0.5)
        h2 = heart.copy().set_opacity(0.6).move_to(women[1].get_center()+DOWN*0.5)
        self.play(Create(VGroup(h1, h2)), run_time=2, lag_ratio=0.5)
        self.wait(3)

        # 女生3有些难办，因为此时她受到了两个男生同时的追求，那么她应该接受谁呢？
        self.play(Indicate(men[0]), Indicate(men[1]), run_time=2)
        self.wait(2)
        # 答案是，女生3根据自己的喜好列表，在A和B中挑选出自己更喜欢的那个，也就是A，选择和A在一起，同时拒绝B。
        rect = SurroundingRectangle(pw3[1])
        self.play(Create(rect), run_time=1)
        self.wait(2)

        h3 = heart.copy().set_opacity(0.5).move_to(women[2].get_center()+DOWN*0.5)

        self.play(
            FadeOut(rect),
            Create(h3),
            men[1].animate.shift(DOWN),
            run_time=2
        )
        self.wait()

        hb = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\Broken_heart.svg").scale(0.5)
        hb1 = hb.copy().set_opacity(0.4).move_to(men[1].get_center())
        self.play(Create(hb1))
        self.wait(4)

        # 这样，男生们第一轮的表白环节就结束了。
        # ACD三位男生各自获得了一位女生的青睐，而B则不巧，没有对象，
        self.play(Circumscribe(men[0]), Circumscribe(men[2]), Circumscribe(men[3]), run_time=2)
        self.wait()
        self.play(Indicate(men[1]), run_time=2)
        self.play(FadeOut(hb1))

        # 但这三位男生还不能高兴的太早，因为整个流程还没有结束，他们也只是暂时地和身边的女生在一起而已。
        # 只要还有人单着，这个算法就会继续。
        self.wait(10)
        # 接下来，依然单身的男生们，准确说是只有这一个男生B，会在自己的名单上划去3号的名字，接着向自己好感排名第二的2号表白。
        cross = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\cross.svg")
        cr1 = cross.copy().scale(0.2).set_opacity(0.5).add_updater(lambda mob: mob.move_to(pm2[1]))
        self.play(FadeIn(cr1), run_time=2)
        self.wait(2)

        self.play(men[1].animate.move_to(women[1].get_center() + DOWN*3))
        self.wait(3)

        # 此时又出现了问题，2号女生已经在第一轮接受了D男生的表白，现在又面临B男生的示好，她该怎么办呢？
        self.play(Indicate(h2))
        self.play(Indicate(men[1]))
        self.wait(2)

        # 答案是，看2号自己的喜好列表，在2号的好感排名里我们能看到，D其实排在最后，
        self.play(ApplyWave(pw2))
        rect = SurroundingRectangle(pw2[7])
        self.wait()
        self.play(Create(rect), run_time=2)

        # 只不过因为第一轮只有D向她表白，所以2号接受了D。
        self.wait(3)
        # 现在，她心目中更好的B前来示好，2号该怎么办呢？
        self.play(Indicate(men[1]), Indicate(pw2[3]))
        self.wait(3)

        # GS算法告诉这位女生的答案很简单，那就是：甩了D。
        # 没错，此时2号就会甩了D，跟B在一起。到这里，算法的第二轮就结束了，单身的人从B变成了D。
        self.play(
            FadeOut(h2), FadeOut(rect),
            men[3].animate.move_to(ORIGIN+DOWN*2),
            run_time=2, lag_ratio=0.5
            )
        hb2 = hb.copy().set_opacity(0.4).move_to(men[3].get_center())
        
        self.play(
            men[1].animate.move_to(women[1].get_center()+ DOWN),
            FadeIn(h2),
            run_time=2, lag_ratio=0.5
        )
        self.wait(2)
        self.play(Create(hb2))
        # 算法第三轮，唯一单身的D划去了名单上的2号，向自己名单上的第二位表白。
        cr2 = cross.copy().scale(0.2).set_opacity(0.5).add_updater(lambda mob: mob.move_to(pm4[1]))
        self.play(FadeIn(cr2), run_time=2)
        self.wait(2)
        self.play(FadeOut(hb2), men[3].animate.move_to(women[3].get_center()+DOWN), run_time=3)
        self.wait(2)

        # 碰巧的是，这正是现在一直孤单一人的4号女生，于是D男生和4号女生成功在一起。
        self.play(Circumscribe(women[3]))
        self.wait()
        h4 = heart.copy().set_opacity(0.5).move_to(women[3].get_center()+DOWN*0.5)
        self.play(Create(h4), run_time=2)
        self.wait(2)
        # 此时，所有人都找到了自己的伴侣，A和3，B和2，C和1，D和4，整个算法流程结束。
        self.play(Indicate(men[0]), Indicate(women[2]))
        self.play(Indicate(men[1]), Indicate(women[1]))
        self.play(Indicate(men[2]), Indicate(women[0]))
        self.play(Indicate(men[3]), Indicate(women[3]))
        self.wait(5)

        # 以上，就是Gale-Shapely算法的基本流程，相信你已经从刚才的过程中发现了一些端倪。

        # 现在，让我们更加明确地定义男生和女生在这套算法中各自的行动准则：
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait(2)
        # 男生的准则有三条，
        boy_rule = Text("男生GS准则", color=BLUE).to_edge(UP)
        self.play(Write(boy_rule))
        self.wait()
        boy_r1 = Text("1. 如果单身，那么就向列表最喜欢的女生表白", color=BLUE).scale(0.6).shift(UP*2+LEFT)
        # 1、如果此时单身，那么就去向自己目前列表上最喜欢的女生表白；
        self.play(Write(boy_r1), run_time=3)
        self.wait(2)
        boy_r2 = Text("2. 如果不是单身，那么保持不动，直到结束或被甩", color=BLUE).scale(0.6).next_to(boy_r1, DOWN, buff=0.2).align_to(boy_r1, LEFT)
        # 2、如果此时不是单身，那么就保持不动，直到流程结束或自己被甩；
        self.play(Write(boy_r2), run_time=3)
        self.wait(2)
        boy_r3 = Text("3. 无论被拒还是被甩，都永远删掉这个女生，回到1", color=BLUE).scale(0.6).next_to(boy_r2, DOWN, buff=0.2).align_to(boy_r1, LEFT)
        # 3、无论是被拒还是被甩，都把这个女生从自己的列表上永远划掉，并进入第一条。
        self.play(Write(boy_r3), run_time=3)
        self.wait(2)

        # 以上就是男生的行动准则。对女生而言只有两条：
        self.wait(3)
        girl_rule = Text("女生GS准则", color=LIGHT_PINK)
        self.play(Write(girl_rule))
        self.wait()
        # 1、静等男生向自己表白，每次选择向自己表白的所有人中最喜欢的那个；
        girl_r1 = Text("1. 等待表白，每次选择最喜欢的人接受", color=LIGHT_PINK).scale(0.6).shift(DOWN).align_to(boy_r1, LEFT)
        self.play(Write(girl_r1), run_time=3)
        self.wait(2)
        # 2、如果有更喜欢的男生向自己表白，则甩掉自己目前的对象，和新的人在一起。
        girl_r2 = Text("2. 如果有更喜欢的人向自己表白，那么和新的人在一起", color=LIGHT_PINK).scale(0.6).next_to(girl_r1, DOWN, buff=0.2).align_to(boy_r1, LEFT)
        self.play(Write(girl_r2), run_time=3)
        self.wait(2)

        # GS算法最了不起的地方在于，它不是一个简单瞎想的流程，而是有着严格的数学证明作为基础。
        self.wait(10)
        # 更有意思的是，这个流程和人类社会真实发生的过程非常相似。
        # 屏幕上的这些行为准则，是有着一定的现实意义的。接下来，就请跟紧我，一起来品味这个看似简单的算法，背后有着怎样丰富的意蕴。

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        
class Enumerate(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)

        men = VGroup(man.copy().scale(0.3).shift(LEFT*1.5+UP*2.4), man.copy().scale(0.3).shift(LEFT*1.5+UP*0.8), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*0.8), man.copy().scale(0.3).shift(LEFT*1.5+DOWN*2.4)) 
        women = VGroup(woman.copy().scale(0.3).shift(RIGHT*1.5+UP*2.4), woman.copy().scale(0.3).shift(RIGHT*1.5+UP*0.8), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*0.8), woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*2.4))
        self.play(LaggedStart(FadeIn(men), FadeIn(women)),
                  run_time=1)
        noteA = MathTex("A", color=ORANGE).scale(0.8).next_to(men[0], DOWN, buff=SMALL_BUFF)
        noteB = MathTex("B", color=ORANGE).scale(0.8).next_to(men[1], DOWN, buff=SMALL_BUFF)
        noteC = MathTex("C", color=ORANGE).scale(0.8).next_to(men[2], DOWN, buff=SMALL_BUFF)
        noteD = MathTex("D", color=ORANGE).scale(0.8).next_to(men[3], DOWN, buff=SMALL_BUFF)
        note_men = VGroup(noteA, noteB, noteC, noteD)

        note1 = MathTex("1", color=ORANGE).scale(0.8).next_to(women[0], DOWN, buff=SMALL_BUFF)
        note2 = MathTex("2", color=ORANGE).scale(0.8).next_to(women[1], DOWN, buff=SMALL_BUFF)
        note3 = MathTex("3", color=ORANGE).scale(0.8).next_to(women[2], DOWN, buff=SMALL_BUFF)
        note4 = MathTex("4", color=ORANGE).scale(0.8).next_to(women[3], DOWN, buff=SMALL_BUFF)
        note_women = VGroup(note1, note2, note3, note4)
        self.play(Create(note_men), Create(note_women))

        M_sockets = [LEFT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
        W_sockets = [RIGHT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
        l1 = Line(M_sockets[0], W_sockets[0], stroke_width=4, color=YELLOW)
        l2 = Line(M_sockets[1], W_sockets[1], stroke_width=4, color=YELLOW)
        l3 = Line(M_sockets[2], W_sockets[2], stroke_width=4, color=YELLOW)
        l4 = Line(M_sockets[3], W_sockets[3], stroke_width=4, color=YELLOW)

        for _ in range(8):
            per = np.random.permutation(4)
            _l1 = Line(M_sockets[0], W_sockets[per[0]], stroke_width=4, color=YELLOW)
            _l2 = Line(M_sockets[1], W_sockets[per[1]], stroke_width=4, color=YELLOW)
            _l3 = Line(M_sockets[2], W_sockets[per[2]], stroke_width=4, color=YELLOW)
            _l4 = Line(M_sockets[3], W_sockets[per[3]], stroke_width=4, color=YELLOW)
            self.play(Transform(l1, _l1), Transform(l2, _l2), Transform(l3, _l3), Transform(l4, _l4),
                run_time=0.5)
            self.wait(0.5)
        self.wait(2)



class Proof(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)
        cross = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\cross.svg")

        self.wait(3)
        # 我们首先把人类求偶的问题抽象成这样一个模型。
        men = VGroup(man.copy().scale(0.3).shift(LEFT*3+DOWN), man.copy().scale(0.3).shift(LEFT*1+DOWN), 
                     man.copy().scale(0.3).shift(RIGHT+DOWN), man.copy().scale(0.3).shift(RIGHT*3+DOWN)) 
        women = VGroup(woman.copy().scale(0.3).shift(LEFT*3+UP*2), woman.copy().scale(0.3).shift(LEFT*1+UP*2), 
                     woman.copy().scale(0.3).shift(RIGHT*1+UP*2), woman.copy().scale(0.3).shift(RIGHT*3+UP*2))
        self.play(LaggedStart(FadeIn(men), FadeIn(women)),
                  run_time=1)
        noteA = always_redraw(lambda: MathTex("A", color=ORANGE).scale(0.8).next_to(men[0], RIGHT, buff=SMALL_BUFF))
        noteB = always_redraw(lambda: MathTex("B", color=ORANGE).scale(0.8).next_to(men[1], RIGHT, buff=SMALL_BUFF))
        noteC = always_redraw(lambda: MathTex("C", color=ORANGE).scale(0.8).next_to(men[2], RIGHT, buff=SMALL_BUFF))
        noteD = always_redraw(lambda: MathTex("D", color=ORANGE).scale(0.8).next_to(men[3], RIGHT, buff=SMALL_BUFF))
        note_men = VGroup(noteA, noteB, noteC, noteD)

        note1 = always_redraw(lambda: MathTex("1", color=ORANGE).scale(0.8).next_to(women[0], RIGHT, buff=SMALL_BUFF))
        note2 = always_redraw(lambda: MathTex("2", color=ORANGE).scale(0.8).next_to(women[1], RIGHT, buff=SMALL_BUFF))
        note3 = always_redraw(lambda: MathTex("3", color=ORANGE).scale(0.8).next_to(women[2], RIGHT, buff=SMALL_BUFF))
        note4 = always_redraw(lambda: MathTex("4", color=ORANGE).scale(0.8).next_to(women[3], RIGHT, buff=SMALL_BUFF))
        note_women = VGroup(note1, note2, note3, note4)

        self.play(Create(note_men), Create(note_women))

        pm1 = always_redraw(
            lambda: MathTex("(", "3", ",",  "4",  ",",  "2", ",",  "1", ")").scale(0.7).next_to(men[0], DOWN, buff=0.2)
        )
        pm2 = always_redraw(
            lambda: MathTex("(", "3", ",",  "2",  ",",  "4", ",",  "1", ")").scale(0.7).next_to(men[1], DOWN, buff=0.2)
        )
        pm3 = always_redraw(
            lambda: MathTex("(", "1", ",",  "3",  ",",  "4", ",",  "2", ")").scale(0.7).next_to(men[2], DOWN, buff=0.2)
        )
        pm4 = always_redraw(
            lambda: MathTex("(", "2", ",",  "4",  ",",  "3", ",",  "1", ")").scale(0.7).next_to(men[3], DOWN, buff=0.2)
        )

        pw1 = always_redraw(
            lambda: MathTex("(", "A", ",",  "D",  ",",  "C", ",",  "B", ")").scale(0.7).next_to(women[0], UP, buff=0.2)
        )
        pw2 = always_redraw(
            lambda: MathTex("(", "A", ",",  "B",  ",",  "C", ",",  "D", ")").scale(0.7).next_to(women[1], UP, buff=0.2)
        )
        pw3 = always_redraw(
            lambda: MathTex("(", "A", ",",  "C",  ",",  "D", ",",  "B", ")").scale(0.7).next_to(women[2], UP, buff=0.2)
        )
        pw4 = always_redraw(
            lambda: MathTex("(", "B", ",",  "A",  ",",  "D", ",",  "C", ")").scale(0.7).next_to(women[3], UP, buff=0.2)
        )

        self.play(Create(VGroup(pm1, pm2, pm3, pm4, pw1, pw2, pw3, pw4)), run_time=1, lag_ratio=0.5)

        # 首先，之前的自由市场我们已经看到，劈腿的过程有可能重复发生、无穷无尽。
        # 那GS算法会不会出现这样的情况呢？
        # 很幸运的是，这是不可能的，而道理很简单：
        self.wait(2)
        # 因为所有男人列表上没有被划掉的女生总数是有限的，一开始一共nxn等于n平方，
        rect = SurroundingRectangle(VGroup(pm1, pm2, pm3, pm4))
        self.play(Create(rect))
        numb = MathTex(r"n\times n=n^2", color=GREEN).next_to(rect, DOWN, buff=0.1)
        self.play(Write(numb), run_time=2)
        self.wait(3)
        # 而每一轮都会不断的从这个有限的列表里划掉若干个女生。
        # 总数有限，又在不断消耗，最终这个过程肯定会结束，不可能无限循环。
        self.play(FadeOut(numb), FadeOut(rect))
        self.wait(2)

        # 无限循环的问题解决了，我们来证明第二个重要的问题：
        # 这个流程最终得到的配对一定是稳定的。
        # 如果你仔细回味之前的这个流程就会发现，
        self.play(
            FadeOut(men[0]),FadeOut(men[2]),FadeOut(men[3]),
            FadeOut(pm1), FadeOut(pm3), FadeOut(pm4),
            FadeOut(noteA), FadeOut(noteC), FadeOut(noteD),
            run_time=2
        )
        # 随着轮数的增加，一个男人追求的对象在他心里只会越来越糟，
        self.play(men[1].animate.move_to(women[2].get_center() + DOWN), run_time=1)
        self.wait(0.5)
        cr3 = cross.copy().scale(0.2).set_opacity(0.5).add_updater(lambda mob: mob.move_to(pm2[1]))
        self.play(Create(cr3), run_time=0.5)
        self.wait(0.5)
        self.play(men[1].animate.move_to(women[1].get_center() + DOWN), run_time=1)
        self.wait(0.5)
        cr4 = cross.copy().scale(0.2).set_opacity(0.5).add_updater(lambda mob: mob.move_to(pm2[3]))
        self.play(Create(cr4), run_time=0.5)
        self.wait(0.5)
        self.play(men[1].animate.move_to(women[3].get_center() + DOWN), run_time=1)
        self.wait(0.5)
        cr5 = cross.copy().scale(0.2).set_opacity(0.5).add_updater(lambda mob: mob.move_to(pm2[5]))
        self.play(Create(cr5), run_time=0.5)
        self.wait()
        # 而每个女人的伴侣却在越来越好。
        # 所以，如果我们考虑任何一对男女，他们在最后没有在一起，他们有没有可能劈腿呢？（停顿）
        self.wait(3)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        m1 = man.copy().set_color(BLUE).scale(0.4).shift(LEFT*1.5 + UP)
        m2 = man.copy().set_color(GREEN).scale(0.4).shift(LEFT*1.5 + DOWN)
        w1 = woman.copy().set_color(GREEN).scale(0.4).shift(RIGHT*1.5 + UP)
        w2 = woman.copy().set_color(LIGHT_PINK).scale(0.4).shift(RIGHT*1.5 + DOWN)
        self.play(Create(VGroup(m1, m2, w1, w2)))

        noteA = MathTex("A", color=ORANGE).scale(0.5).next_to(m1, DOWN, buff=0.1)
        noteB = MathTex("B", color=ORANGE).scale(0.5).next_to(m2, DOWN, buff=0.1)
        note1 = MathTex("1", color=ORANGE).scale(0.5).next_to(w1, DOWN, buff=0.1)
        note2 = MathTex("2", color=ORANGE).scale(0.5).next_to(w2, DOWN, buff=0.1)

        
        self.play(Create(VGroup(noteA, noteB, note1, note2)))

        l1 = Line(1.2*LEFT+UP, 1.2*RIGHT+UP, stroke_width=4, color=YELLOW)
        l2 = Line(1.2*LEFT+DOWN, 1.2*RIGHT+DOWN, stroke_width=4, color=YELLOW)
        self.wait(2)
        self.play(Create(VGroup(l1, l2)), run_time=1)

        r1 = SurroundingRectangle(m1)
        r2 = SurroundingRectangle(w2)
        qm = Tex("?", color=YELLOW).scale(2).shift(UP*2.5)
        self.play(Create(r1), Create(r2), run_time=2)
        self.play(Write(qm))
        self.wait(2)
        self.play(FadeOut(qm), FadeOut(r1), FadeOut(r2))

        # 答案是不可能，因为，要劈腿，首先需要男人喜欢这个女人胜过自己现在的官配，
        self.wait(3)
        gr1 = w2.copy().scale(0.5).move_to(ORIGIN + LEFT*5)
        gr_sign = MathTex(">", color=RED).next_to(gr1, RIGHT, buff=0.1)
        gr2 = w1.copy().scale(0.5).next_to(gr_sign, RIGHT, buff=0.1)
        man_prefer = VGroup(gr1, gr_sign, gr2)
        self.play(Create(man_prefer), run_time=2)
        # 而因为男生都是按照下降的顺序表白的，所以这个男人肯定之前早已经找过这个女人了，
        self.wait(3)
        self.play(Indicate(w2), run_time=2)
        # 而且最终的结局告诉我们，他们并没有在一起。
        self.wait(2)
        self.play(Indicate(l1), Indicate(l2))
        # 没有在一起有两种情况，当时要么是当场被拒，
        # 要么是一开始成功后来被甩了。

        ### 这里用下面的Reject和Dump
        self.wait(5)

        # 这两种情况都有一个共同点，那就是女人一定是因为一个更好的对象、才拒绝或甩了这个男人，
        # 在这个男人放弃这个女人之后，这个女人一定拥有着他更满意的对象。
        # 我们又知道，在所有之后的流程里，这个女人的伴侣只会变得越来越满意，
        # 所以，当时就更喜欢自己对象的女人，现在肯定只会对自己的对象更满意。
        ggr1 = m2.copy().scale(0.5).move_to(ORIGIN + RIGHT*4)
        ggr_sign = MathTex(">", color=RED).next_to(ggr1, RIGHT, buff=0.1)
        ggr2 = m1.copy().scale(0.5).next_to(ggr_sign, RIGHT, buff=0.1)
        woman_prefer = VGroup(ggr1, ggr_sign, ggr2)
        self.play(Create(woman_prefer), run_time=2)

        # 当时拒绝或者甩了这个男人，以后就更不可能会喜欢这个男人超过自己的官配。
        # 因为这里的男女是我们任意选取的，所以我们知道对于任何没有配在一起的男女都成立，
        # 所以，GS算法最终得到的流程一定是稳定的匹配，
        self.wait(3)
        self.play(Circumscribe(man_prefer), Circumscribe(woman_prefer), run_time=2)
        self.wait(2)
        # 没有任何两个人想要背叛自己配对的对象劈腿。

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        self.wait(12)
        # 在大学的算法设计课堂上，GS算法基本上讲到这里就结束了，绝大部分的科普也只会点到这里为止。
        # 可在我看来，GS算法背后丰富的内涵远远超过了一个数学算法本身，而延展到了真实的社会。
        # 细心深入地品味它，你会得到深刻的启示。
        # 比如，我想先问这样一个问题：你觉得这个算法对于男生和女生来说公平吗？

        question = Text("GS算法对男女公平吗？", color=RED).shift(UP*2)
        self.play(Write(question), run_time=2)
        self.wait(5)

        # 你觉得它是更有利于男生，还是更有利于女生呢？可以把你的答案写在投票和弹幕里。
        # 很多人从直觉上观察这个算法的流程，会替男生打抱不平，觉得这个算法明显更有利于女生。
        # 道理是，男生追求的对象只能越来越差，女生的对象却越来越好；
        # 男生有了对象之后还可能被甩，可女生一旦有了对象就永远不会单身，只会让自己的对象变得越来越理想。
        # 凭什么！这不公平！男人什么时候才能站起来，气抖冷。
        # 可是，接下来我说的结论可能会让你非常吃惊：这个算法本质上是非常有利于男性的。

        answer = Text("完全有利于男生", color=YELLOW).next_to(question, DOWN, buff=0.4)
        self.play(Write(answer), run_time=2)
        self.wait(10)

        # 而且不是简单的有利于哪一个男性，这个算法流程可以让所有的男性，没错，是所有的男性，在稳定匹配的条件下，同时获得所有可能的对象里最好的那一个。
        self.play(FadeOut(answer), FadeOut(question))
        # 首先，我们可以一一列举所有可能的配对方法，并在其中找到稳定的匹配。
        # 注意到，每一个男性在这些匹配中都会获得不同的对象，而这些不同的对象里一定有一个让他自己最满意的。
        # 我们这里假设对任何一个男人，在所有的稳定匹配中，他可能匹配到的最满意的女人，就是他的真命天女。
        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)

        protoman = man.copy().scale(0.4).shift(3*DOWN+2*LEFT)
        zmtn = Text("的真命天女是", color=GREEN).next_to(protoman, RIGHT, buff=0.1)
        protowoman = woman.copy().scale(0.4).set_color(ORANGE).next_to(zmtn, RIGHT, buff=0.1)

        self.wait(2)
        self.play(Create(VGroup(protoman, zmtn, protowoman)))
        self.wait(3)
        # 而我们证明也非常简单，核心就两句话：命里有时终须有，命里若无莫强求。

        txt1 = Text("命里有时终须有", color=ORANGE).scale(2).shift(UP*2.5)
        txt2 = Text("命里若无莫强求", color=ORANGE).scale(2).next_to(txt1, DOWN)
        self.play(Write(txt1), run_time=2)
        self.play(Write(txt2), run_time=2)
        self.wait(6)
        self.play(FadeOut(VGroup(txt1, txt2)))

        # 在GS算法的流程中，每个人一定不可能和比真命天女更好的人在一起，但也一定不会错过真命天女。
        # 为什么？让我们来一步步跟随这GS算法的流程。
        # 在这个流程里，每个男人都会从自己最中意的女人开始表白，但这其中，绝大部分男人表白的都不是真命天女，而是癞蛤蟆想吃天鹅肉。


        # 当小帅向小美表白时，只要小美在小帅名单上的位置高于小帅的真命天女，那么在任何一个最终稳定的匹配中，小美都不可能和小帅走到最后。
        
        ht = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\heart.svg")
        cross = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\cross.svg")
        hb = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\Broken_heart.svg")

        man.scale(0.5).shift(UP*2 + LEFT)
        woman.scale(0.5).shift(UP*2 + RIGHT)
        ht.set_opacity(0.6).scale(0.5).shift(UP*2.5)
        self.play(Create(woman))
        
        hero = man.copy().set_color(BLUE).move_to(ORIGIN+DOWN*2)
        self.wait()
        self.play(Create(hero))
        self.play(hero.animate.move_to(woman.get_center()+DOWN))
        self.wait(2)
        self.play(Create(cross), run_time=2)

        # 原因很简单，如果小帅小美真能走到最后，我们又知道GS算法得到的一定是稳定匹配，
        self.wait(2)
        self.play(FadeOut(cross))
        self.play(hero.animate.move_to(ORIGIN+UP*2+LEFT), run_time=2)
        self.play(Create(ht))
        self.wait(3)
        # 那小美就成为了小帅心目中比真命天女更好的结局，这和真命天女是小帅在所有稳定匹配中可能得到的最满意的女生的【定义】矛盾。
        self.play(Indicate(woman))
        self.wait(2)
        
        rect = SurroundingRectangle(VGroup(protoman, zmtn, protowoman))
        self.play(Create(rect))
        self.wait(2)
        self.play(FadeOut(rect))

        # 这告诉了我们一个什么道理？正是：命里若无莫强求。
        # 那个拒绝你、甚至是甩了你的人，本来在任何一条世界线里，都不可能是你稳定的伴侣。
        # Ta要么早已经有了比你更好的对象，所以根本不会降格考虑你，
        # 要么即使现在接受了你，以后还是可能因为遇见更好的人去抛弃你。
        # 被拒绝或者被甩，其实是一种有益的筛选，
        # 帮你排除掉那些本来就不适合、或是镜花水月般不能走到最后的人。
        # 你应该做的，是大大方方地往前看、向前走，接着在你的列表名单中向后面的名字追求，
        # 那些拒绝和抛弃你的人从来就不可能属于你，没有必要伤心和难过。

        # 更没必要去做舔狗

        # 请注意，这不是简单的安慰、更不是心灵鸡汤，这是数学用严谨的逻辑推理告诉你的最优解。

class Proof2(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)
        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)
        cross = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\cross.svg")

        # 接下来，我们来证明“命里有时终须有”。刚才我们已经知道，GS算法的流程最终一定能得到稳定匹配，
        # 所以不可能有男人跟比自己真命天女更好的女人走到最后。
        # 可是，GS算法会不会让一些男人失去自己的真命天女呢？接下来的推导将会告诉你，放心，不会的。
        # 我们可以用反证法，假设存在这样一个倒霉蛋，我们叫他牛郎，他的真命天女是织女。
        niulang = man.copy().scale(0.5).shift(LEFT*3)
        nl_text = Text("牛郎", color=WHITE).scale(0.8).add_updater(lambda mob: mob.next_to(niulang, DOWN, buff=0.1))
        self.play(FadeIn(niulang), run_time=2)
        self.play(Write(nl_text))
        self.wait(3)
        # 牛郎是第一个在这个算法流程中失去了自己真命天女的人。
        zhinv = woman.copy().scale(0.5).shift(RIGHT*3)
        zhn_text = Text("织女", color=RED).scale(0.8).add_updater(lambda mob: mob.next_to(zhinv, DOWN, buff=0.1))
        self.play(FadeIn(zhinv), run_time=2)
        self.play(Write(zhn_text))
        self.wait(3)
        # 失去有两种，要么是当场被织女拒绝了，要么是被织女甩了。

        #### 还是用下面的reject和dump

        # 无论是哪种情况，我们都把时间定格在牛郎被迫离开织女的那一刻。
        laowang = niulang.copy().set_color(YELLOW).move_to(ORIGIN+UP*2+LEFT)
        lw_text = Text("老王", color=YELLOW).scale(0.8).add_updater(lambda mob: mob.next_to(laowang, DOWN, buff=0.1))

        ht = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\heart.svg").scale(0.6).shift(UP*2)
        self.play(zhinv.animate.move_to(ORIGIN+UP*2+RIGHT), 
                  niulang.animate.move_to(ORIGIN+DOWN*2),
                  run_time=2)
        self.wait(2)

        # 在这一刻，牛郎失去织女的原因，一定是因为织女身边有一个更好的男人，对吧？
        self.play(FadeIn(laowang), run_time=2)
        # 我们不妨叫这个男人老王。老王要么是早就捷足先登，导致织女看不上牛郎；要么，就是后来者居上，把牛郎赶走了。
        self.wait(2)
        self.play(Write(lw_text), run_time=1)
        self.wait(2)

        gr1 = laowang.copy().scale(0.6).move_to(ORIGIN + LEFT*5 + UP)
        gr_sign = MathTex(">", color=RED).next_to(gr1, RIGHT, buff=0.1)
        gr2 = niulang.copy().scale(0.6).next_to(gr_sign, RIGHT, buff=0.1)
        nt1 = Text("老王", color=YELLOW).scale(0.4).next_to(gr1, DOWN, buff=0.1)
        nt2 = Text("牛郎", color=WHITE).scale(0.4).next_to(gr2, DOWN, buff=0.1)
        zhn_prefer = VGroup(gr1, gr_sign, gr2, nt1, nt2)
        self.play(Create(zhn_prefer), run_time=2)

        self.wait(5)

        # 但接下来我们会证明，根本不可能有这样的老王，牛郎表白的时候不会有，之后在一起时也不会有人横刀夺爱。
        cr = cross.copy().move_to(laowang).set_opacity(0.8)
        self.play(Create(cr))
        self.wait(4)
        self.play(FadeOut(cr))
        self.wait(4)

        # 证明的关键在于注意一件事，牛郎是【第一个】失去自己真命天女的人。
        self.play(Indicate(niulang), run_time=2)
        self.wait(2)
        # 所以牛郎被抛弃或者拒绝的时候，和织女在一起的老王一定还没有失去自己的真命天女，因为牛郎是第一个倒霉蛋嘛。
        rect = SurroundingRectangle(laowang)
        self.play(Create(rect), run_time=2)
        self.wait(3)
        self.play(FadeOut(rect))
        self.wait(3)

        # 所以，织女要么是老王的真命天女，要么在老王的排名里比他的真命天女还要高。

        s1 = zhinv.copy().scale(0.6).move_to(ORIGIN + LEFT*6.5 + DOWN)
        s2 = MathTex(r"\geq", color=RED).next_to(s1, RIGHT, buff=0.1)
        s3 = zhinv.copy().set_color(ORANGE).scale(0.6).next_to(s2, RIGHT, buff=0.4)
        s4 = Text("老王真命天女", color=ORANGE).scale(0.4).next_to(s3, DOWN, buff=0.1)
        s5 = Text("织女", color=LIGHT_PINK).scale(0.4).next_to(s1, DOWN, buff=0.1)
        lw_prefer = VGroup(s1, s2, s3, s5, s4)
        self.play(Create(lw_prefer), run_time=2)
        self.wait(3)

        # 行吧，高就高呗，老王癞蛤蟆吃到了天鹅肉，还永久地拆散了牛郎织女，有什么问题吗？
        # 不，有问题，而且问题很大。这里我们需要记得另一件事，
        # 之所以织女能够成为牛郎的真命天女，是因为存在一个稳定匹配，
        wangsao = zhinv.copy().set_color(GREEN).move_to(ORIGIN + DOWN + RIGHT)
        ht.move_to(ORIGIN + UP)

        ht2 = ht.copy().shift(DOWN * 2)
        # 在那个美好的世界线里，牛郎和织女是匹配在一起的，而老王则安分的和王嫂在一起。
        self.play(
            niulang.animate.move_to(ORIGIN + UP*1.5 + LEFT),
            zhinv.animate.move_to(ORIGIN + UP*1.5 + RIGHT),
            laowang.animate.move_to(ORIGIN + DOWN + LEFT),
            run_time=2
        )
        self.wait()
        self.play(FadeIn(wangsao), FadeIn(ht), FadeIn(ht2), run_time=2)
        ws_text = Text("王嫂", color=LIGHT_BROWN).scale(0.8).add_updater(
            lambda mob: mob.next_to(wangsao, DOWN, buff=0.1)
        )
        self.play(Write(ws_text))

        # 可是，请注意我们写在左边的这两个条件：织女相比牛郎更喜欢老王，
        r1 = SurroundingRectangle(zhn_prefer)
        self.wait(4)
        self.play(Create(r1), run_time=2)
        self.wait(3)

        gg1 = MathTex(r">", color=RED).next_to(s3, RIGHT, buff=0.4)
        gg2 = wangsao.copy().scale(0.6).next_to(gg1, RIGHT, buff=0.1)
        gg3 = Text("王嫂", color=LIGHT_BROWN).scale(0.4).next_to(gg2, DOWN, buff=0.1)
        

        # 而我们刚才说了，织女要么是老王的真命天女、要么比老王的真命天女还要高，
        self.play(Indicate(lw_prefer), run_time=2)


        # 总而言之，织女在老王的心目中肯定比一个稳定匹配的王嫂要好（毕竟得不到的才是永远在骚动嘛）。
        self.play(Create(VGroup(gg1, gg2, gg3)))
        self.wait(3)

        r2 = SurroundingRectangle(VGroup(lw_prefer, gg1, gg2, gg3))
        self.play(Create(r2), run_time=2)
        self.wait(3)
        # 这里就出现了大问题，织女和老王此时在这个匹配中就成为了不稳定因素，他们会很容易私奔劈腿。

        self.play(
            niulang.animate.shift(LEFT),
            ht.animate.shift(LEFT),
            zhinv.animate.shift(LEFT),
            laowang.animate.shift(RIGHT),
            ht2.animate.shift(RIGHT),
            wangsao.animate.shift(RIGHT),
            run_time=2
        )
        self.wait()
        danger = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\danger.svg").scale(0.8).set_opacity(0.7)
        self.play(Create(danger), run_time=2)
        self.wait(3)
        
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        # 而我们说了，这整个匹配是一个稳定匹配，不可能有人想要私奔。
        # 终于，我们得到了矛盾。这个矛盾表明，老王是不存在的。牛郎一旦找到了织女，他就一定能和织女在一起，安稳地走到最后。
        self.wait(8)
        # 再重复一遍，牛郎一旦找到了织女，他就一定能和织女在一起，安稳地走到最后。这不是鸡汤，是数学定理。
        # 这，不就是“命里有时终须有”吗。


class Reject(Scene):
    def construct(self):
        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(YELLOW)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)
        ht = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\heart.svg")
        cross = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\cross.svg")
        hb = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\Broken_heart.svg")

        exp = Text("被拒", color=WHITE).shift(4*LEFT)
        self.add(exp)

        man.scale(0.5).shift(UP*2 + LEFT)
        woman.scale(0.5).shift(UP*2 + RIGHT)
        ht.set_opacity(0.6).scale(0.5).shift(UP*2.5)
        self.play(Create(man), Create(woman))
        self.play(Create(ht))
        
        hero = man.copy().set_color(BLUE).move_to(ORIGIN+DOWN*2)
        self.wait()
        self.play(Create(hero))
        self.play(hero.animate.move_to(woman.get_center()+DOWN))
        cross.scale(0.5).move_to(woman.get_center() + 0.5*DOWN)
        self.wait(0.5)
        self.play(Create(cross))
        self.wait(0.5)
        self.play(hero.animate.shift(DOWN*2))
        self.wait(0.5)
        hb.scale(0.5).set_opacity(0.7).move_to(hero)
        self.play(FadeIn(hb))
        self.wait()

class Dump(Scene):
    def construct(self):
        hero = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)
        ht = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\heart.svg")
        cross = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\cross.svg")
        hb = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\Broken_heart.svg")
        
        exp = Text("被甩", color=PURE_GREEN).shift(4*LEFT)
        self.add(exp)

        hero.scale(0.5).shift(UP*2 + LEFT)
        woman.scale(0.5).shift(UP*2 + RIGHT)
        ht.set_opacity(0.6).scale(0.5).shift(UP*2.5)
        man = hero.copy().set_color(YELLOW).move_to(ORIGIN+DOWN*2)

        self.play(Create(hero), Create(woman))
        self.play(Create(ht))
        
        
        self.wait()
        self.play(Create(man))
        self.play(man.animate.move_to(woman.get_center()+DOWN))
        cross.scale(0.5).move_to(woman.get_center() + 0.5*DOWN)
        self.wait(0.5)
        self.play(FadeOut(ht))
        self.play(hero.animate.move_to(ORIGIN+DOWN*2), man.animate.move_to(ORIGIN+UP*2 + LEFT))
        self.wait(0.5)
        hb.scale(0.5).set_opacity(0.7).next_to(hero, DOWN)
        self.play(FadeIn(ht))
        self.wait(0.5)
        _hero = hero.copy().set_color(PURE_GREEN)
        self.play(Transform(hero, _hero), FadeIn(hb))
        self.wait()


class LoveInClass(Scene):
    def construct(self):
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        title = Text("勇敢去追！被拒拉倒！", color=YELLOW).scale(2)
        self.play(Write(title), time=2)
        self.wait(2)
        self.play(FadeOut(title))
        
        # 我们最后来说最后一件简短但很有意思的事：阶级。
        self.wait(2)
        jieji = Text("阶级", color=GOLD).scale(2)
        self.play(Write(jieji))
        
        # 你知道吗，稳定婚姻算法中还潜藏着婚姻关系中阶级的秘密。
        self.wait(5)

        self.play(FadeOut(jieji))

        # 我们这里假设，根据外貌、个人能力、经济实力、家庭地位等等因素，
        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)
        
        men = VGroup(man.copy().scale(0.3).shift(LEFT*1.5+UP*2.4).set_color(YELLOW), 
                     man.copy().scale(0.3).shift(LEFT*1.5+UP*0.8).set_color(YELLOW), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*0.8), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*2.4)) 
        women = VGroup(woman.copy().scale(0.3).shift(RIGHT*1.5+UP*2.4).set_color(YELLOW), 
                       woman.copy().scale(0.3).shift(RIGHT*1.5+UP*0.8).set_color(YELLOW), 
                       woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*0.8), 
                       woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*2.4))
        M_sockets = [LEFT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]
        W_sockets = [RIGHT*1.2+UP*2.4+DOWN*i*1.6 for i in range(4)]

        self.play(LaggedStart(FadeIn(men), FadeIn(women)),
                  run_time=1)
        
        noteA = always_redraw(lambda: MathTex("A", color=ORANGE).scale(0.8).next_to(men[0], DOWN, buff=SMALL_BUFF))
        noteB = always_redraw(lambda: MathTex("B", color=ORANGE).scale(0.8).next_to(men[1], DOWN, buff=SMALL_BUFF))
        noteC = always_redraw(lambda: MathTex("C", color=ORANGE).scale(0.8).next_to(men[2], DOWN, buff=SMALL_BUFF))
        noteD = always_redraw(lambda: MathTex("D", color=ORANGE).scale(0.8).next_to(men[3], DOWN, buff=SMALL_BUFF))
        note_men = VGroup(noteA, noteB, noteC, noteD)

        note1 = always_redraw(lambda: MathTex("1", color=ORANGE).scale(0.8).next_to(women[0], DOWN, buff=SMALL_BUFF))
        note2 = always_redraw(lambda: MathTex("2", color=ORANGE).scale(0.8).next_to(women[1], DOWN, buff=SMALL_BUFF))
        note3 = always_redraw(lambda: MathTex("3", color=ORANGE).scale(0.8).next_to(women[2], DOWN, buff=SMALL_BUFF))
        note4 = always_redraw(lambda: MathTex("4", color=ORANGE).scale(0.8).next_to(women[3], DOWN, buff=SMALL_BUFF))
        note_women = VGroup(note1, note2, note3, note4)

        self.play(Create(note_men), Create(note_women))

        # 男性和女性群体中都各有k个人显著地高于剩余的n-k个人，我们称这部分人为“高阶级人群”。
        brace = Brace(men[0:2], LEFT, buff=SMALL_BUFF)
        t1 = Text("高富帅").set_color(YELLOW).next_to(brace, LEFT, buff=0.1)
        brace2 = Brace(women[0:2], RIGHT, buff=SMALL_BUFF)
        t2 = Text("白富美").set_color(YELLOW).next_to(brace2, RIGHT, buff=0.1)
        # 为了方便起见，我们假设男性和女性的数量是一样多的，都是n个人。
        self.wait(2)
        self.play(
            GrowFromCenter(brace),
            Create(t1),
            GrowFromCenter(brace2),
            Create(t2),
        )
        self.wait(4)
        self.play(FadeOut(brace), FadeOut(brace2), FadeOut(t1), FadeOut(t2))
        self.wait(5)
        # 这将体现在他们在异性心目中的排名上。无论男女，每一个人的排名里，
        # 尽管同一个阶级内部可能有不同的顺序，但都高阶级的对象一定排在剩余人的前面。

        highman = men[0].copy().move_to(ORIGIN+LEFT*6+UP*0.5)
        man_greater = MathTex(">", color=RED).next_to(highman, RIGHT, buff=0.1)
        lowman = men[2].copy().next_to(man_greater, RIGHT, buff=0.1)
        man_hirer = VGroup(highman, man_greater, lowman)

        highwoman = women[0].copy().move_to(ORIGIN+LEFT*6+DOWN*0.5)
        woman_greater = MathTex(">", color=RED).next_to(highwoman, RIGHT, buff=0.1)
        lowwoman = women[2].copy().next_to(woman_greater, RIGHT, buff=0.1)
        woman_hirer = VGroup(highwoman, woman_greater, lowwoman)

        self.play(Create(man_hirer), Create(woman_hirer), run_time=2 )

        self.wait(10)
        # 毕竟，是个人都想要自己的对象好看又有才华还有钱嘛。
        # 于是，这种阶级的排名会立刻导出一个结论：
        # 在稳定婚姻匹配里，高阶级的男人只会找高阶级的女人，而相对低阶级的男人只会找低阶级的女人。
        self.play(Circumscribe(VGroup(men[0], men[1], women[0], women[1])), run_time=2)
        self.wait()
        self.play(Circumscribe(VGroup(men[2], men[3], women[2], women[3])), run_time=2)

        # 为什么？假设这里有一个灰姑娘，她是低阶级的女人，但匹配上了高阶级的白马王子。
        rect = SurroundingRectangle(women[3], color=ORANGE)
        self.play(Create(rect))
        line1 = Line(M_sockets[0], W_sockets[3], color=YELLOW, stroke_width=4)
        self.wait()
        self.play(Create(line1), FadeOut(rect), run_time=2)
        self.wait(4)

        # 此时，因为高阶级的男性里跑出去了一个，所以高阶级男性的数量不足以匹配高阶级的女性。
        self.play(Circumscribe(VGroup(men[0], men[1])), run_time=2)

        # 因此，一定有一个高阶级的女性被迫和低阶级的男性匹配了。
        self.play(Indicate(women[1]))
        line2 = Line(M_sockets[2], W_sockets[1], color=YELLOW, stroke_width=4)
        self.wait()
        self.play(Create(line2), run_time=2)
        self.wait(2)

        # 现在我们就关注这四个人，因为我们知道，任何一个人都更喜欢高阶级的异性。
        self.play(
            FadeOut(VGroup(men[1], men[3], women[0], women[2], noteB,
                           noteD, note1, note3))
        )
        self.wait(2)
        self.play(Circumscribe(man_hirer), Circumscribe(woman_hirer), run_time=2)
        self.wait(3)
        # 所以，这两个跨越阶级的高阶级男女，彼此之间就都会觉得对方比自己现在的对象更好，
        self.play(Indicate(men[0]), Indicate(women[1]), run_time=2)
        newl = DashedLine(M_sockets[0], W_sockets[1], color=ORANGE, stroke_width=4)
        self.wait(2)
        self.play(Create(newl))
        self.wait(3)

        # 因此这个匹配一定是不稳定的。
        self.play(Uncreate(line1), Uncreate(line2), run_time=2)
        self.wait(3)
        
        # 换言之，所有的高阶级男女，一定会内部消化。
        newl2 = DashedLine(M_sockets[1], W_sockets[0], color=ORANGE, stroke_width=4)
        self.play(
            FadeIn(VGroup(men[1], men[3], women[0], women[2], noteB,
                           noteD, note1, note3)),
        )
        self.play(Create(newl2), run_time=2)
        self.wait(5)

        # 这个结论甚至对于更细致的阶级刻画也是成立的。

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        text_1 = Text("@漫士科普").scale(0.25).to_corner(UP+LEFT).shift(DOWN)
        text_2 = Text("仿冒必究",color=RED).scale(0.25).next_to(text_1, DOWN)
        self.add(text_1, text_2)

        man = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\man.svg").set_color(BLUE)
        woman = SVGMobject(r"C:\Users\Ray Lu\PycharmProjects\manim\project6_GS\woman.svg").set_color(LIGHT_PINK)
        men = VGroup(man.copy().scale(0.3).shift(LEFT*1.5+UP*2.5).set_color(YELLOW), 
                     man.copy().scale(0.3).shift(LEFT*1.5+UP*1.5).set_color(GREEN), 
                     man.copy().scale(0.3).shift(LEFT*1.5+UP*0.5).set_color(GREEN), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*0.5).set_color(GREEN), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*1.5).set_color(DARK_BROWN), 
                     man.copy().scale(0.3).shift(LEFT*1.5+DOWN*2.5).set_color(DARK_BROWN), 
                     ) 
        women = VGroup(woman.copy().scale(0.3).shift(RIGHT*1.5+UP*2.5).set_color(YELLOW), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+UP*1.5).set_color(GREEN), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+UP*0.5).set_color(GREEN), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*0.5).set_color(GREEN), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*1.5).set_color(DARK_BROWN), 
                     woman.copy().scale(0.3).shift(RIGHT*1.5+DOWN*2.5).set_color(DARK_BROWN))

        self.play(Create(men), Create(women), run_time=2)
        self.wait(2)

        M_sockets = [LEFT*1.2+UP*2.5+DOWN*i for i in range(6)]
        W_sockets = [RIGHT*1.2+UP*2.5+DOWN*i for i in range(6)]

        # 如果人群存在三六九等，而且大家择偶的顺序也是越高的越喜欢，
        a1 = men[0].copy().move_to(ORIGIN+LEFT*6+UP*0.5)
        a2 = MathTex(">", color=RED).next_to(a1, RIGHT, buff=0.1)
        a3 = men[2].copy().next_to(a2, RIGHT, buff=0.1)
        a4 = MathTex(">", color=RED).next_to(a3, RIGHT, buff=0.1)
        a5 = men[5].copy().next_to(a4, RIGHT, buff=0.1)
        man_hirer = VGroup(a1,a2,a3,a4,a5)

        b1 = women[0].copy().move_to(ORIGIN+LEFT*6+DOWN*0.5)
        b2 = MathTex(">", color=RED).next_to(b1, RIGHT, buff=0.1)
        b3 = women[2].copy().next_to(b2, RIGHT, buff=0.1)
        b4 = MathTex(">", color=RED).next_to(b3, RIGHT, buff=0.1)
        b5 = women[5].copy().next_to(b4, RIGHT, buff=0.1)
        woman_hirer = VGroup(b1,b2,b3,b4,b5)

        self.play(Create(man_hirer), Create(woman_hirer), run_time=2)

        # 那么最终的匹配结果，一定层次分明、等级森严。上等和上等匹配，中等和中等匹配，下等和下等匹配。
        l1 = Line(M_sockets[0], W_sockets[0], color=YELLOW, stroke_width=4)
        l2 = Line(M_sockets[1], W_sockets[2], color=YELLOW, stroke_width=4)
        l3 = Line(M_sockets[2], W_sockets[3], color=YELLOW, stroke_width=4)
        l4 = Line(M_sockets[3], W_sockets[1], color=YELLOW, stroke_width=4)
        l5 = Line(M_sockets[4], W_sockets[5], color=YELLOW, stroke_width=4)
        l6 = Line(M_sockets[5], W_sockets[4], color=YELLOW, stroke_width=4)
        self.wait(3)
        self.play(Create(VGroup(l1, l2, l3, l4, l5, l6)),
                  run_time=5, lag_ratio=0.5)

        seg1 = DashedLine(ORIGIN+LEFT*3+UP*2, ORIGIN+RIGHT*3+UP*2, color=YELLOW)
        seg2 = DashedLine(ORIGIN+LEFT*3+DOWN, ORIGIN+RIGHT*3+DOWN, color=BLUE)
        self.wait()
        self.play(Create(seg1), Create(seg2))

        self.wait(4)
        # 人类社会，门当户对，等级森严，由此可窥一斑。
        # 所以，如果你想要获得更好的伴侣，其实最关键的因素还是：提升自己，其次就是大胆去追。

class Q7(Scene):
    def construct(self):
        fm = Text("UP主的脸呢？", color=ORANGE).scale(1.5)
        self.play(FadeIn(fm))
        self.wait()
        self.play(FadeOut(fm))