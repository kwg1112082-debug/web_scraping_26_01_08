# Web Scraping Project

이 프로젝트는 파이썬을 이용한 웹 스크래핑 프로젝트입니다. 현재 `web_scrap` 가상환경 세팅이 완료되었습니다.

## 가상환경 (Virtual Environment) 세팅

프로젝트 루트에 `web_scrap` 폴더 이름으로 가상환경이 생성되어 있습니다.

### 1. 가상환경 활성화 (Windows)

터미널에서 아래 명령어를 입력하여 가상환경을 활성화할 수 있습니다.

```powershell
.\web_scrap\Scripts\activate
```

활성화되면 터미널 프롬프트 왼쪽에 `(web_scrap)` 표시가 나타납니다.

### 2. 패키지 설치

가상환경이 활성화된 상태에서 필요한 라이브러리를 설치합니다.

```powershell
pip install requests beautifulsoup4
```

### 3. 가상환경 비활성화

작업을 마치고 가상환경을 종료하려면 다음 명령어를 입력합니다.

```powershell
deactivate
```

---

## 프로젝트 구조

- `web_scrap/`: 파이썬 가상환경 디렉토리
- `README.md`: 프로젝트 안내 및 세팅 방법 (현재 파일)
