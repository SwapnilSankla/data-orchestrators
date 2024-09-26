import os


class ProjectPath:
    @staticmethod
    def get():
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
