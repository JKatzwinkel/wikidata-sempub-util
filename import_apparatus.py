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

# remaining properties that we could not import automatically
remains = {}

cnt = 0
for identifier, article in apparatus.items():
  cnt += 1
  if cnt > 1:
    break
  # extract lang
  lang = article['Language']
  labels = {}

  # create record for failed properties
  remains[identifier] = {
      'meta' : []
      }
  for key in ['Language', 'articleType']:
    remains[identifier][key] = article[key]

  # if item page is already assigned, then skip
  if 'item_page' in article:
    continue

  # otherwise, create itempage
  item_page = wiki.create_item()
  article['item_page'] = item_page.id

  # iterate over DC metadata
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

      if prop: # no property field means ignore this key
        # see if we need to split value string
        if 'delimiter' in mappings[key]:
          values = value.split(mappings[key]['delimiter'])
        else:
          values = [value]

        for value in values:

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

          # log if we fail to import statement
          if not target:
            remains[identifier]['meta'].append(statement)
          else:
            # create claim
            claim = wiki.create_claim(prop.id)
            claim.setTarget(target)
            # support claim with article URL
            wiki.add_source_url(claim, article['url'])
            # add claim to item page
            item_page.addClaim(claim, bot=True)

          print(key, value, prop, prop.getType(), target)

    else:
      # log if we can't map property
      remains[identifier]['meta'].append(statement)

  # add labels to item page
  item_page.editLabels(labels=labels, bot=True)

  print(labels)
  print()


# save corpus data
json.dump(apparatus, open('apparatus/corpus.json', 'w'),
    indent=True, ensure_ascii=False)

# save corpus data we could not import automatically
json.dump(remains, open('apparatus/remains.json', 'w+'),
    indent=True, ensure_ascii=False)


