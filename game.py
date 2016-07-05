import pygame
import pygame.locals
import sys
import pygame.sprite

import balloon
import tower
import sprite_groups
import colours
import path
import icon
import copy

import logging
import logging.config



logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')





pygame.init()

DISPLAYSURF=pygame.display.set_mode((400,400))
pygame.display.set_caption('ML Tower Defence')

main_path = path.Path()

# linear_tower = tower.create_tower(tower.LINEAR_TOWER, (150, 150), DISPLAYSURF)
# three_sixty_tower = tower.create_tower(tower.THREE_SIXTY_TOWER, (80, 100), DISPLAYSURF)
# teleportation_tower = tower.create_tower(tower.TELEPORTATION_TOWER, (150, 250), DISPLAYSURF)
# explosion_tower = tower.create_tower(tower.EXPLOSION_TOWER, (150, 50), DISPLAYSURF)
# sprite_groups.tower_sprites.add(linear_tower, three_sixty_tower, teleportation_tower, explosion_tower)

b1= balloon.create_balloon_context(balloon.BALLOON_L5, main_path, 0)
sprite_groups.ballon_sprites.add(b1)

linear_tower_icon = icon.create_icon(icon.LINEAR_TOWER_ICON, (300, 100))
three_sixty_tower_icon = icon.create_icon(icon.THREE_SIXTY_TOWER_ICON, (300, 150))
explosion_tower_icon = icon.create_icon(icon.EXPLOSION_TOWER_ICON, (300, 200))
teleportation_tower_icon = icon.create_icon(icon.TELEPORTATION_TOWER_ICON, (300, 250))
sprite_groups.tower_icon_sprites.add(linear_tower_icon,
                                     three_sixty_tower_icon,
                                     explosion_tower_icon,
                                     teleportation_tower_icon)

basic_dashboard = pygame.draw.rect(DISPLAYSURF, colours.GRAY, (0, 300, 400, 100))

fpsClock = pygame.time.Clock()

while True:
    for event in pygame.event.get():

        #left mouse button clicked, if a tower_icon had already been selected, make a tower there
        # otherwise, create a tower icon at the cursor position
        if event.type == pygame.locals.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if sprite_groups.selected_tower_icon_sprite:
                new_tower = tower.create_tower(sprite_groups.selected_tower_icon_sprite.sprite.tower_type, pos, DISPLAYSURF)
                sprite_groups.tower_sprites.add(new_tower)
                sprite_groups.selected_tower_icon_sprite.empty()
            else:
                for tower_icon in sprite_groups.tower_icon_sprites:
                    if tower_icon.rect.collidepoint(pos):
                        tower_icon.on_left_mouse_button_up()
                        duplicate_tower_icon = tower_icon.duplicate()
                        logger.info('type of duplicate_tower is: ' + str(type(duplicate_tower_icon)))
                        sprite_groups.selected_tower_icon_sprite.add(duplicate_tower_icon)

        #right mouse button is clicked. Remove the tower icon currently on the cursor (if it exists)
        elif event.type == pygame.locals.MOUSEBUTTONUP and event.button == 3:
            sprite_groups.selected_tower_icon_sprite.empty()

        elif event.type==pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    #tower_sprites.update()


    DISPLAYSURF.fill(colours.BLACK)
    basic_dashboard = pygame.draw.rect(DISPLAYSURF, colours.GRAY, (0, 300, 400, 100))

    sprite_groups.tower_sprites.update(sprite_groups.ballon_sprites, sprite_groups.bullet_sprites)
    sprite_groups.tower_sprites.draw(DISPLAYSURF)

    sprite_groups.ballon_sprites.update(sprite_groups.bullet_sprites)
    sprite_groups.ballon_sprites.draw(DISPLAYSURF)

    sprite_groups.bullet_sprites.update()
    sprite_groups.bullet_sprites.draw(DISPLAYSURF)

    sprite_groups.tower_icon_sprites.draw(DISPLAYSURF)

    sprite_groups.selected_tower_icon_sprite.update(pygame.mouse.get_pos())
    sprite_groups.selected_tower_icon_sprite.draw(DISPLAYSURF)

    fpsClock.tick(15)
    pygame.display.update()


