from decorator import commander

@commander
def run(channel, user, message):
    print "chan", channel, "user", user, "message", message
    return (channel, "testzz")
