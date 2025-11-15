

def show_inventory(game_state):
    """
    Содержимое инвентаря игрока
    """
    inventory = game_state['player_inventory']

    if inventory:
        print(f"Инвентарь: {', '.join(inventory)}.")
    else:
        print("Инвентарь пуст.")


def get_input(prompt="> "):
    """
    Считывает ввод пользователя с обработкой прерываний
    """
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"