from enum import Enum
from typing import Tuple, Optional


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class ToyRobot:
    """
    A class representing a toy robot that can move on a 5x5 table.
    """

    def __init__(self):
        self._x: Optional[int] = None
        self._y: Optional[int] = None
        self._direction: Optional[Direction] = None
        self._placed: bool = False

    @staticmethod
    def is_valid_position(x: int, y: int) -> bool:
        """
        Check if the given position is valid on the table.

        param x: The x-coordinate
        param y: The y-coordinate
        return: True if the position is valid, False otherwise
        """
        return 0 <= x < 5 and 0 <= y < 5

    def place(self, x: int, y: int, direction: Direction) -> None:
        """
        Place the robot on the table at the given position and direction.

        param x: The x-coordinate
        param y: The y-coordinate
        param direction: The direction the robot is facing
        """
        if self.is_valid_position(x, y):
            self._x, self._y = x, y
            self._direction = direction
            self._placed = True

    def move(self) -> None:
        """
        Move the robot one unit forward in the direction it is facing.
        """
        if not self._placed:
            return

        new_x, new_y = self._get_new_position()
        if self.is_valid_position(new_x, new_y):
            self._x, self._y = new_x, new_y

    def _get_new_position(self) -> Tuple[int, int]:
        """
        Calculate the new position after a move.

        return: A tuple containing the new (x, y) coordinates
        """
        moves = {
            Direction.NORTH: (0, 1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, -1),
            Direction.WEST: (-1, 0)
        }
        dx, dy = moves[self._direction]
        return self._x + dx, self._y + dy

    def rotate(self, clockwise: bool = True) -> None:
        """
        Rotate the robot 90 degrees.

        param clockwise: True for clockwise rotation, False for counter-clockwise
        """
        if self._placed:
            rotation = 1 if clockwise else -1
            self._direction = Direction((self._direction.value + rotation) % 4)

    def report(self) -> str:
        """
        Report the current position and direction of the robot.

        return: A string representation of the robot's state
        """
        return f"{self._x},{self._y},{self._direction.name}" if self._placed else "Robot not placed on the table"


def process_command(robot: ToyRobot, command: str) -> Optional[str]:
    """
    Process a command for the robot.

    param robot: The ToyRobot instance
    param command: The command string
    return: The result of the REPORT command, if applicable
    """
    parts = command.split()
    if parts[0] == 'PLACE':
        try:
            x, y, direction = parts[1].split(',')
            robot.place(int(x), int(y), Direction[direction])
        except (ValueError, IndexError, KeyError):
            return "Invalid PLACE command"
    elif parts[0] == 'MOVE':
        robot.move()
    elif parts[0] == 'LEFT':
        robot.rotate(clockwise=False)
    elif parts[0] == 'RIGHT':
        robot.rotate(clockwise=True)
    elif parts[0] == 'REPORT':
        return robot.report()
    else:
        return "Invalid command"
    return None


def main() -> None:
    """
    Main function to run the Toy Robot Simulator.
    """
    robot = ToyRobot()
    print("Enter commands (PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | EXIT):")
    while True:
        command = input().strip().upper()
        if command == 'EXIT':
            break
        result = process_command(robot, command)
        if result:
            print(result)


if __name__ == "__main__":
    main()
