'''
爬取快代理，建立自己的IP池（国内高匿代理），并存储到MongoDB数据库中
'''
import random
import pymongo
import requests
from lxml import etree
import time

class KuaiDaiLiSpider:

    def __init__(self):
        self.url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.test_url = 'http://www.baidu.com'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
        self.conn = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.conn['ipdb']
        self.myset = self.db['ipset']

    def get_proxy(self, url):
        html = requests.get(url=url, headers=self.headers).text
        p = etree.HTML(html)
        # 先写基准的xpath
        tr_list = p.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for tr in tr_list:
            ip = tr.xpath('./td[1]/text()')[0].strip()
            port = tr.xpath('./td[2]/text()')[0].strip()
            # 测试代理是否可用
            self.test_proxy(ip, port)

    def test_proxy(self, ip, port):
        # 测试一个高匿代理IP是否可用
        proxies = {
            'http': 'http://{}:{}'.format(ip, port),
            'https': 'https://{}:{}'.format(ip, port)
        }
        try:
            res = requests.get(url=self.test_url, proxies=proxies, headers=self.headers)
            if res.status_code == 200:
                ip_item = {}
                print(ip, port, '\033[31m可用\033[0m')
                ip_item['ip'] = ip
                ip_item['port'] = port
                ip_item['valid'] = '可用'
                self.myset.insert_one(ip_item)
        except Exception as e:
            print(ip, port, "不可用")

    def run(self):
        for i in range(1, 4425):
            url = self.url.format(i)
            self.get_proxy(url)
            time.sleep(random.uniform(2, 3))


if __name__ == '__main__':

    spider = KuaiDaiLiSpider()
    spider.run()
















# //table[@class="table table-bordered table-striped"]/tbody/tr/td[1]/text()