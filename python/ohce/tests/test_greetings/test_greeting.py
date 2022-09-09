import pytest

from greetings import get_greeting_for_user
from greetings.greeting_schedule import find_greeting
from user_messages.process_user_messages import get_answer_on_user_message


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


def test_answer_for_user_message_should_be_a_reverted_user_message() -> None:
    name = "XXX"
    message_from_user = "hola"
    result = get_answer_on_user_message(message_from_user, name)
    assert result == "aloh"


def test_answer_for_user_palindrome_message_should_be_a_reverted_user_message_with_special_sentence() -> None:
    name = "XXX"
    message_from_user = "able was I ere I saw elba"
    result = get_answer_on_user_message(message_from_user, name)
    special_sentence = r"¡Bonita palabra!"
    assert result[0] == message_from_user
    assert result[1] == special_sentence


def test_says_goodbyes_when_key_word_used() -> None:
    name = "XXX"
    message_from_user = "Stop!"
    result = get_answer_on_user_message(message_from_user, name)
    goodbyes = r"Adios XXX"
    assert result == goodbyes

