import os
import pickle
import pathlib
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from lib.upload_counter import get_next_counter
from lib.utils.index import get_path

# 필요한 권한 스코프
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    """YouTube API 클라이언트 인증"""
    creds = None
    token_path = 'token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    youtube = build('youtube', 'v3', credentials=creds)
    return youtube

def upload_video(youtube, file_path, title, description):
    """동영상 업로드"""
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['example', 'video'],
            'categoryId': '22',  # 'People & Blogs'
        },
        'status': {
            'privacyStatus': 'public',  # 공개 상태: 'public', 'private', 'unlisted'
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"업로드 진행률: {int(status.progress() * 100)}%")
        except Exception as e:
            print(f"업로드 중 오류 발생: {e}")
            return
    print("업로드 완료:", response.get('id'))

def upload_videos_from_folder(folder_path):
    """폴더 내 모든 동영상 업로드"""
    youtube = authenticate_youtube()
    folder_path = get_path(user, "user")
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')):
            file_path = os.path.join(folder_path, file_name)
            counter = get_next_counter()
            title = f"Epic Moments #{counter}"  # 번호 추가
            description = f"@{user}"  #f"{title}의 설명입니다."
            print(f"업로드 시작: {file_name} (Title: {title})")
            upload_video(youtube, file_path, title, description)
        else:
            print(f"지원되지 않는 파일 형식: {file_name}")


