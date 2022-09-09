import typing as tp


def get_answer_on_user_message(
        message: str,
        special_sentence_for_palindrome: str = r"¡Bonita palabra!"
) -> tp.Union[str, list[str]]:
    reverted_user_message = message[::-1]
    if reverted_user_message == message:
        return [reverted_user_message, special_sentence_for_palindrome]
    return reverted_user_message
