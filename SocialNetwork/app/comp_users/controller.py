from xml.etree.ElementTree import Element, ElementTree, SubElement, tostring
from flask import Blueprint, Flask, Response, make_response, redirect, render_template, render_template_string, request, url_for
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

        for i in range(page_limit):
            try:
                child = SubElement(
                    users, 'user', uri=request.base_url + '/' + res_list[(int(page_num) - 1) * page_limit + i]['nickname'])
                child.text = res_list[(int(page_num) - 1)
                                      * page_limit + i]['fullname']
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
            previous.text = request.base_url + request.path + \
                "?page=" + str(int(page_num) - 1)

        if int(page_num) < max_pages:
            nex = SubElement(metadata, 'next')
            nex.text = request.base_url + request.path + \
                "?page=" + str(int(page_num) + 1)

        if request.content_type == 'application/xml':
            return Response(tostring(root), content_type='application/xml'), 200

        template = render_template_string("""
            <html>
                <body>
                    {% for i in tree.find('./users') %}
                        <a href={{i.attrib['uri']}}> {{i.text}} </a> <br>
                    {%endfor%}
                    <br>
                    <br>
                    <br> Total Users: {{tree.find('./metadata/total-users')}} <br>
                    <br>
                    {% if tree.find('./metadata/previous') != None %}
                        <a href = {{tree.find('./metadata/previous').text}}> Prev </a>
                    {%endif%}
                    
                    page  {{tree.find('./metadata/page').text}}  /  {{tree.find('./metadata/page-limit').text}}
                    
                    {% if tree.find('./metadata/next') != None %}
                        <a href = {{tree.find('./metadata/next').text}}> Next </a>
                    {%endif%}

                </body>
            </html>
        """, tree=root)
        response = make_response(template)

        return response, 200

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
            PREFIX rdf: <http://www.w3.org/2000/01/rdf-schema#>

            ASK {
                ?s foaf:nick ?o .
                FILTER(str(?o) = \"""" + name + """\")
            }
        """
        res = g.query(q)
        res_list = []
        for row in res:
            res_list.append(row)

        if not res_list[0]:
            return "User with that nickname does not exist", 400

        q = """
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                        SELECT ?name ?nickname ?gender ?birthday ?email ?joined
                        WHERE {
                            ?list a mst:User .
                            ?list foaf:nick ?nickname .
                            FILTER(str(?nickname) = \"""" + str(name) + """\") .
                            OPTIONAL{?list foaf:name ?name .}
                            OPTIONAL{?lsit foaf:gender ?gender .}
                            OPTIONAL{?list mst:birthday ?birthday .}
                            OPTIONAL{?list mst:email ?email .}
                            OPTIONAL{?list mst:joined ?joined .}
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

        child_posts = SubElement(root, 'posts')
        child_posts.text = str(request.base_url + '/posts')

        child_comments = SubElement(root, 'comments')
        child_comments.text = str(request.base_url + '/comments')

        child_likes = SubElement(root, 'likes')
        child_likes.text = str(request.base_url + '/likes')

        child_friends = SubElement(root, 'friends')
        child_friends.text = str(request.base_url + '/friends')

        return Response(tostring(root)), 200

    if request.method == "DELETE":
        q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
            PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

            DELETE {
                ?s foaf:nick ?t .
            }
            WHERE {
                ?s a mst:User .
                ?s foaf:nick ?t .
                FILTER(str(?t) = \"""" + str(name) + """\") .
            }
        """

        res = g.update(q)

        return redirect('/users/'), 204

    if request.method == "PUT":

        for item in request.form:
            if not request.form[item] == "":
                if item in ['name', 'nick', 'gender']:
                    q = """
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                        DELETE {
                            ?s foaf:""" + item + """ ?o .
                        }
                        INSERT {
                            ?s foaf:""" + item + """ \"""" + str(request.form[item]) + """\"
                        }
                        WHERE {
                            ?s a mst:User .
                            ?s foaf:nick ?t .
                            FILTER(str(?t) = \"""" + str(name) + """\") .
                            ?s foaf:""" + item + """ ?o .
                        }
                    """
                    res = g.update(q)
                else:
                    q = """
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                        DELETE {
                            ?s mst:""" + item + """ ?o .
                        }
                        INSERT {
                            ?s mst:""" + item + """ \"""" + str(request.form[item]) + """\"
                        }
                        WHERE {
                            ?s a mst:User .
                            ?s mst:nick ?t .
                            FILTER(str(?t) = \"""" + str(name) + """\") .
                            ?s mst:""" + item + """ ?o .
                        }
                    """
                    res = g.update(q)

        return "Updated", 200


@bp_user.route('/<name>/posts')
def userPosts(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT DISTINCT ?date ?text
                    WHERE {
                        ?s foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                        ?s foaf:made ?list .
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

    return Response(tostring(root)), 200


@bp_user.route('/<name>/comments')
def userComments(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT ?date ?text
                    WHERE {
                        ?s foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                        ?s foaf:made ?list .
                        ?list rdf:type mst:Comment .
                        ?list mst:text ?text .
                        OPTIONAL {
                            ?list mst:postDate ?date .
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

    return Response(tostring(root)), 200


@bp_user.route('/<name>/likes', methods=['GET', 'PUT', 'DELETE'])
def userLikes(name):
    q = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                    PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                    SELECT ?list
                    WHERE {
                        ?s foaf:nick ?t 
                        FILTER(str(?t) = \"""" + str(name) + """\") .
                        ?s mst:likes ?list
                    }
                """

    res = g.query(q)

    root = Element('response')
    for row in res:
        child = SubElement(root, 'like')
        child.text = str(row['list'])

    return Response(tostring(root)), 200


@bp_user.route('/<name>/friends', methods=['GET', 'PUT', 'DELETE'])
def userFriends(name):
    if request.method == 'GET':
        q = """
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
                        PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

                        SELECT DISTINCT ?nickname ?name
                        WHERE {
                            ?s foaf:nick ?t 
                            FILTER(str(?t) = \"""" + str(name) + """\") .
                            ?s mst:hasFriend ?list .
                            ?list foaf:nick ?nickname .
                            ?list foaf:name ?name .
                        }
                    """

        res = g.query(q)

        root = Element('Response')
        for row in res:
            child = SubElement(
                root, 'friend', uri=request.host_url + 'users/' + row['nickname'])
            child.text = str(row['name'])

        return Response(tostring(root)), 200

    if request.method == 'DELETE':
        nick = request.form['nickname']

        q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
            PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

            DELETE {
                ?s mst:hasFriend ?t .
                ?t mst:hasFriend ?s .
            }
            WHERE {
                ?s foaf:nick ?n .
                FILTER(str(?n) = \"""" + str(name) + """\") .
                ?t a mst:User .
                ?t foaf:nick ?nickname
                FILTER(str(?nickname) = \"""" + str(nick) + """\") .
            }
        """
        res = g.update(q)

        return redirect(request.base_url), 204

    if request.method == 'PUT':
        nick = request.form['nickname']

        q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
            PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

            INSERT {
                ?s mst:hasFriend ?t .
                ?t mst:hasFriend ?s .
            } 
            WHERE {
                ?t foaf:nick ?name .
                FILTER(str(?name) = \"""" + str(name) + """\") .
                ?s a mst:User .
                ?s foaf:nick ?nickname .
                FILTER(str(?nickname) = \"""" + str(nick) + """\") .
            }
        """
        res = g.update(q)

        return redirect(request.base_url), 200
    else:
        return "Bad Request", 400
