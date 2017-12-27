# coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import urllib2
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
dirName='wikiArts'
if not os.path.exists(dirName):
	os.makedirs(dirName)
artists_url="https://www.wikiart.org/en/alphabet/"
f = open("wikiArts/errlog.txt","a")
startChar='d'
for char in range(ord(startChar),ord('z')+1):
	html=requests.get(artists_url+chr(char))
	soup = BeautifulSoup(html.text, "lxml")
	lists= soup.find(class_='artists-list')
	for li in lists.find_all_next('li',class_=''):
		num=li.find('s',class_='total-link')
		if num!=None :
			if int(num.find('span',class_='total-text').text)>=100:
				name=li.find('li',class_='title').text
				print "====="+name+"====="
				if not os.path.exists(dirName+"/"+name.strip()):
					os.makedirs(dirName+"/"+name.strip())
				nowNum=0
				page=1
				count=1
				while True:
					url='https://www.wikiart.org'+num.find('a').get('href')+'?json=2&page='+str(page)
					print url
					artJson=json.loads(requests.get(url).text)
					nowNum+=len(artJson['Paintings'])
					for img in artJson['Paintings']:
						filename = img['paintingUrl'].split("/")[3]+".jpg"
						req = urllib2.Request(url = img['image'])
						try:
							if not os.path.exists("./wikiArts/"+name.strip()+"/"+filename):
								result = urllib2.urlopen(req).read()
								picf = open("./wikiArts/"+name.strip()+"/"+filename,"wb")
								picf.write(urllib2.urlopen(req).read())
								picf.close()
							print "["+str(count)+"/"+str(artJson['AllPaintingsCount'])+"] : "+filename
						except:
							print("Error: "+str(sys.exc_info()[0]))
							f.write(img['image']+"\n")
						count+=1
					if nowNum>=int(artJson['AllPaintingsCount']):
						break
					page+=1