import unittest
from service.PlayerService import PlayerService
import discord


class MyTestCase(unittest.TestCase):
    service = PlayerService
    player = [('Karot', '#9JPP0RQP', 13), ('•Karot悟空•', '#QVC0LVQG', 13), ('•Trunks絶市•', '#LVPUYRP', 12),
              ('Nameless復帰', '#VRQJ2R2R', 11)]
    players = [('#2J9QUGR2R', '•あCrimineᴿᴼᴹᴵ•', 12, '315286876623732750'),
               ('#9JPP0RQP', 'Karot', 13, '340083460389732352'), ('#QVC0LVQG', '•Karot悟空•', 13, '340083460389732352'),
               ('#LVPUYRP', '•Trunks絶市•', 12, '340083460389732352'),
               ('#VRQJ2R2R', 'Nameless復帰', 11, '340083460389732352')]
    line = "```13 #9JPP0RQP Karot``````13 #QVC0LVQG •Karot悟空•``````12 #LVPUYRP •Trunks絶市•``````11 #VRQJ2R2R Nameless復帰```"

    def test_createPlayerList(self):
        self.assertEqual(self.service.createPlayerList(self.service, self.player), self.line)


if __name__ == '__main__':
    unittest.main()
