import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Knot Menu")

# Colors
BLACK = (0, 0, 30)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)     # Soft Pink
YELLOW = (255, 255, 0)     # Yellow
LIGHT_BLUE = (173, 216, 230)  # Light Blue
ORANGE = (255, 165, 0)     # Orange
PURPLE = (128, 0, 128)     # Purple

# Fonts
FONT_BIG = pygame.font.Font(None, 50)
HEADER_1 = pygame.font.Font(None, 80)
HEADER_2 = pygame.font.Font(None, 60)

# Knot parameters
NUM_NODES = 20
knot_nodes = []
knot_springs = []
dragging_node = None
dragging_offset = (0, 0)

# Galaxy parameters
NUM_STARS = 150
stars = []  # List to store the stars for the galaxy

# Sinusoidal parameters
WAVE_AMPLITUDE = 20
WAVE_FREQUENCY = 0.1
WAVE_SPEED = 0.05
sinusoidal_lines = []

def initialize_knot():
    """Initialize nodes in a circular pattern to create a knot."""
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    radius = 150
    global knot_nodes, knot_springs, dragging_node, dragging_offset, sinusoidal_lines
    dragging_node = None
    dragging_offset = (0, 0)
    knot_nodes = []

    for i in range(NUM_NODES):
        angle = i * (2 * math.pi / NUM_NODES)
        x = center_x + radius * math.cos(angle) + random.uniform(-20, 20)
        y = center_y + radius * math.sin(angle) + random.uniform(-20, 20)
        knot_nodes.append({"x": x, "y": y, "vx": 0, "vy": 0, "ox": x, "oy": y})

    # Define springs as connections between consecutive nodes
    knot_springs = [(i, (i + 1) % NUM_NODES) for i in range(NUM_NODES)]

    # Initialize sinusoidal lines
    sinusoidal_lines = []
    for i in range(len(knot_nodes)):
        start_node = knot_nodes[i]
        end_node = knot_nodes[(i + 1) % len(knot_nodes)]
        sinusoidal_lines.append({
            "start": start_node,
            "end": end_node,
            "offset": random.uniform(0, 2 * math.pi)
        })

    # Initialize galaxy stars
    for _ in range(NUM_STARS):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(50, 250)
        speed = random.uniform(0.01, 0.05)
        stars.append({"x": 0, "y": 0, "angle": angle, "radius": radius, "speed": speed})

def draw_galaxy():
    """Draw a swirling spiral galaxy effect in the background."""
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    for star in stars:
        # Update angle to rotate the galaxy over time
        star["angle"] += star["speed"]
        star["radius"] += 0.2  # Gradually increase the radius for the spiral effect

        # Calculate new x and y positions with increasing radius
        star["x"] = center_x + star["radius"] * math.cos(star["angle"])
        star["y"] = center_y + star["radius"] * math.sin(star["angle"])

        # Check if the star is outside the screen and reset its position if so
        if star["x"] < 0 or star["x"] > SCREEN_WIDTH or star["y"] < 0 or star["y"] > SCREEN_HEIGHT:
            # Reset position if the star is out of bounds
            star["radius"] = random.uniform(50, 250)  # Reset radius to keep it within screen
            star["angle"] = random.uniform(0, 2 * math.pi)  # Random angle to make it look random
            star["x"] = center_x + star["radius"] * math.cos(star["angle"])
            star["y"] = center_y + star["radius"] * math.sin(star["angle"])

        # Draw the star (soft white-blue color)
        pygame.draw.circle(SCREEN, LIGHT_BLUE, (int(star["x"]), int(star["y"])), 2)

def draw_sinusoidal_lines():
    """Draw the sinusoidal lines between nodes."""
    for line in sinusoidal_lines:
        start = line["start"]
        end = line["end"]
        offset = line["offset"]
        color = PURPLE

        # Generate sinusoidal curve between start and end node
        points = []
        for t in range(101):  # 101 points for smooth curve
            x = start["x"] + (end["x"] - start["x"]) * t / 100
            y = start["y"] + (end["y"] - start["y"]) * t / 100
            y += WAVE_AMPLITUDE * math.sin(WAVE_FREQUENCY * t + offset)  # Sinusoidal perturbation
            points.append((x, y))

        # Draw the sinusoidal line
        pygame.draw.aalines(SCREEN, color, False, points)

def draw_knot():
    """Draw the interactive knot with multiple colored springs."""
    for spring in knot_springs:
        node1 = knot_nodes[spring[0]]
        node2 = knot_nodes[spring[1]]

        dx, dy = node2["x"] - node1["x"], node2["y"] - node1["y"]
        dist = math.sqrt(dx**2 + dy**2)

        # Assign different colors based on distance for each spring
        if dist < 50:
            color = PINK
        elif dist < 100:
            color = YELLOW
        elif dist < 150:
            color = LIGHT_BLUE
        else:
            color = ORANGE

        pygame.draw.line(SCREEN, color, (int(node1["x"]), int(node1["y"])),
                         (int(node2["x"]), int(node2["y"])), 3)

    # Draw nodes with white circles
    for node in knot_nodes:
        pygame.draw.circle(SCREEN, WHITE, (int(node["x"]), int(node["y"])), 6)

def update_knot():
    """Update the knot's physics."""
    global dragging_node

    for spring in knot_springs:
        node1 = knot_nodes[spring[0]]
        node2 = knot_nodes[spring[1]]

        dx, dy = node2["x"] - node1["x"], node2["y"] - node1["y"]
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            continue

        force = (dist - 50) * 0.1
        fx, fy = force * dx / dist, force * dy / dist
        node1["vx"] += fx
        node1["vy"] += fy
        node2["vx"] -= fx
        node2["vy"] -= fy

    for node in knot_nodes:
        if node == dragging_node:
            continue

        dx, dy = node["ox"] - node["x"], node["oy"] - node["y"]
        node["vx"] += 0.05 * dx
        node["vy"] += 0.05 * dy

        node["vx"] *= 0.9
        node["vy"] *= 0.9

        node["x"] += node["vx"]
        node["y"] += node["vy"]

    for i, node1 in enumerate(knot_nodes):
        for j, node2 in enumerate(knot_nodes):
            if i != j:
                dx, dy = node2["x"] - node1["x"], node2["y"] - node1["y"]
                dist = math.sqrt(dx**2 + dy**2)
                if dist < 20 and dist > 0:
                    repel_force = (20 - dist) * 0.2
                    fx, fy = repel_force * dx / dist, repel_force * dy / dist
                    node1["vx"] -= fx
                    node1["vy"] -= fy
                    node2["vx"] += fx
                    node2["vy"] += fy

def handle_knot_events():
    """Handle the events for dragging nodes in the knot."""
    global dragging_node, dragging_offset
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for node in knot_nodes:
                if abs(mouse_x - node["x"]) < 10 and abs(mouse_y - node["y"]) < 10:
                    dragging_node = node
                    dragging_offset = (node["x"] - mouse_x, node["y"] - mouse_y)
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_node = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging_node:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dragging_node["x"] = mouse_x + dragging_offset[0]
                dragging_node["y"] = mouse_y + dragging_offset[1]

def main():
    """Main loop for the knot game."""
    initialize_knot()

    while True:
        handle_knot_events()
        SCREEN.fill(BLACK)
        draw_galaxy()
        draw_sinusoidal_lines()
        draw_knot()
        update_knot()
        pygame.display.flip()
        pygame.time.delay(10)

if __name__ == "__main__":
    main()