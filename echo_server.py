import socket
 
HOST = '127.0.0.1'       # Hostname to bind
PORT = 9090              # Open non-privileged port 9090
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    print data
conn.close()
