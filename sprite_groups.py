import pygame
import logging
import logging.config


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')


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

# contains all the tower icons
tower_icon_sprites = pygame.sprite.Group()

#contains the current three upgrade icons to show in the dashboard
upgrade_icon_sprites = pygame.sprite.Group()

# the tower icon the user has selected. If this icon is present, it is always positioned at the mouse position
selected_tower_icon_sprite = pygame.sprite.GroupSingle()
