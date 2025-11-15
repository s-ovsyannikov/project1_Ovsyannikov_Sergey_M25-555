#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import move_player, take_item, solve_puzzle
from labyrinth_game.utils import show_room_description, show_inventory


def main():
    """точка входа в игру."""
    print("Первая попытка запустить проект!")

if __name__ == "__main__":
    main()

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }

