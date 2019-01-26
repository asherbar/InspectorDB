import unittest

from project.test.postgres_container_utils import PostgresContainerManager


class TestQuery(unittest.TestCase):
    postgres_container_manager = None

    # @classmethod
    # def setUpClass(cls):
    #     cls.postgres_container_manager = PostgresContainerManager()
    #     cls.postgres_container_manager.run()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls.postgres_container_manager.remove()
