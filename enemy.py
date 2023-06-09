import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):

		#在Entity里面建立敌人类
		super().__init__(groups)
		self.sprite_type = 'enemy'

		#导入图片
		self.import_graphics(monster_name)			#确定是哪一个类型的怪
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]

		# 怪物的移动
		self.rect = self.image.get_rect(topleft = pos) 			#获取位置
		self.hitbox = self.rect.inflate(0,-10) 					#设置碰撞的具体方块
		self.obstacle_sprites = obstacle_sprites			    #障碍物（为了实现怪物与障碍物的碰撞）

		# 怪物属性的设置
		self.monster_name = monster_name
		monster_info = monster_data[self.monster_name]				#根据名称从怪物集合中获取该怪物数据
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']				#伤害
		self.resistance = monster_info['resistance']			#被攻击时被击退格
		self.attack_radius = monster_info['attack_radius']		#攻击范围
		self.notice_radius = monster_info['notice_radius']		#侦查半径
		self.attack_type = monster_info['attack_type']			#攻击方式

		# 与人物的互动
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player							#对人物的攻击（具体函数在level中）
		self.trigger_death_particles = trigger_death_particles  	#死亡特效
		self.add_exp = add_exp

		# 创建无敌帧（避免被连续快速多次攻击）
		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 300

		# 音效（可不加）
		self.death_sound = pygame.mixer.Sound('../ONION/audio/death.wav')
		self.hit_sound = pygame.mixer.Sound('../ONION/audio/hit.wav')
		self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
		self.death_sound.set_volume(0.6)
		self.hit_sound.set_volume(0.6)
		self.attack_sound.set_volume(0.6)

	def import_graphics(self,name):				#从文件夹中导入图片（因为存在多个相似文件夹，直接写了个函数解决）
		self.animations = {'idle':[],'move':[],'attack':[]}
		main_path = f'../ONION/graphics/monsters/{name}/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

	def get_player_distance_direction(self,player):      		#获取与人物的方向与距离（用于移动）
		enemy_vec = pygame.math.Vector2(self.rect.center)		#怪位置
		player_vec = pygame.math.Vector2(player.rect.center)	#人物位置
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def get_status(self, player):          				#判断怪物下一步应该做什么
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self,player):  			#进行怪物动作的实现
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()   #获取时间戳（为了实现攻击的冷却）
			self.damage_player(self.attack_damage,self.attack_type)
			self.attack_sound.play()
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()

	def animate(self):             #多张图片的反复播放
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):        # 制造攻击的冷却
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self,player,attack_type):        #有关受到攻击的实现
		if self.vulnerable:
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()      #判断是技能伤害还是武器伤害
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):      #确认是否死亡
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center,self.monster_name)   #死亡特效
			self.add_exp(self.exp)
			self.death_sound.play()

	def hit_reaction(self):    #实现击退
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self):    #不断更新状态
		self.hit_reaction()
		self.move(self.speed)
		self.animate()
		self.cooldowns()
		self.check_death()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)