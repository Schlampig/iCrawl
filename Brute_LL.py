
# coding: utf-8
import urllib2 as u2

start = 1
end = 2285

for i in xrange(start,end+1):
    now_url = 'https://app.lovelivewiki.com/images/4.0/cards/' + str(i) + '.png'
    try:
        now_picture = u2.urlopen(now_url).read()
        now_name = str(i)
        with open('{}.{}'.format(i, 'png'),'wb') as f:
            f.write(now_picture)
    except:
        continue



