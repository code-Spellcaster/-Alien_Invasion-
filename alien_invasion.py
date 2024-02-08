import sys
from time import sleep

import pygame

from settings import Settings
from  game_stats import GameStats
from scoreboard import  Scoreboard
from button import  Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Clase general para manejar el comportamiento y recursos del juego."""

    def __init__(self):
        """Inicia el juego, crea los recursos."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # Inicializa Pygame.mixer
        pygame.mixer.init()

        # Carga los efectos de sonido
        self.laser_sound = pygame.mixer.Sound("sound/laser.wav")
        self.boom_sound = pygame.mixer.Sound("sound/boom.wav")
        self.mouseclick_sound = pygame.mixer.Sound("sound/mouseclick.wav")

        # Carga y reproduce la música de fondo
        self.main_music = "sound/dimensions.ogg"
        self.menu_music = "sound/menu_BattleTheme.mp3"
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.play(-1)

        # Tamaño de la pantalla, completamente editable.
        # A futuro podria agregar opciones de menu y pasarlo a settings completamente
#       self.screen = pygame.display.set_mode((500, 700))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Crea una instancia para almacenar las estadisticas del juego,
        # y crear un panel de puntaje.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Empezar Alien Invasion en un estado activo.
        self.game_active = False

        # Hace el boton de "Play".
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Comienza el bucle principal para el juego."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)
    def _check_events(self):
        # Presta atencion a eventos del mouse y el teclado.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Al precionar flecha derecha, vandera en 'true', al soltar la tecla bandera en 'false'
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Responder a presionar teclas."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responder a soltar teclas."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Inicia un nuevo juego cuando el jugador presiona "Play". """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.mouseclick_sound.play()
            # Resetea la configuracion del juego.
            self.settings.initialize_dinamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Detiene la música del menú
            pygame.mixer.music.stop()

            # Limpia cualquier remanente de balas y aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Crea una flota nueva y centra la nave.
            self._create_fleet()
            self.ship.center_ship()

            # Oculta el cursor del mouse.
            pygame.mouse.set_visible(False)

            # Selecciona y reproduce la canción principal
            pygame.mixer.music.load(self.main_music)
            pygame.mixer.music.play(-1)

    def _fire_bullet(self):
        """Crear una bala nueva y agregarla al grupo."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.laser_sound.play()

    def _update_bullets(self):
        """Actualiza la posicion de las balas y elimina las viejas."""
        #Actualiza la posicion de las balas.
        self.bullets.update()

        # Borrando las balas viejas.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Se podria mostrar en un rectangulito en la pantalla, despues...
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Responde a coliciones de las balas"""
        # Borra cualquier bala y alien que haya impactado.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.boom_sound.play()
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Si ya no quedan aliens.
            # Destrulle las balas existentes y crea una nueva flota.
            self.bullets.empty()
            self._create_fleet()
            self.settings.incrase_speed()

            # Aumentar el nivel.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Chequea si la flota esta en un borde, o si llego abajo, entonce actualiza posiciones."""
        self._check_fleet_edges()
        self._check_aliens_bottom()
        self.aliens.update()

        # Revisar impactos nave-aliens.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit!!!")
            self._ship_hit()

    def _check_fleet_edges(self):
        """Responde en consecuencia si alguno de los aliens ha alcanzado el borde."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Baja la flota entera y le cambia la direccion."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Redibuja la pantalla cada vez que pase a travez del bucle.
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Dibuja el panel de puntaje.
        self.sb.show_score()

        # Dibujar el boton de "Play" si el juego esta inactivo.
        if not self.game_active:
            self.play_button.draw_button()

        # Muestra la pantalla dibujada mas reciente.
        pygame.display.flip()

    def _create_fleet(self):
        """ Crea la flota de aliens."""
        # Hacer un alien y seguir agregando hasta que no quede lugar.
        # El espacio entre cada uno es del 1 alien (ancho y largo).
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Al incluir el panel de puntaje este tapaba la primer fila de aliens, asi que multiplique el valor
        # para que la primera fila vaya mas abajo y no se monte con el panel.
        current_x, current_y = alien_width, (alien_height * 2)
        # El primer valor define las filas de aliens.
        # Mas grande el numero, menos filas y mayor distancia a la nave.
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Terminada una fila; reseteamos el valor de x, e incrementamos el valor.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Crear un alien y colocarlo en la flota."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _ship_hit(self):
        """Responde a la nave siendo impactada por un alien."""
        if self.stats.ships_left > 0:
            # Quita una nave restante (vida), y actualiza el panel.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Borra balas y aliens restantes.
            self.bullets.empty()
            self.aliens.empty()

            # Crea una nueva flota y centra la nave.
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Verifica si es que algun alien ha alcanzado la parte inferior de la pantalla."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Tratalo como si la nave hubiera sido impactada.
                self._ship_hit()
                # Si un alien toco el fondo, no necesito seguir verificando el resto.
                break

if __name__ == '__main__':
    # Crea una instancia del juego, y corre el juego.
    ai = AlienInvasion()
    ai.run_game()
