import re
import urllib
import json
import HTMLParser
import ranking-function
from ranking-function import BM25
class WebCrawler:

  def __init__(self,query):
    self.query = query
    self.urls = [] # List of URLs to be visited
    self.visited = dict() # Dictionary keeping track of all the visited URLs

  def fetch_google_results(self):
    search_query = urllib.urlencode ( { 'q' : self.query } )
    response1 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5' ).read()
    response2 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5&start=5' ).read()
    json1 = json.loads ( response1 )
    json2 = json.loads ( response2 )
    results = json1 [ 'responseData' ] [ 'results' ] + json2 [ 'responseData' ] [ 'results' ]
    for result in results:
      self.urls.append(result['url'])

  def parse_page(self,url,query):
      handle = urllib.urlopen(url)
      html_gunk = handle.read()
      print html_gunk

  def crawl(self):
    self.fetch_google_results() #build URLs





def main():
  query = raw_input ( 'Query: ' )
  crawl = WebCrawler(query)



if __name__ == '__main__':
  main()

