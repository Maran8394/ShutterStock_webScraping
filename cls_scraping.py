import csv
import logging
import re
from itertools import chain
from time import ctime

import requests
from bs4 import BeautifulSoup


class Scraping:

    def __init__(self, url, loger_name, csv_file_name, links_file_name):
        self.url = url
        self.loger_name = loger_name
        self.csv_file_name = csv_file_name
        self.links_file_name = links_file_name
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        self.mainpage()

    def page_loggers(self, text):
        logging.basicConfig(filename=f"logs/{self.loger_name}.log", filemode="a", format='%(asctime)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')
        l = logging.getLogger()
        l.setLevel(logging.INFO)
        l.info(text)

    def excel_write(self, write_list, file_name):
        given_file_name = f"collected_data/{file_name}.csv"
        try:
            with open(given_file_name, 'r+', newline='', encoding="ISO-8859-1", errors='ignore') as read_file:
                reader_writer = csv.reader((line.replace('\0', '') for line in read_file))
                if write_list not in reader_writer:
                    with open(given_file_name, 'a+', newline='', encoding="ISO-8859-1",
                              errors='ignore') as f:
                        writer = csv.writer(f, delimiter=",")
                        writer.writerow(write_list)
                        f.close()
                else:
                    return False
        except FileNotFoundError:
            f = open(given_file_name, 'w+', newline='', encoding='utf-8', errors='ignore')
            f.close()
            self.excel_write(write_list, file_name)
        except Exception as e:
            print(e)

    def author_datails_write(self, link):
        for l in link:
            raw_html = requests.get(l, headers=self.header)
            soup = BeautifulSoup(raw_html.content, 'html.parser')
            try:
                name = soup.find('h1', class_="u_a_a9083")

                about = soup.find_all('div', class_="aa_a_15778")
                styles = soup.find_all('div', 'aa_e_e2ec7')
                social_media_links = soup.find_all('a', class_="u_b_96ed0")
                about_list = []
                styles_list = []

                s_links = [str(link.get("href")) for link in social_media_links]
                l_s_links = len(s_links)
                while l_s_links < 4:
                    s_links.append("None")
                    l_s_links += 1
                for i in about:
                    st = ""
                    for j in i:
                        st = st + str(j.text)
                    about_list.append(st)

                for i in styles:
                    l = [j.text for j in i]
                    styles_list.append(l)

                if len(styles_list) == 4:
                    styles = [' '.join([str(elem) for elem in styles_list[0]])]
                    subject = [' '.join([str(elem) for elem in styles_list[1]])]
                    equipment = [' '.join([str(elem) for elem in styles_list[2]])]
                    other = [' '.join([str(elem) for elem in styles_list[3]])]
                    final_list = list(chain([name.text], s_links, about_list, styles, subject, equipment, other))
                    status = self.excel_write(write_list=final_list, file_name=self.csv_file_name)
                    if not status:
                        print("Exist -- >", final_list[0])
                    else:
                        print("Writed......", final_list[0])

                elif len(styles_list) == 3:
                    styles = [' '.join([str(elem) for elem in styles_list[0]])]
                    subject = [' '.join([str(elem) for elem in styles_list[1]])]
                    equipment = [' '.join([str(elem) for elem in styles_list[2]])]
                    final_list = list(chain([name.text], s_links, about_list, styles, subject, equipment))
                    status = self.excel_write(write_list=final_list, file_name=self.csv_file_name)
                    if not status:
                        print("Exist -- >", final_list[0])
                    else:
                        print("Writed......", final_list[0])

                elif len(styles_list) == 2:
                    styles = [' '.join([str(elem) for elem in styles_list[0]])]
                    subject = [' '.join([str(elem) for elem in styles_list[1]])]
                    final_list = list(chain([name.text], s_links, about_list, styles, subject))
                    status = self.excel_write(write_list=final_list, file_name=self.csv_file_name)
                    if not status:
                        print("Exist -- >", final_list[0])
                    else:
                        print("Writed......", final_list[0])

                elif len(styles_list) == 1:
                    styles = [' '.join([str(elem) for elem in styles_list[0]])]
                    final_list = list(chain([name.text], s_links, about_list, styles))
                    status = self.excel_write(write_list=final_list, file_name=self.csv_file_name)
                    if not status:
                        print("Exist -- >", final_list[0])
                    else:
                        print("Writed......", final_list[0])

                else:
                    final_list = list(chain([name.text], s_links, about_list))
                    status = self.excel_write(write_list=final_list, file_name=self.csv_file_name)
                    if not status:
                        print("Exist -- >", final_list[0])
                    else:
                        print("Writed......", final_list[0])

            except Exception as e:
                print(l)
                print(e)

    def get_author_link(self, links):
        try:
            links_list = set()
            for link in links:
                raw_html = requests.get(link, headers=self.header)
                soup = BeautifulSoup(raw_html.content, 'html.parser')
                k = soup.find('a', class_="")
                link = "https://www.shutterstock.com" + str(k.get('href')).replace("video", "about")
                status = self.excel_write(write_list=[str(link).removeprefix("https://")],
                                          file_name=self.links_file_name)
                if not status:
                    print("Exist --> ", link)
                    continue
                links_list.add(link)
                print("New Author : ", link)

            if links_list:
                print(len(links_list), "AUTHOR LINKS FETCHED", ctime())
                self.author_datails_write(link=links_list)
                links_list.clear()
            else:
                print("NO NEW AUTHOR LINKS FETCHED")
        except Exception as e:
            print(e)

    def mainpage(self):
        try:
            base_url = self.url
            links_list = []
            while base_url is not None:
                print("START :", base_url)
                if "page" in base_url:
                    page = re.findall(r'\d+', base_url)
                    print(f"PAGE {page[0]} START", ctime())
                    self.page_loggers(text=f"{page[0]} Page Started")
                else:
                    print(f"PAGE {base_url} START", ctime())
                    self.page_loggers(text=f"{base_url} Page Started")

                raw_html = requests.get(base_url, headers=self.header)
                soup = BeautifulSoup(raw_html.content, 'html.parser')
                k = soup.find_all('a', class_="")
                for i in k:
                    link = "https://www.shutterstock.com" + str(i.get('href'))
                    links_list.append(link)
                print("ALL POSTS LINKS FETCHED", ctime())
                self.get_author_link(links=links_list)
                links_list.clear()
                if "page" in base_url:
                    page = re.findall(r'\d+', base_url)
                    print(f"PAGE {page[0]} COMPLETED", ctime())
                    print()
                    self.page_loggers(f"{page[0]} Page completed")
                else:
                    print(f"{base_url} Page completed", ctime())
                    self.page_loggers(f"{base_url} PAGE COMPLETED")

                next_page_class = soup.find('a', class_="z_b_6e283")
                next_page_link = "https://www.shutterstock.com" + str(next_page_class.get('href'))
                if base_url == next_page_link:
                    base_url = None
                else:
                    base_url = next_page_link
        except Exception as e:
            print(e)


drone_footage = Scraping(
    url="https://www.shutterstock.com/video/search/drone-footage?page=1905",
    loger_name="drone-footage",
    links_file_name="UserProfileLinks",
    csv_file_name="drone-footage",
)
