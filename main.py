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

enemies_killed = 0
level = 1
level_requirement = 20+round((level*2)**1.05)

delay_time = 0

#definitions
def newmob(typpity):
    enemy = Mob(typpity)
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

def next_level():
    global level,enemies_killed,level_requirement
    enemies_killed = 0
    level += 1
    level_requirement = 20+round((level*2)**1.05)

    newmob('heavy')
    if level//3 >= 1:
        for i in range(level//3):
            newmob('basic')
    else:
        newmob('basic')

    return level, enemies_killed, level_requirement

def draw_shield_bar(surf, x, y, pct,color):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 5) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


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
        self.expl_anim['md'] = []
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
            img_lg = pygame.transform.scale(img,(500,500))
            self.expl_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img,(30,30))
            self.expl_anim['sm'].append(img_sm)
            img_md = pygame.transform.scale(img, (80, 80))
            self.expl_anim['md'].append(img_md)


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
        self.max_health = 5
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
            self.shoot_delay = 175
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
        if self.health > self.max_health:
            self.health = self.max_health
        keystate = pg.key.get_pressed()
        if keystate[pg.K_d]:
            self.speedx = 10
        if keystate[pg.K_a]:
            self.speedx = -10
        self.rect.x += self.speedx

        if keystate[pg.K_SPACE]:
            self.shoot()
        if keystate[pg.K_LSHIFT]:
            ui_screens.shop()


class Mob(pg.sprite.Sprite):
    def __init__(self,typey):
        pg.sprite.Sprite.__init__(self)
        "make more enemy types"
        self.type = typey
        #LOOK LIKE WHAT?
        if self.type == 'basic':
            self.width = 40
            self.height = 40
            self.meteor_list = []
            self.load_images()
            self.pick = rn.choice(self.meteor_list[5:])
            self.image = self.pick
            self.health = 2
            self.score = 300
            self.speedy = rn.randint(-3, -2)

        if self.type == 'heavy':
            self.width = rn.randint(65,70)
            self.height = rn.randint(65,70)
            self.meteor_list = []
            self.load_images()
            self.pick = rn.choice(self.meteor_list[:5])
            self.image = self.pick
            self.health = 16
            self.score = 800
            self.speedy = -1

        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = rn.randint(20,WIDTH-20)
        self.rect.bottom = HEIGHT-rn.randint(-200,-5)
        #stats
        #health
        self.k = False
        #speed


    def load_images(self):
        for i in range(1, 9):
            filename = 'meteor_img/meteor{}.png'.format(i)
            img = pg.image.load(filename)
            self.meteor_list.append(img)

    def update(self):
        global enemies_killed
        if self.rect.bottom <= 0:
            self.rect.bottom = HEIGHT - rn.randint(-200, -5)
        self.rect.y += self.speedy
        if self.health <= 0:
            self.k = True
        if self.k and self.type == 'basic':
            expl = Explosion(self.rect.center, "sm")
            all_sprite.add(expl)
            ship.score += self.score
            enemies_killed += 1
            newmob('basic')
            self.kill()

        if self.k and self.type == 'heavy':
            expl = Explosion(self.rect.center, "md")
            all_sprite.add(expl)
            ship.score += self.score
            enemies_killed += 1
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
            self.width = 12
            self.height = 20
            self.rect.centerx = x
            self.rect.bottom = y

        if self.type == '2-1v1':
            self.speedy = 8
            self.speedx = 0
            self.width = 12
            self.height = 20
            self.rect.centerx = x-18
            self.rect.bottom = y
        if self.type == '2-1v2':
            self.speedy = 8
            self.speedx = 0
            self.width = 12
            self.height = 20
            self.rect.centerx = x+18
            self.rect.bottom = y

        if self.type == '3-1':
            self.speedy = 12
            self.speedx = rn.randint(-3,3)
            self.rect.centerx = x
            self.rect.bottom = y

        if self.type == '2-2v1':
            self.speedy = 10
            self.speedx = 0
            self.rect.centerx = x+18
            self.rect.bottom = y
        if self.type == '2-2v2':
            self.speedy = 10
            self.speedx = 0
            self.rect.centerx = x-18
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

        self.image = pg.transform.scale(self.image, (self.width, self.height))

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.kill()


class Screens():
    def __init__(self):
        self.money = 0
        self.selectable = []
        self.selected = 0
        self.go = True

    def update_shop(self):
        keystate = pg.key.get_pressed()
        if ship.upgrade == '0':
            self.selectable = ['1','X']
        elif ship.upgrade == '1':
            self.selectable = ['2-1','2-2']
        elif ship.upgrade == '2-1':
            self.selectable = ['3-1','X']
        elif ship.upgrade == '2-2':
            self.selectable = ['X','3-2']
        elif ship.upgrade == '3-1':
            self.selectable = ['X','X']
        elif ship.upgrade == '3-2':
            self.selectable = ['X','X']

        if keystate[pg.K_1]:
            self.selected = 1
        if keystate[pg.K_2] and self.selectable[1] != 'X':
            self.selected = 2
        if keystate[pg.K_3]:
            self.selected = 3

        if keystate[pg.K_TAB] and self.selected == 1 and self.go and self.selectable[0] != 'X':
            if self.selectable[0] == '1' and self.money >= 5:
                ship.upgrade = '1'
                self.money -= 5
                self.go = False
            if self.selectable[0] == '2-1' and self.money >= 10:
                ship.upgrade = '2-1'
                self.money -= 10
                self.go = False
            if self.selectable[0] == '3-1' and self.money >= 20:
                ship.upgrade = '3-1'
                self.money -= 20
                self.go = False

        if keystate[pg.K_TAB] and self.selected == 2 and self.go and self.selectable[1] != 'X':
            if self.selectable[1] == '2-2' and self.money >= 10:
                ship.upgrade = '2-2'
                self.money -= 10
                self.go = False
            if self.selectable[1] == '3-2' and self.money >= 20:
                ship.upgrade = '3-2'
                self.money -= 20
                self.go = False

        if keystate[pg.K_TAB] and self.selected == 3 and self.go and ship.health < ship.max_health:
            if self.money >= 5:
                ship.health += 1
                self.money -= 5
                self.go = False

        if not keystate[pg.K_TAB]:
            self.go = True

    def shop(self):
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
            keystate = pg.key.get_pressed()
            if keystate[pg.K_LCTRL]:
                holding = False
            screen.fill(BLACK)
            self.update_shop()
            drawtext(screen, "Money: " + str(self.money), 24, 60 , 40, VIOLET)
            drawtext(screen, "Selected: " + str(self.selected), 24, 60 , 64, VIOLET)
            drawtext(screen, "Options: " + str(self.selectable[0]) + ", " + str(self.selectable[1]), 24, WIDTH-160, 40, VIOLET)
            drawtext(screen, "A: left, D: right, space: shoot", 24, WIDTH//2, 100, VIOLET)
            drawtext(screen, "Shift: open shop, Ctrl: close shop, ", 24, WIDTH//2, 130, VIOLET)
            drawtext(screen, "1: upgrade 1, 2: upgrade 2, 3: regain 1 health", 24, WIDTH//2, 160, VIOLET)
            pygame.display.flip()

    def menu(self):
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
            keystate = pg.key.get_pressed()
            if keystate[pg.K_LCTRL]:
                holding = False
            screen.fill(BLACK)
            drawtext(screen, "Pygameshooterthingy", 32, WIDTH // 2, 24, VIOLET)
            drawtext(screen, "A: left   D: right   Space: shoot", 24, WIDTH // 2, 100, VIOLET)
            drawtext(screen, "Shift: open shop  Ctrl: close menus  Tab: confirm", 24, WIDTH // 2, 130, VIOLET)
            drawtext(screen, "1: upgrade 1  2: upgrade 2  3: regain 1 health", 24, WIDTH // 2, 160, VIOLET)
            pygame.display.flip()

    def death(self):
        global running

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
                    running = False
            keystate = pg.key.get_pressed()
            if keystate[pg.K_LCTRL]:
                holding = False
            screen.fill(BLACK)
            drawtext(screen, "You have met your end,", 32, WIDTH // 2, 24, VIOLET)
            drawtext(screen, "But you can always try again.", 32, WIDTH // 2, 64, VIOLET)
            drawtext(screen, "You died with a score of " + str(ship.score), 24, WIDTH // 2, 124, VIOLET)
            drawtext(screen, "And you died on level " + str(level), 24, WIDTH // 2, 152, VIOLET)

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

ui_screens = Screens()

for i in range(8):
    newmob('basic')

background_img = pg.image.load("starfield.png")
background_img = pg.transform.scale(background_img,(WIDTH,HEIGHT))
background_rect = background_img.get_rect()

ui_screens.menu()

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

    now = pygame.time.get_ticks()

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
        ui_screens.money += 1

    if ship.health == 0:
        expl = Explosion(ship.rect.midbottom, "lg")
        all_sprite.add(expl)
        ship.kill()
        ship.health = -5
        delay_time = now

    if ship.health <= -1:
        delay = 2000
        if now - delay_time > delay:
            delay_time = now
            ui_screens.death()

    if enemies_killed >= level_requirement:
        level, enemies_killed, level_requirement = next_level()

    # Update
    all_sprite.update()
    # Draw / render
    screen.blit(background_img,background_rect)
    all_sprite.draw(screen)
    draw_shield_bar(screen, 20, HEIGHT-50,ship.health,VIOLET)
    drawtext(screen,str(ship.score),16,WIDTH-20,HEIGHT-50,VIOLET)
    drawtext(screen,str(ship.upgrade),16,20,HEIGHT-80,VIOLET)
    drawtext(screen, str(ui_screens.money), 16, WIDTH - 20, HEIGHT - 80, VIOLET)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()