#!/usr/bin/env python3

from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import show_inventory, get_input, take_item, move_player, use_item
from labyrinth_game.constants import ROOMS


game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }

def process_command(game_state, command):
    """
    Обрабатывает команду пользователя.
    Разделяет команду и аргумент, выполняет запрошенное действие.
    """
    parts = command.split()
    action = parts[0] if parts else ""
    arg = parts[1] if len(parts) > 1 else None

    match action:
        case "look":
            describe_current_room(game_state)

        case "inventory":
            show_inventory(game_state)

        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление (north, south, east, west).")

        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет, который хотите взять.")

        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет, который хотите использовать.")

        case "quit" | "exit":
            print("Игра окончена.")
            return False  # Флаг для завершения цикла

        case _:
            print(
                "Неизвестная команда. Доступные команды: "
                "look, go <направление>, take <предмет>, "
                "use <предмет>, inventory, quit/exit."
            )

    return True  # Продолжать игру


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
