from src.trivia.game import Game, QuestionCategory
from src.trivia.exception import MaximumPlayerLimitExceededException

import pytest


def setup_the_test_game(names_of_players: str = ["Player"]) -> Game:
    game = Game()
    for name in names_of_players:
        game.add_player(name)
    return game


def test_you_can_add_player_to_the_game() -> None:
    game = Game()
    player = "chris"
    game.add_player(player)

    assert game.how_many_players == 1
    assert game.players[0] == player


def test_you_can_add_maximum_number_of_players() -> None:
    game = Game()
    players = ('a', 'b', 'c', 'd', 'e', 'f')

    for player in players:
        game.add_player(player)

    assert game.how_many_players == len(players)


def test_you_cannot_exceed_the_players_limit() -> None:
    game = Game()
    players = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k')

    with pytest.raises(MaximumPlayerLimitExceededException):
        for player in players:
            game.add_player(player)


@pytest.mark.parametrize("place, message", [
    (0, "Pop Question 0\n"),
    (3, "Rock Question 0\n"),
    (2, "Sports Question 0\n"),
    (1, "Science Question 0\n"),
])
def test_ask_question_should_print_question_from_given_category(capsys, place: int, message: str) -> None:

    game = setup_the_test_game()
    game.places[0] = place
    capsys.readouterr()  # filter out irrelevant messages

    game._ask_question()

    captured_question = capsys.readouterr()

    assert captured_question.out == message


def test_game_should_have_access_to_fifty_questions_in_each_category() -> None:
    game = setup_the_test_game()

    assert len(game.pop_questions) == 50
    assert len(game.science_questions) == 50
    assert len(game.sports_questions) == 50
    assert len(game.rock_questions) == 50


@pytest.mark.parametrize("place, category", [
    (0, QuestionCategory.POP),
    (4, QuestionCategory.POP),
    (8, QuestionCategory.POP),
    (1, QuestionCategory.SCIENCE),
    (5, QuestionCategory.SCIENCE),
    (9, QuestionCategory.SCIENCE),
    (2, QuestionCategory.SPORTS),
    (6, QuestionCategory.SPORTS),
    (10, QuestionCategory.SPORTS),
    (3, QuestionCategory.ROCK),
    (7, QuestionCategory.ROCK),
    (11, QuestionCategory.ROCK),
])
def test_current_category_should_return_question_category_based_on_the_place_of_player(
        place: int,
        category: str,
) -> None:
    game = setup_the_test_game()

    game.places[0] = place

    assert game._current_category == category


def test_current_category_should_return_rock_question_for_undefined_place() -> None:
    game = setup_the_test_game()

    game.places[0] = "Undefined"

    assert game._current_category == QuestionCategory.ROCK


@pytest.mark.parametrize("roll", [1, 3, 5])
def test_roll_should_free_player_from_penalty_box_when_rolled_number_is_odd(roll: int) -> None:
    game = setup_the_test_game()
    game.in_penalty_box[0] = 1
    game.roll(roll)

    assert game.is_getting_out_of_penalty_box is True


@pytest.mark.parametrize("roll", [2, 4, 6])
def test_roll_should_hold_a_player_in_penalty_box_when_rolled_number_is_even(roll: int) -> None:
    game = setup_the_test_game()
    game.in_penalty_box[0] = 1
    game.roll(roll)

    assert game.is_getting_out_of_penalty_box is False


def test_roll_should_restart_place_after_exceeding_board_places() -> None:
    game = setup_the_test_game()
    board_places_limit = 11
    game.places[0] = board_places_limit
    game.roll(1)

    assert game.places[0] <= board_places_limit


def test_roll_should_move_player_by_rolled_number() -> None:
    game = setup_the_test_game()
    rolled_number = 2
    current_place = 5
    game.places[0] = current_place
    game.roll(rolled_number)

    assert game.places[0] == rolled_number + current_place


def test_roll_should_inform_about_who_is_rolling_and_what_was_rolled(capsys) -> None:
    game = setup_the_test_game()
    capsys.readouterr()  # Catch not needed messages
    rolled_number = 5
    game.roll(rolled_number)

    captured_message = capsys.readouterr()
    captured_message = captured_message.out.split("\n")

    assert captured_message[0] == "Player is the current player"
    assert captured_message[1] == f"They have rolled a {rolled_number}"


def test_roll_should_inform_about_gettin_out_of_penalty_box(capsys) -> None:
    game = setup_the_test_game()
    capsys.readouterr()  # Catch not needed messages

    rolled_number = 5
    game.in_penalty_box[0] = 1
    game.roll(rolled_number)

    captured_message = capsys.readouterr()
    captured_message = captured_message.out.split("\n")

    assert captured_message[2] == 'Player is getting out of the penalty box'


def test_roll_should_inform_about_getting_out_of_penalty_box_when_rolled_odd_number(capsys) -> None:
    game = setup_the_test_game()
    capsys.readouterr()  # Catch not needed messages

    rolled_number = 5
    game.in_penalty_box[0] = 1
    game.roll(rolled_number)

    captured_message = capsys.readouterr()
    captured_message = captured_message.out.split("\n")

    assert captured_message[2] == 'Player is getting out of the penalty box'


def test_roll_should_inform_about_staying_in_penelty_box_when_rolled_even_number(capsys) -> None:
    game = setup_the_test_game()
    capsys.readouterr()  # Catch not needed messages

    rolled_number = 6
    game.in_penalty_box[0] = 1
    game.roll(rolled_number)

    captured_message = capsys.readouterr()
    captured_message = captured_message.out.split("\n")

    assert captured_message[2] == 'Player is not getting out of the penalty box'


def test_roll_should_inform_about_the_new_place_of_player_when_he_get_out_of_penalty_box(capsys) -> None:
    game = setup_the_test_game()
    capsys.readouterr()  # Catch not needed messages

    rolled_number = 3
    current_place = 5
    game.places[0] = current_place
    game.in_penalty_box[0] = 1
    game.roll(rolled_number)

    captured_message = capsys.readouterr()
    captured_message = captured_message.out.split("\n")

    assert captured_message[3] == 'Player\'s new location is 8'

