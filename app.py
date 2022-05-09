from rdflib import Graph
from flask import Flask

g = Graph().parse("v11.owl", format='xml')

app = Flas(__name__)

@app.route('/users')
def listUsers():
    q = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

        SELECT DISTINCT ?name
        WHERE {
            ?name a mst:User
        }
    """
    res = g.query(q)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')
