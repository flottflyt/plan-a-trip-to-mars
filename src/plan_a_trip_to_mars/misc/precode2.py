"""Pre-code for INF-1400.

21 February 2018 Revision 4 (Lars Brenna):
- Removed references to inherit object. (Bloat.)
- Corrected error messages in mul and truediv.
- Changed from "return False" to raise Exception when there is no intersection.

16 January 2017 Revision 3 (Mads Johansen):
Rewritten to conform to Python 3 standard. Made class iterable, added property as_point,
replaced magnitude with __abs__ (to reflect mathematical vector notation), added rotate method.

22 January 2012 Revision 2 (Martin Ernstsen):
Reraise exception after showing error message.

11 February 2011 Revision 1 (Martin Ernstsen):
Fixed bug in intersect_circle. Updated docstrings to Python standard.
Improved __mul__. Added some exception handling. Put example code in separate
function.

"""

from __future__ import annotations

from math import cos, hypot, radians, sin


class ReturnZeroError(ZeroDivisionError):
    """Class for keeping track of errors that occur when dividing by zero.

    Arguments:
        ZeroDivisionError {exception} -- inherits from ZeroDivisionError to make it a similar class with the same attributes
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class Vector2D[T]:
    """Implements a two dimensional vector.

    :param x: First component for the vector.
    :param y: Second component for the vector.
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Representation of the class when printed."""
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self) -> str:
        """Return the string representation of the class."""
        return f"Vector(X: {self.x}, Y: {self.y}) Magnitude: {abs(self)}"

    def __nonzero__(self) -> bool:
        """Make Vector2D(0,0) evaluate to False, all other vectors evaluate to True.

        :returns: Boolean evaluation of vector.
        """
        return self.as_point != (0, 0)

    __bool__ = __nonzero__

    def __add__(self, b: Vector2D) -> Vector2D:
        """Vector addition.

        :returns: New vector where x = self.x + b.x and y = self.y + b.y
        """
        return Vector2D(self.x + b.x, self.y + b.y)

    def __sub__(self, b: Vector2D) -> Vector2D:
        """Vector subtraction.

        :returns: New vector where x = self.x - b.x and y = self.y - b.y
        """
        return Vector2D(self.x - b.x, self.y - b.y)

    def __eq__(self, other: object) -> bool:
        """Vector equality.

        :returns: True if both components of this vector are equal to those of b.
        """
        if hasattr(other, "x") and hasattr(other, "y"):
            return self.x == other.x and self.y == other.y
        return False

    def __mul__(self, b: float) -> Vector2D:
        """Vector multiplication by a scalar.

        :param: Any value that can be coerced into a float.
        :returns: New vector where x = self.x * b and y = self.y * b
        """
        try:
            return Vector2D(self.x * b, self.y * b)
        except ValueError as e:
            msg = f"Right value must be castable to float, was {b}"
            raise ValueError(msg) from e

    def __truediv__(self, b: float) -> Vector2D:
        """Vector division by a scalar.

        :param: Any value that can be coerced into a float.
        :returns: New vector where x = self.x / b and y = self.y / b
        """
        try:
            return Vector2D(self.x / b, self.y / b)
        except ValueError as e:
            msg = f"Right value must be castable to float, was {b}"
            raise ValueError(msg) from e

    def __iter__(self) -> Vector2D:
        """Return a generator function used to iterate over components of vector.

        :returns: Iterator over components.
        """
        yield from self.__dict__.values()

    def __rmul__(self, b: float) -> Vector2D:
        """Vector multiplication."""
        try:
            return Vector2D(self.x * b, self.y * b)
        except (ValueError, ZeroDivisionError) as e:
            msg = f"Scalar must be castable to float, was {b}"
            raise ValueError(msg) from e

    def __abs__(self) -> float:
        """Return the magnitude of the vector."""
        return hypot(self.x, self.y)

    def normalized(self) -> Vector2D:
        """Return a new vector with the same direction but magnitude 1.

        :returns: A new unit vector with the same direction as self.
        Throws ZeroDivisionError if trying to normalize a zero vector.
        """
        try:
            m = abs(self)
            return self / m
        except ZeroDivisionError as e:
            msg = "Attempted to normalize a zero vector, return a unit vector at zero degrees"
            raise ReturnZeroError(msg) from e

    def copy(self) -> Vector2D:
        """Return a copy of the vector.

        :returns: A new vector identical to self.
        """
        return Vector2D(self.x, self.y)

    @property
    def as_point(self) -> tuple[int, int]:
        """A tuple representation of the vector, useful for pygame functions.

        :returns: A tuple of the vectors components.
        """
        return round(self.x), round(self.y)

    def rotate(self, theta: float) -> Vector2D:
        """Vector rotation.

        :param theta: The angle of rotation in degrees.
        :returns: A new vector which is the same length, but rotated by theta.
        """
        cos_theta, sin_theta = cos(radians(theta)), sin(radians(theta))
        newx = round(self.x * cos_theta - self.y * sin_theta, 6)
        newy = round(self.x * sin_theta + self.y * cos_theta, 6)
        return Vector2D(newx, newy)
