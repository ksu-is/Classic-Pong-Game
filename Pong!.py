import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
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

# Difficulty levels
difficulty = "Medium"  # Default difficulty

# Frame rate control
clock = pygame.time.Clock()
FPS = 60

# Scoring
user_score = 0
computer_score = 0
WINNING_SCORE = 5

# Font for score display and difficulty selection screen
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

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

# Function to set computer's paddle speed based on difficulty
def set_computer_speed():
    global COMPUTER_SPEED
    if difficulty == "Easy":
        COMPUTER_SPEED = 2
    elif difficulty == "Medium":
        COMPUTER_SPEED = 4
    elif difficulty == "Hard":
        COMPUTER_SPEED = 6

# Function to display the difficulty selection screen
def display_difficulty_screen():
    screen.fill(BLACK)
    title_text = font.render("Pong Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    easy_text = small_font.render("Press 1 for Easy", True, WHITE)
    medium_text = small_font.render("Press 2 for Medium", True, WHITE)
    hard_text = small_font.render("Press 3 for Hard", True, WHITE)

    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

# Game loop
def game_loop():
    global user_score, computer_score, ball_x, ball_y, ball_speed_x, ball_speed_y

    # Main game loop
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

        # Computer paddle follows ball (slower or faster based on difficulty)
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
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        elif computer_score == WINNING_SCORE:
            display_winner("Computer")
            user_score, computer_score = 0, 0
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2

        # Redraw screen with the background features
        screen.fill(BLACK)  # Black background
        # Draw middle line
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        # Draw center circle
        pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 50, 2)
        pygame.draw.rect(screen, WHITE, user_paddle)
        pygame.draw.rect(screen, WHITE, computer_paddle)
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
        display_scores()
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)

# Difficulty selection screen loop
def difficulty_selection_loop():
    global difficulty
    selecting_difficulty = True
    while selecting_difficulty:
        display_difficulty_screen()

        # Handle difficulty selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Easy
                    difficulty = "Easy"
                    selecting_difficulty = False
                elif event.key == pygame.K_2:  # Medium
                    difficulty = "Medium"
                    selecting_difficulty = False
                elif event.key == pygame.K_3:  # Hard
                    difficulty = "Hard"
                    selecting_difficulty = False

    # Start the game loop after difficulty selection
    set_computer_speed()
    game_loop()

# Start the game by showing the difficulty screen
difficulty_selection_loop()
