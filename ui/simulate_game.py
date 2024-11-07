import pygame
import time
from .ui_utility import *
from .pause_menu import choose_algorithm_menu

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

def simulate_single_game(input_file, output_file, no_solution_due_to_cats=False):
    # Load map and check if there's no solution due to incorrect cat count
    grid, _ = load_map(input_file)
    
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
    
    # Pass a value (e.g., True) for `playing` to simulate
    simulate(grid, stats["path"], stats, playing=True)

def wait_for_exit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        pygame.display.flip()