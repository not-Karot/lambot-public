import unittest

from service.WarService import WarService


class MyTestCase(unittest.TestCase):
    dictionary = {739754997377663067: ['#208JLLJQQ', 1],
                  739755632340500510: ['#2900Y0PP2', 1],
                  822441604076797992: ['#2PRURUYPR', 1],
                  723889611473944600: ['#208JLLJQQ', 1]}
    service = WarService

    def test_getFirstChannelIDByTag_1(self):
        test_channel = 739754997377663067
        self.service.dict = self.dictionary
        self.assertEqual(self.service.getFirstChannelIDByTag(self.service, '#208JLLJQQ'), test_channel)

    def test_getFirstChannelIDByTag_2(self):
        self.service.dict = self.dictionary
        self.assertEqual(self.service.getFirstChannelIDByTag(self.service, '#208JLLJQT'), -1)

    def test_getAllChannelsIDByTag_1(self):
        test_list = [739754997377663067, 723889611473944600]
        self.service.dict = self.dictionary
        self.assertEqual(self.service.getAllChannelsIDByTagPostTrue(self.service, '#208JLLJQQ'), test_list)


if __name__ == '__main__':
    unittest.main()
