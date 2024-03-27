from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

customService = Service(ChromeDriverManager().install())
customOption = Options()
browser = webdriver.Chrome(service=customService, options=customOption)

# 제목, 가격, 리뷰 수, link => 엑셀이나 CSV 파일 같은 것으로 저장


def crawl_naver_shopping(query="샤오미"):
    URL = f"https://search.shopping.naver.com/search/all?query={query}"
    browser.get(URL)
    browser.execute_script("window.scrollBy(0,1000);")
    time.sleep(0.3)
    product_names = browser.find_elements(
        By.CSS_SELECTOR,
        "div > div > div.product_info_area__xxCTi > div.product_title__Mmw2K > a",
    )
    product_prices = browser.find_elements(
        By.CSS_SELECTOR,
        "div > div > div.product_info_area__xxCTi > div.product_price_area__eTg7I > strong > span.price > span > em",
    )
    product_reviews = browser.find_elements(
        By.CSS_SELECTOR,
        "div > div > div.product_info_area__xxCTi > div.product_etc_box__ElfVA > a:nth-child(1) > em",
    )
    product_info = []
    for product_name, product_price, product_review in zip(
        product_names, product_prices, product_reviews
    ):
        title = product_name.get_attribute("title")
        price = product_price.text.replace(",", "")
        review = product_review.text.replace(",", "").replace("(", "").replace(")", "")
        link = product_name.get_attribute("href")
        product_info.append(
            {"제품명": title, "가격": price, "리뷰수": review, "링크": link}
        )

    return product_info


if __name__ == "__main__":
    result = crawl_naver_shopping("삼성전자")
    df = pd.DataFrame(result)
    df.to_excel("삼성전자.xlsx")
