import pymongo

myclient = pymongo.MongoClient("mongodb://211.65.197.70:27017/")

dblist = myclient.list_database_names()
print(dblist)

mydb = myclient["sysinfo"]
print(mydb)

mycol = mydb["211.65.197.175"]

x = mycol.find_one()

print(x)