import pygame as p
import ChessEngine

WIDTH, HEIGHT = 1080, 800  # Adjusted width to fit the board and side panel
DIMENSION = 8
BORDER_SIZE = 10  # Border thickness
PADDING = 20  # Space around the board
SIDE_PANEL_WIDTH = 250  # Width of the right-side panel
BOARD_SIZE = HEIGHT - 2 * PADDING  # Ensuring a square board
SQ_SIZE = BOARD_SIZE // DIMENSION
MAX_FPS = 300
IMAGES = {}
lastMoveText = "Last Move: --"  # Stores the last move notation

# Load images
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

# Resize images dynamically
def resizeImages(square_size):
    for piece in IMAGES:
        IMAGES[piece] = p.transform.scale(IMAGES[piece], (square_size, square_size))

def main():
    global SQ_SIZE, WIDTH, HEIGHT, BOARD_SIZE, lastMoveText

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
    p.display.set_caption("Chess Game")  # Set window title
    clock = p.time.Clock()
    font = p.font.Font(None, 36)  # Font for last move display

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    resizeImages(SQ_SIZE)

    running = True
    sqSelected = ()
    playerClicks = []
    hoverSquare = None

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.VIDEORESIZE:
                WIDTH, HEIGHT = e.w, e.h
                BOARD_SIZE = HEIGHT - 2 * PADDING
                SQ_SIZE = BOARD_SIZE // DIMENSION
                screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
                resizeImages(SQ_SIZE)

            elif e.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                if PADDING <= x <= PADDING + BOARD_SIZE and PADDING <= y <= PADDING + BOARD_SIZE:
                    col, row = (x - PADDING) // SQ_SIZE, (y - PADDING) // SQ_SIZE
                    
                    if sqSelected == (row, col):
                        sqSelected, playerClicks = (), []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            lastMoveText = "Last Move: " + move.getChessNotation()  # Update last move
                            moveMade = True
                        sqSelected, playerClicks = (), []

            elif e.type == p.KEYDOWN and e.key == p.K_z:
                gs.undoMove()
                lastMoveText = "Last Move: --"  # Reset last move display
                moveMade = True

            elif e.type == p.MOUSEMOTION:
                x, y = e.pos
                if PADDING <= x <= PADDING + BOARD_SIZE and PADDING <= y <= PADDING + BOARD_SIZE:
                    hoverSquare = ((y - PADDING) // SQ_SIZE, (x - PADDING) // SQ_SIZE)
                else:
                    hoverSquare = None

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, hoverSquare, font)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, hoverSquare, font):
    drawBackground(screen)
    drawBoard(screen, hoverSquare)
    drawPieces(screen, gs.board)
    drawSidePanel(screen, font)

def drawBackground(screen):
    """Creates a gradient background for better aesthetics."""
    for y in range(HEIGHT):
        color = (50 + y // 10, 50 + y // 10, 50 + y // 10)  # Subtle gradient effect
        p.draw.line(screen, color, (0, y), (WIDTH, y))

def drawBoard(screen, hoverSquare):
    """Draws the chessboard with borders and hover effect."""
    colors = [p.Color("white"), p.Color("grey")]
    highlight_color = p.Color(200, 200, 100, 150)  # Light yellow for hover

    # Draw border
    border_rect = p.Rect(PADDING - BORDER_SIZE, PADDING - BORDER_SIZE, BOARD_SIZE + 2 * BORDER_SIZE, BOARD_SIZE + 2 * BORDER_SIZE)
    p.draw.rect(screen, p.Color("black"), border_rect)  

    # Draw chessboard
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            rect = p.Rect(PADDING + c * SQ_SIZE, PADDING + r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, rect)
            
            if hoverSquare == (r, c):  # Highlight hovered square
                p.draw.rect(screen, highlight_color, rect, 4)

def drawPieces(screen, board):
    """Draws the pieces on the board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(PADDING + c * SQ_SIZE, PADDING + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSidePanel(screen, font):
    """Draws the side panel with move history and other info."""
    panel_x = PADDING + BOARD_SIZE + 20
    panel_y = PADDING
    panel_width = SIDE_PANEL_WIDTH
    panel_height = BOARD_SIZE

    # Draw panel background
    p.draw.rect(screen, (30, 30, 30), (panel_x, panel_y, panel_width, panel_height))  
    p.draw.rect(screen, (200, 200, 200), (panel_x, panel_y, panel_width, panel_height), 2)  

    # Draw last move text
    move_text_surface = font.render(lastMoveText, True, (255, 255, 255))
    screen.blit(move_text_surface, (panel_x + 10, panel_y + 20))

if __name__ == "__main__":
    main()
