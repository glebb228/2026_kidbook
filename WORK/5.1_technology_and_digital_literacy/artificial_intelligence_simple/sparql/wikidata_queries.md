# Запросы к WikiData

Запросы можно запускать в [Wikidata Query Service](https://query.wikidata.org/).

## Базовые сущности темы

```sparql
SELECT ?item ?itemLabel ?description WHERE {
  VALUES ?item {
    wd:Q11660
    wd:Q2539
    wd:Q192776
    wd:Q117246174
    wd:Q116291231
  }
  OPTIONAL {
    ?item schema:description ?description.
    FILTER(LANG(?description) = "ru")
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "ru,en". }
}
```

## Связанные понятия

```sparql
SELECT ?property ?propertyLabel ?related ?relatedLabel WHERE {
  VALUES ?item { wd:Q11660 wd:Q2539 wd:Q192776 wd:Q117246174 wd:Q116291231 }
  ?item ?property ?related.
  FILTER(STRSTARTS(STR(?related), STR(wd:)))
  SERVICE wikibase:label { bd:serviceParam wikibase:language "ru,en". }
}
LIMIT 100
```

