
# coding: utf-8


import urllib2 as u2
import re
from bs4 import BeautifulSoup

main_name = 'http://www.gfwiki.org'
main_url = main_name + '/index.php?title=%E6%88%98%E6%9C%AF%E5%B0%91%E5%A5%B3%EF%BC%88%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89'
main_page = u2.urlopen(main_url).read()
link_reg = '<a href="/index.php\?title=.+" title=".+">'

count = 1
link_all = re.findall(link_reg, main_page)[count:]
for i in link_all:
    now_url = main_name + i.split('\"')[1]
    now_page = u2.urlopen(now_url).read()
    now_soup = BeautifulSoup(now_page)
    
    her_mode_1 = '\xe9\xbb\x98\xe8\xae\xa4\xe6\xad\xa3\xe5\xb8\xb8' # '默认正常'
    her_mode_2 = '\xe9\xbb\x98\xe8\xae\xa4\xe9\x87\x8d\xe5\x88\x9b' # '默认重创'
    her_url_1 = main_name + now_soup.find('div',{'title':her_mode_1}).find('a',{'class':'image'}).get('href')
    her_url_2 = main_name + now_soup.find('div',{'title':her_mode_2}).find('a',{'class':'image'}).get('href')
    
    her_soup_1 = main_name + BeautifulSoup(u2.urlopen(her_url_1).read()).find('a',{'class':'internal'}).get('href')
    her_soup_2 = main_name + BeautifulSoup(u2.urlopen(her_url_2).read()).find('a',{'class':'internal'}).get('href')
    
    
    try:
        herself_1 = u2.urlopen(her_soup_1).read()
        count += 1
        hername_1 = str(count) +'OK'
        with open('{}.{}'.format(hername_1, 'jpg'),'wb') as f:
            f.write(herself_1)
    except:
        print('OK_404')
    
    try:
        herself_2 = u2.urlopen(her_soup_2).read()
        count += 1
        hername_2 = str(count) +'Bad'
        with open('{}.{}'.format(hername_2, 'jpg'),'wb') as f:
            f.write(herself_2)
    except:
        print('Bad_404')
    
    print count
    




