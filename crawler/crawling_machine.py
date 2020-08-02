from crawler.youtube.crawler_top_youtuber import Crawler as ty_Crawler
from crawler.youtube.crawler_channel import Crawler as channel_Crawler
from crawler.youtube.crawler_video import Crawler as video_Crawler

def crawling_machine():
	# 채널리스트 반환
	ch_list = ty_Crawler()
	
	# 채널 crawling
	for ch in ch_list:
		(v_list, channel_hash) = channel_Crawler(ch)

		# 영상 crawling
		for v in v_list:
			video_Crawler(v, channel_hash)

	return False