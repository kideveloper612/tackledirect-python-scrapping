import requests
import os
import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()
    return driver


def wait_for(driver, condition):
    delay = 3  # seconds
    try:
        return WebDriverWait(driver, delay).until(EC.presence_of_element_located(condition))
    except TimeoutException:
        pass


def write(lines, file_name):
    with open(file=file_name, encoding='utf-8', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def main():
    driver = get_driver()

    urls = [
        'https://www.tackledirect.com/strike-king-kvd-1-5-deep-crankbait.html',
        'https://www.tackledirect.com/megabass-destroyer-usa-rods.html'
    ]

    for url in urls:
        driver.get(url)
        title = driver.find_element_by_class_name('cyc-item-h1').text

        color_options = driver.find_elements_by_css_selector('#strike-king-kvd-1-5-deep-crankbait-opt > option')
        for color_option in color_options:
            color = color_option.text
            if color == '- Select Option -':
                continue
            driver.find_element_by_xpath("//select[@id='strike-king-kvd-1-5-deep-crankbait-opt']/option[text()='{}']".format(color)).click()
            price = driver.find_element_by_class_name('cyc-item-price').text.replace('Price:', '').strip()
            image = driver.find_element_by_id('cycmainproductimage').get_attribute('src')
            qty = driver.find_element_by_css_selector('[name="vwquantity0"]').get_attribute('value')
            print(title, image, price, color, qty)


if __name__ == '__main__':
    main()
