########################################################
#         Script to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  dated- 26 June 2016                 #
########################################################

#!usr/bin/env python3

import os
import bs4
import re
import requests
import time
import tqdm

os.makedirs('Wallhaven', exist_ok=True)
pgid = int(input('How Many pages you want to Download: '))
print('Number of Wallpapers to Download: ' + str(24 * pgid))
for i in range(1, pgid + 1):
    url = 'https://alpha.wallhaven.cc/latest?page=' + str(i)
    urlreq = requests.get(url)
    soup = bs4.BeautifulSoup(urlreq.text, 'lxml')
    soupid = soup.findAll('a', {'class': 'preview'})
    res = re.compile(r'\d+')
    imgid = res.findall(str(soupid))
    imgext = ['jpg', 'png', 'bmp']
    for i in range(len(imgid)):
        url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % imgid[
            i]
        for ext in imgext:
            iurl = url + ext
            imgreq = requests.get(iurl)
            if imgreq.status_code == 200:
                print('Downloading: ' + iurl)
                with open(os.path.join('Wallhaven', os.path.basename(iurl)), 'ab') as imageFile:
                    for chunk in tqdm.tqdm(imgreq.iter_content(1024), total=(int(imgreq.headers['content-length']) / 1024), unit='KB'):
                        time.sleep(0.01)
                        imageFile.write(chunk)
            break
