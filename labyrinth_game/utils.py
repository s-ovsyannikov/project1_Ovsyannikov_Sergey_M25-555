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

