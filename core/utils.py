import random
import re
from pypinyin import lazy_pinyin


BRIGHT_COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#FF9FF3', '#54A0FF',
    '#5F27CD', '#00D2D3', '#FF9F43', '#10AC84', '#EE5A24',
    '#A3CB38', '#1289A7', '#D980FA', '#B53471', '#FFC312'
]


def get_random_color():
    return random.choice(BRIGHT_COLORS)


def parse_student_text(text):
    text = text.strip()
    if not text:
        return []
    parts = re.split(r'[\s,，、\n\r\t]+', text)
    seen = set()
    result = []
    for p in parts:
        name = p.strip()
        if name and name not in seen:
            seen.add(name)
            result.append(name)
    return result


def match_student(student_name, keyword):
    if not keyword:
        return True
    keyword = keyword.strip().lower()
    if not keyword:
        return True
    if keyword in student_name.lower():
        return True
    try:
        py = ''.join(lazy_pinyin(student_name)).lower()
        py_init = ''.join([p[0] for p in lazy_pinyin(student_name)]).lower()
        if keyword in py or keyword in py_init:
            return True
    except Exception:
        pass
    return False