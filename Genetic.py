import sunfish
import PST

MAX_NUM_MOVES = 100
SEARCH_TIME = 0.2

class Engine:
    def __init__(self, pst):
        self.pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0, pst)
        self.searcher = sunfish.Searcher()
        self.pst = pst
    
    def reset_position(self):
        self.pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0, self.pst)

class Game:
    def __init__(self, white_engine, black_engine):
        self.white = white_engine
        self.black = black_engine
        self.winner = ""
        self.num_moves = 0
        self.moves = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]

    def play(self):
        self.white.reset_position()
        self.black.reset_position()
        while True:
            # White to move.
            move, score = self.white.searcher.search(self.white.pos, secs=SEARCH_TIME)
            self.white.pos = self.white.pos.move(move)
            self.black.pos = self.black.pos.move(move)
            self.moves[self.num_moves%8] = move
            self.num_moves += 1
            sunfish.print_pos(self.white.pos.rotate())

            if self.white.pos.score <= -sunfish.MATE_LOWER:
                self.winner = "White"
                return

            # Black to move.
            move, score = self.black.searcher.search(self.black.pos, secs=SEARCH_TIME)
            self.white.pos = self.white.pos.move(move)
            self.black.pos = self.black.pos.move(move)
            self.moves[self.num_moves%8] = move
            self.num_moves += 1
            sunfish.print_pos(self.black.pos)

            if self.black.pos.score <= -sunfish.MATE_LOWER:
                self.winner = "Black"
                return

            # Check for draw
            if (self.moves[0] == self.moves[4] and self.moves[2] == self.moves[6] and
                self.moves[1] == self.moves[5] and self.moves[3] == self.moves[7]):
                self.winner = "Draw"
                return
            if self.num_moves >= MAX_NUM_MOVES:
                self.winner = "Draw"
                return
        

class Match:
    def __init__(self, engine1, engine2, num_games):
        self.engine1 = engine1
        self.engine2 = engine2
        self.num_games = num_games
        self.score = 0

    def play(self):
        for i in range(self.num_games):
            game = Game(self.engine1, self.engine2)
            game.play()
            if game.winner == "White":
                self.score += 1
            elif game.winner == "Black":
                self.score -= 1
        # Now switch sides
        for i in range(self.num_games):
            game = Game(self.engine2, self.engine1)
            game.play()
            if game.winner == "Black":
                self.score += 1
            elif game.winner == "White":
                self.score -= 1
        print("Final score:", self.score)


def main():
    engine1 = Engine(PST.init_pst)
    engine2 = Engine(PST.init_pst)
    match = Match(engine1, engine2, 2)
    match.play()
    if match.score > 0:
        print("Winner is Engine1!")
    elif match.score < 0:
        print("Winner is Engine2!")
    else:
        print("Match ends in a draw")
    


if __name__ == '__main__':
    main()