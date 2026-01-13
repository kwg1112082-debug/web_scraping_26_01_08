
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
  
  # 페이지 헤드라인 (섹션 제목)
  section_title = soup.select_one(".sa_head_link")
  if section_title:
    print(f"섹션: {section_title.get_text(strip=True)}\n")
  
  # 모든 뉴스 항목 가져오기 (sa_text 클래스)
  news_items = soup.select(".sa_text")
  
  print(f"총 {len(news_items)}개의 뉴스를 찾았습니다.\n")
  print("=" * 80)
  
  # 각 뉴스 항목에서 정보 추출
  news_list = []
  
  for item in news_items:
    # 1. 링크 추출 (sa_text_title 클래스의 href 속성)
    link_element = item.select_one(".sa_text_title")
    link = link_element.get('href') if link_element else None
    
    # 2. 제목 추출 (sa_text_strong 클래스)
    title_element = item.select_one(".sa_text_strong")
    title = title_element.get_text(strip=True) if title_element else None
    
    # 3. 내용 추출 (sa_text_lede 클래스)
    content_element = item.select_one(".sa_text_lede")
    content = content_element.get_text(strip=True) if content_element else None
    
    # 4. 신문사 추출 (sa_text_info의 후손인 sa_text_press 클래스)
    news_corp_element = item.select_one(".sa_text_info .sa_text_press")
    news_corp = news_corp_element.get_text(strip=True) if news_corp_element else None
    
    # 딕셔너리로 정리
    news_info = {
      "title": title,
      "content": content,
      "link": link,
      "news_corp": news_corp
    }
    
    news_list.append(news_info)
    
    # 각 뉴스 정보 출력
    print(f"\n📰 뉴스 {len(news_list)}")
    print(f"제목: {news_info['title']}")
    print(f"신문사: {news_info['news_corp']}")
    print(f"내용: {news_info['content'][:50]}..." if news_info['content'] else "내용: None")
    print(f"링크: {news_info['link']}")
    print("-" * 80)
  
  print(f"\n✅ 총 {len(news_list)}개의 뉴스 정보 수집 완료!")
  
  # 전체 리스트 출력 (선택사항)
  # print("\n전체 뉴스 리스트:")
  # for idx, news in enumerate(news_list, 1):
  #   print(f"{idx}. {news}")