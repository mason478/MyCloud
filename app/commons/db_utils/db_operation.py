from app.commons.change_format import RET
from app.commons.my_exception import SqlOperationError, SqlConditionError


class DbOperation:
    def __init__(self, connect):
        self.connection = connect.pool.connection()

    def select_all_data(self, table, fields=[]):
        """
        :param table: 待查询的表
        :param fields: 待查询的字段(column name)
        :return:list
        """
        sql = "select {field} from {tab}".format(field=",".join(fields), tab=table)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                if not result:
                    return []
                return result
        except Exception:
            raise SqlOperationError(RET.SQL_OPERATION_ERROR)

    def select_data_by_condition(self, table, fields=[], condition=dict):
        """
        根据条件查询数据
        :param table:str:
        :param fields: list
        :param condition: dict:{key:value},查询条件为key==value
        :return: dict
        """
        where = []
        for k, v in condition.items():
            where.append("{}={}".format(k, v))
        sql = "select {} from {} where {}".format(','.join(fields), table, ' AND '.join(where))
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                if not result:
                    return None
                return result
        except Exception:
            raise SqlOperationError(RET.SQL_OPERATION_ERROR)

    def update_data(self, table, fields=dict, condition=dict):
        """

        :param table:
        :param fields:{}
        :param condition:{}
        :return:
        """
        data = ','.join(["{}={}".format(k, v) for k, v in fields.items()])
        where = " AND ".join(["{}={}".format(k, v) for k, v in condition.items()])
        sql = 'update {} set {} where {}'.format(table, data, where)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise SqlOperationError(RET.SQL_OPERATION_ERROR)
        finally:
            self.connection.close()

    # TODO:有问题
    def insert_data(self, table, data=dict):
        fields, values = [], []
        for k, v in data.items():
            fields.append(k)
            values.append(v)
        sql = "INSERT INTO `{}` (`{}`) VALUES ({})".format(table, ','.join(fields), ",".join(values))
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise SqlOperationError(RET.SQL_OPERATION_ERROR)
        finally:
            self.connection.close()

    def delete_data(self, table, condition=dict):
        if not isinstance(condition, dict) or not condition:
            raise SqlConditionError(error_code=RET.SQL_CONDITION_ERROR,
                                    error_msg="delete condition is required,or it will delete all the data")
        where = ["{}={}".format(k, v) for k, v in condition.items()]
        sql = "DELETE FROM {} WHERE {}".format(table, ','.join(where))
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise SqlOperationError(RET.SQL_OPERATION_ERROR)
        finally:
            self.connection.close()


if __name__ == "__main__":
    import pymysql
    from DBUtils.PooledDB import PooledDB

    from app.commons.common_init import logger


    class SqlConnect:
        def __init__(self, app=None):
            self.pool = None
            if app:
                self.init_app(app)
            else:
                self.pool = PooledDB(pymysql, maxconnections=10,
                                     maxcached=5,
                                     mincached=5,
                                     blocking=True,
                                     db='user', user='mason',
                                     password='1111',
                                     host='localhost', port=3306,
                                     cursorclass=pymysql.cursors.DictCursor)


    c = SqlConnect()
    dbop = DbOperation(c)
    try:
        # r = dbop.select_all_data(table='sequence', fields=['name'])
        # r2=dbop.update_data(table='sequence',fields={'sequence':2},condition={'id':2})
        # r2 = dbop.insert_data(table='sequence', data={'name': 'wangjiefewfe','sequence':'2'})
        r2 = dbop.delete_data(table='sequence', condition={'id': 7})
        print(r2)
    except SqlOperationError as e:
        import traceback

        print(traceback.format_exc())
        print(e.error_code)
