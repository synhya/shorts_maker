from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle

# 설정
CHROME_DRIVER_PATH = "chromedriver"  # 크롬드라이버 경로
COOKIES_PATH = "cookies.pkl"  # 쿠키 저장 경로
YOUTUBE_UPLOAD_URL = "https://www.youtube.com/upload"

def save_cookies(driver, path):
    """브라우저 쿠키 저장"""
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path):
    """저장된 쿠키 불러오기"""
    if os.path.exists(path):
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

def login_youtube(driver):
    """YouTube 로그인"""
    driver.get("https://accounts.google.com/")
    print("로그인 후 Enter 키를 누르세요...")
    input()  # 사용자가 직접 로그인 후 Enter

    # 로그인 완료 후 쿠키 저장
    save_cookies(driver, COOKIES_PATH)

def upload_video(driver, video_path, title, description):
    """YouTube에 동영상 업로드"""
    driver.get(YOUTUBE_UPLOAD_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    # 파일 업로드
    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(video_path)
    print("동영상 업로드 시작...")

    # 제목 입력
    title_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='제목']"))
    )
    title_box.clear()
    title_box.send_keys(title)

    # 설명 입력
    description_box = driver.find_element(By.XPATH, "//textarea[@aria-label='설명']")
    description_box.clear()
    description_box.send_keys(description)

    # 업로드 완료 대기 후 게시
    time.sleep(10)  # 동영상 처리 대기
    next_button = driver.find_elements(By.XPATH, "//ytcp-button[@id='next-button']")
    for _ in range(3):  # 세 번 Next 버튼 클릭
        next_button[0].click()
        time.sleep(2)

    # 게시 버튼 클릭
    publish_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='done-button']"))
    )
    publish_button.click()

    print("업로드 완료!")

if __name__ == "__main__":
    # 크롬드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)

    try:
        driver.get("https://www.youtube.com/")
        load_cookies(driver, COOKIES_PATH)  # 쿠키 로드
        driver.refresh()

        if "login" in driver.current_url:
            print("로그인 필요")
            login_youtube(driver)

        video_path = "path_to_video.mp4"  # 업로드할 동영상 경로
        title = "Sample Title"  # 동영상 제목
        description = "Sample Description"  # 동영상 설명

        upload_video(driver, video_path, title, description)
    finally:
        driver.quit()
