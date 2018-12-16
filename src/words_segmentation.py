import jieba
from pymongo import  MongoClient

def get_collection(collection_name):
    client = MongoClient("202.115.161.211", 8042)
    db_auth = client.admin
    db_auth.authenticate('rw_m', 'Db_rw')
    db = client['qcj_companyInfo']
    collection = db[collection_name]
    return collection

def stopwordlist(filepath):
    with open(filepath,"r",encoding="utf-8") as fr:
        lines = fr.readlines()
    stopwords = [line.strip() for line in lines]
    return stopwords

def word_segmentation(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordlist('stopword.txt')  # 这里加载停用词的路径
    outLsit = []
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outLsit.append(word)
    return outLsit

def get_keywords(collection_name,separation_sign,key_name,another_collection_name):
    news_collection = get_collection(collection_name)
    info_dict = {}
    for info in news_collection.find():
        if key_name not in info:
            continue
        keys = info[key_name].strip().split(separation_sign)
        for key in keys:
            if key != None and key != "":
                if key in info_dict:
                    info_dict[key] = info_dict[key] + 1
                else:
                    info_dict[key] = 1

    copyright_collection = get_collection(another_collection_name)
    for keyword in list(info_dict.keys()):
        copyright_collection.insert_one({"word":keyword,"frequency":info_dict[keyword]})

def get_news_keywords():
    news_collection = get_collection("news")
    news_dict = {}
    for news_info in news_collection.find():
        keys = news_info["keys"].strip().split(";")
        for key in keys:
            if key != None and key != "":
                if key in news_dict:
                    news_dict[key] = news_dict[key] + 1
                else:
                    news_dict[key] = 1

    copyright_collection = get_collection("news_keywords")
    for keyword in list(news_dict.keys()):
        copyright_collection.insert_one({"word":keyword,"frequency":news_dict[keyword]})

def get_recruit():
    col = get_collection("recruit")
    recruit_dict = {}
    for info in col.find():
        if info["position"] in recruit_dict:
            recruit_dict[info["position"]] = recruit_dict[info["position"]] + 1
        else:
            recruit_dict[info["position"]] = 1

    recruit_keywords = get_collection("recruit_keywords")
    for keyword in list(recruit_dict.keys()):
        recruit_keywords.insert_one({"word":keyword,"frequency":recruit_dict[keyword]})


def get_copyright_keywords():
    software_collection = get_collection("software_copyright_keywords")
    copyright_dict = {}
    for info in software_collection.find():
        if info["word"] in copyright_dict:
            copyright_dict[info["word"]] = copyright_dict[info["word"]] + info["frequency"]
        else:
            copyright_dict[info["word"]] = info["frequency"]

    work_collection = get_collection("work_copyright")
    for work_info in work_collection.find():
        outList = word_segmentation(work_info["workName"])
        for word in outList:
            if word in copyright_dict:
                copyright_dict[word] = copyright_dict[word] + 1
            else:
                copyright_dict[word] = 1

    copyright_collection = get_collection("copyright_keywords")
    for keyword in list(copyright_dict.keys()):
        copyright_collection.insert_one({"word":keyword,"frequency":copyright_dict[keyword]})

def get_company_list():
    company_list = []
    company_result = get_collection("company_profile").find()
    for company_obj in company_result:
        company_list.append(company_obj["companyName"])
    return company_list

#文献专利按公司存储
def get_keyword_by_company(collection_name, separation_sign, key_name, another_collection_name):
    collection = get_collection(collection_name)
    company_collection = get_collection("company_profile")
    count = 1
    for profile in company_collection.find():
        company_name = profile["companyName"]
        print(str(count) + ". " + company_name)
        count += 1
        info_dict = {}
        for info in collection.find({"companyName":company_name}):
            if key_name not in info:
                continue
            keys = info[key_name].strip().split(separation_sign)
            for key in keys:
                if key != None and key != "":
                    if key in info_dict:
                        info_dict[key] = info_dict[key] + 1
                    else:
                        info_dict[key] = 1

        another_collection = get_collection(another_collection_name)
        for keyword in list(info_dict.keys()):
            another_collection.insert_one({"companyName":company_name,"word":keyword,"frequency":info_dict[keyword]})


def main():
    company_collection = get_collection("company_profile")
    software_collection = get_collection("software_copyright")
    collection = get_collection("software_copyright_keywords")
    for profile in company_collection.find():
        companyName = profile["companyName"]
        software_keywords = {}
        for software in software_collection.find({"companyName":companyName}):
            softwareName = software["softwareName"]
            outList = word_segmentation(softwareName)
            for word in outList:
                if word in software_keywords:
                    software_keywords[word] = software_keywords[word] + 1
                else:
                    software_keywords[word] = 1
        for key in list(software_keywords.keys()):
            # print({"companyName":companyName,"word":key,"frequency":software_keywords[key]})
            collection.insert_one({"companyName":companyName,"word":key,"frequency":software_keywords[key]})

if __name__ == '__main__':
    # main()
    # get_copyright_keywords()
    # get_news_keywords()
    # 获取专利关键字集合
    # get_keywords("patent",",","keywords","patent_keywords")
    #获取文献关键字

    # get_keywords("literature",";","keyword","literature_keywords")
    # 获取职位关键字
    # get_recruit()
    #按公司存储文献关键字
    # get_keyword_by_company("literature",";","keyword","literature_keywords_by_company")
    #按公司存储专利关键字
    # get_keyword_by_company("patent", ",", "keywords", "patent_keywords_by_company")