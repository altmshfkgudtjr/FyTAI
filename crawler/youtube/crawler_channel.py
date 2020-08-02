from datetime import datetime
import hashlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from crawler.init_crawler import init_crawler
from etc.post_wash import post_wash
from etc.string_to_int import str2num_counter, str2num_date
from model.channel import channel
from module.connection import FyTAI__channel

def Crawler(url):
	try:
		# URL 마지막 문자가 '/'이 아니게 정제
		while url[len(url)-1] == '/':
			url = url[:-1]

		# 크롤러 생성자 호출
		crawler = init_crawler(url)
		# 양식 생성자 호출
		model = channel()

		# Get Chrome driver 1
		chrome = crawler.get_chrome()

		# 채널 정보 수집
		chrome.get(url+'/about')
		WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#right-column")))

		html = chrome.page_source
		bs = crawler.bs4(html)

		model.title = bs.select('div#text-container')[0].get_text(" ", strip = True)
		model.title = post_wash(model.title)
		model.info = bs.select('yt-formatted-string#description')[0].get_text(" ", strip = True)
		model.info = post_wash(model.info)
		model.date = bs.select('div#right-column > yt-formatted-string > span')[1].get_text(" ", strip = True)
		model.date = datetime.strptime(model.date, "%Y. %m. %d.")
		model.view = bs.select('div#right-column > yt-formatted-string')[2].get_text(" ", strip = True).replace(',', '')[4:-1]
		model.view = int(model.view)
		model.subscribe = bs.select('yt-formatted-string#subscriber-count')[0].get_text(" ", strip = True)[4:-1]
		model.subscribe = str2num_counter(model.subscribe)
		model.subscribe = model.subscribe == '' and -1 or model.subscribe
		model.hash = model.title + datetime.strftime(model.date, "%Y-%m-%d")
		model.hash = hashlib.md5(model.hash.encode('utf-8')).hexdigest()

		print("\n","-"*50)
		print("'",model.title,"' 채널 정보 수집을 시작합니다.")
		print("구독자 수:",model.subscribe,"명, 조회 수:",model.view,"회")
		print("바로가기:", url)
		print("-"*50,"\n")

		# 채널 내 커뮤니티 정보 수집
		chrome.get(url+'/community')
		WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > ytd-backstage-post-thread-renderer")))

		# 채널 내 커뮤니티 정보 수집을 위한 Chromedriver 2
		chrome2 = crawler.get_chrome()

		# 커뮤니티 포스트 페이지네이션을 위한 기억값
		before_posts_cnt = 0
		now_posts_cnt = 0

		while 1:
			print("[END] Key Down. :::: Community")
			chrome.find_element_by_tag_name("body").send_keys(Keys.END)
			# 3초동안 명시적 대기
			time.sleep(3)

			html = chrome.page_source
			bs = crawler.bs4(html)

			posts = bs.select('#contents > ytd-backstage-post-thread-renderer')
			# 현재 포스트 갯수 갱신
			now_posts_cnt = len(posts)

			# 새롭게 수집한 포스트 수가 이전 댓글 수랑 같으면 중지
			if before_posts_cnt == now_posts_cnt:
				break

			# 이전 포스트개수를 제외한 나머지 정보 수집
			for post in posts[before_posts_cnt:]:
				post_url = post.find('a', {"class": "yt-simple-endpoint style-scope ytd-button-renderer"})['href']
				chrome2.get(crawler.get_domain() + post_url)
				WebDriverWait(chrome2, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content.style-scope ytd-expander")))

				html2 = chrome2.page_source
				bs2 = crawler.bs4(html2)

				post_form = {}
				post_form['content'] = bs2.select('#content.style-scope ytd-expander')[0].get_text(" ", strip = True)
				post_form['content'] = post_wash(post_form['content'])
				post_form['date'] = bs2.select('#published-time-text')[0].get_text(" ", strip = True)
				post_form['date'] = str2num_date(post_form['date'])
				post_form['like'] = bs2.find('span', {'id': 'vote-count-middle'}).get_text(" ", strip = True)
				post_form['like'] = str2num_counter(post_form['like'])
				post_form['like'] = post_form['like'] == '' and -1 or post_form['like']
				post_form['comments'] = []

				# 포스트 내 댓글 페이지네이션을 위한 기억값
				before_comments_cnt = 0
				now_comments_cnt = 0

				while 1:
					print("[END] Key Down. :::: Community - Comments")
					chrome2.find_element_by_tag_name("body").send_keys(Keys.END)
					# 3초동안 명시적 대기
					time.sleep(3)

					html2 = chrome2.page_source
					bs2 = crawler.bs4(html2)
					
					if len(bs2.select('div#contents')) < 3:
						break

					comments = bs2.select('div#contents')[2].select('ytd-comment-thread-renderer')
					now_comments_cnt = len(comments)

					# 새롭게 수집한 댓글 수가 이전 댓글 수랑 같으면 중지
					if before_comments_cnt == now_comments_cnt:
						break

					# 이전 댓글 갯수를 제외한 나머지 정보 수집
					for comment in comments[before_comments_cnt:]:
						comment_form = {}
						comment_form['content'] = comment.select('#expander #content')[0].get_text(" ", strip = True)
						comment_form['content'] = post_wash(comment_form['content'])
						comment_form['date'] = comment.select('#header-author > yt-formatted-string')[0].get_text(" ", strip = True)
						comment_form['date'] = str2num_date(comment_form['date'])
						comment_form['like'] = comment.select('#vote-count-middle')[0].get_text(" ", strip = True)
						comment_form['like'] = str2num_counter(comment_form['like'])
						comment_form['like'] = comment_form['like'] == '' and -1 or comment_form['like']
						post_form['comments'].append(comment_form)

					# 이전 댓글 갯수 갱신
					before_comments_cnt = now_comments_cnt

				print("[POST]", post_form['content'][:20]+'...',' :::: 댓글 수:',len(post_form['comments']))

				model.posts.append(post_form)

			# 이전 포스트 갯수 갱신
			before_posts_cnt = now_posts_cnt

		# 데이베이스 삽입
		# [ 이미 존재하면 Update, 존재하지 않으면 Insert ]
		if FyTAI__channel(crawler.get_db()).find__one(model.hash) != None:
			FyTAI__channel(crawler.get_db()).insert__one(model.get_data())
		else:
			FyTAI__channel(crawler.get_db()).update__one(model.get_data())

		# Quit Chrome driver 2	
		chrome2.quit()

		# 채널 동영상 리스트 수집
		chrome.get(url+'/videos?view=0&sort=dd&shelf_id=0')
		WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-grid-video-renderer.style-scope")))

		video_list = []

		# 영상 페이지네이션을 위한 기억값
		before_videos_cnt = 0
		now_videos_cnt = 0

		while 1:
			print("[END] Key Down. :::: Video")
			chrome.find_element_by_tag_name("body").send_keys(Keys.END)
			# 3초동안 명시적 대기
			time.sleep(3)

			html = chrome.page_source
			bs = crawler.bs4(html)

			videos = bs.select('ytd-grid-video-renderer.style-scope')
			now_videos_cnt = len(videos)

			# 새롭게 수집한 영상 수가 이전 영상 수랑 같으면 중지
			if before_videos_cnt == now_videos_cnt:
				break

			for video in videos[before_videos_cnt:]:
				video_url = video.find('a')['href']
				video_list.append(crawler.get_domain() + video_url)

			# 이전 영상 갯수 갱신
			before_videos_cnt = now_videos_cnt

		print("\n","-"*50)
		print("'",model.title,"' 채널 총 영상 수:", len(video_list),"개")
		print("\n'",model.title,"' 채널 정보 수집을 완료하였습니다.\n")
		print("-"*50,"\n")

		channel_hash = model.hash
		# 채널 식별값 반환하기위한 변수 할당

	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Channel URL is not verified. Or, other problems may have occurred.\n")

		# Quit Chrome driver 2	
		try:
			chrome2.quit()
		except:
			print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Chrome Driver2 is already closed!\n")

	# Quit Chrome driver 1
	try:
		chrome.quit()
	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Chrome Driver1 is already closed!\n")

	# 양식 소멸자 호출
	del model
	# 크롤러 소멸자 호출
	del crawler

	# 비디오 링크 리스트 반환
	return (video_list, channel_hash)