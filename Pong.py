import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('PinPong_Game_Pro')
fps = 60


class Player:
    def __init__(self, x, y, width, height, color, speed, is_ai=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.is_ai = is_ai

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=7)

    def move(self, keys, up_key, down_key, ball=None):
        if self.is_ai and ball:
            if ball.speed_x > 0 and ball.rect.centerx > WIDTH // 2:
                if abs(self.rect.centery - ball.rect.centery) > 10:
                    if self.rect.centery < ball.rect.centery:
                        self.rect.y += self.speed
                    else:
                        self.rect.y -= self.speed
        else:
            if keys[up_key] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[down_key] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed

        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT


class Ball:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.radius = radius
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.color = color
        self.start_speed_x = speed_x
        self.start_speed_y = speed_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.waiting = False
        self.wait_timer = 0

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def update(self):
        if self.waiting:
            if pygame.time.get_ticks() - self.wait_timer > 1000:
                self.waiting = False
            return

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.waiting = True
        self.wait_timer = pygame.time.get_ticks()
        self.speed_x = self.start_speed_x * random.choice([-1, 1])
        self.speed_y = self.start_speed_y * random.choice([-1, 1])


def draw_scene(score1, score2, is_ai):
    screen.fill((20, 20, 25))
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, (60, 60, 60), (WIDTH // 2 - 2, y + 10, 4, 20))

    font = pygame.font.SysFont('Arial', 60, bold=True)
    small_font = pygame.font.SysFont('Arial', 18)

    s1_txt = font.render(str(score1), True, (200, 50, 50))
    s2_txt = font.render(str(score2), True, (50, 50, 200))

    mode_label = "2 PLAYER MODE" if is_ai else "AI MODE"
    mode_txt = small_font.render(f"TAB: {mode_label}", True, (100, 100, 100))

    screen.blit(s1_txt, (WIDTH // 4, 30))
    screen.blit(s2_txt, (WIDTH * 3 // 4 - 20, 30))
    screen.blit(mode_txt, (WIDTH // 2 - mode_txt.get_width() // 2, HEIGHT - 30))


player1 = Player(20, HEIGHT // 2 - 50, 15, 100, (200, 50, 50), 7)
player2 = Player(WIDTH - 35, HEIGHT // 2 - 50, 15, 100, (50, 50, 200), 6, is_ai=True)
ball = Ball(WIDTH // 2, HEIGHT // 2, 10, (255, 255, 255), 7, 7)

score1 = 0
score2 = 0
accel = 1.05

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                player2.is_ai = not player2.is_ai

    keys = pygame.key.get_pressed()
    player1.move(keys, pygame.K_w, pygame.K_s)
    player2.move(keys, pygame.K_UP, pygame.K_DOWN, ball)

    ball.update()

    if ball.rect.colliderect(player1.rect):
        ball.speed_x = abs(ball.speed_x) * accel
        ball.rect.left = player1.rect.right
        offset = (ball.rect.centery - player1.rect.centery) / (player1.rect.height / 2)
        ball.speed_y = offset * abs(ball.speed_x)

    if ball.rect.colliderect(player2.rect):
        ball.speed_x = -abs(ball.speed_x) * accel
        ball.rect.right = player2.rect.left
        offset = (ball.rect.centery - player2.rect.centery) / (player2.rect.height / 2)
        ball.speed_y = offset * abs(ball.speed_x)

    if ball.rect.left < 0:
        score2 += 1
        ball.reset()
    if ball.rect.right > WIDTH:
        score1 += 1
        ball.reset()

    if abs(ball.speed_x) > 18:
        ball.speed_x = 18 if ball.speed_x > 0 else -18

    draw_scene(score1, score2, player2.is_ai)
    player1.draw()
    player2.draw()
    ball.draw()

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()