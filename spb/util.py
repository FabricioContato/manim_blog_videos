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

def typing_animation_with_cursor(text: str, cursor: Rectangle, scene: Scene):
    math_char_aling_dic = {'"': UP, '=': array([0., 0., 0.])}
    math_chars = ['"', "="]

    wait_time = .2
    cursor_line_start_ref = cursor.copy()

    special_chars = [" ", "\n"]
    text_obj_list = [char if char in special_chars else MathTex(char, should_center=True) if char in math_chars else Text(char) for char in text]
    last_text_obj = None
    line_first_printalbe_char = None

    for text_obj in text_obj_list:

        if text_obj == "\n":
            last_text_obj = None
            line_first_printalbe_char = None
            scene.remove(cursor)
            cursor.next_to(cursor_line_start_ref, DOWN, aligned_edge=LEFT)
            cursor_line_start_ref.move_to(cursor)
            continue
        elif text_obj == " ":
            last_text_obj = None
            cursor.next_to(cursor, RIGHT, aligned_edge=DOWN+LEFT)
            continue

        elif line_first_printalbe_char == None:
            line_first_printalbe_char = text_obj
            scene.add(cursor)
            scene.wait(wait_time)
            last_text_obj = text_obj
            text_width = text_obj.width
            aligned_edge = DOWN if type(text_obj) is Text or type(text_obj) is str else math_char_aling_dic[text_obj.tex_string]
            text_obj.next_to(cursor, LEFT, buff=-1*text_width, aligned_edge=aligned_edge)

        elif last_text_obj == None:
            last_text_obj = text_obj
            text_width = text_obj.width
            aligned_edge = DOWN if type(text_obj) is Text or type(text_obj) is str else math_char_aling_dic[text_obj.tex_string]
            text_obj.next_to(cursor, LEFT, buff=-1*text_width, aligned_edge=aligned_edge)
        else:
            aligned_edge = DOWN if type(text_obj) is Text or type(text_obj) is str else math_char_aling_dic[text_obj.tex_string]
            text_obj.next_to(last_text_obj, RIGHT, buff=0, aligned_edge=aligned_edge)
            last_text_obj = text_obj
        
        scene.add(cursor)
        cursor.next_to(text_obj, RIGHT, aligned_edge=DOWN+LEFT)
        scene.add(text_obj)
        scene.wait(wait_time)
