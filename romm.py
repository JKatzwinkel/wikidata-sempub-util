#!/usr/bin/python

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

def str_claim(claim):
  t = c.target
  if type(t) is wiki.page.ItemPage:
    return '{} ({})'.format(t.id, t.get().get('labels', {}).get('en'))
  else:
    return '{} ({})'.format(t, type(t))
  return t.toJSON()



# set up connection to wikidata
site = wiki.Site("wikidata", "wikidata")
repo = site.data_repository()


# retrieve item page
#item = wiki.ItemPage(repo, "q461726") # romm
#item = wiki.ItemPage(repo, "q957911") # jan leyda
#item = wiki.ItemPage(repo, "q5449165")
item = wiki.ItemPage(repo, "q42")


# retrieve item dictionary
idict = item.get()
# get claims dictionary
claims = idict.get("claims", {})

# go thru claims
for p, clist in claims.items():
  prop = wiki.PropertyPage(repo, p)
  print('{} ({}):'.format(p, prop.get().get('labels', {}).get('en')))
  for c in clist:
    print(' {}'.format(str_claim(c)))
    if len(c.qualifiers) > 0:
      print('  {}'.format(c.qualifiers))

# show claims made about occupation (P106)
#for claim in claims.get("P106"):
#  print_json(claim.toJSON())

