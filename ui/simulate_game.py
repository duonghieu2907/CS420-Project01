import pyautogui
import pygame
import time
from .ui_utility import *

# Define movement directions for the simulation
directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]

def parse_output(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    try:
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
    except:
        stats = {
            "algorithm": lines[0].strip(),
            "error": lines[1].strip()
        }
        return stats


def find_ares_position(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@' or cell == '+':
                return i, j
    return None

def load_weights(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()
        weights = list(map(int, first_line.split(',')))  # Assuming weights are comma-separated
    return weights

def update_grid(grid, action, weights, total_weight, stone_index_list):
    ares_x, ares_y = find_ares_position(grid)
    for dx, dy, move, push in directions:
        if action == move or action == push:
            new_x, new_y = ares_x + dx, ares_y + dy
            move_cost = 1  # Default move cost for Ares

            # Handle movement actions (lowercase)
            if action.islower() and grid[new_x][new_y] in [' ', '.']:
                grid[new_x][new_y] = '@' if grid[new_x][new_y] == ' ' else '+'
                grid[ares_x][ares_y] = ' ' if grid[ares_x][ares_y] == '@' else '.'
            
            # Handle push actions (uppercase) and update stone positions
            elif action.isupper():
                stone_x, stone_y = new_x + dx, new_y + dy
                stone_index_list[stone_x][stone_y] = stone_index_list[new_x][new_y]
                stone_index_list[new_x][new_y] = None  # no stone at previous place

                if grid[new_x][new_y] in ['$', '*'] and grid[stone_x][stone_y] in [' ', '.']:
                   # stone_index = find_stone_index(grid, new_x, new_y)  # Use the position of the stone being pushed
                    stone_index = stone_index_list[stone_x][stone_y]
                    if stone_index is not None and stone_index < len(weights):  # Check bounds
                        move_cost += weights[stone_index]  # Add the stone's weight to move cost
                    grid[new_x][new_y] = '@' if grid[new_x][new_y] == '$' else '+'
                    grid[ares_x][ares_y] = ' ' if grid[ares_x][ares_y] == '@' else '.'
                    grid[stone_x][stone_y] = '*' if grid[stone_x][stone_y] == '.' else '$'
            
            # Update total weight with the calculated move cost
            total_weight += move_cost
            break
    return total_weight

def find_stone_index(grid, stone_x, stone_y):
    # Find the stone index based on its position
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '$' or cell == '*':
                if (i, j) == (stone_x, stone_y):
                    return len([s for r in grid for s in r if s == '$'])  # Calculate the index based on position
    return None

def render_simulation_controls(stats, speed, step_count, total_weight, paused):
    # Define the control area on the right side of the screen
    controls_rect = pygame.Rect(WIDTH - 260, 20, 250, 420)
    pygame.draw.rect(screen, (200, 200, 200), controls_rect, border_radius=10)

    # Display step and weight information
    step_text = FONT.render(f"Steps: {step_count}", True, (0, 0, 0))
    weight_text = FONT.render(f"Weight: {total_weight}", True, (0, 0, 0))
    speed_text = FONT.render("Speed:", True, (0, 0, 0))

    screen.blit(step_text, (controls_rect.x + 20, controls_rect.y + 20))
    screen.blit(weight_text, (controls_rect.x + 20, controls_rect.y + 60))
    
    # Display speed bar
    pygame.draw.rect(screen, (200, 200, 200), (controls_rect.x + 20, controls_rect.y + 140, 180, 20))
    pygame.draw.rect(screen, (0, 128, 255), (controls_rect.x + 20, controls_rect.y + 140, int(speed * 2), 20))
    screen.blit(speed_text, (controls_rect.x + 20, controls_rect.y + 100))

    # Add instructions for changing speed
    speed_instruction_text_1 = small_font.render("Use LEFT and RIGHT", True, (0, 0, 0))
    speed_instruction_text_2 = small_font.render("keys to change speed", True, (0, 0, 0))

    screen.blit(speed_instruction_text_1, (controls_rect.x + 20, controls_rect.y + 170))
    screen.blit(speed_instruction_text_2, (controls_rect.x + 20, controls_rect.y + 200))

    # Pause/Resume button and Restart button
    pause_button = Button("Pause", (controls_rect.x + 125, controls_rect.y + 280))
    restart_button = Button("Restart", (controls_rect.x + 125, controls_rect.y + 360))

    pause_button.draw(screen, pygame.mouse.get_pos())
    restart_button.draw(screen, pygame.mouse.get_pos())

    return pause_button, restart_button

def simulate(grid, path, stats, playing, original_grid, weights, stone_index_list):
    speed = 50
    step_count = 0
    total_weight = 0  # Initialize total weight count for each move
    paused = False

    no_solution = path == "No solution"
    if no_solution:
        render_simulation(grid, stats, speed, display_end_text=True, no_solution=True)
        return

    action_index = 0  # Track the current action index in the path

    # Main simulation loop
    while action_index < len(path) and playing:
        if not paused:
            # Perform the next action in the path
            action = path[action_index]
            total_weight = update_grid(grid, action, weights, total_weight, stone_index_list)
            step_count += 1
            action_index += 1

            # Render updated grid and controls
            render_simulation(grid, stats, speed)
            pause_button, restart_button = render_simulation_controls(stats, speed, step_count, total_weight, paused)
            pygame.display.flip()
            time.sleep(0.01 * (100 - speed))

        # Event handling for pause, restart, and speed adjustment
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event.pos):
                    paused = not paused  # Toggle paused state
                elif restart_button.is_clicked(event.pos):
                    # Reset grid to original state and restart simulation
                    grid = [row[:] for row in original_grid]  # Deep copy the original grid
                    # Load the index_stone at each cell
                    stone_index_list = [[None for _ in row] for row in grid]
                    stone_index = 0

                    for i in range(len(grid)):
                        for j in range(len(grid[i])):
                            if grid[i][j] == '$' or grid[i][j] == "*":
                                stone_index_list[i][j] = stone_index
                                stone_index += 1
                    step_count = 0
                    total_weight = 0
                    action_index = 0  # Reset action index
                    paused = False  # Ensure simulation restarts in the play state
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speed = max(10, speed - 10)
                elif event.key == pygame.K_RIGHT:
                    speed = min(100, speed + 10)

    # End of simulation: remove pause instructions and display final state
    while playing:
        render_simulation(grid, stats, speed, display_end_text=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
                return

def simulate_single_game(input_file, output_file, weights, no_solution_due_to_cats=False):
    grid, _ = load_map(input_file)

    #Load the index_stone at each cell
    stone_index_list = [[None for _ in row] for row in grid]
    stone_index = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '$' or grid[i][j] == "*":
                stone_index_list[i][j] = stone_index
                stone_index += 1

    original_grid = [row[:] for row in grid]  # Make a deep copy of the original grid for restarting
    
    if no_solution_due_to_cats:
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

    stats = parse_output(output_file)
    if 'error' not in stats:
        simulate(grid, stats["path"], stats, playing=True, original_grid=original_grid, weights=weights, stone_index_list= stone_index_list)
    else:
        print(stats['error'])
        pyautogui.alert(stats['error'])


def wait_for_exit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        pygame.display.flip()