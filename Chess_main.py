import pygame as P
import sys
from Chess_engine import create_board

WIDTH=512
HEIGHT=512
SQ_SIZE=WIDTH//8
FPS=15

LIGHT=(238, 238, 210)
DARK=(118, 150, 86)
#This makes the board 
def draw_board (screen):
    for i in range (0,8):
        for j in range(0,8):
            if((i+j)%2==0):
                color=LIGHT
            else:
                color= DARK
            P.draw.rect(screen,color,(j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE))

#This loades the images into the dict
def load_image():
    my_dict={}
    pieces=["wK","wQ","wR","wB","wN","wP","bK","bQ","bR","bB","bN","bP"]
    for piece in pieces:
        image=P.image.load("Chess_images/"+ piece +".png")
        resize_image=P.transform.scale(image,(SQ_SIZE,SQ_SIZE))
        my_dict[piece]=resize_image
    return my_dict

#This draws the pieces 

def draw_pieces(screen,board,my_dict):
    for i in range(0,8):
        for j in range(0,8):
            piece=board[i][j]
            if(piece=="--"):
                continue
            else:
                image=my_dict[piece]
                screen.blit(image,(j*SQ_SIZE,i*SQ_SIZE))


#Create the function to draw the highlights

def draw_highlights(screen,current_selected):
    highlight=(246, 246, 105)
    if(current_selected==None):
        return None
    else:
        (row,col)=current_selected
        pixelX=col*SQ_SIZE
        pixelY=row*SQ_SIZE
        P.draw.rect(screen,highlight,(pixelX,pixelY,SQ_SIZE,SQ_SIZE))



#Create def main to run the and test the app 

def main():
    P.init()
    screen=P.display.set_mode((WIDTH,HEIGHT))
    P.display.set_caption("Chess Engine")
    clock=P.time.Clock()
    board=create_board()
    images=load_image()
    click_history_list=[]
    move_history=[]
    current_selected=None
    track_turn=True
    while True:
        for event in P.event.get():
            if event.type==P.QUIT:
                P.quit()
                sys.exit()
            if(event.type==P.MOUSEBUTTONDOWN):
                get_position=event.pos
                (X,Y)=get_position
                row=Y//SQ_SIZE
                col=X//SQ_SIZE
                click=(row,col)
                click_history_list.append(click)
                if(len(click_history_list)==1):
                    piece=board[row][col]
                    if(piece=="--"):
                        click_history_list=[]
                    else:
                        current_selected=click
                        if((track_turn==True and piece[0]=="w") or track_turn==False and piece[0]=="b"):
                            current_selected=click
                        else:
                            click_history_list=[]

                if(len(click_history_list)==2):
                    (row_0,col_0)=click_history_list[0]
                    (row_1,col_1)=click_history_list[1]
                    start_row=row_0
                    start_col=col_0
                    end_row=row_1
                    end_col=col_1
                    piece=board[start_row][start_col]
                    captured_piece=board[end_row][end_col]
                    board[end_row][end_col]=piece
                    board[start_row][start_col]="--"
                    newtuple=(start_row,start_col,end_row,end_col,piece,captured_piece)
                    move_history.append(newtuple)
                    current_selected=None
                    click_history_list=[]
                    track_turn=not track_turn
            if(event.type==P.KEYDOWN):
                if(event.key==P.K_z):
                    if((move_history)!=0):
                        last_move=move_history.pop()
                        (start_row,start_col,end_row,end_col,piece,captured_piece) = last_move
                        board[end_row][end_col]=captured_piece
                        board[start_row][start_col]=piece



        
        draw_board(screen)
        draw_highlights(screen,current_selected)
        draw_pieces(screen,board,images)
        P.display.flip()
        clock.tick(FPS)
main()


    
        

