import os,re,sys
import numpy as np
import pandas as pd
from collections import defaultdict
import time
import pdb

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

################
def get_price(price_row):
    price_str = price_row[0].contents[0].split()[1].split(',')[0]
    list_digits = [i for i in price_str if i.isnumeric()]
    price_int = int(''.join(list_digits))
    return price_int
##################
def get_disabled_bool(soup):
    next_page_row = soup.find_all('li', {'class':'next-page'})
    disabled_next = bool(len(next_page_row[0].find_all('a', {'class':'disabled'})))
    return disabled_next

##################
def check_is_number(value):
    if value.isnumeric():
       return int(value)
    else:
        return np.nan
##################
def get_info_auto(list_autos, df_as24):

    for item in list_autos:
        n_row_df = len(df_as24)
        model_row = item.find_all('h2',{'class':"cldt-summary-makemodel sc-font-bold sc-ellipsis"})
        try:
            model = model_row[0].contents[0]
        except:
            print(model_row, model)
            #if it does not find the model, then skip
            continue
        df_as24.loc[n_row_df,'model'] = model
        #
        version_row = item.find_all('h2',{'class':"cldt-summary-version sc-ellipsis"})
        if len(version_row)>0:
            version = version_row[0].contents[0]
        else:
            version = None
        df_as24.loc[n_row_df,'version'] = version
        #
        equipments = item.find_all('h3', {'class':"cldt-summary-subheadline sc-font-m sc-ellipsis", 'data-item-name':"sub-headline"})
        if len(equipments) > 0:
            df_as24.loc[n_row_df,'equipments'] = equipments[0].contents
        else:
            df_as24.loc[n_row_df,'equipments'] = None
        #
        price_row = item.find_all('span',{'class':"cldt-price sc-font-xl sc-font-bold", 'data-item-name':"price"})
        price = get_price(price_row)
        df_as24.loc[n_row_df,'price'] = price
        #
        list_details = item.find_all('ul',{'data-item-name':"vehicle-details"})
    
        for child in list_details:
            list_li = child.find_all('li')
            for i, li_item in enumerate(list_li[0:len(list_features)]):
                if list_features[i] == 'mileage':
                    value = li_item.contents[0].strip().split(' ')[0].replace('.','')
                    print(n_row_df, list_features[i],check_is_number(value))
                    df_as24.loc[n_row_df, list_features[i]] = check_is_number(value)                    
                elif list_features[i] == 'n_owners':
                    value = li_item.contents[0].strip().split()[0]
                    print(n_row_df, list_features[i],check_is_number(value))
                    df_as24.loc[n_row_df, list_features[i]] = check_is_number(value)    
                else:
                    print(n_row_df, list_features[i],li_item.contents[0].strip())
                    df_as24.loc[n_row_df, list_features[i]] = li_item.contents[0].strip()
    return df_as24
##################
#list of autos to scrap
list_marca = ['Fiat', 'BMW', 'Renault','Citroen','Peugeot']
list_modello = ['Punto Evo', 'i3', 'ZOE','C-Zero','iOn']
list_file_out_name = ['data/AS24_Punto_Evo.csv', 'data/AS24_BMWi3.csv','data/AS24_ZOE.csv','data/AS24_CZero.csv','data/AS24_iOn.csv']
#set the auto to scrap
pos=4
marca = list_marca[pos]
modello = list_modello[pos]
csv_file_name = list_file_out_name[pos]
##################
#run the scraper
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
driver.get("https://www.autoscout24.it/")
#
#look for the brand input
elem_marca = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Marca']")))
elem_marca = driver.find_element(By.XPATH, "//input[@placeholder='Marca']")
elem_marca.send_keys(marca)
elem_marca.send_keys(Keys.RETURN)
#
time.sleep(3)
#look for the model input
elem_modello = driver.find_element(By.XPATH, "//input[@type='text'][@data-role='user-query'][@placeholder='Modello']")
elem_modello.send_keys(modello)
elem_modello.send_keys(Keys.RETURN)
#
time.sleep(3)
#click on search button
driver.find_element(By.XPATH, "//button[@data-test-id='search-execution-car']").click()
time.sleep(10)
#parse the first page
soup = BeautifulSoup(driver.page_source, features="lxml")


##################
#now, set the features columns and the dataframe

list_features = ['mileage','mmyy','power','use_type','n_owners','gear','fuel_type']
list_cols = ['model', 'version', 'equipments'] + list_features + ['price']
df_as24 = pd.DataFrame(columns=list_cols)
#parse the auto's list
list_autos = soup.find_all('div', class_="cl-list-element cl-list-element-gap")
#get the data into the dataframe
df_as24 = get_info_auto(list_autos, df_as24)

#check if there are next pages. If yes, 'disabled_next=False
disabled_next = get_disabled_bool(soup)

#loop on the pages until disabled_next=True
while not disabled_next:
    #click on 'next-page' button
    driver.find_element(By.XPATH, "//li[@class='next-page']").click()
    #wait
    time.sleep(3)
    #check the page is loaded
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cl-list-element cl-list-element-gap']")))
    #parse the page
    soup = BeautifulSoup(driver.page_source, features="lxml")
    #parse the auto's list
    list_autos = soup.find_all('div', class_="cl-list-element cl-list-element-gap")
    #get the data
    df_as24 = get_info_auto(list_autos, df_as24)
    print(df_as24.tail())
    #update the boolean
    disabled_next = get_disabled_bool(soup)
#    pdb.set_trace()
#exit firefox
driver.quit()
#write a csv file
df_as24.to_csv(csv_file_name)