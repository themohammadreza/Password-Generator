import random
import string
import os
from abc import ABC, abstractmethod


class PasswordGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass

class RandomPasswordGenerator(PasswordGenerator):
    def __init__(self, length=16, include_uppercase=False, include_numbers=True, include_symbols=False) -> None:
        self.length = length
        self.characters = string.ascii_lowercase

        if include_uppercase:
            self.characters += string.ascii_uppercase
        if include_numbers:
            self.characters += string.digits
        if include_symbols:
            self.characters += string.punctuation

    def generate(self):
        return ''.join([random.choice(self.characters) for _ in range(self.length)])


class MemorablePasswordGenerator(PasswordGenerator):
    def __init__(
        self,
        words_no: int = 4,
        separator: str = '-',  # Fixed spelling
        capitalize: bool = False,
    ):
        self.words_no = words_no
        self.separator = separator  # Fixed spelling
        self.capitalize = capitalize
        self.vocabulary = self._load_wordlist()

    def _load_wordlist(self) -> list[str]:
        wordlist_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "eff_large_wordlist.txt")
        )
        with open(wordlist_path, "r") as f:
            return [line.split()[1] for line in f]

    def generate(self) -> str:
        password_words = self.separator.join(
            random.choice(self.vocabulary) 
            for _ in range(self.words_no)
        )
        
        return password_words.upper() if self.capitalize else password_words


class PinGenerator(PasswordGenerator):
    def __init__(self, length=16):
        self.length = length

    def generate(self):
        return ''.join([random.choice(string.digits) for _ in range(self.length)])


password = MemorablePasswordGenerator()
print(password.generate())
