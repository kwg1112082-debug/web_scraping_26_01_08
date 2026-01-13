# 📄 네이버 뉴스 추출 소스코드 (ver.FINAL)

본 문서는 `scrap_test-ver.FINAL.py`의 전체 소스코드를 포함하고 있습니다.

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime  # [조건 반영] 현재 시간을 구하기 위한 라이브러리

# ==========================================================
# [설정] 스크래핑할 대상 URL 및 수집 제한
# ==========================================================
TARGET_URL = "https://news.naver.com/section/104"
MAX_NEWS_LIMIT = 100  # 필터링을 위해 넉넉하게 수집합니다.

def main():
    # 1. 1단계: 웹페이지 접속 및 HTML 가져오기 (requests 사용)
    print(f"\n[접속 시도] {TARGET_URL} 데이터를 가져오는 중입니다...")
    try:
        response = requests.get(TARGET_URL, timeout=5)
        if response.status_code != 200:
            print(f"❌ 접속 실패: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return

    # 2. 2단계: BeautifulSoup을 이용한 데이터 추출
    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.select('.sa_text')
    
    news_data_list = []

    for article in articles:
        # 제목 추출
        title_tag = article.select_one('.sa_text_title')
        if not title_tag: continue
        
        strong_tag = title_tag.select_one('.sa_text_strong')
        title_text = strong_tag.get_text(strip=True) if strong_tag else title_tag.get_text(strip=True)
        
        # 링크, 내용, 언론사 추출
        article_link = title_tag['href']
        lede_tag = article.select_one('.sa_text_lede')
        content_text = lede_tag.get_text(strip=True) if lede_tag else "내용 없음"
        press_tag = article.select_one('.sa_text_press')
        press_name = press_tag.get_text(strip=True) if press_tag else "알 수 없음"

        # 수집된 데이터를 딕셔너리에 저장
        news_info = {
            "신문사": press_name,
            "제목": title_text,
            "내용": content_text,
            "링크": article_link
        }
        news_data_list.append(news_info)


    # 3. [미션 2 - 조건 2] 'ai' 단어가 포함된 뉴스만 필터링
    # 제목에 'ai' 또는 'AI'가 있는 데이터만 골라냅니다.
    filtered_news = [news for news in news_data_list if 'ai' in news['제목'].lower()]
    print(f"\n✅ 필터링 완료: 총 {len(news_data_list)}개 중 'AI' 관련 뉴스 {len(filtered_news)}개를 찾았습니다.")


    # 4. [미션 2 - 조건 3] 현재 날짜를 구하여 파일명 생성
    # 예) naver_news_20260113.xlsx
    today_str = datetime.now().strftime("%Y%m%d")
    excel_filename = f"naver_news_{today_str}.xlsx"


    # 5. [미션 1] 엑셀 저장 (Pandas 라이브러리 사용)
    if len(filtered_news) > 0:
        # 데이터프레임 생성
        df = pd.DataFrame(filtered_news)
        
        # [조건 적용] index=False: 인덱스 번호 제외, engine='openpyxl': 스타일링 사용
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='네이버 AI 뉴스')
            
            # 6. [미션 2 - 조건 1] 엑셀 스타일 업그레이드 (가독성 강화 버전)
            from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
            
            worksheet = writer.sheets['네이버 AI 뉴스']
            
            # --- 스타일 정의 ---
            # 배경색: 진한 파란색(제목), 연한 회색(줄무늬 효과용 또는 기본)
            header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid') 
            
            # 서체: 제목 영문/한글 가독성 고려
            header_font = Font(name='맑은 고딕', size=14, bold=True, color='FFFFFF') # 흰색 굵은 글씨
            data_font = Font(name='맑은 고딕', size=12)
            title_font = Font(name='맑은 고딕', size=12, bold=True) # 제목은 더 강조
            
            # 정렬 및 테두리
            center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            left_alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                                 top=Side(style='thin'), bottom=Side(style='thin'))

            # (1) 제목 행(Header) 스타일 적용
            worksheet.row_dimensions[1].height = 30 # 제목 행 높이 조절
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_alignment
                cell.border = thin_border

            # (2) 데이터 행 스타일 적용
            for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, max_row=worksheet.max_row), start=2):
                worksheet.row_dimensions[row_idx].height = 25 # 데이터 행 높이 조절
                for cell in row:
                    cell.border = thin_border
                    cell.alignment = left_alignment
                    
                    # '제목' 열(B열, index 1)은 글자를 굵게 설정
                    if cell.column == 2:
                        cell.font = title_font
                    else:
                        cell.font = data_font
            
            # (3) 열 너비 최적화 (가독성 확보)
            worksheet.column_dimensions['A'].width = 15 # 신문사
            worksheet.column_dimensions['B'].width = 60 # 제목 (가장 중요하므로 넓게)
            worksheet.column_dimensions['C'].width = 50 # 내용
            worksheet.column_dimensions['D'].width = 70 # 링크

        print(f"🎉 과제 수행 완료! '{excel_filename}' 파일이 생성되었습니다.")
    else:
        print("⚠️ 'AI' 키워드가 포함된 뉴스가 없어 파일을 생성하지 않았습니다.")

if __name__ == "__main__":
    main()
```
