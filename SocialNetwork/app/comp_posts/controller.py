from xml.etree.ElementTree import Element, SubElement, tostring
from flask import Blueprint, Flask, Response, request
from rdflib import query
from app import g

bp_post = Blueprint('post', __name__, url_prefix='/posts')

@bp_post.route('')
def listPosts():
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT ?date ?text ?author
                    WHERE {
                        ?list rdf:type mst:Post .
                        ?list mst:postDate ?date .
                        ?list mst:text ?text .
                    }
                """

    res = g.query(q)
    
    root = Element('response')

    for row in res:
        child = SubElement(root, 'post')
        date = SubElement(child, 'postDate')
        date.text = str(row['date'])
        tex = SubElement(child, 'text')
        tex.text = str(row['text'])

    return Response(tostring(root), mimetype='application/xml'), 200
