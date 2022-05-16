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

                    SELECT ?date ?text ?author ?authornick ?comment 
                    WHERE {
                        ?list rdf:type mst:Post .
                        ?list mst:postDate ?date .
                        ?list mst:text ?text .
                        OPTIONAL {
                            ?list foaf:maker ?o .
                            ?o foaf:nick ?authornick .
                            ?o foaf:name ?author .
                            ?list mst:hasComment ?comment .
                        }
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
        if row['authornick']:
            author = SubElement(
                child, 'poster', uri=request.host_url + 'users/' + row['authornick'])
            author.text = str(row['author'])
        if row['comment']:
            comments = SubElement(child, 'comments')
            q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT ?text 
                    WHERE {
                        ?list rdf:type mst:Post .
                        ?list mst:postDate ?date .
                        ?list mst:text ?text .
                    }
                """
            

    return Response(tostring(root), mimetype='application/xml'), 200
