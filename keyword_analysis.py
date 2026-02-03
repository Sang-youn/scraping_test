from collections import Counter
from konlpy.tag import Okt
import csv
from datetime import date
import os

def keyword_analysis(keywords, top_n=30):
  # 형태소 분석 
  okt = Okt()
  nouns = okt.nouns(keywords)
  words = [word for word in nouns if len(word) > 1]
  
  count = Counter(words)
  return count.most_common(top_n)

def save_keyword_analysis(keyword_analysis, filename='keyword_analysis.csv'):
  today = date.today().strftime('%Y-%m-%d')
  
  # 처음 만들어진 파일인지 확인하기 위해 행 개수를 카운트
  row_count = 0
  
  # 날짜가 있는지 확인용 변수
  date_exists = False
  
  # print(f'os.path.exists({filename}): {os.path.exists(filename)}')
  # 해당 날짜가 있으면 추가하지 않도록 수정 
  if os.path.exists(filename):
    with open(filename, 'r') as f:
      reader = csv.reader(f)
      rows = list(reader)
      row_count = len(rows)
      for row in rows:
        if row[0] == today:
          date_exists = True
          break
        
  with open(filename, 'a') as f:
    writer = csv.writer(f)
    if row_count == 0:
      writer.writerow(['date', 'keyword', 'count'])
    if not date_exists:
      for keyword, count in keyword_analysis:
        writer.writerow([today, keyword, count])
      