from selenium.webdriver.common.keys import Keys
import requests
from queue import Queue
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


episode_urls = []
episode_names = []
number_of_thread = 5
q = Queue()
threads = []

def get_urls():
    return episode_urls

def get_names():
    return episode_urls


def join_thread():
    for t in threads:
        t.join()


def join_queue():
    q.join()


def create_threads():
    for _ in range(number_of_thread):
        t = threading.Thread(target=queue_manager)
        t.start()
        threads.append(t)
    return threads


def queue_put():
    for i in range(len(episode_urls)):
        q.put(i)


def queue_empty():
    for i in range(number_of_thread):
        q.put(None)


def queue_manager():
    while True:
        current_episode = q.get()
        print("Queue size " + str(q.qsize()))
        time.sleep(0.1)
        print("Current episode " + str(current_episode))

        if current_episode is None:
            #q.task_done()
            print(threading.enumerate())
            break
        print("Downloading " + str(current_episode) + " episode")
        download_from_url(episode_urls[current_episode], episode_names[current_episode])
        q.task_done()
        print("Episode " + str(current_episode) + " downloaded")
        #if q.empty():
        #    print(threading.enumerate())
        #    break


def download_from_url(url, name):
        r = requests.get(url)
        #filename = get_filename_from_cd(r.headers.get('content-disposition'))
        with open('D:/Script/' + name + '.mp4', 'wb') as f:
            f.write(r.content)
'''
def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    print(fname)
    if len(fname) == 0:
        return None
    return fname[0]
'''

def download_best_quality(element_list):
    download_links = element_list[1].find_elements_by_xpath("//ul[@class='tlsiconkoi']/li")
    download_links[len(download_links)-1].click()


def save_link_to_list(driver, element_list):
    download_links = element_list[1].find_elements_by_xpath("//ul[@class='tlsiconkoi']/li/a")
    episode_urls.append(download_links[-1].get_attribute('href'))
    episode_names.append(driver.find_element_by_class_name('ball').text)

def wait_season_page_load_and_gather_list(driver):
    try:
        season = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
        )
    except Exception as inst:
        print("Exception in function wait_season_page_load_and_gather_list. Error loading Show page")
        print(inst)

    season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
    return season_list


def previous_page(driver):
    try:
        footer = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "menuniz"))
        )
    except Exception as inst:
        print("Exception in function previous_page. Cant find back button")
        print(inst)
    try:
        button = driver.find_element_by_xpath("//img[@src='/style/img/vernutca.png']")
        button.click()
    except Exception as inst:
        pass


def define_opened_page_go_to_seasons_page(driver):
    if "anwap.bio/serials/comm/" in driver.current_url:
        parsed_url = driver.current_url.split("/")
        parsed_url.remove('comm')
        if parsed_url[-1].isdigit() and parsed_url[-2].isdigit():  # Сheck if we are not on 1st page of comments
            del parsed_url[-1]  # Delete page id from ult

        target_url = '/'.join(parsed_url)
        driver.get(target_url)
        driver.get(target_url)
    try:
        blm_check = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "blm"))
        )
    except Exception as inst:
        print("Exception in function define_opened_page_go_to_seasons_page. Couldn't find elemebt on page. Passable")
        print(inst)
        pass

    if len(blm_check)==1:  # Go to shows page
        previous_page(driver)
    else:
        for i in range(2):
            previous_page(driver)


def find_and_click_search_results(driver, main):
    results = main.find_elements_by_class_name("tF2Cxc")
    link = results[0].find_element_by_class_name("yuRUbf")
    link.click()


def search_and_wait_results(driver, show):
    search = driver.find_element_by_name("q")
    search.clear()
    search.send_keys("site:m.anwap.bio/serials " +"'"+show+"'")
    search.send_keys(Keys.RETURN)
    try:
        main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
        )
        return main
    except Exception as inst:
        print("Exception in function search_and_wait_results. Google page didnt open in time")
        print(inst)


def close_adblock(driver):
    curWindowHndl = driver.current_window_handle
    driver.switch_to_window(driver.window_handles[1])
    driver.close()
    driver.switch_to_window(curWindowHndl)


def wait_downloads_to_finish(driver):
    WebDriverWait(driver, 300, 1).until(every_downloads_chrome(driver))


def every_downloads_chrome(driver):  #  Function to wait for all downloads to finish
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)


def episode_loop(driver):  # Download all episodes starting from 1
    while True:
        try:
            element_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "blm"))
            )
            head = element_list[0].find_element_by_class_name("serialnav")
        except Exception as inst:
            print("Exception in function episode_loop. Couldn't load page")
            print(inst)

        if "Следующая" in head.text:
            #download_best_quality(element_list)
            save_link_to_list(driver, element_list)
            head_next = head.find_element_by_xpath("//img[@src='/style/img/sright.png']")
            head_next.click()
        else:
            save_link_to_list(driver, element_list)
            #download_best_quality(element_list)
            for i in range(2):
                previous_page(driver)
            break

        

def start_download_process(driver): 
    season_list = wait_season_page_load_and_gather_list(driver)
    current_season = 0
    overall_seasons = len(season_list)
    while current_season < overall_seasons:
        season_list = wait_season_page_load_and_gather_list(driver)
        season_list[current_season].click()
        download_season(driver)
        current_season = current_season + 1
    

def download_season(driver): 
    try:
        list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blm"))
        )
        first_episode = list.find_element_by_xpath("//ul[@class='tl']/li")
        first_episode.click()
        episode_loop(driver)

    except Exception as inst:
        print("Exception in function download_season. Couldn't load page")
        print(inst)