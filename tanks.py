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
players_tank_image = pg.image.load(path.join(img_dir, 'tank-top-view-png-left.png')).convert()
players_tank_image_right = pg.image.load(path.join(img_dir, 'tank-top-view-png-right.png')).convert()
players_tank_image_down = pg.image.load(path.join(img_dir, 'tank-top-view-png-down.png')).convert()
players_tank_image_up = pg.image.load(path.join(img_dir, 'tank-top-view-png.png')).convert()
red_ball_image = pg.image.load(path.join(img_dir, 'red-solid-circle-png-image.png')).convert()


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
		self.direction = 'left'

	def update(self):
		self.dx_set = 0
		self.dy_set = 0
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] and self.rect.left >= 0:
			self.image = pg.transform.scale(players_tank_image, (60, 60))
			self.direction = 'left'
			self.dx_set = -3
		elif keys[pg.K_RIGHT] and self.rect.right <= W:
			self.image = pg.transform.scale(players_tank_image_right, (60, 60))
			self.direction = 'right'
			self.dx_set = 3
		elif keys[pg.K_DOWN] and self.rect.bottom <= H:
			self.image = pg.transform.scale(players_tank_image_down, (60, 60))
			self.direction = 'down'
			self.dy_set = 3
		elif keys[pg.K_UP] and self.rect.top >= 0:
			self.image = pg.transform.scale(players_tank_image_up, (60, 60))
			self.direction = 'up'
			self.dy_set = -3

		self.rect.x += self.dx_set
		self.rect.y += self.dy_set

	def shoot(self):
		if len(bullets) == 0:
			bullet = Bullet(self.rect.centerx, self.rect.centery)
			all_sprites.add(bullet)
			bullets.add(bullet)



class Bullet(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(red_ball_image, (10, 10))
		self.image.set_colorkey('black')
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

		if player_tank.direction == 'left':
			self.direction = 'left'
		elif player_tank.direction == 'right':
			self.direction = 'right'
		elif player_tank.direction == 'up':
			self.direction = 'up'
		elif player_tank.direction == 'down':
			self.direction = 'down'

	def update(self):
		if self.direction == 'left':
			self.rect.x -= 8
			if self.rect.left < 0:
				self.kill()
		elif self.direction == 'right':
			self.rect.x += 8
			if self.rect.right > W:
				self.kill()
		elif self.direction == 'up':
			self.rect.y -= 8
			if self.rect.top < 0:
				self.kill()
		elif self.direction == 'down':
			self.rect.y += 8
			if self.rect.bottom > H:
				self.kill()



all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
player_tank = PlayerTank()
all_sprites.add(player_tank)




while True:
	clock.tick(FPS)
	events = pg.event.get()
	for ev in events:
		if ev.type == pg.QUIT:
			pg.quit()
			sys.exit()
		elif ev.type == pg.KEYDOWN:
			if ev.key == pg.K_SPACE:
				player_tank.shoot()


	# all_sprites = pg.sprite.Group()
	# player_tank = PlayerTank()
	# all_sprites.add(player_tank)
	sc.fill('white')

	all_sprites.update()
	all_sprites.draw(sc)

	pg.display.update()



# snd_dir = path.join(path.dirname(__file__), 'snd')
# font = pg.font.Font(None, 22)
