# Tic-Tac-Toe: Simple 2-player terminal version

def print_board(b):
    print("\n")
    print(f" {b[0]} | {b[1]} | {b[2]} ")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]} ")
    print("\n")

def check_winner(b):
    lines = [
        (0,1,2),(3,4,5),(6,7,8), # rows
        (0,3,6),(1,4,7),(2,5,8), # cols
        (0,4,8),(2,4,6)          # diagonals
    ]
    for i, j, k in lines:
        if b[i] == b[j] == b[k] and b[i] in ("X", "O"):
            return b[i]
    if all(cell in ("X", "O") for cell in b):
        return "draw"
    return None

def main():
    board = [str(i+1) for i in range(9)]
    player = "X"
    print("Tic-Tac-Toe — 2 Players")
    print("Enter positions 1-9.\n")
    print_board(board)

    while True:
        move = input(f"Player {player}, choose a position (1-9): ").strip()
        if move not in [str(i) for i in range(1,10)]:
            print("Invalid input, try again.")
            continue
        idx = int(move) - 1
        if board[idx] in ("X", "O"):
            print("That spot is taken. Try another.")
            continue
        board[idx] = player
        print_board(board)

        result = check_winner(board)
        if result == "X" or result == "O":
            print(f"🎉 Player {result} wins!")
            break
        elif result == "draw":
            print("It's a draw!")
            break

        player = "O" if player == "X" else "X"

if __name__ == "__main__":
    main()