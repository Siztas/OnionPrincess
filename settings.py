#基础设置
from support import *

WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

#红蓝条
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../ONION/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# 武器库
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'../ONION/graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'../ONION/graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../ONION/graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../ONION/graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../ONION/graphics/weapons/sai/full.png'}}

# 技能库
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'../ONION/graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'../ONION/graphics/particles/heal/heal.png'}}

# 怪物库
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../ONION/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../ONION/audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../ONION/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../ONION/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

# 颜色
color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# 地图集
maps = {
	"Original":{},
	"Island":{
		"layouts":{
			'boundary': '../ONION/map/map_FloorBlocks.csv',   #从csv文件中导入地图
			'grass': '../ONION/map/map_Grass.csv',
			'object': '../ONION/map/map_Objects.csv',
			'entities': '../ONION/map/map_Entities.csv',
			'Interaction':'../ONION/map/map_NPC.csv'
		},
		"graphics" :{
			'grass': '../ONION/graphics/Grass',    #障碍物图片地址
			'objects': '../ONION/graphics/objects',
			'NPC':'../ONION/graphics/npc'}},
	"BossRoom":{},
	"Erebus":{}
}