import random
import string

MAX_LENGHT_PIN = 3


def generate_pin():
    return ''.join(
        random.choice(f"{string.ascii_uppercase}{string.digits}") for _ in range(MAX_LENGHT_PIN)
    )
