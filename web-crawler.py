import os
import re
import urlnorm
import ranking_function
import Queue as Q
import robotparser
import customurllib
from ranking_function import BM25
from BeautifulSoup import BeautifulSoup
from pygoogle import pygoogle
from customurllib import customURLlib

class WebCrawler:

  def __init__(self,query):
    self.query = query
    self.urls = Q.PriorityQueue() # Priority Queue of URLs to be visited and their depth [(score,(url,depth))]
    self.visited = {} # Dictionary keeping track of all the visited URLs
    self.valid_mime_types = ["text/html","text/plain","text/enriched"]
    self.connectives = ['or','and','is','this']
    self.illegal_extensions = ['gci','gif','jpg','png','css','js','mp3','mp4','mkv']
    self.illegal_folders = ['/cgi-bin/','/images/','/javascripts/','/js/','/css/','/stylesheets/']
    self.depth_reached = 0
    self.rp = robotparser.RobotFileParser()
    self.url_controller = customURLlib()

  def calculate_BM25_score(url):
    url_controller.retrieve(url,"temp.html")
    webpage = 'temp.html'
    bm25 = BM25(webpage,delimiter=' ')
    query = self.query.split()
    score = bm25.BM25Score(query)

    try:
      os.remove(webpage)
    except OSError:
      print "Unable to remove File"

    return score


  def fetch_google_results(self):
    search = pygoogle(self.query)
    results = search.get_urls()[:10] #Only get the first 10 results
    print "Google Results Fetched"
    for result in results:
      score = self.calculate_BM25_score(result)
      self.urls.put((score,(result.encode('utf8'),1))) #All google results are at depth 1 with google.com being at depth 0 | Initially priority is 0


  def normalize_url(self,url):
    return urlnorm.norm(url).encode('utf8') #URL normalization method

  def is_illegal_folder(self,url):
    for f in self.illegal_folders:
        if f in url:
          return True
    return False

  def is_illegal_extension(self,url):
    url_components = urlparse.urlparse(url)
    if url_components.path.split('.')[1] in self.illegal_extensions:
      return True
    else:
      return False


  def parse_page(self,html_document,depth,query):

    soup = BeautifulSoup(html_document)

    new_depth = depth+1

    for link in soup.findAll('a', attrs={'href': re.compile("^(http|https)://")}):

      href = link.get('href')

      if (rp.can_fetch("*", href) == True) and (self.normalize_url(href) not in self.visited) and (self.is_illegal_folder(href) == False) and (self.is_illegal_extension(href) == False):
        score = self.calculate_BM25_score(url) #BM25 score for the webpage
        self.urls.put((score,(href,new_depth)))


  def crawl(self):
    # Pop the URL based on priority

    while len(self.visited) <= 20 and not self.urls.empty(): # Initially trying to visit 20 pages

      next_url = self.urls.get()

      url = next_url[1][0]

      depth = next_url[1][1]
      print "Now Crawling: " + str(url)
      self.depth_reached = depth
      try:

        document = url_controller.open(url)

        mime_type = document.info().gettype()

      except IOError as e:
        print e

      # Normalise the URL before inserting

      self.visited[self.normalize_url(url)] = depth

      if mime_type in self.valid_mime_types:
        self.parse_page(document,depth,self.query)
      else:
        continue

    print self.visited

def main():
  query = 'dog'#raw_input ( 'Query: ' )

  crawler = WebCrawler(query)

  crawler.fetch_google_results()

  crawler.crawl()


if __name__ == '__main__':
  main()

