from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import StaleElementReferenceException

def naver(driver,menuGroup,placeName,actions,time):
    menuButtton = driver.find_elements(By.XPATH,"//div[contains(@class,'place_fixed_maintab')]/div/div/div/div/a[@role='tab']/span")
    for i,val in enumerate(menuButtton):

        time.sleep(3)
        getButton = driver.find_elements(By.XPATH,"//div[contains(@class,'place_fixed_maintab')]/div/div/div/div/a[@role='tab']/span")[i]
        if str(getButton.text) == "메뉴":
            try:
                time.sleep(2)
                actions.click(getButton).perform()
                time.sleep(1)
                
                moreButtonOne = driver.find_elements(By.XPATH,"//a[contains(@class,'sc_extend_view')]")
                moreButtonTwo = driver.find_elements(By.XPATH,"//a[contains(@class,'_3iTUo')]")
                if len(moreButtonOne) != 0:
                    try:
                        for button in moreButtonOne:
                            actions.move_to_element(button)
                            time.sleep(1)
                            actions.click(button)
                    except StaleElementReferenceException:
                        pass
                elif len(moreButtonTwo) != 0:
                    try:
                        for button in moreButtonTwo:
                            actions.move_to_element(button)
                            time.sleep(1)
                            actions.click(button)
                    except StaleElementReferenceException:
                        pass
                #메뉴 가져오기
                NaverMenu = driver.find_element(By.TAG_NAME,"body")
                NaverMenuHtml = NaverMenu.get_attribute('innerHTML')
                NaverMenuInfo = BeautifulSoup(NaverMenuHtml,"html.parser")
                #종류가 3가지라서
                menuListOne = NaverMenuInfo.select("div.list_area > ul.list_place_col1 > div.list_item.type_menu")
                menuListTwo = NaverMenuInfo.select("div.place_section_content > ul._2yHts > li._3j-Cj")
                menuListThree = NaverMenuInfo.select("div.place_section_content > div.V3nwG > div._1G9dE")
                
                if len(menuListOne) != 0:
                    for getMenu in menuListOne:
                        menuName = getMenu.select("div.info_area > a.inner > div.tit.ellp2 > span.tit_inner > span")[0].text
                        menuPrice = getMenu.select("div.info_area > a.inner > div.price")
                        if len(menuPrice) !=0:
                            menuPrice = menuPrice[0].text
                        else:
                            menuPrice = None
                        menuImg = getMenu.select("a.thumb_area > div.thumb._item > img")
                        if len(menuImg) != 0:
                            menuImg = menuImg[0].attrs['src']
                        else:
                            menuImg  = None
                        
                        menuKind = dict()
                        menuKind["menuName"] = str(menuName)
                        menuKind["menuPrice"] = str(menuPrice)
                        menuKind["menuImg"] = str(menuImg)
                        menuGroup[str(menuName)] = menuKind
                        time.sleep(2)
                        #print(placeName)
                        #print(menuName)
                        #print(menuPrice)
                        #print(menuImg)
                        #print("="*20)
                elif len(menuListTwo) !=0:
                    for getMenu in menuListTwo:
                        
                        menuName = getMenu.select("a > div._2CZ7z > div._25ryC > div > span")[0].text
                        menuPrice = getMenu.select("a > div > div._3qFuX")
                        if len(menuPrice) != 0:
                            menuPrice = menuPrice[0].text
                        else:
                            menuPrice = None

                        #img 종류 2개
                        menuImgOne = getMenu.select("div._1H9RR > div.place_thumb._3BYTN > div")
                        menuImgTwo = getMenu.select("div._1H9RR > div.place_thumb > div")

                        if len(menuImgOne) !=0:
                            menuImg = menuImgOne[0].attrs['style']
                            menuImg = re.search("\".+\"",menuImg).group(0).strip('"')
                        
                        elif len(menuImgTwo) !=0:
                            menuImg = menuImgTwo[0].attrs['style']
                            menuImg = re.search("\".+\"",menuImg).group(0).strip('"')
                        
                        else:
                            menuImg  = None

                        
                        menuKind = dict()
                        menuKind["menuName"] = str(menuName)
                        menuKind["menuPrice"] = str(menuPrice)
                        menuKind["menuImg"] = str(menuImg)
                        menuGroup[str(menuName)] = menuKind
                        time.sleep(2)
                        #print(placeName)
                        #print(menuName)
                        #print(menuPrice)
                        #print(menuImg)
                        #print("="*20)
                elif len(menuListThree) != 0:
                    for getMenu in menuListThree:
                        menuName = getMenu.select("div._2ZgMX > span")[0].text
                        menuPrice = getMenu.select("div._3APi5 > span")
                        if len(menuPrice) !=0:
                            menuPrice  = menuPrice[0].text
                        else:
                            menuPrice = None
                        menuImg = None
                        
                        menuKind = dict()
                        menuKind["menuName"] = str(menuName)
                        menuKind["menuPrice"] = str(menuPrice)
                        menuKind["menuImg"] = str(menuImg)
                        menuGroup[str(menuName)] = menuKind
                        time.sleep(2)
                        #print(placeName)
                        #print(menuName)
                        #print(menuPrice)
                        #print(menuImg)
                        #print("="*20)
                else:
                    print(placeName)
                
            except StaleElementReferenceException:
                print(placeName)
                print("*"*20)
                time.sleep(2)
                pass
            break