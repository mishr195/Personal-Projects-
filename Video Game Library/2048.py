import random
import copy
import tkinter as tk
from tkinter import messagebox

def initialize_board():
        # Initialize a 4x4 board with two random tiles
        board = [[0] * 4 for _ in range(4)]
        add_new_tile(board)
        add_new_tile(board)
        return board

def print_board(board):
        for row in board:
            print(" ".join(map(str, row)))

def add_new_tile(board):
        # Add a new tile (2 or 4) to a random empty cell
        empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            board[i][j] = random.choice([2, 4])

def move(board, direction):
        # Move the tiles in the specified direction
        original_board = copy.deepcopy(board)

        if direction == 'up':
            for j in range(4):
                col = [board[i][j] for i in range(4) if board[i][j] != 0]
                col = merge_tiles(col)
                for i in range(4):
                    board[i][j] = col[i] if i < len(col) else 0

        elif direction == 'down':
            for j in range(4):
                col = [board[i][j] for i in range(3, -1, -1) if board[i][j] != 0]
                col = merge_tiles(col)
                for i in range(3, -1, -1):
                    board[i][j] = col[3 - i] if 3 - i < len(col) else 0

        elif direction == 'left':
            for i in range(4):
                row = [board[i][j] for j in range(4) if board[i][j] != 0]
                row = merge_tiles(row)
                for j in range(4):
                    board[i][j] = row[j] if j < len(row) else 0

        elif direction == 'right':
            for i in range(4):
                row = [board[i][j] for j in range(3, -1, -1) if board[i][j] != 0]
                row = merge_tiles(row)
                for j in range(3, -1, -1):
                    board[i][j] = row[3 - j] if 3 - j < len(row) else 0

        return original_board != board

def merge_tiles(line):
        # Merge adjacent identical tiles in a line
        merged_line = []
        i = 0
        while i < len(line):
            if i < len(line) - 1 and line[i] == line[i + 1]:
                merged_line.append(line[i] * 2)
                i += 2
            else:
                merged_line.append(line[i])
                i += 1
        return merged_line + [0] * (len(line) - len(merged_line))

def is_game_over(board):
        # Check if the game is over (no more moves)
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0 or (i < 3 and board[i][j] == board[i + 1][j]) or \
                (j < 3 and board[i][j] == board[i][j + 1]):
                    return False
        return True

def game_over():
        result = messagebox.askquestion("Game Over", "Do you want to play again?")
        return result == 'yes'

def reset_game():
        global board
        board = initialize_board()
        update_display()

def update_display():
        canvas.delete("all")
        for i in range(4):
            for j in range(4):
                value = board[i][j]
                color = get_tile_color(value)
                canvas.create_rectangle(j * 80, i * 80, (j + 1) * 80, (i + 1) * 80, fill=color, outline="black")
                if value != 0:
                    canvas.create_text((j + 0.5) * 80, (i + 0.5) * 80, text=str(value), font=('Helvetica', 20, 'bold'))

        if is_game_over(board):
            if game_over():
                reset_game()

def get_tile_color(value):
        colors = {
            0: "#CDC1B4",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E",
        }
        return colors.get(value, "#CDC1B4")


root = tk.Tk()
root.title("2048 Game")


board = initialize_board()

canvas = tk.Canvas(root, width=320, height=320, bg="#BBADA0")
canvas.pack()

def handle_key(event):
        direction = None
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            direction = event.keysym.lower()
        if direction:
            if move(board, direction):
                add_new_tile(board)
                update_display()


root.bind('<Up>', handle_key)
root.bind('<Down>', handle_key)
root.bind('<Left>', handle_key)
root.bind('<Right>', handle_key)

update_display()
root.mainloop()

