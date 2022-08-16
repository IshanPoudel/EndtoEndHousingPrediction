'''Start Scraping , will store master_links first and then go to scrape the actual house data.'''


from Scraping.Store_master_links import store_master_links
from Scraping.Store_Values import store

store_master_links()
store()