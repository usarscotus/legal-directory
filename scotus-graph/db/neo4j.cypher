// Cypher setup for SCOTUS citation graph

// Ensure unique constraint on opinion id
CREATE CONSTRAINT opinion_id IF NOT EXISTS
FOR (o:Opinion) REQUIRE o.id IS UNIQUE;

// Load opinions
// :param opinions_csv => path to courtlistener_opinions.csv
LOAD CSV WITH HEADERS FROM $opinions_csv AS row
MERGE (o:Opinion {id: toInteger(row.id)})
SET o.docket = row.docket,
    o.case_name = row.case_name,
    o.date_filed = row.date_filed,
    o.citation = row.citation,
    o.absolute_url = row.absolute_url;

// Load citation relationships
// :param citations_csv => path to courtlistener_citations.csv
LOAD CSV WITH HEADERS FROM $citations_csv AS row
MATCH (src:Opinion {id: toInteger(row.source_id)}),
      (tgt:Opinion {id: toInteger(row.target_id)})
MERGE (src)-[:CITES]->(tgt);
