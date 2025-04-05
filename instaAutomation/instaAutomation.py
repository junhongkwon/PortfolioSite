##instagram

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import os

import mdata

# 대기 시간 random
wait_time = random.uniform(5, 15)

# 필요한 변수 정의
insta_id = input('Enter Instagram ID : ')
insta_pw = input('Enter Instagram PW : ')
insta_tag = input('Enter Hashtag : ')
insta_cnt = int(input('Count : '))
insta_comm = [
    "오늘도 최고예요! ", "당신의 하루가 행복으로 가득하길! ", "너무 멋져요! 응원할게요! ", "보는 것만으로도 기분이 좋아지네요! ",
    "긍정적인 에너지가 전해져요! ", "당신 덕분에 하루가 밝아졌어요! ", "항상 응원하고 있어요! ", "정말 감동적인 순간이에요! ",
    "계속 빛나는 하루 보내세요! ", "사랑과 행복이 가득한 하루 되세요! ", "당신의 미소가 최고예요! ", "너무 귀엽고 사랑스러워요! ",
    "에너지가 넘치네요! ", "언제나 당신을 응원해요! ", "최고예요! 자신감을 가지세요! ", "오늘도 빛나는 하루 보내세요! ",
    "당신의 노력에 박수를 보냅니다! ", "정말 멋진 순간이에요! ", "행복이 가득한 날 되세요! ", "매일매일 행복하시길 바라요! ",
    "당신은 소중한 사람이에요! ", "너무 사랑스럽고 멋져요! ", "세상에서 가장 빛나는 사람! ", "모든 순간이 아름답길 바라요! ",
    "당신 덕분에 미소가 지어졌어요! ", "웃는 모습이 너무 아름다워요! ", "오늘도 파이팅! ", "당신의 존재만으로도 빛나요! ",
    "행복한 하루 되세요! ", "지금 이 순간, 당신이 최고예요! ", "당신의 꿈을 응원해요! ", "모든 일이 잘 풀릴 거예요! ",
    "세상을 밝히는 에너지가 느껴져요! ", "당신이 있어서 너무 좋아요! ", "오늘도 반짝이는 하루 보내세요! ",
    "사랑과 기쁨이 가득하길! ", "당신의 노력이 빛을 발할 거예요! ", "힘든 날도 있지만, 당신은 멋져요! ",
    "언제나 따뜻한 마음이 전해져요! ", "행운이 가득한 하루 되세요! ", "당신 덕분에 기분이 좋아졌어요! ",
    "늘 건강하고 행복하세요! ", "당신의 밝은 에너지가 좋아요! ", "힘내세요! 당신은 할 수 있어요! ",
    "오늘도 좋은 일만 가득하길! ", "당신은 충분히 멋져요! ", "최고의 하루 보내세요! ", "당신을 응원하는 사람이 많아요! ",
    "미소가 참 예뻐요! ", "오늘도 빛나는 하루 보내세요! ", "당신 덕분에 힘이 나요! ", "아름다운 날 보내세요! ",
    "매 순간이 행복하길 바라요! ", "세상에서 하나뿐인 소중한 존재! ", "당신의 꿈이 이뤄지길 응원해요! ",
    "언제나 밝은 모습이 너무 좋아요! ", "당신의 긍정적인 에너지가 최고예요! ", "정말 멋지고 특별한 사람이에요! ",
    "늘 행복하고 건강하세요! ", "지금 이 순간을 즐기세요! ", "당신의 미소가 힘이 돼요! ", "오늘도 좋은 하루 보내세요! ",
    "마음이 따뜻해지는 순간이에요! ", "세상에 더 많은 행복이 가득하길! ", "당신의 열정이 느껴져요! ",
    "너무 멋져요! 계속 도전하세요! ", "당신은 충분히 빛나고 있어요! ", "소중한 순간을 함께할 수 있어 행복해요! ",
    "당신 덕분에 하루가 밝아졌어요! ", "모든 꿈이 이루어지길 바라요! ", "긍정적인 기운이 가득 느껴져요! ",
    "행복이 넘치는 하루 보내세요! ", "세상을 환하게 만드는 사람이에요! ", "언제나 응원할게요! 힘내세요! ",
    "오늘도 감사한 하루 보내세요! ", "당신은 세상에서 하나뿐인 소중한 존재! ", "당신의 하루가 특별하길 바라요! ",
    "행복과 사랑이 가득한 날 되세요! ", "반짝이는 순간을 만끽하세요! ", "당신의 에너지가 너무 좋아요! ",
    "언제나 긍정적인 마음으로! ", "모든 순간이 특별하길 바라요! ", "당신을 보면 행복해져요! ", "오늘도 소중한 하루 보내세요! ",
    "당신의 따뜻한 마음이 전해져요! ", "긍정적인 생각이 행복을 가져와요! ", "당신의 미소는 세상을 밝히는 빛이에요! ",
    "모든 일이 잘 풀릴 거예요! ", "당신의 하루가 반짝이길! ", "언제나 즐겁고 행복한 순간이 가득하길! ",
    "소중한 사람들과 함께 행복하세요! ", "당신은 항상 멋져요! ", "세상을 밝히는 당신이 좋아요! ",
    "오늘도 사랑이 넘치는 하루 보내세요! ", "당신의 밝은 에너지가 최고예요! ", "기분 좋은 하루 보내세요! ",
    "매일매일 특별한 순간을 만드세요! ", "당신 덕분에 행복한 기운이 전해져요! "
]

# 크롬드라이버 로딩
option = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
option.add_experimental_option("detach", True)
option.add_argument('user-agent=' + user_agent)
service = Service()
driver = webdriver.Chrome(options=option, service=service)
driver.maximize_window()

driver.get("https://instagram.com/")

time.sleep(10)

WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR,
     "#loginForm > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(1) > div > label > input")
))

driver.find_element(By.CSS_SELECTOR, "#loginForm > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(1) > div > label > input").send_keys(mdata.id)
driver.find_element(By.CSS_SELECTOR, "#loginForm > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(2) > div > label > input").send_keys(mdata.pw)
driver.find_element(By.CSS_SELECTOR, "#loginForm > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(3)").click()

# 잠시 대기
time.sleep(wait_time)

# 4. 작업할 해시태그 검색 결과 페이지로 이동
driver.get(f'https://www.instagram.com/explore/tags/{insta_tag}/')
time.sleep(wait_time)


first_feed = driver.find_elements(By.CSS_SELECTOR, "div._aagw")
time.sleep(wait_time)
first_feed[0].click()


for idx in range(insta_cnt) :

    time.sleep(wait_time)
    next_btn = driver.find_element(By.CSS_SELECTOR, 'body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div:nth-child(1) > div > div > div._aaqg._aaqh > button > div > span > svg')
    # 좋아요 버튼 가져오기
    like_btn = driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="좋아요"], svg[aria-label="좋아요 취소"]')

    # 좋아요가 눌려있는지 체크
    is_liked = like_btn.get_attribute("aria-label") == "좋아요 취소"

    if not is_liked:
        actions = ActionChains(driver)
        actions.move_to_element(like_btn).click().perform()
        try:
            # 댓글 입력창 찾기
            comment_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="댓글 달기..."]'))
            )

            # 댓글창 클릭
            comment_box.click()
            time.sleep(1)  # 안정성을 위해 잠시 대기

            # 랜덤 댓글 선택
            comment_text = random.choice(insta_comm)

            # 댓글 입력 및 등록
            time.sleep(5)
            comment_box = driver.find_element(By.XPATH, '//textarea[@aria-label="댓글 달기..."]')
            comment_box.send_keys(comment_text)
            time.sleep(5)  # 입력 후 대기
            comment_box.send_keys(Keys.ENTER)

            # 다음 게시물로 이동을 위해 잠시 대기
            time.sleep(3)
            next_btn.click()
        except Exception as e:
            print(f"댓글 입력 중 오류 발생: {e}")
    else:
        next_btn.click()


print(f"작업 완료 : {idx + 1} 회")
