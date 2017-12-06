# coding: utf-8


import urllib2 as u2
import re
from bs4 import BeautifulSoup

main_name = 'https://www.zjsnrwiki.com'
main_url = main_name + '/wiki/\xe8\x88\xb0\xe5\xa8\x98\xe5\x9b\xbe\xe9\x89\xb4'  # 舰娘图鉴
main_page = u2.urlopen(main_url).read()
reg_all = '<center><b><a href="/wiki/.+" title=".+">.+</a></b></center>'

count = 198
link_all = re.findall(reg_all, main_page)[count:]

for i in link_all:
    now_url = main_name + i.split('\"')[1]
    now_page = u2.urlopen(now_url).read()
    reg_normal = '<img alt="L NORMAL [0-9]+.png" src="https://www.zjsnrwiki.com/images/.+.png" width="1024" height="1024">'
    reg_broken = '<img alt="L BROKEN [0-9]+.png" src="https://www.zjsnrwiki.com/images/.+.png" width="1024" height="1024">'
    link_normal = re.findall(reg_normal, now_page)
    link_broken = re.findall(reg_broken, now_page)
    link_normal = link_normal[0].split('\"')[3]
    link_broken = link_broken[0].split('\"')[3]

    try:
        girl_normal = u2.urlopen(link_normal).read()
        count += 1
        name_normal = str(count) + 'NORMAL'
        with open('{}.{}'.format(name_normal, 'png'), 'wb') as f:
            f.write(girl_normal)
    except:
        print('{}:NORMAL_404').format(str(count))

    try:
        girl_broken = u2.urlopen(link_broken).read()
        count += 1
        name_broken = str(count) + 'BROKEN'
        with open('{}.{}'.format(name_broken, 'png'), 'wb') as f:
            f.write(girl_broken)
    except:
        print('{}:BROKEN_404').format(str(count))

    print count

