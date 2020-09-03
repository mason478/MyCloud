import traceback

from flask_restplus import Namespace, Resource, reqparse
from flask import send_from_directory, after_this_request
from flask import url_for
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from app.commons.setting import JWT_SECRET, JWT_EXPIRETIME
from app.commons.auth import auth_required
from app.commons.auth.moudles import TokenBase, VerificationCode
from app.commons.files_utils import FileHandler
from app.commons.auth.moudles import VerificationCode
from app.commons.change_format import RET, add_response
from app.commons.log_handler import logger
from app.commons.db_utils.db import DB
from app.commons.my_exception import DBError, DBNotExistError, SendEmailError
from app.commons.token_handler import create_token
from app.core import User
from app.commons.token_handler import create_verification_code
from app.commons.send_email import SendEmail
from app.commons.error_handler.error_register import ErrorRegister

ns = Namespace('users')

base_parser = reqparse.RequestParser()
base_parser.add_argument('Authorization', type=str, location='headers', required=True)

login_parser = ns.parser()
login_parser.add_argument('account', type=str, required=True, location='form')
login_parser.add_argument('password', type=str, required=True, location='form')

ErrorRegister(ns, exceptions=[DBError, DBNotExistError, SendEmailError])


# Login,登录方式：账户名登录
@ns.route('/account-login')
class UserLoginByAccount(Resource):
    @ns.doc(parser=login_parser)
    def post(self, *args):
        args = login_parser.parse_args()
        account = args.get('account')
        password = args['password']

        is_correct, user_id = DB.check_password(account=account, password=password)
        if is_correct:
            user_obj = User(user_id=user_id, account=account)
            token = create_token(user_data=user_obj)
            TokenBase(id=str(user_id), token=token, expire_time=JWT_EXPIRETIME)  # 把token存入redis

            @after_this_request
            def set_cookie(response):
                cookie_token = token
                response.set_cookie('token', cookie_token)
                return response

            logger.logger.info("Login by account successfully!")
            return add_response()
        return add_response(r_code=RET.PASSWORD_ERROR)


login_by_email_parser = ns.parser()
login_by_email_parser.add_argument('email', type=str, required=True, location='form')
login_by_email_parser.add_argument('password', type=str, required=True, location='form')


# 邮箱登录
@ns.route('/email-login')
class LoginByEmail(Resource):
    @ns.doc(parser=login_by_email_parser)
    def post(self, *args):
        args = login_by_email_parser.parse_args()
        email = args['email']
        password = args['password']
        # TODO:检查邮箱格式
        is_correct, user_id = DB.check_password(email=email, password=password)
        account_name = DB.is_exist_user(email=email)[0].get('account')  # TODO:因为改了接口，现在这里有bug

        if is_correct:
            user_obj = User(user_id=user_id, email=email, account=account_name)  # 账户名一定存在
            token = create_token(user_data=user_obj)
            TokenBase(id=str(user_id), token=token, expire_time=JWT_EXPIRETIME)  # 把token存入redis

            @after_this_request
            def set_cookie(response):
                cookie_token = token
                response.set_cookie('token', cookie_token)
                return response

            logger.logger.info("Login by email successfully!")
            return add_response({'token': token}, r_code=RET.OK)
        return add_response(r_code=RET.PASSWORD_ERROR), 401


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
        # TODO:检查account是否有重名
        is_exists = DB.is_exist_user(email=email)
        if is_exists:
            return add_response(r_code=RET.USER_ALEADY_EXISTS)
        account_exists = DB.is_exist_user(account=account)
        if account_exists:
            return add_response(r_code=RET.ACCOUNT_EXISTS)

        # 检查验证码与缓存中的是否一样，然后插入数据库
        is_correct = VerificationCode(email=email).validate_code(v_code)
        if not is_correct:
            return add_response(r_code=RET.VERIFY_CODE_ERROR), 401
        user_id = DB.generate_user_id()
        DB.create_new_user(account=account, password=password, user_id=user_id, email=email)
        u = User(user_id=user_id, account=account, email=email)
        FileHandler.create_directory_by_user(u)  # 注册的时候给用户新建一个文件夹（空间）
        token = create_token(u)  # 注册完之后直接登录，生成token
        TokenBase(id=str(user_id), token=token, expire_time=JWT_EXPIRETIME)  # 把token存入redis

        @after_this_request
        def set_cookie(response):
            cookie_token = u.token
            response.set_cookie('token', cookie_token)
            return response

        return add_response({'token': u.token}, RET.OK)


verification_code_parser = ns.parser()
verification_code_parser.add_argument('email', required=True, type=str)


# 获取验证码
@ns.route('/verification-code')
class GetVerificationCode(Resource):
    @ns.doc(parser=verification_code_parser)
    def get(self):
        args = verification_code_parser.parse_args()
        email = args['email']
        v_code = create_verification_code(email=email)
        SendEmail.send(msg=v_code, subject="验证码", receivers=[email])
        return add_response()
