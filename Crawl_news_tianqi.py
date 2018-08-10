import re
import csv
import time
import pickle
from tqdm import tqdm
# from urllib import request
import requests
from bs4 import BeautifulSoup


def get_this_news(link_now):
    # input: this_link, link of the current news page
    # output: dict_info, dictionary storing the necessary information about the news
    # get soup
#     this_html = request.urlopen(link_now).read()
#     this_html = this_html.decode('utf-8')
    this_html = requests.get(link_now)
    this_soup = BeautifulSoup(this_html.content, 'html.parser')
    dict_info = {'url': '', 'publish_date': '', 'source': '', 'title': '', 'body': ''}
    basic_info = this_soup.find('div', 'time').get_text()
    dict_info['url'] = link_now
    dict_info['publish_date'] = re.findall(r'\d\d\d\d-\d\d-\d\d', basic_info)[0]
    dict_info['source'] = re.findall(r'(?<=来源：)(\S+)', basic_info)[0]
    dict_info['title'] = this_soup.find('h1').get_text().replace(' ', '，')
    raw_context = this_soup.find('div', 'texts').find_all('p')
    context = ''
    for text in raw_context:
        try:
            text['class']
        except:
            if text.string is not None:
                context += text.string + '\n'
    dict_info['body'] = context
    return dict_info


if __name__ == '__main__':
    root_path = 'https://www.tianqi.com/news/list_404_'
    max_page = 100

    with open('news_tianqi.csv', 'w', encoding='utf-8-sig')as f:
        news = csv.writer(f)
        news.writerow(['url', 'publish_date', 'source', 'title', 'body'])
        for i in tqdm(range(max_page)):
            url_now = root_path + str(i+1) + '.html'
#             html_page = request.urlopen(url_now).read()
#             html_page = html_page.decode('utf-8')
            html_page = requests.get(url_now)
            html_soup = BeautifulSoup(html_page.content, 'html.parser')
            html_soup = html_soup.find_all('li')
            for soup_now in html_soup:
                link_now = soup_now.find('a').get('href')
                try:
                    info_now = get_this_news(link_now)
                    news.writerow([info_now['body'], info_now['publish_date'], info_now['source'], info_now['title'], info_now['url']])
                except:
                    continue
