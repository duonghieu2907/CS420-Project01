import pygame
import os
from ui_utility import screen, IMAGES, FONT, SQUARE_SIZE, BACKGROUND_COLOR, WIDTH, HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT, load_map
from simulate_game import  parse_output, simulate

# Function to render map
def render_map(grid, page_text, additional_text=""):
    screen.fill(BACKGROUND_COLOR)
    
    # Render page indicator
    page_text_rendered = FONT.render(page_text, True, (0, 0, 0))
    screen.blit(page_text_rendered, (WIDTH // 2 - page_text_rendered.get_width() // 2, 10))

    # Render grid
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x, y = j * SQUARE_SIZE, HEADER_HEIGHT + i * SQUARE_SIZE
            screen.blit(IMAGES.get(cell, IMAGES[" "]), (x, y))

    # Render navigation and additional instructions
    instructions = FONT.render("Use LEFT and RIGHT arrow keys to navigate maps.", True, (0, 0, 0))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT + HEADER_HEIGHT + 10))

    # Render "Press Enter"
    if additional_text:
        additional_text_rendered = FONT.render(additional_text, True, (0, 0, 0))
        screen.blit(additional_text_rendered, (WIDTH // 2 - additional_text_rendered.get_width() // 2, HEIGHT + HEADER_HEIGHT - 40))

# Main function for displaying maps with navigation
def map_display():
    input_folder = "../input"
    map_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")])
    playing = True
    if not map_files:
        print("No map files found in the input folder.")
        pygame.quit()
        return

    current_map_idx = 0
    grid, no_solution_due_to_cats = load_map(os.path.join(input_folder, map_files[current_map_idx]), skip_first_line=True)

    while playing:
        # Determine page text
        page_text = f"Map {current_map_idx + 1} {'(end)' if current_map_idx == len(map_files) - 1 else ''}"
        additional_text = "Press Enter to choose this map"

        # Render the map and footer text
        render_map(grid, page_text, additional_text)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                playing = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and current_map_idx < len(map_files) - 1:
                    current_map_idx += 1
                    grid, no_solution_due_to_cats = load_map(os.path.join(input_folder, map_files[current_map_idx]), skip_first_line=True)
                elif event.key == pygame.K_LEFT and current_map_idx > 0:
                    current_map_idx -= 1
                    grid, no_solution_due_to_cats = load_map(os.path.join(input_folder, map_files[current_map_idx]), skip_first_line=True)
                elif event.key == pygame.K_RETURN:  # Start simulation for chosen map
                    output_file = f"../output/output-{current_map_idx + 1:02d}.txt"
                    simulate_single_game(os.path.join(input_folder, map_files[current_map_idx]), output_file, no_solution_due_to_cats, playing)

        pygame.display.flip()
    pygame.quit()
# Function to render the simulation, displaying "No solution found" if needed
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

    # Draw speed bar
    pygame.draw.rect(screen, (200, 200, 200), (20, HEIGHT - 70 + HEADER_HEIGHT, 200, 20))
    pygame.draw.rect(screen, (0, 128, 255), (20, HEIGHT - 70 + HEADER_HEIGHT, int(speed * 2), 20))
    speed_text = FONT.render("Speed:", True, (0, 0, 0))
    screen.blit(speed_text, (20, HEIGHT - 100 + HEADER_HEIGHT))

    # Display stats if applicable
    if display_end_text and not no_solution:
        time_text = FONT.render(f"Time: {stats['time_taken']} seconds", True, (0, 0, 0))
        memory_text = FONT.render(f"Memory: {stats['memory_used']} KB", True, (0, 0, 0))
        screen.blit(time_text, (WIDTH - 300, HEIGHT - 100 + HEADER_HEIGHT))
        screen.blit(memory_text, (WIDTH - 300, HEIGHT - 70 + HEADER_HEIGHT))

    # Display navigation and pause instructions
    pause_text = FONT.render("Press SPACE to pause, SPACE again to continue", True, (0, 0, 0))
    exit_text = FONT.render("Press ESC to exit", True, (0, 0, 0))
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT + HEADER_HEIGHT - 40))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT + HEADER_HEIGHT - 10))

def simulate_single_game(input_file, output_file, no_solution, playing):
    # Load map and check if there's no solution due to incorrect cat count
    grid, _ = load_map(input_file)
    
    if no_solution:
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
        pygame.display.flip()
        wait_for_exit(playing)
        return

    # Parse simulation results normally if there’s only one cat
    stats = parse_output(output_file)
    simulate(grid, stats["path"], stats, playing)

def wait_for_exit(playing):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                playing = False
                print(f"Press esc ")
                #pygame.quit()
                return
        pygame.display.flip()
        
# Run map display
map_display()