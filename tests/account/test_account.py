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
