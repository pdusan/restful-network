from unicodedata import name
from xml.etree.ElementTree import Element, SubElement, tostring
from flask import Blueprint, Flask, Response, redirect, request
from pyparsing import rest_of_line
from rdflib import query
from app import g

bp_user = Blueprint('user', __name__, url_prefix='/users')

@bp_user.route('', methods=['GET', 'POST'])
def listUsers():
    if request.method == 'GET':
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
            max_pages = (total_users // page_limit) + 1

        if int(page_num) > max_pages:
            page_num = max_pages

        root = Element('response')
        users = SubElement(root, 'users')

        for i in range (page_limit):
            try:
                child = SubElement(
                    users, 'user', uri=request.base_url + '/' + res_list[(int(page_num) - 1) * page_limit + i]['nickname'])
                child.text = res_list[(int(page_num) - 1) * page_limit + i]['fullname']
            except:
                break

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
    if request.method == 'POST':
        name = request.form['name']
        nick = request.form['nickname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        email = request.form['email']
        joined = request.form['joined']

        q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
            PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>
            PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>

            ASK {
                ?s foaf:nick ?o .
                FILTER(str(?o) = \"""" + nick + """\")
            }
        """
        res = g.query(q)
        res_list = []
        for row in res:
            res_list.append(row)
        
        if res_list[0]:
            return "User with that nickname already exists", 400
        else:

            q = """
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>
                PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>

                INSERT DATA {
                    ?s a mst:User .
                    ?s foaf:name \"""" + name + """\" .
                    ?s foaf:nick \"""" + nick + """\" .
                    ?s foaf:gender \"""" + gender + """\" .
                    ?s mst:birthday \"""" + birthday + """\" .
                    ?s mst:email \"""" + email + """\" .
                    ?s mst:joined \"""" + joined + """\" .
                }
            """

            g.update(q)
            print(len(g))

            return redirect("/users/"+nick), 201 
    else:
        return "Bad request", 400

@bp_user.route('/<name>', methods=['GET', 'PUT', 'DELETE'])
def listUser(name):
    if request.method == "GET":
        q = """
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                        SELECT ?name ?nickname ?gender ?birthday ?email ?joined
                        WHERE {
                            ?list foaf:nick ?nickname .
                            FILTER(str(?nickname) = \"""" + str(name) + """\") .
                            ?list foaf:name ?name .
                            ?lsit foaf:gender ?gender .
                            ?list mst:birthday ?birthday .
                            ?list mst:email ?email .
                            ?list mst:joined ?joined .
                        }
                    """

        res = g.query(q)
        res_list = []
        for row in res:
            res_list.append(row)

        root = Element('user')

        child_name = SubElement(root, 'name')
        child_name.text = str(res_list[0]['name'])

        child_nickname = SubElement(root, 'nickname')
        child_nickname.text = str(res_list[0]['nickname'])

        child_gender = SubElement(root, 'gender')
        child_gender.text = str(res_list[0]['gender'])

        child_birthday = SubElement(root, 'birthday')
        child_birthday.text = str(res_list[0]['birthday'])

        child_email = SubElement(root, 'email')
        child_email.text = str(res_list[0]['email'])

        child_joined = SubElement(root, 'joined')
        child_joined.text = str(res_list[0]['joined'])

        return Response(tostring(root), mimetype='application/xml'), 200

    if request.method == "DELETE":
        q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
            PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

            DELETE {
                ?s foaf:nick ?t .
            }
            WHERE {
                ?s foaf:nick ?t .
                FILTER(str(?t) = \"""" + str(name) + """\") .
            }
        """

        res = g.update(q)

        return redirect('/users/'), 204
    
    if request.method == "PUT":
        


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