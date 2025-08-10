import pygame
import random

pygame.init()

# define constants
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
TILE_SIZE = 25
BG = (169, 169, 169)  # Dark grey
MINES = 60
GAME_LOST = False
MINE_IMAGE = pygame.transform.scale(
    pygame.image.load("mine.jpg"), (TILE_SIZE, TILE_SIZE)
)
FLAG_IMAGE = pygame.transform.scale(
    pygame.image.load("flag.png"), (TILE_SIZE, TILE_SIZE)
)
TEXT1 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("1", True, ("blue")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)
TEXT2 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("2", True, ("green")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)
TEXT3 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("3", True, ("red")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)
TEXT4 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("4", True, ("purple")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)
TEXT5 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("5", True, ("orange")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)
TEXT6 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("6", True, ("black")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)
TEXT7 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("7", True, ("pink")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)
TEXT8 = pygame.transform.scale(
    pygame.font.Font(None, 64).render("8", True, ("brown")),
    (TILE_SIZE * 0.75, TILE_SIZE * 0.75),
)


# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(MINE_IMAGE)


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.value = 0
        self.flagged = False
        self.game_over_indicator = False


def game_over():
    for tile in coordinates:
        tile.is_revealed = True
        tile.game_over_indicator = True
    global GAME_LOST
    GAME_LOST = True


def set_mines():
    random.shuffle(coordinates)
    for i in range(MINES):
        coordinates[i].is_mine = True
        # Update neighboring tile counts
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = next(
                    (
                        tile
                        for tile in coordinates
                        if tile.x == coordinates[i].x + dx * TILE_SIZE
                        and tile.y == coordinates[i].y + dy * TILE_SIZE
                    ),
                    None,
                )
                if neighbor:
                    neighbor.value += 1


def draw_grid():
    pygame.draw.line(screen, (0, 0, 0), (0, 48), (SCREEN_WIDTH, 48), 2)
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(50, SCREEN_HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            tile = next(
                (tile for tile in coordinates if tile.x == x and tile.y == y), None
            )
            if tile.is_revealed:
                if tile.is_mine and tile.game_over_indicator:
                    screen.blit(MINE_IMAGE, (x, y))
                else:
                    if tile.value > 0:
                        screen.blit(globals()[f"TEXT{tile.value}"], (x + 5, y + 5))
            elif tile.flagged:
                screen.blit(FLAG_IMAGE, (x, y))
            else:
                pygame.draw.rect(screen, (100, 100, 100), rect, 1)


def clear_nearby_tiles(tile):
    if tile.value == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = next(
                    (
                        t
                        for t in coordinates
                        if t.x == tile.x + dx * TILE_SIZE
                        and t.y == tile.y + dy * TILE_SIZE
                    ),
                    None,
                )
                if neighbor and not neighbor.is_revealed:
                    neighbor.is_revealed = True
                    clear_nearby_tiles(neighbor)


def clicked(mouse_x, mouse_y, button):
    if button == 1:  # Left click
        for tile in coordinates:
            if (
                tile.x <= mouse_x < tile.x + TILE_SIZE
                and tile.y <= mouse_y < tile.y + TILE_SIZE
            ):
                if tile.is_mine:
                    game_over()
                tile.is_revealed = True
                clear_nearby_tiles(tile)
                break
    elif button == 3:  # Right click
        for tile in coordinates:
            if (
                tile.x <= mouse_x < tile.x + TILE_SIZE
                and tile.y <= mouse_y < tile.y + TILE_SIZE
            ):
                tile.flagged = not tile.flagged

                break


def reset_game():
    global coordinates, clock, elapsed_time, start_time, GAME_LOST
    coordinates = []
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(50, SCREEN_HEIGHT, TILE_SIZE):
            coordinates.append(Tile(x, y))
    set_mines()
    clock = pygame.time.Clock()
    elapsed_time = 0
    start_time = pygame.time.get_ticks()
    GAME_LOST = False


def check_if_won():
    if all(tile.is_revealed or tile.is_mine for tile in coordinates):
        return True
    else:
        return False


def game_over_screen():
    global GAME_LOST
    if GAME_LOST:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))

        screen.blit(
            text,
            (
                SCREEN_WIDTH // 2 - text.get_width() // 2,
                SCREEN_HEIGHT // 2 - text.get_height() // 2,
            ),
        )
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("You Won!", True, (0, 255, 0))
        screen.blit(
            text,
            (
                SCREEN_WIDTH // 2 - text.get_width() // 2,
                SCREEN_HEIGHT // 2 - text.get_height() // 2,
            ),
        )
    font = pygame.font.Font(None, 36)
    text = font.render("Press any key to restart", True, ("black"))
    screen.blit(
        text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 40)
    )
    for key in pygame.event.get():
        if key.type == pygame.KEYDOWN:
            reset_game()


def main():
    global clock, screen, coordinates, elapsed_time, start_time
    reset_game()
    running = True
    while running:
        screen.fill(BG)  # Fill the screen with background color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked(mouse_x, mouse_y, event.button)
        draw_grid()
        if GAME_LOST:
            game_over_screen()
        elif check_if_won():
            game_over_screen()
        if not GAME_LOST and not check_if_won():
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        font = pygame.font.Font(None, 36)

        text = font.render(f"Time Elapsed: {elapsed_time}s", True, ("black"))
        screen.blit(text, (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
