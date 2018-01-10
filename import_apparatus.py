#!/usr/bin/python

import json
from sys import argv
import re

import wiki
import search
from apparatus.convert import mappings

# helper function for lookup
def exact_match(record, name, lang):
  if record.get('description', '') != 'Wikipedia disambiguation page':
    match = record.get('match', {})
    if match.get('text', '').lower() == name.lower():
      if match.get('language', '') == lang:
        return True
  return False

# try and retrieve wikidata item by name search
def lookup(name, lang):
  results = search.lookup(name, lang=lang)
  results = results.get('search', [])
  # only use results with exact matching labels
  results = [r for r in results if exact_match(r, name, lang)]
  # only use result if there is only a single one left (no ambiguity)
  if len(results) == 1:
    return wiki.item(results[0]['id'])

# default statements:
default_statements = {
    # published in apparatus
    'P1433': ['Q30689463'],
    # instance of academic journal article
    'P31': ['Q18918145']
    }


# if article ids are passed as command line arguments, we only process those articles
selected_keys = argv[1:] if len(argv) > 1 else None
if selected_keys:
  print('about to import article{}'.format('s' if len(selected_keys)>1 else ''),
      ', '.join(selected_keys))


# load corpus
apparatus = json.load(open('apparatus/corpus.json', 'r'))

# remaining properties that we could not import automatically
try:
  remains = json.load(open('apparatus/remains.json', 'r'))
except:
  remains = {}

cnt = 0
for identifier in selected_keys or apparatus.keys():
  article = apparatus.get(identifier)
  # use only reviews and articles (which is almost everything)
  # and only resources that have not been imported yet
  #if not article or article['articleType'] not in ['Reviews', 'Articles'] or article.get('done'):
  if not article or article.get('done'):
    continue

  # after ingestion of 1 article, we stop
  cnt += 1
  if cnt > 1 and not selected_keys:
    break

  # extract lang
  lang = article['Language']
  labels = {}
  descriptions = {}

  print('processing resource # {} ({})'.format(identifier, lang))

  # if item page is already assigned, use this item page to populate
  if 'item_page' in article:
    item_page = wiki.item(article['item_page'])
    print('loaded item page ', item_page)
  else:
    # otherwise, create itempage
    item_page = wiki.create_item()
    article['item_page'] = item_page.id
    print('created item page {}'.format(item_page.id))

    article['item_page'] = item_page.id

  # create record for failed properties
  remains[identifier] = {
      'meta' : []
      }
  for key in ['Language', 'articleType']:
    remains[identifier][key] = article[key]
  remains[identifier]['item_page'] = item_page.id

  # add default statements
  for p, qq in default_statements.items():
    for q in qq:
      claim = wiki.create_claim(p)
      target = wiki.item(q)
      claim.setTarget(target)
      item_page.addClaim(claim, bot=True)
      #provide proof!!!
      wiki.add_source_url(claim, article['url'])

  # register all reified objects of statements using certain property
  # in order to avoid identical statements to be made
  related_entities = {}

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
    elif key == 'DC.Description':
      if 'lang' in statement:
        descriptions[statement['lang']] = value

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
          values = re.split(mappings[key]['delimiter'], value)
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
              # issue a search for items matching the string, use result if there is only one candidate
              # use english if field has no language qualifier
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

              if not (type(target) == wiki._wiki.page.ItemPage and
                  target in related_entities.get(prop.id, [])):

                print('creating claim using property {}'.format(prop.id))
                # create claim
                claim = wiki.create_claim(prop.id)
                print('claim {} about to have target set: {}'.format(claim, target))
                claim.setTarget(target)
                # add claim to item page
                print('add claim to item page {}'.format(item_page.id))
                item_page.addClaim(claim, bot=True)
                # support claim with article URL
                print('add source URL as a reference: {}'.format(article['url']))
                wiki.add_source_url(claim, article['url'])

                # if target is an item, register statement in order to avoid doubles
                if type(target) == wiki._wiki.page.ItemPage:
                  related_entities[prop.id] = related_entities.get(prop.id, []) + [target]

              else:
                print('target {} already used in statement with property {}.'.format(target.id, prop.id))

            except Exception as e:

              print('error: {}'.format(e))
              print('could not import statement {}'.format(split_statement))
              remains[identifier]['meta'].append(split_statement)



          print(key, value, prop, prop.getType(), target)

    else:
      # log if we can't map property
      remains[identifier]['meta'].append(statement)

  # flag article as processed
  article['done'] = True

  # add labels and descriptions to item page
  item_page.editLabels(labels=labels, bot=True)
  item_page.editDescriptions(descriptions=descriptions, bot=True)


  print(labels)
  print()


# save corpus data
json.dump(apparatus, open('apparatus/corpus.json', 'w'),
    indent=True, ensure_ascii=False)

# save corpus data we could not import automatically
json.dump(remains, open('apparatus/remains.json', 'w+'),
    indent=True, ensure_ascii=False)


