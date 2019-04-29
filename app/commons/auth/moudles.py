from app.commons.cache import CacheDict
from app.commons.common_init import connect


class TokenBase(CacheDict):
    def __init__(self, id, token=None, refresh_token=None, expire_time=None):
        """
        token在redis里的格式为{"Token:{id}":{"token":{token}}}
        :param id: str:user id
        :param token:
        :param refresh_token:
        :param expire_time:
        """
        super(TokenBase, self).__init__(connect, "Token:"+id) #所以在这里需要加上"Token"

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

    def validate_token(self,input_token):
        """
        比对token
        :param input_token str: 将要比对的token
        :return:
        """
        if self['token']==input_token:
            return True
        return False


# if __name__=="__main__":
#     t=TokenBase(fields='Token:18')
#     print('hello')