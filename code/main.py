import pygame
from os.path import join
from random import randint,uniform
import time

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
        self.cooldown_duration = 400  

        #mask
        self.mask = pygame.mask.from_surface(self.image)

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
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_time()
            
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
        self.rect.centery -= 1000 * dt

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.orginal_surf = surf
        self.image = self.orginal_surf
        self.rect = self.image.get_frect(center= pos)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 4000 
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(300, 400)
        self.rotation = 0
        self.rotation_speed = randint(40,50)

    def update(self,dt):
        self.rect.center += self.direction* self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.orginal_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center= self.rect.center)

class AnimitedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frames_index += 20 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill() 

def collisons():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)  # Ensure meteors are removed on collision
    if collision_sprites:
        damage_sound.play()
        time.sleep(2)
        running = False

    for lasers in laser_sprites:
        collided_sprite = pygame.sprite.spritecollide(lasers, meteor_sprites, True)
        if collided_sprite:
            lasers.kill()
            AnimitedExplosion(explosion_frame, lasers.rect.midtop, all_sprites)
            explosion_sound.play()

def displayer():
    current_time  = pygame.time.get_ticks() // 100
    text_surface = font.render(str(current_time), True, (240,240,240))
    text_rec = text_surface.get_frect(midbottom= (window_width/2, window_height - 50))
    display_surface.blit(text_surface, text_rec)

    pygame.draw.rect(display_surface, (230,243,230), text_rec, 2, 10)

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
font = pygame.font.Font(join('images','Oxanium-Bold.ttf'), 40)
explosion_frame = [ pygame.image.load(join('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio','laser.wav'))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(join('audio','explosion.wav'))
damage_sound = pygame.mixer.Sound(join('audio','damage.ogg'))
game_sound = pygame.mixer.Sound(join('audio','game_music.wav'))
game_sound.set_volume(0.3)
game_sound.play()

#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
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
            Meteor(meteor_surf, (x,y), [all_sprites, meteor_sprites] )

    #update
    all_sprites.update(dt)
    collisons()

    #draw the game
    display_surface.fill('gray5')
    all_sprites.draw(display_surface)
    displayer()
    pygame.display.update()

pygame.quit()