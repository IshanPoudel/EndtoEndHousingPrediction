''' Grabs each house_link from the master_link database , calls the get_values_from
_each_house function and stores it in the house_attributes database.
Can use threading if specified on the config file.'''


import config
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
import config
import time
import traceback
import re
import mysql.connector
import threading
from threading import Lock
from random import randint

#import function from get_values_fr0m_each_house
from Get_values_from_each_house import get_house_attributes


db = mysql.connector.connect(host="localhost",
                             user=config.user,
                             passwd=config.password,
                             db='real_estate_db_for_ml'
                             )
mycursor = db.cursor()

def chunks(list_to_split , n_parts):
    ''' Splits the house link list into n_parts for threading. '''

    n_parts = max(1, n_parts)
    n_parts = min(n_parts , len(list_to_split))

    print("Splitting into" + str(n_parts) + " parts")

    chunk_size, remainder = divmod(len(list_to_split), n_parts)




    return (list_to_split[i*chunk_size+min(i,remainder):(i+1)*chunk_size+min(i+1 , remainder)]  for i in range(n_parts))


def update_to_db(link_and_id ):

    ''' Grbas link_and_id from the master database and updates it.'''
    count = 0
    for link , id in link_and_id:
        time.sleep(randint(5 , 20))

        to_commit = get_house_attributes(link)

        query = "INSERT INTO HOUSE_ATTRIBUTES(house_id , address , num_bed, num_bath , sq_ft , price ) VALUES (%s , %s , %s , %s , %s , %s) "
        if to_commit[0]=='Error':
            print("Error")
        else:
            #change value of house_agent_table
            try:

                print("Before updating num_bed = %d , num_bath = %d " , to_commit[1] , to_commit[2])


                mycursor.execute(query , (int(id) , str(to_commit[0]), to_commit[1] , to_commit[2] , to_commit[3] , to_commit[4]) )
                db.commit()

                #change value of data_present of house_link table to true
                Q = "UPDATE house_link SET DataScraped=true WHERE houseID="+str(id)
                mycursor.execute(Q)
                db.commit()

                print("Updated house with address"+ to_commit[0])
                count = count+1

            except Exception:
                print("Could not update")
                print(traceback.format_exc())
    print("Updated " + str(count) + "values")


def store():
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 passwd="rootroot",
                                 database="real_estate_db_for_ml")

    mycursor = db.cursor()

    mycursor.execute("SELECT link , houseID FROM house_link WHERE DataScraped = false")
    link_and_id = mycursor.fetchall()

    split_link_into_n_parts = config.no_of_threads
    list_for_threads = chunks(link_and_id, split_link_into_n_parts)

    # split the list into equal sizes and feed it to the function below .
    # link_and_id have to be split into equal parts.

    lock = Lock()

    threads = []

    # for house_link_and_id in list_for_threads:
    #     print(house_link_and_id)
    #     print("haha")

    for house_link_and_id in list_for_threads:
        t = threading.Thread(target=update_to_db, args=(house_link_and_id,))
        t.start()
        print("I started a thread")
        threads.append(t)

    for thread in threads:
        thread.join()


