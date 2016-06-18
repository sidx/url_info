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
	#return render(request, 'urlDetails.html',{})
	print response_data
	#printUrlData(response_data)
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def printUrlData(data):
	print 'here'
	return render_to_response('urlDetails.html', data)

def getSiteData(url):
	from bs4 import BeautifulSoup
	from urlparse import urlparse, urlunparse
	import urllib2
	
	scheme, netloc, path, params, query, fragment = urlparse(url)
	#print netloc
	if not netloc:
		netloc, path = path, ''
	if scheme == '':
		parsedUrl =  urlunparse(('http', netloc, path, params, query, fragment))
	else:
		parsedUrl = url
	siteData = urllib2.urlopen(parsedUrl)
	
	originalUrl = siteData.url
	siteSoup = BeautifulSoup(siteData.read(), "lxml")
	pageHead = siteSoup.head
	pageTitle = siteSoup.title
	#print pageHead
	#print "-------------------------------------"
	#print pageTitle
	imgTagList = siteSoup.select('img[src]')
	imgLinks = []
	for img in imgTagList:
		imgUrl = originalUrl + img['src']
		if imgUrl not in imgLinks:
			imgLinks.append(imgUrl)
	#print imgLinks
	#print siteData
	return dict(url=url,originalUrl=originalUrl,title=pageTitle.string, imgList = imgLinks)