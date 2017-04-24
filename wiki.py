#!/usr/bin/python

import re
import pywikibot as wiki

from SPARQLWrapper import SPARQLWrapper, JSON

sparqli = SPARQLWrapper('https://query.wikidata.org/bigdata/namespace/wdq/sparql')
sparqli.setReturnFormat(JSON)

site = wiki.Site('wikidata', 'wikidata')
repo = site.data_repository()

def extract_id(url):
  """ Extracts item or property ID from any string."""
  return re.findall("[PpQq][1-9][0-9]*", url)[0]

def item(id):
  if not id.lower().startswith('q'):
    id = extract_id(id)
  return wiki.ItemPage(repo, id)


def prop(id):
  if not id.lower().startswith('p'):
    id = extract_id(id)
  return wiki.PropertyPage(repo, id)


def label(entity):
  labels = entity.get().get('labels', {})
  if 'en' in labels:
    return labels.get('en')
  else:
    for v in labels.values():
      return v

def sparql(query, limit=500):
  sparqli.setQuery('select * where {{{}}} limit {}'.format(query, limit))
  results = sparqli.query().convert()
  return results.get('results', {}).get('bindings', [])

