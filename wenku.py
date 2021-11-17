import re
import requests
from requests.api import get
from requests.cookies import RequestsCookieJar
from requests.models import Response
import re
from bs4 import BeautifulSoup
import os
class wenku8:
    def __init__(self):
        self.cookies = RequestsCookieJar()
        self.userAgent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        #答应我用自己的电脑好吗？
        self.Headers = {
            "origin": "https://www.wenku8.net",
            "referer": "https://www.wenku8.net/login.php",
            "user-agent": self.userAgent}
        self.filename = './book/'
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        
    def response_text(self,url):
            """请求函数"""
            response = requests.get(url,headers=self.Headers,cookies=self.cookies) # 发送请求带入cookies
            if response.status_code==200:
                response.encoding="gbk"
            result = response.text
            self.cookies.update(response.cookies) #更新cookies
            return result

    def wenkulogin(self,account,password):
        postUrl = 'https://www.wenku8.net/login.php?do=submit'
        postData = {
            "username":account,
            "password":password,
            "usecookie": 86400,#86400 一天 315360000一年 0 浏览器进程
            "action": 'login'
        }
        response = requests.post(postUrl,data=postData,headers=self.Headers)
        # print(f"statusCode = {response.status_code}")
        if response.status_code==200:
            response.encoding="gbk"
        self.cookies.update(response.cookies)
        # return response.text
        print("登录成功")

    def bookcase(self):
        url = 'https://www.wenku8.net/modules/article/bookcase.php'
        r = requests.get(url,headers=self.Headers,cookies=self.cookies)
        if r.status_code==200:
            r.encoding="gbk"
        self.cookies.update(r.cookies)
        print("bookcase"+"\n"+r.text)

    def getbook(self,bookurl):
        bookid = self.getbookid(bookurl)
        a = int(int(bookid) // 1000)
        booknovel = "https://www.wenku8.net/novel/{}/{}/index.htm".format(a,bookid)
        print(booknovel+"这次要看的书")
        bookrespronse = requests.get(booknovel,headers=self.Headers,cookies=self.cookies)
        bookrespronse.encoding = "gbk"
        soup = BeautifulSoup(bookrespronse.text,'html.parser')
        bookname = soup.find('div',id="title").string#获取标题
        print(bookname)
        if not os.path.exists(self.filename+bookname):
            os.mkdir(self.filename+bookname)
        #获取章节
        all_chapter = soup.find('table')
        # print('all_chapter',all_chapter)
        self.getchapter(all_chapter,bookname,int(bookid))



    def getbookid(self,s):
        return re.split('\W+',s)[-2]
    def getchapter(self,all_chapter,bookname,bookid):
        a = int(bookid // 1000)
        filename = self.filename + bookname + '/'
        filename1 = ''
        tr_list = all_chapter.find_all('tr')
        for i in tr_list:
            td_list = i.find_all('td')
            print('td_list',td_list)
            for j in td_list:
                # print(j['class'])
                if j['class'][0] == 'vcss':
                    # print(j.text)
                    filename1 = filename+j.string
                    if not os.path.exists(filename1):
                        os.mkdir(filename1)
                    continue
                else:
                    if j.a != None:
                        s = j.a['href'][:-4]
                        self.gettxt('https://www.wenku8.net/novel/{}/{}/{}.htm'.format(a,bookid,s),filename1)
        return

    def gettxt(self,url,filename):#获取章节内容并写入 
        a = self.response_text(url)
        soup = BeautifulSoup(a,'html.parser')
        chapter_title = soup.find('div',id='title').string
        soup1 = soup.find("div",id='content')
        if soup1.div != None:
            self.getimage(url,filename)
        else:
            for ul in soup1.find_all('ul'):
                ul.decompose()
            filename = filename + '/{}'.format(chapter_title)+'.txt'
            with open(filename,'w+',encoding="utf-8") as f:
                f.write(chapter_title)
                f.write(soup1.get_text())
            f.close()
        return chapter_title+'ok'
    
    def getimage(self,url,filename):
        a = self.response_text(url)
        soup = BeautifulSoup(a,'html.parser')
        chapter_title = soup.find('div',id='title').string
        soup = soup.find("div",id='content')
        imagelist = soup.find_all('div',class_="divimage")
        for i in imagelist:
            img_href = i.a.img['src']
            # print(i.a.img['src'])
            self.saveimage(img_href,filename)
        return chapter_title+'ok'

    def saveimage(self,url,filename):
        # os.chdir(filename)
        r = requests.get(url,headers=self.Headers,cookies=self.cookies,timeout=100)
        p = re.split('\W+',url)
        file_path = filename + '/' + p[-2] + '.' + p[-1]
        with open(file_path,"wb") as f:
            f.write(r.content)
        f.close


WK = wenku8()
# WK.wenkulogin('你的账号','你的密码')
# WK.getbook('https://www.wenku8.net/book/3058.htm')
WK.getbook('https://www.wenku8.net/book/3032.htm')