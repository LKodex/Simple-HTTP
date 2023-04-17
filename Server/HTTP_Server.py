import socket as socks
import threading

CRLF = '\r\n'

def replyNotFoundRequest(socket):
    httpHeader = 'HTTP/1.1 404 Not Found' + CRLF + CRLF
    htmlNotFound = '<!DOCTYPE html><html><head><title>404 - Not Found</title></head><body><h1>Error 404 - Not Found</h1></body></html>'
    socket.send(httpHeader.encode())
    socket.send(htmlNotFound.encode())
    socket.send(''.encode())
    socket.close()

def replyBadRequest(socket):
    httpHeader = 'HTTP/1.1 400 Bad Request' + CRLF + CRLF
    htmlBadRequest = '<!DOCTYPE html><html><head><title>400 - Bad Request</title></head><body><h1>Error 400 - Bad Request</h1></body></html>'
    socket.send(httpHeader.encode())
    socket.send(htmlBadRequest.encode())
    socket.send(''.encode())
    socket.close()

def replyNotImplemented(socket):
    httpHeader = 'HTTP/1.1 501 Not Implemented' + CRLF + CRLF
    htmlNotImplemented = '<!DOCTYPE html><html><head><title>501 - Not Implemented</title></head><body><h1>Error 501 - Not Implemented</h1></body></html>'
    socket.send(httpHeader.encode())
    socket.send(htmlNotImplemented.encode())
    socket.send(''.encode())
    socket.close()

def replyRequestedFile(socket, filePath):
    try:
        PUBLIC_FOLDER = 'public'
        file = open(PUBLIC_FOLDER + filePath)
        data = file.read()
        httpHeader = 'HTTP/1.1 200 Ok' + CRLF + CRLF
        socket.send(httpHeader.encode())
        socket.send(data.encode())
        socket.send(''.encode())
        socket.close()
    except FileNotFoundError:
        replyNotFoundRequest(socket)

def replyRequest(socket, address):
    BUFFER_SIZE = 1024
    buffer = socket.recv(BUFFER_SIZE).decode()
    print(buffer)
    bufferTokens = buffer.split()
    METHOD_INDEX = 0
    PATH_INDEX = 1
    HTTP_VERSION_INDEX = 2
    if len(bufferTokens) < 3 or bufferTokens[HTTP_VERSION_INDEX] != 'HTTP/1.1':
        return replyBadRequest(socket)
    if bufferTokens[METHOD_INDEX] == 'GET':
        if bufferTokens[PATH_INDEX] == '/':
            bufferTokens[PATH_INDEX] = '/index.html'
        replyRequestedFile(socket, bufferTokens[PATH_INDEX])
    else:
        replyNotImplemented(socket)

def main():
    ADDRESS = 'localhost'
    PORT    = 8080
    socket = socks.socket(socks.AF_INET, socks.SOCK_STREAM)
    socket.bind((ADDRESS, PORT))
    socket.listen()
    for i in range(100):
        connection, address = socket.accept()
        responseThread = threading.Thread(target=replyRequest, args=(connection, address))
        responseThread.start()        

if __name__ == '__main__':
    main()
