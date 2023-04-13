import random

from FighterEntity import FighterEntity
from Utilities import Utilities


class Enemy(FighterEntity):
   def __init__(self, screen, MIDDLE, number):
      super().__init__(screen, MIDDLE)
      self.MIDDLE = MIDDLE
      self.radius = random.randint(5, 40)
      self.colour = "blue"
      self.number = number
      self.speed = random.randint(1, 5)
      # self.halfradius = self.radius / 2
      # self.x = random.randint(50, 5000)
      # self.y = random.randint(50, 5000)
      self.x = random.randint(2500, 3500)
      self.y = random.randint(2500, 3500)
      # self.boundary = None
      # self.updateBoundaries()

   # def draw(self):
   #   pygame.draw.circle(self.screen, "blue", pygame.Vector2(self.x, self.y), self.radius)

   def updatePosition(self, deltax, deltay):
      # print(f"Updating enemy {self.number} position from {self.x}, {self.y} with delta {
      # deltax}, {deltay}")
      # tweak upper value, but basically make large jumps impossible
      if 0 < abs(deltax) < 100:
         self.x += deltax
      if 0 < abs(deltay) < 100:
         self.y += deltay

   def moveToPlayer(self):
      xydistance = Utilities.calculateDistance((self.x, self.y), self.MIDDLE)
      # sin(angle) = xydistance / y-difference
      # cos(angle) = x-difference / xydistance
      deltax = 0 if xydistance == 0 else - self.speed * round(
         (self.x - self.MIDDLE[0]) / xydistance)
      deltay = 0 if self.y - self.MIDDLE[1] == 0 else - self.speed * round(
         xydistance / (self.y - self.MIDDLE[1]))
      self.updatePosition(deltax, deltay)

   def moveFromPlayer(self, extradistance):
      xydistance = Utilities.calculateDistance((self.x, self.y), self.MIDDLE)
      # newX = oldX + xDiff * abs(xydiff * extraDistance / oldDistance)
      deltax = ((self.x - self.MIDDLE[0]) * (abs(xydistance + 2 * extradistance) / xydistance))
      deltay = ((self.y - self.MIDDLE[1]) * (abs(xydistance + 2 * extradistance) / xydistance))
      # print(f"moveFromPlayer: {self.x = }, {self.y = }")
      # print(f"moveFromPlayer: {extradistance = }, {xydistance = }, {deltax = }, {deltay = }")
      self.updatePosition(deltax, deltay)

   # code for if we want boundaries at any time
   # def updateBoundaries(self):
   #    self.boundary = {(
   #        self.radius * math.cos(tau) + self.x,
   #        self.radius * math.sin(tau) + self.y,
   #    ) for tau in range(360)}
   #
   # def checkBoundary(self, other):
   #    pass
