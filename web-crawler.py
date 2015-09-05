import re, urllib, json as m_json

def fetch_google_results(passed_query):
  urls = []
  query = passed_query
  query = urllib.urlencode ( { 'q' : query } )
  response1 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query + '&rsz=5' ).read()
  response2 = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query + '&rsz=5&start=5' ).read()
  json1 = m_json.loads ( response1 )
  json2 = m_json.loads ( response2 )
  results = json1 [ 'responseData' ] [ 'results' ] + json2 [ 'responseData' ] [ 'results' ]
  for result in results:
    urls.append(result['url'])
  return urls


def parse_page(url,query):
    handle = urllib.urlopen(url)
    html_gunk = handle.read()
    print html_gunk

def main():
  query = raw_input ( 'Query: ' )
  search_results = fetch_google_results(query)
  parse_page(search_results[0],query)

if __name__ == '__main__':
  main()

