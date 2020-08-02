from bs4 import BeautifulSoup

def parse(text):
	return BeautifulSoup(text, 'html.parser')