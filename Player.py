from Entity import Entity
from constants import PLAYER_START_POS, PLAYER_ANIMATION_SPEED, PLAYER_ANIMATION_FRAMES, ENTITY_BASE_SPEED, PLAYER_CHERRY_SPEED
from pygame import Vector2

class Player(Entity):
    """

    Attributes:
        actual_animation_frame: Numer aktualnej klatki animacji
        animation_timer: Licznik czasu do zmiany czasu animacji
        collected_points: Ilość punktów zebranych przez gracza
        can_eat_timer: Licznik czasu możliwaści zjedania duchów
        cherry_timer: Licznik czasu zwiększonej prędkości

    """
    def __init__(self):
        super().__init__(PLAYER_START_POS[0], PLAYER_START_POS[1], Vector2(0, 0), Vector2(0, 0))
        self.actual_animation_frame = 0
        self.animation_timer = 0
        self.collected_points = 0
        self.can_eat_timer = 0
        self.cherry_timer = 0

    def update(self):
        """ Funkcja aktualizująca pozycję gracza i sprawdza, czy gracz może zjadać duchów i miec większą prędkość
        """
        self.update_pos()
        self.animation_timer += 1
        self.can_eat_timer -= 1
        self.can_eat_timer = max(self.can_eat_timer, 0)
        self.cherry_timer -= 1
        self.cherry_timer = max(self.cherry_timer, 0)
        if self.cherry_timer > 0:
            self.speed = PLAYER_CHERRY_SPEED
        else:
            self.speed = ENTITY_BASE_SPEED
        if self.animation_timer >= 1 / PLAYER_ANIMATION_SPEED:
            self.animation_timer = 0
            self.actual_animation_frame += 1
            if self.actual_animation_frame >= PLAYER_ANIMATION_FRAMES:
                self.actual_animation_frame = 0

    def change_direction(self, direction):
        """
        Funkcyja zmienająca kierunek gracza na podany

        Args:
            direction: Nowy kierunek poruszania się gracza
        """
        self.next_direction = direction

    def check_collision_point(self, point):
        """
        Funkcyja sprawdzająca czy jest kolozija jednoskti z podanym punktem na plaszy

        Args:
            point: Punkt dla którego jest sprawdzana kolizia
        Retruns:
            True jeśli kolizja występuje, False w przeciwnym przypadku
        """
        return self.map_pos == point.map_pos
