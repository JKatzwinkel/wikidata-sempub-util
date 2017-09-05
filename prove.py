import wiki
import json
import sys

journal="Q38110802"
prove = wiki.item(journal)
proven = json.load(open('import/{}.json'.format(journal), 'r'))

for qid, dat in proven.items():
  if 'item_page' in dat:
    itempage = wiki.item(dat.get('item_page'))
    claims = itempage.get().get('claims')
    for pid, claim_list in claims.items():
      if pid in dat.get('properties', {}):
        print('featured property', pid)
        for claim in claim_list:
          target = claim.getTarget()
          if target.id in dat.get('properties', {}).get(pid, []):
            print(target.id, pid, qid)
            wiki.add_source_url(claim, itempage=target)
            sys.exit(0)





