import pygame
import os
from Player import Player
from Ghost import Ghost
from Point import Point
from PowerUp import PowerUp
from Cherry import Cherry
from constants import *


class Main:
    """

    Attributes:
        is_running: Stan uruchomienia gry. Początkowo ustawiony na True i służy do kontrolowania pętli gry
        game_over: Atrybut wskazujący, czy gra się zakończyła. Początkowo ustawiony na False
        screen: Obiekt klasy Surface z biblioteki Pygame, powierzchnię okna gry, na której renderowana jest gra
        draw_screen: Obiekt klasy Surface z biblioteki Pygame, reprezentujący powierzchnię używaną do rysowania elementów gry
        timer: Obiekt klasy Clock z biblioteki Pygame, używany do kontrolowania liczby klatek na sekundę w grze
        textures: Słownik przechowujący załadowane tekstury używane w grze. Klucze to nazwy tekstur, a wartości to obiekty klasy Surface z biblioteki Pygame
        player: Instancja klasy Player reprezentująca postać gracza w grze
        ghosts: Lista zawierająca instancje klasy Ghost reprezentujące duchy w grze
        collectible: Lista zawierająca instancje klas Point, PowerUp i Cherry reprezentujące przedmioty do zebrania w grze

    """
    def __init__(self):
        pygame.init()

        self.is_running = True
        self.game_over = False
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Pacman")
        self.draw_screen = pygame.Surface((BOARD_SIZE[0] * BOARD_TILE_SIZE, BOARD_SIZE[1] * BOARD_TILE_SIZE))
        self.timer = pygame.time.Clock()

        self.textures = {}
        self.load_textures()

        self.player = Player()

        self.ghosts = self.create_ghosts()

        self.collectible = self.get_collectibles_id()

        while self.is_running:
            self.check_events()
            self.check_keys()
            self.game()
            self.draw()
            self.display_update()

        pygame.quit()

    def load_textures(self):
        """ Funkcja wczytująca tekstury gry z plików znajdujących się w katalogu "textures" i przechowuje je w słowniku textures.
        """
        for file_name in os.listdir("textures"):
            texture = pygame.image.load("textures/" + file_name)
            self.textures[file_name[:-4]] = texture

    def display_update(self):
        """ Funkcja odświeżająca ekran i przeskalowująca powierzchnie do rysowania
        """
        self.screen.blit(pygame.transform.scale(self.draw_screen, SCREEN_SIZE), (0, 0))
        self.timer.tick(FPS)
        pygame.display.update()

    def check_events(self):
        """ Funkcja spawdzająca zdarzena w grze
        Retruns:
            False, jeśli użytkownik naciśnie przycisk "Zamknij"
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def check_keys(self):
        """ Funkcja sprawdzająca wciśnięcie klawiszy przez użytkownika i zmiany kierunku gracza na podstawie wciśniętych klawiszy
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.player.change_direction(pygame.Vector2(0, -1))
        if keys[pygame.K_DOWN]:
            self.player.change_direction(pygame.Vector2(0, 1))
        if keys[pygame.K_LEFT]:
            self.player.change_direction(pygame.Vector2(-1, 0))
        if keys[pygame.K_RIGHT]:
            self.player.change_direction(pygame.Vector2(1, 0))

    def check_ghost_player_collision(self):
        """
        Funkcja aprawdzająca czy wystąpiła kolizija gracza z którymkolwiek duchem
        Retruns:
            True, jeśli kolizia wystąpiła
        """
        i = 0
        while i < len(self.ghosts):
            if self.ghosts[i].map_pos == self.player.map_pos:
                if self.player.can_eat_timer > 0:
                    self.ghosts.pop(i)
                else:
                    return True
            i += 1

    def game(self):
        """
        Funkcja zawierająca główną logikę gry

        Jeśli gra nie jest zakończona, aktualizowane są położenie gracza i duchów

        Zmienia wartość atrybutu game_over na True, jeśli:
            wystąpiła kolizia gracza z duchem - warunek przegranej
            gracz zebrał wszystkie punkty z planszy - warunek wygranej

        Również sprawdzane są kolizje gracza z przedmiotami do zebrania. Jeśli gracz koliduje z punktem, zwiększana
        jest liczba zebranych punktów. Jeśli gracz koliduje z power-upem, ustawiany jest timer, który pozwala graczowi na zjedzenie duchów.
        Jeśli gracz koliduje z wiśnią, ustawiany jest timer, który wpływa na szybkość poruszania się duchów

        """
        if not self.game_over:
            self.player.update()
            for ghost in self.ghosts:
                ghost.change_direction()
                ghost.update_pos()

        i = 0
        while i < len(self.collectible):
            if self.player.check_collision_point(self.collectible[i]):
                if isinstance(self.collectible[i], Point):
                    self.player.collected_points += 1
                if isinstance(self.collectible[i], PowerUp):
                    self.player.can_eat_timer = CAN_EAT_TIMER
                if isinstance(self.collectible[i], Cherry):
                    self.player.cherry_timer = CHERRY_TIMER
                self.collectible.pop(i)

            i += 1

        if self.player.collected_points == 242:
            self.ghosts = []
            self.game_over = True

        self.check_ghost_player_collision()
        if self.check_ghost_player_collision():
            self.game_over = True

    def draw(self):
        """
        Funkcja odpowiedzialna za rysowanie grafiki gry na ekranie

        Na początku wypełnia ekran kolorem tła, a następnie rysuje planszę gry.
        Następnie rysuje gracza, biorąc pod uwagę aktualną animację i kierunek poruszania się gracza. Jeśli kierunek gracza jest w lewo,
        tekstura gracza zostaje odbita lustrzanie. Jeśli kierunek gracza jest w górę, tekstura gracza zostaje obrócona o 90 stopni
        zgodnie z ruchem wskazówek zegara. Jeśli kierunek gracza jest w dół, tekstura gracza zostaje obrócona o 90 stopni przeciwnie
        do ruchu wskazówek zegara

        Następnie rysuje przedmioty do zebrania na planszy gry

        Następnie rysuje duchów. Wykorzystywane są różne tekstury dla każdego ducha, a także możliwość dezaktywacji
        duchów, gdy gracz może je zjeść

        Na końcu, jeśli gra jest zakończona, w zależności od wyniku gry wyświetla się odpowiedni komunikat ("You Win" lub "Game Over")

        """
        self.draw_screen.fill(BACKGROUND_COLOR)
        self.draw_board()

        # rysowanie gracza
        player_texture = self.textures["player_" + str(self.player.actual_animation_frame)]
        if self.player.direction.x == -1:
            player_texture = pygame.transform.flip(player_texture, True, False)
        if self.player.direction.y == -1:
            player_texture = pygame.transform.rotate(player_texture, 90)
        if self.player.direction.y == 1:
            player_texture = pygame.transform.rotate(player_texture, -90)

        self.draw_screen.blit(player_texture, self.player.pos - pygame.Vector2(PLAYER_SHIFT[0], PLAYER_SHIFT[1]))


        # rysowanie rzeczy do zbierania
        for collectiable in self.collectible:
            collectiable.draw(self.draw_screen)

        # rysowanie duchów
        ghosts_texture = [self.textures["ghost" + str(i)] for i in range(1, 6)]
        i = 0
        if self.player.can_eat_timer > 0:
            for ghost in self.ghosts:
                self.draw_screen.blit(self.textures["ghost_disabled"], ghost.pos - pygame.Vector2(3, 3))
        else:
            for ghost in self.ghosts:
                self.draw_screen.blit(ghosts_texture[i], ghost.pos - pygame.Vector2(3, 3))
                i += 1

        if self.game_over and self.player.collected_points == 242:
            self.draw_screen.blit(self.textures['you_win'], (100, 100))
        elif self.game_over:
            self.draw_screen.blit(self.textures['game_over'], (100, 100))


    def draw_board(self):
        """
        Funkcja rysująca planszę na powierzchni do rysowania
        Przechodzi po tablice BOARD i w zależności od znaczenia rysuje odpowiedni rysunek
        """
        for y, line in enumerate(BOARD):
            for x, tile in enumerate(line):
                if tile in [3, 4]:
                    texture = self.textures["wall-straight"]
                    if tile == 4:
                        texture = pygame.transform.rotate(texture, 90)
                    self.draw_screen.blit(texture, pygame.Vector2(x, y) * BOARD_TILE_SIZE)
                elif tile in [5, 6, 7, 8]:
                    texture = self.textures["wall-corner"]
                    if tile == 7:
                        texture = pygame.transform.rotate(texture, -90)
                    elif tile == 6:
                        texture = pygame.transform.rotate(texture, 180)
                    elif tile == 5:
                        texture = pygame.transform.rotate(texture, 90)
                    self.draw_screen.blit(texture, pygame.Vector2(x, y) * BOARD_TILE_SIZE)
                elif tile == 10:
                    texture = self.textures["wall"]
                    self.draw_screen.blit(texture, pygame.Vector2(x, y) * BOARD_TILE_SIZE)

    def get_collectibles_id(self):
        """
        Funkcja tworząca punkty do zbierania
        Retruns:
            Lista objektów wszystkich rodzai punktów do zrierania
        """
        collectibles_id = []
        for i in range(len(BOARD)):
            for j in range(len(BOARD[i])):
                if BOARD[i][j] == 1:
                    collectibles_id.append(Point(j, i))
                if BOARD[i][j] == 2:
                    collectibles_id.append(PowerUp(j, i))
                if BOARD[i][j] == 9:
                    collectibles_id.append(Cherry(j, i))
        return collectibles_id

    def create_ghosts(self):
        """
        Funkcja tworząca duchów
        Returns:
            Lista obiektów duchów, gdzie każdy duch jest tworzony na podstawie pozycji startowych
        """
        ghosts_list = []
        for pos in GHOSTS_START_POS:
            ghosts_list.append(Ghost(pos[0], pos[1]))
        return ghosts_list


if __name__ == "__main__":
    Main()
