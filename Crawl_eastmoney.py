import re
import pickle
from tqdm import tqdm
from urllib import request
from bs4 import BeautifulSoup


def assign_url(s):
    d = {'stock_hk': 'http://hk.eastmoney.com/news/cggdd.html',  # 港股
         'stock_usa': 'http://stock.eastmoney.com/news/cmgdd.html',  # 美股
         'forex': 'http://forex.eastmoney.com/news/cwhdd.html',  # 外汇
         'futures': 'http://futures.eastmoney.com/news/cqhdd.html',  # 期货
         'gold': 'http://gold.eastmoney.com/news/chjdd.html',  # 黄金
         'news_world': 'http://finance.eastmoney.com/news/cgjjj.html',  # 国际新闻
         'news_china': 'http://finance.eastmoney.com/news/cgnjj.html',  # 国内新闻
         'remark': 'http://stock.eastmoney.com/news/cgspj.html',  # 评级
         'industry': 'http://stock.eastmoney.com/news/chydd.html',  # 行业
         'SCI': 'http://stock.eastmoney.com/news/cdpfx.html'}  # 大盘
    try:
        return d[s]
    except:
        raise KeyError('The key name cannot be found.')

        
def get_this_news(this_link):
    # input: this_link, link of the current news page
    # output: dict_info, dictionary storing the necessary information about the news
    # get soup
    this_html = request.urlopen(this_link).read()
    this_html = this_html.decode('utf-8')
    this_soup = BeautifulSoup(this_html)
    # fill in the dictionary
    dict_info = {'web': '', 'publish_date': '', 'publish_time': '', 'resource': '', 'title': '', 'context': '', 'type': ''}
    main_food = this_soup.find('div', 'newsContent')
    dict_info['web'] = this_link
    dict_info['publish_date'] = main_food.find('div', 'time').get_text().split(' ')[0]
    dict_info['publish_time'] = main_food.find('div', 'time').get_text().split(' ')[0]
    dict_info['resource'] = main_food.find('div', 'source data-source').get_text().replace('\r', '').replace('\n', '').replace('来源：', '').strip()
    dict_info['title'] = main_food.h1.get_text().replace(' ', ', ')
    context = main_food.find('div', 'Body').get_text()
    if len(context) > 0: 
        context = context.replace('\u3000', '').replace('\r', '').replace('\n', '').strip()
        context = context.replace(re.findall(r'\(责任编辑：DF[0-9]{,3}\)', context)[0], '').strip()
    dict_info['context'] = context
    return dict_info


def get_this_theme(crawl_name, max_page=5):
    # input: crawl_name is a string
    print('Now crawl theme: ', crawl_name)
    save_name = 'eastmoney_' + crawl_name + '.pkl'
    url = assign_url(crawl_name)
    # Crawl theme page that lists all news with links
    info_all = []
    for i in tqdm(range(max_page)):
        if i > 0:
            url_now = url.replace('.html', '') + '_' + str(i+1) + '.html'
        else:
            url_now = url
        try:
            html_page = request.urlopen(url_now).read()
        except:
            continue
        html_page = html_page.decode('utf-8')
        theme_soup = BeautifulSoup(html_page)
        theme_soup = theme_soup.find_all('div', 'text')
        for soup_now in theme_soup:
            link_now = soup_now.find('a').get('href')  
            try:
                info_now = get_this_news(link_now)
                link_now['type'] = crawl_name
                info_all.append(info_now)
            except:
                continue        
    # Saving crawled information               
    with open(save_name, 'wb') as f:
        pickle.dump(info_all, f)
    print('Finish to crawl theme: ', crawl_name)
    return None


if __name__ == '__main__':
    # Crawl
    lst_theme = ['stock_hk', 'stock_usa', 'forex', 'futures', 'gold', 
                 'news_world', 'news_china', 'remark', 'industry', 'SCI']
    for now_theme in lst_theme:
        get_this_theme(crawl_name=now_theme, max_page=25)
    print('Crawling finished.')

    # Test
    name = 'SCI'
    load_path = 'eastmoney_' + name + '.pkl'
    with open(load_path, 'rb') as f:
        info_all = pickle.load(f)
    print('length of info_all:', len(info_all))

    for info_now in info_all:
        print('title:', info_now['title'], 'length of context:', len(info_now['context']))
        print('web:', info_now['resource'])
        print('-' * 30)
