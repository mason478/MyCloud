class RET:
    OK = 0

    #系统级错误
    UNKNOWN_ERROR=1001

    # 应用级错误
    FILE_ERROR = 2001
    FILE_NOT_FOUND=2002

    #验证错误
    TOKEN_NULL=3001
    TOKEN_INVALID=3002
    TOKEN_PARSER_ERROR=3003
    TOKEN_EXPIRED=3004

    #数据库链接错误
    REDIS_CONNECT_ERROR=5001

    SQL_OPERATION_ERROR = 5010
    SQL_CONDITION_ERROR=5011


error_dict = {
    RET.FILE_ERROR: '非法的文件名或扩展名',
    RET.TOKEN_NULL:"token为空",
    RET.TOKEN_INVALID:"非法的token",
    RET.TOKEN_PARSER_ERROR:"token解析错误",
    RET.REDIS_CONNECT_ERROR:"redis连接错误",
    RET.TOKEN_EXPIRED:"Token过期",
    RET.UNKNOWN_ERROR:"内部未知错误",
    RET.SQL_OPERATION_ERROR:"数据库操作错误",
    RET.SQL_CONDITION_ERROR:"数据库输入条件错误"
}


def add_response(j_dict={}, r_code=RET.OK):
    r_dict = {}
    if r_code == RET.OK:
        r_dict['result'] = j_dict
        r_dict.update({"error_code": 0, 'reason': '成功'})
        return r_dict
    r_dict.update({'result': {}, 'error_code': r_code, 'reason': error_dict.get(r_code)})
    return r_dict
