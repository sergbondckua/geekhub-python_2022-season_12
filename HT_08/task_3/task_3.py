"""Банкомат"""

import csv
import json
import random
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Автоматичне додавання Style.RESET_ALL в кінець print


def validate_user_access(func):
    """Декоратор на валідність логіна та пароля"""

    def wrapper(login: str, passwd: str, *args, **kwargs):
        # Відкриває файл с даними доступу
        try:
            with open("db/users.csv", "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["username"] == login and row["password"] == passwd:
                        return func(login, passwd, *args, **kwargs)

                    # Якщо логін вірний, а пароль ні, даємо ще спроби вводу пароля
                    elif row["username"] == login:
                        for attempt in range(2):
                            if row["password"] == input(
                                    f"Incorrect password, try again: "):
                                return func(login, passwd, *args, **kwargs)
                            else:
                                print(f"Try again, last attempt!")
                        raise Exception("Access denied!")

                # Якщо логін не знайдено в БД, пропонуємо реєстрацію
                print(Fore.LIGHTGREEN_EX + "Not found username, need registration")
                if input("You want sign_up? - yes/no: ").strip() in ["yes", "y"]:
                    return sign_up(login)
                raise Exception("Access denied!")
        except FileNotFoundError:
            raise FileNotFoundError("Need create users.csv")

    return wrapper


def write_statement(client: str, **kwargs):
    """Записує в файл транзакції клієнта"""

    #  Формуємо дані для виписки транзакцій
    data = {
        "id": random.randint(0, 99999999),
        "time": datetime.now().timestamp().__int__(),
        "description": kwargs["desc"],
        "amount": kwargs["amount"],
        "balance": kwargs["balance"]
    }

    # Читаємо/Оновлюємо/Записуємо до файлу виписки клієнта
    try:
        with open(f"asset/{client}_transactions.json", "r+", encoding="utf-8") as f:
            file_data = json.load(f)
            file_data.append(data)

        with open(f"asset/{client}_transactions.json", "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=4)
    except FileNotFoundError:
        with open(f"asset/{client}_transactions.json", "w", encoding="utf-8") as f:
            json.dump([data], f, indent=4)


def sign_up(client):
    """Реєстрація нового клієнта"""
    print(Fore.LIGHTRED_EX + "Registration".center(100, '~'))
    with open("db/users.csv", "a", encoding="utf-8", newline="") as f:
        users = csv.DictReader(client)
        if client in users:
            print('Name is already registered, try again with unique name')
            return start()
        pre_passwd = input(client.capitalize() + ", enter your new password: ")
        repeat_passwd = input(client.capitalize() + ", repeat your password: ")
        passwd = pre_passwd if repeat_passwd == pre_passwd else False
        if not passwd:
            print("Passwords don't match")
            return sign_up(client)
        writer = csv.writer(f)
        writer.writerow([client, passwd])
        print(Fore.GREEN + "Wellcome to ATM!".center(100, '~'))

    return sign_in(client, passwd)


@validate_user_access
def sign_in(login: str, passwd: str) -> dict:
    """Повертає словник з даними доступа клієнта"""
    print(
        Fore.CYAN + f"\nHello {login.capitalize()}, "
                    f"access successfully\n" + Style.RESET_ALL
    )
    return dict(login=login, password=passwd)


def get_balance(client: str):
    """Отримує баланс клієнта"""
    try:
        with open(f"asset/{client}_balance.txt", "r") as f:
            balance = f.read()
            return balance
    except FileNotFoundError:
        with open(f"asset/{client}_balance.txt", "w") as f:
            balance = 0
            f.write(str(balance))
    return 0


def make_deposit(client: str) -> tuple:
    """Поповнює баланс"""
    current_balance = get_balance(client)
    deposit = abs(int(input("Enter your deposit: $")))
    new_balance = int(current_balance) + deposit
    with open(f"asset/{client}_balance.txt", "w", encoding="utf-8") as f:
        f.write(str(new_balance))
        write_statement(
            client, desc="Deposit", amount=deposit, balance=new_balance
        )
    return deposit, new_balance


def make_withdraw(client: str):
    """Знімає кошти, зменшує баланс"""
    amount = abs(int(input("What amount to withdraw?: $")))
    current_balance = get_balance(client)
    new_balance = int(current_balance) - amount
    if new_balance > 0:
        with open(f"asset/{client}_balance.txt", "w", encoding="utf-8") as f:
            f.write(str(new_balance))
            write_statement(
                client, desc="Withdraw", amount=-amount, balance=new_balance
            )
        return amount, new_balance
    else:
        print(Fore.RED + f"It is not possible to withdraw "
                         f"{Fore.BLACK}{Back.RED}${amount}{Style.RESET_ALL}"
                         f"{Fore.RED}, your balance: {Back.YELLOW}"
                         f"${get_balance(client)}{Style.RESET_ALL}"
              )
    return False


def start():
    print(Fore.CYAN + "Authorization required: Sign in please!")
    username = input("Enter a username: ")
    password = input("Enter your password: ")
    client = sign_in(username, password)
    stop = True
    while stop:
        choose = input(Fore.LIGHTBLACK_EX +
                       f"\nCHOOSE AN ITEM:{Style.RESET_ALL}\n"
                       f"{Fore.LIGHTYELLOW_EX}[1] - Balance{Style.RESET_ALL}\n"
                       f"{Fore.GREEN}[2] - Deposit{Style.RESET_ALL}\n"
                       f"{Fore.MAGENTA}[3] - Withdraw{Style.RESET_ALL}"
                       f"{Fore.RESET}\n[4] - EXIT\n" + Style.RESET_ALL
                       )
        # Select 1
        if choose == "1":
            print(f"[BALANCE]".center(30, "#"))
            balance = get_balance(client.get('login'))
            print(Fore.YELLOW + f"{client['login'].capitalize()}, "
                                f"your balance is "
                                f"{Fore.BLACK}{Back.YELLOW}${balance}"
                  )

        # Select 2
        elif choose == "2":
            print("[DEPOSIT]".center(30, "#"))
            deposit = make_deposit(client.get('login'))
            print(Fore.LIGHTGREEN_EX +
                  f"{client['login'].capitalize()}, "
                  f"now {Back.LIGHTBLACK_EX}+${deposit[0]}"
                  f"{Style.RESET_ALL + Fore.LIGHTGREEN_EX} and "
                  f"your new balance is {Back.LIGHTBLACK_EX}"
                  f"${deposit[1]}"
                  )

        # Select 3
        elif choose == "3":
            print("[WITHDRAW]".center(30, "#"))
            withdraw = make_withdraw(client.get('login'))
            if withdraw:
                print(Fore.LIGHTGREEN_EX +
                      f"{client['login'].capitalize()}, "
                      f"now {Back.LIGHTBLACK_EX}-${withdraw[0]}"
                      f"{Style.RESET_ALL + Fore.LIGHTGREEN_EX} and "
                      f"your new balance is {Back.LIGHTBLACK_EX}"
                      f"${withdraw[1]}" + Style.RESET_ALL
                      )

        # Select 4
        elif choose == "4":
            print("[EXIT]".center(30, "#"))
            print(f"Bye-bye, {client['login'].capitalize()}!".center(30, '-'))
            stop = False
        else:
            print(Fore.YELLOW + "Such an item is not on the menu. Try again!")


if __name__ == '__main__':
    start()
