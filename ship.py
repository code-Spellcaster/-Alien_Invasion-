import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Una clase para manejar la nave."""

    def __init__(self, ai_game):
        """Inicializando la nave y dandole la posicion inicial"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Carga la imagen de la nave y la orienta recta.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Iniciar cada nave nueva abajo al centro de la pantalla.
        self.rect.midbottom = self.screen_rect.midbottom

        # Guarda un 'float' para la posicion exacta horizontal de la nave.
        self.x = float(self.rect.x)

        # 'Bandera de Movimiento'; comienza con una nave que no se esta moviendo.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Actualiza la posicion de la nave basado en la 'Bandera de Movimiento'"""
        # Actualiza el valor x de la nave, no el del rect(angulo).
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Dibuja la nave en su posicion actual"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centra la nave en la pantalla."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
