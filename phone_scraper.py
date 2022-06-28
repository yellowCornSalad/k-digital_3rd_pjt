from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

TLGM_BOT_TOKEN = "5593781783:AAE7yYSezsPGqZENciEbcpY6r2AKsfShqKs"
driver = webdriver.Chrome(options=options)

driver.get("https://www.joongabi.com/trend")
# driver.implicitly_wait(5)
sleep(2)
id = driver.find_element_by_class_name("input-id")
id.send_keys("jgy9701")
password = driver.find_element_by_class_name("input-password")
password.send_keys("wkddbs1017$$")
driver.find_element_by_class_name("login-button").click()

# driver.find_element_by_class_name("v-btn").click()
sleep(4)
driver.find_element(By.XPATH, '//*[@id="container"]/section/div[1]/div[2]/div[3]/div[3]/div/button[1]').click()
sleep(2)
driver.find_element(By.XPATH, '//*[@id="container"]/section/div[1]/div[2]/div[3]/div[3]/div/button[1]').click()
sleep(2)
driver.find_element(By.XPATH, '//*[@id="container"]/section/div[1]/div[2]/div[3]/div[3]/div/button').click()

sleep(2)
element = driver.find_element_by_id("input-49")
element.click()
sleep(1)
element.send_keys(Keys.DELETE)
# element.click()
element.send_keys("아이폰 SE 64G")
element.send_keys(Keys.ENTER)
# element.clear()


driver.find_element(By.XPATH, '//*[@id="container"]/section/div[1]/div[2]/div[3]/div[1]/div[1]/div/button').click()

sleep(3)

# driver.find_element(By.XPATH, '//*[@id="container"]/section/div[1]/div[3]/div[1]/div[1]/div[2]/input').click()
driver.find_element(By.XPATH, '//*[@id="container"]/section/div[1]/div[3]/div[1]/div[2]/div[1]/input').click()
# driver.find_element(By.XPATH, '//*[@id="container"]/section/div[1]/div[3]/div[1]/div[2]/div[3]/input').click()
sleep(1)
items = driver.find_elements(By.XPATH, '//*[@id="container"]/section/div[2]/div[2]')
for item in items:
    temp = item.find_elements_by_tag_name('td')
    for i in temp:
        print(i.text)

sleep(5)
# items = driver.find_elements(By.CSS_SELECTOR, ".statsdiv  .results .listdiv .videodiv")


# driver.close()