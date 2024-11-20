import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
user_paddle = pygame.Rect(50, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
computer_paddle = pygame.Rect(WIDTH - 70, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball properties
BALL_RADIUS = 10
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5

# Computer paddle speed
COMPUTER_SPEED =5

# Frame rate control
clock = pygame.time.Clock()
FPS = 60

# Scoring
user_score = 0
computer_score = 0
WINNING_SCORE = 5

# Font for score display
font = pygame.font.Font(None, 74)

# Function to display scores and win message
def display_scores():
    user_text = font.render(f"{user_score}", True, WHITE)
    computer_text = font.render(f"{computer_score}", True, WHITE)
    screen.blit(user_text, (WIDTH // 4, 20))
    screen.blit(computer_text, ((WIDTH // 4) * 3, 20))

def display_winner(winner):
    winner_text = font.render(f"{winner} WINS!", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # User paddle follows mouse
    _, mouse_y = pygame.mouse.get_pos()
    user_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, mouse_y - (PADDLE_HEIGHT // 2)))

    # Computer paddle follows ball (slower)
    if computer_paddle.centery < ball_y:
         computer_paddle.y += COMPUTER_SPEED
    elif computer_paddle.centery > ball_y:
        computer_paddle.y -= COMPUTER_SPEED

    # Prevent computer paddle from going off-screen
    computer_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, computer_paddle.y))

    # Move the ball
    ball_x += ball_speed_x
  	  ball_y += ball_speed_y

    # Ball bounces off top and bottom walls
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_speed_y *= -1

    # Ball bounces off paddles
    if user_paddle.colliderect((ball_x - BALL_RADIUS, ball_y, BALL_RADIUS * 2, BALL_RADIUS * 2)) and ball_speed_x < 0:
        ball_speed_x *= -1
    elif computer_paddle.colliderect((ball_x + BALL_RADIUS, ball_y, BALL_RADIUS * 2, BALL_RADIUS * 2)) and ball_speed_x > 0:
        ball_speed_x *= -1

    # Check for scoring
    if ball_x < 0:
        computer_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1
    elif ball_x > WIDTH:
        user_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1

    # Check for a winner
    if user_score == WINNING_SCORE:
        display_winner("User")
        user_score, computer_score = 0, 0
        ball_x, ball_y = WIDTH / 2, HEIGHT / 2
    elif computer_score == WINNING_SCORE:
        display_winner("Computer")
        user_score, computer_score = 0, 0
        ball_x, ball_y = WIDTH / 2, HEIGHT / 2

    # Redraw screen
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, user_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
    display_scores()
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)
