# test_capitalize.py

from permguard_sdk.sample.my_fun import my_fun


def capital_case(x: str) -> str:
    return x.capitalize()


def test_capital_case() -> None:
    print(my_fun())
    assert capital_case(my_fun()) == 'Ciao'
