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

                    SELECT ?name
                    WHERE {
                        ?name a mst:Comment
                    }
                """

    res = g.query(q)
    return res.serialize(format='xml')