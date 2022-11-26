# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:14:50 2022

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
import math
import logging 
import datetime
import numpy as np





class webscrap():
    def __init__(self,driver,username,password,url,logger):
        self.driver=driver
        self.username=username
        self.password=password
        self.url=url
        self.logger=logger
    def login_page(self):
        self.driver.get(self.url)
        self.logger.info("IN login page")
        #self.driver.maximize_window()
        time.sleep(3)
        try:
            self.driver.find_element(by="xpath",value='//*[@id="accountName"]').send_keys("davidwu")
            time.sleep(3)
            self.driver.find_element(by="xpath",value='//*[@id="password"]').send_keys('TnAR2Zj7vnFRVj!')
            time.sleep(3)
            self.driver.find_element(by="xpath",value='//*[@id="loginSubmit"]').click()
            self.driver.implicitly_wait(20)
            self.logger.info("loggin successfully")
        except:
            self.logger.error("error in login the website")
        
    def searchbox(self):
        try:
            time.sleep(10)
            t='document.querySelector("#headerContainer > ol-header-t1").shadowRoot.querySelector("#search-button").click()'
            searchbox=self.driver.execute_script(t)
          
            self.logger.info("searchbox successfully")
        except:
            time.sleep(10)
            self.searchbox()
        
                
    def vehiclepage_index(self,vehicle_page_index):
        try:
            num=vehicle_page_index
            list_page='document.querySelector("#onboarding-srp > nw-pagination > div > ul > li:nth-child({p}) > a").click()'.format(p=num)
            self.driver.execute_script(list_page)
        except:
            time.sleep(10)
            self.vehiclepage_index(vehicle_page_index)

        
    def vehiclepage(self,vehicle_number):
        try:
            vehicles_list=self.driver.find_elements(by="xpath",value='//*[@id="vehicleListing"]/div') 
            name_vehicle=vehicles_list[0].find_elements(by="class name",value="vehicleLink")
            vp=name_vehicle[2*(vehicle_number-1)].text
            ##### timer 
            timer=vehicles_list[0].find_elements(by="class name",value="timer")
            date_vec,start_vec=timer[2*(vehicle_number-1)].text,timer[2*(vehicle_number)-1].text
            #######
            list_name=[]
            for i,c in enumerate(name_vehicle):
                if i%2==0:
                    list_name.append(c.text)

            #######
            name_vehicle[2*(vehicle_number-1)].click()
            self.logger.info("vechile:{p}  reading the data ".format(p=vp))
            return(vp,date_vec,start_vec)
        except:
            time.sleep(10)
            return(self.vehiclepage(vehicle_number))


    def title_car(self):
        try:
            v = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-title-position-ol-page-title").shadowRoot.querySelector("ol-subtitle").shadowRoot.querySelector("div > span > div:nth-child(2) > kar-vin-1x-0y-0zdevelop115").shadowRoot.querySelector("kar-tooltip-1x-0y-0zdevelop115 > kar-typography-1x-0y-0zdevelop115.vin__text.hydrated")'
            vin = self.driver.execute_script(v).text
            m = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-title-position-ol-page-title").shadowRoot.querySelector("ol-subtitle").shadowRoot.querySelector("div")'
            header = self.driver.execute_script(m).text
            self.logger.info("title data successfull")
            return(header,vin)
        except:
            time.sleep(5)
            return(self.title_car())
    
    def dealer_block(self):
        #location
        try:
            location = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-sidebar-position-ol-auction-channel").shadowRoot.querySelector("div > div.vehicle-location-and-status > div.vehicle-location-and-status__fields")'
            vl =self.driver.execute_script(location)
            vehiclelocation = vl.text.split("\n")
            p = {}
            for c in range(len(vehiclelocation)//2):
                p[vehiclelocation[c*2]] = vehiclelocation[c*2+1]
            ###info
            information = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-sidebar-position-ol-purchase-options").shadowRoot.querySelector("div")'
            i = self.driver.execute_script(information)
            information1 = i.text.split("\n")
            for c in range(len(information1)//2):
                p[information1[c*2]] = information1[c*2+1]
            self.logger.info("dealer_block data successfull")
            return(p)
        except:
            return(self.dealer_block())
    
    
    def inspection_summary(self):
        #inspection
        try:
            inspectsummary = self.driver.execute_script('return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-1-position-ol-inspection-summary").shadowRoot.querySelector("div")')
            inspectsummary_table=inspectsummary.find_elements(by="class name",value="inspection-summary__column")
            inspection_table1=inspectsummary_table[0]
            inspection_table2=inspectsummary_table[1]
            name_values = inspection_table1.find_elements(by="tag name",value="ol-field")
            table=[]
            for c in name_values:
                table.append(str(c.text).split("\n"))
            name_values = inspection_table2.find_elements(by="tag name",value="ol-field")
            for c in name_values:
                table.append(str(c.text).split("\n"))
            dict_table={}
            for c in table:
                dict_table[c[0]]=c[1]
            self.logger.info("inspection  data successfull")
            return(dict_table)
        except:
            return(self.inspection_summary())
    
    def vehicle_history(self):
        #### vehicle histroy 
        try:
            vht = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-2-position-ol-vehicle-history-reports").shadowRoot.querySelector("div")'
            vehicle_history_table1 = self.driver.execute_script(vht)
            vehicle_history = str(vehicle_history_table1.text).split("\n")
            self.logger.info("vechile_history data successfull")
            return(vehicle_history)
        except:
            return(self.vehicle_history())
        
        
    def vehicle_damage(self):
        try:
            dmg = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-3-position-ol-damages").shadowRoot.querySelector("ol-table-1x-0y-0zdevelop91")'
            damages = self.driver.execute_script(dmg)
            if damages is None:
                return("None")
            else:
                vehicledamages = damages.text.split("\n")
                end=len(vehicledamages)
                for i,c in enumerate(vehicledamages):
                    if len(c)>200:
                        end=i
                vd=np.array(vehicledamages[:end])
                vd=vd.reshape(-1,3)
                vdmg=pd.DataFrame(vd[1:])
                vdmg.columns=vd[0]
                vdmg=vdmg.to_dict()
                self.logger.info("vechile_damage data successfull")
                return(vdmg)
        except:
            return(self.vehicle_damage())
        
    def tire_info(self):
        #tires 
        try:
            tires ='return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-3-position-ol-tire-detail").shadowRoot.querySelector("div")'
            table_hydrated = self.driver.execute_script(tires)
            t=table_hydrated.text
            list_table_hydrate=t.split("\n")
            list_table_hydrate.insert(0,"Rating")
            k=len(list_table_hydrate)

            if k>2:
                np_list=np.array(list_table_hydrate)
                reshaped=np_list.reshape(-1,7)
            else:
                np_list=np.array(list_table_hydrate)
                reshaped=np_list.reshape(-1,2)

            df=pd.DataFrame(reshaped[1:])
            df.columns=reshaped[0]
            self.logger.info("tire info data successfull")
            return(df.to_dict())
        except:
            return(self.tire_info())
            
    
    def vehicle_data(self):
        try:
            complete_data={}
            #information
            information='return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-3-position-ol-vehicle-data").shadowRoot.querySelector("div > div > ol-original-data").shadowRoot.querySelector("ol-original-vehicle-info").shadowRoot.querySelector("div")' 
            vh = self.driver.execute_script(information)
            vehicle_information1 = vh.find_elements(by = "class name", value = "vehicle-info__key")
            vehicle_information2 = vh.find_elements(by = "class name", value = "vehicle-info__value")
            p = {}
            for c in range(len(vehicle_information1)):
                p[vehicle_information1[c].text] = vehicle_information2[c].text
                
            complete_data["information"]=p  
            self.logger.info("vehicle_information data successfull")
            
            ############### additional info
            avi = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-3-position-ol-vehicle-data").shadowRoot.querySelector("div > div > ol-original-data").shadowRoot.querySelector("ol-original-data-additional-vehicle-info")'
            additionalvi = self.driver.execute_script(avi)
            additional = additionalvi.text.split("\n")
            complete_data["additional_info"]=additional
            self.logger.info("vehicle additonal info data successfull")
            
            ############### high value
            
            hvo = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-3-position-ol-vehicle-data").shadowRoot.querySelector("div > div > ol-original-data").shadowRoot.querySelector("div > ol-original-data-high-value-options").shadowRoot.querySelector("ol-original-data-generic-list").shadowRoot.querySelector("div")'
            highvo = self.driver.execute_script(hvo)
            highvalueoption = highvo.text.split("\n")
            complete_data["high_value"]=highvalueoption
            self.logger.info("vehicle high value data successfull")
            ############  equipments 
            
            e = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-3-position-ol-vehicle-data").shadowRoot.querySelector("div > div > ol-original-data").shadowRoot.querySelector("div > ol-original-data-equipment").shadowRoot.querySelector("ol-original-data-generic-list")'
            e_ment = self.driver.execute_script(e)
            equipment = e_ment.text.split("\n")
            complete_data["equipments"]=equipment
            self.logger.info("vehicle equipments data successfull")
            
            
            
            return(complete_data)
        except:
            return(self.vehicle_data())
        
    
    
    def blackbox(self):
        try:

            blackbook = 'return document.querySelector("#microfrontends > ol-widget-shell").shadowRoot.querySelector("#template1-below-the-fold-3-position-ol-appraisals").shadowRoot.querySelector("div > div > div:nth-child(1) > ol-titled-card").shadowRoot.querySelector("div > ol-gridded-content").shadowRoot.querySelector("div > div")'   
            bb = self.driver.execute_script(blackbook)
            blackbook1 = bb.text.split("\n")
            appraisal = {}
            for c in range(len(blackbook1)//2):
                appraisal[blackbook1[c*2]] = blackbook1[c*2+1]
            self.logger.info("appraisal data successfull")
            return(appraisal)
        except:
            return(self.blackbox())

    def back(self):
        self.driver.back()
    def close(self):
        self.driver.quit()
        
        
        


    



    

        
        