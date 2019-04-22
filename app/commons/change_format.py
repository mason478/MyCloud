class RET:
    OK = 0

    # 应用级错误
    FILE_ERROR = 2001


error_dict = {
    RET.FILE_ERROR: '非法的文件名或扩展名',
}


def add_response(j_dict={}, r_code=RET.OK):
    r_dict = {}
    if r_code == RET.OK:
        r_dict['result'] = j_dict
        r_dict.update({"error_code": 0, 'reason': '成功'})
        return r_dict
    r_dict.update({'result': {}, 'error_code': r_code, 'reason': error_dict.get(r_code)})
    return r_dict
