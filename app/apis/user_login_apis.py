import traceback

from flask_restplus import Namespace, Resource, reqparse
from flask import send_from_directory
from flask import url_for
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from app.commons.auth import auth_required
from app.commons.change_format import RET, add_response
from app.commons.log_handler import logger
from app.commons.db_utils.db import DB
from app.commons.my_exception import SqlOperationError

ns = Namespace('users')

base_parser = reqparse.RequestParser()
base_parser.add_argument('Authorization', type=str, location='headers', required=True)

login_parser = ns.parser()
login_parser.add_argument('account', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)


@ns.route('/accounts')
class UserLogin(Resource):
    @ns.doc(parser=login_parser)
    def post(self, *args):
        args = login_parser.parse_args()
        account = args['account']
        password = args['password']
        # try:
        #     DB.

        try:
            is_correct = DB.check_password(account=account, password=password)
            if is_correct:
                # TODO:生成token,存入:1.redis;2.cookie
                logger.logger.info("Login successfully")
                return add_response()
            return add_response(r_code=RET.PASSWORD_ERROR)
        except SqlOperationError as e:
            logger.logger.error("Mysql error:{},trackback:{}".format(e, traceback.format_exc()))
            return add_response(r_code=e.error_code)


admin_parser = base_parser.copy()
admin_parser.add_argument('account', type=str, required=True, location='form',help='管理员新增用户的账号')
admin_parser.add_argument('password',type=str,required=True,default='1111', location='form')


# admin can add formal users
@ns.route('/admin')
class AdminAddUser(Resource):
    @ns.doc(parser=admin_parser)
    @auth_required
    def post(self,user_id):
        #TODO:查询数据库进行比对
        #TODO:向数据库插入新的用户
        pass