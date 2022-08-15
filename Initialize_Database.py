''' Initializes the database for value entry'''
import mysql.connector
import config

db = mysql.connector.connect(host="localhost" ,user = config.user , passwd= config.password)

mycursor = db.cursor()

mycursor.execute("DROP DATABASE IF EXISTS REAL_ESTATE_DB_FOR_ML")
mycursor.execute("CREATE DATABASE REAL_ESTATE_DB_FOR_ML")

db = mysql.connector.connect(host="localhost" ,
    user = config.user ,
    passwd= config.password,
    db='real_estate_db_for_ml'

    )

mycursor = db.cursor()

#create house_link table
mycursor.execute("CREATE TABLE house_link(  link VARCHAR(1000)  , houseID int PRIMARY KEY AUTO_INCREMENT , DataScraped Boolean not null default 0)")

#create house_atrributes table
# mycursor.execute("CREATE TABLE HOUSE_AGENT (house_id int PRIMARY KEY ,FOREIGN KEY(house_id) REFERENCES house_link(houseID), street_address VARCHAR(1000) , state_address  VARCHAR(1000) , agent_name VARCHAR(1000) , AGENCY VARCHAR(1000) , trec VARCHAR(10) , updated_on_final VARCHAR(10) default 'false')")

mycursor.execute("CREATE TABLE HOUSE_ATTRIBUTES(house_id int , address VARCHAR(1000) , num_bed int , num_bath double, sq_ft double(10,2) , price double(10,2))")

#Added stuff t