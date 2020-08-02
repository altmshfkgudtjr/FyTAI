from etc.driver_agent import chromedriver
from etc.db_connect import mongo
from etc.url_requestor import request_url
from etc.beautiful_parser import parse

class init_crawler:
	# 생성자
	def __init__(self, url):
		super(init_crawler, self).__init__()
		self.url = url 
		self.url_list = []
		self.page_num = 1
		self.target = ''

		# DB Client
		(self.db, self.client) = mongo()

	# db Cursor 반환
	def get_db(self):
		return self.db

	# Selenium 요청
	def get_chrome(self):
		driver = chromedriver()
		return driver

	# Request 요청
	def request_page(self, url):
		text = request_url(url)
		bs = parse(text)
		return bs

	# Page Text Bs4
	def bs4(self, text):
		bs = parse(text)
		return bs

	# target url 세팅
	def next_target(self):
		if len(self.url_list) == 0:
			self.target = None
		else:
			self.target = self.url_list.pop(0)

	# 페이지 넘버 이동
	def update_page(self, num):
		self.page_num += num
		self.target = self.url + str(self.page_num)

	# 도메인 추출
	def get_domain(self):
		return self.url.split('/')[0] + '//' + self.url.split('/')[2]

	# target url_list 반환
	def get_url_list(self):
		return self.url_list

	# db connection 해제
	def __del__(self):
		try:
			self.client.close()
		except:
			print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: DB cursor is not opened!\n")