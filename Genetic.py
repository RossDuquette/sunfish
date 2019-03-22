import sunfish
import PST

MAX_NUM_MOVES = 100

class Engine:
    def __init__(self, pst):
        self.pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0, pst)
        self.searcher = sunfish.Searcher()


def main():
    white = Engine(sunfish.pst)
    black = Engine(PST.pst)
    winner = "Draw"
    num_moves = 0
    moves = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
    while True:
        # White to move.
        move, score = white.searcher.search(white.pos, secs=0.5)
        white.pos = white.pos.move(move)
        black.pos = black.pos.move(move)
        moves[num_moves%6] = move
        num_moves += 1
        sunfish.print_pos(white.pos.rotate())

        if white.pos.score <= -sunfish.MATE_LOWER:
            winner = "White"
            break

        # Black to move.
        move, score = black.searcher.search(black.pos, secs=0.5)
        white.pos = white.pos.move(move)
        black.pos = black.pos.move(move)
        moves[num_moves%6] = move
        num_moves += 1
        sunfish.print_pos(black.pos)

        if black.pos.score <= -sunfish.MATE_LOWER:
            winner = "Black"
            break

        # Check for draw
        if (moves[0] == moves[2] and moves[2] == moves[4] and
           moves[1] == moves[3] and moves[3] == moves[5]):
            break;
        if num_moves >= MAX_NUM_MOVES:
            break
    
    print(winner)


if __name__ == '__main__':
    main()