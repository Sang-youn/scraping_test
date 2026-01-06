from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import os
import time

# 구글 검색 결과 추출
def google_search_result(result):
  result_list = []
  if result.select_one('a[jsname="UWckNb"]') :
    desc_elem = list(map(lambda x: f'div[style="-webkit-line-clamp:{x}"]', [1,2,3]))
    desc = ','.join(desc_elem)
    
    result_dict = {
      'site': ' || '.join(list(map(lambda x: x.text, result.select_one('div.CA5RN').select('div')))),
      'title': result.select_one('a[jsname="UWckNb"] > h3').text,
      'url': result.select_one('a[jsname="UWckNb"]').get('href'),
      'desc': result.select_one(desc).text,
      'rpos': result.get('data-rpos', '9999')
    }
    result_list.append(result_dict)
  else:
    pass
  
  return result_list

# 구글 검색 정보
google_search = {
  'url': 'https://www.google.com',
  'search_box': 'textarea[name="q"]',
  'search_button': 'input[type="submit"][name="btnK"]',
  'search_results': 'div.MjjYud > div.A6K0A',
  'select' : google_search_result # 구글 검색 결과 추출 함수를 dict에 저장
}


# 검색 타입(일단 구글만 먼저)
srch_dict = {'google': google_search}

class ChromiumScraper:

  # 생성자
  def __init__(self, srch_type):
     # 검색 타입 체크
    if srch_type not in srch_dict:
      raise ValueError(f"Invalid search type: {srch_type}")
    self.srch_info = srch_dict.get(srch_type)
  
  # 컨텍스트 매니저 시작
  def __enter__(self):
    # print(f"ChromiumScraper __enter__: {self.srch_info}")
    try:
      service = Service(executable_path=os.getenv('CHROME_DRIVER_PATH'))
      options = webdriver.ChromeOptions()
      # 로봇이 아닙니다 방지
      options.add_argument("--disable-blink-features=AutomationControlled")
      self.driver = webdriver.Chrome(service=service, options=options)
      return self
    
    except Exception as e:
      print(f"Error: {e}")
      return None

  # 컨텍스트 매니저 종료
  def __exit__(self, exc_type, exc_value, traceback):
      print("ChromiumScraper __exit__")
      self.driver.quit()
  
  # 검색 시작
  def search(self, keyword):
    print(f"ChromiumScraper search: {keyword}")
    # print(f"ChromiumScraper search: {self.srch_info}")
    self.driver.get(self.srch_info['url'])
    self.driver.implicitly_wait(1)
    elem = self.driver.find_element(By.CSS_SELECTOR, self.srch_info['search_box'])
    elem.clear() # 검색창 초기화
    elem.send_keys(keyword) # 검색창에 'Python' 입력
    elem.send_keys(Keys.RETURN) # 검색창에 입력한 내용 전송
    time.sleep(1)
    return self.driver.page_source

  def get_search_results(self, page_source):
    soup = bs(page_source, 'html.parser')
    search_results = soup.select(self.srch_info['search_results'])
    return list(map(lambda x: self.srch_info['select'](x), search_results))
    
    
