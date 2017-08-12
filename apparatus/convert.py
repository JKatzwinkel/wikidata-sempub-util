#!/usr/bin/python

# map ISO639-1 language codes to corresponding wikidata item pages
lang_map = {'cs': 'Q9056',
  'en': 'Q1860',
  'lv': 'Q9078',
  'pl': 'Q809',
  'ru': 'Q7737',
  'ukr': 'Q8798'}

mappings = {
    'Language': {
      'property': 'P364'
      },
    'doi': {
      'property': 'P356'
      },
    'id': {
      'property': 'P2322'
      },
    'url': {
      'property' : 'P953'
      },
    'Creator.PersonalName': {
      'property': 'P2093'
      },
    'Source.Volume': {
      'property': 'P478'
      },
    'Source.Issue': {
      'property': 'P433'
      },
    'Contributor.Sponsor': {
      'property': 'P859'
      },
    'Rights': {
      'property': 'P275'
      }
    'Title': {
      'property' : 'P1476'
      }
    'Subject': {
      'property' : 'P921'
      }

  }
