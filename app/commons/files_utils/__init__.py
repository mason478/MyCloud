import os
import pathlib

from app.commons.setting import UPLOAD_FILE_PATH
from app.commons.my_exception import FileHandlerError
from app.commons.change_format import RET


class FileHandler:
    @classmethod
    def is_exist_directory(cls, path):
        if not os.path.isdir(UPLOAD_FILE_PATH + '/' + path):
            os.makedirs(UPLOAD_FILE_PATH + '/' + path)
        return UPLOAD_FILE_PATH + '/' + path

    @classmethod
    def is_exist_files(cls, path, filename):
        pl = pathlib.Path(path + '/' + filename)
        return pl.exists()

    @classmethod
    def create_directory_by_user(cls, user_obj):
        if not os.path.isdir(UPLOAD_FILE_PATH + '/' + user_obj.id_hash):
            os.makedirs(UPLOAD_FILE_PATH + '/' + user_obj.id_hash)

    @classmethod
    def list_files(cls, path):
        """
        列出路径下的所有文件
        :param path: 相对路径
        :return:
        """
        try:
            files_list = os.listdir(UPLOAD_FILE_PATH + '/' + path)
            return files_list
        except Exception as e:
            raise FileHandlerError(error_code=RET.FILE_LISTS_ERROR)


if __name__ == "__main__":
    f = FileHandler
    r = f.list_files('5b0f4449ff5e390f0659'+'/')
    print(r)
