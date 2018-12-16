from selenium import webdriver
from time import sleep
import random
from bs4 import BeautifulSoup
import re

def get_driver():
    chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path)
    return driver

def write_question(i,question,filepath):
    with open(filepath,"a",encoding="utf-8") as fw:
        fw.write(str(i)+ "." + question)

def write_answer(answer,filepath):
    with open(filepath,"a",encoding="utf-8") as fw:
        fw.write("    " + answer + "\n")

java_review_filepath = "java_review.text"
network_review_filepath = "network_review.text"

if __name__ == '__main__':
    driver = get_driver()
    # 牛客网java复习题，网络复习题
    # for i in range(1,121):
    #     driver.get("https://www.nowcoder.com/ta/review-java/review?page=" + str(i))
    #     sleep(random.randint(5,10))
    #     question = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]').text
    #     answerList = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]').text.split("\n")
    #     write_question(i,question,java_review_filepath)
    #     for answer in answerList:
    #         write_answer(answer,java_review_filepath)
    #     if i % random.randint(5,10) == 0:
    #         sleep(random.randint(30,90))
    # for j in range(1,12):
    #     driver.get("https://www.nowcoder.com/ta/review-network/review?tpId=33&tqId=21189&query=&asc=true&order=&page=" + str(j))
    #     sleep(random.randint(3, 5))
    #     question = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]').text
    #     answerList = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]').text.split("\n")
    #     write_question(j,question,network_review_filepath)
    #     for answer in answerList:
    #         write_answer(answer,network_review_filepath)
    #     if i % random.randint(5,10) == 0:
    #         sleep(random.randint(30,90))
    driver.get("http://jmjh.miit.gov.cn/newsInfoWebMessage.action?newsId=12829621&moduleId=1062")
    html = driver.page_source
    bs4_object = BeautifulSoup(html, "html.parser")
    pattern = re.compile('<div id="con_con" class="con_con">(.*?)</div>',re.S)
    rs = re.findall(pattern,html)
    print(len(rs))
    for r in rs:
        if r != None:
            print(r)
    driver.quit()
