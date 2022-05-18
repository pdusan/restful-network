from xml.etree.ElementTree import Element, ElementTree, SubElement, tostring
from flask import Blueprint, Flask, Response, request, render_template, make_response
from rdflib import query
from app import g

bp_media = Blueprint('media', __name__, url_prefix='/media')

@bp_media.route('')
def listMedia():
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont#>

                    SELECT  ?description ?duration ?locator ?title ?upload 
                    WHERE {
                        ?s rdfs:subClassOf ma-ont:MediaResource .  
                        ?res a ?s .
                        OPTIONAL {
                            ?res ma-ont:title ?title.
                            OPTIONAL {
                                ?res ma-ont:description ?description .
                                OPTIONAL {
                                    ?res ma-ont:duration ?duration .
                                    OPTIONAL {
                                        ?res ma-ont:locator ?locator .
                                        OPTIONAL {
                                            ?res ma-ont:title ?title .
                                            OPTIONAL {
                                                ?res mst:uploadDate ?upload .
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                """

    res = g.query(q)

    root = Element('response')
    
    for row in res:
        child = SubElement(root, 'mediaObject')
        
        desc = SubElement(child, 'description')
        desc.text = str(row['description'])

        dur = SubElement(child, 'duration')
        dur.text = str(row['duration'])

        loc = SubElement(child, 'locator')
        loc.text = str(row['locator'])

        title = SubElement(child, 'title')
        title.text = str(row['title'])

        date = SubElement(child, 'upload')
        date.text = str(row['upload'])

    if request.content_type == 'application/xml':
        return Response(tostring(root), content_type='application/xml'), 200

    template = render_template('media.html', tree=root)
    response = make_response(template)

    return response, 200


@bp_media.route('/<type>')
def listMediaType(type):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont#>

                    SELECT DISTINCT ?description ?duration ?locator ?title ?upload 
                    WHERE {
                        ?res a mst:""" + str(type) + """ .    
                        OPTIONAL {
                            ?res ma-ont:title ?title.
                            OPTIONAL {
                                ?res ma-ont:description ?description .
                                OPTIONAL {
                                    ?res ma-ont:duration ?duration .
                                    OPTIONAL {
                                        ?res ma-ont:locator ?locator .
                                        OPTIONAL {
                                            ?res ma-ont:title ?title .
                                            OPTIONAL {
                                                ?res mst:uploadDate ?upload .
                                            }
                                        }
                                    }
                                }
                            }
                        } 
                    }
                """

    res = g.query(q)

    root = Element('response')
    
    for row in res:
        child = SubElement(root, 'mediaObject')
        
        desc = SubElement(child, 'description')
        desc.text = str(row['description'])

        dur = SubElement(child, 'duration')
        dur.text = str(row['duration'])

        loc = SubElement(child, 'locator')
        loc.text = str(row['locator'])

        title = SubElement(child, 'title')
        title.text = str(row['title'])

        date = SubElement(child, 'upload')
        date.text = str(row['upload'])

    if request.content_type == 'application/xml':
        return Response(tostring(root), content_type='application/xml'), 200

    template = render_template('media.html', tree=root)
    response = make_response(template)

    return response, 200