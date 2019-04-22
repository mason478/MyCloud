import os

from flask_restplus import Api, Namespace, fields, Resource
from flask import send_from_directory
from flask import url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from app.commons.change_format import RET,add_response
from app.commons.setting import UPLOAD_FILE_PATH
from app.commons.input_checker.filename_checking import is_allowed_file

ns = Namespace('files')

upload_parser = ns.parser()
upload_parser.add_argument('file', type=FileStorage, location='files', required=True)


@ns.route('/upload')
class UploadFiles(Resource):
    @ns.doc(parser=upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        file = args['file']
        filename=is_allowed_file(file.filename)
        if filename is False:
            return add_response(r_code=RET.FILE_ERROR)

        file.save(os.path.join(UPLOAD_FILE_PATH, filename))
        return add_response(r_code=RET.OK,j_dict={"url":url_for('api1.files_download',filename=file.filename)})


@ns.route('/download/<string:filename>')
class Download(Resource):
    def get(self, filename):
        return send_from_directory(UPLOAD_FILE_PATH, filename)
