from __future__ import annotations
from tkinter import Tk, BOTH, Canvas


class Cell:
    def __init__(
        self,
        window: Window,
        point1: Point,
        point2: Point,
    ) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = point1.get_x()
        self.__x2 = point2.get_x()
        self.__y1 = point1.get_y()
        self.__y2 = point2.get_y()
        self.__win = window

    def draw(self) -> None:
        top_left = Point(self.__x1, self.__y1)
        top_right = Point(self.__x2, self.__y1)
        bottom_left = Point(self.__x1, self.__y2)
        bottom_right = Point(self.__x2, self.__y2)
        colour_dict = {False: "white", True: "black"}

        self.__win.draw_line(Line(top_left, top_right), colour_dict[self.has_top_wall])

        self.__win.draw_line(
            Line(top_right, bottom_right), colour_dict[self.has_right_wall]
        )

        self.__win.draw_line(
            Line(top_left, bottom_left), colour_dict[self.has_left_wall]
        )

        self.__win.draw_line(
            Line(bottom_left, bottom_right), colour_dict[self.has_bottom_wall]
        )

    def draw_move(self, to_cell: Cell, undo=False) -> None:
        line_colour = "gray" if undo else "red"
        end_point = to_cell.get_center()
        start_point = self.get_center()
        self.__win.draw_line(Line(start_point, end_point), line_colour)

    def get_center(self) -> Point:
        center_x = (self.__x1 + self.__x2) / 2
        center_y = (self.__y1 + self.__y2) / 2
        return Point(center_x, center_y)


class Point:
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self, x) -> None:
        self.__x = x

    def set_y(self, y) -> None:
        self.__y = y

    def __repr__(self) -> str:
        return f"X:{self.__x}\tY:{self.__y}"


class Line:
    def __init__(self, point1: Point, point2: Point) -> None:
        self.__point1 = point1
        self.__point2 = point2

    def draw(self, canvas: Canvas, fill_colour: str) -> None:
        x1, y1 = self.__point1.get_x(), self.__point1.get_y()
        x2, y2 = self.__point2.get_x(), self.__point2.get_y()
        canvas.create_line(x1, y1, x2, y2, fill=fill_colour, width=2)


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, height=height, width=width, bg="white")
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        self.__running = False

    def draw_line(self, line: Line, fill_colour: str) -> None:
        line.draw(self.__canvas, fill_colour)
