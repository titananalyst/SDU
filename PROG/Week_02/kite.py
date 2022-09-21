"""
This program prints the perimeter of a kite given
- half the length of its perpendicular bisector
- the length of the two segments in which the angular bisector is divided by the perpendicular bisector.
"""

# Parameters:
# Half length of the perpendicular bisector
p = 12.0
# Lengths of the two segments forming the angular bisector
a1 = 5.0  
a2 = 35.0
# End of parameters

# Print the parameters
print("Half length of the perpendicular bisector:",p)
print("Lengths the angular bisector:",a1,"+",a2)

# auxiliary function
def hypotenuse(a : float, b : float) -> float:
  """
  Computes the length of the hypotenuse of a
  right triangle with legs a and b.

  >>> hypotenuse(3.0,4.0)
  5.0
  """
  print
  return (a ** 2 + b ** 2) ** 0.5

# compute the lengths of the two types of sides using Pythagoras' formula
# using p and a1 as legs
b1 = hypotenuse(p,a1)
# using p and a2 as legs
b2 = hypotenuse(p,a2)

# compute and print the perimeter
perimeter = 2 * b1 + 2 * b2
print("Perimeter:",perimeter)
