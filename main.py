from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

service = Service(executable_path=os.getenv('CHROME_DRIVER_PATH'))

driver = webdriver.Chrome(service=service)

try:
  driver.get('https://www.google.com')
  time.sleep(3)
  print(driver.title) # 페이지 타이틀 출력
finally:
  driver.quit()