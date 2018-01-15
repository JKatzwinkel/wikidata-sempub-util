#!/bin/bash

function fileage {
	echo $(($(date +%s) - $(date +%s -r $1)))	
}

# if this hasn't just been done anyway..
if [[ $(fileage urls_all.txt) -gt 43200 ]]; then
	# retrieve all apparatus article URLs from website
	echo "retrieve article URLs from apparatus website..."

	for url in $(curl -s http://www.apparatusjournal.net/index.php/apparatus/issue/archive \
		| grep -o "http:\/\/www\.apparatusjournal\.net\/index\.php\/apparatus\/issue\/view\/[0-9]\+"); do 
		curl -s "$url" | grep -o "http:\/\/www\.apparatusjournal\.net\/index\.php\/apparatus\/article\/view\/[0-9]\+\/[0-9]\+"; 
	done | sort -u > urls_all.txt 
fi


# if metadata files are still fresh, skip this
if [[ $(fileage corpus.xml) -gt 300 ]]; then
	total=$(cat urls_all.txt | wc -l)
	echo "begin extraction of metadata from $total web resources..."

	# create XML file with metadata
	echo "<corpus>" > corpus.xml

	# load publication urls, retrieve resource and extract <meta> fields featuring dublin core vocabulary
	counter=0
	while read url; do
		(( counter++ ))
		echo "$counter / $total : $url"
		echo "<resource url=\"$url\">" >> corpus.xml
		# extract <meta> elements
		curl -s "$url" | grep -o "<meta name=\"DC\.[^>]*\/>" >> corpus.xml
		echo "</resource>" >> corpus.xml
	done < urls_all.txt

	echo "</corpus>" >> corpus.xml


	#echo "remove DC.Description fields"
	# remove DC.Description fields because of character encoding problems
	#cat corpus.xml | grep -v "DC\.Description" > corpus.bck
	#mv corpus.bck corpus.xml

	# make sure there is no ISO639-1 violation where lang=ukr
	sed -i 's/\(ISO639-1.*\)ukr/\1uk/' corpus.xml

fi


echo "export XML metadata to JSON file"
# convert XML to json
python xml2json.py

# remove elementtree xml namespace artifact
echo "fix namespace artifacts from previous step"
sed -i  's/{http:\/\/www\.w3\.org\/XML\/1998\/namespace}//g' corpus.json 


# go back to apparatus website and extract DOI identifiers from article abstract pages
echo "extract DOI strings from apparatus web ressources and restructure metadata a little bit"
python extract_doi.py



