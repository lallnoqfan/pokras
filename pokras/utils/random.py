from random import seed, randint


def dices(seed_value: int, count: int = 5) -> list[int]:
    """
    Generates `count` number of random numbers between 0 and 9 based on provided seed.

    Args:
        seed_value: seed value
        count: number of random numbers to generate
    """
    seed(seed_value)
    return [randint(0, 9) for _ in range(count)]
