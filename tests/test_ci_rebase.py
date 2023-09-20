import unittest


class CITestCase(unittest.TestCase):

    def test_ci_rebase(self):
        self.assertEqual('true', 'true')

    def test_ci_rebase_v2(self):
        self.assertEqual('false', 'false')

    def test_ci_rebase_v3(self):
        self.assertEqual('v3', 'v3')

    def test_ci_rebase_v4(self):
        self.assertEqual('v4', 'v4')
