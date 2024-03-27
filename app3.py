import requests
from bs4 import BeautifulSoup
import pyautogui
import openpyxl

keyword = pyautogui.prompt("검색어를 입력하세요 >>>")

wb = openpyxl.Workbook("coupang_result.xlsx")
ws = wb.create_sheet(keyword)
ws.append(["순위", "브랜드명", "상품명", "가격", "상세페이지링크"])

rank = 1
done = False

for page in range(1, 5):
    if done:
        break
    print(f"{page}번째 페이지 입니다.")
    main_url = f"https://www.coupang.com/np/search?&q={keyword}&page={page}"
    header = {
        "Host": "www.coupang.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    response = requests.get(main_url, headers=header)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("a.search-product-link")

    for link in links:
        if len(link.select("span.ad-badge-text")) > 0:
            print("광고 상품입니다.")
        else:
            sub_url = "https://www.coupang.com/" + link.attrs["href"]
            print(sub_url)
            response = requests.get(sub_url, headers=header)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            try:
                brand_name = soup.select_one("a.prod-brand-name").text
            except:
                brand_name = ""

            brand_name = brand_name.strip()
            product_name = soup.select_one("h2.prod-buy-header__title").text
            
            try:
                product_price = soup.select_one("span.total-price > strong").text
            except:
                product_price = 0

            print(rank, brand_name, product_name, product_price)

            ws.append([rank, brand_name, product_name, product_price, sub_url])
            rank += 1
            if rank > 100:
                done = True
                break

wb.save("coupang_result.xlsx")
