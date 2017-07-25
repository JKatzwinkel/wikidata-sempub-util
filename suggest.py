#!/usr/bin/python

from sys import argv, exit

import wiki

template= """
    select distinct ?sub ?subLabel ?property ?propertyLabel ?type ?typeLabel ?obj ?objLabel {{
      {{
        ?sub ?p wd:{entity} .
        ?sub wdt:P31|wdt:P279 ?type .
        ?property wikibase:directClaim ?p .
        SERVICE wikibase:label {{
          bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en"
        }}
      }} union {{
        wd:{entity} ?p ?obj .
        ?obj wdt:P31|wdt:P279 ?type .
        ?property wikibase:directClaim ?p .
        SERVICE wikibase:label {{
          bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en"
        }}
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


list_labels = lambda ls: ', '.join([labels.get(i) for i in set(ls)])

for prop, vals in sorted([(k,v) for k,v in properties.items()], key=lambda t:len(t[1])):
  print('\n=== {} ({})\n'.format(wiki.extract_id(prop), labels.get(prop)))
  for item, typ in vals:
    print('{} ({})  -- {} ({})'.format(
      wiki.extract_id(item), labels.get(item),
      wiki.extract_id(typ), labels.get(typ)))


    #print('{} ({}) - {}'.format(wiki.extract_id(prop), labels.get(prop), list_labels(types)))


