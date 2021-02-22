
from selenium import webdriver
import warnings
from queue import Queue
import threading
from selenium.webdriver.chrome.options import Options
import func

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


try:
    func.create_threads()
    print(threading.enumerate())
    func.queue_put()
    func.queue_manager()
    func.join_queue()
    print("Exited Queue")
    print(threading.enumerate())
    func.queue_empty()
    func.join_thread()


except Exception as inst:
        print("Exception during download process")
        print(inst)
else:
    print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
    threading.enumerate()
finally:
    driver.quit()
