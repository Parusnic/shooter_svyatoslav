#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as get_time





font.init()
def show_text(x, y, text, font_size, text_color):
    font1 = font.SysFont('Arial', font_size)
    caption = font1.render(text, True, text_color)
    window.blit(caption, (x, y))

class Gamesprite(sprite.Sprite):
    def __init__(self,imagename,x,y,speed):
        super().__init__()
        self.image = image.load(imagename)
        self.image = transform.scale(self.image,(65,65))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Player(Gamesprite):
    def __init__(self,imagename,x,y,speed,lives=3):
        super().__init__(imagename,x,y,speed)
        self.last_shoot = 0
        self.lives = lives
        self.image_live = transform.scale(self.image,(30,30))
    def draw_lives(self):
        for i in range(self.lives):
            window.blit(self.image_live,(660-i*40,10))

    def update(self):
        
        get_pressed = key.get_pressed()
        if get_pressed[K_a]:
            self.rect.x -= self.speed
        if get_pressed[K_d]:
            self.rect.x += self.speed
        if get_pressed[K_SPACE]:
            if get_time() - self.last_shoot > .2:
                self.shoot()
                self.last_shoot = get_time()

    def shoot(self):
        new_bullet = Bullet("bullet.png",self.rect.centerx-3,self.rect.y,7)
        bullets.add(new_bullet)

class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(1,635)
            missed.count += 1
            missed.render()


class Asteroid(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(1,635)

class Bullet(Gamesprite):
    def update(self): 
        self.rect.y -= self.speed
    def __init__(self,imagename,x,y,speed):
        super().__init__(imagename,x,y,speed)
        self.image = transform.scale(self.image,(10,30))

class Counter:
    def __init__(self, x, y, font_size, text):
        self.pos = (x,y)
        self.text = text
        self.font_size = font_size
        self.count = 0

    def render(self):
        f = font.SysFont("Arial", self.font_size)
        self.image = f.render(self.text + str(self.count),True,(255,255,255))
    
    def show(self):
        window.blit(self.image, self.pos)
missed = Counter(10,10,20,'количество пропущеных:')
missed.render()
killed = Counter(10,30,20,'количество убитых:')
killed.render()

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monsters.add(Enemy("ufo.png",randint(1,635),0,randint(1,3)))
window = display.set_mode((700,500))
pic = image.load("galaxy.jpg")
pic = transform.scale(pic,(700,500))
asteroids = sprite.Group()
for i in range(3):
    asteroids.add(Asteroid("asteroid.png",randint(1,635),0,randint(1,3)))
game = True
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.03)
player = Player("rocket.png",10,435,3)
font.init()

clock = time.Clock()
finished = False

while game:
    clock.tick(60)
    if finished == False:
        window.blit(pic,(0,0))
        player.update()
        player.reset()
        player.draw_lives()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        missed.show()
        killed.show()
        
        for s in sprite.groupcollide(monsters,bullets,False,True):
            s.rect.y = 0
            s.rect.x = randint(1,635)  
            killed.count += 1
            if killed.count == 10:
                monsters.add(Enemy("ufo.png",randint(1,635),0,randint(1,3)))
                monsters.add(Enemy("ufo.png",randint(1,635),0,randint(1,3)))
            killed.render()
        if killed.count >= 20:
            show_text(300,250,'YOU WIN',50,(255,255,255))
            finished = True
        if player.lives <= 0:
            show_text(300,250,'GAME OVER',50,(255,255,255))
            finished = True
        for a in sprite.spritecollide(player,asteroids,False) + sprite.spritecollide(player,monsters,False) :
            a.rect.y = 0
            a.rect.x = randint(1,635)
            player.lives -= 1 

        


        display.update()
    for e in event.get():
        if e.type == QUIT:
            game = False
   
    