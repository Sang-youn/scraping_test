import matplotlib.pyplot as plt
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
from PIL import Image
import numpy as np

def create_wordcloud(text, filename = 'wordcloud.png'):
  okt = Okt()
  nouns = okt.nouns(text)
  words = [word for word in nouns if len(word) > 1]
  count = Counter(words)
  # 마스크 이미지 적용  
  mask_image = np.array(Image.open('./mask_images/image.png'))
  # 워드클라우드 생성
  wordcloud = WordCloud(
    width=800, height=400, background_color='white',
    mask=mask_image,
    font_path='./AppleGothic.ttf')
  gen = wordcloud.generate_from_frequencies(count)
  # 워드클라우드 이미지 저장
  wordcloud.to_file(filename)
  # return count