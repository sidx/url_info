from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def index(request):
	return render(request, 'form.html', {})


def getUrlData(request):
	import json
	url = request.POST['url']
	response_data = getSiteData(url)
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def printUrlData(data):
	return render_to_response('urlDetails.html', data)

def getSiteData(url):
	from bs4 import BeautifulSoup
	from urlparse import urlparse, urlunparse
	import urllib2
	
	scheme, netloc, path, params, query, fragment = urlparse(url)
	if not netloc:
		netloc, path = path, ''
	if scheme == '':
		parsedUrl =  urlunparse(('http', netloc, path, params, query, fragment))
	else:
		parsedUrl = url
	siteData = urllib2.urlopen(parsedUrl)
	
	originalUrl = siteData.url
	originalUrlParse = urlparse(originalUrl)
	
	siteSoup = BeautifulSoup(siteData.read(), "lxml")
	pageHead = siteSoup.head
	pageTitle = siteSoup.title
	pageText = siteSoup.get_text()
	imgTagList = siteSoup.select('img[src]')
	imgLinks = []
	for img in imgTagList:
		if img['src'].find('http') !=0:
			imgUrl = originalUrlParse.scheme +"://"+ originalUrlParse.netloc + img['src']
		else:
			imgUrl = img['src']
		print imgUrl
		if imgUrl not in imgLinks:
			imgLinks.append(imgUrl)
	return dict(url=url,originalUrl=originalUrl,originalProvider=originalUrlParse.netloc,allText=pageText, title=pageTitle.string, imgList = imgLinks)
