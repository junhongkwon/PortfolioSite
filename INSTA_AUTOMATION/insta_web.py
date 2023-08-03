import time
import random
import chromedriver_autoinstaller 
import mdata

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


def instaBot():
    
    #크롬드라이버 로딩
    chromedriver_autoinstaller.install()
    option = webdriver.ChromeOptions()
    service = Service()
    driver = webdriver.Chrome(options=option, service=service)
    driver.maximize_window()

    #인스타그램 페이지 방문
    driver.get("https://instagram.com/")

    #로그인 화면이 나올때 까지 Waiting
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    ))

    #ID, PW 입력 후 클릭하여 로그인
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(mdata.id)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(mdata.pw)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()

    #검색 창에 키워드를 입력한 후, 해당 페이지로 이동
    driver.implicitly_wait(15)
    driver.find_element(By.CLASS_NAME, '_ac8f').click() 
    driver.implicitly_wait(15)
    driver.find_element(By.CLASS_NAME, "_a9--._a9_1").click()
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "div[class='x1iyjqo2 xh8yej3'] div:nth-child(2) span:nth-child(1) div:nth-child(1) a:nth-child(1) div:nth-child(1) div:nth-child(2) div:nth-child(1) div:nth-child(1) span:nth-child(1) span:nth-child(1)").click()
    driver.implicitly_wait(10)
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'x1lugfcp').send_keys("여행")
    driver.implicitly_wait(10)
    driver.get("https://www.instagram.com/explore/locations/531628454/")

    #목표 링크 N개 추출하기
    all_posting_sel = "div[id^='mount_0_0'] > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div > div.x78zum5.xdt5ytf.x10cihs4.x1t2pt76.x1n2onr6.x1ja2u2z > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y > section > main > article > div:nth-child(4) > div"
    #키워드로 검색한 포스팅 게시물이 나타날때 까지 대기(30초 안에 나타나면 즉시 다음 프로세스 진행)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, all_posting_sel)
    ))

    
    links = []
    #N번 스크롤 내리기(포스팅 개수가 쌓일만큼 스크롤하기)
    while len(links) < 30:
        for _ in range(2):
             driver.execute_script("window.scrollBy(0,600);")
             time.sleep(0.3)

            #포스팅 링크 추출하기 href 추출
        all_posting_box = driver.find_element(By.CSS_SELECTOR, all_posting_sel)
        post_links = all_posting_box.find_elements(By.TAG_NAME, "a") # return []

        for eachLink in post_links:
            link = eachLink.get_attribute('href')
            links.append(link)

        #중복제거
        links = set(links) #중복 제거
        links = list(links) #리스트로 자료형 변환



    #N개의 링크를 모두 추출 성공
    with open('instaLinks.txt', 'a') as f:
        for link in links:
            f.write(f"{link}\n")
    print("************")    
    print(len(links), "개의 링크를 추출하였습니다.")


    #N개의 링크를 읽기
    instaLinks = []
    with open('instaLinks.txt', "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            instaLinks.append(line.rstrip())


    #추출한 인스타그램 링크 방문
    cnt = 1

    for instalink in instaLinks:
        time.sleep(random.uniform(6, 10))
        print(f"{cnt} 번째 링크 방문")
        driver.get(instalink)
        time.sleep(random.uniform(5, 10))
        
        cnt=cnt+1
    
        #방문한 링크마다 좋아요 누르기

        like_btn = driver.find_element(By.CLASS_NAME, 'xp7jhwk')
        btn_svg = like_btn.find_element(By.TAG_NAME, 'svg') 
        svg = btn_svg.get_attribute('aria-label')
        
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'xp7jhwk')
        ))
        
        if(svg=="좋아요"):
            like_btn.click()
            time.sleep(random.uniform(5, 10))
        else :  
            pass

    print("모든 작업 완료")
    # driver.quit()
    # input()

instaBot()



