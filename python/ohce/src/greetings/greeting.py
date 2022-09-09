import typing as tp


def get_greeting_for_user(time_of_current_greeting: int, greeting_schedule: tp.Callable[[int], str], name: str) -> str:
    greeting_for_current_time = greeting_schedule(time_of_current_greeting)
    return greeting_for_current_time.format(name)
