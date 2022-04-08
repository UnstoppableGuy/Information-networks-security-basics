import random
import re
import string

import info


def remove_comments(tokens):
    new_tokens = []
    comment_view = 0
    for token in tokens:
        if comment_view == 1 and token == '\n' or comment_view == 2 and token == '*/':
            comment_view = 0

        if comment_view == 0:
            if token == '//':
                comment_view = 1
            elif token == '/*':
                comment_view = 2
            elif token != '*/':
                new_tokens.append(token)

    tokens[:] = new_tokens[:]


def remove_debug_info(tokens):
    new_tokens = []
    is_console, brackets_cnt = False, 0
    for token in tokens:
        if is_console:
            if token == '(':
                brackets_cnt += 1
            if token == ')':
                brackets_cnt -= 1
                if brackets_cnt == 0:
                    is_console = False
        elif token == 'console':
            is_console = True
        else:
            new_tokens.append(token)

    tokens[:] = new_tokens[:]


def rename_variables(tokens):
    code_variables = set()
    for token in tokens:
        if (
            re.match(r'\b[A-Za-z_]\w*', token, re.IGNORECASE) and not re.match(r'\".*\"', token)
            and token not in info.keywords
        ):
            code_variables.add(token)
    new_variables = [''.join([random.choice(string.ascii_letters) for _ in range(random.randint(5, 15))])
                     for _ in range(len(code_variables))]
    replacing_dict = dict(zip(code_variables, new_variables))

    new_tokens = []
    for token in tokens:
        if token in replacing_dict:
            new_tokens.append(replacing_dict[token])
        else:
            new_tokens.append(token)

    tokens[:] = new_tokens[:]
