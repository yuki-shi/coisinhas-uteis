import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


url = 'https://victoriousseo.com/post-sitemap.xml'


def getLinks(url):

	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	xml_loc = [x for x in soup.findAll('loc')]

	links = []

	for item in xml_loc:
		
		link = item.text
		links.append(link)

	return links


def scrape(linkList):

	titles = []
	
	# usando tqdm pois sou ansiosa
	with tqdm(total = len(linkList)) as loop:
		for link in linkList:
			r = requests.get(link)
			url = r.text.encode('utf-8')
			soup = BeautifulSoup(url, 'html.parser')
			titles.append(soup.title.get_text())
			loop.update()
			

	return titles


def writeCSV(titles):

	df = pd.DataFrame(titles)
	df.to_csv('titles.csv', index=False)




links = getLinks(url)
titles = scrape(links)
writeCSV(titles)
