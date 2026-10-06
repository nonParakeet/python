from getpass import getpass
from itertools import product
from string import ascii_lowercase, digits


CHARACTERS = ascii_lowercase + digits
MAX_LENGTH = 4


def crack_password(target: str, charset: str = CHARACTERS, max_length: int = MAX_LENGTH) -> int | None:
    if not charset:
        raise ValueError("charset must not be empty")
    if max_length < 1:
        raise ValueError("max_length must be at least 1")

    attempts = 0
    for length in range(1, max_length + 1):
        for characters in product(charset, repeat=length):
            attempts += 1
            if "".join(characters) == target:
                return attempts
    return None


def main() -> None:
    print("Local demonstration only: this does not connect to accounts or services.")
    print("Search alphabet: lowercase letters and digits; maximum length: 4.")
    target = getpass("Enter a password to test: ")

    if not target:
        print("The password cannot be empty.")
        return

    attempts = crack_password(target)
    if attempts is None:
        print("Not found within the configured alphabet and length limit.")
    else:
        print(f"Found after {attempts:,} guesses.")


if __name__ == "__main__":
    main()