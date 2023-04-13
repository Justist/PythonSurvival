import math
import random

import pygame

MIDDLE = (3000, 3000)


class FighterEntity:
   def __init__(self, screen):
      self.x = -1
      self.y = -1
      self.screen = screen
      self.colour = None
      self.radius = -1


class Enemy(FighterEntity):
   def __init__(self, screen, number):
      super().__init__(screen)
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
      #print(f"Updating enemy {self.number} position from {self.x}, {self.y} with delta {deltax}, {deltay}")
      # tweak upper value, but basically make large jumps impossible
      if 0 < abs(deltax) < 100:
         self.x += deltax
      if 0 < abs(deltay) < 100:
         self.y += deltay

   def moveToPlayer(self):
      xydistance = Utilities.calculateDistance((self.x, self.y), MIDDLE)
      # sin(angle) = xydistance / y-difference
      # cos(angle) = x-difference / xydistance
      deltax = 0 if xydistance == 0 else - self.speed * round((self.x - MIDDLE[0]) / xydistance)
      deltay = 0 if self.y - MIDDLE[1] == 0 else - self.speed * round(xydistance / (self.y - MIDDLE[1]))
      self.updatePosition(deltax, deltay)

   def moveFromPlayer(self, extradistance):
      xydistance = Utilities.calculateDistance((self.x, self.y), MIDDLE)
      # newX = oldX + xDiff * abs(xydiff * extraDistance / oldDistance)
      deltax = ((self.x - MIDDLE[0]) * (abs(xydistance + 2 * extradistance) / xydistance))
      deltay = ((self.y - MIDDLE[1]) * (abs(xydistance + 2 * extradistance) / xydistance))
      #print(f"moveFromPlayer: {self.x = }, {self.y = }")
      #print(f"moveFromPlayer: {extradistance = }, {xydistance = }, {deltax = }, {deltay = }")
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


class Player(FighterEntity):
   def __init__(self, screen):
      super().__init__(screen)
      self.x = MIDDLE[0]
      self.y = MIDDLE[1]
      self.radius = 30
      self.colour = "red"
      self.middle = pygame.Vector2(self.screen.get_width() / 2,
                                   self.screen.get_height() / 2)

   def draw(self):
      # player is always drawn in the middle
      pygame.draw.circle(self.screen, self.colour, self.middle, self.radius)


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
      if (x + radius > MIDDLE[0] - (screenwidth // 2) and
            x - radius < MIDDLE[0] + (screenwidth // 2) and
            y + radius > MIDDLE[1] - (screenheight // 2) and
            y - radius < MIDDLE[1] + (screenheight // 2)):
         pygame.draw.circle(screen, fighter.colour, Utilities.convertCoords(fighter),
                            fighter.radius)

   @staticmethod
   def convertCoords(fighter: FighterEntity):
      Utilities.locationSanityCheckFighter(fighter)
      screen = fighter.screen
      middleX, middleY = screen.get_width() / 2, screen.get_height() / 2
      return middleX + (fighter.x - MIDDLE[0]), middleY + (fighter.y - MIDDLE[1])


class Game:
   def __init__(self):
      pygame.init()
      self.screen = pygame.display.set_mode((1280, 720))
      self.screenwidth = self.screen.get_width()
      self.screenheight = self.screen.get_height()
      self.clock = pygame.time.Clock()
      self.deltatime = 1

      self.player = Player(self.screen)
      # initialise enemies
      self.enemies = [Enemy(self.screen, n) for n in range(10)]

   def drawEnemies(self):
      for enemy in self.enemies:
         Utilities.draw(enemy)

   def moveEnemiesToPlayer(self):
      for enemy in self.enemies:
         enemy.moveToPlayer()

   def updateEnemiesPositions(self, enemyDelta):
      for enemy in self.enemies:
         enemy.updatePosition(enemyDelta[0], enemyDelta[1])

   def handleInput(self):
      enemydelta = [0, 0]
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w]:
         enemydelta[1] += 30 * self.deltatime
      if keys[pygame.K_s]:
         enemydelta[1] -= 30 * self.deltatime
      if keys[pygame.K_a]:
         enemydelta[0] += 30 * self.deltatime
      if keys[pygame.K_d]:
         enemydelta[0] -= 30 * self.deltatime
      if enemydelta != [0, 0]:
         self.updateEnemiesPositions(enemydelta)

   def checkEnemyPlayerCollision(self):
      for enemy in self.enemies:
         distance = Utilities.calculateDistanceFighters(self.player, enemy)
         radiussum = self.player.radius + enemy.radius
         if abs(distance) < radiussum:
            enemy.moveFromPlayer((radiussum - abs(distance)) * 2)

   def gameLoop(self):
      gameActive = True
      while gameActive:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               gameActive = False
         self.screen.fill("white")
         self.player.draw()
         self.handleInput()
         self.moveEnemiesToPlayer()
         self.checkEnemyPlayerCollision()
         self.drawEnemies()
         pygame.display.flip()
         self.clock.tick(60)
         # self.deltatime = self.clock.tick(60)/1000  # fps


if __name__ == "__main__":
   game = Game()
   game.gameLoop()
   pygame.quit()
