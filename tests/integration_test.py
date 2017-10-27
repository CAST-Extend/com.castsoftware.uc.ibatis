import cast_upgrade_1_5_14 # @UnusedImport
import unittest
from cast.application.test import run
from cast.application import create_postgres_engine


class TestIntegration(unittest.TestCase):

    def test1(self):
        
        run(kb_name='b820_1377_local', application_name='ibatis', engine=create_postgres_engine())


if __name__ == "__main__":
    unittest.main()
