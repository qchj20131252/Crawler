from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json
import time
import random

base_info_url_file_path = "E:/PycharmProjects/Crawler/src/resource/base_info_url.txt"
partner_file_path = "E:/PycharmProjects/Crawler/src/resource/partners.json"
business_info_file_path = "E:/PycharmProjects/Crawler/src/resource/business_info.json"
mainmember_file_path = "E:/PycharmProjects/Crawler/src/resource/mainmembers.json"
error_log_file_path = "E:/PycharmProjects/Crawler/src/resource/error_log.txt"

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

def write_error_log(error_info):
    with open(error_log_file_path,"a",encoding="utf-8") as fw:
        fw.write(error_info)

def login(driver):
    driver.get("https://www.qichacha.com/user_login")

def get_company_name(driver):
    company_name = driver.find_element_by_xpath('//*[@id="company-top"]/div[1]/div[2]/div[1]/h1').text
    return company_name

def get_bs4_object(driver):
    html = driver.page_source
    bs4_object = BeautifulSoup(html, "html.parser")
    return bs4_object

def get_business_info(driver):
    business_info = {}
    xpaths ={u'公司名称':'//*[@id="company-top"]/div/div[2]/div[1]/h1',u'法定代表人':'//*[@id="Cominfo"]/table[1]/tbody/tr[2]/td[1]/div/div[1]/div[2]/a[1]',
            u'注册资本':'//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[2]',u'实缴资本':'//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[4]',
            u'经营状态':'//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[2]',u'成立日期':'//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[4]',
            u'注册号':'//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]',u'组织机构代码':'//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[4]',
            u'纳税人识别号':'//*[@id="Cominfo"]/table[2]/tbody/tr[4]/td[2]',u'统一社会信用代码':'//*[@id="Cominfo"]/table[2]/tbody/tr[4]/td[4]',
            u'公司类型':'//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[2]',u'所属行业':'//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[4]',
            u'核准日期':'//*[@id="Cominfo"]/table[2]/tbody/tr[6]/td[2]',u'登记机关':'//*[@id="Cominfo"]/table[2]/tbody/tr[6]/td[4]',
            u'所属地区':'//*[@id="Cominfo"]/table[2]/tbody/tr[7]/td[2]',u'英文名':'//*[@id="Cominfo"]/table[2]/tbody/tr[7]/td[4]',
            u'曾用名':'//*[@id="Cominfo"]/table[2]/tbody/tr[8]/td[2]',u'参保人数':'//*[@id="Cominfo"]/table[2]/tbody/tr[8]/td[4]',
            u'人员规模':'//*[@id="Cominfo"]/table[2]/tbody/tr[9]/td[2]',u'营业期限':'//*[@id="Cominfo"]/table[2]/tbody/tr[9]/td[4]',
            u'企业地址':'//*[@id="Cominfo"]/table[2]/tbody/tr[10]/td[2]','经营范围':'//*[@id="Cominfo"]/table[2]/tbody/tr[11]/td[2]'}
    keys = list(xpaths.keys())
    for key in keys:
        try:
            business_info[key] = driver.find_element_by_xpath(xpaths[key]).text.strip()
        except:
            business_info[key] = "-"
    write_json_file(business_info,business_info_file_path)

def get_partners(driver,bs4_object,company_name):
    try:
        partner_table = str(bs4_object.select('#Sockinfo')[0])
        pattern_title = re.compile('<th.*?>(.*?)</th>',re.S)
        titles = re.findall(pattern_title,partner_table)
        regex = '<tr.*?<td.*?>(.*?)</td.*?<td.*?h3.*?>(.*?)</h3.*?/td.*?'
        for i in range(len(titles) - 2):
            regex += '<td.*?>(.*?)<.*?'
        regex += '/tr>'
        pattern_attrs = re.compile(regex,re.S)
        attrs = re.findall(pattern_attrs,partner_table)
        partner_info = {}
        for attr in attrs:
            partner_info['公司名称'] = company_name
            for i in range(1,len(titles)):
                partner_info[titles[i]] = attr[i].strip()
            write_json_file(partner_info,partner_file_path)
            partner_info = {}
    except IndexError:
        error_info = company_name+"无主要人员信息\n"
        write_error_log(error_info)
        pass

def get_mainmembers(driver,bs4_object,company_name):
    try:
        mainmember_table = str(bs4_object.select('#Mainmember')[0])
        pattern_title = re.compile('<th.*?>(.*?)</th>', re.S)
        titles = re.findall(pattern_title, mainmember_table)
        pattern_mainmember = re.compile('<tr.*?<td.*?>(.*?)</td.*?<td.*?h3.*?>(.*?)</h3.*?/td.*?<td.*?>(.*?)<.*?/tr>',re.S)
        members = re.findall(pattern_mainmember,mainmember_table)
        members_dict = {}
        for member in members:
            members_dict["公司名称"] = company_name
            for i in range(1,len(titles)):
                members_dict[titles[i]] = member[i].strip()
            write_json_file(members_dict,mainmember_file_path)
            members_dict = {}
    except IndexError:
        error_info = company_name+"无股东信息\n"
        write_error_log(error_info)
        pass

def main():
    driver = get_driver()
    urls = get_urls(base_info_url_file_path)

    login(driver)
    time.sleep(15)

    for i in range(3414,len(urls)):
        driver.get(urls[i].strip())
        company_name = get_company_name(driver)
        bs4_object = get_bs4_object(driver)
        get_business_info(driver)
        get_partners(driver,bs4_object,company_name)
        get_mainmembers(driver,bs4_object,company_name)
        print(i+1)
        time.sleep(random.randint(10,30))
        if i%random.randint(50,100) == 0:
            time.sleep(random.randint(120,300))

    driver.quit()



if __name__ == '__main__':
    main()