import func

print("Введите название сериала")
show = input()

print("Какой сайт выбрать для скачки ( 1-anwap | 2-zetflix ) ")
site = input()

downloader = func.show_downloader()
if int(site) == 1:
    anwap_downloader = downloader.show_downloader_anwap(show)
    main = anwap_downloader.search_and_wait_results()
    anwap_downloader.find_and_click_search_results(main)
    anwap_downloader.define_opened_page_go_to_seasons_page()
    anwap_downloader.start_download_process()
    downloader.episode_urls = anwap_downloader.return_urls()
    downloader.episode_names = anwap_downloader.return_names()
    driver = anwap_downloader.driver
else:
    zetflix_downloader = downloader.show_downloader_zetflix(show)
    zetflix_downloader.open_site()
    zetflix_downloader.find_searchbar()
    zetflix_downloader.click_show()
    zetflix_downloader.prepare_download_links()
    downloader.episode_urls = zetflix_downloader.return_urls()
    downloader.episode_names = zetflix_downloader.return_names()
    driver = zetflix_downloader.driver
try:
    downloader.create_threads()
    downloader.queue_put()
    downloader.q.join()
    print("Exited Queue")
    downloader.queue_empty()
    downloader.join_threads()
except Exception as inst:
        print("Exception during download process")
        print(inst)
else:
    print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
finally:
    driver.quit()
