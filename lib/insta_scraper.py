import instaloader
from instaloader import Hashtag, Profile
import requests
import json
import os

from lib.utils.index import get_path, save_to_json

# Instaloader 인스턴스 생성
L = instaloader.Instaloader(download_video_thumbnails=True)

# 로그인 함수 (필요한 경우)
def login(username, password):
    try:
        L.login(username, password)
        print("Logged in successfully.")
    except Exception as e:
        print(f"Login failed: {e}")
        
# 썸네일 다운로드 함수
def download_thumbnail(url, save_path):
    """썸네일 다운로드"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return save_path
        else:
            print(f"Failed to download thumbnail: {url}")
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")
    return None

# 사용자 Reels를 다운로드하는 함수
def download_user_reels(target_user, min_likes=10000, min_comments=10, proxies=None):
    try:
        profile = Profile.from_username(L.context, target_user)
    except Exception as e:
        print(f"Failed to load profile: {e}")
        return

    path = get_path(target_user, "user")
    metadata = []

    # Reels 스크래핑 및 다운로드
    for post in profile.get_posts():
        if post.is_video and post.typename == 'GraphVideo' and post.likes >= min_likes and post.comments >= min_comments:
            print(f"Downloading Reel: {post.url}")
            L.download_post(post, target=path)

            # 썸네일 다운로드
            thumbnail_path = os.path.join(path, f"{post.shortcode}_thumbnail.jpg")
            thumbnail_downloaded = download_thumbnail(post.url, thumbnail_path)

            # 메타데이터 저장
            metadata.append({
                "username": target_user,
                "likes": post.likes,
                "comments": post.comments,
                "view_count": post.video_view_count,
                "post_url": post.url,
                "download_path": os.path.join(path, f"{post.shortcode}.mp4"),
                "thumbnail_path": thumbnail_downloaded if thumbnail_downloaded else "Thumbnail not available"
            })

    # JSON 저장
    json_file_path = os.path.join(path, "metadata.json")
    save_to_json(metadata, json_file_path)

    print(f"Downloaded all reels from {target_user}.")
    return path

# 특정 해시태그의 릴스 다운로드
def download_reels_by_hashtag(hashtag, min_likes=10000, min_comments=10, max_count=10):
    try:
        tag = Hashtag.from_name(L.context, hashtag)
    except Exception as e:
        print(f"Failed to load hashtag: {e}")
        return []

    print(f"Fetching reels for #{hashtag}...")
    path = get_path(hashtag, "hashtag")
    metadata = []
    count = 0

    for post in tag.get_posts():
        if post.is_video and post.typename == 'GraphVideo' and post.likes >= min_likes and post.comments >= min_comments:
            print(f"Downloading Reel: {post.url}")
            L.download_post(post, target=path)

            # 썸네일 다운로드
            thumbnail_path = os.path.join(path, f"{post.shortcode}_thumbnail.jpg")
            thumbnail_downloaded = download_thumbnail(post.url, thumbnail_path)

            # 메타데이터 저장
            metadata.append({
                "username": post.owner_username,
                "likes": post.likes,
                "comments": post.comments,
                "view_count": post.video_view_count,
                "post_url": post.url,
                "download_path": os.path.join(path, f"{post.shortcode}.mp4"),
                "thumbnail_path": thumbnail_downloaded if thumbnail_downloaded else "Thumbnail not available"
            })

            count += 1
            if count >= max_count:
                break

    # JSON 저장
    json_file_path = os.path.join(path, "metadata.json")
    save_to_json(metadata, json_file_path)

    print(f"Downloaded {count} reels for #{hashtag}.")
    return path
