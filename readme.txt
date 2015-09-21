List of files:

1. web-crawler.py - Main program file containing the crawler, the parser and a method to fetch results from google. This file when executed crawls the web based on a query passed by the user

2. ranking_function.py - This file is used to calculate the ranking function of a given webpage provided a query. The ranking function depends on how much the webpage is relevant to the given query.

3. customurllib.py - Overriden urllib library for handling http_401 / Unauthorized access error.

Execution:

To execute the program install all the libraries listed in the requirements.txt file. After complete installation run the file 'web-crawler.py'. The program will then ask the user for a query. Based on that query the crawler will crawl the web and write the results in a file named output.txt

Known Bugs:

1. The program, for some webpages throws a UnicodeEncodeError where it has trouble parsing some unicode to utf-8 while calculating BM25 score and other places. I am unsure what MIME type is causing this error and I am unable to recreate it.

Output file pattern:

Pattern = "URL | BM25 score | depth | return code | time"
