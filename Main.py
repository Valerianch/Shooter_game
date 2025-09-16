from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, playre_image, playre_x, playre_y, playre_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(playre_image),(w,h))
        self.speed = playre_speed
        self.rect = self.image.get_rect()
        self.rect.x = playre_x
        self.rect.y = playre_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(('пуля_bulletboss3.png'), self.rect.centerx, self.rect.top, 15, 20,60)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost += 1 
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80,620) 
            
window = display.set_mode((700,500))
wino = transform.scale(image.load('фон_background2.png'),(700,500))
display.set_caption('Шутер')

clock = time.Clock()
FPS = 40

lost = 0 #пропущенный
shot = 0 #сбитый
life = 3 #жизни
num_fire = 0 #отстреленные
rel_time = False #процес перезарядки

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.3)
kick = mixer.Sound('fire.ogg')
kick.set_volume(0.4)

life_bar = transform.scale(image.load('life_bar.png'), (30,30))

playre = Player('player.png', 200, 400, 5, 60, 50)
asters = sprite.Group()
for i in range(1,4):
    aster = Asteroid('метиорит_meteor2_4.png', randint(80,620), -50, randint(2,5), 50,50)
    asters.add(aster)
monsters = sprite.Group()
for i in range (1,6):
    monster = Enemy('враг_enemy2_2.png', randint(80,620), -50, randint(1,3), 70, 60)
    monsters.add(monster)
    
bullets = sprite.Group()

game = True
finish = False

font.init()
font1 = font.SysFont('georgia', 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game  = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 7 and rel_time == False:
                    playre.fire()
                    kick.play()
                    num_fire += 1
                if num_fire >= 7 and rel_time == False:
                    rel_time = True 
                    start_time=timer()
                    
    
    if not finish:
        text_shot = font1.render('Счет: '+str(shot), 1, (255,255,255))
        text_lose = font1.render('Пропущено: '+ str(lost), 1, (255,255,255))
        window.blit(wino, (0,0))
    
        window.blit(text_lose, (10,50))
        window.blit(text_shot, (10,10))
        
        playre.update()
        monsters.update()
        bullets.update()
        asters.update()
        playre.reset()
        monsters.draw(window)
        bullets.draw(window)
        asters.draw(window)
        if rel_time == True:
            nuw_time = timer()
            dif_time = nuw_time - start_time
            if dif_time < 3:
                text_perez = font1.render('Перезарядка, ждите...', 1, (136, 130, 0))
                window.blit(text_perez, (250,200))
            else:
                num_fire = 0
                rel_time = False
        
        sprites_list=sprite.groupcollide(monsters, bullets, True, True)
        for _ in sprites_list:
            shot += 1
            monster = Enemy('враг_enemy2_2.png', randint(80,620), -50, randint(1,3), 70, 60)
            monsters.add(monster)
        
        if sprite.spritecollide(playre, asters, True) or sprite.spritecollide(playre, monsters, True):
            life -=1
        
        if lost >= 12 or life == 0:
            finish = True
            text_proig = font1.render('Вы ПРОИГРАЛИ!!!', 1, (136, 3, 3))
            window.blit(text_proig, (250,200))
        
        if shot == 10:
            finish = True
            text_victory = font1.render('Вы Победили!!!', 1, (5, 152, 3))
            window.blit(text_victory, (250,200))
        
        if life == 3:
            window.blit(life_bar, (580,10))
            window.blit(life_bar, (615,10))
            window.blit(life_bar, (650,10))
        if life == 2:
            window.blit(life_bar, (615,10))
            window.blit(life_bar, (650,10))
        if life == 1:
            window.blit(life_bar, (650,10))
        
        display.update()
    
    else:
        finish = False
        lost = 0 
        shot = 0 
        life = 3
        num_fire = 0
        rel_time = False
        for m in monsters:
            m.kill()
        for a in asters:
            a.kill()
        for b in bullets:
            b.kill()
        clock.tick(20)
        for i in range(1,4):
            aster = Asteroid('метиорит_meteor2_4.png', randint(80,620), -50, randint(2,5), 50,50)
            asters.add(aster)
        for i in range (1,6):
            monster = Enemy('враг_enemy2_2.png', randint(80,620), -50, randint(1,3), 70, 60)
            monsters.add(monster)
    
    clock.tick(FPS)
