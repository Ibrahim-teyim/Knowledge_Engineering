from rdflib import Graph, Literal, RDF, URIRef


kg = Graph()
kg.parse("knowledge_graph.ttl", format="turtle")
print("Number of triples in the KG: ", len(kg))

# show some elements within the KG
# for s, p, o in kg:
#     print(s, p, o)
query = """
    PREFIX ex: <http://example.org/>
    SELECT ?news ?ratings
    WHERE {
        ?news a ex:News .
        ?news ex:ratings ?ratings .
    }
    ORDER BY DESC(?ratings)
    LIMIT 1
"""
# Execute the query
results = kg.query(query)

# Print the results
for row in results:
    actor = str(row[0]).replace(
        "file:///Users/ibrahimteymurlu/Documents/Code/Knowledge_Engineering/", ""
    )
    print(f"Actor: {actor}")
