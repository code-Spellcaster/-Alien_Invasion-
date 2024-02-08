class Settings:
    """Una clase para guardar todas las configuraciones para Alien Invasion."""
    
    def __init__(self):
        """Inicia las configuraciones ESTATICAS del juego"""
        # Configuraciones de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ajustes de la nave.
        self.ship_limit = 3

        # Ajustes de las balas.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # Se podrian limitar las balas, si quisiera.
        self.bullets_allowed = 6

        # Ajustes de los Alien.
        self.fleet_drop_speed = 10


        # Que tan rapido se vuelve el juego.
        self.speedup_scale = 1.1
        # Que tan rapido aumenta el puntaje que dan los aliens.
        self.score_scale = 1.5

        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        """Inicializa configuraciones DINAMICAS que cambian a medida avanza el juego."""
        self.ship_speed = 5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction en 1 representa derecha; -1 representa izquierda.
        self.fleet_direction = 1

        # Ajustes de puntaje.
        self.alien_points = 50

    def incrase_speed(self):
        """Ajustes de aumento de velocidad y del valor de puntaje de los aliens."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # Podria mostrarse en lugar de esto, un cartelito en la pantalla al lado del alien "+ X pts" ...
        #print(self.alien_points)
