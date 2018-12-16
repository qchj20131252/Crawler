from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote
import math
import re
import json
import time
import random

def get_driver():
    chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path)
    return driver

def get_urls(url_file_path):
    with open(url_file_path, 'r') as f:
        urls = f.readlines()
    return urls

def write_json_file(partner_dict,filepath):
    json_str = json.dumps(partner_dict, ensure_ascii=False) + '\n'
    with open(filepath, "a", encoding="utf8") as fw:
        fw.write(json_str)

def write_company_name_file(company_name_file_path,company_name):
    with open(company_name_file_path,"a",encoding="utf-8") as fw:
        fw.write(company_name + '\n')

def login(driver):
    driver.get("https://www.qichacha.com/user_login")

def get_bs4_object(driver):
    html = driver.page_source
    bs4_object = BeautifulSoup(html, "html.parser")
    return bs4_object

def get_software_copyright(bs4_object,company_name):
    software_copyright_html = str(bs4_object)
    software_copyright_pattern = re.compile('<tr.*?td class="tx">(.*?)</td.*?td width="278">(.*?)</td.*?td>(.*?)</td.*?td width="102">(.*?)</td.*?td width="140">(.*?)</td.*?td>(.*?)</td.*?td>(.*?)</td.*?/tr>',re.S)
    software_copyrights = re.findall(software_copyright_pattern,software_copyright_html)
    software_copyright_titles = ['软件名称','版本号','发布日期','软件简称','登记号','登记批准日期']
    for software_copyright in software_copyrights:
        software_copyright_dict = {'公司名称':company_name}
        for i in range(len(software_copyright_titles)):
            software_copyright_dict[software_copyright_titles[i]] = software_copyright[i+1]
        write_json_file(software_copyright_dict,software_copyright_file_path)



def get_work_copyright(bs4_object,company_name):
    work_copyright_html = str(bs4_object)
    work_copyright_pattern = re.compile('<td.*?>(.*?)</td.*?<td.*?>(.*?)</td.*?<td.*?>(.*?)</td.*?<td.*?>(.*?)</td.*?<td>(.*?)</td.*?<td.*?>(.*?)</td.*?<td.*?>(.*?)</td>',re.S)
    work_copyrights = re.findall(work_copyright_pattern,work_copyright_html)
    work_copyright_titles = ['作品名称','首次发表日期','创作完成日期','登记号','登记日期','登记类别']
    for work_copyright in work_copyrights:
        work_copyright_dict = {'公司名称': company_name}
        for i in range(len(work_copyright_titles)):
            work_copyright_dict[work_copyright_titles[i]] = work_copyright[i + 1]
        write_json_file(work_copyright_dict, work_copyright_file_path)


def write_copyright_error_log(copyright_error_log_file_path,copyright_error_log):
    with open(copyright_error_log_file_path,"a",encoding="utf-8") as fw:
        fw.write(copyright_error_log + '\n')


def main(start):
    urls = get_urls(copyright_url_file_path)
    # urls = ['https://www.qichacha.com/cassets_32958fee409855508cb1cf375cbb34a6']
    driver = get_driver()
    login(driver)
    time.sleep(15)
    for i in range(start,len(urls)):
        driver.get(urls[i])
        time.sleep(5)
        company_name = driver.find_element_by_xpath('//*[@id="company-top"]/div[1]/div[2]/div[1]/h1').text
        write_company_name_file(company_name_file_path,company_name)

        software_copyright_number = int(driver.find_element_by_xpath('//*[@id="assets_div"]/section[1]/div/a[5]').text.split(' ')[1].strip())
        work_copyright_number = int(driver.find_element_by_xpath('//*[@id="assets_div"]/section[1]/div/a[4]').text.split(' ')[1].strip())

        # 查看当前公司有无软件著作权，有的话拼接url爬取，没有的话爬取下一条信息

        if software_copyright_number == 0:
            software_copyright_error_log = company_name + "无软件著作权或者网页未加载或跳转失败"
            write_copyright_error_log(copyright_error_log_file_path,software_copyright_error_log)
        else:
            for j in range(1, math.ceil(software_copyright_number / 10) + 1):
                software_copyright_url = 'https://www.qichacha.com/company_getinfos?unique=' + urls[i].split('_')[1] + '&companyname=' + quote(company_name) + '&p=' + str(j) + '&tab=assets&box=rjzzq'
                driver.get(software_copyright_url)
                time.sleep(3)
                software_copyright_bs4_object = get_bs4_object(driver)
                get_software_copyright(software_copyright_bs4_object, company_name)
                time.sleep(random.randint(3,5))

        # 查看当前公司有无作品著作权，有的话拼接url爬取，没有的话爬取下一条信息

        if work_copyright_number == 0:
            work_copyright_error_log = company_name + "无作品著作权或者网页未加载或跳转失败"
            write_copyright_error_log(copyright_error_log_file_path,work_copyright_error_log)
        else:
            for j in range(1, math.ceil(work_copyright_number / 10) + 1):
                work_copyright_url = 'https://www.qichacha.com/company_getinfos?unique=' + urls[i].split('_')[1] + '&companyname=' + quote(company_name) + '&p=' + str(j) + '&tab=assets&box=zzq'
                driver.get(work_copyright_url)
                time.sleep(3)
                work_copyright_bs4_object = get_bs4_object(driver)
                get_work_copyright(work_copyright_bs4_object, company_name)
                time.sleep(random.randint(3,5))

        print(i + 1)

        if i%random.randint(30,50) == 0:
            time.sleep(random.randint(30,60))

    driver.quit()

copyright_url_file_path = "E:/PycharmProjects/Crawler/src/resource/copyright_url.txt"
company_name_file_path = "E:/PycharmProjects/Crawler/src/resource/company_name.txt"
copyright_error_log_file_path = "E:/PycharmProjects/Crawler/src/resource/copyright_error_log.txt"
software_copyright_file_path = "E:/PycharmProjects/Crawler/src/resource/software_copyright.txt"
work_copyright_file_path = "E:/PycharmProjects/Crawler/src/resource/work_copyright.txt"
teng = '17378579620 11/13 500+'
ye = '18482116959 11/14 500+'
chen = '15996166342 11/14 600+'
su = '18681692529 11/14 600+'
if __name__ == '__main__':
    start = 3401
    main(start)