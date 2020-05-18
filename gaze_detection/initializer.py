import os

from gaze_detection.definitions import PATH_UPLOADS


class Initializer:

    @staticmethod
    def initialize_db():
        pass

    @staticmethod
    def initialize_files():
        """
        Ensure that all required files (eg. log files, data files) are there
        :return:
        """
        required_file_paths = []

        # create files, if required
        for path_file in required_file_paths:
            if not os.path.exists(path_file):
                path_dir = os.path.dirname(path_file)
                if not os.path.isdir(path_dir):
                    os.makedirs(path_dir)
                os.mknod(path_file)


    @staticmethod
    def initialize_folders():
        """
        Ensure that all required folders are there
        :return:
        """
        required_folder_paths = [PATH_UPLOADS]

        # create files, if required
        for path_folder in required_folder_paths:
            if not os.path.isdir(path_folder):
                os.makedirs(path_folder)


if __name__ == '__main__':
    Initializer.initialize_db()
    Initializer.initialize_folders()
    Initializer.initialize_files()
