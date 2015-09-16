# WEB CRAWLER WITHOUT RANKING FUNCTION
import os
import re
import urlnorm
# import ranking_function
import Queue as Q
import robotparser
import customurllib
import urlparse
# from ranking_function import BM25
from BeautifulSoup import BeautifulSoup
from pygoogle import pygoogle
from customurllib import customURLlib

class WebCrawler:

  def __init__(self,query):
    self.query = query
    self.urls = []
    self.visited = {} # Dictionary keeping track of all the visited URLs
    self.valid_mime_types = ["text/html","text/plain","text/enriched"]
    self.connectives = ['or','and','is','this']
    self.illegal_extensions = ['gci','gif','jpg','png','css','js','mp3','mp4','mkv']
    self.illegal_folders = ['/cgi-bin/','/images/','/javascripts/','/js/','/css/','/stylesheets/']
    self.depth_reached = 0
    # self.rp = robotparser.RobotFileParser()
    self.url_controller = customURLlib()


  # #Alternate Method for Testing | To be commented out if not in Use
  # def fetch_google_results(self):
  #   import urllib
  #   import json
  #   print "Searcing Google"
  #   search_query = urllib.urlencode ( { 'q' : self.query } )
  #   #Find a better way to get Google Results


  #   res1 = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'+search_query+'&rsz=5').read()

  #   res2 = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'+search_query+'&rsz=5&start=5').read()


  #   json1 = json.loads ( res1 )

  #   json2 = json.loads ( res2 )

  #   results = json1 [ 'responseData' ] [ 'results' ] + json2 [ 'responseData' ] [ 'results' ]

  #   for result in results:
  #     print result['url']
  #     score = self.calculate_BM25_score(result['url'])
  #     self.urls.put((score,(str(result['url']),1))) #All google results are at depth 1 with google.com being at depth 0

  #============= METHOD FOR GOOGLE SEARCHING =======================
  def fetch_google_results(self):
    print "Searching Google"
    search = pygoogle(self.query)
    results = search.get_urls()[:10] #Only get the first 10 results
    for result in results:
      print "Google Result: " + str(result)
      self.urls.append((str(result),1)) #All google results are at depth 1 with google.com being at depth 0


  def normalize_url(self,url):
    return str(urlnorm.norm(url)) #URL normalization method
    #Normalization temporarily removed

  def is_illegal_folder(self,url):
    for f in self.illegal_folders:
        if f in url:
          return True
    return False

  def is_illegal_extension(self,url):
    url_components = urlparse.urlparse(url).path.split('.')
    if len(url_components)>1:
      if url_components[1] in self.illegal_extensions:
        return True
      else:
        return False
    else:
      return False


  def parse_page(self,html_document,depth,query):
    print "Parsing URL"
    soup = BeautifulSoup(html_document)
    new_depth = depth+1
    for link in soup.findAll('a', attrs={'href': re.compile("^(http|https)://")}):
      href = str(link.get('href'))
      print "Now Crawling: " + str(href)
      if not(self.normalize_url( href ) in self.visited) and (self.is_illegal_folder(href) == False) and (self.is_illegal_extension(href) == False):
        self.urls.append((href,new_depth))


  def crawl(self):

    while len(self.visited) <= 100 and not (self.urls == []):

      next_url = self.urls.pop(0)

      url = str(next_url[0])

      depth = int(next_url[1])

      print "Now Crawling: " + str(url)
      self.depth_reached = depth
      try:

        document = self.url_controller.open(url)

        mime_type = document.info().gettype()

      # Normalise the URL before inserting

        self.visited[self.normalize_url(url)] = depth

        if (mime_type in self.valid_mime_types):
          self.parse_page(document,depth,self.query)
        else:
          continue
      except IOError as e:
        print e


    print self.visited
    print self.urls

def main():
  query = raw_input ( 'Query: ' )

  crawler = WebCrawler(query)

  crawler.fetch_google_results()

  crawler.crawl()


if __name__ == '__main__':
  main()

