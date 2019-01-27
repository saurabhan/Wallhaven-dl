########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  dated- 26 June 2016                 #
#                 Update - 29 June 2016                #
########################################################

import os
import getpass
import bs4
import re
import requests
import tqdm
import time
import urllib

os.makedirs('Wallhaven', exist_ok=True)
BASEURL=""
cookies=dict()

def login():
    global cookies
    print('NSFW images require login')
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    cookies = requests.post('https://alpha.wallhaven.cc/auth/login', data={'username':username, 'password':password}).cookies

def category():
    global BASEURL
    print('''
    ****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ').lower()
    ctags = {'all':'111', 'anime':'010', 'general':'100', 'people':'001', 'ga':'110', 'gp':'101' }
    ctag = ctags[ccode]

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw':'100', 'sketchy':'010', 'nsfw':'001', 'ws':'110', 'wn':'101', 'sn':'011', 'all':'111'}
    ptag = ptags[pcode]

    if pcode in ['nsfw', 'wn', 'sn', 'all']:
        login()

    BASEURL = 'https://alpha.wallhaven.cc/search?categories=' + \
        ctag + '&purity=' + ptag + '&page='

def latest():
    global BASEURL
    print('Downloading latest')
    BASEURL = 'https://alpha.wallhaven.cc/latest?page='

def search():
    global BASEURL
    query = input('Enter search query: ')
    BASEURL = 'https://alpha.wallhaven.cc/search?q=' + \
        urllib.parse.quote_plus(query) + '&page='

def downloadPage(pageId, totalImage):
    url = BASEURL + str(pageId)
    urlreq = requests.get(url, cookies=cookies)
    soup = bs4.BeautifulSoup(urlreq.text, 'lxml')
    soupid = soup.findAll('a', {'class': 'preview'})
    res = re.compile(r'\d+')
    imgId = res.findall(str(soupid))
    imgext = ['jpg', 'png', 'bmp']
    for imgIt in range(len(imgId)):
        currentImage = (((pageId - 1) * 24) + (imgIt + 1))
        filename = 'wallhaven-%s.' % imgId[imgIt]
        url = 'https://wallpapers.wallhaven.cc/wallpapers/full/%s' % filename
        for ext in imgext:
            iurl = url + ext
            osPath = os.path.join('Wallhaven', filename)
            if not os.path.exists(osPath):
                imgreq = requests.get(iurl, cookies=cookies)
                if imgreq.status_code == 200:
                    print("Downloading : %s - %s / %s" % (filename, currentImage , totalImage))
                    with open(osPath, 'ab') as imageFile:
                        for chunk in imgreq.iter_content(1024):
                            imageFile.write(chunk)
                    break
                elif (imgreq.status_code != 403 and imgreq.status_code != 404):
                    print("Unable to download %s - %s / %s" % (filename, currentImage , totalImage))
            else:
                print("%s already exist - %s / %s" % (filename, currentImage , totalImage))
                break

def main():
    Choice = input('''Choose how you want to download the image:

    Enter "category" for downloading wallpapers from specified categories
    Enter "latest" for downloading latest wallpapers
    Enter "search" for downloading wallpapers from search

    Enter choice: ''').lower()
    while Choice not in ['category', 'latest', 'search']:
        if Choice != None:
            print('You entered an incorrect value.')
        choice = input('Enter choice: ')

    if Choice == 'category':
        category()
    elif Choice == 'latest':
        latest()
    elif Choice == 'search':
        search()

    pgid = int(input('How Many pages you want to Download: '))
    totalImageToDownload = str(24 * pgid)
    print('Number of Wallpapers to Download: ' + totalImageToDownload)
    for j in range(1, pgid + 1):
        downloadPage(j, totalImageToDownload)

if __name__ == '__main__':
    main()
