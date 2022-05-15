from xml.etree.ElementTree import Element, SubElement, tostring
from flask import Blueprint, Flask, Response, request
from rdflib import query
from app import g

bp_comment = Blueprint('comment', __name__, url_prefix='/comments')

@bp_comment.route('')
def listComments():
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT ?date ?text
                    WHERE {
                        ?s foaf:made ?list .
                        ?list rdf:type mst:Comment .
                        ?list mst:text ?text .
                    }
                """

    res = g.query(q)
    
    root = Element('response')

    for row in res:
        child = SubElement(root, 'post')
        tex = SubElement(child, 'text')
        tex.text = str(row['text'])

    return Response(tostring(root), mimetype='application/xml'), 200