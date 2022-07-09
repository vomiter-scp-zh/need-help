from selenium import webdriver  #從library中引入webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import time
import sys
import os
import gc



chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless") #無頭模式
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-notifications")
chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
target="http://scp-zh-tr.wikidot.com/scp-zh-617"

success_time=0
fail_time=0

def main_fun():
    chrome.get(target)

    chrome.find_element(By.CSS_SELECTOR,'#pagerate-button').click()

    waithere=1
    waittime=0


    while waithere==1 and waittime<10:
        if chrome.find_elements(By.CSS_SELECTOR,'#action-area>p:nth-child(5)>a'):
            chrome.find_element(By.CSS_SELECTOR,'#action-area>p:nth-child(5)>a').click()
            waithere=0
        else:
            chrome.find_element(By.CSS_SELECTOR,'#pagerate-button').click()
            waittime+=1
            time.sleep(1)
    else:
        if waithere==0:
            print('取得查看評分者按鈕：成功')
        if waittime>=10:
            print('取得查看評分者按鈕：失敗')

    del waithere
    del waittime
    gc.collect()




    waithere=1
    waittime=0
    while waithere==1 and waittime<10:
        if chrome.find_elements(By.CSS_SELECTOR,'#who-rated-page-area>h2'):
            waithere=0
            print('取得評分者列表：成功')
        else:
            chrome.find_element(By.CSS_SELECTOR,'#action-area>p:nth-child(5)>a').click()
            waittime+=1
            time.sleep(1)
    
    del waithere
    del waittime
    gc.collect()




    unfair_vote=0

    raw_del_rates=chrome.find_elements(By.CSS_SELECTOR,'#who-rated-page-area>div>span.deleted+span')
    for i in range(len(raw_del_rates)):
        if '-' in raw_del_rates[i].get_attribute('innerHTML'):
            unfair_vote+=1
        if '+' in raw_del_rates[i].get_attribute('innerHTML'):
            unfair_vote-=1

    print(unfair_vote)
    del unfair_vote
    del raw_del_rates
    gc.collect()

    return(1)
    

while True:
    fail_time+=1
    if fail_time+success_time>999:
        gc.collect()
    try: 
        if main_fun()==1:
            success_time+=1
            fail_time-=1
    except:
        pass
    print(success_time)
    print(fail_time)
