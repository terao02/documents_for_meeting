import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tabulate import tabulate
import numpy as np
import pandas as pd

op = Options()

# プロキシ関係の設定
op.add_argument("--disable-gpu")
op.add_argument("--disable-extensions")
op.add_argument("--proxy-server='direct://'")
op.add_argument("--proxy-bypass-list=*")
op.add_argument("--start-maximized")
op.add_argument("--headless")

BASE_URL = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta' \
           '=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=131' \
           '06&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=1310' \
           '9&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116' \
           '&sc=13117&sc=13119&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&' \
           'mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'


def get_brand_and_price(target_pages):
    target_pages = int(target_pages)
    address_and_price = []
    max_page = 0

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(chrome_options=op)

    driver.get(BASE_URL)
    # サーバ負荷対策
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    links = soup.find('div', class_='pagination pagination_set-nav')
    if links:
        lis = links.find_all('a')
        # 検索結果のページをスクレイピング
        max_page = int(lis[-2].text)
    if target_pages > max_page:
        target_pages = max_page

    for i in range(1, target_pages + 1):
        page_url = BASE_URL + '&page=' + str(i)
        driver.get(page_url)
        # サーバ負荷対策
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        div_class = 'cassetteitem'
        for url in soup.find_all('div', class_=div_class):
            address = url.find(class_="cassetteitem_detail-col1").text
            idx = address.find('区')
            district = address[:idx + len('区')]
            district = district.strip("東京都")
            price = url.find(class_="cassetteitem_other-emphasis ui-text--bold")
            price = float(price.text.strip("万円"))
            address_and_price.append([district, price])
    driver.quit()
    return address_and_price


def get_average_par_brand(target_brand_name, brand_and_price):
    n = 0
    x_sum = 0
    for index in range(len(brand_and_price)):
        if target_brand_name == brand_and_price[index][0]:
            x_sum += brand_and_price[index][1]
            n += 1
    x_bar = x_sum / n
    return n, x_bar


def get_U_dispersion(target_brand_name, brand_and_price, x_bar, n):
    U = 0
    for index in range(len(brand_and_price)):
        if target_brand_name == brand_and_price[index][0]:
            U += (brand_and_price[index][1] - x_bar) ** 2

    if n > 1:
        U = np.sqrt(U / (n - 1))
    else:
        U = 0
    return U


def get_public_average(brand_and_price):
    brand_name_elements = []
    quantity_elements = []
    sample_mean_elements = []
    unbiased_dispersion_elements = []
    lower_limit_average_elements = []
    upper_limit_average_elements = []

    unique_names = set(list(map(lambda x: x[0], brand_and_price)))

    for name in unique_names:
        n, x_bar = get_average_par_brand(name, brand_and_price)
        U = get_U_dispersion(name, brand_and_price, x_bar, n)

        lower_average = x_bar - 2.776 * (U / np.sqrt(n))
        upper_average = x_bar + 2.776 * (U / np.sqrt(n))

        brand_name_elements.append(name)
        quantity_elements.append(n)
        sample_mean_elements.append(x_bar)
        unbiased_dispersion_elements.append(U)
        lower_limit_average_elements.append(lower_average)
        upper_limit_average_elements.append(upper_average)

    df = pd.DataFrame(dict(区名=brand_name_elements,
                           検出数=quantity_elements,
                           標本平均=sample_mean_elements,
                           普遍分散=unbiased_dispersion_elements,
                           信頼区間最小値=lower_limit_average_elements,
                           信頼区間最大値=upper_limit_average_elements))
    print(tabulate(df, df.columns, tablefmt='presto', showindex=True))
    return 0


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--Pages')
    args = parser.parse_args()
    Pages = args.Pages
    if Pages is None:
        print("Not found error")
    else:
        value_brand = get_brand_and_price(Pages)
        get_public_average(value_brand)
