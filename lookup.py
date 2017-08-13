#!/usr/bin/python

from urllib.request import build_opener
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
import json
import re
from sys import stdin
import math

import wiki
from search import lookup




# load search terms from file, look them up at wikidata
#properties = {}
#entities = []
#
#for line in open('searchterms', 'r'):
#  term = line.strip()
#  res = lookup(term).get('search', {})
#  if type(res) is list and len(res) > 0:
#    res = res[0]
#    print('{} ({}) - {}'.format(
#      res.get('label'),
#      res.get('id'),
#      res.get('description')))
#    entities.append(res.get('id'))
#    claims = wiki.item(res.get('id')).get().get('claims')
#    for k,v in claims.items():
#      properties[k] = properties.get(k, 0) + 1
#  else:
#    print('{} - no result'.format(term))



#
#baseline = {}
##find random person instances at sparql endpoint
#humans = wiki.sparql('?s wdt:P31 wd:Q5', limit=100)
#for h in humans:
#  claims = wiki.item(h['s']['value']).get().get('claims')
#  for k,v in claims.items():
#    if k in properties:
#      baseline[k] = baseline.get(k,0) + 1
#
#
##show results
#for k,v in sorted(properties.items(), key=lambda t:t[1], reverse=True):
#  if v > 2 and 100*v/len(entities)>baseline.get(k):
#    p = wiki.prop(k)
#    print('{} ({}) - {} ({} %) vs {}'.format(
#      wiki.label(p),
#      p.id,
#      v,
#      100.*v/len(entities),
#      baseline.get(k)))

# load q5 (humans) from json file
humans = json.load(open('q5.json', 'r'))

propdocs = {}
def init_propdocs():
  # create inverse dictionary containing number of docs featuring specific property
  print('init inverse dictionary')
  for k in propdocs.keys():
    propdocs[k] = 0
  for props in humans.values():
    for p in props.keys():
      propdocs[p] = propdocs.get(p, 0) + 1

init_propdocs()

def idf(prop):
  # TODO for now, humans is the corpus
  try:
    return math.log(len(humans) / propdocs.get(prop, 0))
  except:
    print('division by zero:', prop)
    return 1

# interactive mode
if __name__ == '__main__':
  # read input and look up search term
  tfidf = {}
  tf = {}
  while True:
    print('>>> ',end='')
    term = stdin.readline()

    res = lookup(term).get('search', {})
    if type(res) is list and len(res) > 0:
      res = res[0]
      print('{} ({}) - {}'.format(
        res.get('label'),
        res.get('id'),
        res.get('description')))

      concepturi = res.get('concepturi')
      # save into corpus if not already in there
      if concepturi not in humans:
        claims = wiki.item(res.get('id')).get().get('claims')
        for k,v in claims.items():
          claims[k] = [c.toJSON() for c in v]
        humans[concepturi] = claims
        print('adding {} to corpus. accum size: {}'.format(res.get('label'), len(humans)))

      # measures
      for k,v in claims.items():
        # compute tfidf
        tf[k] = tf.get(k,0) + len(v)
        tfidf[k] = tf[k] * idf(k)

      avg = sum([v for k,v in tfidf.items()]) / len(tfidf)
      for k, v in sorted([(k,v) for k,v in tfidf.items()], key=lambda t:t[1]):
        if v > avg * 4 / 5 and wiki.prop(k).type != 'external-id':
          label = ' ({})'.format(wiki.label(wiki.prop(k)))
        else:
          label = ''
        print('{} - {:.2f}{}'.format(k, v, label))
