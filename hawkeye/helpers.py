""" Helper functions """

import os

class Helpers(object):

    @staticmethod
    def get_assets_path():
        return os.path.join(os.path.dirname(__file__), '..', 'assets')