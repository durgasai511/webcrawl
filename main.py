# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 10:59:05 2022

@author: Durgasai
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:16:55 2022

@author: Durgasai
"""

from selenium import webdriver  
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.chrome.options import Options
import json 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import math
import logging 
import datetime
from browser import webscrap
import schedule
import sys
import os
import datetime 
from pymongo import MongoClient 
from io import StringIO





#data = {'TIME':["2.sec"],'CARNAME':[28,34,29,42],'CAR_VIN':[""]}
def append_data_to_excel(excel_name, data):
    columns = []
    for k, v in data.items():
        columns.append(k)
    df = pd.DataFrame([data],index= None)
    df_source = None
    if os.path.exists(excel_name):
        df_source = pd.read_excel(excel_name,engine='openpyxl')
    if df_source is not None:
        df_dest = df_source.append(df)
    else:
        df_dest = df
    with pd.ExcelWriter(excel_name) as writer:    
        df_dest.to_excel(writer, index = False, columns=columns)












def crawl_one_vehicle(vehicle_number,car1):
    ########################### cars ###############
    pagenumber=math.ceil(vehicle_number/25)
    car1.vehiclepage_index(pagenumber)
    carnumber=((vehicle_number-1)%25)+1
    #### log and record
    vehicle_name,date_vec,start_vec=car1.vehiclepage(carnumber)
    ############ car page ############
    p={}
    p["title"],vin=car1.title_car()
    p["Dealer_block"]=car1.dealer_block()
    p["Inspection_summary"]=car1.inspection_summary()
    p["vehicle_history()"]=car1.vehicle_history()
    p["tire_info"]=car1.tire_info()
    p["vehicle_damage"] = car1.vehicle_damage()
    p["vehicle_data"] = car1.vehicle_data()
    p["blackbox"]=car1.blackbox()
    
    ############### back #############
    car1.back()
    #################### record file update #############
    now = datetime.datetime.now()
    recorddata={"TIME":now,"Vehicle name":vehicle_name,"VIN number":vin,"auction_data":date_vec,"auction_time":start_vec} # record data # record data 
    
    append_data_to_excel(excel_name="recordfile.xlsx",data= recorddata) #function 
    
    return(p,vin)

    


def crawl():
    ########## global variable #########\
    global vehicle_every_day_number
    global carsdata_mongo
    global driver
    ################ driver ######################
    ###############################################################################






    logging.basicConfig(filename=str(datetime.date.today())+'crawl.log',level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s',filemode='w')
    logger = logging.getLogger("mymodile")
    logger.info("Chrome is setting up")
    print("log")
    try:
        chromeOptions=webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--window-size=1920,1200")
        #chromeOptions.add_argument("--remote-debugging-port=9222")
        chromeOptions.add_argument('--no-sandbox')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chromeOptions)
        url="https://buy.adesa.com/openauction/home.html?utm_campaign=login&utm_medium=header&_ga=2.221806684.53809960.1661774707-923575821.1661774707&utm_content=button&utm_source=adesa.com&SAMLResponse=eJylVF1v2zAM%2FCuG3%2BPG3oJtQmIsSDAgwJpuTdEBfWMl2pZtfUCS2%2F78SU5ipJmbDpvfeCKP1B3luQXRanKLVitpMdqsF7EqS1pSqouqbrlogDY1QqNrDbqpRC0KqrWPyji6R2O5kos4S6ZxtLG2w420DqTz0DTLJtPPk%2BzLXZqR6YyksySdfXiIoxfRSktC40XcGUkUWG6JBIGWOEp2y%2BvvxBMSsBaN8%2FynJfpyjTbKKaraOJ%2BHbNLPZHJrled6QvPVJ7A0AYYWEqrE%2FOo0bb5XY%2BfAdfZ1tFIMo3toO7w8gO2zD4IyNPF%2F0WzVD68Cf8L4Kt%2BPekp0Bh2uvDzK9teGBNOZKgRtJAVJUVLKC1rVlYam8p8QqmzDRkB1bvq%2Fy0x23WON1B2irZdgs46%2BKSPAva1NmqQ9wtmk6FPJLy6ZerZrJYDLnx20vODIAl3Q7LTTSsmCh5qgzTW6SrHLJlBBHhHMYOIY0RocRFvlbuSNWRYOzR9Cf9oL%2FfFh8HCM5%2Bzo6GXnKhncRYHSRX34vqGnxb6Hwxc3Aq1av1q3WOQX3yAlNOR5OGziszLsMOgo1cjZK2y4yoAel3XY5eOvKP8NC7%2BerQ%3D%3D"
        logger.info("driver is loaded Successfully")
    except: 
        logger.error("driver is not loaded properly")   
    ############################ login 
    username="davidwu"
    password='TnAR2Zj7vnFRVj!'
    car1=webscrap(driver,username,password,url,logger)
    car1.login_page()
    ############################## searchbox
    car1.searchbox()
    val=True
    print(vehicle_every_day_number)
    while val:
        print(vehicle_every_day_number)
        
        cardata,VIN=crawl_one_vehicle(vehicle_every_day_number,car1)
        
       
        print(VIN)
        ######################## data to  json ####################
        #with open("{VIN}.json".format(VIN=VIN), "w") as outfile:
            #json.dump(cardata, outfile)
        ########################### 
        
        
        
        ##################dumping to json #######
        mongocar={"VIN":VIN,"cardata":cardata}
        record = json.dumps(mongocar) 
        io = StringIO(record)   #converting string to json 
        mongocar=json.load(io)
        
        
        ################# dumping the data to monog db
        
        rec=mydatabase.carsdata_mongo.insert_one(mongocar)
        ######################################################
        vehicle_every_day_number=vehicle_every_day_number+1
        now=datetime.datetime.now().time()
        if datetime.time(21,00,0,0) < now:
            car1.close()
            break
            
            
            


vehicle_every_day_number = 1   ##### vehicle number 
 

######################################## mongodb ################### 
client=MongoClient()
  
# Connect with the portnumber and host
host=  'mongodb://127.0.0.1:27017'
client = MongoClient(host) # local host 
  
# Access database
mydatabase = client["adesa"]
  
# Access collection of the database
carsdata_mongo=mydatabase["carsdata"]
####################################################



      
schedule.every().day.at("09:00").do(crawl)
now = datetime.datetime.now()
print("now =", now)
while True:
    ##################
    
    schedule.run_pending()
    time.sleep(1)
    #print("##################"+str(vehicle_every_day_number))
       
    
            
     