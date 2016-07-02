import pygame
import logging

logging.basicConfig(level=logging.DEBUG)

class BallonGroup(pygame.sprite.AbstractGroup):

    def __init__(self):
        super().__init__()

    def draw(self, surface):
        """Modified from Abstract group to draw the BallonContext's currentBallon"""
        logging.debug('Inside BallonGroup draw. START. Length: {}'.format(len(self.sprites())))
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.current_ballon.image, spr.current_ballon.rect)
        self.lostsprites = []




bullet_sprites = pygame.sprite.Group()
tower_sprites = pygame.sprite.Group()
ballon_sprites = BallonGroup()
