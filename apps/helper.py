from . import on_command

@on_command(['HELP'])
def run(robot, channel, user, tokens):
    return channel, '\n'.join(robot.docs)
