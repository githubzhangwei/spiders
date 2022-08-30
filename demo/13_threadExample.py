import threading
from queue import Queue

import requests
from lxml import etree

"""_summary_
多线程实现数据爬虫案例
"""


class QiubaiSpider:
    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def get_url_list(self):
        for i in range(1, 3):
            self.url_queue.put(self.url_temp.format(i))

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url, header=self.headers)
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()

    def get_content_list(self):
        html_str = self.html_queue.get()
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@id='content-left']/div")
        content_list = []
        for div in div_list:
            item = {}
            item["content"] = div.xpath(".//div[@class='content']/span/text()")
            item["author_gender"] = div.xpath(
                ".//div[contains(@class,'articleGender')/@class")
            item["author_gender"] = item["author_gender"][0].split(
                " ")[-1].replace("Icon", "") if len(item["author_gender"]) > 0 else ""
            content_list.append(item)
        self.content_queue.put(content_list)
        self.content_queue.task_done()

    def save_content_list(self):
        while True:
            content_list = self.content_queue.get()
            for i in content_list:
                print(i)
            self.content_queue.task_done()

    def run(self):
        thread_list = []
        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)

        for i in range(10):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)

        for i in range(2):
            t_html = threading.Thread(target=self.get_content_list)
            thread_list.append(t_html)

        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)

        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，该线程不重要主线程结束，子线程结束
            t.start()

        for q in (self.url_queue, self.html_queue, self.content_queue):
            q.join()  # 让主线程等待阻塞，等待队列的任务完成之后再完成

        print("主线程结束")


if __name__ == "__main__":
    qiubai = QiubaiSpider()
    qiubai.run()
