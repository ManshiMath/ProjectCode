from manim import *
import numpy as np

class Lang(Scene):
    def construct(self):
        quest = Text("什么是语言的规律？", color=RED).scale(1.2)
        self.wait(0.5)
        self.play(
            Write(quest),
            run_time=1
        )
        self.wait(1)

class GPT(Scene):
    def construct(self):
        text = Text("Generative Pre-trained Transformer", color=BLUE).shift(UP*2)
        Chinesetrans = Text("生成式预训练变换器", color=BLUE).next_to(text, DOWN, buff=0.2)
        abbr = Text("GPT", font='heiti', color=YELLOW).scale(2).next_to(Chinesetrans, DOWN, buff=0.8)
        self.wait(0.5)
        self.play(
            Write(text),
            run_time=1
        )
        self.wait(0.2)
        self.play(
            Write(Chinesetrans),
            run_time=1
        )
        self.wait(2)
        self.play(
            Write(abbr),
            run_time=1
        )
        self.wait(1)

class Compute(Scene):
    def construct(self):
        text = MathTex(r"4\times 5=", "20").scale(2).set_color(YELLOW).shift(UP*2)
        text[0].set_color(BLUE)
        self.wait(0.5)
        self.play(Write(text[0]))
        self.wait(2)
        self.play(Write(text[1]))

        nlp_sentence = Text("女神说不聊天洗澡去了，我应该", font='heiti', color=BLUE).next_to(text, DOWN, buff=0.5)
        ques_mark = Text("?", font='heiti', color=YELLOW).next_to(nlp_sentence, RIGHT, buff=0.2)
        cursor = Text("_", font='heiti', color=WHITE).scale(1.2).next_to(nlp_sentence, RIGHT, buff=0.2).shift(DOWN*0.2)
        ques_mark.scale(1.5).next_to(cursor, DOWN, buff=0.3)

        self.wait(1)
        self.play(
            Write(nlp_sentence),
            run_time=1
        )
        self.add(cursor)
        self.play(
            Write(ques_mark),
            run_time=1
        )
        curser_light = ValueTracker(1.0)
        cursor.add_updater(lambda m: m.set_opacity(curser_light.get_value()))
        for _ in range(10):
            self.play(
                curser_light.animate.set_value(0),
                run_time=0.2
            )
            self.wait(0.3)
            self.play(
                curser_light.animate.set_value(1),
                run_time=0.2
            )
            self.wait(0.3)

class g1(Scene):
    def construct(self):
        title = Text("1-Gram Model", color=YELLOW).to_edge(UP)
        line = Line(start=LEFT*7, end=RIGHT*7).next_to(title, DOWN, buff=0.2)
        sent = VGroup()
        text = ["我","在","哪","里","面","条","件","下","的","话","就","…"]
        sent.add(Text(text[0], color=WHITE).scale(1.2).shift(LEFT*4))
        for i in text[1:]:
            sent.add(Text(i, color=WHITE).scale(1.2).next_to(sent[-1], RIGHT, buff=0.1))
        self.play(Write(title), GrowFromCenter(line))
        self.wait(0.5)
        # self.play(
        #     Write(sent),
        #     run_time=2
        # )
        rect = SurroundingRectangle(sent[0], color=YELLOW)
        self.play(Write(sent[0]), Create(rect), run_time=0.5)
        self.wait(0.5)

        # light = ValueTracker(1.0)
        # rect.add_updater(lambda m: m.set_opacity(light.get_value()))
        for i in range(1, len(sent)):
            self.play(
                Indicate(sent[i-1], color=YELLOW),
                run_time=0.6
            )
            self.play(
                Write(sent[i]),   
                run_time=0.4
            )
            self.play(rect.animate.become(SurroundingRectangle(sent[i], color=YELLOW)), run_time=0.2)
            self.wait(0.5)
        self.wait(1)

class g2(Scene):
    def construct(self):
        title = Text("2-Gram Model", color=YELLOW).to_edge(UP)
        line = Line(start=LEFT*7, end=RIGHT*7).next_to(title, DOWN, buff=0.2)
        sent = VGroup()
        text = ["我","们","都","会","发","生","事","情","很","复","杂","…"]
        sent.add(Text(text[0], color=WHITE).scale(1.2).shift(LEFT*4))
        for i in text[1:]:
            sent.add(Text(i, color=WHITE).scale(1.2).next_to(sent[-1], RIGHT, buff=0.1))
        self.play(Write(title), GrowFromCenter(line))
        self.wait(0.5)
        # self.play(
        #     Write(sent),
        #     run_time=2
        # )
        rect = SurroundingRectangle(sent[0:2], color=YELLOW)
        self.play(Write(sent[0:2]), Create(rect), run_time=0.5)
        self.wait(0.5)

        # light = ValueTracker(1.0)
        # rect.add_updater(lambda m: m.set_opacity(light.get_value()))
        for i in range(2, len(sent)):
            self.play(
                Indicate(sent[i-2:i], color=YELLOW),
                run_time=0.6
            )
            self.play(
                Write(sent[i]),   
                run_time=0.4
            )
            self.play(rect.animate.become(SurroundingRectangle(sent[i-1:i+1], color=YELLOW)), run_time=0.2)
            self.wait(0.5)
        self.wait(1)

class SM_all(Scene):
    def construct(self):
        title = Text("统计语言模型 Statistical Language Model", color=YELLOW).scale(0.8).to_edge(UP)
        line = Line(start=LEFT*7, end=RIGHT*7).next_to(title, DOWN, buff=0.2)
        # self.play(Write(title), GrowFromCenter(line))
        self.add(title, line)
        self.wait()

        text = ["东","风","来","了","，","春","天","的","脚","步","近","了","。"]
        sent = VGroup()
        sent.add(Text(text[0], color=GREEN).shift(LEFT*4))
        for i in text[1:]:
            sent.add(Text(i, color=GREEN).next_to(sent[-1], RIGHT, buff=0.1))
        
        rect = SurroundingRectangle(sent[0], color=YELLOW)
        self.play(Write(sent[0]), Create(rect), run_time=0.5)
        self.wait(0.5)

        for i in range(1, len(sent)):
            # self.play(
            #     Indicate(sent[0:i], color=YELLOW),
            #     run_time=0.6
            # )
            self.play(
                Write(sent[i]),   
                run_time=0.4
            )
            self.play(rect.animate.become(SurroundingRectangle(sent[0:i+1], color=YELLOW)), run_time=0.2)
            self.wait(0.4)
        self.wait(2)

class Tai(Scene):
    def construct(self):
        text1 = Text("她那时还太年轻，\n不知道所有礼物都在暗中标好了价格。", font='heiti', color=WHITE).scale(0.8).shift(UP+LEFT)
        text2 = Text("机关算尽太聪明，反误了卿卿性命。", font='kaiti', color=RED).scale(0.8).next_to(text1, DOWN, buff=0.8).shift(RIGHT)
        text3 = Text("\"太穷了，我家太穷了。\"福贵说。",  color=BLUE).scale(0.8).next_to(text2, DOWN, buff=0.8).shift(LEFT)
        etc = Text("……", font='heiti', color=YELLOW).scale(0.8).next_to(text3, DOWN, buff=0.8).shift(RIGHT*4)

        self.wait()
        self.play(LaggedStart(
            Write(text1),
            Write(text2),
            Write(text3),
            run_time=3
        ))
        self.wait(0.5)
        self.play(Write(etc))
        self.wait(5)

        grammar = Text("太+（形容词）", font='heiti', color=RED).scale(1.2).to_edge(UP)
        self.play(Write(grammar))
        self.wait(2)

    

class Jielong(Scene):
    def construct(self):

        nlp_sentence = Text("我的腿马上就软了，站在那里哆嗦起来，我说:\n“我只有一个儿子，求你行行好，救活他吧。\n医生点点头，表示知道了，可他又说:\n“你为什么", color=WHITE).shift(UP)
        ques_mark = Text("?", font='heiti', color=YELLOW).next_to(nlp_sentence, DOWN, buff=0.2).align_to(nlp_sentence, LEFT)
        cursor = Text("_", font='heiti', color=WHITE).next_to(ques_mark, DOWN, buff=0.3).align_to(nlp_sentence, LEFT)

        self.wait(1)
        self.play(
            Write(nlp_sentence),
            run_time=4
        )
        self.add(cursor)
        self.play(
            Write(ques_mark),
            run_time=0.5
        )
        curser_light = ValueTracker(1.0)
        cursor.add_updater(lambda m: m.set_opacity(curser_light.get_value()))
        for _ in range(6):
            self.play(
                curser_light.animate.set_value(0),
                run_time=0.2
            )
            self.wait(0.3)
            self.play(
                curser_light.animate.set_value(1),
                run_time=0.2
            )
            self.wait(0.3)
        
        result = Text("只生一个儿子", font='heiti', color=RED).next_to(nlp_sentence, DOWN, buff=0.2).align_to(nlp_sentence, LEFT)
        self.play(
            FadeOut(cursor),
            Transform(ques_mark, result), run_time=2
            )
        
        ref = Text("《活着》余华", font='heiti', color=YELLOW).scale(0.8).to_edge(DOWN+RIGHT).shift(UP)
        self.play(Write(ref))
        self.wait(2)


class SFT(Scene):
    def construct(self):
        text1 = Text("监督训练微调 Supervised Fintune", color=BLUE).scale(1.2).shift(UP*2)
        text2 = Text("人类反馈强化 RLHF", color=YELLOW).scale(1.2).next_to(text1, DOWN, buff=0.5)
        full = Text("Reinforcement Learning with Human Feedback", color=RED).next_to(text2, DOWN, buff=0.2)
        self.play(Write(text1))
        self.wait()
        self.play(Write(text2))
        self.wait(0.5)
        self.play(Write(full))
        self.wait(2)

class SFT_exp(Scene):
    def construct(self):
        # self.play(Write(title), GrowFromCenter(line))
        self.wait()

        text = ["冠心病","由","冠状","动脉","内","的","动脉","粥样","硬化","导致"]
        sent = VGroup()
        sent.add(Text(text[0], color=GREEN).shift(LEFT*4))
        for i in text[1:]:
            sent.add(Text(i, color=GREEN).next_to(sent[-1], RIGHT, buff=0.1))
        
        rect = SurroundingRectangle(sent[0], color=YELLOW)
        self.play(Write(sent[0]), Create(rect), run_time=0.5)
        self.wait(0.5)

        for i in range(1, len(sent)):
            # self.play(
            #     Indicate(sent[0:i], color=YELLOW),
            #     run_time=0.6
            # )
            self.play(
                Write(sent[i]),   
                run_time=0.4
            )
            self.play(rect.animate.become(SurroundingRectangle(sent[0:i+1], color=YELLOW)), run_time=0.2)
            self.wait(0.4)
        self.wait(2)