from show_downloader_zetflix import show_downloader_zetflix
from show_downloader_anwap import show_downloader_anwap

if __name__ == "__main__":
    print("Введите название сериала")
    show = input()

    print("Какой сайт выбрать для скачки ( 1-anwap | 2-zetflix ) ")
    site = input()

    if int(site) == 1:
        downloader = show_downloader_anwap(show)
    else:
        downloader = show_downloader_zetflix(show)

    driver = downloader.gather_list_to_download()
    try:
        downloader.start()
    except Exception as inst:
            print("Exception during download process")
            print(inst)
    else:
        print("JOB DONE!!!!!!!!!!!!!!!!!!!!!!!")
    finally:
        driver.quit()
