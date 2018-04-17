# -*- coding: utf-8 -*-

from faker import Faker
import random
import sys
from babel.dates import format_time

fake = Faker()

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

ZH_ABS_FORMATS = [
    'short',
    'ah点m分',
    'ah点mm分',
    'H点m分',
    'H点mm分',
]

EN_ABS_FORMATS = [

]

ZH_REL_PREFIXS = {
    '今天': '+0D',
    '明天': '+1D',
    '后天': '+2D',
    '大后天': '+3D',
    '下周': '+7D',

    '周日': 'TW7',
    '这周日': 'TW7',
    '本周日': 'TW7',
    '下周日': 'NW7',

    '{}秒后': '+{}S',
    '{}秒以后': '+{}S',
    '再过{}秒': '+{}S',
    '{}分钟后': '+{}M',
    '{}分钟以后': '+{}M',
    '再过{}分钟': '+{}M',
    '{}小时后': '+{}H',
    '{}小时以后': '+{}H',
    '再过{}小时': '+{}H',
}

EN_REL_PREFIXS = {

}

for i in range(1, 8):
    ZH_REL_PREFIXS.update({
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


def generate_date(locale):
    if locale == 'en':
        locale = 'en_US'
        formats = EN_ABS_FORMATS
        relative = EN_REL_PREFIXS
    else:
        locale = 'zh_CN'
        formats = ZH_ABS_FORMATS
        relative = ZH_REL_PREFIXS

    dt = fake.future_datetime(end_date='+30d')

    machine_readable = dt.strftime('%H:%M')
    human_readable = format_time(dt, format=random.choice(formats), locale=locale)

    r = random.random()
    if r < 0.3:
        machine_readable = 'ABS>' + machine_readable
    elif 0.3 <= r <= 0.7:
        prefix = random.choice([k for k in relative.keys() if '{}' not in k])
        machine_readable = relative[prefix] + '>' + machine_readable
        human_readable = prefix + human_readable
    else:
        rand = random.randrange(start=1, stop=60)
        prefix = random.choice([k for k in relative.keys() if '{}' in k])
        machine_readable = relative[prefix].format(rand)
        human_readable = prefix.format(rand)

    return human_readable, machine_readable, dt


def generate_dataset(n, locale):
    lines = []
    for i in range(n):
        h, m, _ = generate_date(locale)
        lines.append(m.ljust(9) + ',' + h + '\n')

    with open('dataset_{}_{}.txt'.format(locale, n), 'wt', encoding='utf-8') as f:
        f.writelines(lines)


def main(p, locale):
    fake.seed(pow(2, p))
    random.seed(pow(2, p))
    generate_dataset(pow(10, p), locale)

if __name__ == '__main__':
    p, locale = sys.argv[1:3]
    p = int(p)
    assert p >= 1
    assert locale in ('zh', 'en')
    main(p, locale)
    