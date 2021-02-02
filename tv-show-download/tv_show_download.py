
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import warnings
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import func

path_to_extension = r'C:\Program Files (x86)\3.10.1_0'
chrome_options = Options()
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Прячем ошибки браузера из консоли
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('load-extension=' + path_to_extension)
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver.create_options()
warnings.filterwarnings("ignore") # Игнорим предупреждения

driver.get("https://google.com")
func.close_adblock(driver)
print("Введите название сериала")
show = input()
main = func.search_and_wait_results(driver, show)
func.find_and_click_search_results(driver, main)
func.define_opened_page_go_to_seasons_page(driver)
func.start_download_process(driver)
try:
    WebDriverWait(driver, 300, 1).until(func.every_downloads_chrome)
except Exception as inst:
        print("Exception during download process. Download timeout")
        print(inst)
else:
    print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
finally:
    driver.quit()
