#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, image1, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(image1), (85, 70))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bomb.png', 5, self.rect.centerx, self.rect.top)
        bullets.add(bullet)

class Enemy(GameSprite):
    def move(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > 500:
            self.rect.x = randint(0, 600)
            self.rect.y = 0
            lose += 1

class Bullet(GameSprite):
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

crocodilo = Player('bombardilo.jpeg', 10, 350, 420)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('gusini.jpg', randint(1, 5), randint(0, 600), 0)
    monsters.add(monster)

window = display.set_mode((700, 500))
display.set_caption('Шутер')

background = transform.scale(image.load('sos.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

lose = 0 
font.init()
font1 = font.Font(None, 30)
font2 = font.Font(None, 70)
win_label = font2.render('Ti pobedil', True, (0, 115, 255))
lose_label1 = font2.render('Ti proigral', True, (0, 115, 255))

#! гы
# TODO orewuuftshdxtw6ifg

schetchik = 0

fps = 60
clock = time.Clock()
game = True
zhizni = 10
while game:
    window.blit(background, (0, 0))
    crocodilo.reset()
    crocodilo.move()
    monsters.draw(window)
    for monster in monsters:
        monster.move()

    bullets.draw(window)
    for bullet in bullets:
        bullet.move()

    if lose >= 10:
        window.blit(lose_label1, (250, 200))
        display.update()
        time.delay(3000)
        game = False

    if zhizni <= 0:
        window.blit(lose_label1, (250, 200))
        display.update()
        time.delay(3000)
        game = False

    sprites_list = sprite.groupcollide(monsters, bullets, True, True)

    sprites1_list = sprite.spritecollide(crocodilo, monsters, False)

    for s in sprites1_list:
        s.kill()
        zhizni -= 1
        monster = Enemy('gusini.jpg', randint(1, 5), randint(0, 600), 0)
        monsters.add(monster)

    for s in sprites_list:
        schetchik += 1
        monster = Enemy('gusini.jpg', randint(1, 5), randint(0, 600), 0)
        monsters.add(monster)

    if schetchik >= 30:
        window.blit(win_label, (250, 200))
        display.update()
        time.delay(3000)
        game = False

    score = font1.render('ochki: ' + str(schetchik), True, (255, 255, 255))
    lose_label = font1.render('propuscheno: ' + str(lose), True, (255, 255, 255))
    zizni = font1.render('zhizni: ' +str(zhizni), True, (255, 255, 255))
    window.blit(score, (10, 20))
    window.blit(lose_label, (10, 50))
    window.blit(zizni, (10, 80))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                crocodilo.fire()

    display.update()
    clock.tick(fps)