from manim import *
import numpy as np

def a_to_b_mod_p(a, b, p):
    # fast power
    if b == 0:
        return 1
    if b % 2 == 0:
        return a_to_b_mod_p(a*a%p, b//2, p)
    else:
        return a*a_to_b_mod_p(a*a%p, b//2, p) % p

class AliceBob(Scene):
    def construct(self):
        alice = SVGMobject("woman.svg").scale(0.8).set_color(PINK)
        bob = SVGMobject("man.svg").scale(0.8).set_color(BLUE)
        eve = SVGMobject("man.svg").scale(0.8).set_color(GREEN)

        alice.shift(RIGHT*3.5)
        bob.shift(LEFT*3.5)

        self.play(FadeIn(alice), FadeIn(bob))
        self.wait(2)

        # 注意看，这里有一个小伙子叫小帅，他喜欢的姑娘叫小美。
        # 马上就要放寒假了，小帅想要向小美表白，这堂最后的语文课是他唯一的机会。
        heart = SVGMobject("heart.svg").scale(0.8).set_color(RED)
        self.play(FadeIn(heart))
        self.wait(2)
        self.play(FadeOut(heart))
        self.wait(2)

        # 为此，小帅准备了一串数字x=5201314想要表明自己的心意。
        msg = MathTex("5201314").scale(1.5).shift(UP*2).set_color(RED)
        self.play(Write(msg), run_time=2)
        self.wait(2)
        paper = Rectangle(width=6, height=2).move_to(msg).set_fill(GOLD_D, opacity=0.3).set_stroke(width=0.)
        paper.add_to_back()
        
        self.play(FadeIn(paper), run_time=1)
        self.wait(2)

        _paper = paper.copy().scale(0.5).shift(LEFT*5)
        _msg = msg.copy().scale(0.5).move_to(_paper)

        # 但是问题来了，在课堂上，他们只能靠传小纸条通信，这会经过中间很多同学，
        self.play(
            alice.animate.shift(RIGHT*1.5),
            bob.animate.shift(LEFT*1.5),
            FadeIn(eve),
            Transform(paper, _paper),
            Transform(msg, _msg),
            run_time=2
        )
        self.wait()
        # 中间传递的同学都能打开纸条、看到这串肉麻的数字，
        exclam = MathTex("!").scale(2).move_to(eve.get_center()).set_color(RED).set_stroke(width=5., background=True)
        self.play(
            paper.animate.shift(RIGHT*5),
            msg.animate.shift(RIGHT*5),
            run_time=1.5
        )
        self.play(Write(exclam), run_time=1)
        self.play(Wiggle(exclam), run_time=1)
        self.play(Wiggle(exclam), run_time=1)
        self.wait(2)
        # 那么小帅和小美的八卦很快就会传遍全校。因此，这串数字需要加密。
        self.play(
            paper.animate.shift(LEFT*5),
            msg.animate.shift(LEFT*5),
            FadeOut(exclam),
        )
        self.wait()
        encry = Text("加密").scale(1.2).move_to(paper).set_color(RED).set_stroke(width=5., background=True)
        self.play(Write(encry), run_time=1)
        self.wait()
        self.play(FadeOut(encry), run_time=1)
        self.wait(2)
        # 该怎么加密呢？小帅想到了一个办法，那就是给这串数字随便加一个随机的整数，比如1123759，实际传递过去一个6325073，
        msg_ = msg.copy().scale(2).shift(DOWN*4 + RIGHT*2)
        key = MathTex("+","1123759").scale(1.5).next_to(msg_, RIGHT).set_color(BLUE)
        result = MathTex("=","6325073").scale(1.5).next_to(key, RIGHT).set_color(YELLOW)
        encry_msg = result[1].copy().scale(0.5).move_to(paper)
        self.play(ReplacementTransform(msg, msg_))
        self.wait()
        self.play(Write(key), run_time=1)
        self.wait(0.5)
        self.play(Write(result), run_time=1)
        self.wait(2)
        self.play(TransformFromCopy(result[1], encry_msg), run_time=1)
        self.wait(2)

        # 这样，传纸条的人肯定就不知道是什么意思了。
        self.play(
            paper.animate.shift(RIGHT*5),
            encry_msg.animate.shift(RIGHT*5),
            run_time=1.5
        )
        self.wait()
        question_mark = MathTex("?").scale(2).move_to(eve.get_center()).set_color(RED).set_stroke(width=5., background=True)
        self.play(Write(question_mark), run_time=1)
        self.wait(2)
        self.play(FadeOut(question_mark), run_time=1)
        # 等到了小美那边，只需要把接收到的数字减去1123759，就完成了一次只属于两人之间的悄悄话。
        self.play(
            paper.animate.shift(RIGHT*5),
            encry_msg.animate.shift(RIGHT*5),
            run_time=1.5
        )
        self.wait(2)

        encry_msg_ = encry_msg.copy().scale(2).next_to(msg_, DOWN)
        decry = MathTex("-","1123759").scale(1.5).next_to(encry_msg_, RIGHT).set_color(BLUE)
        get_msg = MathTex("=","5201314").scale(1.5).next_to(decry, RIGHT).set_color(RED)

        self.play(TransformFromCopy(encry_msg, encry_msg_))
        self.wait()
        self.play(Write(decry), run_time=1)
        self.wait(0.5)
        self.play(Write(get_msg), run_time=1)
        self.wait(2)

        # 上面这个过程就是一个经典的密码学情境，要传输的信息x被称为“明文”，加密用的这串数字被称作“密钥”，
        r1 = SurroundingRectangle(msg_, buff=0.1)
        r2 = SurroundingRectangle(key[1], buff=0.1)
        r1_lbl = Text("明文").next_to(r1, UP).set_stroke(width=5., background=True)
        r2_lbl = Text("密钥").next_to(r2, UP).set_stroke(width=5., background=True)
        self.play(Create(r1))
        self.play(Write(r1_lbl))
        self.wait()
        self.play(Create(r2))
        self.play(Write(r2_lbl))
        self.wait(2)
        # 明文通过加上密钥变成乱七八糟的密文过程被称作“加密”，而用密钥将密文还原成原文的过程被称作“解密”。
        enc_lbl = Text("加密").next_to(msg_, LEFT, buff=0.3).set_color(ORANGE)
        dec_lbl = Text("解密").next_to(encry_msg_, LEFT, buff=0.3).set_color(BLUE)
        # self.play(FadeOut(r1), FadeOut(r2), FadeOut(r1_lbl), FadeOut(r2_lbl))
        self.play(Write(enc_lbl))
        self.wait(2)
        self.play(Write(dec_lbl))
        self.wait(2)
        # 桥豆麻袋！愿望虽然美好，可又有一个新的问题出现了：小美又怎么知道密钥的这串数字是什么呢？
        self.play(
            FadeOut(r1), FadeOut(r1_lbl),
            FadeOut(r2), FadeOut(r2_lbl),
            FadeOut(enc_lbl), FadeOut(dec_lbl),
        )
        
        arr_to_key = Arrow(alice.get_center(), r2.get_right(), buff=0.1).set_color(GREEN)
        how_question = MathTex("?").scale(3).set_color(RED).set_stroke(width=5., background=True).move_to(arr_to_key, UP)
        self.play(Create(arr_to_key), run_time=2)
        self.play(Write(how_question), run_time=1)
        self.wait(2)
        # 难道小帅需要再写个纸条：“密钥：1123759，解密时减去密钥”吗？
        paper2 = paper.copy().shift(LEFT*10)
        content2 = Text("解密：\n减去1123759").scale(0.5).move_to(paper2).set_color(BLUE)
        self.play(LaggedStart(FadeIn(paper2), Write(content2)), run_time=1.5)
        self.wait()
        self.play(
            paper2.animate.shift(RIGHT*5),
            content2.animate.shift(RIGHT*5),
        )
        self.wait(2)
        # 要知道，这个纸条也要经手中间的同学，让他们看到这个纸条，自己就完全能解密了，那整个加密就完全形同虚设了。
        rect = SurroundingRectangle(VGroup(paper2, eve), buff=0.1)
        rect2 = SurroundingRectangle(VGroup(encry_msg_, decry, get_msg), buff=0.1)
        self.play(Create(rect), Create(rect2), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(rect), FadeOut(paper2), FadeOut(content2), FadeOut(rect2))

class RSA(Scene):
    def construct(self):
        # 这个问题在真实世界中普遍存在，说白了就是：哪里去找一只老鼠给猫挂上铃铛？
        title = Text("对称加密").set_color(GREEN).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN)
        self.play(Write(title), GrowFromCenter(line), run_time=1)
        self.wait(2)
        # 它的困难核心就在于加密解密的过程是“对称的”。
        # 所谓对称，本质上就是说任何人只要有了密钥，加密和解密算起来是一样简单的，无非是加一个数和减一个数的区别。
        person = SVGMobject('man.svg').scale(0.8).set_color(GOLD).shift(UP)
        msg = MathTex("5201314").scale(1.5).shift(LEFT*3.5+DOWN*2).set_color(RED)
        enc_text = MathTex("6325073", color=YELLOW).scale(1.5).shift(RIGHT*3.5+DOWN*2)
        knowkey = MathTex("1123759").scale(0.6).next_to(person, UP+RIGHT).set_color(BLUE)

        rect_msg = Rectangle(width=4, height=2.6).move_to(msg).set_fill(opacity=0.3, color=BLUE).add_to_back()
        rect_enc = Rectangle(width=4, height=2.6).move_to(enc_text).set_fill(opacity=0.3, color=ORANGE).add_to_back()

        right_arr = Arrow(rect_msg.get_right(), rect_enc.get_left(), buff=0.1).set_color(ORANGE).shift(UP*0.3)
        encry_lbl = MathTex("+1123759").scale(0.8).next_to(right_arr, UP).set_color(ORANGE)
        left_arr = Arrow(rect_enc.get_left(), rect_msg.get_right(), buff=0.1).set_color(GREEN).shift(DOWN*0.3)
        decry_lbl = MathTex("-1123759").scale(0.8).next_to(left_arr, DOWN).set_color(GREEN)

        self.play(
            FadeIn(person),
            Write(knowkey),
            run_time=2
        )
        self.wait()
        self.play(Write(msg), FadeIn(rect_msg), run_time=1)
        self.wait()
        self.play(
            LaggedStart(Create(right_arr), Write(encry_lbl)),
            run_time=2
        )
        self.wait()
        self.play(
            Write(enc_text), 
            FadeIn(rect_enc),
            run_time=1
        )
        self.wait()
        self.play(
            LaggedStart(Create(left_arr), Write(decry_lbl)),
            run_time=2
        )
        self.wait(3)
        # 因为对称，所以传递密钥就几乎相当于泄露信息本身，如果双方只能通过传小纸条传递所有信息，那么就不存在安全的传递密钥的办法。
        cross = Cross(knowkey).set_color(RED)
        self.play(Write(cross), run_time=2)
        self.wait(3)
        # 为了解决这个问题，1977年，来自麻省理工的三位教授：Ron Rivest，Adi Shamir，Leonard Adleman共同提出了人类第一个非对称加密算法，
        new_title = Text("非对称加密").set_color(YELLOW).to_edge(UP)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [title, line]],
            Transform(title, new_title),
        )
        self.wait(2)
        # 这个算法也因此用他们三个的姓氏共同命名为RSA算法。
        name1 = Text("Ron Rivest").next_to(line, DOWN, buff=0.2).set_color(BLUE)
        # name2 = Text("Adi ","S", "hamir").next_to(name1, DOWN, buff=0.2).align_to(name1, LEFT).set_color(BLUE)
        name2 = Text("Adi Shamir").next_to(name1, DOWN, buff=0.2).align_to(name1, LEFT).set_color(BLUE)
        # name3 = Text("Lenord ","A","dleman").next_to(name2, DOWN, buff=0.2).align_to(name2, LEFT).set_color(BLUE)
        name3 = Text("Lenord Adleman").next_to(name2, DOWN, buff=0.2).align_to(name2, LEFT).set_color(BLUE)
        self.play(
            LaggedStart(Write(name1), Write(name2), Write(name3)),
            run_time=2
        )
        self.wait(2)
        RSA_text = Text("RSA  Algorithm").scale(2).set_color(YELLOW)
          
        self.play(
            LaggedStart(
                TransformFromCopy(name1[3], RSA_text[0]),
                TransformFromCopy(name2[3], RSA_text[1]),
                TransformFromCopy(name3[6], RSA_text[2]),
                FadeIn(RSA_text[3:]),
                FadeOut(VGroup(name1, name2, name3)),
            ),
            run_time=3
        )
        self.wait(2)
        # 非对称加密算法完美解决了“怎么传递密钥”的难题，成为互联网上使用至今的重要加密算法。
        # 那么，RSA算法是怎么工作的呢？答案，其实就藏在这道联考题的第三问中。
        _rsa_text = Text("ElGamal Algorithm").set_color(YELLOW).to_edge(UP)

        self.play(
            Transform(RSA_text, _rsa_text),
            FadeOut(title),
            run_time=1.5
        )
        # 声明一下，它和RSA算法并不完全一样，但本质是类似的。我们一点点来看。
        self.wait(2)
        # 小帅首先让小美自己偷偷选择一个数字n，这个n是私密的，我们把它叫做私钥。
        alice = SVGMobject("woman.svg").set_color(PINK).shift(RIGHT*4)
        bob = SVGMobject("man.svg").set_color(BLUE).shift(LEFT*4)
        self.play(FadeIn(alice), FadeIn(bob))

        # 小帅首先在纸条上写下一个很大的质数p，一个整数a，传递给小美，
        right1 = Arrow(bob.get_right(),alice.get_left(),  buff=0.1).set_color(GREEN).shift(UP*1.5)
        lbl1 = MathTex("p=10000019,", r"a=3").scale(0.8).next_to(right1, UP).set_color(ORANGE).shift(DOWN*0.1)
        self.play(
            LaggedStart(Create(right1), Write(lbl1)),
            run_time=1.5
        )
        self.wait(4)
        
        # 同时让小美自己偷偷选择一个数字n，这个n是私密的，我们把它叫做私钥。
        private_key = MathTex("n=13940").scale(0.8).next_to(alice, UP+RIGHT).set_color(PURPLE_A)
        self.play(Write(private_key), run_time=1)
        self.wait(2)
        priv_lbl = Text("私钥").scale(0.8).next_to(private_key, DOWN, buff=0.2).set_color(YELLOW)
        rect_priv = SurroundingRectangle(private_key, buff=0.1)
        self.play(
            Create(rect_priv),
            Write(priv_lbl),
            run_time=1.5
        )
        self.wait()
        self.play(FadeOut(rect_priv), FadeOut(priv_lbl))
        # 然后，小美把a的n次方除以p的余数写给小帅，这个数字我们记作b。
        apn_modp = a_to_b_mod_p(3, 13940, 10000019)
        left1 = Arrow(alice.get_left(),bob.get_right(), buff=0.1).set_color(GOLD).next_to(right1, DOWN, buff=0.5)
        b = MathTex("b=a^{n,\otimes}="+str(apn_modp)).scale(0.8).next_to(left1, UP).set_color(BLUE).shift(DOWN*0.1)
        #  这就是第一个条件n=log(p)a b的含义。这里的b其实也是一个密钥，
        note = MathTex(r"n=\log(p)_a b \quad\Leftrightarrow\quad b= a^{n,\otimes}").shift(DOWN*3).set_color(ORANGE)
        self.play(
            LaggedStart(Create(left1), Write(b)),
            run_time=1.5
        )
        self.wait(3)
        self.play(Write(note), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(note))
        self.wait(2)

        pub_key = Text("公钥").scale(0.8).next_to(left1, DOWN, buff=0.1).set_color(ORANGE)
        rect = SurroundingRectangle(b, buff=0.1)
        self.play(
            Create(rect),
            Write(pub_key),
            run_time=1.5
        )
        self.wait(2)
        # 但是因为它是写在纸条上、所有传递的人都能看到的，所以被叫做“公钥”。
        self.play(FadeOut(rect), FadeOut(pub_key))

        # 现在，纸条上已经有了三个数字: p，a,还有公钥b。
        self.play(Indicate(lbl1[0]))
        self.wait(0.5)
        self.play(Indicate(lbl1[1]))
        self.wait(0.5)
        self.play(Indicate(b))
        self.wait(2)
        # 小帅开始进行加密了，假设x=5201314为想要加密的原文，小帅也随便取一个秘密的数字k，
        select_k = MathTex("k=114514").scale(0.8).next_to(bob, UP+LEFT).set_color(YELLOW)
        # 计算x乘以b的k次方除以p的余数，也就是题目中的y2，然后再计算a的k次方除以p的余数得到y1。
        right2 = Arrow(bob.get_right(),alice.get_left(),  buff=0.1).set_color(GREEN).next_to(left1, DOWN, buff=1.2)
        lbl3_1 = MathTex(r"y_1=a^{k,\otimes}=",str(a_to_b_mod_p(apn_modp, 114514, 10000019))).scale(0.8).next_to(right2, UP).set_color(BLUE).shift(DOWN*0.1)
        lbl3_2 = MathTex(r"y_2=x\otimes b^{k,\otimes}=",
                         str(5201314*a_to_b_mod_p(3, 114514, 10000019)%10000019)
                ).scale(0.8).next_to(right2, DOWN).set_color(ORANGE).shift(UP*0.1)
        self.play(LaggedStart(
            Write(select_k),
            Create(right2),
        ), run_time=1.5)
        self.play(Write(lbl3_1), run_time=2)
        self.wait(4)
        self.play(Write(lbl3_2), run_time=2)
        self.wait(4)
        # shift everything except [rsa, line] to the left
        self.play(
            *[mob.animate.shift(LEFT*2.5) for mob in self.mobjects if mob not in [RSA_text, line, alice, private_key]],
            alice.animate.shift(LEFT*1.5).scale(1.5),
            private_key.animate.shift(LEFT*1.5+UP*0.8),
            run_time=1.5
        )
        self.wait(2)

        # 将y1和y2一起传递给小美。最终，小美通过计算题目中所展示的y2*y1的n(p-2)次方，并计算它除以p的余数，就能还原出x的值了。
        calc_decry = MathTex(r"y_2\otimes y_1^{n(p-2),\otimes}").next_to(alice, DOWN).set_color(BLUE)
        eq1 = MathTex(r"=2524935\times 6194260^{13940\times 10000017}").scale(0.8).next_to(alice, DOWN).set_color(BLUE)
        eq2 = MathTex(r"\equiv 5201314 \pmod{10000019}").next_to(eq1, DOWN).set_color(RED).scale(0.8).align_to(eq1, LEFT)
        self.play(Write(calc_decry), run_time=2)
        self.wait()
        self.play(LaggedStart(
            ReplacementTransform(calc_decry, eq1),
        ), run_time=1)
        self.wait()
        self.play(Write(eq2), run_time=1)
        self.wait()
        heart = SVGMobject("heart.svg").scale(0.8).set_color(RED).move_to(alice).set_opacity(0.6)
        rct_res = SurroundingRectangle(eq2, buff=0.1)
        self.play(Create(rct_res))
        self.play(FadeIn(heart), run_time=1.5)
        self.wait(3)
        
        self.play(
            FadeOut(rct_res),
            FadeOut(heart),
            FadeOut(VGroup(eq1, eq2)),
        )
        self.play(
            *[mob.animate.shift(RIGHT*2.5) for mob in self.mobjects if mob not in [RSA_text, line, alice, private_key]],
            alice.animate.shift(RIGHT*1.5).scale(2/3),
            private_key.animate.shift(RIGHT*1.5+DOWN*0.8),
            run_time=2
        )
        self.wait(5)
        # 这都什么乱七八糟的啊喂！不急，我们一点点看。
        # 首先，我们验证以下，小美真的可以完美还原x的数值吗？这其实就是第三小问让我们证明的事情。
        self.play(
            *[mob.animate.shift(LEFT*3) for mob in self.mobjects if mob not in [RSA_text, line]],
            run_time = 1.5
        )
        
        # 利用余数对于乘法和加法平行的特点，我们可以完全忽略掉“求余数”的过程，
        # 就当成正常的运算。带入y1和y2，我们得到等式右边等于x*a^{kn(p-2)}*b^k，
        e1 = MathTex(r"y_2\otimes",r"y_1^{n(p-2),\otimes}").scale(0.8).shift(RIGHT*3.3+UP*0.5).set_color(BLUE)
        e1_ = MathTex(r"y_2\times y_1^{n(p-2)}").scale(0.8).shift(RIGHT*3.3+UP*0.5)
        modp_sign = MathTex(r"\bmod p").scale(0.8).next_to(e1_, RIGHT, buff=0.6).set_color(RED)
        e2 = MathTex(r"=x\times b^{k}\times ( a^{k})^{n(p-2)}").scale(0.8).next_to(e1, DOWN).align_to(e1, LEFT)
        e3 = MathTex(r"=x\cdot a^{kn}\cdot a^{kn(p-2)}").scale(0.8).next_to(e2, DOWN).align_to(e2, LEFT)
        e4 = MathTex(r"=x\cdot a^{kn(p-1)}").scale(0.8).next_to(e3, DOWN).align_to(e3, LEFT)
        e5 = MathTex(r"=x\cdot (","a^{p-1}",r")^{kn}").scale(0.8).next_to(e3, DOWN).align_to(e3, LEFT)
        ferm_rect = SurroundingRectangle(e5[1], buff=0.1)
        equal_1 = MathTex(r"\equiv 1").scale(0.8).next_to(ferm_rect, RIGHT).set_color(YELLOW).set_stroke(width=5., background=True)
        one = MathTex(r"1").move_to(e5[1]).set_color(YELLOW)
        e6 = MathTex(r"\equiv x\pmod{p}").next_to(e5, DOWN).set_color(RED).align_to(e5, LEFT)
        
        self.play(Write(e1), run_time=1.5)
        self.wait(3)
        self.play(ReplacementTransform(e1, e1_), run_time=1.5)
        self.wait(2)
        self.play(Write(modp_sign), run_time=1.5)
        self.wait(3)
        self.play(Write(e2), run_time=1.5)
        self.wait(3)
        self.play(Write(e3), run_time=1.5)
        self.wait(3)
        self.play(Write(e4), run_time=1.5)
        self.wait(3)
        self.play(ReplacementTransform(e4, e5), run_time=1.5)
        self.wait(3)
        self.play(Create(ferm_rect))
        self.wait(2)
        self.play(Write(equal_1), run_time=1.5)
        self.play(
            Transform(e5[1], one),
            FadeOut(ferm_rect), FadeOut(equal_1),
            run_time=1.5
        )
        self.wait(3)
        self.play(Write(e6), run_time=1.5)
        self.wait(3)
        # 而b=a^n，所以第三项变成了a^kn，带入之后可以在指数上提取一个kn的公因式，
        # 于是得到x*a^{kn(p-1)}，我们可以进一步根据幂函数的性质，写成x*(a^{p-1})^{kn}，
        # 重点来了，括号里的部分我们刚才已经用费马小定理证明了，它在除以p求余数的意义下等于1，
        # 所以整个指数变成了1^kn，于是整个式子除以p的余数就等于x，
        # 我们证明了小美能够还原出小帅写下的数字了。
        # 你也能从这里反过来看出，为什么会出现一个神秘的n(p-2)次方，
        rect_exp = SurroundingRectangle(e1[1], buff=0.1)
        rect_ind = SurroundingRectangle(e3, buff=0.1)
        self.play(Create(rect_exp))
        self.wait(3)
        self.play(Create(rect_ind))
        self.wait(3)
        self.play(FadeOut(VGroup(rect_exp, rect_ind)))
        self.wait(2)
        # 它的目的就是为了配合另一个nk过来，刚好用费马小定理变成1。
        # 于是，我们终于通关了这道让万千高三考生流泪的压轴题。
        self.play(
            *[FadeOut(mob) for mob in [e1, e1_, modp_sign, e2, e3, e4, e5, e6]],
            run_time=1
        )
        self.play(
            *[mob.animate.shift(RIGHT*3) for mob in self.mobjects if mob not in [RSA_text, line]],
        )
        _new_b = MathTex("b=a^n").scale(0.8).move_to(b).set_color(BLUE)
        _new_lbl3_1 = MathTex(r"y_1=a^{k,\otimes}").scale(0.8).move_to(lbl3_1).set_color(BLUE)
        _new_lbl3_2 = MathTex(r"y_2=",r"x\otimes b^{k,\otimes}").scale(0.8).move_to(lbl3_2).set_color(ORANGE)
        self.play(
            Transform(b, _new_b),
            Transform(lbl3_1, _new_lbl3_1),
            Transform(lbl3_2, _new_lbl3_2),
            run_time=1.5
        )
        self.wait(2)

        # 但是问题还没有结束，这个题目还有很多微妙的机关。比如，为什么这里小帅要一个随便选的k呢？
        rect = SurroundingRectangle(select_k, buff=0.1)
        question = MathTex("?").scale(2).set_color(RED).set_stroke(width=5., background=True).move_to(rect)
        self.play(Create(rect), Write(question), run_time=1.5)
        self.wait(3)
        # 相比于上面的X集合，这个k为什么不允许它等于p-1呢？
        # 我们不妨来看看，如果k真的等于p-1了，到底会发生什么。
        cross_k = Cross(select_k).set_color(RED)
        _new_k = MathTex("k=p-1").scale(0.8).next_to(select_k, DOWN, buff=0.4).set_color(YELLOW)
        self.play(FadeOut(question), Create(cross_k), Write(_new_k), run_time=1.5)
        self.wait(2)
        # 此时根据我们前面的费马小定理，y1直接变成了1，而b^k则等于a^{(p-1)k}，
        y1_eq_1 = MathTex(r"=b^{p-1,\otimes}=1").scale(0.8).next_to(lbl3_1, RIGHT).set_color(YELLOW)
        y2_eq_x = MathTex(r"=x\otimes 1", "=x").scale(0.8).next_to(lbl3_2, RIGHT).set_color(ORANGE)
        self.play(Write(y1_eq_1), run_time=1.5)
        self.wait(2)
        self.play(Write(y2_eq_x), run_time=1.5)
        self.wait(2)
        danger = SVGMobject("danger.svg").scale(0.8).next_to(y2_eq_x, DOWN)
        self.play(FadeIn(danger), run_time=1.5)
        self.wait()
        self.play(Wiggle(danger))
        self.wait(3)
        self.play(FadeOut(danger), FadeOut(VGroup(y1_eq_1, y2_eq_x)),
                  FadeOut(VGroup(cross_k, _new_k, rect, question)))
        # 我们先算a的p-1次方，立刻得到它除以p的余数就等于1，所以y2就等于x本身。
        # 注意看，y1=1，y2=x完全不妨碍我们得到最终的结论,y1*y2=x，但是这种情况下出现了一个致命的问题，
        # 小帅在最后一轮要把y1和y2写在纸条上传给小美的。此时纸条上将赫然写着1和完整的明文，也就是5201314。
        # 传纸条的人都知道了具体的内容，整个加密失去意义。这便是题目中特别去掉了k=p-1的原因。
        # 还有一个问题，为什么非要小帅选择一个k呢？小帅能不能偷懒、固定这个k是1？这个问题其实非常深刻。
        # 我们回答它之前，先提问另一个更重要的问题：我们展示的这坨复杂的流程，凭什么就能保证传纸条的人无法破解小帅传递的信息x呢？
        # 而答案，就在这道题的主旨：离散对数上。

        # 而且，这还同时解释了为什么小帅必须要选一个随机的k，如果小帅偷懒总是用k=1，那么中间传纸条的八卦同学可就开心了。
        const_k_text = Text("k为常数").scale(0.8).next_to(select_k, DOWN, buff=0.4).set_color(YELLOW)
        # 他知道b，也知道p，所以只需要将y2乘以b的p-k-1次方，那么这个数值就等于x*b^{p-1}，而第二项我们根据费马小定理知道等于1，
        attack = MathTex(r"x\otimes b^{k,\otimes}",r"\times b^{p-k-1,\otimes}",r"=x\otimes",r" b^{p-1}").scale(0.8).shift(DOWN*2.5)
        self.play(Write(const_k_text), run_time=1.5)
        self.wait(2)
        self.play(
            TransformFromCopy(lbl3_2[1], attack[0]),
        )
        self.wait()
        self.play(Write(attack[1]), run_time=1.5)
        self.wait()
        self.play(Write(attack[2:]), run_time=1)
        self.wait(2)
        rect_eq1 = SurroundingRectangle(attack[-1], buff=0.1)
        eq1 = MathTex(r"\equiv 1").scale(0.8).next_to(rect_eq1, RIGHT).set_color(YELLOW).set_stroke(width=5., background=True)
        self.play(Create(rect_eq1))
        self.play(Write(eq1), run_time=1.5)
        self.wait(3)
        # 于是整个式子就等于x=5201314。为了避免这件事，小帅随机取一个k，这不影响小美的解密过程，毕竟1的任意次方都是1，
        # 但却可以成功避免中间人直接通过y2破解原文，是不是很巧妙呢。
        

class OneWay(Scene):
    def construct(self):
        title = Text("离散对数").set_color(RED).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN)
        # 简单来说，整个非对称加密算法最核心的原理在于，有一条计算的单行道，正着走很容易，反着走却极其困难，
        eq = MathTex(r"a^x\equiv b\pmod{p}").shift(UP*1.5).set_color(BLUE)
        bigx = MathTex(r"x").scale(5).set_color(BLUE).shift(LEFT*4+DOWN)
        bigb = MathTex(r"b").scale(5).set_color(ORANGE).shift(RIGHT*4+DOWN)
        right_arr = Arrow(bigx.get_right(), bigb.get_left(), buff=1).set_color(GREEN).shift(UP*0.2)
        left_arr = Arrow(bigb.get_left(), bigx.get_right(), buff=1).set_color(RED).shift(DOWN*0.2)
        tick_sign = MathTex(r"\checkmark").scale(3).set_color(GREEN).next_to(right_arr, UP)
        cross_sign = MathTex(r"\times").scale(3).set_color(RED).next_to(left_arr, DOWN)

        discret_log = MathTex(r"x=\log(p)_a b").scale(1.5).set_color(RED).shift(DOWN*2.5)

        self.play(Write(title), GrowFromCenter(line), run_time=1)
        self.wait(2)
        self.play(Write(eq), run_time=1.5)
        self.wait(2)
        self.play(LaggedStart(
            Write(bigx),
            Create(right_arr),
            Write(bigb),
        ), run_time=2, lag_ratio=0.1)
        self.play(Write(tick_sign), run_time=2)
        self.wait(2)
        self.play(LaggedStart(
            Create(left_arr),
            Write(discret_log),
        ), run_time=2, lag_ratio=0.1)
        self.play(Write(cross_sign), run_time=2)
        self.wait(4)

        # 这条单行道就是“离散指数/对数”。如果我们知道了a、n和p，那么计算a的n次方除以p的余数是容易的，

        # 你只需要一直不断地乘以a、乘n次，每次只关注余数就可以了。其实还有更快的做法叫做快速幂，它不需要n次乘法，只需要log n次，
        # 这里不再展开，总之你只需要知道它很好算。
        # 但是，如果你想要反过来，知道a、b和p，想要求出一个n，让a的n次方和b模p同余，那么这件事难如登天。
        # 如果忽略余数，那么根据a和b求n的过程其实就是对数。
        # 因此，单行道难以逆行这件事，其实本质上就是说“离散对数”难以求解。除了一个个枚举n看看a的n次方是不是同余b，
        # 人类目前没有找到本质更好的办法。
        # 正因此，小美可以放心的把b=a^n公开地传递给小帅，而不必担心传递的同学算出自己的私钥n来偷听和解密。
        # 因为想要根据a、b和p求出指数n的过程叫离散指数，是极其困难的。

class FastPower(Scene):
    def construct(self):
        title = Text("快速幂").set_color(RED).to_edge(UP)
        line = Line(LEFT*7, RIGHT*7).next_to(title, DOWN)
        
        self.play(Write(title), GrowFromCenter(line), run_time=1)

        e1 = MathTex(r"3^{17}", r"\equiv",r"3\times(3^8)^2").set_color(GOLD).scale(1.2).shift(UP*1.5)
        e2 = MathTex(r"3^{8}", r"\equiv",r"(3^4)^2").set_color(GOLD).scale(1.2).next_to(e1, DOWN, buff=0.3).align_to(e1, LEFT)
        e3 = MathTex(r"3^{4}", r"\equiv",r"(3^2)^2").set_color(GOLD).scale(1.2).next_to(e2, DOWN, buff=0.3).align_to(e2, LEFT)
        e4 = MathTex(r"3^{2}", r"\equiv",r"(3^1)^2").set_color(GOLD).scale(1.2).next_to(e3, DOWN, buff=0.3).align_to(e3, LEFT)

        self.play(Write(e1), run_time=1)
        self.wait(0.3)
        self.play(Write(e2), run_time=1)
        self.wait(0.3)
        self.play(Write(e3), run_time=1)
        self.wait(0.3)
        self.play(Write(e4), run_time=1)

        modp = MathTex(r"\bmod p").set_color(YELLOW).scale(2).shift(RIGHT*3)
        self.wait()
        self.play(Write(modp), run_time=1.5)
        self.wait(2)
