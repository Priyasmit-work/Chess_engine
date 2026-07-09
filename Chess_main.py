import pygame as P
import sys
from Chess_engine import create_board,get_pawn_moves,get_rook_moves,get_bishop_moves,get_queen_moves,get_knight_moves,get_king_moves,get_all_moves,is_in_check,find_king,get_legal_moves

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

def draw_highlights(screen,current_selected,valid_moves,in_check_position):
    highlight=(246, 246, 105)
    if(current_selected!=None):
        (row,col)=current_selected
        pixelX=col*SQ_SIZE
        pixelY=row*SQ_SIZE
        P.draw.rect(screen,highlight,(pixelX,pixelY,SQ_SIZE,SQ_SIZE))
        for move in valid_moves:
            end_row=move[2]
            end_col=move[3]
            P.draw.rect(screen,(0,255,0),(end_col*SQ_SIZE,end_row*SQ_SIZE,SQ_SIZE,SQ_SIZE),4)
    if(in_check_position!=None):
            (check_row,check_col)=in_check_position
            P.draw.rect(screen,(220, 20, 20),(check_col*SQ_SIZE,check_row*SQ_SIZE,SQ_SIZE,SQ_SIZE),4)
        

def draw_fonts(screen,font):
    files=["a","b","c","d","e","f","g","h"]
    rank=["8","7","6","5","4","3","2","1"]
    for i in range(0,8):
        label=font.render(files[i],True,(0,0,0))
        screen.blit(label,(i*SQ_SIZE+SQ_SIZE-18,HEIGHT-18))
        label=font.render(rank[i],True,(0,0,0))
        screen.blit(label,(2,i*SQ_SIZE+2))    

    


#Create def main to run the and test the app 

def main():
    P.init()
    screen=P.display.set_mode((WIDTH,HEIGHT))
    P.display.set_caption("Chess Engine")
    clock=P.time.Clock()
    font=P.font.SysFont("Arial",16,bold=True)
    board=create_board()
    images=load_image()
    click_history_list=[]
    move_history=[]
    valid_moves=[]
    current_selected=None
    track_turn=True
    in_check_position=None
    en_passant_square=None
    castling_rights={"white_king_move": False,
           "black_king_move":False,
           "white_kingside_rook_move": False,
           "white_queenside_rook_move":False,
           "black_kingside_rook_move":False,
           "black_queenside_rook_move":False}


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
                            valid_moves = get_legal_moves(board, row, col, piece[0],en_passant_square,castling_rights)
                        else:
                            click_history_list=[]
                            current_selected=None

                if(len(click_history_list)==2):
                    (row_0,col_0)=click_history_list[0]
                    (row_1,col_1)=click_history_list[1]
                    start_row=row_0
                    start_col=col_0
                    end_row=row_1
                    end_col=col_1
                    if((start_row,start_col,end_row,end_col) in valid_moves):
                        piece=board[start_row][start_col]
                        captured_piece=board[end_row][end_col]
                        board[end_row][end_col]=piece
                        board[start_row][start_col] = "--"
                        if(piece[1]=="P" and (end_row,end_col)==en_passant_square):
                            if(piece[0]=="w"):
                                board[end_row+1][end_col]="--"
                            if(piece[0]=="b"):
                                board[end_row-1][end_col]="--"
                        if (piece[1] == "K" and abs(end_col - start_col) == 2):
                            if(end_col>start_col):
                                    board[start_row][5]=board[start_row][7]
                                    board[start_row][7]="--"
                            else:
                                    board[start_row][3]=board[start_row][0]
                                    board[start_row][0]="--"

                        
                        if(piece[1]=="P" and abs(end_row-start_row)==2):
                            en_passant_square=((start_row+end_row)//2,end_col)
                        else:
                            en_passant_square=None
                        if piece == "wK":
                            castling_rights["white_king_moved"] = True
                        elif piece == "wR" and start_col == 7:
                            castling_rights["white_kingside_rook_moved"] = True
                        elif piece == "wR" and start_col == 0:
                            castling_rights["white_queenside_rook_moved"] = True
                        elif piece == "bK":
                                castling_rights["black_king_moved"] = True
                        elif piece == "bR" and start_col == 7:
                                castling_rights["black_kingside_rook_moved"] = True
                        elif piece == "bR" and start_col == 0:
                                castling_rights["black_queenside_rook_moved"] = True
        
                        newtuple=(start_row,start_col,end_row,end_col,piece,captured_piece)
                        move_history.append(newtuple)
                        track_turn=not track_turn
                        if(track_turn==True):
                            color_string="w"
                        else:
                            color_string="b"
                        if(is_in_check(board,color_string)==True):
                            in_check_position=find_king(board,color_string)
                        else:
                            in_check_position=None
                        

                    valid_moves=[]
                    current_selected=None
                    click_history_list=[]
            if(event.type==P.KEYDOWN):#This checks the undo part 
                if(event.key==P.K_z):
                    if((move_history)!=0):
                        last_move=move_history.pop()
                        (start_row,start_col,end_row,end_col,piece,captured_piece) = last_move
                        board[end_row][end_col]=captured_piece
                        board[start_row][start_col]=piece



        
        draw_board(screen)
        draw_highlights(screen,current_selected,valid_moves,in_check_position)
        draw_fonts(screen,font)
        draw_pieces(screen,board,images)
        P.display.flip()
        clock.tick(FPS)
main()


    
        

