from datetime import datetime
import sys
import time
from crawler.crawling_machine import crawling_machine
from crawler.youtube.crawler_channel import Crawler as youtube_channel_crawler
from nb_signature import nb_signature

'''
How to use?
================================
`python3 main.py` : You can choice the task.
`python3 main.py auto` : You can run scrapping program automatic.
						 [auto, Auto, AUTO, aUTo] : Possible
						 [1, true, false, auto] : Impossible
'''
if __name__ == "__main__":
	if len(sys.argv) == 1:
		pass
	elif len(sys.argv) == 2:
		AUTO_ARG = sys.argv[1]
		if AUTO_ARG.lower() == 'auto':
			# 크롤러 시작
			crawling_machine()
		else:
			print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Input args are invalid.\n")
			exit()
	else:
		print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Input args are invalid.\n")
		exit()

	print()
	print('		   ::::::::::::::::::::::::')
	print('		   :::: FyTAI Scrapper ::::')
	print('		   ::::::::::::::::::::::::')
	print('	  	   [',datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),']')
	# NB 시그니쳐 출력
	nb_signature()

	print()
	print("="*62)
	print("			Select Task!")
	print("="*62,"\n")
	print("1. Auto")
	print("2. Youtube Channel Scrapping")
	print("3. Exit")
	print()

	while 1:
		try:
			num = int(input(">>> "))
			if num > 3:
				continue
			else:
				break
		except:
			print("\n",'\x1b[6;37;41m' + '[WARNING]' + '\x1b[0m'," :::: Input only int type.\n")

	if num == 1:
		# 크롤러 시작
		crawling_machine()
	elif num == 2:
		url = input("Channel URL: ")
		# 유튜브 채널 크롤러 시작
		youtube_channel_crawler(url)
	elif num == 3:
		print("\n\nFyTAI Scrapper Exit.", '\x1b[0;30;42m' + '[Success]' + '\x1b[0m', "\n")
		# 프로그램 종료
		exit()