import pygame as P
import sys
from Chess_engine import create_board,get_pawn_moves,get_rook_moves,get_bishop_moves,get_queen_moves,get_knight_moves,get_king_moves,get_all_moves,is_in_check,find_king,get_legal_moves,is_checkmate,is_stalemate,get_random_moves,get_best_moves

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


def draw_promotion(screen,images,color):
    if color=="w":
        choices=["wQ","wR","wN","wB"]
    else:
        choices=["bQ","bR","bN","bB"]
    box_x=WIDTH//2-SQ_SIZE*2
    box_y=HEIGHT//2-SQ_SIZE//2
    P.draw.rect(screen, (50,50,50), (box_x-5, box_y-5, SQ_SIZE*4+10, SQ_SIZE+10))
    for i in range(len(choices)):
        piece=choices[i]
        x=box_x+i*SQ_SIZE
        y=box_y
        P.draw.rect(screen,(255,255,255),(x,y,SQ_SIZE,SQ_SIZE))
        screen.blit(images[piece],(x,y))




def draw_game_over(screen, message, font):
    # dark overlay
    overlay = P.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # message text
    big_font = P.font.SysFont("Arial", 32, bold=True)
    small_font = P.font.SysFont("Arial", 20)
    
    text = big_font.render(message, True, (255, 255, 255))
    restart = small_font.render("Press R to restart", True, (255, 255, 0))
    
    # center on screen
    text_x = WIDTH//2 - text.get_width()//2
    text_y = HEIGHT//2 - 40
    restart_x = WIDTH//2 - restart.get_width()//2
    restart_y = HEIGHT//2 + 10
    
    screen.blit(text, (text_x, text_y))
    screen.blit(restart, (restart_x, restart_y))

def draw_start_screen(screen):
    screen.fill((49,46,43))
    big_font=P.font.SysFont("Arial",42,bold=True)
    med_font=P.font.SysFont("Arial",22)
    small_font=P.font.SysFont("Arial",18)

    title  = big_font.render("Chess Engine",         True, (255, 255, 255))
    choose = med_font.render("Choose your color:",   True, (200, 200, 200))
    white  = small_font.render("W  —  Play as White", True, (240, 217, 181))
    black  = small_font.render("B  —  Play as Black", True, (150, 150, 150))
    screen.blit(title,  (WIDTH//2 - title.get_width()//2,  HEIGHT//2 - 100))
    screen.blit(choose, (WIDTH//2 - choose.get_width()//2, HEIGHT//2 - 20))
    screen.blit(white,  (WIDTH//2 - white.get_width()//2,  HEIGHT//2 + 30))
    screen.blit(black,  (WIDTH//2 - black.get_width()//2,  HEIGHT//2 + 70))

    


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
    castling_rights={"white_king_moved": False,
           "black_king_moved":False,
           "white_kingside_rook_moved": False,
           "white_queenside_rook_moved":False,
           "black_kingside_rook_moved":False,
           "black_queenside_rook_moved":False}
    promotion_pawn_position=False
    promotion_pending=False
    promotion_color=False
    game_over=False
    game_over_message=""
    player_color=None
    ai_color=None

    while player_color is None:
        for event in P.event.get():
            if event.type == P.QUIT:
                P.quit()
                sys.exit()
            if event.type == P.KEYDOWN:
                if event.key == P.K_w:
                    player_color = "w"
                    ai_color = "b"
                if event.key == P.K_b:
                    player_color = "b"
                    ai_color = "w"
        draw_start_screen(screen)
        P.display.flip()
        clock.tick(FPS)


    while True:
        for event in P.event.get():
            if event.type==P.QUIT:
                P.quit()
                sys.exit()
            if(event.type==P.MOUSEBUTTONDOWN):
                if game_over:
                    pass
                if promotion_pending==True:
                    (X,Y)=event.pos
                    box_x=WIDTH//2 - SQ_SIZE*2
                    box_y=HEIGHT//2 - SQ_SIZE//2
                    if box_x <= X <= box_x + SQ_SIZE*4 and box_y <= Y <= box_y + SQ_SIZE:
                        i = (X - box_x) // SQ_SIZE
                        if promotion_color == "w":
                            choices = ["wQ","wR","wN","wB"]
                        else:
                            choices = ["bQ","bR","bN","bB"]
                        chosen_piece = choices[i]
                        (prom_row, prom_col) = promotion_pawn_position
                        board[prom_row][prom_col] = chosen_piece
                        promotion_pending = False
                        promotion_pawn_position = None
                        promotion_color = None
                        continue
                get_position=event.pos
                (X,Y)=get_position
                row=Y//SQ_SIZE
                col=X//SQ_SIZE
                click=(row,col)
                click_history_list.append(click)

                #---------------------------------1st Click---------------------------
                if(len(click_history_list)==1):
                    piece=board[row][col]
                    if(piece=="--"):
                        click_history_list=[]
                    else:
                        current_selected=click
                        if piece[0]==player_color and ((track_turn==True and player_color=="w") or track_turn==False and player_color=="b"):
                            current_selected=click
                            valid_moves = get_legal_moves(board, row, col, piece[0],en_passant_square,castling_rights)
                        else:
                            click_history_list=[]
                            current_selected=None
                #------------------2nd Click-----------------------------------------
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

#----------------------------------------------------------------------------------------------------#
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
                        if(piece[1]=="P" and piece[0]=="w" and end_row==0):
                            promotion_pending=True
                            promotion_pawn_position=(end_row,end_col)
                            promotion_color="w"
                        elif(piece[1]=="P" and piece[0]=="b" and end_row==7):
                            promotion_pending=True
                            promotion_pawn_position=(end_row,end_col)
                            promotion_color="b"
                        
                        if(piece[1]=="P" and abs(end_row-start_row)==2):
                            en_passant_square=((start_row+end_row)//2,end_col)
                        else:
                            en_passant_square=None
#----------------------------------------------------------------------------------------------#This is the move part
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
                        if(track_turn)==True:
                             color_string="w"
                        else:
                            color_string="b"
                        if(is_in_check(board,color_string)==True):
                            in_check_position=find_king(board,color_string)
                        else:
                            in_check_position=None
                        
                        if is_checkmate(board, color_string):
                            game_over = True
                            if color_string == "w":
                                game_over_message = "Black Wins by Checkmate!"
                            else:
                                game_over_message = "White Wins by Checkmate!"

                        elif is_stalemate(board, color_string):
                            game_over = True
                            game_over_message = "Stalemate! It's a Draw!"         #This is track turn of the white and black

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
                if event.key == P.K_r and game_over:
                    board = create_board()
                    click_history_list = []
                    move_history = []
                    valid_moves = []
                    current_selected = None
                    track_turn = True
                    in_check_position = None
                    en_passant_square = None
                    game_over = False
                    game_over_message = ""
                    promotion_pending = False
                    promotion_color = None
                    ai_color=None
                    player_color=None
                    castling_rights = {
                        "white_king_moved"          : False,
                        "white_kingside_rook_moved" : False,
                        "white_queenside_rook_moved": False,
                        "black_king_moved"          : False,
                        "black_kingside_rook_moved" : False,
                        "black_queenside_rook_moved": False,
                    }
                    while player_color is None:
                        for event in P.event.get():
                            if event.type == P.QUIT:
                                P.quit()
                                sys.exit()
                            if event.type == P.KEYDOWN:
                                if event.key == P.K_w:
                                    player_color = "w"
                                    ai_color = "b"
                                if event.key == P.K_b:
                                    player_color = "b"
                                    ai_color = "w"
                        draw_start_screen(screen)
                        P.display.flip()
                        clock.tick(FPS)
        ai_turn=((track_turn==False and ai_color=="b") or (track_turn==True and ai_color=="w"))
        if(ai_turn  and not game_over and not promotion_pending):
            ai_move = get_best_moves(board,ai_color,2,en_passant_square,castling_rights)
            if ai_move is not None:
                (start_row, start_col, end_row, end_col) = ai_move
                piece=board[start_row][start_col]
                captured_piece=board[end_row][end_col]
                board[end_row][end_col]=piece
                board[start_row][start_col] = "--"
                if piece[1] == "P" and (end_row, end_col) == en_passant_square:
                    if piece[0] == "b":
                        board[end_row-1][end_col] = "--"

            # castling
                if piece[1] == "K" and abs(end_col - start_col) == 2:
                    if end_col > start_col:
                        board[start_row][5] = board[start_row][7]
                        board[start_row][7] = "--"
                    else:
                        board[start_row][3] = board[start_row][0]
                        board[start_row][0] = "--"

                # pawn promotion - auto queen for AI
                if piece[1] == "P" and end_row == 7:
                    board[end_row][end_col] = ai_color+"Q"

                # update en passant
                if piece[1] == "P" and abs(end_row - start_row) == 2:
                    en_passant_square = ((start_row+end_row)//2, end_col)
                else:
                    en_passant_square = None

                # update castling rights
                if piece == "bK":
                    castling_rights["black_king_moved"] = True
                elif piece == "bR" and start_col == 7:
                    castling_rights["black_kingside_rook_moved"] = True
                elif piece == "bR" and start_col == 0:
                    castling_rights["black_queenside_rook_moved"] = True

                # switch turn back to white
                track_turn = True

                # check detection
                if is_in_check(board,player_color):
                    in_check_position = find_king(board, player_color)
                else:
                    in_check_position = None

                # checkmate and stalemate
                if is_checkmate(board, player_color):
                    game_over = True
                    game_over_message = "AI  Wins by Checkmate!"
                elif is_stalemate(board, player_color):
                    game_over = True
                    game_over_message = "Stalemate! Draw!"
        
        
        draw_board(screen)
        draw_highlights(screen,current_selected,valid_moves,in_check_position)
        draw_fonts(screen,font)
        draw_pieces(screen,board,images)
        if(promotion_pending):
            draw_promotion(screen,images,promotion_color)
        if game_over:
            draw_game_over(screen, game_over_message, font)
        P.display.flip()
        clock.tick(FPS)
main()


    
        

