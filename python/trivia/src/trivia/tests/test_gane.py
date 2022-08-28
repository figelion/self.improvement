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






