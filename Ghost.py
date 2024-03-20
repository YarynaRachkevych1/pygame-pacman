from Entity import Entity
from pygame import Vector2
from constants import GHOST_CHANGE_DIRECTION_TIMER, WALL_IDS
import random


class Ghost(Entity):
    """

    Attributes:
        direction_timer: Licznik czasu do zmiany kierunku ruchu ducha
        counter: Licznik klatek

    """
    def __init__(self, x, y):
        super().__init__(x, y, Vector2(0, -1), Vector2(0, -1))
        self.direction_timer = 0
        self.counter = 0

    def change_direction(self):
        """Funkcja zmieniająca kierunek poruszania się duchaj co wartość zmiennej direction_timer lub jeśli występuje kolizia ze ściną
        """
        if self.counter < 50:
            if self.counter >= 48:
                self.next_direction = random.choice([Vector2(1, 0), Vector2(-1, 0)])
                self.direction = self.next_direction
            self.counter += 1
        else:
            WALL_IDS.append(10)
            if self.check_next_collision(self.direction) or self.direction_timer == GHOST_CHANGE_DIRECTION_TIMER:
                self.next_direction = random.choice([Vector2(0, -1), Vector2(0, 1), Vector2(1, 0), Vector2(-1, 0)])
                self.direction = self.next_direction
                self.direction_timer = 0
            self.direction_timer += 1
