import colours
import pygame
import path
import abc
import logging
import logging.config
import bullet
import bank



logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleLogger')

BALLOON_L1 = 'BALLOON_L1'
BALLOON_L2 = 'BALLOON_L2'
BALLOON_L3 = 'BALLOON_L3'
BALLOON_L4 = 'BALLOON_L4'
BALLOON_L5 = 'BALLOON_L5'


class Balloon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""

    def __init__(self, colour, dimension, path, bounty=20, path_indexer=0):
        logger.debug('PATH_INDEXER is at' + str(path_indexer))
        super().__init__()

        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.path_index = path_indexer  # this is used for iterating which tuple of the path to move to. Very useful with teleportation
        self.rect.centerx = path[self.path_index][0]
        self.rect.centery = path[self.path_index][1]
        self.path = path
        self.bounty = bounty

    def update(self, bullet_sprites):
        collided_bullets = pygame.sprite.spritecollide(self, bullet_sprites, False)
        logger.critical(str(collided_bullets))
        if collided_bullets:
            for collided_bullet in collided_bullets:
                if isinstance(collided_bullet, bullet.StandardBullet):
                    logger.debug('=================== STANDARD BULLET=======================')
                    collided_bullet.handle_ballon_collision()
                    logger.warn('inside the standard bullet')
                    return True  # represents should handle pop
                elif isinstance(collided_bullet, bullet.ExplosionBullet):
                    logger.debug('=================== EXPLOSION BULLET=======================')
                    # explosion bullet will create more bullets
                    collided_bullet.handle_ballon_collision(bullet_sprites)
                    logger.warn('inside the explosion bullet')
                    return True  # represents should handle pop
                elif isinstance(collided_bullet, bullet.TeleportationBullet):
                    logger.debug('=================== TELEPORTATION BULLET=======================')
                    collided_bullet.handle_ballon_collision()
                    self.teleport()
                    return False  # represents don't hanlde pop. This ballon is being teleported
                raise NotImplementedError('the collided_bullet type is not allowed!')
        else:
            self.move()

    def move(self):
        if self.path_index >= len(self.path) -1:
            raise NotImplementedError('if balloon reaches end. Not sure what happens')
        else:
            logger.debug('inside the move() method. The path indexer is: ' + str(self.path_index))
            self.rect.centerx = self.path[self.path_index][0]
            self.rect.centery = self.path[self.path_index][1]
            self.path_index += 1
            logger.debug('just changed teh move() path_indexer value to 2. It is actually: ' + str(self.path_index))


    def teleport(self, back_track_path_indexer=20):
        """Teleports back 20 tuples on the path"""
        logger.debug('inside teleport()')
        if back_track_path_indexer > self.path_index:
            self.path_index = 0
        else:
            self.path_index -= back_track_path_indexer


class BalloonL1(Balloon):
    """First, and lowest, level of Ballon"""
    def peel_layer(self):
        logger.debug('inside BallonL1s peel_layer() method')
        return None  # there is no layer to return


class BalloonL2(Balloon):
    def peel_layer(self):
        logger.debug('inside BallonL2s peel_layer() method')
        return create_balloon(BALLOON_L1, self.path, self.path_index)


class BalloonL3(Balloon):
    def peel_layer(self):
        logger.debug('inside BallonL3s peel_layer() method')
        return create_balloon(BALLOON_L2, self.path, self.path_index)


class BalloonL4(Balloon):
    def peel_layer(self):
        logger.debug('inside BallonL4s peel_layer() method')
        return create_balloon(BALLOON_L3, self.path, self.path_index)


class BalloonL5(Balloon):
    def peel_layer(self):
        logger.debug('inside BallonL5s peel_layer() method. The path index is: ' + str(self.path_index))
        return create_balloon(BALLOON_L4, self.path, self.path_index)

class BalloonContext(Balloon):
    def __init__(self, current_ballon):
        pygame.sprite.Sprite.__init__(self)
        self.current_ballon = current_ballon

    def update(self, bullet_sprites):
        # if is_handle_pop is true, then it is destroyed. If it is false, then it has moved
        is_handle_pop = self.current_ballon.update(bullet_sprites)
        if is_handle_pop:
            self.handle_pop()

    def handle_pop(self):
        """Allocate money and peel layer"""
        logger.debug('inside BallonContext handle_pop()')
        bank.deposit(self.current_ballon.bounty)
        logger.warn(str(self.current_ballon.bounty))
        self.current_ballon = self.current_ballon.peel_layer()
        if self.current_ballon is None:
            self.kill()

    def get_centerX(self):
        return self.current_ballon.rect.centerx

    def get_centerY(self):
        return self.current_ballon.rect.centery


def create_balloon(balloon_type, path, path_indexer=0):
    """Creates appropriate ballon. Used by BallonContext"""
    if balloon_type == BALLOON_L1:
        return BalloonL1(colours.RED, (30, 30), path, 10, path_indexer)
    elif balloon_type == BALLOON_L2:
        return BalloonL2(colours.ORANGE, (30, 30), path, 20, path_indexer)
    elif balloon_type == BALLOON_L3:
        return BalloonL3(colours.YELLOW, (30, 30), path, 30, path_indexer)
    elif balloon_type == BALLOON_L4:
        return BalloonL4(colours.GREEN, (30, 30), path, 40, path_indexer)
    elif balloon_type == BALLOON_L5:
        return BalloonL5(colours.BLUE, (30, 30), path, 50, path_indexer)
    else:
        raise NotImplementedError('Not implemented yet!')


def create_balloon_context(balloon_type, path, path_indexer=0):
    """Creates BallonContext objects with the appropriate ballon as the state"""
    balloon = create_balloon(balloon_type, path, path_indexer)
    return BalloonContext(balloon)
