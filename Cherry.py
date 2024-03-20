import pygame

from Collectible import Collectible
from constants import BOARD_TILE_SIZE

class Cherry(Collectible):
    """
    Attributes:
        map_pos: Posycja wiśni do zbierania wzgędem planszy (indeks w tablicy)
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, screen):
        """
        Funkcja rysująca wiśnię. Pozycja wiśni jest obliczana na podstawie jej pozycji na mapie.
        Wiśnia jest rysowana jako okrąg o promieniu 4 pikseli na odpowiednich współrzędnych X i Y.

        Args:
             screen: ekran gry, na którym ma być narysowana wiśnia
        """
        pygame.draw.circle(screen, 'red', (self.map_pos.x * BOARD_TILE_SIZE + 5,
                                                     self.map_pos.y * BOARD_TILE_SIZE + 5), 4)