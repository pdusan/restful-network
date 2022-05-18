from xml.etree.ElementTree import Element, SubElement, tostring
from flask import Blueprint, Flask, Response, request, render_template, make_response
from rdflib import query
from app import g

bp_comment = Blueprint('comment', __name__, url_prefix='/comments')


def sparql_contains(words):
    ret = """"""
    for word in words:
        ret += "FILTER CONTAINS(lcase(str(?text)), \""+word+"\") . \n"
    return ret


@bp_comment.route('')
def listComments():
    if request.args.get('search'):
        params = request.args.get('search')
        keywords = params.split()

        q = """
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                        SELECT ?date ?text ?search ?count ?author ?authornick
                        WHERE {
                            ?list rdf:type mst:Comment .
                            VALUES ?search {\"""" + params + """\"} 
                            ?list mst:text ?text .
                            """ + sparql_contains(keywords) + """
                            OPTIONAL {
                                ?list foaf:maker ?t .
                                ?t foaf:nick ?authornick .
                                ?t foaf:name ?author .
                                OPTIONAL {
                                    ?list mst:postDate ?date .
                                }
                            }
                            BIND(((strlen(?text) - strlen(replace(?text, ?search, ""))) / strlen(?search)) as ?count)
                        } ORDER BY DESC(?count)
                    """

    else:
        q = """
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                        SELECT ?date ?text ?author ?authornick
                        WHERE {
                            ?list rdf:type mst:Comment .
                            ?list mst:text ?text .
                            OPTIONAL {
                                ?list foaf:maker ?t .
                                ?t foaf:nick ?authornick .
                                ?t foaf:name ?author .
                                OPTIONAL {
                                    ?list mst:postDate ?date .
                                }
                            }
                        }
                    """

    res = g.query(q)

    root = Element('response')

    for row in res:
        child = SubElement(root, 'comment')
        tex = SubElement(child, 'text')
        tex.text = str(row['text'])
        if row['date']:
            postDate = SubElement(child, 'postDate')
            postDate.text = str(row['date'])
        if row['author']:
            author = SubElement(
                child, 'commenter', uri=request.host_url + 'users/' + row['authornick'])
            author.text = str(row['author'])

    if request.content_type == 'application/xml':
        return Response(tostring(root), content_type='application/xml'), 200

    template = render_template('comments.html', tree=root)
    response = make_response(template)

    return response, 200
