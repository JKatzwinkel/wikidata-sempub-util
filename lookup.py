#!/usr/bin/python

from urllib.request import build_opener
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
import json

import wiki

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


def lookup(query):
  param = {
      'action': 'wbsearchentities',
      'language': 'en',
      'search': query}
  wdata = request(ends['search'], **param)
  result = json.loads(wdata)
  return result


properties = {}

for line in open('searchterms', 'r'):
  term = line.strip()
  res = lookup(term).get('search', {})
  if type(res) is list and len(res) > 0:
    res = res[0]
    print('{} ({}) - {}'.format(
      res.get('label'),
      res.get('id'),
      res.get('description')))
    claims = wiki.item(res.get('id')).get().get('claims')
    for k,v in claims.items():
      properties[k] = properties.get(k, 0) + 1

for k,v in sorted(properties.items(), key=lambda t:t[1], reverse=True):
  p = wiki.prop(k)
  print('{} ({}) - {}'.format(
    wiki.label(p),
    p.id,
    v))

