import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg

if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT) # (127.0.0.1, 12000)
    
    with socket(AF_INET, SOCK_STREAM) as client_socket:

        client_socket.connect(SERVER_ADDR)
        
        # 서버로부터 누가 먼저 시작할지 메시지 받음
        recv_msg = client_socket.recv(SIZE).decode()

        if check_msg(recv_msg, SERVER_IP): # ETTTP format인지 검사

            line_num = recv_msg.split('\r\n') 
            first_player = line_num[2].split(':')[1]

            if first_player == 'YOU':
                start = 1 # client가 게임 시작
            else:
                start = 0 # server가 게임 시작
    
            # ACK 전송
            line_num = recv_msg.split('\r\n')
            player = line_num[2].split(':')[1] # 서버가 보낸 메시지에서 YOU / ME 추출
            
            ack_msg = 'ACK ETTTP/1.0\r\n'
            ack_msg += f'Host:{SERVER_IP}\r\n'
            ack_msg += f'First-Move:{player}\r\n'
            ack_msg += '\r\n'
            
            client_socket.send(ack_msg.encode())
        
        # === game start ===        
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        