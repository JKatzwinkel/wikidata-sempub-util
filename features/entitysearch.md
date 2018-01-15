## entity search in neonion

identification of entity during semantic classification.
first, look up search term using API action `wbsearchentities`, 

    https://www.wikidata.org/w/api.php?action=wbsearchentities&search=apparatus&language=en

then feed the results in a sparl query of the following form:


    SELECT distinct ?itemLabel ?item
    WHERE
    {
      VALUES ?item {wd:Q1183543 wd:Q620681 wd:Q30689463 wd:Q1229245 wd:Q28452457 wd:Q16829711 wd:Q28452477} . # results from wbsearchentities query
      ?item (wdt:P31/wdt:P279*) wd:Q4119870. # item representing class linked to concept used for classification in neonion
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 100
 



