#!/usr/bin/env python
#coding=utf-8

import socket
import re

HOST = '127.0.0.1'
PORT = 8000

#Read index.html, put into HTTP response data
index_content = '''
HTTP/1.0 200 ok
Content-Type: text/html

'''

file = open('index.html', 'r')
index_content += file.read()
file.close()


#Read picture, put into HTTP response data
file = open('T-mac.jpg', 'rb')
pic_content = '''
HTTP/1.0 200 ok
Content-Type: image/jpg

'''
# print(type(pic_content))
# print(type(file.read()))
temp_doc = file.read()
# temp_doc.decode('GBK')
pic_content = pic_content.encode()
pic_content += temp_doc
# pic_content = pic_content.decode()
file.close()



#Configure socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(100)

#infinite loop
while True:
    # maximum number of requests waiting
    conn, addr = sock.accept()
    request = conn.recv(1024)
    request = request.decode()
    # print(type(request.split(' ')[1]))
    temp_1 = request.split(' ')[0]
    # method = request.split(' ')[0].decode()
    method = temp_1
    temp_2 = request.split(' ')[1]
    # print(type(request.split(' ')[1]))
    # src  = request.split(' ')[1].decode()
    src = temp_2

    print ('Connect by: ', addr)
    print ('Request is:\n', request)

    #deal wiht GET method
    if method == 'GET':
        if src == '/index.html':
            content = index_content
        elif src == '/T-mac.jpg':
            content = pic_content
        
        else:
            content = '''
HTTP/1.0 200 ok
Content-Type: text/html

<body>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>404 not found!</title>
    </head>
    <body>
        <h1>404 not found!</h1>
    </body>
    </html>
</body>
            '''
            # continue

    
    #deal with POST method
    elif method == 'POST':
        form = request.split('\r\n')
        entry = form[-1]      # main content of the request
        content = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += entry
        content += '<br /><font color="green" size="7">register successs!</p>'
    
    ######
    # More operations, such as put the form into database
    # ...
    ######
    
    else:
        continue

    if type(content).__name__ == 'str':
        content = content.encode()
    # else:
    #     content = content.decode()
    conn.sendall(content)
    
    #close connection
    conn.close()