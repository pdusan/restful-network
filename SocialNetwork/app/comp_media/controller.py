from xml.etree.ElementTree import Element, SubElement, tostring
from flask import Blueprint, Flask, Response, request
from rdflib import query
from app import g

bp_media = Blueprint('media', __name__, url_prefix='/media')

@bp_media.route('')
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


@bp_media.route('/<type>')
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