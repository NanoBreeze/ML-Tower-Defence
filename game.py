import pygame
import pygame.locals
import sys
import pygame.sprite

import ballon
import tower


class Hi(pygame.sprite.Sprite):

    def __init__(self, color, width, height, something):
        super().__init__()
        self.image = pygame.image.load('images/cat.png')

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 150

    def update(self):
        #print('update called')
        pass

pygame.init()

DISPLAYSURF=pygame.display.set_mode((400,300))
pygame.display.set_caption('HelloWorld!')



t1 = tower.LinearTower((50, 30))
b1 = ballon.BallonL1((0, 0, 255), (150, 200), 1, 30, 30)

tower_sprites = pygame.sprite.Group(t1)
#all_ballons = pygame.sprite.Group(b1)
ballon_sprites = pygame.sprite.Group(b1)

#b1 = ballon.BallonL1((0, 0, 255), DISPLAYSURF, (100, 100), 5)
#backs = pygame.sprite.OrderedUpdates()
#t1 = tower.LinearTower()

while True:
    for event in pygame.event.get():
        if event.type==pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
    #tower_sprites.update()
    tower_sprites.draw(DISPLAYSURF)
    ballon_sprites.draw(DISPLAYSURF)
    #DISPLAYSURF.blit(t1, (300, 300))

    pygame.display.update()


