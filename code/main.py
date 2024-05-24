import pygame
from os.path import join
from random import randint

#general setup
pygame.init()
window_width,window_height = 1280, 700
display_surface = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Shooter')
running = True

# plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x,y = 0,0

# importing an image
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (window_width/2, window_height/2))
player_dir = 1

star_img = pygame.image.load(join('images','star.png')).convert_alpha()
star_pos = [(randint(0,window_width), randint(0,window_height)) for i in range(20)]

meteor_img = pygame.image.load(join('images','meteor.png')).convert_alpha()
meteor_pos_frec = meteor_img.get_frect(center = (window_width/2, window_height/2))

laser_img = pygame.image.load(join('images','laser.png')).convert_alpha()
laser_pos_frec = laser_img.get_frect(bottomleft = (20, window_height - 20))

while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game
    display_surface.fill('gray5')
    for pos in star_pos:
        display_surface.blit(star_img,pos)

    display_surface.blit(meteor_img, meteor_pos_frec)
    display_surface.blit(laser_img, laser_pos_frec)

    #player movement
    player_rect.right += player_dir * 0.4
    if player_rect.right > window_width or player_rect.left < 0:
        player_dir *= -1
    display_surface.blit(player_surf, player_rect)
    pygame.display.update()


pygame.quit()