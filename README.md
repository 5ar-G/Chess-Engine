This is Simple schess engine made as quick side project.
Chess engine is not too adnvanced soo it cant performe moves like en-passant or casteling but it can be played if you have knoledge in chess.

____Explanation____


chess engine works by simulating a game of chess on an 8x8 board using the following principles:

Board Representation: The game state is represented by a 2D list, where each position on the board holds a string (like "wP" for a white pawn or "bK" for a black king). The board is updated with each move.

Move Generation: The engine can generate valid moves for each piece (pawn, rook, knight, bishop, queen, and king). It does this by defining specific movement logic for each type of piece and checking if the destination square is valid (empty or occupied by an opponent's piece).

Turn-based Logic: The game alternates between white and black players (self.whiteToMove tracks whose turn it is). The engine checks and updates the turn after each move.

Move Execution: When a move is made (makeMove method), the piece is moved on the board, and special rules like pawn promotion (when a pawn reaches the last row) and king movement are handled.

Undo Functionality: The engine allows players to undo moves, restoring the board to its previous state, including the positions of the pieces and the turn order.

Check and Checkmate: The engine checks whether a player’s king is under attack (in check) and whether there are valid moves available to escape the check. If no moves are available, it checks for checkmate or stalemate conditions.

Move Validity: The getValidMoves function generates all possible moves and filters out those that would place the current player's king in check.

Helper Methods: Several methods help with calculating legal moves for each piece, such as getPawnMoves, getRookMoves, and getKnightMoves. These functions take into account the piece's movement rules and the current state of the board.

In summary, this engine simulates a chess game by tracking the board's state, generating valid moves, and managing turn-based gameplay. It also includes basic rules like checkmate, stalemate, and pawn promotion.