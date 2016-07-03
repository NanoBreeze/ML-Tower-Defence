import colours
import pygame
import path
import abc
import logging
import bullet

logging.basicConfig(level=logging.DEBUG)

BALLON_L1 = 'BALLON_L1'
BALLON_L2 = 'BALLON_L2'
BALLON_L3 = 'BALLON_L3'
BALLON_L4 = 'BALLON_L4'
BALLON_L5 = 'BALLON_L5'

class Ballon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""
    def __init__(self, colour, dimension, path, path_indexer=0) :
        logging.debug('PATH_INDEXER is at' + str(path_indexer))
        super().__init__()

        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.path_index= path_indexer #this is used for iterating which tuple of the path to move to. Very useful with teleportation
        self.rect.centerx = path[self.path_index][0]
        self.rect.centery = path[self.path_index][1]
        self.path = path

    def update(self, bullet_sprites):
        collided_bullets = pygame.sprite.spritecollide(self, bullet_sprites, False)
        if collided_bullets:
            for collided_bullet in collided_bullets:
                if type(collided_bullet) is bullet.StandardBullet:
                    logging.debug('=================== STANDARD BULLET=======================')
                    collided_bullet.handle_ballon_collision()
                    return True  # represents should handle pop
                elif type(collided_bullet) is bullet.ExplosionBullet:
                    logging.debug('=================== EXPLOSION BULLET=======================')
                    #explosion bullet will create more bullets
                    collided_bullet.handle_ballon_collision(bullet_sprites)
                    return True  # represents should handle pop
                elif type(collided_bullet) is bullet.TeleportationBullet:
                    logging.debug('=================== TELEPORTATION BULLET=======================')
                    collided_bullet.handle_ballon_collision()
                    self.teleport()
                    return False

        else:
            self.move()

    def move(self):
        try:
            print('inside the move() method. The path indexer is: ' + str(self.path_index))
            self.rect.centerx = self.path[self.path_index][0]
            self.rect.centery = self.path[self.path_index][1]
            self.path_index += 1
            print('just changed teh move() path_indexer value to 2. It is actually: ' + str(self.path_index))
        except:
            pass


    def teleport(self, back_track_path_indexer=20):
        """Teleports back 20 tuples on the path"""
        logging.debug('inside teleport()')
        if back_track_path_indexer > self.path_index:
            self.path_index = 0
        else:
            self.path_index -= back_track_path_indexer



class BallonL1(Ballon):
   """First, and lowest, level of Ballon"""
   def peel_layer(self):
        logging.debug('inside BallonL1s peel_layer() method')
        return None #there is no layer to return



class BallonL2(Ballon):
    def peel_layer(self):
        logging.debug('inside BallonL2s peel_layer() method')
        return create_ballon(BALLON_L1, self.path, self.path_index)

class BallonL3(Ballon):
    def peel_layer(self):
        logging.debug('inside BallonL3s peel_layer() method')
        return create_ballon(BALLON_L2, self.path, self.path_index)


class BallonL4(Ballon):
    def peel_layer(self):
        logging.debug('inside BallonL4s peel_layer() method')
        return create_ballon(BALLON_L3, self.path, self.path_index)


class BallonL5(Ballon):
    def peel_layer(self):
        logging.debug('inside BallonL5s peel_layer() method. The path index is: ' + str(self.path_index))
        return create_ballon(BALLON_L4, self.path, self.path_index)


class BallonContext(Ballon):
    def __init__(self, current_ballon):
        pygame.sprite.Sprite.__init__(self)
        self.current_ballon = current_ballon

    def update(self, bullet_sprites):
        #if is_handle_pop is true, then it is destroyed. If it is false, then it has moved
        is_handle_pop = self.current_ballon.update(bullet_sprites)
        if is_handle_pop:
            self.handle_pop()

    def handle_pop(self):
        """Allocate money and peel layer"""
        logging.debug('inside BallonContext handle_pop()')
        self.current_ballon = self.current_ballon.peel_layer()
        if self.current_ballon is None:
            self.kill()
        logging.debug('last line of handle_pop()')

    def get_centerX(self):
        return self.current_ballon.rect.centerx

    def get_centerY(self):
        return self.current_ballon.rect.centery




def create_ballon(ballon_type, path, path_indexer=0):
    """Creates appropriate ballon. Used by BallonContext"""
    if ballon_type == BALLON_L1:
        return BallonL1(colours.RED, (30, 30), path, path_indexer)
    elif ballon_type == BALLON_L2:
        return BallonL2(colours.ORANGE, (30, 30), path, path_indexer)
    elif ballon_type == BALLON_L3:
        return BallonL3(colours.YELLOW, (30, 30), path, path_indexer)
    elif ballon_type == BALLON_L4:
        return BallonL4(colours.GREEN, (30, 30), path, path_indexer)
    elif ballon_type == BALLON_L5:
        return BallonL5(colours.BLUE, (30, 30), path, path_indexer)
    else:
        raise NotImplementedError('Not implemented yet!')


def create_ballon_context(ballon_type, path, path_indexer=0):
    """Creates BallonContext objects with the appropriate ballon as the state"""
    if ballon_type == BALLON_L1:
        ballonL1 = BallonL1(colours.RED, (30, 30), path, 0)
        return BallonContext(ballonL1)
    elif ballon_type == BALLON_L2:
        ballonL2 = BallonL2(colours.ORANGE, (30, 30), path, 0)
        return BallonContext(ballonL2)
    elif ballon_type == BALLON_L3:
        ballonL3 = BallonL3(colours.YELLOW, (30, 30), path, 0)
        return BallonContext(ballonL3)
    elif ballon_type == BALLON_L4:
        ballonL4 = BallonL4(colours.GREEN, (30, 30), path, 0)
        return BallonContext(ballonL4)
    elif ballon_type == BALLON_L5:
        ballonL5 = BallonL5(colours.BLUE, (30, 30), path, 0)
        return BallonContext(ballonL5)
    else:
        raise NotImplementedError('Not implemented yet!')