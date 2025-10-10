from manim import *
from util import *

class SPB_1(Scene):
    def construct(self):
        wordpress = ImageMobject("media/images/my_assets/wordpress.png").scale(1.5)
        shopify = ImageMobject("media/images/my_assets/Shopify_logo.png").scale(1.5)
        wix = ImageMobject("media/images/my_assets/wix.png").scale(1.5)
        blogger = ImageMobject("media/images/my_assets/Blogger.png").scale(0.35)
        hugo = ImageMobject("media/images/my_assets/hugo.png").scale(1.5)
        jekyll = ImageMobject("media/images/my_assets/Jekyll.png").scale(1.5)
        aws = ImageMobject("media/images/my_assets/aws.png").scale(1.0)
        fb = ImageMobject("media/images/my_assets/firebase.png").scale(0.6)
        gridsome = ImageMobject("media/images/my_assets/Gridsome.png").scale(0.5)
        gpt = ImageMobject("media/images/my_assets/gpt.png").scale(0.2)

        wordpress.to_edge(UP).to_edge(LEFT)
        blogger.to_edge(UP)
        shopify.to_edge(UP).to_edge(RIGHT)
        wix.to_edge(DOWN).to_edge(LEFT)
        hugo.to_edge(DOWN)
        jekyll.to_edge(DOWN).to_edge(RIGHT)
        fb.next_to(aws, LEFT, buff=2)
        gridsome.next_to(aws, LEFT, buff=0)
        gpt.to_edge(UP).to_edge(RIGHT)

        self.play(FadeIn(wordpress), run_time=0.3)
        self.play(FadeIn(shopify), run_time=0.3)
        self.play(FadeIn(blogger), run_time=0.3)
        self.play(FadeIn(wix), run_time=0.3)
        self.play(FadeIn(hugo), run_time=0.3)
        self.play(FadeIn(jekyll), run_time=0.3)
        self.play(FadeIn(aws), run_time=0.3)
        self.play(FadeIn(fb), run_time=0.3)
        self.play(FadeIn(gridsome), run_time=0.3)
        self.play(FadeIn(gpt), run_time=0.3)


        #self.play(FadeIn(wordpress, shopify, blogger, wix, hugo, jekyll, aws, fb, gridsome, gpt))
        self.wait(2)

        codewall = ImageMobject("media/images/my_assets/codewall.jpg").scale(1)

        self.play(FadeIn(codewall), codewall.animate.to_edge(DOWN,buff=-1), run_time=10)

text = """
<html>
  <head>
    <meta charset="UTF-8">
  </head>
  <body>
    <header>
      <div class="container-fluid">

"""

class SPB_2(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        pc_case = Rectangle(WHITE, 8, 11)
        pc_screen = pc_case.copy().set_color(GREEN).scale(0.9)
        self.play(Write(pc_case), Write(pc_screen))

        cursor = Rectangle(GREEN, .8, .6)
        cursor.set_fill(color=GREEN, opacity=1)

        cursor.next_to(pc_screen, LEFT, buff=-.6, aligned_edge=UP)
        cursor = cursor.scale(.5)
        # I am planing a typing animation
        # https://www.reddit.com/r/manim/comments/1ag560t/typing_animation_with_blinking_cursor/
        self.add(cursor)

        typing_animation_with_cursor(text=text, cursor=cursor, scene=self)

        self.wait(2)
    
  

        #self.play(cursor.animate.move_to(cursor, RIGHT))
         #t = Text(text).scale(.8)
         #t.next_to(cursor.get_center(), RIGHT, aligned_edge=UP)
         #self.play(AddTextLetterByLetter(t, time_per_char=.2 ))