# coding=utf-8
# 2015-11-19
# yaoms
# emoji 表情符号转义
"""
emoji 表情 编码/解码 类
    encode_string_emoji(string)
    decode_string_emoji(string)
"""
import re


def __is_normal_char(c):
    """
    判断字符是不是普通字符, 非普通字符, 认定为 emoji 字符
    :param c:
    :return: 普通字符 True, Emoji 字符 False
    """
    i = ord(c)
    return (
        i == 0x0 or
        i == 0x9 or
        i == 0xA or
        i == 0xD or
        (i >= 0x20 and i <= 0xD7FF) or
        (i >= 0xE000 and i <= 0xFFFD) or
        (i >= 0x10000 and i <= 0x10FFFF)
    )

def __emoji_encode(c):
    """
    Emoji 字符编码
    :param c:
    :return: Emoji 代码
    """
    if __is_normal_char(c):
        return c
    else:
        return "[emj]%s[/emj]" % format(ord(c), 'x')

def __emoji_decode(code):
    """
    解码 Emoji 代码
    :param code:
    :return: Emoji 字符
    """
    m = re.match(r"\[emj\]([a-fA-F0-9]+)\[/emj\]", code)
    if m:
        h = m.group(1)
        return unichr(int(h, 16))


def encode_string_emoji(string):
    """
    遍历并转换其中的 Emoji 字符
    :param string:
    :return: Emoji 代码字符串
    """
    return "".join([__emoji_encode(c) for c in string])

def decode_string_emoji(string):
    """
    解码 Emoji 代码 字符串
    :param string:
    :return: 含有 Emoji 字符的字符串
    """
    p = re.compile(r"\[emj\][a-fA-F0-9]+\[/emj\]")
    new_string = ""
    n_start = 0
    for m in p.finditer(string):
        new_string += string[n_start:m.start()] + \
                      __emoji_decode(string[m.start():m.end()])
        n_start = m.end()

    if n_start < len(string):
        new_string += string[n_start:]

    return new_string

if __name__ == '__main__':
    __string_raw = open("/tmp/emoji.txt").read().decode("utf-8")
    print __string_raw
    __s1 = encode_string_emoji(__string_raw)
    print __s1
    __s2 = decode_string_emoji(__s1)
    print __s2