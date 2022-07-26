import random
import re


print('Игра началась!')
SHOW_MUST_GO_ON = True

main_field = [['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
              ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']]


def show_field(field):
    # Ф-ция для вывода в консоль игрового поля

    print(['x', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    for i in range(0, 10):
        print(field[i], 'y' + str(i + 1))
    print('\n')


def move_player(field):
    # Функция хода игрока

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    while True:

        try:
            move_y = int(input('Введите номер клетки от 1 до 10 по x:'))
            move_x = int(input('Введите номер клетки от 1 до 10 по y:'))
        except ValueError:
            print('Введите корректные значения')
            continue

        if move_x not in values or move_y not in values:
            print('Введите корректные значения')
            continue

        if field[move_x - 1][move_y - 1] == '_':
            field[move_x - 1][move_y - 1] = 'x'
            break

        print('Клетка должна быть пустой')


def move_pc(field):
    # Функция хода ПК

    while True:
        move_x = random.randint(0, 9)
        move_y = random.randint(0, 9)

        if field[move_x][move_y] == '_':
            field[move_x][move_y] = 'o'
            break


def make_diag(field):
    # Ф-ция превращения диагоналей в горизонтальные линии для дальнейшей проверки по диагонали

    field_diag = []
    for i in range(0, 10):

        if i < 5:
            field_diag.append(field[i][4 - i:])
            field_diag[i] = field_diag[i] + ['_'] * (10 - len(field_diag[i]))
        elif i == 5:
            field_diag.append(field[i][:])
            field_diag[i] = ['_'] + field_diag[i][:-1]
        else:
            field_diag.append(field[i][:5 - i])
            field_diag[i] = ['_'] * (10 - len(field_diag[i][:-1])) + field_diag[i][:-1]

    return list(map(list, zip(*field_diag)))


def check_looser(field, query):
    # Функция проверки победителя

    r_pattern = {
        'pc': r'o{5}',
        'player': r'x{5}'
    }
    winner = {
        'pc': 'Победа за Игроком!',
        'player': 'Победа за ПК'
    }

    for i in range(0, 10):
        global SHOW_MUST_GO_ON

        if re.search(r_pattern[query], ''.join(field[i])):
            print(winner[query])
            print('Конец игры!')
            show_field(main_field)
            SHOW_MUST_GO_ON = False


step = 1
while SHOW_MUST_GO_ON:

    # Блок вывода в консоль иинформации:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print('~' * 53)
    print(" " * 17, '| ', f'{step}-й ход!', ' |')
    print('~' * 53)
    show_field(main_field)

    move_player(main_field)
    move_pc(main_field)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Блок проверки победителя
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    T_field = list(map(list, zip(*main_field)))  # Транспонирование матрицы для проверки по горизонтали

    field_diag = make_diag(main_field)  # Превращение диагоналей в горизонтали

    R_diag_field = []
    for i in range(0, 10):
        R_diag_field.append(list(reversed(main_field[i])))
    R_diag_field = make_diag(R_diag_field)  # Превращение диагоналей реверса в диагонали

    fields = [main_field, T_field, field_diag, R_diag_field]

    for f in fields:
        check_looser(f, 'pc')
        check_looser(f, 'player')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Блок выводва в консоль ин-ции и проверка ничьи
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    step += 1
    if step == 50:
        print('ПОСЛЕДНИЙ ХОД!')
    elif step > 50 and SHOW_MUST_GO_ON:
        print("У НАС СЕГОДНЯ НИЧЬЯ!")
        print('Конец игры!')
        break