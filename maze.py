from graphics import Window, Point, Cell
from time import sleep
import random


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window = None,
        seed=None,
    ) -> None:
        if seed is not None:
            seed = random.seed(seed)
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self.create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._unvisit_cells()

    def create_cells(self):
        start_x = self._x1
        start_y = self._y1

        for row in range(self._num_rows):
            col_of_cells = []
            y_value = start_y + row * self._cell_size_y
            for col in range(self._num_cols):
                x_value = start_x + col * self._cell_size_x
                start_point = Point(x_value, y_value)
                end_point = Point(
                    x_value + self._cell_size_x, y_value + self._cell_size_y
                )
                new_cell = Cell(self._win, start_point, end_point)
                new_cell.draw()
                self._animate()
                col_of_cells.append(new_cell)
            self._cells.append(col_of_cells)

    def _animate(self) -> None:
        self._win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        start_cell = self._cells[0][0]
        end_cell = self._cells[len(self._cells) - 1][len(self._cells[0]) - 1]

        start_cell.has_left_wall = False
        end_cell.has_right_wall = False
        start_cell.draw()
        end_cell.draw()

    def _break_walls_r(self, row, col):
        if (
            row < 0
            or row >= self._num_rows
            or col < 0
            or col >= self._num_cols
            or self._cells[row][col].visited
        ):
            return

        current_cell = self._cells[row][col]
        current_cell.visited = True
        breakable_walls = ["top", "bottom", "left", "right"]

        if row == 0 or not current_cell.has_top_wall:
            breakable_walls.remove("top")
        if col == 0 or not current_cell.has_left_wall:
            breakable_walls.remove("left")
        if row == self._num_rows - 1 or not current_cell.has_bottom_wall:
            breakable_walls.remove("bottom")
        if col == self._num_cols - 1 or not current_cell.has_right_wall:
            breakable_walls.remove("right")

        while len(breakable_walls) > 0:
            removed_wall = random.choice(breakable_walls)
            breakable_walls.remove(removed_wall)

            if removed_wall == "top" and not self._cells[row - 1][col].visited:
                current_cell.has_top_wall = False
                self._cells[row - 1][col].has_bottom_wall = False
                self._break_walls_r(row - 1, col)
            elif removed_wall == "bottom" and not self._cells[row + 1][col].visited:
                current_cell.has_bottom_wall = False
                self._cells[row + 1][col].has_top_wall = False
                self._break_walls_r(row + 1, col)
            elif removed_wall == "right" and not self._cells[row][col + 1].visited:
                current_cell.has_right_wall = False
                self._cells[row][col + 1].has_left_wall = False
                self._break_walls_r(row, col + 1)
            elif removed_wall == "left" and not self._cells[row][col - 1].visited:
                current_cell.has_left_wall = False
                self._cells[row][col - 1].has_right_wall = False
                self._break_walls_r(row, col - 1)

        current_cell.draw()
        self._animate()

    def _unvisit_cells(self) -> None:
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self) -> bool:
        return self._solve_r(0, 0)

    def _solve_r(self, row: int, col: int) -> bool:
        if row == self._num_rows - 1 and col == self._num_cols - 1:
            return True
        next_cells = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]

        current_cell = self._cells[row][col]
        if row == 0 or self._cells[row - 1][col].visited or current_cell.has_top_wall:
            next_cells.remove((row - 1, col))
        if (
            row == self._num_rows - 1
            or self._cells[row + 1][col].visited
            or current_cell.has_bottom_wall
        ):
            next_cells.remove((row + 1, col))
        if col == 0 or self._cells[row][col - 1].visited or current_cell.has_left_wall:
            next_cells.remove((row, col - 1))
        if (
            col == self._num_cols - 1
            or self._cells[row][col + 1].visited
            or current_cell.has_right_wall
        ):
            next_cells.remove((row, col + 1))

        current_cell.visited = True

        while len(next_cells) > 0:
            next_row, next_col = next_cells.pop()
            next_cell = self._cells[next_row][next_col]
            current_cell.draw_move(next_cell)
            self._animate()

            if self._solve_r(next_row, next_col):
                return True
            current_cell.draw_move(next_cell, undo=True)
            self._animate()

        return False
