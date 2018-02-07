from socket import *
from base.constants import ALLOWED_METHODS
from base.error import Error
from base.base_class import BaseClass

class Messenger(BaseClass):
    """ Class responsible for handling sockets inside diffie-hellman protocol. """

    def __init__(self, remote_addr='', port=9889, listen=False, logfile='stdout'):
        BaseClass.__init__(self, logfile)
        self.socket = socket(AF_INET, SOCK_STREAM)
        if listen:
            self.__create_socket_listen(remote_addr, port)
        else:
            self.__create_socket_connect(remote_addr, port)

    def __getattr__(self, attribute):
        def missing_method(*args, **kwargs):
            if kwargs.get('log'):
                self.logger.log(kwargs.get('log_priority') or 0, kwargs['log'])
            return self.__send_msg(str(attribute), *args)
        return missing_method

    def accept_connection(self, connect_function):
        """
            Starts accepting connections from the socket.
            If a connection is established, sends arguments
            conn, addr to connect_function.
        """
        self.socket.setblocking(True)
        conn, addr = self.socket.accept()


    def receive(self):
        """ Receives a message from the connected socket. """
        # Receives data in chunks
        chunks = []
        msg = ''
        while True:
            chunk = self.socket.recv(CHUNK_SIZE)
            splitted_chunk = chunk.split(SEPARATOR)
        return chunks

    def send_mult_msg(self, msg_list):
        """
            Sends multiple messages through send_msg.
            args:
            + msg_list
            A list of lists of arguments to be passed to messenger.send_msg().
            ex: [ ['sync'], ['recv_num', 2, 3] ]
        """
        for msg in msg_list:
            try:
                self.send_msg(msg[0], *msg[1:])
            except TypeError:
                raise Error.MessengerError('msg_list must be a list of arguments to pass to send_msg')

    def send_msg(self, method, *args):
        """ Sends a single message following our Diffie-hellman protocol """
        if method not in ALLOWED_METHODS:
            raise Error.MessengerError('method not allowed')

        clean_args = []
        for arg in args:
            # Auto-raises error if str() doesn't work
            clean_arg = str(arg)
            if SEPARATOR in clean_arg:
                raise Error.SecurityError('Separator found in arg: ' + arg
                                          + '\nUse messenger.send_mult_msg if that is intended.')
            clean_args.append(clean_arg)

        full_message = method + ' ' + ' '.join(clean_args) + SEPARATOR
        max_length = len(full_message)
        i = 0
        while i < max_length:
            # Sends message in chunks
            sent = self.sock.send(full_message[i:])
            if sent == 0:
                raise Error.ConnectionError('Connection broken')
            i += sent

    def close(self):
        """ Closes socket connection. """
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()

    # Private

    def __create_socket_listen(self, remote_addr, port):
        self.socket.bind((remote_addr, port))
        self.socket.listen(10)

    def __create_socket_connect(self, remote_addr, port):
        try:
            self.socket.connect((remote_addr, port))
        except timeout:
            raise Error.MessengerError('Connection timed out.')
