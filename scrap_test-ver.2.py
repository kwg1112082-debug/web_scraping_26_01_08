import requests
from bs4 import BeautifulSoup

# ==========================================================
# [설정] 스크래핑할 대상 URL 및 옵션
# ==========================================================
TARGET_URL = "https://news.naver.com/section/104"
MAX_NEWS_LIMIT = 50  # 최대 수집할 뉴스 개수

def main():
    # 1단계: 웹페이지 요청 (Requests) - [ver.3 기능: 안전성 강화]
    print(f"\n[접속 시도] {TARGET_URL} 데이터를 가져오는 중입니다...")
    
    try:
        # timeout=5: 5초 안에 응답이 없으면 에러 발생 (무한 대기 방지)
        response = requests.get(TARGET_URL, timeout=5)
        
        # HTTP 상태 코드 검사
        if response.status_code != 200:
            print(f"❌ 접속 실패! 상태 코드: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 접속 중 오류 발생: {e}")
        return

    print("✅ 접속 성공! HTML 분석을 시작합니다.\n")


    # 2단계: HTML 파싱 (BeautifulSoup)
    soup = BeautifulSoup(response.text, "lxml")


    # 3단계: 뉴스 데이터 추출
    
    # [ver.3 기능: 섹션 제목 추출]
    section_title_tag = soup.select_one(".sa_head_link")
    if section_title_tag:
        section_name = section_title_tag.get_text(strip=True)
        print(f"📌 현재 섹션: {section_name}")
    else:
        print("📌 섹션 정보를 찾을 수 없습니다.")

    # 네이버 뉴스 목록의 각 기사는 <div class="sa_text"> 안에 담겨 있습니다.
    articles = soup.select('.sa_text')
    
    # 수집 개수 제한 (slicing 사용)
    articles = articles[:MAX_NEWS_LIMIT]
    
    print(f"[{MAX_NEWS_LIMIT}개 제한] 탐색된 기사 요소 개수: {len(articles)}개")
    print("=" * 60)

    # 수집된 데이터를 저장할 리스트
    news_data_list = []

    for article in articles:
        # (1) 제목 및 링크 추출 using CSS Selector
        # <a class="sa_text_title" href="..."> ... </a>
        title_tag = article.select_one('.sa_text_title')
        
        # 제목 태그가 없는 경우(광고 등)는 건너뜀
        if not title_tag:
            continue
            
        # 제목 텍스트 (strong 태그 안)
        strong_tag = title_tag.select_one('.sa_text_strong')
        title_text = strong_tag.get_text(strip=True) if strong_tag else title_tag.get_text(strip=True)
        
        # 기사 링크 (href 속성)
        article_link = title_tag['href']

        # (2) 기사 요약 내용 추출
        # 목록에서 보이는 짤막한 내용 (sa_text_lede)
        lede_tag = article.select_one('.sa_text_lede')
        content_text = lede_tag.get_text(strip=True) if lede_tag else "내용 미리보기 없음"

        # (3) 언론사 정보 추출
        press_tag = article.select_one('.sa_text_press')
        press_name = press_tag.get_text(strip=True) if press_tag else "언론사 정보 없음"

        # 딕셔너리로 묶어서 리스트에 추가
        news_info = {
            "press": press_name,
            "title": title_text,
            "content": content_text,
            "link": article_link
        }
        news_data_list.append(news_info)


    # 4단계: 결과 출력
    for idx, news in enumerate(news_data_list, start=1):
        print(f"📰 No.{idx}")
        print(f"   신문사: {news['press']}")
        print(f"   제목: {news['title']}")
        print(f"   내용: {news['content']}...")
        print(f"   링크: {news['link']}")
        print("-" * 60)

    print(f"\n✅ 최종 수집 완료: 총 {len(news_data_list)}개의 뉴스를 정리했습니다.")

# 스크립트 실행
if __name__ == "__main__":
    main()
