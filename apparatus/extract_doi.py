#!/usr/bin/python


import json
import re
from urllib.request import urlopen

doix=re.compile('http:\/\/dx\.doi\.org\/10\.[0-9]{5}\/app\.[0-9]{4}\.[0-9.-]{4,}')
doipx = re.compile(r'http:\/\/dx\.doi\.org\/')


# extract DOI from article's abstract page
metadata = json.load(open('corpus.json', 'r'))
for resource in metadata.values():
    print('.', end='')
    abstract_uris = [m['content'] for m in resource['meta'] if m['name'] == 'DC.Identifier.URI']
    if len(abstract_uris) > 0:
        doi_url = None
        # parse webpage
        for line in urlopen(abstract_uris[0]):
            uris = doix.findall(u'{}'.format(line))
            if len(uris) > 0:
                # take DOI but remove prefix
                doi_url = doipx.sub('', uris[0])
                print('.', end='')
        resource['doi'] = doi_url
    print(' ', end='')

    # remove fields with empty values
    meta = [m for m in resource['meta'] if len(m['content']) > 0]
    resource['meta'] = meta

    # move language and articletype fields up to root level for easier access
    top = [m for m in resource['meta'] if m['name'] in ['DC.Language','DC.Type.articleType']]
    for m in top:
        key = m['name'].split('.')[-1]
        resource[key] = m['content']

    # add source doi pointing to this apparatus journal article
    resource['meta'].append({"name": "DC.Source.DOI", "content": doi_url})


json.dump(metadata, open('corpus.json', 'w'), indent=True, ensure_ascii=False)


