import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from string import Template

import re
import numpy as np
import pandas as pd
from tabulate import tabulate

op = Options()

# プロキシ関係の設定
op.add_argument("--disable-gpu")
op.add_argument("--disable-extensions")
op.add_argument("--proxy-server='direct://'")
op.add_argument("--proxy-bypass-list=*")
op.add_argument("--start-maximized")
op.add_argument("--headless")

BASE_URL = Template('https://suumo.jp/chintai/${target_name}/city/')

PREFECTURES = {"北海道": "hokkaido_", "青森県": "aomori", "岩手県": "iwate",
               "宮城県": "miyagi", "秋田県": "akita", "山形県": "yamagata",
               "福島県": "fukushima", "茨城県": "ibaraki", "栃木県": "tochigi",
               "群馬県": "gumma", "埼玉県": "saitama", "千葉県": "chiba",
               "東京都": "tokyo", "神奈川県": "kanagawa", "新潟県": "niigata",
               "富山県": "toyama", "石川県": "ishikawa", "福井県": "fukui",
               "山梨県": "yamanashi", "長野県": "nagano", "岐阜県": "gifu",
               "静岡県": "shizuoka", "愛知県": "aichi", "三重県": "mie",
               "滋賀県": "shiga", "京都府": "kyoto", "大阪府": "osaka",
               "兵庫県": "hyogo", "奈良県": "nara", "和歌山県": "wakayama",
               "鳥取県": "tottori", "島根県": "shimane", "岡山県": "okayama",
               "広島県": "hiroshima", "山口県": "yamaguchi", "徳島県": "tokushima",
               "香川県": "kagawa", "愛媛県": "ehime", "高知県": "kochi",
               "福岡県": "fukuoka", "佐賀県": "saga", "長崎県": "nagasaki",
               "熊本県": "kumamoto", "大分県": "oita", "宮崎県": "miyagi",
               "鹿児島県": "kagoshima", "沖縄": "okinawa"}


def get_checkbox_id():
    target_id_and_axis = []
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    links = soup.find("div", class_="l-searchtable")
    for url in links.find_all("li"):
        input_info = str(url.input)
        input_id = input_info.split('"')
        if input_id[1] != "disabled":
            target_id_and_axis.append(input_id[3])
    return target_id_and_axis


def search_property(target_ids):
    # 調べたい区のチェックボックスにチェック
    for city_id in target_ids:
        y = str(driver.find_element_by_id(city_id).location["y"] - 100)
        driver.execute_script("window.scrollTo(0," + y + ");")
        target_check_box = driver.find_element_by_xpath("//input[@id='" +
                                                       city_id +
                                                       "']")
        target_check_box.click()

    y = str(driver.find_element_by_id("ts0").location["y"] - 100)
    driver.execute_script("window.scrollTo(0," + y + ");")
    driver.find_element_by_xpath("//input[@id='ts0']").click()
    driver.find_element_by_xpath("//input[@id='ts1']").click()

    # 検索開始
    search_button = "ui-btn ui-btn--serachpanel " \
                    "searchpanel-box-btn js-shikugunSearchBtn2"

    target_button = driver.find_element_by_xpath("//a[@class='" +
                                                 search_button +
                                                 "']")
    target_button.click()
    cur_url = driver.current_url
    return cur_url


def get_survey_pages(target_pages):
    max_page = 0
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    links = soup.find('div', class_='pagination pagination_set-nav')
    if links:
        lis = links.find_all('a')
        # 検索結果のページをスクレイピング
        max_page = int(lis[-2].text)
    if target_pages > max_page:
        target_pages = max_page
    return target_pages


def get_address(url):
    # 住所から字のみを抽出
    address_class = "cassetteitem_detail-col1"
    address = url.find(class_=address_class).text
    address = address.replace('東京都', '')
    for c in ["区", "市", "郡", "町"]:
        idx = address.find(c)
        if idx != -1:
            break
    if idx != -1:
        address = address[:idx + 1]
    return address


def get_price(url):
    price_class = "cassetteitem_other-emphasis ui-text--bold"
    price = url.find(class_=price_class)
    price = float(price.text.strip("万円")) * 10000
    return int(price)


def get_nearest_station(url):
    bus = 0
    nearest_station_class = "cassetteitem_detail-text"
    nearest_station = url.find(class_=nearest_station_class).text.rsplit(" ")

    train_and_station_name = nearest_station[0].rsplit("/")
    if len(train_and_station_name) == 1:
        route = "-"
        station = "-"
        walking_time = 0
    else:
        route = train_and_station_name[0]
        station = train_and_station_name[1]
        walking_time = int(re.sub("\\D", "", nearest_station[1]))
    if "バス" in nearest_station[1]:
        bus = 1
    return [route, station, walking_time, bus]


def get_Age(url):
    age_class = "cassetteitem_detail-col3"
    age = url.find(class_=age_class).text.rsplit("\n")
    age = re.sub("\\D", "", age[1])
    if age == "":
        age = 1
    return int(age)


def get_property_info(target_pages, base_property_url):
    address_and_price = []
    for page in range(1, target_pages + 1):
        page_url = base_property_url + "&page=" + str(page)
        driver.get(page_url)
        # サーバ負荷対策
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        div_class = 'cassetteitem'
        for url in soup.find_all('div', class_=div_class):
            address = get_address(url)
            price = get_price(url)

            route_station_time = get_nearest_station(url)
            floor_plan = url.find(class_="cassetteitem_madori").text
            area = float(url.find(class_="cassetteitem_menseki").text[:-2])
            age = get_Age(url)

            address_and_price.append([address,
                                      price,
                                      route_station_time[0],
                                      route_station_time[1],
                                      route_station_time[2],
                                      route_station_time[3],
                                      floor_plan,
                                      area,
                                      age])
        print("finished scraping ", page, " pages!")
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


def get_table(aria_and_price):
    info_list = [[], [], [], [], [], [], [], [], []]

    for i in aria_and_price:
        info_list[0].append(i[0])
        info_list[1].append(i[1])
        info_list[2].append(i[2])
        info_list[3].append(i[3])
        info_list[4].append(i[4])
        info_list[5].append(i[5])
        info_list[6].append(i[6])
        info_list[7].append(i[7])
        info_list[8].append(i[8])

    df = pd.DataFrame(dict(エリア名=info_list[0],
                           賃料=info_list[1],
                           路線=info_list[2],
                           最寄駅=info_list[3],
                           徒歩時間=info_list[4],
                           バス有無=info_list[5],
                           間取り=info_list[6],
                           面積=info_list[7],
                           築年数=info_list[8]))
    print(tabulate(df, df.columns, tablefmt='presto', showindex=True))
    df.to_csv('suumo.csv')
    return df


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-m', '--municipality', default=None,
                        type=str, help="area name to listen on")
    parser.add_argument('-p', '--pages', default=99999,
                        type=int, help="pages to listen on")
    args = parser.parse_args()

    pages = int(args.pages)
    if pages is None:
        pages = 999999
    municipality = args.municipality

    if municipality in PREFECTURES.keys():
        municipality = PREFECTURES[municipality]
        city_url = BASE_URL.substitute(target_name=municipality)
        driver = webdriver.Chrome()
        #driver = webdriver.Chrome(chrome_options=op)
        driver.get(city_url)
        # サーバ負荷対策
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
        check_box_ids = get_checkbox_id()

        property_list_url = search_property(check_box_ids)
        survey_scope = get_survey_pages(pages)
        info_for_analysis = get_property_info(survey_scope,
                                              property_list_url)
        get_table(info_for_analysis)
        driver.quit()
