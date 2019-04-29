import os

from flask_restplus import Api, Namespace, fields, Resource, reqparse
from flask import send_from_directory
from flask import url_for
from werkzeug.datastructures import FileStorage

from app.commons.change_format import RET, add_response
from app.commons.setting import UPLOAD_FILE_PATH
from app.commons.input_checker.filename_checking import is_allowed_file
from app.commons.auth.moudles import TokenBase
from app.commons.auth import auth_required
from app.commons.common_init import logger

ns = Namespace('files')

base_parse = reqparse.RequestParser()
base_parse.add_argument('Authorization', type=str, location='headers', required=True)

upload_parser = base_parse.copy()
upload_parser.add_argument('file', type=FileStorage, location='files', required=True)


@ns.route('/upload')
class UploadFiles(Resource):
    @ns.doc(parser=upload_parser)
    @auth_required
    def post(self, user_id):
        args = upload_parser.parse_args()
        file = args['file']
        # TODO:目前只支持英文文件名
        # TODO:检查是否有相同的文件名
        # TODO:检查文件是否已存在，若已存在，则禁止上传
        filename = is_allowed_file(file.filename)
        if filename is False:
            return add_response(r_code=RET.FILE_ERROR)

        file.save(os.path.join(UPLOAD_FILE_PATH, filename))
        # TODO:给文件名进行对称加密
        encrypt_filename = filename
        return add_response(r_code=RET.OK, j_dict={"url": url_for('api1.files_download', filename=file.filename)})


# TODO:filename为密文
@ns.route('/download/<string:filename>')
class Download(Resource):
    @ns.doc(parser=base_parse)
    @auth_required
    def get(self, user_id, filename):
        # TODO:对文件名进行解密
        return send_from_directory(UPLOAD_FILE_PATH, filename)


# 根据用户ｉｄ返回所有的文件名
@ns.route('/source/all')
class AllTheFiles(Resource):
    @ns.doc(parser=base_parse)
    @auth_required
    def get(self, user_id):
        # TODO:通过数据库查询用户对应的文件空间

        # TODO:这样同时返回文件夹和文件，暂时不处理
        files_list = os.listdir(UPLOAD_FILE_PATH)
        print(TokenBase('18').token)
        return add_response(r_code=RET.OK, j_dict={"files_list": files_list})
