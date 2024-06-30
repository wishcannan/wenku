from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import re
import requests
 
class wenkupool():
    __filename = './book/'
    __headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    def __init__(self,bookname) -> None:
        self.__bookname = bookname
        self.__chaptname = ''
        self.q = 0
        self.l = 0

    def done(self,chaptname:str='',data:list = []):
        self.__chaptname = chaptname
        self.l = len(data)
        num = self.l//4
        executor = ThreadPoolExecutor(max_workers=num)
        results = executor.map(self.__downimg,data)
        executor.shutdown()
        print(f'{chaptname}图片下载完成')
        self.q = 0



    def __downimg(self,i:str):#url
        pattern = re.compile("^https?:\\/\\/[^:<>\"]*\\/(\\d+)\\.((png)|(jpg)|(webp)|(jpeg))$")
        matchobj = pattern.match(i)
        imgname:str = str(matchobj.group(1))
        imgtype = matchobj.group(2)
        with open(self.__filename+self.__bookname+'/'+self.__chaptname+'/'+imgname+'.'+imgtype,'wb') as f:
            res = requests.get(url=i,headers=self.__headers)#访问图片也要带header
            if res.status_code == 200:
                f.write(res.content)
        self.q += 1
        print(f'下载完成{i},进度{self.q}/{self.l}')
        return i

# print(14//5)