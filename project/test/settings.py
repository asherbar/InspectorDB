"""
A settings file for tests only. To run all tests with these setting execute:
    ./manage.py test --settings=project.test.setting
"""
import os

os.environ['SECRET_KEY'] = 'Nsq3x77qpLlMd0Fx'

# Needed in order to override original settings
# noinspection PyUnresolvedReferences
from project.settings import *

DEBUG = True
