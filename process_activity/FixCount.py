import pymongo

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")

my_collection = my_client['pinfo']['activity']

def fix_count():
    all = my_collection.find()
    for one in all:
        count = one['count']
        if count == 1:
            c_count = count
        else:
            c_count = int(count / 2)
        new_values = {'$set': {'count':c_count}}
        query = {'_id': one['_id']}
        my_collection.update_one(query, new_values)
if __name__ == '__main__':
    fix_count()
    # one = my_collection.find_one({"host_ip":'211.65.197.175', "proc_name":'watchdog/1'})
    # print(one)
    # query = {'_id': one['_id']}
    # print(my_collection.find_one(query))
    # new_values = {'$set': {'count': 2849}}
    # my_collection.update_one(query, new_values)
    # one = my_collection.find_one({"host_ip": '211.65.197.175', "proc_name": 'watchdog/1'})
    # print(one)


# {host_ip:'211.65.197.175', proc_name:'watchdog/1'}