# ETTTP-project

[23-1] 이화여자대학교 정보통신공학(34743-02) Term Project

`EWHA Tic-Tac-Toe Protocol (ETTTP)`

## 👥 Member
<table cellspacing="0" cellpadding="0" width="100%">
  <tr width="100%">
    <td align="center">
      <a>유지민</a>
    </td>
    <td align="center">
      <a>이해원</a>
    </td>
  </tr>

<tr width="100%">
    <td align="center">
      <img src="https://github.com/jiminnee.png" width="80px"/>
    </td>
    <td align="center">
      <img src="https://github.com/haewonny.png" width="80px"/>
    </td>
  </tr>
  
  <tr width="100%">
    <td align="center">
      <a href="https://github.com/jiminnee">@jiminnee</a>
    </td>
    <td align="center">
      <a href="https://github.com/Haewonny">@Haewonny</a>
    </td>
  </tr>
</table>

## ℹ️ 프로젝트 소개
<p align='center'>
<img width="800" alt="Tic-Tac-Toe ex" src="https://github.com/Haewonny/Algorithm_python/assets/94354545/27c44e75-16bd-45ae-af25-4d5096735f2b">
</p>
본 프로젝트를 통해 online Tic-Tac-Toe 게임을 구현했다. 이 게임은 기능적인 측면에서 Peer-to-Peer 구조를 가지며, TCP connection을 기반으로 한 socket programming을 통해 Client와 Server가 통신한다. 즉, Server는 Server peer, Client는 Client peer 역할을 수행한다고 가정한다. Application message protocol은 ETTTP 형식을 준수하도록 했으며, 이를 통해 각 peer들은 실시간으로 상대방의 움직임을 보드에 반영하고 우승자를 찾는다.

```
  1️⃣ Client와 Server가 TCP connection (Port number = 12000)을 시도한다.

  2️⃣ Server는 첫 번째 플레이어를 선택하고, 이를 Client와 공유한다.

  3️⃣ Client와 Server의 게임 GUI window가 열린다.

  4️⃣ Client와 Server는 자신의 차례일 때, [3X3]의 보드판에 자신의 말을 놓을 수 있다.

  5️⃣ Client와 Server는 지속적으로 게임 우승자가 생겼는지 확인한 후, 결과값을 서로 공유한다. 

  6️⃣ 서로 공유한 결과값이 같은 우승자를 나타내는 경우, 게임이 종료된다.
```

## 💌 ETTTP format

1. Response Message
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
New-Move: (1,2) \r\n
\r\n
```

2. Request Message
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
First-Move: YOU \r\n
\r\n
```

3. Result Poll Message
```
RESULT ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
Winner: ME \r\n
\r\n
```
