from urllib.request import build_opener
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
import json

import wiki

ends = {'search': 'https://www.wikidata.org/w/api.php'}

related_types_query_template = '{{?s ?p wd:{obj}}} union {{wd:{obj} ?p ?s}} . ?s wdt:P31 ?item'

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



def related_types(qid):
    """ returns the types of all entities directly related to given item via whatever property """
    return wiki.query(related_types_query_template.format(obj=qid))


def quick_labels(pagelist):
    """ use Site.preloaditempages method to get quick previews of item pages capable of supplying label strings. """
    return [q.get().get('labels',{}).get('en') for q in wiki._site.preloaditempages(pagelist)]

