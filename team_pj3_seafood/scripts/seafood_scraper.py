from time import sleep
from tkinter.tix import Select
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import csv
def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get("https://www.susansijang.co.kr/nsis/miw/ko/info/miw3130")
select = Select(driver.find_element_by_id('kdfshCode'))
<<<<<<< HEAD
select.select_by_visible_text('우럭')
=======
select.select_by_visible_text('넙치(광어)')
>>>>>>> ac94b4b8703c8307f44c15c8da454553ce53232d
btn = driver.find_element_by_id('searchBtn')
btn.click()
dates = date_range("2022-01-02", "2022-07-06")
result = []
result.append(["날짜", "어종", "산지","규격", "포장","수량","중량","평균가"])
for date in dates:
    try:
        driver.find_element(By.ID, 'searchStartDe').send_keys(Keys.CONTROL, 'a')
        driver.find_element(By.ID, 'searchStartDe').send_keys(date)
        driver.find_element(By.ID, 'searchEndDe').send_keys(Keys.CONTROL, 'a')
        driver.find_element(By.ID, 'searchEndDe').send_keys(date)
        driver.find_element(By.ID, 'searchBtn').click()
        sleep(random.uniform(1,3))
    # while(driver.find_element_by_xpath('//*[@id="contents"]/form[2]/div[2]/a[4]').text!="다음 페이지로 가기"):
    #     for i in range(5,14):
    #        ## 데이터 불러오기
    #         items = driver.find_elements(By.CSS_SELECTOR, '.list-table tbody')
    #         btn = driver.find_elements(By.CSS_SELECTOR, '.pagination a')
    #         for items in items:
    #             items = items.text
    #             items = items.split('\n')
    #             for n in range(len(items)):
    #                 # print(n)
    #                 item = items[n].split(' ')
    #                 species = item[0]
    #                 origin = item[1]
    #                 unit = item[3]
    #                 avg_price = item[8]
    #                 print(f"날짜: {date}, 어종: {species}, 산지: {origin}, 포장: {unit}, 평균가: {avg_price}")
    #         temp = '//*[@id="contents"]/form[2]/div[2]/a['+str(i)+']'
    #         driver.find_element_by_xpath(temp).click()
        pages = driver.find_element_by_class_name('pagination')
        page = pages.find_elements_by_tag_name('a')
        for i in page:
            # print(i)
            temp = '//*[@id="contents"]/form[2]/div[2]/a['+str(i.text)+']'
            driver.find_element_by_xpath(temp).click()
            # 데이터 불러오기
            items = driver.find_elements(By.CSS_SELECTOR, '.list-table tbody')
            btn = driver.find_elements(By.CSS_SELECTOR, '.pagination a')
            for items in items:
                items = items.text
                items = items.split('\n')
                for n in range(len(items)):
                    # print(n)
                    item = items[n].split(' ')
                    species = item[0]
                    origin = item[1]
                    standard = item[2]
                    unit = item[3]
                    amount = item[4]
                    weight = item[5]
                    avg_price = item[8]
                    # print(f"날짜: {date}, 어종: {species}, 산지: {origin}, 포장: {unit}, 평균가: {avg_price}")
                    temp=[]
                    temp.append(date)
                    temp.append(species)
                    temp.append(origin)
                    temp.append(standard)
                    temp.append(unit)
                    temp.append(amount)
                    temp.append(weight)
                    temp.append(avg_price)
                    result.append(temp)
    except Exception as e:
        continue
# t = datetime.today().strftime("%Y-%m-%d-%H")
base_path = './seafood_data_junho/'
file_name = base_path + "넙치2022" + ".csv"
with open(file_name, 'a', encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(result)
# # data_table = driver.find_element_by_class_name('list-table')
# # print(data_table.text[0])
# data_table = driver.find_element_by_css_selector('.list-table table tbody')
# print(data_table.text)
print("finish")