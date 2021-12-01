import csv
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def excel_write(write_list, file_name):
    try:
        with open("collected_data/" + file_name, 'r+', newline='', encoding="ISO-8859-1", errors='ignore') as read_file:
            reader_writer = csv.reader((line.replace('\0', '') for line in read_file))
            if write_list not in reader_writer:
                with open("collected_data/" + file_name, 'a+', newline='', encoding="ISO-8859-1", errors='ignore') as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow(write_list)
                    f.close()
            else:
                return True
    except FileNotFoundError:
        f = open("collected_data/" + file_name, 'w+', newline='', encoding='utf-8', errors='ignore')
        f.close()
        excel_write(write_list, file_name)
    except Exception as e:
        print(e)


def get_author_link(li, split_by):
    s = Service(executable_path="C:/SeleniumDrivers/chromedriver.exe")
    driver1 = webdriver.Chrome(service=s)
    user_profile_links_lists = set()
    for i in li:
        driver1.get(i)
        By_word = driver1.find_elements(By.CLASS_NAME, "oc_Q_7bfac")
        for ij in By_word:
            split_str = str(ij.text).split(split_by)
            by_name = driver1.find_elements(By.LINK_TEXT, split_str[1])
            by_name_link = by_name[0].get_attribute('href')
            user_profile_links_lists.add(by_name_link)
    driver1.quit()
    return user_profile_links_lists


def page_loggers(log_name, text):
    logging.basicConfig(filename=f"logs/{log_name}.log", filemode="a", format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    l = logging.getLogger()
    l.setLevel(logging.INFO)
    l.info(text)
