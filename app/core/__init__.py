from app.commons.encode_decode.MD5 import hash_value
from app.commons.setting import UPLOAD_FILE_PATH


class User:
    def __init__(self, user_id, account, email=None):
        self.user_id = str(user_id)
        self.account = account
        self.email = email
        self.token = None
        self.id_hash = hash_value(self.user_id)
        self.file_root = UPLOAD_FILE_PATH + '/' + self.id_hash  # 用户的根目录
