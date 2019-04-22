from flask import Blueprint
from flask_restplus import Api,apidoc

api_v1=Blueprint("api1",__name__,url_prefix='/api/v1')

api=Api(api_v1,version='0.1.0',title="File Manager",description='nothing to say')
