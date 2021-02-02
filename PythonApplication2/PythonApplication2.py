
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import warnings
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

path_to_extension = r'C:\Program Files (x86)\3.10.1_0'
chrome_options = Options()

# Прячем ошибки браузера из консоли
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('load-extension=' + path_to_extension)

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver.create_options()
warnings.filterwarnings("ignore") # Игнорим предупреждения
driver.get("https://google.com")
curWindowHndl = driver.current_window_handle
driver.switch_to_window(driver.window_handles[1])
driver.close() # Закрываем окно Адблока
driver.switch_to_window(curWindowHndl)
overall_seasons = 0
current_season = 0
print("Введите название сериала")
show = input()
search = driver.find_element_by_name("q")
search.clear()
search.send_keys("site:m.anwap.bio/serials " +"'"+show+"'")
search.send_keys(Keys.RETURN)

def every_downloads_chrome(driver): # Функция по ожиданию окончания всех загрузок
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

def episode_loop(): # Скачиваем все серии начиная с 1
    a=1
    while a == 1:
        try:
            element_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "blm"))
            )
            head = element_list[0].find_element_by_class_name("serialnav")
        
    
            if "Следующая" in head.text:
                download_links = element_list[1].find_elements_by_xpath("//ul[@class='tlsiconkoi']/li")
                #time.sleep(1)
                download_links[len(download_links)-1].click()
                head_next = head.find_element_by_xpath("//img[@src='/style/img/sright.png']")
                #time.sleep(1)
                head_next.click()
            else:
                a=0
                download_links = element_list[1].find_elements_by_xpath("//ul[@class='tlsiconkoi']/li")
                download_links[len(download_links)-1].click()
                footer = driver.find_element_by_xpath("//img[@src='/style/img/vernutca.png']")
                footer.click()
                try:
                    footer2 = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "menuniz"))
                    )
                    footer2 = driver.find_element_by_xpath("//img[@src='/style/img/vernutca.png']")
                    footer2.click()
                except Exception as inst:
                    print("Exception caught episode")
                    print(inst)
                    driver.quit()
        
        except Exception as inst:
            print("Exception caught episode")
            print(inst)
            driver.quit()

def start_download_process(current_season, overall_seasons): # Начинаем процесс скачивания
    while current_season < overall_seasons:
            season = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
            )
            season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
            season_list[current_season].click()
            download_season(current_season)
            current_season = current_season + 1
    return current_season

#def download_episode(episode):
#    episode.click()
#    chwd = driver.window_handles
#    p = driver.current_window_handle
    #print(chwd)
    #print(p)
    #time.sleep(3)
#    for w in chwd:
#        if(w!=p)and len(chwd)>1:
#
#            driver.switch_to.window(w)
#    episode_loop()
          

def download_season(cur_season): #Запуск процесса скачивания первой серии
    try:
        list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blm"))
        )
        first_episode = list.find_element_by_xpath("//ul[@class='tl']/li")
        #print(len(episode_list))
        #for episode in episode_list:
        #download_episode(first_episode)
        first_episode.click()
        episode_loop()

    except Exception as inst:
        print("Exception caught season page")
        print(inst)
        driver.quit()


try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    results = main.find_elements_by_class_name("tF2Cxc")
    #for result in results:
    #    print(result.text)
    
    link = results[0].find_element_by_class_name("yuRUbf")
    link.click()
    if "anwap.bio/serials/comm/" in driver.current_url:
        parsed_url = driver.current_url.split("/")
        parsed_url.remove('comm')
        if parsed_url[-1].isdigit() and parsed_url[-2].isdigit():
            del parsed_url[-1]
        target_url = '/'.join(parsed_url)
        #final_url = "window.open('"+ target_url +"');"
        print(target_url)
        #time.sleep(5)
        #driver.execute_script(final_url)
        driver.get(target_url)
        driver.get(target_url)
                
                #driver.get(target_url)

                #footer2 = WebDriverWait(driver, 10).until(
                #EC.presence_of_element_located((By.CLASS_NAME, "menuniz"))
                #)
                #footer = footer2.find_element_by_xpath("//img[@src='/style/img/back.png']")
                #footer = footer2.find_element_by_xpath("//a[@href='/serials/1138']")
                #offset_top = footer.get_attribute('offsetTop')
                #offset_width = footer.get_attribute('offsetWidth')
                #print(offset_top)
                #print(offset_width)
                #print(footer.text)
                #footer.click()
                #time.sleep(10)

    try:
        season = None
        season = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
        )
    finally:
        try:
            blm_check = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "blm"))
            )
        
            if season is not None and "Сезоны:" in season.text:
                season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
                overall_seasons = len(season_list)
                current_season = 0
                #print(overall_seasons)
                start_download_process(current_season, overall_seasons)
                WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
                print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
                driver.quit()
            elif len(blm_check)==1:
                if blm_check[0].text.find("1 сезон") != -1:
                    print(blm_check[0].text)
                    download_season(0)
                    current_season = 1
                    season = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
                    )
                    season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
                    overall_seasons = len(season_list)
                    start_download_process(current_season, overall_seasons)
                    WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
                    print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
                    driver.quit()
                else:
                    try:
                        footer2 = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "menuniz"))
                        )
                        footer2 = driver.find_element_by_xpath("//img[@src='/style/img/vernutca.png']")
                        footer2.click()
                        season = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
                        )
                        season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
                        overall_seasons = len(season_list)
                        current_season = 0
                        start_download_process(current_season, overall_seasons)
                        WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
                        print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
                        driver.quit()
                    except Exception as inst:
                        print("Exception caught in not 1st season page")
                        print(inst)
                        driver.quit()
            elif len(blm_check)==2:
                try:
                    Description = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "blm"))
                    )
                    Description_list = Description.find_elements_by_xpath("//tbody/tr/td")
                    lenght = len(Description_list)
                    counter = 0
                    i = 0
                    while i < lenght and counter <2:
                        print(Description_list[i].text + Description_list[i+1].text)
                        if ("Сезон" in Description_list[i].text and "1" in Description_list[i+1].text) or ("Серия" in Description_list[i].text and "1" in Description_list[i+1].text):
                            print(Description_list[i].text + Description_list[i+1].text)
                            counter = counter + 1
                        i = i + 2
                    if counter == 2:
                        episode_loop()
                        current_season = 1
                        season = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
                        )
                        season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
                        overall_seasons = len(season_list)
                        start_download_process(current_season, overall_seasons)
                        WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
                        print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
                        driver.quit()
                    elif counter != 2:
                        footer = driver.find_element_by_xpath("//img[@src='/style/img/vernutca.png']")
                        footer.click()
                        time.sleep(1)
                        footer2 = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "menuniz"))
                        )
                        footer2 = driver.find_element_by_xpath("//img[@src='/style/img/vernutca.png']")
                        footer2.click()
                        season = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
                        )
                        season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
                        overall_seasons = len(season_list)
                        current_season = 0
                        #print(overall_seasons)
                        start_download_process(current_season, overall_seasons)
                        WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
                        print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
                        driver.quit()

                except Exception as inst:
                    print("Exception caught in 3rd try")
                    print(inst)
                    driver.quit()

    
    

            #driver.quit()
        except Exception as inst:
            print("Exception caught in 2nd try")
            print(inst)
            driver.quit()

except Exception as inst:
    print("Exception caught in 1st try")
    print(inst)
    driver.quit()
