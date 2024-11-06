import pygame
import time
from ui_utility import screen, IMAGES, FONT, SQUARE_SIZE, BACKGROUND_COLOR, WIDTH, HEIGHT, HEADER_HEIGHT, load_map

directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]

# Parsing function for simulation
def parse_output(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    stats = {
        "algorithm": lines[0].strip(),
        "steps": int(lines[1].split(": ")[1]),
        "total_weight": int(lines[2].split(": ")[1]),
        "nodes_generated": int(lines[3].split(": ")[1]),
        "time_taken": float(lines[4].split(": ")[1].split()[0]),
        "memory_used": float(lines[5].split(": ")[1].split()[0]),
        "path": lines[6].strip(),
    }
    return stats

# Function to render simulation
def render_simulation(grid, stats, speed, display_end_text=False):
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the algorithm name in the header area
    algorithm_text = FONT.render(f"Algorithm: {stats['algorithm']}", True, (0, 0, 0))
    screen.blit(algorithm_text, (WIDTH // 2 - algorithm_text.get_width() // 2, 10))

    # Render the grid below the header
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x, y = j * SQUARE_SIZE, HEADER_HEIGHT + i * SQUARE_SIZE
            screen.blit(IMAGES.get(cell, IMAGES[" "]), (x, y))

    # Draw the speed bar below the grid
    pygame.draw.rect(screen, (200, 200, 200), (20, HEIGHT - 70 + HEADER_HEIGHT, 200, 20))
    pygame.draw.rect(screen, (0, 128, 255), (20, HEIGHT - 70 + HEADER_HEIGHT, int(speed * 2), 20))
    speed_text = FONT.render("Speed:", True, (0, 0, 0))
    screen.blit(speed_text, (20, HEIGHT - 100 + HEADER_HEIGHT))

    # Display end message, time, and memory if the simulation has ended
    if display_end_text:
        time_text = FONT.render(f"Time: {stats['time_taken']} seconds", True, (0, 0, 0))
        memory_text = FONT.render(f"Memory: {stats['memory_used']} KB", True, (0, 0, 0))
        exit_text = FONT.render("Press SPACE to exit", True, (0, 0, 0))
        screen.blit(time_text, (WIDTH - 300, HEIGHT - 100 + HEADER_HEIGHT))
        screen.blit(memory_text, (WIDTH - 300, HEIGHT - 70 + HEADER_HEIGHT))
        screen.blit(exit_text, (WIDTH // 2 - 100, HEIGHT - 40 + HEADER_HEIGHT))

# Function to find Ares's position in the grid
def find_ares_position(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@' or cell == '+':
                return i, j
    return None

# Function to update the grid based on action
def update_grid(grid, action):
    ares_x, ares_y = find_ares_position(grid)
    for dx, dy, move, push in directions:
        if action == move or action == push:
            new_x, new_y = ares_x + dx, ares_y + dy
            if action.islower() and grid[new_x][new_y] in [' ', '.']:
                grid[new_x][new_y] = '@' if grid[new_x][new_y] == ' ' else '+'
                grid[ares_x][ares_y] = ' ' if grid[ares_x][ares_y] == '@' else '.'
            elif action.isupper():
                stone_x, stone_y = new_x + dx, new_y + dy
                if grid[new_x][new_y] in ['$', '*'] and grid[stone_x][stone_y] in [' ', '.']:
                    grid[new_x][new_y] = '@' if grid[new_x][new_y] == '$' else '+'
                    grid[ares_x][ares_y] = ' ' if grid[ares_x][ares_y] == '@' else '.'
                    grid[stone_x][stone_y] = '*' if grid[stone_x][stone_y] == '.' else '$'
            break

# Function to simulate movement
def simulate(grid, path, stats):
    speed = 50
    display_end_text = False
    for action in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and display_end_text:
                    pygame.quit()
                    return
                elif event.key == pygame.K_LEFT:
                    speed = max(10, speed - 10)
                elif event.key == pygame.K_RIGHT:
                    speed = min(100, speed + 10)

        update_grid(grid, action)
        render_simulation(grid, stats, speed)
        pygame.display.flip()
        time.sleep(0.01 * (100 - speed))

    display_end_text = True
    while True:
        render_simulation(grid, stats, speed, display_end_text)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.quit()
                return

# Main function
def simulate_game(output_file, map_file):
    grid = load_map(map_file)
    stats = parse_output(output_file)
    simulate(grid, stats["path"], stats)

# Test
simulate_game("output/output-01.txt", "input/input-01.txt")