from rdflib import Graph
from flask import Flask

g = Graph().parse("v11.owl", format='xml')

app = Flask(__name__)


@app.route('/')
def greeting():
    return "Hello!"


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
    return res.serialize(format='xml')

@app.route('/users/<name>')
def listUser(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT DISTINCT ?list
                    WHERE {
                        ?list foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')

@app.route('/users/<name>/posts')
def userPosts(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT DISTINCT ?list
                    WHERE {
                        ?s foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                        ?s foaf:made ?list .
                        ?list rdf:type mst:Post
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')

@app.route('/users/<name>/comments')
def userComments(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT DISTINCT ?list
                    WHERE {
                        ?s foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                        ?s foaf:made ?list .
                        ?list rdf:type mst:Comment
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')

@app.route('/users/<name>/likes')
def userLikes(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT DISTINCT ?list
                    WHERE {
                        ?s foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                        ?s mst:likes ?list
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')

@app.route('/users/<name>/friends')
def userFriends(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT DISTINCT ?list
                    WHERE {
                        ?s foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                        ?s mst:hasFriend ?list
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')

@app.route('/posts')
def listPosts():
    q = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

        SELECT DISTINCT ?name
        WHERE {
            ?name a mst:Post
        }
    """

    res = g.query(q)
    return res.serialize(format='xml')


@app.route('/comments')
def listComments():
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT ?name
                    WHERE {
                        ?name a mst:Comment
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')


@app.route('/media')
def listMedia():  
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont#>

                    SELECT DISTINCT ?name
                    WHERE {
                        ?s rdfs:subClassOf ma-ont:MediaResource .  
                        ?name a ?s   
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')

@app.route('/media/<type>')
def listMediaType(type):  
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont#>

                    SELECT DISTINCT ?name
                    WHERE {
                        ?name a mst:""" + str(type) + """ .     
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', use_reloader='true')
