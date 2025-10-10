from manim import *
from util import *

class SPB(Scene):
    def construct(self):
        question_text = Text("""
                             What about software to help me with blog posts ?""").scale(0.8)



        _, cue_time, remaning_time_after_cue = add_audio_to_video_from_text(
            scene=self,
            text="""What about software to help me with blog posts ?""",
            cue_word=None,
            file_name="introduction",
            replace_older_file=False,
            sync=False )

        #self.wait(cue_time)
        self.play(Write(question_text), run_time=remaning_time_after_cue)

        wordpress = ImageMobject("./my_assets/wordpress.png").scale(1)
        shopify = ImageMobject("./my_assets/Shopify_logo.png").scale(0.5)
        wix = ImageMobject("./my_assets/wix.png").scale(1)
        blogger = ImageMobject("./my_assets/Blogger.png").scale(0.15)
        hugo = ImageMobject("./my_assets/hugo.png").scale(1)
        jekyll = ImageMobject("./my_assets/Jekyll.png").scale(1)

        wordpress.to_edge(UP).to_edge(LEFT)
        blogger.to_edge(UP)
        shopify.to_edge(UP).to_edge(RIGHT)
        wix.to_edge(DOWN).to_edge(LEFT)
        hugo.to_edge(DOWN)
        jekyll.to_edge(DOWN).to_edge(RIGHT)

        self.play(FadeIn(wordpress, blogger, shopify, wix, hugo, jekyll))
        self.wait(2)