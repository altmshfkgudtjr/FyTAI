from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from crawler.init_crawler import init_crawler

def Crawler():
	# 반환될 output 리스트 선언
	link_list = []

	try:
		# 크롤러 생성자 호출
		crawler = init_crawler("https://kr.noxinfluencer.com/")

		# 크롤링 url 추가
		crawler.url_list = [
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-science%20%26%20technology-youtuber-sorted-by-subs-weekly',
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-people%20%26%20blogs-youtuber-sorted-by-subs-weekly',
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-comedy-youtuber-sorted-by-subs-weekly'
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-gaming-youtuber-sorted-by-subs-weekly',
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-autos%20%26%20vehicles-youtuber-sorted-by-subs-weekly',
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-pets%20%26%20animals-youtuber-sorted-by-subs-weekly',
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-sports-youtuber-sorted-by-subs-weekly',
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-news%20%26%20politics-youtuber-sorted-by-subs-weekly',
			'https://kr.noxinfluencer.com/youtube-channel-rank/top-200-kr-howto%20%26%20style-youtuber-sorted-by-subs-weekly',
		]

		# Get Chrome driver
		chrome = crawler.get_chrome()

		# url 리스트 반복
		for url in crawler.url_list:
			# Chrome 페이지 이동
			chrome.get(url)
			WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#rank-table-body")))

			# 특정 tag가 display: none이 사라질 때까지 [END] 키 반복 누름.
			while chrome.find_element_by_class_name("end-mark-wrap").value_of_css_property("display") != 'block':
				print("[END] Key Down. :::: Top Chart")
				chrome.find_element_by_tag_name("body").send_keys(Keys.END)
				# 3초동안 명시적 대기
				time.sleep(3)

			# 해당 페이지 Parse
			html = chrome.page_source
			bs = crawler.bs4(html)

			# 유튜버들 개인 페이지 파싱
			youtubers = bs.findAll('tr', {'class': 'item'})
			for youtuber in youtubers:
				channel = crawler.get_domain() + youtuber.find('a')['href']

				# 개인 페이지에서 유튜브 Youtube 채널 페이지 파싱
				bs_ytb = crawler.request_page(channel)
				link = bs_ytb.find('a', {'class': 'icon-wrapper'})['href']
				print("[PUSH]", link)
				time.sleep(3)

				# 반환될 output 리스트에 추가
				link_list.append(link)
				channel = None

	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Top channel scrapping faild. Some problems may have occurred.\n")

	# Quit Crhome driver
	try:
		chrome.quit()
	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Chrome Driver1 is already closed!\n")

	# 크롤러 소멸자 호출
	try:
		del crawler
	except:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Crawler is already closed!\n")

	return link_list
