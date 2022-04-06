import string
import sys


class Caesar:

    @staticmethod
    def read_file(file_path: str) -> str:
        with open(file_path, 'r') as read_file:
            text = read_file.read()
        return text

    @staticmethod
    def write_file(file_path: str, text: str) -> None:
        with open(file_path, 'w') as write_file:
            write_file.write(text)

    @staticmethod
    def _define_alphabet(letter: str) -> tuple:
        eng_alphabet = string.ascii_lowercase
        rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

        if letter in eng_alphabet or letter in rus_alphabet:
            curr_alphabet = eng_alphabet if letter in eng_alphabet else rus_alphabet
            return curr_alphabet, len(curr_alphabet)
        else:
            return None, None

    @classmethod
    def caesar_code(cls, text: str, key: int, mode: int) -> str:
        cipher_text = []
        for letter in text:
            alphabet, power_alphabet = cls._define_alphabet(letter.lower())
            if alphabet is None:
                cipher_text.append(letter)
                continue
            if mode:
                index = (alphabet.find(letter.lower()) - key + power_alphabet) % power_alphabet
            else:
                index = (alphabet.find(letter.lower()) + key) % power_alphabet
            ciph_let = alphabet[index]
            cipher_text.append(ciph_let if letter.islower() else ciph_let.upper())
        return "".join(cipher_text)


def main(file_path: str, key: str, mode: str):
    caesar = Caesar()

    if key.isdigit() and mode.isdigit():
        try:
            text = caesar.read_file(file_path)
            cipher_text = caesar.caesar_code(text, int(key), int(mode))
            new_file_path = file_path + "_caesar_" + mode
            caesar.write_file(new_file_path, cipher_text)
            print(f"Check file {new_file_path}")
            return new_file_path
        except FileNotFoundError:
            print("File not found")
    else:
        print("The key or mode must be a number!")


if __name__ == "__main__":
    args = sys.argv[1:]
    final_path = None
    try:
        _file_path = args[0]
        _key = args[1]
        _mode = args[2]
    except IndexError:
        _file_path = input("Enter filepath: ")
        _key = input("Enter key: ")
        _mode = input("Enter mode:\n 0 - encrypt\n 1 - decrypt\n")
    finally:
        final_path = main(_file_path, _key, _mode)

    if final_path is None:
        pass
    else:
        main(final_path, _key, str(1 - int(_mode)))
