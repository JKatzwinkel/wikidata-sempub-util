

# map properties to DC fields and item pages to property values
mappings = {
    'Language': {
      'property': 'P407',
      # map ISO639-1 language codes to corresponding wikidata item pages
      'map': {
        'cs': 'Q9056',
        'en': 'Q1860',
        'lv': 'Q9078',
        'pl': 'Q809',
        'ru': 'Q7737',
        'uk': 'Q8798',
        'de': 'Q188'
        }
      },
    'DC.Source.DOI': {
      'property': 'P356'
      },
    'DC.Language': {
      'property': 'P407',
      # map ISO639-1 language codes to corresponding wikidata item pages
      'map': {
        'cs': 'Q9056',
        'en': 'Q1860',
        'lv': 'Q9078',
        'pl': 'Q809',
        'ru': 'Q7737',
        'uk': 'Q8798',
        'de': 'Q188'
        }
      },
    'DC.Identifier.URI': {
#      'property': 'P856' # official website
      },
    'P953': {
      'property' : 'P953' # full work available
      },
    'DC.Creator.PersonalName': {
      'property': 'P2093' # author name string
      },
    'P50': {
      'property': 'P50' # author
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
    'DC.Coverage.spatial': {
        'property': 'P921', #main subject
        'delimiter': '[,;]'
      },
     'DC.Coverage.temporal': {
        'property': 'P921', #main subject
        'delimiter': '[,;]'
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
        'Reviews': 'Q637866', # book review
        'Articles': None, # don't use property
        'Editorial': 'Q871232', # editorial
        'Interviews': 'Q4202018' # interview
        }
      },
    'DC.Source': {},
    'DC.Source.ISSN': {},
    'DC.Type': {},
    'DC.Title.Alternative': {},
    'DC.Description': {}


  }

