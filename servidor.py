#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
from socket import socket as Socket
from os import curdir, sep

# A simple web server

# Issues:
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more

max_user = 10

def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=8020, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    #with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # The socket stays connected even after this script ends. So in order
    # to allow the immediate reuse of the socket (so that we can kill and
    # re-run the server while debugging) we set the following option. This
    # is potentially dangerous in real code: in rare cases you may get junk
    # data arriving at the socket.
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    endpoint = ('', args.port)

    ss.bind(endpoint)
    ss.listen(max_user)

    print("server ready")

    while True:

         cs = ss.accept()[0] 
         request = cs.recv(1024).decode('ascii')
         request_descompuesto = request.split('\n')
         print("%s" %request_descompuesto[0])
         reply = http_handle(request_descompuesto[0])
         cs.send(reply)
         cs.close()
	 #cs.send(reply.encode('ascii'))

         print("\n\nReceived request")
         print("======================")
         print(request.rstrip())
         print("======================")


         print("\n\nReplied with")
         print("======================")
         print(reply.rstrip())
         print("======================")


    return 0


def http_handle(request_string):
    """Given a http requst return a response
    Both request and response are unicode strings with platform standard
    line endings.
    """
    
    solicitud = request_string.split(' ')
    assert not isinstance(request_string, bytes)

    # Fill in the code to handle the http request here. You will probably want
    # to write additional functions to parse the http request into a nicer data
    # structure (eg a dict), and to easily create http responses.

    # esta funcion DEBE RETORNAR UNA CADENA que contenga el recurso (archivo)
    # que se consulta desde un navegador e.g. http://localhost:2080/index.html
    # En el ejemplo anterior se esta solicitando por el archivo 'index.html'
    # Referencias que pueden ser de utilidad
    # - https://www.acmesystems.it/python_http, muestra como enviar otros
    #                                           archivos ademas del HTML
    # - https://goo.gl/i7hJYP, muestra como construir un mensaje de respuesta
    #                          correcto en HTTP
    try:
        sendReply = False
        recurso = solicitud[1].split('.')

        if recurso[-1] == 'html':
            mimetype = 'text/html'
            sendReply = True
        if recurso[-1] == 'jpg':
            mimetype = 'image/jpeg'
            sendReply = True
        if recurso[-1] == 'js':
            mimetype = 'application/javascript'
            sendReply = True
        if recurso[-1] == 'gif':
            mimetype = 'image/gif'
            sendReply = True
        if recurso[-1] == 'css':
            mimetype = 'text/css'
            sendReply = True

        if sendReply == True:
            #Open the static file requested and send it
            print("RUTA: " + curdir + solicitud[1])
            f = open(curdir + solicitud[1], 'rb') 
            data = f.read()
            headers = "HTTP/1.1 200 OK\n" + "Content-Type: " + mimetype + "\n" + "Connection: close\n" + "\n"
            answer = bytes(headers,'UTF-8') + data
            f.close()
            return answer

    except IOError:
        f = open(curdir + "/404.html")
        data = f.read()
        headers = "HTTP/1.1 404 Error\n" + "Content-Type: text/html\n" + "Connection: close\n" + "\n"
        answer = headers + data
        f.close()
        return answer

if __name__ == "__main__":
    sys.exit(main())
