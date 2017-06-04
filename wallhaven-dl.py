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

def login():
    print('NSFW images require login')
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    req = requests.post('https://alpha.wallhaven.cc/auth/login', data={'username':username, 'password':password})
    return req.cookies

def category():
    print('''****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ')
    ALL = '111'
    ANIME = '010'
    GENERAL = '100'
    PEOPLE = '001'
    GENERAL_ANIME = '110'
    GENERAL_PEOPLE = '101'
    if ccode.lower() == "all":
        ctag = ALL
    elif ccode.lower() == "anime":
        ctag = ANIME
    elif ccode.lower() == "general":
        ctag = GENERAL
    elif ccode.lower() == "people":
        ctag = PEOPLE
    elif ccode.lower() == "ga":
        ctag = GENERAL_ANIME
    elif ccode.lower() == "gp":
        ctag = GENERAL_PEOPLE

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
        cookies = login()
    else:
        cookies = dict()

    CATURL = 'https://alpha.wallhaven.cc/search?categories=' + \
        ctag + '&purity=' + ptag + '&page='
    return (CATURL, cookies)


def latest():
    print('Downloading latest')
    latesturl = 'https://alpha.wallhaven.cc/latest?page='
    return (latesturl, dict())

def search():
    query = input('Enter search query: ')
    searchurl = 'https://alpha.wallhaven.cc/search?q=' + \
        urllib.parse.quote_plus(query) + '&page='
    return (searchurl, dict())

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
        BASEURL, cookies = category()
    elif Choice == 'latest':
        BASEURL, cookies = latest()
    elif Choice == 'search':
        BASEURL, cookies = search()

    pgid = int(input('How Many pages you want to Download: '))
    print('Number of Wallpapers to Download: ' + str(24 * pgid))
    for j in range(1, pgid + 1):
        totalImage = str(24 * pgid)
        url = BASEURL + str(j)
        urlreq = requests.get(url, cookies=cookies)
        soup = bs4.BeautifulSoup(urlreq.text, 'lxml')
        soupid = soup.findAll('a', {'class': 'preview'})
        res = re.compile(r'\d+')
        imgid = res.findall(str(soupid))
        imgext = ['jpg', 'png', 'bmp']
        for i in range(len(imgid)):
            currentImage = (((j - 1) * 24) + (i + 1))
            url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % imgid[
                i]
            for ext in imgext:
                iurl = url + ext
                osPath = os.path.join('Wallhaven', os.path.basename(iurl))
                if not os.path.exists(osPath):
                    imgreq = requests.get(iurl, cookies=cookies)
                    if imgreq.status_code == 200:
                        print("Downloading : %s - %s / %s" % ((os.path.basename(iurl)), currentImage , totalImage))
                        with open(osPath, 'ab') as imageFile:
                            for chunk in imgreq.iter_content(1024):
                                imageFile.write(chunk)
                        break
                else:
                    print("%s already exist - %s / %s" % os.path.basename(iurl), currentImage , totalImage)

if __name__ == '__main__':
    main()
