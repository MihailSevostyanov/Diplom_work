from random import random


def send_sms(phone):
    random_code = random.randint(100000, 999999)
    return random_code
