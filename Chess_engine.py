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

def get_pawn_moves(board,row,col):
        move=[]
        piece=board[row][col]
        if(piece[0]=="w"):
                move_direction= -1
        else:
                move_direction= +1
        next_row=row+move_direction
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




                

                
                
        
        

                           
        
