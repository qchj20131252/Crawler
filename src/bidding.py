from selenium import webdriver
from time import sleep
import random
from bs4 import BeautifulSoup
import re


# 省采购公告
province_bidding_url = "http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&moreType=provincebuyBulletinMore&channelCode=sjcg1&rp=25&page="
# 市县级采购公告
city_bidding_url = "http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&moreType=provincebuyBulletinMore&channelCode=sjcg2&rp=25&page="
# 省采购公告url存储文件路径
province_bidding_url_file_path = "E:/PycharmProjects/Crawler/src/resource/province_bidding_url.txt"
# 市县级采购公告url存储文件路径
city_bidding_url_file_path = "E:/PycharmProjects/Crawler/src/resource/city_bidding_url.txt"

def get_driver():
    chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path)
    return driver

def get_bs4_object(driver):
    html = driver.page_source
    bs4_object = BeautifulSoup(html, "html.parser")
    return bs4_object

# 获取采购公告url
def get_bidding_url(url,url_file_path,page_num):
    driver = get_driver()
    for i in range(1,page_num):
        while i%10 == 0:
            sleep(random.randint(30,60))
        driver.get(url + str(i))
        sleep(10)
        bs4_object = get_bs4_object(driver)
        html = str(bs4_object)
        pattern = re.compile('<li>.*?<div class="time curr.*?<span>(.*?)</span>(.*?)</div>.*?<a href="(.*?)".*?title="(.*?)".*?</li>',re.S)
        bidding_url_list = re.findall(pattern,html)
        print(len(bidding_url_list))
        for bidding_url in bidding_url_list:
            if "html" in bidding_url[0]:
                write_url(province_bidding_url_file_path, bidding_url[2].split("/")[-2] + "," + bidding_url[2] + "," + bidding_url[3])
            else:
                write_url(province_bidding_url_file_path, bidding_url[1].strip() + "-" + bidding_url[0] + "," + bidding_url[2].replace("amp;","") + "," + bidding_url[3])
        print(i)
        break
    driver.quit()
# 写入url文件
def write_url(file_path,url):
    with open(file_path,"a",encoding="utf-8") as fw:
        fw.write(url + "\n")

if __name__ == '__main__':
    # 获取省级采购公告url
    get_bidding_url(province_bidding_url,province_bidding_url_file_path,793)
    # 获取市县级采购公告
    # get_bidding_url(city_bidding_url,city_bidding_url_file_path,)