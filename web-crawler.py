import re
import urllib
import json
import HTMLParser
class WebCrawler:
  def __init__(self,query):
    self.query = query
    self.urls = []
    self.visited = dict()

  def fetch_google_results(self):
    search_query = urllib.urlencode ( { 'q' : self.query } )
    response1 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5' ).read()
    response2 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5&start=5' ).read()
    json1 = json.loads ( response1 )
    json2 = json.loads ( response2 )
    results = json1 [ 'responseData' ] [ 'results' ] + json2 [ 'responseData' ] [ 'results' ]
    for result in results:
      self.urls.append(result['url'])

  def crawler(self):
    self.fetch_google_results() #build URLs


  def parse_page(self,url,query):
      handle = urllib.urlopen(url)
      html_gunk = handle.read()
      print html_gunk


def main():
  query = raw_input ( 'Query: ' )
  crawl = WebCrawler(query)



if __name__ == '__main__':
  main()

