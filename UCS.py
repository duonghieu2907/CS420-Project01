import heapq

class State:
    def __init__(self, ares_pos, stones, cost):
        self.ares_pos = ares_pos  # Ares' current position (x, y)
        self.stones = stones  # Positions of stones in the form of a list of (x, y)
        self.cost = cost  # Cost to reach this state

    def __lt__(self, other):
        return self.cost < other.cost

def parse_input(file_path):
    with open(file_path, 'r') as file:
        weights = list(map(int, file.readline().strip().split()))
        grid = [list(line.strip()) for line in file.readlines()]
    return weights, grid

def find_initial_state(weights, grid):
    ares_pos = None
    stones = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                ares_pos = (i, j)
            elif cell == '$':
                stones.append((i, j))
    return State(ares_pos, stones, 0)

def is_valid_move(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] not in ['#']

def push_stone(ares_pos, stone_pos, grid):
    x, y = stone_pos
    dx, dy = ares_pos[0] - x, ares_pos[1] - y
    new_stone_pos = (x + dx, y + dy)  # Move stone in the same direction Ares is facing
    if is_valid_move(new_stone_pos[0], new_stone_pos[1], grid):
        return new_stone_pos
    return None

def get_successors(state, weights, grid):
    successors = []
    ares_x, ares_y = state.ares_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dx, dy in directions:
        new_ares_pos = (ares_x + dx, ares_y + dy)
        
        # Check for moving Ares
        if is_valid_move(new_ares_pos[0], new_ares_pos[1], grid):
            # Moving without pushing a stone
            successors.append(State(new_ares_pos, state.stones[:], state.cost + 1))
        
        # Check for pushing a stone
        for i, stone_pos in enumerate(state.stones):
            if stone_pos == new_ares_pos:
                stone_pushed = True
                new_stone_pos = push_stone(state.ares_pos, stone_pos, grid)
                if new_stone_pos:
                    # Update stone position
                    new_stones = state.stones[:]
                    new_stones[i] = new_stone_pos
                    # Calculate the cost
                    stone_weight = weights[i]
                    successors.append(State(new_ares_pos, new_stones, state.cost + stone_weight + 1))
        
    return successors

def goal_state(state, grid):
    # Check if all stones are on switches
    stone_positions = set(state.stones)
    for i in range(len(state.stones)):
        x, y = state.stones[i]
        if grid[x][y] != '.':
            return False
    return True

def uniform_cost_search(weights, grid):
    initial_state = find_initial_state(weights, grid)
    priority_queue = []
    heapq.heappush(priority_queue, initial_state)
    visited = set()

    while priority_queue:
        current_state = heapq.heappop(priority_queue)

        if goal_state(current_state, grid):
            return current_state.cost  # Return the cost when all stones are on switches
        
        state_key = (current_state.ares_pos, tuple(current_state.stones))
        if state_key in visited:
            continue
        visited.add(state_key)

        for successor in get_successors(current_state, weights, grid):
            if (successor.ares_pos, tuple(successor.stones)) not in visited:
                heapq.heappush(priority_queue, successor)

    return -1  # If no solution is found

# Example usage
if __name__ == "__main__":
    weights, grid = parse_input('input\input-01.txt')
    print("Weights:", weights)
    print("Grid:")
    for row in grid:
        print(row)
    result = uniform_cost_search(weights, grid)
    print("Minimum cost to push all stones onto switches:", result)
