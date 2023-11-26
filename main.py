from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time


def finding_page(location):
    driver = webdriver.Chrome()
    driver.get('https://www.zameen.com/')
    time.sleep(10)

    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "google_ads_iframe_/31946216/Splash_660x500_0"))
        )
        
        button.click()

    except:
        print('Ad not found or not clickable...')
    
    try:
        pyautogui.hotkey('ctrl', 'w')

        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ef5cccac"))
        )
        
        button.click()

        time.sleep(10)
    
    except:
        print('Drop down menu not found or is not clickable...')
    
    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='{location}']"))
        )
        
        # Click the button
        button.click()
    
    except:
        print('Input location not found...')
    
    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@aria-label='Find button']"))
        )
        
        # Click the button
        button.click()

    except:
        print('Find button not found or is not clickable...')

    return driver.page_source


def scraping_info(html_text):
    soup = BeautifulSoup(html_text, 'lxml')

    listings = soup.find_all('h2', class_ = 'c0df3811')
    titles = []
    for listing in listings:
        titles.append(listing.text)

    listings = soup.find_all('span', class_ = 'f343d9ce')
    prices = []
    for listing in listings:
        prices.append(listing.text)

    listings = soup.find_all('div', class_ = 'f74e80f3')
    links = []
    for listing in listings:
        links.append(f"https://www.zameen.com{listing.a['href']}")
    
    data_dict = {
        'title':titles,
        'price':prices,
        'link':links
    }

    return pd.DataFrame(data_dict)


if __name__ == '__main__':
    location = input('Enter your desired location: ')
    html_text = finding_page(location)
    df = scraping_info(html_text)
    df.to_csv('./zameen.csv', index=False)