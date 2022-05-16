from flask import Blueprint, Flask, Response, request, app
from rdflib import query
from config import UPLOAD_DIR



bp_upload = Blueprint('upload', __name__, url_prefix='/upload')

@bp_upload.route('', methods=['POST'])
def uploadGraph():

    file = request.files['graph']
    name = file.filename

    file.save(UPLOAD_DIR, name)

    return "Graph Added", 201