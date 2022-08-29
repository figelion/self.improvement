#!/usr/bin/env python3

from collections import defaultdict
from enum import Enum
from random import randrange

from src.trivia.exception import MaximumPlayerLimitExceededException


class QuestionCategory(Enum):
    POP = "Pop"
    SCIENCE = "Science"
    SPORTS = "Sports"
    ROCK = "Rock"


class Game:
    def __init__(self):
        self.players = []
        self.players_limit = 6
        self.places = [0] * self.players_limit
        self.limit_of_max_number_place = 11
        self.in_penalty_box = [0] * self.players_limit

        self.purses = [0] * self.players_limit
        self.required_number_of_coins_to_win_game = 6


        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        self._question_category_for_place = self._create_question_for_places()

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append(self.create_rock_question(i))

    def _create_question_for_places(self) -> dict[int, QuestionCategory]:
        question_category_for_place = {
            0: QuestionCategory.POP,
            4: QuestionCategory.POP,
            8: QuestionCategory.POP,
            1: QuestionCategory.SCIENCE,
            5: QuestionCategory.SCIENCE,
            9: QuestionCategory.SCIENCE,
            2: QuestionCategory.SPORTS,
            6: QuestionCategory.SPORTS,
            10: QuestionCategory.SPORTS,
            3: QuestionCategory.ROCK,
            7: QuestionCategory.ROCK,
            11: QuestionCategory.ROCK,
        }
        return defaultdict(lambda: QuestionCategory.ROCK, question_category_for_place)


    def create_rock_question(self, index):
        return "Rock Question %s" % index

    def add_player(self, player_name):
        if self.how_many_players > self.players_limit:
            raise MaximumPlayerLimitExceededException("Players limit exceeded")
        self.players.append(player_name)
        print(player_name + " was added")
        print("They are player number %s" % len(self.players))

    @property
    def how_many_players(self):
        return len(self.players)

    def is_playable(self):
        return self.how_many_players >= 2

    def roll(self, roll):
        print("%s is the current player" % self.players[self.current_player])
        print("They have rolled a %s" % roll)

        if self._is_player_in_penalty_box():
            # TODO[30.08.2022 - 01:10: figelion]: Rename methods
            if self._did_player_get_out_of_a_penalty_box_by_rolling_odd_number(roll):
                self._prepare_player_to_escape_from_penalty_box()
                self._progress_player_in_game(roll)
            else:
                self._imprison_player_in_penalty_box()
        else:
            self._progress_player_in_game(roll)

    def _is_player_in_penalty_box(self):
        return self.in_penalty_box[self.current_player]

    def _did_player_get_out_of_a_penalty_box_by_rolling_odd_number(self, roll):
        return roll % 2 != 0

    def _prepare_player_to_escape_from_penalty_box(self):
        self.is_getting_out_of_penalty_box = True
        self._print_information_about_getting_out_of_penalty_box()

    def _print_information_about_getting_out_of_penalty_box(self):
        print("%s is getting out of the penalty box" % self.players[self.current_player])

    def _progress_player_in_game(self, roll: int):
        self.move_player(roll)
        self.print_current_player_position()
        self.print_question_category()
        self.print_question()

    def move_player(self, roll):
        self.places[self.current_player] = self.places[self.current_player] + roll
        if self.places[self.current_player] > self.limit_of_max_number_place:
            self.places[self.current_player] = self.places[self.current_player] - 12

    def print_current_player_position(self):
        print(self.players[self.current_player] + \
              '\'s new location is ' + \
              str(self.places[self.current_player]))

    def print_question_category(self):
        print("The category is %s" % self.get_current_question_category_name())

    def get_current_question_category_name(self):
        return self._current_category.value

    def print_question(self):
        return print(self._get_question_for_category(self._current_category))

    def _get_question_for_category(self, category: QuestionCategory):
        question = {
            QuestionCategory.POP: self.pop_questions.pop(0),
            QuestionCategory.SCIENCE: self.science_questions.pop(0),
            QuestionCategory.SPORTS: self.sports_questions.pop(0),
            QuestionCategory.ROCK: self.rock_questions.pop(0),
        }
        return question[category]

    def _imprison_player_in_penalty_box(self):
        self.print_information_about_staying_in_penalty_box()
        self.is_getting_out_of_penalty_box = False

    def print_information_about_staying_in_penalty_box(self):
        print("%s is not getting out of the penalty box" % self.players[self.current_player])

    def _get_question_category_for_place(self, place: int):
        return self._question_category_for_place[place]

    @property
    def _current_category(self):
        return self._get_question_category_for_place(self.places[self.current_player])

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                self.in_penalty_box[self.current_player] = False
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print(self.players[self.current_player] + \
                      ' now has ' + \
                      str(self.purses[self.current_player]) + \
                      ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True

        else:

            print("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            print(self.players[self.current_player] + \
                  ' now has ' + \
                  str(self.purses[self.current_player]) + \
                  ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == self.required_number_of_coins_to_win_game)


def start_test_game(game: Game) -> None:
    game.add_player('Chgfhhet')
    game.add_player('Pat')
    game.add_player('Suea')

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner:
            break


if __name__ == '__main__':
    not_a_winner = False
    game = Game()
    start_test_game(game)

