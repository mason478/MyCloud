from Crypto.Cipher import AES
import base64

data_secret = "972e0a2ef7354918"
data_secret_iv = "7ce27787c7b24425"

def base64_encrypt(data):
    return base64.b64encode(data)

# 对明文进行aes128加密或者对密文解密
class AES_Encrypt:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

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

if __name__=="__main__":
    plaint='123ggewg5dwdw6'
    a=AES_Encrypt(key=data_secret,iv=data_secret_iv)
    secret=a.encrypt(plaint)
    print(secret)