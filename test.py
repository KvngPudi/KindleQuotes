import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import requests

cookies_dict = {}

def save_cookies(driver, cookies_file):
    time.sleep(.5)
    cookies = driver.get_cookies()
    # print(cookies)
    with open(cookies_file, 'wb') as file:
        pickle.dump(cookies, file)
    print(f"Cookies saved to {cookies_file}")

def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                if 'sameSite' not in cookie:
                    cookie['sameSite'] = 'None'
                if driver.current_url.startswith("https://read.amazon.com"):
                    if cookie['domain'] == "read.amazon.com" or cookie['domain'].endswith(".amazon.com"):
                        # print(f"Adding cookie: {cookie}")
                        driver.add_cookie(cookie)
                    else:
                        print(f"Skipping cookie with invalid domain: {cookie}")
                elif driver.current_url.startswith("https://www.amazon.com"):
                    if cookie['domain'] == ".amazon.com":
                        # print(f"Adding cookie: {cookie}")
                        driver.add_cookie(cookie)
                    else:
                        print(f"Skipping cookie with invalid domain: {cookie}")
        print("Cookies loaded")

def cookieRefresh(driver, cookies_file):
    save_cookies(driver, cookies_file)
    print("Cookies are refreshed")
    time.sleep(1800)

def main():
    bookHighlights = {}
    url = "https://read.amazon.com/notebook?ref_=kcr_notebook_lib&language=en-US"
    cookies_file = "cookies.pkl"

    driver = webdriver.Chrome()
    driver.get(url)

    if os.path.exists(cookies_file):
        load_cookies(driver, cookies_file)
        driver.refresh()
        print("Page refreshed after loading cookies")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'kp-notebook-library-each-book'))
        )
        print("Cookies are still valid")   
    except Exception as e:
        print("Cookies are expired or invalid, manual login required")
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'kp-notebook-library-each-book'))
        )
        save_cookies(driver, cookies_file)  

    bookHighlights = kindleHighlights(driver, cookies_file) 
    # for key, value in bookHighlights.items():
    #     print(f"{key}: {value}")   

    backendURL = "http://54.89.225.92/save_highlights"

    response = requests.post(backendURL, json=bookHighlights)

    if response.status_code == 200:
        print("Highlights sent to backend server")
    else:
        print(f"Failed to send book information. {response.status_code}, Response: {response.text}")  

    cookieRefresh(driver, cookies_file)
    driver.quit()

def kindleHighlights(driver, cookies_file):
    bookHighlights = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    books = driver.find_elements(By.CLASS_NAME, 'kp-notebook-library-each-book')

    for book in books:
        try:
            book.click()
            save_cookies(driver, cookies_file)
            page_source = driver.page_source
            time.sleep(2)
            highlights = getHighlights(page_source)
            # print(highlights)
            bookHighlights[book.text] = highlights
            
        except Exception as e:
            print(f"Could not extract highlights for a book: {e}")
    
    for key, value in bookHighlights.items():
        print(f"{key}: {value}") 
    return bookHighlights          

def getHighlights(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    elements = soup.find_all('span', id='highlight')
    highlights = []
    for e in elements:
        highlights.append(e.text)
        # print(e.text)    
    return highlights  


if __name__ == "__main__":    
    main()
