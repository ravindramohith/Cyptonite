import random


def generate_distinct_random_numbers(n):
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)

    while y == x:
        y = random.randint(0, n - 1)

    return x, y

