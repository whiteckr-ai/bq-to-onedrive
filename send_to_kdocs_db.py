import csv
import requests
import sys
import os

TOKEN = os.environ.get("KDOCS_TOKEN")
FILE_ID = os.environ.get("KDOCS_DB_FILE_ID")
CSV_FILE = "result.csv"  

DB_SCRIPT_NAME = "V2-5vnUpdVQGXoWN9loeiAx39" 

if not TOKEN or not FILE_ID:
    print("❌ 에러: 토큰이나 문서 ID 누락")
    sys.exit(1)

db_records = []
try:
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f) # 💡 단순 배열 모드로 원복
        header = next(reader)  # 💡 첫 줄(헤더)은 건너뛰고 순수 데이터만 담습니다.
        for row in reader:
            db_records.append(row)
except Exception as e:
    print(f"❌ CSV 읽기 실패: {e}")
    sys.exit(1)

API_URL = f"https://www.kdocs.cn/api/v3/ide/file/{FILE_ID}/script/{DB_SCRIPT_NAME}/sync_task"

headers = {
    "Content-Type": "application/json",
    "AirScript-Token": TOKEN
}

# 💡 테스트를 위해 5개만 전송합니다.
payload = {
    "Context": {
        "argv": {
            "records": db_records[:5] 
        }
    }
}

print("🚀 KDocs DB로 전송 시작... (테스트용 5개 전송)")

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    print(f"📩 응답: {response.text}")
    if response.status_code == 200:
        print("✅ 통신 완료!")
    else:
        print(f"⛔ 실패: {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ 통신 에러: {e}")
    sys.exit(1)
