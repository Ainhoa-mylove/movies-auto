import requests
from lxml import etree
import time
from fake_useragent import UserAgent
from threading import Thread


f=open('movie_info.text','a+')
class crawler():
    def __init__(self):
        self.url='https://www.80s.tw/movie/list'
        ua=UserAgent()
        self.headers={
            'UserAgent':ua.random
        }
    def do_request(self,url):
        req=requests.get(
        url=url,
        headers=self.headers
        ).content.decode('utf-8')
        return req

    def do_analysis(self):
        req=self.do_request(self.url)
        s=etree.HTML(req)
        html_data=s.xpath('//div[@class="clearfix noborder block1"]/ul[2]//li')
        for li in html_data:
            number=li.xpath('./h3/a/@href')[0].strip()
            number1=number.split('/')[2]
            name=li.xpath('./h3//a/text()')[0].strip()
            date=self.get_twopage(number1)
            data_list=(name,date)
            for list in data_list:
                print('开始写入！！')
                f.write(list+' ')
            f.write('\n')
        f.close()

    def get_twopage(self,number):
        url='https://www.80s.tw/movie/{}'.format(number)
        response=self.do_request(url)
        s=etree.HTML(response)
        movie_actor=[]
        two_html=s.xpath('//div[@id="minfo"]')
        for li in two_html:
            actor=li.xpath('./div[2]/span[3]/a/text()')
            for i in actor:
                movie_actor.append(i)
            date=li.xpath('./div[2]/div[1]/span[5]/text()')[0].strip()
            return date

    def main(self):
        t = Thread(target=self.do_analysis())
        t.daemon=True
        t.start()
        t.join()

if __name__ == '__main__':
    start=time.time()
    c=crawler()
    c.main()
    end=time.time()
    print('执行时间：%.2f' % (end - start))
