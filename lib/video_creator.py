# video_creator.py

import os
from moviepy.editor import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS

def create_slideshow_with_audio(title, content_texts, image_paths, output_filename="slideshow.mp4"):
    clips = []
    duration = 2  # 각 이미지의 표시 시간 (초)

    # 이미지 슬라이드 클립 생성
    for img_path in image_paths:
        img_clip = ImageClip(img_path).set_duration(duration)
        clips.append(img_clip)

    # 슬라이드 쇼를 하나의 클립으로 연결
    slideshow = concatenate_videoclips(clips, method="compose")

    # 자막 텍스트를 하나의 문자열로 병합
    caption_text = f"{title}\n\n" + "\n".join(content_texts)

    # TTS로 음성 파일 생성
    tts = gTTS(text=caption_text, lang='ko')
    tts.save("caption_audio.mp3")
    audio_clip = AudioFileClip("caption_audio.mp3").set_duration(slideshow.duration)

    # 재생 속도 조정 (1.5배속 예시)
    audio_clip = audio_clip.fx(vfx.speedx, 1.5)  # 원하는 배속 설정

    # 자막 텍스트 클립 생성
    txt_clip = TextClip(caption_text, fontsize=24, color='white', size=slideshow.size, method='caption').set_duration(slideshow.duration)
    txt_clip = txt_clip.set_position(("center", "bottom"))

    # 슬라이드 쇼에 자막과 음성 추가하여 최종 클립 생성
    final_clip = CompositeVideoClip([slideshow, txt_clip])
    final_clip = final_clip.set_audio(audio_clip)

    # 최종 클립을 파일로 저장
    final_clip.write_videofile(output_filename, fps=24)

    # 임시 음성 파일 삭제
    os.remove("caption_audio.mp3")
