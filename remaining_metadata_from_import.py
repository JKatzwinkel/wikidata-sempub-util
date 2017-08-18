#!/usr/bin/python

import json

from apparatus.convert import mappings


metadata = json.load(open('apparatus/remains.json', 'r'))

for identifier, article in metadata.items():
  table = []
  # register required fields
  header = ['name', 'content']

  print('\n[{}] http://www.wikidata.org/wiki/{} ({}, {})'.format(
    article.get('item_page'), article.get('item_page'),
    article.get('Language'), article.get('articleType')))

  # read all statements
  for statement in article['meta']:
    row = {}
    for k,v in statement.items():
      if not k in header:
        header += [k]
      row[header.index(k)] = v
    table += [row]

  # add field names to table
  table.insert(0, {i:f for i,f in enumerate(header)})

  # format table
  width = lambda k:max([len(row.get(header.index(k),'')) for row in table])
  widths = {k:width(k) for k in header}
  # header line
  template = u' | '.join([u'{{: <{}}}'.format(widths[field]) for field in header])
  print(template.format(*['-'*widths[field] for field in header]))
  print(template.format(*header))
  print(template.format(*['-'*widths[field] for field in header]))
  for row in table[1:]:
    print(template.format(*[row.get(k,'') for k in range(len(header))]))





