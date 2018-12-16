from selenium import webdriver
from time import sleep
import random
from bs4 import BeautifulSoup
import re

def get_driver():
    chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path)
    return driver

if __name__ == '__main__':
    driver = get_driver()
    driver.get("http://www.ccgp-sichuan.gov.cn/view/staticpags/shiji_jggg/40288687657ff75501678168d9783fe5.html")
    name = driver.find_element_by_xpath('//*[@id="myPrintArea"]/table/tbody/tr[2]/td[2]').text
    print(name)
    sleep(10)
    driver.quit()