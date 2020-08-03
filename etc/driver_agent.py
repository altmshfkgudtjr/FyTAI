from selenium import webdriver
from platform import platform

def chromedriver():
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument("disable-gpu")
	options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36")
	options.add_argument("lang=ko_KR")

	if platform().startswith("Windows"):
		driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
	else:
		driver = webdriver.Chrome('/home/ubuntu/chromedriver', chrome_options=options)

	return driver