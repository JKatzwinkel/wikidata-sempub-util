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

# remaining properties that we could not import automatically
remains = {}

cnt = 0
for identifier, article in apparatus.items():
  # use only reviews and articles (which is almost everything)
  # and only resources that have not been imported yet
  if article['articleType'] not in ['Reviews', 'Articles'] or article.get('done'):
    continue

  cnt += 1
  if cnt > 1:
    break

  # extract lang
  lang = article['Language']
  labels = {}

  print('processing resource # {} ({})'.format(identifier, lang))

  # create record for failed properties
  remains[identifier] = {
      'meta' : []
      }
  for key in ['Language', 'articleType']:
    remains[identifier][key] = article[key]

  # if item page is already assigned, use this item page to populate
  if 'item_page' in article:
    item_page = wiki.item(article['item_page'])
  else:
    # otherwise, create itempage
    item_page = wiki.create_item()
    article['item_page'] = item_page.id
    print('created item page {}'.format(item_page.id))

    item_page.touch()
    article['item_page'] = item_page.id

  remains[identifier]['item_page'] = item_page.id

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
      # retrieve property object from wikidata
      prop = mappings[key].get('property')
      if prop:
        prop = wiki.prop(prop)

      if prop: # no property field means ignore this key
        print('use property {}'.format(prop))
        # see if we need to split value string
        if 'delimiter' in mappings[key]:
          values = value.split(mappings[key]['delimiter'])
        else:
          values = [value]

        for value in values:
          print('value:', value)

          split_statement = {k:v for k,v in statement.items()}
          split_statement['content'] = value

          target = value

          # if values have a direct mapping to wikidata items, use those
          if 'map' in mappings[key]:
            qid = mappings[key]['map'].get(value)
            if qid:
              target = wiki.item(qid)
            else:
              target = None
          else:
            # reify targets if property expects wikidata item of date
            if prop.type == 'wikibase-item':
              target = lookup(value, statement.get('lang', 'en'))
            elif prop.type == 'time':
              target = wiki.create_date(value)
            elif prop.type == 'monolingualtext':
              target = wiki.create_monolingualtext(value, lang)

          # log if we fail to import statement
          if not target:
            remains[identifier]['meta'].append(split_statement)
            print('could not import statement:', split_statement)
          else:
            try:

              print('creating claim using property {}'.format(prop.id))
              # create claim
              claim = wiki.create_claim(prop.id)
              print('claim {} about to have target set: {}'.format(claim, target))
              claim.setTarget(target)
              # support claim with article URL
              #print('add source URL as a reference: {}'.format(article['url']))
              #wiki.add_source_url(claim, article['url'])
              # add claim to item page
              print('add claim to item page {}'.format(item_page.id))
              item_page.addClaim(claim, bot=True)

              article['done'] = True

            except Exception as e:

              print('error: {}'.format(e))
              print('could not import statement {}'.format(split_statement))
              remains[identifier]['meta'].append(split_statement)



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


