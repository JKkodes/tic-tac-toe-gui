#!/usr/bin/env python3

import random
import tkinter as tk
from tkinter import messagebox

# All winning triplets (0-based indices)
WIN_COMBOS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


class TicTacToeApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe (X = You, O = Computer)")

        # Board state: list of 9 elements, 'X', 'O', or ' ' for empty
        self.board = [' '] * 9

        # Create status label
        self.status_label = tk.Label(root, text="Your turn: click a number (1-9)", font=("Helvetica", 12))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))

        # Create 3x3 grid of buttons
        self.buttons = []
        for i in range(9):
            btn = tk.Button(root, text=str(i + 1), width=8, height=4,
                            font=("Helvetica", 20),
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=1 + i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        #play again / Reset button
        self.reset_button = tk.Button(root, text="Play Again / Reset", command=self.reset_board)
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=(5, 10))

        #Tracking whether the game is active (to prevent moves after game end)
        self.game_active = True

        # Start fresh
        self.reset_board()

   
    #UI and helper methods
    def reset_board(self):
        self.board = [' '] * 9
        for i, btn in enumerate(self.buttons):
            btn.config(text=str(i + 1), state="normal")
        self.game_active = True
        self.status_label.config(text="Your turn: click a number (1-9)")

    def on_click(self, index):
        if not self.game_active:
            return

        if self.board[index] != ' ':
            return

        #Player move
        self.board[index] = 'X'
        self.update_button(index, 'X', disabled=True)

        #checking for player's win or draw
        winner = self.check_winner(self.board)
        if winner == 'X':
            self.end_game("You win! Congratulations!")
            return
        if self.is_board_full(self.board):
            self.end_game("It's a draw!")
            return

#slight delay so it doesn't feel instant
        self.status_label.config(text="Computer is thinking...")
        self.root.after(250, self.computer_turn)

    def update_button(self, index, symbol, disabled=False):
        btn = self.buttons[index]
        btn.config(text=symbol)
        if disabled:
            btn.config(state="disabled")

    def end_game(self, message):
        self.game_active = False
        # Disable all buttons
        for btn in self.buttons:
            btn.config(state="disabled")
        self.status_label.config(text=message)
        # Show a popup as well
        messagebox.showinfo("Game Over", message)


    #Game logic methods
    def check_winner(self, board):
        """Check the board for a winner.
        Returns 'X' if player wins, 'O' if computer wins, or None if no winner yet."""
        for a, b, c in WIN_COMBOS:
            if board[a] == board[b] == board[c] and board[a] in ('X', 'O'):
                return board[a]
        return None

    def is_board_full(self, board):
        return all(cell in ('X', 'O') for cell in board)

    def available_moves(self, board):
        return [i for i, cell in enumerate(board) if cell == ' ']

    def computer_turn(self):
        if not self.game_active:
            return

        self.computer_move(self.board)

               # finding the new O and update its button
        for i, btn in enumerate(self.buttons):
            if self.board[i] == 'O' and btn['state'] != 'disabled':
                # Update this button to O and disable it
                self.update_button(i, 'O', disabled=True)
                break
            # If the button already shows 'O' (from previous state), ensure it's disabled
            if self.board[i] == 'O':
                btn.config(state="disabled")

        # Check for computer win or draw
        winner = self.check_winner(self.board)
        if winner == 'O':
            self.end_game("Computer wins! Better luck next time.")
            return
        if self.is_board_full(self.board):
            self.end_game("It's a draw!")
            return

        # Back to player's turn
        self.status_label.config(text="Your turn: click an empty cell")

    def computer_move(self, board):

        """picks the best available move for O"""

          # try to wininning move for O
        for idx in self.available_moves(board):
            board_copy = board[:]
            board_copy[idx] = 'O'
            if self.check_winner(board_copy) == 'O':
                board[idx] = 'O'
                return

           # otherwise block the player
        for idx in self.available_moves(board):
            board_copy = board[:]
            board_copy[idx] = 'X'
            if self.check_winner(board_copy) == 'X':
                board[idx] = 'O'
                return

        # 3) take center if open
        center = 4
        if board[center] == ' ':
            board[center] = 'O'
            return

        # 4) take a corner if possible
        corners = [0, 2, 6, 8]
        open_corners = [i for i in corners if board[i] == ' ']
        if open_corners:
            board[random.choice(open_corners)] = 'O'
            return

        # 5) Take any other open spot (sides)
        sides = [1, 3, 5, 7]
        open_sides = [i for i in sides if board[i] == ' ']
        if open_sides:
            board[random.choice(open_sides)] = 'O'
            return

        # Fallback (shouldn't be needed): random open spot
        moves = self.available_moves(board)
        if moves:
            board[random.choice(moves)] = 'O'


def main():
# keeps board size fixed
    root = tk.Tk()
 # keeps board size fixed
    root.resizable(False, False)
    app = TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()