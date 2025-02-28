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

power_chance = .10

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

def newpower():
    power = Power()
    all_sprite.add(power)
    powers.add(power)

class Power(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # LOOK LIKE WHAT?
        self.width = 32
        self.height = 32
        self.type = rn.randint(0,1)
        # self.image = pg.Surface((self.width, self.height))
        # self.image.fill(ORANGE)
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
        # check
        self.hit = False
        self.delay = 300
        self.last_delay = 0

    def update(self):
        self.rect.y += self.speedy
        if now - self.last_delay > self.delay:
            self.last_delay = now
            self.type = rn.randint(0, 1)
            if self.type == 0:
                self.image = pg.image.load("icons/Icon.1_18.png")
            elif self.type == 1:
                self.image = pg.image.load("icons/Icon.5_96.png")
            self.image = pg.transform.scale(self.image, (self.width, self.height))

#create objects
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #LOOK LIKE WHAT?
        self.width = 36
        self.height = 48
        #self.image = pg.Surface((self.width,self.height))
        #self.image.fill(BLUE)
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
        #powerups
        self.power = '0'
    def shoot(self):
        if self.power == '0':
            self.shoot_delay = 240
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('0')
        if self.power == '1':
            self.shoot_delay = 200
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('1')
        if self.power == '2':
            self.shoot_delay = 340
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('2v1')
                newbullet('2v2')
                newbullet('2v3')
        if self.power == '3':
            self.shoot_delay = 140
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                newbullet('3')

    def update(self):
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_RIGHT]:
            self.speedx = 10
        if keystate[pg.K_LEFT]:
            self.speedx = -10
        if keystate[pg.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx


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
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = rn.randint(20,WIDTH-20)
        self.rect.bottom = HEIGHT-rn.randint(-200,-5)
        #stats
        #health
        self.health = rn.randint(1,2)
        self.k = False
        #speed
        self.speedy = rn.randint(-3,-2)
    def load_images(self):
        for i in range(1, 11):
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
            self.kill()
            newmob()

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,typeq):
        pg.sprite.Sprite.__init__(self)
        # LOOK LIKE WHAT?
        self.width = 8
        self.height = 16
        # self.image = pg.Surface((self.width, self.height))
        # self.image.fill(ORANGE)
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

        elif self.type == '1':
            self.speedy = 7
            self.speedx = 0
            self.rect.centerx = x
            self.rect.bottom = y

        elif self.type == '2v1':
            self.speedy = 9
            self.speedx = -2
            self.rect.centerx = x
            self.rect.bottom = y
        elif self.type == '2v2':
            self.speedy = 10
            self.speedx = 0
            self.rect.centerx = x
            self.rect.bottom = y
        elif self.type == '2v3':
            self.speedy = 9
            self.speedx = 2
            self.rect.centerx = x
            self.rect.bottom = y

        elif self.type == '3':
            self.speedy = 12
            self.speedx = rn.randint(-3,3)
            self.rect.centerx = x
            self.rect.bottom = y

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.kill()


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
powers = pg.sprite.Group()
ui = pg.sprite.Group()

ship = Player()
all_sprite.add(ship)
friendlies.add(ship)

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
        ship.health -= 1
        newmob()

    hit_mob = pygame.sprite.groupcollide(enemies,bullets,False,True)
    if hit_mob:
        for mob in hit_mob:
            mob.health -= 1
        ship.score += rn.randrange(455,500)
        pick = rn.random()
        if pick <= power_chance:
            newpower()

    hit_power = pygame.sprite.spritecollide(ship, powers, True)
    if hit_power:
        ship.power = str(random.randint(0,3))
        newmob()

    if ship.health <= 0:
        running = False

    # Update
    now = pygame.time.get_ticks()
    all_sprite.update()
    # Draw / render
    screen.blit(background_img,background_rect)
    all_sprite.draw(screen)
    ui.draw(screen)
    drawtext(screen,str(ship.score),16,WIDTH-20,0,VIOLET)
    drawtext(screen,str(ship.health),16,20,0,VIOLET)
    drawtext(screen,str(ship.power),32,20,20,VIOLET)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()