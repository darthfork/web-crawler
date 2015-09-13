import re
import urllib
import json
# import ranking-function
# from ranking-function import BM25
from BeautifulSoup import BeautifulSoup

class WebCrawler:

  def __init__(self,query):
    self.query = query
    self.urls = [] # List of URLs to be visited and their depth [(url,depth)]
    self.visited = {} # Dictionary keeping track of all the visited URLs
    self.valid_mime_types = ["text/html"]
    self.depth_reached = 0

  def fetch_google_results(self): #optimize this step
    search_query = urllib.urlencode ( { 'q' : self.query } )
    #Find a better way to get Google Results
    response1 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5' ).read()
    response2 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + search_query + '&rsz=5&start=5' ).read()
    json1 = json.loads ( response1 )
    json2 = json.loads ( response2 )
    results = json1 [ 'responseData' ] [ 'results' ] + json2 [ 'responseData' ] [ 'results' ]
    for result in results:
      self.urls.append((result['url'], 1)) #All google results are at depth 1 with google.com being at depth 0

  def normalize_url(self,url):
    return url #URL normalization method skeleton


  def print_urls(self):
    print self.urls

  def parse_page(self,html_document,depth,query): #Extract all the links from the page and add them to the URLs list
    soup = BeautifulSoup(html_document)

    new_depth = depth+1

    for link in soup.findAll('a', attrs={'href': re.compile("^(http|https)://")}):

      if self.normalize_url(link) not in self.visited:

        href = link.get('href')

        #Filter the 'href' variable above to determine if it is relevant to the query

        self.urls.append((href,new_depth))


  def crawl(self):
    # Pop first URL from the URLs list and add it to the visited list and then parse them

    while self.depth_reached <= 2: #initially trying till depth 5
      url_tuple = self.urls.pop(0)

      url = url_tuple[0]

      depth = url_tuple[1]

      self.depth_reached = depth
      try:

        document = urllib.urlopen(url)
        mime_type = document.info().gettype()

      except urllib.error as e:

        error = e.read()
        print error

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

