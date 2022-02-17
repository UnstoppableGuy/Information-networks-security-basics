import random
import functools

import des.const as dc


def get_binary(num, cnt=0):
    bits = []
    while num:
        bits.append(num & 1)
        num >>= 1
    for _ in range(cnt - len(bits)):
        bits.append(0)
    bits.reverse()
    return bits


def get_decimal(bits):
    num = 0
    for bit in bits:
        num = (num << 1) + bit
    return num


def get_by_table(table, seq):
    return [seq[pos - 1] for pos in table]


def gen_keys(key):
    byts = [[] for _ in range(8)]
    for i, bit in enumerate(key):
        byts[i // 7].append(bit)
    for byt in byts:
        app = functools.reduce(lambda p, n: p ^ n, byt, 0)
        byt.append(app ^ 1)

    nk = functools.reduce(lambda p, n: p + n, byts, [])

    ci = get_by_table(dc.C0, nk)
    di = get_by_table(dc.D0, nk)

    keys = []
    for shift in dc.SH:
        ci = ci[shift:] + ci[:shift]
        di = di[shift:] + di[:shift]
        full_key = ci + di
        keys.append(get_by_table(dc.K, full_key))

    return keys


def f(block, key):
    block = get_by_table(dc.E, block)
    block = [block[i] ^ key[i] for i in range(len(block))]

    s_res = []
    for block_id in range(8):
        block_start = block_id * 6
        a = (block[block_start] << 1) + block[block_start+5]
        b = 0
        for i in range(1, 5):
            b += block[block_start + i] << (4 - i)

        s_res += get_binary(dc.S[block_id][a][b], 4)

    return get_by_table(dc.P, s_res)


def encrypt(message, key):
    keys = gen_keys(get_binary(key, 56))

    result = bytearray()
    for bs in range(0, len(message), 8):
        block = []
        for i in range(bs, bs + 8):
            block.extend(get_binary(message[i], 8))

        d_ip = get_by_table(dc.IP, block)
        dl, dr = d_ip[:32], d_ip[32:]
        for i in range(16):
            new_dl = dr
            f_res = f(dr, keys[i])
            new_dr = [f_res[pos] ^ dl[pos] for pos in range(len(f_res))]
            dl, dr = new_dl, new_dr

        new_d = dl + dr
        d_res = get_by_table(dc.IP_n, new_d)
        for i in range(0, 64, 8):
            result.append(get_decimal(d_res[i: i + 8]))

    return result


def decrypt(message, key):
    keys = gen_keys(get_binary(key, 56))

    result = bytearray()
    for bs in range(0, len(message), 8):
        block = []
        for i in range(bs, bs + 8):
            block.extend(get_binary(message[i], 8))

        d_ip = get_by_table(dc.IP, block)
        dl, dr = d_ip[:32], d_ip[32:]
        for i in range(15, -1, -1):
            new_dr = dl
            f_res = f(dl, keys[i])
            new_dl = [f_res[pos] ^ dr[pos] for pos in range(len(f_res))]
            dl, dr = new_dl, new_dr

        new_d = dl + dr
        d_res = get_by_table(dc.IP_n, new_d)
        for i in range(0, 64, 8):
            result.append(get_decimal(d_res[i: i + 8]))

    return result


def get_random_key():
    return random.randrange(0, 1 << 56, 1)
