''' For each link it gets , it grabs the houses relevant attributes.
Run get_house_attributes()
'''



from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Arlington<!-- -->, <!-- -->TX<!-- --> <!-- -->76013
# 76013

def parse_address(address_value):

    address = ""

    for value in address_value.split("<!-- -->"):
        if value != ', ' and value != " ":
            address = "".join((address, value + " "))
    return address

def parse_float(num):

    num = num.translate({ord('$'): None})
    num = num.translate({ord(','): None})
    num = float(num)
    return num

def parse_int(num):
    num = num.translate({ord('$'): None})
    num = num.translate({ord(','): None})
    num = int(num)
    return num


def parse_bed_bath_sqft(html):
    soup = BeautifulSoup(html, 'html.parser')

    try:

        bed_tag = soup.find("div", {"data-rf-test-id": "abp-beds"})
        num_bed = bed_tag.find("div", {"class": "statsValue"})
        num_bed = parse_int(num_bed.get_text())
    except:
        num_bed = "None"

    try:

        baths_tag = soup.find("div", {"data-rf-test-id": "abp-baths"})
        num_baths = baths_tag.find("div", {"class": "statsValue"})
        print("Before parsing : " + num_baths.get_text())
        num_baths = parse_float(num_baths.get_text())
        print("num_baths for this house is %d"  ,num_baths )

    except:
        num_baths = "None"

    try:

        sqft_tag = soup.find("div", {"data-rf-test-id": "abp-sqFt"})
        sqft_num = sqft_tag.find("span", {"class": "statsValue"})
        sqft_num = parse_float(sqft_num.get_text())

    except:
        sqft_num="None"

    return (num_bed , num_baths , sqft_num)


def get_house_attributes(url):
    ''' Given a url , it grabs all the relevant information for that house.'''



    chrome_options = Options()  # Instantiate an options class for the selenium webdriver
    chrome_options.add_argument("--headless")  # So that a chrome window does not pop up

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)


    driver.implicitly_wait(10)


    try:

        XPATH_TUPLE_FOR_ADDRESS = (By.XPATH, "//*[@id='content']/div[11]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/div/div/header/div/h1/div[2]")
        data = driver.find_element(*XPATH_TUPLE_FOR_ADDRESS)
        html_for_house_address = data.get_attribute('innerHTML')
        address = parse_address(html_for_house_address)
    except:
        address = "None"



    try:
        XPATH_TUPLE_FOR_PRICE = (By.XPATH , "//*[@id='content']/div[11]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/div/div/div/div[1]/div" )
        price_data = driver.find_element(*XPATH_TUPLE_FOR_PRICE).get_attribute('innerHTML')
        price_data = parse_float(price_data)


    except:
        price_data = "None"

    try:
        XPATH_TUPLE_FOR_BED_BATH_SQFT = (By.XPATH , "//*[@id='content']/div[11]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/div/div/div")
        html = driver.find_element(*XPATH_TUPLE_FOR_BED_BATH_SQFT).get_attribute('innerHTML')
        bed_bath_sqft = parse_bed_bath_sqft(html)
    except:
        bed_bath_sqft= "None"

    driver.close()

    #have bed , bath , sq ft as different
    num_bed = bed_bath_sqft[0]
    num_bath = bed_bath_sqft[1]
    sqft_num = bed_bath_sqft[2]



    return  address , num_bed , num_bath , sqft_num, price_data





