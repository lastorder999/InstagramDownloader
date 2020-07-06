from bs4 import BeautifulSoup
import requests
import os



def GetUrlImage(URL):
	r = requests.get(URL)
	htmlParser = BeautifulSoup(r.text, 'html.parser')
	# linkImage = soup.find_all("meta",{"property":"og:image"})
	metaFile = htmlParser.find(property="og:image")
	actualURLImage = metaFile['content']
	return actualURLImage

def GetNameImage(URLImage):
	URLWasSplitBySlash = URLImage.split('/')[-1]
	imageFileName = URLWasSplitBySlash.split('?')[0]
	return imageFileName

def DowloadImage(nameImage, URLImage):
	r = request.get(URLImage)
	downloadCommand = '''wget -O {} "{}"'''
	os.system(downloadCommand.format(nameImage, URLImage))



# from selenium import webdriver
# driver = webdriver.Firefox(executable_path=r'C:\Users\*****\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe')
# driver.get(link)
# html = driver.execute_script("return document.documentElement.outerHTML;")
# html = driver.execute_script("return document.documentElement.innerHTML;")
# html = driver.page_source
# find_all("img",{"style":"object-fit: cover;"})