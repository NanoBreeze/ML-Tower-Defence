import colours
import pygame
import path
import abc
import logging

logging.basicConfig(level=logging.DEBUG)

BALLON_L1 = 'BALLON_L1'
BALLON_L2 = 'BALLON_L2'
BALLON_L3 = 'BALLON_L3'

class Ballon(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    """Base class for all Ballons, which are the enemies"""



    def __init__(self, colour, dimension, path) :

        super().__init__()

        self.image = pygame.Surface([dimension[0], dimension[1]])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = path[0][0]
        self.rect.centery = path[0][1]
        self.counter = 1 #this is used for iterating witht he path. This is a bad idea, might need a generator instead
        self.path = path



    def update(self, bullet_sprites):
        if pygame.sprite.spritecollide(self, bullet_sprites, False):
            #self.kill()
            self.handle_pop()
        else:
            self.move()

    @abc.abstractmethod
    def handle_pop(self):
        """This method is called when the ballon is popped"""
        pass

    def move(self):
        try:
            self.rect.centerx = self.path[self.counter][0]
            self.rect.centery = self.path[self.counter][1]
            self.counter += 1
        except:
            pass



class BallonL1(Ballon):
   """First, and lowest, level of Ballon"""

   def handle_pop(self):
       logging.debug('inside BallonL1s hanlde_pop()')

   def update(self, bullet_sprites):
       if pygame.sprite.spritecollide(self, bullet_sprites, True):
           # self.kill()
           return True  # represents should handle pop
       else:
           self.move()

   def peel_layer(self):
        logging.debug('inside BallonL1s peel_layer() method')
        return None #there is no layer to return

class BallonL2(Ballon):

    def handle_pop(self):
        logging.debug('inside BallonL2s hanlde_pop()')

    def peel_layer(self):
        logging.debug('inside BallonL2s peel_layer() method')
        self.path = self.path[self.counter:]
        return create_ballon(BALLON_L1, self.path)

    def update(self, bullet_sprites):
        if pygame.sprite.spritecollide(self, bullet_sprites, True): #setting this to True might be against decoupling
            # self.kill()
            return True #represents should handle pop
        else:
            self.move()



class BallonContext(Ballon):
    def __init__(self, current_ballon):
        pygame.sprite.Sprite.__init__(self)
        self.current_ballon = current_ballon

    def update(self, bullet_sprites):
        is_handle_pop = self.current_ballon.update(bullet_sprites)
        if (is_handle_pop):
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





def create_ballon(ballon_type, path):
    if ballon_type == BALLON_L1:
        return BallonL1(colours.RED, (30, 30), path)

    elif ballon_type == BALLON_L2:
        return BallonL2(colours.ORANGE, (30, 30), path)

    else:
        raise NotImplementedError('Not implemented yet!')

def create_ballon_context(ballon_type, path):
    if ballon_type == BALLON_L1:
        ballonL1 = BallonL1(colours.RED, (30, 30), path)
        return BallonContext(ballonL1)

    elif ballon_type == BALLON_L2:
        ballonL2 = BallonL2(colours.ORANGE, (30, 30), path)
        return BallonContext(ballonL2)

    else:
        raise NotImplementedError('Not implemented yet!')