# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By


class DouyuSpider(object):
    def __init__(self):
        self.start_url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()

    def get_content_list(self):
        li_list = self.driver.find_elements(
            by=By.XPATH, value=r'//ul[@class="layout-Cover-list"]/li')

        content_list = []
        for li in li_list:
            item = {}
            item["room_img"] = li.find_element(
                by=By.XPATH, value=r'.//img[contains(@class,"DyImg-content")]/').get_attribute("src")
            item["room_title"] = li.find_element(
                by=By.XPATH, value=r'.//span[@class="DyListCover-zone"]').text
            item["anchor_name"] = li.find_element(
                by=By.XPATH, value=r'.//div[@class="DyListCover-userName"]').text
            item["watch_num"] = li.find_element(
                by=By.XPATH, value=r'.//span[@class="DyListCover-hot"]').text
            content_list.append(item)
            print(item)
        next_url = self.driver.li.find_element(
            by=By.XPATH, value=r'//a[@class="dy-Pagination-item-custom"]')
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content_list(self, content_list):
        pass

    def run(self):
        # start_url
        # 发送请求，获取响应
        self.driver.get(self.start_url)
        # 提取数据，获取下一页的元素
        content_list, next_url = self.get_content_list()
        # 保存数句
        self.save_content_list(content_list)
        # 点击下一页循环
        while next_url is not None:
            next_url.click()
            content_list, next_url = self.get_content_list()
            self.save_content_list(content_list)


if __name__ == '__main__':
    dou_yu = DouyuSpider()
    dou_yu.run()
