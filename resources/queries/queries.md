## Can Carbamazepine be given orally?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (IF(MAX(?conditionMet) = 1, "yes", "unknown") AS ?answer)
WHERE {
    ?s a drug:Drug .
    ?s skos:prefLabel ?prefLabel .
    FILTER(lcase(?prefLabel) = "carbamazepine")
    ?s drug:usage/drug:dosage/drug:route ?route.
    BIND (
        IF (?route = "By mouth", 1, 0) 
    as ?conditionMet)
}
```

## Could Pregabalin cause delirium or aggression?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT (IF(MAX(?conditionMet) = 1, "yes", "unknown") AS ?answer)
WHERE {
    ?s a drug:Drug .
    ?s skos:prefLabel ?prefLabel .
    FILTER(lcase(?prefLabel) = "pregabalin")
    ?s drug:sideEffect ?sideEffect .
    BIND (
        IF (contains(lcase(?sideEffect), "delirium") || contains(lcase(?sideEffect), "aggression"), 1, 0) 
    as ?conditionMet)
}
```

## Can Co-Trimoxazole be given while breastfeeding?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?answer 
WHERE {
    ?s a drug:Drug .
    ?s skos:prefLabel ?prefLabel .
    FILTER(lcase(?prefLabel) = "co-trimoxazole")
    ?s drug:usage ?usage .
    ?usage drug:patientCondition "BreastFeeding" .
    OPTIONAL {
        ?usage drug:safetyLevel ?safetyLevel .
    }
    BIND (
        IF(!bound(?safetyLevel), "unknown",
          IF(?safetyLevel != "unsafe", "yes", "no"))
        AS ?answer
    )
}
```

## Is Ciclosporin safe in Pregnancy?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?answer
WHERE {
    ?s a drug:Drug .
    ?s skos:prefLabel ?prefLabel .
    FILTER(lcase(?prefLabel) = "ciclosporin")
    ?s drug:usage ?usage .
    ?usage drug:patientCondition "Pregnancy" .
    OPTIONAL {
        ?usage drug:safetyLevel ?safetyLevel .
    }
    BIND (
        IF(!bound(?safetyLevel), "unknown",
          IF(?safetyLevel = "safe", "yes", "no"))
        AS ?answer
    )
}
```

## Is it safe to take Cefadroxil for renally impaired patients?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?answer
WHERE {
    ?s a drug:Drug .
    ?s skos:prefLabel ?prefLabel .
    FILTER(lcase(?prefLabel) = lcase("Cefadroxil"))
    ?s drug:usage ?usage .
    ?usage drug:patientCondition "RenalImpairment" .
        OPTIONAL {
        ?usage drug:safetyLevel ?safetyLevel .
    }
    BIND (
        IF(!bound(?safetyLevel), "unknown",
          IF(?safetyLevel = "safe", "yes", "no"))
        AS ?answer
    )
}
```

## Can Aciclovir be used for more than 2 times per day?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?answer
WHERE {
    ?s a drug:Drug .
    ?s skos:prefLabel ?prefLabel .
    FILTER(lcase(?prefLabel) = "aciclovir")
    ?s drug:usage/drug:dosage ?dosage .
    OPTIONAL {
        ?dosage drug:frequency ?frequency.
       	?dosage drug:duration "P1D"^^xsd:duration.
        BIND (?frequency > 2 as ?initialAnswer).
    }
    BIND(IF(!BOUND(?initialAnswer), "unknown", IF(?initialAnswer = true, "yes", "no")) as ?answer)
}
```

## Can Bilastine be given to a 5 year old child?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?answer
WHERE {
    ?s a drug:Drug .
    ?s skos:prefLabel ?prefLabel .
    FILTER(lcase(?prefLabel) = "bilastine")
    ?s drug:usage/drug:dosage ?dosage .
    OPTIONAL {
    	?dosage drug:group ?patientGroup.
    }
    OPTIONAL {
    	?dosage drug:minAge ?minAge.
    }
    OPTIONAL {
    	?dosage drug:maxAge ?maxAge.
    }
    OPTIONAL {
        ?dosage drug:ageUnit ?ageUnit.
    }

    BIND (15 as ?age)
    BIND ( 
        IF (?patientGroup != "child", "unknown",
            IF(
                !BOUND(?ageUnit), 
                "unknown",
                IF(!BOUND(?minAge) && !BOUND(?maxAge), 
                   "unknown",
                    (
                        IF(
                            BOUND(?minAge) && BOUND(?maxAge) && BOUND(?ageUnit),
                            (?minAge < ?age && ?maxAge > ?age && ?ageUnit = "years"),
                            IF(
                                BOUND(?minAge) && !BOUND(?maxAge) && BOUND(?ageUnit), 
                                (?minAge < ?age && ?ageUnit = "years"),
                                IF(
                                    !BOUND(?minAge) && BOUND(?maxAge) && BOUND(?ageUnit), 
                                    (?maxAge > ?age && ?ageUnit = "years"), 
                                    "unknown"
                                )
                            )
                        )
                    )
                )
            )
        )
        as ?initialAnswer
    )
    BIND(IF(str(?initialAnswer) = "unknown", "unknown", IF(?initialAnswer = true, "yes", "no")) as ?answer)
}
```

## Is there any interaction between abacavir and carbamazepine?
```
PREFIX drug: <http://drug.uk/model/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX sh: <http://www.w3.org/ns/shacl#>

ASK {
    ?in drug:interactingDrug ?s .
    ?s skos:prefLabel ?sPrefLabel .
    FILTER(lcase(?sPrefLabel) = "abacavir")
    ?in drug:interactingDrug ?o .
    ?o skos:prefLabel ?oPrefLabel .
    FILTER(lcase(?oPrefLabel) = "carbamazepine")
}
```