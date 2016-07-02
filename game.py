import pygame
import pygame.locals
import sys
import pygame.sprite

import ballon
import tower
import sprite_groups
import colours
import path
import logging

logging.basicConfig(level=logging.DEBUG)





pygame.init()

DISPLAYSURF=pygame.display.set_mode((400,300))
pygame.display.set_caption('ML Tower Defence')

main_path = path.Path()

t1 = tower.create_tower(tower.LINEAR_TOWER, DISPLAYSURF)
b1= ballon.create_ballon_context(ballon.BALLON_L2, main_path)
assert type(b1) is ballon.BallonContext, 'b1 is not a BallonContext'

sprite_groups.tower_sprites.add(t1)

sprite_groups.ballon_sprites.add(b1)



fpsClock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type==pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    #tower_sprites.update()
    DISPLAYSURF.fill(colours.BLACK)
    sprite_groups.tower_sprites.update(sprite_groups.ballon_sprites, sprite_groups.bullet_sprites)
    sprite_groups.tower_sprites.draw(DISPLAYSURF)

    sprite_groups.ballon_sprites.update(sprite_groups.bullet_sprites)
    sprite_groups.ballon_sprites.draw(DISPLAYSURF)

    sprite_groups.bullet_sprites.update()
    sprite_groups.bullet_sprites.draw(DISPLAYSURF)


    fpsClock.tick(15)
    pygame.display.update()


