from xml.etree.ElementTree import Element, SubElement, tostring
from flask import Blueprint, Flask, Response, request
from rdflib import query
from app import g

bp_user = Blueprint('user', __name__, url_prefix='/users')

@bp_user.route('', methods=['GET'])
def listUsers():
    q = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

        SELECT DISTINCT ?nickname ?fullname
        WHERE {
            ?u a mst:User .
            ?u foaf:nick ?nickname .
            ?u foaf:name ?fullname
        }
    """

    res = g.query(q)
    root = Element('users')
    for row in res:
        child = SubElement(
            root, 'user', uri=request.base_url + '/' + row['nickname'])
        child.text = row['fullname']

    return Response(tostring(root), mimetype='application/xml'), 202

@bp_user.route('/<name>')
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

@bp_user.route('/<name>/posts')
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

@bp_user.route('/<name>/comments')
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

@bp_user.route('/<name>/likes')
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

@bp_user.route('/<name>/friends')
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