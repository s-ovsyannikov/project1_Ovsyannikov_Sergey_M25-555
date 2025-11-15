from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    """
    Описывает текущую комнату на основе game_state.
    Показывает название, описание, предметы, выходы, наличие загадок
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    # название комнаты 
    print(f'\n== {current_room.upper()} ==')

    # описание комнаты
    print(room['description'])

    # предметы в комнате
    if room['items']:
        print(f'Заметные предметы {' , '.join(room['items'])}.')

    # имеющиеся выходы
    exits = ', '.join(room['exits'].keys())
    print(f"Выходы: {exits}.")

    # загадки
    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """
    Решение загадок
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, answer = room['puzzle']
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()

    if user_answer == answer.lower():
        print("Правильно! Загадка решена.")
        room['puzzle'] = None  # убираем загадку из комнаты

        # Награда
        if current_room == 'hall':
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили: treasure_key!")
    else:
        print("Неверно. Попробуйте снова.")    

def attempt_open_treasure(game_state):
    """
    Попытка открыть сундук в сокровищнице.
    """
    current_room = game_state['current_room']

    # Проверяем что игрок в сокровищнице и там есть сундук
    if current_room != 'treasure_room' or 'treasure_chest' not in ROOMS[current_room]['items']:
        return False  
    
    inventory = game_state['player_inventory']

    # если у игрока есть ключ
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS[current_room]['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True

    # ключа нет, попытка ввести код
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