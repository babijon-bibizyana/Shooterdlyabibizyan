from typing import Any
from pygame import *
from random import randint 


mixer.init()
mixer.music.load('springlox.ogg')
mixer.music.play()
fire_sound = mixer.Sound('sdoxlox.ogg')

font.init()

font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))

font2 = font.Font(None, 36)

img_enemy = 'ahah.png'
img_back = 'lala123.png'
img_bullet = 'lala.png '
img_hero = 'lala2.png'

score = 0
goal = 1000
lost = 0
max_lost = 5

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y,size_x,size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.y > 5:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-0, self.rect.top,15, 20, 15)
        bullets.add(bullet)
        bullet = Bullet(img_bullet, self.rect.centerx-35, self.rect.top,15, 20, 15)
        bullets.add(bullet)
        bullet = Bullet(img_bullet, self.rect.centerx+35, self.rect.top,15, 20, 15)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(5, win_width - 80)
            self.rect.y = - 40
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()

win_width = 800
win_height = 600
display.set_caption('SHOOTER')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back),(win_width, win_height))

ship = Player(img_hero, 5, win_height-90, 50, 80, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint( 5, win_width - 80), -15, 130,100, randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()

finish = True
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()


    if  finish:
        window.blit(background, (0,0))
        
        text = font2.render('Счёт: ' + str(score), 1,(255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено: ' + str (lost), 1, (255,255,255))
        window.blit(text_lose,(10,50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 2
            monster = Enemy(img_enemy, randint(5, win_width - 80), -40 , 130,100, randint(1,3))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = False
            window.blit(lose,(200, 200))
        
        if score >= goal:
            finish = False
            window.blit(win,(200,200))

    else:
        finish = True
        score = 0
        lost = 0
        for b in bullets:
            b.kill() 
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(5, win_width - 80), -40, 130,100, randint(1,3))
            monsters.add(monster)

    display.update()
    time.delay(25)