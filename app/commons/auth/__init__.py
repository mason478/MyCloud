import traceback
from flask import request

from app.commons.change_format import RET, add_response
from app.commons.token_handler import decode_jwt
from app.commons.my_exception import GetTokenError
from app.commons.auth.moudles import TokenBase
from app.commons.my_exception import RedisServiceError
from app.commons.log_handler import logger

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
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return add_response({}, RET.TOKEN_NULL), 401
        auth_token = extra_token(auth_header)
        if auth_token is None:
            return add_response({}, RET.TOKEN_INVALID), 401

        payload_dict = None
        try:
            payload_dict = decode_jwt(auth_token)  # 解码后的token 是 dict
            payload_keys = list(payload_dict.keys())
            print(payload_dict)
            fields = ['user_id', 'account', 'id_hash','exp', 'iat']  # payload 应该含有的字段
            cmp = all(True if k in payload_keys else False for k in fields)  # 字段的对照
            if not cmp:
                return add_response({}, RET.TOKEN_INVALID), 401
            valid = True

        except GetTokenError as e:
            logger.logger.error(msg="Get token error:{},trace back:{}".format(e, traceback.format_exc()))
            valid = False
            ret = add_response({}, e.error_code)
        except Exception as e:
            logger.logger.error("Parser token error:{}".format(e))
            valid = False
            ret = add_response({}, RET.TOKEN_PARSER_ERROR)

        if valid:
            try:
                # 验证token 在redis的储存情况
                user_id = str(payload_dict.get('user_id'))
                id_hash=payload_dict.get('id_hash')
                valid = TokenBase(user_id).validate_token(auth_token)
                if valid:
                    ret = func(*args, user_id, id_hash,**kwargs)
            except RedisServiceError as e:
                logger.logger.error(msg="Get token from redis error:{},trace back:{}".format(e, traceback.format_exc()))
                ret = add_response({}, e.error_code)
            except Exception as e:
                logger.logger.error(msg="Internal error:{},trace back:{}".format(e, traceback.format_exc()))
                ret = add_response({}, RET.UNKNOWN_ERROR)
        return ret

    return wrapper
