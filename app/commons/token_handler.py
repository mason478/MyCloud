# 生成jwt token,解码token等
import time
import base64

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError, JWSSignatureError

from app.commons.setting import JWT_SECRET, JWT_EXPIRETIME
from app.commons.my_exception import GetTokenError
from app.commons.change_format import RET
from app.commons.auth.moudles import TokenBase, VerificationCode
from app.commons.setting import CODE_LENGTH, EXPIRE_TIME


def create_token(user_data, expire_time=JWT_EXPIRETIME):
    """
    通过user_data类的实例生成jwt
    :param user_data:an user object
    :param expire_time:
    :return:
    """
    start_time = int(time.time())
    expire_time = start_time + expire_time

    base_msg = {
        'user_id': user_data.user_id,
        "account": user_data.account,
        'exp': expire_time,
        'iat': start_time
    }
    token_jwt = encode_jwt(base_msg)
    user_data.token = token_jwt

    TokenBase(id=str(user_data.user_id), token=token_jwt, expire_time=JWT_EXPIRETIME)  # 把token存入redis
    return token_jwt


def decode_jwt(token):
    '''
    解码token
    :param token:
    :return:
    '''
    # jwt有三段，第一部分我们称它为头部（header),第二部分我们称其为载荷（payload)，第三部分是签证（signature).
    try:
        s = JWT_SECRET.encode()
        secret = base64.b64encode(s)
        payload = jwt.decode(token, secret.decode(), algorithms='HS256')
        return payload
    except JWSSignatureError as e:
        raise GetTokenError(RET.TOKEN_INVALID)
    except ExpiredSignatureError as e:
        raise GetTokenError(RET.TOKEN_EXPIRED)
    except JWTError as e:
        raise GetTokenError(RET.TOKEN_INVALID)


def encode_jwt(data):
    """
    生成jwt
    :param data:dict
    :return:
    """
    secret = base64.b64encode(JWT_SECRET.encode())
    r = jwt.encode(data, secret.decode())
    return r


def create_verification_code(email, long=CODE_LENGTH):
    # TODO:生成验证码，&refresh_token
    v_code = '1234'
    VerificationCode(email=email, v_code=v_code, expire_time=EXPIRE_TIME)  # 把验证码存入redis
    return v_code


if __name__ == "__main__":
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDAwLCJhY2NvdW50Ijoid2FuZ2ppZSIsImV4cCI6MTU1Nj' \
            'Y5OTExNywiaWF0IjoxNTU2NjkxOTE3fQ.tjTiIWiW9awrV7NJOFgL6QhFoKW9oZI4Hgs9yMGeLBk'
    # e=encode_jwt({'user_name':'wangjie','iat':time.time(),'node_id':'1234'})
    try:
        r = decode_jwt(token)
        print(r)
    except Exception as e:
        print(e)
