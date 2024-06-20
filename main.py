from graphics import Window, Line, Point, Cell
from maze import Maze


def main() -> None:
    win = Window(800, 600)
    origin = Point(0, 0)
    lines = [
        Line(origin, Point(0, 100)),
        Line(origin, Point(100, 0)),
        Line(origin, Point(100, 100)),
    ]
    cells = [
        Cell(win, Point(0, 0), Point(100, 100)),
        Cell(win, Point(0, 100), Point(100, 200)),
        Cell(win, Point(100, 100), Point(200, 200)),
        Cell(win, Point(100, 0), Point(200, 100)),
    ]
    # for line in lines:
    #     win.draw_line(line, "black")

    # for cell in cells:
    #     cell.draw()
    # cells[0].draw_move(cells[1])
    # cells[1].draw_move(cells[2], True)

    maze = Maze(10, 10, 20, 20, 25, 25, win)
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
