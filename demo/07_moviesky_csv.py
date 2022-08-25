import csv
import random
import re
import ssl
import time
from urllib import request

from ua_info import ua_list


# 定义一个爬虫类
class MaoyanSpider(object):
    # 初始化
    # 定义初始页面url
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.url = 'https://www.dytt8.net/html/gndy/dyzz/index.html'  # 天堂电影
        self.url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    # 请求函数

    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        req = request.Request(url=url, headers=headers)
        context = ssl._create_unverified_context()
        res = request.urlopen(req, context=context)
        html = res.read().decode('GBK')
        # 直接调用解析函数
        self.parse_html(html)

    # 解析函数
    def parse_html(self, html):
        # 正则表达式
        re_bds = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>'
        re_bds = r'<table.*?<a.*?>(.*?)</a>.*?<font.*?>(.*?)</font>.*?/table>'
        # 生成正则表达式对象
        pattern = re.compile(re_bds, re.S)
        r_list = pattern.findall(html)
        self.save_html(r_list)

    # 保存数据函数，使用python内置csv模块
    def save_html(self, r_list):
        # 生成文件对象
        with open('dytt8.net.csv', 'a', newline='', encoding="GBK") as f:
            # 生成csv操作对象
            writer = csv.writer(f)
            # 整理数据
            for r in r_list:
                name = r[0].strip()
                # 日期：2022-08-19 23:28:20
                # 切片截取时间
                time = r[1].strip()[3:]
                L = [name, time]
                # 写入csv文件
                writer.writerow(L)
                print(name, time)

    # 主函数
    def run(self):
        # 抓取第一页数据
        for offset in range(1, 5, 8):
            url = self.url.format(offset)
            self.get_html(url)
            # 生成1-2之间的浮点数
            time.sleep(random.uniform(1, 2))


# 以脚本方式启动
if __name__ == '__main__':
    # 捕捉异常错误
    try:
        spider = MaoyanSpider()
        spider.run()
    except Exception as e:
        print("错误:", e)
