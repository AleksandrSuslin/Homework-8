import random


class Card:

    def __init__(self, name):

        self._name = name
        self._number_of_values = 15
        self._matrix = []
        for row in range(0, 3):
            self._matrix.append([None for column in range(0, 9)])



        six_numbers_in_row = True


        while six_numbers_in_row:
            self._clear()
            for column in range(0, 6):
                place_for_none = random.randint(0, 2)
                for row in range(0, 3):
                    if row != place_for_none:
                        self._matrix[row][column] = 0

            six_numbers_in_row = False
            for row in self._matrix:
                if row.count(0) == 6:
                    six_numbers_in_row = True
                    break


        for column in range(6, 9):
            six_numbers_in_row = True
            while six_numbers_in_row:
                place_for_0 = random.randint(0, 2)
                if self._matrix[place_for_0].count(0) < 5:
                    six_numbers_in_row = False
                    self._matrix[place_for_0][column] = 0


        for column in range(0, 9):
            new_position = random.randint(0, 8)
            for row in range(0, 3):
                buf = self._matrix[row][column]
                self._matrix[row][column] = self._matrix[row][new_position]
                self._matrix[row][new_position] = buf


        for row in range(0, 3):
            for column in range(0, 9):
                if self._matrix[row][column] == 0:
                    duplicate_detected = True
                    while duplicate_detected:
                        new_value = column * 10 + random.randint(1, 10)
                        if not [self._matrix[0][column], self._matrix[1][column],
                                self._matrix[2][column]].count(new_value):
                            duplicate_detected = False
                            self._matrix[row][column] = new_value



    def _clear(self):
        for row in range(0, 3):
            for column in range(0, 9):
                self._matrix[row][column] = None

    @property
    def is_empty(self):
        return not self._number_of_values

    def output(self):
        title = ' ' + self._name + ' '
        if len(title) <= 24:
            print(title.center(26, '-'))
        else:
            print('-' * 26)
        for y in self._matrix:
            string = ''
            for x in y:
                if not x:
                    string += '   '
                elif x == -1:
                    string += ' - '
                else:
                    string += '{:>2} '.format(str(x))
            print(string)
        print('-' * 26)

    def find(self, value):
        for row in self._matrix:
            if row.count(value):
                return True
        return False

    def cross_out(self, value):
        for row in range(0, 3):
            for column in range(0, 9):
                if self._matrix[row][column] == value:
                    self._matrix[row][column] = -1
                    self._number_of_values -= 1
                    return value
        return None


class PouchOfBarrels:


    def __init__(self):
        self._array = list(range(1, 91))

    @property
    def left(self):
        return len(self._array)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._array):
            return self._array.pop(random.randint(0, len(self._array) - 1))
        raise StopIteration


last_comp_move = True
mistake_chance = 0.5


player_card = Card('Ваша карточка')
comp_card = Card('Карточка компьютера')

barrels = PouchOfBarrels()

print('Игра начинается'.upper())


player_loss = False
draw_flag = False

for new_barrel in barrels:
    print('\nНовый бочонок: {} (осталось {})'.format(new_barrel, barrels.left))
    player_card.output()
    comp_card.output()


    if input('Зачеркнуть цифру? (y/n) ') == 'y':
        if player_card.cross_out(new_barrel):
            print('Число {} вычеркнуто из вашей карточки.'.format(new_barrel))
            if player_card.is_empty and not last_comp_move:
                break
        else:
            print('Будьте внимательнее! Числа {} нет в вашей карточке.'.format(new_barrel))
            player_loss = True
            if not last_comp_move:
                break
    else:
        if player_card.find(new_barrel):
            print('Будьте внимательнее! В вашей карточке есть число {}.'.format(new_barrel))
            player_loss = True
            if not last_comp_move:
                break


    if mistake_chance and random.uniform(0, 99) < mistake_chance:
        print('Компьютер ошибается! В его карточке {} {}'.format(
            'есть число' if comp_card.find(new_barrel) else 'нет числа', new_barrel))
        if player_loss:
            draw_flag = True
        break
    else:
        if comp_card.cross_out(new_barrel):
            print('Компьютер вычёркивает число {} из своей карточки.'.format(new_barrel))

    if player_card.is_empty and comp_card.is_empty:
        draw_flag = True
        break
    if player_card.is_empty:
        break
    if comp_card.is_empty:
        player_loss = True
        break
    if player_loss:
        break

if draw_flag:
    print('Игра окончена. Ничья!')
elif player_loss:
    print('Игра окончена. Вы проиграли!')
else:
    print('Игра окончена. Поздравляем, вы выиграли!')