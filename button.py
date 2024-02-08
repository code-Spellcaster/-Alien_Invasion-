import pygame.font

class Button:
    """Una clase para construir botones en el juego."""

    def __init__(self, ai_game, msg):
        """Inicia los atributos del boton."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Definir las dimensiones y propiedades del boton.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Construir el objeto rect del boton y centrarlo.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Para que el mensaje solo deba ser ingresado una vez.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Convierte el texto en una imagen renderizada y centra el texto debajo."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Dibuja un boton en blanco y entonces dibuja el mensaje"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
