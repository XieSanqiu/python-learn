import pymongo

mongo = pymongo.MongoClient("mongodb://211.65.197.70:27017")
record_time_col = mongo['pinfo']['record_time']
#record_time_col.insert_one({'type':'collect_rate', 'host':'211.65.197.175', 'rate':300})
query1 = {'type':'collect_rate', 'host':'211.65.197.175'}
x = record_time_col.find_one(query1, {'_id':0, 'rate':1})['rate']
print(x)