from pytest import fixture
from random import randint
from typing import Iterator, Dict, Callable

from typing import List
from dataclasses import dataclass

# @dataclass
# class Account:
#     id: int
#     account: str
#     name: str
#     balance: float


def find_by(fn: Callable[[str], list], data: list) -> list:
    return [*filter(fn, data)]


def account_exists(account: tuple, accounts: list, find_by) -> bool:
    return True if find_by(lambda x: x[1] == account[0], accounts) != [] else False


@fixture
def account_list():
    return [[1, "45854-8", "Tiago Emanuel Assunção", 150.5],
            [2, "48545-8", "Larissa Sandra Pires", 50],
            [3, "78546-8", "Ester Rayssa Galvão", 315],
            [4, "78965-8", "Kevin Jorge Peixoto", 420.5],
            [5, "00215-8", "Mariah Fabiana Ferreira", 320.5],
            [6, "02157-8", "Renato Tiago Galvão", 350],
            [7, "98025-8", "Louise Eliane Galvão", 650]]


@fixture
def account_generator():
    return ({i+1: f"{randint(1, 99999):05}-{randint(1, 9)}"}
            for i in range(3))


def test_account_exists(account_list):

    assert account_exists(("45854-8",), account_list, find_by)


def test_total_of_three_accounts(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    print(f"\n\033[94m{accounts}\033[00m")
    assert accounts.__len__() == 3


def test_check_first_account_exists(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert len(accounts[0][1]) == 7


def test_check_second_account_exists(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert len(accounts[1][2]) == 7


def test_check_three_account_exists(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert len(accounts[2][3]) == 7


def test_check_if_first_account_has_hyphen(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert accounts[0][1][5:6].__eq__("-")


def test_check_if_second_account_has_hyphen(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert accounts[1][2][5:6].__eq__("-")


def test_check_if_three_account_has_hyphen(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert accounts[2][3][5:6].__eq__("-")


def test_check_if_first_account_has_check_digit(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert accounts[0][1].split("-")[1].__len__() == 1


def test_check_if_second_account_has_check_digit(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert accounts[1][2].split("-")[1].__len__() == 1


def test_check_if_three_account_has_check_digit(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    assert accounts[2][3].split("-")[1].__len__() == 1
