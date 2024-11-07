import pygame
import time
import os
from ui_utility import screen, IMAGES, FONT, SQUARE_SIZE, BACKGROUND_COLOR, WIDTH, HEIGHT, HEADER_HEIGHT, load_map

directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]

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
        "path": lines[6].strip() if len(lines) > 6 else "No solution"
    }
    return stats

def render_simulation(grid, stats, speed, display_end_text=False, no_solution=False):
    screen.fill(BACKGROUND_COLOR)
    
    # Display algorithm name or "No solution" at the top
    if no_solution:
        title_text = FONT.render("No solution for this map", True, (255, 0, 0))
    else:
        title_text = FONT.render(f"Algorithm: {stats['algorithm']}", True, (0, 0, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

    # Render the grid cells with images for walls, floor, stones, baskets, etc.
    if grid:
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x, y = j * SQUARE_SIZE, HEADER_HEIGHT + i * SQUARE_SIZE
                screen.blit(IMAGES.get(cell, IMAGES[" "]), (x, y))

    # Draw the speed adjustment bar below the grid
    pygame.draw.rect(screen, (200, 200, 200), (20, HEIGHT - 70 + HEADER_HEIGHT, 200, 20))
    pygame.draw.rect(screen, (0, 128, 255), (20, HEIGHT - 70 + HEADER_HEIGHT, int(speed * 2), 20))
    speed_text = FONT.render("Speed:", True, (0, 0, 0))
    screen.blit(speed_text, (20, HEIGHT - 100 + HEADER_HEIGHT))

    # Display simulation completion message with time and memory stats, if applicable
    if display_end_text and not no_solution:
        time_text = FONT.render(f"Time: {stats['time_taken']} seconds", True, (0, 0, 0))
        memory_text = FONT.render(f"Memory: {stats['memory_used']} KB", True, (0, 0, 0))
        weight_text = FONT.render(f"Weight: {stats['total_weight']} $", True, (0, 0, 0))
        step_text = FONT.render(f"Step: {stats['steps']} ", True, (0, 0, 0))
        screen.blit(time_text, (WIDTH - 300, HEIGHT - 100 + HEADER_HEIGHT))
        screen.blit(memory_text, (WIDTH - 300, HEIGHT - 70 + HEADER_HEIGHT))
        screen.blit(weight_text, (WIDTH - 300, HEIGHT - 130 + HEADER_HEIGHT))
        screen.blit(step_text, (WIDTH - 300, HEIGHT - 160 + HEADER_HEIGHT))

    # Display persistent instructions at the bottom
    pause_text = FONT.render("Press SPACE to pause, SPACE again to continue", True, (0, 0, 0))
    exit_text = FONT.render("Press ESC to exit", True, (0, 0, 0))
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT + HEADER_HEIGHT - 40))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT + HEADER_HEIGHT - 10))

def find_ares_position(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@' or cell == '+':
                return i, j
    return None

def update_grid(grid, action):
    ares_x, ares_y = find_ares_position(grid)
    for dx, dy, move, push in directions:
        if action == move or action == push:
            new_x, new_y = ares_x + dx, ares_y + dy

            # Handle movement actions (lowercase)
            if action.islower() and grid[new_x][new_y] in [' ', '.']:
                grid[new_x][new_y] = '@' if grid[new_x][new_y] == ' ' else '+'
                grid[ares_x][ares_y] = ' ' if grid[ares_x][ares_y] == '@' else '.'

            # Handle push actions (uppercase) and update stone positions
            elif action.isupper():
                stone_x, stone_y = new_x + dx, new_y + dy
                if grid[new_x][new_y] in ['$', '*'] and grid[stone_x][stone_y] in [' ', '.']:
                    grid[new_x][new_y] = '@' if grid[new_x][new_y] == '$' else '+'
                    grid[ares_x][ares_y] = ' ' if grid[ares_x][ares_y] == '@' else '.'
                    grid[stone_x][stone_y] = '*' if grid[stone_x][stone_y] == '.' else '$'
            break

def simulate(grid, path, stats, playing):
    speed = 50
    display_end_text = False
    paused = False

    # Check if the map has a solution
    no_solution = path == "No solution"
    if no_solution:
        display_end_text = True

    # Process actions if there's a solution
    for action in path:
        if no_solution:
            break  # Skip simulation if there's no solution

        # Handle pause state
        while paused:
            render_simulation(grid, stats, speed)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #playing = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                    elif event.key == pygame.K_ESCAPE:
                        #pygame.quit()
                        playing = False
                        return
                    elif event.key == pygame.K_LEFT:
                        speed = max(10, speed - 10)
                    elif event.key == pygame.K_RIGHT:
                        speed = min(100, speed + 10)

        # Handle main simulation events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #playing = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = True
                elif event.key == pygame.K_ESCAPE:
                    #pygame.quit()
                    playing = False
                    return
                elif event.key == pygame.K_LEFT:
                    speed = max(10, speed - 10)
                elif event.key == pygame.K_RIGHT:
                    speed = min(100, speed + 10)

        # Update grid based on the current action
        update_grid(grid, action)
        render_simulation(grid, stats, speed)
        pygame.display.flip()
        time.sleep(0.01 * (100 - speed))



    # Display the end text after completing the path
    display_end_text = True
    while True:
        render_simulation(grid, stats, speed, display_end_text, no_solution)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #playing = False
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                #pygame.quit()
                playing = False
                return

def simulate_single_game(input_file, output_file):
    grid, no_solution_due_to_cats = load_map(input_file)
    
    if no_solution_due_to_cats:
        # Display the map with a "No solution found" message
        stats = {
            "algorithm": "Not applicable",
            "steps": 0,
            "total_weight": 0,
            "nodes_generated": 0,
            "time_taken": 0,
            "memory_used": 0,
            "path": "No solution"
        }
        render_simulation(grid, stats, speed=50, display_end_text=True, no_solution=True)
        wait_for_exit()
        return

    # Parse simulation results normally if only one cat is present
    stats = parse_output(output_file)
    simulate(grid, stats["path"], stats)

def wait_for_exit():
    """Waits for user to press ESC to exit after no-solution message."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        pygame.display.flip()