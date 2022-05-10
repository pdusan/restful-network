from flask import Flask
from rdflib import Graph

g = Graph().parse("SocialNetwork/app/resources/v11.owl", format='xml')

app = Flask(__name__)

app.config.from_object('config')

@app.route("/")
def start():
    return "HELLO"

from app.comp_users.controller import bp_user as users
from app.comp_posts.controller import bp_post as posts
from app.comp_comments.controller import bp_comment as comments
from app.comp_media.controller import bp_media as media

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(comments)
app.register_blueprint(media)