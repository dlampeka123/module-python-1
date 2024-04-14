from piece import Pawn, King, Knight, Rook, Bishop, Queen, Piece


class GameBoard:

    def __init__(self):
        self.squares = {(x, y): None for x in range(1, 9) for y in range(1, 9)}
        self.update_board()

    def update_board(self):
        initial_positions = {}

        for x in range(1, 9):
            initial_positions[(x, 2)] = ('w', Pawn)

        # Setting up pawns for black player
        for x in range(1, 9):
            initial_positions[(x, 7)] = ('b', Pawn)

        # Setting up other pieces
        for y, player_color in zip([1, 8], ['w', 'b']):
            for x, piece_class in zip([1, 8], [Rook, Rook]):
                initial_positions[(x, y)] = (player_color, piece_class)

            for x, piece_class in zip([2, 7], [Knight, Knight]):
                initial_positions[(x, y)] = (player_color, piece_class)

            for x, piece_class in zip([3, 6], [Bishop, Bishop]):
                initial_positions[(x, y)] = (player_color, piece_class)

            initial_positions[(4, y)] = (player_color, Queen)
            initial_positions[(5, y)] = (player_color, King)

        for (x, y), (color, piece_class) in initial_positions.items():
            self.squares[(x, y)] = piece_class(color, x, y)

    def validate_move(self, from_, to_):
        piece = self.squares[from_]
        destination_piece = self.squares[to_]

        if not piece:
            return False

        moves = piece.get_possible_moves()

        if to_ not in moves:
            return False

        if destination_piece and destination_piece.color == piece.color:
            return False

        if isinstance(piece, (Rook, Pawn, Bishop, Queen)):
            if not self.check_barriers(from_, to_, moves):
                return False

        return True

    def check_barriers(self, from_, to_, moves):
        x1, y1 = from_
        x2, y2 = to_

        if x1 == x2:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if self.squares[(x1, y)]:
                    return False
        elif y1 == y2:
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if self.squares[(x, y1)]:
                    return False
        elif abs(x1 - x2) == abs(y1 - y2):
            x_step = 1 if x1 < x2 else -1
            y_step = 1 if y1 < y2 else -1
            x, y = x1 + x_step, y1 + y_step
            while (x, y) != (x2, y2):
                if self.squares[(x, y)]:
                    return False
                x += x_step
                y += y_step

        return True

    def make_move(self, from_, to_):
        piece = self.squares[from_]
        if not piece:
            return False

        if not self.validate_move(from_, to_):
            return False

        self.squares[to_] = self.squares[from_]
        self.squares[from_] = None
        return True
