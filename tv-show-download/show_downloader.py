import requests
import threading
import time
from queue import Queue


class show_downloader:
    def __init__(self):
        self.episode_urls = []
        self.episode_names = []
        self.q = Queue()
        self.number_of_thread = 5
        self.threads = []

    def join_threads(self):
        for t in self.threads:
            t.join()

    def create_threads(self):
        for _ in range(self.number_of_thread):
            t = threading.Thread(target=self.queue_manager)
            t.start()
            self.threads.append(t)

    def queue_put(self):
        for i in range(len(self.episode_urls)):
            self.q.put(i)

    def queue_empty(self):
        for _ in range(self.number_of_thread):
            self.q.put(None)

    def queue_manager(self):
        while True:
            current_episode = self.q.get()
            print("Queue size " + str(self.q.qsize()))
            time.sleep(0.1)
            print("Current episode " + str(current_episode))
            if current_episode is None:
                print(threading.enumerate())
                break
            print("Downloading " + str(current_episode) + " episode")
            self.download_from_url(self.episode_urls[current_episode], self.episode_names[current_episode])
            self.q.task_done()
            print("Episode " + str(current_episode) + " downloaded")

    def download_from_url(self, url, name):
            r = requests.get(url, stream=True)
            with open('D:/Script/' + name + '.mp4', 'wb') as f:
                f.write(r.content)
