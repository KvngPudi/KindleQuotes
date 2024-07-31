from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import requests

with open('cookies.json', 'r') as file:
    cookies = json.load(file)

# Convert cookies to a format suitable for requests
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

url = "https://read.amazon.com/notebook?ref_=kcr_notebook_lib&language=en-US"

response = requests.get(url, headers=headers, cookies=cookies_dict)
soup = BeautifulSoup(response.content, 'html.parser')



def main():
    with open('cookies.json', 'r') as file:
        cookies = json.load(file)

    # Convert cookies to a format suitable for requests
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    url = "https://read.amazon.com/notebook?ref_=kcr_notebook_lib&language=en-US"

    response = requests.get(url, headers=headers, cookies=cookies_dict)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        books = getBooks(soup)
        highlights = {}

        for book in books:
            print("extracting highlights for " + book)
            try:
                hs = getHighlights(soup)
                highlights[book] = hs
            except Exception as e:
                print(f"Could not extract highlights for {book}: {e}")
    else:
        print(f"Failed to retrieve page: {response.status_code}")

def getBooks(soup): 
    books = []
    book_elements = soup.find_all('h2')  

    for book_element in book_elements:
        book_title = book_element.text.strip()
        books.append(book_title)
        # print(book_title)
    return books

def getHighlights(soup):
    elements = soup.find_all('span', id='highlight')
    highlights = []
    for e in elements:
        highlights.append(e.text)
        print(e.text)
    return highlights  

if __name__ == "__main__":
    main()
