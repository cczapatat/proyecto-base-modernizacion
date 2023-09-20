import unittest


class CITestCase(unittest.TestCase):

    def test_ci_rebase(self):
        self.assertEqual('true', 'true')
