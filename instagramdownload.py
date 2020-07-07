from bs4 import BeautifulSoup
import requests
import lxml
import sys


def GetUrlImage(URL):
	r = requests.get(URL)
	htmlParser = BeautifulSoup(r.text, 'lxml')
	metaFile = htmlParser.find(property="og:image")
	actualURLImage = metaFile['content']
	return actualURLImage

def GetNameImage(URLImage):
	URLWasSplitBySlash = URLImage.split('/')[-1]
	imageFileName = URLWasSplitBySlash.split('?')[0]
	return imageFileName

def DowloadImage(nameImage, URLImage):
	r = requests.get(URLImage)
	with open(nameImage, 'wb') as fileImage:
		fileImage.write(r.content)
	
def main(url):
	urlimage = GetUrlImage(url)
	nameimage = GetNameImage(urlimage)
	DowloadImage(nameimage, urlimage)

if __name__ == '__main__':
	main(sys.argv[1])
