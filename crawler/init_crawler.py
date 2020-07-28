from etc.db_connect import mongo
from etc.url_requestor import request_url
from etc.html_parser import parse

class init_crawler:
	# 생성자
	def __init__(self, url):
		super(crawler, self).__init__()
		self.url = url 
		self.domain = self.url.split('/')[0] + '//' + self.url.split('/')[2]
		self.url_list = []
		self.page_num = 1
		self.target = changePage(self.page_num)

		# DB Client    
		self.db = mongo()

	# return db
	def getDB(self):
		return self.db

	# 페이지 넘버 이동
	def updatePage(self, num):
		self.page_num += num
		self.target = self.url + str(self.page_num)

	# 페이지 가져오기
	def getPage(self):
		request = request_url(self.target).text
		page = parse(request)
		return page

	# 페이지 리스트 생성
	def makePagelist(self, sub_url_list, num):
		if num <= len(self.url_list):
			return False
		elif sub_url_list:
			for url in sub_url_list:
				self.url_list.append(self.domain + url['href'])
			return True
		else:
			return False

	# 도메인 추출
	def getDomain(self):
		return self.domain

	# target url_list 반환
	def getURLlist(self):
		return self.url_list

	# DB cursor 반환
	def getDB(self):
		return self.db

	# 소멸자
	def __del__(self):
		self.db.close()