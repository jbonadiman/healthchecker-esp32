from uping import ping

five_minutes = const(300000)

config = {
    'network_hc_ping': 'https://hc-ping.com/<GUID>',

    'server_ping': '<LOCALIP>',
    'server_hc_ping': 'https://hc-ping.com/<GUID>',
}

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    try:
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        while True:
            data = s.recv(100)
            if not data:
                break
    finally:
        s.close()

def ping_network(t):
    try:
        print(f"Pinging {config['network_hc_ping']}...")
        http_get(config['network_hc_ping'])
    except Exception as exc:
        print(f'An error ocurred: {str(exc)}')

def ping_local_server(t):
    try:
        print(f"Pinging {config['server_ping']}...")
        result = ping(config['server_ping'], quiet=True)
        if result[0] == result[1]:
            http_get(config['server_hc_ping'])
    except Exception as exc:
        print(f'An error ocurred: {str(exc)}')

def main():
    from machine import Timer

    timer_network = Timer(0)
    timer_network.init(
            period=five_minutes,
            mode=Timer.PERIODIC,
            callback=ping_network
    )

    timer_server = Timer(1)
    timer_server.init(
            period=five_minutes,
            mode=Timer.PERIODIC,
            callback=ping_local_server
    )
