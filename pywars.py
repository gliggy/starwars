#!/bin/python3

import pygame
import sys
import fileinput

pygame.init()

# should try finding a good star wars font, but this will do...
font = pygame.font.SysFont('Nimbus Sans Bold', 48, True, False)


try:
    # take txts from first arg
    txts = list(sys.argv[1])
    txts[:] = [''.join(txts[:])]
    index = 0
    for x in txts:
        txts[index] = x.split('\\n')
        index += 1
    print(txts)
except IndexError:
    # take txts from stdin
    txts = list(line.rstrip() for line in fileinput.input())
    index = 0
    for x in txts:
        txts[index] = x.split('\\n')
        index += 1
    print(txts)
    
fps=30
fpsclock=pygame.time.Clock()


surface = pygame.display.set_mode((800,800))

temp_surf_len = 400
temp_surf_width = 400
temp_surf = pygame.Surface((temp_surf_width,temp_surf_len))

pygame.display.set_caption("Star Wars")

White=(255,255,255)
Black=(0,0,0)
p1 = temp_surf_width/2
p2 = temp_surf_len/2
step=5
while True:
    surface.fill(Black)
    temp_surf.fill((0,0,0,255))
    y = 0
    for txt in txts:
        print(txt)
        texty = font.render(txt, 1, (255,255,0))
        # score_write.fill(yellow)
        temp_surf.blit(texty, (0, y))
        y += 40
        if y > temp_surf_len:
            temp_surf_len = y
            temp_surf = pygame.Surface((temp_surf_width,temp_surf_len))

    surface.blit(temp_surf, (p1,p2))

    #pygame.draw.rect(sur_obj, (255,0,0), (p1, p2, 70, 65))
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    key_input = pygame.key.get_pressed()   
    if key_input[pygame.K_LEFT]:
        p1 -= step
    if key_input[pygame.K_UP]:
        p2 -= step
    if key_input[pygame.K_RIGHT]:
        p1 += step
    if key_input[pygame.K_DOWN]:
        p2 += step
    pygame.display.update()
    fpsclock.tick(fps)