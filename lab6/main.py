import re

import info
import obfuscate


def read_file(path):
    with open(path, 'r') as f:
        return f.readlines()


def write_in_file(path, text):
    with open(path, 'w') as f:
        f.writelines(text)


def get_tokens_from_code(code):
    tokens = []
    for line in code:
        while line:
            for pattern in info.patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    tokens.append(line[:match.end()])
                    line = line[match.end():]
                    break
    return tokens


def get_code_from_tokens(tokens):
    return ''.join(tokens)


def main():
    path = 'test.js'
    obfuscate_flags = (True, True, True)

    code = read_file(path)
    tokens = get_tokens_from_code(code)

    if obfuscate_flags[0]:
        obfuscate.remove_comments(tokens)

    if obfuscate_flags[1]:
        obfuscate.remove_debug_info(tokens)

    if obfuscate_flags[2]:
        obfuscate.rename_variables(tokens)

    code = get_code_from_tokens(tokens)
    write_in_file('result.js', code)


if __name__ == '__main__':
    main()
