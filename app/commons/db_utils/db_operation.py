from app.commons.change_format import RET
from app.commons.my_exception import SqlOperationError, SqlConditionError


class DbOperation:
    def __init__(self, connect):
        self.connection = connect.pool.connection() # 与连接池建立连接

    def select_all_data(self, table, fields=[]):
        """
        :param table: 待查询的表
        :param fields: 待查询的字段(column name)
        :return:lit
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
        :return: []
        """
        where = []
        for k, v in condition.items():
            where.append("{}='{}'".format(k, v))
        sql = "select {} from {} where {}".format(','.join(fields), table, ' AND '.join(where))
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                if not result:
                    return []
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
        data = ','.join(["{}='{}'".format(k, v) for k, v in fields.items()])
        where = " AND ".join(["{}='{}'".format(k, v) for k, v in condition.items()])
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

    def insert_data(self, table, data=dict):
        fields, values = [], []
        for k, v in data.items():
            fields.append(k)
            values.append("'%s'"%v)
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table, ','.join(fields), ",".join(values))
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
        """
        delete data from table,and condition must be dict and not an empty dict,else all data will be deleted.
        :param table:
        :param condition: {key,value},in sql:where key=value
        :return: None
        """
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



    class SqlConnect:
        def __init__(self, app=None):
            self.pool = None
            if app:
                # self.init_app(app)
                pass
            else:
                self.pool = PooledDB(pymysql, maxconnections=10,
                                     maxcached=5,
                                     mincached=5,
                                     blocking=True,
                                     db='mycloud', user='mason',
                                     password='1111',
                                     host='localhost', port=3306,
                                     cursorclass=pymysql.cursors.DictCursor)


    c = SqlConnect()
    dbop = DbOperation(c)
    try:
        # r = dbop.select_all_data(table='user', fields=['name'])
        # r2=dbop.update_data(table='user',fields={'':2},condition={'id':2})
        # r2 = dbop.insert_data(table='user', data={'account': 'wangjie2','user_id':1001,})
        # r2 = doop.delete_data(table='sequence', condition={'id': 7})
        r2=dbop.select_data_by_condition(table='user',fields=['password','user_id'],condition={'account':'wangjie'})
        print(r2)
    except SqlOperationError as e:
        import traceback

        print(traceback.format_exc())
        print(e.error_code)
