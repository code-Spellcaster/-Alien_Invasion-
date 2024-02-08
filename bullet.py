import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Una clase para manejar las balas disparadas desde la nave."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Crear una bala recta a (0, 0) y despues fijar la posicion correcta.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Guarda la posicion de la bala como un float.
        self.y = float(self.rect.y)

    def update(self):
        """Mover la bala hacia arriba de la pantalla."""
        # Actualiza la posicion exacta de la bala.
        self.y -= self.settings.bullet_speed
        # Actualiza la posicion del rect(angulo).
        self.rect.y = self.y

    def draw_bullet(self):
        """Dibuja la bala en la pantalla."""
        pygame.draw.rect(self.screen, self.color, self.rect)
