import pygame
from .constants import BLACK, BLUE, GREEN, GREY, WHITE, RED, SQUARE_SIZE, BORDER

class Node:
    def __init__(self, row, col, color=WHITE) -> None:
        self.color = color
        self.height = self.width = SQUARE_SIZE
        self.row = row
        self.col = col
        self.x_position, self.y_position = self.__calculate_position()

    def __calculate_position(self):
        x_position = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y_position = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

        return x_position, y_position

    def make_start_node(self):
        self.color = GREEN

    def make_end_node(self):
        self.color = RED

    def make_barrier_node(self):
        self.color = BLACK

    def make_open_node(self):
        self.color = GREY

    def make_closed_node(self):
        self.color = BLUE

    def draw_node(self, window):
        pygame.draw.rect(
            window,
            self.color,
            (self.row * SQUARE_SIZE, self.col * SQUARE_SIZE, SQUARE_SIZE - BORDER, SQUARE_SIZE - BORDER)
        )

    def is_empty_node(self):
        return not (self.is_end() or self.is_start() or self.is_border())

    def clear(self):
        self.color = WHITE

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def get_position(self):
        return self.row, self.col
