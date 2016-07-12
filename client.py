"""
This file contains the screen for the client (attacker), requires a server to be already set up
"""
import pygame
import pygame.locals
import sys
import pygame.sprite
import logging.config
import threading
from collections import defaultdict

import colours
import socket

import plotting_and_ML

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 400))
pygame.display.set_caption('ML Tower Defence')
fpsClock = pygame.time.Clock()

def sanitize_message_and_add_to_stats(server_message, server_stats):
    """
    Interprets the server message correctly in order to provide the correct values to ServerStats
    Possible values:
    L=18.
    B=625.
    T=499987854.t=LINEAR_TOWER.s=2.r=70.p=1.
    T=499984651.s=2.
    T=499984651.r=2.
    T=499984651.p=2.
    T=499984651.c=2.
    T=499984651.
    Note: T represents tower. All values are delimited by .
    """
    try:  # adding try because if server presses button quickly, sometimes many delimited values come
        if server_message[0] == 'L':  # this is lifepoints

            lifepoint = server_message[2:-1]
            server_stats.lifepoint = int(lifepoint)

        elif server_message[0] == 'B':  # this is the bank balance
            possible_bank_balances = [c for c in server_message.split('.') if
                                      c]  # for error checking sometimes too many B's come in, eg, B=12.B=15.B=17. will overflow
            for bank_balance in possible_bank_balances:
                bank_balance = server_message[2:-1]
                logger.debug('the bank balance is ' + bank_balance)
                server_stats.bank_balance = int(bank_balance)

        elif server_message[0] == 'T':  # this is a tower
            delimited_values = [c for c in server_message.split('.') if c]  # removes last empty string

            logger.debug('tower:' + str(delimited_values))

            tower_id = delimited_values[0][2:]
            if len(delimited_values) == 1:  # this tower has been deleted
                server_stats.remove_tower_stat(tower_id)

            elif len(delimited_values) == 2:  # this tower has been upgraded

                updated_value = delimited_values[1][2:]

                if delimited_values[1][0] == 's':  # speed update
                    server_stats.update_tower_stat_speed(tower_id, updated_value)
                elif delimited_values[1][0] == 'r':  # radius update
                    server_stats.update_tower_stat_radius(tower_id, updated_value)
                elif delimited_values[1][0] == 'p':  # pop_power update
                    server_stats.update_tower_stat_pop_power(tower_id, updated_value)
                elif delimited_values[1][0] == 'c':  # pop_count update
                    server_stats.update_tower_stat_pop_count(tower_id, updated_value)
                else:
                    raise NotImplementedError('the specified letter is not valid')

            elif len(delimited_values) == 7:  # a new tower is created
                tower_type = delimited_values[1][2:]
                speed_update_value = delimited_values[2][2:]
                radius_update_value = delimited_values[3][2:]
                pop_power_update_value = delimited_values[4][2:]
                x_pos = delimited_values[5][2:]
                y_pos = delimited_values[6][2:]

                server_stats.add_tower_stat(tower_id, tower_type, speed_update_value, radius_update_value, pop_power_update_value,
                                            x_pos, y_pos)

                # update the matplotlib with new vaues (NOTE: not displaying graph here because matplotlib can only be shown on the main thread)
                logger.debug('about to call plotting from client')
                plotting_and_ML.update_plot_with_new_tower(int(x_pos), int(y_pos))

            else:
                raise NotImplementedError('the tower creation pattern (number of delimiters) isnt correct')
    except:
        logger.critical("an error occured in sanitization and was passed. The server message was {}".format(server_message))


def dedicated_handle_receiving_messages(client, server_stats, formatted_server_stats):
    """Client contains socket, server_stats contains all messages from server, and formatted_server_message formats them into blittable labels"""
    while True:
        server_message = client.wait_to_receive_message_from_server()
        sanitize_message_and_add_to_stats(server_message, server_stats)
        formatted_server_stats.internally_make_fonts(server_stats)


def dedicated_sending_messages(client, balloon_number):
    client.send_message(balloon_number)


class Client:
    def __init__(self, server_ip_address='127.0.0.1', server_port=1060):
        self.server_ip_address = server_ip_address
        self.server_port = server_port

        self.sock = None

    def connect_with_server(self):
        """Creates a socket that connects with the server. Assumes the server is already created"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 1060))

    def send_message(self, message):
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

    def close_client(self):
        self.sock.close()


class ServerStats:
    """A class that contains all the messages from the server
    the tower-related messages are placed in a dictionary of the form, "tower_id" : (type, speed, radius, pop_power)
    lifepoints and bank balances are in their own variables
    """

    class TowerStat:
        "Stores the stats related to a tower, id, tower_type, speed, radius, pop_power"

        def __init__(self, tower_id=-1, tower_type='Unavailable', speed=-1, radius=-1, pop_power=-1, x_pos=-1, y_pos=-1):
            self.tower_id = tower_id
            self.tower_type = tower_type
            self.speed = speed
            self.radius = radius
            self.pop_power = pop_power
            self.pop_count = 0
            self.x_pos = x_pos
            self.y_pos = y_pos

    def __init__(self):
        self.tower_stats = defaultdict(lambda: self.TowerStat())

        self.lifepoint = -1
        self.bank_balance = -1

    def add_tower_stat(self, tower_id, tower_type, speed, radius, pop_power, x_pos, y_pos):
        "Save the stats related to the tower to the self.tower_stats dictionary"
        self.tower_stats[tower_id] = self.TowerStat(tower_id, tower_type, speed, radius, pop_power, x_pos, y_pos)

    def update_tower_stat_speed(self, tower_id, speed):
        self.tower_stats[tower_id].speed = speed

    def update_tower_stat_radius(self, tower_id, radius):
        self.tower_stats[tower_id].radius = radius

    def update_tower_stat_pop_power(self, tower_id, pop_power):
        self.tower_stats[tower_id].pop_power = pop_power

    def update_tower_stat_pop_count(self, tower_id, pop_count):
        self.tower_stats[tower_id].pop_count = pop_count
        # plotting_and_ML.update_plot_with_pop_count(int(self.tower_stats[tower_id].x_pos),
        #                                            int(self.tower_stats[tower_id].y_pos),
        #                                            pop_count)

    def remove_tower_stat(self, tower_id):
        del self.tower_stats[tower_id]
        logger.debug('removed tower. the length of tower_stats is {}'.format(len(self.tower_stats)))


class FormattedServerMessages:
    lifepoint_label = None
    bank_balance_label = None

    tower_stats_labels = None

    def internally_make_fonts(self, server_stats):
        """Creates a list of font associated with each stat stored in server_stats"""
        self.lifepoint_label = pygame.font.SysFont("freesansbold", 15).render('Lifepoint: {}'.format(server_stats.lifepoint),
                                                                              True,
                                                                              (255, 255, 0))

        self.bank_balance_label = pygame.font.SysFont("freesansbold", 15).render(
            'Bank balance: {}'.format(server_stats.bank_balance), True, (255, 255, 0))

        self.tower_stats_labels = [
            pygame.font.SysFont("freesansbold", 15).render(
                '{0} - Spd: {1} - Rad: {2} - Pop pow: {3} - Pop count: {4} - x: {5} - y {6}'
                    .format(tower_stat.tower_type, tower_stat.speed, tower_stat.radius,
                            tower_stat.pop_power, tower_stat.pop_count, tower_stat.x_pos, tower_stat.y_pos), True,
                (255, 255, 0))
            for tower_stat in server_stats.tower_stats.values()
            ]
        # logger.debug('inside internally_make_fonts. The length of tower_stats_labels list is: ' + str(len(self.tower_stats_labels)))

    def get_all_tower_labels_and_positions(self):
        """
        :return: list of 2-element tuples, first element is label (used with blitting), second is its position.
        Returns all the labels, so they can be blitted onto the screen and their position
        """
        try:
            return [(tower_stat_label, (10, i * 10)) for i, tower_stat_label in enumerate(self.tower_stats_labels)]
        except:
            return []

    def get_lifepoint_label_and_position(self):
        return self.lifepoint_label, (200, 50)

    def get_bank_balance_label_and_position(self):
        return self.bank_balance_label, (200, 70)


def begin_game():
    """Display the start screen, if user presses any key, proceed to the game"""

    client = Client()
    client.connect_with_server()

    server_stats = ServerStats()  # contains messages sent from server
    formatted_server_messages = FormattedServerMessages()  # contains the formatted versions of all message, ideally called by serve_stats

    t_handle_receiving_messages = threading.Thread(target=dedicated_handle_receiving_messages,
                                                   args=(client, server_stats, formatted_server_messages),
                                                   name='client_waiting_to_receive_thread')
    t_handle_receiving_messages.start()

    start_message_font = pygame.font.SysFont("freesansbold", 50)


    while True:
        for event in pygame.event.get():
            # number presses represent balloons
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    dedicated_sending_messages(client, '1')  # numbers represent balloons
                elif event.key == pygame.K_2:
                    dedicated_sending_messages(client, '2')  # numbers represent balloons
                elif event.key == pygame.K_3:
                    dedicated_sending_messages(client, '3')  # numbers represent balloons
                elif event.key == pygame.K_4:
                    dedicated_sending_messages(client, '4')  # numbers represent balloons
                elif event.key == pygame.K_5:
                    dedicated_sending_messages(client, '5')  # numbers represent balloons
                elif event.key == pygame.K_p:
                    plotting_and_ML.try_machine_learning(server_stats.tower_stats)

            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
                client.close_client()

        DISPLAYSURF.fill(colours.BLACK)
        start_label = start_message_font.render("Client ", True, (255, 255, 0))
        DISPLAYSURF.blit(start_label, (250, 150))

        for tower_label, position in formatted_server_messages.get_all_tower_labels_and_positions():
            try:
                DISPLAYSURF.blit(tower_label, position)
            except:
                pass

        try:
            lifepoint_label, position = formatted_server_messages.get_lifepoint_label_and_position()
            DISPLAYSURF.blit(lifepoint_label, position)
        except:
            pass
        try:
            bank_balance_label, position = formatted_server_messages.get_bank_balance_label_and_position()
            DISPLAYSURF.blit(bank_balance_label, position)
        except:
            pass  # if can't show, labels, do nothing (aka, don't show them)
        plotting_and_ML.set_up_values(server_stats.tower_stats)
        plotting_and_ML.show_plot()
        fpsClock.tick(15)
        pygame.display.update()
