import json

def get_path (username, category):
    return f"vids/{category}/{username}_reels" 
  
def save_to_json(data, file_path):
    """데이터를 JSON 파일로 저장"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved metadata to {file_path}")