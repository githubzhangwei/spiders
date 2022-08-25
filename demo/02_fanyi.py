# coding=utf-8
import json
import sys

import requests


class FanyiSpider:
    def __init__(self, trans_str):
        self.trans_str = trans_str
        self.lang_detect_url = "https://fanyi.baidu.com/langdetect"
        # "https://fanyi.baidu.com/basetrans"
        self.trans_url = "https://cn.bing.com/ttranslatev3?isVertical=1&&IG=69AE79EB80F34E39A33C0574E30DF1FE&IID=translator.5025.1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }

    def parse_url(self, url, post_data):
        response = requests.post(url, data=post_data, headers=self.headers)
        assert response.status_code == 200
        return json.loads(response.content.decode())

    def get_ret(self, dict_response):
        #ret = dict_response["trans"][0]["dst"]
        print(dict_response)

    def run(self):
        # 获取语言类型
        lang_detect_data = {"query": self.trans_str}
        lang = self.parse_url(self.lang_detect_url, lang_detect_data)["lan"]
        # 准备post数据
        trans_data = {"from": "zh", "to": "en", "query": self.trans_str} if lang == "zh" else \
            {"from": "en", "to": "zh", "query": self.trans_str}

        trans_data = {"fromLang": "auto-detect", "to": "en", "text": self.trans_str} if lang == "zh" else \
            {"fromLang": "auto-detect", "to": "zh", "text": self.trans_str}
        # 发送请求获取响应
        dict_response = self.parse_url(self.trans_url, trans_data)
        # 提取翻译结果
        self.get_ret(dict_response)


if __name__ == "__main__":
    trans_str = sys.argv[1]
    baidu_fanyi = FanyiSpider(trans_str)
    baidu_fanyi.run()
