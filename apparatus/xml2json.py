#!/usr/bin/python

import xml.etree.ElementTree as ET
import json
import os

if os.path.exists('corpus.json'):
    metadata = json.load(open('corpus.json', 'r'))
else:
    metadata = {}


tree = ET.parse('corpus.xml')

for r in tree.findall('resource'):
    print('.', end='')

    url = r.attrib.get('url')
    idfield = r.find('./meta[@name="DC.Identifier"]')
    identifier = idfield.attrib['content']

    authorfields = r.findall('./meta[@name="DC.Creator.PersonalName"]')
    authors = [a.attrib['content'] for a in authorfields]


    # try to use metadata records from existing json file if possible
    record = metadata.get(identifier, {'id': identifier, 'url': url})
    # put some extra fields in there for multiple utilization of values
    record['meta'] = [{"name": "P953", "content": url}]
    for author in authors:
        record['meta'].append({"name": "P50", "content": author})

    # copy metadata
    for e in r.getchildren():
        record['meta'].append(e.attrib)

    metadata[identifier] = record

with open('corpus.json', 'w+') as dumpfile:
    json.dump(metadata, dumpfile, ensure_ascii=False, indent=True)


