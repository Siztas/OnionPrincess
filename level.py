import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from Interaction import *

class Level:
	def __init__(self):

		# 界面
		self.display_surface = pygame.display.get_surface()
		self.game_paused_upgrade_menu = False

		# 元素（人物、怪物、障碍物）的初始化
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.chat_sprites = pygame.sprite.Group()
		self.chatable_sprites = pygame.sprite.Group()


		# 攻击元素的初始化
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# 创建地图并导入所有元素
		self.create_map()

		# 血条、蓝条等
		self.ui = UI()
		self.upgrade = Upgrade(self.player)

		# 离子特效
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)





	def create_map(self):

		layouts = {
			'boundary': import_csv_layout('../ONION/map/map_FloorBlocks.csv'),   #从csv文件中导入地图
			'grass': import_csv_layout('../ONION/map/map_Grass.csv'),
			'object': import_csv_layout('../ONION/map/map_Objects.csv'),
			'entities': import_csv_layout('../ONION/map/map_Entities.csv'),
			'Interaction':import_csv_layout('../ONION/map/map_NPC.csv')
		}
		graphics = {
			'grass': import_folder('../ONION/graphics/Grass'),    #障碍物图片地址
			'objects': import_folder('../ONION/graphics/objects'),
			'NPC':import_folder('../ONION/graphics/npc')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')   #在（x,y)处创建障碍物组的一些元素
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile(
								(x,y),
								[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
								'grass',
								random_grass_image)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

						if style == 'entities':
							if col == '394':
								self.player = Player(
									(x,y),
									[self.visible_sprites,self.chat_sprites],
									self.obstacle_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic,
									self.creat_chat)
							else:
								if col == '390': monster_name = 'bamboo'
								elif col == '391': monster_name = 'spirit'
								elif col == '392': monster_name ='raccoon'
								else: monster_name = 'squid'
								Enemy(
									monster_name,
									(x,y),
									[self.visible_sprites,self.attackable_sprites],
									self.obstacle_sprites,
									self.damage_player,
									self.trigger_death_particles,
									self.add_exp)
						if style == 'Interaction' :
							if col == '0':
								surf = graphics['NPC'][0]
								NPC((x,y),
									 [self.visible_sprites,self.obstacle_sprites,self.chatable_sprites],
									surf,self.player)
							if col == 't':
								surf = graphics['Transmit'][0]
								Transmit((x,y),
									 [self.visible_sprites,self.obstacle_sprites,self.chatable_sprites],
									surf,self.player,Level)


	# def create_map(self):
	#
	# 	layouts = {
	# 		'boundary': import_csv_layout('../ONION/map/map_FloorBlocks.csv'),   #从csv文件中导入地图
	# 		'grass': import_csv_layout('../ONION/map/map_Grass.csv'),
	# 		'object': import_csv_layout('../ONION/map/map_Objects.csv'),
	# 		'entities': import_csv_layout('../ONION/map/map_Entities.csv'),
	# 		'Interaction':import_csv_layout('../ONION/map/map_NPC.csv')
	# 	}
	# 	graphics ={
	# 		'grass': import_folder('../ONION/graphics/Grass'),    #障碍物图片地址
	# 		'objects': import_folder('../ONION/graphics/objects'),
	# 		'NPC':import_folder('../ONION/graphics/npc')}
	#
	# 	for style,layout in layouts.items():
	# 		for row_index,row in enumerate(layout):
	# 			for col_index, col in enumerate(row):
	# 				if col != '-1':
	# 					x = col_index * TILESIZE
	# 					y = row_index * TILESIZE
	# 					if style == 'boundary':
	# 						Tile((x,y),[self.obstacle_sprites],'invisible')   #在（x,y)处创建障碍物组的一些元素
	# 					if style == 'grass':
	# 						random_grass_image = choice(graphics['grass'])
	# 						Tile(
	# 							(x,y),
	# 							[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
	# 							'grass',
	# 							random_grass_image)
	#
	# 					if style == 'object':
	# 						surf = graphics['objects'][int(col)]
	# 						Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
	#
	# 					if style == 'entities':
	# 						if col == '394':
	# 							self.player = Player(
	# 								(x,y),
	# 								[self.visible_sprites,self.chat_sprites],
	# 								self.obstacle_sprites,
	# 								self.create_attack,
	# 								self.destroy_attack,
	# 								self.create_magic,
	# 								self.creat_chat)
	# 						else:
	# 							if col == '390': monster_name = 'bamboo'
	# 							elif col == '391': monster_name = 'spirit'
	# 							elif col == '392': monster_name ='raccoon'
	# 							else: monster_name = 'squid'
	# 							Enemy(
	# 								monster_name,
	# 								(x,y),
	# 								[self.visible_sprites,self.attackable_sprites],
	# 								self.obstacle_sprites,
	# 								self.damage_player,
	# 								self.trigger_death_particles,
	# 								self.add_exp)
	# 					if style == 'Interaction' :
	# 						if col == '0':
	# 							surf = graphics['NPC'][0]
	# 							NPC((x,y),
	# 								 [self.visible_sprites,self.obstacle_sprites,self.chatable_sprites],
	# 								surf,self.player)
	# 						if col == 't':
	# 							surf = graphics['Transmit'][0]
	# 							Transmit((x,y),
	# 								 [self.visible_sprites,self.obstacle_sprites,self.chatable_sprites],
	# 								surf,self.player,Level)


	def create_attack(self):
		
		self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])     #实现攻击

	def create_magic(self,style,strength,cost):											#实现技能
		if style == 'heal':
			self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

		if style == 'flame':
			self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

	def creat_chat(self):
		if self.chat_sprites :
			for chat_sprite in self.chat_sprites:
				collision_chat_sprites = pygame.sprite.spritecollide(chat_sprite,self.chatable_sprites,False)
				if collision_chat_sprites:
					for co_chat_sprite in collision_chat_sprites:
						if co_chat_sprite.sprite_type == 'NPC':
							co_chat_sprite.creat_chat()
						if co_chat_sprite.sprite_type == 'Transmit':
							co_chat_sprite.creat_chat()

	def destroy_attack(self):					#实现草丛的破坏
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def player_attack_logic(self):          #通过碰撞实现对怪物与草丛的攻击
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0,75)
							for leaf in range(randint(3,6)):           #实现草丛被破坏后的粒子特效
								self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	def damage_player(self,amount,attack_type):         #实现对人物的攻击
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])     #被攻击后的离子特效

	def trigger_death_particles(self,pos,particle_type):

		self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

	def add_exp(self,amount):

		self.player.exp += amount     #人物加经验

	def toggle_menu(self):

		self.game_paused_upgrade_menu = not self.game_paused_upgrade_menu

	def main_menu_1(self):

		self.game_paused_main_menu = not self.game_paused_main_menu


	def run(self):         #游戏的运行
		self.visible_sprites.custom_draw(self.player)					#创建人物（函数在下面YS类中）
		self.ui.display(self.player)									#创建血蓝条
		
		if self.game_paused_upgrade_menu:
			self.upgrade.display()

		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()
		

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# 一些基础设置
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# 导入地图最底层（无任何障碍物、怪物、人物）
		self.floor_surf = pygame.image.load('../ONION/graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)


