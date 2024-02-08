import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Una clase para representar un alien individual en la flota."""

    def __init__(self, ai_game):
        """Inicializar el alien y definir su posicion inicial"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carga la imagen del alien y define su atributo de rectangulo.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Comience cada nuevo alien cerca del borde superior izquierdo de la pantalla.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Almacena la posicion horizontal exacta.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Devuelve True si un alien esta en el borde de la pantalla."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Mover un alien a la derecha o a la izquierda."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
