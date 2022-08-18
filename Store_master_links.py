''' Based on the url at the config file  , it gets each link on redfin and stores it in the databse.

Call the function store_master_link() '''


from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import *
import config
import time
import re
import mysql.connector

def get_list_of_houses(url):
    list_of_houses = []

    try:
        chrome_options = Options()  # Instantiate an options class for the selenium webdriver
        # chrome_options.add_argument("--headless")  # So that a chrome window does not pop up
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        time.sleep(10)

        # From website get all the tags



        driver.get(url)
        time.sleep(20)

        driver.implicitly_wait(10)
        html_text = driver.page_source
        # convert based on 'html parser'
        soup = BeautifulSoup(html_text, 'html.parser')
        # print(soup)
        # print("AFTER BREAK \n\n")

        # //*[@id="MapHomeCard_5"]

        # get all the div ids .

        homecard_list = soup.find("div", {"id": "content"})
        homecard_list = homecard_list.find("div", {"data-react-server-container": "7"})
        homecard_list = homecard_list.find("div", {"data-react-server-container": "14"})
        homecard_list = homecard_list.find("div", {"data-react-server-container": "18"})
        homecard_list = homecard_list.find("div", {"data-react-server-root-id": "22"})

        homecard_list = homecard_list.find("div", {"class": "HomeViewsAndDisclaimer"})
        homecard_list = homecard_list.find("div", {"class": "HomeViews"})
        homecard_list = homecard_list.find("div", {"class": "PhotosView bg-color-white"})
        homecard_list = homecard_list.find("div")

        # find all homnecard_List
        homecard_list = homecard_list.find_all("div", {"id": re.compile("^MapHomeCard")})

        text = "3D WALKTHROUGH"

        # homecard_list = soup.find("div" , {"class": "HomeCardContainer defaultSplitMapListView"})


        for home in homecard_list:

            text_blob = home.get_text()
            if (text not in text_blob):
                # get_link
                home = home.find("a")
                home = home['href']
                home = "https://www.redfin.com" + home
                list_of_houses.append(home)

        return list_of_houses


    except Exception as e:
        print(e)
        return list_of_houses


def store_master_links():

    db = mysql.connector.connect(host="localhost",
                                 user=config.user,
                                 passwd=config.password,
                                 db='real_estate_db_for_ml'
                                 )
    mycursor = db.cursor()


    url = config.url
    url_list = []
    url_list.append(url)

    for i in range(2 , 10):
        url_list.append(url+"/page-"+str(i))

    for url in url_list:
            time.sleep(20)
            print("Getting values from "+ url)


            house_link = get_list_of_houses(url)

            #need to know which errors did not work
            if house_link is None:
                print(url + "did not work")

            for house in house_link:
                # check if it is already in the database.
                # you have an incoming stream of houses , once you reach a house that has already been read previously you stop
                query = "SELECT link FROM house_link WHERE link = " + " '" + house + "'"
                mycursor.execute(query)
                check_if_present = mycursor.fetchall()

                if not check_if_present:
                    mycursor.execute("INSERT INTO house_link ( link ) VALUES (%s )",
                                     (house,))
                    db.commit()
                    print("Inserted into database")

                if check_if_present:
                    print("Up to Date")
                    print(house + "already in the table")
                    return
  






