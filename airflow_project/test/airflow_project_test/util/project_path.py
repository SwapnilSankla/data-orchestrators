import os


# pylint: disable=R0903: too-few-public-methods
class ProjectPath:
    @staticmethod
    def get():
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
