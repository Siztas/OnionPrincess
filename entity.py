import pygame
from math import sin

#由于人物和怪物的移动与碰撞一模一样，所以直接创建一个父类
class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = pygame.math.Vector2()

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed       #更新横坐标并判断水平碰撞
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed		#更新纵坐标并判断垂直碰撞
		self.collision('vertical')
		self.rect.center = self.hitbox.center           #获得此时坐标

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # 右走代表另一个物体左侧收到碰撞
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # 左走代表另一个物体右侧收到碰撞
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # 下走上撞
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # 上走下撞
						self.hitbox.top = sprite.hitbox.bottom

	def wave_value(self):
		value = sin(pygame.time.get_ticks())   #为了实现受到攻击后的虚化效果
		if value >= 0: 
			return 255
		else: 
			return 0

	def getPos(self):
		return (self.hitbox.x,self.hitbox.y)