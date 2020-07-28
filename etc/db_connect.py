from pymongo import MongoClient
from platform import platform
import db_info

def mongo:
	if platform().startswith("Windows"):
		client = MongoClient('localhost', 27017)
	else:
		client = MongoClient('mongodb://%s:%s@%s' %(db_info.MONGODB_ID, db_info.MONGODB_PW, db_info.MONGODB_HOST))
	db = client['fytai']
	
	return db