# Parent class for player and enemies
class FighterEntity:
   def __init__(self, screen, MIDDLE):
      self.MIDDLE = MIDDLE
      self.x = -1
      self.y = -1
      self.screen = screen
      self.colour = None
      self.radius = -1
