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
from test import load_cookies, save_cookies

bookInformation = {} 
url = "https://read.amazon.com/kindle-library"
cookies_file = "cookies.pkl"

driver = webdriver.Chrome()
driver.get(url)

if os.path.exists(cookies_file):
        load_cookies(driver, cookies_file)
        driver.refresh()
        print("Page refreshed after loading cookies")

while True:
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load more titles')]"))
        )
        load_more_button.click()
        time.sleep(5)  # Wait for additional content to load
    except Exception as e:
        print("No more 'Load more titles' button found or unable to click.")
        break
       

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'books-content'))
    )
    print("Cookies are still valid")   
except Exception as e:
    print("Cookies are expired or invalid, manual login required")
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.ID, 'books-content'))
    )
    save_cookies(driver, cookies_file) 

time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
with open("page_source.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())
time.sleep(2)
books = soup.find_all('li', role='button')

for book in books:
    title_div = book.find('div', id=lambda x: x and x.startswith('book_info-title'))
    title = title_div.text.strip() if title_div else 'N/A'
    
    author_div = book.find('div', id=lambda x: x and x.startswith('book_info-author'))
    author = author_div.text.strip() if author_div else 'N/A'
    
    image_tag = book.find('img', id=lambda x: x and 'Select to open quick view' in x)
    image_url = image_tag['src'] if image_tag else 'N/A'
    
    bookInformation[title] = {
        'author': author,
        'imageURL': image_url
    }
    print(f"Title: {title}, Author: {author}, Image URL: {image_url}")

backendURL = "http://54.89.225.92/save_books"

response = requests.post(backendURL, json=bookInformation)

if response.status_code == 200:
     print("Books sent to backend server")
else:
     print(f"Failed to send book information. {response.status_code}, Response: {response.text}")    



