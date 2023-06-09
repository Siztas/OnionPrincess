import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):

		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('ONION')
		self.clock = pygame.time.Clock()

		self.level = Level()
		self.isStart = False
		self.isPaused = False

		main_sound = pygame.mixer.Sound('../ONION/audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)

		self.nowMap = "Original"
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()
					if event.key == pygame.K_ESCAPE:
						self.isPaused = True
					if event.key == pygame.K_p:
						self.save()


			mouse = pygame.mouse.get_pos()
			if self.isStart and not self.isPaused:
				self.screen.fill(WATER_COLOR)
				self.level.run()
				pygame.display.update()
				self.clock.tick(FPS)
			elif self.isStart and self.isPaused:
				self.inGame_menu(mouse)
			elif not self.isStart:
				self.startGame_menu(mouse)

	def startGame_menu(self, mouse):
		self.screen.fill((150,200,150))
		text = smallfont.render('Start', True, color)

		# if mouse is hovered on a button it
		# changes to lighter shade
		if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGTH / 2 <= mouse[1] <= HEIGTH / 2 + 40:
			pygame.draw.rect(self.screen, color_light, [WIDTH / 2, HEIGTH / 2, 140, 40])

		else:
			pygame.draw.rect(self.screen, color_dark, [WIDTH / 2, HEIGTH / 2, 140, 40])

		# superimposing the text onto our button
		self.screen.blit(text, (WIDTH / 2 + 50, HEIGTH / 2))

		if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGTH / 2 <= mouse[1] <= HEIGTH / 2 + 40 and pygame.mouse.get_pressed()[0]:
			self.isStart = True

		# updates the frames of the game
		pygame.display.update()

	def inGame_menu(self, mouse):
		self.screen.fill((100,100,100))

		text_quit = smallfont.render('Back', True, color)

		# if mouse is hovered on a button it
		# changes to lighter shade
		if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGTH / 2 <= mouse[1] <= HEIGTH / 2 + 40:
			pygame.draw.rect(self.screen, color_light, [WIDTH / 2, HEIGTH / 2, 140, 40])

		else:
			pygame.draw.rect(self.screen, color_dark, [WIDTH / 2, HEIGTH / 2, 140, 40])

		# superimposing the text onto our button
		self.screen.blit(text_quit, (WIDTH / 2 + 50, HEIGTH / 2))

		if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGTH / 2 <= mouse[1] <= HEIGTH / 2 + 40 and pygame.mouse.get_pressed()[0]:
			self.isPaused = False

		# updates the frames of the game
		pygame.display.update()

	def save(self):
		player_pos = self.level.player.getPos()
		print("pos:",player_pos)
		player_stats = self.level.player.getStats()
		player_maxStats = self.level.player.getMaxStats()
		print("Stats",player_stats)
		print("MaxStats",player_maxStats)


if __name__ == '__main__':
	smallfont = pygame.font.SysFont('Corbel', 35)
	game = Game()
	game.run()