from Genetic import PST
import sunfish

def main():
    pst, piece = sunfish.init_pst, sunfish.init_piece
    PST.save_data(pst, piece, "Init")

if __name__ == '__main__':
    main()