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
  res = []
  for entity_id in argv[1:]:
    query = template.format(entity=entity_id)
    res.extend(wiki.sparql(query))
else:
  exit()


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
  for i in range(2):
    for entity in [e for e,k in concepts.items() if len(k) < 1]:
      res = wiki.sparql(templ_super.format(entity=wiki.extract_id(entity)))
      for fact in res:
        labels[get(fact, 'superclass')] = get(fact, 'superclassLabel')
      if len(res) > 0:
        concepts[entity] = [get(r, 'superclass') for r in res]
        for concept in concepts[entity]:
          concepts[concept] = []
      else:
        concepts.pop(entity)
  # graph assembly done
  # now walk up tree
  visits = {e:entities.count(e) for e in entities}
  frontier = entities[:]
  while len(frontier) > 0:
    for entity in frontier[:]:
      # perform step from concept to superclass
      frontier.remove(entity)
      frontier.extend(concepts.get(entity, []))
      for c in concepts.get(entity, []):
        visits[c] = visits.get(c, 0) + 1
  # return betweenness values
  return visits





recommendations = {}
recommendedprop = {}

for prop, vals in sorted([(k,v) for k,v in properties.items()], key=lambda t:len(t[1])):
  print('\n=== {} ({}) ({}) ==='.format(wiki.extract_id(prop), labels.get(prop), len(vals)))
  # count how often a class occurs
  class_support = {}
  for item, typ in sorted(vals):
    print('val: {} ({})  --> {} ({})'.format(
      wiki.extract_id(item), labels.get(item),
      wiki.extract_id(typ), labels.get(typ)))
    class_support[typ] = class_support.get(typ,0) + 1
  if len(vals) > 2:
    print('support:')
    for k,v in sorted([(k,v) for k,v in class_support.items()], key=lambda t:t[1]):
      if v > 1:
        print('{} ({}): {}'.format(k, labels.get(k), v))
        if v == max(class_support.values()) and v/len(vals) > .6:
          recommendations[k] = recommendations.get(k, []) + [(prop, v/len(vals))]
          # if class has strong support, the associated property can be considered
          # a potential recommendation
          recommendedprop[prop] = v
    # get data from class inheritance traversal
    # but only if none of the classes found under this property has
    # a decisive support itself
    if max(class_support.values()) / len(vals) < .6:
      print('support of common superclasses:')
      visits = common_superclass([t for i,t in vals])
      for k,v in sorted([(k,v) for k,v in visits.items()], key=lambda t:t[1]):
        if v > 1:
          print('{} ({}): {}'.format(k, labels.get(k), v))
          if v == max(visits.values()) and v/len(vals) > .7:
            recommendations[k] = recommendations.get(k, []) + [(prop, v/len(vals))]
            # only if there is a strong concept associated, current property can become
            # recommendation
            recommendedprop[prop] = v

      #   print('common superclasses:')
      #   superclasses = common_superclass([t for i,t in vals])
      #   for concept in superclasses:
      #     print('{} {}'.format(concept, labels.get(concept)))



print('\n\n---------------------\nwould recommend classes:')
for rec, supporting in recommendations.items():
  print('{} ({})'.format(rec, labels.get(rec)))
  for prop, support in supporting:
    print('   {:.2f} at {} ({})'.format(
      support, wiki.extract_id(prop), labels.get(prop)))
  print()

print('properties:')
for rec, support in recommendedprop.items():
  print('{} ({}) with {:.2f}'.format(rec, labels.get(rec), support))

