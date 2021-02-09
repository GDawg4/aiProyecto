from pydash import uniq, remove, flatten
from copy import copy, deepcopy
from math import inf


class GameBoard:
    def __init__(self):
        self.red_base = [
            1, 2, 3, 4, 5,
            11, 12, 13, 14,
            21, 22, 23,
            31, 32,
            41
        ]
        self.blue_base = [
            60,
            70, 69,
            80, 79, 78,
            90, 89, 88, 87,
            100, 99, 98, 97, 96
        ]
        self.game_board = [
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
        ]
        self.current_turn = False

    def current_turn_to_symbol(self):
        return 1 if self.current_turn else 2

    def bool_to_symbol(self, turn):
        return 1 if turn else 2

    def symbol_to_bool(self, turn):
        return turn == 1

    def is_other_player(self, x, y, current_board=None):
        if current_board is None:
            current_board = self.game_board
        return current_board[y - 1][x - 1] != 0 and current_board[y - 1][x - 1] != self.current_turn_to_symbol()

    def is_same_player(self, x, y, current_board=None):
        if current_board is None:
            current_board = self.game_board
        return current_board[y - 1][x - 1] == self.current_turn_to_symbol()

    def is_empty(self, x, y, current_board=None):
        if current_board is None:
            current_board = self.game_board
        return current_board[y - 1][x - 1] == 0

    def is_full(self, x, y, current_board=None):
        if current_board is None:
            current_board = self.game_board
        return current_board[y - 1][x - 1] != 0

    def get_chips_positions(self, board, current_symbol):
        return [
            [i+1, j+1]
            for i in range(len(self.game_board))
            for j in range(len(self.game_board[i]))
            if board[j][i] == current_symbol
        ]

    def get_moves_from_positions(self, chips):
        return [
            self.get_possible_moves(positions[0], positions[1])
            for positions in chips
        ]

    def master(self, board, current_turn, level):
        current_symbol = self.bool_to_symbol(current_turn)
        chips = self.get_chips_positions(board, current_symbol)
        moves = self.get_moves_from_positions(chips)

        # final = [
        #     [] for i in chips
        # ]
        # for i in range(len(chips)):
        #     for j in range(len(moves[i])):
        #         final[i].append(
        #             self.move_pretend(
        #                 chips[i][0],
        #                 chips[i][1],
        #                 moves[i][j][0],
        #                 moves[i][j][1]
        #             )
        #         )
        #scores = [[] for i in chips]
        # for i in final:
        #     for j in i:
        #         scores.append(
        #             self.get_score_max(
        #                 j,
        #                 not current_turn
        #             )
        #         )
        # scores = []
        # for i in final:
        #     for j in i:
        #         temp_chips = self.get_chips_positions(j, not current_turn)
        #         score = self.min(
        #             not current_turn,
        #             temp_chips,
        #             self.get_moves_from_positions(temp_chips)
        #         )
        #         scores.append(score)
        #         print(j)
        # print(scores)
        # print(len(scores))
        return self.max(current_symbol, chips, moves)

    def min(self, current_turn, chips, moves):
        best_move = {
            'start': [0, 0],
            'end': [0, 0],
            'score': inf
        }
        for i in range(len(chips)):
            for j in range(len(moves[i])):
                current_score = -self.get_score_max(
                    self.move_pretend(
                        chips[i][0],
                        chips[i][1],
                        moves[i][j][0],
                        moves[i][j][1]
                    ),
                    current_turn
                )
                if current_score < best_move['score']:
                    best_move['start'] = chips[i]
                    best_move['end'] = moves[i][j]
                    best_move['score'] = current_score
        return best_move

    def max(self, current_turn, chips, moves):
        best_move = {
            'start': [0, 0],
            'end': [0, 0],
            'score': -inf
        }
        for i in range(len(chips)):
            for j in range(len(moves[i])):
                current_score = self.get_score_max(
                    self.move_pretend(
                        chips[i][0],
                        chips[i][1],
                        moves[i][j][0],
                        moves[i][j][1]
                    ),
                    current_turn
                )
                if current_score > best_move['score']:
                    best_move['start'] = chips[i]
                    best_move['end'] = moves[i][j]
                    best_move['score'] = current_score
        return best_move

    def get_score_max(self, board, turn):
        chips_positions = self.get_chips_positions(
            board,
            current_symbol=self.bool_to_symbol(turn)
        )
        possible_moves = self.get_moves_from_positions(
            chips_positions
        )
        distances = [
            (20-i[0]-i[1])**2
            for i in chips_positions
        ]
        return len(flatten(possible_moves))*100-sum(distances)*10

    def play_best_move(self, level=1):
        best_move = self.master(self.game_board, self.current_turn, level)
        if self.move(
            best_move['start'][0],
            best_move['start'][1],
            best_move['end'][0],
            best_move['end'][1],
        ):
            self.current_turn = not self.current_turn

    def is_adjacent(self, initial_x, initial_y, final_x, final_y):
        return ((initial_x + 1 == final_x or initial_x - 1 == final_x) and (initial_y == final_y)) or \
               ((initial_y + 1 == final_y or initial_y - 1 == final_y) and (initial_x == final_x)) or \
               (initial_x + 1 == final_x and initial_y + 1 == final_y) or \
               (initial_x + 1 == final_x and initial_y - 1 == final_y) or \
               (initial_x + 1 == final_x and initial_y + 1 == final_y) or \
               (initial_x + 1 == final_x and initial_y - 1 == final_y)

    def is_a_movable_position_if_jumping(self, initial_x, initial_y, final_x, final_y):
        return (
                (initial_x + 2 == final_x and initial_y == final_y) or
                (initial_x - 2 == final_x and initial_y == final_y) or
                (initial_x == final_x and initial_y + 2 == final_y) or
                (initial_x == final_x and initial_y - 2 == final_y) or
                (initial_x + 2 == final_x and initial_y + 2 == final_y) or
                (initial_x - 2 == final_x and initial_y - 2 == final_y) or
                (initial_x + 2 == final_x and initial_y + 2 == final_y) or
                (initial_x - 2 == final_x and initial_y - 2 == final_y)
        )

    def is_out_of_bounds(self, x):
        return x > len(self.game_board)

    def has_other_chip_between(self, initial_x, initial_y, final_x, final_y, current_board=None):
        if current_board is None:
            current_board = self.game_board
        return current_board[(initial_y + final_y) // 2 - 1][(initial_x + final_x) // 2 - 1] != 0

    def is_a_first_grade_move(self, initial_x, initial_y, final_x, final_y, current_board=None):
        if current_board is None:
            current_board = self.game_board
        # a = self.is_adjacent(initial_x, initial_y, final_x, final_y)
        b = self.is_a_movable_position_if_jumping(initial_x, initial_y, final_x, final_y)
        c = self.has_other_chip_between(initial_x, initial_y, final_x, final_y, current_board)
        return b and c

    def move_pretend(self, initial_x, initial_y, final_x, final_y, current_board=None):
        if current_board is None:
            current_board = deepcopy(self.game_board)
        current_board[initial_y - 1][initial_x - 1] = 0
        current_board[final_y - 1][final_x - 1] = self.current_turn_to_symbol()
        return current_board

    def get_possible_moves(self, initial_x, initial_y, current_board=None, visited=None, level = 0):
        if current_board is None:
            current_board = deepcopy(self.game_board)
        if visited is None:
            visited = [[initial_x, initial_y]]
        else:
            visited.append([initial_x, initial_y])
        adjacent_options = []
        all_options = []
        for row in range(len(self.game_board)):
            for cell in range(len(self.game_board[row])):
                if self.is_legal(initial_x, initial_y, cell + 1, row + 1, current_board) and self.is_a_first_grade_move(
                        initial_x, initial_y, cell + 1, row + 1):
                    all_options.append([cell + 1, row + 1])
                if level == 0 and self.is_legal(initial_x, initial_y, cell + 1, row + 1, current_board) and self.is_adjacent(initial_x, initial_y, cell + 1, row + 1):
                    adjacent_options.append([cell + 1, row + 1])

        for pair in all_options:
            if len(pair) > 0 and [pair[0], pair[1]] not in visited:
                current_board = self.move_pretend(initial_x, initial_y, pair[0], pair[1], current_board)
                level += 1
                all_options = all_options + self.get_possible_moves(pair[0], pair[1], current_board, visited, level=level)
                #all_options.remove([initial_x, initial_y])
        return uniq(all_options + adjacent_options)

    def is_legal(self, initial_x, initial_y, final_x, final_y, current_board=None):
        if current_board is None:
            current_board = self.game_board
        if self.is_same_player(initial_x, initial_y, current_board) and self.is_empty(final_x, final_y):
            return True
        return False

    def move(self, initial_x, initial_y, final_x, final_y):
        self.game_board[initial_y - 1][initial_x - 1] = 0
        self.game_board[final_y - 1][final_x - 1] = self.current_turn_to_symbol()
        return True

    def has_red_won(self):
        has_one_red = False
        for cell in self.blue_base:
            cell_corrected = cell - 1
            if self.game_board[cell_corrected // 10][cell_corrected % 10] == 0:
                return False
            elif self.game_board[cell_corrected // 10][cell_corrected % 10] == 1:
                has_one_red = True
        return has_one_red

    def has_blue_won(self):
        has_one_blue = False
        for cell in self.red_base:
            cell_corrected = cell - 1
            if self.game_board[cell_corrected // 10][cell_corrected % 10] == 0:
                return False
            elif self.game_board[cell_corrected // 10][cell_corrected % 10] == 2:
                has_one_blue = True
        return has_one_blue

    def has_won(self):
        if self.has_red_won():
            return 1
        elif self.has_blue_won():
            return 2
        return 0

    def play(self):
        while not self.has_red_won() and not self.has_blue_won():
            print(self.__str__())
            if not self.current_turn:
                initial_x = input('x inicial')
                initial_x = int(initial_x)
                initial_y = input('y inicial')
                initial_y = int(initial_y)
                final_x = input('x final')
                final_x = int(final_x)
                final_y = input('y final')
                final_y = int(final_y)
                if self.move(initial_x, initial_y, final_x, final_y):
                    self.current_turn = not self.current_turn
                else:
                    return False
            else:
                self.play_best_move()

    def __str__(self):
        string = ''
        for row in self.game_board:
            for cell in row:
                string += str(cell)
                string += '|'
            string += '\n'
        string += 'El jugador actual es {}'.format("rojo" if self.current_turn else "azul")
        return string
