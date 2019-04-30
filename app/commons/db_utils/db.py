from app.commons.db_utils.db_operation import DbOperation
from app.commons.common_init import sql_connect


# 对DbOperation的继承，最顶层调用就用这个类
class DB(DbOperation):
    def __init__(self, connect=sql_connect):
        super(DB, self).__init__(connect)

