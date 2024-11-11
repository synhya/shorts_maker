# content_scraper.py

import requests
from bs4 import BeautifulSoup
import os
from os.path import getsize

def get_content_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 1. 글 제목과 본문 텍스트 추출
    title_tag = soup.find("span", class_="title_subject")
    if title_tag is None:
        print("Title tag not found")
        return None, None, None
    title = title_tag.get_text(strip=True)

    # 본문 내용 텍스트 수집
    content_texts = []
    content_divs = soup.select(".writing_view_box .write_div div")
    for div in content_divs:
        text = div.get_text(strip=True)
        if text:
            content_texts.append(text)

    # 2. 이미지 URL 추출
    headers["Referer"] = url
    image_paths = []
    image_links = soup.select(".appending_file_box .appending_file li a")
    
    for index, link in enumerate(image_links, start=1):
        img_url = link.get("href")
        savename = f"{index}_{img_url.split('no=')[2]}"
        response = requests.get(img_url, headers=headers)
        
        # 이미지 저장
        path = f"Image/{savename}"
        if not os.path.exists("Image"):
            os.makedirs("Image")

        if os.path.isfile(path):
            if getsize(path) != len(response.content):
                print("이름은 겹치는 다른 파일입니다. 다운로드 합니다.")
                with open(path + "[1]", "wb") as file:
                    file.write(response.content)
        else:
            with open(path, "wb") as file:
                file.write(response.content)

        image_paths.append(path)

    return title, content_texts, image_paths
