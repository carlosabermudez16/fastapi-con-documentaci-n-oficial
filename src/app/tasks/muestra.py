from typing import Annotated


def process_items(items: list[str], items_t: tuple[int, int, str], item_s: set[bytes]):
    for item in items:
        print(item)
    return items_t, item_s


def process_items_2(prices: dict[str, float]):
    for item_name, item_price in prices.items:
        print(item_name)
        print(item_price)


def process_items_3(item: int | str):
    print(item)


def say_hi(name: str | None = None):
    if name:
        print(f"Hey {name}!")
    else:
        print("Hello world")


def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id
