import pygame
import sys,socket,time,pickle

WIDTH = 700
HEIGHT = 700
SQUARE_LEN = 170
HOST = "127.0.0.1"
PORT = 9999

board = [[None]*3,[None]*3,[None]*3]
squares_pos = [[None]*3,[None]*3,[None]*3]

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  

pygame.init()
font = pygame.font.SysFont('comicsans',45)
font1 = pygame.font.SysFont('comicsans',60)
font2 = pygame.font.SysFont('comicsans',75)
font3 = pygame.font.SysFont('comicsans',25)
clock = pygame.time.Clock()

def draw_lines(win,w,h,s):
    pygame.draw.line(win,(0,0,0),((w-s)/2,h/7),((w-s)/2,h/7+3*s),4)
    pygame.draw.line(win,(0,0,0),((w+s)/2,h/7),((w+s)/2,h/7+3*s),4)
    pygame.draw.line(win,(0,0,0),(w/7,(h-s)/2),(w/7+3*s,(h-s)/2),4)
    pygame.draw.line(win,(0,0,0),(w/7,(h+s)/2),(w/7+3*s,(h+s)/2),4)

    for i in range(3):
        for j in range(3):
            squares_pos[i][j] = [(w//7+i*s,h//7+j*s),(w//7+(i+1)*s,h//7+(j+1)*s)]


circle = 1
def draw_figures(win,x,y,s):
    global circle
    for i in range(3):
        for j in range(3):
            (x1,y1) = squares_pos[i][j][0]
            (x2,y2) = squares_pos[i][j][1]
            if x in range(x1,x2) and y in range(y1,y2):
                if circle and (board[i][j] == None):
                    pygame.draw.circle(win,(0,0,0),((x1+x2)//2,(y1+y2)//2),s//3,4)
                    board[i][j] = 0
                    circle = 0
                elif (board[i][j]== None):
                    pygame.draw.line(win,(0,0,0),(x1+40,y1+40),(x2-40,y2-40),6)
                    pygame.draw.line(win,(0,0,0),(x1+40,y1+s-40),(x2-40,y2-s+40),6)
                    board[i][j] = 1
                    circle = 1
                return

def Game_over(s,win):
    
    for i in range(3):
        if(board[i][0]==board[i][1]==board[i][2]==1):
            (x1,y1) = squares_pos[i][0][0]
            (x2,y2) = squares_pos[i][2][0]
            pygame.draw.line(win,(0,0,0),(x1+s//2,y1),(x2+s//2,y2+s),4)
            return 1
        elif(board[i][0]==board[i][1]==board[i][2]==0):
            (x1,y1) = squares_pos[i][0][0]
            (x2,y2) = squares_pos[i][2][0]
            pygame.draw.line(win,(0,0,0),(x1+s//2,y1),(x2+s//2,y2+s),4)
            return 0
    
    for j in range(3):
        if(board[0][j]==board[1][j]==board[2][j]==1):
            (x1,y1) = squares_pos[0][j][0]
            (x2,y2) = squares_pos[2][j][0]
            pygame.draw.line(win,(0,0,0),(x1,y1+s//2),(x2+s,y2+s//2),4)
            return 1
        elif(board[0][j]==board[1][j]==board[2][j]==0):
            (x1,y1) = squares_pos[0][j][0]
            (x2,y2) = squares_pos[2][j][0]
            pygame.draw.line(win,(0,0,0),(x1,y1+s//2),(x2+s,y2+s//2),4)
            return 0

    if(board[0][0]==board[1][1]==board[2][2]==1):
        (x1,y1) = squares_pos[0][0][0]
        (x2,y2) = squares_pos[2][2][0]
        pygame.draw.line(win,(0,0,0),(x1,y1),(x2+s,y2+s),4)
        return 1        
    if(board[0][2]==board[1][1]==board[2][0]==1):
        (x1,y1) = squares_pos[2][0][0]
        (x2,y2) = squares_pos[0][2][0]
        pygame.draw.line(win,(0,0,0),(x1+s,y1),(x2,y2+s),4)
        return 1    
    if(board[0][0]==board[1][1]==board[2][2]==0):
        (x1,y1) = squares_pos[0][0][0]
        (x2,y2) = squares_pos[2][2][0]
        pygame.draw.line(win,(0,0,0),(x1,y1),(x2+s,y2+s),4)
        return 0  
    if(board[0][2]==board[1][1]==board[2][0]==0):
        (x1,y1) = squares_pos[2][0][0]
        (x2,y2) = squares_pos[0][2][0]
        pygame.draw.line(win,(0,0,0),(x1+s,y1),(x2,y2+s),4)
        return 0  

    a = 0
    for i in range(3):
        for j in range(3):
            if board[i][j]==None:
                a = 0
                return None
            else:
                a = 1
        
    return 2        

def Game():
    global circle
    try:
        client.connect((HOST,PORT))
        con = client.recv(1)
        if con == b"0":
            print("Server is busy!")
            return

        print(f"Connected to {HOST}:{PORT}")
    except:
        print("Server is not running!")
        return    

    caption = client.recv(1000).decode("utf-8")

    win = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption(caption)
    
    if(caption.startswith("Player-1")):
        my_turn = 1
    else:
        my_turn = 0   

    win.fill((255,255,255))
    draw_lines(win,WIDTH,HEIGHT,SQUARE_LEN)
    win.blit(font1.render("TIC-TAC-TOE!",True,(0,0,0)),(360,30))

    a = 0
    b = 0
    mouse_pos = {"x":None,"y":None}
    run = True

    while run:
        connections = pickle.loads(client.recv(200))["conn"]
        client.sendall(pickle.dumps(mouse_pos))
        player = pickle.loads(client.recv(2000))
        
        if connections==2:    
            
            if caption.startswith("Player-1") and player["moved"]['Player-2']:
                draw_figures(win,player["pos"]["x"],player["pos"]["y"],SQUARE_LEN)  
                my_turn = 1

            elif caption.startswith("Player-2") and player["moved"]['Player-1']:
                draw_figures(win,player["pos"]["x"],player["pos"]["y"],SQUARE_LEN) 
                my_turn = 1
        
        mouse_pos = {"x":None,"y":None}

        if b:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and my_turn==1 and connections==2: 
                x,y = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                if WIDTH//7<=x<=WIDTH//7+3*SQUARE_LEN and WIDTH//7<=y<=WIDTH//7+3*SQUARE_LEN:
                    draw_figures(win,x,y,SQUARE_LEN) 
                    mouse_pos = {"x":x,"y":y} 
                    my_turn = 0

        if connections==2 and a==0:
            win.fill((255,255,255))
            draw_lines(win,WIDTH,HEIGHT,SQUARE_LEN)
            win.blit(font1.render("TIC-TAC-TOE!",True,(0,0,0)),(360,30))

            if caption.startswith("Player-1"):
                win.blit(font3.render("Player-2 : connected",False,(0,0,0)),(30,40))
            else:    
                win.blit(font3.render("Player-1 : connected",False,(0,0,0)),(30,40))

            a = 1    
        elif a==0:
            win.blit(font3.render("Player-2 : Not connected",False,(0,0,0)),(30,40)) 


        game_over = Game_over(SQUARE_LEN,win)
        if game_over==0:
            text = font.render("Game Over : Player-1 wins!",True,(0,0,0))
            win.blit(text,(160,650))
            b = 1
        elif game_over == 1:
            text = font.render("Game Over : Player-2 wins!",True,(0,0,0))
            win.blit(text,(160,650))
            b = 1 
        elif game_over == 2:
            text = font.render("Game Over : Draw!",True,(0,0,0))
            win.blit(text,(240,650))    
            b = 1 

        pygame.display.update()
    time.sleep(2)

if __name__ == "__main__":
    Game()