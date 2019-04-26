import traceback
from flask import request, abort, Response

from app.commons.change_format import RET, add_response
from app.commons.token_handler import decode_jwt


def extra_token(headers):
    """
    auth_header 包含两部分，一个是“bearer”前缀,另外就是jwt实体,以空格分割;从header 提取token
    :return:auth token
    """
    header_list = headers.split()
    if len(header_list) == 2:
        auth_type, auth_token = header_list[0], header_list[1]
        if auth_type.upper() == "BEARER":
            return auth_token
        return None
    return None


# 装饰器，用来验证token
def auth_required(func):
    def wrapper(*args):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return add_response({}, RET.TOKEN_NULL), 401
        auth_token = extra_token(auth_header)
        if auth_token is None:
            return add_response({}, RET.TOKEN_INVALID), 401
        try:
            payload_list = decode_jwt(auth_token)  # 解码后的token 是 dict
            payload_keys = list(payload_list.keys())
            fields = ['user_id', 'user_name', 'exp', 'iat']  # payload 应该含有的字段
            cmp = all(True if k in payload_keys else False for k in fields)  # 字段的对照
            if not cmp:
                return add_response({}, RET.TOKEN_INVALID), 401
            valid = True

        except Exception as e:
            # TODO:打log
            valid=False
            return add_response({}, RET.TOKEN_PARSER_ERROR)
        if valid:
            #验证token 在redis的储存情况
            pass

    return wrapper
