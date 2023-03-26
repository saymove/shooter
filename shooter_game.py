from random import *
from pygame import *
from time import time as timer

#крутой проеукт 

num_fire = 0
now_time = 0
last_time = 0
lost = 0
score = 0
window = display.set_mode((1250, 650))
display.set_caption("Шутер")
back = transform.scale(image.load('swink.jpg'), (1250, 650))
mixer.init()
mixer.music.load('pepa.mp3')
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')



bullets = sprite.Group()

sprite2 = transform.scale(image.load('kolbasa.png'), (160, 120))
bullet = transform.scale(image.load('rotik.png'), (80, 100))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
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
        if keys[K_a] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x<1120:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('rotik.png', self.rect.centerx, self.rect.top, 65, 85, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 650:
            self.rect.x = randint(80, 1150)
            self.rect.y = 0
            lost = lost + 1

ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('kolbasa.png', randint(80, 1150), -40, 120, 80, randint(1, 5))
    ufos.add(ufo)

cheeses = sprite.Group()
for s in range(1, 4):
    cheese = Enemy('cheese.png', randint(80, 1150), -40, 130, 90, randint(1, 3))
    cheeses.add(cheese)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

max_lost = 7

font.init()
font2 = font.SysFont('Times New Roman', 48)

lose1 = font2.render('ЛОШАРА!', True, (180, 0, 0))
win1 = font2.render('ТЫ ЛУЧШАЯ ПЕППА', True, (255, 0, 255))
r = font2.render('ПЕРЕЗАРЯДКА!', True, (255, 0, 0))

sprite1 = transform.scale(image.load('swin.png'), (130, 190))
        
player = Player('pep.png', 600, 460, 150, 190, 10)
rel_time = False
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN and e.button == 1 and finish == False:
        #проверяем, сколько выстрелов сделано и не происходит ли перезарядка
            if num_fire < 5 and rel_time == False:
                num_fire = num_fire + 1
                fire_sound.play()
                player.fire()
                     
            if num_fire  >= 5 and rel_time == False : #если игрок сделал 5 выстрелов
                last_time = timer() #засекаем время, когда это произошло
                rel_time = True #ставим флаг перезарядки
           
            
            
    if not finish:
        window.blit(back, (0, 0))
        win = font2.render('Съедено:' + str(score), 1, (255, 0, 255))
        window.blit(win, (10, 40))
        lose = font2.render('Голоден:' + str(lost), 1, (255, 0, 255))
        window.blit(lose, (10, 80))
        bul = font2.render('Потрачено:' + str(num_fire), 1, (255, 0, 255))
        window.blit(bul, (10, 120))
        player.update()
        player.reset()
        ufos.update()
        ufos.draw(window)
        cheeses.update()
        cheeses.draw(window)
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(ufos, bullets, True, True)
        if rel_time == True:
            now_time = timer() 
            if now_time - last_time < 2:
                window.blit(r, (200, 500))
            else:
                num_fire = 0 
                rel_time = False

        
        for c in collides:
            score = score + 1
            ufo = Enemy('kolbasa.png', randint(80, 1150), -40, 120, 80, randint(1, 5))
            ufos.add(ufo)
        if sprite.spritecollide(player, ufos, False) or lost >= max_lost or sprite.spritecollide(player, cheeses, False):
            finish = True
            window.blit(lose1, (200, 200))
            mixer.music.stop()
            fire_sound.stop()
            mixer.music.load('loshara.mp3')
            mixer.music.play(+4)
        if score >= 10:
            finish = True
            window.blit(win1, (200, 200))
            mixer.music.stop()
            mixer.music.load('ti_peppa.mp3')
            mixer.music.play(+4)
        display.update()
time.delay(60)
    
