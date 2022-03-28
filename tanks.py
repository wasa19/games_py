import pygame as pg
from random import randint, randrange
from os import path
import sys

pg.init()


FPS = 50
W = 800
H = 800
sc = pg.display.set_mode((W,H))


img_dir = path.join(path.dirname(__file__), 'img')
players_tank_image = pg.image.load(path.join(img_dir, 'tank.png')).convert()
players_tank_image_right = pg.image.load(path.join(img_dir, 'tank_right.png')).convert()
players_tank_image_down = pg.image.load(path.join(img_dir, 'tank_down.png')).convert()
players_tank_image_up = pg.image.load(path.join(img_dir, 'tank_up.png')).convert()


pg.font.init()
pg.mixer.init()
clock = pg.time.Clock()


class PlayerTank(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(players_tank_image, (60, 60))
		self.image.set_colorkey('black')
		self.rect = self.image.get_rect()
		self.rect.centerx = W / 2
		self.rect.centery = H / 2
		self.dx_set = 0
		self.dy_set = 0

	def update(self):
		self.dx_set = 0
		self.dy_set = 0
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] and self.rect.left >= 0:
			self.image = pg.transform.scale(players_tank_image, (60, 60))
			self.dx_set = -3
		elif keys[pg.K_RIGHT] and self.rect.right <= W:
			self.image = pg.transform.scale(players_tank_image_right, (60, 60))
			self.dx_set = 3
		elif keys[pg.K_DOWN] and self.rect.bottom <= H:
			self.image = pg.transform.scale(players_tank_image_down, (60, 60))
			self.dy_set = 3
		elif keys[pg.K_UP] and self.rect.top >= 0:
			self.image = pg.transform.scale(players_tank_image_up, (60, 60))
			self.dy_set = -3

		self.rect.x += self.dx_set
		self.rect.y += self.dy_set


all_sprites = pg.sprite.Group()
player_tank = PlayerTank()
all_sprites.add(player_tank)




while True:
	clock.tick(FPS)
	events = pg.event.get()
	for ev in events:
		if ev.type == pg.QUIT:
			pg.quit()
			sys.exit()


	# all_sprites = pg.sprite.Group()
	# player_tank = PlayerTank()
	# all_sprites.add(player_tank)
	sc.fill('white')

	all_sprites.update()
	all_sprites.draw(sc)


	pg.display.update()



# img_dir = path.join(path.dirname(__file__), 'img')
# snd_dir = path.join(path.dirname(__file__), 'snd')
# pg.font.init()
# pg.init()
# pg.mixer.init()
# sc = pg.display.set_mode((W,H))
# font = pg.font.Font(None, 22)
