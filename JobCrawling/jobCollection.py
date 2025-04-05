import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm
import warnings
import urllib3
import openpyxl
from openpyxl.styles import Alignment

# 경고 메시지를 무시하기 위해 설정 (보안 경고를 무시)
warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)

data = []  # 결과를 저장할 빈 리스트 초기화

# 사용자로부터 입력을 받는 부분
keyword = input("Enter Keyword: ")  # 검색할 키워드 입력
pageNum = input("How Many Pages? ")  # 크롤링할 페이지 수 입력

# 입력 값이 숫자인지 확인
if not pageNum.isdigit():
    print("페이지 번호는 숫자만 입력할 수 있습니다.")  # 페이지 번호가 숫자가 아닐 경우 오류 메시지 출력
    exit()  # 종료

# 각 페이지를 순차적으로 요청
for n in tqdm(range(1, int(pageNum) + 1)):  # 페이지 번호에 따라 반복 (tqdm으로 진행 상태 표시)
    try:
        # 페이지 요청 (Job Korea 사이트)
        response = req.get(f"https://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No={n}", 
                           headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
        
        # 응답이 성공적이지 않으면 해당 페이지를 스킵
        if response.status_code != 200:
            print(f"페이지 {n}을 불러오는 데 실패했습니다.")  # 실패한 페이지 번호 출력
            continue  # 다음 페이지로 넘어감
        
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = bs(response.text, "html.parser")
        jobs = soup.find_all("article", class_="list-item")  # 각 채용 공고를 찾기 위해 article 태그 사용

        for job in jobs:
            try:
                # 채용 기업명 추출
                jobName_tag = job.select_one("a.corp-name-link.dev-view")
                jobName = jobName_tag.text.strip() if jobName_tag else ""  # 기업명이 없으면 빈 문자열
                
                # 채용 제목 추출
                jobTitle_tag = job.select_one("a.information-title-link.dev-view")
                jobTitle = jobTitle_tag.text.strip() if jobTitle_tag else ""  # 채용 제목이 없으면 빈 문자열

                # 채용 제목 태그에서 URL 추출 (href 속성)
                if jobTitle_tag and "href" in jobTitle_tag.attrs:
                    url = jobTitle_tag["href"]
                    jobUrl = f"https://www.jobkorea.co.kr/{url}"  # 절대 URL로 변환
                else:
                    continue  # URL이 없으면 해당 공고는 건너뛰기

                # 추가 정보 항목 추출
                moreInfo = job.select("ul.chip-information-group > li.chip-information-item")

                # 각 항목 초기화
                jobMoreInfo = {'경력': None, '학력': None, '채용형태': None, '위치': None, '마감일': None, 'URL' : None}
                
                # 각 항목에서 필요한 정보 추출
                for item in moreInfo:
                    text = item.text.strip()
                    if any(keyword in text for keyword in ["경력", "신입", "경력무관"]):
                        jobMoreInfo['경력'] = text  # 경력 정보 저장
                    elif any(academic in text for academic in ["고졸", "학력무관", "석사", "대졸"]):
                        jobMoreInfo['학력'] = text  # 학력 정보 저장
                    elif any(sort in text for sort in ["정규직", "계약직","프리", "인턴", "연수생", "교육생"]):
                        jobMoreInfo['채용형태'] = text  # 채용 형태 정보 저장
                    elif any(city in text for city in ["서울", "경기"]):
                        jobMoreInfo['위치'] = text  # 위치 정보 저장
                    elif any(dueDate in text for dueDate in ["D-", "상시", "오늘"]):
                        jobMoreInfo['마감일'] = text  # 마감일 정보 저장
                    
                # 빈 값이나 "정보 없음"이 있을 경우 해당 공고를 데이터에 추가하지 않음
                if jobName != "" and jobTitle != "":
                    data.append([jobName, jobTitle, jobMoreInfo['경력'], jobMoreInfo['학력'], jobMoreInfo['채용형태'], jobMoreInfo['위치'], jobMoreInfo['마감일'], jobUrl])

            except Exception as e:
                print("Error:", e)  # 예외 발생 시 에러 메시지 출력

    except Exception as e:
        print(f"예외 발생: {e}")  # 페이지 요청 중 예외 발생 시 에러 메시지 출력

# DataFrame 생성
df = pd.DataFrame(data, columns=['companyName', 'title', 'career', 'academic', 'formOfEmployement', 'location', 'dueDate', 'url'])

# 엑셀 파일로 저장
df.to_excel('jobPosting.xlsx', index=False)

# 엑셀 파일 열기
wb = openpyxl.load_workbook('jobPosting.xlsx')
ws = wb.active

# 열 너비를 자동으로 조정
for col in ws.columns:
    max_length = 0
    column = col[0].column_letter  # 열 이름 가져오기
    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)  # 셀 값의 길이 중 최대 값 찾기
        except:
            pass
    adjusted_width = (max_length + 2)  # 여유 공간 추가
    ws.column_dimensions[column].width = adjusted_width  # 열 너비 조정

# 글자 잘리지 않게 셀 내용 자동 줄 바꿈 설정
for row in ws.iter_rows():
    for cell in row:
        cell.alignment = Alignment(wrap_text=True)  # 셀에 내용이 길면 자동으로 줄 바꿈 설정

# 저장
wb.save('jobPosting.xlsx')

print("Crawling Completed! Data is saved to jobPosting.xlsx with adjusted formatting.")  # 크롤링 완료 메시지 출력
