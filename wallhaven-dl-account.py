########################################################
#        Program to Download Wallpapers from           #
#                  your account                        #
#               alpha.wallhaven.cc                     #
#                                                      #
########################################################

import os
import getpass
import bs4
import re
import requests
import tqdm
import time
import urllib 
import math

os.makedirs('Wallhaven', exist_ok=True)

def login():
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    req = requests.post('https://alpha.wallhaven.cc/auth/login', data={'username':username, 'password':password})
    return (req.cookies,username)

def dlcolecpage(urlcolecpage,cookies):
    urlreqcolection = requests.get(urlcolecpage, cookies=cookies)
    soupcolection = bs4.BeautifulSoup(urlreqcolection.text, 'lxml')

    listnbpage = soupcolection.findAll('h2')
    nbpage = listnbpage[1].text.split(' ')[-1]
    listcollectionName = soupcolection.findAll('h1')
    collectionName = listcollectionName[1].text

    osPath = os.path.join('Wallhaven', collectionName)
    if not os.path.exists(osPath):
        os.makedirs(osPath)

    soupid = soupcolection.findAll('a', {'class': 'preview'})
    res = re.compile(r'\d+')
    imgid = res.findall(str(soupid))
    imgext = ['jpg', 'png', 'bmp']
    for i in range(len(imgid)):
        url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % imgid[i]
        for ext in imgext:
            iurl = url + ext
            osPath = os.path.join('Wallhaven', collectionName, os.path.basename(iurl))
            if not os.path.exists(osPath):
                imgreq = requests.get(iurl, cookies=cookies)
                if imgreq.status_code == 200:
                    print("Downloading : %s" % ((os.path.basename(iurl))))
                    with open(osPath, 'ab') as imageFile:
                        for chunk in imgreq.iter_content(1024):
                            imageFile.write(chunk)
            else:
                print("%s already exist" % os.path.basename(iurl))

from tqdm import tqdm
from math import *

def main():
    cookies, username = login()
    userurl = 'https://alpha.wallhaven.cc/user/'+ username +'/favorites'
    urlreq = requests.get(userurl, cookies=cookies)
    soup = bs4.BeautifulSoup(urlreq.text, 'lxml')
    for li in soup.findAll('li', {'class': 'collection'}):

        a = li.find('a')
        colectionurl = a['href'] 
        colectionurlNB = colectionurl + "?page=" + "1"

        urlreqcolection = requests.get(colectionurlNB, cookies=cookies)
        soupcolection = bs4.BeautifulSoup(urlreqcolection.text, 'lxml')

        listnbpage = soupcolection.findAll('h2')
        nbpage = listnbpage[1].text.split(' ')[-1]
        listcollectionName = soupcolection.findAll('h1')
        if len(listcollectionName) > 0:
            collectionName = listcollectionName[1].text
        else:
            collectionName = "bonneQuestion"


        osPath = os.path.join('Wallhaven', collectionName)
        if not os.path.exists(osPath):
            os.makedirs(osPath)

        soupid = soupcolection.findAll('a', {'class': 'preview'})
        res = re.compile(r'\d+')
        imgid = res.findall(str(soupid))
        imgext = ['jpg', 'png', 'bmp']
        for i in range(len(imgid)):
            url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % imgid[i]
            for ext in imgext:
                iurl = url + ext
                osPath = os.path.join('Wallhaven', collectionName, os.path.basename(iurl))
                if not os.path.exists(osPath):
                    imgreq = requests.get(iurl, cookies=cookies, stream=True)
                    if imgreq.status_code == 200:
                        print("Downloading : %s " % ((os.path.basename(iurl))))
                        total_size = int(imgreq.headers.get('content-length', 0))
                        with open(osPath, 'ab') as imageFile:
                            for chunk in tqdm(imgreq.iter_content(1024), total=math.ceil(total_size/1024), unit='KB', unit_scale=True):
                                imageFile.write(chunk)
                        break
                else:
                    print("%s already exist" % os.path.basename(iurl))
        try:
            nbpage = int(nbpage)+1
            for i in range(2,nbpage):
                colectionurlNB = colectionurl + "?page=" + str(i)
                dlcolecpage(colectionurlNB,cookies)
        except:
            pass

if __name__ == '__main__':
    main()
