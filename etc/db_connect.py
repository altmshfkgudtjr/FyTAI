from pymongo import MongoClient
from platform import platform
from etc.db_info import info

def mongo():
	# if platform().startswith("Windows"):
	# 	client = MongoClient('localhost', 27017)
	# else:
	db_info = info()
	client = MongoClient('mongodb://%s:%s@%s' %(db_info['MONGO_ID'], db_info['MONGO_PW'], db_info['MONGO_HOST']))
	
	db = client['fytai']
	
	return (db, client)