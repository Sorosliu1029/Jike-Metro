# -*- coding: utf-8 -*-

from faker import Faker
import random
from babel.dates import format_time

fake = Faker()
fake.seed(1234)
random.seed(1234)

TRANS_TABLE = str.maketrans({
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '七',
    '8': '八',
    '9': '九',
    '0': '零'
})

ABS_FORMATS = [
    'short',
    'medium',
    'ah点m分',
    'ah点m分s秒',
    'ah点mm分',
    'ah点mm分ss秒',
    'H点m分',
    'H点m分s秒',
    'H点mm分',
    'H点mm分ss秒',
]

REL_PREFIXS = {
    '今天': '+0D',
    '明天': '+1D',
    '后天': '+2D',
    '大后天': '+3D',
    '下周': '+7D',

    '周日': 'TW7',
    '这周日': 'TW7',
    '本周日': 'TW7',
    '下周日': 'NW7',

    '?秒后': '+?S',
    '?秒以后': '+?S',
    '再过?秒': '+?S',
    '?分钟后': '+?M',
    '?分钟以后': '+?M',
    '再过?分钟': '+?M',
    '?小时后': '+?H',
    '?小时以后': '+?H',
    '再过?小时': '+?H',
}

for i in range(1, 8):
    REL_PREFIXS.update({
        '周{}'.format(str(i).translate(TRANS_TABLE)): 'TW{}'.format(i),
        '这周{}'.format(str(i).translate(TRANS_TABLE)): 'TW{}'.format(i),
        '本周{}'.format(str(i).translate(TRANS_TABLE)): 'TW{}'.format(i),
        '下周{}'.format(str(i).translate(TRANS_TABLE)): 'NW{}'.format(i),
    })


def translate_two_digits(digits):
    digits = str(digits)
    assert 1 <= len(digits) <= 2
    if len(digits) == 1:
        return digits.translate(TRANS_TABLE)
    else:
        tens = digits[0].translate(TRANS_TABLE) if 2 <= int(digits[0]) <= 9 else ''
        units = digits[1].translate(TRANS_TABLE) if int(digits[1]) != 0 else ''
        return '{}十{}'.format(tens, units)


def generate_date():
    dt = fake.future_datetime(end_date='+30d')

    machine_readable = dt.strftime('%H:%M:%S')
    human_readable = format_time(dt, format=random.choice(ABS_FORMATS), locale='zh_CN')

    r = random.random()
    if r < 0.3:
        machine_readable = 'ABS>' + machine_readable
    elif 0.3 <= r <= 0.7:
        prefix = random.choice([k for k in REL_PREFIXS.keys() if '?' not in k])
        machine_readable = REL_PREFIXS[prefix] + '>' + machine_readable
        human_readable = prefix + human_readable
    else:
        prefix = random.choice([k for k in REL_PREFIXS.keys() if '?' in k])
        machine_readable = REL_PREFIXS[prefix]
        human_readable = prefix

    return human_readable, machine_readable, dt


def generate_dataset(m):
    lines = []
    for i in range(m):
        h, m, _ = generate_date()
        lines.append(h + ',' + m + '\n')

    with open('dataset.txt', 'wt', encoding='utf-8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    generate_dataset(int(1e3))
