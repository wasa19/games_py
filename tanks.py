import pygame as pg
import random
# from random import randint, randrange
from os import path
import sys

pg.init()


FPS = 50
W = 800
H = 800
count = 0
helth = 10
lvl_no = 1
sc = pg.display.set_mode((W,H))


img_dir = path.join(path.dirname(__file__), 'img')
players_tank_image = pg.image.load(path.join(img_dir, 'tank-top-view-png-left.png')).convert()
players_tank_image_right = pg.image.load(path.join(img_dir, 'tank-top-view-png-right.png')).convert()
players_tank_image_down = pg.image.load(path.join(img_dir, 'tank-top-view-png-down.png')).convert()
players_tank_image_up = pg.image.load(path.join(img_dir, 'tank-top-view-png.png')).convert()
red_ball_image = pg.image.load(path.join(img_dir, 'red-solid-circle-png-image.png')).convert()
yellow_ball_image = pg.image.load(path.join(img_dir, 'yellow-solid-circle-png-image.png'))
green_ball_image = pg.image.load(path.join(img_dir, 'green-solid-circle-png-image.png'))

pg.font.init()
font = pg.font.Font(None, 26)
font_message = pg.font.Font(None, 56)
pg.mixer.init()
clock = pg.time.Clock()

def show_go_screen():
	sc.fill('#F4A460')
	font = pg.font.Font(None, 58)
	text_name = font.render('Танк и Мячики', True, 'black')
	text_name_place = text_name.get_rect(midtop = (W/2, H/4))
	text_opt = font.render('стрелки - двигаться, пробел - стрелять', True, 'white')
	text_opt_place = text_opt.get_rect(midtop =(W/2, H/2))
	if count > 0:
	    text_pts = font.render('Мячей сбито: ' + str(count), True, 'red')
	    text_pts_place = text_pts.get_rect(midtop = (W/2, H*0.8))
	    sc.blit(text_pts, text_pts_place)
	sc.blit(text_name, text_name_place)
	sc.blit(text_opt, text_opt_place)
    
	pg.display.flip()
	wating = True
	while wating:
		clock.tick(FPS)
		for i in pg.event.get():
			if i.type == pg.QUIT:
				pg.quit()
				sys.exit()
			if i.type == pg.KEYUP:
				wating = False



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


class Enemy(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(random.choice([red_ball_image, yellow_ball_image, green_ball_image]), (30, 30))
		self.image.set_colorkey('black')
		self.rect = self.image.get_rect()
		self.rect.centerx = random.randint((W/2+30), (W-40))
		self.rect.centery = random.randint((H/2+30), (H-40))
		self.dx_set = random.randint(2, 6)
		if self.dx_set >= 4:
			self.dy_set = random.randint(2, 4)
		else:
			self.dy_set = random.randint(4, 6)

	def update(self):
		if self.rect.top <= 0 or self.rect.bottom >= H:
			self.dy_set = -self.dy_set
		if self.rect.left <= 0 or self.rect.right >= W:
			self.dx_set = -self.dx_set

		self.rect.x += self.dx_set
		self.rect.y += self.dy_set


all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
enemys = pg.sprite.Group()
enemy = Enemy()
player_tank = PlayerTank()
enemys.add(enemy)
all_sprites.add(player_tank)
all_sprites.add(enemy)


running = True
game_over = True

while running:
	if game_over:
		helth = 10
		lvl_no = 1
		show_go_screen()
		count = 0
		game_over = False
	clock.tick(FPS)
	events = pg.event.get()
	for ev in events:
		if ev.type == pg.QUIT:
			pg.quit()
			sys.exit()
		elif ev.type == pg.KEYDOWN:
			if ev.key == pg.K_SPACE:
				player_tank.shoot()

	if len(enemys) < lvl_no:
		enemy = Enemy()
		enemys.add(enemy)
		all_sprites.add(enemy)

	hits = pg.sprite.groupcollide(enemys, bullets, True, True)
	for hit in hits:
	    # hit_snd.play()
	    pg.time.delay(300)
	    count += 1
	    if count == 10:
	    	lvl_no = 2
	    if count == 25:
	    	lvl_no = 3
	    if count ==50:
	    	lvl_no = 4

	collsn = pg.sprite.spritecollide(player_tank, enemys, True)
	for coll in collsn:
		pg.time.delay(300)
		helth -= 1
		if helth == 0:
			helth = 10
			game_over = True
			for enemy in enemys:
				if len(enemys) > 1:
					enemy.kill()

	# all_sprites = pg.sprite.Group()
	# player_tank = PlayerTank()
	# all_sprites.add(player_tank)
	sc.fill('white')

	all_sprites.update()
	all_sprites.draw(sc)

	text_scr = font.render('очки: ' + str(count), True, 'orange')
	text_lvl = font.render('уровень: ' + str(lvl_no), True, 'blue')
	text_place_scr = text_scr.get_rect(midbottom = (40, H-40))
	text_place_lvl = text_lvl.get_rect(midbottom = (W/2, H-40))
	text_lv = font.render('жизни: ' + str(helth), True, 'red')
	text_place_lv = text_lv.get_rect(midbottom = (W-100, H-40))
	sc.blit(text_scr, text_place_scr)
	sc.blit(text_lvl, text_place_lvl)
	sc.blit(text_lv, text_place_lv)


	pg.display.update()



# snd_dir = path.join(path.dirname(__file__), 'snd')
# font = pg.font.Font(None, 22)
