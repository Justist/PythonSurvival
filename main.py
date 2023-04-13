import pygame

from Enemy import Enemy
from Player import Player
from Utilities import Utilities


class Game:
   def __init__(self):
      pygame.init()
      self.MIDDLE = (3000, 3000)
      self.screen = pygame.display.set_mode((1280, 720))
      self.screenwidth = self.screen.get_width()
      self.screenheight = self.screen.get_height()
      self.clock = pygame.time.Clock()
      self.deltatime = 1

      self.player = Player(self.screen, self.MIDDLE)
      # initialise enemies
      self.enemies = [Enemy(self.screen, self.MIDDLE, n) for n in range(10)]

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
         self.clock.tick(60)  # self.deltatime = self.clock.tick(60)/1000  # fps


if __name__ == "__main__":
   game = Game()
   game.gameLoop()
   pygame.quit()
