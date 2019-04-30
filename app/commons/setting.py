#这里的配置和config.py配置的含义不同：config.py 是对需要初始化的模块进行配置
import os

UPLOAD_FILE_PATH = os.getcwd()
NOT_ALLOWED_EXTENTIONS = ['html', 'js', 'css', 'sh']

JWT_SECRET = "EtnCx2igyMUIQkc9"
JWT_EXPIRETIME = 60 * 60 * 24  # jwt的过期时间

# 文字加密密码
ENCRYPT = "ThisisSecret"

#hash　key
HASH_KEY=os.getenv('HASH_KEY',"ThisIsHashKey")
