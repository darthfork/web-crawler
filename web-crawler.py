import re
import urllib
import json
import HTMLParser
import ranking-function
from ranking-function import BM25
from lxml.html import parse

class WebCrawler:

  def __init__(self,query):
    self.query = query
    self.urls = [] # List of URLs to be visited
    self.visited = dict() # Dictionary keeping track of all the visited URLs
    self.num_links = 0

  def fetch_google_results(self):
    search_query = urllib.urlencode ( { 'q' : self.query } )
    response1 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5' ).read()
    response2 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5&start=5' ).read()
    json1 = json.loads ( response1 )
    json2 = json.loads ( response2 )
    results = json1 [ 'responseData' ] [ 'results' ] + json2 [ 'responseData' ] [ 'results' ]
    for result in results:
      self.urls.append(result['url'])

  def parse_page(self,url,query): #Extract all the links from the page and add them to the URLs list
    #

  def crawl(self): # Pop first URL from the URLs list and add it to the visited list and then parse them
    while num_links != 100: #initially trying for 100 links
      url = urls.pop(-1)
      num_links += 1
      visited[num_links] = url
      parse_page(url,self.query)


def main():
  query = raw_input ( 'Query: ' )
  crawl = WebCrawler(query)



if __name__ == '__main__':
  main()

