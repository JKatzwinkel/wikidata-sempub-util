#!/usr/bin/python

import re as _re
import pywikibot as _wiki

from SPARQLWrapper import SPARQLWrapper, JSON

__all__ = ['repo', 'sparql', 'item', 'prop', 'label', 'extract_id']

_sparqli = SPARQLWrapper('https://query.wikidata.org/bigdata/namespace/wdq/sparql')
_sparqli.setReturnFormat(JSON)

_site = _wiki.Site('wikidata', 'wikidata')
repo = _site.data_repository()

def create_item():
  """ returns a newly created item page """
  return _wiki.ItemPage(repo)

def create_claim(pid):
  """ Pass property identifier string (P...) """
  return _wiki.Claim(repo, pid)

def create_date(date):
  """ give date in format: 'YYYY-MM-DD' """
  fields = date.split('-')
  if len(fields) == 3:
    kwargs = {key:int(fields[i]) for i,key in enumerate(['year','month','day'])}
    return _wiki.WbTime(**kwargs)
  return None

def extract_id(url):
  """ Extracts item or property ID from any string."""
  return _re.findall("[PpQq][1-9][0-9]*", url)[0]

def item(id):
  if not id.lower().startswith('q'):
    id = extract_id(id)
  return _wiki.ItemPage(repo, id)


def prop(id):
  if not id.lower().startswith('p'):
    id = extract_id(id)
  return _wiki.PropertyPage(repo, id)


def label(entity):
  labels = entity.get().get('labels', {})
  if 'en' in labels:
    return labels.get('en')
  else:
    for v in labels.values():
      return v

def sparql(query, limit=500):
  _sparqli.setQuery('select * where {{{}}} limit {}'.format(query, limit))
  results = _sparqli.query().convert()
  return results.get('results', {}).get('bindings', [])

