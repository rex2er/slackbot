from functools import wraps

def commander(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        robot, channel, user, message = args
        channel, message = func(channel, user, message)
        if channel and message:
            robot.client.rtm_send_message(channel, message)
            return message

        return True#func(*args, **kwargs)

    return wrapper
