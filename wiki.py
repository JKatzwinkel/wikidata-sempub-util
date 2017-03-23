#!/usr/bin/python

import pywikibot as wiki

site = wiki.Site('wikidata', 'wikidata')
repo = site.data_repository()

def item(id):
  return wiki.ItemPage(repo, id)


def prop(id):
  return wiki.PropertyPage(repo, id)


def label(entity):
  labels = entity.get().get('labels', {})
  if 'en' in labels:
    return labels.get('en')
  else:
    for v in labels.values():
      return v

