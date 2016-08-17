import os

from settings import API_TOKEN, INIT_CHANNEL
from slackclient import SlackClient

class Robot(object):
    def __init__(self):
        self.client = SlackClient(API_TOKEN)
        self._connected = False

    @staticmethod
    def throw_err(data):
        raise RuntimeError(data)

    def _connect(self):
        if self._connected:
            return True

        if self.client.rtm_connect():
            self._connected = True
            return True
        else:
            return False

    def _join_channel(self):
        if not self._connected:
            return False

        for channels in INIT_CHANNEL:
            print "\t- Joining a channel: %s" % channels
            self.client.server.join_channel(channels)

        return True

    def _extract(self, message):
        if len(message) != 1:
            return False

        message = message[0]
        if not message.has_key('type') or message['type'] != 'message':
            return False

        if not message.has_key('channel'):
            return False

        if not message.has_key('user'):
            return False

        return {'user': message['user'], 'text': message['text'], 'channel': message['channel']}

    def _parse_message(self, message):
        """
        !git aaaa bbbb
        """
        msg_body = message.split(" ")
        if not msg_body[0].startswith("!"):
            return False

        return {'cmd': msg_body[0][1:], 'arg': msg_body[1:]}

    def handle_message(self, channel, user, message):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        msg = self._parse_message(message)
        if msg:
            """
            vulnerable? i dont give a shit though
            """
            mod_name = "cmd_%s.py" % (msg['cmd'])
            mod_path = os.path.join(curr_dir, mod_name)
            if os.path.exists(mod_path):
                module = __import__(mod_name[:-len(".py")])
                module.run(self, channel, user, msg['arg'])
                return True
            else:
                print "\t- The module %s doesn't exist on the current directory" % mod_name

        return False

    def run(self):
        if self._connect():
            print "[+] Slackbot has been sucessfully connected!"
        else:
            self.throw_err("[-] Slackbot failed to attach the slackbot existing over the channels....")

        if self._join_channel():
            print "[+] Slackbot joined the initially given channels"
        else:
            self.throw_err("[-] Slackbot failed to join the initially given channels....")

        while 1:
            message = self._extract(self.client.rtm_read())
            if message:
                if message['user'] != u"BLIND":
                    continue

                if not self.handle_message(message['channel'], message['user'], message['text']):
                    print "[-] Failed to execute the command:", "\"", message['text'], "from the user", message['user'], "on the channel", message['channel'], "\""

rbt = Robot()
rbt.run()
