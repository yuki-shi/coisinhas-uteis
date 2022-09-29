from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# === === === ===


def sitemap_crawl(url):

	def get_urls(url):
	  soup = BeautifulSoup(requests.get(url).content, 'html.parser')
	  xmls = [x for x in soup.find_all('loc')]
	  urls = []
	  for xml in xmls:
	    urls.append(xml.text)

	  return urls

	# --- 
	
	# Extração de sitemaps
	sitemaps = get_urls(url)

	pages = []

	# Extração de cada URL em cada sitemap
	for sitemap in sitemaps:
	  pages.extend(get_urls(sitemap))

	 return pages


# === === === ===


url = 'yuki.com'
pages = sitemap_crawl(url)

result = {}

for page in pages:
  soup = BeautifulSoup(requests.get(page).text, 'html.parser')
  ps = soup.find_all('p')
  for p in ps:
    result.setdefault(page, []).append(p)

 df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in result.items()]))
 df.to_csv('paragrafos.csv', index=False)
