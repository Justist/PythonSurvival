import math

import pygame

from FighterEntity import FighterEntity


class Utilities:
   minlocation = 50
   maxlocation = 5000

   @staticmethod
   def locationSanityCheck(location: tuple):
      x, y = location
      if not Utilities.minlocation <= x <= Utilities.maxlocation:
         x = 50 if x - Utilities.maxlocation <= 0 else Utilities.maxlocation
      if not Utilities.minlocation <= y <= Utilities.maxlocation:
         y = 50 if y - Utilities.maxlocation <= 0 else Utilities.maxlocation
      return x, y

   @staticmethod
   def locationSanityCheckFighter(fighter: FighterEntity):
      return Utilities.locationSanityCheck((fighter.x, fighter.y))

   @staticmethod
   def calculateDistance(location1, location2):
      location1 = Utilities.locationSanityCheck(location1)
      location2 = Utilities.locationSanityCheck(location2)
      x1, y1 = location1
      x2, y2 = location2
      return math.sqrt(math.pow(abs(x1 - x2), 2) + math.pow(abs(y1 - y2), 2))

   @staticmethod
   def calculateDistanceFighters(fighter1: FighterEntity, fighter2: FighterEntity):
      fighter1.x, fighter1.y = Utilities.locationSanityCheckFighter(fighter1)
      fighter2.x, fighter2.y = Utilities.locationSanityCheckFighter(fighter2)
      return Utilities.calculateDistance((fighter1.x, fighter1.y), (fighter2.x, fighter2.y))

   @staticmethod
   def draw(fighter: FighterEntity):
      x, y, radius, screen = fighter.x, fighter.y, fighter.radius, fighter.screen
      screenwidth, screenheight = screen.get_width(), screen.get_height()
      if (x + radius > fighter.MIDDLE[0] - (screenwidth // 2) and
            x - radius < fighter.MIDDLE[0] + (screenwidth // 2) and
            y + radius > fighter.MIDDLE[1] - (screenheight // 2) and
            y - radius < fighter.MIDDLE[1] + (screenheight // 2)):
         pygame.draw.circle(screen, fighter.colour, Utilities.convertCoords(fighter),
                            fighter.radius)

   @staticmethod
   def convertCoords(fighter: FighterEntity):
      Utilities.locationSanityCheckFighter(fighter)
      screen = fighter.screen
      middleX, middleY = screen.get_width() / 2, screen.get_height() / 2
      return middleX + (fighter.x - fighter.MIDDLE[0]), middleY + (fighter.y - fighter.MIDDLE[1])
