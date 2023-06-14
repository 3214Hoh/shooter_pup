#Создай собственный Шутер!
from pygame import *
from random import randint
#dist
win_width = 700
win_height = 500 

#text
font.init()
font1 = font.SysFont('Arial',80)
win = font1.render('YOU WIN',True, (255,255,255))
lose = font1.render('YOU LOSE',True, (255,0,0))

font2 = font.SysFont('Arial',36)


#mixer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
#fps and time
FPS = 60
clock = time.Clock()
finish = False 
#main window
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')

lost_counter = 0
shutted_enemys = 0
enemys_to_killed = 10 
max_to_lost = 3

#back wind
background = transform.scale(image.load('galaxy.jpg'), (win_width,win_height))
#classes:
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed ):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT]and self.rect.x< win_width -80:
            self.rect.x +=self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,15, 20, 15)
        bullets.add(bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        global lost_counter
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y =0
            self.rect.x = randint(80,win_width-80)
            lost_counter += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed #<<---------------------------
        if self.rect.y < 0:
            self.kill()
#OBJECKT
player = Player('rocket.png',5, win_height-100 ,80,100,15)
enemy=Enemy('ufo.png',5, win_height-100 ,80,100,2)
#bullet= Bullet('bullet.png',5,win_height-100,30,50,12)
###

ufos = sprite.Group()
for i in range (5):
    ufo = Enemy('ufo.png', randint(80,win_width-80), -100,80,50,randint(1,5))
    ufos.add(ufo)


bullets = sprite.Group()

#game circle
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()
    if finish != True:
        window.blit(background,(0,0))
        player.update()
        player.reset()

        ufos.update()
        bullets.update()

        ufos.draw(window)
        bullets.draw(window)
        collides= sprite.groupcollide(bullets,ufos, True,True)
        for ufos in collides:
            shutted_enemys += 1 
            ufo = Enemy('ufo.png', randint(80,win_width-80),80,50,randint(1,5))
            ufos.add(ufo)
        if sprite.spritecollide(player,ufos , False) or lost_counter >= max_to_lost:
            finish = True
            window.blit(lose, (200,200))
        if shutted_enemys >= enemys_to_killed:
            finish = True
            window.blit(win,(200,200))
    
        killed_counter  =  font2.render("Счет"+ str(shutted_enemys), 1, (255,255,255))
        window.blit(killed_counter, (10,20))

        lost_counter2 = font2.render('Пропущенные'+ str(lost_counter), 1, (255,255,255))
        window.blit(lost_counter2, (10,50))
        display.update()
        time.delay(FPS)

