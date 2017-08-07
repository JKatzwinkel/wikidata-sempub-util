#!/bin/bash

echo "<corpus>" > corpus.xml

# load publication urls, retrieve resource and extract <meta> fields featuring dublin core vocabulary
while read url; do
	echo "<resource url=\"$url\">" >> corpus.xml
	# extract <meta> elements
	curl -s "$url" | grep -o "<meta name=\"DC\.[^>]*\/>" >> corpus.xml
	echo "</resource>" >> corpus.xml
done < urls_all.txt

echo "</corpus>" >> corpus.xml
