
from collections import namedtuple

msg = namedtuple('msg', ['name', 'text'])
a = msg('yy', 'ntecn {} dfbdfb')
a.text = a.text.format('KKKK')

print(a.text)

examp = {
    "temp": [
        1,
        1,
        0,
        1,
        1
    ],
    "done_step": 14,
    "message_id": 755,
    "need_to_remove": False
}