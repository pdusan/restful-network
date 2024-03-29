from config import BASE_DIR
from flask import Flask
from rdflib import Graph


app = Flask(__name__)

app.config.from_object('config')

g = Graph().parse(BASE_DIR+"/app/resources/v11.owl", format='xml')

q = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX mst: <https://mis.cs.univie.ac.at/ontologies/2021SS/mst#>
            PREFIX ma-ont: <http://www.w3.org/ns/ma-ont>

            INSERT {
                ?s foaf:nick "Maxie" .
            }
            WHERE {
                ?s a mst:User .
                ?s foaf:name ?t .
                FILTER (str(?t) = "Maximilian Meyer")
            }
        """

res = g.update(q)

@app.route("/")
def start():
    return "HELLO"

from app.comp_users.controller import bp_user as users
from app.comp_posts.controller import bp_post as posts
from app.comp_comments.controller import bp_comment as comments
from app.comp_media.controller import bp_media as media
from app.comp_upload.controller import bp_upload as upload

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(comments)
app.register_blueprint(media)
app.register_blueprint(upload)