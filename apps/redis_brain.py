from . import on_command


HELP_MSG = [
    '='*20,
    '%s',
    '='*20
]
BRAIN_KEY = 'brain_key'


def update_brain_key(brain, key):
    keys = brain.get(BRAIN_KEY)
    if keys:
        L = set(keys.split(','))
        if key not in L:
            L.add(key)
    else:
        L = [key]
    brain.set(BRAIN_KEY, ','.join(L))


@on_command(['memo'])
def run(robot, channel, user, tokens):
    '''전자두뇌에 무언가를 메모해둡니다'''
    token_count = len(tokens)

    if token_count < 1:
        keys = robot.brain.get(BRAIN_KEY)
        if not keys:
            keys = '메모해둔 내용이 없습니다.'
        return channel, '\n'.join(HELP_MSG) % keys

    key = tokens[0]
    if token_count == 1:
        value = robot.brain.get(key)
        message = value if value else ('%s? 처음 듣는 말이네요.' % key)
    else:
        value = tokens[1]
        update_brain_key(robot.brain, key)
        robot.brain.set(key, value)
        message = '메모해두었습니다.\n%s: %s' % (key, value)
    return channel, message
