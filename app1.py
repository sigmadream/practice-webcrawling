from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

customService = Service(ChromeDriverManager().install())
customOption = Options()
browser = webdriver.Chrome(service = customService,
                           options = customOption)

URL = 'https://www.naver.com/'
browser.get(URL)
browser.implicitly_wait(10)

# 메일 값 획득
temp = browser.find_element(By.XPATH, '//*[@id="shortcutArea"]/ul/li[1]/a/span[2]').text
print(temp)

temp = browser.find_element(By.XPATH, '//*[@id="shortcutArea"]/ul/li[1]/a').text
print(temp)

# send_keys
browser.find_element(By.XPATH, '//*[@id="query"]').send_keys('aaaaaa')
time.sleep(5)