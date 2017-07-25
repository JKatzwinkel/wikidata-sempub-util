#!/usr/bin/python

from sys import argv, exit

import wiki

template= """
    select distinct ?sub ?subLabel ?property ?propertyLabel ?type ?typeLabel ?obj ?objLabel {{
      {{
        ?sub ?p wd:{entity} .
        ?sub wdt:P31 ?type .
        ?property wikibase:directClaim ?p .
        SERVICE wikibase:label {{
          bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en"
        }}
      }} union {{
        wd:{entity} ?p ?obj .
        ?obj wdt:P31 ?type .
        ?property wikibase:directClaim ?p .
        SERVICE wikibase:label {{
          bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en"
        }}
      }}
    }}"""

templ_super = """
  select distinct ?superclass ?superclassLabel {{
    wd:{entity} wdt:P279 ?superclass .
    SERVICE wikibase:label {{
      bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
    }}
  }}"""

if len(argv) > 1:
  query = template.format(entity=argv[1])
else:
  exit()

res = wiki.sparql(query)

properties = {}
types = {}
labels = {}

get = lambda record, key: record.get(key, {}).get('value')

for fact in res:
  item = get(fact, 'obj') or get(fact, 'sub')
  label= get(fact, 'objLabel') or get(fact, 'subLabel')
  prop = get(fact, 'property')
  plbl = get(fact, 'propertyLabel')
  typ  = get(fact, 'type')
  tlbl = get(fact, 'typeLabel')
  # store values
  labels[item] = label
  labels[prop] = plbl
  labels[typ] = tlbl
  properties[prop] = properties.get(prop, []) + [(item, typ)]
  types[prop] = types.get(prop, []) + [typ]




def common_superclass(entities):
  concepts = {e:[] for e in entities}
  for entity in [e for e,k in concepts.items() if len(k) < 1]:
    res = wiki.sparql(templ_super.format(entity=wiki.extract_id(entity)))
    if len(res) > 0:
      concepts[entity] = [get(r, 'superclass') for r in res]
      for concept in concepts[entity]:
        concepts[concept] = []
    else:
      concepts.pop(entity)
  # graph assembly done
  # now walk up tree
  visits = {}
  frontier = set(entities)
  while len(frontier) > 0:
    for entity in frontier.copy():
      # perform step from concept to superclass
      frontier.remove(entity)
      frontier.update(set(concepts.get(entity, [])))
      for c in concepts.get(entity, []):
        visits[c] = visits.get(c, 0) + 1
  # return betweenness values
  return visits







for prop, vals in sorted([(k,v) for k,v in properties.items()], key=lambda t:len(t[1])):
  print('\n=== {} ({})'.format(wiki.extract_id(prop), labels.get(prop)))
  for item, typ in sorted(vals):
    print('val: {} ({})  --> {} ({})'.format(
      wiki.extract_id(item), labels.get(item),
      wiki.extract_id(typ), labels.get(typ)))
  visits = common_superclass([t for i,t in vals])
  for k,v in sorted([(k,v) for k,v in visits.items()], key=lambda t:t[1]):
    if v > 1:
      print('{} : {}'.format(k, v))
    #   print('common superclasses:')
    #   superclasses = common_superclass([t for i,t in vals])
    #   for concept in superclasses:
    #     print('{} {}'.format(concept, labels.get(concept)))




