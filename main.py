import pygame
import random

pg = pygame
rn = random

WIDTH = 520
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238,130,238)
ORANGE = (255, 165, 0)

font_name = pg.font.match_font('arial')

#object number
enemy_num = 0
bullet_num = 0

#definitions
def newmob():
    enemy = Mob()
    all_sprite.add(enemy)
    enemies.add(enemy)

def newbullet(typeq):
    bullet = Bullet(ship.rect.centerx, ship.rect.bottom,typeq)
    all_sprite.add(bullet)
    bullets.add(bullet)

def drawtext(surf,text,size,x,y,color):
    font = pg.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def newmoney():
    mon = Money()
    all_sprite.add(mon)
    moneys.add(mon)


class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.width = 40
        self.height = 40
        # Need shooting
        self.expl_anim = {}
        self.expl_anim['sm'] = []
        self.expl_anim['lg'] = []
        self.load_image()
        self.image = self.expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 60
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def load_image(self):
        for i in range(1,10):
            filename = 'explosion_img/explosion{}.png'.format(i)
            img = pygame.image.load(filename)
            img_lg = pygame.transform.scale(img,(50,50))
            self.expl_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img,(30,30))
            self.expl_anim['sm'].append(img_sm)


class Power(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # LOOK LIKE WHAT?
        self.width = 32
        self.height = 32
        self.type = rn.randint(0,1)
        "type"
        if self.type == 0:
            self.image = pg.image.load("icons/Icon.1_18.png")
        elif self.type == 1:
            self.image = pg.image.load("icons/Icon.5_96.png")
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = rn.randint(20,WIDTH-20)
        self.rect.bottom = HEIGHT + 20
        #stats
        # speed
        self.speedy = -5

    def update(self):
        self.rect.y += self.speedy


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #LOOK LIKE WHAT?
        self.width = 36
        self.height = 48
        self.image = pg.image.load("playerShip1_orange.png")
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.image = pg.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.top = 5
        #score
        self.score = 0
        #stats
        #health
        self.health = 3
        #speed
        self.speedx = 4
        self.speedy = 2
        #weapon
        self.shoot_delay = 240
        self.last_shot = 0
        #upgrades
        self.upgrade = '0'
        self.bullet_version = 1

    def shoot(self):
        if self.upgrade == '0':
            self.shoot_delay = 240
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('0')

        if self.upgrade == '1':
            self.shoot_delay = 200
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('1')

        if self.upgrade == '2-1':
            self.shoot_delay = 150
            if now - self.last_shot > self.shoot_delay and self.bullet_version == 1:
                self.last_shot = now
                newbullet('2-1v1')
                self.bullet_version = 2
            if now - self.last_shot > self.shoot_delay and self.bullet_version == 2:
                self.last_shot = now
                newbullet('2-1v2')
                self.bullet_version = 1
        if self.upgrade == '3-1':
            self.shoot_delay = 140
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('3-1')

        if self.upgrade == '2-2':
            self.shoot_delay = 300
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('2-2v1')
                newbullet('2-2v2')
        if self.upgrade == '3-2':
            self.shoot_delay = 340
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('3-2v1')
                newbullet('3-2v2')
                newbullet('3-2v3')


    def update(self):
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_d]:
            self.speedx = 10
        if keystate[pg.K_a]:
            self.speedx = -10
        self.rect.x += self.speedx

        if keystate[pg.K_SPACE]:
            self.shoot()
        if keystate[pg.K_LSHIFT]:
            upshop.shop_screen()


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        "make more enemy types"
        self.type = '1'
        #LOOK LIKE WHAT?
        if self.type == '1':
            self.width = 40
            self.height = 40
            self.meteor_list = []
            self.load_images()
            self.pick = rn.choice(self.meteor_list)
            self.image = self.pick
            self.health = 2
            self.score = 300
        if self.type == 'big':
            self.width = rn.randint(35,45)
            self.height = rn.randint(35,45)
            self.meteor_list = []
            self.load_images()
            self.pick = rn.choice(self.meteor_list)
            self.image = self.pick
            self.health = 10
            self.score = 800

        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = rn.randint(20,WIDTH-20)
        self.rect.bottom = HEIGHT-rn.randint(-200,-5)
        #stats
        #health
        self.k = False
        #speed
        self.speedy = rn.randint(-3,-2)

    def load_images(self):
        for i in range(1, 9):
            filename = 'meteor_img/meteor{}.png'.format(i)
            img = pg.image.load(filename)
            self.meteor_list.append(img)

    def update(self):
        if self.rect.bottom <= 0:
            self.rect.bottom = HEIGHT - rn.randint(-200, -5)
        self.rect.y += self.speedy
        if self.health <= 0:
            self.k = True
        if self.k:
            expl = Explosion(self.rect.center, "sm")
            all_sprite.add(expl)
            ship.score += self.score
            newmob()
            self.kill()


class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,typeq):
        pg.sprite.Sprite.__init__(self)
        # LOOK LIKE WHAT?
        self.width = 8
        self.height = 16
        self.image = pg.image.load("laserBlue03.png")
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        #stats
        self.type = typeq
        # speed
        self.choices = [-18,18]
        self.speedy = 0
        self.speedx = 0

        if self.type == '0':
            self.speedy = 10
            self.speedx = 0
            self.rect.centerx = x
            self.rect.bottom = y

        if self.type == '1':
            self.speedy = 7
            self.speedx = 0
            self.rect.centerx = x
            self.rect.bottom = y

        if self.type == '3-1':
            self.speedy = 12
            self.speedx = rn.randint(-3,3)
            self.rect.centerx = x
            self.rect.bottom = y

        if self.type == '2-1v1':
            self.speedy = 8
            self.speedx = 0
            self.rect.centerx = x-18
            self.rect.bottom = y
        if self.type == '2-1v2':
            self.speedy = 8
            self.speedx = 0
            self.rect.centerx = x+18
            self.rect.bottom = y

        if self.type == '2-2v1':
            self.speedy = 10
            self.speedx = -1
            self.rect.centerx = x
            self.rect.bottom = y
        if self.type == '2-2v2':
            self.speedy = 10
            self.speedx = 1
            self.rect.centerx = x
            self.rect.bottom = y

        if self.type == '3-2v1':
            self.speedy = 9
            self.speedx = -2
            self.rect.centerx = x
            self.rect.bottom = y
        if self.type == '3-2v2':
            self.speedy = 10
            self.speedx = 0
            self.rect.centerx = x
            self.rect.bottom = y
        if self.type == '3-2v3':
            self.speedy = 9
            self.speedx = 2
            self.rect.centerx = x
            self.rect.bottom = y

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.kill()


class Shop():
    def __init__(self):
        self.money = 0
        self.selectable = []
        self.selected = 0

    def update(self):
        keystate = pg.key.get_pressed()
        if ship.upgrade == '0':
            self.selectable = ['1']
        elif ship.upgrade == '1':
            self.selectable = ['2-1','2-2']
        elif ship.upgrade == '2-1':
            self.selectable = ['3-1']
        elif ship.upgrade == '2-2':
            self.selectable = ['3-2']

        if keystate[pg.K_1]:
            self.selected = 1
        if keystate[pg.K_2] and len(self.selectable) > 1:
            self.selected = 2
        if keystate[pg.K_TAB] and self.selected == 1:
            if self.selectable == '1':
                ship.upgrade = '1'
            if self.selectable == '2-1':
                ship.upgrade = '2-1'
            if self.selectable == '3-1':
                ship.upgrade = '3-1'
        if keystate[pg.K_TAB] and self.selected == 2:
            if self.selectable == '2-2':
                ship.upgrade = '2-1'
            if self.selectable == '3-2':
                ship.upgrade = '3-1'


    def shop_screen(self):
        screen.fill(BLACK)
        holding = True
        while holding:
            # keep loop running at the right speed
            clock.tick(FPS)
            # Process input (events)
            for event2 in pygame.event.get():
                # check for closing window
                if event2.type == pygame.QUIT:
                    holding = False
                if event2[pg.K_LCTRL]:
                    holding = False

            self.update()
            drawtext(screen, "Money: " + str(upshop.money), 24, 60 , 40, VIOLET)
            drawtext(screen, "Selected: " + str(upshop.selected), 24, 60 , 64, VIOLET)
            drawtext(screen, "Options: " + str(upshop.selectable[1]), 24, WIDTH-80, 40, VIOLET)
            pygame.display.flip()

class Money(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = pg.image.load("money1.png")
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = rn.randint(20,WIDTH-20)
        self.rect.bottom = HEIGHT + 20
        self.speedy = -5

    def update(self):
        self.rect.y += self.speedy

# initialize pygame and create window
pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()

all_sprite = pg.sprite.Group()
enemies = pg.sprite.Group()
friendlies = pg.sprite.Group()
bullets = pg.sprite.Group()
moneys = pg.sprite.Group()
ui = pg.sprite.Group()

ship = Player()
all_sprite.add(ship)
friendlies.add(ship)

upshop = Shop()

for i in range(8):
    newmob()

background_img = pg.image.load("starfield.png")
background_img = pg.transform.scale(background_img,(WIDTH,HEIGHT))
background_rect = background_img.get_rect()

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    hit_player = pygame.sprite.spritecollide(ship,enemies,True)
    if hit_player:
        expl = Explosion(ship.rect.midbottom, "sm")
        all_sprite.add(expl)
        ship.health -= 1

    hit_mob = pygame.sprite.groupcollide(enemies,bullets,False,True)
    if hit_mob:
        for mob in hit_mob:
            mob.health -= 1
        pick = rn.random()
        if pick <= .1:
            newmoney()

    hit_money = pygame.sprite.spritecollide(ship, moneys, True)
    if hit_money:
        upshop.money += 1

    if ship.health <= 0:
        expl = Explosion(ship.rect.midbottom, "lg")
        ship.kill()

    # Update
    now = pygame.time.get_ticks()
    all_sprite.update()
    # Draw / render
    screen.blit(background_img,background_rect)
    all_sprite.draw(screen)
    ui.draw(screen)
    drawtext(screen,str(ship.score),16,WIDTH-20,HEIGHT-50,VIOLET)
    drawtext(screen,str(ship.health),16,20,HEIGHT-50,VIOLET)
    drawtext(screen,str(ship.upgrade),16,20,HEIGHT-80,VIOLET)
    drawtext(screen,str(upshop.money),16,WIDTH-20,HEIGHT-80,VIOLET)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()