import random

# IMAGES
import discord

king_with_sword = "http://www.pngmart.com/files/3/Clash-of-Clans-PNG-Transparent.png"
discord_image = "https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png"
barb_destroys_pc = "https://media.discordapp.net/attachments/830882773367259196/830886084627267584/3kmn9hen1tv51.png"
super_wizard = "https://media.discordapp.net/attachments/830882773367259196/830886308595105862/gnit4ww4ad361.png?width=716&height=858"
imperial_king = "https://media.discordapp.net/attachments/830882773367259196/830886851329654804/lmcv0xjktns51.png?width=523&height=858"

# EMOJI
barb = "<:barb:826478237344858142>"
# sword = "<:sword:826479574992814140>"
sword = "<:swords:836905285372608512>"
shield = "<:shield:826478264033607680>"
th15 = "<:15:1028478312928002118>"
th14 = "<:14:828991721181806623>"
th13 = "<:13:701579367146455172>"
th12 = "<:12:701579365162418188>"
th11 = "<:11:701579365699551293>"
th10 = "<:10:701579365661671464>"
th9 = "<:09:701579365389041767>"
th8 = "<:08:701579365321801809>"
th7 = "<:07:701579365598756874>"
th6 = "<:06:701579365573459988>"
th5 = "<:05:701579365581848616>"
th4 = "<:04:701579365850284092>"
th3 = "<:03:701579364600643634>"
th2 = "<:02:701579364483203133>"
th1 = "<:01:701579364193534043>"
th0 = "<:00:not_found>"
star0 = "<:0_stars:826489159048495114>"
star1 = "<:1_star:826489159371587654>"
star2 = "<:2_stars:826489159450755112>"
star3 = "<:3_stars:826489161154297866> "
aq = "<:aq:652161132362072094>"
rc = "<:rc:657803787808800789>"
bk = "<:bk:652161160908505101>"
gw = "<:gw:652161163089543179>"
barbarian = "<:Barbarian:652161146241024001>"
archer = "<:Archer:652161113911328779>"
hogrider = "<:HogRider:652161144890458113>"
yeti = "<:Yeti:664470331590967319>"
wizard = "<:Wizard:652161302696820767>"
witch = "<:Witch:652161301715615767>"
wallbreaker = "<:WallBreaker:664467934357225472>"
valk = "<:valk:652161298901106689>"
pekka = "<:pekka:652161146597539841>"
minion = "<:Minion:652161149357260890>"
miner = "<:Miner:652161139471286282>"
lavahound = "<:lavahound:652161149026041876>"
icegolem = "<:ig:652161154608660500>"
headhunter = "<:hh:726648598871277650>"
healer = "<:Healer:652161145116950558>"
golem = "<:Golem:652161155665756170>"
goblin = "<:Goblin:652161144215306260>"
giant = "<:Giant:652161150385127426>"
ed = "<:ed:652161143724441610>"
dragon = "<:Dragon:652161143993008141>"
bowler = "<:Bowler:652161155757899777>"
baloon = "<:Balloon:652161116218327040>"
bd = "<:bd:652161141480488980>"
troops = [aq, bk, gw, rc, barbarian, archer, hogrider, yeti, wizard, witch, wallbreaker, valk, pekka, minion, miner,
          lavahound, icegolem, headhunter, healer, golem, goblin, giant, ed, dragon, bowler, baloon, bd]
images = [king_with_sword, super_wizard, barb_destroys_pc, king_with_sword]

th_list = [th0, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, th12, th13, th14, th15]

war_colors = {'friendly': discord.Color.dark_gold(), 'random': discord.Color.dark_orange(),
              'cwl': discord.Color.dark_magenta()}
status_colors = {'winning': discord.Color.dark_green(), 'losing': discord.Color.dark_red(), 'tie': discord.Color.dark_gold(),
                 'won': discord.Color.green(), 'lost': discord.Color.red(), 'tied': discord.Color.gold()}

def getRandomTroop():
    random_index = random.randrange(len(troops))

    return troops[random_index]


def getRandomImage():
    random_index = random.randrange(len(images))
    return images[random_index]


def getTownHallimage(level):
    return th_list[level]


def getTownHallLevelInt(emoji_code):
    return int(emoji_code[2:4])


def getLastTownHallLevelInt():
    return getTownHallLevelInt(th_list[-1])


PAGINATOR_TYPE = 2
