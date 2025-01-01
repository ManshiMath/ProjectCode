import numpy as np
from manim import *

class Video1(Scene):
    def construct(self):
        paper = SVGMobject("paper.svg").set_stroke(width=4).scale(0.5).set_color(GOLD)
        # number_list = [8, 11, 19, 23, 27, 33, 45, 55, 67, 98]
        # random permute number list
        number_list = [67, 19, 8, 98, 23, 33, 11, 27, 55, 45]

        def i2p(i, num=10, offset=UP*1.5):
            return ORIGIN + (i - num/2 +0.5) * RIGHT * 1.2 + offset

        # paper_list = [paper.copy().move_to(i2p(i)) for i in range(10)]
        paper_list = VGroup()
        for i in range(10):
            paper_list.add(paper.copy().move_to(i2p(i)))

        number_text_list = VGroup()
        for i in range(len(paper_list)):
            number_text_list.add(MathTex(str(number_list[i]), color=YELLOW).scale(0.8).set_stroke(width=2, color=GRAY, background=True).add_updater(lambda m, idx=i: m.next_to(paper_list[idx], UP, buff=0.3)))
        
        self.play(Create(paper_list), run_time=1)
        self.wait()
    
        self.play(
            Create(number_text_list), run_time=1.5
        )
        self.wait(5)

        # sort
        line = DashedLine(LEFT*7, RIGHT*7, color=WHITE, stroke_width=4)
        regionA = MathTex(r"A", color=RED).scale(2).set_stroke(width=2, color=GRAY, background=True).shift(UP*1.5 + LEFT*6.5)
        regionB = MathTex(r"B", color=BLUE).scale(2).set_stroke(width=2, color=GRAY, background=True).shift(DOWN*1.5 + LEFT*6.5)
        self.play(GrowFromCenter(line), run_time=1.5)
        self.play(Write(regionA), Write(regionB),
                  *[paper.animate.shift(RIGHT*0.5) for paper in paper_list],
                   run_time=1.5)
        self.wait(2)

        # Selection Sort procedure
        min_box = SurroundingRectangle(paper_list[0], color=GREEN, buff=0.1, corner_radius=0.1)
        scan_box = SurroundingRectangle(VGroup(paper_list[0], min_box), color=YELLOW, buff=0.1, corner_radius=0.2)
        min_sign = MathTex(r"\min", color=BLUE).scale(0.8).add_updater(lambda m: m.next_to(min_box, DOWN, buff=0.25))
        self.play(Create(scan_box), run_time=1)
        self.play(Create(min_box), run_time=1)
        self.play(Write(min_sign), run_time=1)
        self.wait()

        # save state for all objects
        paper_list.save_state()
        number_text_list.save_state()
        scan_box.save_state()
        min_box.save_state()

        A_list = list(range(10))
        B_list = []

        for i in range(10):
            min_value = number_list[A_list[0]]
            min_idx = 0
            wait_time = 2 if i == 0 else 0.5
            self.play(
                    scan_box.animate.move_to(paper_list[A_list[0]]), 
                    min_box.animate.move_to(paper_list[A_list[0]]),
                    run_time=0.5
                )
            self.wait(wait_time)
            for j in range(1, len(A_list)):
                self.play(scan_box.animate.move_to(paper_list[A_list[j]]), run_time=0.5)
                self.wait(0.5)
                if number_list[A_list[j]] < min_value:
                    min_value = number_list[A_list[j]]
                    min_idx = j
                    self.play(min_box.animate.move_to(paper_list[A_list[j]]), run_time=0.5)
                    self.wait(0.5)

            self.play(
                paper_list[A_list[min_idx]].animate.move_to(i2p(i, offset=DOWN*1.5)),
                run_time=wait_time
            )
            B_list.append(A_list.pop(min_idx))
            self.wait(wait_time)

        self.wait(3)
        
        self.play(
            LaggedStart(*[Indicate(paper_list[i], scale_factor=1.2) for i in B_list], lag_ratio=0.2),
        )

        # restore state
        self.play(
            Restore(paper_list),
            Restore(number_text_list),
            Restore(scan_box),
            Restore(min_box),
            run_time=2
        )
        self.wait(2)

        # # add a operation counter
        counter_num = ValueTracker(0)
        counter = DecimalNumber(0, color=WHITE, num_decimal_places=0).scale(2).set_stroke(width=2, color=GRAY, background=True).add_updater(lambda m: m.set_value(counter_num.get_value()))
        self.play(Create(counter), run_time=1)

        A_list = list(range(10))
        B_list = []

        for i in range(10):
            min_value = number_list[A_list[0]]
            min_idx = 0
            wait_time = 0.22
            self.play(
                    scan_box.animate.move_to(paper_list[A_list[0]]), 
                    min_box.animate.move_to(paper_list[A_list[0]]),
                    run_time=0.2
                )
            self.wait(wait_time)
            for j in range(1, len(A_list)):
                self.play(scan_box.animate.move_to(paper_list[A_list[j]]), 
                          counter_num.animate.increment_value(1.),
                          run_time=0.3)
                if number_list[A_list[j]] < min_value:
                    min_value = number_list[A_list[j]]
                    min_idx = j
                    self.play(
                        min_box.animate.move_to(paper_list[A_list[j]]), 
                        counter_num.animate.increment_value(1.),
                        run_time=0.2
                    )

            self.play(
                paper_list[A_list[min_idx]].animate.move_to(i2p(i, offset=DOWN*1.5)),
                run_time=wait_time
            )
            B_list.append(A_list.pop(min_idx))

        self.wait()
        self.play(Circumscribe(counter), run_time=1.5)
        self.wait(2)

class Combine(Scene):
    def construct(self):
        # Create 8 lines of different length representing 8 numbers
        lines = VGroup()
        len_list = [3, 9, 7, 2, 8, 4, 5, 10, 1, 6]
        def i2hor_off(i, num=10, gap=1, offset=ORIGIN):
            return (i - num/2 +0.5) * RIGHT * gap + offset
        
        for i in range(10):
            lines.add(Line(ORIGIN, UP*len_list[i]*0.25, color=WHITE, stroke_width=15).shift(i2hor_off(i)+UP))
        self.play(Create(lines), run_time=1.5)
        self.wait(2)

        x_mid = len_list[5]

        dline = DashedLine(ORIGIN, DOWN*5, color=ORANGE, stroke_width=4)
        self.play(Create(dline), run_time=1.5)

        pivot_line = lines[5].copy().set_color(RED).shift(i2hor_off(-1.5))
        lbl = Text("标准", font='heiti', color=YELLOW).scale(0.8).set_stroke(width=5, background=True).next_to(pivot_line, DOWN, buff=0.2)
        self.play(TransformFromCopy(lines[5], pivot_line), run_time=1.5)
        self.play(Write(lbl), run_time=1)
        self.wait(2)

        A_list = []
        A_list_values = []
        B_list = []
        B_list_values = []
        anchor_A = DOWN*2+LEFT*5+ORIGIN
        anchor_B = DOWN*2+RIGHT+ORIGIN
        anchor_line = pivot_line.copy().shift(DOWN*4)
        A_sign = MathTex(r"A", color=RED).scale(1.5).set_stroke(width=5, background=True).next_to(anchor_A, UP, buff=0.2)
        B_sign = MathTex(r"B", color=BLUE).scale(1.5).set_stroke(width=5, background=True).next_to(anchor_B, UP, buff=0.2)
        self.play(Write(A_sign), Write(B_sign), run_time=1)

        for i in range(10):
            if len_list[i] <= x_mid:
                self.play(lines[i].animate.next_to(pivot_line, RIGHT, buff=0.2).align_to(pivot_line, DOWN), run_time=0.5)
                self.wait(0.2)
                A_list.append(i)
                A_list_values.append(len_list[i])
                # move to A region
                _pos = lines[i].copy().move_to(anchor_A+RIGHT*len(A_list)*0.7).align_to(anchor_line, DOWN)
                self.play(lines[i].animate.move_to(_pos), run_time=0.3)
            else:
                self.play(lines[i].animate.next_to(pivot_line, RIGHT, buff=0.2).align_to(pivot_line, DOWN), run_time=0.5)
                self.wait(0.2)
                B_list.append(i)
                B_list_values.append(len_list[i])
                # move to B region
                _pos = lines[i].copy().move_to(anchor_B+RIGHT*len(B_list)*0.7).align_to(anchor_line, DOWN)
                self.play(lines[i].animate.move_to(_pos), run_time=0.3)
            self.wait(0.2)

        self.wait(2)
        self.play(
            FadeOut(pivot_line), FadeOut(lbl), 
            dline.animate.shift(UP*2.5),
            A_sign.animate.shift(UP*2.5),
            B_sign.animate.shift(UP*2.5),
            *[lines[i].animate.shift(UP*2.5) for i in range(10)],
            run_time=1)
        self.wait()
        anchor_A = LEFT*5+ORIGIN + UP*0.5
        anchor_B = RIGHT+ORIGIN  + UP*0.5
        anchor_line.shift(UP*2.5)
        # Rearrange the lines in A and B region to sort them
        A_arrange_map = np.argsort(A_list_values).tolist()
        B_arrange_map = np.argsort(B_list_values).tolist()
        A_arrange_map = [A_arrange_map.index(i) for i in range(len(A_list))]
        B_arrange_map = [B_arrange_map.index(i) for i in range(len(B_list))]
        print(A_arrange_map, B_arrange_map)
        self.play(
            *[lines[A_list[i]].animate.move_to(anchor_A+RIGHT*A_arrange_map[i]*0.7).align_to(anchor_line, DOWN) for i in range(len(A_list))],
            *[lines[B_list[i]].animate.move_to(anchor_B+RIGHT*B_arrange_map[i]*0.7).align_to(anchor_line, DOWN) for i in range(len(B_list))],
            run_time=1
        )
        self.wait(3)

        big_ques_mark = MathTex(r"?", color=GOLD).scale(5).set_stroke(width=5, background=True)
        self.play(Write(big_ques_mark), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(big_ques_mark), run_time=1)

        # FadeOut the dline, shift A_list lines towards RIGHT, B_list lines towards LEFT to come closer
        self.play(
            FadeOut(dline),
            FadeOut(A_sign), FadeOut(B_sign),
            *[lines[A_list[i]].animate.shift(RIGHT*1.2) for i in range(len(A_list))],
            *[lines[B_list[i]].animate.shift(LEFT*1.2) for i in range(len(B_list))],
            run_time=1
        )

        bright = ValueTracker(1.0)
        pivot_line.next_to(lines[5], RIGHT, buff=0.75).align_to(lines[0], DOWN).add_updater(lambda m: m.set_opacity(bright.get_value()))
        compare_line = DashedLine(pivot_line.get_end()+LEFT*4, pivot_line.get_end()+RIGHT*6, color=YELLOW, stroke_width=4)

        leq_lbl = MathTex(r"\leq", color=GREEN).scale(1.5).set_stroke(width=5, background=True).shift(DOWN*2+LEFT*1.5)
        pline1 = pivot_line.copy().next_to(leq_lbl, RIGHT, buff=0.4)
        sent1 = VGroup(leq_lbl, pline1)

        geq_lbl = MathTex(r">", color=RED).scale(1.5).set_stroke(width=5, background=True).shift(DOWN*2+RIGHT*1.5)
        pline2 = pivot_line.copy().next_to(geq_lbl, RIGHT, buff=0.4)
        sent2 = VGroup(geq_lbl, pline2)

        self.play(Create(sent1), Create(sent2), run_time=1.5)
        self.play(FadeIn(pivot_line), FadeIn(compare_line), run_time=1)
        self.play(bright.animate.set_value(0.), run_time=1, rate_func=there_and_back)
        self.play(bright.animate.set_value(0.), run_time=1, rate_func=there_and_back)
        self.play(bright.animate.set_value(0.), run_time=1, rate_func=there_and_back)
        self.play(bright.animate.set_value(0.), run_time=0.5)
        self.play(FadeOut(sent1), FadeOut(sent2), FadeOut(compare_line), run_time=1)

        self.play(
            *[lines[A_list[i]].animate.shift(RIGHT*0.4) for i in range(len(A_list))],
            *[lines[B_list[i]].animate.shift(LEFT*0.4) for i in range(len(B_list))],
            run_time=1.5
        )
        self.wait()
        rect = SurroundingRectangle(lines, color=YELLOW, buff=0.2)
        self.play(Create(rect), run_time=1.5)
        self.wait(2)

class Video2(Scene):
    def construct(self):
        paper = SVGMobject("paper.svg").set_stroke(width=4).scale(0.5).set_color(GOLD)
        # number_list = [8, 11, 19, 23, 27, 33, 45, 55, 67, 98]
        # random permute number list
        number_list = [67, 19, 8, 98, 23, 33, 11, 27, 55, 45]

        def i2p(i, num=10, offset=UP*1.5):
            return ORIGIN + (i - num/2 +0.5) * RIGHT * 1.2 + offset

        # paper_list = [paper.copy().move_to(i2p(i)) for i in range(10)]
        paper_list = VGroup()
        for i in range(10):
            paper_list.add(paper.copy().move_to(i2p(i, offset=UP*2)))

        number_text_list = VGroup()
        for i in range(len(paper_list)):
            number_text_list.add(MathTex(str(number_list[i]), color=YELLOW).scale(0.8).set_stroke(width=2, color=GRAY, background=True).add_updater(lambda m, idx=i: m.next_to(paper_list[idx], UP, buff=0.3)))
        
        self.play(Create(paper_list), Create(number_text_list), run_time=1.5)
        self.wait(2)

        line = DashedLine(LEFT*7, RIGHT*7, color=WHITE, stroke_width=4).shift(DOWN*1.5)
        regionA = MathTex(r"A", color=RED).scale(2).set_stroke(width=2, color=GRAY, background=True).shift(LEFT*6.5)
        regionB = MathTex(r"B", color=BLUE).scale(2).set_stroke(width=2, color=GRAY, background=True).shift(DOWN*3 + LEFT*6.5)

        self.play(GrowFromCenter(line), run_time=1.5)
        self.play(Write(regionA), Write(regionB), run_time=1)
        self.wait(2)

        # Quick Sort procedure
        pivot_box = SurroundingRectangle(VGroup(paper_list[5], number_text_list[5]), color=RED, buff=0.1, corner_radius=0.1)
        scan_box = SurroundingRectangle(paper_list[0], color=YELLOW, buff=0.1, corner_radius=0.2)
        xmid = number_list[5]
        pivot_sign = Text("标准=33", font='heiti', color=YELLOW).scale(0.8).shift(UP*2).set_stroke(width=5, background=True).add_background_rectangle()
        self.play(Create(pivot_box), Write(pivot_sign), run_time=1)
        self.wait()
        self.play(Create(scan_box), FadeOut(pivot_box), run_time=1)
        self.wait()

        A_list = []
        B_list = []

        for i in range(10):
            self.play(scan_box.animate.move_to(paper_list[i]), run_time=0.5)
            if number_list[i] <= xmid:
                A_list.append(i)
                self.play(paper_list[i].animate.move_to(i2p(len(A_list)-1, offset=0)), run_time=0.5)
            else:
                B_list.append(i)
                self.play(paper_list[i].animate.move_to(i2p(len(B_list)-1, offset=DOWN*3)), run_time=0.5)

            self.wait(0.5)
        self.wait(2)

        self.play(FadeOut(scan_box), FadeOut(pivot_sign), run_time=1.5)
        self.wait(2)

        # Recursive solve
        self.play(
            *[FadeOut(paper_list[i]) for i in B_list],
            *[FadeOut(number_text_list[i]) for i in B_list],
            run_time=1.5
        )
        self.wait(2)
        rect = SurroundingRectangle(VGroup(*[paper_list[i] for i in A_list]), color=YELLOW, buff=0.1)
        self.play(Create(rect), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(rect), run_time=1)
        self.wait(2)

        _paper_list = VGroup()
        _number_text_list = VGroup()
        for i in range(len(A_list)):
            _paper_list.add(paper_list[A_list[i]])#.copy().move_to(i2p(i, num=len(A_list), offset=UP*2)))
            _number_text_list.add(number_text_list[A_list[i]])
        
        self.play(
            *[paper.animate.move_to(i2p(i, num=len(A_list), offset=UP*2.5)) for i, paper in enumerate(_paper_list)],
            run_time=1.5
        )
        # Recursive divide and conquer
        pivot_box = SurroundingRectangle(VGroup(_paper_list[2], _number_text_list[2]), color=RED, buff=0.1, corner_radius=0.1)
        scan_box = SurroundingRectangle(_paper_list[0], color=YELLOW, buff=0.1, corner_radius=0.2)
        xmid = number_list[A_list[2]]
        pivot_sign = Text("标准=23", font='heiti', color=YELLOW).scale(0.8).shift(UP*2).set_stroke(width=5, background=True).add_background_rectangle()
        self.play(Create(pivot_box), Write(pivot_sign), run_time=1)
        self.play(Create(scan_box), FadeOut(pivot_box), run_time=1)
        self.wait()

        _A_list = []
        _B_list = []
        for i in range(len(_paper_list)):
            self.play(scan_box.animate.move_to(_paper_list[i]), run_time=0.5)
            if number_list[A_list[i]] <= xmid:
                _A_list.append(i)
                self.play(_paper_list[i].animate.move_to(i2p(len(_A_list)-1, offset=0)), run_time=0.3)
            else:
                _B_list.append(i)
                self.play(_paper_list[i].animate.move_to(i2p(len(_B_list)-1, offset=DOWN*3)), run_time=0.3)

            self.wait(0.2)
        
        self.wait(2)

class Video3(Scene):
    def construct(self):
        list1 = [67, 19, 8, 98, 23, 33, 11, 27, 55, 45]
        list2 = [19, 8, 23, 33, 11, 27, 0, 67, 98, 55, 45]
        # list3 = [[19, 8, 23, 11], [33, 27], [55, 45], [67, 98]]
        list3 = [19, 8, 23, 11, 0, 33, 27, 0,  55, 45, 0, 67, 98]
        # list4 = [[8, 11], [19, 23], [33], [27], [45], [55], [67],[98]]
        list4 = [8, 11, 0, 19, 23, 0, 33, 0, 27, 0, 45, 0, 55, 0, 67, 0, 98]
        # list5 = [[8], [11], [19], [23], [33], [27], [45], [55], [67],[98]]
        list5 = [8, 0, 11, 0, 19, 0, 23, 0, 33, 0, 27, 0, 45, 0, 55, 0, 67, 0, 98]
        
        def i2p(i, num=10, gap=1, offset=ORIGIN):
            return (i - num/2 +0.5) * RIGHT * gap + offset
        
        texg1 = VGroup()
        gap_sum = 0
        st_pos = i2p(0, offset=UP*3, gap=0.8, num=min(len(list1), 15))
        for i in range(len(list1)):
            if list1[i] > 0:
                texg1.add(MathTex(str(list1[i]), color=YELLOW).scale(0.8).set_stroke(width=1, color=GRAY, background=True).move_to(st_pos+gap_sum*RIGHT))
                gap_sum += 0.8
            else:
                gap_sum += 0.4
            
        texg2 = VGroup()
        gap_sum = 0
        st_pos = i2p(0, offset=UP*1.5, gap=0.8, num=min(len(list2), 15))
        seglist2 = [[]]
        for i in range(len(list2)):
            if list2[i] > 0:
                texg2.add(MathTex(str(list2[i]), color=YELLOW).scale(0.8).set_stroke(width=1, color=GRAY, background=True).move_to(st_pos+gap_sum*RIGHT))
                gap_sum += 0.8
                seglist2[-1].append(len(texg2)-1)
            else:
                gap_sum += 0.4
                seglist2.append([])
        
        texg3 = VGroup()
        gap_sum = 0
        st_pos = i2p(0, offset=UP*0, gap=0.8, num=min(len(list3), 15))
        seglist3 = [[]]
        for i in range(len(list3)):
            if list3[i] > 0:
                texg3.add(MathTex(str(list3[i]), color=YELLOW).scale(0.8).set_stroke(width=1, color=GRAY, background=True).move_to(st_pos+gap_sum*RIGHT))
                gap_sum += 0.8
                seglist3[-1].append(len(texg3)-1)
            else:
                gap_sum += 0.4
                seglist3.append([])
        
        texg4 = VGroup()
        gap_sum = 0
        st_pos = i2p(0, offset=DOWN * 1.5, gap=0.8, num=min(len(list4), 15))
        seglist4 = [[]]
        for i in range(len(list4)):
            if list4[i] > 0:
                texg4.add(MathTex(str(list4[i]), color=YELLOW).scale(0.8).set_stroke(width=1, color=GRAY, background=True).move_to(st_pos+gap_sum*RIGHT))
                gap_sum += 0.8
                seglist4[-1].append(len(texg4)-1)
            else:
                gap_sum += 0.4
                seglist4.append([])

        texg5 = VGroup()
        gap_sum = 0
        st_pos = i2p(0, offset=DOWN*3, gap=0.8, num=min(len(list5), 15))
        seglist5 = [[]]
        for i in range(len(list5)):
            if list5[i] > 0:
                texg5.add(MathTex(str(list5[i]), color=YELLOW).scale(0.8).set_stroke(width=1, color=GRAY, background=True).move_to(st_pos+gap_sum*RIGHT))
                gap_sum += 0.8
                seglist5[-1].append(len(texg5)-1)
            else:
                gap_sum += 0.4
                seglist5.append([])

        # remove all zeros in all lists
        _list1 = [i for i in list1 if i > 0]
        _list2 = [i for i in list2 if i > 0]
        _list3 = [i for i in list3 if i > 0]
        _list4 = [i for i in list4 if i > 0]
        _list5 = [i for i in list5 if i > 0]
        # Build idx mapping from list1 to list2
        map12 = [_list1.index(_list2[i]) for i in range(len(_list2)) if _list2[i] > 0]
        map23 = [_list2.index(_list3[i]) for i in range(len(_list3)) if _list3[i] > 0]
        map34 = [_list3.index(_list4[i]) for i in range(len(_list4)) if _list4[i] > 0]
        map45 = [_list4.index(_list5[i]) for i in range(len(_list5)) if _list5[i] > 0]

        back_rect = SurroundingRectangle(texg1, color=BLUE, buff=0.2)
        self.play(Create(texg1), run_time=1)
        self.play(FadeIn(back_rect), run_time=1)
        self.wait(2)

        # transform list1 to list2
        rect_group = VGroup()
        line_group = VGroup()
        print(seglist2)
        print(map12)

        self.play(
            LaggedStart(
                *[TransformFromCopy(texg1[map12[i]], texg2[i]) for i in range(len(map12))],
                run_time=3, lag_ratio=0.3
            )
        )
        self.wait()
        for seg in seglist2:
            # Transfrom from copy of list1 to seg of list2   
            rect_group.add(SurroundingRectangle(VGroup(*[texg2[i] for i in seg]), color=BLUE, buff=0.2))
            line_group.add(Line(back_rect.get_bottom(), rect_group[-1].get_top(), color=ORANGE, stroke_width=4))
            self.play(Create(rect_group[-1]), Create(line_group[-1]), run_time=1)
            self.wait(0.5)
        self.wait(2)

        # transform list2 to list3
        self.play(
            LaggedStart(
                *[TransformFromCopy(texg2[map23[i]], texg3[i]) for i in seglist3[0]],
                *[TransformFromCopy(texg2[map23[i]], texg3[i]) for i in seglist3[1]],
                run_time=3, lag_ratio=0.3
            )
        )
        self.wait()
        rect_group.add(SurroundingRectangle(VGroup(*[texg3[i] for i in seglist3[0]]), color=BLUE, buff=0.2))
        line_group.add(Line(rect_group[-3].get_bottom(), rect_group[-1].get_top(), color=ORANGE, stroke_width=4))
        self.play(Create(rect_group[-1]), Create(line_group[-1]), run_time=1)
        self.wait(0.5)

        rect_group.add(SurroundingRectangle(VGroup(*[texg3[i] for i in seglist3[1]]), color=BLUE, buff=0.2))
        line_group.add(Line(rect_group[-4].get_bottom(), rect_group[-1].get_top(), color=ORANGE, stroke_width=4))
        self.play(Create(rect_group[-1]), Create(line_group[-1]), run_time=1)
        self.wait()

        self.play(
            LaggedStart(
                *[TransformFromCopy(texg2[map23[i]], texg3[i]) for i in seglist3[2]],
                *[TransformFromCopy(texg2[map23[i]], texg3[i]) for i in seglist3[3]],
                run_time=3, lag_ratio=0.3
            )
        )

        rect_group.add(SurroundingRectangle(VGroup(*[texg3[i] for i in seglist3[2]]), color=BLUE, buff=0.2))
        line_group.add(Line(rect_group[-4].get_bottom(), rect_group[-1].get_top(), color=ORANGE, stroke_width=4))
        self.play(Create(rect_group[-1]), Create(line_group[-1]), run_time=1)
        self.wait(0.5)

        rect_group.add(SurroundingRectangle(VGroup(*[texg3[i] for i in seglist3[3]]), color=BLUE, buff=0.2))
        line_group.add(Line(rect_group[-5].get_bottom(), rect_group[-1].get_top(), color=ORANGE, stroke_width=4))
        self.play(Create(rect_group[-1]), Create(line_group[-1]), run_time=1)
        self.wait()

        
        # transform list3 to list4

        self.play(
            LaggedStart(
                *[TransformFromCopy(texg3[map34[i]], texg4[i]) for i in range(len(map34))],
                run_time=2, lag_ratio=0.3
            )
        )
        self.wait()
        cnt = 1
        for seg in seglist4:
            rect_group.add(SurroundingRectangle(VGroup(*[texg4[i] for i in seg]), color=BLUE, buff=0.2))
            line_group.add(Line(rect_group[-5-cnt//2].get_bottom(), rect_group[-1].get_top(), color=ORANGE, stroke_width=4))
            cnt += 1
        self.play(Create(rect_group[-8:]), Create(line_group[-8:]), run_time=1.5)
        self.wait(2)

        self.play(
            LaggedStart(
                *[TransformFromCopy(texg4[map45[i]], texg5[i]) for i in range(len(map45))],
                run_time=2, lag_ratio=0.3
            )
        )
        self.wait(2)
        self.play(
            LaggedStart(
            *[Indicate(m) for m in texg5],
            lag_ratio=0.5, run_time=3
            )
        )

        count_lbl = VGroup()
        count_lbl.add(MathTex(r"10", color=WHITE).scale(1.5).set_stroke(width=5, background=True).next_to(texg1, LEFT, buff=0.5))
        count_lbl.add(MathTex(r"10", color=WHITE).scale(1.5).set_stroke(width=5, background=True).next_to(texg2, LEFT, buff=0.5))
        count_lbl.add(MathTex(r"10", color=WHITE).scale(1.5).set_stroke(width=5, background=True).next_to(texg3, LEFT, buff=0.5))
        count_lbl.add(MathTex(r"2", color=WHITE).scale(1.5).set_stroke(width=5, background=True).next_to(texg4, LEFT, buff=0.5))
        
        self.play(Create(count_lbl), run_time=2)
        self.wait()
        total32 = MathTex(r"10+10+10+2=32", color=YELLOW).scale(2.5).set_stroke(width=5, background=True).add_background_rectangle()
        self.play(Write(total32), run_time=2)

        # Clear all objects
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5
        )
        self.wait()

        neq100 = MathTex(r"n=1000", color=YELLOW).scale(2).set_stroke(width=5, background=True).to_edge(UP)

        select_sort = Text("选择排序:", font='heiti', color=WHITE).set_stroke(width=5, background=True).shift(LEFT*5)
        select_sort_formula = MathTex(r"\frac{n(n-1)}{2}=499500", color=YELLOW).set_stroke(width=5, background=True).align_to(select_sort, DOWN)

        quick_sort = Text("快速排序:", font='heiti', color=BLUE).set_stroke(width=5, background=True).next_to(select_sort, DOWN, buff=0.8)
        quick_sort_formula = MathTex(r"n\log_2 n \approx 10000", color=YELLOW).set_stroke(width=5, background=True).align_to(quick_sort, DOWN)

        self.play(Write(neq100), run_time=1)
        self.wait()
        self.play(Write(select_sort), Write(select_sort_formula), run_time=1.5)
        self.wait()
        self.play(Write(quick_sort), Write(quick_sort_formula), run_time=1.5)
        self.wait(2)

        rect1 = SurroundingRectangle(select_sort_formula, color=WHITE, buff=0.2)
        rect2 = SurroundingRectangle(quick_sort_formula, color=WHITE, buff=0.2)
        fifty_times = Text("50倍!", font='heiti', color=RED).set_stroke(width=5, background=True).next_to(rect1, RIGHT, buff=0.8)
        self.play(Create(rect1), Create(rect2), Write(fifty_times), run_time=1.5)
        self.wait(2)

class Video4(Scene):
    def construct(self):
        # Create a 8x8 grid
        def i2p(i, j, num=8, gap=0.8, offset=ORIGIN):
            return (j - num/2 + 0.5) * RIGHT * gap + (i - num/2 +0.5) * DOWN * gap + offset
        def idx2ij(idx, num=8):
            return idx // num, idx % num
        def ij2idx(i, j, num=8):
            return i * num + j
        
        sq_list = VGroup()
        for i in range(8):
            for j in range(8):
                sq_list.add(Square(side_length=0.8, color=BLACK, stroke_width=3).set_fill(color=WHITE, opacity=0.8).shift(i2p(i, j)))
        
        self.play(Create(sq_list), run_time=1.5)
        self.wait(3)

        self.play(
            sq_list[ij2idx(2, 5)].animate.set_fill(color=BLACK, opacity=0.9),
            run_time=1.5
        )
        blk0 = VGroup(
            sq_list[ij2idx(3, 3)].copy().set_fill(color=PURPLE, opacity=0.9),
            sq_list[ij2idx(3, 4)].copy().set_fill(color=PURPLE, opacity=0.9),
            sq_list[ij2idx(4, 3)].copy().set_fill(color=PURPLE, opacity=0.9),
        )

        tile1 = VGroup(
            sq_list[ij2idx(3, 3)].copy().set_fill(color=RED, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(3, 4)].copy().set_fill(color=RED, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(4, 3)].copy().set_fill(color=RED, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            Line(sq_list[ij2idx(3, 3)].get_center(), sq_list[ij2idx(3, 4)].get_center(), color=DARKER_GRAY, stroke_width=5),
            Line(sq_list[ij2idx(3, 3)].get_center(), sq_list[ij2idx(4, 3)].get_center(), color=DARKER_GRAY, stroke_width=5)
        ).to_edge(LEFT).shift(UP*2)
        tile2 = VGroup(
            sq_list[ij2idx(3, 3)].copy().set_fill(color=BLUE, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(4, 4)].copy().set_fill(color=BLUE, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(4, 3)].copy().set_fill(color=BLUE, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            Line(sq_list[ij2idx(4, 3)].get_center(), sq_list[ij2idx(4, 4)].get_center(), color=DARKER_GRAY, stroke_width=5),
            Line(sq_list[ij2idx(4, 3)].get_center(), sq_list[ij2idx(3, 3)].get_center(), color=DARKER_GRAY, stroke_width=5)
        ).to_edge(LEFT).shift(DOWN*2)
        tile3 = VGroup(
            sq_list[ij2idx(3, 3)].copy().set_fill(color=GREEN, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(3, 4)].copy().set_fill(color=GREEN, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(4, 4)].copy().set_fill(color=GREEN, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            Line(sq_list[ij2idx(3, 4)].get_center(), sq_list[ij2idx(4, 4)].get_center(), color=DARKER_GRAY, stroke_width=5),
            Line(sq_list[ij2idx(3, 4)].get_center(), sq_list[ij2idx(3, 3)].get_center(), color=DARKER_GRAY, stroke_width=5)
        ).to_edge(RIGHT).shift(UP*2)
        tile4 = VGroup(
            sq_list[ij2idx(3, 4)].copy().set_fill(color=YELLOW, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(4, 4)].copy().set_fill(color=YELLOW, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            sq_list[ij2idx(4, 3)].copy().set_fill(color=YELLOW, opacity=0.9).set_stroke(width=5, color=DARK_BROWN),
            Line(sq_list[ij2idx(4, 4)].get_center(), sq_list[ij2idx(4, 3)].get_center(), color=DARKER_GRAY, stroke_width=5),
            Line(sq_list[ij2idx(4, 4)].get_center(), sq_list[ij2idx(3, 4)].get_center(), color=DARKER_GRAY, stroke_width=5),
        ).to_edge(RIGHT).shift(DOWN*2)
        self.play(FadeIn(tile1), FadeIn(tile2), FadeIn(tile3), FadeIn(tile4), run_time=2)
        self.wait(4)

        hl1 = DashedLine(LEFT*5, RIGHT*5, color=ORANGE, stroke_width=5)
        vl1 = DashedLine(UP*5, DOWN*5, color=ORANGE, stroke_width=5)
        self.play(Create(hl1), Create(vl1), run_time=1.5)
        self.wait(2)
    
        self.play(FadeIn(blk0), run_time=1)
        self.wait(2)

        state_color_map = [RED, BLUE, GREEN, YELLOW]
        state = 0
        for _ in range(3):
            state = (state + 3) % 4
            self.play(
                Rotate(blk0, angle=-PI/2, about_point=ORIGIN),
                run_time=0.5
            )
            self.wait(0.5)

        big_rect = Square(side_length=3.5, color=YELLOW, stroke_width=4).shift(i2p(1.5, 1.5))
        self.wait(3)
        dark_list = [i for i in range(64) if not(i // 8 < 4 and i % 8 < 4)]
        self.play(
            *[sq_list[i].animate.set_opacity(0.2) for i in dark_list],
            run_time=1.5
        )
        self.wait(2)
        self.play(Create(big_rect), run_time=1.5)
        same_sub_problem = Text("同样的子问题!", font='heiti', color=YELLOW).set_stroke(width=5, background=True).next_to(big_rect, RIGHT, buff=0.2)
        self.play(Write(same_sub_problem), run_time=1)
        self.wait(2)
        # restore the opacity
        self.play(
            *[sq_list[i].animate.set_opacity(0.8) for i in dark_list],
            FadeOut(same_sub_problem),
            run_time=1.5
        )
        self.wait()

        # show same problem for other 3 quadrants
        dark_list2 = [i for i in range(64) if not(i // 8 < 4 and i % 8 >= 4)]
        self.play(
            *[sq_list[i].animate.set_opacity(0.2) for i in dark_list2],
            big_rect.animate.move_to(i2p(1.5, 5.5)),
            run_time=1
        )
        self.wait(0.5)
        dark_list3 = [i for i in range(64) if not(i // 8 >= 4 and i % 8 < 4)]
        self.play(
            *[sq_list[i].animate.set_opacity(0.2) for i in dark_list3],
            *[sq_list[i].animate.set_opacity(0.8) for i in range(64) if i not in dark_list3],
            big_rect.animate.move_to(i2p(5.5, 1.5)),
            run_time=1
        )
        self.wait(0.5)
        dark_list4 = [i for i in range(64) if not(i // 8 >= 4 and i % 8 >= 4)]
        self.play(
            *[sq_list[i].animate.set_opacity(0.2) for i in dark_list4],
            *[sq_list[i].animate.set_opacity(0.8) for i in range(64) if i not in dark_list4],
            big_rect.animate.move_to(i2p(5.5, 5.5)),
            run_time=1
        )
        self.wait()
        self.play(
            FadeOut(big_rect),
            *[sq_list[i].animate.set_opacity(0.8) for i in range(64)],
        )

        self.play(
            FadeOut(blk0), 
            FadeOut(hl1), FadeOut(vl1),
            run_time=1)
        
        solution_list = VGroup()
        def solve(x, y, s, dx, dy):
            """ Divide and Conquer for (x, x+s) and (y, y+s) 
            The hole is at (dx, dy)
            select the tile that combine with the hole can cover each quadrant
            the recursive call for the 4 quadrants
            """
            
            if s == 1:
                return
            # Decide the tile that can cover the hole with correct position
            print(x, y, s, dx, dy)
            if dx >= x + s//2 and dy >= y + s//2: # hole at 4th quadrant, use tile1
                print(f"find tile1 at {x+s//2}, {y+s//2}")
                solution_list.add(tile1.copy().align_to(sq_list[ij2idx(x+s//2-1, y+s//2-1)], UP+LEFT))
                case = 1
            elif dx >= x + s//2 and dy < y + s//2: # hole at 3rd quadrant, use tile3
                print(f"find tile3 at {x+s//2}, {y+s//2+1}")
                solution_list.add(tile3.copy().align_to(sq_list[ij2idx(x+s//2-1, y+s//2)], UP+RIGHT))
                case = 3
            elif dx < x + s//2 and dy >= y + s//2: # hole at 2nd quadrant, use tile2
                print(f"find tile2 at {x+s//2+1}, {y+s//2}")
                solution_list.add(tile2.copy().align_to(sq_list[ij2idx(x+s//2, y+s//2-1)], DOWN+LEFT))
                case = 2
            elif dx < x + s//2 and dy < y + s//2: # hole at 1st quadrant, use tile2
                print(f"find tile4 at {x+s//2+1}, {y+s//2+1}")
                solution_list.add(tile4.copy().align_to(sq_list[ij2idx(x+s//2, y+s//2)], DOWN+RIGHT))
                case = 4
            else:
                print("Error!")
                return
            rect = SurroundingRectangle(VGroup(*[sq_list[ij2idx(i, j)] for i in range(x, x+s) for j in range(y, y+s)]), color=YELLOW, buff=0.2)
            hline = DashedLine(rect.get_left(), rect.get_right(), color=ORANGE, stroke_width=4)
            vline = DashedLine(rect.get_top(), rect.get_bottom(), color=ORANGE, stroke_width=4)
            self.play(Create(rect), Create(hline), Create(vline), run_time=0.25)
            self.play(FadeIn(solution_list[-1]), run_time=0.5)
            self.wait(0.1)
            self.play(FadeOut(rect), FadeOut(hline), FadeOut(vline), run_time=0.25)
            # Recursive call for 4 quadrants
            if case == 1:
                solve(x, y, s//2, x+s//2-1, y+s//2-1)
                solve(x, y+s//2, s//2, x+s//2-1, y+s//2)
                solve(x+s//2, y, s//2, x+s//2, y+s//2-1)
                solve(x+s//2, y+s//2, s//2, dx, dy)
            elif case == 2:
                solve(x, y, s//2, x+s//2-1, y+s//2-1)
                solve(x, y+s//2, s//2, dx, dy)
                solve(x+s//2, y, s//2, x+s//2, y+s//2-1)
                solve(x+s//2, y+s//2, s//2, x+s//2, y+s//2)
            elif case == 3:
                solve(x, y, s//2, x+s//2-1, y+s//2-1)
                solve(x, y+s//2, s//2, x+s//2-1, y+s//2)
                solve(x+s//2, y, s//2, dx, dy)
                solve(x+s//2, y+s//2, s//2, x+s//2, y+s//2)
            else:
                solve(x, y, s//2, dx, dy)
                solve(x, y+s//2, s//2, x+s//2-1, y+s//2)
                solve(x+s//2, y, s//2, x+s//2, y+s//2-1)
                solve(x+s//2, y+s//2, s//2, x+s//2, y+s//2)

        solve(0, 0, 8, 2, 5)
                
        # group1 = solution_list[0]
        # group1 = VGroup(solution_list[0])
        # # group2 = solution_list[1, 6, 11, 16]
        # group2 = VGroup(*[solution_list[i] for i in [1, 6, 11, 16]])
        # idx = [i for i in range(len(solution_list)) if i not in [0, 1, 6, 11, 16]]
        # group3 = VGroup(*[solution_list[i] for i in idx])

        # self.play(LaggedStart(*[FadeIn(m) for m in group1], run_time=1))
        # self.wait()
        # self.play(LaggedStart(*[FadeIn(m) for m in group2], run_time=1.5))
        # self.wait()
        # self.play(LaggedStart(*[FadeIn(m) for m in group3], run_time=2))
        # self.wait(2)
