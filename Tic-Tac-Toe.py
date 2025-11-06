"""
I acknowledge the use of Microsoft Copilot to co-create code in this file
(e.g., initial CLI version, minimax AI, and Tkinter GUI integration).
"""


import tkinter as tk
from tkinter import messagebox
import math

LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

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

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe")

        self.board = [str(i+1) for i in range(9)]
        self.buttons = []
        self.human = "X"
        self.ai = "O"
        self.current = "X"
        self.scores = {"X":0, "O":0, "draw":0}
        self.starter = "X"
        self.game_over = False

        header = tk.Frame(root)
        header.pack(padx=10, pady=10)

        self.info_var = tk.StringVar(value="Choose your symbol (X goes first).")
        tk.Label(header, textvariable=self.info_var, font=("Segoe UI", 12)).grid(row=0, column=0, columnspan=3, pady=(0,8))

        self.score_var = tk.StringVar()
        self.update_score()
        tk.Label(header, textvariable=self.score_var, font=("Segoe UI", 11)).grid(row=1, column=0, columnspan=3, pady=(0,10))

        sym = tk.Frame(header)
        sym.grid(row=2, column=0, columnspan=3, pady=(0,10))
        tk.Label(sym, text="You are:").pack(side=tk.LEFT, padx=(0,6))
        tk.Button(sym, text="X (first)", command=lambda: self.set_symbols("X")).pack(side=tk.LEFT, padx=4)
        tk.Button(sym, text="O (second)", command=lambda: self.set_symbols("O")).pack(side=tk.LEFT, padx=4)

        grid = tk.Frame(root)
        grid.pack(padx=10, pady=10)
        for i in range(9):
            btn = tk.Button(grid, text=" ", width=4, height=2,
                            font=("Segoe UI", 24, "bold"),
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        controls = tk.Frame(root)
        controls.pack(padx=10, pady=(0,10))
        tk.Button(controls, text="Restart Round", command=self.restart_round).grid(row=0, column=0, padx=5)
        tk.Button(controls, text="Reset Scores", command=self.reset_all).grid(row=0, column=1, padx=5)

    def set_symbols(self, human_choice):
        self.human = human_choice
        self.ai = "O" if self.human == "X" else "X"
        self.starter = "X"
        self.info_var.set(f"You are {self.human}. {self.starter} starts.")
        self.restart_round()

    def on_click(self, idx):
        if self.game_over or self.human != self.current:
            return
        if self.board[idx] in ("X","O"):
            return
        self.place(idx, self.human)
        self.after_move()

    def after_move(self):
        w = winner(self.board)
        if w:
            self.finish_round(w)
            return
        self.current = "O" if self.current == "X" else "X"
        if self.current == self.ai and not self.game_over:
            self.root.after(300, self.ai_turn)

    def ai_turn(self):
        _, move = minimax(self.board, self.ai, self.human, True)
        if move is not None:
            self.place(move, self.ai)
        self.after_move()

    def place(self, idx, symbol):
        self.board[idx] = symbol
        self.buttons[idx].configure(text=symbol, state="disabled")

    def finish_round(self, result):
        self.game_over = True
        if result in ("X","O"):
            self.scores[result] += 1
            msg = f"{result} wins!"
        else:
            self.scores["draw"] += 1
            msg = "It's a draw."
        self.update_score()
        self.info_var.set(msg + " Click 'Restart Round' to play again.")
        self.starter = "O" if self.starter == "X" else "X"

    def update_score(self):
        self.score_var.set(f"Scores  X: {self.scores['X']}   O: {self.scores['O']}   Draws: {self.scores['draw']}")

    def restart_round(self):
        self.board = [str(i+1) for i in range(9)]
        for btn in self.buttons:
            btn.configure(text=" ", state="normal")
        self.game_over = False
        self.current = self.starter
        self.info_var.set(f"You are {self.human}. {self.current} to move.")
        if self.current == self.ai:
            self.root.after(300, self.ai_turn)

    def reset_all(self):
        self.scores = {"X":0, "O":0, "draw":0}
        self.update_score()
        self.starter = "X"
        self.restart_round()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()