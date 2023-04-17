import socket as socks
import sys

CRLF = '\r\n'

def main():
    if len(sys.argv) < 3:
        exit()
    serverHost = sys.argv[1]
    serverPort = int(sys.argv[2])
    resourcePath = sys.argv[3] if len(sys.argv) > 3 else ''
    socket = socks.socket(socks.AF_INET, socks.SOCK_STREAM)
    socket.connect(( serverHost, serverPort ))
    httpRequest = f'GET /{resourcePath} HTTP/1.1' + CRLF
    httpRequest += f'Host: {serverHost}:{serverPort}' + CRLF
    httpRequest += 'User-Agent: Simple HTTP Client (Python 3 CLI)' + CRLF + CRLF
    socket.send(httpRequest.encode())
    BUFFER_SIZE = 4096
    response = ''
    buffer = ' '
    while buffer != '':
        buffer = socket.recv(BUFFER_SIZE).decode()
        print(buffer)
        response += buffer
    print(response)

if __name__ == '__main__':
    main()