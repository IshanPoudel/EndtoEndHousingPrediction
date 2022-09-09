# Deploy your full stack housing predictor by creating your own custom data set.



Making use of  property listings websites available online  , a crawler picks out housing features from each listing and adds it to a database. 

Once sufficient information is stored on a database , the application automatically parses the data points into a pandas dataframe. 




<H1> You can choose which area to use as the basis for your dataset. </H1>

1) Go to <a href = "https://www.redfin.com/city/30794/TX/Dallas">redfin.com </a> and search foor any location you want. 

2) Draw a map around such as the one below and put the link in the <code> config.py </code> file in the variable name <code> url</code>.
<img src = "https://github.com/IshanPoudel/EndtoEndHousingPrediction/blob/main/Assets/Drawing%20the%20input.png" width = "600" height = "500" >

3) To make the scraping more effecient , multi threading is used. To configure how many threads you want to use change the <code> no_of_threads</code> in <code> config.py </code>

4) Run <code> Start_Scraping.py </code>

<h1> Configuring database </h1>

1) In the <code> user</code> and <code>password</code> file in <code> config.py </code> specify the username and password of the local MySQL database. 

2) Once the scraper is run , the following database is created. 
  House_link consists of the house links scraped from the website. 
 
  <img src = "https://github.com/IshanPoudel/EndtoEndHousingPrediction/blob/main/Assets/House_Link.png"  width = "800" height = "500">
  
  
  House_attributes consists of data parameters for each of the house.
  
  <img src="https://github.com/IshanPoudel/EndtoEndHousingPrediction/blob/main/Assets/House_Attributes.png"  width = "800" height = "500">
  
  
 
 <h1> Preprocessing the dataset </h1>
 
   
