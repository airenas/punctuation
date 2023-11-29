import unittest

import text_to_train


class TestChangeUnk(unittest.TestCase):

    def test_no_change(self):
        self.assertEqual("olia", text_to_train._change_unk('olia'))
        self.assertEqual("<NUM>", text_to_train._change_unk('<NUM>'))
        self.assertEqual("</S>", text_to_train._change_unk('</S>'))
        self.assertEqual("10-a", text_to_train._change_unk('10-a'))

    def test_change(self):
        self.assertEqual('<UNK>', text_to_train._change_unk('<>'))
        self.assertEqual('<UNK>', text_to_train._change_unk('<10,34,3434>'))
        self.assertEqual('<UNK>', text_to_train._change_unk('<unk>'))


if __name__ == '__main__':
    unittest.main()
