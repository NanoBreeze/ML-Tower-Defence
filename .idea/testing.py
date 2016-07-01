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
hi = Hi(1, 100, 100, 5)
hey = Hi(1, 100, 100, 5)
hey.rect.x = 125
hey.rect.y = 150
wow = Hi(1, 100, 100, 5)
wow.rect.x = 400
wow.rect.y = 400
all_sprites = pygame.sprite.Group(hi, hey, wow)

hit = pygame.sprite.spritecollide(hi, all_sprites, False)
pygame.sprite.collide_circle()
for i in hit:
    print('hey')

#b1 = ballon.BallonL1((0, 0, 255), DISPLAYSURF, (100, 100), 5)
#backs = pygame.sprite.OrderedUpdates()
#t1 = tower.LinearTower()

while True:
    for event in pygame.event.get():
        if event.type==pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
    all_sprites.update()
    all_sprites.draw(DISPLAYSURF)
    #DISPLAYSURF.blit(t1, (300, 300))

    pygame.display.update()


