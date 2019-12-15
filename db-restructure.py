from pymongo import MongoClient


client = MongoClient('localhost',27017)

db = client['sensors']
col_temp = db['temperature']
col_data = db['data']
col_net = db['network']
print ("Check_Internet - mongodb connection error")


col_temp.delete_many(col_temp.find({'temp':None}))

for record in col_temp.find():

    testdata = {'time': record['time'], 'sensor':record['sensor'], 'value': record['temp']}
    col_data.insert_one(testdata)

for record in col_net.find():

    testdata = {'time': record['time'], 'sensor':4, 'value': record['ms-delay']}
    col_data.insert_one(testdata)

client.close()