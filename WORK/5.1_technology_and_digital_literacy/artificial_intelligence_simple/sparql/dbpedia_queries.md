# Запросы к DBpedia

Запросы можно запускать в [DBpedia SPARQL Endpoint](https://dbpedia.org/sparql).

## Описания базовых сущностей

```sparql
SELECT ?item ?label ?abstract WHERE {
  VALUES ?item {
    <http://dbpedia.org/resource/Artificial_intelligence>
    <http://dbpedia.org/resource/Machine_learning>
    <http://dbpedia.org/resource/Artificial_neural_network>
    <http://dbpedia.org/resource/Generative_artificial_intelligence>
  }
  OPTIONAL {
    ?item rdfs:label ?label.
    FILTER(LANG(?label) = "en")
  }
  OPTIONAL {
    ?item dbo:abstract ?abstract.
    FILTER(LANG(?abstract) = "en")
  }
}
```

## Связанные ресурсы

```sparql
SELECT ?property ?related WHERE {
  <http://dbpedia.org/resource/Artificial_intelligence> ?property ?related.
  FILTER(ISIRI(?related))
}
LIMIT 100
```

