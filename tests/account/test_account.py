from pytest import fixture
from random import randint
from typing import Iterator, Dict


@fixture
def account_generator():
    return ({i+1: f"{randint(1, 99999):05}-{randint(1, 9)}"}
            for i in range(3))


def test_total_of_three_accounts(account_generator: Iterator[Dict[int, str]]) -> None:
    accounts = list(account_generator)
    print(f"\n\033[94m{accounts}\033[00m")
    assert accounts.__len__() == 3


def test_check_first_account_exists(account_generator) -> None:
    accounts = list(account_generator)
    assert len(accounts[0][1]) == 7


def test_check_second_account_exists(account_generator) -> None:
    accounts = list(account_generator)
    assert len(accounts[1][2]) == 7


def test_check_three_account_exists(account_generator) -> None:
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
