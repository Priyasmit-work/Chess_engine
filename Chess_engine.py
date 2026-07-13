def create_board():
        empty_rows=[["--"]*8 for i in range(4)]
        return [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            * empty_rows,
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]

#Create a function that get the pawns move 

def get_pawn_moves(board,row,col,en_passant_square=None):
        move=[]
        piece=board[row][col]
        if(piece[0]=="w"):
                move_direction= -1
        else:
                move_direction= +1
        next_row=row+move_direction
        if not(0<=next_row<=7):
             return move           
        if(board[next_row][col]=="--"):
                move.append((row,col,next_row,col))

        if(piece[0]=="w" and row == 6):
                next_row=row-2
                if(board[row+move_direction][col]=="--" and board[next_row][col]=="--"):
                        move.append((row,col,next_row,col))
        if(piece[0]=="b" and row == 1):
                next_row=row+2
                if(board[row+move_direction][col]=="--" and board[next_row][col] =="--"):
                        move.append((row,col,next_row,col))
        if(col-1>=0):
                if(board[row+move_direction][col-1]!="--"):
                    if(piece[0]=="w" and board[row+move_direction][col-1][0]=="b"):
                        move.append((row,col,row+move_direction,col-1))
                    if piece[0] == "b" and board[row+move_direction][col-1][0] == "w":
                        move.append((row, col, row+move_direction, col-1))
        
        if(col+1<=7):
               if(board[row+move_direction][col+1]!="--"):
                    if(piece[0]=="w" and board[row+move_direction][col+1][0]=="b"):
                        move.append((row,col,row+move_direction,col+1))
                    if piece[0] == "b" and board[row+move_direction][col+1][0] == "w":
                        move.append((row, col, row+move_direction, col+1))
        if (en_passant_square is not None):
             (ep_row,ep_col)=en_passant_square
             if(piece[0]=="w"):
                  if (row ==3 and (ep_row,ep_col)==(row-1,col-1)):
                       move.append((row,col,ep_row,ep_col))
                  if(row == 3 and (ep_row,ep_col)==(row-1,col+1)):
                       move.append((row,col,ep_row,ep_col))
             if(piece[0]=="b"):
                  if (row ==4 and (ep_row,ep_col)==(row+1,col-1)):
                       move.append((row,col,ep_row,ep_col))
                  if(row == 4 and (ep_row,ep_col)==(row+1,col+1)):
                       move.append((row,col,ep_row,ep_col))
                  
        return move

def get_rook_moves(board, row, col):
    move = []
    piece = board[row][col]
    directions = [(-1,0),(+1,0),(0,-1),(0,+1)]
    for direction in directions:
        travel_row = row + direction[0]
        travel_col = col + direction[1]
        while 0 <= travel_row <= 7 and 0 <= travel_col <= 7:
            if board[travel_row][travel_col] == "--":
                move.append((row, col, travel_row, travel_col))
            elif board[travel_row][travel_col][0] == piece[0]:
                break
            else:
                move.append((row, col, travel_row, travel_col))
                break
            travel_row = travel_row + direction[0]
            travel_col = travel_col + direction[1]
    return move


def get_bishop_moves(board,row,col):
      move=[]
      piece=board[row][col]
      directions=[(-1,-1),(+1,+1),(-1,+1),(+1,-1)]
      for direction in directions:
        travel_row = row + direction[0]
        travel_col = col + direction[1]
        while 0 <= travel_row <= 7 and 0 <= travel_col <= 7:
            if board[travel_row][travel_col] == "--":
                move.append((row, col, travel_row, travel_col))
            elif board[travel_row][travel_col][0] == piece[0]:
                break
            else:
                move.append((row, col, travel_row, travel_col))
                break
            travel_row = travel_row + direction[0]
            travel_col = travel_col + direction[1]
      return move


def get_queen_moves(board,row,col):
      move=[]
      piece=board[row][col]
      directions=[(-1,0),(+1,0),(0,-1),(0,+1),(-1,-1),(+1,+1),(-1,+1),(+1,-1)]
      for direction in directions:
        travel_row = row + direction[0]
        travel_col = col + direction[1]
        while 0 <= travel_row <= 7 and 0 <= travel_col <= 7:
            if board[travel_row][travel_col] == "--":
                move.append((row, col, travel_row, travel_col))
            elif board[travel_row][travel_col][0] == piece[0]:
                break
            else:
                move.append((row, col, travel_row, travel_col))
                break
            travel_row = travel_row + direction[0]
            travel_col = travel_col + direction[1]
      return move


def get_knight_moves(board,row,col):
     move=[]
     piece=board[row][col]
     directions=[(+2,-1),(+2,+1),(+1,+2),(-1,+2),(+1,-2),(-1,-2),(-2,-1),(-2,+1)]
     for direction in directions:
          travel_row=row+direction[0]
          travel_col=col+direction[1]
          if( 0 <= travel_row <= 7 and 0 <= travel_col <= 7):
               if(board[travel_row][travel_col] == "--" or  board[travel_row][travel_col][0] != piece[0]):
                    move.append((row,col,travel_row,travel_col))
    
     return move


def get_king_moves(board, row, col, castling_rights=None):
    move = []
    piece = board[row][col]
    directions = [(-1,0),(+1,0),(0,-1),(0,+1),(-1,-1),(+1,+1),(-1,+1),(+1,-1)]
    for direction in directions:
        travel_row = row + direction[0]
        travel_col = col + direction[1]
        if 0 <= travel_row <= 7 and 0 <= travel_col <= 7:
            if board[travel_row][travel_col] == "--" or board[travel_row][travel_col][0] != piece[0]:
                move.append((row, col, travel_row, travel_col))

    if (piece[0] == "w" and castling_rights is not None):
        if (not castling_rights["white_king_move"] and
            not castling_rights["white_kingside_rook_move"] and
            board[7][5] == "--" and board[7][6] == "--"):
            move.append((row, col, row, col+2))
        if (not castling_rights["white_king_move"] and
            not castling_rights["white_queenside_rook_move"] and
            board[7][1] == "--" and
            board[7][2] == "--" and
            board[7][3] == "--"):
            move.append((row, col, row, col-2))

    if (piece[0] == "b" and castling_rights is not None):
        if (not castling_rights["black_king_move"] and
            not castling_rights["black_kingside_rook_move"] and
            board[0][5] == "--" and board[0][6] == "--"):
            move.append((row, col, row, col+2))
        if (not castling_rights["black_king_move"] and
            not castling_rights["black_queenside_rook_move"] and
            board[0][1] == "--" and
            board[0][2] == "--" and
            board[0][3] == "--"):
            move.append((row, col, row, col-2))

    return move


def get_all_moves(board,color):
     moves=[]
     for i in range(0,8):
          for j in range(0,8):
               piece=board[i][j]
               if(piece=="--" or piece[0]!= color):
                    continue
               if(piece[1]=="P"):
                    moves.extend(get_pawn_moves(board,i,j))
               elif(piece[1]=="R"):
                    moves.extend(get_rook_moves(board,i,j))
               elif(piece[1]=="Q"):
                    moves.extend(get_queen_moves(board,i,j))
               elif(piece[1]=="B"):
                    moves.extend(get_bishop_moves(board,i,j))
               elif(piece[1]=="N"):
                    moves.extend(get_knight_moves(board,i,j))
               elif(piece[1]=="K"):
                    moves.extend(get_king_moves(board,i,j))
     return moves


def is_in_check(board,color):
    for i in range(0,8):
        for j in range(0,8):
            piece=board[i][j]
            if(piece!= "--" and piece[0]==color and piece[1]=="K"):
                position=(i,j)
    opponent_color="b" if color=="w" else "w"
    get_moves=get_all_moves(board,opponent_color)
    for moves in get_moves:
        if(position == (moves[2], moves[3])):
            return True
    return False

def get_legal_moves(board,row,col,color,en_passant_square=None,castling_rights=None):
    candidate_moves=[]
    piece=board[row][col]
    if(piece[1]=="P"):
        candidate_moves=get_pawn_moves(board,row,col,en_passant_square)
    elif(piece[1]=="R"):
        candidate_moves=get_rook_moves(board,row,col)
    elif(piece[1]=="B"):
        candidate_moves=get_bishop_moves(board,row,col)
    elif(piece[1]=="Q"):
        candidate_moves=get_queen_moves(board,row,col)
    elif(piece[1]=="N"):
        candidate_moves=get_knight_moves(board,row,col)
    elif(piece[1]=="K"):
        candidate_moves=get_king_moves(board,row,col,castling_rights)
    else:
        candidate_moves=[]
    legal_moves=[]
    for moves in candidate_moves:
          (start_row,start_col,end_row,end_col)=moves 
          saved_piece=board[end_row][end_col]
          board[end_row][end_col]=board[start_row][start_col]
          board[start_row][start_col]="--"
          if(is_in_check(board,piece[0])==False):
               legal_moves.append(moves)
          board[start_row][start_col]=board[end_row][end_col]
          board[end_row][end_col]=saved_piece
    return legal_moves


def find_king(board,color):
     for i in range(0,8):
        for j in range(0,8):
            piece=board[i][j]
            if(piece !="--" and piece[0]==color and piece[1]=="K"):
                position=(i,j)
            
     return position








