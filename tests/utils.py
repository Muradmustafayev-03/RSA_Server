import string
import random


def generate_random_message(length: int = 100) -> str:
    """
    Generate a random message of the specified length.

    :param length: The length of the message to generate.
    :type length: int

    :return: A random message of the specified length.
    :rtype: str
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
