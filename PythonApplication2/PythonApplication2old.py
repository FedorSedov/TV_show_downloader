
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

path_to_extension = r'C:\Program Files (x86)\3.10.1_0'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver.create_options()
driver.get("https://m.anwap.bio/serials/down/33649")
curWindowHndl = driver.current_window_handle
driver.switch_to_window(driver.window_handles[1])
driver.close() #closes new tab
driver.switch_to_window(curWindowHndl)
overall_seasons = 0
current_season = 0

def episode_loop():
    a=1
    while a == 1:
        try:
            element_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "blm"))
            )
            head = element_list[0].find_element_by_class_name("serialnav")
        
    
            if "Следующая" in head.text:
                download_links = element_list[1].find_elements_by_xpath("//ul[@class='tlsiconkoi']/li")
                time.sleep(1)
                download_links[len(download_links)-1].click()
                head_next = head.find_element_by_xpath("//img[@src='/style/img/sright.png']")
                time.sleep(1)
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

def start_download_process(current_season, overall_seasons):
    while current_season < overall_seasons:
            season = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
            )
            season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
            season_list[current_season].click()
            download_season(current_season)
            current_season = current_season + 1
    return current_season

def start_download_process_from1(current_season, overall_seasons):
    season_list[current_season].click()
    download_season(current_season)
    return 1

def download_episode(episode):
    episode.click()
    chwd = driver.window_handles
    p = driver.current_window_handle
    #print(chwd)
    #print(p)
    #time.sleep(3)
    for w in chwd:
        if(w!=p)and len(chwd)>1:

            driver.switch_to.window(w)
    episode_loop()

            
    


def download_season(cur_season):
    try:
        list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blm"))
        )
        first_episode = list.find_element_by_xpath("//ul[@class='tl']/li")
        #print(len(episode_list))
        #for episode in episode_list:
        download_episode(first_episode)

    except Exception as inst:
        print("Exception caught season page")
        print(inst)
        driver.quit()

try:
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
                    print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
                    driver.quit()
                except Exception as inst:
                    print("Exception caught in 1st try")
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
                    print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
                    driver.quit()

            except Exception as inst:
                print("Exception caught in 3st try")
                print(inst)
                driver.quit()

    
    

        #driver.quit()
    except Exception as inst:
        print("Exception caught in 1st try")
        print(inst)
        driver.quit()



    
