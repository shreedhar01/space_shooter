import pygame
from os.path import join
from random import randint

#general setup
pygame.init()
window_width,window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Shooter')
running = True

# plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x,y = 0,0

# importing an image
player_surf = pygame.image.load(join('images','player.png')).convert_alpha()
star_img = pygame.image.load(join('images','star.png')).convert_alpha()
star_pos = [(randint(0,window_width), randint(0,window_height)) for i in range(20)]

while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game
    display_surface.fill('gray5')
    for pos in star_pos:
        display_surface.blit(star_img,pos)
    x += .25
    y += .15
    display_surface.blit(player_surf, (x, y))
    pygame.display.update()


pygame.quit()