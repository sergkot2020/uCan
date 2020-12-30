import json
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.terminal import TerminalFormatter
from datetime import datetime


def log(json_obj):
    p = json.dumps(json_obj, indent=2, sort_keys=True, ensure_ascii=False)
    print(highlight(p, JsonLexer(), TerminalFormatter()))


def print_log(name, result, text=''):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log({
        'task': name,
        'result': result,
        'msg': text,
        'data': now
    })
