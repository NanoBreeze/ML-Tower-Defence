import pygame
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')


class BalloonGroup(pygame.sprite.AbstractGroup):
    """Sprite group for storing Balloons (aka, Balloon objects"""

    def __init__(self):
        super().__init__()

    def draw(self, surface):
        """Modified from Abstract group to draw the Balloon's current_balloon instead of its rect values"""
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.current_balloon_state.image, spr.current_balloon_state.rect)
        self.lostsprites = []


bullet_sprites = pygame.sprite.Group()
tower_sprites = pygame.sprite.Group()
balloon_sprites = BalloonGroup()

tower_icon_sprites = pygame.sprite.Group() # contains all the tower icons

upgrade_icon_sprites = pygame.sprite.Group() #contains the current three upgrade icons to show in the dashboard

sell_tower_icon_sprite = pygame.sprite.GroupSingle()

# the tower icon the user has selected. If this icon is present, it is always positioned at the mouse position
selected_tower_icon_sprite = pygame.sprite.GroupSingle()

