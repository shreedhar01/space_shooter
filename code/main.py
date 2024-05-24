import pygame
from os.path import join
from random import randint,uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (window_width/2, window_height/2))
        self.direction = pygame.math.Vector2()
        self.speed = 200

        #cooldown time -> leaser
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 40

    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - keys[pygame.K_LEFT]
        self.direction.y = int(keys[pygame.K_DOWN]) - keys[pygame.K_UP]
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_key = pygame.key.get_just_pressed()
        if recent_key[pygame.K_SPACE] and self.can_shoot:
            laser = Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()  

        self.laser_time()

        # if keys[pygame.K_SPACE] and self.can_shoot:
        #     laser = Laser(laser_surf, self.rect.midtop, all_sprites)
        #     self.can_shoot = False
        #     self.laser_shoot_time = pygame.time.get_ticks()
            
class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, star_surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (randint(0,window_width),randint(0,window_height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center= pos)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 2500 
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(300, 400)

    def update(self,dt):
        self.rect.center += self.direction* self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()

#general setup
pygame.init()
window_width,window_height = 1280, 700
display_surface = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

#import surf
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()

#sprites
all_sprites = pygame.sprite.Group()
for i in range(20):
    star = Stars(all_sprites,star_surf)
player = Player(all_sprites)

#costume time -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, window_width), randint(-100, -50)
            Meteor(meteor_surf, (x,y), all_sprites )

    all_sprites.update(dt)

    #draw the game
    display_surface.fill('gray5')
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()