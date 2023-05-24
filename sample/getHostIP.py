import socket
 
def print_mynetwork_info():
    host = socket.gethostname()
    ip_addr = socket.gethostbyname(host)
    print('HOST :' + host)
    print("ip Address :" + ip_addr)    

if __name__ == '__main__':
    print_mynetwork_info()
