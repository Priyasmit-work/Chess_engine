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

#Create def main to run the and test the app 

def main():
    P.init()
    screen=P.display.set_mode((WIDTH,HEIGHT))
    P.display.set_caption("Chess Engine")
    clock=P.time.Clock()
    board=create_board()
    images=load_image()
    while True:
        for event in P.event.get():
            if event.type==P.QUIT:
                P.quit()
                sys.exit()
        draw_board(screen)
        draw_pieces(screen,board,images)
        P.display.flip()
        clock.tick(FPS)
main()


    
        

