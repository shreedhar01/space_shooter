import pygame
from os.path import join
from random import randint

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

#general setup
pygame.init()
window_width,window_height = 1280, 700
display_surface = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
for i in range(20):
    star = Stars(all_sprites,star_surf)
player = Player(all_sprites)

meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
meteor_pos_frec = meteor_surf.get_frect(center = (window_width/2, window_height/2))

laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()

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
            pass

    all_sprites.update(dt)

    #draw the game
    display_surface.fill('gray5')
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()