from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

service = Service(executable_path=os.getenv('CHROME_DRIVER_PATH'))


try:
  options = webdriver.ChromeOptions()
  
  # 로봇이 아닙니다 방지
  options.add_argument("--disable-blink-features=AutomationControlled")
  driver = webdriver.Chrome(service=service, options=options)
  
  # 키워드 파일을 읽는다
  with open('keyword.txt', 'r') as file:
    keywords = file.readlines()
    for keyword in keywords:
      keyword = keyword.strip() # 키워드 공백제거
      print(keyword)
      driver.get('https://www.google.com')
      driver.implicitly_wait(1)
      print(driver.title) # 페이지 타이틀 출력
      elem = driver.find_element(By.NAME, "q") # 검색창 찾기
      elem.clear() # 검색창 초기화
      elem.send_keys(keyword) # 검색창에 'Python' 입력
      elem.send_keys(Keys.RETURN) # 검색창에 입력한 내용 전송
      time.sleep(1)

  time.sleep(3)
  driver.close()
finally:
  driver.quit()