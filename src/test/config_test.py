from src import configurator
import unittest

config = configurator.Configurator("test_config.json")


class MyTestCase(unittest.TestCase):
    def test_read_config(self):
        self.assertEqual("Test", config.read_config()['Test'])

    def test_write_config(self):

        data = config.read_config()
        data['Test2'] = "Test2"

        config.write_config(data)

        self.assertEqual("Test2",config.read_config()['Test2'])

