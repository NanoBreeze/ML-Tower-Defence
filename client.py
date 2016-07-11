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
import time
import threading
from collections import namedtuple

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 400))
pygame.display.set_caption('ML Tower Defence')


def dedicated_client_waiting_to_receive_message_function(client, server_stats, formatted_server_messages):
    """Client contains socket, server_stats contains all messages from server, and formatted_server_message formats them into blittable labels"""
    while True:
        server_message = client.wait_to_receive_message_from_server()
        server_stats.add_server_message(server_message)
        formatted_server_messages.format_message(server_message)
        # logger.debug('server_message: {}'.format(server_message))


class Client:
    def __init__(self, server_ip_address='127.0.0.1', server_port=1060):
        self.server_ip_address = server_ip_address
        self.server_port = server_port

        self.sock = None

    def connect_with_server(self):
        """Creates a socket that connects with the server. Assumes the server is already created"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 1060))

    def send_message_to_client(self, message):
        """
        :param message: str, message to send to server
        sends the message to server
        """

        assert self.sock is not None, 'the socket must not be None'

        message = message.encode('ascii')
        self.sock.sendall(message)

    def wait_to_receive_message_from_server(self):
        """Wait to receive 1 message from server. Note: self.sock.recv(...) is a blocking call"""
        assert self.sock is not None, 'the socket must not be None'

        server_message = self.sock.recv(1000)
        logger.debug('received message')
        server_message = server_message.decode('ascii')
        return server_message


class ServerStats:
    """A class that contains all the messages from the server"""

    def __init__(self):
        self.messages_from_server = []

    def add_server_message(self, server_message):
        """Add message to server stat's list as well as call formatted server messages"""

        assert isinstance(server_message, str), 'server_message must be a string'

        self.messages_from_server.append(server_message)

    def remove_server_messaeg(self, server_message):
        try:
            self.messages_from_server.remove(server_message)
        except:
            raise LookupError('the server_message doesnt exist')


class FormattedServerMessages:
    class MessageFontPosition:
        """object storing the message, font, position of label, and id of message"""

        def __init__(self, message, position):
            assert isinstance(message, str), "message must be a string"
            assert isinstance(position, tuple) and len(position) == 2, 'position must be a 2-element tuple'

            self.message = message
            self.font = pygame.font.SysFont("freesansbold", 15)
            self.position = position

    """Contains all the pygame.font.SysFont and label_fon.render(....) associated with every message. This way, the DISPLAYSURF can
     easily display all necessary fonts"""

    def __init__(self):
        self.id = 0

        # font, label (contains the actual rendered object
        self.message_font_positions = {}  # contains info associated with actual renderig

    def format_message(self, message):
        """Store the message, and find correct position, and id into the self.all_message_font ..."""
        self.id += 1

        m = self.MessageFontPosition(message=message, position=(50, self.id * 50))
        self.message_font_positions[self.id] = m

    def get_all_labels(self):
        """
        :return: list of 2-element tuples, first element is label (used with blitting), second is its position.
        Returns all the labels, so they can be blitted onto the screen and their position
        """

        return [(message_font_position.font.render(message_font_position.message, True, (255, 255, 0)),
                 message_font_position.position) \
                for message_font_position in self.message_font_positions.values()]


def begin_game():
    """Display the start screen, if user presses any key, proceed to the game"""

    client = Client()
    client.connect_with_server()

    server_stats = ServerStats()  # contains messages sent from server
    formatted_server_messages = FormattedServerMessages()  # contains the formatted versions of all message, ideally called by serve_stats

    client_waiting_to_receive_message_thread = threading.Thread(target=dedicated_client_waiting_to_receive_message_function,
                                                                args=(client, server_stats, formatted_server_messages),
                                                                name='client_waiting_to_receive_thread')
    client_waiting_to_receive_message_thread.start()

    # formatted_server_messages = FormattedServerMessages()
    # formatted_server_messages.format_message('hello')
    # formatted_server_messages.format_message('world')

    start_message_font = pygame.font.SysFont("freesansbold", 50)
    server_tower_stats_font = pygame.font.SysFont('freesansbold', 15)

    while True:
        for event in pygame.event.get():
            # pressing 's' makes the player the server; 'c' the client; any other key starts in solo mode
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(colours.BLACK)
        start_label = start_message_font.render("Client ", True, (255, 255, 0))

        DISPLAYSURF.blit(start_label, (250, 150))

        for formatted_server_message in formatted_server_messages.get_all_labels():
            DISPLAYSURF.blit(formatted_server_message[0], formatted_server_message[1])

        pygame.display.update()
