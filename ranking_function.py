'''
    This gile calcualtes the Okapi BM25 ranking function for comparing pages
    The web-crawler file passes a webpage to this file
    The method BM25 score is then invoked which calculates the BM25 score of the webpage based on a specified query.
    References: https://en.wikipedia.org/wiki/Okapi_BM25
'''
import gensim
from gensim import corpora
import math

class BM25 :
    def __init__(self, fn_docs, delimiter='|') :
        self.dictionary = corpora.Dictionary()
        self.DF = {}
        self.delimiter = delimiter
        self.DocTF = []
        self.DocIDF = {}
        self.N = 0
        self.DocAvgLen = 0
        self.fn_docs = fn_docs
        self.DocLen = []
        self.buildDictionary()
        self.TFIDF_Generator()

    def buildDictionary(self) :
        raw_data = []
        try:
            for line in self.fn_docs:
                raw_data.append(line.strip().split(self.delimiter))
            self.dictionary.add_documents(raw_data)
        except IOError:
            pass
        except UnicodeDecodeError:
            pass

    def TFIDF_Generator(self, base=math.e) :
        try:
            docTotalLen = 0
            for line in self.fn_docs:
                doc = line.strip().split(self.delimiter)
                docTotalLen += len(doc)
                self.DocLen.append(len(doc))
                #print self.dictionary.doc2bow(doc)
                bow = dict([(term, freq*1.0/len(doc)) for term, freq in self.dictionary.doc2bow(doc)])
                for term, tf in bow.items() :
                    if term not in self.DF :
                        self.DF[term] = 0
                    self.DF[term] += 1
                self.DocTF.append(bow)
                self.N = self.N + 1
            for term in self.DF:
                self.DocIDF[term] = math.log((self.N - self.DF[term] +0.5) / (self.DF[term] + 0.5), base)
            self.DocAvgLen = docTotalLen / self.N
        except UnicodeDecodeError:
            pass

    def BM25Score(self, Query=[], k1=1.5, b=0.75) :
        try:
            query_bow = self.dictionary.doc2bow(Query)
            scores = []
            for idx, doc in enumerate(self.DocTF) :
                commonTerms = set(dict(query_bow).keys()) & set(doc.keys())
                tmp_score = []
                doc_terms_len = self.DocLen[idx]
                for term in commonTerms :
                    upper = (doc[term] * (k1+1))
                    below = ((doc[term]) + k1*(1 - b + b*doc_terms_len/self.DocAvgLen))
                    tmp_score.append(self.DocIDF[term] * upper / below)
                scores.append(sum(tmp_score))
            return int(math.ceil(sum(scores)))
        except ZeroDivisionError:
             pass

    def TFIDF(self) :
        tfidf = []
        for doc in self.DocTF :
            doc_tfidf  = [(term, tf*self.DocIDF[term]) for term, tf in doc.items()]
            doc_tfidf.sort()
            tfidf.append(doc_tfidf)
        return tfidf

