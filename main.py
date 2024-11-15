# main.py
from lib.insta_scraper import download_user_reels
from lib.api_video_uploader import upload_videos_from_folder

# 다운로드할 사용자 이름
user_to_scrape = input("Enter the username to download reels: ")

path = f"vids/{user_to_scrape}_reels"
download_user_reels(path, user_to_scrape)

upload_videos_from_folder(path, user_to_scrape)

# 다운로드한 Reels를 유튜브에 업로드
# Selenium을 사용하여 유튜브에 로그인하고 업로드