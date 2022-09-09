import pytest

from greetings import get_greeting_for_user
from greetings.greeting_schedule import find_greeting


@pytest.mark.parametrize("greeting_time", [20, 21, 5])
def test_greeting_between_20_6_succeeds(greeting_time: int) -> None:
    name = "XXX"
    result = get_greeting_for_user(
        time_of_current_greeting=greeting_time,
        greeting_schedule=find_greeting,
        name=name
    )
    assert result == fr"¡Buenas noches {name}!"


@pytest.mark.parametrize( "greeting_time", [6, 8, 11])
def test_greeting_between_6_12_succeeds(greeting_time: int) -> None:
    name = "XXX"
    result = get_greeting_for_user(
        time_of_current_greeting=greeting_time,
        greeting_schedule=find_greeting,
        name=name
    )
    assert result == fr"¡Buenos días {name}!"


@pytest.mark.parametrize("greeting_time", [12, 13, 17])
def test_greeting_between_12_20_succeeds(greeting_time: int) -> None:
    name = "XXX"
    result = get_greeting_for_user(
        time_of_current_greeting=greeting_time,
        greeting_schedule=find_greeting,
        name=name
    )
    assert result == fr"¡Buenas tardes {name}!"


def test_detected_palindrome() -> None:
    assert False


def test_says_goodbyes_when_key_word_used() -> None:
    assert False

