import re
from itertools import chain
from time import ctime

import requests
from bs4 import BeautifulSoup

from selenium_files.utils import page_loggers, excel_write


def author_datails_write(link, file_name):
    for l in link:
        raw_html = requests.get(l, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        soup = BeautifulSoup(raw_html.content, 'html.parser')
        try:
            name = soup.find('h1', class_="u_a_a9083")

            about = soup.find_all('div', class_="aa_a_15778")
            styles = soup.find_all('div', 'aa_e_e2ec7')
            social_media_links = soup.find_all('a', class_="u_b_96ed0")
            about_list = []
            styles_list = []

            s_links = [str(s.get("href")) for s in social_media_links]
            l_s_links = len(s_links)
            while l_s_links < 4:
                s_links.append("None")
                l_s_links += 1
            for i in about:
                s = ""
                for j in i:
                    s = s + str(j.text)
                about_list.append(s)

            for i in styles:
                l = [j.text for j in i]
                styles_list.append(l)

            if len(styles_list) == 4:
                styles = [' '.join([str(elem) for elem in styles_list[0]])]
                subject = [' '.join([str(elem) for elem in styles_list[1]])]
                equipment = [' '.join([str(elem) for elem in styles_list[2]])]
                other = [' '.join([str(elem) for elem in styles_list[3]])]
                final_list = list(chain([name.text], s_links, about_list, styles, subject, equipment, other))
                status = excel_write(write_list=final_list, file_name=file_name)

                print("Writed......")
            elif len(styles_list) == 3:
                styles = [' '.join([str(elem) for elem in styles_list[0]])]
                subject = [' '.join([str(elem) for elem in styles_list[1]])]
                equipment = [' '.join([str(elem) for elem in styles_list[2]])]
                final_list = list(chain([name.text], s_links, about_list, styles, subject, equipment))
                excel_write(write_list=final_list, file_name=file_name)
                print("Writed......")

            elif len(styles_list) == 2:
                styles = [' '.join([str(elem) for elem in styles_list[0]])]
                subject = [' '.join([str(elem) for elem in styles_list[1]])]
                final_list = list(chain([name.text], s_links, about_list, styles, subject))
                excel_write(write_list=final_list, file_name=file_name)
                print("Writed......")

            elif len(styles_list) == 1:
                styles = [' '.join([str(elem) for elem in styles_list[0]])]
                final_list = list(chain([name.text], s_links, about_list, styles))
                excel_write(write_list=final_list, file_name=file_name)
                print("Writed......")

            else:
                final_list = list(chain([name.text], s_links, about_list))
                excel_write(write_list=final_list, file_name=file_name)
                print("Writed......")

        except Exception as e:
            print(l)
            print(e)


def get_author_link(links, csv_file_name, links_file_name):
    try:
        links_list = set()
        for link in links:
            raw_html = requests.get(link, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/35.0.1916.47 Safari/537.36'})
            soup = BeautifulSoup(raw_html.content, 'html.parser')
            k = soup.find('a', class_="")
            link = "https://www.shutterstock.com" + str(k.get('href')).replace("video", "about")
            status = excel_write(write_list=[str(link).removeprefix("https://")], file_name=links_file_name)
            if status:
                print("EXIST --> ", link)
                continue
            links_list.add(link)
            print("New Author : ", link)

        if links_list:
            print(len(links_list), "AUTHOR LINKS FETCHED", ctime())
            author_datails_write(link=links_list, file_name=csv_file_name)
            links_list.clear()
        else:
            print("NO NEW AUTHOR LINKS FETCHED")
    except Exception as e:
        print(e)


def mainpage(url, loger_name, csv_file_name, links_file_name):
    try:
        base_url = url
        links_list = []
        while base_url is not None:
            print("START :", base_url)
            if "page" in base_url:
                page = re.findall(r'\d+', base_url)
                print(f"PAGE {page[0]} START", ctime())
                page_loggers(loger_name, f"{page[0]} Page Started")
            else:
                print(f"PAGE {base_url} START", ctime())
                page_loggers(loger_name, f"{base_url} Page Started")

            raw_html = requests.get(base_url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/35.0.1916.47 Safari/537.36'})
            soup = BeautifulSoup(raw_html.content, 'html.parser')
            k = soup.find_all('a', class_="")
            for i in k:
                link = "https://www.shutterstock.com" + str(i.get('href'))
                links_list.append(link)
            print("ALL POSTS LINKS FETCHED", ctime())
            get_author_link(links=links_list, csv_file_name=csv_file_name, links_file_name=links_file_name)
            links_list.clear()
            if "page" in base_url:
                page = re.findall(r'\d+', base_url)
                print(f"PAGE {page[0]} COMPLETED", ctime())
                print()
                page_loggers(loger_name, f"{page[0]} Page completed")
            else:
                print(f"{base_url} Page completed", ctime())
                page_loggers(loger_name, f"{base_url} PAGE COMPLETED")

            next_page_class = soup.find('a', class_="z_b_6e283")
            next_page_link = "https://www.shutterstock.com" + str(next_page_class.get('href'))
            if base_url == next_page_link:
                base_url = None
            else:
                base_url = next_page_link
    except Exception as e:
        print(e)


URL = "https://www.shutterstock.com/video/search/drone-footage?page=1905"
LOGER_NAME = "drone-footage"
CSV_FILENAME = "drone-footage.csv"
CSV_LINKS_FILENAME = "UserProfileLinks.csv"

mainpage(url=URL, loger_name=LOGER_NAME,
         csv_file_name=CSV_FILENAME, links_file_name=CSV_LINKS_FILENAME)
