import os
import unittest

from werkzeug.security import check_password_hash, generate_password_hash

from app.commons.db_utils.connect import SqlConnect
from app.commons.db_utils.db_operation import DbOperation
from app.commons.my_exception import SqlOperationError, DBError, DBNotExistError, FileHandlerError
from app.commons.db_utils.db import DB
from app.commons.cache.base import CacheObject, CacheDict
from app.commons.cache.connect import RedisConnect
from app.commons.auth.moudles import VerificationCode, TokenBase
from app.commons.files_utils import FileHandler
from app.commons.token_handler import create_token, decode_jwt


class App(object):
    def __init__(self):
        self.config = {
            "DEBUG": True,
            "HOST": 'localhost',
            "PORT": 8081,

            "REDIS_HOST": 'localhost',
            "REDIS_PORT": 6379,
            "REDIS_PASSWORD": os.getenv('REDIS_PASSWORD', "62f4ada291da"),
            "REDIS_DB": 0,

            # log 配置
            "LOG_LEVEL": 'debug',  # 日志等级，大于这个等级的日志才会被记录,有:info,debug,error等
            "LOG_TYPE": 'steam',  # 是否是轮回日志,rotate:轮回，stream:日志流
            "LOG_PATH": os.getcwd(),
            "LOG_NAME": 'mycloud.log',  # 轮回日志记录的名称
            "LOG_MAX_BYTES": 1024 * 1024 * 10,
            "LOG_BACK_UP_COUNT": 7,
            # mysql及连接池的配置,
            "POOL_MAX_CONNECTION": 10,
            "POOL_MAX_CACHE": 5,
            "POOL_MIN_CACHE": 5,
            "POOL_BLOCKING": True,
            "DB": 'mycloud',
            "DB_USER": 'mason',
            "DB_PASSWORD": '1111',
            "DB_HOST": 'localhost',
            "DB_PORT": 3306,

        }


apps = App()
# init connect
sql_connect = SqlConnect(apps)


class TestDbOperation(unittest.TestCase):

    def setUp(self):
        self.db = DbOperation(connect=sql_connect)

    def tearDown(self):
        self.db.connection.close()

    def test_db_insert(self):
        password = generate_password_hash(password='1111')
        assert self.db.insert_data(table='user',
                                   data={'name': 'wangjie', 'account': 'wangjie1234653', 'password': password,
                                         'user_id': 1002}) is None

    def test_db_select(self):
        r = self.db.select_data_by_condition(table='user', fields=['name', 'account', 'password'],
                                             condition={"name": 'wangjie'})
        print(r)
        assert isinstance(r, list)

    def test_db_update(self):
        self.db.update_data(table='user', fields={'email': 'wangjie@qq.com'}, condition={'id': 6})

    def test_db_delete_data(self):
        r = self.db.delete_data(table='user', condition={"id": 14})
        assert r is None


test_user_id = 1010


# 测试DB模块，这是最顶层调用模块
class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = DB(connect=sql_connect)

    def tearDown(self):
        self.db.delete_data(table='user', condition={'user_id': test_user_id})
        self.db.connection.close()

    def test_check_password(self):
        trueodfalse, userid = self.db.check_password(password='1111', account='wangjie1234653')
        assert trueodfalse is True
        assert userid == 1002

    def test_is_exist_user(self):
        r1 = self.db.is_exist_user(account='wangjie1234653')
        r2 = self.db.is_exist_user(account='wangjie123465fwg3')

        r3 = self.db.is_exist_user(email='wangjie@qq.com')
        r4 = self.db.is_exist_user(email='wangjie@qqfewf.com')

        assert r1, r3 is True
        assert r2 is False and r4 is False

    def test_create_new_user(self):
        r = self.db.create_new_user(account='for_the_test', password='1234', user_id=test_user_id, is_admin=1)
        t, user_id = self.db.check_password(password='1234', account='for_the_test')
        assert r is None
        assert t is True
        assert user_id == test_user_id

    def test_is_admin(self):
        assert self.db.is_admin(user_id=1004) is True
        assert self.db.is_admin(user_id=1002) is False


# 测试redis连接的中间件
redis_connect = RedisConnect(app=apps)


class TestRedisMiddleWear(unittest.TestCase):
    def setUp(self):
        self.cache = CacheDict(connect=redis_connect, key='Test')

    def test_set_and_get_item(self):
        self.cache['name'] = 'wangjie'
        assert self.cache['name'] == 'wangjie'

    def test_expire(self):
        self.cache.expire(time=60)

    def test_delete(self):
        self.cache.delete()


# 测试token的存取类
class TestTokenBase(unittest.TestCase):
    def test_set_token(self):
        TokenBase(id='233', token='this is a token', connects=redis_connect)

    def test_get_token(self):
        assert TokenBase(id='233', connects=redis_connect).token == 'this is a token'

    def test_token_validate_token(self):
        assert TokenBase(id='233', connects=redis_connect).validate_token(input_token='this is a token') is True
        assert TokenBase(id='233', connects=redis_connect).validate_token(input_token='this is a token2') is False


# 测试验证码的存取
class TestVCode(unittest.TestCase):
    def test_set_vcode(self):
        VerificationCode(email='123@qq.com', v_code='12354', expire_time=60 * 5, connects=redis_connect)

    def test_get_vcode(self):
        r = VerificationCode(email='123@qq.com', connects=redis_connect).v_code
        assert r == '12354'

    def test_validate_vcode(self):
        assert VerificationCode(email='123@qq.com', connects=redis_connect).validate_code(input_code='12354') is True
        assert VerificationCode(email='123@qq.com', connects=redis_connect).v_code is None


# 测试跟文件处理相关的类
directory = 'test_directory'


class TestFileHandler(unittest.TestCase):

    def test_is_exist_directory(self):
        FileHandler.is_exist_directory(directory=directory, path=os.getcwd())

    def test_is_exist_file(self):
        assert FileHandler.is_exist_files(path=os.getcwd(), filename='test_middleware.py') is True
        assert FileHandler.is_exist_files(path=os.getcwd(), filename='test_middleware_not_exists.py') is False

    def test_delte_directory(self):
        try:
            FileHandler.delete_directory(path=os.getcwd(), directory_name=directory)
        except FileHandlerError as e:
            assert e.error_code == 1003

    def test_listsall(self):
        l = FileHandler.list_files(path=os.getcwd(), directory_name='')
        print(l)

    def test_delete(self):
        FileHandler.delete_directory(path=os.getcwd(), directory_name='test')


class UserData:
    user_id = '123'
    account = 'wangjie'
    id_hash = 'fa4243ce'


u = UserData()


class TestTokenHanlder(unittest.TestCase):

    def test_create_token(self):
        token = create_token(user_data=u)
        return token

    def test_decode_token(self):
        token = self.test_create_token()
        payload = decode_jwt(
            token=token)
        fiels = ['user_id', 'account', 'id_hash', 'exp', 'iat']
        cmp = all(True if f in payload.keys() else False for f in fiels)
        assert cmp is True


