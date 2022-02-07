from tkinter import Menubutton
from django.forms import CheckboxInput
from numpy import getbufsize
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
from posixpath import split
import json
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
import naverMenuCrawling

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)

actions = ActionChains(driver)
#json파일 전체
JsonGroup = dict()

goWhere = str(input("원하는 행정구역을 입력하세요: "))
admDivision = str(input("원하는 행정동을 입력하세요: "))

#새 탭 생성
driver.execute_script('window.open("https://naver.com");')
time.sleep(1)
#원래 탭으로 이동
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)

""""
# 행정구역 가져오기 (from wiki)
wikiAdmDivisionURL = 'https://ko.wikipedia.org/wiki/'+goWhere+'_(부산광역시)'
driver.get(wikiAdmDivisionURL)

admDivisionElement = driver.find_element(By.CSS_SELECTOR,
        "div#mw-content-text > div.mw-parser-output").find_elements(By.XPATH,
            "//table[contains(@class, 'wikitable sortable jquery-tablesorter')]/tbody/tr/td/b/a")

admDivisionlist = []
for admDivisionInfo in admDivisionElement:
    admDivisionlist.append(admDivisionInfo.text)


for admDivision in admDivisionlist:
"""
kakaomapadmDivisionURL = 'http://map.kakao.com/?q=부산광역시%20'+goWhere+'%20'+admDivision+'%20음식점#'

driver.get(kakaomapadmDivisionURL)

#장소 더보기 클릭
moreElement = driver.find_element(By.ID,"info\\.search\\.place\\.more")
#error 발생시 이곳에 time.sleep(3)
actions.move_to_element(moreElement)
actions.click(moreElement)
actions.click(moreElement).perform()
time.sleep(3)

#끝인지 확인하는 버튼
nextButton = driver.find_element(By.ID,"info\\.search\\.page\\.next")
hasNext = "disabled" not in nextButton.get_attribute("class").split(" ")

page =1 

while hasNext:

    for i in range(1,6):
        time.sleep(2)
        
        while True:
            
            try:
                
                movePageButtonURL = "info\\.search\\.page\\.no"+str(i)
                movePageButton = driver.find_element(By.ID,movePageButtonURL)
                
                checkMovePageButton = "HIDDEN" in movePageButton.get_attribute("class").split(" ")
                if checkMovePageButton:
                    break
                actions.move_to_element(movePageButton)
                time.sleep(1)
                actions.click(movePageButton).perform()
                time.sleep(5)
                break
            except StaleElementReferenceException:
                continue
        
        if checkMovePageButton:
            break

        listElement = driver.find_elements(By.CSS_SELECTOR," ul#info\\.search\\.place\\.list > li")

        for item in listElement:
            store_html = item.get_attribute('innerHTML')
            store_info = BeautifulSoup(store_html, "html.parser")

            placeName = store_info.select('.head_item > .tit_name > .link_name')

            # 광고 제외
            if len(placeName) == 0:
                        continue 
    
            placeName = store_info.select('.head_item > .tit_name > .link_name')[0].text
            placeAddress = store_info.select('.info_item > .addr > p')[0].text
            placeHour = store_info.select('.info_item > .openhour > p > a')[0].text
            placeTel = store_info.select('.info_item > .contact > span')[0].text
            placeKakaoReviewPoint = store_info.select('.rating > .score > em')[0].text
            #휴무일로 저장되었을 경우
            if len(str(placeHour)) == 3:
                placeHour = "휴무일 "+placeHour

            #상세 검색
            placeMoreURL = store_info.select('.info_item > .contact > a')[0].attrs['href']
            #상세 검색하기위해 새 탭으로 이동
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
            
            #메뉴 크롤링
            driver.get(placeMoreURL)
            time.sleep(3)
            
            menuGroup = dict()

            menu = driver.find_elements(By.XPATH,"//div[contains(@id, 'mArticle')]/div[@data-viewid='menuInfo']/ul/li")
            for menuList in menu:
                menuHtml = menuList.get_attribute('innerHTML')
                menuInfo = BeautifulSoup(menuHtml, "html.parser")

                menuImgCheck = menuInfo.select('a > span > img')
                if len(menuImgCheck) !=0 :
                    menuImg = menuImgCheck[0].attrs["src"]
                else:
                    menuImg = None
                menuName = menuInfo.select('.info_menu > span.loss_word')[0].text
                menuPrice = menuInfo.select('.info_menu > em.price_menu')
                if len(menuPrice) == 0 :
                    continue
                menuPrice = menuPrice[0].text
                #print(menuName)
                #print(menuPrice)
                #print(menuImg)
                #print("="*20)
                menuKind = dict()
                menuKind["menuName"] = str(menuName)
                menuKind["menuPrice"] = str(menuPrice)
                menuKind["menuImg"] = str(menuImg)
                menuGroup[str(menuName)] = menuKind
            
            #가게 이미지 출력
            placeImg = driver.find_elements(By.XPATH,
                "//div[@data-viewid='photoSection']/div[contains(@class, 'photo_area')]/ul/li[contains(@class,'size_l')]/a")
            if len(placeImg) !=0:
                placeImg = placeImg[0].get_attribute('style')
                placeImgURL = re.search("\".+\"",placeImg).group(0).strip('"')

            #태그
            tag = driver.find_elements(By.XPATH,"//div[contains(@id, 'mArticle')]/div[@data-viewid='basicInfo']/div[@data-viewid='basicInfo']/div[contains(@class,'placeinfo_default')]/div[contains(@class,'location_detail')]/div[contains(@class,'txt_tag')]/span/a")
            placeTag  = ""
            for getTag  in tag:
                placeTag+= getTag.text+" " 

            #네이버 평점 크롤링
            searchURL = "https://map.naver.com/v5/search/"+placeName
            stopNum = 0
            for get in str(placeAddress).split():
                searchURL += "%20"+get
                if stopNum == 1:
                    break
                stopNum+=1

            driver.get(searchURL)
            time.sleep(3)
            driver.switch_to.frame("searchIframe")
            time.sleep(1)
            placeList = driver.find_elements(By.XPATH,"//li[@data-laim-exp-id='undefined']/div[contains(@class,'_3ZU00 _1rBq3')]/a/div/div/span[contains(@class,'_3Apve')]")
            if 1<len(placeList):
                time.sleep(3)
                try:
                    actions.click(placeList[0]).perform()
                    time.sleep(1)
                except StaleElementReferenceException:
                    pass
                
            driver.switch_to.default_content()
            time.sleep(1)
            #네이버 리뷰
            
            try:
                driver.switch_to.frame("entryIframe")
                placeMain = driver.find_element(By.XPATH,"//div[contains(@id,'app-root')]/div/div/div[contains(@class,'place_detail_wrapper')]")
                placeMainHtml = placeMain.get_attribute('innerHTML')
                placeMainInfo = BeautifulSoup(placeMainHtml,"html.parser")
                placeNaverReviewPoint = placeMainInfo.select("._1kUrA > span._1Y6hi._1A8_M > em")
                if len(placeNaverReviewPoint) == 0:
                    placeNaverReviewPoint = None
                else:
                    placeNaverReviewPoint = placeNaverReviewPoint[0].text
                time.sleep(2)
                #카카오에 메뉴가 없을 경우 네이버에서
                if len(menu) == 0:
                    naverMenuCrawling.naver(driver,menuGroup,placeName,actions,time)
                    
            except NoSuchFrameException:
                
                placeNaverReviewPoint = None

            
            #print(placeTag)
            #print(placeImgURL)
            #print(place_name)
            #print(place_address)
            #print(place_hour)
            #print(place_tel)
            #print(place_reviewPoint)
            #print("="*100)
            #print(placeNaverReviewPoint)
            StoreGroup = dict()
            StoreGroup["placeName"] = str(placeName)
            StoreGroup["placeAddress"] = str(placeAddress)
            StoreGroup["placeHour"] = str(placeHour)
            StoreGroup["placeTel"] = str(placeTel)
            StoreGroup["placeKakaoReviewPoint"] = str(placeKakaoReviewPoint)
            StoreGroup["placeNaverReviewPoint"] = str(placeNaverReviewPoint)
            StoreGroup["placeTag"] = str(placeTag)
            StoreGroup["placeImgURL"] = str(placeImgURL)
            StoreGroup["placeMenu"] = menuGroup

            JsonGroup[str(placeName)] = StoreGroup

            #원래 탭으로 돌아가기
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)

        #마지막 페이지(34page이면 멈추도록)
        if page  == 34 :
            break
            
        page += 1
    
    nextButton = driver.find_element(By.ID,"info\\.search\\.page\\.next")
    hasNext = "disabled" not in nextButton.get_attribute("class").split(" ")
    
    if not hasNext :
        print("crawling end")
        break
    else:
        while True:
            try:
                actions.move_to_element(nextButton)
                time.sleep(3)
                actions.click(nextButton).perform()
                time.sleep(3)
                break
            except StaleElementReferenceException:
                continue

time.sleep(5)
driver.close()

jsonFilename = admDivision+'.json'
with open(jsonFilename,'w',encoding='utf-8') as make_file:
    json.dump(JsonGroup, make_file,ensure_ascii = False,  indent="\t")

