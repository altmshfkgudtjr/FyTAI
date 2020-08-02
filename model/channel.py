from datetime import datetime

'''
title : 채널명
info : 채널 설명
view : 채널 총 조회 수
subscribe : 채널 구독 수
date : 채널 가입 날짜
posts : 채널 커뮤니티 게시글
hash : 채널 고유 식별값
'''
class channel:
	def __init__(self):
		super(channel, self).__init__()
		self.title = ''
		self.info = ''
		self.view = 0
		self.subscribe = 0
		self.date = datetime.now()
		self.posts = []
		self.hash = ''

	def get_data(self):
		output = {
			'title': self.title,
			'info': self.info,
			'date': self.date,
			'view': self.view,
			'subscribe': self.subscribe,
			'posts': self.posts,
			'hash': self.hash
		}
		return output