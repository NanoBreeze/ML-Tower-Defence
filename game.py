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
import bank


import logging
import logging.config



logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')





pygame.init()

DISPLAYSURF=pygame.display.set_mode((400,400))
pygame.display.set_caption('ML Tower Defence')

main_path = path.Path()


b1= balloon.create_balloon_context(balloon.BALLOON_L5, main_path, 0)
sprite_groups.ballon_sprites.add(b1)

linear_tower_icon = icon.create_tower_icon(icon.LINEAR_TOWER_ICON, (300, 100))
three_sixty_tower_icon = icon.create_tower_icon(icon.THREE_SIXTY_TOWER_ICON, (300, 150))
explosion_tower_icon = icon.create_tower_icon(icon.EXPLOSION_TOWER_ICON, (300, 200))
teleportation_tower_icon = icon.create_tower_icon(icon.TELEPORTATION_TOWER_ICON, (300, 250))
sprite_groups.tower_icon_sprites.add(linear_tower_icon,
                                     three_sixty_tower_icon,
                                     explosion_tower_icon,
                                     teleportation_tower_icon)

basic_dashboard = pygame.draw.rect(DISPLAYSURF, colours.GRAY, (0, 300, 400, 100))

fpsClock = pygame.time.Clock()

#select font type
bank_balance = pygame.font.SysFont("freesansbold", 15)


while True:
    for event in pygame.event.get():

        #left mouse button clicked, if a tower_icon had already been selected, make a tower there
        # otherwise, if the click is on a tower, show stats of tower.
        # if it was on an icon, create a tower icon at the cursor position
        if event.type == pygame.locals.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if sprite_groups.selected_tower_icon_sprite:
                new_tower = tower.create_tower(sprite_groups.selected_tower_icon_sprite.sprite._tower_type, pos, DISPLAYSURF)
                bank.withdraw(new_tower.cost)
                sprite_groups.tower_sprites.add(new_tower)
                sprite_groups.selected_tower_icon_sprite.empty()
            else:
                is_tower_icon = False #this is bad design will change later, maybe use returns
                for tower_icon in sprite_groups.tower_icon_sprites:
                    if tower_icon.rect.collidepoint(pos):
                        logger.debug('A tower icon is pressed')
                        tower_icon.on_left_mouse_button_up()
                        duplicate_tower_icon = tower_icon.duplicate()
                        sprite_groups.selected_tower_icon_sprite.add(duplicate_tower_icon)
                        sprite_groups.upgrade_icon_sprites.empty()
                        sprite_groups.sell_tower_icon_sprite.empty()
                        is_tower_icon = True
                        break #only one tower at a time, thus after finding it, no need to continue for looping

                is_tower = False
                if is_tower_icon == False: #if a tower icon wasn't pressed, check if a legit tower was pressed
                    for tow in sprite_groups.tower_sprites: #must not be named with tower, will result in name clashes
                        if tow.rect.collidepoint(pos):
                            logger.debug('A legit tower is pressed on')
                            sprite_groups.upgrade_icon_sprites.empty()
                            sprite_groups.sell_tower_icon_sprite.empty()
                            tow.handle_is_clicked(sprite_groups.upgrade_icon_sprites, sprite_groups.sell_tower_icon_sprite)
                            is_tower = True
                            break

                if is_tower == False: #if a legit tower wasn't pressed, check if press was elsewhere
                    if not basic_dashboard.collidepoint(pos):
                        sprite_groups.upgrade_icon_sprites.empty() #empties the icons if no tower is selected and the click isn't in the dashboard
                        sprite_groups.sell_tower_icon_sprite.empty()

                #check if an Upgrade type was pressed
                for upgrade_icon in sprite_groups.upgrade_icon_sprites:
                    if upgrade_icon.rect.collidepoint(pos):
                        upgrade_icon.on_left_mouse_button_up(sprite_groups.upgrade_icon_sprites)
                        break


                #check if the "sell" button was pressed
                if sprite_groups.sell_tower_icon_sprite:
                    if sprite_groups.sell_tower_icon_sprite.sprite.rect.collidepoint(pos):
                        sprite_groups.sell_tower_icon_sprite.sprite.on_left_mouse_button_up()


        #right mouse button is clicked. Remove the tower icon currently on the cursor (if it exists)
        elif event.type == pygame.locals.MOUSEBUTTONUP and event.button == 3:
            sprite_groups.selected_tower_icon_sprite.empty()

        elif event.type==pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    #tower_sprites.update()


    DISPLAYSURF.fill(colours.BLACK)

    #draw dashboard and upgrade sprites
    basic_dashboard = pygame.draw.rect(DISPLAYSURF, colours.GRAY, (0, 300, 400, 100))
    sprite_groups.upgrade_icon_sprites.draw(DISPLAYSURF)
    sprite_groups.sell_tower_icon_sprite.draw(DISPLAYSURF)

    sprite_groups.tower_sprites.update(sprite_groups.ballon_sprites, sprite_groups.bullet_sprites)
    sprite_groups.tower_sprites.draw(DISPLAYSURF)

    sprite_groups.ballon_sprites.update(sprite_groups.bullet_sprites)
    sprite_groups.ballon_sprites.draw(DISPLAYSURF)

    sprite_groups.bullet_sprites.update()
    sprite_groups.bullet_sprites.draw(DISPLAYSURF)

    sprite_groups.tower_icon_sprites.draw(DISPLAYSURF)

    sprite_groups.selected_tower_icon_sprite.update(pygame.mouse.get_pos())
    sprite_groups.selected_tower_icon_sprite.draw(DISPLAYSURF)


    # render text
    label = bank_balance.render("Bank balance: {}".format(bank.balance), True, (255,255,0))
    DISPLAYSURF.blit(label, (300, 50))

    fpsClock.tick(15)
    pygame.display.update()


