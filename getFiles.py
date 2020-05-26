#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取torrent的相关图片

from bs4 import BeautifulSoup
import requests,queue,threading

filesQueue = queue.Queue()

def getFile(fileLink,fileName,outdir,enable_proxy = False, m = "g",tcode = 'vic8w2AM', proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "下载单独文件"
    proxies = {}
    timeout = 15
    picFilename = ''
    picFilename = fileName

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    
##    outfile_name = str(btItem['title'] + '.torrent')
##    outfile_name = fileName
##    outdir = str(torrentsPath + r'/' + btItem['title'])
    outdir = outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)
##    outfile_full_path = str(outdir + r'/' + outfile_name)
    
    try:
        if m == 'p':
            tcode = fileLink
            formdata={'code':tcode}
            r1 = requests.post('http://www.jandown.com/fetch.php',data = formdata, headers = headers)
            if b'<html>' in r1.content:
                r1.content = ''
                print('not torrent')
        else:
            r1 = requests.get(fileLink, headers = headers,proxies = proxies,timeout = timeout)
            
        imgContent = r1.content
        if len(imgContent) > 0:
            picFullpath = (outdir + r'/' + picFilename)
            ofile = open(picFullpath,'wb')
            ofile.write(imgContent)
            ofile.close()
    except Exception as e:
        print('error:',e)

##    return picFilename,content

def getFileT(myQueue,m,enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "线程函数"
    proxies = {}
    timeout = 15
##    picFilename = ''

    imgLink = myQueue.get_nowait()
##    picFilename = imgLink[imgLink.rfind('/')+1:len(imgLink)]

    try:
        getFile(fileLink=imgLink['link'],filename=imgLink['ofile'],outdir=imgLink['oDir'],m=m)
    except Exception as e:
        print('error:',e)

def getFiles(fileList,m):
    #fileList:[{'link':fullurl,'ofile':outPutfilename,'oDir':outdir},]
    for item in fileList:
        filesQueue.put(item)
    threadN = 10
    jqueue = filesQueue.qsize()
    if jqueue < threadN:
        threadN = jqueue

    threads = []
    for i in range(0,threadN):
        thread = threading.Thread(target = getFileT, args = (filesQueue,m,))
        threads.append(thread)
        thread.start()
    for thread1 in threads:
        thread1.join()

if __name__ == '__main__':
    outfilename,imgContent = getFile()
    outfile = open(outfilename,'wb')
    outfile.write(imgContent)
    outfile.close()
    print(outfilename,' be saved')
