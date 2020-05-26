#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取网页中的torrent的链接码,应用于jandown这个网站

from bs4 import BeautifulSoup
import requests

def get_torrentlink(myreq_url='https://bt.aisex.com/bt/htm_data/16/1609/860163.html',enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "从指定的网页中获取torrent的代码"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    try:
        r1 = requests.get(myreq_url,headers = headers, timeout = 15)
    except Exception as e:
        print('error:',e)
        

    soup = BeautifulSoup(r1.content,'html.parser')
    tCode = 'notExist'

    #锚点A没被放在img标签里的
    m_as = soup.find('div',id = 'read_tpc').find_all('a') #链接在read_tpc这个div里
    for m_a in m_as:
        #print m_a
        temp_href = m_a.get('href') #这个是获取<a href=...>的href值
        #print temp_href
        pos_jandown = temp_href.find('jandown') #判断是否是包含torrent代码的链接,标志是jandown这个网站
        #print pos_jandown
        if pos_jandown != -1:
            #print m_a
            #print temp_href
            #print pos_jandown
            linkpos=temp_href.find('=') #需要的torrent代码在"link.php?ref="后面
            #链接码的长度是10
            tCode = temp_href[linkpos+1:linkpos+11]

    
    #锚点A被放在了img标签里的
#        myimgs=soup.find('div',id='read_tpc').find_all('img')
    #print 'images-----------'
#        for myimg in myimgs[1:]:
        #print myimg
        #print
#            mylinks = myimg.find_all('a')
#            print u'mylink,href值'
#            myhref = mylinks[0].get('href')    #这个是输出<a href>的href值
#            print myhref
#            print 'A string------'
#            print mylinks[0].string #这个是输出<a>...</a>之间的内容
#        for mylink in mylinks:
#            print mylink.string
#            print        
#            linkpos=myhref.find('=') #需要的torrent代码在"link.php?ref="后面
        #linkpos=mylinks[0].string.find('=')
        #或者string.index('=')
#            print linkpos
        #链接码的长度是10
#            tCode = mylinks[0].string[linkpos+1:linkpos+11]
#            print tCode


    #获取img链接到列表imgs
    imgsList = []
    m_imgs = soup.find('div',id = 'read_tpc').find_all('img')
    for m_img in m_imgs:
        imgsList.append(m_img.get('src'))

    #获取title
    title = ''
    title = soup.find('h1',id = 'subject_tpc').next_element #或者.get_text() 或者.text 或者.innerHTML 或者.innerText
    title = title.strip()
    tRes = {'btCode':tCode,'title':title,'imgsList':imgsList}
    #tRes.append({'btCode':tCode,'title':title,'imgsList':imgsList})

##    return tCode,title,imgsList
    return tRes

if __name__ == '__main__':
    print(get_torrentlink(myreq_url='https://www.aisex.com/bt/htm_data/16/1609/860163.html'))
