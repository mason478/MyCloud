from flask import Blueprint
from flask_restplus import Api,apidoc
from app.apis.files_apis import ns as file_ns

api_v1=Blueprint("api1",__name__,url_prefix='/api/v1')

api=Api(api_v1,version='0.1.0',title="File Manager",description='nothing to say')

api.add_namespace(file_ns)