#!/usr/bin/python

from sys import argv
import json

from pygments import highlight, lexers, formatters

import pywikibot as wiki



def print_json(json_obj, indent=2):
  # Print formatted and highlighted json
  pretty = json.dumps(json_obj, indent=2)
  colorful = highlight(pretty,
      lexers.JsonLexer(),
      formatters.TerminalFormatter())
  print(colorful)




# set up connection to wikidata
site = wiki.Site("wikidata", "wikidata")
repo = site.data_repository()

for arg in argv[1:]:
  if arg.lower().startswith('p'):
    item = wiki.PropertyPage(repo, arg)
  if arg.lower().startswith('q'):
    item = wiki.ItemPage(repo, arg)
  info = item.get()
  print(info.get('labels',{}).get('en'))
  for k, claims in info.get('claims',{}).items():
    prop = wiki.PropertyPage(repo, k)
    print('{} ({})'.format(prop.id, prop.get().get('labels',{}).get('en')))
    for claim in claims:
      print_json(claim.toJSON())


