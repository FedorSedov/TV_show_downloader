
from selenium import webdriver
import warnings
from queue import Queue
import threading
from selenium.webdriver.chrome.options import Options
import func
import time
import requests


def queue_manager():
    episode_name = 1
    while True:
        episode_name += 1
        current_episode = q.get()
        print("Queue size " + str(q.qsize()))
        time.sleep(0.1)
        print("Current episode " + str(current_episode))

        if current_episode is None:
            #q.task_done()
            print(threading.enumerate())
            break
        print("Downloading " + str(current_episode) + " episode")
        download_from_url(episode_urls[current_episode], episode_name)
        q.task_done()
        print("Episode " + str(current_episode) + " downloaded")
        #if q.empty():
        #    print(threading.enumerate())
        #    break

def download_from_url(url, t):
    r = requests.get(url)
    # filename = get_filename_from_cd(r.headers.get('content-disposition'))
    with open('D:/Script/' + str(t) + '.mp4', 'wb') as f:
        f.write(r.content)


path_to_extension = r'C:\Program Files (x86)\3.10.1_0'
chrome_options = Options()
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Hide browser errors from console
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('load-extension=' + path_to_extension)
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver.create_options()
warnings.filterwarnings("ignore") # Ignore warnings

driver.get("https://google.com")
func.close_adblock(driver)
print("Введите название сериала")
show = input()
main = func.search_and_wait_results(driver, show)
func.find_and_click_search_results(driver, main)
func.define_opened_page_go_to_seasons_page(driver)
func.start_download_process(driver)

number_of_thread = 5
q = Queue()
threads = []

episode_urls = func.get_urls()
episode_names = func.get_names()

for _ in range(number_of_thread):
    t = threading.Thread(target=queue_manager)
    t.start()
    threads.append(t)

for i in range(len(episode_urls)):
    q.put(i)

q.join()

for i in range(number_of_thread):
    q.put(None)

for t in threads:
    t.join()



