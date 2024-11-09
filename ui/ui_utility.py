import pygame
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600
HEADER_HEIGHT = 50
FOOTER_HEIGHT = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT + HEADER_HEIGHT + FOOTER_HEIGHT))
pygame.display.set_caption("Knitting Kitten")

# Colors based on the palette
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (253, 240, 213)
TITLE_COLOR = (96, 108, 56)
BUTTON_COLOR = (188, 108, 37)
HOVER_COLOR = (221, 161, 94)
BUTTON_TEXT_COLOR = (255, 255, 255)  # White text on buttons
TITLE_TEXT_COLOR = (96, 108, 56)    # Title text color

BUTTON_SPACING = 80  # Vertical spacing between buttons

# Square size for grid elements
SQUARE_SIZE = 60

# Fonts with adjustable title font size
title_font = pygame.font.Font(None, 150)
title_map_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 50)
button_map_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)
FONT = pygame.font.Font(None, 36)

# Get the absolute path to the "items" folder relative to the current file
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
items_folder = os.path.join(project_root, "items")

# Load images dynamically using the constructed path
IMAGES = {
    "#": pygame.image.load(os.path.join(items_folder, "wall.png")),
    " ": pygame.image.load(os.path.join(items_folder, "floor.png")),
    "$": pygame.image.load(os.path.join(items_folder, "knitting_ball.png")),
    ".": pygame.image.load(os.path.join(items_folder, "basket.png")),
    "*": pygame.image.load(os.path.join(items_folder, "ball_in_basket.png")),
    "+": pygame.image.load(os.path.join(items_folder, "cat_in_basket.png")),
    "@": pygame.image.load(os.path.join(items_folder, "cat.png")),
}

# Function to load map from file
def load_map(file_path, skip_first_line=True):
    try:
        with open(file_path, 'r') as f:
            # Parse weights if skipping the first line
            weights = list(map(int, f.readline().strip().split())) if skip_first_line else []
            
            # Parse the grid, keeping leading and trailing whitespace in each row
            grid = [list(line.rstrip('\n')) for line in f.readlines()]

        # Validate grid for the number of stones
        stone_count = sum(row.count('$') + row.count('*') for row in grid)
        if len(weights) != stone_count:
            print(f"Error: Number of stones does not match weights in {file_path}.")
            return None, True  # Indicate a loading error with mismatched weights

        # Check for the number of cats (Ares) in the grid
        cat_count = sum(row.count('@') + row.count('+') for row in grid)
        if cat_count != 1:
            print("No solution: Incorrect number of cats in the grid.")
            return grid, True  # Indicate that there’s an unsolvable map due to cat count
        
        return grid, False  # Return grid and indicate no issues found

    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return None, True  # Indicate an error in loading
    
# Function to render the simulation
def render_simulation(grid, stats, speed, display_end_text=False, no_solution=False):
    screen.fill(BACKGROUND_COLOR)
    
    # Display algorithm name or "No solution"
    title_text = FONT.render("No solution for this map" if no_solution else f"Algorithm: {stats['algorithm']}", True, (255, 0, 0) if no_solution else (0, 0, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

    # Render grid
    if grid:
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x, y = j * SQUARE_SIZE, HEADER_HEIGHT + i * SQUARE_SIZE
                screen.blit(IMAGES.get(cell, IMAGES[" "]), (x, y))

    # Display stats if applicable
    if display_end_text and not no_solution:
        step_text = FONT.render(f"Steps: {stats['steps']}", True, (0, 0, 0))
        weight_text = FONT.render(f"Weight: {stats['total_weight']} $", True, (0, 0, 0))
        nodes_text = FONT.render(f"Nodes: {stats['nodes_generated']}", True, (0, 0, 0))
        time_text = FONT.render(f"Time: {stats['time_taken']} seconds", True, (0, 0, 0))
        memory_text = FONT.render(f"Memory: {stats['memory_used']} KB", True, (0, 0, 0))

        # Position each text vertically
        screen.blit(step_text, (WIDTH - 300, HEIGHT - 220 + HEADER_HEIGHT))
        screen.blit(weight_text, (WIDTH - 300, HEIGHT - 190 + HEADER_HEIGHT))
        screen.blit(nodes_text, (WIDTH - 300, HEIGHT - 160 + HEADER_HEIGHT))
        screen.blit(time_text, (WIDTH - 300, HEIGHT - 130 + HEADER_HEIGHT))
        screen.blit(memory_text, (WIDTH - 300, HEIGHT - 100 + HEADER_HEIGHT))

        # Display navigation exit message
        exit_text = FONT.render("Press ESC to exit", True, (0, 0, 0))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT + HEADER_HEIGHT - 10))

# Button classes and functions
class Button:
    def __init__(self, text, pos, font=None):
        self.text = text
        self.pos = pos
        # Use the provided font or fall back to a default font
        self.font = font if font else button_font  
        self.rendered_text = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        self.rect = self.rendered_text.get_rect(center=self.pos)

    def draw(self, screen, mouse_pos):
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect.inflate(20, 20), border_radius=10)
        screen.blit(self.rendered_text, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class MapButton:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rendered_text = button_map_font.render(self.text, True, WHITE)
        self.rect = pygame.Rect(0, 0, 300, 180)  # Large rectangle for map layout
        self.rect.center = self.pos

    def draw(self, screen, mouse_pos):
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Draw the layout preview (placeholder for map layout)
        layout_color = (200, 200, 200)
        layout_rect = pygame.Rect(self.rect.x + 20, self.rect.y + 20, 260, 120)
        pygame.draw.rect(screen, layout_color, layout_rect)

        # Draw some example walls or obstacles within the layout
        obstacle_color = (150, 150, 150)
        pygame.draw.rect(screen, obstacle_color, (layout_rect.x + 20, layout_rect.y + 60, 30, 30))
        pygame.draw.rect(screen, obstacle_color, (layout_rect.x + 100, layout_rect.y + 80, 20, 20))
        pygame.draw.rect(screen, obstacle_color, (layout_rect.x + 150, layout_rect.y + 50, 15, 50))

        screen.blit(self.rendered_text, self.rendered_text.get_rect(center=(self.rect.centerx, self.rect.centery + 70)))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def draw_arrow_button(screen, direction, pos, mouse_pos):
    arrow_color = HOVER_COLOR if pygame.Rect(pos[0] - 20, pos[1] - 20, 40, 40).collidepoint(mouse_pos) else BUTTON_COLOR
    arrow_points = [(pos[0] + 20, pos[1] - 20), (pos[0] - 20, pos[1]), (pos[0] + 20, pos[1] + 20)] if direction == "left" else \
                   [(pos[0] - 20, pos[1] - 20), (pos[0] + 20, pos[1]), (pos[0] - 20, pos[1] + 20)]
    pygame.draw.polygon(screen, arrow_color, arrow_points)