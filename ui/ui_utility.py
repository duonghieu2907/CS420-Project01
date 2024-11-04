import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban")

# Colors based on the palette
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (253, 240, 213)
TITLE_COLOR = (96, 108, 56)
BUTTON_COLOR = (188, 108, 37)
HOVER_COLOR = (221, 161, 94)
BUTTON_TEXT_COLOR = (255, 255, 255)  # White text on buttons
TITLE_TEXT_COLOR = (96, 108, 56)    # Title text color

BUTTON_SPACING = 80  # Vertical spacing between buttons

# Fonts with adjustable title font size
title_font = pygame.font.Font(None, 150)
title_map_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 50)
button_map_font = pygame.font.Font(None, 40)

# Button class
class Button:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rendered_text = button_font.render(self.text, True, BUTTON_TEXT_COLOR)
        self.rect = self.rendered_text.get_rect(center=self.pos)

    def draw(self, screen, mouse_pos):
        # Change color on hover
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect.inflate(20, 20), border_radius=10)
        screen.blit(self.rendered_text, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Button class with layout preview
class MapButton:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rendered_text = button_map_font.render(self.text, True, WHITE)
        self.rect = pygame.Rect(0, 0, 300, 180)  # Large rectangle for map layout
        self.rect.center = self.pos

    def draw(self, screen, mouse_pos):
        # Change color on hover
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

        # Draw the map name
        screen.blit(self.rendered_text, self.rendered_text.get_rect(center=(self.rect.centerx, self.rect.centery + 70)))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)



# Draw arrow buttons for pagination with hover effect
def draw_arrow_button(screen, direction, pos, mouse_pos):
    # Define the default color
    arrow_color = HOVER_COLOR if pygame.Rect(pos[0] - 20, pos[1] - 20, 40, 40).collidepoint(mouse_pos) else BUTTON_COLOR

    # Define the points for the left or right arrow
    arrow_points = [(pos[0] + 20, pos[1] - 20), (pos[0] - 20, pos[1]), (pos[0] + 20, pos[1] + 20)] if direction == "left" else \
                   [(pos[0] - 20, pos[1] - 20), (pos[0] + 20, pos[1]), (pos[0] - 20, pos[1] + 20)]

    # Draw the arrow as a polygon
    pygame.draw.polygon(screen, arrow_color, arrow_points)