from socket import *
import thread
from base.constants import ALLOWED_METHODS
from base.error import Error
from base.base_class import BaseClass

class Messenger(BaseClass):

    def __init__(self, remote_addr, port=9889, logfile='stdout'):
        BaseClass.__init__(self, logfile)
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.connect((remote_addr, port))
        except

    def __getattr__(self, attribute):
        def missing_method(*args, **kwargs):
            if kwargs.get('log'):
                self.logger.log(kwargs.get('log_priority') or 0, kwargs['log'])
            return self.__send_msg(str(attribute), *args)
        return missing_method

    def accept_connection(self):
        pass

    def receive(self):
        pass

    def __send_msg(self, method, *args):
        self.socket
        if method not in ALLOWED_METHODS:
            raise Error.MessengerError('method not allowed')
        full_message = method + ' ' + ' '.join(args) + '\n\n'
        max_length = len(full_message)
        i = 0
        while i < max_length:
            # Sends message in chunks
            sent = self.sock.send(full_message[i:])
            if sent == 0:
                raise Error.ConnectionError('Connection broken')
            i += sent
