from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    """
    Содержимое инвентаря игрока
    """
    inventory = game_state['player_inventory']

    if inventory:
        print(f"Инвентарь: {', '.join(inventory)}.")
    else:
        print("Инвентарь пуст.")

  
def move_player(game_state, direction):
    """
    Перемещение игрока в выбранном направлении (если существует такая возможность) 
    """
    current_room = game_state['current_room']
    room_exits = ROOMS[current_room]['exits']


    if direction not in room_exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = room_exits[direction]

    # проверка для treasure_room
    if next_room == 'treasure_room':
        if 'rusty_key' in game_state['player_inventory']:
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
            game_state['current_room'] = next_room
            game_state['steps'] += 1
            describe_current_room(game_state)
            random_event(game_state)  
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return

    # обычный перемещение
    game_state['current_room'] = next_room
    game_state['steps'] += 1
    describe_current_room(game_state)
    random_event(game_state)  

def take_item(game_state, item_name):
    """
    Добавление предмета в инвентарь
    """
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']

    if item_name in room_items:
        game_state['player_inventory'].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """
    Использование инвентаря
    """
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    # логика использования предметов
    if item_name == 'torch':
        print("Стало светлее. Вы видите больше деталей вокруг.")
    elif item_name == 'sword':
        print("Вы чувствуете уверенность, держа меч в руках.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Вы открыли бронзовую шкатулку! Внутри — ржавый ключ.")
        else:
            print("Шкатулка уже открыта, внутри пусто.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")

def get_input(prompt="> "):
    """
    Считывает ввод пользователя с обработкой прерываний
    """
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"