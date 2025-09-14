
def get() -> dict:
  return {
    "1" : {
        "question": "Can carbamazepine be given orally?",
        "answer": "yes",
        "drug": "carbamazepine",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    
                    SELECT (IF(MAX(?conditionMet) = 1, "yes", "unknown") AS ?answer)
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "carbamazepine")
                        ?s drug:usage/drug:dosage/drug:route ?route.
                        BIND (
                            IF (?route = "By mouth", 1, 0) 
                        as ?conditionMet)
                    }}
                    """
        ""
    },
    "2" : {
        "question": "Could pregabalin cause delirium or confusion?",
        "answer": "yes",
        "drug": "pregabalin",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    
                    SELECT (IF(MAX(?conditionMet) = -1, "unknown", IF(MAX(?conditionMet) = 1, "yes", "no")) AS ?answer)
                    WHERE {{
                            ?s a drug:Drug .
                            ?s skos:prefLabel ?prefLabel .
                            FILTER(lcase(?prefLabel) = "pregabalin")
                            OPTIONAL {{
                                    ?s drug:sideEffect ?sideEffect .
                                }}
                            BIND (
                                IF(!BOUND(?sideEffect), 
                                    -1,
                                    IF (contains(lcase(?sideEffect), "delirium") || contains(lcase(?sideEffect), "confusion"), 
                                        1, 
                                        0
                                    ) 
                                ) as ?conditionMet
                            )
                        }}
                    """
    },
    "3" : {
        "question": "Can co-trimoxazole be given while breastfeeding?",
        "answer": "yes",
        "drug": "co-trimoxazole",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    
                    SELECT ?answer 
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "co-trimoxazole")
                        ?s drug:usage ?usage .
                        ?usage drug:patientCondition "BreastFeeding" .
                        OPTIONAL {{
                            ?usage drug:safetyLevel ?safetyLevel .
                        }}
                        BIND (
                            IF(!bound(?safetyLevel), "unknown",
                              IF(?safetyLevel != "unsafe", "yes", "no"))
                            AS ?answer
                        )
                    }}
                    """
    },
    "4" : {
        "question": "Is ciclosporin safe in Pregnancy?",
        "answer": "no",
        "drug": "ciclosporin",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    
                    SELECT ?answer
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "ciclosporin")
                        ?s drug:usage ?usage .
                        ?usage drug:patientCondition "Pregnancy" .
                        OPTIONAL {{
                            ?usage drug:safetyLevel ?safetyLevel .
                        }}
                        BIND (
                            IF(!bound(?safetyLevel), "unknown",
                              IF(?safetyLevel = "safe", "yes", "no"))
                            AS ?answer
                        )
                    }}
                    """
    },
    "5" : {
        "question": "Is it safe to take cefadroxil for renally impaired patients?",
        "answer": "no",
        "drug": "cefadroxil",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    
                    SELECT ?answer
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "cefadroxil")
                        ?s drug:usage ?usage .
                        ?usage drug:patientCondition "RenalImpairment" .
                        OPTIONAL {{
                            ?usage drug:safetyLevel ?safetyLevel .
                        }}
                        BIND (
                            IF(!bound(?safetyLevel), "unknown",
                              IF(?safetyLevel = "safe", "yes", "no"))
                            AS ?answer
                        )
                    }}
                    """
    },
    "6" : {
        "question": "Can aciclovir be used for more than 2 times per day?",
        "answer": "yes",
        "drug": "aciclovir",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    
                    SELECT ?answer
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "aciclovir")
                        ?s drug:usage/drug:dosage ?dosage .
                        OPTIONAL {{
                            ?dosage drug:frequency ?frequency.
                            ?dosage drug:duration "P1D"^^xsd:duration.
                            BIND (?frequency > 2 as ?initialAnswer).
                        }}
                        BIND(IF(!BOUND(?initialAnswer), "unknown", IF(?initialAnswer = true, "yes", "no")) as ?answer)
                    }}
                    """
    },
    "7" : {
        "question": "Can bilastine be given to a 15 year old child?",
        "answer": "yes",
        "drug": "bilastine",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    
                    SELECT ?answer
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "bilastine")
                        ?s drug:usage/drug:dosage ?dosage .
                        OPTIONAL {{
                            ?dosage drug:group ?patientGroup.
                        }}
                        OPTIONAL {{
                            ?dosage drug:minAge ?minAge.
                        }}
                        OPTIONAL {{
                            ?dosage drug:maxAge ?maxAge.
                        }}
                        OPTIONAL {{
                            ?dosage drug:ageUnit ?ageUnit.
                        }}
                    
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
                    }}
                    """
    },
    "8" : {
        "question": "Is there any interaction between abacavir and carbamazepine?",
        "answer": "yes",
        "drug": "abacavir-interactions",
        "prompt-template": "nl-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                        SELECT ?answer
                        WHERE {{
                            BIND (
                                IF (
                                    EXISTS {{
                                        ?in drug:interactingDrug/skos:prefLabel ?sPrefLabel .
                                        FILTER(lcase(?sPrefLabel) = "abacavir")
                                        ?in drug:interactingDrug/skos:prefLabel ?oPrefLabel .
                                        FILTER(lcase(?oPrefLabel) = "carbamazepine")
                                    }},
                                    "yes",
                                    "no"
                                ) as ?answer
                            )
                        }}
                    """
    },
    "9": {
        "question": "For an adult, what is the dosage amount and dosage unit of abacavir for HIV infection?",
        "answer": "600.0, mg",
        "drug": "abacavir",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "abacavir")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("HIV infection"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "10": {
        "question": "For an adult, what is the dosage amount and dosage unit of abaloparatide for Constipation?",
        "answer": "unknown, unknown",
        "drug": "abaloparatide",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "abaloparatide")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("constipation"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "11": {
        "question": "For an adult, what is the dosage amount and dosage unit of aciclovir for Herpes simplex keratitis?",
        "answer": "1.0, cm",
        "drug": "aciclovir",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "aciclovir")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("Herpes simplex keratitis"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "12": {
        "question": "For an adult, what is the dosage amount and dosage unit of alendronic acid for Treatment and prevention of postmenopausal osteoporosis?",
        "answer": "70.0, mg",
        "drug": "alendronic-acid",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "alendronic acid")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("Treatment and prevention of postmenopausal osteoporosis"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "13": {
        "question": "For an adult, what is the dosage amount and dosage unit of amitriptyline hydrochloride for Neuropathic pain?",
        "answer": "25.0, mg",
        "drug": "amitriptyline-hydrochloride",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "amitriptyline hydrochloride")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("neuropathic pain"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "14": {
        "question": "For an adult, what is the dosage amount and dosage unit of amlodipine for Hypertension?",
        "answer": "10.0, mg",
        "drug": "amlodipine",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "amlodipine")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("hypertension"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "15": {
        "question": "For an adult, what is the dosage amount and dosage unit of apixaban for Treatment of deep-vein thrombosis?",
        "answer": "10.0, mg",
        "drug": "apixaban",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "apixaban")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("treatment of deep-vein thrombosis"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "16": {
        "question": "For an adult, what is the dosage amount and dosage unit of atorvastatin for Hypercholesterolaemia?",
        "answer": "10.0, mg",
        "drug": "atorvastatin",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "atorvastatin")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("hypercholesterolaemia"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "17": {
        "question": "For an adult, what is the dosage amount and dosage unit of betaxolol for Ocular hypotension?",
        "answer": "unknown, unknown",
        "drug": "betaxolol",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "betaxolol")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("ocular hypotension"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "18": {
        "question": "For an adult, what is the dosage amount and dosage unit of bilastine for Symptomatic relief of allergic rhinoconjunctivitis and urticaria?",
        "answer": "unknown, unknown",
        "drug": "bilastine",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "bilastine")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("symptomatic relief of allergic rhinoconjunctivitis and urticaria"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "19": {
        "question": "For an adult, what is the dosage amount and dosage unit of carbamazepine for Epilepsy?",
        "answer": "unknown, unknown",
        "drug": "carbamazepine",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "carbamazepine")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("Epilepsy"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "20": {
        "question": "For an adult, what is the dosage amount and dosage unit of cefadroxil for Skin infections?",
        "answer": "unknown, unknown",
        "drug": "cefadroxil",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "cefadroxil")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("Skin infections"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "21": {
        "question": "For an adult, what is the dosage amount and dosage unit of ciclosporin for Severe psoriasis?",
        "answer": "2.5, mg/kg",
        "drug": "ciclosporin",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "ciclosporin")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("Severe psoriasis"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "22": {
        "question": "For an adult, what is the dosage amount and dosage unit of co-trimoxazole for Leg ulcer infection?",
        "answer": "960.0, mg",
        "drug": "co-trimoxazole",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "co-trimoxazole")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("leg ulcer infection"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "23": {
        "question": "For an adult, what is the dosage amount and dosage unit of flucloxacillin for Pneumonia?",
        "answer": "unknown, unknown",
        "drug": "flucloxacillin",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "flucloxacillin")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("pneumonia"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "24": {
        "question": "For an adult, what is the dosage amount and dosage unit of gelatin for Stabiliser in vaccines?",
        "answer": "1.0, L",
        "drug": "gelatin",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "gelatin")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("Stabiliser in vaccines"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "25": {
        "question": "For an adult, what is the dosage amount and dosage unit of hyoscine butylbromide for Gastrointestinal smooth muscle spasm?",
        "answer": "20.0, mg",
        "drug": "hyoscine-butylbromide",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "hyoscine butylbromide")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("Gastrointestinal smooth muscle spasm"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "26": {
        "question": "For an adult, what is the dosage amount and dosage unit of paracetamol for Fever?",
        "answer": "1.0, g",
        "drug": "paracetamol",
        "prompt-template": "dosage-qa-template.txt",
        "query": """PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "paracetamol")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("fever"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "27": {
        "question": "For an adult, what is the dosage amount and dosage unit of pregabalin for Generalised anxiety disorder?",
        "answer": "200.0, mg",
        "drug": "pregabalin",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "pregabalin")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("generalised anxiety disorder"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    },
    "28": {
        "question": "For an adult, what is the dosage amount and dosage unit of zilucoplan for Myasthenia gravis?",
        "answer": "32.4, mg",
        "drug": "zilucoplan",
        "prompt-template": "dosage-qa-template.txt",
        "query": """ PREFIX drug: <http://drug.uk/model/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>   
                    SELECT ?amount ?unit
                    WHERE {{
                        ?s a drug:Drug .
                        ?s skos:prefLabel ?prefLabel .
                        FILTER(lcase(?prefLabel) = "zilucoplan")
                        
                        ?s drug:usage ?usage.
                        ?usage drug:indication ?indication.
                        FILTER(lcase(?indication) = lcase("myasthenia gravis"))
                        
                        ?usage drug:dosage ?dosage .
                        ?dosage drug:group "adult".
                        ?dosage drug:amount ?amount.
                        ?dosage drug:unit ?unit
                    }}
                """
    }
}