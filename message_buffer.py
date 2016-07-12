"""This is a message buffer and is used by server.py and contains the messages for server to send to client. These messages include the stats of tower"""

import threading

buffer = []
binary_semaphore = threading.Semaphore(value=1)  # since it is inconsistent to read and push to buffer


def __push_message(message):
    """Adds message to buffer and calls server to display that message. A message cannot be added and read at the same time,
    thus, implemented a semaphore. THis is intended to be an internal method, please don't call"""
    with binary_semaphore:
        buffer.append(message)


def get_zeroth_message():
    """Gets the message at the front of the list. Consider using a queue instead. If no message, return None"""
    front_message = None
    with binary_semaphore:
        try:
            front_message = buffer.pop(0)
        except:
            front_message = None
    return front_message


def push_lifepoint_message(lifepoint):
    """Sends the lifepoint of the server to the client.
    Format: L=18.
    """
    formatted_lifepoint_message = 'L={}.'.format(lifepoint)
    __push_message(formatted_lifepoint_message)


def push_bank_balance_message(bank_balance):
    """ Format: B=625."""

    formatted_bank_balance_message = 'B={}.'.format(bank_balance)
    __push_message(formatted_bank_balance_message)


def push_create_new_tower_message(tower_id, tower_type, speed, radius, pop_power):
    """Format: T=499987854.t=LINEAR_TOWER.s=2.r=70.p=1."""
    formatted_tower_message = 'T={0}.t={1}.s={2}.r={3}.p={4}.'.format(tower_id, tower_type, speed, radius, pop_power)
    __push_message(formatted_tower_message)


def push_update_tower_speed_message(tower_id, speed):
    """Format: T=499984651.s=2."""
    formatted_tower_message = 'T={0}.s={1}.'.format(tower_id, speed)
    __push_message(formatted_tower_message)


def push_update_tower_radius_message(tower_id, radius):
    """Format: T=499984651.r=2."""
    formatted_tower_message = 'T={0}.r={1}.'.format(tower_id, radius)
    __push_message(formatted_tower_message)


def push_update_tower_pop_power_message(tower_id, pop_power):
    """Format: T=499984651.p=2."""
    formatted_tower_message = 'T={0}.p={1}.'.format(tower_id, pop_power)
    __push_message(formatted_tower_message)

def push_update_tower_pop_count_message(tower_id, pop_count):
    """Format: T=499984651.c=5"""
    formatted_tower_message = 'T={0}.c={1}.'.format(tower_id, pop_count)
    __push_message(formatted_tower_message)

def push_sell_tower_message(tower_id):
    """Format: T=499984651."""
    formatted_tower_message = 'T={0}.'.format(tower_id)
    __push_message(formatted_tower_message)
