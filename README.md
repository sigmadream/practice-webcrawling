# 웹 크롤링

> [Naver 쇼핑](https://shopping.naver.com)을 크롤링해서 DB에 저장 후에 해당 데이터를 기반으로 간다한 서비를 만들어봅시다.

## 준비사항

- python >= 3.8
    - pip install selenium
    - pip install webdriver-manager
- VSCode
    - Python
- Selenium
- BeatufulSoup4
- Pandas
- SQLite / PostgreSQL
- Flask / FastAPI
- + crontab

## 가상환경 구성

웹 서버를 구동할 것을 가정하고 있어서, `가상환경`을 구축하는걸 추천합니다. `ctrl+command+p` > `Python: Create Enviroment` > `Venv`에서 파이썬 버전 선택하시면 됩니다.

## XPath 확인 및 값 가져오기

```python
# 메일 값 획득
temp = browser.find_element(By.XPATH, '//*[@id="shortcutArea"]/ul/li[1]/a/span[2]').text
print(temp)

temp = browser.find_element(By.XPATH, '//*[@id="shortcutArea"]/ul/li[1]/a').text
print(temp)

# send_keys
browser.find_element(By.XPATH, '//*[@id="query"]').send_keys('aaaaaa')
time.sleep(5)
```