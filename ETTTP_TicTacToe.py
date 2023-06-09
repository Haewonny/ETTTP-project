import random
import tkinter as tk
from socket import *
import _thread

SIZE = 1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr # 상대방 ip
        self.recv_ip = src_addr # 나의 ip
        
        self.total_cells = 9
        self.line_size = 3
           
        # Client와 Server UI를 위한 변수 설정 
        if client:
            self.myID = 1   # 0 : server, 1 : client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
            게임을 종료하기 위한 'Quit' 버튼 생성
            이 버튼을 누르면 게임이 종료됨
        '''
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
   
    def create_status_frame(self):
        '''
            "Hold" 또는 "Ready"를 보여주는 UI
        '''
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')

    def create_result_frame(self):
        '''
            result를 보여주는 UI
        '''
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')

    def create_debug_frame(self):
        '''
            user가 입력할 수 있는 Debug UI
        '''
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)

    def create_board_frame(self):
        '''
            Tic-Tac-Toe Board UI
        '''
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
    def play(self, start_user=1): 
        '''
            game을 시작하기 위해 호출하는 함수
            start_user : 1이면 client가 게임 시작, 0이면 server가 게임 시작
        '''
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())

    def quit(self):
        '''
            GUI를 close하기 위한 함수
        '''
        self.destroy()
        
    def my_move(self, e, user_move):    
        '''
            player가 클릭한 버튼을 읽어옴

            e : event
            user_move : 버튼 번호 (0 ~ 8)
        '''
        # my turn이 아니거나 이미 선택된 버튼이면 아무것도 하지 않음
        if self.board[user_move] != 0 or not self.my_turn:
            return

        # peer에게 move를 보냄 
        valid = self.send_move(user_move)
        
        # peer로부터 ACK가 오지 않거나, not valid 하다면 게임 종료
        if not valid:
            self.quit()
            
        # user의 선택에 맞게 Tic-Tac-Toe board를 업데이트 함
        self.update_board(self.user, user_move)
        
        # game이 아직 종료되지 않았다면, turn을 바꿈
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())

    def get_move(self):
        '''
            다른 peer의 move를 가져오는 함수
            socket을 통해 메시지를 받아오고, 그것이 유효한지 확인
            유효하다면, dst_addr에 ACK 메시지 전송 
            유효하지 않다면, socket 닫고 종료
        '''
        msg_valid_check = False # 초기값
        
        msg = self.socket.recv(1024).decode() # socket으로 메시지 받아오기 
        msg_valid_check = check_msg(msg, self.recv_ip) # 유효한 메시지인지 체크 
        
        if not msg_valid_check: # Message is not valid
            self.socket.close()   
            self.quit()
            return
        else:  # If message is valid - send ack, update board and change turn
            # next-move 값 가져오기
            line_num = msg.split('\r\n')
            move = line_num[2].split(':')[1]
            row = int(move[1])
            col = int(move[3])
            
            loc = row * 3 + col # 버튼 번호 계산

            # ACK 전송
            ack_msg = 'ACK ETTTP/1.0\r\n'
            ack_msg += f'Host:{self.send_ip}\r\n' 
            ack_msg += f'New-Move:{move}\r\n'
            ack_msg += '\r\n'
    
            self.socket.send(ack_msg.encode())
            
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
                
    def send_debug(self):
        '''
            텍스트 박스에 입력한 input 내용으로 peer에게 메시지를 보내는 함수
            내 차례가 아니면 입력한 메시지를 수행하지 않음
        '''
        # 내 차례가 아니라면
        if not self.my_turn:
            self.t_debug.delete(1.0,"end") 
            return
        
        # input box에서 메시지를 가져옴
        d_msg = self.t_debug.get(1.0,"end") # 1행의 0열 가져오기

        # 입력 받아오면 \\r\\n으로 되어서 이걸 \r\n으로 수정하기
        d_msg = d_msg.replace("\\r\\n","\r\n") 
        self.t_debug.delete(1.0,"end")
        
        # debug 메시지에서 필요한 정보 추출
        line_num1 = d_msg.split('\r\n')

        if check_msg(d_msg, self.recv_ip):
            move = line_num1[2].split(':')[1]
            row = int(move[1])
            col = int(move[3])
        else:
            return
        
        ''' 선택된 위치 (직접 입력한 (row, col))가 이미 놓아진 곳인지 체크 '''
        user_move = row * 3 + col # 선택된 위치
        
        # my turn이 아니거나 이미 선택된 버튼이면 아무것도 하지 않음
        if self.board[user_move] != 0 or not self.my_turn:
            return
        
        ''' peer에게 메시지 전송 '''
        # If the location is not taken, send message         
        send_message = 'SEND ETTTP/1.0\r\n'
        send_message += f'Host:{self.send_ip}\r\n' 
        send_message += f'New-Move:({row},{col})\r\n' 
        send_message += '\r\n'

        self.socket.send(send_message.encode())
        
        ''' ack를 받으면 input에서 move를 가져옴 '''
        recv_msg = self.socket.recv(SIZE).decode() # ack 받기 
        line_num2 = recv_msg.split('\r\n') # \r\n을 기준으로 line 구분

        if check_msg(recv_msg, self.recv_ip):
            ack_move = line_num2[2].split(':')[1]
            ack_row = (int)(ack_move[1])
            ack_col = (int)(ack_move[3])
        
        loc = ack_row * 3 + ack_col # peer's move, from 0 to 8
        
        self.update_board(self.user, loc) 
            
        if self.state == self.active: # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        
    def send_move(self,selection):
        '''
            버튼을 클릭해서 peer에게 send message를 보내는 함수
            selection : 선택된 버튼
        '''
        row,col = divmod(selection,3)

        # Send message 
        send_message = 'SEND ETTTP/1.0\r\n'
        send_message += f'Host:{self.send_ip}\r\n' 
        send_message += f'New-Move:({row},{col})\r\n' 
        send_message += '\r\n'

        self.socket.send(send_message.encode())

        # ACK 수신 후, check_msg 수행
        recv_msg = self.socket.recv(SIZE).decode()

        line_num = recv_msg.split('\r\n') # \r\n을 기준으로 line 구분

        if check_msg(recv_msg, self.recv_ip):
            move = line_num[2].split(':')[1]
            # ACK message 속 (row, col)
            ack_row = (int)(move[1])
            ack_col = (int)(move[3])

            # 클릭한 (row, col) == ACK 메시지의 (row, col)
            if ack_row == row and ack_col == col:
                return True
        else:
            return False

        return True
    
    def check_result(self,winner,get=False):
       '''
            두 peer의 결과가 같은지 확인하는 함수
            get : get=False이면 이 사용자가 winner이며 결과를 먼저 report해야 함
       '''
       if not get: # winner
           result_poll_msg = 'RESULT ETTTP/1.0\r\n'
           result_poll_msg += f'Host:{self.send_ip}\r\n'
           result_poll_msg += f'Winner:{winner}\r\n'
           result_poll_msg += '\r\n'
           self.socket.send(result_poll_msg.encode())
           return True
       else: # loser
           result_recv_msg = self.socket.recv(SIZE).decode()
           line_num = result_recv_msg.split('\r\n')
           if check_msg(result_recv_msg, self.recv_ip):
               if line_num[2].split(':')[1] == 'ME':
                   return True
               else:
                   return False
           
        
    def update_board(self, player, move, get=False):
        '''
            클릭된 경우 board를 업데이트 하는 함수
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
            status를 체크하는 함수 - 게임이 끝났는지 아닌지 정의 
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
            winning line을 하이라이트 하는 함수
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'
# =========== End of Root class (TTT 클래스 마지막) ===========

def check_msg(msg, recv_ip):
    '''
        받은 메시지가 ETTTP 포맷인지 체크하는 함수
    '''
    line_num = msg.split('\r\n')

    if len(line_num) < 4:
        return False
    
    # ETTTP/1.0 확인
    if not line_num[0].split(' ')[1].startswith('ETTTP/1.0'):
        return False
    
    ''' 3가지 message type 에 따라 구분 '''
    msg_type = line_num[0].split(' ')[0]
    # Case1 : request message
    if msg_type == 'SEND':
        line = None
        for i in line_num:
            if i.startswith('New-Move:'):
                line = i
                break
            if i.startswith('First-Move:'):
                line = i
                break
        if not line:
            return False
        
    # Case2 : response message
    elif msg_type == 'ACK':
        line = None
        for i in line_num:
            if i.startswith('New-Move:'):
                line = i
                break
        if not line:
            return False
        
    # Case3 : result poll message
    elif msg_type == 'RESULT':
        line = None
        for i in line_num:
            if i.startswith('Winner:'):
                line = i
                break
        if not line:
            return False
    else:
        return False
    
    # HOST format 및 IP 확인
    if not line_num[1].startswith('Host:{}'.format(recv_ip)):
        return False        
         
    # 네번째 줄 확인
    if line_num[3] != '':
        return False

    return True

