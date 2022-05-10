from xml.etree.ElementTree import Element, SubElement, tostring
from flask import Blueprint, Flask, Response, request
from rdflib import query
from app import g

bp_user = Blueprint('user', __name__, url_prefix='/users')

@bp_user.route('', methods=['GET'])
def listUsers():
    if request.args.get('page'):
        page_num = request.args.get('page')
    else:
        page_num = 1

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
    res_list = []
    for row in res:
        res_list.append(row)
    
    page_limit = 2
    total_users = len(res)
    if total_users % page_limit == 0:
        max_pages = total_users / page_limit
    else:
        max_pages = (total_users % page_limit) + 1

    if int(page_num) > max_pages:
        page_num = max_pages

    root = Element('response')
    users = SubElement(root, 'users')

    for i in range (int(page_num) - 1, int(page_num) - 1 + page_limit):
        child = SubElement(
            users, 'user', uri=request.base_url + '/' + res_list[i]['nickname'])
        child.text = res_list[i]['fullname']

    metadata = SubElement(root, 'metadata')

    count = SubElement(metadata, 'total-users')
    count.text = str(total_users)

    lim = SubElement(metadata, 'page-limit')
    lim.text = str(page_limit)

    page = SubElement(metadata, 'page')
    page.text = str(page_num)

    if int(page_num) > 1:
        previous = SubElement(metadata, 'previous')
        previous.text = request.base_url + request.path + "?page=" + str(int(page_num) - 1)
    
    if int(page_num) < max_pages:
        nex = SubElement(metadata, 'next')
        nex.text = request.base_url + request.path + "?page=" + str(int(page_num) + 1)

    return Response(tostring(root), mimetype='application/xml'), 200

@bp_user.route('/<name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
    return Response(res.serialize(format='xml'), mimetype='application/xml'), 200

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