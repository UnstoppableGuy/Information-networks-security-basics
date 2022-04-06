import sys
from string import ascii_lowercase


class Vigenere:

    @classmethod
    def read_file(cls, file_path: str) -> str:
        with open(file_path, 'r') as read_file:
            text = read_file.read()
        return text

    @classmethod
    def write_file(cls, file_path: str, text: str) -> None:
        with open(file_path, 'w') as write_file:
            write_file.write(text)

    @staticmethod
    def generate_key(key: str, text: str) -> str:
        new_key = list(key)
        while len(new_key) < len(text):
            new_key.extend(key)
        return "".join(new_key)[:len(text) + 1]

    @staticmethod
    def _define_alphabet(letter: str) -> tuple:
        eng_alphabet = ascii_lowercase
        rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

        if letter in eng_alphabet or letter in rus_alphabet:
            curr_alphabet = eng_alphabet if letter in eng_alphabet else rus_alphabet
            return curr_alphabet, len(curr_alphabet)
        else:
            return None, None

    @staticmethod
    def check_key(key: str) -> bool:
        rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        if not len(set(key.lower()) - set(ascii_lowercase)):
            return True
        elif not len(set(key.lower()) - set(rus_alphabet)):
            return True
        else:
            return False

    @classmethod
    def vigenere_code(cls, text: str, key: str, mode: int) -> str:
        cipher_text = []
        i = 0
        for letter in text:
            alph, power_alph = cls._define_alphabet(letter.lower())
            if alph is None:
                cipher_text.append(letter)
                continue
            kv = alph.find(key[i].lower())
            if mode:
                index = (alph.find(letter.lower()) - kv + power_alph) % power_alph
            else:
                index = (alph.find(letter.lower()) + kv) % power_alph
            ciph_let = alph[index]
            cipher_text.append(ciph_let if letter.islower() else ciph_let.upper())
            i += 1
        return "".join(cipher_text)


def main(file_path, key, mode):
    vigenere = Vigenere()

    if mode.isdigit():
        try:
            if not vigenere.check_key(key):
                raise KeyError
            text = vigenere.read_file(file_path)
            key = vigenere.generate_key(key, text)
            cipher_text = vigenere.vigenere_code(text, key, int(mode))
            new_file_path = file_path + "_vigenere_" + mode
            vigenere.write_file(new_file_path, cipher_text)
            print(f"Check file {new_file_path}")
            return new_file_path
        except FileNotFoundError:
            print("File not found")
        except KeyError:
            print("The key is not only letters")
    else:
        print("The mode must be a number!")


if __name__ == "__main__":
    # print('args->', sys.argv[1:])
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
