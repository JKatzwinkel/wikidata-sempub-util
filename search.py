from urllib.request import build_opener
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
import json

ends = {'search': 'https://www.wikidata.org/w/api.php'}


def request(url, **kwargs):
  kwargs['format'] = 'json'

  opener = build_opener()
  url = "%s?%s" % (url, urlencode(kwargs))

  try:
    wdata = opener.open(url).read().decode()

  except (URLError, HTTPError) as e:
    print(e)

  return wdata


def lookup(query, lang='en'):
  """ Goes to wikidata and tries to return item or property as json."""
  param = {
      'action': 'wbsearchentities',
      'language': lang,
      'search': query}
  wdata = request(ends['search'], **param)
  result = json.loads(wdata)
  return result


