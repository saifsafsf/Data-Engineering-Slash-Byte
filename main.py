from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.zameen.com')

driver.implicitly_wait(20)
element = driver.find_element(By.XPATH, "//img[@class='close_cross_big']")
print(element.click)

# element = WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "ef5cccac"))
# )
# element.click()

# inp = 3
# html_text = requests.get(f'https://www.zameen.com/Homes/Islamabad-{inp}-1.html').text
# soup = BeautifulSoup(html_text, 'lxml')

# print(soup.prettify())