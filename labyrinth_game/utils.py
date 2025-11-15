import math

from labyrinth_game.constants import ALTERNATIVE_ANSWERS, ROOMS


def pseudo_random(seed, modulo):
    """
    генератор случайных чисел
    """
    if modulo <= 0:
        return 0

    value = math.sin(seed * 12.9898) * 43758.5453
    fractional = value - math.floor(value)
    return int(fractional * modulo)

def trigger_trap(game_state):
    """
    ловушка: потеря предмета или урон
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        # выбор случайного предмета
        index = pseudo_random(game_state['steps'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли: {lost_item}!")
    else:
        # если инвентарь пустой
        roll = pseudo_random(game_state['steps'], 10)
        if roll < 3:  # 30% шанс проиграть
            print("Пол проваливается под вами... Вы проиграли!")
            game_state['game_over'] = True
        else:
            print("Вы чудом удержались на краю пропасти. Вам повезло!")


def random_event(game_state):
    """
    Генерирует случайное событие при перемещении (вероятность 10%)
    """
    event_chance = pseudo_random(game_state['steps'], 10)
    if event_chance != 0:
        return  

    # выбор типов случайных событий (0–2)
    event_type = pseudo_random(game_state['steps'] + 1, 3)
    current_room = game_state['current_room']


    match event_type:
        case 0:
            # нашли монетку
            ROOMS[current_room]['items'].append('coin')
            print("Вы заметили на полу блестящую монетку и подобрали её.")

        case 1:
            # испуг
            print("Вы слышите странный шорох в темноте...")
            if 'sword' in game_state['player_inventory']:
                print("Вы взмахнули мечом — шорох затих. Похоже, вы отпугнули кого-то.")


        case 2:
            # ловушка в trap_room
            if (current_room == 'trap_room' and
                    'torch' not in game_state['player_inventory']):
                print("В темноте что-то щёлкает... Это ловушка!")
                trigger_trap(game_state)


def describe_current_room(game_state):
    """
    описание текущей комнаты
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")
    print(room['description'])

    if room['items']:
        print(f"Заметные предметы: {', '.join(room['items'])}.")


    exits = ', '.join(room['exits'].keys())
    print(f"Выходы: {exits}.")


    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")




def solve_puzzle(game_state):
    """
    отгадывание загадок с учетом альтернативных вариантов ответов
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, answer = room['puzzle']
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()

    valid_answers = [answer.lower()]
    if answer in ALTERNATIVE_ANSWERS:
        valid_answers.extend(ALTERNATIVE_ANSWERS[answer])


    if user_answer in valid_answers:
        print("Правильно! Загадка решена.")
        room['puzzle'] = None  # Убираем загадку

        # Награда зависит от комнаты
        if current_room == 'hall':
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили: treasure_key!")
        elif current_room == 'cellar':
            game_state['player_inventory'].append('hint')
            print("Вы нашли подсказку! 42!")
        elif current_room == 'gallery':
            game_state['player_inventory'].append('mystery cube')
            print("Вы получили: mystery cube")

    else:
        print("Неверно. Попробуйте снова.")
        # В trap_room неверный ответ активирует ловушку
        if current_room == 'trap_room':
            trigger_trap(game_state)



def attempt_open_treasure(game_state):
    """
    попытка открыть сундук в treasure_room.
    """
    current_room = game_state['current_room']

    # проверка, что игрок в treasure_room и там есть сундук
    if (current_room != 'treasure_room' or
            'treasure_chest' not in ROOMS[current_room]['items']):
        return False

    inventory = game_state['player_inventory']

    # если есть ключ
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS[current_room]['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True

    # нет ключа, предлагает ввести код
    print("Сундук заперт. У вас нет treasure_key. Попробовать ввести код? (да/нет)")
    choice = input("> ").strip().lower()

    if choice != 'да':
        print("Вы отступаете от сундука.")
        return False

    puzzle = ROOMS[current_room]['puzzle']
    if puzzle is None:
        print("Код неизвестен.")
        return False

    question, answer = puzzle
    print(question)
    user_code = input("Введите код: ").strip()


    if user_code == answer:
        print("Код принят! Замок щёлкает. Сундук открыт!")
        ROOMS[current_room]['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    else:
        print("Неверный код. Сундук остаётся запертым.")
        return False