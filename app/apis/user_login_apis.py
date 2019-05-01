import traceback

from flask_restplus import Namespace, Resource, reqparse
from flask import send_from_directory, after_this_request
from flask import url_for
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from app.commons.auth import auth_required
from app.commons.auth.moudles import VerificationCode
from app.commons.change_format import RET, add_response
from app.commons.log_handler import logger
from app.commons.db_utils.db import DB
from app.commons.my_exception import DBError, DB_Not_Exist_Error
from app.commons.token_handler import create_token
from app.core import User
from app.commons.token_handler import create_verification_code

ns = Namespace('users')

base_parser = reqparse.RequestParser()
base_parser.add_argument('Authorization', type=str, location='headers', required=True)

login_parser = ns.parser()
login_parser.add_argument('account', type=str, required=True, location='form')
login_parser.add_argument('password', type=str, required=True, location='form')


# Login,登录方式：账户名登录
@ns.route('/account')
class UserLoginByAccount(Resource):
    @ns.doc(parser=login_parser)
    def post(self, *args):
        args = login_parser.parse_args()
        account = args.get('account')
        password = args['password']

        try:
            is_correct, user_id = DB.check_password(account=account, password=password)
            if is_correct:
                user_obj = User(user_id=user_id, account=account)
                token = create_token(user_data=user_obj)

                @after_this_request
                def set_cookie(response):
                    cookie_token = token
                    response.set_cookie('token', cookie_token)
                    return response

                logger.logger.info("Login successfully!")
                return add_response()
            return add_response(r_code=RET.PASSWORD_ERROR)
        except DB_Not_Exist_Error as e:
            return add_response(r_code=e.error_code)
        except DBError as e:
            logger.logger.error("DB error:{},traceback:{}".format(e, traceback.format_exc()))
            return add_response(r_code=e.error_code)


login_by_email_parser = ns.parser()
login_by_email_parser.add_argument('email', type=str, required=True, location='form')
login_by_email_parser.add_argument('password', type=str, required=True, location='form')


# 邮箱登录
@ns.route('/email')
class LoginByEmail(Resource):
    @ns.doc(parser=login_by_email_parser)
    def post(self, *args):
        args = login_by_email_parser.parse_args()
        email = args['email']
        password = args['password']

        try:
            is_correct, user_id = DB.check_password(email=email, password=password)
            account_name = DB.is_exist_user(email=email)[0].get('account')
            if is_correct:
                user_obj = User(user_id=user_id, email=email, account=account_name)  # 账户名一定存在
                token = create_token(user_data=user_obj)

                @after_this_request
                def set_cookie(response):
                    cookie_token = token
                    response.set_cookie('token', cookie_token)
                    return response

                logger.logger.info("Login successfully!")
                return add_response()
            return add_response(r_code=RET.PASSWORD_ERROR)
        except DB_Not_Exist_Error as e:
            return add_response(r_code=e.error_code)
        except DBError as e:
            logger.logger.error("DB error:{},traceback:{}".format(e, traceback.format_exc()))
            return add_response(r_code=e.error_code)


# 通过邮箱注册
register_parser = ns.parser()
register_parser.add_argument('email', required=True, location='form', type=str)
register_parser.add_argument('password', required=True, location='form', type=str)
register_parser.add_argument('verification_code', required=True, location='form', type=str)
register_parser.add_argument('nickname', type=str, required=True, location='form', help='账户昵称，可以用来登录')


@ns.route('/register')
class Register(Resource):
    @ns.doc(parser=register_parser)
    def post(self, *args):
        args = register_parser.parse_args()
        email = args['email']
        password = args['password']
        v_code = args['verification_code']
        account = args['nickname']  # nickname 就是account（别名）
        # TODO:检查验证码与缓存中的是否一样，然后插入数据库
        is_correct = VerificationCode(email=email).validate_code(v_code)
        if not is_correct:
            return add_response(r_code=RET.VERIFY_CODE_ERROR)
        user_id = DB.generate_user_id()
        try:
            DB.create_new_user(account=account, password=password, user_id=user_id, email=email)
        except DBError as e:
            logger.logger.error("DB error:{},traceback:{}".format(e.error_code, traceback.format_exc()))
            return add_response(r_code=e.error_code)


verification_code_parser = ns.parser()
verification_code_parser.add_argument('email', required=True, type=str)


# 获取验证码
@ns.route('/verification-code')
class GetVerificationCode(Resource):
    @ns.doc(parser=verification_code_parser)
    def get(self):
        args = verification_code_parser.parse_args()
        email = args['email']
        # TODO：发送邮件
        v_code = create_verification_code(email=email)
        return add_response()


admin_parser = base_parser.copy()
admin_parser.add_argument('account', type=str, required=True, location='form', help='管理员新增用户的账号')
admin_parser.add_argument('password', type=str, required=True, default='1111', location='form')
admin_parser.add_argument('email', type=str, location='form')
admin_parser.add_argument('is_admin', type=int, default=0, help="新增的账户是否有管理员权限", location='form')


# admin can add formal users
@ns.route('/admin')
class AdminAddUser(Resource):
    @ns.doc(parser=admin_parser)
    @auth_required
    def post(self, user_id):
        args = admin_parser.parse_args()
        account = args['account']
        password = args['password']
        is_admin = args['is_admin']

        if is_admin != 0:
            is_admin = 1
        # TODO:查询数据库进行比对,是否已经存在
        # TODO:向数据库插入新的用户
        try:
            login_user_is_admin = DB.is_admin(user_id)  # 判断登录的用户是否是管理员
        except DBError as e:
            logger.logger.error("SQL error:{}.traceback:{}".format(e.error_code, traceback.format_exc()))
            return add_response(r_code=e.error_code)
        if not login_user_is_admin:
            return add_response(r_code=RET.PERMISSION_NOT_ADMIN)

        try:
            new_user_id = DB.generate_user_id()  # 这里是新增用户的user_id
            DB.create_new_user(account=account, password=password, is_admin=is_admin, user_id=new_user_id)
            return add_response(RET.OK)
        except DBError as e:
            logger.logger.error("SQL error:{}.traceback:{}".format(e.error_code, traceback.format_exc()))
            return add_response(r_code=e.error_code)
