from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
from selenium.webdriver.chrome.options import Options
from show_downloader import show_downloader


class show_downloader_anwap(show_downloader):
    def __init__(self, show):
        super().__init__()
        self.show = show
        self.driver = self.chromedriver()
        self.episode_urls = []
        self.episode_names = []

    def gather_list_to_download(self):
        main = self.search_and_wait_results()
        self.find_and_click_search_results(main)
        self.define_opened_page_go_to_seasons_page()
        self.start_download_process()
        driver = self.driver
        return driver

    def chromedriver(self):
        path_to_extension = r'C:\Program Files (x86)\3.10.1_0'
        chrome_options = Options()
        #chrome_options.headless = True
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        # Hide browser errors from console
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument('load-extension=' + path_to_extension)
        driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
        driver.create_options()
        warnings.filterwarnings("ignore")  # Ignore warnings
        return driver

    def download_best_quality(self, element_list):
        download_links = element_list[1].find_elements_by_xpath("//ul[@class='tlsiconkoi']/li")
        download_links[len(download_links) - 1].click()

    def save_link_to_list(self, element_list):
        download_links = element_list[1].find_elements_by_xpath("//ul[@class='tlsiconkoi']/li/a")
        self.episode_urls.append(download_links[-1].get_attribute('href'))
        self.episode_names.append(self.driver.find_element_by_class_name('ball').text)
        print(self.episode_names)

    def wait_season_page_load_and_gather_list(self):
        try:
            season = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "blc2"))
            )
            season_list = season.find_elements_by_xpath("//ul[@class='tl2']/li")
            return season_list
        except Exception as inst:
            print("Exception in function wait_season_page_load_and_gather_list. Error loading Show page")
            print(inst)

    def previous_page(self):
        try:
            footer = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "menuniz"))
            )
            button = self.driver.find_element_by_xpath("//img[@src='/style/img/vernutca.png']")
            button.click()
        except Exception as inst:
            print("Exception in function previous_page. Cant find back button")
            print(inst)
            pass

    def define_opened_page_go_to_seasons_page(self):
        if "anwap.bio/serials/comm/" in self.driver.current_url:
            parsed_url = self.driver.current_url.split("/")
            parsed_url.remove('comm')
            if parsed_url[-1].isdigit() and parsed_url[-2].isdigit():  # Сheck if we are not on 1st page of comments
                del parsed_url[-1]  # Delete page id from ult

            target_url = '/'.join(parsed_url)
            self.driver.get(target_url)
            self.driver.get(target_url)
            print("Comment -> Show page transition completed")
        try:
            blm_check = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "blm"))
            )
            if len(blm_check) == 1:  # Go to shows page
                self.previous_page()
                print("Show page transition completed")
            else:
                for _ in range(2):
                    self.previous_page()
                print("Show page transition completed")
        except Exception as inst:
            print(
                "Exception in function define_opened_page_go_to_seasons_page. Couldn't find element on page. Passable")
            print(inst)

    def find_and_click_search_results(self, main):
        results = main.find_elements_by_class_name("tF2Cxc")
        link = results[0].find_element_by_class_name("yuRUbf")
        link.click()
        print("Link clicked")

    def search_and_wait_results(self):
        self.driver.get("https://google.com")
        search = self.driver.find_element_by_name("q")
        search.clear()
        search.send_keys("site:n.anwap.bio/serials " + "'" + self.show + "'")
        search.send_keys(Keys.RETURN)
        try:
            main = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "main"))
            )
            print("Search completed")
            return main
        except Exception as inst:
            print("Exception in function search_and_wait_results. Google page didnt open in time")
            print(inst)

    def close_popup(self):
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.close()
            self.driver.switch_to_window(handles[1])

    def view_popup(self):
        print(self.driver.window_handles)
        print(self.driver.current_window_handle)

    def wait_downloads_to_finish(self):
        WebDriverWait(self.driver, 300, 1).until(self.every_downloads_chrome())

    def every_downloads_chrome(self):  # Function to wait for all downloads to finish
        if not self.driver.current_url.startswith("chrome://downloads"):
            self.driver.get("chrome://downloads/")
        return self.driver.execute_script("""
            var items = document.querySelector('downloads-manager')
                .shadowRoot.getElementById('downloadsList').items;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """)

    def episode_loop(self):  # Download all episodes starting from 1
        while True:
            try:
                element_list = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "blm"))
                )
                head = element_list[0].find_element_by_class_name("serialnav")
                if "Следующая" in head.text:
                    # download_best_quality(element_list)
                    self.save_link_to_list(element_list)
                    head_next = head.find_element_by_xpath("//img[@src='/style/img/sright.png']")
                    head_next.click()
                else:
                    self.save_link_to_list(element_list)
                    # download_best_quality(element_list)number_of_thread
                    for i in range(2):
                        self.previous_page()
                    break
            except Exception as inst:
                print("Exception in function episode_loop. Couldn't load page")
                print(inst)

    def start_download_process(self):
        season_list = self.wait_season_page_load_and_gather_list()
        current_season = 0
        overall_seasons = len(season_list)
        while current_season < overall_seasons:
            season_list = self.wait_season_page_load_and_gather_list()
            season_list[current_season].click()
            print("Season clicked")
            self.download_season()
            current_season = current_season + 1

    def download_season(self):
        self.close_popup()
        try:
            episode_list = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "blm"))
            )
            first_episode = episode_list.find_element_by_xpath("//ul[@class='tl']/li")
            first_episode.click()
            self.episode_loop()
        except Exception as inst:
            print("Exception in function download_season. Couldn't load page")
            print(inst)

    def return_urls(self):
        return self.episode_urls

    def return_names(self):
        return self.episode_names