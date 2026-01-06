from web_scraper import ChromiumScraper
import json

with open('keyword.txt', 'r') as file:
  keywords = file.readlines()

with ChromiumScraper('google') as s:
  for keyword in keywords:
    s.search(keyword.strip())
    print(json.dumps(s.get_search_results(s.driver.page_source), indent=4, ensure_ascii=False))
    print('--------------------------------')
  