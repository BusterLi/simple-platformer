import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1280, 720  # Increased screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Define clock speed variable
clock_speed = 1.0  # You can adjust this value to control the speed of the game

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 70)  # Player's rectangle
        self.velocity_y = 0  # Vertical velocity
        self.gravity = 0.5 * clock_speed  # Adjusted gravity effect for a more natural fall
        self.jump_strength = -15  # Adjusted jump strength for a more controlled jump
        self.on_ground = False  # Check if player is on the ground

    def move(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5 * clock_speed  # Move left
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5 * clock_speed  # Move right

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check for ground collision
        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y += self.jump_strength

class Spike:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # Define the spike's rectangle

    def draw(self, surface):
        # Draw spike as a red triangle
        points = [
            (self.rect.x, self.rect.y + self.rect.height),  # Bottom left
            (self.rect.x + self.rect.width // 2, self.rect.y),  # Top point
            (self.rect.x + self.rect.width, self.rect.y + self.rect.height)  # Bottom right
        ]
        pygame.draw.polygon(surface, (255, 0, 0), points)  # Draw spike as red triangle

class Door:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # Define the door's rectangle

    def draw(self, surface):
        pygame.draw.rect(surface, (139, 69, 19), self.rect)  # Draw door as brown rectangle

class Coin:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)  # Define the coin's rectangle
        self.collected = False  # Track if the coin has been collected

    def draw(self, surface):
        if not self.collected:  # Only draw if not collected
            pygame.draw.circle(surface, (255, 215, 0), (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2), self.rect.width // 2)  # Draw coin as a yellow circle

def main():
    player = Player(WIDTH // 2, HEIGHT - 100)  # Create a player instance
    spike = Spike(WIDTH // 2 - 35, HEIGHT - 70, 70, 70)  # Create a spike at the bottom center
    door = Door(WIDTH - 100, HEIGHT - 100, 50, 100)  # Create a brown door at the end

    # Create a list of coins scattered around the level, all lowered
    coins = [
        Coin(100, 550, 30),  # Coin 1 (lowered)
        Coin(300, 450, 30),  # Coin 2 (lowered)
        Coin(600, 350, 30),  # Coin 3 (lowered)
        Coin(800, 450, 30),  # Coin 4 (lowered)
        Coin(1100, 550, 30)  # Coin 5 (lowered)
    ]

    clock = pygame.time.Clock()  # Create a clock object to control frame rate
    game_over = False  # Track if the game is over

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Jump when space is pressed
                    if game_over:
                        main()  # Restart the game
                    else:
                        player.jump()

        keys = pygame.key.get_pressed()  # Get the state of all keys
        if not game_over:
            player.move(keys)  # Move the player

            # Check for collision with the spike
            if player.rect.colliderect(spike.rect):
                print("Player touched the spike! Restarting...")  # Debugging line
                player.rect.x = 0  # Reset player position to the far left
                player.rect.y = HEIGHT - 100  # Reset player position to the same height
                player.velocity_y = 0  # Reset vertical velocity

            # Check for collision with coins
            for coin in coins:
                if player.rect.colliderect(coin.rect) and not coin.collected:
                    coin.collected = True  # Mark the coin as collected
                    print("Coin collected!")  # Debugging line

            # Check for collision with the door
            if player.rect.colliderect(door.rect):
                game_over = True  # Set game over state

        # Fill the screen with a color (e.g., white)
        screen.fill((255, 255, 255))

        # Draw the player
        pygame.draw.rect(screen, (0, 0, 255), player.rect)  # Draw the player as a blue rectangle

        # Draw the spike
        spike.draw(screen)

        # Draw the door
        door.draw(screen)

        # Draw coins
        for coin in coins:
            coin.draw(screen)

        # Display win message if game is over
        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("You Win!", True, (0, 128, 0))
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press SPACE to Restart", True, (0, 0, 0))
            screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

        # Update the display
        pygame.display.flip()

        # Control the frame rate based on clock speed
        clock.tick(60 * clock_speed)  # Adjust the frame rate based on clock speed

if __name__ == "__main__":
    main()
