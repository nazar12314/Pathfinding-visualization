import pygame
from visualization.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK
from visualization.Board import Board

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding visualizer")
FPS = 60


def get_row_col_from_mouse(position):
    x, y = position
    return y // SQUARE_SIZE, x // SQUARE_SIZE


def main():
    run = True
    clock = pygame.time.Clock()
    clear_mode = False

    WINDOW.fill(BLACK)

    board = Board()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    clear_mode = not clear_mode
                elif event.key == pygame.K_SPACE:
                    board.find_shortest_path(WINDOW)
                elif event.key == pygame.K_r:
                    board = Board()

            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                row = int(x // SQUARE_SIZE)
                col = int(y // SQUARE_SIZE)

                if clear_mode:
                    board.clear_node(row, col)
                    continue

                if board.start_position is None:
                    board.set_start_position(row, col)

                elif board.end_position is None:
                    board.set_end_position(row, col)

                elif (row, col) not in [board.start_position, board.end_position]:
                    board.set_barrier_node(row, col)

        board.draw_board(WINDOW)

    pygame.quit()


if __name__ == "__main__":
    main()
