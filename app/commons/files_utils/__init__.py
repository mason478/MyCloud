import os
import pathlib

from app.commons.setting import UPLOAD_FILE_PATH
from app.commons.my_exception import FileHandlerError
from app.commons.change_format import RET


class FileHandler:
    @classmethod
    def is_exist_directory(cls, directory, path=None):
        if path is None:
            if not os.path.isdir(UPLOAD_FILE_PATH + '/' + directory):
                os.makedirs(UPLOAD_FILE_PATH + '/' + directory)
            return UPLOAD_FILE_PATH + '/' + directory
        else:
            if not os.path.isdir(path + '/' + directory):
                os.makedirs(path + '/' + directory)
            return path + '/' + directory

    @classmethod
    def is_exist_files(cls, path, filename):
        pl = pathlib.Path(path + '/' + filename)
        return pl.exists()

    @classmethod
    def create_directory_by_user(cls, user_obj):
        if not os.path.isdir(UPLOAD_FILE_PATH + '/' + user_obj.id_hash):
            os.makedirs(UPLOAD_FILE_PATH + '/' + user_obj.id_hash)

    @classmethod
    def list_files(cls, directory_name, path=None):
        """
        列出路径下的所有文件
        :param path: 绝对路径
        :param directory_name :文件夹的名字

        :return:
        """
        if path is None:
            p = UPLOAD_FILE_PATH
        else:
            p = path
        try:
            files_list = os.listdir(p + '/' + directory_name)
            return files_list
        except Exception as e:
            raise FileHandlerError(error_code=RET.FILE_LISTS_ERROR)

    @classmethod
    def delete_directory(cls, path, directory_name):
        try:
            os.rmdir(path + '/' + directory_name)
        except Exception as e:
            raise FileHandlerError(error_code=RET.FILE_OR_DIR_DEL_ERROR)


if __name__ == "__main__":
    f = FileHandler
    r = f.list_files('5b0f4449ff5e390f0659' + '/')
    print(r)
