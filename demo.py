"""Run safe, fictional examples for a classroom or portfolio demonstration."""

from app import print_result
from password_analyzer import analyze_password


TEST_CASES = {
    "Common password": "password",
    "Short repeated password": "aaa111",
    "Predictable sequence": "Qwerty1234",
    "Longer mixed example": "Maple!River7Cloud",
    "Passphrase-style example": "Cedar-Moon-47!Harbor",
}


def main() -> None:
    print("Password Security Tool — sample-only demonstration")
    for name, sample_password in TEST_CASES.items():
        print(f"\n{name}")
        print_result(analyze_password(sample_password))


if __name__ == "__main__":
    main()

