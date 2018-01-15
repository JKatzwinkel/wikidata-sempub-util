### accessing wikidata from python

### pywikibot 

central upstream is maintained on wikimedia's own gerrit:

    https://gerrit.wikimedia.org/r/pywikibot/core.git

- [configure pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation#Configure_Pywikibot)
- 

Here are some docs/sources of central modules/classes:

- [`ItemPage`](https://doc.wikimedia.org/pywikibot/_modules/pywikibot/page.html#ItemPage)
- [`PropertyPage`](https://doc.wikimedia.org/pywikibot/_modules/pywikibot/page.html#PropertyPage)


#### bots schreiben

der serioese weg ist offenbar, einen bot als subclass von `WikidataBot` (`pywikibot/bot.py`) zu definieren.
wenn man ihn instanziiert, sollte man anscheinend parameter `use_from_page=False` uebergeben damit er weisz dasz er 
auf items, nicht auf wikipedia pages operiert. Die idee ist dasz er dann in `treat_page_and_item` die actions ausfuehrt
die er fuer jede itempage vorgesehen hat. Welche itempages dabei drangenommen werden, kann man festlegen indem man einen
iterator in `self.generator` tut.

<!--- vim: set ts=2 sw=2 tw=120 noet ft=markdown : -->
