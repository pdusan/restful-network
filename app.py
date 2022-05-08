from rdflib import Graph

g = Graph().parse("v11.owl", format='xml')

q = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?name
    WHERE {
        ?p rdf:type foaf:User .
    }
"""

print(g.serialize(format="turtle"))
