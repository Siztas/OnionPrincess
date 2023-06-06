from random import choice

from enemy import Enemy
from player import Player
from settings import *
from support import *
from tile import Tile
from ui import UI
from weapon import Weapon


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        # 需要导入csv文件
        layouts = {'boundary': import_csv_layout('onion.csv'),
                   'grass': import_csv_layout('onion.csv'),
                   'entities': import_csv_layout('enemy.csv')}
        # 'object':import_csv_layout('onion.csv')}
        graphics = {'grass': import_folder('人物包')}
        # 'objects':import_folder('人物包')}
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':  # -1是地图中的可移动路径
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary' and col == 2:  # 地图边界
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if style == 'grass':  # 草丛
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y),
                                 [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                                 'grass',
                                 random_grass_image)
                        # if style == 'object':
                        #     surf = graphics['objects'][int(col)]
                        #     Tile((x,y),[self.visible_sprites,self.obstacles_sprites],'object',surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacles_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                elif col == '393':
                                    monster_name = 'squid'
                                    Enemy(monster_name, (x, y),
                                          [self.visible_sprites, self.attackable_sprites],
                                          self.obstacles_sprites,
                                          self.damage_player)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load('floor.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
