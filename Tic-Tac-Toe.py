# Tic-Tac-Toe with AI (minimax) - single round, CLI

import math

LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def print_board(b):
    print("\n")
    print(f" {b[0]} | {b[1]} | {b[2]} ")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]} ")
    print("\n")

def winner(b):
    for a, c, d in LINES:
        if b[a] == b[c] == b[d] and b[a] in ("X","O"):
            return b[a]
    if all(x in ("X","O") for x in b):
        return "draw"
    return None

def available_moves(b):
    return [i for i, v in enumerate(b) if v not in ("X","O")]

def minimax(b, ai, human, is_ai_turn, depth=0):
    w = winner(b)
    if w == ai:
        return 10 - depth, None
    if w == human:
        return depth - 10, None
    if w == "draw":
        return 0, None

    if is_ai_turn:
        best_score = -math.inf
        best_move = None
        for m in available_moves(b):
            b[m] = ai
            score, _ = minimax(b, ai, human, False, depth+1)
            b[m] = str(m+1)
            if score > best_score:
                best_score, best_move = score, m
        return best_score, best_move
    else:
        best_score = math.inf
        best_move = None
        for m in available_moves(b):
            b[m] = human
            score, _ = minimax(b, ai, human, True, depth+1)
            b[m] = str(m+1)
            if score < best_score:
                best_score, best_move = score, m
        return best_score, best_move

def ai_move(b, ai, human):
    _, move = minimax(b, ai, human, True)
    return move

def main():
    board = [str(i+1) for i in range(9)]
    human = input("Choose your symbol (X goes first) [X/O]: ").strip().upper() or "X"
    if human not in ("X","O"):
        human = "X"
    ai = "O" if human == "X" else "X"
    current = "X"
    print_board(board)

    while True:
        if current == human:
            mv = input(f"Your move ({human}) 1-9: ").strip()
            if mv not in [str(i) for i in range(1,10)]:
                print("Invalid input.")
                continue
            idx = int(mv) - 1
            if board[idx] in ("X","O"):
                print("Spot taken.")
                continue
            board[idx] = human
        else:
            move = ai_move(board, ai, human)
            board[move] = ai
            print(f"AI ({ai}) chooses {move+1}")

        print_board(board)
        w = winner(board)
        if w in ("X","O"):
            print(f"{w} wins!")
            break
        elif w == "draw":
            print("It's a draw.")
            break

        current = "O" if current == "X" else "X"

if __name__ == "__main__":
    main()