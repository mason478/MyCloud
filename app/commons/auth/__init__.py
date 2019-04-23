# 装饰器，用来验证token
import traceback
from flask import request,abort,Response


# def auth_required(func):
#     def wrapper(*args):
#         auth_header=request.headers.get('Authorization')
#
#     return wrapper

