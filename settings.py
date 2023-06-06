WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../期末/font.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# 武器
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '../期末/武器/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': '../期末/武器/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': '../期末/武器/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': '../期末/武器/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': '../期末/武器/sai/full.png'}}

# 技能
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': '../期末/技能/flame/素材.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': '../期末/技能/heal/素材人物.png'}}

# 敌人
monster_data = {'squid': {'health': 100,
                          'exp': 100,
                          'damage': 20,
                          'attack_type': 'slash',
                          'attack_sound': '../期末/音乐/20 - Good Time.ogg',
                          'speed': 0.5,
                          'resistance': 3,
                          'attack_radius': 80,
                          'notice_radius': 360}
                }
