

# map properties to DC fieldsand item pages to property values
mappings = {
    'Language': {
      'property': 'P364',
      # map ISO639-1 language codes to corresponding wikidata item pages
      'map': {
        'cs': 'Q9056',
        'en': 'Q1860',
        'lv': 'Q9078',
        'pl': 'Q809',
        'ru': 'Q7737',
        'uk': 'Q8798'
        }
      },
    'DC.Source.DOI': {
      'property': 'P356'
      },
    'DC.Language': {
      'property': 'P364',
      # map ISO639-1 language codes to corresponding wikidata item pages
      'map': {
        'cs': 'Q9056',
        'en': 'Q1860',
        'lv': 'Q9078',
        'pl': 'Q809',
        'ru': 'Q7737',
        'ukr': 'Q8798'
        }
      },
    'DC.Identifier.URI': {
      'property': 'P854' # reference URL
      },
    'P953': {
      'property' : 'P953' # full work available
      },
    'DC.Creator.PersonalName': {
      'property': 'P2093' # author name string
      },
    'DC.Source.Volume': {
      'property': 'P478' # volume
      },
    'DC.Source.Issue': {
      'property': 'P433' # issue
      },
    'DC.Contributor.Sponsor': {
      'property': 'P859', # sponsor
      'delimiter': ';' # split content string at this character
      },
    'DC.Rights': {
      'property': 'P275', # license
      'map': {
        'http://creativecommons.org/licenses/by/4.0': 'Q20007257'
        }
      },
    'DC.Title': {
      'property' : 'P1476'
      },
    'DC.Subject': {
      'property' : 'P921' # main subject
      },
    'DC.Identifier': {
      'property': 'P2322' # article ID
      },
    'DC.Date.issued': {
      'property': 'P577' # publication date
      },
    'DC.Type.articleType': {
      'property': 'P136', # genre
      'map': {
        'Reviews': 'Q637866',
        'Articles': 'Q213051'
        }
      },
    'DC.Source': {},
    'DC.Source.ISSN': {},
    'DC.Type': {},
    'DC.Title.Alternative': {}


  }


