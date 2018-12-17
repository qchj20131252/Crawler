from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json
import time
import random
from pymongo import MongoClient
from urllib.parse import quote

literatur_url_log_file_path = "E:/PycharmProjects/Crawler/src/resource/literature_url_log.txt"

def get_mongodb_connection():
    client = MongoClient("202.115.161.211",8042)
    db_auth = client.admin
    db_auth.authenticate('rw_m', 'Db_rw')
    db = client["qcj_companyInfo"]
    return db

def get_driver():
    chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path)
    return driver

def get_bs4_object(driver):
    html = driver.page_source
    bs4_object = BeautifulSoup(html, "html.parser")
    return bs4_object

def write_log(filepath,content):
    with open(filepath,"a",encoding="utf-8") as fw:
        fw.write(content + "\n")

if __name__ == '__main__':
    db = get_mongodb_connection()
    collection = db["company_profile"]
    literature_url_collection = db["literature_url"]
    company_profiles = collection.find()
    driver = get_driver()
    company_list = []
    for company_profile in company_profiles:
        company_list.append(company_profile["companyName"])
    print("导出完成！！")
    print(company_list[-1])
    for company in company_list:
        print(company)
        driver.get("http://old.wanfangdata.com.cn/")
        query_input = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/input')
        submit = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/button')
        keyword = "作者单位:" + company
        query_input.send_keys(keyword)
        submit.click()
        while True:
            pattern = re.compile(
                    '<div class="record-item">.*?<div class="record-title">.*?<a class="title" href="(.*?)".*?>(.*?)</a>.*?</div>',
                    re.S)
            bs4_object = get_bs4_object(driver)
            html = str(bs4_object)
            rs = re.findall(pattern, html)
            if len(rs) == 0:
                log = company + "，无相关科技文献"
                write_log(literatur_url_log_file_path,log)
                break
            for r in rs:
                literature_url_collection.insert_one({"companyName":company,"url":r[0],"document_name":r[1]})

            try:
                next_page_button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/p/a[5]')
                next_page_button.click()
            except:
                break
    print("科技文献url收集完成!!!")


