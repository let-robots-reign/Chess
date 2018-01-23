WHITE = 0
BLACK = 1
number_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
letter_to_number = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


def opponent(color):
    """
    Returns the color opposite to the current one.
    """
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):
    """
    Prints the board in ASCII
    """
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row + 1, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(number_to_letter[col], end='    ')
    print()


def main():
    """
    Main function.
    Handling the move.
    """
    board = Board()  # Создаём шахматную доску
    while True:  # Цикл ввода команд игроков
        print_board(board)  # Выводим положение фигур на доске
        print('Команды:')  # Подсказка по командам
        print('    exit                               -- выход')
        print('    <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        if board.current_player_color() == WHITE:  # Выводим приглашение игроку нужного цвета
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        # Переводим команду из понятных человеку в цифры ряда и столбца
        row, col = int(command[1]) - 1, letter_to_number[command[0]]
        row1, col1 = int(command[4]) - 1, letter_to_number[command[3]]
        # Варианты ответа на введенный ход
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
            '''if board.move_and_promote_pawn(row, col, row1, col1):  # Превращение пешки
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
                    board.field[row][col] = None'''
            if board.stalemate_white(board):  # Пат белым
                print('Белым пат! Ничья!')
                raise SystemExit
            if board.stalemate_black(board):  # Пат черным. Не стоит elif, потому что возможен обоюдный пат
                print('Черным пат! Ничья!')
                raise SystemExit
            elif board.mate(board, board.king_white.row, board.king_white.col):  # Мат белым
                print('Белому королю мат! Черные побеждают!')
                raise SystemExit
            elif board.mate(board, board.king_black.row, board.king_black.col):  # Мат черным
                print('Черному королю мат! Белые побеждают!')
                raise SystemExit
            elif board.is_under_attack(board, board.king_white.row, board.king_white.col):  # Шах белым
                print('Белому королю шах!')
            elif board.is_under_attack(board, board.king_black.row, board.king_black.col):  # Шах черным
                print('Черному королю шах!')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


def correct_coords(row, col):
    """
    Checks if "row" and "col" are within the board.
    """
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE  # начальный цвет - белый
        self.field = []  # список доски (пока пустой)
        self.king_white = King(0, 4, WHITE)  # объект короля белых
        self.king_black = King(7, 4, BLACK)  # объект короля черных
        # Задаем фигуры на доске
        for row in range(8):
            self.field.append([None] * 8)  # Вначале заполняем 64 клетки типом None
        # Заполняем доску фигурами
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
        return self.color  # возвращает цвет текущего игрока

    def cell(self, row, col):
        """
        Returns a string representing the piece.
        Format: 'w' or 'b' + piece char.
        """
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        """
        Returns an object representing the piece.
        """
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        """
        Moves the piece from (row, col) to (row1, col1)
        If movable, returns True
        Otherwise, False
        """
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False # Нельзя пойти за пределы доски
        if row == row1 and col == col1:
            return False  # Нельзя пойти в ту же клетку
        piece = self.field[row][col]  # "Вытаскиваем фигуру"
        if piece is None:
            return False  # Если не фигура
        if piece.get_color() != self.color:
            return False  # Если фигура не того цвета
        if self.field[row1][col1] is None:                          # Если клетка, в которую ходим, свободна
            if not piece.can_move(self, row, col, row1, col1):      # Но если фигура туда пойти не может,
                return False                                        # Вернет False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):  # Если в клетке - фигура другого цвета
            if not piece.can_attack(self, row, col, row1, col1):                 # Но если фигура не может ее атаковать
                return False                                                     # Вернет False
        else:
            return False  # если в клетке - фигура того же цвета, вернет False
        if isinstance(piece, King) and self.is_under_attack(self, row1, col1):  # Запрет хода королем под шах
            return False
        if (self.color == WHITE and self.is_under_attack(self, self.king_white.row, self.king_white.col)) \
                or (self.color == BLACK and self.is_under_attack(self, self.king_black.row, self.king_black.col)):
            # Запрет хода, не уводящего короля из-под шаха
            return False
        # Если дошли до этого момента, осуществляем ход.
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)  # Обновляем позицию фигуры.
        self.color = opponent(self.color)  # Инверсируем цвет.
        return True

    def is_under_attack(self, board, row, col):
        """
        Checks if the cell is under attack
        Used in identifying check.
        """
        if not correct_coords(row, col):
            return False
        global figures  # Делаем так, чтобы список был доступен вне функции.
        figures = []  # Список атакующих фигур (нужно для функции определения мата)
        for i in self.field:  # Для каждого ряда на доске
            for piece in i:  # Для каждой клетки в ряду
                if piece is not None:  # Если клетка содержит фигуру
                    if self.field[row][col] is None:  # Если анализируемая клетка пуста
                        # Если цвет фигуры противоположен цвету клетки и фигура может туда переместиться
                        if piece.get_color() != self.current_player_color() \
                                and piece.can_move(board, piece.row, piece.col, row, col):
                            figures.append([piece, piece.row, piece.col])  # Добавляем в список фигуру и ее координаты
                    else:
                        # То же, но только сравнивается не с текущим цветом, а с цветом фигуры на анализируемой клетке
                        if piece.get_color() != self.field[row][col].get_color() \
                                and piece.can_move(board, piece.row, piece.col, row, col):
                            figures.append([piece, piece.row, piece.col])
        if len(figures) > 0:  # Если список непустой
            return True
        return False

    def mate(self, board, row, col):
        """
        Identifying mate.
        """
        if self.is_under_attack(board, row, col):  # Проверяем, атаковано ли поле с королем
            possible_move = False  # Возможность побега
            #  Проверяем, атакованы ли соседние с королём и свободные от его фигур поля
            moves_king = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]  # Возможные ходы
            for i in moves_king: # Проходимся по возможным ходам
                if self.get_piece(row, col).can_move(board, row, col, row + i[0], col + i[1])\
                        and not self.is_under_attack(board, row + i[0], col + i[1]):
                    possible_move = True

            if not possible_move:
                # Ситуация без возможных выходов
                # Остается либо закрыть короля своей фигурой, либо съесть нападающую фигуру
                if len(figures) > 1:
                    return True  # Если атакующих фигур две, то это мат
                elif self.is_under_attack(board, figures[0][1], figures[0][2]):  # В figures записаны координаты атакующей фигуры
                    return False  # Если атакующую фигуру можно съесть, то не мат
                # Если фигуру нельзя съесть, остается только закрыть ее
                elif isinstance(figures[0][0], Knight):  # Если фигура -- конь, то закрыть ее нельзя
                    return True
                # Фигуру также нельзя закрыть в том случае, если она стоит на соседнем поле
                else:
                    for i in moves_king:
                        if (row + i[0], col + i[1]) == (figures[0][1], figures[0][2]):
                            return True

                    #  Если фигура не стоит на соседнем поле, то происходит проверка, можно ли перекрыть линию атаки
                    # TODO: check if the player is able to defend the king.
                    #  Еще не реализовано
            return False  # Если есть выход, то не мат
        return False

    def stalemate_white(self, board):
        """
        Checking the stalemate for white.
        To know if the player is able to move, "go through" all possible options.
        At the same time, the king mustn't be checked.
        """
        if self.is_under_attack(board, self.king_white.row, self.king_white.col):  # Если король под шахом, то не пат
            return False
        if self.current_player_color() == WHITE:
            for i in self.field:
                for piece in i:
                    if piece is not None and piece.get_color() == WHITE:
                        row, col = piece.row, piece.col
                        if isinstance(piece, Pawn):  # У пешки есть 4 возможных варианта хода
                            moves_pawn = [(1, 0), (2, 0), (1, 1), (1, -1)]
                            for j in moves_pawn:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False  # Если у стороны есть хотя бы один ход, то это не пат

                        elif isinstance(piece, Rook):
                            for j in range(8):
                                if piece.can_move(self, row, col, row, j):  # Проходимся по ряду, где стоит ладья
                                    return False
                                elif piece.can_move(self, row, col, j, col):  # И по столбцу
                                    return False

                        elif isinstance(piece, Bishop):
                            # Если слон может пойти хотя бы на одну клетку по диагонали, то это не пат
                            moves_bishop = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
                            for j in moves_bishop:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False

                        elif isinstance(piece, Knight):
                            # У коня 8 вариантов хода
                            moves_knight = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
                            for j in moves_knight:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False

                        elif isinstance(piece, Queen):
                            # Объединим условия ладьи и слона
                            for j in range(8):
                                if piece.can_move(self, row, col, row, j):
                                    return False
                                elif piece.can_move(self, row, col, j, col):
                                    return False

                            moves_queen = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
                            for j in moves_queen:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False

                        elif isinstance(piece, King):
                            moves_king = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
                            for j in moves_king:
                                if piece.can_move(board, row, col, row + j[0], col + j[1]) \
                                        and not self.is_under_attack(board, row + j[0], col + j[1]):
                                    return False
            return True  # Если ни одного хода не найдено, то это пат
        return False

    def stalemate_black(self, board):
        """
        Checking the stalemate for black.
        To know if the player is able to move, "go through" all possible options.
        At the same time, the king mustn't be checked.
        """
        if self.is_under_attack(board, self.king_black.row, self.king_black.col):  # Если король под шахом, то не пат
            return False
        if self.current_player_color() == BLACK:
            for i in self.field:
                for piece in i:
                    if piece is not None and piece.get_color() == BLACK:
                        row, col = piece.row, piece.col
                        if isinstance(piece, Pawn):  # У пешки есть 4 возможных варианта хода
                            moves_pawn = [(1, 0), (2, 0), (1, 1), (1, -1)]
                            for j in moves_pawn:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False  # Если у стороны есть хотя бы один ход, то это не пат

                        elif isinstance(piece, Rook):
                            for j in range(8):
                                if piece.can_move(self, row, col, row, j):
                                    return False
                                elif piece.can_move(self, row, col, j, col):
                                    return False

                        elif isinstance(piece, Bishop):
                            # Если слон может пойти хотя бы на одну клетку по диагонали, то это не пат
                            moves_bishop = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
                            for j in moves_bishop:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False

                        elif isinstance(piece, Knight):
                            # У коня 8 вариантов хода
                            moves_knight = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
                            for j in moves_knight:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False

                        elif isinstance(piece, Queen):
                            # Объединим условия ладьи и слона
                            for j in range(8):
                                if piece.can_move(self, row, col, row, j):
                                    return False
                                elif piece.can_move(self, row, col, j, col):
                                    return False

                            moves_queen = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
                            for j in moves_queen:
                                if piece.can_move(self, row, col, row + j[0], col + j[1]):
                                    return False

                        elif isinstance(piece, King):
                            moves_king = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
                            for j in moves_king:
                                if piece.can_move(board, row, col, row + j[0], col + j[1]) \
                                        and not self.is_under_attack(board, row + j[0], col + j[1]):
                                    return False
            return True  # Если ни одного хода не найдено, то это пат
        return False

    def move_and_promote_pawn(self, row, col, row1, col1):
        """
        Pawn promotion.
        """
        piece = self.field[row][col]
        if not isinstance(piece, Pawn):
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
        if self.field[row1][col1] is not None:
            piece1 = self.field[row1][col1]
            if piece1.get_color() == piece.get_color():
                return False
        return True

    def castling_white0(self):  # Рокировка с Rook(0, 0)
        if isinstance(self.field[0][4], King) and isinstance(self.field[0][0], Rook):  # на своих ли местах
            if self.field[0][0].turns > 0:  # кол-во ходов д. = 0
                return False
            if self.field[0][4].turns > 0:  # то же для короля
                return False
            if self.field[0][1] is not None or self.field[0][2] is not None or self.field[0][3] is not None:
                return False  # если какие-то клетки между ними заняты, рокировка невозможна
            # В иных случаях осуществляем рокировку
            self.field[0][2] = King(0, 2, WHITE)
            self.field[0][4] = None
            self.field[0][0] = None
            self.field[0][3] = Rook(0, 3, WHITE)
            return True
        return False

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
        return False

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
        super().__init__(row, col, color)  # Параметры row, col, color наследуются от класса Piece
        self.two_ranks_move = False  # Параметр нужен для "взятия на проходе"

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):  # Несмотря на то, что это проверяется в move_piece(), понадобится для других функций
            return False
        # Взятие на проходе
        '''if self.get_color() == WHITE:
            if isinstance(board.field[row1 - 1][col1], Pawn):  # Проверяем, есть ли по соседству пешки
                if board.field[row1 - 1][col1].two_ranks_move and board.field[row1 - 1][col1].get_color() == BLACK:
                    board.field[row1 - 1][col1] = None
                    return True
        elif self.get_color() == BLACK:
            if correct_coords(row1 + 1, col1) and isinstance(board.field[row1 + 1][col1], Pawn):
                if board.field[row1 + 1][col1].two_ranks_move and board.field[row1 + 1][col1].get_color() == WHITE:
                    board.field[row1 + 1][col1] = None
                    return True'''

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
        super().__init__(row, col, color)  # вызываем конструктор родительского класса
        self.turns = 0  # Количество ходов, нужно для рокировки

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по вертикали есть фигура
            if board.get_piece(r, col) is not None:
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if not board.get_piece(row, c) is not None:
                return False
        self.turns += 1
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight(Piece):  # Класс, описывающий коня
    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        res = [abs(col - col1), abs(row - row1)]
        if res[0] == 1 and res[1] == 2:  # разница между столбцами должна быть 1, между рядами - 2
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
        if not correct_coords(row1, col1):
            return False
        if abs(row1 - row) > 1 or abs(col1 - col) > 1:
            return False  # если разница между клетками больше 1
        # рокировка
        if (row1, col1) == (0, 2):
            return board.castling_white0()
        elif (row1, col1) == (0, 6):
            return board.castling_white7()
        elif (row1, col1) == (7, 2):
            return board.castling_black0()
        elif (row1, col1) == (7, 6):
            return board.castling_black7()
        #
        self.turns += 1
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Piece):  # Класс, описывающий ферзя
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False

        xr = abs(row1 - row)  # разница между рядами
        xc = abs(col1 - col)  # разница между столбцами
        if row1 != row and col1 != col and xc != xr:
            return False

        dx = 1 if row1 > row else -1 if row1 < row else 0  # Проверка, что на пути фигуры нет других фигур
        dy = 1 if col1 > col else -1 if col1 < col else 0
        x = row + dx
        y = col + dy
        while x != row1 or y != col1:
            if board.get_piece(x, y) is not None:
                return False
            x += dx
            y += dy
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(Piece):  # Класс, описывающий слона
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        res = [abs(col - col1), abs(row - row1)]
        if res[0] != res[1]: # разницы между рядами и между столбцами д. б. равны
            return False

        dx = 1 if row1 > row else -1 if row1 < row else 0  # Проверка, что на пути фигуры нет других фигур
        dy = 1 if col1 > col else -1 if col1 < col else 0
        x = row + dx
        y = col + dy
        while x != row1 or y != col1:
            if board.get_piece(x, y) is not None:
                return False
            x += dx
            y += dy
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


if __name__ == "__main__":
    main()
