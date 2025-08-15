import random
import string
from wordfreq import top_n_list
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
    def __init__(self,
                 words_no: int = 6,
                 seperator: str = '-',
                 capitalize: bool = False,
    ):
        self.words_no = words_no
        self.seperator = seperator
        self.capitalize = capitalize

        self.vocabulary = top_n_list("en", self.words_no)

    def generate(self) -> str:
        password_words = self.seperator.join([random.choice(self.vocabulary) for _ in range(self.words_no)])

        if self.capitalize:
            password_words = password_words.upper()

        return password_words


class PinGenerator(PasswordGenerator):
    def __init__(self, length=16):
        self.length = length

    def generate(self):
        return ''.join([random.choice(string.digits) for _ in range(self.length)])


password = MemorablePasswordGenerator(capitalize=True)
print(password.generate())
