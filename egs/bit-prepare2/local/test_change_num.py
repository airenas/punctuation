import unittest

from importlib import import_module

import change_num


class TestChangeNum(unittest.TestCase):

    def test_no_change(self):
        self.assertEqual(change_num.change_word('{10}'), '{10}')
        self.assertEqual(change_num.change_word('adsad'), 'adsad')
        self.assertEqual(change_num.change_word('XI'), 'XI')

    def test_change(self):
        self.assertEqual('<NUM>', change_num.change_word('10'))
        self.assertEqual('<NUM>', change_num.change_word('10,34,3434'))
        self.assertEqual('<NUM>', change_num.change_word('10-34'))
        self.assertEqual('<NUM>', change_num.change_word('10.34.3434'))
        self.assertEqual('<NUM>', change_num.change_word('10:34'))
        self.assertEqual('<NUM>', change_num.change_word('.0'))


if __name__ == '__main__':
    unittest.main()
