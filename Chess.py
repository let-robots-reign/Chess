WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):  # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        # Варианты ответа на введенный ход
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
            if board.move_and_promote_pawn(row, col, row1, col1):  # Превращение пешки
                pawn = board.field[row][col]
                piece_char = input('Введите фигуру, на которую хотите заменить пешку: ')
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
            if board.mate(board, board.king_white.row, board.king_white.col):
                print('Белому королю мат! Черные побеждают!')
            elif board.mate(board, board.king_black.row, board.king_black.col):
                print('Черному королю мат! Белые побеждают!')
            elif board.is_under_attack(board, board.king_white.row, board.king_white.col):
                print('Белому королю шах!')
            elif board.is_under_attack(board, board.king_black.row, board.king_black.col):
                print('Черному королю шах!')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


def correct_coords(row, col):
    """
    Функция проверяет, что координаты (row, col) лежат
    внутри доски
    """
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        self.king_white = King(0, 4, WHITE)
        self.king_black = King(7, 4, BLACK)
        # Задаем фигуры на доске
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(0, 0, WHITE), Knight(0, 1, WHITE), Bishop(0, 2, WHITE), Queen(0, 3, WHITE),
            self.king_white, Bishop(0, 5, WHITE), Knight(0, 6, WHITE), Rook(0, 7, WHITE)
        ]
        self.field[1] = [
            Pawn(1, 0, WHITE), Pawn(1, 1, WHITE), Pawn(1, 2, WHITE), Pawn(1, 3, WHITE),
            Pawn(1, 4, WHITE), Pawn(1, 5, WHITE), Pawn(1, 6, WHITE), Pawn(1, 7, WHITE)
        ]
        self.field[6] = [
            Pawn(6, 0, BLACK), Pawn(6, 1, BLACK), Pawn(6, 2, BLACK), Pawn(6, 3, BLACK),
            Pawn(6, 4, BLACK), Pawn(6, 5, BLACK), Pawn(6, 6, BLACK), Pawn(6, 7, BLACK)
        ]
        self.field[7] = [
            Rook(7, 0, BLACK), Knight(7, 1, BLACK), Bishop(7, 2, BLACK), Queen(7, 3, BLACK),
            self.king_black, Bishop(7, 5, BLACK), Knight(7, 6, BLACK), Rook(7, 7, BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """
        Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.
        """
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        """
        Возвращает объект - фигуру
        """
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        """
        Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет -- вернёт False
        """
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # Нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
        return True

    def is_under_attack(self, board, row, col):
        """
        Проверка, находится ли данная клетка под боем.
        Используется для идентификации шаха.
        """
        global figures
        figures = []  # Список атакующих фигур (нужно для функции определения мата)
        for i in self.field:
            for piece in i:
                if piece is not None:
                    if self.field[row][col] is not None:
                        if piece.get_color() != self.field[row][col].get_color() \
                                and piece.can_move(board, piece.row, piece.col, row, col):
                            figures.append([piece, piece.row, piece.col])
        if len(figures) > 0:
            return True
        return False

    def mate(self, board, row, col):
        """
        Проверка на мат.
        """
        if self.is_under_attack(board, row, col):  # Проверяем, атаковано ли поле с королем
            possible_moves = 0  # Число возможных побегов
            if correct_coords(row + 1, col - 1):  # Проверяем, атакованы ли соседние с королём и свободные от его фигур поля
                if self.move_piece(row, col, row + 1, col - 1) and not self.is_under_attack(board, row + 1, col - 1):
                    possible_moves += 1
            if correct_coords(row + 1, col):
                if self.move_piece(row, col, row + 1, col) and not self.is_under_attack(board, row + 1, col):
                    possible_moves += 1
            if correct_coords(row + 1, col + 1):
                if self.move_piece(row, col, row + 1, col + 1) and not self.is_under_attack(board, row + 1, col + 1):
                    possible_moves += 1
            if correct_coords(row, col + 1):
                if self.move_piece(row, col, row, col + 1) and not self.is_under_attack(board, row, col + 1):
                    possible_moves += 1
            if correct_coords(row - 1, col + 1):
                if self.move_piece(row, col, row - 1, col + 1) and not self.is_under_attack(board, row - 1, col + 1):
                    possible_moves += 1
            if correct_coords(row - 1, col):
                if self.move_piece(row, col, row - 1, col) and not self.is_under_attack(board, row - 1, col):
                    possible_moves += 1
            if correct_coords(row - 1, col - 1):
                if self.move_piece(row, col, row - 1, col - 1) and not self.is_under_attack(board, row - 1, col - 1):
                    possible_moves += 1
            if correct_coords(row, col - 1):
                if self.move_piece(row, col, row, col - 1) and not self.is_under_attack(board, row, col - 1):
                    possible_moves += 1
            if possible_moves == 0:
                # Ситуация без возможных выходов
                # Остается либо закрыть короля своей фигурой, либо съесть нападающую фигуру
                if len(figures) > 1:
                    return True  # Если атакующих фигур две, то это мат
                elif self.is_under_attack(board, figures[0][1], figures[0][2]):
                    return False  # Если атакующую фигуру можно съесть, то не мат
                # Если фигуру нельзя съесть, остается только закрыть ее
                elif isinstance(figures[0][0], Knight):  # Если фигура -- конь, то закрыть ее нельзя
                    return True
                # Фигуру также нельзя закрыть в том случае, если она стоит на соседнем поле
                else:
                    if correct_coords(row + 1, col - 1):
                        if (row + 1, col - 1) == (figures[0][1], figures[0][2]):
                            return True
                    if correct_coords(row + 1, col):
                        if (row + 1, col) == (figures[0][1], figures[0][2]):
                            return True
                    if correct_coords(row + 1, col + 1):
                        if (row + 1, col + 1) == (figures[0][1], figures[0][2]):
                            return True
                    if correct_coords(row, col + 1):
                        if (row, col + 1) == (figures[0][1], figures[0][2]):
                            return True
                    if correct_coords(row - 1, col + 1):
                        if (row - 1, col + 1) == (figures[0][1], figures[0][2]):
                            return True
                    if correct_coords(row - 1, col):
                        if (row - 1, col) == (figures[0][1], figures[0][2]):
                            return True
                    if correct_coords(row - 1, col - 1):
                        if (row - 1, col - 1) == (figures[0][1], figures[0][2]):
                            return True
                    if correct_coords(row, col - 1):
                        if (row, col - 1) == (figures[0][1], figures[0][2]):
                            return True

                    #  Если фигура не стоит на соседнем поле, то происходит проверка, можно ли перекрыть линию атаки
                    #  Еще не реализовано
            return False  # Если есть выход, то не мат
        return False

    def move_and_promote_pawn(self, row, col, row1, col1):
        piece = self.field[row][col]
        if not isinstance(piece, Pawn):
            return False
        if self.field[row1][col1] is not None:
            piece1 = self.field[row1][col1]
            if piece1.get_color() == piece.get_color():
                return False
        if not correct_coords(row1, col1):
            return False
        if (abs(row1 - row)) > 1 or (abs(col1 - col)) > 1:
            return False
        if row == row1 and col == col1:
            return False
        if (self.field[row1][col1] is not None) and (row + 1 == row1) and (col == col1) and piece.get_color() == WHITE:
            return False
        if (self.field[row1][col1] is not None) and (row - 1 == row1) and (col == col1) and piece.get_color() == BLACK:
            return False
        if row1 < row and piece.get_color() == WHITE:
            return False
        if row1 > row and piece.get_color() == BLACK:
            return False
        return True

    def castling_white0(self):  # Рокировка с Rook(0, 0)
        if isinstance(self.field[0][4], King) and isinstance(self.field[0][0], Rook):
            if self.field[0][0].turns > 0:
                return False
            if self.field[0][4].turns > 0:
                return False
            if self.field[0][1] is not None or self.field[0][2] is not None or self.field[0][3] is not None:
                return False
            self.field[0][2] = King(0, 2, WHITE)
            self.field[0][4] = None
            self.field[0][0] = None
            self.field[0][3] = Rook(0, 3, WHITE)
            return True

    def castling_black0(self):  # Рокировка с Rook(7, 0)
        if isinstance(self.field[7][0], Rook) and isinstance(self.field[7][4], King):
            if self.field[7][0].turns > 0:
                return False
            if self.field[7][4].turns > 0:
                return False
            if self.field[7][3] is not None or self.field[7][2] is not None or self.field[7][1] is not None:
                return False
            self.field[7][2] = King(7, 2, BLACK)
            self.field[7][4] = None
            self.field[7][0] = None
            self.field[7][3] = Rook(7, 2, BLACK)
            return True
        return False

    def castling_white7(self):  # Рокировка с Rook(0, 7)
        if isinstance(self.field[0][4], King) and isinstance(self.field[0][7], Rook):
            if self.field[0][7].turns > 0:
                return False
            if self.field[0][4].turns > 0:
                return False
            if self.field[0][5] is not None or self.field[0][6] is not None:
                return False
            self.field[0][6] = King(0, 6, WHITE)
            self.field[0][4] = None
            self.field[0][7] = None
            self.field[0][5] = Rook(0, 5, WHITE)
            return True

    def castling_black7(self):  # Рокировка с Rook(7, 7)
        if isinstance(self.field[7][7], Rook) and isinstance(self.field[7][4], King):
            if self.field[7][7].turns > 0:
                return False
            if self.field[7][4].turns > 0:
                return False
            if self.field[7][5] is not None or self.field[7][6] is not None:
                return False
            self.field[7][6] = King(7, 6, BLACK)
            self.field[7][4] = None
            self.field[7][7] = None
            self.field[7][5] = Rook(7, 5, BLACK)
            return True
        return False


class Piece:  # Класс, от которого наследуются все фигуры
    def __init__(self, row, col, color):  # Определение координат фигуры и цвета
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):  # Переопределение координат фигуры
        self.row = row
        self.col = col

    def get_color(self):  # Метод возвращает цвет фигуры
        return self.color


class Pawn(Piece):  # Класс, описывающий пешку
    def __init__(self, row, col, color):
        super().__init__(row, col, color)  # Параметры row, col, color, наследуются от класса Piece
        self.two_ranks_move = False  # Параметр нужен для "взятия на проходе"

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Взятие на проходе
        if self.get_color() == WHITE:
            if isinstance(board.field[row1 - 1][col1], Pawn):  # Проверяем, есть ли по соседству пешки
                if board.field[row1 - 1][col1].two_ranks_move and board.field[row1 - 1][col1].get_color() == BLACK:
                    board.field[row1 - 1][col1] = None
                    return True
        elif self.get_color() == BLACK:
            if isinstance(board.field[row1 + 1][col1], Pawn):
                if board.field[row1 + 1][col1].two_ranks_move and board.field[row1 + 1][col1].get_color() == WHITE:
                    board.field[row1 + 1][col1] = None
                    return True

        # Пешка может ходить только по вертикали
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            self.two_ranks_move = False
            return True

        # ход на 2 клетки из начального положения
        if row == start_row and row + 2 * direction == row1 and board.field[row + direction][col] is None:
            self.two_ranks_move = True
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):  # Пешка - единственная фигура, которая атакует не так, как ходит
        direction = 1 if (self.color == WHITE) else -1
        return row + direction == row1 and (col + 1 == col1 or col - 1 == col1)


class Rook(Piece):  # Класс, описывающий ладью
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.turns = 0  # Количество ходов, нужно для рокировки

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(row, c) is None):
                return False
        self.turns += 1
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight(Piece):  # Класс, описывающий коня
    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        res = [abs(col - col1), abs(row - row1)]
        if min(res) == 1 and max(res) == 2:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(Piece):  # Класс, описывающий короля
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.turns = 0  # Количество ходов, нужно для рокировки

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if abs(row1 - row) > 1 or abs(col1 - col) > 1:
            return False
        if board.is_under_attack(board, row1, col1):  # Запрет хода королем под шах
            return False
        if (row1, col1) == (0, 2):
            return board.castling_white0()
        elif (row1, col1) == (0, 6):
            return board.castling_white7()
        elif (row1, col1) == (7, 2):
            return board.castling_black0()
        elif (row1, col1) == (7, 6):
            return board.castling_black7()
        self.turns += 1
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Piece):  # Класс, описывающий ферзя
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        piece = board.get_piece(row1, col1)
        if row == row1 and col == col1:
            return False
        if piece is not None:
            if piece.get_color() == self.color:
                return False
        xr = abs(row1 - row)
        xc = abs(col1 - col)
        if row1 != row and col1 != col and xc != xr:
            return False

        dx = 1 if row1 > row else -1 if row1 < row else 0  # Проверка, что на пути фигуры нет других фигур
        dy = 1 if col1 > col else -1 if col1 < col else 0
        x = row + dx
        y = col + dy
        while x != row1 or y != col1:
            if not (board.get_piece(x, y) is None):
                return False
            x = x + dx
            y = y + dy
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):  # Класс, описывающий слона
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        res = [abs(col - col1), abs(row - row1)]
        if res[0] != res[1]:
            return False

        dx = 1 if row1 > row else -1 if row1 < row else 0  # Проверка, что на пути фигуры нет других фигур
        dy = 1 if col1 > col else -1 if col1 < col else 0
        x = row + dx
        y = col + dy
        while x != row1 or y != col1:
            if not (board.get_piece(x, y) is None):
                return False
            x = x + dx
            y = y + dy
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

if __name__ == "__main__":
    main()