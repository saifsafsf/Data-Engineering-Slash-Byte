from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time


def finding_page(location):
    '''
    Returns the source page text for the given location

    Parameters
    ----------
    location : str
        The location given by the user to collect data about

    Returns
    -------
    driver.current_url : str
        The url referring to the properties list from the given location
    
    num_of_pages : int
        Number of pages that can be iterated to collect data from this location
    '''

    # Setting up Chrome driver, make sure the chromedriver.exe is in the same directory
    driver = webdriver.Chrome()
    driver.get('https://www.zameen.com/')
    time.sleep(5)

    # CLicking the google ad since the close button is not accessible
    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "google_ads_iframe_/31946216/Splash_660x500_0"))
        )
        
        button.click()

    except:
        print('Ad not found or not clickable...')
        return '', 0
    
    # Close the ad & open the drop-down list of cities
    try:
        # Ctrl + W to close the ad tab, do not change the window until the ad is closed
        pyautogui.hotkey('ctrl', 'w')

        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ef5cccac"))
        )
        
        button.click()
    
    except:
        print('Drop down menu not found or is not clickable...')
        return '', 0
    
    # Choose the input location from the drop-down list
    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='{location}']"))
        )
        
        button.click()
    
    except:
        print('Input location not found...')
        return '', 0
    
    # Clicking the 'find' button
    try:
        button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@aria-label='Find button']"))
        )
        
        button.click()

    except:
        print('Find button not found or is not clickable...')
        return '', 0
    
    # Extracting the number of properties available for the location
    html_text = requests.get(driver.current_url).text
    soup = BeautifulSoup(html_text, 'lxml')

    num_of_properties = int(''.join(soup.find('h1', class_='_2aa3d08d').text.split()[0].split(',')))

    # calculating the number of webpages using number of properties
    num_of_pages = num_of_properties // 25

    return driver.current_url, num_of_pages


def scraping_info(base_url, num_of_pages = 3):
    '''
    Returns titles, prices, & URLs for all properties available on the base url and subsequent given number of pages

    Parameters
    ----------
    base_url : str
        The link to page 1 of the given location
    
    num_of_pages : int
        the number of webpages available for the given location

    Returns
    -------
    df : pd.DataFrame
        A dataframe containing all the scraped data (titles, prices, URLs)
    '''

    titles = []
    prices = []
    links = []

    # for each webpage of the location's properties
    for page_num in range(1, num_of_pages+1):
        
        # changing the page number for each iteration in the url
        url = base_url[:-6] + str(page_num) + '.html'

        # retrieving page source
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # extracting all the titles
        listings = soup.find_all('h2', class_ = 'c0df3811')
        for listing in listings:
            titles.append(listing.text)

        # extracting all the prices
        listings = soup.find_all('span', class_ = 'f343d9ce')
        for listing in listings:
            prices.append(listing.text)

        # extracting all the URLs
        listings = soup.find_all('div', class_ = 'f74e80f3')
        for listing in listings:
            links.append(f"https://www.zameen.com{listing.a['href']}")
        
    # creating a dictionary to make a dataframe
    data_dict = {
        'title': titles,
        'price': prices,
        'link': links
    }

    # returning a dataframe for easier conversions into JSON or CSV
    df = pd.DataFrame(data_dict)

    return df


if __name__ == '__main__':
    location = input('Enter your desired location: ')

    # finding the source page & scraping the information
    url, num_of_pages = finding_page(location)
    df = scraping_info(url)

    # saving the dataframe into a CSV
    df.to_csv(f'./zameen-{location}.csv', index=False)