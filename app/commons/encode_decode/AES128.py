import base64
from urllib import parse

from Crypto.Cipher import AES

from app.commons.setting import ENCRYPT_KEY, ENCRYPT_KEY_IV


def base64_encrypt(data):
    return base64.b64encode(data)


# 对明文进行aes128加密或者对密文解密
class AES_Encrypt:
    def __init__(self):
        self.key = ENCRYPT_KEY
        self.iv = ENCRYPT_KEY_IV

    def __pad(self, text):
        '''填充方式,如缺少n位，则填充n个chr(n)'''
        n = 16 - ((len(text)) % 16)
        text += chr(n) * n
        return str.encode(text)

    def __unpad(self, text):
        n = ord(text[-1])
        return text[:-n]

    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        """解密"""
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(enc.encode(encoding='utf-8'))
        # 执行解密密并转码返回str
        decrypted_text = str(cipher.decrypt(base64_decrypted), encoding='utf-8')
        decrypted_text = self.__unpad(decrypted_text)
        return decrypted_text


class EncryptUrlSafe(AES_Encrypt):

    @classmethod
    def encrypt_url_safe(cls, raw):
        """
        由于AES128加密后会有斜杠等url不安全的字符，故进行url-safe转换
        :param raw:
        :return: url safe code
        """
        secret_text = (cls().encrypt(raw)).decode()  # 先加密
        url_safe_code = parse.quote(secret_text, safe='')
        return url_safe_code

    @classmethod
    def decrypt_url_safe(cls, secret_text):
        secret_text = parse.unquote(secret_text)  # 先进行url转码
        plain = cls().decrypt(secret_text)  # 再解密
        return plain


if __name__ == "__main__":
    plaint = '123ggewg5dwdicwsfww6i.gif'
    a = AES_Encrypt()
    secret = str(a.encrypt(plaint).decode())
    safe = EncryptUrlSafe.encrypt_url_safe(plaint)
    print(secret)
    print(safe)
    print(EncryptUrlSafe.decrypt_url_safe('XaaF7TVTmVMa2irQsKNtDr59JbYiPj8Ot%2F3wTjvKbBM%3D'))
