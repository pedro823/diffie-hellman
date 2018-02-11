from socket import *
import base64
import threading
from base.constants import ALLOWED_METHODS, CHUNK_SIZE, SEPARATOR
from base.base_class import BaseClass
import base.error as error

class Messenger(BaseClass):
    """ Class responsible for handling sockets inside diffie-hellman protocol. """

    def __init__(self, remote_addr='', port=9889, listen=False, **kwargs):
        BaseClass.__init__(self, **kwargs)
        self.socket = socket(AF_INET, SOCK_STREAM)
        if listen:
            self.__create_socket_listen(remote_addr, port)
        else:
            self.__create_socket_connect(remote_addr, port)

    def __getattr__(self, attribute):
        """
            Another method of calling send_msg.
            method is taken as first part of the message.
            e.g. Messenger.recv_num(b'2', b'3') == Messenger.send_msg('recv_num', b'2', b'3')
        """

        def missing_method(*args, **kwargs):
            if kwargs.get('log'):
                self.logger.log(kwargs.get('log_priority') or 0, kwargs['log'])
            return self.send_msg(str(attribute), *args)
        return missing_method

    def accept_connection(self, connect_function):
        """
            Starts accepting connections from the socket.
            If a connection is established, sends arguments
            conn, addr to connect_function.
        """
        self.socket.setblocking(True)
        while True:
            conn, addr = self.socket.accept()
            flag = connect_function(conn, addr)
            if flag:
                break

    def receive(self):
        """
            Receives a message from the connected socket until next separator.
            Returns a bytearray of the message.
        """
        # Receives data in chunks
        msg = bytearray()
        b_separator = SEPARATOR.encode('utf-8')
        while True:
            chunk = self.socket.recv(CHUNK_SIZE)
            if chunk == b'':
                raise error.ConnectionError('Connection broken')
            msg += chunk
            if b_separator in chunk:
                break
        if msg[msg.rfind(SEPARATOR) + len(SEPARATOR):] != b'':
            self.logger.log(2, "WARN -- Discarding messages after SEPARATOR: %s" % msg.decode('uft-8'))
        encoded_msg = msg[0:msg.find(b_separator)] # strips separator and other messages
        return base64.b64decode(encoded_msg)

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
                raise error.MessengerError('msg_list must be a list of arguments to pass to send_msg')

    def send_msg(self, method, *args):
        """ Sends a single message following our Diffie-hellman protocol """
        if method not in ALLOWED_METHODS:
            raise error.MessengerError('method not allowed')

        full_message = bytearray(method, encoding='utf-8')
        for i in args:
            if type(i) not in [bytes, bytearray]:
                raise error.MessengerError('Not all arguments are bytes: %s' % i)
            full_message += i
        full_message += SEPARATOR.encode('utf-8')

        # Message is b64 encoded
        encoded_message = base64.b64encode(full_message)
        max_length = len(encoded_message)
        i = 0
        while i < max_length:
            # Sends message in chunks
            sent = self.socket.send(encoded_message[i:])
            if sent == 0:
                raise error.ConnectionError('Connection broken')
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
            raise error.MessengerError('Connection timed out.')
