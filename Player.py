import pygame

from FighterEntity import FighterEntity


class Player(FighterEntity):
   def __init__(self, screen, MIDDLE):
      super().__init__(screen, MIDDLE)
      self.MIDDLE = MIDDLE
      self.x = self.MIDDLE[0]
      self.y = self.MIDDLE[1]
      self.radius = 30
      self.colour = "red"
      self.screenmiddle = pygame.Vector2(self.screen.get_width() / 2,
                                         self.screen.get_height() / 2)

   def draw(self):
      # player is always drawn in the middle
      pygame.draw.circle(self.screen, self.colour, self.screenmiddle, self.radius)
