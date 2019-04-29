import os

UPLOAD_FILE_PATH = os.getcwd()
NOT_ALLOWED_EXTENTIONS = ['html', 'js', 'css', 'sh']

JWT_SECRET = "EtnCx2igyMUIQkc9"
JWT_EXPIRETIME = 60 * 60 * 24  # jwt的过期时间

# 文字加密密码
ENCRYPT = "ThisisSecret"
