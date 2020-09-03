from app.commons.cache import CacheDict
from app.commons.common_init import connect


class TokenBase(CacheDict):
    def __init__(self, id, token=None, refresh_token=None, expire_time=None,connects=None):
        """
        token在redis里的格式为{"Token:{id}":{"token":{token}}}
        :param id: str:user id
        :param token:
        :param refresh_token:
        :param expire_time:
        :param connect:RedisConnect obj
        """
        if connects is not None:
            super(TokenBase, self).__init__(connects, "Token:" + id)  # 所以在这里需要加上"Token" string
        else:
            super(TokenBase, self).__init__(connect, "Token:" + id)  # 所以在这里需要加上"Token" string

        # 设置token
        if token:
            self['token'] = token
        if refresh_token:
            self['refresh_token'] = refresh_token
        if expire_time:
            self.expire(time=expire_time)

    @property
    def token(self):
        return self['token']

    @property
    def refresh_token(self):
        return self['refresh_token']

    def validate_token(self, input_token):
        """
        比对token
        :param input_token :str: 将要比对的token
        :return:
        """
        if self['token'] == input_token:
            return True
        return False


# 用于验证码的存取
class VerificationCode(CacheDict):
    def __init__(self, email, v_code=None, expire_time=None,connects=None):
        """
        验证码在redis的存储格式为：{"VerificationCode:{email}":{"v_code":v_code}}
        :param email:
        :param v_code:
        :param expire_time: 过期时间，单位秒
        """
        if connects is not None:
            super().__init__(connect=connects, key="VerificationCode:" + email)
        else:
            super().__init__(connect=connect, key="VerificationCode:" + email)

        if v_code:
            self['v_code'] = v_code
        if expire_time:
            self.expire(time=expire_time)

    @property
    def v_code(self):
        return self['v_code']

    def validate_code(self, input_code):
        if self['v_code'] == input_code:
            self.delete()  # 验证正确后就删除验证码
            return True
        return False

# if __name__=="__main__":
#     t=TokenBase(fields='Token:18')
#     print('hello')
