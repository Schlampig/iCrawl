# -*- coding: UTF-8 -*-


import pickle
from tqdm import tqdm
from urllib import request
from bs4 import BeautifulSoup


def assign_url(s):
    d = {'hongguan': 'http://www.financialnews.com.cn/hg/',
         'jianguan': 'http://www.financialnews.com.cn/jg/ld/',
         'yinhang': 'http://www.financialnews.com.cn/yh/sd/',
         'zhengquan': 'http://www.financialnews.com.cn/zq/stock/',
         'baoxian': 'http://www.financialnews.com.cn/bx/bxsd/',
         'hujin': 'http://www.financialnews.com.cn/if/if/',
         'waihui': 'http://www.financialnews.com.cn/sc/wh/',
         'xintuo': 'http://www.financialnews.com.cn/trust/cyzc/',
         'shuju': 'http://www.financialnews.com.cn/sj_142/jrsj/'}
    try:
        return d[s]
    except:
        raise KeyError('The key name cannot be found.')


def get_this_news(this_link):
    # 爬取当前link的新闻内容
    this_html = request.urlopen(this_link).read()
    this_html = this_html.decode('utf-8')
    this_soup = BeautifulSoup(this_html)
    # 构造字典
    dict_info = {'author': '', 'source': '', 'date': '', 'title': '', 'context': ''}
    # 获取标题
    dict_info['title'] = this_soup.find_all('div', 'content_title')[0].get_text()
    # 发布信息
    raw_info = this_soup.find_all('div', 'content_info')
    lst_info = raw_info[0].get_text().split('\n')
    for i in lst_info:
        if '来源' in i:
            dict_info['source'] = i.replace('来源：', '').strip()
        elif '作者' in i:
            dict_info['author'] = i.replace('作者：', '').replace('记者', '').strip()
        elif '日期' in i:
            dict_info['date'] = i.replace('发布日期：', '').replace(' ', ',').strip()
        else:
            continue
    # 获取正文
    raw_text = this_soup.find_all('div', 'Custom_UnionStyle')
    if len(raw_text) == 0:
        # 格式不是<div class='Custom_UnionStyle'>，而是<div class='TRS_Editor'>,
        # 其中<div><p class='Custom_UnionStyle'></p></div>
        raw_text = this_soup.find_all('div', 'TRS_Editor')[0]
        raw_text = raw_text.find_all('p', 'Custom_UnionStyle')
    context = ''
    for line in raw_text:
        context_now = line.get_text().replace(' ', '')
        context += context_now
    dict_info['context'] = context

    return dict_info


if __name__ == '__main__':
    crawl_name = 'hongguan'
    save_name = 'financialnews_' + crawl_name + '.pkl'
    url = assign_url(crawl_name)
    max_page = 20

    # 爬取信息
    info_all = []
    for i in tqdm(range(max_page)):
        if i > 0:
            url_now = url + 'index_' + str(i) + '.html'
        else:
            url_now = url

        try:
            html_page = request.urlopen(url_now).read()
        except:
            continue

        html_page = html_page.decode('utf-8')
        theme_soup = BeautifulSoup(html_page)
        for batch_news in theme_soup.find_all('ul', id='list'):
            batch_links = batch_news.find_all('a')
            for link in batch_links:
                link_now = link.get('href')
                if len(link_now) > 0:
                    link_now = url + link_now.lstrip('.')  # 注意：此处是url而非url_now
                try:
                    info_now = get_this_news(link_now)
                    info_all.append(info_now)
                except:
                    continue

    # 存储爬取的文件信息
    with open(save_name, 'wb') as f:
        pickle.dump(info_all, f)

    print('Crawling finished.')
    
    # 测试爬取是否成功，读取并打印某个爬好的文件
    # load_path = 'financialnews_hongguan.pkl'
    # with open(load_path, 'rb') as f:
    #     info_all = pickle.load(f)
    # print(len(info_all))
    # 
    # for info_now in info_all:
    #     print(info_now['title'])
    #     print('-'*30)
