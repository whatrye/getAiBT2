#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取torrent的相关图片

##from bs4 import BeautifulSoup
import requests,queue,threading

import gettorrentlink3
from getFiles2 import getFiles

linksQueue = queue.Queue()

def getTandI_thread(myQueue,torrentsPath,enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "获取torrent的相关图片"
    proxies = {}
    timeout = 15
    picFilename = ''

    while True:
        try:
            tp = myQueue.get_nowait()
            j = myQueue.qsize()
        except Exception as e:
            break

    ##    n = 0
    ##    for tp in linksList:
        btsList = []
        imgsList = []
    ##    n=n+1
        print(tp['link'])
        tResDict = gettorrentlink3.get_torrentlink(myreq_url = str(tp['link']), enable_proxy = enable_proxy, proxy_string = proxy_string)
        for imgLink in tResDict['imgsList']:
            #outfilename =imgLink[imgLink.rfind('/')+1:len(imgLink)]
            outfilename =imgLink[imgLink.rfind('/')+1:]
            a = {'link':imgLink,'ofile':outfilename,'oDir':str(torrentsPath + r'/' +tResDict['title'])}
            imgsList.append(a)
        if tResDict['btCode'] != 'notExist':
            b = {'link':tResDict['btCode'],'ofile':str(tResDict['title'])+'.torrent','oDir':str(torrentsPath + r'/' +tResDict['title'])}
            btsList.append(b)
            
        if len(btsList) >0:
            getFiles(fileList=btsList,m='p')
        if len(imgsList) >0:
            getFiles(fileList=imgsList,m='g')

def getTrAndImgs(linksList,torrentsPath):
    #以线程方式获取单网页并获取torrent和img的链接
    for tp in linksList:
        linksQueue.put(tp)
    threadN = 100
    jqueue = linksQueue.qsize()
    print('total ',jqueue,' items')
    if jqueue < threadN:
        threadN = jqueue

    if jqueue > 0:
        threads = []
        for i in range(0,threadN):
            thread = threading.Thread(target = getTandI_thread, args = (linksQueue,torrentsPath,))
            threads.append(thread)
            thread.start()
        for thread1 in threads:
            thread1.join()

if __name__ == '__main__':
    outfilename,imgContent = getImg()
    outfile = open(outfilename,'wb')
    outfile.write(imgContent)
    outfile.close()
    print(outfilename,' be saved')
