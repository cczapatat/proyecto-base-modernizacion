import unittest


class CITestCase(unittest.TestCase):

    def test_ci_rebase_test(self):
        self.assertEqual('true', 'true')