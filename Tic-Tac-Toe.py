import tkinter as tk
from tkinter import messagebox

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

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe")

        self.board = [str(i+1) for i in range(9)]
        self.buttons = []
        self.current = "X"
        self.game_over = False

        self.info_var = tk.StringVar(value=f"{self.current} to move.")
        tk.Label(root, textvariable=self.info_var, font=("Segoe UI", 12)).pack(pady=(10,0))

        grid = tk.Frame(root)
        grid.pack(padx=10, pady=10)

        for i in range(9):
            btn = tk.Button(grid, text=" ", width=4, height=2,
                            font=("Segoe UI", 24, "bold"),
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        tk.Button(root, text="Restart", command=self.restart).pack(pady=(0,10))

    def on_click(self, idx):
        if self.game_over:
            return
        if self.board[idx] in ("X","O"):
            return
        self.place(idx, self.current)
        w = winner(self.board)
        if w:
            self.finish(w)
            return
        self.current = "O" if self.current == "X" else "X"
        self.info_var.set(f"{self.current} to move.")

    def place(self, idx, sym):
        self.board[idx] = sym
        self.buttons[idx].configure(text=sym, state="disabled")

    def finish(self, res):
        self.game_over = True
        if res in ("X","O"):
            self.info_var.set(f"{res} wins! Click Restart.")
        else:
            self.info_var.set("Draw. Click Restart.")

    def restart(self):
        self.board = [str(i+1) for i in range(9)]
        for b in self.buttons:
            b.configure(text=" ", state="normal")
        self.game_over = False
        self.current = "X"
        self.info_var.set(f"{self.current} to move.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()