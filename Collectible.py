from pygame import Vector2
from abc import abstractmethod


class Collectible:
    """
    Attributes:
        map_pos: Posycja jednostki do zbierania wzgędem planszy (indeks w tablicy)
    """

    def __init__(self, x, y):
        self.map_pos = Vector2(x, y)

    @abstractmethod
    def draw(self, screen):
        """
        Metoda abstrakcyjna, która rysuje jednostkę do zbierania na ekranie gry.

        Args:
            screen: Ekran gry, na którym ma być narysowana jednostka do zbierania
        """
        pass
