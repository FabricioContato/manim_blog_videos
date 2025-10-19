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
       <a class="navbar-brand" href="/">
         <span>&#60;<i class="bi bi-house-door-fill"></i>&#62;</span>
           </a>
           <button class="navbar-toggler">
            <span class="navbar-toggler-icon"></span>

"""

class SPB_2(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        pc_case = Rectangle(WHITE, 9, 16)
        pc_screen = pc_case.copy().set_color(GREEN).scale(0.9)
        self.play(Write(pc_case), Write(pc_screen))

        cursor = Rectangle(GREEN, .8, .6)
        cursor.set_fill(color=GREEN, opacity=1)

        cursor.next_to(pc_screen, LEFT, buff=-.6, aligned_edge=UP)
        cursor = cursor.scale(.5)
        self.add(cursor)

        typing_animation_with_cursor(text=text, color=GREEN, scale=0.5, wait_time=0.25, cursor=cursor, scene=self)

        self.wait(2)

class TagObj:
    def __init__(self, scene: Scene, tag: str, identation: int, text: str, text_scale=0.5, tag_scale=0.5):
        self.scene = scene
        self.tag = tag
        self.identation = identation
        self.text = text
        self.text_scale = text_scale
        self.tag_scale = tag_scale
        self.initiate_scene_objects()

    def initiate_scene_objects(self):
        self.identation_sqr = Rectangle(YELLOW, 3, 3)
        self.tag_rect = Rectangle(YELLOW, 1.5, 3)
        self.text_rect = Rectangle(YELLOW, 1.5, 3)
        
        self.tag_rect.next_to(self.identation_sqr, RIGHT, aligned_edge=UP, buff=0)
        self.text_rect.next_to(self.identation_sqr, RIGHT, aligned_edge=DOWN, buff=0)

        self.identation_Text = Text(str(self.identation))
        self.tag_Text = Text(self.tag).scale(self.tag_scale)
        self.text_Text = Text(self.text).scale(self.text_scale)

        self.identation_Text.move_to(self.identation_sqr.get_center())
        self.tag_Text.move_to(self.tag_rect.get_center())
        self.text_Text.move_to(self.text_rect.get_center())

        self.group = VGroup(self.identation_sqr, self.tag_rect, self.text_rect, self.identation_Text, self.tag_Text, self.text_Text)


class SPB_3(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        to1 = TagObj(scene=self, tag="#card-title", identation=1, text="place holder")
        to2 = TagObj(scene=self, tag="#div", identation=0, text="place holder2")
        to2.group.next_to(to1.group, DOWN)
        self.add(to1.group, to2.group)
