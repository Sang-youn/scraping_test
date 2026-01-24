import matplotlib.pyplot as plt
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter


def create_wordcloud(text):
  okt = Okt()
  nouns = okt.nouns(text)
  words = [word for word in nouns if len(word) > 1]
  count = Counter(words)
  
  wordcloud = WordCloud(
    width=800, height=400, background_color='white',
    font_path='./AppleGothic.ttf')
  gen = wordcloud.generate_from_frequencies(count)
  plt.figure(figsize=(10, 8))
  plt.imshow(gen)
  plt.axis('off')
  plt.show()
  # return count