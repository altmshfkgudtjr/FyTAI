from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from crawler.init_crawler import init_crawler
from etc.post_wash import post_wash
from etc.string_to_int import str2num_counter, str2num_date, str2num_time
from model.video import video
from module.connection import FyTAI__video

def Crawler(url, channel_hash):
	try:
		# 크롤러 생성자 호출
		crawler = init_crawler(url)
		# 양식 생성자 호출
		model = video()

		# Get Chrome driver
		chrome = crawler.get_chrome()

		# 영상 정보 수집
		chrome.get(url)
		time.sleep(3)

		# 댓글 표시를 위한 Key Down
		print("[END] Key Down. :::: Community")
		chrome.find_element_by_tag_name("body").send_keys(Keys.END)
		WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents ytd-comment-thread-renderer")))
		
		# 유튜브 영상 광고가 존재할 경우, 광고를 기다렸다가 Skip을 누른다.
		try:
			print("[AD]", chrome.find_element_by_class_name(".ytp-ad-preview-container.countdown-next-to-thumbnail"))
			print("광고를 기다리는 중...")
			WebDriverWait(chrome, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.ytp-ad-skip-button.ytp-button")))
			chrome.find_element_by_class_name(".ytp-ad-skip-button.ytp-button").click()
		except:
			pass

		time.sleep(5)

		html = chrome.page_source
		bs = crawler.bs4(html)

		model.channel = channel_hash
		model.title = bs.select('#container > h1')[0].get_text(" ", strip=True)
		model.title = post_wash(model.title)
		model.content = bs.select('#description')[0].get_text(" ", strip=True)
		model.content = post_wash(model.content)
		model.view = bs.find('span', {'class': 'view-count style-scope yt-view-count-renderer'}).get_text(" ", strip=True)[4:-1]
		model.view = int(model.view.replace(',', ''))
		model.like = bs.select('#top-level-buttons #text')[0].get_text(" ", strip=True)
		model.like = str2num_counter(model.like)
		model.like = model.like == '' and -1 or model.like
		model.dislike = bs.select('#top-level-buttons #text')[1].get_text(" ", strip=True)
		model.dislike = str2num_counter(model.dislike)
		model.dislike = model.dislike == '' and -1 or model.dislike
		model.date = bs.select('#date yt-formatted-string')[0].get_text(" ", strip=True)
		if model.date.find("실시간 스트리밍") != -1:
			model.date = model.date.split(':')[1:]
		try:
			model.date = datetime.strptime(model.date, "%Y. %m. %d.")
		except:
			model.date = datetime.strptime(model.date, "%b %d, %Y")
		model.hash = url.split('?v=')[1]

		print("\n","-"*50)
		print("'",model.title,"' 영상 정보 수집을 시작합니다.")
		print("업로드 날짜:",model.date.strftime("%Y-%m-%d"))
		print("조회 수:",model.view,"회, 좋아요 수:",model.like,"명")
		print("바로가기:", url)
		print("-"*50,"\n")

		'''
		비동기 Page에서 page source를 얻기 위한 Action 작업
		'''
		# 영상 댓글 페이지네이션을 위한 기억값
		before_comments_cnt = 0
		now_comments_cnt = 0
		idx = 1

		print("[COMMENT] 댓글 수집 중...")
		while 1:
			html = chrome.page_source
			bs = crawler.bs4(html)

			comments = bs.select('ytd-comment-thread-renderer')
			now_comments_cnt = len(comments)

			# 새롭게 수집한 댓글 수가 이전 댓글 수랑 같으면 중지
			if before_comments_cnt == now_comments_cnt:
				break

			for comment in comments[before_comments_cnt:]:
				print("[COMMENT] 댓글 존재 ::::",idx,"/N 개")
				if comment.find('ytd-button-renderer', {'id': 'more-replies'}) != None:
					print("[REPLY] 대댓글 존재")
					# 해당 Tag 위치로 이동
					ActionChains(chrome).move_to_element(chrome.find_element_by_xpath('//*[@id="contents"]/ytd-comment-thread-renderer['+str(idx)+']//*[@id="more-replies"]/a//*[@id="text"]')).perform()
					chrome.find_element_by_xpath('//*[@id="contents"]/ytd-comment-thread-renderer['+str(idx)+']//*[@id="more-replies"]/a//*[@id="text"]').click()
					# 5초동안 명시적 대기
					time.sleep(5)

					# 대댓글 더보기가 존재하는 경우 클릭
					try:
						while chrome.find_element_by_xpath('//*[@id="contents"]/ytd-comment-thread-renderer['+str(idx)+']//*[@id="continuation"]/yt-next-continuation/paper-button/yt-formatted-string'):
							print("[MORE REFLY] 대댓글 더보기를 클릭하였습니다.")
							chrome.find_element_by_xpath('//*[@id="contents"]/ytd-comment-thread-renderer['+str(idx)+']//*[@id="continuation"]/yt-next-continuation/paper-button/yt-formatted-string').click()
							# 5초동안 명시적 대기
							time.sleep(5)
					except:
						pass
				# comment 위치 식별값 갱신
				idx += 1
			# 이전 댓글 갯수 갱신
			before_comments_cnt = now_comments_cnt

			# 페이지 하단으로 내리기
			print("[END] Key Down. :::: Video")
			chrome.find_element_by_tag_name("body").send_keys(Keys.END)
			WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comment-thread-renderer")))
			time.sleep(5)


		# 영상 댓글 페이지네이션을 위한 기억값
		idx = 1

		html = chrome.page_source
		bs = crawler.bs4(html)

		comments = bs.select('ytd-comment-thread-renderer')

		# 이전 댓글 갯수를 제외한 나머지 정보 수집
		for comment in comments:
			comment_form = {}
			comment_form['content'] = comment.select('#expander #content')[0].get_text(" ", strip = True)
			comment_form['content'] = post_wash(comment_form['content'])
			comment_form['date'] = comment.select('#header-author > yt-formatted-string')[0].get_text(" ", strip = True)
			comment_form['date'] = str2num_date(comment_form['date'])
			comment_form['like'] = comment.select('#vote-count-middle')[0].get_text(" ", strip = True)
			comment_form['like'] = str2num_counter(comment_form['like'])
			comment_form['like'] = comment_form['like'] == '' and -1 or comment_form['like']
			comment_form['replies'] = []
			# 하이라이트 댓글 수집
			for h in comment.select('#expander #content a'):
				if h.get_text(" ", strip = True).find(':') != -1:
					model.highlight.append(h.get_text(" ", strip = True))

			print("[COMMENT] '",model.title[:10],"... ' 영상의 '", comment_form['content'][:10],"...' 댓글 수집 중..")

			# 대댓글이 존재하는 경우 대댓글 정보 수집
			if comment.find('ytd-button-renderer', {'id': 'more-replies'}) != None:
				replies = comment.select('#expander-contents > #loaded-replies > ytd-comment-renderer')

				for reply in replies:
					reply_form = {}
					reply_form['content'] = reply.select('#expander #content')[0].get_text(" ", strip = True)
					reply_form['content'] = post_wash(reply_form['content'])
					reply_form['date'] = reply.select('#header-author > yt-formatted-string')[0].get_text(" ", strip = True)
					reply_form['date'] = str2num_date(reply_form['date'])
					reply_form['like'] = reply.select('#vote-count-middle')[0].get_text(" ", strip = True)
					reply_form['like'] = str2num_counter(reply_form['like'])
					reply_form['like'] = reply_form['like'] == '' and -1 or reply_form['like']
					# 하이라이트 댓글 수집
					for h in reply.select('#expander #content a'):
						if h.get_text(" ", strip = True).find(':') != -1:
							model.highlight.append(h.get_text(" ", strip = True))

					print("[REPLY] '",comment_form['content'][:10],"... ' 댓글의 '", reply_form['content'][:10],"...' 대댓글 수집 중..")
					# 수집한 대댓글 댓글 양식의 대댓글 리스트에 추가
					comment_form['replies'].append(reply_form)

			# 수집한 댓글 영상 양식의 댓글 리스트에 추가
			model.comments.append(comment_form)
			idx += 1

		# 광고시간이 수집되는 것을 방지하기 위해서 제일 마지막 작업으로 수행
		model.time = bs.find('div', {'class': 'ytp-time-display notranslate'}).findAll('span')[2].get_text(" ", strip=True)
		model.time = str2num_time(model.time)

		if FyTAI__video(crawler.get_db()).find__one(model.hash) != None:
			FyTAI__video(crawler.get_db()).insert__one(model.get_data())
		else:
			FyTAI__video(crawler.get_db()).update__one(model.get_data())

		print("\n","-"*50)
		print("[VIDEO] '", model.title[:20],"' :::: 댓글 수:",len(model.comments))
		print("\n'",model.title[:20],"' 영상 정보 수집을 완료하였습니다.")
		print("\n","-"*50)

	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Video scrapping faild. Some problems may have occurred.\n")

	# Quit Chrome driver
	try:
		chrome.quit()
	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Chrome Driver1 is already closed!\n")

	# 크롤러 소멸자 호출
	try:
		del model
	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Video Model is already closed!\n")
	# 크롤러 소멸자 호출
	try:
		del crawler
	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Crawler is already closed!\n")

	return "success"