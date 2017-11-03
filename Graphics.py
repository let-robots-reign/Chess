import tkinter as tk
from Chess import *


def prepare_and_start():
    """
    Function that initializes the board.
    """
    canvas.delete('all')
    color_index = 0

    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = 50 + col * CELL_SIZE, 50 + row * CELL_SIZE
            x2, y2 = 50 + col * CELL_SIZE + CELL_SIZE, 50 + row * CELL_SIZE + CELL_SIZE
            canvas.create_rectangle((x1, y1), (x2, y2), fill=cell_colors[color_index])
            make_button(x1, y1, color_index)
            color_index = not color_index
        color_index = not color_index


def make_button(row, col, color):
    """
    Making the buttons.
    """
    if (row, col) in coords_to_piece:  # making the piece button
        tk.Button(master, image=coords_to_piece[row, col], bg=cell_colors[color], height=95, width=95).place(x=row, y=col)
    else:  # making the cell button
        if color == 0:
            tk.Button(master, image=white_cell_pic, bg=cell_colors[color], height=95, width=95).place(x=row, y=col)
        elif color == 1:
            tk.Button(master, image=black_cell_pic, bg=cell_colors[color], height=95, width=95).place(x=row, y=col)


ROWS = COLS = 8
CELL_SIZE = 100
cell_colors = ['#EADEBD', '#2E3234']  # 0 - black, 1 - white
master = tk.Tk()
white_cell_pic = tk.PhotoImage(file='white_cell.gif')
black_cell_pic = tk.PhotoImage(file='black_cell.gif')
black_rook_pic = tk.PhotoImage(file='black_rook.gif')
black_knight_pic = tk.PhotoImage(file='black_knight.gif')
black_bishop_pic = tk.PhotoImage(file='black_bishop.gif')
black_queen_pic = tk.PhotoImage(file='black_queen.gif')
black_king_pic = tk.PhotoImage(file='black_king.gif')
black_pawn_pic = tk.PhotoImage(file='black_pawn.gif')
white_rook_pic = tk.PhotoImage(file='white_rook.gif')
white_knight_pic = tk.PhotoImage(file='white_knight.gif')
white_bishop_pic = tk.PhotoImage(file='white_bishop.gif')
white_queen_pic = tk.PhotoImage(file='white_queen.gif')
white_king_pic = tk.PhotoImage(file='white_king.gif')
white_pawn_pic = tk.PhotoImage(file='white_pawn.gif')

coords_to_piece = {(50, 50): black_rook_pic, (150, 50): black_knight_pic, (250, 50): black_bishop_pic,
                   (350, 50): black_queen_pic, (450, 50): black_king_pic, (550, 50): black_bishop_pic,
                   (650, 50): black_knight_pic, (750, 50): black_rook_pic, (50, 150): black_pawn_pic,
                   (150, 150): black_pawn_pic, (250, 150): black_pawn_pic, (350, 150): black_pawn_pic,
                   (450, 150): black_pawn_pic, (550, 150): black_pawn_pic, (650, 150): black_pawn_pic,
                   (750, 150): black_pawn_pic, (50, 750): white_rook_pic, (150, 750): white_knight_pic,
                   (250, 750): white_bishop_pic, (350, 750): white_queen_pic, (450, 750): white_king_pic,
                   (550, 750): white_bishop_pic, (650, 750): white_knight_pic, (750, 750): white_rook_pic,
                   (50, 650): white_pawn_pic, (150, 650): white_pawn_pic, (250, 650): white_pawn_pic,
                   (350, 650): white_pawn_pic, (450, 650): white_pawn_pic, (550, 650): white_pawn_pic,
                   (650, 650): white_pawn_pic, (750, 650): white_pawn_pic,}


canvas = tk.Canvas(master, width=CELL_SIZE * ROWS + 100, height=CELL_SIZE * COLS + 100)
canvas.pack()
prepare_and_start()
master.mainloop()
