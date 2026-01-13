from bs4 import BeautifulSoup
import requests # 웹사이트에 요청을 보내고 응답을 받는 라이브러리

# 1. requests : 원하는 웹사이트에 요청
url = "https://news.naver.com/section/105"

try:
  resp = requests.get(url, timeout=5)
  print(f"1. Requests: SUCCESS (Status Code: {resp.status_code})")
except Exception as e:
  print(f"1. Requests: FAILED ({e})")

if resp.status_code == 200:
  soup = BeautifulSoup(resp.text, 'lxml')
  # print(soup)
  # 뉴스 헤드라인 타이틀 가져오기
  # find() : 검색 된 엘리먼트중에 제일 먼저 검색된 데이터 하나만 수집
  print(soup.select_one(".sa_head_link").get_text(strip=True))

  # 각 뉴스의 헤드라인 기사 제목
  # find_all() : 검색 된 엘리먼트들을 리스트화 한다.
  print(soup.select(".sa_text_strong"))
  titles_elements = soup.select(".sa_text_strong")

  # 텍스트만 추출
  titles = [title.get_text(strip=True) for title in titles_elements]

  # print(titles)
  for idx, title in enumerate(titles):
    no = idx + 1
    print(f"{no} : {title}")