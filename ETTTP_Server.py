import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg

if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM) # create TCP welcoming socket
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    print('The server is ready to receive') 
    
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()

        start = random.randrange(0,2)  # select random to start - 0, 1 중에 하나
        '''
            Send start move information to peer
            start가 1이면 client가 게임 시작, 0이면 server가 게임 시작
        '''
        if start == 0:
            start_msg = 'SEND ETTTP/1.0\r\nHost:' + client_addr[0] + '\r\nFirst-Move:ME\r\n\r\n'
            client_socket.send(start_msg.encode()) # server가 게임 시작
        elif start == 1:
            start_msg = 'SEND ETTTP/1.0\r\nHost:' + client_addr[0] + '\r\nFirst-Move:YOU\r\n\r\n'
            client_socket.send(start_msg.encode()) # client가 게임 시작

        # ACK를 받음 - ACK가 옳은 경우, 게임 시작
        ack_msg = client_socket.recv(1024).decode()
        
        if check_msg(ack_msg, client_addr):
            
            line_num = ack_msg.split('\r\n') # \r\n을 기준으로 line 구분
            first_player = line_num[2].split(':')[1] # YOU, ME
            
            if ((start == 0 and first_player == 'ME') or (start == 1 and first_player == 'YOU')):
                break
            else:
                exit
        
        # === game start ===        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        break
    server_socket.close()
    
    