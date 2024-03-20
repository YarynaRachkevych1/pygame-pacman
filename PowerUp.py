import pygame

from Collectible import Collectible
from constants import BOARD_TILE_SIZE

class PowerUp(Collectible):
    """
    Attributes:
        map_pos: Posycja punktu bonusowego do zbierania wzgędem planszy (indeks w tablicy)
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, screen):
        """
        Funkcja rysująca bonusowy punkt. Pozycja bonusowy punktu jest obliczana na podstawie jej pozycji na mapie.
        Punkt jest rysowany jako okrąg o promieniu 4 pikseli na odpowiednich współrzędnych X i Y.

        Args:
             screen: ekran gry, na którym ma być narysowany bonusowy punkt
        """
        pygame.draw.circle(screen, 'white', (self.map_pos.x * BOARD_TILE_SIZE + 5,
                                                       self.map_pos.y * BOARD_TILE_SIZE + 5), 4)