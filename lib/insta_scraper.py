import instaloader
from instaloader import Profile
import requests

# Instaloader 인스턴스 생성
L = instaloader.Instaloader(download_video_thumbnails=False)

# 로그인 함수 (필요한 경우)
def login(username, password):
    try:
        L.login(username, password)
        print("Logged in successfully.")
    except Exception as e:
        print(f"Login failed: {e}")

# 사용자 Reels를 다운로드하는 함수
def download_user_reels(target_user, proxies=None):
    # 프로필 정보 로드
    try:
        profile = Profile.from_username(L.context, target_user)
    except Exception as e:
        print(f"Failed to load profile: {e}")
        return
    
    # Reels 스크래핑 및 다운로드
    for post in profile.get_posts():
        if post.is_video and post.typename == 'GraphVideo':
            print(f"Downloading Reel: {post.url}")
            L.download_post(post, target=f"{target_user}_reels")
    print(f"Downloaded all reels from {target_user}.")

# 프록시를 사용하여 실시간 Reels 가져오기
def fetch_reel_video(reel_url, proxies=None):
    try:
        response = requests.get(reel_url, proxies=proxies)
        if response.status_code == 200:
            with open("reel_video.mp4", "wb") as f:
                f.write(response.content)
            print("Downloaded Reel video successfully.")
        else:
            print("Failed to fetch Reel video.")
    except Exception as e:
        print(f"Error fetching video: {e}")