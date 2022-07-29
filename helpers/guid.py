import string
from functools import reduce


def compress(guid_long: str) -> str:
    """
    Compresses a guid_long to a compressed guid.
    :param guid_long:
    :return:
    """
    guid_long = guid_long.replace('-', '').replace('{', '').replace('}', '')
    bs = [int(guid_long[i : i + 2], 16) for i in range(0, len(guid_long), 2)]

    def b64(v, l=4):
        return "".join([CHARS[(v // (64 ** i)) % 64] for i in range(l)][::-1])

    return "".join([b64(bs[0], 2)] + [b64((bs[i] << 16) + (bs[i + 1] << 8) + bs[i + 2]) for i in range(1, 16, 3)])


def expand(guid_compressed: str) -> str:
    """
    Expands a guid_compressed to a long guid.
    :param guid_compressed:
    :return:
    """
    def b64(v):
        return reduce(lambda a, b: a * 64 + b, map(lambda c: CHARS.index(c), v))

    bs = [b64(guid_compressed[0:2])]
    for i in range(5):
        d = b64(guid_compressed[2 + 4 * i : 6 + 4 * i])
        bs += [(d >> (8 * (2 - j))) % 256 for j in range(3)]
    return "".join(["%02x" % b for b in bs])


CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase + "_$"

