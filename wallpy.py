########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  dated- 26 June 2016                 #
########################################################

import os
import bs4
import re
import requests

os.makedirs('Wallhaven', exist_ok=True)
url = 'https://alpha.wallhaven.cc/latest'
urlreq = requests.get(url)
soup = bs4.BeautifulSoup(urlreq.text, 'lxml')
soupid = soup.findAll('a', {'class': 'preview'})
res = re.compile(r'\d+')
imgid = res.findall(str(soupid))
imgext = ['jpg', 'png', 'bmp']
for i in range(len(imgid)):
    url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % imgid[
        i]
    iurl = url + imgext[0]
    imgreq = requests.get(iurl)
    er = imgreq.status_code
    if er == 404:
        iurl == url + imgext[1]
        er2 = imgreq.status_code
        if er2 == 404:
            iurl == url + imgext[2]
    print('Downloading: ' + iurl)
    imageFile = open(os.path.join('Wallhaven', os.path.basename(iurl)), 'ab')
    for chunk in imgreq.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
