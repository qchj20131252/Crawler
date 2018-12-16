from pymongo import MongoClient
import json

# 获取mongo数据库的集合信息
def get_collection(collection_name):
    client = MongoClient("202.115.161.211", 8042)
    db_auth = client.admin
    db_auth.authenticate('rw_m', 'Db_rw')
    db = client['qcj_companyInfo']
    collection = db[collection_name]
    return collection

# 读取存储著作权信息的文件
def read_file(file_path):
    with open(file_path,"r",encoding="utf-8") as fr:
        content = fr.readlines()
    return content

# 导入著作权到mongo
def import_copyright(collection_name,title_dict,file_path):
    collection = get_collection(collection_name)
    copyright_json_list = read_file(file_path)
    copyright_number = 0
    for copyright_json in copyright_json_list:
        new_copyright_dict = {}
        copyright_dict = json.loads(copyright_json,encoding="utf-8")
        copyright_title_list = list(copyright_dict.keys())
        for copyright_title in copyright_title_list:
            if copyright_title in title_dict:
                new_copyright_dict[title_dict[copyright_title]] = copyright_dict[copyright_title]
        collection.insert_one(new_copyright_dict)
        copyright_number += 1
    return copyright_number

# 导入主要人员到mongo
def import_mainmember(collection_name,file_path):
    collection = get_collection(collection_name)
    mainmember_json_list = read_file(file_path)
    mainmember_number = 0
    for mainmember_json in mainmember_json_list:
        new_mainmember_dict = {}
        mainmember_dict = json.loads(mainmember_json,encoding="utf-8")
        new_mainmember_dict["companyName"] = mainmember_dict["公司名称"]
        new_mainmember_dict["name"] = mainmember_dict[" 姓名"]
        new_mainmember_dict["job"] = mainmember_dict["职务"]
        collection.insert_one(new_mainmember_dict)
        mainmember_number += 1
    return mainmember_number

def get_copyright_keywords():
    software_collection = get_collection("software_copyright_keywords")
    copyright_dict = {}
    for info in software_collection.find():
        if info["word"] in copyright_dict:
            copyright_dict[info["word"]] = copyright_dict[info["word"]] + info["frequency"]
        else:
            copyright_dict[info["word"]] = info["frequency"]

def main():
    # 导入作品著作权 2018/11/15
    work_copyright_file_path = "E:/PycharmProjects/Crawler/src/resource/work_copyright.txt"
    work_copyright_title_dict = {'公司名称':'companyName','作品名称':'workName','首次发表日期':'firstPublishedDate',
                  '创作完成日期':'completionDate','登记号':'registrationNumber','登记日期':'registrationDate',
                  '登记类别':'registrationCategory'}
    work_copyright_collection_name = "work_copyright"
    work_copyright_number = import_copyright(work_copyright_collection_name,work_copyright_title_dict,work_copyright_file_path)
    print(work_copyright_number)

    # 导入软件著作权 2018/11/15
    software_copyright_file_path = "E:/PycharmProjects/Crawler/src/resource/software_copyright.txt"
    software_copyright_title_dict = {"公司名称": "companyName", "软件名称": "softwareName", "版本号": "versionNumber",
                                      "发布日期": "releaseDate", "软件简称": "softwareAbbreviation",
                                      "登记号": "registrationNumber", "登记批准日期": "registrationApprovalDate"}
    software_copyright_collection_name = "software_copyright"
    software_copyright_number = import_copyright(software_copyright_collection_name,software_copyright_title_dict,software_copyright_file_path)
    print(software_copyright_number)

    # 导入主要人员 2018/11/15
    mainmember_file_path = "E:/PycharmProjects/Crawler/src/resource/mainmembers.json"
    mainmember_collection_name = "mainmember"
    mainmember_number = import_mainmember(mainmember_collection_name,mainmember_file_path)
    print("主要人员信息共有" + str(mainmember_number) + "条")



if __name__ == '__main__':
    # main()
    get_copyright_keywords()