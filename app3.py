import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

df = None  # 전역 변수로 선언
product_links = []  # 상품 링크를 저장할 리스트


def crawl_naver_shopping(query):
    global products_info
    if not query:
        return

    customService = Service(ChromeDriverManager().install())
    customOption = Options()
    browser = webdriver.Chrome(service=customService, options=customOption)

    browser.get(
        f"https://search.shopping.naver.com/search/all?query={query}&cat_id=&frm=NVSHATC"
    )

    browser.execute_script("window.scrollBy(0, 1000);")
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

    products_info = []

    for product_element, price_element, review_element in zip(
        product_names, product_prices, product_reviews
    ):
        title = product_element.get_attribute("title")
        price = price_element.text.replace(",", "")
        review = review_element.text.replace(",", "").replace("(", "").replace(")", "")
        link = product_element.get_attribute("href")  # 상품 링크 가져오기
        products_info.append(
            {"제목": title, "가격": price, "리뷰 수": int(review), ".": link}
        )
    browser.quit()
    return products_info


def on_double_click(event):
    selected_item = result_listbox.get(result_listbox.curselection())
    names = ""
    link = ""

    for i in selected_item[4:]:
        if i == "/":
            names = names[:-1]
            break
        else:
            names = names + i

    for x in products_info:
        if x["제목"] == names:
            link = x["."]  # 선택된 상품의 링크 가져오기

    new_window = tk.Toplevel(root)
    new_window.geometry("500x60")
    new_window.resizable(False, False)
    new_frame = tk.Frame(new_window)
    new_frame.pack()
    zzim = tk.Button(
        new_frame,
        text="찜하기",
        command=lambda: open_link_in_browser(link, 1, code.get()),
    )
    zzim.pack(side=tk.LEFT, padx=5)

    baguni = tk.Button(
        new_frame,
        text="장바구니 추가",
        command=lambda: open_link_in_browser(link, 2, code.get()),
    )
    baguni.pack(side=tk.LEFT, padx=5)

    code = tk.Entry(new_frame)
    code.pack(side=tk.BOTTOM, pady=5)

    root.mainloop


def open_link_in_browser(link, n, code):
    customService = Service(ChromeDriverManager().install())
    customOption = Options()
    
    browser = webdriver.Chrome(service=customService, options=customOption)
    browser.get(link)
    browser.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.3)

    if n == 1:
        browser.find_element(
            By.CSS_SELECTOR,
            "#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div.XqRGHcrncz > div:nth-child(2) > div._3Dy-2NaoiG.N\=a\:pcs\.fav > a",
        ).click()
    else:
        browser.find_element(
            By.CSS_SELECTOR,
            "#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div.XqRGHcrncz > div:nth-child(2) > div.C_muF3UG0-.sys_chk_cart.N\=a\:pcs\.cart > a",
        ).click()

    time.sleep(0.3)
    da = Alert(browser)
    da.accept()

    time.sleep(2)
    browser.switch_to.window(browser.window_handles[-1])
    browser.find_element(By.CSS_SELECTOR, "#ones").click()

    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR, "#disposable").send_keys(code)

    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR, "#otnlog\\.login").click()
    time.sleep(1)
    browser.quit()


def start_crawling():
    global df
    query = entry.get()
    products_info = crawl_naver_shopping(query)
    df = pd.DataFrame(products_info)
    for index, row in df.iterrows():
        product_info = (
            f'제목: {row["제목"]} / 가격: {row["가격"]}원 / 리뷰 수: {row["리뷰 수"]}개'
        )
        result_listbox.insert(tk.END, product_info)


def sort_df(order, column):
    global df
    if df is not None:
        if column == "가격":
            if order == "오름차순":
                ascending_order = True
            else:
                ascending_order = False
        else:
            ascending_order = False

        sorted_df = df.sort_values(by=column, ascending=ascending_order)
        result_listbox.delete(0, tk.END)
        for index, row in sorted_df.iterrows():
            product_info = f'제목: {row["제목"]} / 가격: {row["가격"]}원 / 리뷰 수: {row["리뷰 수"]}개'
            result_listbox.insert(tk.END, product_info)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("네이버 쇼핑 크롤러")
    root.geometry("900x600")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack()

    label = tk.Label(frame, text="검색어 입력:")
    label.pack(side=tk.LEFT)

    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT)

    button = tk.Button(frame, text="검색", command=start_crawling)
    button.pack(side=tk.LEFT, padx=10)

    ascend_price_button = tk.Button(
        frame, text="낮은 가격순", command=lambda: sort_df("오름차순", "가격")
    )
    ascend_price_button.pack(side=tk.LEFT, padx=5)

    descend_price_button = tk.Button(
        frame, text="높은 가격순", command=lambda: sort_df("내림차순", "가격")
    )
    descend_price_button.pack(side=tk.LEFT, padx=5)

    ascend_review_button = tk.Button(
        frame, text="리뷰 많은 순", command=lambda: sort_df("내림차순", "리뷰 수")
    )
    
    ascend_review_button.pack(side=tk.LEFT, padx=5)

    result_listbox = tk.Listbox(root, width=120, height=15)
    result_listbox.pack(padx=10, pady=10)

    entry.bind("<Return>", lambda event=None: start_crawling())
    result_listbox.bind("<Double-Button-1>", on_double_click)  # 더블클릭 이벤트 바인딩

    root.mainloop()
