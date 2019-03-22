import pickle
from random import randint
import sunfish

MAX_NUM_MOVES = 100
SEARCH_TIME = 1

class PST:
    def randomize_pst(pst, randomness):
        new_pst = {}
        for piece,table in pst.items():
            new_pst[piece] = []
            for square in range(len(table)):
                new_pst[piece].append(table[square] + randint(-1*randomness,randomness))
            new_pst[piece] = tuple(new_pst[piece])
        return new_pst

    def randomize_piece(piece, randomness):
        new_piece = {}
        for letter,value in piece.items():
            new_piece[letter] = value + randint(-1*randomness,randomness)
        return new_piece

    def generate_pst_padded(pst, piece):
        for k,table in pst.items():
            padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
            pst[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
            pst[k] = (0,)*20 + pst[k] + (0,)*20
        return pst
        

    def save_data(pst, piece, prefix):
        f = open('Store/' + prefix + '_pst.pckl', 'wb')
        pickle.dump(pst, f)
        f.close()
        f = open('Store/' + prefix + '_piece.pckl', 'wb')
        pickle.dump(piece, f)
        f.close()

    def load_data(prefix):
        f = open('Store/' + prefix + '_pst.pckl', 'rb')
        pst = pickle.load(f)
        f.close()
        f = open('Store/' + prefix + '_piece.pckl', 'rb')
        piece = pickle.load(f)
        f.close()
        return pst, piece



class Engine:
    def __init__(self, prefix):
        self.load_from_pckl(prefix)
        self.pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0, self.pst_padded)
        self.searcher = sunfish.Searcher()
    
    def reset_position(self):
        self.pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0, self.pst_padded)

    def load_from_pckl(self, prefix):
        self.pst, self.piece = PST.load_data(prefix)
        self.pst_padded = PST.generate_pst_padded(self.pst, self.piece)
    
    def save_to_pckl(self, prefix):
        PST.save_data(self.pst, self.piece, prefix)

    def evolve(self, random_pst, random_piece):
        self.pst = PST.randomize_pst(self.pst, random_pst)
        self.piece = PST.randomize_piece(self.piece, random_piece)
        self.pst_padded = PST.generate_pst_padded(self.pst, self.piece)


class Game:
    def __init__(self, white_engine, black_engine, print_pos):
        self.white = white_engine
        self.black = black_engine
        self.print = print_pos
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
            if self.print:
                sunfish.print_pos(self.white.pos.rotate())
                print(-self.white.pos.score)

            if self.white.pos.score <= -sunfish.MATE_LOWER:
                self.winner = "White"
                return

            # Black to move.
            move, score = self.black.searcher.search(self.black.pos, secs=SEARCH_TIME)
            self.white.pos = self.white.pos.move(move)
            self.black.pos = self.black.pos.move(move)
            self.moves[self.num_moves%8] = move
            self.num_moves += 1
            if self.print:
                sunfish.print_pos(self.black.pos)
                print(self.black.pos.score)

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
    def __init__(self, engine1, engine2, num_games, print_pos=False):
        self.engine1 = engine1
        self.engine2 = engine2
        self.num_games = num_games
        self.print_pos = print_pos
        self.results = []
        self.score = 0

    def play(self):
        for i in range(self.num_games):
            game = Game(self.engine1, self.engine2, self.print_pos)
            game.play()
            if game.winner == "White":
                self.results.append(1)
                self.score += 1
            elif game.winner == "Black":
                self.results.append(-1)
                self.score -= 1
            else:
                self.results.append(0)
        # Now switch sides
        for i in range(self.num_games):
            game = Game(self.engine2, self.engine1, self.print_pos)
            game.play()
            if game.winner == "Black":
                self.results.append(1)
                self.score += 1
            elif game.winner == "White":
                self.results.append(-1)
                self.score -= 1
            else:
                self.results.append(0)
        print("Results:", self.results)
        print("Final score:", self.score)


def main():
    #Configurations
    piece_randomness = 10
    pst_randomness = 10
    games_per_match = 2
    generations = 20
    # Load current best engine
    engine1 = Engine("Best")
    engine2 = Engine("Best")
    engine2.evolve(pst_randomness, piece_randomness)
    engine2.save_to_pckl("GEN1")
    for gen in range(generations):
        match = Match(engine1, engine2, games_per_match, True)
        print("Generation", gen+1)
        match.play()
        if match.score > 0:
            print("Winner is Engine1!")
        elif match.score < 0:
            print("Winner is Engine2!")
        else:
            print("Match ends in a draw")
    


if __name__ == '__main__':
    main()