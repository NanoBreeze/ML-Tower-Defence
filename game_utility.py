import level
import pygame


def create_game_levels():
    """
    :return: a list of level objects
     Creates the levels used in this game, in sequential order
    """

    return [level.Level1(),
            level.Level2(),
            level.Level3()]


def set_bank_balance_font():
    return pygame.font.SysFont("freesansbold", 15)


def set_life_point_font():
    return pygame.font.SysFont("freesansbold", 15)
