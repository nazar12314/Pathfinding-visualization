from .Node import Node
from .constants import ROWS, COLS, WHITE
from queue import PriorityQueue
import pygame


class Board:
    def __init__(self) -> None:
        self.nodes = []
        self.start_position = None
        self.end_position = None
        self.__create_board()

    def __create_board(self):
        for row in range(ROWS):
            self.nodes.append([])
            for col in range(COLS):
                self.nodes[row].append(Node(row, col, WHITE))

    def draw_board(self, window):
        for row in range(ROWS):
            for col in range(COLS):
                self.nodes[row][col].draw_node(window)
        
        pygame.display.update()

    def set_start_position(self, row, col):
        self.start_position = self.nodes[row][col]
        self.nodes[row][col].make_start_node()

    def set_end_position(self, row, col):
        self.end_position = self.nodes[row][col]
        self.nodes[row][col].make_end_node()

    def set_barrier_node(self, row, col):
        self.nodes[row][col].make_barrier_node()

    def clear_node(self, row, col):
        node = self.nodes[row][col]
        if node.is_start():
            self.start_position = None
        elif node.is_end():
            self.end_position = None
        node.clear()

    def manage_node(self, row, col):
        node = self.nodes[row][col]

        if not node.is_empty_node():
            if node.is_start():
                self.start_position = None
            elif node.is_end():
                self.end_position = None
            node.clear()
        else:
            node.make_border_node()

    def get_neighbours(self, row, col):
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        neighbours = []

        for x_move, y_move in moves:
            new_row = row + y_move
            new_col = col + x_move
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and not self.nodes[new_row][new_col].is_barrier():
                neighbours.append(self.nodes[row + y_move][col + x_move])

        return neighbours

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current, window):
        while current in came_from:
            current = came_from[current]
            current.make_closed_node()
            self.draw_board(window)

    def find_shortest_path(self, window):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start_position))
        came_from = {}
        g_score = {node: float('inf') for row in self.nodes for node in row}
        g_score[self.start_position] = 0

        f_score = {node: float('inf') for row in self.nodes for node in row}

        f_score[self.start_position] = self.h(
            self.start_position.get_position(),
            self.end_position.get_position()
        )

        open_set_hash = {self.start_position}

        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end_position:
                self.reconstruct_path(came_from, current, window)
                self.start_position.make_start_node()
                self.end_position.make_end_node()
                return True

            for neighbour in self.get_neighbours(current.row, current.col):
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score

                    f_score[neighbour] = temp_g_score + self.h(
                        neighbour.get_position(),
                        self.end_position.get_position()
                    )

                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.make_open_node()

            self.draw_board(window)

            if current != self.start_position:
                current.make_open_node()

        return False
