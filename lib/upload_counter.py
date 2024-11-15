import os
import json

COUNTER_FILE = "upload_counter.json"  # 숫자를 저장할 파일 이름

def get_next_counter():
    """저장된 숫자를 불러오고 증가시킵니다."""
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {"counter": 1}  # 파일이 없으면 초기값 설정

    current_number = data["counter"]
    data["counter"] += 1

    with open(COUNTER_FILE, "w") as file:
        json.dump(data, file)

    return current_number