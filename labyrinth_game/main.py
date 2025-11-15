#!/usr/bin/env python3

from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import show_inventory, get_input
from labyrinth_game.constants import ROOMS


game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }

def main():
    """Начало игры"""
    game_state = {
        'current_room': 'entrance',
        'player_inventory': []
    }

    print("Добро пожаловать в Лабиринт сокровищ!")

    """ Основной игровой цикл """

    # Описание стартовой комнаты
    describe_current_room(game_state)

    # Игровой цикл
    while True:  
        command = get_input("> ")

        if command == "quit":
            print("Игра окончена.")
            break

        elif command == "look":
            describe_current_room(game_state)

        elif command == "inventory":
            show_inventory(game_state)

        else:
            print("Неизвестная команда. Доступные команды: look, inventory, quit.")

if __name__ == "__main__":
    main()
