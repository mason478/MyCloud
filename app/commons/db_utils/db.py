from werkzeug.security import check_password_hash, generate_password_hash

from app.commons.db_utils.db_operation import DbOperation
from app.commons.common_init import sql_connect
from app.commons.my_exception import SqlOperationError


# 对DbOperation的继承，最顶层调用就用这个类
class DB(DbOperation):
    def __init__(self, connect=sql_connect):
        super(DB, self).__init__(connect)

    @classmethod
    def check_password(cls,account, password):
        """
        比对密码在数据库中的哈希值
        :param account:
        :param password: 密码明文
        :return: bool
        """
        try:
            password_hash=cls.select_data_by_condition(table='user',fields=['password'],condition={'account':account})
            is_correct=check_password_hash(pwhash=password_hash,password=password)
            return is_correct
        except SqlOperationError as e:
            raise SqlOperationError
