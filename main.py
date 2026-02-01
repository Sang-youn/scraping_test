from web_scraper import ChromiumScraper
import json
import sys
from word_cloud import create_wordcloud
from datetime import datetime
import os


def main():
  
  srch_type = "google"
  if len(sys.argv) > 2:
    srch_type = sys.argv[2]
    
  with open('keyword.txt', 'r') as file:
    keywords = file.readlines()

  with ChromiumScraper(srch_type) as s:
    for keyword in keywords:
      s.search(keyword.strip())
      page_parse_list = s.get_search_results(s.driver.page_source)
      s.page_next()
      page_parse_list.extend(s.get_search_results(s.driver.page_source))
      unique_data = remove_duplicate(page_parse_list)
      # print(json.dumps(unique_data, indent=4, ensure_ascii=False))
      if not os.path.exists(f'./{datetime.now().strftime("%Y%m%d")}'):
        os.makedirs(f'./{datetime.now().strftime("%Y%m%d")}')
      print('--------------------------------')
      create_wordcloud(' '.join(list(map(lambda x: x['desc'], unique_data))), f'./{datetime.now().strftime("%Y%m%d")}/{srch_type}_{keyword.strip()}_{datetime.now().strftime("%H%M")}.png')
      print('--------------------------------')

# 중복제거
def remove_duplicate(list):
  unique_data = set(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in list)
  
  # null 값 제거
  return [json.loads(data) for data in unique_data if json.loads(data) is not None]

if __name__ == '__main__':
  main()