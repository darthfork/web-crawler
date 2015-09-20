'''
  Overriding the urllib library to check for unauthorized pages
'''
import urllib
class customURLlib(urllib.FancyURLopener):
  def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
    return None
