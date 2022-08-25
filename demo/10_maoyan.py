import random

import requests
from lxml import etree

from ua_info import ua_list

# coding:utf8


class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://m.maoyan.com/#movie/classic'
        self.headers = {'User-Agent': random.choice(ua_list)}

    def save_html(self):
        html = requests.get(url=self.url, headers=self.headers).text
        parse_html = etree.HTML(html)
        # 基准 xpath 表达式，匹配10个<dd>节点对象
        dd_list = parse_html.xpath(
            '//div[@class="title line-ellipsis"]/span/text()')
        print(dd_list)
        exit()
        # 构建item空字典将提取的数据放入其中
        item = {}
        for dd in dd_list:
            # 处理字典数据，注意xpath表达式匹配结果是一个列表，因此需要索引[0]提取数据
            item['name'] = dd.xpath(
                './/div[contains(@class,"title")]/text()')
            item['actor'] = dd.xpath(
                './/div[contains(@class,"actor")]/text()')
            item['score'] = dd.xpath(
                './/span[@class="grade"]/text()')
            # 输出数据
            print(item)

    def run(self):
        self.save_html()


if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.run()
