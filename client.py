"""
This file contains the screen for the client (attacker), requires a server to be already set up
"""
import pygame
import pygame.locals
import sys
import pygame.sprite
import logging.config
import abc
import colours
import socket

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 400))
pygame.display.set_caption('ML Tower Defence')


sock = None

server_ip_addrses = '127.0.0.1'
server_port = 1060

def begin_game():
    """Display the start screen, if user presses any key, proceed to the game"""

    #connect with server. Assumes the server is already created

    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip_addrses, server_port))
    # print('Client about to send to serve')
    # sock.sendall(b'Hi there, server')
    sock.close()


    logger.info('CLIENT begin_game() called')
    while True:
        for event in pygame.event.get():
            # pressing 's' makes the player the server; 'c' the client; any other key starts in solo mode
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(colours.BLACK)
        start_message = pygame.font.SysFont("freesansbold", 50)
        start_label = start_message.render("Client ", True, (255, 255, 0))

        DISPLAYSURF.blit(start_label, (200, 200))
        pygame.display.update()
