from werkzeug.utils import secure_filename

from app.commons.setting import NOT_ALLOWED_EXTENTIONS


# 检查文件名的合法性
# TODO:目前不支持中文名
def is_allowed_file(filename):
    filename = secure_filename(filename)
    name_list = filename.split('.', 1)
    if len(name_list) == 1:
        return False
    if name_list[-1] in NOT_ALLOWED_EXTENTIONS:
        return False
    return filename
