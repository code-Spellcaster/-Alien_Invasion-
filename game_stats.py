class GameStats:
    """Hacer seguimiento a estadisticas para Alien Invasion."""

    def __init__(self, ai_game):
        """Inicializar estadisticas."""
        self.settings = ai_game.settings
        self.reset_stats()
        # El puntaje maximo nunca debe ser reiniciado.
        self.high_score = 0

    def reset_stats(self):
        """Inicializa estadisticas que han cambiado durante el juego."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
