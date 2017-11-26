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

            piece = board.field[row][col]
            if piece is not None:
                if isinstance(piece, Pawn):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=black_pawn_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=white_pawn_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Rook):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=black_rook_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=white_rook_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Knight):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=black_knight_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=white_knight_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Bishop):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=black_bishop_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=white_bishop_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Queen):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=black_queen_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=white_queen_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, King):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=black_king_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=white_king_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

            else:
                if color_index == 0:
                    tk.Button(master, image=white_cell_pic, bg=cell_colors[color_index],
                              height=95, width=95).place(x=x1, y=y1)
                elif color_index == 1:
                    tk.Button(master, image=black_cell_pic, bg=cell_colors[color_index],
                              height=95, width=95).place(x=x1, y=y1)

            color_index = not color_index
        color_index = not color_index


def button_pressed(event):
    turns.append((event.widget.winfo_y() // 100, event.widget.winfo_x() // 100))
    if len(turns) % 2 == 0 and len(turns) > 0:
        row, col, row1, col1 = turns[-2][0], turns[-2][1], turns[-1][0], turns[-1][1]
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
            if board.move_and_promote_pawn(row, col, row1, col1):  # Превращение пешки
                pawn = board.field[row][col]
                piece_char = input('Введите фигуру, на которую хотите заменить пешку (Q, R, B, N): ')
                if piece_char == 'Q':
                    board.field[row1][col1] = Queen(row1, col1, pawn.get_color())
                    board.field[row][col] = None
                elif piece_char == 'R':
                    board.field[row1][col1] = Rook(row1, col1, pawn.get_color())
                    board.field[row][col] = None
                elif piece_char == 'B':
                    board.field[row1][col1] = Bishop(row1, col1, pawn.get_color())
                    board.field[row][col] = None
                elif piece_char == 'N':
                    board.field[row1][col1] = Knight(row1, col1, pawn.get_color())
                    board.field[row][col] = None
            if board.stalemate_white(board):
                print('Белым пат! Ничья!')
            if board.stalemate_black(board):  # Не стоит elif, потому что возможен обоюдный пат
                print('Черным пат! Ничья!')
            elif board.mate(board, board.king_white.row, board.king_white.col):
                print('Белому королю мат! Черные побеждают!')
            elif board.mate(board, board.king_black.row, board.king_black.col):
                print('Черному королю мат! Белые побеждают!')
            elif board.is_under_attack(board, board.king_white.row, board.king_white.col):
                print('Белому королю шах!')
            elif board.is_under_attack(board, board.king_black.row, board.king_black.col):
                print('Черному королю шах!')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')
        main()


def main():
    prepare_and_start()
    master.bind("<Button-1>", button_pressed)


ROWS = COLS = 8
CELL_SIZE = 100
cell_colors = ['#EADEBD', '#2E3234']  # 0 - black, 1 - white
turns = []
master = tk.Tk()
board = Board()
board.color = BLACK
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
canvas = tk.Canvas(master, width=CELL_SIZE * ROWS + 100, height=CELL_SIZE * COLS + 100)
canvas.pack()
main()
master.mainloop()
