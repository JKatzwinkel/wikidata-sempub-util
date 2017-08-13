#!/usr/bin/python

import json

import wiki
import search
from apparatus.convert import mappings


# fetch first item matching name
def lookup(name, lang):
  results = search.lookup(name, lang=lang)
  results = results.get('search', [])
  if len(results) > 0:
    return wiki.item(results[0]['id'])

# load corpus
apparatus = json.load(open('apparatus/corpus.json', 'r'))
# use only reviews and articles (which is almost everything)
apparatus = {i:a for i,a in apparatus.items() if a['articleType'] in ['Reviews','Articles']}

for article in apparatus.values():
  lang = article['Language']
  labels = {}
  for key in ['Language']:
    prop = wiki.prop(mappings.get(key, {}).get('property'))
    value = article[key]
    link = mappings.get(key, {}).get('map', {}).get(value)
    if link:
      link = wiki.item(link)
    print('{}: {} - {} type {} {}'.format(key,
      value,
      prop,
      prop.getType(),
      '' if not link else link)
      )
  for statement in article['meta']:
    key = statement['name']
    value = statement['content']

    # put appropriate information into labels map
    if key == 'DC.Title':
      labels[lang] = value
    elif key == 'DC.Title.Alternative':
      if 'lang' in statement:
        labels[statement['lang']] = value

    # handle mapped DC properties
    if key in mappings:
      prop = wiki.prop(mappings[key].get('property'))
      target = value

      # if values have a direct mapping to wikidata items, use those
      if 'map' in mappings[key]:
        qid = mappings[key]['map'].get(value)
        if qid:
          target = wiki.item(qid)
      else:
        # reify targets if property expects wikidata item of date
        if prop.getType() == 'wikibase-item':
          target = lookup(value, statement.get('lang', 'en'))
        elif prop.getType() == 'time':
          target = wiki.create_date(value)

      print(key, value, prop, prop.getType(), target)
    else:
      print('{} not in fucking mappings'.format(key))
  print(labels)
  print()




