"""Interactive entry point for the Password Security Tool."""

from getpass import getpass

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


def main() -> None:
    print("Password Security Tool — local educational analysis")
    print("Use a sample password only. Your typed characters will not be displayed or saved.\n")
    password = getpass("Enter a sample password: ")
    print_result(analyze_password(password))


if __name__ == "__main__":
    main()

