# main.py

from lib.dc_scraper import get_content_from_url
from lib.insta_scraper import download_user_reels, login
from lib.video_creator import create_slideshow_with_audio

# 다운로드할 사용자 이름
user_to_scrape = input("Enter the username to download reels: ")
download_user_reels(user_to_scrape)

# # 콘텐츠와 이미지 가져오기
# url = "https://gall.dcinside.com/board/view/?id=dcbest&no=279518"  # 실제 URL로 변경하세요.
# title, content_texts, image_paths = get_content_from_url(url)

# # 영상 생성
# if title and content_texts and image_paths:
#     create_slideshow_with_audio(title, content_texts, image_paths, "youtube_short.mp4")
# else:
#     print("콘텐츠를 가져오지 못했습니다.")
