import socket


def scan_ports(domain):
    ports = [21,22,25,53,80,110,143,443,3306,8080,8443]

    open_ports = []

    ip = socket.gethostbyname(domain)

    for port in ports:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(1)

        if sock.connect_ex((ip, port)) == 0:
            open_ports.append(port)

        sock.close()

    return open_ports