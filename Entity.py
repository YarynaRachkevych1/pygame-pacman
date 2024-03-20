import pygame
from pygame import Vector2
from constants import ENTITY_BASE_SPEED, BOARD_TILE_SIZE, BOARD, WALL_IDS
from math import ceil
from abc import abstractmethod


class Entity:
    """

    Attributes:
        pos: Pozycja wzgędem plaszczyzny rysowania
        map_pos: Pozycja wzgędem planszu (indeks w tablicy)
        direction: Kierunek poruszania się
        next_direction: Nastepny kirunek poruszania się
        speed: Prędość poruszania się

    """
    def __init__(self, x, y, direction, next_direction):
        self.pos = pygame.Vector2(x, y)
        self.map_pos = Vector2()
        self.direction = direction
        self.next_direction = next_direction
        self.speed = ENTITY_BASE_SPEED

    def update_pos(self):
        """ Funkcja aktualizująca pozycję jednostki
        """
        # portale
        if self.map_pos == Vector2(0, 15):
            self.map_pos = Vector2(28, 15)
            self.pos = self.map_pos * BOARD_TILE_SIZE
        elif self.map_pos == Vector2(29, 15):
            self.map_pos = Vector2(1, 15)
            self.pos = self.map_pos * BOARD_TILE_SIZE

        # sprawdzanie, czy można zmienić kierunek
        if not self.check_next_collision(self.next_direction):
            self.direction = self.next_direction.copy()
        if not self.check_next_collision(self.direction):
            self.pos += self.direction * self.speed

        # aktualizacja map_pos
        if self.direction.x == -1:
            self.map_pos.x = ceil(self.pos.x / BOARD_TILE_SIZE)
        else:
            self.map_pos.x = self.pos.x // BOARD_TILE_SIZE
        if self.direction.y == -1:
            self.map_pos.y = ceil(self.pos.y / BOARD_TILE_SIZE)
        else:
            self.map_pos.y = self.pos.y // BOARD_TILE_SIZE

    def check_next_collision(self, direction):
        """
        Funkcyja sprawdzająca czy jest kolozija ze ścianą

        Args:
            direction: Kierunek poruszania się jednostki
        Retruns:
            True jeśli kolizja występuje, False w przeciwnym przypadku
        """
        next_map_pos = self.map_pos + direction
        if 0 <= int(next_map_pos.y) <= 32 and 0 <= int(next_map_pos.x) <= 29:
            return BOARD[int(next_map_pos.y)][int(next_map_pos.x)] in WALL_IDS
        return False

    @abstractmethod
    def change_direction(self):
        """
        Metoda abstrakcyjna, zmieniająca kierunek poruszania się jednostki
        """
        pass