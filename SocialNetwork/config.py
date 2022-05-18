import os
from distutils.log import debug
from pickle import TRUE


debug = TRUE

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_DIR = BASE_DIR + '/app/resources/'
