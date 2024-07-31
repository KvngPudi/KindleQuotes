from selenium import webdriver
import json
import pickle
import time
import requests

response = requests.get("http://54.89.225.92/get_cookies")
ios_cookies = response.json()



driver = webdriver.Chrome()


url = "https://read.amazon.com/notebook?ref_=kcr_notebook_lib&language=en-US"
driver.get(url)


for name, value in ios_cookies.items():
    driver.add_cookie({
        'name': name,
        'value': value.strip('"'),
        'domain': '.amazon.com',  
        'path': '/' 
    })


driver.get(url)

time.sleep(5)


updated_cookies = driver.get_cookies()


with open('cookies.pkl', 'wb') as file:
    pickle.dump(updated_cookies, file)


