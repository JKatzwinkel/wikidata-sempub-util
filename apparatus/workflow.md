### apparatus ressourcen nach wikidata hochladen wie?

#### artikel URLs parsen

Zunaechst mal offenbar erstmal an die URLs der einzelnen artikel ranwanzen:

    curl -s "http://www.apparatusjournal.net/index.php/apparatus/issue/view/{2,3,6}" | grep -o "http:\/\/www\.apparatusjournal\.net\/index\.php\/apparatus\/article\/view\/[0-9]*\/[0-9]*" > urls_all.txt

wobei das auch schon wieder nicht aktuell ist denn es ist schon wieder eine issue hinzugekommen. Man sollte auch die URLs der issues erstmal aus dem html parsen vllt.

     curl -s http://www.apparatusjournal.net/index.php/apparatus/issue/archive | grep -o "http:\/\/www\.apparatusjournal\.net\/index\.php\/apparatus\/issue\/view\/[0-9]\+"

Dann kombinieren und bereits 57 resource locators genieszen:

    for url in $(curl -s http://www.apparatusjournal.net/index.php/apparatus/issue/archive | grep -o "http:\/\/www\.apparatusjournal\.net\/index\.php\/apparatus\/issue\/view\/[0-9]\+"); do curl -s "$url" | grep -o "http:\/\/www\.apparatusjournal\.net\/index\.php\/apparatus\/article\/view\/[0-9]\+\/[0-9]\+"; done | sort -u > urls_all.txt 


#### artikel runterladen und metadaten extrahieren

Dann habe ich damals anscheinend mit `apparatus/meta.sh` die `<meta>` tags aus dem html gepult und in eine XML datei geschrieben deren root-element `<corpus>` hiesz, genau wie sie selbst.

Aber wie bekommen wir das XML in JSON so wie wir es gern haben wollen?
Offenbar haben wir das damals mit dem commit `19fee0b8` magischerweise hinbekommen, aber nichts dazu notiert wie.

Ah ok zum glueck haben wir es doch aufgeschrieben es ist nur im anderen repo (thesis-repo). Dort in `apparatus.md` stehen ein paar hinweise und codebrocken. Haben das offenbar alles in python mit elementtree erledigt.

vorher musz man wohl noch die `DC.Description` felder rausschmeiszen wegen character encoding fehler. Das scheinen wir laut bash history folgendermaszen gemacht zu haben:

    cat corpus.xml | grep -v "DC\.Description" > corpus.xml

Dann mit elementtree ein dictionary `metadata` anlegen und befuellen:

    metadata = {}
    for r in tree.findall('resource'):      
        url=r.attrib.get('url')
        i=r.find('./meta[@name="DC.Identifier"]')
        record = {'id': i.attrib['content'],'url':url,'meta':[]}
        for e in r.getchildren():
            record['meta'].append(e.attrib)
        metadata[i.attrib['content']] = record

wir sollten ein json-object bekommen wo alles drinsteht was wir brauchen.

allerdings haben wir ein problem mit XML namespace und muessen aus der json-datei noch den ns-zusatz `{http://www.w3.org/XML/1998/namespace}` rausgreppen.

dann muessen wir uns fuer jeden artikel noch die DOI beschaffen die aber nur auf der abstract-webseite steht. 
Von jeder DOI entfernen wir jeweils den prefix `http://dx.doi.org/`.



#### bibliographische metadaten nach wikidata hochladen

Zum ingesten in wikidata dient offensichtlich das script `import_apparatus.py`. Dort wird auch das modul `apparatus/convert.py` importiert, das eine datenstruktur `mappings` enthaelt in der steht, welche wikidata property man fuer welches dublin core feld nimmt.


<!--- vim: set ts=2 sw=2 tw=0 noet ft=markdown : -->
