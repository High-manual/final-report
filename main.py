import os
import gspread
import openai
import pandas as pd
import logging
from collections import defaultdict
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    logger.info("스프레드시트 열기 시도 중...")
    spreadsheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1BQvsUDaQJwM2VaGOk0q4JsAuSDwyMu_LY3eW9QJynDY/edit"
    )
    sheet_list = spreadsheet.worksheets()
    logger.info(f"{len(sheet_list)}개의 시트를 발견함")
except Exception:
    logger.exception("스프레드시트 열기 또는 인증에 실패했습니다.")
    exit(1)

grouped_tasks = defaultdict(list)

def summarize_day(task, issue, method, result):
    try:
        prompt = (
            "다음은 하루 동안 수행한 작업입니다. 이 내용을 기반으로 하루 작업 전체를 실무적으로 간결하게 1줄로 요약해 주세요.\n\n"
            f"작업명: {task}\n문제: {issue}\n해결방법: {method}\n결과: {result}"
        )
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "넌 실무 요약 전문가야."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip() if response.choices[0].message.content else ""
    except Exception:
        logger.exception("하루 요약 중 오류 발생")
        return "요약 실패"

def summarize_overall(logs):
    try:
        prompt = (
            "다음은 한 담당자의 날짜별 작업 요약입니다.\n"
            "이 사람의 활동을 실무적으로 분석해 문제 해결 중심으로 요약해 주세요.\n"
            "줄글이 아닌 불릿 포인트 형식으로 5줄 이내로 작성해 주세요.\n\n"
            "작업 요약:\n" + "\n".join(f"- {log}" for log in logs)
        )
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "넌 기업 실무 요약 전문가야."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip() if response.choices[0].message.content else ""
    except Exception:
        logger.exception("전체 요약 중 오류 발생")
        return "전체 요약 실패"

for sheet in sheet_list:
    date = sheet.title.strip()
    logger.info(f"'{date}' 시트 처리 중")
    try:
        df = pd.DataFrame(sheet.get_all_records())
    except Exception:
        logger.exception(f"{date} 시트 읽기 실패")
        continue

    for _, row in df.iterrows():
        group = str(row.get('조', '')).strip()
        name = str(row.get('이름', '')).strip()
        if not group or not name:
            continue

        task = str(row.get('작업명', '')).strip()
        issue = str(row.get('문제/이슈', '')).strip()
        method = str(row.get('해결방법', '')).strip()
        result = str(row.get('결과 내용', '')).strip()
        
        if not (task or issue or method or result):
            continue

        summary = summarize_day(task, issue, method, result)
        grouped_tasks[(group, name)].append(f"{date}: {summary}")

logger.info(f"{len(grouped_tasks)}명의 담당자 작업기록 요약 완료")

output_dir = "조별_간결요약_CSV"
os.makedirs(output_dir, exist_ok=True)

results_by_group = defaultdict(list)

for (group, name), logs in grouped_tasks.items():
    logger.info(f"전체 요약 생성 중: [조 {group}] {name}")
    summary = summarize_overall(logs)
    per_day_log = "\n".join(logs)
    results_by_group[group].append({
        '이름': name,
        '날짜별 작업기록': per_day_log,
        '요약': summary
    })

logger.info("CSV 저장 시작")
for group, records in results_by_group.items():
    try:
        df = pd.DataFrame(records)
        filename = f"조{group}.csv"
        df.to_csv(os.path.join(output_dir, filename), index=False, encoding='utf-8')
        logger.info(f"저장 완료: {filename}")
    except Exception:
        logger.exception(f"조 {group} CSV 저장 실패")

logger.info("작업 완료")
