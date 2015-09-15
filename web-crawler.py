import re
import urllib
import urlnorm
import ranking_function
from ranking_function import BM25
from BeautifulSoup import BeautifulSoup
from pygoogle import pygoogle
from urlparse import urlparse
import Queue as Q

class WebCrawler:

  def __init__(self,query):
    self.query = query
    self.urls = Q.PriorityQueue() # Priority Queue of URLs to be visited and their depth [(score,(url,depth))]
    self.visited = {} # Dictionary keeping track of all the visited URLs
    self.valid_mime_types = ["text/html"]
    self.connectives = ['or','and','is','this']
    self.illegal_extensions = ['gci','gif','jpg','png','css','js']
    self.depth_reached = 0

  def calculate_BM25_score(url):
    urlib.urlretrieve(url,"temp.html")
    fn_docs = 'temp.html'
    bm25 = BM25(fn_docs,delimiter=' ')
    query = self.query.split()
    #get single normalized value of BM25 score for a page
    score = bm25.BM25Score(query)
    return score


  def fetch_google_results(self): #optimize this step
    search = pygoogle(query)
    results = search.get_urls()[:10] #Only get the first 10 results
    for result in results:
      score = self.calculate_BM25_score(result)
      self.urls.put((score,(result.encode('utf8'),1))) #All google results are at depth 1 with google.com being at depth 0 | Initially priority is 0

  def normalize_url(self,url):
    return urlnorm.norm(url).encode('utf8') #URL normalization method

  def print_visited_urls(self):
    print self.visited

  def parse_page(self,html_document,depth,query):
    url_components = urlparse(self.url)
    if url_components.path.split('.')[1] is in self.illegal_extensions:
      continue #Add a regular expression for excluding -cgi-bin | -images | -css

    soup = BeautifulSoup(html_document)

    new_depth = depth+1

    for link in soup.findAll('a', attrs={'href': re.compile("^(http|https)://")}):

      if self.normalize_url(link) not in self.visited:

        href = link.get('href')

        # Calculate BM25 score for the URL
        score = self.calculate_BM25_score(url)
        self.urls.put((score,(href,new_depth)))


  def crawl(self):
    # Pop the URL based on priority

    while len(self.visited) <= 20 and not self.urls.empty(): # Initially trying to visit 20 pages

      next_url = self.urls.get()

      url = next_url[1][0]

      depth = next_url[1][1]

      self.depth_reached = depth
      try:

        document = urllib.urlopen(url)

        mime_type = document.info().gettype()

      except IOError as e:
        print e

      # Normalise the URL before inserting

      self.visited[self.normalize_url(url)] = depth

      if mime_type in self.valid_mime_types:
        self.parse_page(document,depth,self.query)

    self.print_urls()

def main():
  query = 'dog'#raw_input ( 'Query: ' )

  crawler = WebCrawler(query)

  crawler.fetch_google_results()

  crawler.crawl()


if __name__ == '__main__':
  main()

