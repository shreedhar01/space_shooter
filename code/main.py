import pygame
from os.path import join
from random import randint

#general setup
pygame.init()
window_width,window_height = 1280, 700
display_surface = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# plain surface
# surf = pygame.Surface((100,200))
# surf.fill('orange')
# x,y = 0,0

# importing an image
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
player_pos_frect = player_surf.get_frect(center = (window_width/2, window_height/2))
player_dir = pygame.math.Vector2()
player_speed = 200

star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
star_pos = [(randint(0,window_width), randint(0,window_height)) for i in range(20)]

meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
meteor_pos_frec = meteor_surf.get_frect(center = (window_width/2, window_height/2))

laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
laser_pos_frec = laser_surf.get_frect(bottomleft = (20, window_height - 20))
laser_dir = pygame.math.Vector2()
laser_speed = 500

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     print(event.key == pygame.K_DOWN)
        # if event.type == pygame.MOUSEMOTION:
        #     player_pos_frect.center = event.pos

    #input
    keys = pygame.key.get_pressed()
    player_dir.x = int(keys[pygame.K_RIGHT]) - keys[pygame.K_LEFT]
    player_dir.y = int(keys[pygame.K_DOWN]) - keys[pygame.K_UP]
    player_dir = player_dir.normalize() if player_dir else player_dir

    recent_key = pygame.key.get_just_pressed()
    if recent_key[pygame.K_SPACE]:
        laser_dir.y -= 1
    else:
        laser_dir.y = 0


    #what happening can be explain by below code
    # if keys[pygame.K_RIGHT]:
    #     player_dir.x = 1
    # else:
    #     player_dir.x = 0
    # if keys[pygame.K_LEFT]:
    #     player_dir.x = -1
    # else:
    #     player_dir.y = 0
     
    player_pos_frect.center += player_dir * player_speed * dt #main movement 
    laser_pos_frec.center += laser_dir * laser_speed * dt

    #draw the game
    display_surface.fill('gray5')
    for pos in star_pos:
        display_surface.blit(star_surf,pos)

    display_surface.blit(meteor_surf, meteor_pos_frec)
    display_surface.blit(laser_surf, laser_pos_frec)

    #player movement
    # if player_pos_frect.bottom > window_height or player_pos_frect.top < 0:
    #     player_dir.y *= -1
    # if player_pos_frect.right > window_width or player_pos_frect.left < 0:
    #     player_dir.x *= -1

    display_surface.blit(player_surf, player_pos_frect)
    pygame.display.update()


pygame.quit()