from datetime import datetime

'''
channel : 채널 식별값
title : 영상명
content : 영상 설명
time : 영상 길이
view : 영상 조회 수
like : 영상 좋아요 수
dislike : 영상 싫어요 수
date : 영상 업로드 날짜
highlight: 영상 하이라이트
comment : 영상 댓글
hash: 영상 식별값
'''
class video:
	def __init__(self):
		super(video, self).__init__()
		self.channel = ''
		self.title = ''
		self.content = ''
		self.time = ''
		self.view = 0
		self.like = 0
		self.dislike = 0
		self.date = datetime.now()
		self.highlight = []
		self.comments = []
		self.hash = ''

	def get_data(self):
		output = {
			'channel': self.channel,
			'title': self.title,
			'content': self.content,
			'date': self.date,
			'time': self.time,
			'view': self.view,
			'like': self.like,
			'dislike': self.dislike,
			'highlight': self.highlight,
			'comments': self.comments,
			'hash': self.hash
		}
		return output