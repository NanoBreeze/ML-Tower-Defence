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

linear_tower = tower.create_tower(tower.LINEAR_TOWER, (150, 150), DISPLAYSURF)
three_sixty_tower = tower.create_tower(tower.THREE_SIXTY_TOWER, (80, 100), DISPLAYSURF)
teleportation_tower = tower.create_tower(tower.TELEPORTATION_TOWER, (150, 150), DISPLAYSURF)

b1= ballon.create_ballon_context(ballon.BALLON_L5, main_path, 0)
assert type(b1) is ballon.BallonContext, 'b1 is not a BallonContext'

sprite_groups.tower_sprites.add(linear_tower, three_sixty_tower, teleportation_tower)

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


