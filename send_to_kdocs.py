import csv
import requests
import sys
import os

TOKEN = os.environ.get("KDOCS_TOKEN")
FILE_ID = os.environ.get("KDOCS_FILE_ID")
CSV_FILE = "result.csv"  
SCRIPT_NAME = "V2-7ywFu9flguvfUNoAffFcws"  # KDocs에 작성한 함수 이름

if not TOKEN or not FILE_ID:
    print("❌ 에러: 토큰이나 문서 ID가 설정되지 않았습니다.")
    sys.exit(1)

# 1. CSV 파일을 DB 레코드 구조로 읽기
db_records = []
try:
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f) # 💡 핵심: 헤더를 Key로 하는 딕셔너리로 읽음
        for row in reader:
            # KDocs DB가 요구하는 { "fields": { "컬럼명": "값" } } 형태로 조립
            db_records.append({"fields": dict(row)})
except Exception as e:
    print(f"❌ CSV 읽기 실패: {e}")
    sys.exit(1)

# 2. KDocs API 주소 및 헤더 설정
API_URL = f"https://www.kdocs.cn/api/v3/ide/file/{FILE_ID}/script/{SCRIPT_NAME}/sync_task"

headers = {
    "Content-Type": "application/json",
    "AirScript-Token": TOKEN
}

# 3. KDocs가 인식하는 Context.argv 형태로 포장
payload = {
    "Context": {
        "argv": {
            "records": db_records  # 💡 변수명을 DB스럽게 'records'로 변경
        }
    }
}

# 4. 데이터 전송
print(f"🚀 KDocs DB로 데이터 전송 시작... (총 {len(db_records)}개 레코드)")
try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        print("✅ KDocs DB 업데이트 성공!")
    else:
        print(f"⛔ KDocs 업데이트 실패! (상태코드: {response.status_code})")
        print(response.text)
        sys.exit(1)
except Exception as e:
    print(f"❌ 통신 에러: {e}")
    sys.exit(1)
