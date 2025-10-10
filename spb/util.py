from gtts import gTTS
import os
from mutagen.mp3 import MP3

video_audio_relative_path = r"./util_audio/video_audio/"
cue_audio_relative_path = r"./util_audio/cue_audio/"
if not os.path.exists(video_audio_relative_path):
    os.makedirs(video_audio_relative_path)

if not os.path.exists(cue_audio_relative_path):
    os.makedirs(cue_audio_relative_path)

def cue_time_calculator(text, cue_word, language="en", replace_older_file=False):
    if type(cue_word) is str and cue_word in text:
        cue_index = text.find(cue_word)
        partial_text = text[: cue_index + len(cue_word)]
        file_name_for_partial_text = 'cue_'+ cue_word + "_for_" + text[: len(text)//2]
        generate_audio_file_from_text(text=partial_text, file_path=cue_audio_relative_path ,file_name=file_name_for_partial_text, language=language, replace_older_file=replace_older_file)
        cue_time = int(MP3(cue_audio_relative_path + file_name_for_partial_text + ".mp3").info.length) * .8
        return cue_time
    
    else:
        return 0

def generate_audio_file_from_text(text, file_name, file_path ,file_extention=".mp3", language="en", replace_older_file=False):
    file_name_already_exists = os.path.isfile(file_path + file_name + file_extention)

    if file_name_already_exists and replace_older_file:
        os.remove(file_path + file_name + file_extention)
        file_name_already_exists = False

    if not file_name_already_exists:
        gTTS(text=text, lang=language, slow=False).save(file_path + file_name + file_extention)

def add_audio_to_video_from_text(scene, text, file_name, file_extention=".mp3", cue_word=None, language="en", replace_older_file=False ,sync=True):
    generate_audio_file_from_text(text=text, file_path=video_audio_relative_path ,file_name=file_name, file_extention=file_extention, language=language, replace_older_file=replace_older_file)

    scene.add_sound(video_audio_relative_path + file_name + file_extention)

    audio_time = int(MP3(video_audio_relative_path + file_name + file_extention).info.length)
    if sync:
        scene.wait(audio_time)
    
    cue_time = cue_time_calculator(text=text, cue_word=cue_word, language=language, replace_older_file=replace_older_file)

    remaning_time_after_cue = audio_time - cue_time

    return audio_time, cue_time, remaning_time_after_cue


def add_parallel_audioTTS_with_animation(scene, animation, text, cue_word, file_name, file_extention=".mp3", language="en", replace_older_file=False):
    
    add_audio_to_video_from_text(scene=scene, text=text, file_name=file_name, file_extention=file_extention, language=language, replace_older_file=replace_older_file ,sync=False)
    audio_time = int(MP3(video_audio_relative_path + file_name + file_extention).info.length)

    cue_time = 0
    if type(cue_word) is str and cue_word in text:
        cue_index = text.find(cue_word)
        partial_text = text[: cue_index + len(cue_word)]
        file_name_for_partial_text = 'cue_'+ cue_word + "_for_" + file_name
        generate_audio_file_from_text(text=partial_text, file_path=cue_audio_relative_path, file_name=file_name_for_partial_text, file_extention=file_extention, language=language, replace_older_file=replace_older_file)
        cue_time = int(MP3(cue_audio_relative_path + file_name_for_partial_text + file_extention).info.length) * .8
        scene.wait(cue_time)

    animation_time = 0

    if type(animation) is list:
        [scene.play(animation_) if hasattr(animation_, 'run_time') else scene.play(animation_, run_time=1) for animation_ in animation]
        animation_time = sum([animation_.get_run_time() if hasattr(animation_, 'run_time') else 1 for animation_ in animation])
    else:
        scene.play(animation) if hasattr(animation, 'run_time') else scene.play(animation, run_time=1)
        animation_time = animation.get_run_time() if hasattr(animation, 'run_time') else 1

    aux_list = [audio_time, animation_time + cue_time]
    aux_list.sort()
    remaning_time = aux_list[-1] - aux_list[0]

    if remaning_time > 0:
        scene.wait(remaning_time)


#-------------------------------

from manim import *
from numpy import array

def typing_animation_with_cursor(text: str, color, cursor: Rectangle, scene: Scene, scale=1, wait_time=.1):
    cursor.scale(scale)
    cursor_line_start_ref = cursor.copy()
    math_char_aling_dic = {'"': UP, '=': array([0., 0., 0.])}
    math_chars = ['"', "="]
    special_chars = [" ", "\n"]
    under_base_line_chars = ['g', 'j', 'p', 'q', 'y']

    
    last_char = None
    line_first_printalbe_char = None

    def is_an_under_base_line_char(char):
        return char in under_base_line_chars

    def char_to_manim_obj(char):
        return MathTex(char, color=color).scale(scale) if char in math_chars else Text(char, color=color).scale(scale)

    def move_cursor_foward():
        if last_char:
            cursor.next_to(last_char, RIGHT, buff=0.025)
        else:
            cursor.next_to(cursor, RIGHT, buff=0)
        
        cursor.align_to(cursor_line_start_ref, DOWN)

    def line_feed():
        cursor.next_to(cursor_line_start_ref, DOWN, buff=0.2, aligned_edge=LEFT)
        cursor_line_start_ref.move_to(cursor)

    def print_char(char_obj, print_under_base_line=False):
        #text_height = char.height
        #aligned_edge = (DOWN + LEFT) if type(char) is Text or type(char) is str else math_char_aling_dic[char]
        aligned_edge = math_char_aling_dic[char] if char in math_chars else (DOWN + LEFT)
        char_obj.move_to(cursor.get_center())
        char_obj.align_to(cursor, aligned_edge)
        if print_under_base_line:
            char_obj.shift(DOWN * (char_obj.height * 0.3) )
        #char.next_to(cursor, DOWN, buff=-1*text_height, aligned_edge=aligned_edge)

    for char in text:

        if char == "\n": #Line feed
            last_char = None
            line_first_printalbe_char = None
            scene.remove(cursor)
            line_feed()
            continue

        elif char == " ": #blank space
            last_char = None
            move_cursor_foward()
            if line_first_printalbe_char:
                scene.wait(wait_time)
            continue

        elif line_first_printalbe_char == None: #first line printalbe char
            char_obj = char_to_manim_obj(char)
            line_first_printalbe_char = char_obj
            scene.add(cursor)
            scene.wait(wait_time)
            last_char = char_obj
            print_char(char_obj, print_under_base_line=is_an_under_base_line_char(char))

        elif last_char == None: # not first lpc and the last char was a npc
            char_obj = char_to_manim_obj(char)
            last_char = char_obj
            print_char(char_obj, print_under_base_line=is_an_under_base_line_char(char))
        
        else: # a pc following another pc
            char_obj = char_to_manim_obj(char)
            print_char(char_obj, print_under_base_line=is_an_under_base_line_char(char))
            last_char = char_obj
        
        scene.add(cursor)
        move_cursor_foward()
        scene.add(char_obj)
        scene.wait(wait_time)
