from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# driver.find_element(By. , '')
driver = webdriver.Chrome("./chromedriver")
driver.get("https://www.susansijang.co.kr/nsis/miw/ko/info/miw3130")
# driver.implicitly_wait(5)
sleep(3)



## 어종 클릭
# driver.find_element(By.ID, 'kdfshCode').click()
driver.find_element(By.XPATH, '//*[@id="kdfshCode"]/option[2]').click()

## 날짜 입력
def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates

dates = date_range("2017-01-02", "2017-01-03")

for date in dates:
  driver.find_element(By.ID, 'searchStartDe').send_keys(Keys.CONTROL, 'a')
  driver.find_element(By.ID, 'searchStartDe').send_keys(date)
  driver.find_element(By.ID, 'searchEndDe').send_keys(Keys.CONTROL, 'a')
  driver.find_element(By.ID, 'searchEndDe').send_keys(date)

  driver.find_element(By.ID, 'searchBtn').click()
  sleep(random.uniform(1,3))

  ## 데이터 불러오기
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
      unit = item[3]
      avg_price = item[8]
      print(f"날짜: {date}, 어종: {species}, 산지: {origin}, 포장: {unit}, 평균가: {avg_price}")      

driver.close()