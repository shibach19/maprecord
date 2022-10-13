# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 22:29:42 2022

@author: Eason
"""


#===============


import csv
from time import sleep

from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.by import By

#-----------------------------------------------------------------------------

def loadlistitem(itemnum,ouputlist):    
    for x in range (0,itemnum):    # 讀取目標網站清單個數
        sleep(8)
        
        # 找第一個商家
        #li = browser.find_elements(By.CLASS_NAME,"rllt__details")
        #li[x].click()
       
        #點擊左邊列表簽單商家
        try:
            li = browser.find_elements(By.CLASS_NAME,"dbg0pd.eDIkBe")
            li[x].click()
        except:
            print("Finall ! ")
        #
        
        #pane = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]')
        sleep(1)
    
        #商家頁面點擊 更多評論
        comnum = (4,8,12,16,20)
        commentnumber =  int(comnum[3])
        panel_click = browser.find_element(By.CLASS_NAME,"hqzQac").click()
        
        sleep(3)
        
        #設定迴圈載入更多評論 動態載入
        for i in range(0,commentnumber):
            try:
                page2 = browser.find_element(By.XPATH,'/html/body/span/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[2]')
                browser.execute_script('arguments[0].scrollBy(0, 1000000);', page2)
                print(i)
            except:
                break
            sleep(1)
        
        print("--------------------------------------")
        
        # 用美湯解析網頁內容
        sp = Soup(browser.page_source,"html.parser")
        
        #資料處理 - > 尋找每一則評論的div
        transtable = sp.find_all("div",class_="WMbnJf vY6njf gws-localreviews__google-review")
        storeid = sp.find("div",class_="P5Bobd")
       
        #將找到的div進行資料處理 並新增進去output的list中
        for article in transtable:
            scores = article.find("span", class_="Fam1ne EBe2gf")
            users = article.find("div",class_="TSUbDb")
            comments = article.find("div",class_="Jtu6Td")
            time = article.find("span",class_="dehysf lTi8oc")
            print("商店名稱：" + storeid.text)
            print("用戶:"+ users.text )
            print("時間:" + time.string )
            print("評分:"+ scores['aria-label'])
            print("評論:"+ comments.text )
            ouputlist.append([ storeid.text , users.text , time.string 
                             , scores['aria-label'] , comments.text] )
     
            
        #匯入csv檔，儲存在同一路徑中 檔名為output.csv
        with open('output.csv', 'w',encoding='UTF-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(ouputlist)
            
        print("Finished")
        sleep(5)
        browser.back()
        #返回到商家清單

#--------------------------------------------------------
#設定GPS位置
params = {
    'latitude': 24.145890,
    'longitude': 120.645221,
    'accuracy': 1000
}


browser  = webdriver.Chrome()
browser.execute_cdp_cmd('Page.setGeolocationOverride', params)
# 設定GPS 結束
# 讀取目標網站
browser.get("https://www.google.com/search?tbs=lf:1,lf_ui:4&tbm=lcl&sxsrf=ALiCzsav51EW5_t4v0ZbmFap6nj0p-DpeQ:1657281327420&q=%E8%B7%AF%E6%98%93%E8%8E%8E&rflfq=1&num=10&ved=2ahUKEwjo8cCGnun4AhXINd4KHVJBDQsQtgN6BAgLEAY#rlfi=hd:;si:;mv:[[24.16568411919236,120.72173693735263],[24.118768443241237,120.62594988901279],null,[24.142228433509775,120.67384341318271],14]")
#End
#

# 計算目標個數  用於副程式之迴圈數值
countnum = browser.find_elements(By.CLASS_NAME,"rllt__details")
itemnum = len(countnum)
#
ouputlist  = [['商店名稱','姓名','時間','評分','評論']]

#呼叫副程式 - > 進行資料撈取
loadlistitem(itemnum,ouputlist)

#載入左側商家清單中，為換頁做準備
leftpanel = browser.find_element(By.ID,"center_col")
browser.execute_script('arguments[0].scrollBy(0, 1000000);', leftpanel)
#換頁
browser.find_element(By.ID,"pnnext").click()
sleep(5)

#繼續進行
loadlistitem(itemnum,ouputlist)


