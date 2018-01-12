import tkinter as tk
from Chess import *


def get_cell_color(row, col):
    """
    Returns the color of the given cell.
    """
    if row % 2 == 0 and col % 2 == 0:
        return 1
    elif row % 2 == 0 and col % 2 == 1:
        return 0
    elif row % 2 == 1 and col % 2 == 0:
        return 0
    elif row % 2 == 1 and col % 2 == 1:
        return 1


def prepare_and_start():
    """
    Function that initializes the board.
    """
    canvas.delete('all')
    v.set('Ход белых')
    tk.Label(master, textvariable=v, font=("Tahoma, 16")).place(x=415, y=860)
    color_index = 0
    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = 50 + col * CELL_SIZE, 50 + row * CELL_SIZE
            piece = field[row][col]
            if piece is not None:
                if isinstance(piece, Pawn):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=white_pawn_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=black_pawn_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Rook):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=white_rook_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=black_rook_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Knight):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=white_knight_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=black_knight_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Bishop):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=white_bishop_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=black_bishop_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, Queen):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=white_queen_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=black_queen_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)

                elif isinstance(piece, King):
                    if piece.get_color() == WHITE:
                        tk.Button(master, image=white_king_pic, bg=cell_colors[color_index],
                                  height=95, width=95).place(x=x1, y=y1)
                    elif piece.get_color() == BLACK:
                        tk.Button(master, image=black_king_pic, bg=cell_colors[color_index],
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
    master.bind("<Button-1>", button_pressed)


def button_pressed(event):
    """
    Handles the move.
    """
    global turns
    info.set('                                                                                      ')
    turns.append((event.widget.winfo_y() // 100, event.widget.winfo_x() // 100))
    if len(turns) == 2:
        row, col, row1, col1 = turns[0][0], turns[0][1], turns[1][0], turns[1][1]
        piece = field[row][col]
        piece_literal = board.cell(row, col)
        if board.move_piece(row, col, row1, col1):
            tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=250, y=20)

            color_index1 = 0 if get_cell_color(row, col) == 0 else 1
            img1 = black_cell_pic if color_index1 == 0 else white_cell_pic
            tk.Button(master, image=img1, bg=cell_colors[color_index1], height=95, width=95).place(x=col * 100 + 50,
                                                                                                   y=row * 100 + 50)
            color_index2 = 1 if get_cell_color(row1, col1) == 0 else 0

            if piece_literal[1] == 'P':
                #print(1)
                img = white_pawn_pic if piece_literal[0] == 'b' else black_pawn_pic
                tk.Button(master, image=img, bg=cell_colors[color_index2], height=95, width=95).place(x=col1 * 100 + 50,
                                                                                                      y=row1 * 100 + 50)

            elif piece_literal[1] == 'R':
                img = white_rook_pic if piece_literal[0] == 'b' else black_rook_pic
                tk.Button(master, image=img, bg=cell_colors[color_index2], height=95, width=95).place(x=col1 * 100 + 50,
                                                                                                      y=row1 * 100 + 50)

            elif piece_literal[1] == 'N':
                img = white_knight_pic if piece_literal[0] == 'b' else black_knight_pic
                tk.Button(master, image=img, bg=cell_colors[color_index2], height=95, width=95).place(x=col1 * 100 + 50,
                                                                                                      y=row1 * 100 + 50)

            elif piece_literal[1] == 'K':
                img = white_king_pic if piece_literal[0] == 'b' else black_king_pic
                tk.Button(master, image=img, bg=cell_colors[color_index2], height=95, width=95).place(x=col1 * 100 + 50,
                                                                                                      y=row1 * 100 + 50)

            elif piece_literal[1] == 'Q':
                img = white_queen_pic if piece_literal[0] == 'b' else black_queen_pic
                tk.Button(master, image=img, bg=cell_colors[color_index2], height=95, width=95).place(x=col1 * 100 + 50,
                                                                                                      y=row1 * 100 + 50)

            elif piece_literal[1] == 'B':
                img = white_bishop_pic if piece_literal[0] == 'b' else black_bishop_pic
                tk.Button(master, image=img, bg=cell_colors[color_index2], height=95, width=95).place(x=col1 * 100 + 50,
                                                                                                      y=row1 * 100 + 50)

            if board.move_and_promote_pawn(row, col, row1, col1):  # Превращение пешки
                pawn = board.field[row][col]
                info.set('Введите фигуру, на которую хотите заменить пешку (Q, R, B, N): ')
                tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=150, y=20)
                piece_char = tk.Entry(master, width=20, bd=1).place(x=300, y=20)
                if piece_char == 'Q':
                    field[row1][col1] = Queen(row1, col1, pawn.get_color())
                    field[row][col] = None
                elif piece_char == 'R':
                    field[row1][col1] = Rook(row1, col1, pawn.get_color())
                    field[row][col] = None
                elif piece_char == 'B':
                    field[row1][col1] = Bishop(row1, col1, pawn.get_color())
                    field[row][col] = None
                elif piece_char == 'N':
                    field[row1][col1] = Knight(row1, col1, pawn.get_color())
                    field[row][col] = None
            if board.stalemate_white(board):
                info.set('Белым пат! Ничья!')
                tk.Label(master, textvaribale=info, font=("Tahoma, 16")).place(x=250, y=20)
            if board.stalemate_black(board):  # Не стоит elif, потому что возможен обоюдный пат
                info.set('Черным пат! Ничья!')
                tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=250, y=20)
            elif board.mate(board, board.king_white.row, board.king_white.col):
                info.set('Белому королю мат! Черные побеждают!')
                tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=250, y=20)
            elif board.mate(board, board.king_black.row, board.king_black.col):
                info.set('Черному королю мат! Черные побеждают!')
                tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=250, y=20)
            elif board.is_under_attack(board, board.king_white.row, board.king_white.col):
                info.set('Белому королю шах!')
                tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=250, y=20)
            elif board.is_under_attack(board, board.king_black.row, board.king_black.col):
                info.set('Черному королю шах!')
                tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=250, y=20)
        else:
            info.set('Координаты некорректы! Попробуйте другой ход!')
            tk.Label(master, textvariable=info, font=("Tahoma, 16")).place(x=250, y=20)
        #print(turns)
        turns = []
    if board.current_player_color() == BLACK:
        v.set('Ход белых')
        tk.Label(master, textvariable=v, font=("Tahoma, 16")).place(x=415, y=860)
    else:
        v.set('Ход черных')
        tk.Label(master, textvariable=v, font=("Tahoma, 16")).place(x=415, y=860)


ROWS = COLS = 8
CELL_SIZE = 100
cell_colors = ['#EADEBD', '#2E3234']  # 0 - black, 1 - white
turns = []
master = tk.Tk()
board = Board()
board.color = BLACK
v = tk.StringVar()
info = tk.StringVar()
field = board.field[::-1]
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
prepare_and_start()
master.mainloop()