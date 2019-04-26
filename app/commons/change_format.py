class RET:
    OK = 0

    # 应用级错误
    FILE_ERROR = 2001

    #验证错误
    TOKEN_NULL=3001
    TOKEN_INVALID=3002
    TOKEN_PARSER_ERROR=3003



error_dict = {
    RET.FILE_ERROR: '非法的文件名或扩展名',
    RET.TOKEN_NULL:"token为空",
    RET.TOKEN_INVALID:"非法的token",
    RET.TOKEN_PARSER_ERROR:"token解析错误"
}


def add_response(j_dict={}, r_code=RET.OK):
    r_dict = {}
    if r_code == RET.OK:
        r_dict['result'] = j_dict
        r_dict.update({"error_code": 0, 'reason': '成功'})
        return r_dict
    r_dict.update({'result': {}, 'error_code': r_code, 'reason': error_dict.get(r_code)})
    return r_dict
