import re
from itertools import chain
from time import ctime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from utils import get_author_link, excel_write, page_loggers


def about_and_description(link, file_name, link_file_name):
    global author_name
    s = Service(executable_path="C:/SeleniumDrivers/chromedriver.exe")
    driver1 = webdriver.Chrome(service=s)
    for count, link in enumerate(link):
        about_link = str(link).replace('/video', '/about')
        driver1.get(about_link)
        status = excel_write(write_list=[str(about_link).removeprefix("https://")], file_name=link_file_name)
        if status:
            continue

        author_name_list = set()

        try:
            author_name = driver1.find_element(By.CLASS_NAME, 'u_a_a9083').text
        except NoSuchElementException:
            print(link)

        author_name_list.add(author_name)
        social_media_links_list = []
        social_media_links = driver1.find_elements(By.CLASS_NAME, "u_b_96ed0")
        if social_media_links:
            [social_media_links_list.append(item.get_attribute('href')) for item in social_media_links]
        else:
            social_media_links_list.append("None")

        while len(social_media_links_list) < 5:
            social_media_links_list.append("None")

        description = driver1.find_elements(By.CLASS_NAME, "aa_a_15778")
        about_list = [str(j.text).replace('\n', ' ') for j in description]
        d = driver1.find_elements(By.CLASS_NAME, "aa_e_e2ec7")
        separated_h2_btns = [re.findall(r'[A-Z][^A-Z]*', str(t.text).replace("\n", ' ')) for t in d]

        if len(separated_h2_btns) == 4:
            styles = [' '.join([str(elem) for elem in separated_h2_btns[0]])]
            subject = [' '.join([str(elem) for elem in separated_h2_btns[1]])]
            equipment = [' '.join([str(elem) for elem in separated_h2_btns[2]])]
            other = [' '.join([str(elem) for elem in separated_h2_btns[3]])]
            final_list = list(
                chain(list(author_name_list), social_media_links_list, about_list, styles, subject, equipment, other))
            excel_write(final_list, file_name)

        elif len(separated_h2_btns) == 3:
            styles = [' '.join([str(elem) for elem in separated_h2_btns[0]])]
            subject = [' '.join([str(elem) for elem in separated_h2_btns[1]])]
            equipment = [' '.join([str(elem) for elem in separated_h2_btns[2]])]
            final_list = list(
                chain(list(author_name_list), social_media_links_list, about_list, styles, subject, equipment))
            excel_write(final_list, file_name)

        elif len(separated_h2_btns) == 2:
            styles = [' '.join([str(elem) for elem in separated_h2_btns[0]])]
            subject = [' '.join([str(elem) for elem in separated_h2_btns[1]])]
            final_list = list(
                chain(list(author_name_list), social_media_links_list, about_list, styles, subject))
            excel_write(final_list, file_name)

        elif len(separated_h2_btns) == 1:
            styles = [' '.join([str(elem) for elem in separated_h2_btns[0]])]
            final_list = list(
                chain(list(author_name_list), social_media_links_list, about_list, styles))
            excel_write(final_list, file_name)

        else:
            final_list = list(
                chain(list(author_name_list), social_media_links_list, about_list))
            excel_write(final_list, file_name)

        print(count, "ith Iteration Completed", ctime())
        author_name_list.clear()
        social_media_links_list.clear()
        about_list.clear()
    driver1.quit()
    return


def footage_links_lists(url, file_name, log_name, link_file_name):
    s = Service(executable_path="C:/SeleniumDrivers/chromedriver.exe")
    driver1 = webdriver.Chrome(service=s)
    link_lists = []
    base_url = url
    while base_url is not None:
        if "page" in url:
            page = re.findall(r'\d+', base_url)
            print(f"{page[0]} Page Start", ctime())
            page_loggers(log_name, f"{page[0]} Page Started")
        else:
            print(f"{base_url} Page Start", ctime())
            page_loggers(log_name, f"{base_url} Page Started")

        driver1.get(base_url)

        chosen_footage = driver1.find_elements(By.CLASS_NAME, "z_k_6cd44")
        for a in chosen_footage:
            single_footage = a.find_elements(By.CLASS_NAME, "k_a_48274")
            for ab in single_footage:
                link = ab.find_elements(By.TAG_NAME, "a")
                for b in link:
                    l = b.get_attribute('href')
                    link_lists.append(l)

        get_name_lists = get_author_link(link_lists, "By\n")
        link_lists.clear()

        print("Author Links Fetched : ", ctime())

        about_and_description(get_name_lists, file_name=file_name, link_file_name=link_file_name)
        get_name_lists.clear()
        if "page" in url:
            page = re.findall(r'\d+', url)
            print(f"{page[0]} Page completed", ctime())
            page_loggers(log_name, f"{page[0]} Page completed")
        else:
            print(f"{url} Page completed", ctime())
            page_loggers(log_name, f"{url} Page completed")

        links = driver1.find_element(By.CLASS_NAME, 'z_b_6e283')
        url = links.get_attribute('href')
        if base_url == url:
            base_url = None
        else:
            base_url = url
    driver1.close()
    return 0


print("START : ", ctime())

lists = footage_links_lists(url="https://www.shutterstock.com/video/search/aerial-community?page=101",
                            file_name="aerial-community.csv", log_name="aerial-community",
                            link_file_name="aerial-community-links.csv")
