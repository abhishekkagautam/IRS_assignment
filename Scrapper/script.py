import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import time
import sys
import os
import requests

driver  = webdriver.Chrome("chromedriver.exe")

def get_url(search_term):
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_ss_ts-do-p_4_4"
    search_term = search_term.replace(" ","+")
    url= template.format(search_term)+"&page={}"
    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.tesco.com/groceries/'+str(atag.get('href'))
    
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return
    
    try :       
        rating = item.i.text
        review_count = item.find('span',{'class':'a-size-base','dir':'auto'})
        if type(review_count) != 'NoneType':
            review_count=review_count.text
        else :
            review_count = ''
            
            
    except AttributeError:
        rating =''
        review_count =''
    
    result = (description,price,rating,review_count,url)
    
    return result

if __name__ == "__main__":
    
    count=0
    records =[]
    qurey=input("Enter Item to be searched")
    url = get_url(qurey)
    path="./"+qurey
    os.mkdir(path)
    
    for page in range(1,21):
        driver.get(url.format(page))
        
        soup = BeautifulSoup(driver.page_source,"html.parser")
        results = soup.find_all('div',{'data-component-type':'s-search-result'})

        for item in results:
            record =extract_record(item)
            if record:
                records.append(record)
                i=item.img
                try:
                    urllib.request.urlretrieve(i['src'],path+'/'+str(count)+".jpg")
                    count+=1
                    print("Number of entries= "+str(count),end='\r')
                except Exception as e:
                    pass
            
    driver.close()

    with open(qurey+'.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','rating','ReviewCount','Url'])
        writer.writerows(records)
    
    