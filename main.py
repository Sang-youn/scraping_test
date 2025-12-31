from web_scraper import ChromiumScraper

with open('keyword.txt', 'r') as file:
  keywords = file.readlines()

with ChromiumScraper('google') as s:
  for keyword in keywords:
    s.search(keyword.strip())
  print(s.driver.page_source)