"""
This module defines the data model for the simulation. Specifically, it provides a class for representing patches of the simulation grid and a class for representing cells that inhabit these patches.


Requirements
------------
Python 3.7 or higher.

Notes
-----
This module provided as material for Phase 1 of the exam project for DM562, DM857, DS830 (2022). 
"""

# Version 1.1
# Changes and bugfixes
# - Patch renders its coordinates in the wrong order (Patch.__repr__)
# - Divide is missing a precondition (Cell.divide)

from __future__ import annotations # to use a class in type hints of its members
from typing import Optional
import random  # new Phase_2

# This is a new Class
class BasePatch:
  """Represents a 'BasePatch' at the intersection of the riven row and column of the simulation grid."""

  def __init__(self:BasePatch, row:int, col:int):
    self._col = col
    self._row = row
  
  def col(self:BasePatch)->int:
    """Returns the index of the column containing this patch."""
    return self._col

  def row(self:BasePatch)->int:
    """Returns the index of the row containing this patch."""
    return self._row


# This is a new Class
class ObstaclePatch(BasePatch):
  """Represents a 'ObstaclePatch' at the intersection of the riven row and column of the simulation grid."""

  def __init__(self:ObstaclePatch, row:int, col:int):
    self._is_obstacle = True
    self._col = col  # TODO: check if correctly gives col or ._col
    self._row = row  # TODO: check if correctly takes row or ._row

  def col(self:ObstaclePatch)->int:
    """Returns the index of the column containing this patch."""
    return self._col

  def row(self:ObstaclePatch)->int:
    """Returns the index of the row containing this patch."""
    return self._row

  # deleted this method because we dont use something likes this
  # def change(self:ObstaclePatch)->None:
  #   """This cell will no longer be an obstacle.
  #   It changes the status of the patch to a CellPatch
    
  #   Precondition: the patch is a Obstacle patch"""
  #   assert self.is_obstacle(), "the patch must be a Obstacle patch"
  #   self._is_obstacle = False
    
  def is_obstacle(self:ObstaclePatch)->bool:
    "Returns whether this is an obstacle patch."
    return self._is_obstacle


# This is the modified "Patch" class from Phase_1
class CellPatch(BasePatch):
  """Represents a 'patch' at the intersection of the riven row and column of the simulation grid."""
  
  def __init__(self:CellPatch, row:int, col:int, toxicity:int):
    """    
    Parameters
    ----------
    row, col: int
      The index of the row and column containing this patch.
    """
    self._col = col
    self._row = row
    self._toxicity = toxicity  # new Phase_2
    self._cell : Optional[Cell] = None

  def col(self:CellPatch)->int:
    """Returns the index of the column containing this patch."""
    return self._col

  def row(self:CellPatch)->int:
    """Returns the index of the row containing this patch."""
    return self._row

  def toxicity(self:CellPatch)->int:  # new Phase_2
    """Returns the toxicity level of this patch."""
    return self._toxicity
  
  def has_cell(self:CellPatch)->bool:
    """Checks if the patch holds a cell."""
    return self._cell is not None

  def put_cell(self:CellPatch,cell:Cell)->None:
    """Puts a cell on this patch.
    
    Preconditions: there is no cell on this patch and the cell is not on another patch
    """
    assert not self.has_cell(), "This patch has a cell."
    assert cell.patch() is self, "The cell is on another patch."
    self._cell = cell

  def remove_cell(self:CellPatch)->None:
    """Removes any cell currently on this patch."""
    self._cell = None

  def cell(self:CellPatch)->Optional[Cell]:
    """Returns the cell currently on this patch, if any."""
    return self._cell

  def __repr__(self:CellPatch)->str:
    """Returns a string representation of this patch."""
    return f"Patch({self.row()}, {self.col()})"


# This is the modified "Cell" class from Phase_1
class Cell:
  """Represents a cell in the simulation."""

  def __init__(self:Cell,patch:CellPatch,resistance_level:int):
    """    
    Parameters
    ----------
    patch: Patch
      The patch that will contain this cell (added automatically). The patch must be free.
    """
    self._age_limit = 10  # new Phase_2 (int)
    self._division_limit = 7  # new Phase_2 (int)
    self._division_probability = 0.6  # new Phase_2 (float)
    self._division_cooldown = 1 # new Phase_2 (int)
    self._resistance_level = resistance_level  # new Phase_2 (int)
    self._parent : Optional[Cell] = None  # new Phase_2 (cell input)
    # TODO: not sure if parent should be written as argument in the constructor or not
    #       since it is an optional input for the _parent attribute
    self._generation = 0

    # old from Phase_1
    self._patch = patch
    self._age = 0
    self._divisions = 0
    self._last_division = 0
    self._alive = True
    # inform patch that this cell is on it
    patch.put_cell(self)
  
  def resistance(self:Cell)->int:  # new Phase_2
    """Returns the resistance level of this cell."""
    return self._resistance_level

  def parent(self:Cell)->Optional[Cell]:  # new Phase_2
    """Returns the parent of this cell."""
    return self._parent

  def generation(self:Cell)->int:  # new Phase_2
    """Returns the generation level of this cell."""
    return self._generation

  def patch(self:Cell)->CellPatch:
    """Returns the patch of this cell. If the cell is dead, it returns the patch where the cell died."""
    return self._patch

  def age(self:Cell)->int:
    """Returns the age in ticks of this cell or the age at the time of death if the cell is dead."""
    return self._age
  
  def divisions(self:Cell)->int:
    """Returns number of division performed by this cell."""
    return self._divisions

  def last_division(self:Cell)->int:
    """Returns the time in ticks since the last division this cell (or its creation if it never divided)."""
    return self._last_division
  
  def is_alive(self:Cell)->bool:
    """Returns whether this cell is alive."""
    return self._alive

  def tick(self:Cell, patch:CellPatch)->None:
    self._age = self._age + 1  # update the age
    self._last_division = self._last_division + 1  # update the last division counter
    # TODO: implement the dying method here instead of in the simulation code as before
    #       dying through ageing, division or poisoning

    # chance of dying by poisoning
    # TODO: figure out if the difference is a absolute value or if the toxicity 
    #       always has to be higher than the resistance level. 
    #       Technically the cell should not die if the resistance level is 
    #       higher than the toxicity level (my thoughts Jonas)
    p = abs(patch.toxicity() - self.resistance) / 100  # prob as described in pdf
    if p < round(random.random(), 2):  # random probability for death by poisoning
      self.die()

    
    # TODO: implement update status if cell is alive or dead, when it is not already
    #       enought with the method die! (it also updates the status)


  # old tick method from Phase_1
  '''
  def tick(self:Cell)->None:  # added generation cumulation per tick
    """Register with this cell that a tick in the simulation happened making the cell age.
    
    Precondition: the cell is alive."""
    assert self.is_alive(), "the cell must be alive."
    self._age = self._age + 1
    self._last_division = self._last_division + 1
    self._generation = self._generation + 1  # new Phase_2
    # TODO: Not sure if generation is correctly implemented here
  '''

  def die(self:Cell)->None:
    """This cell dies and is removed from its current patch.

    Precondition: the cell is alive."""
    assert self.is_alive(), "the cell must be alive."
    self._alive = False
    # removes the cell from this cell's patch
    self._patch.remove_cell()
  
  # TODO: Check and correcht divide method
  def divide(self:Cell, patch:CellPatch)->bool:
    """Divides this cell using a given patch and returns a booelan if the division 
    was successful. To divide the division probability is used and it is calculated
    by reducing the base division probability by the cell resistance level divided by 20.
    
    The attempt fails with probability 1-p if the cell had a successful division during the last
    Cell.division_cooldown tick. 
    The resistance level is inherited from the parent cell where the value mutates randomly
    between +/- 2 from the parent cell.
    
    Precondition: the cell is alive, the patch is free"""

    assert patch.is_alive(), "the cell must be alive"
    
    p = self._division_probability - (Cell.resistance() / 20)
    if random.uniform(0, 1) > p:
      return False
    
    # TODO: problem to understand the statement with Cell.division_cooldown 
    #       because it should not be possibly to divide during a cooldown?
    if Cell.division_cooldown < Cell._last_division:
      return False
    
    # TODO: not sure if this correctly appends a correct patch or just overrides the old one
    self._last_division = 0  # reset the counter from the last division
    self._divisions = self._divisions + 1  # updates the division counter
    new_cell = Cell(patch, self.resistance() + int(random.randint(-2, 2)))
    patch.cell(new_cell)

  # old divide from Phase_1 (new in Phase_2)
  '''
  def divide(self:Cell,patch:CellPatch)->Cell:
    """Divides this cell using the given patch and returns the new cell.
    
    Precondition: the cell is alive, the patch is free."""
    assert self.is_alive(), "the cell must be alive."
    self._last_division = 0 # reset the counter from the last division
    self._divisions = self._divisions + 1 # updates the division count
    return Cell(patch)
  '''

  def died_by_age(self:Cell)->bool:
    # TODO: check age with age limit and if reached initial diying by age and increment statistics?
    pass

  def died_by_division(self:Cell)->bool:
    # TODO: check division with division limit and if reached initial diying by age and increment statistics?
    pass

  def died_by_poisoning(self:Cell)->bool:
    # TODO: check died by toxicity exceeded and if reached initial diying by age and increment statistics?
    pass

# TODO: Finish the other methods by diying