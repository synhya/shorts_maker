# main.py
from lib.insta_scraper import download_reels_by_hashtag, download_user_reels
from lib.api_video_uploader import upload_videos_from_folder

# 다운로드할 사용자 이름
# user_to_scrape = input("Enter the username to download reels: ")

# download_user_reels(user_to_scrape)

path = download_reels_by_hashtag("cat", min_likes=1000, min_comments=10, max_count=10)

upload_videos_from_folder(path)

# 다운로드한 Reels를 유튜브에 업로드
# Selenium을 사용하여 유튜브에 로그인하고 업로드