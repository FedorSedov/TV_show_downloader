from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
from selenium.webdriver.chrome.options import Options
from show_downloader import show_downloader


class show_downloader_zetflix(show_downloader):
    def __init__(self, show):
        super().__init__()
        self.show = show
        self.driver = self.chromedriver()
        self.episode_urls = []
        self.episode_names = []

    def gather_list_to_download(self):
        self.open_site()
        self.find_searchbar()
        self.click_show()
        self.prepare_download_links()
        driver = self.driver
        return driver

    def chromedriver(self):
        # path_to_extension = r'C:\Program Files (x86)\3.10.1_0'
        chrome_options = Options()
        # chrome_options.headless = True
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        chrome_options.add_argument("--log-level=3")
        driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
        driver.create_options()
        warnings.filterwarnings("ignore")  # Ignore warnings
        return driver

    def close_popup(self):
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to_window(handles[1])
            self.driver.close()
            # self.driver.switch_to_window(handles[0])

    def open_site(self):
        self.driver.get('https://hd.zetflix.online/search.html?do=search')
        print("Site opened")

    def find_searchbar(self):
        try:
            searchbar = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "textin"))
            )
            print("Searchbar found")
            searchbar.clear()
            print("Searchbar cleared")
            searchbar.send_keys(self.show)
            print("Searchbar populated")
            searchbar.send_keys(Keys.RETURN)
            print("Searchbar send")
        except Exception as inst:
            print("Exception in function find_searchbar. Error loading search page")

    def click_show(self):
        try:
            found_show = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sres-img"))
            )
            print('Show found')
            found_show.click()
            print('Show clicked')
        except Exception as inst:
            print("Exception in function click_show. Error loading search results page")

    def save_episode_name(self):
        try:
            player = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ftitle"))
            )
            textbar = self.driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[1]")
            episode_name = textbar.text.split("»")
            self.episode_names.append(episode_name[-1])
        except:
            print('Exception in function save_episode_name. Error loading show page')

    def save_episode_download_link(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '//div[@class="tabs-b video-box visible"]/iframe')))
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//div[@id="playnd"]/iframe')))
            self.wait_element_and_get_content()
            textContent = self.wait_element_and_get_content()
            while textContent == 'Loading error':
                textContent = self.wait_element_and_get_content()
            if 'hdvideobox' in textContent:
                self.convert_to_download_link_p(textContent)
            else:
                self.convert_to_download_link(textContent)
            print(self.episode_urls)
        except:
            print('Exception in function save_episode_download_link. Error loading show page')

    def find_and_click_next(self):
        try:
            self.driver.switch_to.default_content()
            next = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='pright']/a"))
            )
            nextlink = next.get_attribute('href')
            if nextlink:
                return nextlink
            else:
                print('None')
                return None
        except:
            print('Exception in function find_and_click_next. Error loading show page')
            return None

    def prepare_download_links(self):
        self.driver.get(str(self.driver.current_url) + 'season-01-episode-01/')
        while True:
            self.save_episode_name()
            self.save_episode_download_link()
            nextlink = self.find_and_click_next()
            print(nextlink)
            if nextlink:
                self.driver.get(str(nextlink))
            else:
                break

    def wait_element_and_get_content(self):
        try:
            text_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/script"))
            )
            text_content = text_element.get_attribute('textContent')
            return text_content
        except Exception as inst:
            print("Exception in function wait_element_and_get_content. Error loading show page")
            self.driver.get(self.driver.current_url)
            return 'Loading error'

    def convert_to_download_link_p(self, textContent):
        start = textContent.find("[360p]") + len("[360p]")
        end = textContent.find(",[480p]")
        substring = textContent[start:end]
        download_link = substring.split('/')
        download_link_substring = download_link[-1].split('.')
        download_link_substring.remove('m3u8')
        download_link_substring.append('mp4')
        download_link_substring = '.'.join(download_link_substring)
        download_link[-1] = download_link_substring
        download_link = '/'.join(download_link)
        self.episode_urls.append(download_link)

    def convert_to_download_link(self, textContent):
        start = textContent.find("[360]") + len("[360]")
        end = textContent.find(",[480]")
        substring = textContent[start:end]
        self.episode_urls.append(substring)

    def return_urls(self):
        return self.episode_urls

    def return_names(self):
        return self.episode_names