'''Start Scraping , will store master_links first and then go to scrape the actual house data.'''


from Store_master_links import store_master_links
from Store_Values import store
from CreateModel import  create
from Initialize_Database import  create_db

#create_db()
store_master_links()
store()
create()
