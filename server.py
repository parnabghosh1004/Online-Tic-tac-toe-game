import socket
import threading,pickle
import time

HOST = "127.0.0.1"
PORT = 9999

players_conn = [] 
player = {"moved":{},"pos":{"x":None,"y":None}}

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

def Handle_Player(conn,addr):

    global player

    print(f"{addr[0]}:{addr[1]} connected!")
    if len(players_conn):
        caption = "Player-2"
    else:
        caption = "Player-1"

    conn.sendall(f"{caption} ({addr[0]}:{addr[1]})".encode("utf-8"))
    
    players_conn.append(conn)
    player["moved"][f"{caption}"] = 0
    
    run = True
    while run:
        try:
            conn.sendall(pickle.dumps({"conn":len(players_conn)}))
            
            mouse_pos = pickle.loads(conn.recv(1000))
            
            time.sleep(0.01)
            conn.send(pickle.dumps(player))
            
            if mouse_pos["x"]!=None:
                player["moved"][f"{caption}"] = 1
                time.sleep(0.01)
                player["pos"] = {"x":mouse_pos["x"],"y":mouse_pos["y"]}
            else:
                player["moved"][f"{caption}"] = 0

        except:
            break    

    print(f"{addr[0]}:{addr[1]} disconnected!")
    players_conn.remove(conn)
    conn.close()
    player = {"moved":{},"pos":{"x":None,"y":None}}

def start_server():

    server.listen(2)

    print(f"Server listening on {HOST}:{PORT}")

    run = True
    while run:
        conn,addr = server.accept()
        if len(players_conn)>1:
            conn.sendall("0".encode("utf-8"))
            conn.close()
        else:
            conn.sendall("1".encode("utf-8"))
            thread = threading.Thread(target=Handle_Player,args=(conn,addr))
            thread.daemon = True
            thread.start()

            print(f"Players connected : {threading.active_count()-1}")
        

if __name__ == "__main__":
    start_server() 
    server.close()       