# 生成jwt token,解码token等
import time
import base64

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError, JWSSignatureError

from app.commons.setting import JWT_SECRET, JWT_EXPIRETIME


def create_token(user_data, expire_time=JWT_EXPIRETIME):
    """
    通过user_data类的实例生成jwt
    :param user_data:an object
    :param expire_time:
    :return:
    """
    start_time = int(time.time())
    expire_time = start_time + expire_time

    base_msg = {
        'user_id': user_data.user_id,
        "user_name": user_data.user_name,
        'exp': expire_time,
        'iat': start_time
    }
    token_jwt = encode_jwt(base_msg)
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
        raise e
    except ExpiredSignatureError as e:
        raise e
    except JWTError as e:
        raise e


def encode_jwt(data):
    """
    生成jwt
    :param data:dict
    :return:
    """
    secret = base64.b64encode(JWT_SECRET.encode())
    r = jwt.encode(data, secret.decode())
    return r


if __name__ == "__main__":
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJ3YW5namllIiwiaWF0IjoxNTU1OTg3OTM5LjQ4NTQ2Niw' \
            'ibm9kZV9pZCI6IjEyMzQifQ.f2yPUXPT1dR2RNRGe8RVek7tk6IHiKH6BnnlWreuPTk'
    # e=encode_jwt({'user_name':'wangjie','iat':time.time(),'node_id':'1234'})
    try:
        r = decode_jwt(token)
    except Exception as e:
        print(e)
