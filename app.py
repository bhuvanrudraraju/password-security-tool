"""Interactive entry point for the Password Security Tool."""

import sys
import termios
import tty

from password_analyzer import analyze_password


def print_result(result) -> None:
    """Print feedback without ever printing the password that was entered."""
    print(f"\nAssessment: {result.rating} ({result.score}/10)")
    print("Why:")
    for reason in result.reasons:
        print(f"- {reason}")
    print("Recommendations:")
    for recommendation in result.recommendations:
        print(f"- {recommendation}")


def read_masked_password(prompt: str = "Enter a sample password: ") -> str:
    """Read input locally while displaying a star for each typed character.

    The characters themselves are not echoed. The stars reveal password length,
    which is the trade-off for giving the user visual typing feedback.
    """
    if not sys.stdin.isatty():
        # Keeps the program usable in non-interactive environments.
        return input(prompt)

    print(prompt, end="", flush=True)
    password_characters: list[str] = []
    file_descriptor = sys.stdin.fileno()
    original_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(file_descriptor)
        while True:
            character = sys.stdin.read(1)
            if character in ("\r", "\n"):
                print()
                break
            if character == "\x03":  # Ctrl+C
                raise KeyboardInterrupt
            if character in ("\x7f", "\b"):  # Backspace
                if password_characters:
                    password_characters.pop()
                    print("\b \b", end="", flush=True)
                continue
            if character == "\x04":  # Ctrl+D
                break
            password_characters.append(character)
            print("*", end="", flush=True)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, original_settings)

    return "".join(password_characters)


def main() -> None:
    print("Password Security Tool — local educational analysis")
    print("Use a sample password only. Characters are hidden, but stars show password length.\n")
    password = read_masked_password()
    print_result(analyze_password(password))


if __name__ == "__main__":
    main()
