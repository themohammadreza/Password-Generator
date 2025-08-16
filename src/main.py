import random
import string
import os
from abc import ABC, abstractmethod


class PasswordGenerator(ABC):
    """Base abstract class for password generators.
    
    Provides a common interface for all password generator implementations.
    """
    
    @abstractmethod
    def generate(self) -> str:
        """Generate a password.
        
        Returns:
            A string containing the generated password.
        """
        pass


class RandomPasswordGenerator(PasswordGenerator):
    """Generates random passwords with configurable character sets.
    
    Args:
        length: Length of the password to generate.
        include_uppercase: Whether to include uppercase letters.
        include_numbers: Whether to include numbers.
        include_symbols: Whether to include special symbols.
    """

    def __init__(self, length: int = 16, include_uppercase: bool = False, 
                 include_numbers: bool = True, include_symbols: bool = False) -> None:
        self.length = length
        self.characters = string.ascii_lowercase

        if include_uppercase:
            self.characters += string.ascii_uppercase
        if include_numbers:
            self.characters += string.digits
        if include_symbols:
            self.characters += string.punctuation

    def generate(self) -> str:
        """Generate a random password.
        
        Returns:
            A random string of specified length using the configured character set.
        """
        return ''.join([random.choice(self.characters) for _ in range(self.length)])


class MemorablePasswordGenerator(PasswordGenerator):
    """Generates memorable passwords using dictionary words.
    
    Args:
        words_no: Number of words to use in the password.
        separator: Character used to join the words.
        capitalize: Whether to capitalize the generated password.
    """

    def __init__(
        self,
        words_no: int = 4,
        separator: str = '-',
        capitalize: bool = False,
    ) -> None:
        self.words_no = words_no
        self.separator = separator
        self.capitalize = capitalize
        self.vocabulary = self._load_wordlist()

    def _load_wordlist(self) -> list[str]:
        """Load the word list from file.
        
        Returns:
            List of words from the EFF large wordlist.
        """
        wordlist_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "eff_large_wordlist.txt")
        )
        with open(wordlist_path, "r") as f:
            return [line.split()[1] for line in f]

    def generate(self) -> str:
        """Generate a memorable password.
        
        Returns:
            A string of dictionary words joined by the separator.
        """
        password_words = self.separator.join(
            random.choice(self.vocabulary) 
            for _ in range(self.words_no)
        )
        return password_words.upper() if self.capitalize else password_words


class PinGenerator(PasswordGenerator):
    """Generates numeric PIN codes.
    
    Args:
        length: Length of the PIN to generate.
    """

    def __init__(self, length: int = 6) -> None:
        self.length = length

    def generate(self) -> str:
        """Generate a PIN code.
        
        Returns:
            A string of random digits of specified length.
        """
        return ''.join([random.choice(string.digits) for _ in range(self.length)])


if __name__ == "__main__":
    """Command-line interface for the password generators.
    
    Allows users to generate different types of passwords with custom parameters.
    """
    while True:
        password_type = input("Enter password type (random, memorable, pin) or 'q' to quit: ")
        password_type = password_type.strip().lower()
        if password_type == "q":
            break
        elif password_type == "random":
            length = int(input("Enter password length (default 6): ") or 6)
            include_uppercase = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
            include_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
            include_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'
            password = RandomPasswordGenerator(length, include_uppercase, include_numbers, include_symbols)
        elif password_type == "memorable":
            words_no = int(input("Enter number of words (default 4): ") or 4)
            capitalize = input("Capitalize words? (y/n): ").strip().lower() == 'y'
            password = MemorablePasswordGenerator(words_no, capitalize=capitalize)
        elif password_type == "pin":
            length = int(input("Enter PIN length (default 6): ") or 6)
            password = PinGenerator(length)
        else:
            print("Invalid password type.")
            continue

        print(password.generate())
