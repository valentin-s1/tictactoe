import pygame
import sys
import time
import tictactoe

#initialize modules
pygame.init()

#define dimensions for game window
width = 900
height = 600

#define colors
black = (0, 0, 0)
white = (255, 255, 255)

#set up game window with previously defined dimensions
screen = pygame.display.set_mode(size=(width, height))

#define fonts & font sizes
play_font = pygame.font.Font("calibri.ttf", 40)
title_font = pygame.font.Font("calibri.ttf", 60)
symbol_font = pygame.font.Font("calibri.ttf", 90)

#initialize user & ai_turn boolean
user = None
ai_turn = False

#set up empty playing field
board = tictactoe.initial_state()

while True:

    #when user quits, script is exited
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            sys.exit("User quit the game.")

    screen.fill(black)

    #user chooses to play as X or O if not yet defined
    if user is None:

        #header is white text "Play Tic-Tac-Toe" with antialising turned on for higher resolution
        header = title_font.render("Play Tic-Tac-Toe", True, white)
        #get rectangular area of header surface
        header_rect = header.get_rect()
        #center the header at (width/2, 75) where (0,0) is the top left corner 
        header_rect.center = ((width / 2), 75)
        #draw header onto header rectangle
        screen.blit(source=header, dest=header_rect)

        #create button to select X
        x_button = pygame.Rect(
            (width/8),      #left
            (height/2),     #top   
            (width/4),      #width
            75              #height
        )
        x_text = play_font.render("Play as X", True, black)
        x_rect = x_text.get_rect()
        x_rect.center = x_button.center
        #draw a white rectangle (with position and dimensions of x_button) onto the game window 
        pygame.draw.rect(screen, white, x_button)
        screen.blit(x_text, x_rect)

        #button is 2/8 wide, so for symmetry reasons the right end of o_button needs to be at 7/8 of the total width
        #-> left end is at 5/8 of the width
        o_button = pygame.Rect(
            5*(width/8),    #left
            (height/2),     #top 
            (width/4),      #width
            75              #height
        )
        o_text = play_font.render("Play as O", True, black)
        o_rect = o_text.get_rect()
        o_rect.center = o_button.center
        pygame.draw.rect(screen, white, o_button)
        screen.blit(o_text, o_rect)

        #check if the user selects a player
        click = pygame.mouse.get_pressed()[0]
        if click == True:
            #get the position of the mouse when clicked
            mouse = pygame.mouse.get_pos()

            #if the mouse is within the confines of x_button, the user chooses X
            if x_button.collidepoint(mouse):
                time.sleep(0.4)
                user = tictactoe.X

            #same goes for o_button
            elif o_button.collidepoint(mouse):
                time.sleep(0.4)
                user = tictactoe.O

    #if user has already chosen to play as X or O
    else:

        #draw the game board
        tile_size = 120
        #width/2 is the center of the middle square (horizontally), so we need to subtract 1.5 tile sizes to end up at the left edge of the tile grid
        #same applies to the height
        tile_origin = (
            width/2 - (1.5*tile_size), 
            height/2 - (1.5*tile_size)
        )
        
        tiles = []

        #loop to store rectangular coordinates of all 9 tiles (3 rows x 3 cols)
        #outer iteration is over rows which is why rows is reset when i completes one iteration
        for i in range(3):
            row = []
            for j in range(3):
                #tile_origin[0] is left edge of grid -> add 0, 1 and 2 times the tile size to get the left edges of the tiles in each row
                #tile_origin[1] is top edge of grid -> in inner iteration (cols), i is constant for an entire loop of j because all tiles are in the same row (same distance from top)
                #store coordinates & dimensions for tiles:
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size, #left
                    tile_origin[1] + i * tile_size, #top
                    tile_size,                      #width
                    tile_size                       #height
                )
                #draw rectangles with line thickness 4
                pygame.draw.rect(screen, white, rect, 4)

                #if current tile is not empty (not None), fill in either X or O at the center of the tile
                if board[i][j] != tictactoe.EMPTY:
                    played_move = symbol_font.render(board[i][j], True, white)
                    move_rect = played_move.get_rect()
                    move_rect.center = rect.center
                    screen.blit(played_move, move_rect)
                    
                row.append(rect)
            tiles.append(row)

        #defines game_over as the terminal state (0 empty tiles)
        game_over = tictactoe.terminal(board)
        #defines the current player (turn 0 is X, turn 1 is O, and so on)
        player = tictactoe.player(board)

        #if the game is over, a winner is decided and the header reflects the result
        if game_over:
            winner = tictactoe.winner(board)
            if winner is None:
                header_text = f"Game over: Tie!"
            else:
                if winner==user:
                    header_text = f"Game over: {winner} (you) wins!"
                else:
                    header_text = f"Game over: {winner} (AI) wins!"
        #if the game is not over, the header reflects whose turn it is 
        elif user == player:
            header_text = f"{user}'s turn"
        else:
            header_text = f"AI's turn"
        header = title_font.render(header_text, True, white)
        header_rect = header.get_rect()
        header_rect.center = ((width/2), 55)
        screen.blit(header, header_rect)

        #check if it is the AI's turn
        if user != player and not game_over:
            #if it is the AI's turn the move is decided by the algorithm and ai_turn switches (player change)
            if ai_turn:
                time.sleep(0.5)
                played_move = tictactoe.minimax(board)
                board = tictactoe.result(board, played_move)
                ai_turn = False
            #if the current turn is not played by the AI, set to true s.t. next move is played by AI
            else:
                ai_turn = True

        click = pygame.mouse.get_pressed()[0]
        #check if the user has clicked, it is their turn and the game is not yet finished
        if click == True and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    #if move can be made (clicked on an empty tile), move board forward by the move played (clicked on tile (i, j))
                    if (board[i][j] == tictactoe.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = tictactoe.result(board, (i, j))

        if game_over:
            new_button = pygame.Rect(width/3, height-90, width/3, 75)
            new_text = play_font.render("New game", True, black)
            new_rect = new_text.get_rect()
            new_rect.center = new_button.center
            pygame.draw.rect(screen, white, new_button)
            screen.blit(new_text, new_rect)
            click = pygame.mouse.get_pressed()[0]
            #if the user presses the "New game" button, the game resets
            if click == True:
                mouse = pygame.mouse.get_pos()
                if new_button.collidepoint(mouse):
                    time.sleep(0.4)
                    user = None
                    board = tictactoe.initial_state()
                    ai_turn = False

    #update displayed contents
    pygame.display.flip()
