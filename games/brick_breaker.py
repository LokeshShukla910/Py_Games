import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10

LIVES_FONT = pygame.font.SysFont("comicsans", 40)
HEART = "❤"
HEART_FONT = pygame.font.SysFont("comicsans", 30)
BUTTON_FONT = pygame.font.SysFont("comicsans", 35)


class Paddle:
    VEL = 5

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction=1):
        self.x = self.x + self.VEL * direction


class Ball:
    VEL = 5

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_vel = 0
        self.y_vel = -self.VEL

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)


class Brick:
    def __init__(self, x, y, width, height, health, colors):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.colors = colors
        self.color = colors[0]

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def collide(self, ball):
        if not (ball.x <= self.x + self.width and ball.x >= self.x):
            return False
        if not (ball.y - ball.radius <= self.y + self.height and ball.y + ball.radius >= self.y):
            return False

        self.hit()
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        return True

    def hit(self):
        self.health -= 1
        t = max(0, self.health / self.max_health)
        self.color = self.interpolate(*self.colors, t)

    @staticmethod
    def interpolate(color_a, color_b, t):
        return tuple(int(a + (b - a) * (1 - t)) for a, b in zip(color_a, color_b))


def draw(win, paddle, ball, bricks, lives):
    win.fill("white")
    paddle.draw(win)
    ball.draw(win)

    for brick in bricks:
        brick.draw(win)

    for i in range(lives):
        heart = HEART_FONT.render(HEART, 1, (255, 0, 0))
        win.blit(heart, (10 + i * (heart.get_width() + 5), HEIGHT - heart.get_height() - 10))

    pygame.display.update()


def draw_restart_button(win):
    button_text = BUTTON_FONT.render("Click to Restart", 1, "blue")
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    win.blit(button_text, button_rect)
    return button_rect


def button_clicked(rect, mouse_pos):
    return rect.collidepoint(mouse_pos)


def display_text(win, text):
    text_render = LIVES_FONT.render(text, 1, "red")
    win.blit(text_render, (WIDTH / 2 - text_render.get_width() / 2, HEIGHT / 2 - text_render.get_height() / 2))
    button_rect = draw_restart_button(win)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_clicked(button_rect, pygame.mouse.get_pos()):
                    waiting = False


def ball_collision(ball):
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
    if ball.y - BALL_RADIUS <= 0:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)


def ball_paddle_collision(ball, paddle):
    if not (ball.x <= paddle.x + paddle.width and ball.x >= paddle.x):
        return
    if not (ball.y + ball.radius >= paddle.y and ball.y - ball.radius <= paddle.y + paddle.height):
        return

    paddle_center = paddle.x + paddle.width / 2
    distance_to_center = ball.x - paddle_center
    percent_width = distance_to_center / (paddle.width / 2)
    angle = percent_width * 75  # max bounce angle
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = -math.cos(angle_radians) * ball.VEL

    ball.set_vel(x_vel, y_vel)


def generate_bricks(rows, cols):
    gap = 2
    brick_width = WIDTH // cols - gap
    brick_height = 20
    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick = Brick(col * brick_width + gap * col, row * brick_height + gap * row,
                          brick_width, brick_height, 2, [(0, 255, 0), (255, 0, 0)])
            bricks.append(brick)
    return bricks


def main():
    clock = pygame.time.Clock()

    paddle_x = WIDTH / 2 - PADDLE_WIDTH / 2
    paddle_y = HEIGHT - PADDLE_HEIGHT - 5
    paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, "black")
    ball = Ball(WIDTH / 2, paddle_y - BALL_RADIUS, BALL_RADIUS, "black")

    bricks = generate_bricks(3, 10)
    lives = 3

    def reset():
        paddle.x = paddle_x
        paddle.y = paddle_y
        ball.x = WIDTH / 2
        ball.y = paddle_y - BALL_RADIUS
        ball.set_vel(0, -ball.VEL)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
            paddle.move(-1)
        if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.VEL <= WIDTH:
            paddle.move(1)

        ball.move()
        ball_collision(ball)
        ball_paddle_collision(ball, paddle)

        for brick in bricks[:]:
            if brick.collide(ball):
                if brick.health <= 0:
                    bricks.remove(brick)

        if ball.y - BALL_RADIUS > HEIGHT:
            lives -= 1
            reset()

        if lives <= 0:
            display_text(win, "You Lost!")
            bricks = generate_bricks(3, 10)
            lives = 3
            reset()

        if len(bricks) == 0:
            display_text(win, "You Won!")
            bricks = generate_bricks(3, 10)
            lives = 3
            reset()

        draw(win, paddle, ball, bricks, lives)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
