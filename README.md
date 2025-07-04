# AI-X 최종 보고서

## 📋 프로젝트 개요

이 프로젝트는 Google Sheets에서 팀별 작업 기록을 수집하고, OpenAI의 GPT 모델을 활용하여 각 팀원의 작업 내용을 요약하는 자동화 시스템입니다. 팀별 작업 내용을 효율적으로 분석하고 요약하여 CSV 파일로 출력합니다.

## 🏗️ 시스템 아키텍처

### 주요 구성 요소
- **데이터 수집**: Google Sheets API를 통한 작업 기록 수집
- **AI 요약**: OpenAI GPT-4o-mini 모델을 활용한 작업 내용 요약
- **데이터 처리**: 팀별/개인별 작업 분석 및 정리
- **결과 출력**: CSV 형태의 구조화된 요약 보고서

## 🚀 주요 기능

### 1. 자동 데이터 수집
- Google Sheets에서 일별 작업 기록 자동 수집
- 팀별, 개인별 작업 내용 자동 분류
- 날짜별 시트 데이터 순차 처리

### 2. AI 기반 요약
- **일별 요약**: 작업명, 문제/이슈, 해결방법, 결과를 바탕으로 한 줄 요약
- **전체 요약**: 개인별 전체 작업 내용을 5줄 이내 불릿 포인트로 요약
- 실무 중심의 문제 해결 관점에서 분석

### 3. 데이터 출력
- 조별 CSV 파일 자동 생성 (조1.csv ~ 조5.csv)
- 각 팀원별 날짜별 작업기록과 전체 요약 포함
- UTF-8 인코딩으로 한글 완벽 지원

## 📁 파일 구조

```
final_report/
├── main.py                          # 메인 실행 파일
├── credential.json  # Google Sheets API 인증 파일
├── .env                             # 환경변수 파일 (OpenAI API 키)
├── .gitignore                       # Git 제외 파일 목록
└── README.md                        # 프로젝트 문서
```

## ⚙️ 설치 및 실행

### 필요 패키지 설치
```bash
pip install gspread openai pandas python-dotenv google-auth
```

### 환경 설정
1. `.env` 파일에 OpenAI API 키 설정:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Google Sheets API 인증 파일 확인:
   - `credential.json` 파일이 프로젝트 루트에 위치해야 함

### 실행
```bash
python main.py
```

## 📊 출력 데이터 형식

### CSV 파일 구조
| 컬럼명 | 설명 |
|--------|------|
| 이름 | 팀원 이름 |
| 날짜별 작업기록 | 날짜별 일일 요약 내용 |
| 요약 | 전체 작업 내용의 5줄 이내 불릿 포인트 요약 |

### 요약 예시
- **일별 요약**: "2025-05-21: 하루 동안 기술 조사 및 연구 자료 소집을 통해 최종 프로젝트 아이디어를 구체화하고 평가 지표를 탐색함."
- **전체 요약**: 실무적 관점에서 문제 해결 중심의 불릿 포인트 형식

## 🔧 기술 스택

- **Python 3.x**: 메인 개발 언어
- **Google Sheets API**: 데이터 수집
- **OpenAI GPT-4o-mini**: AI 요약 생성
- **pandas**: 데이터 처리 및 CSV 출력
- **gspread**: Google Sheets 연동#
