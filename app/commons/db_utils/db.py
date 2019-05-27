from werkzeug.security import check_password_hash, generate_password_hash

from app.commons.db_utils.db_operation import DbOperation
from app.commons.common_init import sql_connect
from app.commons.my_exception import SqlOperationError, DBError,DBNotExistError
from app.commons.change_format import RET


# 对DbOperation的继承，最顶层调用就用这个类
class DB(DbOperation):
    def __init__(self,connect=None):
        if connect is None:
            super(DB, self).__init__(connect=sql_connect)
        else:
            super(DB, self).__init__(connect=connect)


    @classmethod
    def check_password(cls, password, email=None, account=None):
        """
        比对密码在数据库中的哈希值;
        :param account:
        :param email:
        :param password: 密码明文
        :return: bool,user_id
        """
        try:
            password_hash = None
            if email:
                password_hash = cls().select_data_by_condition(table='user', fields=['password','user_id'],
                                                               condition={'email': email})
            if account:
                password_hash = cls().select_data_by_condition(table='user', fields=['password','user_id'],
                                                               condition={'account': account})
            if not password_hash:
                raise DBNotExistError(error_code=RET.USER_NOT_EXIST)
            user_id=password_hash[0].get('user_id')
            is_correct = check_password_hash(pwhash=password_hash[0].get('password'), password=password)
            return is_correct,user_id
        except SqlOperationError as e:
            raise DBError(error_code=e.error_code)

    @classmethod
    def is_exist_user(cls, account=None, email=None):
        """
        判断给定的账号名或者邮箱是否存在相应的用户
        :param account:
        :param email:
        :return: list
        """
        try:
            condition = None
            if account:
                condition = {'account': account}
            if email:
                condition = {'email': email}
            rt = cls().select_data_by_condition(table='user', fields=['user_id', 'account'], condition=condition)
            if rt:
                return True
            return False

        except SqlOperationError as e:
            raise DBError(error_code=e.error_code)

    @classmethod
    def create_new_user(cls, account, password, user_id, email=None, is_admin=0):
        """
        用户的必须有账户名
        :param account:
        :param password:
        :param email:
        :param is_admin:添加的账户是否有管理员权限
        :return: None
        """
        # TODO:user_id
        try:
            password_hash = generate_password_hash(password)
            if email:
                data = {"account": account, "password": password_hash, "email": email, 'is_admin': str(is_admin),
                        "user_id": user_id}
            else:
                data = {"account": account, "password": password_hash, 'is_admin': str(is_admin), "user_id": user_id}
            cls().insert_data(table='user', data=data)
        except SqlOperationError as e:
            raise DBError(error_code=e.error_code)

    @classmethod
    def generate_user_id(cls):
        try:
            user_id_dict = cls().select_data_by_condition(table='user_id_sequence', fields=['number'],
                                                          condition={'name': 'user_id'})
            user_id = user_id_dict[0]['number']
            cls().update_data(table='user_id_sequence', fields={'number': user_id + 1}, condition={'name': 'user_id'})
            return user_id
        except SqlOperationError as e:
            raise DBError(error_code=e.error_code)

    @classmethod
    def is_admin(cls, user_id):
        """
        判断给定的user_id是否有管理员权限
        :param user_id:
        :return: bool
        """
        try:
            ret = cls().select_data_by_condition(table='user', fields=['is_admin'], condition={'user_id': user_id})
            is_admin = ret[0]['is_admin']
            if is_admin == 1:
                return True
            return False
        except SqlOperationError as e:
            raise DBError(error_code=e.error_code)
