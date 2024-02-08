import pygame.font
from pygame.sprite import Group

from ship import Ship
class Scoreboard:
    """Una clase para reportar informacion de puntaje."""

    def __init__(self, ai_game):
        """Inicia los atributos de mantener los puntajes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Ajustes de fuente para la info del puntaje.
        self.text_color = (0, 135, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepara las imagenes de los puntajes iniciales.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Convierte el puntaje en una imagen renderizada."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Muestra el puntaje en la esquina superior derecha de la pantalla.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Dibuja el puntaje, las naves restantes, y el nivel en la pantalla."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Convierte el puntaje maximo en una imagen renderizada."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High score:{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Centrar el puntaje maximo en el medio de la pantalla.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Revisar si hay un puntaje mas alto."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Convertir el nivel en una imagen renderizada."""
        level_str = f"Stage: {str(self.stats.level)}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Posicionarlo un nivel bajo el puntaje
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Mostrar cuantas naves quedan."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
