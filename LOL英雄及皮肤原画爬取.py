#!/usr/bin/env python 
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml import etree
from selenium import webdriver
import os
import json

class LOLSkins():
    def __init__(self):
        self.start_url = 'https://lol.qq.com/data/info-heros.shtml'
        self.driver = webdriver.Chrome()

    def get_hero_num(self):
        li_list = self.driver.find_elements_by_xpath('//*[@id="jSearchHeroDiv"]/li')
        hero_nums = []
        for li in li_list:
            hero_url = li.find_element_by_xpath('./a').get_attribute('href')
            hero_num = hero_url.split('=')[-1]
            hero_nums.append(hero_num)
        return hero_nums
        # print(hero_nums)

    def get_true_url(self):
        true_urls = []
        hero_nums = self.get_hero_num()
        for i in hero_nums:
            true_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + i + '.js'
            true_urls.append(true_url)
        return true_urls
        # print(true_urls)

    def get_skins(self):
        true_urls = self.get_true_url()
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.111Safari / 537.36'
        }
        json_list = []
        for url in true_urls:
            response = requests.get(url=url, headers=headers).text
            data = json.loads(response)
            hero_skins_list = data['skins']
            json_list.append(hero_skins_list)
        return json_list
        # print(json_list)

    def save_data(self):
        json_list = self.get_skins()
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.111Safari / 537.36'
        }
        for json in json_list:
            os.mkdir('/LOL皮肤原画/' + json[0]['heroName'] + '--' + json[0]['heroTitle'])
            os.chdir('/LOL皮肤原画/' + json[0]['heroName'] + '--' + json[0]['heroTitle'])
            for i in json:
                try:
                    with open(str(i['name']) + '.jpg', 'wb') as fp:
                            skin = requests.get(i['mainImg'], headers=headers).content
                            fp.write(skin)
                            fp.close()
                except:
                    pass
                continue

    def run(self):
        self.driver.get(self.start_url)
        self.get_hero_num()
        self.get_true_url()
        self.get_skins()
        if not os.path.exists('./LOL皮肤原画'):
            os.mkdir('./LOL皮肤原画')
        self.save_data()
        self.driver.quit()

if __name__ == '__main__':
    lol = LOLSkins()
    lol.run()
