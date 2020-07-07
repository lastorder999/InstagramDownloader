from bs4 import BeautifulSoup
import requests
import lxml
import json
import sys


def URLSingleImage(jsonFile):
	return jsonFile['graphql']['shortcode_media']['display_url'] 

def URLMultipleMedia(jsonFile):
	findURL = jsonFile['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
	return [URLs['node']['display_url'] for URLs in findURL]
	
def URLSingleVideo(jsonFile):
	return jsonFile['graphql']['shortcode_media']['video_url']

def GetUrlImage(URL):
	add = '?__a=1'
	link = URL + add
	r = requests.get(link)
	jsonFile = r.json()
	typeFile = jsonFile['graphql']['shortcode_media']['__typename']
	if typeFile == "GraphImage":
		return URLSingleImage(jsonFile)
	elif typeFile == "GraphVideo":
		return URLSingleVideo(jsonFile)
	elif typeFile == "GraphSidecar":
		return URLMultipleMedia(jsonFile)

def GetNameImage(URLImage):
	URLSplit = URLImage.split('/')[-1]
	URLSplit = URLSplit.split('?')[0]
	return URLSplit

def DowloadImage(nameImage, URLImage):
	r = requests.get(URLImage)

	with open(nameImage, 'wb') as fileImage:
		fileImage.write(r.content)
	
def main(url):
	urlimage = GetUrlImage(url)
	
	if type(urlimage) is list:
		for urls in urlimage:
			DowloadImage(GetNameImage(urls), urls)
	else:
		DowloadImage(GetNameImage(urlimage),urlimage)

if __name__ == '__main__':
	main(sys.argv[1])
