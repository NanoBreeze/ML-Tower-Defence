import pygame
import pygame.locals
import sys
import pygame.sprite
import logging.config
import abc

import tower
import sprite_groups
import colours
import icon
import bank
import life_point
import level
import game_utility

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 400))
pygame.display.set_caption('ML Tower Defence')
fpsClock = pygame.time.Clock()


def show_start_screen():
    """Display the start screen, if user presses any key, proceed to the game"""
    while True:
        if pygame.event.get(pygame.locals.KEYUP):
            return
        DISPLAYSURF.fill(colours.BLACK)
        start_message = pygame.font.SysFont("freesansbold", 50)
        start_label = start_message.render("Start game", True, (255, 255, 0))

        DISPLAYSURF.blit(start_label, (200, 200))
        pygame.display.update()


def show_lose_screen():
    """Display the start screen, if user presses any key, proceed to the game"""
    while True:
        if pygame.event.get(pygame.locals.KEYUP):
            return
        DISPLAYSURF.fill(colours.BLACK)
        start_message = pygame.font.SysFont("freesansbold", 50)
        start_label = start_message.render("Good try", True, (255, 255, 0))

        DISPLAYSURF.blit(start_label, (200, 200))
        pygame.display.update()

def show_win_screen():
    win_message_setup = pygame.font.SysFont("freesansbold", 15)
    win_message_label = win_message_setup.render("Congratulations! You won!", True, colours.GREEN)

    while True:
        DISPLAYSURF.fill(colours.WHITE)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.blit(win_message_label, (200, 200))
        pygame.display.update()


def player_has_completed_level(current_level):
    """returns whether the player has successfully completed the level"""
    # logger.info('the value of check if more ballons is: ' + str(current_level.next_balloon_exists()))
    # logger.info('the sprite group is: ' + str(sprite_groups.balloon_sprites))
    if (current_level.next_balloon_exists() == False) and len(sprite_groups.balloon_sprites) == 0:
        return True
    return False


class LeftMouseClickHandler(metaclass=abc.ABCMeta):
    def __init__(self, next_handler):
        """If this handler is unable to handle the mouse click, call the next handler to do it"""
        assert isinstance(next_handler,
                          LeftMouseClickHandler) or next_handler is None, 'next_handler must be a LeftMouseClickHandler type or None'

        self.next_handler = next_handler

    def handle_click(self, mouse_position):
        """Wrapper for handling click, contains conditional for letting next handler try"""
        is_click_handled = self.try_handle_click(mouse_position)

        assert is_click_handled is True or is_click_handled is False, 'is_handled must be either true or false'

        if is_click_handled is False:
            self.next_handler.handle_click(mouse_position)

    @abc.abstractmethod
    def try_handle_click(self, mouse_position):
        """Each class tries to handle the click"""


class TowerIconClickHandler(LeftMouseClickHandler):
    def try_handle_click(self, mouse_position):
        # logger.debug('towerIconCLickHandler')
        for tower_icon in sprite_groups.tower_icon_sprites:
            if tower_icon.rect.collidepoint(mouse_position):
                # logger.debug('towerIconClickHandler collided')
                duplicate_tower_icon = tower_icon.on_click()
                sprite_groups.selected_tower_icon_sprite.empty()
                sprite_groups.selected_tower_icon_sprite.add(duplicate_tower_icon)
                return True
        return False


class TowerClickHandler(LeftMouseClickHandler):
    def try_handle_click(self, mouse_position):
        # logger.debug('towerCLickHandler')
        for tow in sprite_groups.tower_sprites:  # must not be named with tower, will result in name clashes
            if tow.rect.collidepoint(mouse_position):
                tow.on_click(sprite_groups.upgrade_icon_sprites,
                             sprite_groups.sell_tower_icon_sprite)  # will clear the sprite groups before adding icons
                return True
        return False


class UpgradeIconClickHandler(LeftMouseClickHandler):
    def try_handle_click(self, mouse_position):
        # logger.debug('UpgradeIconClickHandler')
        for upgrade_icon in sprite_groups.upgrade_icon_sprites:
            if upgrade_icon.rect.collidepoint(mouse_position):
                upgrade_icon.on_click(sprite_groups.upgrade_icon_sprites)
                return True
        return False


class SellTowerIconClickHandler(LeftMouseClickHandler):
    def try_handle_click(self, mouse_position):
        # logger.debug('SellTowerIconClickHndler')
        if sprite_groups.sell_tower_icon_sprite:
            if sprite_groups.sell_tower_icon_sprite.sprite.rect.collidepoint(mouse_position):
                sprite_groups.sell_tower_icon_sprite.sprite.on_click()
                sprite_groups.sell_tower_icon_sprite.empty()
                sprite_groups.upgrade_icon_sprites.empty()
                return True
        return False


class CreateNewTowerClickHandler(LeftMouseClickHandler):
    def try_handle_click(self, mouse_position):
        # logger.debug('CreateNewTowerClickHandler')
        if sprite_groups.selected_tower_icon_sprite:
            new_tower = tower.create_tower(sprite_groups.selected_tower_icon_sprite.sprite._tower_type, mouse_position,
                                           DISPLAYSURF)
            #make sure player has enough money to make this tower
            if bank.balance >= new_tower.buy_price:
                bank.withdraw(new_tower.buy_price)
                sprite_groups.tower_sprites.add(new_tower)
            sprite_groups.selected_tower_icon_sprite.empty()
            return True
        return False


class NullClickHandler(LeftMouseClickHandler):
    def try_handle_click(self, mouse_position):
        # logger.debug('NullClickHandler')
        # do nothing
        return True


def handle_left_mouse_click(tower_icon_click_handler, mouse_position):
    tower_icon_click_handler.handle_click(mouse_position)



def begin_game():
    # setup
    sprite_groups.tower_icon_sprites.add(icon.create_tower_icon(icon.LINEAR_TOWER_ICON, (300, 100)),
                                         icon.create_tower_icon(icon.THREE_SIXTY_TOWER_ICON, (300, 150)),
                                         icon.create_tower_icon(icon.EXPLOSION_TOWER_ICON, (300, 200)),
                                         icon.create_tower_icon(icon.TELEPORTATION_TOWER_ICON, (300, 250)))

    basic_dashboard = pygame.draw.rect(DISPLAYSURF, colours.GRAY, (0, 300, 400, 100))

    # select font type
    bank_balance_font = game_utility.set_bank_balance_font()
    life_point_font = game_utility.set_life_point_font()

    levels = [level.Level1(),
              level.Level2(),
              level.Level3()]  # game_utility.create_game_levels()
    current_level = levels.pop(0)

    make_new_balloon_countdown = 10  # called every frame and dictates when to make new balloon

    # create left button click event handlers
    null_click_handler = NullClickHandler(None)
    create_new_tower_click_handler = CreateNewTowerClickHandler(null_click_handler)
    sell_tower_icon_click_handler = SellTowerIconClickHandler(create_new_tower_click_handler)
    upgrade_icon_click_handler = UpgradeIconClickHandler(sell_tower_icon_click_handler)
    tower_click_handler = TowerClickHandler(upgrade_icon_click_handler)
    tower_icon_click_handler = TowerIconClickHandler(tower_click_handler)

    while True:

        # if player finished this level and there are other levels remaining, start them, otherwise, proceed to "Win screen"
        if player_has_completed_level(current_level):
            if levels:
                current_level = levels.pop(0)
            else:
                return show_win_screen

        #check if the player still has life points. If not, player lost
        if life_point.life_balance <= 0:
            return show_lose_screen

        # if it's time to make a new balloon and the next balloon exists, then add that balloon to the balloon_sprites and restart countdown. If it doesn't exist, don't add it
        # if it isn't time to make a new balloon, decrement countdown
        if make_new_balloon_countdown == 0:
            if current_level.next_balloon_exists():
                sprite_groups.balloon_sprites.add(current_level.get_next_balloon())
            make_new_balloon_countdown = 10
        else:
            make_new_balloon_countdown -= 1

        # handle events
        for event in pygame.event.get():

            '''Left mouse button clicked
            1. If clicked on tower icon: the mouse cursor will contain an identical tower icon, set a flag to indicate that a tower
            icon had been selected so that the next mouse click would make that tower
            2. If clicked on tower icon, show sell icon and upgrade icon
            3. If clicked on upgrade icon, notify the upgrade icon
            4. If clicked on sell tower icon, notify the sell tower icon
            5. Anywhere else
                a) if the flag to indicate to create a new tower had been set (user had clicked on a tower icon), create new tower there, and withdraw from bank
                b) nothing happens
            '''

            if event.type == pygame.locals.MOUSEBUTTONUP and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                handle_left_mouse_click(tower_icon_click_handler, mouse_position)  # start of chain of responsibility.

            # right mouse button is clicked. Remove the tower icon currently on the cursor (if it exists)
            elif event.type == pygame.locals.MOUSEBUTTONUP and event.button == 3:
                sprite_groups.selected_tower_icon_sprite.empty()
                sprite_groups.sell_tower_icon_sprite.empty()
                sprite_groups.upgrade_icon_sprites.empty()

            elif event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(colours.BLACK)

        # draw dashboard and upgrade sprites
        pygame.draw.rect(DISPLAYSURF, colours.GRAY, (0, 300, 400, 100))  # draw dashboard
        sprite_groups.tower_sprites.update(sprite_groups.balloon_sprites, sprite_groups.bullet_sprites)
        sprite_groups.balloon_sprites.update(sprite_groups.bullet_sprites)
        sprite_groups.bullet_sprites.update()
        sprite_groups.selected_tower_icon_sprite.update(pygame.mouse.get_pos())

        for sprite_group in sprite_groups.all_sprites:
            sprite_group.draw(DISPLAYSURF)



        # render text
        bank_balance_label = bank_balance_font.render("Bank balance: {}".format(bank.balance), True, (255, 255, 0))
        DISPLAYSURF.blit(bank_balance_label, (300, 50))

        life_balance_label = life_point_font.render("Life points: {}".format(life_point.life_balance), True, (255, 255, 0))
        DISPLAYSURF.blit(life_balance_label, (300, 30))

        fpsClock.tick(15)
        pygame.display.update()


if __name__ == '__main__':
    show_start_screen()
    show_win_or_lose_screen = begin_game()
    show_win_or_lose_screen()
