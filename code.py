import math
import random
import time
import pygame

pygame.init()

# window setup
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

# constants
BG_COLOR = (0, 25, 40)
TOP_BAR_HEIGHT = 45
TARGET_PADDING = 30
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT + 1
LIVES = 3

LABEL_FONT = pygame.font.SysFont("arial", 22, bold=True)
BIG_FONT = pygame.font.SysFont("arial", 32, bold=True)

# target class
class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.25
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size >= self.MAX_SIZE:
            self.grow = False
        self.size += self.GROWTH_RATE if self.grow else -self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.size))
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), int(self.size * 0.75))
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.size * 0.5))
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), int(self.size * 0.25))

    def collide(self, x, y):
        return math.hypot(self.x - x, self.y - y) <= self.size

# ui functions
def format_time(secs):
    milli = int(secs * 10 % 10)
    seconds = int(secs % 60)
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def center(surface, y):
    return WIDTH // 2 - surface.get_width() // 2, y

def draw_top_bar(win, hits, misses, time_elapsed):
    pygame.draw.rect(win, (200, 200, 200), (0, 0, WIDTH, TOP_BAR_HEIGHT))
    pygame.draw.line(win, "black", (0, TOP_BAR_HEIGHT), (WIDTH, TOP_BAR_HEIGHT), 2)

    speed = round(hits / time_elapsed, 1) if time_elapsed > 0 else 0

    texts = [
        f"Time: {format_time(time_elapsed)}",
        f"Speed: {speed} t/s",
        f"Hits: {hits}",
        f"Lives: {LIVES - misses}"
    ]

    x = 15
    for text in texts:
        label = LABEL_FONT.render(text, True, "black")
        win.blit(label, (x, 10))
        x += label.get_width() + 40

def draw_game(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

# game over screen
def show_stats(hits, misses, total_time):
    accuracy = (hits / (hits + misses) * 100) if hits + misses > 0 else 0
    speed = round(hits / total_time, 1) if total_time > 0 else 0

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        WIN.fill(BG_COLOR)

        title = BIG_FONT.render("Game Over", True, "white")
        time_txt = LABEL_FONT.render(f"Time: {format_time(total_time)}", True, "white")
        speed_txt = LABEL_FONT.render(f"Speed: {speed} t/s", True, "white")
        hits_txt = LABEL_FONT.render(f"Hits: {hits}", True, "white")
        acc_txt = LABEL_FONT.render(f"Accuracy: {accuracy:.1f}%", True, "white")
        exit_txt = LABEL_FONT.render("Click anywhere to exit", True, "grey")

        WIN.blit(title, center(title, 150))
        WIN.blit(time_txt, center(time_txt, 220))
        WIN.blit(speed_txt, center(speed_txt, 260))
        WIN.blit(hits_txt, center(hits_txt, 300))
        WIN.blit(acc_txt, center(acc_txt, 340))
        WIN.blit(exit_txt, center(exit_txt, 420))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                return

# main game loop
def main():
    clock = pygame.time.Clock()
    targets = []

    hits = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TOP_BAR_HEIGHT + TARGET_PADDING, HEIGHT - TARGET_PADDING)
                targets.append(Target(x, y))

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        hit_this_click = False

        for target in targets[:]:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                continue

            if clicked and target.collide(*mouse_pos):
                targets.remove(target)
                hits += 1
                hit_this_click = True
                break

        if clicked and not hit_this_click:
            misses += 1

        if misses >= LIVES:
            running = False

        draw_game(WIN, targets)
        draw_top_bar(WIN, hits, misses, elapsed_time)
        pygame.display.update()

   
    show_stats(hits, misses, elapsed_time)

# run
if __name__ == "__main__":
    main()
