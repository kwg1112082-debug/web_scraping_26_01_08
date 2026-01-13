import requests

try :
    response = request.get("https://naver.com", timeout=5)
    print