import socket
from time import time


class Service():
    status = ""
    socket_timeout = 5

    def __init__(self, host, service_name, port):
        self.host = host
        self.name = service_name
        self.port = port
        self.check()

    def __repr__(self):
        return "<{}({}): {}>".format(self.port, self.name, self.status)

    def check(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(self.socket_timeout)
        try:
            client_socket.connect((self.host, self.port))
        except socket.timeout:
            self.status = "Timed out"
        except socket.error as e:
            self.status = e.strerror
        else:
            self.status = "Ok"
        finally:
            client_socket.close()


class Server():
    status = "✅ All is Ok!"
    last_update = time()
    services = []

    def __init__(self, host):
        self.host = host

    def __repr__(self):
        return "<{}({}): {}>".format(self.host, len(self.services), self.status)

    def add_service(self, name, port):
        service = Service(self.host, name, port)
        self.services.append(service)

    def update_status(self):
        fails = 0
        last_status = self.status
        for service in self.services:
            service.check()
            if service.status is not 'Ok':
                fails += 1

        if fails:
            self.status = "‼A problem has occurred"
        else:
            self.status = "✅All is Ok!"
        if fails == len(self.services):
            self.status = "❌Host seems down!"

        if last_status is not self.status:
            self.last_update = time()

    def get_status(self):
        self.update_status()
        status = self.status + "\n"
        for service in self.services:
            service_status = '☑'
            if service.status is not 'Ok':
                service_status = '✖'
            service_status += '{}({}): {}'.format(service.name, service.port, service.status)
            status += service_status + '\n'
        return status, self.last_update
