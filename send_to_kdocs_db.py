import csv
import requests
import sys
import os

TOKEN = os.environ.get("KDOCS_TOKEN")
FILE_ID = os.environ.get("KDOCS_DB_FILE_ID")
CSV_FILE = "result.csv"  

# 💡 주의: 기존 일반 시트용 스크립트 이름과 달라야 합니다! 
# KDocs에서 DB 전용으로 새로 만드신 스크립트 함수의 이름을 넣으세요.
DB_SCRIPT_NAME = "V2-5vnUpdVQGXoWN9loeiAx39" 

if not TOKEN or not FILE_ID:
    print("❌ 에러: 토큰이나 문서 ID 누락")
    sys.exit(1)

# CSV를 DB 형태(Dict)로 읽기
db_records = []
try:
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            db_records.append({"fields": dict(row)})
except Exception as e:
    print(f"❌ CSV 읽기 실패: {e}")
    sys.exit(1)

API_URL = f"https://www.kdocs.cn/api/v3/ide/file/{FILE_ID}/script/{DB_SCRIPT_NAME}/sync_task"

headers = {
    "Content-Type": "application/json",
    "AirScript-Token": TOKEN
}

payload = {
    "Context": {
        "argv": {
            "records": db_records
        }
    }
}

print(f"🚀 KDocs DB로 전송 시작... (전체 {len(db_records)}개 중 테스트용 5개만 전송)")

# 💡 테스트를 위해 앞에서부터 딱 5개의 레코드만 쪼개서 보냅니다.
test_payload = {
    "Context": {
        "argv": {
            "records": db_records[:5] 
        }
    }
}

try:
    response = requests.post(API_URL, headers=headers, json=test_payload, timeout=30)
    
    # 💡 KDocs의 JSON 응답을 파싱해서 잘리지 않게 한 줄씩 출력합니다.
    try:
        resp_json = response.json()
        logs = resp_json.get("data", {}).get("logs", [])
        
        print("📩 [KDocs 상세 에러 추적 로그]")
        for log in logs:
            if isinstance(log, dict) and "args" in log:
                print(f" ➔ {log['args'][0]}")
                
        if response.status_code == 200:
            print("✅ 통신은 완료되었습니다. (위의 ➔ 로그에서 에러 원인을 확인하세요)")
        else:
            print(f"⛔ KDocs DB 실패: 상태코드 {response.status_code}")
            sys.exit(1)
            
    except Exception as parse_e:
        print(f"📩 원본 응답: {response.text}")

except Exception as e:
    print(f"❌ DB 통신 에러: {e}")
    sys.exit(1)
