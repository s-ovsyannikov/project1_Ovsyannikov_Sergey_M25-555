#!/usr/bin/env python3

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import get_input, move_player, show_inventory, take_item, use_item
from labyrinth_game.utils import attempt_open_treasure, describe_current_room, solve_puzzle

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }

def show_help(commands):
    """Выводит список доступных команд."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"{cmd:<16} — {desc}")


def process_command(game_state, command):
    """
    Обрабатывает команду пользователя.
    """
    parts = command.split()
    action = parts[0] if parts else ""
    arg = parts[1] if len(parts) > 1 else None

    match action:
        case "help":
            show_help(COMMANDS)

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

        case "solve":
            solve_puzzle(game_state)
            # После решения загадки проверяем, можно ли открыть сундук
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)

        case "quit" | "exit":
            print("Игра окончена.")
            return False

        case _:
            print(
                "Неизвестная команда. Доступные команды: "
                "look, go <направление>, take <предмет>, "
                "use <предмет>, inventory, solve, quit/exit."
            )

    return True  


def main():
    # инициализация состояния игры
    game_state = {
        'current_room': 'entrance',
        'player_inventory': [],
        'steps': 0,
        'game_over': False
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    # игровой цикл
    while not game_state['game_over']:
        command = get_input("> ")
        
        if command in ("quit", "exit"):
            print("Игра окончена.")
            break

        if not process_command(game_state, command):
            break  # dыход по команде quit/exit

        # проверка на победу после каждой команды
        if game_state['game_over']:
            break


if __name__ == "__main__":
    main()
