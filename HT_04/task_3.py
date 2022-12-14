"""
Користувач вводить змінні "x" та "y" з довільними цифровими значеннями.
Створіть просту умовну конструкцію (звiсно вона повинна бути в тiлi ф-цiї),
під час виконання якої буде перевірятися рівність змінних "x" та "y"
та у випадку нерівності - виводити ще і різницю.
Повинні працювати такі умови (x, y, z заміність на відповідні числа):
    x > y;       вiдповiдь - "х бiльше нiж у на z"
    x < y;       вiдповiдь - "у бiльше нiж х на z"
    x == y.      відповідь - "х дорівнює y"
"""


def get_different(x, y):
    """ Compares calculates"""

    if x > y:
        print(f"{x} бiльше нiж {y} на {x - y}")
    elif x < y:
        print(f"{y} бiльше нiж {x} на {y - x}")
    else:
        print(f"{x} дорівнює {y}")


if __name__ == '__main__':
    first, second = int(input('Введіть число "X":\n')),\
           int(input('Введіть число "Y":\n'))

    get_different(first, second)
