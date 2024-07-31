from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import requests
import pickle


cookies_dict = {}

def main():
    bookHighlights = {}
    url = "https://read.amazon.com/notebook?ref_=kcr_notebook_lib&language=en-US"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    driver = webdriver.Chrome()
    driver.get(url)

    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'kp-notebook-library-each-book'))
    )
    
    getCookies(driver)

    with open('cookies.json', 'r') as file:
        cookies = json.load(file)

    

    response = requests.get(url, headers=headers, cookies=cookies_dict)
    soup = BeautifulSoup(response.content, 'html.parser')   

    books = driver.find_elements(By.CLASS_NAME, 'kp-notebook-library-each-book')

    for book in books:
        try:
            book.click()
            getCookies(driver)
            page_source = driver.page_source
            time.sleep(.5)
            highlights = getHighlights(page_source)
            # print(highlights)
            bookHighlights[book.text] = highlights
            
        except Exception as e:
            print(f"Could not extract highlights for a book: {e}")
            
    # for key, value in bookHighlights.items():
    #     print(f"{key}: {value}")        

    driver.quit()


    
def getHighlights(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    elements = soup.find_all('span', id='highlight')
    highlights = []
    for e in elements:
        highlights.append(e.text)
        # print(e.text)
    return highlights  

def getCookies(driver):
    time.sleep(.5)
    cookies = driver.get_cookies()
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)

    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}     





if __name__ == "__main__":
    main()




















