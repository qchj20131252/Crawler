from pymongo import MongoClient

client = MongoClient("202.115.161.211",8042)
db_auth = client.admin
db_auth.authenticate('rw_m', 'Db_rw')
db = client["qcj_companyInfo"]
collection = db["company_profile"]
company_profile = collection.find()
db2 = client['businfo']
collection2 = db2['literature']