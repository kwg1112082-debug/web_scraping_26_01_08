# 🐍 예제 코드 상세 분석 (README2)

이 문서는 `example_scraping.py` 파일에 작성된 코드가 정확히 어떤 일을 하는지, 초보자의 눈높이에서 아주 자세하게 설명하는 가이드입니다.

---

## 🏃‍♂️ 바로 실행해보기

코드를 분석하기 전에, 먼저 실행부터 해보세요! 터미널에 아래 명령어를 입력하면 됩니다.

```powershell
python example_scraping.py
```
*(실행 결과로 "성공적으로 접속했습니다!"와 링크 목록이 보이면 성공입니다)*

---

## 🧐 코드 한 줄 한 줄 뜯어보기

우리가 작성한 코드는 크게 **3단계**로 이루어져 있습니다.

### 1단계: 배달원 부르기 (Requests)
웹사이트에 접속해서 데이터를 받아오는 단계입니다.

```python
import requests 

url = "https://www.google.com"
response = requests.get(url) 
```
- **`import requests`**: 파이썬에게 "나 인터넷 배달원(Requests) 좀 쓸게"라고 말합니다.
- **`requests.get(url)`**: 배달원에게 "저 주소(`url`)로 가서 내용 좀 받아와!"라고 시킵니다.
- **`response`**: 배달원이 받아온 결과물(포장된 음식)을 이 변수에 저장합니다.

### 2단계: 요리사에게 재료 넘기기 (BeautifulSoup)
받아온 데이터(HTML)를 다듬어서 우리가 보기 좋게 만드는 단계입니다.

```python
from bs4 import BeautifulSoup

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "lxml")
```
- **`if response.status_code == 200`**: 배달이 성공했는지 확인합니다. (200번은 '성공'이라는 뜻입니다)
- **`BeautifulSoup(..., "lxml")`**:
    - 배달온 날것의 재료(`response.text`)를
    - 잘 드는 칼(`lxml`)을 든 요리사(`BeautifulSoup`)에게 넘겨줍니다.
    - 이제 **`soup`**이라는 완성된 요리에서 우리는 원하는 것만 쏙쏙 골라낼 수 있습니다.

### 3단계: 맛있는 것만 골라내기 (데이터 추출)
요리된 결과물에서 우리가 진짜 필요한 정보(링크)만 찾아냅니다.

```python
    # 모든 <a> 태그(링크)를 찾아서 리스트로 만들기
    links = soup.find_all("a")
    
    # 찾은 것 중 앞에서 5개만 뽑아서 보여주기
    for set_idx, link in enumerate(links[:5], 1):
        text = link.get_text().strip()
        print(f"{set_idx}. {text}")
```
- **`soup.find_all("a")`**: "요리사님, 여기서 `<a>`(링크) 태그는 전부 다 찾아주세요!"라고 명령합니다.
- **`link.get_text()`**: 태그 안에 있는 글자(텍스트)만 깔끔하게 발라냅니다.

---

## 💡 팁: 다른 사이트도 해보고 싶다면?

`example_scraping.py` 파일에서 `url` 변수의 주소만 바꿔보세요.

```python
# 네이버로 바꿔보기
url = "https://www.naver.com"
```
주소를 바꾸고 다시 실행하면, 그 사이트의 링크 정보를 가져옵니다. 
(단, 보안이 강력한 사이트는 접속이 안 될 수도 있습니다)
