# Queries on Wikidata
## Get language codes and names
    
```
SELECT DISTINCT ?code ?itemLabel 
WHERE
{
  ?item wdt:P305 ?code.
  [] wdt:P424 ?code.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER by ?code
```
