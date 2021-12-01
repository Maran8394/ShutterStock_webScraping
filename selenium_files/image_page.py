import re
from itertools import chain
from time import ctime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from utils import get_author_link, excel_write


def about_and_description(link, file_name):
    s = Service(executable_path="C:/SeleniumDrivers/chromedriver.exe")
    driver1 = webdriver.Chrome(service=s)
    for count, link in enumerate(link):
        about_link = str(link) + "/about"
        driver1.get(about_link)
        author_name_list = []
        author_name = driver1.find_element(By.CLASS_NAME, 'u_a_a9083').text
        author_name_list.append(author_name)
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
                chain(author_name_list, social_media_links_list, about_list, styles, subject, equipment, other))
            excel_write(final_list, file_name)

        elif len(separated_h2_btns) == 3:
            styles = [' '.join([str(elem) for elem in separated_h2_btns[0]])]
            subject = [' '.join([str(elem) for elem in separated_h2_btns[1]])]
            equipment = [' '.join([str(elem) for elem in separated_h2_btns[2]])]
            final_list = list(
                chain(author_name_list, social_media_links_list, about_list, styles, subject, equipment))
            excel_write(final_list, file_name)

        elif len(separated_h2_btns) == 2:
            styles = [' '.join([str(elem) for elem in separated_h2_btns[0]])]
            subject = [' '.join([str(elem) for elem in separated_h2_btns[1]])]
            final_list = list(
                chain(author_name_list, social_media_links_list, about_list, styles, subject))
            excel_write(final_list, file_name)

        elif len(separated_h2_btns) == 1:
            styles = [' '.join([str(elem) for elem in separated_h2_btns[0]])]
            final_list = list(
                chain(author_name_list, social_media_links_list, about_list, styles))
            excel_write(final_list, file_name)

        else:
            final_list = list(
                chain(author_name_list, social_media_links_list, about_list))
            excel_write(final_list, file_name)

        print(count, "ith Iteration Completed", ctime())
    driver1.quit()
    return


def search_page_getting_links(url):
    s = Service(executable_path="C:/SeleniumDrivers/chromedriver.exe")
    driver1 = webdriver.Chrome(service=s)
    driver1.get(url)
    chosen_image = driver1.find_elements(By.CLASS_NAME, "z_h_81637")
    search_page_links = []
    for count, a in enumerate(chosen_image):
        link = a.get_attribute('href')
        search_page_links.append(link)
    driver1.quit()
    return search_page_links


print("START : ", ctime())
search_page = search_page_getting_links(url="https://www.shutterstock.com/search?page=2")
print("Mainpage Links Fetched : ", ctime())

n = get_author_link(search_page, split_by="By ")
print("Author links fetched : ", ctime())
# n = ["https://www.shutterstock.com/g/Ardea-studio/"]
about_and_description(n, file_name="search_page_data.csv")
print("END : ", ctime())
